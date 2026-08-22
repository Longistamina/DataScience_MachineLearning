'''
Selecting and reordering columns in Polars.

This file is adapted from pandas workflows such as:
+ df[["col3", "col1", "col2"]]
+ df.reindex(columns=["col3", "col1", "col2"])

In Polars, the central idea is df.select(...):
+ It selects columns.
+ It controls output column order.
+ It can accept raw column names and expressions.
+ It works naturally with LazyFrame pipelines.

Content flow:
1. Explicit column selection and reordering
   -> df.select([...]), df.select("col1", "col2"), eager bracket selection,
      df.select(df.columns[slice_of_indices]) to select columns by slice of indices
      df.select(pl.nth(list_of_indices)) to select columns by discrete indices
      pl.col("*"), pl.col("*").exclude(...), and regex column-name selection
2. pandas reindex(columns=...) equivalent
   -> df.select([...]) for existing columns; helper for missing columns filled with null
3. Selecting all except some columns
   -> df.drop(...), pl.exclude(...), pl.all().exclude(...)
4. Programmatic reordering patterns
   -> move columns to the front/end; alphabetical, reverse, and rule-based ordering
5. Expression selection and light transformation
   -> select raw columns, transform columns, rename with alias(), and rename all outputs
6. LazyFrame selection
   -> the same select(...) style, executed only after collect()
7. pl.col() column-expression styles
   -> pl.col("name"), pl.col.name, c("name"), c.name, pl.col("*"),
      pl.col("*").exclude(...), regex patterns such as pl.col("^ham.*$"),
      and special-character column names

Note:
Selectors are not covered here. They are powerful enough to deserve a separate selectors script.
'''

from pathlib import Path

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_float_precision(2)


# =========================================================================================
# 0. Example Data
# =========================================================================================
'''
The pandas file uses emp.csv and focuses on two ways to select/reorder columns.
Here we try to load the same teaching data. If the data folder is not available,
a fallback DataFrame is created so the examples remain readable elsewhere.
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

print(df_emp.schema)
# Schema({'id': Int64, 'name': String, 'salary': Float64, 'start_date': Date, 'dept': String})


# =========================================================================================
# 1. Explicit column selection and reordering
# =========================================================================================

##-------------------------------------##
## df.select(["col3", "col1", "col2"]) ##
##-------------------------------------##
'''
The closest Polars equivalent of pandas df[[...]] is df.select([...]).

Important:
+ The order you write is the order of the output columns.
+ select() returns a new DataFrame.
+ Polars has no custom row index, so there is no row-index side effect.
'''

# Reorder all columns.
df_reordered = df_emp.select(["dept", "name", "salary", "id", "start_date"])
print(df_reordered)
# shape: (8, 5)
# ┌────────────┬──────────┬────────┬─────┬────────────┐
# │ dept       ┆ name     ┆ salary ┆ id  ┆ start_date │
# │ ---        ┆ ---      ┆ ---    ┆ --- ┆ ---        │
# │ str        ┆ str      ┆ f64    ┆ i64 ┆ date       │
# ╞════════════╪══════════╪════════╪═════╪════════════╡
# │ IT         ┆ Rick     ┆ 623.30 ┆ 1   ┆ 2012-01-01 │
# │ Operations ┆ Dan      ┆ 515.20 ┆ 2   ┆ 2013-09-23 │
# │ IT         ┆ Michelle ┆ 611.00 ┆ 3   ┆ 2014-11-15 │
# │ HR         ┆ Ryan     ┆ 729.00 ┆ 4   ┆ 2014-05-11 │
# │ Finance    ┆ Gary     ┆ 843.25 ┆ 5   ┆ 2015-03-27 │
# │ IT         ┆ Nina     ┆ 578.00 ┆ 6   ┆ 2013-05-21 │
# │ Operations ┆ Simon    ┆ 632.80 ┆ 7   ┆ 2013-07-30 │
# │ Finance    ┆ Guru     ┆ 722.50 ┆ 8   ┆ 2014-06-17 │
# └────────────┴──────────┴────────┴─────┴────────────┘

# Select only a subset of columns.
df_subset = df_emp.select(["salary", "id", "dept"])
print(df_subset)
# shape: (8, 3)
# ┌────────┬─────┬────────────┐
# │ salary ┆ id  ┆ dept       │
# │ ---    ┆ --- ┆ ---        │
# │ f64    ┆ i64 ┆ str        │
# ╞════════╪═════╪════════════╡
# │ 623.30 ┆ 1   ┆ IT         │
# │ 515.20 ┆ 2   ┆ Operations │
# │ 611.00 ┆ 3   ┆ IT         │
# │ 729.00 ┆ 4   ┆ HR         │
# │ 843.25 ┆ 5   ┆ Finance    │
# │ 578.00 ┆ 6   ┆ IT         │
# │ 632.80 ┆ 7   ┆ Operations │
# │ 722.50 ┆ 8   ┆ Finance    │
# └────────┴─────┴────────────┘

# Equivalent positional-argument style.
df_subset = df_emp.select("salary", "id", "dept")
# shape: (8, 3)
# ┌────────┬─────┬────────────┐
# │ salary ┆ id  ┆ dept       │
# │ ---    ┆ --- ┆ ---        │
# │ f64    ┆ i64 ┆ str        │
# ╞════════╪═════╪════════════╡
# │ 623.30 ┆ 1   ┆ IT         │
# │ 515.20 ┆ 2   ┆ Operations │
# │ 611.00 ┆ 3   ┆ IT         │
# │ 729.00 ┆ 4   ┆ HR         │
# │ 843.25 ┆ 5   ┆ Finance    │
# │ 578.00 ┆ 6   ┆ IT         │
# │ 632.80 ┆ 7   ┆ Operations │
# │ 722.50 ┆ 8   ┆ Finance    │
# └────────┴─────┴────────────┘

##-----------------------------------------##
## df.select(df.columns[slice_of_indices]) ##
##-----------------------------------------##
'''
df.select(df.columns[slice_of_indices]) to select columns by slice of indices

