'''
Drop columns and rows in Polars.

This file is adapted from pandas workflows such as:
+ df.drop(labels=[...], axis=1, inplace=True/False)
+ df.drop(columns=[...], inplace=True/False)
+ df.drop(labels=[...], axis=0, inplace=True/False)
+ df.drop(index=[...], inplace=True/False)

Important Polars differences:
+ Polars DataFrame.drop(...) is for COLUMNS only.
+ Polars does not use pandas-style custom row indexes.
+ To drop rows, think in terms of keeping/removing rows with expressions:
    - df.filter(~condition)       # keep rows that do NOT match the drop condition
    - df.remove(condition)        # directly remove rows that match the condition
+ There is usually no inplace=True pattern in Polars.
  Reassign the result instead: df = df.drop(...), df = df.filter(...).

Content flow:
1. Example data and pandas-to-Polars mental model
2. Drop columns with DataFrame.drop(...)
3. Drop columns with strict=False for optional/missing columns
4. Drop columns with pl.exclude(...) or selectors
5. In-place column removal with drop_in_place(...)
6. Drop rows by condition using filter(~condition)
7. Drop rows by condition using remove(condition)
8. Drop rows by row number / row position
9. Drop rows by explicit row-label/key columns
10. Drop row ranges with slice/head/tail patterns
11. LazyFrame equivalents
12. Quick pandas-to-Polars mapping
'''

from pathlib import Path

import polars as pl
import polars.selectors as cs

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_float_precision(2)


# =========================================================================================
# 1. Example data and pandas-to-Polars mental model
# =========================================================================================
'''
The pandas source file demonstrates two broad tasks:

1. Drop columns:
   + pandas: df.drop(labels=[...], axis=1)
   + pandas: df.drop(columns=[...])

2. Drop rows:
   + pandas: df.drop(labels=[...], axis=0)
   + pandas: df.drop(index=[...])

In Polars:
+ df.drop(...) removes columns.
+ df.filter(...) keeps rows that satisfy a condition.
+ df.remove(...) removes rows that satisfy a condition.
+ There is no hidden row index. If you need row labels, store them as a normal column.
'''

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

df_emp = pl.read_csv(
    data_dir / "emp.csv",
    try_parse_dates=True,
)

print(df_emp)
# shape: (8, 5)
# ┌─────┬──────────┬────────┬────────────┬────────────┐
# │ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ i64 ┆ str      ┆ f64    ┆ date       ┆ str        │
# ╞═════╪══════════╪════════╪════════════╪════════════╡
# │ 1   ┆ Rick     ┆ 623.30 ┆ 2012-01-01 ┆ IT         │
# │ 2   ┆ Dan      ┆ 515.20 ┆ 2013-09-23 ┆ Operations │
# │ 3   ┆ Michelle ┆ 611.00 ┆ 2014-11-15 ┆ IT         │
# │ 4   ┆ Ryan     ┆ 729.00 ┆ 2014-05-11 ┆ HR         │
# │ 5   ┆ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# │ 6   ┆ Nina     ┆ 578.00 ┆ 2013-05-21 ┆ IT         │
# │ 7   ┆ Simon    ┆ 632.80 ┆ 2013-07-30 ┆ Operations │
# │ 8   ┆ Guru     ┆ 722.50 ┆ 2014-06-17 ┆ Finance    │
# └─────┴──────────┴────────┴────────────┴────────────┘

# Create an explicit row-label column to demonstrate pandas-index-like examples.
# This is a NORMAL column, not a special index.
df_labeled = df_emp.with_columns(
    pl.concat_str(pl.lit("row_"), pl.col("id").cast(pl.String)).alias("row_label")
).select("row_label", pl.all().exclude("row_label"))

print(df_labeled)
# shape: (8, 6)
# ┌───────────┬─────┬──────────┬────────┬────────────┬────────────┐
# │ row_label ┆ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---       ┆ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ str       ┆ i64 ┆ str      ┆ f64    ┆ date       ┆ str        │
# ╞═══════════╪═════╪══════════╪════════╪════════════╪════════════╡
# │ row_1     ┆ 1   ┆ Rick     ┆ 623.30 ┆ 2012-01-01 ┆ IT         │
# │ row_2     ┆ 2   ┆ Dan      ┆ 515.20 ┆ 2013-09-23 ┆ Operations │
# │ row_3     ┆ 3   ┆ Michelle ┆ 611.00 ┆ 2014-11-15 ┆ IT         │
# │ row_4     ┆ 4   ┆ Ryan     ┆ 729.00 ┆ 2014-05-11 ┆ HR         │
# │ row_5     ┆ 5   ┆ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# │ row_6     ┆ 6   ┆ Nina     ┆ 578.00 ┆ 2013-05-21 ┆ IT         │
# │ row_7     ┆ 7   ┆ Simon    ┆ 632.80 ┆ 2013-07-30 ┆ Operations │
# │ row_8     ┆ 8   ┆ Guru     ┆ 722.50 ┆ 2014-06-17 ┆ Finance    │
# └───────────┴─────┴──────────┴────────┴────────────┴────────────┘


