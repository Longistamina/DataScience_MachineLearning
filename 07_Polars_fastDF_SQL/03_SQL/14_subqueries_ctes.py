'''
Polars SQL subqueries, inline views, and WITH common table expressions (CTEs).

Main ideas:
1. A subquery is a SELECT query nested inside another query.
2. An inline view, also called a derived table, is a subquery placed in FROM.
3. WITH common table expressions give names to intermediate query results.
4. CTEs are usually easier to read than deeply nested inline subqueries.
5. Inline views and CTEs are temporary query objects, not permanent Polars tables.
6. In Polars SQL, these queries still build lazy Polars query plans.

Important Polars SQL notes:
+ Frame-level .sql(...) registers the frame as the SQL table named self.
+ LazyFrame.sql(...) returns a LazyFrame, so call .collect() to materialize it.
+ SQLContext is useful when a query needs multiple named tables.
+ The most reliable subquery patterns are:
    - subqueries in FROM
    - subqueries joined as derived tables
    - WITH CTEs
+ Predicate subqueries such as IN (SELECT ...) and scalar subqueries are useful,
  but support can depend on the Polars version. This file shows safe rewrites
  with CTEs and joins when appropriate.
+ CTEs are scoped to a single SQL statement. After the query finishes, the CTE
  name is not registered as a SQLContext table.
'''

import datetime as dt

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(5)
pl.Config.set_tbl_cols(10)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(120)


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 0. Setup data ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The examples are self-contained so this file can run without external datasets.

We create:
+ orders: transaction-level data
+ customers: customer-level lookup data
+ regional_targets: region-level lookup data

