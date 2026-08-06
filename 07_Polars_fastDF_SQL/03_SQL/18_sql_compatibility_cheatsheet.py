# FILE VERSION: 18_sql_compatibility_cheatsheet_v1
'''
Polars SQL compatibility cheat sheet: generic SQL vs Polars SQL reality.

Main ideas:
1. Polars SQL is a query interface over Polars DataFrames/LazyFrames, not a
   full database server.
2. SQL queries are translated into Polars expressions and executed by the
   Polars engine.
3. Native Polars expression syntax is still the primary API; some features land
   there before they appear in SQL.
4. Polars SQL follows PostgreSQL-like syntax where possible, but it supports a
   practical subset rather than every SQL feature.
5. This file is a final reference file, not a deep tutorial for every command.

Practical rule:
    Use SQL when it makes the query easier to read or when you already have SQL.
    Use native Polars when you need the most complete/latest Polars feature set.

Important version note:
+ SQL support changes across Polars versions.
+ Treat this file as a study/reference checklist.
+ When a syntax fails in your installed Polars version, use the native Polars
  equivalent or one of the workaround patterns shown below.
'''

import datetime as dt

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(30)
pl.Config.set_tbl_cols(8)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(120)


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 0. Setup data ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The examples are self-contained so this file can run without external datasets.

The small order table is reused to show:
+ SQL queries through LazyFrame.sql(...)
+ SQLContext queries over multiple named tables
+ native Polars equivalents
+ pandas-style mental mappings
'''

df_orders = pl.DataFrame(
    {
        "order_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
        "customer_id": [1, 2, 1, 3, 2, 4, 1, 3],
        "customer": ["Alice", "Bob", "Alice", "Diana", "Bob", "Evan", "Alice", "Diana"],
        "region": ["East", "West", "East", "North", "West", "North", "East", "North"],
        "product": ["Keyboard", "Mouse", "Monitor", "Keyboard", "Mouse", "Monitor", "Mouse", "Desk"],
        "quantity": [2, 1, 1, 3, 4, 2, 5, 1],
        "unit_price": [120.0, 35.0, 250.0, 120.0, 35.0, 250.0, 35.0, 400.0],
        "discount_rate": [0.10, 0.00, 0.15, 0.05, 0.00, 0.20, 0.05, 0.10],
        "status": ["paid", "pending", "paid", "paid", "paid", "paid", "cancelled", "paid"],
        "priority": [True, False, True, False, False, True, False, True],
        "promo_code": ["VIP", None, "SPRING", None, "VIP", "SPRING", "VIP", None],
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
    .with_columns((c("quantity") * c("unit_price")).alias("gross_amount"))
    .with_columns((c("gross_amount") * c("discount_rate")).alias("discount_amount"))
    .with_columns((c("gross_amount") - c("discount_amount")).alias("net_amount"))
)

lf_orders = df_orders.lazy()

df_customers = pl.DataFrame(
    {
        "customer_id": [1, 2, 3, 4, 5],
        "customer_name": ["Alice", "Bob", "Diana", "Evan", "Fiona"],
        "segment": ["Consumer", "Business", "Consumer", "Enterprise", "Business"],
    }
)

lf_customers = df_customers.lazy()

ctx = pl.SQLContext(orders=lf_orders, customers=lf_customers)

print(df_orders)
print(df_orders.schema)


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. Compatibility overview --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
This table is the high-level cheat sheet.

Status meanings:
+ Yes: normal Polars SQL topic.
+ Partial/version-dependent: useful, but test with your installed version.
+ Prefer native Polars: possible in Polars, but native expressions are usually clearer or more complete.
+ No: not the right mental model for Polars SQL.
'''