# =========================================================================================
# 2. Drop columns with df.drop(...)
# =========================================================================================

##---------------------------------##
## Drop one column: df.drop("col") ##
##---------------------------------##
'''
Polars DataFrame.drop(...) removes columns by name.

There is no axis=1 argument.
There is no columns= argument.
There is no inplace= argument.
'''

df_dropped = df_emp.drop("dept")
print(df_dropped)
# shape: (8, 4)
# columns: id, name, salary, start_date

##----------------------------------------------##
## Drop multiple columns: df.drop(["c1", "c2"]) ##
##----------------------------------------------##

# Equivalent to pandas:
# df_emp.drop(labels=["start_date", "dept"], axis=1)
# df_emp.drop(columns=["start_date", "dept"])

df_dropped = df_emp.drop(["start_date", "dept"])
print(df_dropped)
# shape: (8, 3)
# ┌─────┬──────────┬────────┐
# │ id  ┆ name     ┆ salary │
# │ --- ┆ ---      ┆ ---    │
# │ i64 ┆ str      ┆ f64    │
# ╞═════╪══════════╪════════╡
# │ 1   ┆ Rick     ┆ 623.30 │
# │ 2   ┆ Dan      ┆ 515.20 │
# │ 3   ┆ Michelle ┆ 611.00 │
# │ 4   ┆ Ryan     ┆ 729.00 │
# │ 5   ┆ Gary     ┆ 843.25 │
# │ 6   ┆ Nina     ┆ 578.00 │
# │ 7   ┆ Simon    ┆ 632.80 │
# │ 8   ┆ Guru     ┆ 722.50 │
# └─────┴──────────┴────────┘

##-----------------------------------------------##
## Drop multiple columns as positional arguments ##
##-----------------------------------------------##
'''
Polars also accepts multiple column names as separate positional arguments.
This is equivalent to passing a list of names.
'''

df_dropped = df_emp.drop("id", "start_date")
print(df_dropped)
# shape: (8, 3)
# columns: name, salary, dept

##-----------------------------------------##
## Reassign to emulate pandas inplace=True ##
##-----------------------------------------##
'''
Most Polars operations return a new DataFrame.
To emulate pandas inplace=True, assign the result back to the same variable.
'''

df_tmp = df_emp.clone()
df_tmp = df_tmp.drop("start_date", "dept")
print(df_tmp)
# shape: (8, 3)
# columns: id, name, salary


# =========================================================================================
# 3. Drop columns with strict=False for optional names
# =========================================================================================

##----------------------------------------------##
## Missing columns: strict=True vs strict=False ##
##----------------------------------------------##
'''
By default, Polars checks that all requested column names exist.

This raises an error:
    df_emp.drop("bonus")

Use strict=False when a column may or may not exist.
This is useful in cleaning pipelines where some files have extra columns.
'''

# Safe: "bonus" does not exist, but strict=False ignores it.
df_dropped = df_emp.drop("bonus", strict=False)
print(df_dropped)
# shape: (8, 5)
# Same as df_emp because "bonus" was not present.

# Drop the existing column and ignore the missing one.
df_dropped = df_emp.drop("dept", "bonus", strict=False)
print(df_dropped)
# shape: (8, 4)
# columns: id, name, salary, start_date


# =========================================================================================
# 4. Drop columns with pl.exclude(...) or selectors
# =========================================================================================

##--------------##
## pl.exclude() ##
##--------------##
'''
For column-selection style, pl.exclude(...) means:
"select all columns except these".

This is not exactly the same method as df.drop(...), but the result is often the same.
It is useful when you are already writing a select(...) expression pipeline.
'''

df_without_dates = df_emp.select(pl.exclude("start_date"))
print(df_without_dates)
# shape: (8, 4)
# columns: id, name, salary, dept

# Exclude multiple columns.
df_without_id_dates = df_emp.select(pl.exclude(["id", "start_date"]))
print(df_without_id_dates)
# shape: (8, 3)
# columns: name, salary, dept

