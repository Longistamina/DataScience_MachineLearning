'''
Polars quick DataFrame preview, schema inspection, and memory inspection.

This file is adapted from the pandas workflow:
    df.head()
    df.tail()
    df.info(memory_usage="deep")
    df.memory_usage(deep=True)

In Polars, there is no direct df.info() or df.memory_usage(deep=True) method.
Instead, use a combination of:

1. df.head(n=5): Return the first n rows of the DataFrame.
2. df.tail(n=5): Return the last n rows of the DataFrame.
3. Info-like inspection:
   + df.glimpse(): Dense one-line-per-column preview.
   + df.shape / df.height / df.width: Row and column counts.
   + df.columns / df.dtypes / df.schema: Column names and data types.
   + df.null_count(): Null count per column.
   + df.count(): Non-null count per column.
   + df.describe(): Summary statistics.
4. Memory and performance inspection:
   + df.estimated_size(unit="b"/"kb"/"mb"/...): Estimated heap size.
   + Per-column memory approximation: loop over columns and estimate each selected column.
   + df.n_chunks(strategy="all"): Check chunk counts for all columns.
   + df.rechunk(): Combine chunks for better contiguous memory layout.
   + df.shrink_to_fit(): Shrink capacity to fit the exact data size.
5. LazyFrame inspection:
   + lf.collect_schema(): Inspect schema without collecting the full data.
   + lf.collect_schema().names(): Retrieve the list of LazyFrame column names
   + lf.head(n).collect() / lf.tail(n).collect(): Preview lazy data.
   + lf.explain(): Inspect the lazy query plan.
'''

import polars as pl
from pathlib import Path


data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

# Same dataset used in the pandas version of this guide.
df_medals = pl.read_csv(
    data_dir/"medals.csv",
    skip_rows=4,
)


#-------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 1. df.head() ---------------------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''df.head(n=5): Return the first n rows of the DataFrame. Default n is 5.'''

print(df_medals.head())
# shape: (5, 8)
# First five rows of the medals DataFrame.
# Notice that Polars output has no custom row index column.

print(df_medals.head(3))
# shape: (3, 8)
# First three rows.

####################################
## Negative n in Polars df.head() ##
####################################
'''
In Polars, df.head(-k) means:
    return all rows except the last k rows.

This is different from just asking for a small preview, so use it carefully on large frames.
The small example below makes the behavior easy to see.
'''

df_small = pl.DataFrame(
    {
        "id": [1, 2, 3, 4, 5],
        "letter": ["a", "b", "c", "d", "e"],
    }
)
print(df_small.head(-2))
# shape: (3, 2)
# ┌─────┬────────┐
# │ id  ┆ letter │
# │ --- ┆ ---    │
# │ i64 ┆ str    │
# ╞═════╪════════╡
# │ 1   ┆ a      │
# │ 2   ┆ b      │
# │ 3   ┆ c      │
# └─────┴────────┘
# The last 2 rows were excluded.


#-------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2. df.tail() ---------------------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''df.tail(n=5): Return the last n rows of the DataFrame. Default n is 5.'''

print(df_medals.tail())
# shape: (5, 8)
# Last five rows of the medals DataFrame.

print(df_medals.tail(3))
# shape: (3, 8)
# Last three rows.

####################################
## Negative n in Polars df.tail() ##
####################################
'''
In Polars, df.tail(-k) means:
    return all rows except the first k rows.
'''

print(df_small.tail(-2))
# shape: (3, 2)
# ┌─────┬────────┐
# │ id  ┆ letter │
# │ --- ┆ ---    │
# │ i64 ┆ str    │
# ╞═════╪════════╡
# │ 3   ┆ c      │
# │ 4   ┆ d      │
# │ 5   ┆ e      │
# └─────┴────────┘
# The first 2 rows were excluded.


#-------------------------------------------------------------------------------------------------------#
#----------------------------- 3. Info-like inspection: shape, schema, glimpse -------------------------#
#-------------------------------------------------------------------------------------------------------#
'''
Pandas has df.info(), which prints a compact summary with:
    + row count / index information
    + column names
    + non-null counts
    + dtypes
    + memory usage

Polars does not have a single direct df.info() method.
The Polars approach is to combine several smaller inspection tools.
'''

###############################
## df.shape / height / width ##
###############################

print(df_medals.shape)
# (2311, 8)
# Tuple of (number_of_rows, number_of_columns)

print(df_medals.height)
# 2311
# Number of rows only.

print(df_medals.width)
# 8
# Number of columns only.

############################
## df.columns / df.dtypes ##
############################

print(df_medals.columns)
# ['Year', 'City', 'Sport', 'Discipline', 'NOC', 'Event', 'Event gender', 'Medal']

print(df_medals.dtypes)
# [Int64, String, String, String, String, String, String, String]
# The exact integer width may depend on your file and inference settings.

