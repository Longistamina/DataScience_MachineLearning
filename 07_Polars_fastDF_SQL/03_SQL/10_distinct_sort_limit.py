'''
Polars SQL DISTINCT, ORDER BY, ORDER BY ALL, LIMIT, OFFSET, and FETCH.

Main ideas:
1. SELECT DISTINCT removes duplicate rows from the selected output.
2. DISTINCT ON (...) keeps one row for each unique key or key combination.
3. ORDER BY sorts query results by one or more columns or expressions.
4. ORDER BY ALL sorts by every selected output column.
5. LIMIT keeps the first n rows of the current query result.
6. OFFSET skips rows before returning results.
7. FETCH FIRST / FETCH NEXT is the ANSI-style alternative to LIMIT.

Important Polars SQL notes:
+ Frame-level .sql(...) registers the frame as the SQL table named self.
+ LazyFrame.sql(...) returns a LazyFrame, so call .collect() to materialize it.
+ For deterministic top-n examples, combine ORDER BY with LIMIT or FETCH.
+ DISTINCT applies after SELECT expressions are computed.
+ DISTINCT ON (...) currently supports column names, not arbitrary expressions.
+ FETCH supports row limits, but WITH TIES and PERCENT are not currently supported.
+ Polars has no pandas-style row index. Row order should be made explicit with ORDER BY
  when the order matters.
'''

import datetime as dt

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(20)
pl.Config.set_tbl_cols(9)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(120)


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 0. Setup data --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The examples are self-contained so this file can run without external datasets.

We use:
+ df_dupes for simple DISTINCT examples;
+ lf_sales for realistic sorting, limiting, and top-n examples.
'''

df_dupes = pl.DataFrame(
    {
        "category": ["A", "A", "A", "B", "B", "B", "C"],
        "label": ["x", "x", "y", "p", "p", "q", "z"],
        "value": [10, 10, 20, 30, 30, 40, 50],
    }
)
print(df_dupes)
# shape: (7, 3)
# ┌──────────┬───────┬───────┐
# │ category ┆ label ┆ value │
# │ ---      ┆ ---   ┆ ---   │
# │ str      ┆ str   ┆ i64   │
# ╞══════════╪═══════╪═══════╡
# │ A        ┆ x     ┆ 10    │
# │ A        ┆ x     ┆ 10    │
# │ A        ┆ y     ┆ 20    │
# │ B        ┆ p     ┆ 30    │
# │ B        ┆ p     ┆ 30    │
# │ B        ┆ q     ┆ 40    │
# │ C        ┆ z     ┆ 50    │
# └──────────┴───────┴───────┘

df_sales = pl.DataFrame(
    {
        "order_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012],
        "customer": ["Alice", "Bob", "Alice", "Diana", "Bob", "Evan", "Alice", "Diana", "Fiona", "Bob", "Evan", "Alice"],
        "region": ["East", "West", "East", "North", "West", "North", "East", "North", "South", "West", "North", "East"],
        "product": ["Keyboard", "Mouse", "Monitor", "Keyboard", "Mouse", "Monitor", "Mouse", "Desk", "Desk", "Keyboard", "Mouse", "Keyboard"],
        "quantity": [2, 1, 1, 3, 4, 2, 5, 1, 2, 1, 3, 1],
        "unit_price": [120.0, 35.0, 250.0, 120.0, 35.0, 250.0, 35.0, 400.0, 400.0, 120.0, 35.0, 120.0],
        "discount_rate": [0.10, 0.00, 0.15, 0.05, 0.00, 0.20, 0.05, 0.10, 0.25, 0.00, 0.00, 0.50],
        "shipping_fee": [5.0, 4.0, 8.0, 7.5, 4.0, 10.0, 4.0, 12.0, 12.0, 5.0, 4.0, 5.0],
        "status": ["paid", "pending", "paid", "paid", "paid", "paid", "cancelled", "paid", "paid", "pending", "paid", "paid"],
        "priority": [True, False, True, False, False, True, False, True, False, False, False, True],
        "promo_code": ["VIP", None, "SPRING", None, "VIP", "SPRING", "VIP", None, "CLEARANCE", None, "VIP", "CLEARANCE"],
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
        ],
    }
)
print(df_sales)
# shape: (12, 12)
# ┌──────────┬──────────┬────────┬──────────┬──────────┬───┬───────────┬──────────┬────────────┬────────────┐
# │ order_id ┆ customer ┆ region ┆ product  ┆ quantity ┆ … ┆ status    ┆ priority ┆ promo_code ┆ order_date │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---      ┆   ┆ ---       ┆ ---      ┆ ---        ┆ ---        │
# │ i64      ┆ str      ┆ str    ┆ str      ┆ i64      ┆   ┆ str       ┆ bool     ┆ str        ┆ date       │
# ╞══════════╪══════════╪════════╪══════════╪══════════╪═══╪═══════════╪══════════╪════════════╪════════════╡
# │ 1001     ┆ Alice    ┆ East   ┆ Keyboard ┆ 2        ┆ … ┆ paid      ┆ true     ┆ VIP        ┆ 2024-01-03 │
# │ 1002     ┆ Bob      ┆ West   ┆ Mouse    ┆ 1        ┆ … ┆ pending   ┆ false    ┆ null       ┆ 2024-01-05 │
# │ 1003     ┆ Alice    ┆ East   ┆ Monitor  ┆ 1        ┆ … ┆ paid      ┆ true     ┆ SPRING     ┆ 2024-02-10 │
# │ 1004     ┆ Diana    ┆ North  ┆ Keyboard ┆ 3        ┆ … ┆ paid      ┆ false    ┆ null       ┆ 2024-02-12 │
# │ 1005     ┆ Bob      ┆ West   ┆ Mouse    ┆ 4        ┆ … ┆ paid      ┆ false    ┆ VIP        ┆ 2024-03-01 │
# │ 1006     ┆ Evan     ┆ North  ┆ Monitor  ┆ 2        ┆ … ┆ paid      ┆ true     ┆ SPRING     ┆ 2024-03-15 │
# │ 1007     ┆ Alice    ┆ East   ┆ Mouse    ┆ 5        ┆ … ┆ cancelled ┆ false    ┆ VIP        ┆ 2024-03-20 │
# │ 1008     ┆ Diana    ┆ North  ┆ Desk     ┆ 1        ┆ … ┆ paid      ┆ true     ┆ null       ┆ 2024-04-04 │
# │ 1009     ┆ Fiona    ┆ South  ┆ Desk     ┆ 2        ┆ … ┆ paid      ┆ false    ┆ CLEARANCE  ┆ 2024-04-10 │
# │ 1010     ┆ Bob      ┆ West   ┆ Keyboard ┆ 1        ┆ … ┆ pending   ┆ false    ┆ null       ┆ 2024-04-12 │
# │ 1011     ┆ Evan     ┆ North  ┆ Mouse    ┆ 3        ┆ … ┆ paid      ┆ false    ┆ VIP        ┆ 2024-05-01 │
# │ 1012     ┆ Alice    ┆ East   ┆ Keyboard ┆ 1        ┆ … ┆ paid      ┆ true     ┆ CLEARANCE  ┆ 2024-05-15 │
# └──────────┴──────────┴────────┴──────────┴──────────┴───┴───────────┴──────────┴────────────┴────────────┘

lf_sales = df_sales.lazy()


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. SELECT DISTINCT * -------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
SELECT DISTINCT * returns unique full rows from the selected result.

Native Polars equivalent:
    df.unique()

Remember:
    DISTINCT applies to the output of SELECT, not necessarily to the original table.
'''

