'''
Polars SQL aggregation, GROUP BY, GROUP BY ALL, HAVING, and aggregate FILTER.

Main ideas:
1. Aggregate functions reduce many rows into one summary row.
2. GROUP BY creates one summary row per group key or key combination.
3. GROUP BY ALL automatically groups by all non-aggregate projected columns.
4. WHERE filters input rows BEFORE aggregation.
5. HAVING filters grouped summary rows AFTER aggregation.
6. FILTER (WHERE ...) attached to one aggregate lets different aggregates use
   different row subsets in the same query.
7. COUNT(*) counts rows, while COUNT(column) counts non-null values in that column.
8. COUNT(DISTINCT column) counts unique non-null values.

Important Polars SQL notes:
+ Frame-level .sql(...) registers the frame as the SQL table named self.
+ LazyFrame.sql(...) returns a LazyFrame, so call .collect() to materialize it.
+ Grouping keys remain normal output columns; there is no pandas-style index.
+ Use ORDER BY after GROUP BY when deterministic result order matters.
+ Polars SQL supports aggregate functions such as COUNT, SUM, AVG, MIN, MAX,
  MEDIAN, STDDEV, VARIANCE, QUANTILE_CONT, QUANTILE_DISC, CORR, COVAR,
  FIRST, LAST, and STRING_AGG.
+ Window functions are not the focus here; they are covered in the later
  SQL window/ranking file.
'''

import datetime as dt

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(25)
pl.Config.set_tbl_cols(9)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(120)


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 0. Setup data ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The examples are self-contained so this file can run without external datasets.

The order table intentionally includes:
+ categorical keys: region, product, status
+ boolean values: priority
+ nullable values: promo_code, customer_rating, and one null region
+ numeric values that we aggregate later