###############
## df.schema ##
###############
'''
A Polars schema maps column names to Polars data types.
This is one of the closest replacements for part of pandas df.info().
'''

print(df_medals.schema)
# Schema({
#     'Year': Int64,
#     'City': String,
#     'Sport': String,
#     'Discipline': String,
#     'NOC': String,
#     'Event': String,
#     'Event gender': String,
#     'Medal': String,
# })

#########################
## df.collect_schema() ##
#########################
'''
DataFrame.collect_schema() returns an ordered schema object.
This mirrors LazyFrame.collect_schema(), which is especially useful in lazy workflows.
'''

schema = df_medals.collect_schema()

print(schema)
# Schema({'Year': Int64, 'City': String, ...})

print(schema.names())
# ['Year', 'City', 'Sport', 'Discipline', 'NOC', 'Event', 'Event gender', 'Medal']

print(schema.dtypes())
# [Int64, String, String, String, String, String, String, String]

print(schema.len())
# 8

#################################
## df.collect_schema().names() ##
#################################
'''Retrieve the list of DataFrame column names'''

print(df_medals.collect_schema().names())
# ['Year', 'City', 'Sport', 'Discipline', 'NOC', 'Event', 'Event gender', 'Medal']

##################
## df.glimpse() ##
##################
'''
df.glimpse() is a very useful Polars replacement for the quick-read part of df.info().
It prints one line per column, including:
    + total row count
    + total column count
    + each column name
    + each dtype
    + the first few values in each column

This is especially helpful for wide DataFrames, because each column gets its own line.
'''

# Print to stdout and return None.
df_medals.glimpse()
# Rows: 2311
# Columns: 8
# $ Year           <i64> 1924, 1924, 1924, ...
# $ City           <str> 'Chamonix', 'Chamonix', 'Chamonix', ...
# $ Sport          <str> 'Skating', 'Skating', 'Skating', ...
# $ Discipline     <str> 'Figure skating', 'Figure skating', 'Figure skating', ...
# $ NOC            <str> 'AUT', 'AUT', 'AUT', ...
# $ Event          <str> 'individual', 'individual', 'pairs', ...
# $ Event gender   <str> 'M', 'W', 'X', ...
# $ Medal          <str> 'Silver', 'Gold', 'Gold', ...

# Return the glimpse output as a string.
# Note: In Polars 1.35+, use return_type="string".
# Older versions used return_as_string=True.
glimpse_text = df_medals.glimpse(return_type="string")
print(glimpse_text)

# Return the glimpse output as a DataFrame.
glimpse_frame = df_medals.glimpse(return_type="frame")
print(glimpse_frame)
# shape: (8, 3)
# ┌──────────────┬───────┬─────────────────────────────────┐
# │ column       ┆ dtype ┆ values                          │
# │ ---          ┆ ---   ┆ ---                             │
# │ str          ┆ str   ┆ list[str]                       │
# ╞══════════════╪═══════╪═════════════════════════════════╡
# │ Year         ┆ i64   ┆ ["1924", "1924", … "1924"]      │
# │ City         ┆ str   ┆ ["'Chamonix'", "'Chamonix'", …… │
# │ Sport        ┆ str   ┆ ["'Skating'", "'Skating'", … "… │
# │ Discipline   ┆ str   ┆ ["'Figure skating'", "'Figure … │
# │ NOC          ┆ str   ┆ ["'AUT'", "'AUT'", … "'FIN'"]   │
# │ Event        ┆ str   ┆ ["'individual'", "'individual'… │
# │ Event gender ┆ str   ┆ ["'M'", "'W'", … "'M'"]         │
# │ Medal        ┆ str   ┆ ["'Silver'", "'Gold'", … "'Gol… │
# └──────────────┴───────┴─────────────────────────────────┘

#####################
## df.null_count() ##
#####################
'''
df.null_count() returns a one-row DataFrame with the number of null values in each column.
This is the Polars equivalent of the null-count part of pandas df.info().
'''

print(df_medals.null_count())
# shape: (1, 8)
# ┌──────┬──────┬───────┬────────────┬─────┬───────┬──────────────┬───────┐
# │ Year ┆ City ┆ Sport ┆ Discipline ┆ NOC ┆ Event ┆ Event gender ┆ Medal │
# │ ---  ┆ ---  ┆ ---   ┆ ---        ┆ --- ┆ ---   ┆ ---          ┆ ---   │
# │ u32  ┆ u32  ┆ u32   ┆ u32        ┆ u32 ┆ u32   ┆ u32          ┆ u32   │
# ╞══════╪══════╪═══════╪════════════╪═════╪═══════╪══════════════╪═══════╡
# │ 0    ┆ 0    ┆ 0     ┆ 0          ┆ 0   ┆ 0     ┆ 0            ┆ 0     │
# └──────┴──────┴───────┴────────────┴─────┴───────┴──────────────┴───────┘

