'''
Polars SQL: registering tables and data sources with SQLContext.

This file expands the first SQL intro file by focusing on table registration.

Main ideas:
1. `SQLContext` is a table registry for SQL queries.
2. A registered table name can point to either a DataFrame or a LazyFrame.
3. You can register tables when creating the context:
      + pl.SQLContext(orders=df_orders)
      + pl.SQLContext(frames={"orders": df_orders})
      + pl.SQLContext(register_globals=True)
4. You can register more tables after construction:
      + ctx.register("orders", df_orders)
      + ctx.register_many({"orders": df_orders, "customers": df_customers})
      + ctx.register_many(orders=df_orders, customers=df_customers)
      + ctx.register_globals()
5. Use ctx.tables() or SQL `SHOW TABLES` to inspect registered table names.
6. Use ctx.unregister(...) or a context-manager scope to control table lifetime.
7. Registering LazyFrames is usually preferred for large files because the SQL
   query can still benefit from lazy optimization and pushdown.

Important mental model:
+ Frame-level `.sql(...)` gives one automatic table, usually named `self`.
+ `SQLContext` is the explicit way to query multiple named tables.
+ SQL table names are not file paths. A table name is just the identifier that
  the context maps to a DataFrame or LazyFrame.

Polars docs checked while writing this file:
+ https://docs.pola.rs/user-guide/sql/intro/
+ https://docs.pola.rs/api/python/stable/reference/sql/python_api.html
+ https://docs.pola.rs/api/python/stable/reference/sql/api/polars.SQLContext.register.html
+ https://docs.pola.rs/api/python/stable/reference/sql/api/polars.SQLContext.register_many.html
+ https://docs.pola.rs/api/python/stable/reference/sql/api/polars.SQLContext.register_globals.html
+ https://docs.pola.rs/api/python/stable/reference/sql/api/polars.SQLContext.tables.html
+ https://docs.pola.rs/api/python/stable/reference/sql/api/polars.SQLContext.unregister.html
+ https://docs.pola.rs/api/python/stable/reference/sql/api/polars.SQLContext.execute.html
'''

from pathlib import Path
from tempfile import TemporaryDirectory

import polars as pl
from polars import col as c
from polars.testing import assert_frame_equal

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_tbl_width_chars(120)
pl.Config.set_float_precision(2)


# =========================================================================================
# 0. Setup Data
# =========================================================================================
'''
Use small self-contained tables.

The point of this file is not SQL syntax yet. The point is how DataFrames and
LazyFrames become named SQL tables.
'''

df_orders = pl.DataFrame(
    {
        "order_id": [1, 2, 3, 4, 5, 6],
        "customer_id": [101, 102, 101, 103, 102, 104],
        "region": ["East", "West", "East", "North", "West", "North"],
        "amount": [120.0, 80.0, 220.0, 150.0, 90.0, 310.0],
        "quantity": [2, 1, 3, 2, 1, 4],
    }
)

lf_orders = df_orders.lazy()

print(df_orders)
# shape: (6, 5)
# ┌──────────┬─────────────┬────────┬────────┬──────────┐
# │ order_id ┆ customer_id ┆ region ┆ amount ┆ quantity │
# │ ---      ┆ ---         ┆ ---    ┆ ---    ┆ ---      │
# │ i64      ┆ i64         ┆ str    ┆ f64    ┆ i64      │
# ╞══════════╪═════════════╪════════╪════════╪══════════╡
# │ 1        ┆ 101         ┆ East   ┆ 120.00 ┆ 2        │
# │ 2        ┆ 102         ┆ West   ┆ 80.00  ┆ 1        │
# │ 3        ┆ 101         ┆ East   ┆ 220.00 ┆ 3        │
# │ 4        ┆ 103         ┆ North  ┆ 150.00 ┆ 2        │
# │ 5        ┆ 102         ┆ West   ┆ 90.00  ┆ 1        │
# │ 6        ┆ 104         ┆ North  ┆ 310.00 ┆ 4        │
# └──────────┴─────────────┴────────┴────────┴──────────┘