out_sql = df_dupes.lazy().sql(
    """
    SELECT DISTINCT *
    FROM self
    ORDER BY ALL
    """
)
print(out_sql.collect())
# shape: (5, 3)
# ┌──────────┬───────┬───────┐
# │ category ┆ label ┆ value │
# │ ---      ┆ ---   ┆ ---   │
# │ str      ┆ str   ┆ i64   │
# ╞══════════╪═══════╪═══════╡
# │ A        ┆ x     ┆ 10    │
# │ A        ┆ y     ┆ 20    │
# │ B        ┆ p     ┆ 30    │
# │ B        ┆ q     ┆ 40    │
# │ C        ┆ z     ┆ 50    │
# └──────────┴───────┴───────┘

out_native = (
    df_dupes
    .lazy()
    .unique()
    .sort(df_dupes.columns)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 2. DISTINCT selected columns only ---------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
DISTINCT only considers the columns/expression outputs that appear in SELECT.

Here, two rows with the same category and label are collapsed, even if other columns
not selected from a larger table would have been different.
'''

out_sql = df_dupes.lazy().sql(
    """
    SELECT DISTINCT
        category,
        label
    FROM self
    ORDER BY category, label
    """
)
print(out_sql.collect())
# shape: (5, 2)
# ┌──────────┬───────┐
# │ category ┆ label │
# │ ---      ┆ ---   │
# │ str      ┆ str   │
# ╞══════════╪═══════╡
# │ A        ┆ x     │
# │ A        ┆ y     │
# │ B        ┆ p     │
# │ B        ┆ q     │
# │ C        ┆ z     │
# └──────────┴───────┘

out_native = (
    df_dupes
    .lazy()
    .select("category", "label")
    .unique()
    .sort("category", "label")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. DISTINCT with expressions -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
DISTINCT can also work on computed outputs.

This example creates a revenue band first, then returns the unique bands.
'''

out_sql = lf_sales.sql(
    """
    SELECT DISTINCT
        CASE
            WHEN quantity * unit_price >= 400 THEN 'high'
            WHEN quantity * unit_price >= 150 THEN 'medium'
            ELSE 'low'
        END AS revenue_band
    FROM self
    ORDER BY revenue_band
    """
)
print(out_sql.collect())
# shape: (3, 1)
# ┌──────────────┐
# │ revenue_band │
# │ ---          │
# │ str          │
# ╞══════════════╡
# │ high         │
# │ low          │
# │ medium       │
# └──────────────┘

out_native = (
    lf_sales
    .select(
        pl.when(c("quantity") * c("unit_price") >= 400).then(pl.lit("high"))
        .when(c("quantity") * c("unit_price") >= 150).then(pl.lit("medium"))
        .otherwise(pl.lit("low"))
        .alias("revenue_band")
    )
    .unique()
    .sort("revenue_band")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 4. DISTINCT ON ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
DISTINCT ON (key_column) keeps the first row for each unique key.

The important pattern is:
    SELECT DISTINCT ON (customer) ...
    FROM self
    ORDER BY customer, revenue DESC

This means:
    For each customer, keep the first row after sorting by customer and revenue.

Polars SQL note:
    DISTINCT ON currently supports column names, not arbitrary expressions.
    If you want to rank by an expression, put the expression in SELECT/ORDER BY,
    but keep the DISTINCT ON key itself as a column name.
'''

out_sql = lf_sales.sql(
    """
    SELECT DISTINCT ON (customer)
        customer,
        order_id,
        product,
        quantity * unit_price AS gross_revenue
    FROM self
    ORDER BY customer, gross_revenue DESC
    """
)
print(out_sql.collect())
# shape: (5, 4)
# ┌──────────┬──────────┬─────────┬───────────────┐
# │ customer ┆ order_id ┆ product ┆ gross_revenue │
# │ ---      ┆ ---      ┆ ---     ┆ ---           │
# │ str      ┆ i64      ┆ str     ┆ f64           │
# ╞══════════╪══════════╪═════════╪═══════════════╡
# │ Alice    ┆ 1003     ┆ Monitor ┆ 250.000       │
# │ Bob      ┆ 1005     ┆ Mouse   ┆ 140.000       │
# │ Diana    ┆ 1008     ┆ Desk    ┆ 400.000       │
# │ Evan     ┆ 1006     ┆ Monitor ┆ 500.000       │
# │ Fiona    ┆ 1009     ┆ Desk    ┆ 800.000       │
# └──────────┴──────────┴─────────┴───────────────┘

out_native = (
    lf_sales
    .with_columns((c("quantity") * c("unit_price")).alias("gross_revenue"))
    .sort(["customer", "gross_revenue"], descending=[False, True])
    .unique(subset=["customer"], keep="first", maintain_order=True)
    .select("customer", "order_id", "product", "gross_revenue")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 5. DISTINCT ON multiple columns ---------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
DISTINCT ON can use more than one key column.

Here we keep the largest gross revenue row for each customer/product pair.
'''

out_sql = lf_sales.sql(
    """
    SELECT DISTINCT ON (customer, product)
        customer,
        product,
        order_id,
        quantity * unit_price AS gross_revenue
    FROM self
    ORDER BY customer, product, gross_revenue DESC
    """
)
print(out_sql.collect())
# shape: (10, 4)
# ┌──────────┬──────────┬──────────┬───────────────┐
# │ customer ┆ product  ┆ order_id ┆ gross_revenue │
# │ ---      ┆ ---      ┆ ---      ┆ ---           │
# │ str      ┆ str      ┆ i64      ┆ f64           │
# ╞══════════╪══════════╪══════════╪═══════════════╡
# │ Alice    ┆ Keyboard ┆ 1001     ┆ 240.000       │
# │ Alice    ┆ Monitor  ┆ 1003     ┆ 250.000       │
# │ Alice    ┆ Mouse    ┆ 1007     ┆ 175.000       │
# │ Bob      ┆ Keyboard ┆ 1010     ┆ 120.000       │
# │ Bob      ┆ Mouse    ┆ 1005     ┆ 140.000       │
# │ Diana    ┆ Desk     ┆ 1008     ┆ 400.000       │
# │ Diana    ┆ Keyboard ┆ 1004     ┆ 360.000       │
# │ Evan     ┆ Monitor  ┆ 1006     ┆ 500.000       │
# │ Evan     ┆ Mouse    ┆ 1011     ┆ 105.000       │
# │ Fiona    ┆ Desk     ┆ 1009     ┆ 800.000       │
# └──────────┴──────────┴──────────┴───────────────┘

out_native = (
    lf_sales
    .with_columns((c("quantity") * c("unit_price")).alias("gross_revenue"))
    .sort(["customer", "product", "gross_revenue"], descending=[False, False, True])
    .unique(subset=["customer", "product"], keep="first", maintain_order=True)
    .select("customer", "product", "order_id", "gross_revenue")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 6. ORDER BY one column ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
ORDER BY sorts the final query result.

SQL:
    ORDER BY gross_revenue DESC

Native Polars equivalent:
    .sort("gross_revenue", descending=True)
'''

out_sql = lf_sales.sql(
    """
    SELECT
        order_id,
        customer,
        product,
        quantity * unit_price AS gross_revenue
    FROM self
    ORDER BY gross_revenue DESC
    """
)
print(out_sql.collect())
# shape: (12, 4)
# ┌──────────┬──────────┬──────────┬───────────────┐
# │ order_id ┆ customer ┆ product  ┆ gross_revenue │
# │ ---      ┆ ---      ┆ ---      ┆ ---           │
# │ i64      ┆ str      ┆ str      ┆ f64           │
# ╞══════════╪══════════╪══════════╪═══════════════╡
# │ 1009     ┆ Fiona    ┆ Desk     ┆ 800.000       │
# │ 1006     ┆ Evan     ┆ Monitor  ┆ 500.000       │
# │ 1008     ┆ Diana    ┆ Desk     ┆ 400.000       │
# │ 1004     ┆ Diana    ┆ Keyboard ┆ 360.000       │
# │ 1003     ┆ Alice    ┆ Monitor  ┆ 250.000       │
# │ 1001     ┆ Alice    ┆ Keyboard ┆ 240.000       │
# │ 1007     ┆ Alice    ┆ Mouse    ┆ 175.000       │
# │ 1005     ┆ Bob      ┆ Mouse    ┆ 140.000       │
# │ 1010     ┆ Bob      ┆ Keyboard ┆ 120.000       │
# │ 1012     ┆ Alice    ┆ Keyboard ┆ 120.000       │
# │ 1011     ┆ Evan     ┆ Mouse    ┆ 105.000       │
# │ 1002     ┆ Bob      ┆ Mouse    ┆ 35.000        │
# └──────────┴──────────┴──────────┴───────────────┘

out_native = (
    lf_sales
    .select(
        "order_id",
        "customer",
        "product",
        (c("quantity") * c("unit_price")).alias("gross_revenue"),
    )
    .sort("gross_revenue", descending=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 7. ORDER BY multiple columns -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
For multiple sort keys, write them in priority order.

This example sorts by:
1. customer ascending
2. order_date descending within each customer
3. order_id ascending as a stable tie-breaker
'''

out_sql = lf_sales.sql(
    """
    SELECT
        customer,
        order_date,
        order_id,
        product,
        status
    FROM self
    ORDER BY customer ASC, order_date DESC, order_id ASC
    """
)
print(out_sql.collect())
# shape: (12, 5)
# ┌──────────┬────────────┬──────────┬──────────┬───────────┐
# │ customer ┆ order_date ┆ order_id ┆ product  ┆ status    │
# │ ---      ┆ ---        ┆ ---      ┆ ---      ┆ ---       │
# │ str      ┆ date       ┆ i64      ┆ str      ┆ str       │
# ╞══════════╪════════════╪══════════╪══════════╪═══════════╡
# │ Alice    ┆ 2024-05-15 ┆ 1012     ┆ Keyboard ┆ paid      │
# │ Alice    ┆ 2024-03-20 ┆ 1007     ┆ Mouse    ┆ cancelled │
# │ Alice    ┆ 2024-02-10 ┆ 1003     ┆ Monitor  ┆ paid      │
# │ Alice    ┆ 2024-01-03 ┆ 1001     ┆ Keyboard ┆ paid      │
# │ Bob      ┆ 2024-04-12 ┆ 1010     ┆ Keyboard ┆ pending   │
# │ Bob      ┆ 2024-03-01 ┆ 1005     ┆ Mouse    ┆ paid      │
# │ Bob      ┆ 2024-01-05 ┆ 1002     ┆ Mouse    ┆ pending   │
# │ Diana    ┆ 2024-04-04 ┆ 1008     ┆ Desk     ┆ paid      │
# │ Diana    ┆ 2024-02-12 ┆ 1004     ┆ Keyboard ┆ paid      │
# │ Evan     ┆ 2024-05-01 ┆ 1011     ┆ Mouse    ┆ paid      │
# │ Evan     ┆ 2024-03-15 ┆ 1006     ┆ Monitor  ┆ paid      │
# │ Fiona    ┆ 2024-04-10 ┆ 1009     ┆ Desk     ┆ paid      │
# └──────────┴────────────┴──────────┴──────────┴───────────┘

out_native = (
    lf_sales
    .select("customer", "order_date", "order_id", "product", "status")
    .sort(
        ["customer", "order_date", "order_id"],
        descending=[False, True, False],
    )
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------- 8. ORDER BY NULLS FIRST / NULLS LAST --------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
ORDER BY can control where NULL values appear.

Common SQL patterns:
    ORDER BY promo_code ASC NULLS LAST
    ORDER BY promo_code DESC NULLS FIRST

Native Polars equivalent:
    .sort("promo_code", nulls_last=True)

For descending plus null placement, pass descending=... and nulls_last=...
according to the intended result.
'''

out_sql = lf_sales.sql(
    """
    SELECT
        order_id,
        customer,
        promo_code
    FROM self
    ORDER BY promo_code ASC NULLS LAST, order_id
    """
)
print(out_sql.collect())
# shape: (12, 3)
# ┌──────────┬──────────┬────────────┐
# │ order_id ┆ customer ┆ promo_code │
# │ ---      ┆ ---      ┆ ---        │
# │ i64      ┆ str      ┆ str        │
# ╞══════════╪══════════╪════════════╡
# │ 1009     ┆ Fiona    ┆ CLEARANCE  │
# │ 1012     ┆ Alice    ┆ CLEARANCE  │
# │ 1003     ┆ Alice    ┆ SPRING     │
# │ 1006     ┆ Evan     ┆ SPRING     │
# │ 1001     ┆ Alice    ┆ VIP        │
# │ 1005     ┆ Bob      ┆ VIP        │
# │ 1007     ┆ Alice    ┆ VIP        │
# │ 1011     ┆ Evan     ┆ VIP        │
# │ 1002     ┆ Bob      ┆ null       │
# │ 1004     ┆ Diana    ┆ null       │
# │ 1008     ┆ Diana    ┆ null       │
# │ 1010     ┆ Bob      ┆ null       │
# └──────────┴──────────┴────────────┘

out_native = (
    lf_sales
    .select("order_id", "customer", "promo_code")
    .sort(["promo_code", "order_id"], nulls_last=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 9. ORDER BY expression -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
ORDER BY does not have to use only existing columns.
It can sort by a computed expression.

For readability, it is often nicer to create an alias in SELECT and order by the alias.
'''

out_sql = lf_sales.sql(
    """
    SELECT
        order_id,
        customer,
        product,
        quantity,
        unit_price,
        discount_rate,
        quantity * unit_price * (1 - discount_rate) AS net_revenue
    FROM self
    ORDER BY net_revenue DESC
    LIMIT 5
    """
)
print(out_sql.collect())
# shape: (5, 7)
# ┌──────────┬──────────┬──────────┬──────────┬────────────┬───────────────┬─────────────┐
# │ order_id ┆ customer ┆ product  ┆ quantity ┆ unit_price ┆ discount_rate ┆ net_revenue │
# │ ---      ┆ ---      ┆ ---      ┆ ---      ┆ ---        ┆ ---           ┆ ---         │
# │ i64      ┆ str      ┆ str      ┆ i64      ┆ f64        ┆ f64           ┆ f64         │
# ╞══════════╪══════════╪══════════╪══════════╪════════════╪═══════════════╪═════════════╡
# │ 1009     ┆ Fiona    ┆ Desk     ┆ 2        ┆ 400.000    ┆ 0.250         ┆ 600.000     │
# │ 1006     ┆ Evan     ┆ Monitor  ┆ 2        ┆ 250.000    ┆ 0.200         ┆ 400.000     │
# │ 1008     ┆ Diana    ┆ Desk     ┆ 1        ┆ 400.000    ┆ 0.100         ┆ 360.000     │
# │ 1004     ┆ Diana    ┆ Keyboard ┆ 3        ┆ 120.000    ┆ 0.050         ┆ 342.000     │
# │ 1001     ┆ Alice    ┆ Keyboard ┆ 2        ┆ 120.000    ┆ 0.100         ┆ 216.000     │
# └──────────┴──────────┴──────────┴──────────┴────────────┴───────────────┴─────────────┘

out_native = (
    lf_sales
    .select(
        "order_id",
        "customer",
        "product",
        "quantity",
        "unit_price",
        "discount_rate",
        (c("quantity") * c("unit_price") * (1 - c("discount_rate"))).alias("net_revenue"),
    )
    .sort("net_revenue", descending=True)
    .limit(5)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 10. ORDER BY ALL -------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
ORDER BY ALL sorts by every selected output column.

This is convenient when the selected output has several columns and you want a
lexicographic sort by all of them.

Native Polars equivalent:
    .sort(result_column_names)
'''

out_sql = lf_sales.sql(
    """
    SELECT DISTINCT
        region,
        customer,
        product
    FROM self
    ORDER BY ALL
    """
)
print(out_sql.collect())
# shape: (10, 3)
# ┌────────┬──────────┬──────────┐
# │ region ┆ customer ┆ product  │
# │ ---    ┆ ---      ┆ ---      │
# │ str    ┆ str      ┆ str      │
# ╞════════╪══════════╪══════════╡
# │ East   ┆ Alice    ┆ Keyboard │
# │ East   ┆ Alice    ┆ Monitor  │
# │ East   ┆ Alice    ┆ Mouse    │
# │ North  ┆ Diana    ┆ Desk     │
# │ North  ┆ Diana    ┆ Keyboard │
# │ North  ┆ Evan     ┆ Monitor  │
# │ North  ┆ Evan     ┆ Mouse    │
# │ South  ┆ Fiona    ┆ Desk     │
# │ West   ┆ Bob      ┆ Keyboard │
# │ West   ┆ Bob      ┆ Mouse    │
# └────────┴──────────┴──────────┘

out_native = (
    lf_sales
    .select("region", "customer", "product")
    .unique()
    .sort(["region", "customer", "product"])
)
print(out_native.collect())

#######################
## ORDER BY ALL DESC ##
#######################

out_sql = lf_sales.sql(
    """
    SELECT DISTINCT
        region,
        customer
    FROM self
    ORDER BY ALL DESC
    """
)
print(out_sql.collect())
# shape: (5, 2)
# ┌────────┬──────────┐
# │ region ┆ customer │
# │ ---    ┆ ---      │
# │ str    ┆ str      │
# ╞════════╪══════════╡
# │ West   ┆ Bob      │
# │ South  ┆ Fiona    │
# │ North  ┆ Evan     │
# │ North  ┆ Diana    │
# │ East   ┆ Alice    │
# └────────┴──────────┘

out_native = (
    lf_sales
    .select("region", "customer")
    .unique()
    .sort(["region", "customer"], descending=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 11. LIMIT -----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
LIMIT returns at most n rows.

Important:
    LIMIT without ORDER BY means "first n rows in the current query result", not
    "top n rows" by any meaningful ranking. Use ORDER BY + LIMIT for top-n queries.
'''

out_sql = lf_sales.sql(
    """
    SELECT
        order_id,
        customer,
        product,
        quantity * unit_price AS gross_revenue
    FROM self
    ORDER BY gross_revenue DESC
    LIMIT 3
    """
)
print(out_sql.collect())
# shape: (3, 4)
# ┌──────────┬──────────┬─────────┬───────────────┐
# │ order_id ┆ customer ┆ product ┆ gross_revenue │
# │ ---      ┆ ---      ┆ ---     ┆ ---           │
# │ i64      ┆ str      ┆ str     ┆ f64           │
# ╞══════════╪══════════╪═════════╪═══════════════╡
# │ 1009     ┆ Fiona    ┆ Desk    ┆ 800.000       │
# │ 1006     ┆ Evan     ┆ Monitor ┆ 500.000       │
# │ 1008     ┆ Diana    ┆ Desk    ┆ 400.000       │
# └──────────┴──────────┴─────────┴───────────────┘

out_native = (
    lf_sales
    .select(
        "order_id",
        "customer",
        "product",
        (c("quantity") * c("unit_price")).alias("gross_revenue"),
    )
    .sort("gross_revenue", descending=True)
    .limit(3)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 12. OFFSET and pagination ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
OFFSET skips rows before returning the output.

For pagination, always combine ORDER BY with LIMIT/OFFSET so that page boundaries
are deterministic.

Page 1:
    ORDER BY order_id LIMIT 5 OFFSET 0

Page 2:
    ORDER BY order_id LIMIT 5 OFFSET 5
'''

page_1_sql = lf_sales.sql(
    """
    SELECT
        order_id,
        customer,
        product
    FROM self
    ORDER BY order_id
    LIMIT 5 OFFSET 0
    """
)
print(page_1_sql.collect())
# shape: (5, 3)
# ┌──────────┬──────────┬──────────┐
# │ order_id ┆ customer ┆ product  │
# │ ---      ┆ ---      ┆ ---      │
# │ i64      ┆ str      ┆ str      │
# ╞══════════╪══════════╪══════════╡
# │ 1001     ┆ Alice    ┆ Keyboard │
# │ 1002     ┆ Bob      ┆ Mouse    │
# │ 1003     ┆ Alice    ┆ Monitor  │
# │ 1004     ┆ Diana    ┆ Keyboard │
# │ 1005     ┆ Bob      ┆ Mouse    │
# └──────────┴──────────┴──────────┘

page_2_sql = lf_sales.sql(
    """
    SELECT
        order_id,
        customer,
        product
    FROM self
    ORDER BY order_id
    LIMIT 5 OFFSET 5
    """
)
print(page_2_sql.collect())
# shape: (5, 3)
# ┌──────────┬──────────┬──────────┐
# │ order_id ┆ customer ┆ product  │
# │ ---      ┆ ---      ┆ ---      │
# │ i64      ┆ str      ┆ str      │
# ╞══════════╪══════════╪══════════╡
# │ 1006     ┆ Evan     ┆ Monitor  │
# │ 1007     ┆ Alice    ┆ Mouse    │
# │ 1008     ┆ Diana    ┆ Desk     │
# │ 1009     ┆ Fiona    ┆ Desk     │
# │ 1010     ┆ Bob      ┆ Keyboard │
# └──────────┴──────────┴──────────┘

page_2_native = (
    lf_sales
    .select("order_id", "customer", "product")
    .sort("order_id")
    .slice(offset=5, length=5)
)
print(page_2_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 13. FETCH FIRST / NEXT --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
FETCH is the ANSI SQL-style alternative to LIMIT.

Common forms:
    FETCH FIRST 3 ROWS ONLY
    FETCH NEXT 3 ROWS ONLY

FETCH can be combined with OFFSET.
Polars SQL currently does not support FETCH WITH TIES or FETCH PERCENT.
'''

out_sql = lf_sales.sql(
    """
    SELECT
        order_id,
        customer,
        product,
        quantity * unit_price AS gross_revenue
    FROM self
    ORDER BY gross_revenue DESC
    FETCH FIRST 4 ROWS ONLY
    """
)
print(out_sql.collect())
# shape: (4, 4)
# ┌──────────┬──────────┬──────────┬───────────────┐
# │ order_id ┆ customer ┆ product  ┆ gross_revenue │
# │ ---      ┆ ---      ┆ ---      ┆ ---           │
# │ i64      ┆ str      ┆ str      ┆ f64           │
# ╞══════════╪══════════╪══════════╪═══════════════╡
# │ 1009     ┆ Fiona    ┆ Desk     ┆ 800.000       │
# │ 1006     ┆ Evan     ┆ Monitor  ┆ 500.000       │
# │ 1008     ┆ Diana    ┆ Desk     ┆ 400.000       │
# │ 1004     ┆ Diana    ┆ Keyboard ┆ 360.000       │
# └──────────┴──────────┴──────────┴───────────────┘

out_native = (
    lf_sales
    .select(
        "order_id",
        "customer",
        "product",
        (c("quantity") * c("unit_price")).alias("gross_revenue"),
    )
    .sort("gross_revenue", descending=True)
    .limit(4)
)
print(out_native.collect())

#########################
## OFFSET + FETCH NEXT ##
#########################

out_sql = lf_sales.sql(
    """
    SELECT
        order_id,
        customer,
        product,
        quantity * unit_price AS gross_revenue
    FROM self
    ORDER BY gross_revenue DESC
    OFFSET 2 FETCH NEXT 4 ROWS ONLY
    """
)
print(out_sql.collect())
# shape: (4, 4)
# ┌──────────┬──────────┬──────────┬───────────────┐
# │ order_id ┆ customer ┆ product  ┆ gross_revenue │
# │ ---      ┆ ---      ┆ ---      ┆ ---           │
# │ i64      ┆ str      ┆ str      ┆ f64           │
# ╞══════════╪══════════╪══════════╪═══════════════╡
# │ 1008     ┆ Diana    ┆ Desk     ┆ 400.000       │
# │ 1004     ┆ Diana    ┆ Keyboard ┆ 360.000       │
# │ 1003     ┆ Alice    ┆ Monitor  ┆ 250.000       │
# │ 1001     ┆ Alice    ┆ Keyboard ┆ 240.000       │
# └──────────┴──────────┴──────────┴───────────────┘

out_native = (
    lf_sales
    .select(
        "order_id",
        "customer",
        "product",
        (c("quantity") * c("unit_price")).alias("gross_revenue"),
    )
    .sort("gross_revenue", descending=True)
    .slice(offset=2, length=4)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 14. Top-n per group preview -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
This file focuses on global sorting/limiting.

For top-n per group, plain ORDER BY + LIMIT is not enough because LIMIT applies to
the whole query result. The SQL pattern is usually a window function, which will be
covered later.

Small preview:
    ROW_NUMBER() OVER (PARTITION BY customer ORDER BY revenue DESC)

The native Polars equivalent often uses .over(...), ranking, or group_by().head(...).
'''

out_sql = lf_sales.sql(
    """
    SELECT
        customer,
        order_id,
        product,
        quantity * unit_price AS gross_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY customer
            ORDER BY quantity * unit_price DESC
        ) AS revenue_rank_for_customer
    FROM self
    QUALIFY revenue_rank_for_customer <= 2
    ORDER BY customer, revenue_rank_for_customer
    """
)
print(out_sql.collect())
# shape: (9, 5)
# ┌──────────┬──────────┬──────────┬───────────────┬───────────────────────────┐
# │ customer ┆ order_id ┆ product  ┆ gross_revenue ┆ revenue_rank_for_customer │
# │ ---      ┆ ---      ┆ ---      ┆ ---           ┆ ---                       │
# │ str      ┆ i64      ┆ str      ┆ f64           ┆ u32                       │
# ╞══════════╪══════════╪══════════╪═══════════════╪═══════════════════════════╡
# │ Alice    ┆ 1003     ┆ Monitor  ┆ 250.000       ┆ 1                         │
# │ Alice    ┆ 1001     ┆ Keyboard ┆ 240.000       ┆ 2                         │
# │ Bob      ┆ 1005     ┆ Mouse    ┆ 140.000       ┆ 1                         │
# │ Bob      ┆ 1010     ┆ Keyboard ┆ 120.000       ┆ 2                         │
# │ Diana    ┆ 1008     ┆ Desk     ┆ 400.000       ┆ 1                         │
# │ Diana    ┆ 1004     ┆ Keyboard ┆ 360.000       ┆ 2                         │
# │ Evan     ┆ 1006     ┆ Monitor  ┆ 500.000       ┆ 1                         │
# │ Evan     ┆ 1011     ┆ Mouse    ┆ 105.000       ┆ 2                         │
# │ Fiona    ┆ 1009     ┆ Desk     ┆ 800.000       ┆ 1                         │
# └──────────┴──────────┴──────────┴───────────────┴───────────────────────────┘

# Native equivalent preview. A more complete explanation belongs in the window/ranking file.
out_native = (
    lf_sales
    .with_columns((c("quantity") * c("unit_price")).alias("gross_revenue"))
    .with_columns(
        c("gross_revenue")
        .rank(method="ordinal", descending=True)
        .over("customer")
        .alias("revenue_rank_for_customer")
    )
    .filter(c("revenue_rank_for_customer") <= 2)
    .select("customer", "order_id", "product", "gross_revenue", "revenue_rank_for_customer")
    .sort("customer", "revenue_rank_for_customer")
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 15. SQLContext table example ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Everything above used frame-level .sql(...), where the table is named self.
With SQLContext, use the registered table name in FROM.
'''

ctx = pl.SQLContext(sales=lf_sales)

out_ctx = ctx.execute(
    """
    SELECT DISTINCT ON (customer)
        customer,
        order_id,
        product,
        quantity * unit_price AS gross_revenue
    FROM sales
    ORDER BY customer, gross_revenue DESC
    """
)
print(out_ctx.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 16. Quick mapping -------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Quick SQL -> native Polars mapping:

1. SELECT DISTINCT * FROM self
   -> lf.unique()

2. SELECT DISTINCT col1, col2 FROM self
   -> lf.select("col1", "col2").unique()

3. SELECT DISTINCT ON (key) ... ORDER BY key, value DESC
   -> lf.sort(["key", "value"], descending=[False, True]).unique(subset="key", keep="first", maintain_order=True)

4. ORDER BY col DESC
   -> lf.sort("col", descending=True)

5. ORDER BY col ASC NULLS LAST
   -> lf.sort("col", nulls_last=True)

6. ORDER BY ALL
   -> lf.select(...).sort(list_of_selected_columns)

7. LIMIT n
   -> lf.limit(n) or lf.head(n)

8. LIMIT n OFFSET k
   -> lf.slice(offset=k, length=n)

9. OFFSET k FETCH NEXT n ROWS ONLY
   -> lf.slice(offset=k, length=n)
'''