################
## df.count() ##
################
'''
df.count() returns the number of non-null values per column.
This is comparable to the "Non-Null Count" part of pandas df.info().
'''

print(df_medals.count())
# shape: (1, 8)
# ┌──────┬──────┬───────┬────────────┬──────┬───────┬──────────────┬───────┐
# │ Year ┆ City ┆ Sport ┆ Discipline ┆ NOC  ┆ Event ┆ Event gender ┆ Medal │
# │ ---  ┆ ---  ┆ ---   ┆ ---        ┆ ---  ┆ ---   ┆ ---          ┆ ---   │
# │ u32  ┆ u32  ┆ u32   ┆ u32        ┆ u32  ┆ u32   ┆ u32          ┆ u32   │
# ╞══════╪══════╪═══════╪════════════╪══════╪═══════╪══════════════╪═══════╡
# │ 2311 ┆ 2311 ┆ 2311  ┆ 2311       ┆ 2311 ┆ 2311  ┆ 2311         ┆ 2311  │
# └──────┴──────┴───────┴────────────┴──────┴───────┴──────────────┴───────┘

########################################
## Make your own compact info summary ##
########################################
'''
Because Polars inspection tools are composable, you can make a compact "info table" yourself.
This table is often more convenient than pandas df.info(), because it is a real DataFrame.
'''

info_summary = pl.DataFrame(
    {
        "column": df_medals.columns,
        "dtype": [str(dtype) for dtype in df_medals.dtypes],
        "null_count": [df_medals[col].null_count() for col in df_medals.columns],
        "non_null_count": [df_medals.height - df_medals[col].null_count() for col in df_medals.columns],
    }
)

print(info_summary)
# shape: (8, 4)
# ┌──────────────┬────────┬────────────┬────────────────┐
# │ column       ┆ dtype  ┆ null_count ┆ non_null_count │
# │ ---          ┆ ---    ┆ ---        ┆ ---            │
# │ str          ┆ str    ┆ i64        ┆ i64            │
# ╞══════════════╪════════╪════════════╪════════════════╡
# │ Year         ┆ Int64  ┆ 0          ┆ 2311           │
# │ City         ┆ String ┆ 0          ┆ 2311           │
# │ Sport        ┆ String ┆ 0          ┆ 2311           │
# │ Discipline   ┆ String ┆ 0          ┆ 2311           │
# │ NOC          ┆ String ┆ 0          ┆ 2311           │
# │ Event        ┆ String ┆ 0          ┆ 2311           │
# │ Event gender ┆ String ┆ 0          ┆ 2311           │
# │ Medal        ┆ String ┆ 0          ┆ 2311           │
# └──────────────┴────────┴────────────┴────────────────┘


#-------------------------------------------------------------------------------------------------------#
#-------------------------------------- 4. Memory and Performance --------------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''
Pandas:
    df.memory_usage(deep=True)

Polars:
    df.estimated_size(unit="b")

Important notes:
+ estimated_size() returns an estimate of the total visible heap allocation for the DataFrame.
+ It is not the same as pandas deep Python-object introspection.
+ For Object dtype columns, estimated_size() may severely underestimate memory because it only
  reports pointer size.