##----------------------------------##

df_customers = pl.DataFrame(
    {
        "customer_id": [101, 102, 103, 104, 105],
        "customer": ["Alice", "Bob", "Diana", "Evan", "Frank"],
        "segment": ["Consumer", "Business", "Consumer", "Enterprise", "Business"],
    }
)

lf_customers = df_customers.lazy()

print(df_customers)
# shape: (5, 3)
# ┌─────────────┬──────────┬────────────┐
# │ customer_id ┆ customer ┆ segment    │
# │ ---         ┆ ---      ┆ ---        │
# │ i64         ┆ str      ┆ str        │
# ╞═════════════╪══════════╪════════════╡
# │ 101         ┆ Alice    ┆ Consumer   │
# │ 102         ┆ Bob      ┆ Business   │
# │ 103         ┆ Diana    ┆ Consumer   │
# │ 104         ┆ Evan     ┆ Enterprise │
# │ 105         ┆ Frank    ┆ Business   │
# └─────────────┴──────────┴────────────┘

##----------------------------------##

df_regions = pl.DataFrame(
    {
        "region": ["East", "West", "North", "South"],
        "manager": ["Mia", "Noah", "Olivia", "Liam"],
    }
)

print(df_regions)
# shape: (4, 2)
# ┌────────┬─────────┐
# │ region ┆ manager │
# │ ---    ┆ ---     │
# │ str    ┆ str     │
# ╞════════╪═════════╡
# │ East   ┆ Mia     │
# │ West   ┆ Noah    │
# │ North  ┆ Olivia  │
# │ South  ┆ Liam    │
# └────────┴─────────┘


# =========================================================================================
# 1. Empty SQLContext + register one table
# =========================================================================================
'''
Start with an empty SQLContext, then register one frame.

`register(name, frame)` associates a table name with a DataFrame or LazyFrame.
The method returns the context itself, so it can be chained.
'''

ctx = pl.SQLContext()
ctx.register("orders", lf_orders)

print(ctx.tables())
# ['orders']

out = ctx.execute(
    """
    SELECT
        order_id,
        customer_id,
        amount
    FROM orders
    WHERE amount >= 100
    ORDER BY amount DESC
    """
)

# SQLContext.execute(...) returns a LazyFrame by default.
print(type(out))
print(out.collect())
# <class 'polars.lazyframe.frame.LazyFrame'>
# shape: (4, 3)
# ┌──────────┬─────────────┬────────┐
# │ order_id ┆ customer_id ┆ amount │
# │ ---      ┆ ---         ┆ ---    │
# │ i64      ┆ i64         ┆ f64    │
# ╞══════════╪═════════════╪════════╡
# │ 6        ┆ 104         ┆ 310.00 │
# │ 3        ┆ 101         ┆ 220.00 │
# │ 4        ┆ 103         ┆ 150.00 │
# │ 1        ┆ 101         ┆ 120.00 │
# └──────────┴─────────────┴────────┘


# =========================================================================================
# 2. Register multiple tables by chaining
# =========================================================================================
'''
You can call `.register(...)` repeatedly when the table list is small.

This is often the clearest style when you want to emphasize each table name.
'''

ctx = (
    pl.SQLContext()
    .register("orders", lf_orders)
    .register("customers", lf_customers)
)

print(ctx.tables())
# ['customers', 'orders']