The orders table has enough columns to demonstrate:
+ filtering before/after aggregation
+ inline views in FROM
+ joining to derived tables
+ CTE pipelines
+ rewrites for IN/scalar-subquery style logic
'''

df_orders = pl.DataFrame(
    {
        "order_id": [
            1001, 1002, 1003, 1004, 1005,
            1006, 1007, 1008, 1009, 1010,
            1011, 1012, 1013, 1014, 1015,
        ],
        "customer_id": [
            1, 2, 1, 3, 2,
            4, 1, 3, 5, 2,
            4, 1, 5, 6, 7,
        ],
        "customer": [
            "Alice", "Bob", "Alice", "Diana", "Bob",
            "Evan", "Alice", "Diana", "Fiona", "Bob",
            "Evan", "Alice", "Fiona", "Gina", "Henry",
        ],
        "region": [
            "East", "West", "East", "North", "West",
            "North", "East", "North", "South", "West",
            "North", "East", "South", None, "East",
        ],
        "product": [
            "Keyboard", "Mouse", "Monitor", "Keyboard", "Mouse",
            "Monitor", "Mouse", "Desk", "Desk", "Keyboard",
            "Mouse", "Keyboard", "Monitor", "Desk", "Mouse",
        ],
        "quantity": [2, 1, 1, 3, 4, 2, 5, 1, 2, 1, 3, 1, 1, 2, 6],
        "unit_price": [
            120.0, 35.0, 250.0, 120.0, 35.0,
            250.0, 35.0, 400.0, 400.0, 120.0,
            35.0, 120.0, 250.0, 400.0, 35.0,
        ],
        "discount_rate": [
            0.10, 0.00, 0.15, 0.05, 0.00,
            0.20, 0.05, 0.10, 0.25, 0.00,
            0.00, 0.50, 0.10, 0.15, 0.00,
        ],
        "shipping_fee": [5.0, 4.0, 8.0, 7.5, 4.0, 10.0, 4.0, 12.0, 12.0, 5.0, 4.0, 5.0, 8.0, 12.0, 4.0],
        "status": [
            "paid", "pending", "paid", "paid", "paid",
            "paid", "cancelled", "paid", "paid", "pending",
            "paid", "paid", "refunded", "paid", "paid",
        ],
        "priority": [True, False, True, False, False, True, False, True, False, False, False, True, False, True, False],
        "order_date": [
            dt.date(2024, 1, 3),
            dt.date(2024, 1, 5),
            dt.date(2024, 2, 10),
            dt.date(2024, 2, 12),
            dt.date(2024, 3, 1),
            dt.date(2024, 3, 15),
            dt.date(2024, 3, 20),
            dt.date(2024, 4, 4),
            dt.date(2024, 4, 10),
            dt.date(2024, 4, 12),
            dt.date(2024, 5, 1),
            dt.date(2024, 5, 15),
            dt.date(2024, 5, 20),
            dt.date(2024, 6, 3),
            dt.date(2024, 6, 8),
        ],
    }
)

# Add derived numeric columns using native Polars once.
df_orders = (
    df_orders
    .with_columns(
        (c("quantity") * c("unit_price")).alias("gross_amount")
    )
    .with_columns(
        (c("gross_amount") * c("discount_rate")).alias("discount_amount")
    )
    .with_columns(
        (c("gross_amount") - c("discount_amount")).alias("net_amount")
    )
    .with_columns(
        (c("net_amount") + c("shipping_fee")).alias("total_amount")
    )
)

lf_orders = df_orders.lazy()

# Customer lookup table.
df_customers = pl.DataFrame(
    {
        "customer_id": [1, 2, 3, 4, 5, 6, 7, 8],
        "customer_name": ["Alice", "Bob", "Diana", "Evan", "Fiona", "Gina", "Henry", "Ivy"],
        "segment": ["VIP", "Standard", "VIP", "Standard", "Standard", "VIP", "Standard", "VIP"],
        "signup_year": [2021, 2023, 2020, 2022, 2023, 2021, 2024, 2024],
    }
)

lf_customers = df_customers.lazy()

# Region lookup table.
df_regional_targets = pl.DataFrame(
    {
        "region": ["East", "North", "South", "West"],
        "sales_target": [800.0, 1100.0, 900.0, 500.0],
    }
)

lf_regional_targets = df_regional_targets.lazy()

# SQLContext for examples that need more than one table.
ctx = pl.SQLContext(
    orders=lf_orders,
    customers=lf_customers,
    regional_targets=lf_regional_targets,
)

print(df_orders)
# shape: (15, 16)
# ┌──────────┬────────────┬──────────┬────────┬──────────┬───┬───────────┬───────────┬───────────┬───────────┬───────────┐
# │ order_id ┆ customer_i ┆ customer ┆ region ┆ product  ┆ … ┆ order_dat ┆ gross_amo ┆ discount_ ┆ net_amoun ┆ total_amo │
# │ ---      ┆ d          ┆ ---      ┆ ---    ┆ ---      ┆   ┆ e         ┆ unt       ┆ amount    ┆ t         ┆ unt       │
# │ i64      ┆ ---        ┆ str      ┆ str    ┆ str      ┆   ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       │
# │          ┆ i64        ┆          ┆        ┆          ┆   ┆ date      ┆ f64       ┆ f64       ┆ f64       ┆ f64       │
# ╞══════════╪════════════╪══════════╪════════╪══════════╪═══╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╡
# │ 1001     ┆ 1          ┆ Alice    ┆ East   ┆ Keyboard ┆ … ┆ 2024-01-0 ┆ 240.000   ┆ 24.000    ┆ 216.000   ┆ 221.000   │
# │          ┆            ┆          ┆        ┆          ┆   ┆ 3         ┆           ┆           ┆           ┆           │
# │ 1002     ┆ 2          ┆ Bob      ┆ West   ┆ Mouse    ┆ … ┆ 2024-01-0 ┆ 35.000    ┆ 0.000     ┆ 35.000    ┆ 39.000    │
# │          ┆            ┆          ┆        ┆          ┆   ┆ 5         ┆           ┆           ┆           ┆           │
# │ 1003     ┆ 1          ┆ Alice    ┆ East   ┆ Monitor  ┆ … ┆ 2024-02-1 ┆ 250.000   ┆ 37.500    ┆ 212.500   ┆ 220.500   │
# │          ┆            ┆          ┆        ┆          ┆   ┆ 0         ┆           ┆           ┆           ┆           │
# │ …        ┆ …          ┆ …        ┆ …      ┆ …        ┆ … ┆ …         ┆ …         ┆ …         ┆ …         ┆ …         │
# │ 1014     ┆ 6          ┆ Gina     ┆ null   ┆ Desk     ┆ … ┆ 2024-06-0 ┆ 800.000   ┆ 120.000   ┆ 680.000   ┆ 692.000   │
# │          ┆            ┆          ┆        ┆          ┆   ┆ 3         ┆           ┆           ┆           ┆           │
# │ 1015     ┆ 7          ┆ Henry    ┆ East   ┆ Mouse    ┆ … ┆ 2024-06-0 ┆ 210.000   ┆ 0.000     ┆ 210.000   ┆ 214.000   │
# │          ┆            ┆          ┆        ┆          ┆   ┆ 8         ┆           ┆           ┆           ┆           │
# └──────────┴────────────┴──────────┴────────┴──────────┴───┴───────────┴───────────┴───────────┴───────────┴───────────┘

print(df_customers)
# shape: (8, 4)
# ┌─────────────┬───────────────┬──────────┬─────────────┐
# │ customer_id ┆ customer_name ┆ segment  ┆ signup_year │
# │ ---         ┆ ---           ┆ ---      ┆ ---         │
# │ i64         ┆ str           ┆ str      ┆ i64         │
# ╞═════════════╪═══════════════╪══════════╪═════════════╡
# │ 1           ┆ Alice         ┆ VIP      ┆ 2021        │
# │ 2           ┆ Bob           ┆ Standard ┆ 2023        │
# │ 3           ┆ Diana         ┆ VIP      ┆ 2020        │
# │ …           ┆ …             ┆ …        ┆ …           │
# │ 7           ┆ Henry         ┆ Standard ┆ 2024        │
# │ 8           ┆ Ivy           ┆ VIP      ┆ 2024        │
# └─────────────┴───────────────┴──────────┴─────────────┘

print(df_regional_targets)
# shape: (4, 2)
# ┌────────┬──────────────┐
# │ region ┆ sales_target │
# │ ---    ┆ ---          │
# │ str    ┆ f64          │
# ╞════════╪══════════════╡
# │ East   ┆ 800.000      │
# │ North  ┆ 1100.000     │
# │ South  ┆ 900.000      │
# │ West   ┆ 500.000      │
# └────────┴──────────────┘


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 1. Inline view: subquery in FROM ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
An inline view is a SELECT query inside FROM.

Pattern:
    SELECT ...
    FROM (
        SELECT ...
        FROM ...
    ) AS alias

The alias is important because the outer query needs a table name for the
subquery result.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        customer,
        total_sales
    FROM (
        SELECT
            customer,
            SUM(total_amount) AS total_sales
        FROM self
        GROUP BY customer
    ) AS customer_sales
    WHERE total_sales >= 300
    ORDER BY total_sales DESC
    """
)
print(out_sql.collect())
# shape: (6, 2)
# ┌──────────┬─────────────┐
# │ customer ┆ total_sales │
# │ ---      ┆ ---         │
# │ str      ┆ f64         │
# ╞══════════╪═════════════╡
# │ Fiona    ┆ 845.000     │
# │ Diana    ┆ 721.500     │
# │ Gina     ┆ 692.000     │
# │ …        ┆ …           │
# │ Evan     ┆ 519.000     │
# │ Bob      ┆ 308.000     │
# └──────────┴─────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .group_by("customer")
    .agg(c("total_amount").sum().alias("total_sales"))
    .filter(c("total_sales") >= 300)
    .sort("total_sales", descending=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------- 2. Inline view: filter inside, aggregate outside -------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A subquery can prepare rows before the outer query aggregates them.

Here the inner query keeps only paid orders. The outer query then groups those
already-filtered rows by product.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        product,
        COUNT(*) AS n_paid_orders,
        SUM(total_amount) AS paid_sales
    FROM (
        SELECT
            product,
            total_amount
        FROM self
        WHERE status = 'paid'
    ) AS paid_orders
    GROUP BY product
    ORDER BY paid_sales DESC
    """
)
print(out_sql.collect())
# shape: (4, 3)
# ┌──────────┬───────────────┬────────────┐
# │ product  ┆ n_paid_orders ┆ paid_sales │
# │ ---      ┆ ---           ┆ ---        │
# │ str      ┆ u32           ┆ f64        │
# ╞══════════╪═══════════════╪════════════╡
# │ Desk     ┆ 3             ┆ 1676.000   │
# │ Keyboard ┆ 3             ┆ 635.500    │
# │ Monitor  ┆ 2             ┆ 630.500    │
# │ Mouse    ┆ 3             ┆ 467.000    │
# └──────────┴───────────────┴────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .filter(c("status") == "paid")
    .select("product", "total_amount")
    .group_by("product")
    .agg(
        pl.len().alias("n_paid_orders"),
        c("total_amount").sum().alias("paid_sales"),
    )
    .sort("paid_sales", descending=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------- 3. Inline view: calculate, then filter on alias ------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
SQL usually does not let WHERE use a SELECT alias from the same query level.

Instead, compute the alias inside a subquery, then filter on it in the outer query.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        customer,
        product,
        effective_discount_rate
    FROM (
        SELECT
            order_id,
            customer,
            product,
            discount_amount / gross_amount AS effective_discount_rate
        FROM self
        WHERE gross_amount > 0
    ) AS discounts
    WHERE effective_discount_rate >= 0.15
    ORDER BY effective_discount_rate DESC, order_id
    """
)
print(out_sql.collect())
# shape: (5, 4)
# ┌──────────┬──────────┬──────────┬─────────────────────────┐
# │ order_id ┆ customer ┆ product  ┆ effective_discount_rate │
# │ ---      ┆ ---      ┆ ---      ┆ ---                     │
# │ i64      ┆ str      ┆ str      ┆ f64                     │
# ╞══════════╪══════════╪══════════╪═════════════════════════╡
# │ 1012     ┆ Alice    ┆ Keyboard ┆ 0.500                   │
# │ 1009     ┆ Fiona    ┆ Desk     ┆ 0.250                   │
# │ 1006     ┆ Evan     ┆ Monitor  ┆ 0.200                   │
# │ 1003     ┆ Alice    ┆ Monitor  ┆ 0.150                   │
# │ 1014     ┆ Gina     ┆ Desk     ┆ 0.150                   │
# └──────────┴──────────┴──────────┴─────────────────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .filter(c("gross_amount") > 0)
    .select(
        "order_id",
        "customer",
        "product",
        (c("discount_amount") / c("gross_amount")).alias("effective_discount_rate"),
    )
    .filter(c("effective_discount_rate") >= 0.15)
    .sort(["effective_discount_rate", "order_id"], descending=[True, False])
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------- 4. Join to a derived table ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A subquery in FROM can also be joined like a normal table.

This example joins every order to a per-customer spending summary.
'''