For example: df.select(df.columns[::2]) or df.select(df.columns[-1])
'''

print(df_emp.select(df_emp.columns[::2]))
# shape: (8, 3)
# ┌─────┬────────┬────────────┐
# │ id  ┆ salary ┆ dept       │
# │ --- ┆ ---    ┆ ---        │
# │ i64 ┆ f64    ┆ str        │
# ╞═════╪════════╪════════════╡
# │ 1   ┆ 623.30 ┆ IT         │
# │ 2   ┆ 515.20 ┆ Operations │
# │ 3   ┆ 611.00 ┆ IT         │
# │ 4   ┆ 729.00 ┆ HR         │
# │ 5   ┆ 843.25 ┆ Finance    │
# │ 6   ┆ 578.00 ┆ IT         │
# │ 7   ┆ 632.80 ┆ Operations │
# │ 8   ┆ 722.50 ┆ Finance    │
# └─────┴────────┴────────────┘

print(df_emp.select(df_emp.columns[-1]))
# shape: (8, 1)
# ┌────────────┐
# │ dept       │
# │ ---        │
# │ str        │
# ╞════════════╡
# │ IT         │
# │ Operations │
# │ IT         │
# │ HR         │
# │ Finance    │
# │ IT         │
# │ Operations │
# │ Finance    │
# └────────────┘

##------------------------------------##
## df.select(pl.nth(list_of_indices)) ##
##------------------------------------##
'''
df.select(pl.nth(list_of_indices, strict=True)) to select columns by discrete indices

For example: df.select(pl.nth([0, 2, 4])) or just df.select(pl.nth(0, 2, 4))

if set strict=False, out-of-bounds indices are ignored.
if set strict=True, out-of-bounds indices cause error (default)
'''

print(df_emp.select(pl.nth([0, 2, 4])))
# shape: (8, 3)
# ┌─────┬────────┬────────────┐
# │ id  ┆ salary ┆ dept       │
# │ --- ┆ ---    ┆ ---        │
# │ i64 ┆ f64    ┆ str        │
# ╞═════╪════════╪════════════╡
# │ 1   ┆ 623.30 ┆ IT         │
# │ 2   ┆ 515.20 ┆ Operations │
# │ 3   ┆ 611.00 ┆ IT         │
# │ 4   ┆ 729.00 ┆ HR         │
# │ 5   ┆ 843.25 ┆ Finance    │
# │ 6   ┆ 578.00 ┆ IT         │
# │ 7   ┆ 632.80 ┆ Operations │
# │ 8   ┆ 722.50 ┆ Finance    │
# └─────┴────────┴────────────┘

print(df_emp.select(pl.nth(1, 3)))
# shape: (8, 2)
# ┌──────────┬────────────┐
# │ name     ┆ start_date │
# │ ---      ┆ ---        │
# │ str      ┆ date       │
# ╞══════════╪════════════╡
# │ Rick     ┆ 2012-01-01 │
# │ Dan      ┆ 2013-09-23 │
# │ Michelle ┆ 2014-11-15 │
# │ Ryan     ┆ 2014-05-11 │
# │ Gary     ┆ 2015-03-27 │
# │ Nina     ┆ 2013-05-21 │
# │ Simon    ┆ 2013-07-30 │
# │ Guru     ┆ 2014-06-17 │
# └──────────┴────────────┘

##-------------------------------------------##
## df.select(pl.col("*"))                    ##
## df.select(pl.col("*").exclude("ham"))     ##
## df.select(pl.col("^ham.*$"))              ##
##-------------------------------------------##
'''
Inside df.select(...), pl.col(...) can select columns by name, wildcard,
or regular-expression pattern.

