'''
Polars SQL window functions, ranking functions, named WINDOW clauses, and QUALIFY.

Main ideas:
1. Window functions compute values across related rows without reducing the
   result to one row per group.
2. OVER (...) defines the window.
3. PARTITION BY defines groups inside the window.
4. ORDER BY defines row order inside each partition.
5. Aggregate functions such as SUM, AVG, MIN, MAX, and COUNT can be used as
   window functions.
6. ROW_NUMBER gives a unique sequential number inside a partition.
7. RANK gives tied rows the same rank and leaves gaps after ties.
8. DENSE_RANK gives tied rows the same rank but does not leave gaps.
9. LAG and LEAD access previous and next rows inside an ordered partition.
10. FIRST_VALUE and LAST_VALUE return first/last values inside an ordered frame.
11. WINDOW lets you define a named window once and reuse it.
12. QUALIFY filters rows after window expressions are evaluated.

Important Polars SQL notes:
+ Frame-level .sql(...) registers the frame as the SQL table named self.
+ LazyFrame.sql(...) returns a LazyFrame, so call .collect() to materialize it.
+ Window functions preserve row-level shape, unlike GROUP BY aggregation.
+ Use ORDER BY in the outer query when deterministic final row order matters.
+ RANK and DENSE_RANK require OVER with ORDER BY in the window specification.
+ Polars defaults to ROWS framing semantics for SQL window functions when an
  explicit frame is omitted, specifically:
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  This can differ from some database engines that default to RANGE semantics.
+ QUALIFY is like WHERE for window results. WHERE filters input rows before
  windows are evaluated; QUALIFY filters rows after window values exist.
+ This file focuses on functions documented in Polars SQL:
      ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD,
      FIRST_VALUE, LAST_VALUE, and aggregate functions with OVER.
'''

import datetime as dt

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(10)
pl.Config.set_tbl_cols(12)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(120)


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 0. Setup data ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The examples are self-contained so this file can run without external datasets.

The orders table intentionally includes:
+ multiple customers
+ multiple regions and products
+ repeated amounts to demonstrate rank ties
+ dates to demonstrate ordered window calculations
+ status values so we can compare WHERE vs QUALIFY

We derive gross_amount, discount_amount, net_amount, and total_amount using native
Polars once, then use SQL window functions to analyze those columns.
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
            "North", "East", "South", "South", "East",
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

print(df_orders)
# shape: (15, 16)
# ┌─────────┬─────────┬─────────┬────────┬─────────┬─────────┬───┬─────────┬─────────┬────────┬────────┬────────┬────────┐
# │ order_i ┆ custome ┆ custome ┆ region ┆ product ┆ quantit ┆ … ┆ priorit ┆ order_d ┆ gross_ ┆ discou ┆ net_am ┆ total_ │
# │ d       ┆ r_id    ┆ r       ┆ ---    ┆ ---     ┆ y       ┆   ┆ y       ┆ ate     ┆ amount ┆ nt_amo ┆ ount   ┆ amount │
# │ ---     ┆ ---     ┆ ---     ┆ str    ┆ str     ┆ ---     ┆   ┆ ---     ┆ ---     ┆ ---    ┆ unt    ┆ ---    ┆ ---    │
# │ i64     ┆ i64     ┆ str     ┆        ┆         ┆ i64     ┆   ┆ bool    ┆ date    ┆ f64    ┆ ---    ┆ f64    ┆ f64    │
# │         ┆         ┆         ┆        ┆         ┆         ┆   ┆         ┆         ┆        ┆ f64    ┆        ┆        │
# ╞═════════╪═════════╪═════════╪════════╪═════════╪═════════╪═══╪═════════╪═════════╪════════╪════════╪════════╪════════╡
# │ 1001    ┆ 1       ┆ Alice   ┆ East   ┆ Keyboar ┆ 2       ┆ … ┆ true    ┆ 2024-01 ┆ 240.00 ┆ 24.000 ┆ 216.00 ┆ 221.00 │
# │         ┆         ┆         ┆        ┆ d       ┆         ┆   ┆         ┆ -03     ┆ 0      ┆        ┆ 0      ┆ 0      │
# │ 1002    ┆ 2       ┆ Bob     ┆ West   ┆ Mouse   ┆ 1       ┆ … ┆ false   ┆ 2024-01 ┆ 35.000 ┆ 0.000  ┆ 35.000 ┆ 39.000 │
# │         ┆         ┆         ┆        ┆         ┆         ┆   ┆         ┆ -05     ┆        ┆        ┆        ┆        │
# │ 1003    ┆ 1       ┆ Alice   ┆ East   ┆ Monitor ┆ 1       ┆ … ┆ true    ┆ 2024-02 ┆ 250.00 ┆ 37.500 ┆ 212.50 ┆ 220.50 │
# │         ┆         ┆         ┆        ┆         ┆         ┆   ┆         ┆ -10     ┆ 0      ┆        ┆ 0      ┆ 0      │
# │ 1004    ┆ 3       ┆ Diana   ┆ North  ┆ Keyboar ┆ 3       ┆ … ┆ false   ┆ 2024-02 ┆ 360.00 ┆ 18.000 ┆ 342.00 ┆ 349.50 │
# │         ┆         ┆         ┆        ┆ d       ┆         ┆   ┆         ┆ -12     ┆ 0      ┆        ┆ 0      ┆ 0      │
# │ 1005    ┆ 2       ┆ Bob     ┆ West   ┆ Mouse   ┆ 4       ┆ … ┆ false   ┆ 2024-03 ┆ 140.00 ┆ 0.000  ┆ 140.00 ┆ 144.00 │
# │         ┆         ┆         ┆        ┆         ┆         ┆   ┆         ┆ -01     ┆ 0      ┆        ┆ 0      ┆ 0      │
# │ …       ┆ …       ┆ …       ┆ …      ┆ …       ┆ …       ┆ … ┆ …       ┆ …       ┆ …      ┆ …      ┆ …      ┆ …      │
# │ 1011    ┆ 4       ┆ Evan    ┆ North  ┆ Mouse   ┆ 3       ┆ … ┆ false   ┆ 2024-05 ┆ 105.00 ┆ 0.000  ┆ 105.00 ┆ 109.00 │
# │         ┆         ┆         ┆        ┆         ┆         ┆   ┆         ┆ -01     ┆ 0      ┆        ┆ 0      ┆ 0      │
# │ 1012    ┆ 1       ┆ Alice   ┆ East   ┆ Keyboar ┆ 1       ┆ … ┆ true    ┆ 2024-05 ┆ 120.00 ┆ 60.000 ┆ 60.000 ┆ 65.000 │
# │         ┆         ┆         ┆        ┆ d       ┆         ┆   ┆         ┆ -15     ┆ 0      ┆        ┆        ┆        │
# │ 1013    ┆ 5       ┆ Fiona   ┆ South  ┆ Monitor ┆ 1       ┆ … ┆ false   ┆ 2024-05 ┆ 250.00 ┆ 25.000 ┆ 225.00 ┆ 233.00 │
# │         ┆         ┆         ┆        ┆         ┆         ┆   ┆         ┆ -20     ┆ 0      ┆        ┆ 0      ┆ 0      │
# │ 1014    ┆ 6       ┆ Gina    ┆ South  ┆ Desk    ┆ 2       ┆ … ┆ true    ┆ 2024-06 ┆ 800.00 ┆ 120.00 ┆ 680.00 ┆ 692.00 │
# │         ┆         ┆         ┆        ┆         ┆         ┆   ┆         ┆ -03     ┆ 0      ┆ 0      ┆ 0      ┆ 0      │
# │ 1015    ┆ 7       ┆ Henry   ┆ East   ┆ Mouse   ┆ 6       ┆ … ┆ false   ┆ 2024-06 ┆ 210.00 ┆ 0.000  ┆ 210.00 ┆ 214.00 │
# │         ┆         ┆         ┆        ┆         ┆         ┆   ┆         ┆ -08     ┆ 0      ┆        ┆ 0      ┆ 0      │
# └─────────┴─────────┴─────────┴────────┴─────────┴─────────┴───┴─────────┴─────────┴────────┴────────┴────────┴────────┘


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 1. Window vs GROUP BY mental model -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
GROUP BY collapses rows.
Window functions keep the row-level data and add group-aware summary values.