orders_with_customers_sql = ctx.execute(
    """
    SELECT
        o.order_id,
        c.customer,
        c.segment,
        o.region,
        o.amount,
        o.quantity,
        o.amount * o.quantity AS revenue
    FROM orders AS o
    LEFT JOIN customers AS c
        ON o.customer_id = c.customer_id
    ORDER BY o.order_id
    """
)
print(orders_with_customers_sql.collect())
# shape: (6, 7)
# ┌──────────┬──────────┬────────────┬────────┬────────┬──────────┬─────────┐
# │ order_id ┆ customer ┆ segment    ┆ region ┆ amount ┆ quantity ┆ revenue │
# │ ---      ┆ ---      ┆ ---        ┆ ---    ┆ ---    ┆ ---      ┆ ---     │
# │ i64      ┆ str      ┆ str        ┆ str    ┆ f64    ┆ i64      ┆ f64     │
# ╞══════════╪══════════╪════════════╪════════╪════════╪══════════╪═════════╡
# │ 1        ┆ Alice    ┆ Consumer   ┆ East   ┆ 120.00 ┆ 2        ┆ 240.00  │
# │ 2        ┆ Bob      ┆ Business   ┆ West   ┆ 80.00  ┆ 1        ┆ 80.00   │
# │ 3        ┆ Alice    ┆ Consumer   ┆ East   ┆ 220.00 ┆ 3        ┆ 660.00  │
# │ 4        ┆ Diana    ┆ Consumer   ┆ North  ┆ 150.00 ┆ 2        ┆ 300.00  │
# │ 5        ┆ Bob      ┆ Business   ┆ West   ┆ 90.00  ┆ 1        ┆ 90.00   │
# │ 6        ┆ Evan     ┆ Enterprise ┆ North  ┆ 310.00 ┆ 4        ┆ 1240.00 │
# └──────────┴──────────┴────────────┴────────┴────────┴──────────┴─────────┘

orders_with_customers_native = (
    lf_orders
    .join(lf_customers, on="customer_id", how="left")
    .select(
        "order_id",
        "customer",
        "segment",
        "region",
        "amount",
        "quantity",
        (c("amount") * c("quantity")).alias("revenue"),
    )
    .sort("order_id")
)

assert_frame_equal(
    orders_with_customers_sql.collect(),
    orders_with_customers_native.collect(),
)


# =========================================================================================
# 3. Register tables at SQLContext construction
# =========================================================================================
'''
For reusable SQL examples, it is often clean to register the tables directly in
`SQLContext(...)`.

Option A: use keyword arguments.
The keyword becomes the SQL table name.
'''

ctx_kwargs = pl.SQLContext(
    orders=lf_orders,
    customers=lf_customers,
    regions=df_regions,
)

print(ctx_kwargs.tables())
# ['customers', 'orders', 'regions']

print(
    ctx_kwargs.execute(
        """
        SELECT
            o.order_id,
            c.customer,
            r.manager,
            o.region,
            o.amount
        FROM orders AS o
        LEFT JOIN customers AS c
            ON o.customer_id = c.customer_id
        LEFT JOIN regions AS r
            ON o.region = r.region
        ORDER BY o.order_id
        """
    ).collect()
)
# shape: (6, 5)
# ┌──────────┬──────────┬─────────┬────────┬────────┐
# │ order_id ┆ customer ┆ manager ┆ region ┆ amount │
# │ ---      ┆ ---      ┆ ---     ┆ ---    ┆ ---    │
# │ i64      ┆ str      ┆ str     ┆ str    ┆ f64    │
# ╞══════════╪══════════╪═════════╪════════╪════════╡
# │ 1        ┆ Alice    ┆ Mia     ┆ East   ┆ 120.00 │
# │ 2        ┆ Bob      ┆ Noah    ┆ West   ┆ 80.00  │
# │ 3        ┆ Alice    ┆ Mia     ┆ East   ┆ 220.00 │
# │ 4        ┆ Diana    ┆ Olivia  ┆ North  ┆ 150.00 │
# │ 5        ┆ Bob      ┆ Noah    ┆ West   ┆ 90.00  │
# │ 6        ┆ Evan     ┆ Olivia  ┆ North  ┆ 310.00 │
# └──────────┴──────────┴─────────┴────────┴────────┘