Common multi-column patterns:
+ pl.col("*") selects all columns.
+ pl.col("*").exclude("ham") selects all columns except "ham".
+ pl.col("^ham.*$") selects columns whose names match the regex pattern.

Regex note:
+ For column-name regex selection, use a pattern that starts with ^ and ends with $.
+ "^ham.*$" means: column names that start with "ham".
'''

df_select_pattern = pl.DataFrame(
    {
        "ham": [1, 2, 3],
        "hamburger": [10, 20, 30],
        "hammer": [100, 200, 300],
        "spam": [4, 5, 6],
        "eggs": [7, 8, 9],
    }
)
print(df_select_pattern)
# shape: (3, 5)
# ┌─────┬───────────┬────────┬──────┬──────┐
# │ ham ┆ hamburger ┆ hammer ┆ spam ┆ eggs │
# │ --- ┆ ---       ┆ ---    ┆ ---  ┆ ---  │
# │ i64 ┆ i64       ┆ i64    ┆ i64  ┆ i64  │
# ╞═════╪═══════════╪════════╪══════╪══════╡
# │ 1   ┆ 10        ┆ 100    ┆ 4    ┆ 7    │
# │ 2   ┆ 20        ┆ 200    ┆ 5    ┆ 8    │
# │ 3   ┆ 30        ┆ 300    ┆ 6    ┆ 9    │
# └─────┴───────────┴────────┴──────┴──────┘

# Select all columns using the wildcard expression.
print(df_select_pattern.select(pl.col("*")))
# shape: (3, 5)
# ┌─────┬───────────┬────────┬──────┬──────┐
# │ ham ┆ hamburger ┆ hammer ┆ spam ┆ eggs │
# │ --- ┆ ---       ┆ ---    ┆ ---  ┆ ---  │
# │ i64 ┆ i64       ┆ i64    ┆ i64  ┆ i64  │
# ╞═════╪═══════════╪════════╪══════╪══════╡
# │ 1   ┆ 10        ┆ 100    ┆ 4    ┆ 7    │
# │ 2   ┆ 20        ┆ 200    ┆ 5    ┆ 8    │
# │ 3   ┆ 30        ┆ 300    ┆ 6    ┆ 9    │
# └─────┴───────────┴────────┴──────┴──────┘

# Select all columns except one column.
print(df_select_pattern.select(pl.col("*").exclude("ham")))
# shape: (3, 4)
# ┌───────────┬────────┬──────┬──────┐
# │ hamburger ┆ hammer ┆ spam ┆ eggs │
# │ ---       ┆ ---    ┆ ---  ┆ ---  │
# │ i64       ┆ i64    ┆ i64  ┆ i64  │
# ╞═══════════╪════════╪══════╪══════╡
# │ 10        ┆ 100    ┆ 4    ┆ 7    │
# │ 20        ┆ 200    ┆ 5    ┆ 8    │
# │ 30        ┆ 300    ┆ 6    ┆ 9    │
# └───────────┴────────┴──────┴──────┘

# Select columns by regular-expression pattern.
# This selects column names beginning with "ham": ham, hamburger, hammer.
print(df_select_pattern.select(pl.col("^ham.*$")))
# shape: (3, 3)
# ┌─────┬───────────┬────────┐
# │ ham ┆ hamburger ┆ hammer │
# │ --- ┆ ---       ┆ ---    │
# │ i64 ┆ i64       ┆ i64    │
# ╞═════╪═══════════╪════════╡
# │ 1   ┆ 10        ┆ 100    │
# │ 2   ┆ 20        ┆ 200    │
# │ 3   ┆ 30        ┆ 300    │
# └─────┴───────────┴────────┘

##------------------------------##
## df[["col3", "col1", "col2"]] ##
##------------------------------##
'''
Polars DataFrame also supports bracket selection for eager DataFrames.
However, df.select(...) is the recommended teaching style because it is also
the style used in expressions and LazyFrame pipelines.
'''

# This is accepted for eager DataFrames, but is less Polars-idiomatic.
df_subset_brackets = df_emp[["salary", "id", "dept"]]
print(df_subset_brackets)
# shape: (8, 3)
# columns: salary, id, dept

##------------------------------------##
## Single column: Series vs DataFrame ##
##------------------------------------##
'''
A common beginner question:

+ df_emp["name"] or df_emp.get_column("name") returns a Series.
+ df_emp.select("name") returns a DataFrame with one column.
'''

s_name = df_emp["name"]
print(s_name)
# shape: (8,)
# Series: 'name' [str]

s_name = df_emp.get_column("name")
print(s_name)
# shape: (8,)
# Series: 'name' [str]

df_name = df_emp.select("name")
print(df_name)
# shape: (8, 1)
# columns: name


# =========================================================================================
# 2. pandas reindex(columns=...) equivalent
# =========================================================================================

##---------------------------------------------##
## Existing columns only: use df.select([...]) ##
##---------------------------------------------##
'''
In pandas, df.reindex(columns=[...]) is often used to reorder columns.
If all requested columns exist, Polars uses the same df.select([...]) pattern.
'''

df_reindexed_style = df_emp.select(["dept", "name", "salary", "id", "start_date"])
print(df_reindexed_style)
# shape: (8, 5)
# columns: dept, name, salary, id, start_date

df_reindexed_style = df_emp.select(["salary", "id", "dept"])
print(df_reindexed_style)
# shape: (8, 3)
# columns: salary, id, dept

##-----------------------------------------------------##
## Missing columns: pandas reindex fills with NaN/null ##
##-----------------------------------------------------##
'''
A key difference:

pandas:
    df.reindex(columns=["dept", "bonus", "salary"])

will create a missing "bonus" column filled with NaN.

Polars:
    df.select(["dept", "bonus", "salary"])

raises an error because "bonus" does not exist.

Use a helper when you intentionally want pandas-like "add missing columns as null" behavior.
'''


def select_or_null(df: pl.DataFrame, columns: list[str]) -> pl.DataFrame:
    """Select columns in the requested order; create missing columns as null."""

    return df.select(
        [
            pl.col(col) if col in df.columns else pl.lit(None).alias(col)
            for col in columns
        ]
    )


df_like_reindex = select_or_null(df_emp, ["dept", "bonus", "salary"])
print(df_like_reindex)
# shape: (8, 3)
# ┌────────────┬───────┬────────┐
# │ dept       ┆ bonus ┆ salary │
# │ ---        ┆ ---   ┆ ---    │
# │ str        ┆ null  ┆ f64    │
# ╞════════════╪═══════╪════════╡
# │ IT         ┆ null  ┆ 623.30 │
# │ Operations ┆ null  ┆ 515.20 │
# │ IT         ┆ null  ┆ 611.00 │
# │ HR         ┆ null  ┆ 729.00 │
# │ Finance    ┆ null  ┆ 843.25 │
# │ IT         ┆ null  ┆ 578.00 │
# │ Operations ┆ null  ┆ 632.80 │
# │ Finance    ┆ null  ┆ 722.50 │
# └────────────┴───────┴────────┘


# =========================================================================================
# 3. Selecting all except some columns
# =========================================================================================

##--------------##
## df.drop(...) ##
##--------------##
'''
For "all columns except these", df.drop(...) is the most direct Polars method.
'''

df_without_start_date = df_emp.drop("start_date")
print(df_without_start_date)
# shape: (8, 4)
# columns: id, name, salary, dept

df_without_many = df_emp.drop(["id", "start_date"])
print(df_without_many)
# shape: (8, 3)
# columns: name, salary, dept

##-----------------------------------------##
## pl.exclude(...) / pl.all().exclude(...) ##
##-----------------------------------------##
'''
Inside select(), you can also use expressions.