##----------------------------------##
## Drop by selector: df.drop(cs...) ##
##----------------------------------##
'''
If you studied the selectors file, df.drop(...) also accepts selectors.
Here we only show a few examples because selectors deserve their own script.
'''

# Drop all temporal columns, such as Date and Datetime.
df_no_temporal = df_emp.drop(cs.temporal())
print(df_no_temporal)
# shape: (8, 4)
# columns: id, name, salary, dept

# Drop all string columns.
df_no_strings = df_emp.drop(cs.string())
print(df_no_strings)
# shape: (8, 3)
# columns: id, salary, start_date

# Drop columns whose names end with "date".
df_no_date_named_cols = df_emp.drop(cs.ends_with("date"))
print(df_no_date_named_cols)
# shape: (8, 4)
# columns: id, name, salary, dept


# =========================================================================================
# 5. In-place column removal: drop_in_place()
# =========================================================================================

##--------------------##
## df.drop_in_place() ##
##--------------------##
'''
Polars usually encourages assignment instead of inplace mutation:
    df = df.drop("dept")

However, DataFrame.drop_in_place(name) exists.
It removes ONE column in-place and returns the removed Series.

Use it rarely in tutorials because it mutates the DataFrame and is less pipeline-friendly.
'''

df_tmp = df_emp.clone()
removed_series = df_tmp.drop_in_place("dept")

print(removed_series)
# shape: (8,)
# Series: 'dept' [str]

print(df_tmp)
# shape: (8, 4)
# columns: id, name, salary, start_date


# =========================================================================================
# 6. Drop rows by row number
# =========================================================================================

##------------------------------------------------------------##
## pandas df.drop(index=[0, 3, 5]) with default integer index ##
##------------------------------------------------------------##
'''
In pandas, df.drop(index=[0, 3, 5]) drops index labels 0, 3, and 5.
With a default RangeIndex, that often feels like dropping row positions.

Polars has no hidden index labels, so create a temporary row-number column,
filter/remove by that number, then drop the helper column.
'''

rows_to_drop = [0, 3, 5]

df_dropped_by_position = (
    df_emp
    .with_row_index("__row_nr")
    .filter(~pl.col("__row_nr").is_in(rows_to_drop))
    .drop("__row_nr")
)

print(df_dropped_by_position)
# shape: (5, 5)
# rows at original positions 0, 3, and 5 are removed
# remaining names: Dan, Michelle, Gary, Simon, Guru

# The same idea using remove(...).
df_dropped_by_position = (
    df_emp
    .with_row_index("__row_nr")
    .remove(pl.col("__row_nr").is_in(rows_to_drop))
    .drop("__row_nr")
)

print(df_dropped_by_position)
# shape: (5, 5)
# same result

##-------------------------------------##
## Reusable helper: drop row positions ##
##-------------------------------------##

def drop_row_positions(df: pl.DataFrame, positions: list[int]) -> pl.DataFrame:
    """Drop rows by zero-based row position."""

    return (
        df
        .with_row_index("__row_nr")
        .filter(~pl.col("__row_nr").is_in(positions))
        .drop("__row_nr")
    )


df_dropped_by_position = drop_row_positions(df_emp, [1, 2, 3])
print(df_dropped_by_position)
# shape: (5, 5)
# rows at original positions 1, 2, and 3 are removed
# remaining names: Rick, Gary, Nina, Simon, Guru

##--------------------------------------------##
## Boolean-mask alternative for row positions ##
##--------------------------------------------##
'''
DataFrame.filter(...) can also receive a Python list of booleans.
This is simple for tiny examples, but expression-style row numbers are usually
clearer in real Polars code.
'''

positions_to_drop = {0, 3, 5}
keep_mask = [i not in positions_to_drop for i in range(df_emp.height)]

df_dropped_by_mask = df_emp.filter(keep_mask)
print(df_dropped_by_mask)
# shape: (5, 5)
# same result as dropping positions 0, 3, and 5


# =========================================================================================
# 7. Drop rows by explicit row-label/key columns
# =========================================================================================

##------------------------------------------------------##
## pandas custom index labels -> Polars explicit column ##
##------------------------------------------------------##
'''
The pandas file creates labels such as row_1, row_2, row_3, ... as a custom index.

In Polars, use a normal column instead.
Then dropping rows by "row label" is just filtering/removing by that column.
'''

# Drop rows with labels row_2 and row_4.
df_dropped_labels = df_labeled.filter(
    ~pl.col("row_label").is_in(["row_2", "row_4"])
)

print(df_dropped_labels)
# shape: (6, 6)
# row_label row_2 and row_4 are removed

