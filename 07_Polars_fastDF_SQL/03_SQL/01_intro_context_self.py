'''
Polars SQL introduction: `.sql()`, `SQLContext`, and the special `self` table.

This file introduces the mental model for using SQL with Polars DataFrames and
LazyFrames.

Main ideas:
1. Polars SQL is a query interface over Polars data, not a separate database.
2. SQL queries are planned/executed by the Polars engine, so they fit naturally with LazyFrame workflows.
3. `DataFrame.sql(...)` runs a query against an eager DataFrame and returns an eager DataFrame.
4. `LazyFrame.sql(...)` runs a query against a LazyFrame and returns another LazyFrame.
    Use `.collect()` when you want the actual result.
5. In frame-level `.sql(...)`, the calling frame is automatically available as a SQL table named `self`,
   unless you override it with `table_name=...`.
6. `SQLContext` is the explicit/reusable way to register one or more tables and run SQL queries against them.
7. `pl.sql(...)` is the global-context shortcut. It is convenient in notebooks,
    but `SQLContext` is usually clearer in scripts and reusable examples.
8. You can freely mix SQL results with normal Polars expressions.

This file is intentionally simple. Later files should cover SELECT details,
WHERE predicates, functions, aggregation, joins, CTEs, windows, and compatibility.

Polars docs checked while writing this file:
+ https://docs.pola.rs/api/python/stable/reference/sql/python_api.html
+ https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.sql.html
+ https://docs.pola.rs/api/python/stable/reference/lazyframe/api/polars.LazyFrame.sql.html
+ https://docs.pola.rs/api/python/stable/reference/sql/api/polars.SQLContext.execute.html
'''

from datetime import date

import polars as pl
from polars import col as c
from polars.testing import assert_frame_equal

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_tbl_width_chars(120)
pl.Config.set_float_precision(2)


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 0. Setup Data --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
For this first file, use small self-contained data.

This avoids depending on an external data folder and makes the SQL API behavior
easy to see.
'''

df_orders = pl.DataFrame(
    {
        "order_id": [1, 2, 3, 4, 5, 6],
        "customer_id": [101, 102, 101, 103, 102, 104],
        "customer": ["Alice", "Bob", "Alice", "Diana", "Bob", "Evan"],
        "region": ["East", "West", "East", "North", "West", "North"],
        "amount": [120.0, 80.0, 220.0, 150.0, 90.0, 310.0],
        "quantity": [2, 1, 3, 2, 1, 4],
        "order_date": [
            date(2024, 1, 3),
            date(2024, 1, 5),
            date(2024, 2, 10),
            date(2024, 2, 12),
            date(2024, 3, 1),
            date(2024, 3, 15),
        ],
    }
)

# A second table, used only for a tiny SQLContext preview later.
df_customers = pl.DataFrame(
    {
        "customer_id": [101, 102, 103, 104],
        "segment": ["Consumer", "Business", "Consumer", "Enterprise"],
    }
)

# LazyFrame version of the same orders data.
lf_orders = df_orders.lazy()

##########################################################################

print(df_orders)
# shape: (6, 7)
# ┌──────────┬─────────────┬──────────┬────────┬────────┬──────────┬────────────┐
# │ order_id ┆ customer_id ┆ customer ┆ region ┆ amount ┆ quantity ┆ order_date │
# │ ---      ┆ ---         ┆ ---      ┆ ---    ┆ ---    ┆ ---      ┆ ---        │
# │ i64      ┆ i64         ┆ str      ┆ str    ┆ f64    ┆ i64      ┆ date       │
# ╞══════════╪═════════════╪══════════╪════════╪════════╪══════════╪════════════╡
# │ 1        ┆ 101         ┆ Alice    ┆ East   ┆ 120.00 ┆ 2        ┆ 2024-01-03 │
# │ 2        ┆ 102         ┆ Bob      ┆ West   ┆ 80.00  ┆ 1        ┆ 2024-01-05 │
# │ 3        ┆ 101         ┆ Alice    ┆ East   ┆ 220.00 ┆ 3        ┆ 2024-02-10 │
# │ 4        ┆ 103         ┆ Diana    ┆ North  ┆ 150.00 ┆ 2        ┆ 2024-02-12 │
# │ 5        ┆ 102         ┆ Bob      ┆ West   ┆ 90.00  ┆ 1        ┆ 2024-03-01 │
# │ 6        ┆ 104         ┆ Evan     ┆ North  ┆ 310.00 ┆ 4        ┆ 2024-03-15 │
# └──────────┴─────────────┴──────────┴────────┴────────┴──────────┴────────────┘

print(df_orders.schema)


#--------------------------------------------------------------------------------------------------------------#
#----------------------------- 1. DataFrame.sql(): eager frame in, eager frame out ----------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
`DataFrame.sql(...)` is the easiest first example.

The calling DataFrame is automatically registered as a table named `self`.
That is why the query says:

    FROM self

Because the input is an eager DataFrame, the returned result is also an eager
DataFrame.
'''