Useful patterns:
+ pl.exclude("col")
+ pl.all().exclude("col")
+ pl.all().exclude(["col1", "col2"])
'''

print(df_emp.select(pl.exclude("start_date")))
# shape: (8, 4)
# columns: id, name, salary, dept

print(df_emp.select(pl.all().exclude(["id", "start_date"])))
# shape: (8, 3)
# columns: name, salary, dept


# =========================================================================================
# 4. Programmatic reordering patterns
# =========================================================================================

##------------------------------------##
## Move selected columns to the front ##
##------------------------------------##

front_cols = ["dept", "name"]
other_cols = [col for col in df_emp.columns if col not in front_cols]

# dept and name first; all other columns keep their original relative order.
df_front = df_emp.select(front_cols + other_cols)
print(df_front)
# shape: (8, 5)
# ┌────────────┬──────────┬─────┬────────┬────────────┐
# │ dept       ┆ name     ┆ id  ┆ salary ┆ start_date │
# │ ---        ┆ ---      ┆ --- ┆ ---    ┆ ---        │
# │ str        ┆ str      ┆ i64 ┆ f64    ┆ date       │
# ╞════════════╪══════════╪═════╪════════╪════════════╡
# │ IT         ┆ Rick     ┆ 1   ┆ 623.30 ┆ 2012-01-01 │
# │ Operations ┆ Dan      ┆ 2   ┆ 515.20 ┆ 2013-09-23 │
# │ IT         ┆ Michelle ┆ 3   ┆ 611.00 ┆ 2014-11-15 │
# │ HR         ┆ Ryan     ┆ 4   ┆ 729.00 ┆ 2014-05-11 │
# │ Finance    ┆ Gary     ┆ 5   ┆ 843.25 ┆ 2015-03-27 │
# │ IT         ┆ Nina     ┆ 6   ┆ 578.00 ┆ 2013-05-21 │
# │ Operations ┆ Simon    ┆ 7   ┆ 632.80 ┆ 2013-07-30 │
# │ Finance    ┆ Guru     ┆ 8   ┆ 722.50 ┆ 2014-06-17 │
# └────────────┴──────────┴─────┴────────┴────────────┘

##----------------------------------##
## Move selected columns to the end ##
##----------------------------------##

end_cols = ["id", "start_date"]
other_cols = [col for col in df_emp.columns if col not in end_cols]

# id and start_date last; all other columns keep their original relative order.
df_end = df_emp.select(other_cols + end_cols)
print(df_end)
# shape: (8, 5)
# ┌──────────┬────────┬────────────┬─────┬────────────┐
# │ name     ┆ salary ┆ dept       ┆ id  ┆ start_date │
# │ ---      ┆ ---    ┆ ---        ┆ --- ┆ ---        │
# │ str      ┆ f64    ┆ str        ┆ i64 ┆ date       │
# ╞══════════╪════════╪════════════╪═════╪════════════╡
# │ Rick     ┆ 623.30 ┆ IT         ┆ 1   ┆ 2012-01-01 │
# │ Dan      ┆ 515.20 ┆ Operations ┆ 2   ┆ 2013-09-23 │
# │ Michelle ┆ 611.00 ┆ IT         ┆ 3   ┆ 2014-11-15 │
# │ Ryan     ┆ 729.00 ┆ HR         ┆ 4   ┆ 2014-05-11 │
# │ Gary     ┆ 843.25 ┆ Finance    ┆ 5   ┆ 2015-03-27 │
# │ Nina     ┆ 578.00 ┆ IT         ┆ 6   ┆ 2013-05-21 │
# │ Simon    ┆ 632.80 ┆ Operations ┆ 7   ┆ 2013-07-30 │
# │ Guru     ┆ 722.50 ┆ Finance    ┆ 8   ┆ 2014-06-17 │
# └──────────┴────────┴────────────┴─────┴────────────┘

##----------------------------------------------##
## Alphabetical / reverse / custom sorted order ##
##----------------------------------------------##

# Alphabetical order by column name.
df_alpha = df_emp.select(sorted(df_emp.columns))
print(df_alpha)
# columns: dept, id, name, salary, start_date

# Reverse the current column order.
df_reverse = df_emp.select(list(reversed(df_emp.columns)))
print(df_reverse)
# columns: dept, start_date, salary, name, id

# Put columns matching a rule first.
date_cols = [col for col in df_emp.columns if col.endswith("_date")]
non_date_cols = [col for col in df_emp.columns if col not in date_cols]
df_date_first = df_emp.select(date_cols + non_date_cols)
print(df_date_first)
# columns: start_date, id, name, salary, dept


# =========================================================================================
# 5. Expression selection and light transformation
# =========================================================================================
'''
Unlike pandas df[[...]], Polars select() can select columns AND create transformed
columns in the same call because it accepts expressions.
'''

# Select raw columns and a transformed column.
df_selected_expr = df_emp.select(
    "name",
    "dept",
    pl.col("salary").round(0).alias("salary_rounded"),
)
print(df_selected_expr)
# shape: (8, 3)
# ┌──────────┬────────────┬────────────────┐
# │ name     ┆ dept       ┆ salary_rounded │
# │ ---      ┆ ---        ┆ ---            │
# │ str      ┆ str        ┆ f64            │
# ╞══════════╪════════════╪════════════════╡
# │ Rick     ┆ IT         ┆ 623.00         │
# │ Dan      ┆ Operations ┆ 515.00         │
# │ Michelle ┆ IT         ┆ 611.00         │
# │ Ryan     ┆ HR         ┆ 729.00         │
# │ Gary     ┆ Finance    ┆ 843.00         │
# │ Nina     ┆ IT         ┆ 578.00         │
# │ Simon    ┆ Operations ┆ 633.00         │
# │ Guru     ┆ Finance    ┆ 722.00         │
# └──────────┴────────────┴────────────────┘

# Rename while selecting.
df_selected_renamed = df_emp.select(
    pl.col("id").alias("employee_id"),
    pl.col("name").alias("employee_name"),
    "dept",
)
print(df_selected_renamed)
# shape: (8, 3)
# columns: employee_id, employee_name, dept

# Select all columns and add a suffix to their names.
df_suffixed = df_emp.select(pl.all().name.suffix("_raw"))
print(df_suffixed)
# columns: id_raw, name_raw, salary_raw, start_date_raw, dept_raw


# =========================================================================================
# 6. LazyFrame selection
# =========================================================================================
'''
The same select() style works on LazyFrame.
LazyFrame selection is not executed until collect().