out_sql = ctx.execute(
    """
    SELECT
        o.order_id,
        o.customer,
        o.total_amount,
        s.customer_total_sales,
        s.n_orders_by_customer
    FROM orders AS o
    INNER JOIN (
        SELECT
            customer_id,
            SUM(total_amount) AS customer_total_sales,
            COUNT(*) AS n_orders_by_customer
        FROM orders
        GROUP BY customer_id
    ) AS s
        ON o.customer_id = s.customer_id
    ORDER BY o.order_id
    """
)
print(out_sql.collect())
# shape: (15, 5)
# ┌──────────┬──────────┬──────────────┬──────────────────────┬──────────────────────┐
# │ order_id ┆ customer ┆ total_amount ┆ customer_total_sales ┆ n_orders_by_customer │
# │ ---      ┆ ---      ┆ ---          ┆ ---                  ┆ ---                  │
# │ i64      ┆ str      ┆ f64          ┆ f64                  ┆ u32                  │
# ╞══════════╪══════════╪══════════════╪══════════════════════╪══════════════════════╡
# │ 1001     ┆ Alice    ┆ 221.000      ┆ 676.750              ┆ 4                    │
# │ 1002     ┆ Bob      ┆ 39.000       ┆ 308.000              ┆ 3                    │
# │ 1003     ┆ Alice    ┆ 220.500      ┆ 676.750              ┆ 4                    │
# │ …        ┆ …        ┆ …            ┆ …                    ┆ …                    │
# │ 1014     ┆ Gina     ┆ 692.000      ┆ 692.000              ┆ 1                    │
# │ 1015     ┆ Henry    ┆ 214.000      ┆ 214.000              ┆ 1                    │
# └──────────┴──────────┴──────────────┴──────────────────────┴──────────────────────┘