out_df_sql = df_orders.sql(
    """
    SELECT
        order_id,
        customer,
        region,
        amount
    FROM self
    WHERE amount >= 100
    ORDER BY amount DESC
    """
)

print(type(out_df_sql))
# <class 'polars.dataframe.frame.DataFrame'>

print(out_df_sql)
# shape: (4, 4)
# ┌──────────┬──────────┬────────┬────────┐
# │ order_id ┆ customer ┆ region ┆ amount │
# │ ---      ┆ ---      ┆ ---    ┆ ---    │
# │ i64      ┆ str      ┆ str    ┆ f64    │
# ╞══════════╪══════════╪════════╪════════╡
# │ 6        ┆ Evan     ┆ North  ┆ 310.00 │
# │ 3        ┆ Alice    ┆ East   ┆ 220.00 │
# │ 4        ┆ Diana    ┆ North  ┆ 150.00 │
# │ 1        ┆ Alice    ┆ East   ┆ 120.00 │
# └──────────┴──────────┴────────┴────────┘


#--------------------------------------------------------------------------------------------------------------#
#---------------------------- 2. LazyFrame.sql(): lazy frame in, lazy frame out -------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
`LazyFrame.sql(...)` returns another LazyFrame.

This matches the usual Polars lazy workflow:
    1. Build the query plan.
    2. Keep chaining if needed.
    3. Call `.collect()` only when you want the materialized DataFrame.
'''

out_lf_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        customer,
        amount,
        quantity,
        amount * quantity AS revenue
    FROM self
    WHERE amount >= 100
    ORDER BY revenue DESC
    """
)

print(type(out_lf_sql))
# <class 'polars.lazyframe.frame.LazyFrame'>

print(out_lf_sql.collect())
# shape: (4, 5)
# ┌──────────┬──────────┬────────┬──────────┬─────────┐
# │ order_id ┆ customer ┆ amount ┆ quantity ┆ revenue │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---     │
# │ i64      ┆ str      ┆ f64    ┆ i64      ┆ f64     │
# ╞══════════╪══════════╪════════╪══════════╪═════════╡
# │ 6        ┆ Evan     ┆ 310.00 ┆ 4        ┆ 1240.00 │
# │ 3        ┆ Alice    ┆ 220.00 ┆ 3        ┆ 660.00  │
# │ 4        ┆ Diana    ┆ 150.00 ┆ 2        ┆ 300.00  │
# │ 1        ┆ Alice    ┆ 120.00 ┆ 2        ┆ 240.00  │
# └──────────┴──────────┴────────┴──────────┴─────────┘


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 3. Rename the special `self` table -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
You do not have to use the table name `self`.

Frame-level `.sql(...)` has a `table_name=` parameter. This is useful when the SQL
query is easier to read with a real table name.
'''

out_named_table = lf_orders.sql(
    table_name="orders", # specify table name
    query="""
    SELECT
        order_id,
        customer,
        region,
        amount
    FROM orders
    WHERE region = 'North'
    ORDER BY amount DESC
    """
)

print(out_named_table.collect())
# shape: (2, 4)
# ┌──────────┬──────────┬────────┬────────┐
# │ order_id ┆ customer ┆ region ┆ amount │
# │ ---      ┆ ---      ┆ ---    ┆ ---    │
# │ i64      ┆ str      ┆ str    ┆ f64    │
# ╞══════════╪══════════╪════════╪════════╡
# │ 6        ┆ Evan     ┆ North  ┆ 310.00 │
# │ 4        ┆ Diana    ┆ North  ┆ 150.00 │
# └──────────┴──────────┴────────┴────────┘


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------- 4. SQL query vs native Polars query ---------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The main learning strategy in these files should be:

    SQL version
    native Polars equivalent