This is one reason df.select(...) is better to teach than pandas-style df[[...]]:
it transfers directly to lazy Polars workflows.
'''

lf_emp = df_emp.lazy()

result = (
    lf_emp
    .select("dept", "name", "salary")
    .collect()
)
print(result)
# shape: (8, 3)
# ┌────────────┬──────────┬────────┐
# │ dept       ┆ name     ┆ salary │
# │ ---        ┆ ---      ┆ ---    │
# │ str        ┆ str      ┆ f64    │
# ╞════════════╪══════════╪════════╡
# │ IT         ┆ Rick     ┆ 623.30 │
# │ Operations ┆ Dan      ┆ 515.20 │
# │ IT         ┆ Michelle ┆ 611.00 │
# │ HR         ┆ Ryan     ┆ 729.00 │
# │ Finance    ┆ Gary     ┆ 843.25 │
# │ IT         ┆ Nina     ┆ 578.00 │
# │ Operations ┆ Simon    ┆ 632.80 │
# │ Finance    ┆ Guru     ┆ 722.50 │
# └────────────┴──────────┴────────┘


# =========================================================================================
# 7. pl.col(): Create an expression representing column(s) in a DataFrame
# =========================================================================================
'''
pl.col(...) creates an Expr, not an immediate Series.

That expression is evaluated only inside a Polars context such as:
+ df.select(...)
+ df.with_columns(...)
+ df.filter(...)
+ df.group_by(...).agg(...)
+ LazyFrame select/filter/with_columns pipelines

In df.select("salary"), the string "salary" is convenient shorthand for selecting a column.
However, as soon as you want to transform, compare, aggregate, rename, or reuse a column,
use pl.col("salary") or the imported alias c("salary").
'''

##------------------------------------------##
## pl.col("col_name") -- safest / idiomatic ##
##------------------------------------------##
'''
The call syntax pl.col("col_name") is the safest and most explicit form.
It works for every valid column name, including names with spaces and punctuation.
'''

df_col_demo = pl.DataFrame(
    {
        "col_name": [10, 20, 30],
        "other_col": [1, 2, 3],
        "dept": ["IT", "HR", "IT"],
    }
)

print(df_col_demo)
# shape: (3, 3)
# ┌──────────┬───────────┬──────┐
# │ col_name ┆ other_col ┆ dept │
# │ ---      ┆ ---       ┆ ---  │
# │ i64      ┆ i64       ┆ str  │
# ╞══════════╪═══════════╪══════╡
# │ 10       ┆ 1         ┆ IT   │
# │ 20       ┆ 2         ┆ HR   │
# │ 30       ┆ 3         ┆ IT   │
# └──────────┴───────────┴──────┘

# Select one column using pl.col("col_name").
print(df_col_demo.select(pl.col("col_name")))
# shape: (3, 1)
# ┌──────────┐
# │ col_name │
# │ ---      │
# │ i64      │
# ╞══════════╡
# │ 10       │
# │ 20       │
# │ 30       │
# └──────────┘

# Select and transform using pl.col("col_name").
print(
    df_col_demo.select(
        pl.col("col_name"),
        (pl.col("col_name") + pl.col("other_col")).alias("col_sum"),
        pl.col("dept").str.to_lowercase().alias("dept_lower"),
    )
)
# shape: (3, 3)
# ┌──────────┬─────────┬────────────┐
# │ col_name ┆ col_sum ┆ dept_lower │
# │ ---      ┆ ---     ┆ ---        │
# │ i64      ┆ i64     ┆ str        │
# ╞══════════╪═════════╪════════════╡
# │ 10       ┆ 11      ┆ it         │
# │ 20       ┆ 22      ┆ hr         │
# │ 30       ┆ 33      ┆ it         │
# └──────────┴─────────┴────────────┘

# Use pl.col(...) in filter().
print(df_col_demo.filter(pl.col("col_name") >= 20))
# shape: (2, 3)
# ┌──────────┬───────────┬──────┐
# │ col_name ┆ other_col ┆ dept │
# │ ---      ┆ ---       ┆ ---  │
# │ i64      ┆ i64       ┆ str  │
# ╞══════════╪═══════════╪══════╡
# │ 20       ┆ 2         ┆ HR   │
# │ 30       ┆ 3         ┆ IT   │
# └──────────┴───────────┴──────┘

# Use pl.col(...) in with_columns().
print(
    df_col_demo.with_columns(
        (pl.col("col_name") * 2).alias("col_name_x2")
    )
)
# shape: (3, 4)
# ┌──────────┬───────────┬──────┬─────────────┐
# │ col_name ┆ other_col ┆ dept ┆ col_name_x2 │
# │ ---      ┆ ---       ┆ ---  ┆ ---         │
# │ i64      ┆ i64       ┆ str  ┆ i64         │
# ╞══════════╪═══════════╪══════╪═════════════╡
# │ 10       ┆ 1         ┆ IT   ┆ 20          │
# │ 20       ┆ 2         ┆ HR   ┆ 40          │
# │ 30       ┆ 3         ┆ IT   ┆ 60          │
# └──────────┴───────────┴──────┴─────────────┘

##--------------------------------------------------------##
## pl.col("*"), pl.col("*").exclude(...), and regex names ##
##--------------------------------------------------------##
'''
pl.col(...) is not limited to one exact column name.
It can also create multi-column expressions.