compatibility_overview = pl.DataFrame(
    {
        "Generic SQL idea": [
            "SELECT query",
            "WHERE filtering",
            "ORDER BY / LIMIT / OFFSET / FETCH",
            "GROUP BY / HAVING",
            "JOIN",
            "UNION / INTERSECT / EXCEPT",
            "WITH CTE",
            "Window functions / QUALIFY",
            "CREATE TABLE AS SELECT",
            "SHOW TABLES / DROP TABLE / TRUNCATE",
            "EXPLAIN",
            "UNNEST",
            "INSERT",
            "UPDATE",
            "DELETE",
            "Indexes / primary keys / constraints",
            "Transactions / COMMIT / ROLLBACK",
            "Stored procedures / triggers",
        ],
        "Polars SQL reality": [
            "Yes",
            "Yes",
            "Yes",
            "Yes",
            "Yes, but JOIN ... ON is safest for equi-joins",
            "Yes, including BY NAME variants in recent versions",
            "Yes",
            "Yes, but some window-frame/order limitations exist",
            "Yes through SQLContext",
            "Partial/version-dependent for table mutation commands",
            "Yes",
            "Yes",
            "No",
            "No",
            "Version-dependent; prefer native/filter patterns if needed",
            "No",
            "No",
            "No",
        ],
        "Typical native Polars equivalent": [
            "lf.select(...) / lf.with_columns(...) / lf.collect()",
            "lf.filter(...)",
            "lf.sort(...).limit(...) / lf.slice(...) / lf.head(...)",
            "lf.group_by(...).agg(...).filter(...)",
            "lf.join(...)",
            "pl.concat(...) / joins / filters",
            "Break pipeline into named LazyFrame variables",
            "expressions with .over(...), rank(...), cum_sum(), etc.",
            "Assign result to a LazyFrame variable or register it in SQLContext",
            "ctx.register(...) / ctx.unregister(...) / native replacement frame",
            "lf.explain()",
            "list/array expressions, explode/unnest patterns",
            "pl.concat([old_lf, new_lf]) or write to external storage",
            "with_columns(...) / when-then-otherwise / joins",
            "filter(...) to keep rows or remove rows",
            "Not applicable; Polars is not a database server",
            "Not applicable; Polars works with immutable-style DataFrame results",
            "Not applicable",
        ],
    }
)

print(compatibility_overview)


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 2. Generic SQL vs Polars SQL mindset -------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Generic SQL often assumes a database server with persistent tables.
Polars SQL assumes DataFrames/LazyFrames registered as queryable tables.

Generic database mental model:
    Connect to server -> query persistent tables -> maybe mutate data in-place.