+ For normal Polars numeric/string/list/struct data, estimated_size() is the preferred API.
'''

#########################
## df.estimated_size() ##
#########################

print(df_medals.estimated_size())
# Estimated size in bytes.

print(df_medals.estimated_size("kb"))
# Estimated size in kilobytes.

print(df_medals.estimated_size("mb"))
# Estimated size in megabytes.

#################################
## Per-column estimated memory ##
#################################
'''
Polars does not have df.memory_usage(deep=True) returning one value per column.
You can approximate per-column memory by selecting one column at a time and calling estimated_size().
'''

memory_by_column = pl.DataFrame(
    {
        "column": df_medals.columns,
        "dtype": [str(dtype) for dtype in df_medals.dtypes],
        "estimated_size_b": [
            df_medals.select(pl.col(column)).estimated_size("b")
            for column in df_medals.columns
        ],
        "estimated_size_kb": [
            round(df_medals.select(pl.col(column)).estimated_size("kb"), 3)
            for column in df_medals.columns
        ],
    }
)

print(memory_by_column)
# shape: (8, 4)
# ┌──────────────┬────────┬──────────────────┬───────────────────┐
# │ column       ┆ dtype  ┆ estimated_size_b ┆ estimated_size_kb │
# │ ---          ┆ ---    ┆ ---              ┆ ---               │
# │ str          ┆ str    ┆ i64              ┆ f64               │
# ╞══════════════╪════════╪══════════════════╪═══════════════════╡
# │ Year         ┆ Int64  ┆ 18488            ┆ 18.055            │
# │ City         ┆ String ┆ 21866            ┆ 21.354            │
# │ Sport        ┆ String ┆ 15428            ┆ 15.066            │
# │ Discipline   ┆ String ┆ 28305            ┆ 27.642            │
# │ NOC          ┆ String ┆ 6933             ┆ 6.771             │
# │ Event        ┆ String ┆ 19636            ┆ 19.176            │
# │ Event gender ┆ String ┆ 2311             ┆ 2.257             │
# │ Medal        ┆ String ┆ 12318            ┆ 12.029            │
# └──────────────┴────────┴──────────────────┴───────────────────┘


####################################
## Total from per-column estimate ##
####################################
'''
The sum of per-column estimates is usually close to the total estimate,
but it is not guaranteed to equal df.estimated_size().
Columns can share buffers, and nested data can have special accounting rules.
'''

print(memory_by_column.select(pl.sum("estimated_size_b")))
# shape: (1, 1)
# ┌──────────────────┐
# │ estimated_size_b │
# │ ---              │
# │ i64              │
# ╞══════════════════╡
# │ 125285           │
# └──────────────────┘


print(df_medals.estimated_size("b"))
# 125285

###################
## df.n_chunks() ##
###################
'''
Polars columns are backed by chunked arrays.
Many chunks can appear after repeated concatenation or appending.
For some operations, fewer chunks can improve performance.
'''

print(df_medals.n_chunks())
# Number of chunks in the first column.

print(df_medals.n_chunks(strategy="all"))
# Number of chunks for every column, in column order.

##################
## df.rechunk() ##
##################
'''
df.rechunk() returns a DataFrame with contiguous memory chunks where possible.
Use this after many vertical concatenations if you want to reduce chunk fragmentation.
'''

df_rechunked = df_medals.rechunk()
print(df_rechunked.n_chunks(strategy="all"))
# Usually [1, 1, 1, 1, 1, 1, 1, 1]

########################
## df.shrink_to_fit() ##
########################
'''
df.shrink_to_fit() shrinks allocated capacity to the exact capacity needed for the data.
This can reduce memory overhead in some cases.
'''

before_mb = df_medals.estimated_size("mb")
df_shrunk = df_medals.shrink_to_fit()
after_mb = df_shrunk.estimated_size("mb")

print(before_mb)
print(after_mb)
# 0.11948108673095703
# 0.11948108673095703
# The result may be the same or smaller depending on current allocation capacity.


#-------------------------------------------------------------------------------------------------------#
#----------------------------- 5. LazyFrame Preview and Inspection -------------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''
Polars also has a LazyFrame API.
A LazyFrame does not immediately load/compute all data. It builds a query plan that is executed at collect().

For first inspection of lazy data, avoid collecting the entire dataset too early.
Use collect_schema(), head().collect(), and carefully chosen aggregations instead.
'''

lf_medals = pl.scan_csv(
    data_dir/"medals.csv",
    skip_rows=4,
)

################################
## LazyFrame.collect_schema() ##
################################

print(lf_medals.collect_schema())
# Schema({'Year': Int64, 'City': String, ...})
# Schema inspection can be done without collecting the full data.

########################################
## LazyFrame.collect_schema().names() ##
########################################
'''Retrieve the list of LazyFrame column names'''

print(lf_medals.collect_schema().names())
# ['Year', 'City', 'Sport', 'Discipline', 'NOC', 'Event', 'Event gender', 'Medal']

######################
## LazyFrame.head() ##
######################

print(lf_medals.head(3).collect())
# shape: (3, 8)
# First three rows from the lazy scan.

######################
## LazyFrame.tail() ##
######################

print(lf_medals.tail(3).collect())
# shape: (3, 8)
# Last three rows from the lazy scan.
# Note: tail() may require reading more data than head(), depending on the source.

#####################################
## Lazy row counts and null counts ##
#####################################
'''
LazyFrame does not have a cheap df.shape property like an eager DataFrame.
To get row counts or null counts lazily, express them as queries and collect the small result.
'''

print(lf_medals.select(pl.len().alias("n_rows")).collect())
# shape: (1, 1)
# n_rows
# 2311

print(lf_medals.select(pl.all().null_count()).collect())
# shape: (1, 8)
# Null count for each column.

#########################
## LazyFrame.explain() ##
#########################
'''
lf.explain() prints the lazy query plan.
This is useful for performance debugging and for checking whether filters/projections
are being pushed down to the scan.
'''

query = (
    lf_medals
    .filter(pl.col("Year") >= 2000)
    .select("Year", "City", "Sport", "Medal")
)

print(query.explain())
# Optimized query plan as text.

print(query.head(5).collect())
# Preview the result without collecting the full query output.