This makes SQL feel like another syntax for Polars query expressions, not like a separate tool.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        customer,
        region,
        amount * quantity AS revenue
    FROM self
    WHERE amount >= 100
    ORDER BY customer, revenue
    """
)
print(out_sql.collect())
# shape: (4, 3)
# ┌──────────┬────────┬─────────┐
# │ customer ┆ region ┆ revenue │
# │ ---      ┆ ---    ┆ ---     │
# │ str      ┆ str    ┆ f64     │
# ╞══════════╪════════╪═════════╡
# │ Alice    ┆ East   ┆ 240.00  │
# │ Alice    ┆ East   ┆ 660.00  │
# │ Diana    ┆ North  ┆ 300.00  │
# │ Evan     ┆ North  ┆ 1240.00 │
# └──────────┴────────┴─────────┘

out_native = (
    lf_orders
    .filter(c("amount") >= 100)
    .select(
        c("customer"),
        c("region"),
        (c("amount") * c("quantity")).alias("revenue"),
    )
    .sort("customer", "revenue")
)
print(out_native.collect())
# shape: (4, 3)
# ┌──────────┬────────┬─────────┐
# │ customer ┆ region ┆ revenue │
# │ ---      ┆ ---    ┆ ---     │
# │ str      ┆ str    ┆ f64     │
# ╞══════════╪════════╪═════════╡
# │ Alice    ┆ East   ┆ 240.00  │
# │ Alice    ┆ East   ┆ 660.00  │
# │ Diana    ┆ North  ┆ 300.00  │
# │ Evan     ┆ North  ┆ 1240.00 │
# └──────────┴────────┴─────────┘

# This is optional, but very useful in tutorial files to verify equivalence.
assert_frame_equal(out_sql.collect(), out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 5. SQLContext: explicit tables ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Frame-level `.sql(...)` is best when you want to query one frame.

`SQLContext` is better when you want:
+ multiple tables
+ explicit table registration
+ reusable SQL context
+ more control over eager/lazy output

This first file only gives a small preview. File 02 should go deeper into
registration patterns.
'''

ctx = pl.SQLContext(
    orders=lf_orders,
    customers=df_customers,
)

out_ctx_lazy = ctx.execute(
    """
    SELECT
        o.order_id,
        o.customer,
        c.segment,
        o.amount
    FROM orders AS o
    LEFT JOIN customers AS c
        ON o.customer_id = c.customer_id
    WHERE o.amount >= 100
    ORDER BY o.order_id
    """
)

print(type(out_ctx_lazy))
# <class 'polars.lazyframe.frame.LazyFrame'>

print(out_ctx_lazy.collect())
# shape: (4, 4)
# ┌──────────┬──────────┬────────────┬────────┐
# │ order_id ┆ customer ┆ segment    ┆ amount │
# │ ---      ┆ ---      ┆ ---        ┆ ---    │
# │ i64      ┆ str      ┆ str        ┆ f64    │
# ╞══════════╪══════════╪════════════╪════════╡
# │ 1        ┆ Alice    ┆ Consumer   ┆ 120.00 │
# │ 3        ┆ Alice    ┆ Consumer   ┆ 220.00 │
# │ 4        ┆ Diana    ┆ Consumer   ┆ 150.00 │
# │ 6        ┆ Evan     ┆ Enterprise ┆ 310.00 │
# └──────────┴──────────┴────────────┴────────┘

################################################################

# You can also ask SQLContext.execute(...) to return an eager DataFrame.
out_ctx_eager = ctx.execute(
    """
    SELECT
        region,
        COUNT(*) AS n_orders,
        SUM(amount) AS total_amount
    FROM orders
    GROUP BY region
    ORDER BY region
    """,
    eager=True, # realize and return an eager dataframe
)

print(type(out_ctx_eager))
# <class 'polars.dataframe.frame.DataFrame'>

print(out_ctx_eager)
# shape: (3, 3)
# ┌────────┬──────────┬──────────────┐
# │ region ┆ n_orders ┆ total_amount │
# │ ---    ┆ ---      ┆ ---          │
# │ str    ┆ u32      ┆ f64          │
# ╞════════╪══════════╪══════════════╡
# │ East   ┆ 2        ┆ 340.00       │
# │ North  ┆ 2        ┆ 460.00       │
# │ West   ┆ 2        ┆ 170.00       │
# └────────┴──────────┴──────────────┘


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 6. pl.sql(): global shortcut -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
`pl.sql(...)` is a shortcut that can query compatible frame objects from the
current/global context.

This is convenient in notebooks and quick exploration.
For scripts, teaching files, or larger projects, `SQLContext` is usually clearer
because table registration is explicit.

Because this script defines `lf_orders` at module scope, `pl.sql(...)` can refer
to it by variable name.
'''

out_global_sql = pl.sql(
    """
    SELECT
        customer,
        SUM(amount) AS total_amount
    FROM lf_orders
    GROUP BY customer
    ORDER BY total_amount DESC
    """
)

print(type(out_global_sql))
# <class 'polars.lazyframe.frame.LazyFrame'>

print(out_global_sql.collect())
# shape: (4, 2)
# ┌──────────┬──────────────┐
# │ customer ┆ total_amount │
# │ ---      ┆ ---          │
# │ str      ┆ f64          │
# ╞══════════╪══════════════╡
# │ Alice    ┆ 340.00       │
# │ Evan     ┆ 310.00       │
# │ Bob      ┆ 170.00       │
# │ Diana    ┆ 150.00       │
# └──────────┴──────────────┘


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------- 7. Mix SQL with normal Polars chaining --------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
SQL does not replace the native Polars API.

A very practical pattern is:
    use SQL for the part that is clearer in SQL,
    then continue with normal Polars expressions.
'''

out_mixed = (
    lf_orders
    .sql(
        """
        SELECT
            order_id,
            customer,
            amount * quantity AS revenue
        FROM self
        """
    )
    .filter(c("revenue") >= 300)
    .with_columns(
        (c("revenue") / 100).round(2).alias("revenue_hundreds")
    )
    .sort("revenue", descending=True)
)

print(out_mixed.collect())
# shape: (3, 4)
# ┌──────────┬──────────┬─────────┬──────────────────┐
# │ order_id ┆ customer ┆ revenue ┆ revenue_hundreds │
# │ ---      ┆ ---      ┆ ---     ┆ ---              │
# │ i64      ┆ str      ┆ f64     ┆ f64              │
# ╞══════════╪══════════╪═════════╪══════════════════╡
# │ 6        ┆ Evan     ┆ 1240.00 ┆ 12.40            │
# │ 3        ┆ Alice    ┆ 660.00  ┆ 6.60             │
# │ 4        ┆ Diana    ┆ 300.00  ┆ 3.00             │
# └──────────┴──────────┴─────────┴──────────────────┘


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 8. Common beginner mistakes ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Common mistakes:

1. Forgetting the table name.

   Wrong:
       SELECT order_id, amount WHERE amount > 100

   Right:
       SELECT order_id, amount FROM self WHERE amount > 100

2. Using `self` after changing `table_name=`.

   If you write `table_name="orders"`, then use:
       FROM orders

3. Expecting `LazyFrame.sql(...)` or `SQLContext.execute(...)` to immediately print rows.
   They usually return a LazyFrame. Use `.collect()` when you want results.

4. Thinking Polars SQL is a full database engine.
   It is a SQL interface for Polars queries. For data transformation workflows,
   you usually read/scan data with Polars, query it with SQL or expressions,
   and write results with Polars.

5. Overusing SQL when native Polars is clearer.
   SQL is useful, but Polars expressions are often better
   for schema-aware column selection, selectors, nested data, and custom pipelines.
'''


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 9. Quick summary ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Quick mental map:

1. One eager DataFrame:
       df.sql("SELECT ... FROM self ...")
       -> returns DataFrame

2. One LazyFrame:
       lf.sql("SELECT ... FROM self ...")
       -> returns LazyFrame
       -> use `.collect()`

3. One frame but with a nicer table name:
       lf.sql("SELECT ... FROM orders ...", table_name="orders")

4. Multiple explicit tables:
       ctx = pl.SQLContext(orders=lf_orders, customers=df_customers)
       ctx.execute("SELECT ... FROM orders JOIN customers ...")
       -> usually returns LazyFrame
       -> use `.collect()` or `eager=True`

5. Notebook/global shortcut:
       pl.sql("SELECT ... FROM lf_orders ...")
       -> convenient, but less explicit than SQLContext

6. SQL + native Polars:
       lf.sql("SELECT ... FROM self ...").filter(...).with_columns(...).collect()
'''