Here each order row keeps its own order_id/product/amount, while customer_total
and customer_avg_order are computed over all orders for that customer.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        customer,
        product,
        total_amount,
        SUM(total_amount) OVER (PARTITION BY customer_id) AS customer_total,
        AVG(total_amount) OVER (PARTITION BY customer_id) AS customer_avg_order,
        COUNT(*) OVER (PARTITION BY customer_id) AS customer_n_orders
    FROM self
    ORDER BY customer_id, order_date
    """
)
print(out_sql.collect())
# shape: (15, 7)
# ┌──────────┬──────────┬──────────┬──────────────┬────────────────┬────────────────────┬───────────────────┐
# │ order_id ┆ customer ┆ product  ┆ total_amount ┆ customer_total ┆ customer_avg_order ┆ customer_n_orders │
# │ ---      ┆ ---      ┆ ---      ┆ ---          ┆ ---            ┆ ---                ┆ ---               │
# │ i64      ┆ str      ┆ str      ┆ f64          ┆ f64            ┆ f64                ┆ u32               │
# ╞══════════╪══════════╪══════════╪══════════════╪════════════════╪════════════════════╪═══════════════════╡
# │ 1001     ┆ Alice    ┆ Keyboard ┆ 221.000      ┆ 676.750        ┆ 169.188            ┆ 4                 │
# │ 1003     ┆ Alice    ┆ Monitor  ┆ 220.500      ┆ 676.750        ┆ 169.188            ┆ 4                 │
# │ 1007     ┆ Alice    ┆ Mouse    ┆ 170.250      ┆ 676.750        ┆ 169.188            ┆ 4                 │
# │ 1012     ┆ Alice    ┆ Keyboard ┆ 65.000       ┆ 676.750        ┆ 169.188            ┆ 4                 │
# │ 1002     ┆ Bob      ┆ Mouse    ┆ 39.000       ┆ 308.000        ┆ 102.667            ┆ 3                 │
# │ …        ┆ …        ┆ …        ┆ …            ┆ …              ┆ …                  ┆ …                 │
# │ 1011     ┆ Evan     ┆ Mouse    ┆ 109.000      ┆ 519.000        ┆ 259.500            ┆ 2                 │
# │ 1009     ┆ Fiona    ┆ Desk     ┆ 612.000      ┆ 845.000        ┆ 422.500            ┆ 2                 │
# │ 1013     ┆ Fiona    ┆ Monitor  ┆ 233.000      ┆ 845.000        ┆ 422.500            ┆ 2                 │
# │ 1014     ┆ Gina     ┆ Desk     ┆ 692.000      ┆ 692.000        ┆ 692.000            ┆ 1                 │
# │ 1015     ┆ Henry    ┆ Mouse    ┆ 214.000      ┆ 214.000        ┆ 214.000            ┆ 1                 │
# └──────────┴──────────┴──────────┴──────────────┴────────────────┴────────────────────┴───────────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .with_columns(
        c("total_amount").sum().over("customer_id").alias("customer_total"),
        c("total_amount").mean().over("customer_id").alias("customer_avg_order"),
        c("order_id").count().over("customer_id").alias("customer_n_orders"),
    )
    .select(
        "order_id",
        "customer",
        "product",
        "total_amount",
        "customer_total",
        "customer_avg_order",
        "customer_n_orders",
    )
    .sort("customer_id", "order_date")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 2. PARTITION BY one or more keys ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
PARTITION BY defines the groups used by the window function.

This example computes both:
+ region-level summary columns
+ region/product-level summary columns

The original rows are preserved.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        region,
        product,
        total_amount,
        SUM(total_amount) OVER (PARTITION BY region) AS region_sales,
        AVG(total_amount) OVER (PARTITION BY region) AS region_avg_order,
        SUM(total_amount) OVER (PARTITION BY region, product) AS region_product_sales
    FROM self
    ORDER BY region, product, order_id
    """
)
print(out_sql.collect())
# shape: (15, 7)
# ┌──────────┬────────┬──────────┬──────────────┬──────────────┬──────────────────┬──────────────────────┐
# │ order_id ┆ region ┆ product  ┆ total_amount ┆ region_sales ┆ region_avg_order ┆ region_product_sales │
# │ ---      ┆ ---    ┆ ---      ┆ ---          ┆ ---          ┆ ---              ┆ ---                  │
# │ i64      ┆ str    ┆ str      ┆ f64          ┆ f64          ┆ f64              ┆ f64                  │
# ╞══════════╪════════╪══════════╪══════════════╪══════════════╪══════════════════╪══════════════════════╡
# │ 1001     ┆ East   ┆ Keyboard ┆ 221.000      ┆ 890.750      ┆ 178.150          ┆ 286.000              │
# │ 1012     ┆ East   ┆ Keyboard ┆ 65.000       ┆ 890.750      ┆ 178.150          ┆ 286.000              │
# │ 1003     ┆ East   ┆ Monitor  ┆ 220.500      ┆ 890.750      ┆ 178.150          ┆ 220.500              │
# │ 1007     ┆ East   ┆ Mouse    ┆ 170.250      ┆ 890.750      ┆ 178.150          ┆ 384.250              │
# │ 1015     ┆ East   ┆ Mouse    ┆ 214.000      ┆ 890.750      ┆ 178.150          ┆ 384.250              │
# │ …        ┆ …      ┆ …        ┆ …            ┆ …            ┆ …                ┆ …                    │
# │ 1014     ┆ South  ┆ Desk     ┆ 692.000      ┆ 1537.000     ┆ 512.333          ┆ 1304.000             │
# │ 1013     ┆ South  ┆ Monitor  ┆ 233.000      ┆ 1537.000     ┆ 512.333          ┆ 233.000              │
# │ 1010     ┆ West   ┆ Keyboard ┆ 125.000      ┆ 308.000      ┆ 102.667          ┆ 125.000              │
# │ 1002     ┆ West   ┆ Mouse    ┆ 39.000       ┆ 308.000      ┆ 102.667          ┆ 183.000              │
# │ 1005     ┆ West   ┆ Mouse    ┆ 144.000      ┆ 308.000      ┆ 102.667          ┆ 183.000              │
# └──────────┴────────┴──────────┴──────────────┴──────────────┴──────────────────┴──────────────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .with_columns(
        c("total_amount").sum().over("region").alias("region_sales"),
        c("total_amount").mean().over("region").alias("region_avg_order"),
        c("total_amount").sum().over("region", "product").alias("region_product_sales"),
    )
    .select(
        "order_id",
        "region",
        "product",
        "total_amount",
        "region_sales",
        "region_avg_order",
        "region_product_sales",
    )
    .sort("region", "product", "order_id")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 3. ORDER BY inside OVER: running totals ----------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