'''
Option B: use the `frames={...}` mapping.

This is useful when table names are dynamic or stored in a dictionary.
'''

source_tables = {
    "orders": lf_orders,
    "customers": lf_customers,
    "regions": df_regions,
}

ctx_mapping = pl.SQLContext(frames=source_tables)
print(ctx_mapping.tables())
# ['customers', 'orders', 'regions']

print(
    ctx_mapping.execute(
        """
        SELECT
            region,
            manager
        FROM regions
        ORDER BY region
        """
    ).collect()
)
# shape: (4, 2)
# ┌────────┬─────────┐
# │ region ┆ manager │
# │ ---    ┆ ---     │
# │ str    ┆ str     │
# ╞════════╪═════════╡
# │ East   ┆ Mia     │
# │ North  ┆ Olivia  │
# │ South  ┆ Liam    │
# │ West   ┆ Noah    │
# └────────┴─────────┘



# =========================================================================================
# 4. register_many(): mapping and kwargs
# =========================================================================================
'''
`register_many(...)` is a convenient way to add several tables after the context
already exists.

It accepts:
+ a mapping: {"name": frame, ...}
+ keyword arguments: name=frame
'''

ctx_many = pl.SQLContext()

ctx_many.register_many(
    {
        "orders": lf_orders,
        "customers": lf_customers,
    }
)

print(ctx_many.tables())
# ['customers', 'orders']

ctx_many.register_many(regions=df_regions)
print(ctx_many.tables())
# ['customers', 'orders', 'regions']

print(
    ctx_many.execute(
        """
        SELECT
            r.region,
            r.manager,
            COUNT(o.order_id) AS n_orders,
            SUM(o.amount) AS total_amount
        FROM regions AS r
        LEFT JOIN orders AS o
            ON r.region = o.region
        GROUP BY r.region, r.manager
        ORDER BY r.region
        """
    ).collect()
)
# shape: (4, 4)
# ┌────────┬─────────┬──────────┬──────────────┐
# │ region ┆ manager ┆ n_orders ┆ total_amount │
# │ ---    ┆ ---     ┆ ---      ┆ ---          │
# │ str    ┆ str     ┆ u32      ┆ f64          │
# ╞════════╪═════════╪══════════╪══════════════╡
# │ East   ┆ Mia     ┆ 2        ┆ 340.00       │
# │ North  ┆ Olivia  ┆ 2        ┆ 460.00       │
# │ South  ┆ Liam    ┆ 0        ┆ 0.00         │
# │ West   ┆ Noah    ┆ 2        ┆ 170.00       │
# └────────┴─────────┴──────────┴──────────────┘


# =========================================================================================
# 5. tables() and SHOW TABLES
# =========================================================================================
'''
`ctx.tables()` returns a Python list of registered table names.

`SHOW TABLES` returns the same information as a SQL result frame.
Use whichever form is more convenient for your workflow.
'''

print(ctx_many.tables())
# ['customers', 'orders', 'regions']

show_tables_lazy = ctx_many.execute("SHOW TABLES")
print(type(show_tables_lazy))
print(show_tables_lazy.collect())
# <class 'polars.lazyframe.frame.LazyFrame'>
# shape: (3, 1)
# ┌───────────┐
# │ name      │
# │ ---       │
# │ str       │
# ╞═══════════╡
# │ customers │
# │ orders    │
# │ regions   │
# └───────────┘

# Ask execute(...) to collect immediately.
show_tables_eager = ctx_many.execute("SHOW TABLES", eager=True)
print(type(show_tables_eager))
print(show_tables_eager)
# <class 'polars.dataframe.frame.DataFrame'>
# shape: (3, 1)
# ┌───────────┐
# │ name      │
# │ ---       │
# │ str       │
# ╞═══════════╡
# │ customers │
# │ orders    │
# │ regions   │
# └───────────┘


