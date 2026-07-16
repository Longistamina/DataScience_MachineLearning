'''
Polars SQL: read/scan-style table functions in SQL queries.

This file adapts the regular Polars read/scan workflow to Polars SQL.

Main ideas:
1. Polars SQL can read some files directly inside the SQL FROM clause with
   table functions such as:
       + read_csv('path.csv')
       + read_parquet('path.parquet')
       + read_json('path.ndjson')
       + read_ipc('path.arrow') / read_ipc('path.ipc')
2. A table function behaves like a temporary SQL table produced from the file.
3. You do not need to register the file in SQLContext first when using a table
   function directly.
4. SQLContext.execute(...) returns a LazyFrame by default, so call .collect()
   when you want the result.
5. These examples intentionally show only one compact example per table-function
   API. The detailed native read/scan APIs belong in the separate read/scan file.
6. For unsupported file formats or highly customized parsing options, use the
   native Polars reader/scanner first, then register the DataFrame/LazyFrame in
   SQLContext.

Important distinction:
+ Native Polars has many read/scan APIs: read_csv, scan_csv, read_excel,
  read_json, read_ndjson, scan_ndjson, scan_parquet, scan_ipc, scan_delta,
  scan_lines, scan_pyarrow_dataset, read_database, and more.
+ Polars SQL table functions are a smaller SQL-facing convenience layer. The
  documented table-function examples focus on CSV, Parquet, JSON, and IPC.
+ Important correction: the SQL table function is named read_json(...), but in
  current Polars it uses the NDJSON / JSON-lines reader internally. A standard
  row-oriented JSON array such as [ {...}, {...} ] will fail with an error like:
      ComputeError: Syntax at character 0 ('[')
  Use native pl.read_json(...) first for that format, then register the result
  if you want to query it with SQL.

Polars docs/source checked while writing this file:
+ https://docs.pola.rs/user-guide/sql/select/#table-functions
+ https://docs.pola.rs/user-guide/io/
+ https://docs.pola.rs/user-guide/io/parquet/
+ https://docs.pola.rs/api/python/stable/reference/sql/api/polars.SQLContext.execute.html
+ https://github.com/pola-rs/polars/blob/main/crates/polars-sql/src/table_functions.rs
'''

import json
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


def sql_path(path: Path) -> str:
    '''Return a file path that is safe to place inside a single-quoted SQL string.'''
    return path.as_posix().replace("'", "''")


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 0. Setup Data --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Use tiny temporary files so the examples are completely self-contained.

