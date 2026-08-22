# FILE VERSION: 16_sql_mix_with_native_polars_v1
'''
Mix Polars SQL with native Polars expressions.

This file is intentionally short.

Main ideas:
1. A LazyFrame.sql(...) query returns another LazyFrame, so you can keep chaining
   normal Polars methods such as .with_columns(), .filter(), .select(), .sort(),
   and finally .collect().
2. pl.sql_expr(...) parses SQL expression fragments into normal Polars expressions,
   so you can use SQL-style expressions inside native Polars pipelines.

Use SQL when a query is clearer in SQL.
Use native Polars when method chaining, selectors, or expression APIs are clearer.
You can freely mix both styles in the same workflow.
'''

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(20)
pl.Config.set_tbl_cols(10)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(120)


# =========================================================================================
# 0. Setup data
# =========================================================================================
'''
The examples are self-contained so this file can run without external datasets.

We use a small order table with:
+ ordinary string columns: customer, region, product, status
+ numeric columns: quantity, unit_price, discount_rate
+ one null region to keep the examples realistic
'''

df_orders = pl.DataFrame(
    {
        "order_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
        "customer": ["Alice", "Bob", "Alice", "Diana", "Bob", "Evan", "Alice", "Gina"],
        "region": ["East", "West", "East", "North", "West", "North", "East", None],
        "product": ["Keyboard", "Mouse", "Monitor", "Keyboard", "Mouse", "Monitor", "Mouse", "Desk"],
        "quantity": [2, 1, 1, 3, 4, 2, 5, 2],
        "unit_price": [120.0, 35.0, 250.0, 120.0, 35.0, 250.0, 35.0, 400.0],
        "discount_rate": [0.10, 0.00, 0.15, 0.05, 0.00, 0.20, 0.05, 0.15],
        "status": ["paid", "pending", "paid", "paid", "paid", "paid", "cancelled", "paid"],
    }
)

lf_orders = df_orders.lazy()

print(df_orders)
# shape: (8, 8)
# ┌──────────┬──────────┬────────┬──────────┬──────────┬────────────┬───────────────┬───────────┐
# │ order_id ┆ customer ┆ region ┆ product  ┆ quantity ┆ unit_price ┆ discount_rate ┆ status    │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---      ┆ ---        ┆ ---           ┆ ---       │
# │ i64      ┆ str      ┆ str    ┆ str      ┆ i64      ┆ f64        ┆ f64           ┆ str       │
# ╞══════════╪══════════╪════════╪══════════╪══════════╪════════════╪═══════════════╪═══════════╡
# │ 1001     ┆ Alice    ┆ East   ┆ Keyboard ┆ 2        ┆ 120.000    ┆ 0.100         ┆ paid      │
# │ 1002     ┆ Bob      ┆ West   ┆ Mouse    ┆ 1        ┆ 35.000     ┆ 0.000         ┆ pending   │
# │ 1003     ┆ Alice    ┆ East   ┆ Monitor  ┆ 1        ┆ 250.000    ┆ 0.150         ┆ paid      │
# │ 1004     ┆ Diana    ┆ North  ┆ Keyboard ┆ 3        ┆ 120.000    ┆ 0.050         ┆ paid      │
# │ 1005     ┆ Bob      ┆ West   ┆ Mouse    ┆ 4        ┆ 35.000     ┆ 0.000         ┆ paid      │
# │ 1006     ┆ Evan     ┆ North  ┆ Monitor  ┆ 2        ┆ 250.000    ┆ 0.200         ┆ paid      │
# │ 1007     ┆ Alice    ┆ East   ┆ Mouse    ┆ 5        ┆ 35.000     ┆ 0.050         ┆ cancelled │
# │ 1008     ┆ Gina     ┆ null   ┆ Desk     ┆ 2        ┆ 400.000    ┆ 0.150         ┆ paid      │
# └──────────┴──────────┴────────┴──────────┴──────────┴────────────┴───────────────┴───────────┘


# =========================================================================================
# 1. SQL first, then continue with native Polars
# =========================================================================================
'''
Frame-level .sql(...) registers the current frame as the table named self.

Because lf_orders is a LazyFrame, lf_orders.sql(...) returns another LazyFrame.
That means we can continue the pipeline with native Polars methods.

Workflow:
1. Use SQL for the initial SELECT / WHERE.
2. Use native .with_columns() to add more derived columns.
3. Use native .filter(), .select(), .sort(), and .collect().
'''