# Same idea using remove(...).
df_dropped_labels = df_labeled.remove(
    pl.col("row_label").is_in(["row_5", "row_6"])
)

print(df_dropped_labels)
# shape: (6, 6)
# row_label row_5 and row_6 are removed

##-----------------------------------------##
## Drop rows by stable business key column ##
##-----------------------------------------##
'''
Often, it is better to drop by a stable key column than by row position.
For this employee table, id is a better row identifier than physical row number.
'''

# Drop employees with id 1, 4, and 6.
df_dropped_ids = df_emp.filter(~pl.col("id").is_in([1, 4, 6]))
print(df_dropped_ids)
# shape: (5, 5)
# remaining ids: 2, 3, 5, 7, 8

# Same using remove(...).
df_dropped_ids = df_emp.remove(pl.col("id").is_in([1, 4, 6]))
print(df_dropped_ids)
# shape: (5, 5)
# remaining ids: 2, 3, 5, 7, 8


# =========================================================================================
# 10. Drop row ranges with slice/head/tail
# =========================================================================================

##-----------------------##
## Drop the first n rows ##
##-----------------------##
'''
DataFrame.slice(offset, length=None) selects rows starting at offset.
So dropping the first n rows is simply df.slice(n).
'''

# Drop the first 2 rows.
df_drop_first_two = df_emp.slice(2)
print(df_drop_first_two)
# shape: (6, 5)
# starts from Michelle

##----------------------##
## Drop the last n rows ##
##----------------------##

# Method 1: use slice with height - n.
df_drop_last_two = df_emp.slice(0, df_emp.height - 2)
print(df_drop_last_two)
# shape: (6, 5)
# ends at Nina

# Method 2: Polars head(-n) returns all rows except the last n rows.
df_drop_last_two = df_emp.head(-2)
print(df_drop_last_two)
# shape: (6, 5)
# same result

##-------------------------##
## Drop a middle row range ##
##-------------------------##
'''
To drop a contiguous middle block of rows, concatenate the rows before and
after the block.
'''

# Drop rows at positions 2, 3, and 4.
start = 2
length = 3

df_drop_middle = pl.concat(
    [
        df_emp.slice(0, start),
        df_emp.slice(start + length),
    ]
)

print(df_drop_middle)
# shape: (5, 5)
# dropped original positions 2, 3, 4: Michelle, Ryan, Gary


# =========================================================================================
# 11. LazyFrame equivalents
# =========================================================================================

##------------------##
## LazyFrame.drop() ##
##------------------##
'''
LazyFrame.drop(...) removes columns lazily.
The plan is executed only when collect() is called.
'''

lf_result = (
    df_emp.lazy()
    .drop("start_date", "dept")
    .collect()
)

print(lf_result)
# shape: (8, 3)
# columns: id, name, salary

##----------------------------------------##
## Lazy row-position dropping with helper ##
##----------------------------------------##

lf_result = (
    df_emp.lazy()
    .with_row_index("__row_nr")
    .remove(pl.col("__row_nr").is_in([0, 3, 5]))
    .drop("__row_nr")
    .collect()
)

print(lf_result)
# shape: (5, 5)
# rows at original positions 0, 3, and 5 are removed


# =========================================================================================
# 12. Quick pandas-to-Polars mapping
# =========================================================================================
'''
Pandas -> Polars summary

1. Drop columns

pandas:
    df.drop(labels=["start_date", "dept"], axis=1)
    df.drop(columns=["start_date", "dept"])

polars:
    df.drop(["start_date", "dept"])
    df.drop("start_date", "dept")
    df.select(pl.exclude(["start_date", "dept"]))

2. Drop rows by default integer positions

pandas:
    df.drop(index=[0, 3, 5])

polars:
    (
        df
        .with_row_index("__row_nr")
        .filter(~pl.col("__row_nr").is_in([0, 3, 5]))
        .drop("__row_nr")
    )

3. Drop rows by custom row labels

pandas:
    df_indexed.drop(index=["row_2", "row_4"])

polars:
    # Store row labels as a normal column first.
    df_labeled.filter(~pl.col("row_label").is_in(["row_2", "row_4"]))

4. In-place behavior

pandas:
    df.drop(columns=["dept"], inplace=True)

polars:
    df = df.drop("dept")

5. LazyFrame

pandas:
    no lazy equivalent in ordinary pandas

polars:
    (
        pl.scan_csv("file.csv")
        .drop("unneeded_col")
        .remove(pl.col("dept") == "IT")
        .collect()
    )
'''