ORDER BY inside OVER defines the row order used by ordered window calculations.

This example computes a running total for each customer over time.

The explicit ROWS frame makes the intended cumulative calculation clear:
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
'''

out_sql = lf_orders.sql(
    """
    SELECT
        customer,
        order_id,
        order_date,
        total_amount,
        SUM(total_amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS customer_running_total,
        COUNT(*) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS customer_order_number
    FROM self
    ORDER BY customer_id, order_date, order_id
    """
)
print(out_sql.collect())
# shape: (15, 6)
# ┌──────────┬──────────┬────────────┬──────────────┬────────────────────────┬───────────────────────┐
# │ customer ┆ order_id ┆ order_date ┆ total_amount ┆ customer_running_total ┆ customer_order_number │
# │ ---      ┆ ---      ┆ ---        ┆ ---          ┆ ---                    ┆ ---                   │
# │ str      ┆ i64      ┆ date       ┆ f64          ┆ f64                    ┆ i64                   │
# ╞══════════╪══════════╪════════════╪══════════════╪════════════════════════╪═══════════════════════╡
# │ Alice    ┆ 1001     ┆ 2024-01-03 ┆ 221.000      ┆ 221.000                ┆ 1                     │
# │ Alice    ┆ 1003     ┆ 2024-02-10 ┆ 220.500      ┆ 441.500                ┆ 2                     │
# │ Alice    ┆ 1007     ┆ 2024-03-20 ┆ 170.250      ┆ 611.750                ┆ 3                     │
# │ Alice    ┆ 1012     ┆ 2024-05-15 ┆ 65.000       ┆ 676.750                ┆ 4                     │
# │ Bob      ┆ 1002     ┆ 2024-01-05 ┆ 39.000       ┆ 39.000                 ┆ 1                     │
# │ …        ┆ …        ┆ …          ┆ …            ┆ …                      ┆ …                     │
# │ Evan     ┆ 1011     ┆ 2024-05-01 ┆ 109.000      ┆ 519.000                ┆ 2                     │
# │ Fiona    ┆ 1009     ┆ 2024-04-10 ┆ 612.000      ┆ 612.000                ┆ 1                     │
# │ Fiona    ┆ 1013     ┆ 2024-05-20 ┆ 233.000      ┆ 845.000                ┆ 2                     │
# │ Gina     ┆ 1014     ┆ 2024-06-03 ┆ 692.000      ┆ 692.000                ┆ 1                     │
# │ Henry    ┆ 1015     ┆ 2024-06-08 ┆ 214.000      ┆ 214.000                ┆ 1                     │
# └──────────┴──────────┴────────────┴──────────────┴────────────────────────┴───────────────────────┘


# Native Polars equivalent.
# Sort first so the cumulative operation follows the desired order inside each customer.
out_native = (
    lf_orders
    .sort("customer_id", "order_date", "order_id")
    .with_columns(
        c("total_amount").cum_sum().over("customer_id").alias("customer_running_total"),
        c("order_id").cum_count().over("customer_id").alias("customer_order_number"),
    )
    .select(
        "customer",
        "order_id",
        "order_date",
        "total_amount",
        "customer_running_total",
        "customer_order_number",
    )
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 4. ROW_NUMBER() --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
ROW_NUMBER() gives a unique sequential number inside each ordered partition.

It is useful for:
+ first row per group
+ top N rows per group
+ deterministic tie-breaking when ORDER BY contains enough columns
'''

