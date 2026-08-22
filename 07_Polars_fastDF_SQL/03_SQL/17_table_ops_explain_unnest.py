# FILE VERSION: 17_sql_table_ops_explain_unnest_v1
'''
Polars SQL table operations, EXPLAIN, and UNNEST.

Main ideas:
1. SQLContext stores registered DataFrame/LazyFrame objects as SQL tables.
2. SHOW TABLES lists the tables currently registered in a context.
3. CREATE TABLE AS SELECT creates a new registered table from a query result.
4. DELETE FROM removes rows from a registered table when supported by your Polars version.
5. TRUNCATE TABLE removes all rows while keeping the table registered.
6. DROP TABLE unregisters a table from the SQLContext.
7. EXPLAIN returns the Polars query plan for a SQL query.
8. UNNEST can create rows from array/list literals inside SQL.

Important Polars SQL notes:
+ Polars SQL is not a separate database engine. SQL is translated into Polars
  query plans and executed by Polars.
+ These operations affect tables registered inside the SQLContext. They do not
  modify external files on disk.
+ CREATE TABLE registers a new table in the context. The statement itself is not
  the table; query the table afterwards with SELECT.
+ SQL table-operation support can differ between Polars versions. If DELETE or
  TRUNCATE is unavailable in your installed version, use the native Polars
  fallback patterns shown in this file.
+ Use native Polars expressions when you need maximum compatibility or the newest
  DataFrame features.
'''

import datetime as dt

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(25)
pl.Config.set_tbl_cols(10)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(120)


# =========================================================================================
# 0. Setup data
# =========================================================================================
'''
The examples are self-contained so this file can run without external datasets.

We create a small order table, then register it in SQLContext.
The context is created with eager=True so ctx.execute(...) directly returns a
DataFrame for SELECT/SHOW/EXPLAIN queries.
'''

df_orders = pl.DataFrame(
    {
        "order_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
        "customer": ["Alice", "Bob", "Alice", "Diana", "Bob", "Evan", "Alice", "Diana"],
        "region": ["East", "West", "East", "North", "West", "North", "East", "North"],
        "product": ["Keyboard", "Mouse", "Monitor", "Keyboard", "Mouse", "Monitor", "Mouse", "Desk"],
        "quantity": [2, 1, 1, 3, 4, 2, 5, 1],
        "unit_price": [120.0, 35.0, 250.0, 120.0, 35.0, 250.0, 35.0, 400.0],
        "discount_rate": [0.10, 0.00, 0.15, 0.05, 0.00, 0.20, 0.05, 0.10],
        "status": ["paid", "pending", "paid", "paid", "paid", "paid", "cancelled", "paid"],
        "order_date": [
            dt.date(2024, 1, 3),
            dt.date(2024, 1, 5),
            dt.date(2024, 2, 10),
            dt.date(2024, 2, 12),
            dt.date(2024, 3, 1),
            dt.date(2024, 3, 15),
            dt.date(2024, 3, 20),
            dt.date(2024, 4, 4),
        ],
    }
)

df_orders = (
    df_orders
    .with_columns(
        (c("quantity") * c("unit_price")).alias("gross_amount"),
    )
    .with_columns(
        (c("gross_amount") * c("discount_rate")).alias("discount_amount"),
    )
    .with_columns(
        (c("gross_amount") - c("discount_amount")).alias("net_amount"),
    )
)

lf_orders = df_orders.lazy()

