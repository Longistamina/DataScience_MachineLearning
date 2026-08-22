'''
Polars has two concepts that are worth learning early:

1. Expression
   + A lazy description of a column transformation.
   + Examples: pl.col("amount") * 2, pl.col("name").str.to_uppercase(), pl.col("x").mean()
   + Expressions do not compute anything by themselves. They need an execution context.

2. LazyFrame
   + A lazy query plan for a whole table.
   + You build the plan first, then execute it with .collect().
   + It lets Polars optimize the whole query before reading/computing data.

##------------------------------------------------------------------------------------------------##

Important mental model:

Pandas style:
    often immediate execution, step by step

Polars style:
    expression = what to calculate for one or more columns
    context    = where to run the expression
    LazyFrame  = a full query plan that can be optimized before execution

Common execution contexts for expressions:
+ df.select(...)          choose/compute output columns
+ df.with_columns(...)    add or replace columns
+ df.filter(...)          keep rows where a boolean expression is true
+ df.group_by(...).agg(...) aggregate by groups
+ lazy_frame.select(...), lazy_frame.with_columns(...), lazy_frame.filter(...), etc.
'''

from pathlib import Path
import polars as pl

# Create a small self-contained demo dataset.
# This avoids depending on an external data folder.
df_sales = pl.DataFrame(
    {
        "order_id": [1, 2, 3, 4, 5, 6],
        "customer": ["Alice", "Bob", "Alice", "Diana", "Bob", "Evan"],
        "region": ["East", "West", "East", "North", "West", "North"],
        "amount": [120.0, 80.0, 220.0, 150.0, 90.0, 310.0],
        "quantity": [2, 1, 3, 2, 1, 4],
        "date": [
            "2024-01-03",
            "2024-01-05",
            "2024-02-10",
            "2024-02-12",
            "2024-03-01",
            "2024-03-15",
        ],
    }
)

print(df_sales)
# shape: (6, 6)
# ┌──────────┬──────────┬────────┬────────┬──────────┬────────────┐
# │ order_id ┆ customer ┆ region ┆ amount ┆ quantity ┆ date       │
# │ ---      ┆ ---      ┆ ---    ┆ ---    ┆ ---      ┆ ---        │
# │ i64      ┆ str      ┆ str    ┆ f64    ┆ i64      ┆ str        │
# ╞══════════╪══════════╪════════╪════════╪══════════╪════════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0  ┆ 2        ┆ 2024-01-03 │
# │ 2        ┆ Bob      ┆ West   ┆ 80.0   ┆ 1        ┆ 2024-01-05 │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0  ┆ 3        ┆ 2024-02-10 │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0  ┆ 2        ┆ 2024-02-12 │
# │ 5        ┆ Bob      ┆ West   ┆ 90.0   ┆ 1        ┆ 2024-03-01 │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0  ┆ 4        ┆ 2024-03-15 │
# └──────────┴──────────┴────────┴────────┴──────────┴────────────┘
# columns: order_id, customer, region, amount, quantity, date


# =========================================================================================
# 1. What is a Polars LazyFrame?
# =========================================================================================
'''
A LazyFrame is a query plan, not a materialized table.

DataFrame:
    holds actual data now

LazyFrame:
    holds instructions for how to produce data later

When you chain operations on a LazyFrame, Polars records the operations in a logical query plan.
The plan is executed only when you call .collect() or another execution/sink method.
'''

lf_sales = df_sales.lazy()

print(lf_sales)
# naive plan: (run .explain() to see the plan)

print(type(lf_sales))
# <class 'polars.lazyframe.frame.LazyFrame'>


# =========================================================================================
# 2. Build a lazy query with expressions
# =========================================================================================
'''
LazyFrame methods look similar to DataFrame methods, but they return another LazyFrame.
This means you can keep chaining without executing the query yet.
'''

lazy_query = (
    lf_sales
    .filter(pl.col("amount") >= 100)
    .with_columns(
        (pl.col("amount") * pl.col("quantity")).alias("revenue"),
        pl.col("date").str.to_date().alias("date_parsed"),
    )
    .group_by("region")
    .agg(
        pl.len().alias("n_orders"),
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("amount").mean().alias("avg_amount"),
    )
    .sort("total_revenue", descending=True)
)

print(type(lazy_query))
# <class 'polars.lazyframe.frame.LazyFrame'>

'''
At this point, no result DataFrame has been created.
The object is still a LazyFrame query plan.
'''


# =========================================================================================
# 3. Execute the lazy query with .collect()
# =========================================================================================
'''
.collect() tells Polars to optimize and execute the query.
It returns an eager DataFrame.
'''