Polars SQL mental model:
    Create/register DataFrames or LazyFrames -> build lazy SQL query -> collect result.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        region,
        COUNT(*) AS n_orders,
        SUM(net_amount) AS net_sales
    FROM self
    WHERE status = 'paid'
    GROUP BY region
    ORDER BY net_sales DESC
    """
)
print(out_sql.collect())

# Native Polars equivalent.
out_native = (
    lf_orders
    .filter(c("status") == "paid")
    .group_by("region")
    .agg(
        pl.len().alias("n_orders"),
        c("net_amount").sum().alias("net_sales"),
    )
    .sort("net_sales", descending=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. Query clauses cheat sheet -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
This table maps common SELECT-query clauses to native Polars.

The point is not to memorize every syntax form.
The point is to know which native Polars pattern corresponds to each SQL idea.
'''

query_clause_map = pl.DataFrame(
    {
        "SQL clause": [
            "SELECT columns",
            "SELECT expression AS alias",
            "FROM table",
            "WHERE condition",
            "GROUP BY keys",
            "HAVING aggregate_condition",
            "ORDER BY col DESC NULLS LAST",
            "LIMIT n",
            "OFFSET n",
            "FETCH FIRST n ROWS ONLY",
            "DISTINCT",
            "JOIN ... ON left.key = right.key",
            "WITH cte AS (...) SELECT ...",
            "QUALIFY window_condition",
        ],
        "Native Polars pattern": [
            ".select('col1', 'col2')",
            ".select((expr).alias('alias')) or .with_columns(...)",
            "LazyFrame variable or SQLContext registered name",
            ".filter(condition)",
            ".group_by(keys).agg(...)",
            ".group_by(...).agg(...).filter(aggregate_condition)",
            ".sort('col', descending=True, nulls_last=True)",
            ".limit(n) or .head(n)",
            ".slice(offset, length)",
            ".limit(n)",
            ".unique(...) or expression n_unique()/unique()",
            ".join(other, on=..., how=...)",
            "Use named LazyFrame variables or .pipe(...) functions",
            "Compute window expression, then .filter(...)",
        ],
    }
)

print(query_clause_map)


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 4. Function categories cheat sheet -----------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Polars SQL supports many function families, but the exact function list grows over time.
For serious work, check the function category docs that match your Polars version.

When a SQL function is missing, there is often a native Polars expression method
that can do the same job.
'''

function_category_map = pl.DataFrame(
    {
        "Function category": [
            "Aggregate",
            "Conditional",
            "String",
            "Math / numeric",
            "Temporal",
            "Array/list",
            "Window/ranking",
            "Type conversion",
        ],
        "Typical SQL examples": [
            "COUNT, SUM, AVG, MIN, MAX, MEDIAN, STDDEV, VARIANCE",
            "CASE WHEN, COALESCE, NULLIF, GREATEST, LEAST",
            "LOWER, UPPER, TRIM, SUBSTR, REGEXP_REPLACE, CONCAT",
            "ABS, ROUND, FLOOR, CEIL, POWER, LOG, MOD",
            "EXTRACT, DATE_PART, STRPTIME/DATE parsing functions by version",
            "ARRAY functions, UNNEST by version",
            "ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD",
            "CAST, TRY_CAST, expr::type",
        ],
        "Native Polars examples": [
            "c('x').sum(), c('x').mean(), pl.len()",
            "pl.when(...).then(...).otherwise(...), coalesce",
            "c('s').str.to_lowercase(), .str.replace_all(...)",
            "c('x').round(), abs, log, pow expressions",
            "c('date').dt.year(), .str.strptime(...)",
            "list namespace, explode, arr namespace",
            "rank().over(...), shift().over(...), cum_sum().over(...)",
            "cast(...), strict=False for try-like conversion",
        ],
    }
)

print(function_category_map)


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------- 5. Pandas / SQL / native Polars mappings ----------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
This is a compact translation table for learners coming from pandas or SQL.
'''

pandas_sql_polars_map = pl.DataFrame(
    {
        "Task": [
            "Select columns",
            "Filter rows",
            "Create/modify column",
            "Sort rows",
            "Take first n rows",
            "Drop duplicate rows",
            "Group summary",
            "Filter grouped summaries",
            "Join tables",
            "Stack rows",
            "Window rank per group",
            "Running total per group",
            "Null test",
            "Fill null",
        ],
        "pandas style": [
            "df[['a', 'b']]",
            "df[df['x'] > 0]",
            "df['y'] = ...",
            "df.sort_values('x')",
            "df.head(n)",
            "df.drop_duplicates()",
            "df.groupby('g').agg(...)",
            "groupby result then filter",
            "pd.merge(left, right, on='key')",
            "pd.concat([df1, df2])",
            "df.groupby('g')['x'].rank()",
            "df.groupby('g')['x'].cumsum()",
            "df['x'].isna()",
            "df['x'].fillna(value)",
        ],
        "SQL style": [
            "SELECT a, b FROM t",
            "WHERE x > 0",
            "SELECT ..., expression AS y FROM t",
            "ORDER BY x",
            "LIMIT n",
            "SELECT DISTINCT ...",
            "GROUP BY g",
            "HAVING aggregate_condition",
            "JOIN ... ON ...",
            "UNION ALL",
            "RANK() OVER (PARTITION BY g ORDER BY x)",
            "SUM(x) OVER (PARTITION BY g ORDER BY time)",
            "x IS NULL",
            "COALESCE(x, value)",
        ],
        "Native Polars style": [
            "lf.select('a', 'b')",
            "lf.filter(c('x') > 0)",
            "lf.with_columns((...).alias('y'))",
            "lf.sort('x')",
            "lf.head(n) / lf.limit(n)",
            "lf.unique()",
            "lf.group_by('g').agg(...) ",
            "lf.group_by(...).agg(...).filter(...) ",
            "left.join(right, on='key')",
            "pl.concat([lf1, lf2])",
            "c('x').rank().over('g')",
            "c('x').cum_sum().over('g')",
            "c('x').is_null()",
            "c('x').fill_null(value)",
        ],
    }
)

print(pandas_sql_polars_map)


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------- 6. Runnable SQL and native equivalent -------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A compact example combining common SQL features:
+ WHERE
+ GROUP BY
+ HAVING
+ ORDER BY
+ LIMIT
'''

out_sql = lf_orders.sql(
    """
    SELECT
        product,
        COUNT(*) AS n_orders,
        SUM(quantity) AS units_sold,
        SUM(net_amount) AS net_sales
    FROM self
    WHERE status = 'paid'
    GROUP BY product
    HAVING SUM(net_amount) >= 100
    ORDER BY net_sales DESC
    LIMIT 3
    """
)
print(out_sql.collect())

out_native = (
    lf_orders
    .filter(c("status") == "paid")
    .group_by("product")
    .agg(
        pl.len().alias("n_orders"),
        c("quantity").sum().alias("units_sold"),
        c("net_amount").sum().alias("net_sales"),
    )
    .filter(c("net_sales") >= 100)
    .sort("net_sales", descending=True)
    .limit(3)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 7. Runnable multi-table SQL example --------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
A SQLContext lets you register multiple named tables.
This is the clearest style for joins.
'''

out_sql = ctx.execute(
    """
    SELECT
        c.customer_name,
        c.segment,
        COUNT(*) AS n_paid_orders,
        SUM(o.net_amount) AS net_sales
    FROM orders AS o
    INNER JOIN customers AS c
        ON o.customer_id = c.customer_id
    WHERE o.status = 'paid'
    GROUP BY c.customer_name, c.segment
    ORDER BY net_sales DESC
    """
)
print(out_sql.collect())

# Native Polars equivalent.
out_native = (
    lf_orders
    .join(lf_customers, on="customer_id", how="inner")
    .filter(c("status") == "paid")
    .group_by("customer_name", "segment")
    .agg(
        pl.len().alias("n_paid_orders"),
        c("net_amount").sum().alias("net_sales"),
    )
    .sort("net_sales", descending=True)
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------- 8. Generic SQL commands to be careful with --------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Many generic SQL cheat sheets focus on database commands. Some of those are not
central to Polars because Polars is not a database server.

Do NOT blindly copy generic SQL cheatsheet commands into Polars SQL.
'''

generic_command_reality = pl.DataFrame(
    {
        "Generic SQL command": [
            "CREATE DATABASE db",
            "USE db",
            "CREATE TABLE t (...) schema DDL",
            "CREATE TABLE new AS SELECT ...",
            "INSERT INTO t VALUES (...) ",
            "UPDATE t SET ... WHERE ...",
            "DELETE FROM t WHERE ...",
            "ALTER TABLE t ADD COLUMN ...",
            "CREATE INDEX ...",
            "PRIMARY KEY / FOREIGN KEY",
            "COMMIT / ROLLBACK",
            "ANALYZE / VACUUM",
            "GRANT / REVOKE",
        ],
        "Polars SQL reality": [
            "No database catalog concept",
            "No active database concept",
            "Version-dependent; often not needed for DataFrame workflows",
            "Useful through SQLContext",
            "Not supported as normal database DML",
            "Not supported as normal database DML",
            "Version-dependent in docs; prefer native filter/remove pattern",
            "Use native with_columns/select to create a new frame",
            "No row index/database index concept",
            "No database constraints concept",
            "No transactions concept",
            "No database maintenance/meta-query concept",
            "No database permissions concept",
        ],
        "Polars-style replacement": [
            "Use Python variables, folders, files, or external databases",
            "Reference registered SQLContext table names",
            "Create pl.DataFrame / pl.LazyFrame with schema if needed",
            "ctx.execute('CREATE TABLE ... AS SELECT ...')",
            "pl.concat([existing, new_rows])",
            "with_columns(...) to return a modified DataFrame/LazyFrame",
            "filter(...) to keep rows or remove matching rows",
            "with_columns(...) / select(...)",
            "Sort/filter/group on normal columns; no special index",
            "Validate in application code or external database",
            "Save output only when you choose to write it",
            "Use explain/profile/optimization tools instead",
            "Handle access control outside Polars",
        ],
    }
)

print(generic_command_reality)


#--------------------------------------------------------------------------------------------------------------#
#------------------------------ 9. Known Polars SQL workarounds from practice --------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
These are practical gotchas discovered while writing the tutorial files.

They are intentionally written as pattern replacements rather than full runnable
examples, because exact support can vary across Polars versions.
'''

workarounds = pl.DataFrame(
    {
        "Problem pattern": [
            "SQL read_json(...) on standard JSON array beginning with '['",
            "Range join inside JOIN ... ON, e.g. x >= low AND x < high",
            "Mixed ASC/DESC inside OVER(... ORDER BY ...)",
            "ROWS BETWEEN 1 PRECEDING AND CURRENT ROW",
            "Window PARTITION BY column not selected, then QUALIFY/window resolution fails",
            "Chained CTEs with SELECT * and repeated join key names",
            "Generic SQL expects row index / primary key behavior",
        ],
        "Why it can fail": [
            "Polars SQL table function may expect NDJSON/JSON Lines in your version",
            "Polars SQL JOIN ... ON is safest for equi-join constraints",
            "Some versions do not support mixed directions in window ORDER BY",
            "Some versions only support UNBOUNDED PRECEDING to CURRENT ROW frame",
            "Optimizer/projection may remove the partition column before window resolution",
            "Name resolver can become ambiguous across CTE lineage and joined tables",
            "Polars has no special pandas/database-style row index",
        ],
        "Safer workaround": [
            "Use write_ndjson/read_json, or pl.read_json(...).lazy() then register",
            "Use CROSS JOIN + WHERE for small lookup tables, or native Polars non-equi/range pattern",
            "Use ascending expression like ORDER BY (0 - amount), id",
            "Use LAG/LEAD or native Polars rolling/window expressions",
            "Include needed partition key in inner query, then drop it in an outer SELECT",
            "Avoid SELECT *; select/rename needed keys early",
            "Keep id/index-like values as normal columns",
        ],
    }
)

print(workarounds)


#--------------------------------------------------------------------------------------------------------------#
#------------------------------ 10. SQL snippets that are reference-only here ---------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The snippets below are intentionally NOT executed.
They are here as a final cheat sheet.
'''

SUPPORTED_QUERY_SNIPPETS = {
    "basic_select": """
        SELECT col1, col2, expression AS new_col
        FROM table_name
        WHERE condition
        ORDER BY col1
        LIMIT 10
    """,
    "grouped_summary": """
        SELECT key, COUNT(*) AS n, SUM(value) AS total
        FROM table_name
        WHERE row_condition
        GROUP BY key
        HAVING SUM(value) > 100
        ORDER BY total DESC
    """,
    "join": """
        SELECT l.*, r.extra_col
        FROM left_table AS l
        INNER JOIN right_table AS r
            ON l.key = r.key
    """,
    "cte": """
        WITH filtered AS (
            SELECT *
            FROM table_name
            WHERE condition
        )
        SELECT key, COUNT(*) AS n
        FROM filtered
        GROUP BY key
    """,
    "window_qualify": """
        SELECT *
        FROM table_name
        QUALIFY ROW_NUMBER() OVER (
            PARTITION BY group_key
            ORDER BY value DESC
        ) = 1
    """,
    "set_operation": """
        SELECT a, b FROM table_one
        UNION ALL
        SELECT a, b FROM table_two
    """,
    "explain": """
        EXPLAIN SELECT * FROM table_name WHERE value > 0
    """,
}

for name, snippet in SUPPORTED_QUERY_SNIPPETS.items():
    print(f"\n--- {name} ---")
    print(snippet.strip())

UNSUPPORTED_OR_NOT_DATABASE_SNIPPETS = {
    "insert": "INSERT INTO table_name VALUES (...)  -- not the normal Polars SQL workflow",
    "update": "UPDATE table_name SET x = 1 WHERE id = 10  -- use native with_columns/filter/join patterns",
    "create_index": "CREATE INDEX idx ON table_name(col)  -- not applicable to Polars DataFrames",
    "transaction": "BEGIN; ... COMMIT;  -- not applicable to in-memory Polars query plans",
}

for name, snippet in UNSUPPORTED_OR_NOT_DATABASE_SNIPPETS.items():
    print(f"\n--- be careful: {name} ---")
    print(snippet)


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 11. Final checklist -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Final checklist before writing a Polars SQL query:

1. Are your DataFrames/LazyFrames registered with the table names used in SQL?
2. Are messy column names quoted correctly with double quotes?
3. Are string values quoted with single quotes?
4. Are you using WHERE for row filters and HAVING/QUALIFY for post-aggregation/window filters?
5. Are join keys unambiguous and qualified when multiple tables have the same column name?
6. Are you using ORDER BY when deterministic row order matters?
7. Are you relying on a feature that may be version-dependent?
8. Would the native Polars expression API be clearer or more powerful for this task?
9. Did you remember that SQL returns a LazyFrame unless eager execution is requested?
10. Did you call .collect() only when you actually need the materialized result?
'''

# ┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
# │ Generic SQL idea                ┆ Polars SQL reality              ┆ Typical native Polars equivale… │
# ╞═════════════════════════════════╪═════════════════════════════════╪═════════════════════════════════╡
# │ SELECT query                    ┆ Yes                             ┆ lf.select(...) / lf.with_colum… │
# │ WHERE filtering                 ┆ Yes                             ┆ lf.filter(...)                  │
# │ ORDER BY / LIMIT / OFFSET / FE… ┆ Yes                             ┆ lf.sort(...).limit(...) / lf.s… │
# │ GROUP BY / HAVING               ┆ Yes                             ┆ lf.group_by(...).agg(...).filt… │
# │ JOIN                            ┆ Yes, but JOIN ... ON is safest… ┆ lf.join(...)                    │
# │ UNION / INTERSECT / EXCEPT      ┆ Yes, including BY NAME variant… ┆ pl.concat(...) / joins / filte… │
# │ WITH CTE                        ┆ Yes                             ┆ Break pipeline into named Lazy… │
# │ Window functions / QUALIFY      ┆ Yes, but some window-frame/ord… ┆ expressions with .over(...), r… │
# │ CREATE TABLE AS SELECT          ┆ Yes through SQLContext          ┆ Assign result to a LazyFrame v… │
# │ SHOW TABLES / DROP TABLE / TRU… ┆ Partial/version-dependent for … ┆ ctx.register(...) / ctx.unregi… │
# │ EXPLAIN                         ┆ Yes                             ┆ lf.explain()                    │
# │ UNNEST                          ┆ Yes                             ┆ list/array expressions, explod… │
# │ INSERT                          ┆ No                              ┆ pl.concat([old_lf, new_lf]) or… │
# │ UPDATE                          ┆ No                              ┆ with_columns(...) / when-then-… │
# │ DELETE                          ┆ Version-dependent; prefer nati… ┆ filter(...) to keep rows or re… │
# │ Indexes / primary keys / const… ┆ No                              ┆ Not applicable; Polars is not … │
# │ Transactions / COMMIT / ROLLBA… ┆ No                              ┆ Not applicable; Polars works w… │
# │ Stored procedures / triggers    ┆ No                              ┆ Not applicable                  │
# └─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘

# ┌─────────────────────────────────┬─────────────────────────────────┐
# │ SQL clause                      ┆ Native Polars pattern           │                      │
# ╞═════════════════════════════════╪═════════════════════════════════╡
# │ SELECT columns                  ┆ .select('col1', 'col2')         │
# │ SELECT expression AS alias      ┆ .select((expr).alias('alias'))… │
# │ FROM table                      ┆ LazyFrame variable or SQLConte… │
# │ WHERE condition                 ┆ .filter(condition)              │
# │ GROUP BY keys                   ┆ .group_by(keys).agg(...)        │
# │ HAVING aggregate_condition      ┆ .group_by(...).agg(...).filter… │
# │ ORDER BY col DESC NULLS LAST    ┆ .sort('col', descending=True, … │
# │ LIMIT n                         ┆ .limit(n) or .head(n)           │
# │ OFFSET n                        ┆ .slice(offset, length)          │
# │ FETCH FIRST n ROWS ONLY         ┆ .limit(n)                       │
# │ DISTINCT                        ┆ .unique(...) or expression n_u… │
# │ JOIN ... ON left.key = right.k… ┆ .join(other, on=..., how=...)   │
# │ WITH cte AS (...) SELECT ...    ┆ Use named LazyFrame variables … │
# │ QUALIFY window_condition        ┆ Compute window expression, the… │
# └─────────────────────────────────┴─────────────────────────────────┘

# ┌───────────────────┬─────────────────────────────────┬─────────────────────────────────┐
# │ Function category ┆ Typical SQL examples            ┆ Native Polars examples          │
# ╞═══════════════════╪═════════════════════════════════╪═════════════════════════════════╡
# │ Aggregate         ┆ COUNT, SUM, AVG, MIN, MAX, MED… ┆ c('x').sum(), c('x').mean(), p… │
# │ Conditional       ┆ CASE WHEN, COALESCE, NULLIF, G… ┆ pl.when(...).then(...).otherwi… │
# │ String            ┆ LOWER, UPPER, TRIM, SUBSTR, RE… ┆ c('s').str.to_lowercase(), .st… │
# │ Math / numeric    ┆ ABS, ROUND, FLOOR, CEIL, POWER… ┆ c('x').round(), abs, log, pow … │
# │ Temporal          ┆ EXTRACT, DATE_PART, STRPTIME/D… ┆ c('date').dt.year(), .str.strp… │
# │ Array/list        ┆ ARRAY functions, UNNEST by ver… ┆ list namespace, explode, arr n… │
# │ Window/ranking    ┆ ROW_NUMBER, RANK, DENSE_RANK, … ┆ rank().over(...), shift().over… │
# │ Type conversion   ┆ CAST, TRY_CAST, expr::type      ┆ cast(...), strict=False for tr… │
# └───────────────────┴─────────────────────────────────┴─────────────────────────────────┘

# ┌──────────────────────────┬──────────────────────────────┬──────────────────────────────┬─────────────────────────────┐
# │ Task                     ┆ pandas style                 ┆ SQL style                    ┆ Native Polars style         │
# ╞══════════════════════════╪══════════════════════════════╪══════════════════════════════╪═════════════════════════════╡
# │ Select columns           ┆ df[['a', 'b']]               ┆ SELECT a, b FROM t           ┆ lf.select('a', 'b')         │
# │ Filter rows              ┆ df[df['x'] > 0]              ┆ WHERE x > 0                  ┆ lf.filter(c('x') > 0)       │
# │ Create/modify column     ┆ df['y'] = ...                ┆ SELECT ..., expression AS y  ┆ lf.with_columns((...).alias │
# │                          ┆                              ┆ FR…                          ┆ ('y…                        │
# │ Sort rows                ┆ df.sort_values('x')          ┆ ORDER BY x                   ┆ lf.sort('x')                │
# │ Take first n rows        ┆ df.head(n)                   ┆ LIMIT n                      ┆ lf.head(n) / lf.limit(n)    │
# │ Drop duplicate rows      ┆ df.drop_duplicates()         ┆ SELECT DISTINCT ...          ┆ lf.unique()                 │
# │ Group summary            ┆ df.groupby('g').agg(...)     ┆ GROUP BY g                   ┆ lf.group_by('g').agg(...)   │
# │ Filter grouped summaries ┆ groupby result then filter   ┆ HAVING aggregate_condition   ┆ lf.group_by(...).agg(...).f │
# │                          ┆                              ┆                              ┆ ilt…                        │
# │ Join tables              ┆ pd.merge(left, right,        ┆ JOIN ... ON ...              ┆ left.join(right, on='key')  │
# │                          ┆ on='key'…                    ┆                              ┆                             │
# │ Stack rows               ┆ pd.concat([df1, df2])        ┆ UNION ALL                    ┆ pl.concat([lf1, lf2])       │
# │ Window rank per group    ┆ df.groupby('g')['x'].rank()  ┆ RANK() OVER (PARTITION BY g  ┆ c('x').rank().over('g')     │
# │                          ┆                              ┆ OR…                          ┆                             │
# │ Running total per group  ┆ df.groupby('g')['x'].cumsum( ┆ SUM(x) OVER (PARTITION BY g  ┆ c('x').cum_sum().over('g')  │
# │                          ┆ )                            ┆ OR…                          ┆                             │
# │ Null test                ┆ df['x'].isna()               ┆ x IS NULL                    ┆ c('x').is_null()            │
# │ Fill null                ┆ df['x'].fillna(value)        ┆ COALESCE(x, value)           ┆ c('x').fill_null(value)     │
# └──────────────────────────┴──────────────────────────────┴──────────────────────────────┴─────────────────────────────┘

# ┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
# │ Problem pattern                 ┆ Why it can fail                 ┆ Safer workaround                │
# │ ---                             ┆ ---                             ┆ ---                             │
# │ str                             ┆ str                             ┆ str                             │
# ╞═════════════════════════════════╪═════════════════════════════════╪═════════════════════════════════╡
# │ SQL read_json(...) on standard… ┆ Polars SQL table function may … ┆ Use write_ndjson/read_json, or… │
# │ Range join inside JOIN ... ON,… ┆ Polars SQL JOIN ... ON is safe… ┆ Use CROSS JOIN + WHERE for sma… │
# │ Mixed ASC/DESC inside OVER(...… ┆ Some versions do not support m… ┆ Use ascending expression like … │
# │ ROWS BETWEEN 1 PRECEDING AND C… ┆ Some versions only support UNB… ┆ Use LAG/LEAD or native Polars … │
# │ Window PARTITION BY column not… ┆ Optimizer/projection may remov… ┆ Include needed partition key i… │
# │ Chained CTEs with SELECT * and… ┆ Name resolver can become ambig… ┆ Avoid SELECT *; select/rename … │
# │ Generic SQL expects row index … ┆ Polars has no special pandas/d… ┆ Keep id/index-like values as n… │
# └─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘

# --- basic_select ---
# SELECT col1, col2, expression AS new_col
#         FROM table_name
#         WHERE condition
#         ORDER BY col1
#         LIMIT 10

# --- grouped_summary ---
# SELECT key, COUNT(*) AS n, SUM(value) AS total
#         FROM table_name
#         WHERE row_condition
#         GROUP BY key
#         HAVING SUM(value) > 100
#         ORDER BY total DESC

# --- join ---
# SELECT l.*, r.extra_col
#         FROM left_table AS l
#         INNER JOIN right_table AS r
#             ON l.key = r.key

# --- cte ---
# WITH filtered AS (
#             SELECT *
#             FROM table_name
#             WHERE condition
#         )
#         SELECT key, COUNT(*) AS n
#         FROM filtered
#         GROUP BY key

# --- window_qualify ---
# SELECT *
#         FROM table_name
#         QUALIFY ROW_NUMBER() OVER (
#             PARTITION BY group_key
#             ORDER BY value DESC
#         ) = 1

# --- set_operation ---
# SELECT a, b FROM table_one
#         UNION ALL
#         SELECT a, b FROM table_two

# --- explain ---
# EXPLAIN SELECT * FROM table_name WHERE value > 0

# --- be careful: insert ---
# INSERT INTO table_name VALUES (...)  -- not the normal Polars SQL workflow

# --- be careful: update ---
# UPDATE table_name SET x = 1 WHERE id = 10  -- use native with_columns/filter/join patterns

# --- be careful: create_index ---
# CREATE INDEX idx ON table_name(col)  -- not applicable to Polars DataFrames

# --- be careful: transaction ---
# BEGIN; ... COMMIT;  -- not applicable to in-memory Polars query plans