out_sql = lf_orders.sql(
    """
    SELECT
        customer,
        order_id,
        order_date,
        total_amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
        ) AS order_number_by_customer,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY (0 - total_amount), order_id
        ) AS value_rank_by_customer
    FROM self
    ORDER BY customer_id, order_date, order_id
    """
)
print(out_sql.collect())
# shape: (15, 6)
# ┌──────────┬──────────┬────────────┬──────────────┬──────────────────────────┬────────────────────────┐
# │ customer ┆ order_id ┆ order_date ┆ total_amount ┆ order_number_by_customer ┆ value_rank_by_customer │
# │ ---      ┆ ---      ┆ ---        ┆ ---          ┆ ---                      ┆ ---                    │
# │ str      ┆ i64      ┆ date       ┆ f64          ┆ u32                      ┆ u32                    │
# ╞══════════╪══════════╪════════════╪══════════════╪══════════════════════════╪════════════════════════╡
# │ Alice    ┆ 1001     ┆ 2024-01-03 ┆ 221.000      ┆ 1                        ┆ 1                      │
# │ Alice    ┆ 1003     ┆ 2024-02-10 ┆ 220.500      ┆ 2                        ┆ 2                      │
# │ Alice    ┆ 1007     ┆ 2024-03-20 ┆ 170.250      ┆ 3                        ┆ 3                      │
# │ Alice    ┆ 1012     ┆ 2024-05-15 ┆ 65.000       ┆ 4                        ┆ 4                      │
# │ Bob      ┆ 1002     ┆ 2024-01-05 ┆ 39.000       ┆ 1                        ┆ 3                      │
# │ …        ┆ …        ┆ …          ┆ …            ┆ …                        ┆ …                      │
# │ Evan     ┆ 1011     ┆ 2024-05-01 ┆ 109.000      ┆ 2                        ┆ 2                      │
# │ Fiona    ┆ 1009     ┆ 2024-04-10 ┆ 612.000      ┆ 1                        ┆ 1                      │
# │ Fiona    ┆ 1013     ┆ 2024-05-20 ┆ 233.000      ┆ 2                        ┆ 2                      │
# │ Gina     ┆ 1014     ┆ 2024-06-03 ┆ 692.000      ┆ 1                        ┆ 1                      │
# │ Henry    ┆ 1015     ┆ 2024-06-08 ┆ 214.000      ┆ 1                        ┆ 1                      │
# └──────────┴──────────┴────────────┴──────────────┴──────────────────────────┴────────────────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .sort("customer_id", "order_date", "order_id")
    .with_columns(
        c("order_id").cum_count().over("customer_id").alias("order_number_by_customer")
    )
    .sort("customer_id", "total_amount", "order_id", descending=[False, True, False])
    .with_columns(
        c("order_id").cum_count().over("customer_id").alias("value_rank_by_customer")
    )
    .select(
        "customer",
        "order_id",
        "order_date",
        "total_amount",
        "order_number_by_customer",
        "value_rank_by_customer",
    )
    .sort("customer", "order_date", "order_id")
)
print(out_native.collect())
# shape: (15, 6)
# ┌──────────┬──────────┬────────────┬──────────────┬──────────────────────────┬────────────────────────┐
# │ customer ┆ order_id ┆ order_date ┆ total_amount ┆ order_number_by_customer ┆ value_rank_by_customer │
# │ ---      ┆ ---      ┆ ---        ┆ ---          ┆ ---                      ┆ ---                    │
# │ str      ┆ i64      ┆ date       ┆ f64          ┆ u32                      ┆ u32                    │
# ╞══════════╪══════════╪════════════╪══════════════╪══════════════════════════╪════════════════════════╡
# │ Alice    ┆ 1001     ┆ 2024-01-03 ┆ 221.000      ┆ 1                        ┆ 1                      │
# │ Alice    ┆ 1003     ┆ 2024-02-10 ┆ 220.500      ┆ 2                        ┆ 2                      │
# │ Alice    ┆ 1007     ┆ 2024-03-20 ┆ 170.250      ┆ 3                        ┆ 3                      │
# │ Alice    ┆ 1012     ┆ 2024-05-15 ┆ 65.000       ┆ 4                        ┆ 4                      │
# │ Bob      ┆ 1002     ┆ 2024-01-05 ┆ 39.000       ┆ 1                        ┆ 3                      │
# │ …        ┆ …        ┆ …          ┆ …            ┆ …                        ┆ …                      │
# │ Evan     ┆ 1011     ┆ 2024-05-01 ┆ 109.000      ┆ 2                        ┆ 2                      │
# │ Fiona    ┆ 1009     ┆ 2024-04-10 ┆ 612.000      ┆ 1                        ┆ 1                      │
# │ Fiona    ┆ 1013     ┆ 2024-05-20 ┆ 233.000      ┆ 2                        ┆ 2                      │
# │ Gina     ┆ 1014     ┆ 2024-06-03 ┆ 692.000      ┆ 1                        ┆ 1                      │
# │ Henry    ┆ 1015     ┆ 2024-06-08 ┆ 214.000      ┆ 1                        ┆ 1                      │
# └──────────┴──────────┴────────────┴──────────────┴──────────────────────────┴────────────────────────┘


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 5. RANK() and DENSE_RANK() --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
RANK and DENSE_RANK both assign the same rank to tied values.

Difference:
+ RANK leaves gaps after ties.
+ DENSE_RANK does not leave gaps after ties.

The Mouse product has repeated or close values that make ranking behavior easier
to inspect in the output.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        product,
        order_id,
        customer,
        total_amount,
        RANK() OVER (
            PARTITION BY product
            ORDER BY total_amount DESC
        ) AS product_rank,
        DENSE_RANK() OVER (
            PARTITION BY product
            ORDER BY total_amount DESC
        ) AS product_dense_rank
    FROM self
    ORDER BY product, total_amount DESC, order_id
    """
)
print(out_sql.collect())
# shape: (15, 6)
# ┌──────────┬──────────┬──────────┬──────────────┬──────────────┬────────────────────┐
# │ product  ┆ order_id ┆ customer ┆ total_amount ┆ product_rank ┆ product_dense_rank │
# │ ---      ┆ ---      ┆ ---      ┆ ---          ┆ ---          ┆ ---                │
# │ str      ┆ i64      ┆ str      ┆ f64          ┆ u32          ┆ u32                │
# ╞══════════╪══════════╪══════════╪══════════════╪══════════════╪════════════════════╡
# │ Desk     ┆ 1014     ┆ Gina     ┆ 692.000      ┆ 1            ┆ 1                  │
# │ Desk     ┆ 1009     ┆ Fiona    ┆ 612.000      ┆ 2            ┆ 2                  │
# │ Desk     ┆ 1008     ┆ Diana    ┆ 372.000      ┆ 3            ┆ 3                  │
# │ Keyboard ┆ 1004     ┆ Diana    ┆ 349.500      ┆ 1            ┆ 1                  │
# │ Keyboard ┆ 1001     ┆ Alice    ┆ 221.000      ┆ 2            ┆ 2                  │
# │ …        ┆ …        ┆ …        ┆ …            ┆ …            ┆ …                  │
# │ Mouse    ┆ 1015     ┆ Henry    ┆ 214.000      ┆ 1            ┆ 1                  │
# │ Mouse    ┆ 1007     ┆ Alice    ┆ 170.250      ┆ 2            ┆ 2                  │
# │ Mouse    ┆ 1005     ┆ Bob      ┆ 144.000      ┆ 3            ┆ 3                  │
# │ Mouse    ┆ 1011     ┆ Evan     ┆ 109.000      ┆ 4            ┆ 4                  │
# │ Mouse    ┆ 1002     ┆ Bob      ┆ 39.000       ┆ 5            ┆ 5                  │
# └──────────┴──────────┴──────────┴──────────────┴──────────────┴────────────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .with_columns(
        c("total_amount").rank(method="min", descending=True).over("product").alias("product_rank"),
        c("total_amount").rank(method="dense", descending=True).over("product").alias("product_dense_rank"),
    )
    .select(
        "product",
        "order_id",
        "customer",
        "total_amount",
        "product_rank",
        "product_dense_rank",
    )
    .sort("product", "total_amount", "order_id", descending=[False, True, False])
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------- 6. QUALIFY: top N rows per group ---------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
QUALIFY filters rows after window functions are available.

This is usually cleaner than creating a subquery just to filter by a row number
or rank.

Example:
    Keep the top 2 order values for each customer.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        customer,
        order_id,
        order_date,
        product,
        total_amount
    FROM self
    WINDOW value_window AS (
        PARTITION BY customer_id
        ORDER BY (0 - total_amount), order_id
    )
    QUALIFY ROW_NUMBER() OVER value_window <= 2
    ORDER BY customer, (0 - total_amount), order_id
    """
)
print(out_sql.collect())