# Native Polars equivalent.
customer_summary = (
    lf_orders
    .group_by("customer_id")
    .agg(
        c("total_amount").sum().alias("customer_total_sales"),
        pl.len().alias("n_orders_by_customer"),
    )
)
out_native = (
    lf_orders
    .join(customer_summary, on="customer_id", how="inner")
    .select(
        "order_id",
        "customer",
        "total_amount",
        "customer_total_sales",
        "n_orders_by_customer",
    )
    .sort("order_id")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 5. Basic WITH CTE ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A CTE names an intermediate query result.

Pattern:
    WITH cte_name AS (
        SELECT ...
    )
    SELECT ...
    FROM cte_name

The CTE only exists inside that one SQL statement.
'''

out_sql = ctx.execute(
    """
    WITH paid_orders AS (
        SELECT
            order_id,
            customer,
            product,
            total_amount
        FROM orders
        WHERE status = 'paid'
    )
    SELECT
        customer,
        COUNT(*) AS n_paid_orders,
        SUM(total_amount) AS paid_sales
    FROM paid_orders
    GROUP BY customer
    ORDER BY paid_sales DESC
    """
)
print(out_sql.collect())
# shape: (7, 3)
# ┌──────────┬───────────────┬────────────┐
# │ customer ┆ n_paid_orders ┆ paid_sales │
# │ ---      ┆ ---           ┆ ---        │
# │ str      ┆ u32           ┆ f64        │
# ╞══════════╪═══════════════╪════════════╡
# │ Diana    ┆ 2             ┆ 721.500    │
# │ Gina     ┆ 1             ┆ 692.000    │
# │ Fiona    ┆ 1             ┆ 612.000    │
# │ …        ┆ …             ┆ …          │
# │ Henry    ┆ 1             ┆ 214.000    │
# │ Bob      ┆ 1             ┆ 144.000    │
# └──────────┴───────────────┴────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .filter(c("status") == "paid")
    .select("order_id", "customer", "product", "total_amount")
    .group_by("customer")
    .agg(
        pl.len().alias("n_paid_orders"),
        c("total_amount").sum().alias("paid_sales"),
    )
    .sort("paid_sales", descending=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 6. Multiple CTEs in one WITH ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A WITH block can define more than one CTE.

This is useful when you want to break a query into named steps.

Important practical note:
When chaining CTEs in Polars SQL, avoid SELECT * if the later query joins
against another table with overlapping column names.

Instead:
+ select only the columns you need
+ rename join keys early
+ keep the final join key unambiguous
'''

# out_sql = ctx.execute(
#     """
#     WITH
#     paid_order_rows AS (
#         SELECT
#             order_id AS paid_order_id,
#             customer_id AS paid_customer_id,
#             total_amount AS paid_total_amount
#         FROM orders
#         WHERE status = 'paid'
#     ),
#     customer_sales AS (
#         SELECT
#             paid_customer_id,
#             COUNT(*) AS n_paid_orders,
#             SUM(paid_total_amount) AS paid_sales
#         FROM paid_order_rows
#         GROUP BY paid_customer_id
#     )
#     SELECT
#         c.customer_name,
#         c.segment,
#         n_paid_orders,
#         paid_sales
#     FROM customer_sales
#     INNER JOIN customers AS c
#         ON paid_customer_id = c.customer_id
#     ORDER BY paid_sales DESC
#     """
# )
# print(out_sql.collect())

# out_native = (
#     lf_orders
#     .filter(c("status") == "paid")
#     .select(
#         c("order_id").alias("paid_order_id"),
#         c("customer_id").alias("paid_customer_id"),
#         c("total_amount").alias("paid_total_amount"),
#     )
#     .group_by("paid_customer_id")
#     .agg(
#         pl.len().alias("n_paid_orders"),
#         c("paid_total_amount").sum().alias("paid_sales"),
#     )
#     .join(
#         lf_customers,
#         left_on="paid_customer_id",
#         right_on="customer_id",
#         how="inner",
#     )
#     .select(
#         "customer_name",
#         "segment",
#         "n_paid_orders",
#         "paid_sales",
#     )
#     .sort("paid_sales", descending=True)
# )
# print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 7. Chained CTE pipeline ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A later CTE can refer to an earlier CTE in the same WITH block.

This creates a readable pipeline:
1. paid_orders
2. region_sales
3. region_performance
4. final SELECT
'''

# out_sql = ctx.execute(
#     """
#     WITH
#     paid_orders AS (
#         SELECT
#             region,
#             total_amount
#         FROM orders
#         WHERE status = 'paid' AND region IS NOT NULL
#     ),
#     region_sales AS (
#         SELECT
#             region,
#             COUNT(*) AS n_paid_orders,
#             SUM(total_amount) AS paid_sales
#         FROM paid_orders
#         GROUP BY region
#     ),
#     region_performance AS (
#         SELECT
#             s.region,
#             s.n_paid_orders,
#             s.paid_sales,
#             t.sales_target,
#             s.paid_sales - t.sales_target AS sales_gap
#         FROM region_sales AS s
#         INNER JOIN regional_targets AS t
#             ON s.region = t.region
#     )
#     SELECT
#         region,
#         n_paid_orders,
#         paid_sales,
#         sales_target,
#         sales_gap
#     FROM region_performance
#     ORDER BY sales_gap DESC
#     """
# )
# print(out_sql.collect())

# Native Polars equivalent.
# paid_orders = (
#     lf_orders
#     .filter((c("status") == "paid") & c("region").is_not_null())
#     .select("region", "total_amount")
# )
# region_sales = (
#     paid_orders
#     .group_by("region")
#     .agg(
#         pl.len().alias("n_paid_orders"),
#         c("total_amount").sum().alias("paid_sales"),
#     )
# )
# region_performance = (
#     region_sales
#     .join(lf_regional_targets, on="region", how="inner")
#     .with_columns(
#         (c("paid_sales") - c("sales_target")).alias("sales_gap")
#     )
# )
# out_native = region_performance.select(
#     "region",
#     "n_paid_orders",
#     "paid_sales",
#     "sales_target",
#     "sales_gap",
# ).sort("sales_gap", descending=True)
# print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------- 8. CTE equivalent of a repeated inline view ------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Inline subqueries can become hard to read when they are repeated or nested.
CTEs make the same logic easier to name and reuse in the query.

This query finds each paid order for customers whose paid sales are at least 300.
'''

# out_sql = ctx.execute(
#     """
#     WITH high_value_customers AS (
#         SELECT
#             customer_id,
#             SUM(total_amount) AS paid_sales
#         FROM orders
#         WHERE status = 'paid'
#         GROUP BY customer_id
#         HAVING SUM(total_amount) >= 300
#     )
#     SELECT
#         o.order_id,
#         o.customer,
#         o.product,
#         o.total_amount,
#         h.paid_sales
#     FROM orders AS o
#     INNER JOIN high_value_customers AS h
#         ON o.customer_id = h.customer_id
#     WHERE o.status = 'paid'
#     ORDER BY h.paid_sales DESC, o.order_id
#     """
# )
# print(out_sql.collect())

# Native Polars equivalent.
high_value_customers = (
    lf_orders
    .filter(c("status") == "paid")
    .group_by("customer_id")
    .agg(c("total_amount").sum().alias("paid_sales"))
    .filter(c("paid_sales") >= 300)
)
out_native = (
    lf_orders
    .join(high_value_customers, on="customer_id", how="inner")
    .filter(c("status") == "paid")
    .select("order_id", "customer", "product", "total_amount", "paid_sales")
    .sort(["paid_sales", "order_id"], descending=[True, False])
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 9. CTEs with LEFT JOIN lookup tables -------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
CTEs are often used to build a clean analysis table before joining lookup tables.

Here we build paid customer sales, then left-join the full customers table. The
left join keeps customers that have no paid orders, such as Ivy.
'''

# out_sql = ctx.execute(
#     """
#     WITH paid_customer_sales AS (
#         SELECT
#             customer_id,
#             COUNT(*) AS n_paid_orders,
#             SUM(total_amount) AS paid_sales
#         FROM orders
#         WHERE status = 'paid'
#         GROUP BY customer_id
#     )
#     SELECT
#         c.customer_id,
#         c.customer_name,
#         c.segment,
#         COALESCE(s.n_paid_orders, 0) AS n_paid_orders,
#         COALESCE(s.paid_sales, 0.0) AS paid_sales
#     FROM customers AS c
#     LEFT JOIN paid_customer_sales AS s
#         ON c.customer_id = s.customer_id
#     ORDER BY c.customer_id
#     """
# )
# print(out_sql.collect())

# Native Polars equivalent.
paid_customer_sales = (
    lf_orders
    .filter(c("status") == "paid")
    .group_by("customer_id")
    .agg(
        pl.len().alias("n_paid_orders"),
        c("total_amount").sum().alias("paid_sales"),
    )
)
out_native = (
    lf_customers
    .join(paid_customer_sales, on="customer_id", how="left")
    .with_columns(
        c("n_paid_orders").fill_null(0),
        c("paid_sales").fill_null(0.0),
    )
    .select("customer_id", "customer_name", "segment", "n_paid_orders", "paid_sales")
    .sort("customer_id")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 10. Scalar-subquery idea: use a CTE rewrite --------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
In many SQL dialects, you may write:

    WHERE total_amount > (SELECT AVG(total_amount) FROM orders)

If that scalar-subquery pattern is not supported by your Polars version, rewrite
it as a one-row CTE and CROSS JOIN it into the query.

The CTE rewrite is explicit and works well in Polars SQL.
'''

out_sql = ctx.execute(
    """
    WITH avg_order AS (
        SELECT AVG(total_amount) AS avg_total_amount
        FROM orders
    )
    SELECT
        o.order_id,
        o.customer,
        o.product,
        o.total_amount,
        a.avg_total_amount
    FROM orders AS o
    CROSS JOIN avg_order AS a
    WHERE o.total_amount > a.avg_total_amount
    ORDER BY o.total_amount DESC
    """
)
print(out_sql.collect())
# shape: (5, 5)
# ┌──────────┬──────────┬──────────┬──────────────┬──────────────────┐
# │ order_id ┆ customer ┆ product  ┆ total_amount ┆ avg_total_amount │
# │ ---      ┆ ---      ┆ ---      ┆ ---          ┆ ---              │
# │ i64      ┆ str      ┆ str      ┆ f64          ┆ f64              │
# ╞══════════╪══════════╪══════════╪══════════════╪══════════════════╡
# │ 1014     ┆ Gina     ┆ Desk     ┆ 692.000      ┆ 265.083          │
# │ 1009     ┆ Fiona    ┆ Desk     ┆ 612.000      ┆ 265.083          │
# │ 1006     ┆ Evan     ┆ Monitor  ┆ 410.000      ┆ 265.083          │
# │ 1008     ┆ Diana    ┆ Desk     ┆ 372.000      ┆ 265.083          │
# │ 1004     ┆ Diana    ┆ Keyboard ┆ 349.500      ┆ 265.083          │
# └──────────┴──────────┴──────────┴──────────────┴──────────────────┘

# Native Polars equivalent.
avg_order = lf_orders.select(c("total_amount").mean().alias("avg_total_amount"))
out_native = (
    lf_orders
    .join(avg_order, how="cross")
    .filter(c("total_amount") > c("avg_total_amount"))
    .select("order_id", "customer", "product", "total_amount", "avg_total_amount")
    .sort("total_amount", descending=True)
)
print(out_native.collect())
# shape: (5, 5)
# ┌──────────┬──────────┬──────────┬──────────────┬──────────────────┐
# │ order_id ┆ customer ┆ product  ┆ total_amount ┆ avg_total_amount │
# │ ---      ┆ ---      ┆ ---      ┆ ---          ┆ ---              │
# │ i64      ┆ str      ┆ str      ┆ f64          ┆ f64              │
# ╞══════════╪══════════╪══════════╪══════════════╪══════════════════╡
# │ 1014     ┆ Gina     ┆ Desk     ┆ 692.000      ┆ 265.083          │
# │ 1009     ┆ Fiona    ┆ Desk     ┆ 612.000      ┆ 265.083          │
# │ 1006     ┆ Evan     ┆ Monitor  ┆ 410.000      ┆ 265.083          │
# │ 1008     ┆ Diana    ┆ Desk     ┆ 372.000      ┆ 265.083          │
# │ 1004     ┆ Diana    ┆ Keyboard ┆ 349.500      ┆ 265.083          │
# └──────────┴──────────┴──────────┴──────────────┴──────────────────┘


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------- 11. IN-subquery idea: use SEMI JOIN rewrite ---------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
In many SQL dialects, you may write:

    WHERE customer_id IN (SELECT customer_id FROM customers WHERE segment = 'VIP')

A reliable Polars-style SQL rewrite is to create the VIP customer table as a CTE
and use a SEMI JOIN. A SEMI JOIN keeps rows from the left table that have a match
on the right table, without adding right-table columns.
'''

out_sql = ctx.execute(
    """
    WITH vip_customers AS (
        SELECT customer_id
        FROM customers
        WHERE segment = 'VIP'
    )
    SELECT
        o.order_id,
        o.customer,
        o.product,
        o.total_amount
    FROM orders AS o
    SEMI JOIN vip_customers AS v
        ON o.customer_id = v.customer_id
    ORDER BY o.order_id
    """
)
print(out_sql.collect())
# shape: (7, 4)
# ┌──────────┬──────────┬──────────┬──────────────┐
# │ order_id ┆ customer ┆ product  ┆ total_amount │
# │ ---      ┆ ---      ┆ ---      ┆ ---          │
# │ i64      ┆ str      ┆ str      ┆ f64          │
# ╞══════════╪══════════╪══════════╪══════════════╡
# │ 1001     ┆ Alice    ┆ Keyboard ┆ 221.000      │
# │ 1003     ┆ Alice    ┆ Monitor  ┆ 220.500      │
# │ 1004     ┆ Diana    ┆ Keyboard ┆ 349.500      │
# │ …        ┆ …        ┆ …        ┆ …            │
# │ 1012     ┆ Alice    ┆ Keyboard ┆ 65.000       │
# │ 1014     ┆ Gina     ┆ Desk     ┆ 692.000      │
# └──────────┴──────────┴──────────┴──────────────┘

# Native Polars equivalent.
vip_customers = lf_customers.filter(c("segment") == "VIP").select("customer_id")
out_native = (
    lf_orders
    .join(vip_customers, on="customer_id", how="semi")
    .select("order_id", "customer", "product", "total_amount")
    .sort("order_id")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------- 12. NOT IN / NOT EXISTS idea: use ANTI JOIN rewrite ----------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
ANTI JOIN is the natural Polars SQL rewrite for NOT IN / NOT EXISTS style logic.

This example returns customers who have no paid orders.
'''

out_sql = ctx.execute(
    """
    WITH paid_customer_ids AS (
        SELECT DISTINCT customer_id
        FROM orders
        WHERE status = 'paid'
    )
    SELECT
        c.customer_id,
        c.customer_name,
        c.segment
    FROM customers AS c
    ANTI JOIN paid_customer_ids AS p
        ON c.customer_id = p.customer_id
    ORDER BY c.customer_id
    """
)
print(out_sql.collect())
# shape: (1, 3)
# ┌─────────────┬───────────────┬─────────┐
# │ customer_id ┆ customer_name ┆ segment │
# │ ---         ┆ ---           ┆ ---     │
# │ i64         ┆ str           ┆ str     │
# ╞═════════════╪═══════════════╪═════════╡
# │ 8           ┆ Ivy           ┆ VIP     │
# └─────────────┴───────────────┴─────────┘

# Native Polars equivalent.
paid_customer_ids = (
    lf_orders
    .filter(c("status") == "paid")
    .select("customer_id")
    .unique()
)
out_native = (
    lf_customers
    .join(paid_customer_ids, on="customer_id", how="anti")
    .select("customer_id", "customer_name", "segment")
    .sort("customer_id")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------- 13. CTE scope is one SQL statement -------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A CTE is not registered as a permanent SQLContext table.

The following query works because paid_orders is defined inside the same SQL
statement. But after the statement finishes, ctx.tables() will not include
paid_orders.
'''

out_sql = ctx.execute(
    """
    WITH paid_orders AS (
        SELECT *
        FROM orders
        WHERE status = 'paid'
    )
    SELECT COUNT(*) AS n_paid_orders
    FROM paid_orders
    """
)
print(out_sql.collect())
# shape: (1, 1)
# ┌───────────────┐
# │ n_paid_orders │
# │ ---           │
# │ u32           │
# ╞═══════════════╡
# │ 11            │
# └───────────────┘

print(ctx.tables())
# The registered tables are orders, customers, and regional_targets.
# paid_orders was only a temporary CTE inside the previous statement.


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 14. Use CTE output in later Polars chain ---------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
SQLContext.execute(...) returns a LazyFrame by default.

This means you can write a complex SQL query with CTEs, then continue with native
Polars operations before collecting.
'''

out_sql = ctx.execute(
    """
    WITH customer_sales AS (
        SELECT
            customer_id,
            SUM(total_amount) AS total_sales
        FROM orders
        GROUP BY customer_id
    )
    SELECT
        c.customer_name,
        c.segment,
        s.total_sales
    FROM customer_sales AS s
    INNER JOIN customers AS c
        ON s.customer_id = c.customer_id
    """
)

# Continue with native Polars after SQL.
out_polars_chain = (
    out_sql
    .with_columns(
        pl.when(c("total_sales") >= 600)
        .then(pl.lit("large"))
        .when(c("total_sales") >= 300)
        .then(pl.lit("medium"))
        .otherwise(pl.lit("small"))
        .alias("sales_size")
    )
    .sort("total_sales", descending=True)
)
print(out_polars_chain.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 15. Common mistakes ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Common subquery and CTE mistakes:

1. Forgetting to alias an inline view.

   Better:
       FROM (SELECT ... FROM orders) AS alias_name

2. Expecting a CTE to exist after the SQL statement.

   WITH paid_orders AS (...) SELECT ... FROM paid_orders
   works only inside that one SQL statement.

3. Making a deeply nested query when a CTE pipeline would be easier to read.

   Prefer:
       WITH step1 AS (...), step2 AS (...) SELECT ... FROM step2

4. Filtering on a SELECT alias at the same query level.

   If this is not accepted:
       SELECT total_amount * 2 AS x FROM orders WHERE x > 100

   Use an inline view:
       SELECT * FROM (
           SELECT total_amount * 2 AS x FROM orders
       ) AS q
       WHERE x > 100

5. Writing scalar or predicate subqueries when a join rewrite is clearer.

   Scalar threshold idea:
       Use one-row CTE + CROSS JOIN.

   IN / EXISTS idea:
       Use SEMI JOIN.

   NOT IN / NOT EXISTS idea:
       Use ANTI JOIN.

6. Forgetting that Polars has no pandas-style row index.

   CTEs and subqueries return normal columns, not index levels.
'''