Three very common patterns are:
+ pl.col("*")
  Select all columns.

+ pl.col("*").exclude("ham")
  Start from all columns, then remove one or more columns.

+ pl.col("^ham.*$")
  Select columns whose names match a regular expression.

Again, regex column-name patterns should be written as full-name patterns:
+ start with ^
+ end with $
'''

df_col_pattern = pl.DataFrame(
    {
        "ham": [1, 2, 3],
        "hamburger": [10, 20, 30],
        "hammer": [100, 200, 300],
        "spam": [4, 5, 6],
        "eggs": [7, 8, 9],
    }
)

print(df_col_pattern)
# shape: (3, 5)
# columns: ham, hamburger, hammer, spam, eggs

# pl.col("*") selects every column.
print(df_col_pattern.select(pl.col("*")))
# shape: (3, 5)
# columns: ham, hamburger, hammer, spam, eggs

# pl.col("*").exclude("ham") selects every column except "ham".
print(df_col_pattern.select(pl.col("*").exclude("ham")))
# shape: (3, 4)
# columns: hamburger, hammer, spam, eggs

# pl.col("^ham.*$") selects columns matching the regex pattern.
print(df_col_pattern.select(pl.col("^ham.*$")))
# shape: (3, 3)
# columns: ham, hamburger, hammer

# You can also combine wildcard/regex selection with transformations.
print(
    df_col_pattern.select(
        pl.col("^ham.*$") * 10,
    )
)
# shape: (3, 3)
# columns: ham, hamburger, hammer
# values are multiplied by 10

##----------------------------------------------##
## pl.col.col_name -- convenient attribute form ##
##----------------------------------------------##
'''
For simple column names that are valid Python identifiers, Polars also allows
attribute-style column access:

    pl.col.col_name

This creates the same kind of expression as pl.col("col_name").
It is convenient for quick examples, but the call syntax is more robust.
'''

print(df_col_demo.select(pl.col.col_name))
# shape: (3, 1)
# ┌──────────┐
# │ col_name │
# │ ---      │
# │ i64      │
# ╞══════════╡
# │ 10       │
# │ 20       │
# │ 30       │
# └──────────┘

print(
    df_col_demo.select(
        pl.col.col_name,
        (pl.col.col_name + pl.col.other_col).alias("col_sum"),
    )
)
# shape: (3, 2)
# columns: col_name, col_sum

##-------------------------------------------------##
## from polars import col as c, then c("col_name") ##
##-------------------------------------------------##
'''
At the top of this file we imported:

    from polars import col as c

This makes c("col_name") a shorter alias for pl.col("col_name").
Some people like this style in expression-heavy code because it reduces repetition.
'''

print(df_col_demo.select(c("col_name")))
# shape: (3, 1)
# ┌──────────┐
# │ col_name │
# │ ---      │
# │ i64      │
# ╞══════════╡
# │ 10       │
# │ 20       │
# │ 30       │
# └──────────┘

print(
    df_col_demo.select(
        c("dept"),
        (c("col_name") / c("other_col")).alias("ratio"),
    )
)
# shape: (3, 2)
# ┌──────┬───────┐
# │ dept ┆ ratio │
# │ ---  ┆ ---   │
# │ str  ┆ f64   │
# ╞══════╪═══════╡
# │ IT   ┆ 10.00 │
# │ HR   ┆ 10.00 │
# │ IT   ┆ 10.00 │
# └──────┴───────┘

##----------------------------------------------##
## c("*"), c("*").exclude(...), and regex names ##
##----------------------------------------------##

print(df_col_pattern)
# shape: (3, 5)
# ┌─────┬───────────┬────────┬──────┬──────┐
# │ ham ┆ hamburger ┆ hammer ┆ spam ┆ eggs │
# │ --- ┆ ---       ┆ ---    ┆ ---  ┆ ---  │
# │ i64 ┆ i64       ┆ i64    ┆ i64  ┆ i64  │
# ╞═════╪═══════════╪════════╪══════╪══════╡
# │ 1   ┆ 10        ┆ 100    ┆ 4    ┆ 7    │
# │ 2   ┆ 20        ┆ 200    ┆ 5    ┆ 8    │
# │ 3   ┆ 30        ┆ 300    ┆ 6    ┆ 9    │
# └─────┴───────────┴────────┴──────┴──────┘

# The same multi-column patterns work with the alias c.
print(df_col_pattern.select(c("*")))
# shape: (3, 5)
# columns: ham, hamburger, hammer, spam, eggs

print(df_col_pattern.select(c("*").exclude("ham")))
# shape: (3, 4)
# columns: hamburger, hammer, spam, eggs

print(df_col_pattern.select(c("^ham.*$")))
# shape: (3, 3)
# columns: ham, hamburger, hammer

# You can also combine wildcard/regex selection with transformations.
print(
    df_col_pattern.select(
        c("^ham.*$") * 10,
    )
)
# shape: (3, 3)
# columns: ham, hamburger, hammer
# values are multiplied by 10

##------------------------------------##
## c.col_name -- short attribute form ##
##------------------------------------##
'''
Because c is just an alias for polars.col, c.col_name also works for simple
identifier-like column names.