# Native Polars equivalent.
out_native = (
    lf_orders
    .sort("customer_id", "total_amount", "order_id", descending=[False, True, False])
    .with_columns(
        c("order_id").cum_count().over("customer_id").alias("value_row_number")
    )
    .filter(c("value_row_number") <= 2)
    .select("customer", "order_id", "order_date", "product", "total_amount")
    .sort("customer", "total_amount", "order_id", descending=[False, True, False])
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 7. Named WINDOW clauses ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The WINDOW clause lets you define a named window once and reuse it.

This avoids repeating the same PARTITION BY / ORDER BY specification many times.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        customer,
        order_id,
        order_date,
        total_amount,
        SUM(total_amount) OVER customer_time AS running_total,
        AVG(total_amount) OVER customer_all AS customer_avg,
        COUNT(*) OVER customer_all AS customer_order_count
    FROM self
    WINDOW
        customer_time AS (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        customer_all AS (
            PARTITION BY customer_id
        )
    ORDER BY customer_id, order_date, order_id
    """
)
print(out_sql.collect())
# shape: (15, 7)
# ┌──────────┬──────────┬────────────┬──────────────┬───────────────┬──────────────┬──────────────────────┐
# │ customer ┆ order_id ┆ order_date ┆ total_amount ┆ running_total ┆ customer_avg ┆ customer_order_count │
# │ ---      ┆ ---      ┆ ---        ┆ ---          ┆ ---           ┆ ---          ┆ ---                  │
# │ str      ┆ i64      ┆ date       ┆ f64          ┆ f64           ┆ f64          ┆ u32                  │
# ╞══════════╪══════════╪════════════╪══════════════╪═══════════════╪══════════════╪══════════════════════╡
# │ Alice    ┆ 1001     ┆ 2024-01-03 ┆ 221.000      ┆ 221.000       ┆ 169.188      ┆ 4                    │
# │ Alice    ┆ 1003     ┆ 2024-02-10 ┆ 220.500      ┆ 441.500       ┆ 169.188      ┆ 4                    │
# │ Alice    ┆ 1007     ┆ 2024-03-20 ┆ 170.250      ┆ 611.750       ┆ 169.188      ┆ 4                    │
# │ Alice    ┆ 1012     ┆ 2024-05-15 ┆ 65.000       ┆ 676.750       ┆ 169.188      ┆ 4                    │
# │ Bob      ┆ 1002     ┆ 2024-01-05 ┆ 39.000       ┆ 39.000        ┆ 102.667      ┆ 3                    │
# │ …        ┆ …        ┆ …          ┆ …            ┆ …             ┆ …            ┆ …                    │
# │ Evan     ┆ 1011     ┆ 2024-05-01 ┆ 109.000      ┆ 519.000       ┆ 259.500      ┆ 2                    │
# │ Fiona    ┆ 1009     ┆ 2024-04-10 ┆ 612.000      ┆ 612.000       ┆ 422.500      ┆ 2                    │
# │ Fiona    ┆ 1013     ┆ 2024-05-20 ┆ 233.000      ┆ 845.000       ┆ 422.500      ┆ 2                    │
# │ Gina     ┆ 1014     ┆ 2024-06-03 ┆ 692.000      ┆ 692.000       ┆ 692.000      ┆ 1                    │
# │ Henry    ┆ 1015     ┆ 2024-06-08 ┆ 214.000      ┆ 214.000       ┆ 214.000      ┆ 1                    │
# └──────────┴──────────┴────────────┴──────────────┴───────────────┴──────────────┴──────────────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .sort("customer_id", "order_date", "order_id")
    .with_columns(
        c("total_amount").cum_sum().over("customer_id").alias("running_total"),
        c("total_amount").mean().over("customer_id").alias("customer_avg"),
        c("order_id").count().over("customer_id").alias("customer_order_count"),
    )
    .select(
        "customer",
        "order_id",
        "order_date",
        "total_amount",
        "running_total",
        "customer_avg",
        "customer_order_count",
    )
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 8. LAG() and LEAD(): previous/next rows ---------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
LAG returns a value from a previous row in the ordered partition.
LEAD returns a value from a following row in the ordered partition.

If the requested row does not exist, the result is null.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        customer,
        order_id,
        order_date,
        total_amount,
        LAG(total_amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
        ) AS previous_order_amount,
        LEAD(total_amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
        ) AS next_order_amount,
        total_amount - LAG(total_amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
        ) AS change_from_previous
    FROM self
    ORDER BY customer_id, order_date, order_id
    """
)
print(out_sql.collect())
# shape: (15, 7)
# ┌──────────┬──────────┬────────────┬──────────────┬───────────────────────┬───────────────────┬──────────────────────┐
# │ customer ┆ order_id ┆ order_date ┆ total_amount ┆ previous_order_amount ┆ next_order_amount ┆ change_from_previous │
# │ ---      ┆ ---      ┆ ---        ┆ ---          ┆ ---                   ┆ ---               ┆ ---                  │
# │ str      ┆ i64      ┆ date       ┆ f64          ┆ f64                   ┆ f64               ┆ f64                  │
# ╞══════════╪══════════╪════════════╪══════════════╪═══════════════════════╪═══════════════════╪══════════════════════╡
# │ Alice    ┆ 1001     ┆ 2024-01-03 ┆ 221.000      ┆ null                  ┆ 220.500           ┆ null                 │
# │ Alice    ┆ 1003     ┆ 2024-02-10 ┆ 220.500      ┆ 221.000               ┆ 170.250           ┆ -0.500               │
# │ Alice    ┆ 1007     ┆ 2024-03-20 ┆ 170.250      ┆ 220.500               ┆ 65.000            ┆ -50.250              │
# │ Alice    ┆ 1012     ┆ 2024-05-15 ┆ 65.000       ┆ 170.250               ┆ null              ┆ -105.250             │
# │ Bob      ┆ 1002     ┆ 2024-01-05 ┆ 39.000       ┆ null                  ┆ 144.000           ┆ null                 │
# │ …        ┆ …        ┆ …          ┆ …            ┆ …                     ┆ …                 ┆ …                    │
# │ Evan     ┆ 1011     ┆ 2024-05-01 ┆ 109.000      ┆ 410.000               ┆ null              ┆ -301.000             │
# │ Fiona    ┆ 1009     ┆ 2024-04-10 ┆ 612.000      ┆ null                  ┆ 233.000           ┆ null                 │
# │ Fiona    ┆ 1013     ┆ 2024-05-20 ┆ 233.000      ┆ 612.000               ┆ null              ┆ -379.000             │
# │ Gina     ┆ 1014     ┆ 2024-06-03 ┆ 692.000      ┆ null                  ┆ null              ┆ null                 │
# │ Henry    ┆ 1015     ┆ 2024-06-08 ┆ 214.000      ┆ null                  ┆ null              ┆ null                 │
# └──────────┴──────────┴────────────┴──────────────┴───────────────────────┴───────────────────┴──────────────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .sort("customer_id", "order_date", "order_id")
    .with_columns(
        c("total_amount").shift(1).over("customer_id").alias("previous_order_amount"),
        c("total_amount").shift(-1).over("customer_id").alias("next_order_amount"),
    )
    .with_columns(
        (c("total_amount") - c("previous_order_amount")).alias("change_from_previous")
    )
    .select(
        "customer",
        "order_id",
        "order_date",
        "total_amount",
        "previous_order_amount",
        "next_order_amount",
        "change_from_previous",
    )
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 9. FIRST_VALUE() and LAST_VALUE() ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
FIRST_VALUE and LAST_VALUE use the ordered window frame.

Because Polars SQL defaults to a cumulative ROWS frame when a frame is omitted,
LAST_VALUE with ORDER BY often means "last value up to the current row".

To get the final value across the whole partition, use an explicit frame ending
at UNBOUNDED FOLLOWING.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        customer,
        order_id,
        order_date,
        total_amount,
        FIRST_VALUE(total_amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS first_amount_so_far,
        LAST_VALUE(total_amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS last_amount_so_far,
        LAST_VALUE(total_amount) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS final_amount_for_customer
    FROM self
    ORDER BY customer_id, order_date, order_id
    """
)
print(out_sql.collect())
# shape: (15, 7)
# ┌──────────┬──────────┬────────────┬──────────────┬─────────────────────┬────────────────────┬─────────────────────────┐
# │ customer ┆ order_id ┆ order_date ┆ total_amount ┆ first_amount_so_far ┆ last_amount_so_far ┆ final_amount_for_custom │
# │ ---      ┆ ---      ┆ ---        ┆ ---          ┆ ---                 ┆ ---                ┆ er                      │
# │ str      ┆ i64      ┆ date       ┆ f64          ┆ f64                 ┆ f64                ┆ ---                     │
# │          ┆          ┆            ┆              ┆                     ┆                    ┆ f64                     │
# ╞══════════╪══════════╪════════════╪══════════════╪═════════════════════╪════════════════════╪═════════════════════════╡
# │ Alice    ┆ 1001     ┆ 2024-01-03 ┆ 221.000      ┆ 221.000             ┆ 221.000            ┆ 221.000                 │
# │ Alice    ┆ 1003     ┆ 2024-02-10 ┆ 220.500      ┆ 221.000             ┆ 220.500            ┆ 220.500                 │
# │ Alice    ┆ 1007     ┆ 2024-03-20 ┆ 170.250      ┆ 221.000             ┆ 170.250            ┆ 170.250                 │
# │ Alice    ┆ 1012     ┆ 2024-05-15 ┆ 65.000       ┆ 221.000             ┆ 65.000             ┆ 65.000                  │
# │ Bob      ┆ 1002     ┆ 2024-01-05 ┆ 39.000       ┆ 39.000              ┆ 39.000             ┆ 39.000                  │
# │ …        ┆ …        ┆ …          ┆ …            ┆ …                   ┆ …                  ┆ …                       │
# │ Evan     ┆ 1011     ┆ 2024-05-01 ┆ 109.000      ┆ 410.000             ┆ 109.000            ┆ 109.000                 │
# │ Fiona    ┆ 1009     ┆ 2024-04-10 ┆ 612.000      ┆ 612.000             ┆ 612.000            ┆ 612.000                 │
# │ Fiona    ┆ 1013     ┆ 2024-05-20 ┆ 233.000      ┆ 612.000             ┆ 233.000            ┆ 233.000                 │
# │ Gina     ┆ 1014     ┆ 2024-06-03 ┆ 692.000      ┆ 692.000             ┆ 692.000            ┆ 692.000                 │
# │ Henry    ┆ 1015     ┆ 2024-06-08 ┆ 214.000      ┆ 214.000             ┆ 214.000            ┆ 214.000                 │
# └──────────┴──────────┴────────────┴──────────────┴─────────────────────┴────────────────────┴─────────────────────────┘

# Native Polars equivalent.
# For the final amount in a partition, sort first and use last().over(...).
out_native = (
    lf_orders
    .sort("customer_id", "order_date", "order_id")
    .with_columns(
        c("total_amount").first().over("customer_id").alias("first_amount_for_customer"),
        c("total_amount").last().over("customer_id").alias("final_amount_for_customer"),
        c("total_amount").alias("last_amount_so_far"),
    )
    .select(
        "customer",
        "order_id",
        "order_date",
        "total_amount",
        "first_amount_for_customer",
        "last_amount_so_far",
        "final_amount_for_customer",
    )
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 10. Explicit ROWS frames --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A ROWS frame can define a moving window around the current row.

This example computes a 2-row moving sum per customer:
+ current order
+ one previous order from the same customer
'''

out_sql = lf_orders.sql(
    """
    SELECT
        customer,
        order_id,
        order_date,
        total_amount,
        total_amount
            + COALESCE(
                LAG(total_amount) OVER (
                    PARTITION BY customer_id
                    ORDER BY order_date, order_id
                ),
                0
            ) AS current_plus_previous_amount
    FROM self
    ORDER BY customer_id, order_date, order_id
    """
)
print(out_sql.collect())
# shape: (15, 5)
# ┌──────────┬──────────┬────────────┬──────────────┬──────────────────────────────┐
# │ customer ┆ order_id ┆ order_date ┆ total_amount ┆ current_plus_previous_amount │
# │ ---      ┆ ---      ┆ ---        ┆ ---          ┆ ---                          │
# │ str      ┆ i64      ┆ date       ┆ f64          ┆ f64                          │
# ╞══════════╪══════════╪════════════╪══════════════╪══════════════════════════════╡
# │ Alice    ┆ 1001     ┆ 2024-01-03 ┆ 221.000      ┆ 221.000                      │
# │ Alice    ┆ 1003     ┆ 2024-02-10 ┆ 220.500      ┆ 441.500                      │
# │ Alice    ┆ 1007     ┆ 2024-03-20 ┆ 170.250      ┆ 390.750                      │
# │ Alice    ┆ 1012     ┆ 2024-05-15 ┆ 65.000       ┆ 235.250                      │
# │ Bob      ┆ 1002     ┆ 2024-01-05 ┆ 39.000       ┆ 39.000                       │
# │ …        ┆ …        ┆ …          ┆ …            ┆ …                            │
# │ Evan     ┆ 1011     ┆ 2024-05-01 ┆ 109.000      ┆ 519.000                      │
# │ Fiona    ┆ 1009     ┆ 2024-04-10 ┆ 612.000      ┆ 612.000                      │
# │ Fiona    ┆ 1013     ┆ 2024-05-20 ┆ 233.000      ┆ 845.000                      │
# │ Gina     ┆ 1014     ┆ 2024-06-03 ┆ 692.000      ┆ 692.000                      │
# │ Henry    ┆ 1015     ┆ 2024-06-08 ┆ 214.000      ┆ 214.000                      │
# └──────────┴──────────┴────────────┴──────────────┴──────────────────────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .sort("customer_id", "order_date", "order_id")
    .with_columns(
        c("total_amount").rolling_sum(window_size=2, min_samples=1).over("customer_id").alias("current_plus_previous_amount")
    )
    .select(
        "customer",
        "order_id",
        "order_date",
        "total_amount",
        "current_plus_previous_amount",
    )
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 11. Whole-table windows -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
An empty window OVER () means "use all rows as one window".

This is useful for percentages of total, global counts, and comparing each row
to the whole table average.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        customer,
        region,
        total_amount,
        COUNT(*) OVER () AS n_all_orders,
        SUM(total_amount) OVER () AS all_sales,
        total_amount / SUM(total_amount) OVER () AS share_of_all_sales,
        AVG(total_amount) OVER () AS global_avg_order
    FROM self
    ORDER BY order_id
    """
)
print(out_sql.collect())
# shape: (15, 8)
# ┌──────────┬──────────┬────────┬──────────────┬──────────────┬───────────┬────────────────────┬──────────────────┐
# │ order_id ┆ customer ┆ region ┆ total_amount ┆ n_all_orders ┆ all_sales ┆ share_of_all_sales ┆ global_avg_order │
# │ ---      ┆ ---      ┆ ---    ┆ ---          ┆ ---          ┆ ---       ┆ ---                ┆ ---              │
# │ i64      ┆ str      ┆ str    ┆ f64          ┆ u32          ┆ f64       ┆ f64                ┆ f64              │
# ╞══════════╪══════════╪════════╪══════════════╪══════════════╪═══════════╪════════════════════╪══════════════════╡
# │ 1001     ┆ Alice    ┆ East   ┆ 221.000      ┆ 15           ┆ 3976.250  ┆ 0.056              ┆ 265.083          │
# │ 1002     ┆ Bob      ┆ West   ┆ 39.000       ┆ 15           ┆ 3976.250  ┆ 0.010              ┆ 265.083          │
# │ 1003     ┆ Alice    ┆ East   ┆ 220.500      ┆ 15           ┆ 3976.250  ┆ 0.055              ┆ 265.083          │
# │ 1004     ┆ Diana    ┆ North  ┆ 349.500      ┆ 15           ┆ 3976.250  ┆ 0.088              ┆ 265.083          │
# │ 1005     ┆ Bob      ┆ West   ┆ 144.000      ┆ 15           ┆ 3976.250  ┆ 0.036              ┆ 265.083          │
# │ …        ┆ …        ┆ …      ┆ …            ┆ …            ┆ …         ┆ …                  ┆ …                │
# │ 1011     ┆ Evan     ┆ North  ┆ 109.000      ┆ 15           ┆ 3976.250  ┆ 0.027              ┆ 265.083          │
# │ 1012     ┆ Alice    ┆ East   ┆ 65.000       ┆ 15           ┆ 3976.250  ┆ 0.016              ┆ 265.083          │
# │ 1013     ┆ Fiona    ┆ South  ┆ 233.000      ┆ 15           ┆ 3976.250  ┆ 0.059              ┆ 265.083          │
# │ 1014     ┆ Gina     ┆ South  ┆ 692.000      ┆ 15           ┆ 3976.250  ┆ 0.174              ┆ 265.083          │
# │ 1015     ┆ Henry    ┆ East   ┆ 214.000      ┆ 15           ┆ 3976.250  ┆ 0.054              ┆ 265.083          │
# └──────────┴──────────┴────────┴──────────────┴──────────────┴───────────┴────────────────────┴──────────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .with_columns(
        pl.len().over().alias("n_all_orders"),
        c("total_amount").sum().over().alias("all_sales"),
        c("total_amount").mean().over().alias("global_avg_order"),
    )
    .with_columns(
        (c("total_amount") / c("all_sales")).alias("share_of_all_sales")
    )
    .select(
        "order_id",
        "customer",
        "region",
        "total_amount",
        "n_all_orders",
        "all_sales",
        "share_of_all_sales",
        "global_avg_order",
    )
    .sort("order_id")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 12. WHERE vs QUALIFY --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
WHERE filters input rows before the window function sees them.
QUALIFY filters output rows after the window function is computed.

Example below:
1. WHERE status = 'paid' limits the input to paid orders.
2. ROW_NUMBER ranks paid orders per customer.
3. QUALIFY keeps only each customer's highest-value paid order.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        customer_id,
        customer,
        order_id,
        status,
        product,
        total_amount
    FROM self
    WHERE status = 'paid'
    WINDOW paid_value_window AS (
        PARTITION BY customer_id
        ORDER BY (0 - total_amount), order_id
    )
    QUALIFY ROW_NUMBER() OVER paid_value_window = 1
    ORDER BY customer
    """
)
print(out_sql.collect())
# shape: (7, 6)
# ┌─────────────┬──────────┬──────────┬────────┬──────────┬──────────────┐
# │ customer_id ┆ customer ┆ order_id ┆ status ┆ product  ┆ total_amount │
# │ ---         ┆ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---          │
# │ i64         ┆ str      ┆ i64      ┆ str    ┆ str      ┆ f64          │
# ╞═════════════╪══════════╪══════════╪════════╪══════════╪══════════════╡
# │ 1           ┆ Alice    ┆ 1001     ┆ paid   ┆ Keyboard ┆ 221.000      │
# │ 2           ┆ Bob      ┆ 1005     ┆ paid   ┆ Mouse    ┆ 144.000      │
# │ 3           ┆ Diana    ┆ 1008     ┆ paid   ┆ Desk     ┆ 372.000      │
# │ 4           ┆ Evan     ┆ 1006     ┆ paid   ┆ Monitor  ┆ 410.000      │
# │ 5           ┆ Fiona    ┆ 1009     ┆ paid   ┆ Desk     ┆ 612.000      │
# │ 6           ┆ Gina     ┆ 1014     ┆ paid   ┆ Desk     ┆ 692.000      │
# │ 7           ┆ Henry    ┆ 1015     ┆ paid   ┆ Mouse    ┆ 214.000      │
# └─────────────┴──────────┴──────────┴────────┴──────────┴──────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .filter(c("status") == "paid")
    .sort("customer_id", "total_amount", "order_id", descending=[False, True, False])
    .with_columns(
        c("order_id").cum_count().over("customer_id").alias("paid_value_row_number")
    )
    .filter(c("paid_value_row_number") == 1)
    .select("customer", "order_id", "status", "product", "total_amount")
    .sort("customer")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 13. SQLContext example --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
SQLContext works the same way, except the table name is the registered table name
instead of self.
'''

ctx = pl.SQLContext(orders=lf_orders)

out_sql = ctx.execute(
    """
    SELECT
        customer,
        order_id,
        product,
        region,
        total_amount,
        RANK() OVER (
            PARTITION BY region
            ORDER BY total_amount DESC
        ) AS rank_in_region
    FROM orders
    QUALIFY RANK() OVER (
        PARTITION BY region
        ORDER BY total_amount DESC
    ) <= 3
    ORDER BY region, rank_in_region, order_id
    """
)
print(out_sql.collect())
# shape: (12, 6)
# ┌──────────┬──────────┬──────────┬────────┬──────────────┬────────────────┐
# │ customer ┆ order_id ┆ product  ┆ region ┆ total_amount ┆ rank_in_region │
# │ ---      ┆ ---      ┆ ---      ┆ ---    ┆ ---          ┆ ---            │
# │ str      ┆ i64      ┆ str      ┆ str    ┆ f64          ┆ u32            │
# ╞══════════╪══════════╪══════════╪════════╪══════════════╪════════════════╡
# │ Alice    ┆ 1001     ┆ Keyboard ┆ East   ┆ 221.000      ┆ 1              │
# │ Alice    ┆ 1003     ┆ Monitor  ┆ East   ┆ 220.500      ┆ 2              │
# │ Henry    ┆ 1015     ┆ Mouse    ┆ East   ┆ 214.000      ┆ 3              │
# │ Evan     ┆ 1006     ┆ Monitor  ┆ North  ┆ 410.000      ┆ 1              │
# │ Diana    ┆ 1008     ┆ Desk     ┆ North  ┆ 372.000      ┆ 2              │
# │ …        ┆ …        ┆ …        ┆ …      ┆ …            ┆ …              │
# │ Fiona    ┆ 1009     ┆ Desk     ┆ South  ┆ 612.000      ┆ 2              │
# │ Fiona    ┆ 1013     ┆ Monitor  ┆ South  ┆ 233.000      ┆ 3              │
# │ Bob      ┆ 1005     ┆ Mouse    ┆ West   ┆ 144.000      ┆ 1              │
# │ Bob      ┆ 1010     ┆ Keyboard ┆ West   ┆ 125.000      ┆ 2              │
# │ Bob      ┆ 1002     ┆ Mouse    ┆ West   ┆ 39.000       ┆ 3              │
# └──────────┴──────────┴──────────┴────────┴──────────────┴────────────────┘


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 14. Common mistakes ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Common SQL window-function mistakes:

1. Confusing GROUP BY and OVER.

   GROUP BY collapses rows:
       SELECT customer_id, SUM(total_amount)
       FROM self
       GROUP BY customer_id

   OVER keeps rows:
       SELECT order_id, customer_id,
              SUM(total_amount) OVER (PARTITION BY customer_id)
       FROM self

2. Forgetting ORDER BY inside ordered windows.

   ROW_NUMBER, RANK, DENSE_RANK, LAG, and LEAD are usually meaningful only when
   the window has a clear ORDER BY.

3. Filtering window results with WHERE.

   WHERE runs before windows exist.
   Use QUALIFY for conditions based on window functions.

4. Expecting RANK and DENSE_RANK to behave the same with ties.

   RANK leaves gaps after ties.
   DENSE_RANK does not leave gaps.

5. Expecting ROW_NUMBER to handle ties automatically.

   ROW_NUMBER always assigns unique numbers. Add tie-breaker columns to ORDER BY
   when deterministic ordering matters:
       ORDER BY total_amount DESC, order_id

6. Misunderstanding LAST_VALUE.

   With an ordered cumulative frame, LAST_VALUE means "last value so far".
   To get the final partition value, specify a frame ending at UNBOUNDED FOLLOWING.

7. Relying on output order from window ORDER BY.

   ORDER BY inside OVER controls calculation order inside the window.
   It does not replace the outer query ORDER BY that controls final row display.

8. Forgetting that Polars SQL uses ROWS-style default window framing.

   When exact frame behavior matters, write the frame explicitly.
'''