print(df_orders)
# shape: (8, 12)
# ┌──────────┬──────────┬────────┬──────────┬──────────┬───┬───────────┬────────────┬────────────┬───────────┬───────────┐
# │ order_id ┆ customer ┆ region ┆ product  ┆ quantity ┆ … ┆ status    ┆ order_date ┆ gross_amou ┆ discount_ ┆ net_amoun │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---      ┆   ┆ ---       ┆ ---        ┆ nt         ┆ amount    ┆ t         │
# │ i64      ┆ str      ┆ str    ┆ str      ┆ i64      ┆   ┆ str       ┆ date       ┆ ---        ┆ ---       ┆ ---       │
# │          ┆          ┆        ┆          ┆          ┆   ┆           ┆            ┆ f64        ┆ f64       ┆ f64       │
# ╞══════════╪══════════╪════════╪══════════╪══════════╪═══╪═══════════╪════════════╪════════════╪═══════════╪═══════════╡
# │ 1001     ┆ Alice    ┆ East   ┆ Keyboard ┆ 2        ┆ … ┆ paid      ┆ 2024-01-03 ┆ 240.000    ┆ 24.000    ┆ 216.000   │
# │ 1002     ┆ Bob      ┆ West   ┆ Mouse    ┆ 1        ┆ … ┆ pending   ┆ 2024-01-05 ┆ 35.000     ┆ 0.000     ┆ 35.000    │
# │ 1003     ┆ Alice    ┆ East   ┆ Monitor  ┆ 1        ┆ … ┆ paid      ┆ 2024-02-10 ┆ 250.000    ┆ 37.500    ┆ 212.500   │
# │ 1004     ┆ Diana    ┆ North  ┆ Keyboard ┆ 3        ┆ … ┆ paid      ┆ 2024-02-12 ┆ 360.000    ┆ 18.000    ┆ 342.000   │
# │ 1005     ┆ Bob      ┆ West   ┆ Mouse    ┆ 4        ┆ … ┆ paid      ┆ 2024-03-01 ┆ 140.000    ┆ 0.000     ┆ 140.000   │
# │ 1006     ┆ Evan     ┆ North  ┆ Monitor  ┆ 2        ┆ … ┆ paid      ┆ 2024-03-15 ┆ 500.000    ┆ 100.000   ┆ 400.000   │
# │ 1007     ┆ Alice    ┆ East   ┆ Mouse    ┆ 5        ┆ … ┆ cancelled ┆ 2024-03-20 ┆ 175.000    ┆ 8.750     ┆ 166.250   │
# │ 1008     ┆ Diana    ┆ North  ┆ Desk     ┆ 1        ┆ … ┆ paid      ┆ 2024-04-04 ┆ 400.000    ┆ 40.000    ┆ 360.000   │
# └──────────┴──────────┴────────┴──────────┴──────────┴───┴───────────┴────────────┴────────────┴───────────┴───────────┘

ctx = pl.SQLContext(orders=lf_orders, eager=True)


# =========================================================================================
# 1. SHOW TABLES
# =========================================================================================
'''
SHOW TABLES lists registered table names in the SQLContext.

Native Polars equivalent:
    ctx.tables()
'''

out_sql = ctx.execute("SHOW TABLES")
print(out_sql)
# shape: (1, 1)
# ┌────────┐
# │ name   │
# │ ---    │
# │ str    │
# ╞════════╡
# │ orders │
# └────────┘

print(ctx.tables())
# ['orders']


# =========================================================================================
# 2. CREATE TABLE AS SELECT
# =========================================================================================
'''
CREATE TABLE ... AS SELECT ... creates a new registered table from a query.

The result of the CREATE statement is not the new data itself. Query the new
registered table afterwards with SELECT.
'''

ctx.execute(
    """
    CREATE TABLE paid_orders AS
    SELECT
        order_id,
        customer,
        region,
        product,
        quantity,
        net_amount,
        order_date
    FROM orders
    WHERE status = 'paid'
    """
)

print(ctx.execute("SHOW TABLES"))
# shape: (2, 1)
# ┌─────────────┐
# │ name        │
# │ ---         │
# │ str         │
# ╞═════════════╡
# │ orders      │
# │ paid_orders │
# └─────────────┘