result = lazy_query.collect()

print(result)
# shape: (2, 4)
# ┌────────┬──────────┬───────────────┬────────────┐
# │ region ┆ n_orders ┆ total_revenue ┆ avg_amount │
# │ ---    ┆ ---      ┆ ---           ┆ ---        │
# │ str    ┆ u32      ┆ f64           ┆ f64        │
# ╞════════╪══════════╪═══════════════╪════════════╡
# │ North  ┆ 2        ┆ 1540.0        ┆ 230.0      │
# │ East   ┆ 2        ┆ 900.0         ┆ 170.0      │
# └────────┴──────────┴───────────────┴────────────┘
# region | n_orders | total_revenue | avg_amount

print(type(result))
# <class 'polars.dataframe.frame.DataFrame'>


# =========================================================================================
# 4. Create LazyFrames from scan_* APIs
# =========================================================================================
'''
The best lazy workflow usually starts with a scan function, not an eager read function.

Eager read:
    pl.read_csv(...)       -> DataFrame now

Lazy scan:
    pl.scan_csv(...)       -> LazyFrame plan now, data read later when collected

Why scan can be better:
+ Polars may read only the columns needed by the query.
+ Polars may push filters down toward the file scan.
+ Polars can optimize the whole query before doing work.
'''

# Make a tiny CSV file so this example is runnable.
data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

scan_query = (
    pl.scan_csv(data_dir/"emp.csv")
    .filter(pl.col("salary") >= 700)
    .select(
        "name",
        "salary",
    )
)

print(type(scan_query))
# <class 'polars.lazyframe.frame.LazyFrame'>

print(scan_query.collect())
# shape: (3, 2)
# ┌──────┬────────┐
# │ name ┆ salary │
# │ ---  ┆ ---    │
# │ str  ┆ f64    │
# ╞══════╪════════╡
# │ Ryan ┆ 729.0  │
# │ Gary ┆ 843.25 │
# │ Guru ┆ 722.5  │
# └──────┴────────┘
# reads the CSV, applies the filter/projection, and returns a DataFrame


# =========================================================================================
# 5. Inspect the query plan with explain()
# =========================================================================================
'''
.explain() prints the query plan.
This is useful for understanding what Polars will do when you collect the query.

When reading from files lazily, the optimized plan can show predicate pushdown and
projection pushdown, meaning filters and column selection can be moved closer to the scan.
'''

print(scan_query.explain())
# Csv SCAN [/home/longdpt/Documents/Academic/DataScience_MachineLearning/data/emp.csv]
# PROJECT 2/5 COLUMNS
# SELECTION: [(col("salary")) >= (700.0)]
# ESTIMATED ROWS: 10

# Example plan details vary by Polars version.
# Look for hints such as CSV SCAN, PROJECT, SELECTION, FILTER, WITH_COLUMNS, AGGREGATE, etc.


# =========================================================================================
# 6. Schema checking before collect
# =========================================================================================
'''
A LazyFrame knows a schema for the planned output.
Use .collect_schema() when you want schema information without materializing all data.
This is often safer than asking for .schema directly in lazy pipelines.
'''

schema = scan_query.collect_schema()

print(schema)
# Schema({'name': String, 'salary': Float64})
# Schema of the query output, e.g. order_id, region, revenue


# =========================================================================================
# 7. LazyFrame anti-pattern: collect too early
# =========================================================================================
'''
Try not to call .collect() in the middle of a lazy workflow unless you really need to.

Less ideal:
    temp = pl.scan_csv(...).filter(...).collect()
    result = temp.lazy().select(...).collect()

Better:
    result = (
        pl.scan_csv(...)
        .filter(...)
        .select(...)
        .collect()
    )

The second pattern gives Polars the whole query at once, which gives the optimizer more room to work.
'''


# =========================================================================================
# 8. LazyFrame sinks and streaming-style output
# =========================================================================================
'''
.collect() materializes a DataFrame in memory.

For larger workflows, LazyFrame also has sink methods that write query output directly to storage.
These are useful when the final result should become a file rather than a Python DataFrame.

Examples are commented out because they write files:
'''

# scan_query.sink_parquet(demo_dir / "sales_result.parquet")
# scan_query.sink_csv(demo_dir / "sales_result.csv")
# scan_query.sink_ndjson(demo_dir / "sales_result.ndjson")