In a real project, replace these temporary paths with paths to your own CSV,
Parquet, NDJSON, JSON, or IPC files.
'''

with TemporaryDirectory() as tmp_dir:
    tmp_path = Path(tmp_dir)

    # One dataset reused for CSV and Parquet examples.
    df_orders = pl.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5, 6],
            "customer": ["Alice", "Bob", "Alice", "Diana", "Bob", "Evan"],
            "region": ["East", "West", "East", "North", "West", "North"],
            "amount": [120.0, 80.0, 220.0, 150.0, 90.0, 310.0],
            "quantity": [2, 1, 3, 2, 1, 4],
        }
    )

    # A second simple dataset for JSON / NDJSON.
    df_products = pl.DataFrame(
        {
            "product_id": [101, 102, 103, 104],
            "product": ["Keyboard", "Mouse", "Monitor", "Desk"],
            "category": ["Electronics", "Electronics", "Electronics", "Furniture"],
            "price": [45.0, 25.0, 180.0, 320.0],
        }
    )

    # A third simple dataset for IPC.
    df_cities = pl.DataFrame(
        {
            "country": ["USA", "USA", "USA", "Netherlands"],
            "city": ["New York", "Los Angeles", "Chicago", "Amsterdam"],
            "population": [8_399_000, 3_997_000, 2_705_000, 900_000],
        }
    )

    csv_path = tmp_path / "orders.csv"
    parquet_path = tmp_path / "orders.parquet"
    ndjson_path = tmp_path / "products.ndjson"
    standard_json_path = tmp_path / "products_array.json"
    ipc_path = tmp_path / "cities.arrow"

    df_orders.write_csv(csv_path)
    df_orders.write_parquet(parquet_path)
    df_products.write_ndjson(ndjson_path)

    # This is a standard JSON array. It is NOT used with SQL read_json(...).
    # It is used later to show the native-read-then-register fallback pattern.
    standard_json_path.write_text(
        json.dumps(df_products.to_dicts(), indent=4),
        encoding="utf-8",
    )

    df_cities.write_ipc(ipc_path)

    ctx = pl.SQLContext()

    print(df_orders)
    print(df_products)
    print(df_cities)


    #----------------------------------------------------------------------------------------------------------#
    #-------------------------------------- 1. read_csv('path.csv') -------------------------------------------#
    #----------------------------------------------------------------------------------------------------------#
    '''
    read_csv(...) reads a CSV file directly from the SQL query.

    This is the SQL table-function version of starting from pl.scan_csv(...)
    when you want to stay lazy.
    '''

    out_csv_sql = ctx.execute(
        f"""
        SELECT
            order_id,
            customer,
            region,
            amount
        FROM read_csv('{sql_path(csv_path)}')
        WHERE amount >= 100
        ORDER BY order_id
        """
    )

    print(type(out_csv_sql))
    print(out_csv_sql.collect())

    out_csv_native = (
        pl.scan_csv(csv_path)
        .filter(c("amount") >= 100)
        .select("order_id", "customer", "region", "amount")
        .sort("order_id")
    )

    assert_frame_equal(out_csv_sql.collect(), out_csv_native.collect())


    #----------------------------------------------------------------------------------------------------------#
    #---------------------------------- 2. read_parquet('path.parquet') ---------------------------------------#
    #----------------------------------------------------------------------------------------------------------#
    '''
    read_parquet(...) reads a Parquet file directly from SQL.

    Parquet is a columnar format, so it is usually a better storage format than
    CSV for larger analytical workflows. Native Polars code would usually start
    from pl.scan_parquet(...).
    '''

    out_parquet_sql = ctx.execute(
        f"""
        SELECT
            region,
            COUNT(*) AS n_orders,
            SUM(amount * quantity) AS revenue
        FROM read_parquet('{sql_path(parquet_path)}')
        GROUP BY region
        ORDER BY revenue DESC
        """
    )

    print(out_parquet_sql.collect())

    out_parquet_native = (
        pl.scan_parquet(parquet_path)
        .group_by("region")
        .agg(
            pl.len().alias("n_orders"),
            (c("amount") * c("quantity")).sum().alias("revenue"),
        )
        .sort("revenue", descending=True)
    )

    assert_frame_equal(out_parquet_sql.collect(), out_parquet_native.collect())


    #----------------------------------------------------------------------------------------------------------#
    #------------------------------------- 3. read_json('path.ndjson') ----------------------------------------#
    #----------------------------------------------------------------------------------------------------------#
    '''
    read_json(...) reads an NDJSON / JSON-lines file directly from SQL.

    Important:
    Despite the SQL function name, current Polars SQL routes read_json(...) to
    the NDJSON lazy reader internally. Therefore the file should look like this:
        {"product_id":101,"product":"Keyboard",...}
        {"product_id":102,"product":"Mouse",...}

    A standard row-oriented JSON array like this will fail here:
        [
            {"product_id": 101, "product": "Keyboard", ...},
            {"product_id": 102, "product": "Mouse", ...}
        ]

    For standard JSON arrays, use native pl.read_json(...) first, then register
    the resulting DataFrame/LazyFrame in SQLContext.
    '''

    out_json_sql = ctx.execute(
        f"""
        SELECT
            product_id,
            product,
            category,
            price
        FROM read_json('{sql_path(ndjson_path)}')
        WHERE price >= 30
        ORDER BY price DESC
        """
    )

    print(out_json_sql.collect())

    out_json_native = (
        pl.scan_ndjson(ndjson_path)
        .filter(c("price") >= 30)
        .select("product_id", "product", "category", "price")
        .sort("price", descending=True)
    )

    assert_frame_equal(out_json_sql.collect(), out_json_native.collect())


    #----------------------------------------------------------------------------------------------------------#
    #--------------------------------------- 4. read_ipc('path.arrow') ----------------------------------------#
    #----------------------------------------------------------------------------------------------------------#
    '''
    read_ipc(...) reads an Arrow IPC/Feather-style file directly from SQL.

    Native Polars code would usually start from pl.scan_ipc(...) when you want
    the lazy version.
    '''

    out_ipc_sql = ctx.execute(
        f"""
        SELECT
            country,
            city,
            population
        FROM read_ipc('{sql_path(ipc_path)}')
        WHERE population >= 2000000
        ORDER BY population DESC
        """
    )

    print(out_ipc_sql.collect())

    out_ipc_native = (
        pl.scan_ipc(ipc_path)
        .filter(c("population") >= 2_000_000)
        .select("country", "city", "population")
        .sort("population", descending=True)
    )

    assert_frame_equal(out_ipc_sql.collect(), out_ipc_native.collect())


    #----------------------------------------------------------------------------------------------------------#
    #-------------------------- 5. When SQL table functions are not the best fit ------------------------------#
    #----------------------------------------------------------------------------------------------------------#
    '''
    The SQL table functions are convenient for quick one-off file queries.

    For other sources or more customized readers, prefer this pattern:
        1. Use the native Polars read/scan API.
        2. Register the resulting DataFrame/LazyFrame in SQLContext.
        3. Query the registered table with SQL.

    This keeps advanced reader options in the native API, where they are easiest
    to discover and type-check.

    Example fallback below:
    A standard JSON array is read with native pl.read_json(...), then queried
    with SQL after registration.
    '''

    ctx_standard_json = pl.SQLContext(
        products_array=pl.read_json(standard_json_path).lazy(),
    )

    out_standard_json_registered = ctx_standard_json.execute(
        """
        SELECT
            category,
            AVG(price) AS avg_price
        FROM products_array
        GROUP BY category
        ORDER BY category
        """
    )

    print(out_standard_json_registered.collect())

    out_standard_json_native = (
        pl.read_json(standard_json_path)
        .lazy()
        .group_by("category")
        .agg(c("price").mean().alias("avg_price"))
        .sort("category")
    )

    assert_frame_equal(out_standard_json_registered.collect(), out_standard_json_native.collect())


    #----------------------------------------------------------------------------------------------------------#
    #---------------------------------- 6. Practical path and source advice -----------------------------------#
    #----------------------------------------------------------------------------------------------------------#
    '''
    Practical advice:

    1. Use table functions for short, direct, one-off queries:
           SELECT * FROM read_csv('orders.csv') WHERE amount > 100

    2. Use SQLContext registration when a file source is reused many times:
           ctx.register('orders', pl.scan_csv('orders.csv'))
           ctx.execute('SELECT * FROM orders WHERE amount > 100')

    3. Use native Polars read/scan APIs when you need many parsing options:
           lf = pl.scan_csv(..., schema_overrides=..., try_parse_dates=True)
           ctx.register('orders', lf)

    4. Prefer LazyFrame scan sources for large files when available:
           pl.scan_csv(...)
           pl.scan_parquet(...)
           pl.scan_ipc(...)
           pl.scan_ndjson(...)

    5. If a SQL result scans a temporary file lazily, the file must still exist
       when you call .collect(). Do not delete temporary files before collecting.
    '''


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 7. Quick summary -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Quick map:

CSV:
    SQL:     SELECT * FROM read_csv('path.csv')
    Native:  pl.scan_csv('path.csv')

Parquet:
    SQL:     SELECT * FROM read_parquet('path.parquet')
    Native:  pl.scan_parquet('path.parquet')

NDJSON / JSON Lines:
    SQL:     SELECT * FROM read_json('path.ndjson')
             # current Polars SQL expects NDJSON / JSON Lines here
    Native:  pl.scan_ndjson('path.ndjson')

Standard JSON array:
    Native:  pl.read_json('path.json')
             # then register the resulting DataFrame/LazyFrame in SQLContext

IPC / Arrow / Feather-style files:
    SQL:     SELECT * FROM read_ipc('path.arrow')
    Native:  pl.scan_ipc('path.arrow')

Other sources or advanced reader options:
    Native read/scan first, then register:
        df = pl.read_json('path.json')
        ctx = pl.SQLContext(events=df.lazy())
        ctx.execute('SELECT * FROM events').collect()

Main rule:
    SQL table functions are convenient, but native Polars readers/scanners are
    still the most complete interface for data loading.
'''