out_mixed = (
    lf_orders
    .sql(
        """
        SELECT
            order_id,
            customer,
            region,
            product,
            quantity,
            unit_price,
            quantity * unit_price AS gross_amount,
            status
        FROM self
        WHERE status = 'paid'
        """
    )
    .with_columns(
        (c("gross_amount") >= 250).alias("large_paid_order"),
        c("region").fill_null("Unknown").alias("region"),
    )
    .filter(c("large_paid_order"))
    .select(
        "order_id",
        "customer",
        "region",
        "product",
        "gross_amount",
        "large_paid_order",
    )
    .sort("gross_amount", descending=True)
)
print(out_mixed.collect())
# shape: (4, 6)
# ┌──────────┬──────────┬─────────┬──────────┬──────────────┬──────────────────┐
# │ order_id ┆ customer ┆ region  ┆ product  ┆ gross_amount ┆ large_paid_order │
# │ ---      ┆ ---      ┆ ---     ┆ ---      ┆ ---          ┆ ---              │
# │ i64      ┆ str      ┆ str     ┆ str      ┆ f64          ┆ bool             │
# ╞══════════╪══════════╪═════════╪══════════╪══════════════╪══════════════════╡
# │ 1008     ┆ Gina     ┆ Unknown ┆ Desk     ┆ 800.000      ┆ true             │
# │ 1006     ┆ Evan     ┆ North   ┆ Monitor  ┆ 500.000      ┆ true             │
# │ 1004     ┆ Diana    ┆ North   ┆ Keyboard ┆ 360.000      ┆ true             │
# │ 1003     ┆ Alice    ┆ East    ┆ Monitor  ┆ 250.000      ┆ true             │
# └──────────┴──────────┴─────────┴──────────┴──────────────┴──────────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .filter(c("status") == "paid")
    .select(
        "order_id",
        "customer",
        "region",
        "product",
        "quantity",
        "unit_price",
        (c("quantity") * c("unit_price")).alias("gross_amount"),
        "status",
    )
    .with_columns(
        (c("gross_amount") >= 250).alias("large_paid_order"),
        c("region").fill_null("Unknown").alias("region"),
    )
    .filter(c("large_paid_order"))
    .select(
        "order_id",
        "customer",
        "region",
        "product",
        "gross_amount",
        "large_paid_order",
    )
    .sort("gross_amount", descending=True)
)
print(out_native.collect())


# =========================================================================================
# 2. Native pipeline with SQL expression fragments
# =========================================================================================
'''
pl.sql_expr(...) converts SQL expression strings into normal Polars expressions.

This is useful when:
+ most of the pipeline is clearer in native Polars
+ but one or two expressions are easier to write in SQL syntax

Important:
    pl.sql_expr(...) is for expression fragments, not full SELECT queries.
'''

out_mixed_expr = (
    lf_orders
    .with_columns(
        pl.sql_expr(
            [
                "quantity * unit_price AS gross_amount",
                "quantity * unit_price * discount_rate AS discount_amount",
                "CASE WHEN status = 'paid' THEN true ELSE false END AS is_paid",
            ]
        )
    )
    .with_columns(
        pl.sql_expr("gross_amount - discount_amount AS net_amount")
    )
    .filter(c("is_paid"))
    .group_by("region")
    .agg(
        pl.len().alias("n_paid_orders"),
        c("net_amount").sum().alias("net_sales"),
        pl.sql_expr("AVG(net_amount) AS avg_net_order"),
    )
    .with_columns(c("region").fill_null("Unknown"))
    .sort("net_sales", descending=True)
)
print(out_mixed_expr.collect())
# shape: (4, 4)
# ┌─────────┬───────────────┬───────────┬───────────────┐
# │ region  ┆ n_paid_orders ┆ net_sales ┆ avg_net_order │
# │ ---     ┆ ---           ┆ ---       ┆ ---           │
# │ str     ┆ u32           ┆ f64       ┆ f64           │
# ╞═════════╪═══════════════╪═══════════╪═══════════════╡
# │ North   ┆ 2             ┆ 742.000   ┆ 371.000       │
# │ Unknown ┆ 1             ┆ 680.000   ┆ 680.000       │
# │ East    ┆ 2             ┆ 428.500   ┆ 214.250       │
# │ West    ┆ 1             ┆ 140.000   ┆ 140.000       │
# └─────────┴───────────────┴───────────┴───────────────┘

# Native Polars equivalent.
out_native_expr = (
    lf_orders
    .with_columns(
        (c("quantity") * c("unit_price")).alias("gross_amount"),
        (c("quantity") * c("unit_price") * c("discount_rate")).alias("discount_amount"),
        (c("status") == "paid").alias("is_paid"),
    )
    .with_columns(
        (c("gross_amount") - c("discount_amount")).alias("net_amount")
    )
    .filter(c("is_paid"))
    .group_by("region")
    .agg(
        pl.len().alias("n_paid_orders"),
        c("net_amount").sum().alias("net_sales"),
        c("net_amount").mean().alias("avg_net_order"),
    )
    .with_columns(c("region").fill_null("Unknown"))
    .sort("net_sales", descending=True)
)
print(out_native_expr.collect())


# =========================================================================================
# 3. Quick summary
# =========================================================================================
'''
Quick mental map:

1. SQL query inside a lazy pipeline

    lf.sql("""
        SELECT ...
        FROM self
        WHERE ...
    """).with_columns(...).filter(...).collect()

2. SQL expression inside a native Polars pipeline

    lf.with_columns(
        pl.sql_expr("quantity * unit_price AS gross_amount")
    ).filter(...).collect()

Use full .sql(...) for table-shaped SQL queries.
Use pl.sql_expr(...) for column/expression-shaped SQL snippets.
'''