out_sql = ctx.execute(
    """
    SELECT *
    FROM paid_orders
    ORDER BY order_id
    """
)
print(out_sql)
# shape: (6, 7)
# ┌──────────┬──────────┬────────┬──────────┬──────────┬────────────┬────────────┐
# │ order_id ┆ customer ┆ region ┆ product  ┆ quantity ┆ net_amount ┆ order_date │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---      ┆ ---        ┆ ---        │
# │ i64      ┆ str      ┆ str    ┆ str      ┆ i64      ┆ f64        ┆ date       │
# ╞══════════╪══════════╪════════╪══════════╪══════════╪════════════╪════════════╡
# │ 1001     ┆ Alice    ┆ East   ┆ Keyboard ┆ 2        ┆ 216.000    ┆ 2024-01-03 │
# │ 1003     ┆ Alice    ┆ East   ┆ Monitor  ┆ 1        ┆ 212.500    ┆ 2024-02-10 │
# │ 1004     ┆ Diana    ┆ North  ┆ Keyboard ┆ 3        ┆ 342.000    ┆ 2024-02-12 │
# │ 1005     ┆ Bob      ┆ West   ┆ Mouse    ┆ 4        ┆ 140.000    ┆ 2024-03-01 │
# │ 1006     ┆ Evan     ┆ North  ┆ Monitor  ┆ 2        ┆ 400.000    ┆ 2024-03-15 │
# │ 1008     ┆ Diana    ┆ North  ┆ Desk     ┆ 1        ┆ 360.000    ┆ 2024-04-04 │
# └──────────┴──────────┴────────┴──────────┴──────────┴────────────┴────────────┘

# Native Polars equivalent: build the query and register it manually.
ctx.register(
    name="paid_orders_native",
    frame=(
        lf_orders
        .filter(c("status") == "paid")
        .select(
            "order_id",
            "customer",
            "region",
            "product",
            "quantity",
            "net_amount",
            "order_date",
        )
    ),
)
print(ctx.execute("SELECT * FROM paid_orders_native ORDER BY order_id"))


# =========================================================================================
# 3. CREATE TABLE LIKE
# =========================================================================================
'''
CREATE TABLE ... LIKE existing_table creates an empty table with the same schema.

This is useful when you want to keep a table name and schema but start with no
rows. In native Polars, this is similar to taking head(0) and registering it.
'''

ctx.execute(
    """
    CREATE TABLE empty_paid_orders LIKE paid_orders
    """
)

out_sql = ctx.execute("SELECT * FROM empty_paid_orders")
print(out_sql)
# shape: (0, 7)
# ┌──────────┬──────────┬────────┬─────────┬──────────┬────────────┬────────────┐
# │ order_id ┆ customer ┆ region ┆ product ┆ quantity ┆ net_amount ┆ order_date │
# │ ---      ┆ ---      ┆ ---    ┆ ---     ┆ ---      ┆ ---        ┆ ---        │
# │ i64      ┆ str      ┆ str    ┆ str     ┆ i64      ┆ f64        ┆ date       │
# ╞══════════╪══════════╪════════╪═════════╪══════════╪════════════╪════════════╡
# └──────────┴──────────┴────────┴─────────┴──────────┴────────────┴────────────┘

print(ctx.execute("SHOW TABLES"))
# shape: (4, 1)
# ┌────────────────────┐
# │ name               │
# │ ---                │
# │ str                │
# ╞════════════════════╡
# │ empty_paid_orders  │
# │ orders             │
# │ paid_orders        │
# │ paid_orders_native │
# └────────────────────┘

# Native Polars equivalent.
ctx.register("empty_paid_orders_native", ctx.execute("SELECT * FROM paid_orders").head(0).lazy())
print(ctx.execute("SELECT * FROM empty_paid_orders_native"))


# =========================================================================================
# 4. DELETE FROM
# =========================================================================================
'''
DELETE FROM removes rows from a registered table when supported by your Polars
version.

Example:
    DELETE FROM mutable_orders WHERE status = 'cancelled'

If your installed Polars version does not support DELETE yet, use the native
fallback shown below: filter out the rows you want to remove, then re-register
the table name.
'''

ctx.execute(
    """
    CREATE TABLE mutable_orders AS
    SELECT * FROM orders
    """
)