This is the shortest form, but it has the same limitation as pl.col.col_name:
it is only appropriate when the column name is a clean Python identifier.
'''

print(df_col_demo.select(c.col_name))
# shape: (3, 1)
# ┌──────────┐
# │ col_name │
# │ ---      │
# │ i64      │
# ╞══════════╡
# │ 10       │
# │ 20       │
# │ 30       │
# └──────────┘

print(
    df_col_demo.select(
        c.dept,
        c.col_name.alias("value"),
        (c.col_name > 15).alias("is_large"),
    )
)
# shape: (3, 3)
# ┌──────┬───────┬──────────┐
# │ dept ┆ value ┆ is_large │
# │ ---  ┆ ---   ┆ ---      │
# │ str  ┆ i64   ┆ bool     │
# ╞══════╪═══════╪══════════╡
# │ IT   ┆ 10    ┆ false    │
# │ HR   ┆ 20    ┆ true     │
# │ IT   ┆ 30    ┆ true     │
# └──────┴───────┴──────────┘

##-------------------------------------------------------------##
## Special characters: use pl.col("col name") or c("col name") ##
##-------------------------------------------------------------##
'''
Column names often contain spaces, punctuation, leading digits, or other characters
that cannot be written with Python dot syntax.

For these columns, use the call syntax:
+ pl.col("col name")
+ c("col name")

Do NOT use attribute syntax for these cases.
'''

df_special_names = pl.DataFrame(
    {
        "col name": [10, 20, 30],      # contains a space
        "sales($)": [100.5, 200.0, 150.25],  # contains punctuation
        "2024 score": [90, 85, 95],   # starts with digits and contains a space
        "class.level": ["A", "B", "A"],  # contains a dot
    }
)

print(df_special_names)
# shape: (3, 4)
# ┌──────────┬──────────┬────────────┬─────────────┐
# │ col name ┆ sales($) ┆ 2024 score ┆ class.level │
# │ ---      ┆ ---      ┆ ---        ┆ ---         │
# │ i64      ┆ f64      ┆ i64        ┆ str         │
# ╞══════════╪══════════╪════════════╪═════════════╡
# │ 10       ┆ 100.50   ┆ 90         ┆ A           │
# │ 20       ┆ 200.00   ┆ 85         ┆ B           │
# │ 30       ┆ 150.25   ┆ 95         ┆ A           │
# └──────────┴──────────┴────────────┴─────────────┘

print(
    df_special_names.select(
        pl.col("col name"),
        c("sales($)").round(0).alias("sales_rounded"),
        pl.col("2024 score").alias("score_2024"),
        c("class.level").alias("class_level"),
    )
)
# shape: (3, 4)
# ┌──────────┬───────────────┬────────────┬─────────────┐
# │ col name ┆ sales_rounded ┆ score_2024 ┆ class_level │
# │ ---      ┆ ---           ┆ ---        ┆ ---         │
# │ i64      ┆ f64           ┆ i64        ┆ str         │
# ╞══════════╪═══════════════╪════════════╪═════════════╡
# │ 10       ┆ 100.00        ┆ 90         ┆ A           │
# │ 20       ┆ 200.00        ┆ 85         ┆ B           │
# │ 30       ┆ 150.00        ┆ 95         ┆ A           │
# └──────────┴───────────────┴────────────┴─────────────┘

# These are invalid or unsafe ideas, so keep them as comments:
# pl.col.col name        # invalid Python syntax because of the space
# pl.col.2024_score      # invalid Python syntax because attributes cannot start with digits
# pl.col.sales($)        # invalid Python syntax because of punctuation
# pl.col.class.level     # invalid/ambiguous because class is a Python keyword and dot is not literal

##----------------------------------##
## Practical recommendation summary ##
##----------------------------------##
'''
Recommended habit:

1. Use pl.col("column_name") when teaching beginners or writing robust examples.
2. Use c("column_name") when you want shorter expression-heavy code.
3. Use pl.col.column_name or c.column_name only for quick code with clean column names.
4. Use pl.col("*") or c("*") for all-column wildcard selection.
5. Use pl.col("*").exclude("name") or c("*").exclude("name") for all except some columns.
6. Use pl.col("^pattern$") or c("^pattern$") for regex column-name selection.
7. Always use pl.col("col name") or c("col name") when the column name has spaces,
   punctuation, leading digits, dots, or other special characters.
'''