# =========================================================================================
# 6. eager=True: only controls the returned Python type
# =========================================================================================
'''
By default, SQLContext returns a LazyFrame from execute(...).

If you create the context with eager=True, or call execute(..., eager=True),
Polars returns a DataFrame instead.

Important:
The SQL query itself is still planned through the lazy engine; eager=True only
controls whether the result is collected before being returned to Python.
'''

ctx_lazy_default = pl.SQLContext(orders=lf_orders)
result_lazy = ctx_lazy_default.execute("SELECT * FROM orders WHERE amount > 100")
print(type(result_lazy))
print(result_lazy.collect())

ctx_eager_default = pl.SQLContext(orders=lf_orders, eager=True)
result_eager = ctx_eager_default.execute("SELECT * FROM orders WHERE amount > 100")
print(type(result_eager))
print(result_eager)

# Per-query eager=True overrides the context default.
result_eager_once = ctx_lazy_default.execute(
    "SELECT * FROM orders WHERE amount > 100",
    eager=True,
)
print(type(result_eager_once))
print(result_eager_once)


# =========================================================================================
# 7. Register LazyFrames that come from file scans
# =========================================================================================
'''
A SQL table can be backed by a LazyFrame from `pl.scan_csv(...)`, `pl.scan_parquet(...)`,
or another scan source.

This is usually better than reading the full file eagerly first, because the SQL
query can still benefit from lazy optimization such as projection/filter pushdown
when the source supports it.

This section writes tiny temporary CSV files only to make the example completely
self-contained. In a real project, the paths would point to your actual data files.
'''

with TemporaryDirectory() as tmp_dir:
    tmp_path = Path(tmp_dir)
    orders_path = tmp_path / "orders.csv"
    customers_path = tmp_path / "customers.csv"

    df_orders.write_csv(orders_path)
    df_customers.write_csv(customers_path)

    lf_orders_from_file = pl.scan_csv(orders_path)
    lf_customers_from_file = pl.scan_csv(customers_path)

    ctx_files = pl.SQLContext(
        orders_file=lf_orders_from_file,
        customers_file=lf_customers_from_file,
    )

    print(ctx_files.tables())

    print(
        ctx_files.execute(
            """
            SELECT
                c.segment,
                COUNT(o.order_id) AS n_orders,
                SUM(o.amount * o.quantity) AS total_revenue
            FROM orders_file AS o
            LEFT JOIN customers_file AS c
                ON o.customer_id = c.customer_id
            GROUP BY c.segment
            ORDER BY total_revenue DESC
            """
        ).collect()
    )

'''
Important lifetime note:
If the registered table is a LazyFrame that scans a file, the file must still
exist when the SQL result is collected. The file is not necessarily read at
registration time.
'''


# =========================================================================================
# 8. register_globals(): convenient, but use carefully
# =========================================================================================
'''
`register_globals=True` automatically registers compatible frame objects from the
global namespace using their Python variable names as SQL table names.

This is convenient in notebooks and quick experiments.

In scripts and teaching files, explicit registration is usually clearer because
it avoids accidentally registering unrelated DataFrames/LazyFrames.
'''

# These two variables intentionally have names that we will query as SQL tables.
df_global_demo = pl.DataFrame(
    {
        "a": [1, 2, 3],
        "label": ["x", "y", "z"],
    }
)

lf_global_demo = pl.LazyFrame(
    {
        "a": [2, 3, 4],
        "value": [20, 30, 40],
    }
)

ctx_globals = pl.SQLContext(register_globals=True)

# The context may contain other global frames too, so print only the two names
# this example cares about.
global_names = ctx_globals.tables()
print([name for name in ["df_global_demo", "lf_global_demo"] if name in global_names])

print(
    ctx_globals.execute(
        """
        SELECT
            g1.a,
            g1.label,
            g2.value
        FROM df_global_demo AS g1
        LEFT JOIN lf_global_demo AS g2
            ON g1.a = g2.a
        ORDER BY g1.a
        """
    ).collect()
)