print(
    ctx.execute(
        """
        SELECT status, COUNT(*) AS n_rows
        FROM mutable_orders
        GROUP BY status
        ORDER BY status
        """
    )
)
# shape: (3, 2)
# ┌───────────┬────────┐
# │ status    ┆ n_rows │
# │ ---       ┆ ---    │
# │ str       ┆ u32    │
# ╞═══════════╪════════╡
# │ cancelled ┆ 1      │
# │ paid      ┆ 6      │
# │ pending   ┆ 1      │
# └───────────┴────────┘

try:
    ctx.execute(
        """
        DELETE FROM mutable_orders
        WHERE status = 'cancelled'
        """
    )

    print(
        ctx.execute(
            """
            SELECT status, COUNT(*) AS n_rows
            FROM mutable_orders
            GROUP BY status
            ORDER BY status
            """
        )
    )

except Exception as exc:
    print("DELETE FROM is not available in this Polars version or failed for this context.")
    print(type(exc).__name__, exc)

    # Native Polars fallback: keep rows that do not match the delete condition.
    ctx.register(
        "mutable_orders",
        ctx.execute("SELECT * FROM mutable_orders").lazy().filter(c("status") != "cancelled"),
    )

    print(
        ctx.execute(
            """
            SELECT status, COUNT(*) AS n_rows
            FROM mutable_orders
            GROUP BY status
            ORDER BY status
            """
        )
    )
# shape: (3, 2)
# ┌───────────┬────────┐
# │ status    ┆ n_rows │
# │ ---       ┆ ---    │
# │ str       ┆ u32    │
# ╞═══════════╪════════╡
# │ cancelled ┆ 1      │
# │ paid      ┆ 6      │
# │ pending   ┆ 1      │
# └───────────┴────────┘


# =========================================================================================
# 5. TRUNCATE TABLE
# =========================================================================================
'''
TRUNCATE TABLE removes all rows but keeps the table registered.

This is different from DROP TABLE:
+ TRUNCATE keeps the table name in the context.
+ DROP unregisters the table name.

If TRUNCATE is unavailable in your installed version, use the native fallback:
query the table, take head(0), and register that empty frame back to the same
name.
'''

ctx.execute(
    """
    CREATE TABLE scratch_orders AS
    SELECT * FROM orders
    WHERE region = 'East'
    """
)

print(ctx.execute("SELECT COUNT(*) AS n_rows FROM scratch_orders"))
# shape: (1, 1)
# ┌────────┐
# │ n_rows │
# │ ---    │
# │ u32    │
# ╞════════╡
# │ 3      │
# └────────┘

try:
    ctx.execute("TRUNCATE TABLE scratch_orders")
    print(ctx.execute("SELECT COUNT(*) AS n_rows FROM scratch_orders"))
    print(ctx.execute("SELECT * FROM scratch_orders"))

except Exception as exc:
    print("TRUNCATE TABLE is not available in this Polars version or failed for this context.")
    print(type(exc).__name__, exc)

    # Native Polars fallback.
    ctx.register("scratch_orders", ctx.execute("SELECT * FROM scratch_orders").head(0).lazy())
    print(ctx.execute("SELECT COUNT(*) AS n_rows FROM scratch_orders"))
    print(ctx.execute("SELECT * FROM scratch_orders"))
# shape: (1, 1)
# ┌────────┐
# │ n_rows │
# │ ---    │
# │ u32    │
# ╞════════╡
# │ 0      │
# └────────┘
# shape: (0, 12)
# ┌──────────┬──────────┬────────┬─────────┬──────────┬───┬────────┬────────────┬─────────────┬─────────────┬────────────┐
# │ order_id ┆ customer ┆ region ┆ product ┆ quantity ┆ … ┆ status ┆ order_date ┆ gross_amoun ┆ discount_am ┆ net_amount │
# │ ---      ┆ ---      ┆ ---    ┆ ---     ┆ ---      ┆   ┆ ---    ┆ ---        ┆ t           ┆ ount        ┆ ---        │
# │ i64      ┆ str      ┆ str    ┆ str     ┆ i64      ┆   ┆ str    ┆ date       ┆ ---         ┆ ---         ┆ f64        │
# │          ┆          ┆        ┆         ┆          ┆   ┆        ┆            ┆ f64         ┆ f64         ┆            │
# ╞══════════╪══════════╪════════╪═════════╪══════════╪═══╪════════╪════════════╪═════════════╪═════════════╪════════════╡
# └──────────┴──────────┴────────┴─────────┴──────────┴───┴────────┴────────────┴─────────────┴─────────────┴────────────┘