# =========================================================================================
# 9. Categorized API list for LazyFrame
# =========================================================================================
'''
The lists below are a categorized map of the Polars LazyFrame API.
They are included for orientation, not for memorization.

Detailed documentation:
https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html

A. Creating LazyFrames and lazy sources
+ DataFrame.lazy
+ pl.LazyFrame
+ pl.scan_csv
+ pl.scan_parquet
+ pl.scan_ndjson
+ pl.scan_ipc
+ pl.scan_delta
+ pl.scan_iceberg
+ pl.scan_lines
+ pl.scan_pyarrow_dataset

B. LazyFrame aggregation methods
+ LazyFrame.count
+ LazyFrame.max
+ LazyFrame.mean
+ LazyFrame.median
+ LazyFrame.min
+ LazyFrame.null_count
+ LazyFrame.quantile
+ LazyFrame.std
+ LazyFrame.sum
+ LazyFrame.var

C. LazyFrame attributes
+ LazyFrame.columns
+ LazyFrame.dtypes
+ LazyFrame.schema
+ LazyFrame.width

D. LazyFrame descriptive and plan-inspection methods
+ LazyFrame.describe
+ LazyFrame.explain
+ LazyFrame.show_graph
+ LazyFrame.show

E. LazyFrame manipulation and selection methods
+ LazyFrame.__getitem__
+ LazyFrame.approx_n_unique
+ LazyFrame.bottom_k
+ LazyFrame.cast
+ LazyFrame.clear
+ LazyFrame.clone
+ LazyFrame.drop
+ LazyFrame.drop_nans
+ LazyFrame.drop_nulls
+ LazyFrame.explode
+ LazyFrame.fill_nan
+ LazyFrame.fill_null
+ LazyFrame.filter
+ LazyFrame.first
+ LazyFrame.gather
+ LazyFrame.gather_every
+ LazyFrame.group_by
+ LazyFrame.group_by_dynamic
+ LazyFrame.head
+ LazyFrame.inspect
+ LazyFrame.interpolate
+ LazyFrame.join
+ LazyFrame.join_asof
+ LazyFrame.join_where
+ LazyFrame.last
+ LazyFrame.limit
+ LazyFrame.match_to_schema
+ LazyFrame.melt
+ LazyFrame.merge_sorted
+ LazyFrame.pivot
+ LazyFrame.remove
+ LazyFrame.rename
+ LazyFrame.reverse
+ LazyFrame.rolling
+ LazyFrame.select
+ LazyFrame.select_seq
+ LazyFrame.set_sorted
+ LazyFrame.shift
+ LazyFrame.slice
+ LazyFrame.sort
+ LazyFrame.sql
+ LazyFrame.tail
+ LazyFrame.top_k
+ LazyFrame.unique
+ LazyFrame.unnest
+ LazyFrame.unpivot
+ LazyFrame.update
+ LazyFrame.with_columns
+ LazyFrame.with_columns_seq
+ LazyFrame.with_context
+ LazyFrame.with_row_count
+ LazyFrame.with_row_index

F. LazyGroupBy methods returned by LazyFrame.group_by(...)
+ LazyGroupBy.agg
+ LazyGroupBy.all
+ LazyGroupBy.count
+ LazyGroupBy.first
+ LazyGroupBy.having
+ LazyGroupBy.head
+ LazyGroupBy.last
+ LazyGroupBy.len
+ LazyGroupBy.map_groups
+ LazyGroupBy.max
+ LazyGroupBy.mean
+ LazyGroupBy.median
+ LazyGroupBy.min
+ LazyGroupBy.n_unique
+ LazyGroupBy.quantile
+ LazyGroupBy.sum
+ LazyGroupBy.tail

G. LazyFrame execution, collection, debugging, and utility methods
+ LazyFrame.cache
+ LazyFrame.collect
+ LazyFrame.collect_async
+ LazyFrame.collect_schema
+ LazyFrame.collect_batches
+ LazyFrame.execute
+ LazyFrame.lazy
+ LazyFrame.map_batches
+ LazyFrame.pipe
+ LazyFrame.pipe_with_schema
+ LazyFrame.profile
+ LazyFrame.remote
+ LazyFrame.deserialize
+ LazyFrame.serialize
+ QueryOptFlags

H. LazyFrame sink/output methods
+ LazyFrame.sink_batches
+ LazyFrame.sink_csv
+ LazyFrame.sink_delta
+ LazyFrame.sink_ipc
+ LazyFrame.sink_iceberg
+ LazyFrame.sink_ndjson
+ LazyFrame.sink_parquet

I. Async/in-process query helper APIs
+ InProcessQuery.cancel
+ InProcessQuery.fetch
+ InProcessQuery.fetch_blocking

J. Engine and query-result helper APIs
+ GPUEngine
+ QueryResult.head
+ QueryResult.n_rows_total
+ QueryResult.lazy
'''