We derive gross_amount, discount_amount, net_amount, and total_amount using native
Polars once, then use SQL to aggregate those columns.
'''

df_orders = pl.DataFrame(
    {
        "order_id": [
            1001, 1002, 1003, 1004, 1005,
            1006, 1007, 1008, 1009, 1010,
            1011, 1012, 1013, 1014, 1015,
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
        "promo_code": [
            "VIP", None, "SPRING", None, "VIP",
            "SPRING", "VIP", None, "CLEARANCE", None,
            "VIP", "CLEARANCE", None, "SPRING", None,
        ],
        "customer_rating": [5, None, 4, 3, None, 5, None, 4, 5, None, 3, 5, 2, 4, None],
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

# Add derived numeric columns in a few separate steps so each new column can
# safely depend on columns created earlier.
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
# shape: (15, 17)
# ┌──────────┬──────────┬────────┬──────────┬──────────┬───┬──────────────┬─────────────────┬────────────┬──────────────┐
# │ order_id ┆ customer ┆ region ┆ product  ┆ quantity ┆ … ┆ gross_amount ┆ discount_amount ┆ net_amount ┆ total_amount │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---      ┆   ┆ ---          ┆ ---             ┆ ---        ┆ ---          │
# │ i64      ┆ str      ┆ str    ┆ str      ┆ i64      ┆   ┆ f64          ┆ f64             ┆ f64        ┆ f64          │
# ╞══════════╪══════════╪════════╪══════════╪══════════╪═══╪══════════════╪═════════════════╪════════════╪══════════════╡
# │ 1001     ┆ Alice    ┆ East   ┆ Keyboard ┆ 2        ┆ … ┆ 240.000      ┆ 24.000          ┆ 216.000    ┆ 221.000      │
# │ 1002     ┆ Bob      ┆ West   ┆ Mouse    ┆ 1        ┆ … ┆ 35.000       ┆ 0.000           ┆ 35.000     ┆ 39.000       │
# │ 1003     ┆ Alice    ┆ East   ┆ Monitor  ┆ 1        ┆ … ┆ 250.000      ┆ 37.500          ┆ 212.500    ┆ 220.500      │
# │ 1004     ┆ Diana    ┆ North  ┆ Keyboard ┆ 3        ┆ … ┆ 360.000      ┆ 18.000          ┆ 342.000    ┆ 349.500      │
# │ 1005     ┆ Bob      ┆ West   ┆ Mouse    ┆ 4        ┆ … ┆ 140.000      ┆ 0.000           ┆ 140.000    ┆ 144.000      │
# │ 1006     ┆ Evan     ┆ North  ┆ Monitor  ┆ 2        ┆ … ┆ 500.000      ┆ 100.000         ┆ 400.000    ┆ 410.000      │
# │ 1007     ┆ Alice    ┆ East   ┆ Mouse    ┆ 5        ┆ … ┆ 175.000      ┆ 8.750           ┆ 166.250    ┆ 170.250      │
# │ 1008     ┆ Diana    ┆ North  ┆ Desk     ┆ 1        ┆ … ┆ 400.000      ┆ 40.000          ┆ 360.000    ┆ 372.000      │
# │ 1009     ┆ Fiona    ┆ South  ┆ Desk     ┆ 2        ┆ … ┆ 800.000      ┆ 200.000         ┆ 600.000    ┆ 612.000      │
# │ 1010     ┆ Bob      ┆ West   ┆ Keyboard ┆ 1        ┆ … ┆ 120.000      ┆ 0.000           ┆ 120.000    ┆ 125.000      │
# │ 1011     ┆ Evan     ┆ North  ┆ Mouse    ┆ 3        ┆ … ┆ 105.000      ┆ 0.000           ┆ 105.000    ┆ 109.000      │
# │ 1012     ┆ Alice    ┆ East   ┆ Keyboard ┆ 1        ┆ … ┆ 120.000      ┆ 60.000          ┆ 60.000     ┆ 65.000       │
# │ 1013     ┆ Fiona    ┆ South  ┆ Monitor  ┆ 1        ┆ … ┆ 250.000      ┆ 25.000          ┆ 225.000    ┆ 233.000      │
# │ 1014     ┆ Gina     ┆ null   ┆ Desk     ┆ 2        ┆ … ┆ 800.000      ┆ 120.000         ┆ 680.000    ┆ 692.000      │
# │ 1015     ┆ Henry    ┆ East   ┆ Mouse    ┆ 6        ┆ … ┆ 210.000      ┆ 0.000           ┆ 210.000    ┆ 214.000      │
# └──────────┴──────────┴────────┴──────────┴──────────┴───┴──────────────┴─────────────────┴────────────┴──────────────┘

print(df_orders.schema)


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. Whole-table aggregation -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A SELECT with only aggregate expressions returns one summary row for the whole table.

COUNT(*) counts rows.
COUNT(promo_code) counts non-null promo_code values.
COUNT(DISTINCT customer) counts unique non-null customers.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        COUNT(*) AS n_orders,
        COUNT(promo_code) AS n_orders_with_promo,
        COUNT(DISTINCT customer) AS n_unique_customers,
        SUM(total_amount) AS total_sales,
        AVG(total_amount) AS avg_order_value,
        MIN(total_amount) AS min_order_value,
        MAX(total_amount) AS max_order_value
    FROM self
    """
)
print(out_sql.collect())
# shape: (1, 7)
# ┌──────────┬───────────────────┬───────────────────┬─────────────┬─────────────────┬─────────────────┬─────────────────┐
# │ n_orders ┆ n_orders_with_pro ┆ n_unique_customer ┆ total_sales ┆ avg_order_value ┆ min_order_value ┆ max_order_value │
# │ ---      ┆ mo                ┆ s                 ┆ ---         ┆ ---             ┆ ---             ┆ ---             │
# │ u32      ┆ ---               ┆ ---               ┆ f64         ┆ f64             ┆ f64             ┆ f64             │
# │          ┆ u32               ┆ u32               ┆             ┆                 ┆                 ┆                 │
# ╞══════════╪═══════════════════╪═══════════════════╪═════════════╪═════════════════╪═════════════════╪═════════════════╡
# │ 15       ┆ 9                 ┆ 7                 ┆ 3976.250    ┆ 265.083         ┆ 39.000          ┆ 692.000         │
# └──────────┴───────────────────┴───────────────────┴─────────────┴─────────────────┴─────────────────┴─────────────────┘

# Native Polars equivalent.
out_native = lf_orders.select(
    pl.len().alias("n_orders"),
    c("promo_code").count().alias("n_orders_with_promo"),
    c("customer").n_unique().alias("n_unique_customers"),
    c("total_amount").sum().alias("total_sales"),
    c("total_amount").mean().alias("avg_order_value"),
    c("total_amount").min().alias("min_order_value"),
    c("total_amount").max().alias("max_order_value"),
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 2. COUNT(*) vs COUNT(column) -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
COUNT(column) ignores null values in that column.

Here customer_rating has nulls, so COUNT(*) and COUNT(customer_rating) differ.
AVG(customer_rating) also ignores null ratings.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        COUNT(*) AS n_rows,
        COUNT(customer_rating) AS n_rated_orders,
        AVG(customer_rating) AS avg_rating,
        MIN(customer_rating) AS min_rating,
        MAX(customer_rating) AS max_rating
    FROM self
    """
)
print(out_sql.collect())
# shape: (1, 5)
# ┌────────┬────────────────┬────────────┬────────────┬────────────┐
# │ n_rows ┆ n_rated_orders ┆ avg_rating ┆ min_rating ┆ max_rating │
# │ ---    ┆ ---            ┆ ---        ┆ ---        ┆ ---        │
# │ u32    ┆ u32            ┆ f64        ┆ i64        ┆ i64        │
# ╞════════╪════════════════╪════════════╪════════════╪════════════╡
# │ 15     ┆ 10             ┆ 4.000      ┆ 2          ┆ 5          │
# └────────┴────────────────┴────────────┴────────────┴────────────┘

# Native Polars equivalent.
out_native = lf_orders.select(
    pl.len().alias("n_rows"),
    c("customer_rating").count().alias("n_rated_orders"),
    c("customer_rating").mean().alias("avg_rating"),
    c("customer_rating").min().alias("min_rating"),
    c("customer_rating").max().alias("max_rating"),
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 3. GROUP BY one key -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
GROUP BY creates one summary row for each unique key value.

Polars does not guarantee group output order unless you sort explicitly, so use
ORDER BY when teaching or reporting.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        region,
        COUNT(*) AS n_orders,
        SUM(total_amount) AS total_sales,
        AVG(total_amount) AS avg_order_value
    FROM self
    GROUP BY region
    ORDER BY region NULLS LAST
    """
)
print(out_sql.collect())
# shape: (5, 4)
# ┌────────┬──────────┬─────────────┬─────────────────┐
# │ region ┆ n_orders ┆ total_sales ┆ avg_order_value │
# │ ---    ┆ ---      ┆ ---         ┆ ---             │
# │ str    ┆ u32      ┆ f64         ┆ f64             │
# ╞════════╪══════════╪═════════════╪═════════════════╡
# │ East   ┆ 5        ┆ 890.750     ┆ 178.150         │
# │ North  ┆ 4        ┆ 1240.500    ┆ 310.125         │
# │ South  ┆ 2        ┆ 845.000     ┆ 422.500         │
# │ West   ┆ 3        ┆ 308.000     ┆ 102.667         │
# │ null   ┆ 1        ┆ 692.000     ┆ 692.000         │
# └────────┴──────────┴─────────────┴─────────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .group_by("region")
    .agg(
        pl.len().alias("n_orders"),
        c("total_amount").sum().alias("total_sales"),
        c("total_amount").mean().alias("avg_order_value"),
    )
    .sort("region", nulls_last=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------- 4. Multiple aggregates per group ---------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A single grouped SELECT can compute many summary columns.

Common aggregate functions:
+ SUM, AVG, MIN, MAX
+ MEDIAN
+ STDDEV / VARIANCE
+ FIRST / LAST
'''