# You can also call register_globals() on an existing context.
ctx_register_later = pl.SQLContext()
ctx_register_later.register_globals()
print([name for name in ["df_global_demo", "lf_global_demo"] if name in ctx_register_later.tables()])


# =========================================================================================
# 9. unregister(): remove table names
# =========================================================================================
'''
Use `unregister(...)` when a table name should no longer be available.

It accepts either:
+ one table name as a string
+ several names as a list/collection
'''

ctx_remove = pl.SQLContext(
    orders=lf_orders,
    customers=lf_customers,
    regions=df_regions,
)

print(ctx_remove.tables())
# ['customers', 'orders', 'regions']

ctx_remove.unregister("regions")
print(ctx_remove.tables())
# ['customers', 'orders']

ctx_remove.unregister(["orders", "customers"])
print(ctx_remove.tables())
# []


# =========================================================================================
# 10. Context-manager scope for temporary tables
# =========================================================================================
'''
`SQLContext` can be used as a context manager.

Tables registered inside the `with` scope are automatically unregistered when the
scope exits. Tables registered when the context was constructed persist.
'''

ctx_scope = pl.SQLContext(base_orders=lf_orders)
print(ctx_scope.tables())
# ['base_orders']

with ctx_scope:
    ctx_scope.register_many(
        temp_customers=lf_customers,
        temp_regions=df_regions,
    )
    print(ctx_scope.tables())
    # ['base_orders', 'temp_customers', 'temp_regions']

    print(
        ctx_scope.execute(
            """
            SELECT
                o.order_id,
                c.customer,
                r.manager
            FROM base_orders AS o
            LEFT JOIN temp_customers AS c
                ON o.customer_id = c.customer_id
            LEFT JOIN temp_regions AS r
                ON o.region = r.region
            ORDER BY o.order_id
            """
        ).collect()
    )

# The temporary tables registered inside the with-block are gone.
print(ctx_scope.tables())
# ['base_orders']


# =========================================================================================
# 11. Practical naming advice for SQL tables
# =========================================================================================
'''
Practical advice:

1. Prefer simple SQL table names:
       orders, customers, sales_2024, product_master

2. Avoid spaces, dots, punctuation, and mixed-case names when possible.
   They are legal only with proper SQL identifier quoting, which makes examples
   noisier. Identifier quoting is covered later in the SELECT/alias file.

3. Register LazyFrames for large files:
       ctx.register("orders", pl.scan_csv("orders.csv"))

4. Keep SQLContext setup near the query when writing teaching code. It should be
   obvious where each SQL table name came from.

5. Use `ctx.tables()` or `SHOW TABLES` before debugging a query that says a table
   was not found.
'''


# =========================================================================================
# 12. Quick summary
# =========================================================================================
'''
Quick map:

Frame-level SQL:
    lf.sql("SELECT * FROM self")
        Good for one table.

SQLContext with kwargs:
    ctx = pl.SQLContext(orders=lf_orders, customers=lf_customers)
        Good for simple scripts and tutorials.

SQLContext with mapping:
    ctx = pl.SQLContext(frames={"orders": lf_orders, "customers": lf_customers})
        Good when table names are dynamic.

Add tables later:
    ctx.register("orders", lf_orders)
    ctx.register_many({"orders": lf_orders, "customers": lf_customers})
    ctx.register_many(orders=lf_orders, customers=lf_customers)

Inspect tables:
    ctx.tables()
    ctx.execute("SHOW TABLES").collect()

Remove tables:
    ctx.unregister("orders")
    ctx.unregister(["orders", "customers"])

Control result materialization:
    ctx.execute("SELECT ...")              -> LazyFrame by default
    ctx.execute("SELECT ...", eager=True)  -> DataFrame
    pl.SQLContext(..., eager=True)          -> DataFrame by default from execute(...)
'''