# =========================================================================================
# 6. DROP TABLE
# =========================================================================================
'''
DROP TABLE unregisters a table from SQLContext.

Use IF EXISTS when the table may or may not be present.
This avoids raising an error for missing table names.
'''

print(ctx.execute("SHOW TABLES"))
# shape: (7, 1)
# ┌──────────────────────────┐
# │ name                     │
# │ ---                      │
# │ str                      │
# ╞══════════════════════════╡
# │ empty_paid_orders        │
# │ empty_paid_orders_native │
# │ mutable_orders           │
# │ orders                   │
# │ paid_orders              │
# │ paid_orders_native       │
# │ scratch_orders           │
# └──────────────────────────┘

ctx.execute("DROP TABLE IF EXISTS empty_paid_orders")
ctx.execute("DROP TABLE IF EXISTS empty_paid_orders_native")

print(ctx.execute("SHOW TABLES"))
# shape: (5, 1)
# ┌────────────────────┐
# │ name               │
# │ ---                │
# │ str                │
# ╞════════════════════╡
# │ mutable_orders     │
# │ orders             │
# │ paid_orders        │
# │ paid_orders_native │
# │ scratch_orders     │
# └────────────────────┘

# Native Polars equivalent: unregister the table name.
ctx.unregister("paid_orders_native")
print(ctx.execute("SHOW TABLES"))


# =========================================================================================
# 7. EXPLAIN
# =========================================================================================
'''
EXPLAIN returns the Polars query plan for a SQL query.

This is the SQL equivalent of inspecting a LazyFrame query plan with .explain().
The exact text can differ by Polars version and optimization settings.
'''

out_sql = ctx.execute(
    """
    EXPLAIN
    SELECT
        region,
        SUM(net_amount) AS total_net_amount
    FROM orders
    WHERE status = 'paid'
    GROUP BY region
    ORDER BY total_net_amount DESC
    """
)
print(out_sql)
# shape: (8, 1)
# ┌─────────────────────────────────┐
# │ Logical Plan                    │
# │ ---                             │
# │ str                             │
# ╞═════════════════════════════════╡
# │ SORT BY [descending: [true]] [… │
# │   AGGREGATE[maintain_order: fa… │
# │     [col("net_amount").sum().a… │
# │     FROM                        │
# │     simple π 2/2 ["region", "n… │
# │       FILTER [(col("status")) … │
# │       FROM                      │
# │         DF ["order_id", "custo… │
# └─────────────────────────────────┘

# Native Polars equivalent.
lf_plan = (
    lf_orders
    .filter(c("status") == "paid")
    .group_by("region")
    .agg(c("net_amount").sum().alias("total_net_amount"))
    .sort("total_net_amount", descending=True)
)
print(lf_plan.explain())


# =========================================================================================
# 8. UNNEST
# =========================================================================================
'''
UNNEST can turn array/list literals into a table.

This is useful for small inline lookup tables or demonstration data. For larger
lookup data, it is usually clearer to create/register a Polars DataFrame.
'''