out_sql = lf_orders.sql(
    """
    SELECT
        product,
        COUNT(*) AS n_orders,
        SUM(quantity) AS units_sold,
        SUM(total_amount) AS total_sales,
        AVG(total_amount) AS avg_order_value,
        MIN(total_amount) AS min_order_value,
        MAX(total_amount) AS max_order_value,
        MEDIAN(total_amount) AS median_order_value,
        STDDEV(total_amount) AS std_order_value,
        VARIANCE(total_amount) AS var_order_value
    FROM self
    GROUP BY product
    ORDER BY total_sales DESC
    """
)
print(out_sql.collect())
# shape: (4, 10)
# ┌──────────┬──────────┬────────────┬─────────────┬─────────────┬───┬────────────┬────────────┬────────────┬────────────┐
# │ product  ┆ n_orders ┆ units_sold ┆ total_sales ┆ avg_order_v ┆ … ┆ max_order_ ┆ median_ord ┆ std_order_ ┆ var_order_ │
# │ ---      ┆ ---      ┆ ---        ┆ ---         ┆ alue        ┆   ┆ value      ┆ er_value   ┆ value      ┆ value      │
# │ str      ┆ u32      ┆ i64        ┆ f64         ┆ ---         ┆   ┆ ---        ┆ ---        ┆ ---        ┆ ---        │
# │          ┆          ┆            ┆             ┆ f64         ┆   ┆ f64        ┆ f64        ┆ f64        ┆ f64        │
# ╞══════════╪══════════╪════════════╪═════════════╪═════════════╪═══╪════════════╪════════════╪════════════╪════════════╡
# │ Desk     ┆ 3        ┆ 5          ┆ 1676.000    ┆ 558.667     ┆ … ┆ 692.000    ┆ 612.000    ┆ 166.533    ┆ 27733.333  │
# │ Monitor  ┆ 3        ┆ 4          ┆ 863.500     ┆ 287.833     ┆ … ┆ 410.000    ┆ 233.000    ┆ 105.984    ┆ 11232.583  │
# │ Keyboard ┆ 4        ┆ 7          ┆ 760.500     ┆ 190.125     ┆ … ┆ 349.500    ┆ 173.000    ┆ 124.165    ┆ 15417.062  │
# │ Mouse    ┆ 5        ┆ 19         ┆ 676.250     ┆ 135.250     ┆ … ┆ 214.000    ┆ 144.000    ┆ 66.061     ┆ 4364.062   │
# └──────────┴──────────┴────────────┴─────────────┴─────────────┴───┴────────────┴────────────┴────────────┴────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .group_by("product")
    .agg(
        pl.len().alias("n_orders"),
        c("quantity").sum().alias("units_sold"),
        c("total_amount").sum().alias("total_sales"),
        c("total_amount").mean().alias("avg_order_value"),
        c("total_amount").min().alias("min_order_value"),
        c("total_amount").max().alias("max_order_value"),
        c("total_amount").median().alias("median_order_value"),
        c("total_amount").std().alias("std_order_value"),
        c("total_amount").var().alias("var_order_value"),
    )
    .sort("total_sales", descending=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 5. GROUP BY multiple keys --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Use multiple columns in GROUP BY to create one row per key combination.

This is the SQL equivalent of Polars:
    .group_by("region", "status")
'''

out_sql = lf_orders.sql(
    """
    SELECT
        region,
        status,
        COUNT(*) AS n_orders,
        SUM(total_amount) AS total_sales
    FROM self
    GROUP BY region, status
    ORDER BY region NULLS LAST, status
    """
)
print(out_sql.collect())
# shape: (8, 4)
# ┌────────┬───────────┬──────────┬─────────────┐
# │ region ┆ status    ┆ n_orders ┆ total_sales │
# │ ---    ┆ ---       ┆ ---      ┆ ---         │
# │ str    ┆ str       ┆ u32      ┆ f64         │
# ╞════════╪═══════════╪══════════╪═════════════╡
# │ East   ┆ cancelled ┆ 1        ┆ 170.250     │
# │ East   ┆ paid      ┆ 4        ┆ 720.500     │
# │ North  ┆ paid      ┆ 4        ┆ 1240.500    │
# │ South  ┆ paid      ┆ 1        ┆ 612.000     │
# │ South  ┆ refunded  ┆ 1        ┆ 233.000     │
# │ West   ┆ paid      ┆ 1        ┆ 144.000     │
# │ West   ┆ pending   ┆ 2        ┆ 164.000     │
# │ null   ┆ paid      ┆ 1        ┆ 692.000     │
# └────────┴───────────┴──────────┴─────────────┘


# Native Polars equivalent.
out_native = (
    lf_orders
    .group_by("region", "status")
    .agg(
        pl.len().alias("n_orders"),
        c("total_amount").sum().alias("total_sales"),
    )
    .sort(["region", "status"], nulls_last=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 6. GROUP BY ALL -------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
GROUP BY ALL is a Polars SQL convenience.

It groups by all projected columns that are NOT aggregate expressions, window
expressions, or literal values.

This avoids repeating the same key columns in SELECT and GROUP BY.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        region,
        status,
        SUM(total_amount) AS total_sales,
        COUNT(*) AS n_orders
    FROM self
    GROUP BY ALL
    ORDER BY region NULLS LAST, status
    """
)
print(out_sql.collect())
# shape: (8, 4)
# ┌────────┬───────────┬─────────────┬──────────┐
# │ region ┆ status    ┆ total_sales ┆ n_orders │
# │ ---    ┆ ---       ┆ ---         ┆ ---      │
# │ str    ┆ str       ┆ f64         ┆ u32      │
# ╞════════╪═══════════╪═════════════╪══════════╡
# │ East   ┆ cancelled ┆ 170.250     ┆ 1        │
# │ East   ┆ paid      ┆ 720.500     ┆ 4        │
# │ North  ┆ paid      ┆ 1240.500    ┆ 4        │
# │ South  ┆ paid      ┆ 612.000     ┆ 1        │
# │ South  ┆ refunded  ┆ 233.000     ┆ 1        │
# │ West   ┆ paid      ┆ 144.000     ┆ 1        │
# │ West   ┆ pending   ┆ 164.000     ┆ 2        │
# │ null   ┆ paid      ┆ 692.000     ┆ 1        │
# └────────┴───────────┴─────────────┴──────────┘

# Native Polars equivalent: write the grouping keys explicitly.
out_native = (
    lf_orders
    .group_by("region", "status")
    .agg(
        c("total_amount").sum().alias("total_sales"),
        pl.len().alias("n_orders"),
    )
    .sort(["region", "status"], nulls_last=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 7. WHERE before GROUP BY -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
WHERE filters rows before aggregation.

Example:
    only aggregate completed paid orders.

Rows with status = pending/cancelled/refunded are removed before GROUP BY sees them.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        region,
        COUNT(*) AS n_paid_orders,
        SUM(total_amount) AS paid_sales
    FROM self
    WHERE status = 'paid'
    GROUP BY region
    ORDER BY region NULLS LAST
    """
)
print(out_sql.collect())
# shape: (5, 3)
# ┌────────┬───────────────┬────────────┐
# │ region ┆ n_paid_orders ┆ paid_sales │
# │ ---    ┆ ---           ┆ ---        │
# │ str    ┆ u32           ┆ f64        │
# ╞════════╪═══════════════╪════════════╡
# │ East   ┆ 4             ┆ 720.500    │
# │ North  ┆ 4             ┆ 1240.500   │
# │ South  ┆ 1             ┆ 612.000    │
# │ West   ┆ 1             ┆ 144.000    │
# │ null   ┆ 1             ┆ 692.000    │
# └────────┴───────────────┴────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .filter(c("status") == "paid")
    .group_by("region")
    .agg(
        pl.len().alias("n_paid_orders"),
        c("total_amount").sum().alias("paid_sales"),
    )
    .sort("region", nulls_last=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 8. HAVING after GROUP BY -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
HAVING filters groups after aggregation.

Use WHERE for row-level conditions.
Use HAVING for group-level conditions such as:
    SUM(total_amount) >= 500
    COUNT(*) >= 2
'''

out_sql = lf_orders.sql(
    """
    SELECT
        region,
        COUNT(*) AS n_orders,
        SUM(total_amount) AS total_sales
    FROM self
    GROUP BY region
    HAVING SUM(total_amount) >= 500 AND COUNT(*) >= 2
    ORDER BY total_sales DESC
    """
)
print(out_sql.collect())
# shape: (3, 3)
# ┌────────┬──────────┬─────────────┐
# │ region ┆ n_orders ┆ total_sales │
# │ ---    ┆ ---      ┆ ---         │
# │ str    ┆ u32      ┆ f64         │
# ╞════════╪══════════╪═════════════╡
# │ North  ┆ 4        ┆ 1240.500    │
# │ East   ┆ 5        ┆ 890.750     │
# │ South  ┆ 2        ┆ 845.000     │
# └────────┴──────────┴─────────────┘

# Native Polars equivalent: aggregate first, then filter the aggregated result.
out_native = (
    lf_orders
    .group_by("region")
    .agg(
        pl.len().alias("n_orders"),
        c("total_amount").sum().alias("total_sales"),
    )
    .filter((c("total_sales") >= 500) & (c("n_orders") >= 2))
    .sort("total_sales", descending=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 9. WHERE and HAVING together ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
WHERE and HAVING can appear in the same query.

Execution idea:
1. FROM self
2. WHERE status = 'paid'
3. GROUP BY product
4. HAVING SUM(total_amount) >= 200
5. SELECT / ORDER BY output
'''

out_sql = lf_orders.sql(
    """
    SELECT
        product,
        COUNT(*) AS n_paid_orders,
        SUM(total_amount) AS paid_sales
    FROM self
    WHERE status = 'paid'
    GROUP BY product
    HAVING SUM(total_amount) >= 200
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
    .group_by("product")
    .agg(
        pl.len().alias("n_paid_orders"),
        c("total_amount").sum().alias("paid_sales"),
    )
    .filter(c("paid_sales") >= 200)
    .sort("paid_sales", descending=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 10. Aggregate FILTER (WHERE ...) ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
An aggregate-level FILTER lets different summary columns use different subsets
of rows in the same grouped query.

This is different from query-level WHERE:
+ WHERE removes rows for the entire query.
+ FILTER (WHERE ...) removes rows only for that one aggregate expression.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        region,
        COUNT(*) AS n_all_orders,
        SUM(total_amount) AS all_sales,
        SUM(total_amount) FILTER (WHERE status = 'paid') AS paid_sales,
        SUM(total_amount) FILTER (WHERE status <> 'paid') AS non_paid_sales,
        COUNT(*) FILTER (WHERE priority) AS n_priority_orders,
        AVG(customer_rating) FILTER (WHERE customer_rating IS NOT NULL) AS avg_rating
    FROM self
    GROUP BY region
    ORDER BY region NULLS LAST
    """
)
print(out_sql.collect())
# shape: (5, 7)
# ┌────────┬──────────────┬───────────┬────────────┬────────────────┬───────────────────┬────────────┐
# │ region ┆ n_all_orders ┆ all_sales ┆ paid_sales ┆ non_paid_sales ┆ n_priority_orders ┆ avg_rating │
# │ ---    ┆ ---          ┆ ---       ┆ ---        ┆ ---            ┆ ---               ┆ ---        │
# │ str    ┆ u32          ┆ f64       ┆ f64        ┆ f64            ┆ u32               ┆ f64        │
# ╞════════╪══════════════╪═══════════╪════════════╪════════════════╪═══════════════════╪════════════╡
# │ East   ┆ 5            ┆ 890.750   ┆ 720.500    ┆ 170.250        ┆ 3                 ┆ 4.667      │
# │ North  ┆ 4            ┆ 1240.500  ┆ 1240.500   ┆ 0.000          ┆ 2                 ┆ 3.750      │
# │ South  ┆ 2            ┆ 845.000   ┆ 612.000    ┆ 233.000        ┆ 0                 ┆ 3.500      │
# │ West   ┆ 3            ┆ 308.000   ┆ 144.000    ┆ 164.000        ┆ 0                 ┆ null       │
# │ null   ┆ 1            ┆ 692.000   ┆ 692.000    ┆ 0.000          ┆ 1                 ┆ 4.000      │
# └────────┴──────────────┴───────────┴────────────┴────────────────┴───────────────────┴────────────┘

# Native Polars equivalent.
out_native = (
    lf_orders
    .group_by("region")
    .agg(
        pl.len().alias("n_all_orders"),
        c("total_amount").sum().alias("all_sales"),
        c("total_amount").filter(c("status") == "paid").sum().alias("paid_sales"),
        c("total_amount").filter(c("status") != "paid").sum().alias("non_paid_sales"),
        c("order_id").filter(c("priority")).count().alias("n_priority_orders"),
        c("customer_rating").filter(c("customer_rating").is_not_null()).mean().alias("avg_rating"),
    )
    .sort("region", nulls_last=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 11. Null group keys ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
By default, null values in a grouping key form their own null group.

If you do not want null-key groups, filter them out with WHERE before grouping.
'''

print(
    lf_orders.sql(
        """
        SELECT
            region,
            COUNT(*) AS n_orders,
            SUM(total_amount) AS total_sales
        FROM self
        GROUP BY region
        ORDER BY region NULLS LAST
        """
    ).collect()
)
# shape: (5, 3)
# ┌────────┬──────────┬─────────────┐
# │ region ┆ n_orders ┆ total_sales │
# │ ---    ┆ ---      ┆ ---         │
# │ str    ┆ u32      ┆ f64         │
# ╞════════╪══════════╪═════════════╡
# │ East   ┆ 5        ┆ 890.750     │
# │ North  ┆ 4        ┆ 1240.500    │
# │ South  ┆ 2        ┆ 845.000     │
# │ West   ┆ 3        ┆ 308.000     │
# │ null   ┆ 1        ┆ 692.000     │
# └────────┴──────────┴─────────────┘

print(
    lf_orders.sql(
        """
        SELECT
            region,
            COUNT(*) AS n_orders,
            SUM(total_amount) AS total_sales
        FROM self
        WHERE region IS NOT NULL
        GROUP BY region
        ORDER BY region
        """
    ).collect()
)
# shape: (4, 3)
# ┌────────┬──────────┬─────────────┐
# │ region ┆ n_orders ┆ total_sales │
# │ ---    ┆ ---      ┆ ---         │
# │ str    ┆ u32      ┆ f64         │
# ╞════════╪══════════╪═════════════╡
# │ East   ┆ 5        ┆ 890.750     │
# │ North  ┆ 4        ┆ 1240.500    │
# │ South  ┆ 2        ┆ 845.000     │
# │ West   ┆ 3        ┆ 308.000     │
# └────────┴──────────┴─────────────┘

# Native Polars equivalent for dropping null-key groups.
out_native = (
    lf_orders
    .drop_nulls("region")
    .group_by("region")
    .agg(
        pl.len().alias("n_orders"),
        c("total_amount").sum().alias("total_sales"),
    )
    .sort("region")
)

print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 12. FIRST, LAST, and STRING_AGG -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
FIRST and LAST return the first/last value in the group.

STRING_AGG concatenates string values inside each group.
It can use a custom delimiter, and Polars SQL also supports in-argument ORDER BY
and LIMIT for STRING_AGG.

Note:
    If first/last order matters, sort the input first in a subquery or CTE.
    A later file covers subqueries and CTEs in more detail.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        region,
        FIRST(customer) AS first_customer_seen,
        LAST(customer) AS last_customer_seen,
        STRING_AGG(product, ', ' ORDER BY total_amount DESC LIMIT 3) AS top_3_products_by_value
    FROM self
    WHERE region IS NOT NULL
    GROUP BY region
    ORDER BY region
    """
)
print(out_sql.collect())
# shape: (4, 4)
# ┌────────┬─────────────────────┬────────────────────┬──────────────────────────┐
# │ region ┆ first_customer_seen ┆ last_customer_seen ┆ top_3_products_by_value  │
# │ ---    ┆ ---                 ┆ ---                ┆ ---                      │
# │ str    ┆ str                 ┆ str                ┆ str                      │
# ╞════════╪═════════════════════╪════════════════════╪══════════════════════════╡
# │ East   ┆ Alice               ┆ Henry              ┆ Keyboard, Monitor, Mouse │
# │ North  ┆ Diana               ┆ Evan               ┆ Monitor, Desk, Keyboard  │
# │ South  ┆ Fiona               ┆ Fiona              ┆ Desk, Monitor            │
# │ West   ┆ Bob                 ┆ Bob                ┆ Mouse, Keyboard, Mouse   │
# └────────┴─────────────────────┴────────────────────┴──────────────────────────┘


#--------------------------------------------------------------------------------------------------------------#
#------------------------------- 13. Quantiles, correlation, and covariance -----------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Polars SQL supports statistical aggregate functions.

QUANTILE_CONT uses interpolation.
QUANTILE_DISC chooses a discrete observed value.
CORR and COVAR operate on two numeric columns.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        product,
        MEDIAN(total_amount) AS median_total,
        QUANTILE_CONT(total_amount, 0.75) AS q75_cont,
        QUANTILE_DISC(total_amount, 0.75) AS q75_disc,
        STDDEV(total_amount) AS std_total,
        VARIANCE(total_amount) AS var_total,
        CORR(quantity, total_amount) AS qty_total_corr,
        COVAR(quantity, total_amount) AS qty_total_covar
    FROM self
    GROUP BY product
    ORDER BY product
    """
)
print(out_sql.collect())
# shape: (4, 8)
# ┌──────────┬──────────────┬──────────┬──────────┬───────────┬───────────┬────────────────┬─────────────────┐
# │ product  ┆ median_total ┆ q75_cont ┆ q75_disc ┆ std_total ┆ var_total ┆ qty_total_corr ┆ qty_total_covar │
# │ ---      ┆ ---          ┆ ---      ┆ ---      ┆ ---       ┆ ---       ┆ ---            ┆ ---             │
# │ str      ┆ f64          ┆ f64      ┆ f64      ┆ f64       ┆ f64       ┆ f64            ┆ f64             │
# ╞══════════╪══════════════╪══════════╪══════════╪═══════════╪═══════════╪════════════════╪═════════════════╡
# │ Desk     ┆ 612.000      ┆ 652.000  ┆ 692.000  ┆ 166.533   ┆ 27733.333 ┆ 0.971          ┆ 93.333          │
# │ Keyboard ┆ 173.000      ┆ 253.125  ┆ 221.000  ┆ 124.165   ┆ 15417.062 ┆ 0.980          ┆ 116.542         │
# │ Monitor  ┆ 233.000      ┆ 321.500  ┆ 410.000  ┆ 105.984   ┆ 11232.583 ┆ 0.998          ┆ 61.083          │
# │ Mouse    ┆ 144.000      ┆ 170.250  ┆ 170.250  ┆ 66.061    ┆ 4364.062  ┆ 0.998          ┆ 126.875         │
# └──────────┴──────────────┴──────────┴──────────┴───────────┴───────────┴────────────────┴─────────────────┘

# Native Polars equivalent for the most common statistics.
# Exact quantile interpolation choices can differ by API/interpolation setting,
# so be explicit when you need exact parity.
out_native = (
    lf_orders
    .group_by("product")
    .agg(
        c("total_amount").median().alias("median_total"),
        c("total_amount").quantile(0.75, interpolation="linear").alias("q75_cont"),
        c("total_amount").quantile(0.75, interpolation="nearest").alias("q75_nearest"),
        c("total_amount").std().alias("std_total"),
        c("total_amount").var().alias("var_total"),
        pl.corr("quantity", "total_amount").alias("qty_total_corr"),
        pl.cov("quantity", "total_amount").alias("qty_total_covar"),
    )
    .sort("product")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 14. SQLContext example ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
SQLContext is useful when you want to register named tables.

The aggregation syntax is the same; only the table name changes from self to the
registered table name.
'''

ctx = pl.SQLContext(orders=lf_orders)

out_sql = ctx.execute(
    """
    SELECT
        region,
        product,
        COUNT(*) AS n_orders,
        SUM(total_amount) AS total_sales
    FROM orders
    WHERE status = 'paid'
    GROUP BY region, product
    HAVING SUM(total_amount) >= 100
    ORDER BY region NULLS LAST, total_sales DESC
    """
)

print(out_sql.collect())
# shape: (10, 4)
# ┌────────┬──────────┬──────────┬─────────────┐
# │ region ┆ product  ┆ n_orders ┆ total_sales │
# │ ---    ┆ ---      ┆ ---      ┆ ---         │
# │ str    ┆ str      ┆ u32      ┆ f64         │
# ╞════════╪══════════╪══════════╪═════════════╡
# │ East   ┆ Keyboard ┆ 2        ┆ 286.000     │
# │ East   ┆ Monitor  ┆ 1        ┆ 220.500     │
# │ East   ┆ Mouse    ┆ 1        ┆ 214.000     │
# │ North  ┆ Monitor  ┆ 1        ┆ 410.000     │
# │ North  ┆ Desk     ┆ 1        ┆ 372.000     │
# │ North  ┆ Keyboard ┆ 1        ┆ 349.500     │
# │ North  ┆ Mouse    ┆ 1        ┆ 109.000     │
# │ South  ┆ Desk     ┆ 1        ┆ 612.000     │
# │ West   ┆ Mouse    ┆ 1        ┆ 144.000     │
# │ null   ┆ Desk     ┆ 1        ┆ 692.000     │
# └────────┴──────────┴──────────┴─────────────┘


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 15. Common mistakes ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Common SQL aggregation mistakes:

1. Selecting a non-aggregated column that is not in GROUP BY.

   Usually invalid:
       SELECT region, product, SUM(total_amount)
       FROM self
       GROUP BY region

   Fix:
       GROUP BY region, product
   or remove product from SELECT.

2. Using WHERE for aggregate conditions.

   Invalid idea:
       WHERE SUM(total_amount) >= 500

   Fix:
       HAVING SUM(total_amount) >= 500

3. Forgetting that WHERE runs before aggregation.

   WHERE status = 'paid' changes the input rows.
   FILTER (WHERE status = 'paid') changes only one aggregate column.

4. Relying on group output order.

   Always add ORDER BY when row order matters.

5. Expecting pandas-style index behavior.

   Polars has no custom row index, so grouping keys remain ordinary columns.
'''