out_sql = ctx.execute(
    """
    SELECT *
    FROM UNNEST(
        [1, 2, 3, 4],
        ['Keyboard', 'Mouse', 'Monitor', 'Desk'],
        [120.0, 35.0, 250.0, 400.0]
    ) AS product_lookup(product_id, product, list_price)
    ORDER BY product_id
    """
)
print(out_sql)
# shape: (4, 3)
# ┌────────────┬──────────┬────────────┐
# │ product_id ┆ product  ┆ list_price │
# │ ---        ┆ ---      ┆ ---        │
# │ i64        ┆ str      ┆ f64        │
# ╞════════════╪══════════╪════════════╡
# │ 1          ┆ Keyboard ┆ 120.000    │
# │ 2          ┆ Mouse    ┆ 35.000     │
# │ 3          ┆ Monitor  ┆ 250.000    │
# │ 4          ┆ Desk     ┆ 400.000    │
# └────────────┴──────────┴────────────┘

# Use UNNEST as an inline lookup table in a join.
out_sql = ctx.execute(
    """
    SELECT
        o.order_id,
        o.product,
        o.quantity,
        p.list_price,
        o.quantity * p.list_price AS list_value
    FROM orders AS o
    INNER JOIN UNNEST(
        ['Keyboard', 'Mouse', 'Monitor', 'Desk'],
        [120.0, 35.0, 250.0, 400.0]
    ) AS p(product, list_price)
        ON o.product = p.product
    ORDER BY o.order_id
    """
)
print(out_sql)
# shape: (8, 5)
# ┌──────────┬──────────┬──────────┬────────────┬────────────┐
# │ order_id ┆ product  ┆ quantity ┆ list_price ┆ list_value │
# │ ---      ┆ ---      ┆ ---      ┆ ---        ┆ ---        │
# │ i64      ┆ str      ┆ i64      ┆ f64        ┆ f64        │
# ╞══════════╪══════════╪══════════╪════════════╪════════════╡
# │ 1001     ┆ Keyboard ┆ 2        ┆ 120.000    ┆ 240.000    │
# │ 1002     ┆ Mouse    ┆ 1        ┆ 35.000     ┆ 35.000     │
# │ 1003     ┆ Monitor  ┆ 1        ┆ 250.000    ┆ 250.000    │
# │ 1004     ┆ Keyboard ┆ 3        ┆ 120.000    ┆ 360.000    │
# │ 1005     ┆ Mouse    ┆ 4        ┆ 35.000     ┆ 140.000    │
# │ 1006     ┆ Monitor  ┆ 2        ┆ 250.000    ┆ 500.000    │
# │ 1007     ┆ Mouse    ┆ 5        ┆ 35.000     ┆ 175.000    │
# │ 1008     ┆ Desk     ┆ 1        ┆ 400.000    ┆ 400.000    │
# └──────────┴──────────┴──────────┴────────────┴────────────┘

# Native Polars equivalent: create a small lookup frame and join normally.
lf_product_lookup = pl.LazyFrame(
    {
        "product": ["Keyboard", "Mouse", "Monitor", "Desk"],
        "list_price": [120.0, 35.0, 250.0, 400.0],
    }
)

out_native = (
    lf_orders
    .join(lf_product_lookup, on="product", how="inner")
    .with_columns((c("quantity") * c("list_price")).alias("list_value"))
    .select("order_id", "product", "quantity", "list_price", "list_value")
    .sort("order_id")
)
print(out_native.collect())


# =========================================================================================
# 9. Common mistakes
# =========================================================================================
'''
Common table-operation mistakes:

1. Expecting CREATE TABLE AS SELECT to return the created table directly.

   CREATE TABLE registers the table in SQLContext. Query it afterwards:
       SELECT * FROM new_table

2. Forgetting that SQLContext tables are in-memory/context registrations.

   CREATE, DELETE, TRUNCATE, and DROP here do not update CSV/Parquet files on disk.

3. Confusing TRUNCATE and DROP.

   TRUNCATE TABLE table_name -> keep table name, remove all rows.
   DROP TABLE table_name     -> unregister table name.

4. Expecting every SQL database statement to work.

   Polars SQL supports a useful subset of SQL, but the native DataFrame/LazyFrame
   API is still the primary interface and may support features earlier.

5. Using DELETE/TRUNCATE without checking Polars version.

   Table-operation support can differ between versions. If DELETE/TRUNCATE fails,
   use native Polars filtering/head(0) and re-register the table.
'''
