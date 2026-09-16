'''
The idea of selecting and reordering columns
in tidypyrs is similar to polars.
=> The center is `tf.select()`

Content flow:
1. Explicit column selection and reordering
   -> tl.select([...]), tl.select("col1", "col2"), eager bracket selection,
      tl.select(f.colnames[slice_of_indices]) to select columns by slice of indices
      tl.select(tp.nth(list_of_indices)) to select columns by discrete indices
      f("*"), f("*").exclude(...), and regex column-name selection

2. Selecting all except some columns
   -> tl.drop(...)
   -> tp.exclude(...)
   => f.all().exclude(...)

3. Programmatic reordering patterns
   -> move columns to the front/end
   -> alphabetical ordering
   -> reverse ordering
   -> rule-based ordering

4. Expression selection and light transformation
   -> select raw columns
   -> transform columns
   -> rename with alias()
   -> rename all outputs

5. f() column-expression styles
   -> f("name"), f.name, f("*"),
      f("*").exclude(...), regex patterns such as f("^ham.*$"),
      and special-character column names

Note:
Selectors are not covered here. They are powerful enough to deserve a separate selectors script.
'''

from pathlib import Path

import tidypyrs as tp
from tidypyrs import f

data_dir = next(Path("/home").glob("**/DataScience*/data"))

# Optional display settings for tutorial output.
tp.Config.set_tbl_rows(12)
tp.Config.set_tbl_cols(12)
tp.Config.set_float_precision(2)

# =========================================================================================
# 0. Example Data
# =========================================================================================

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

tl_emp = tp.scan_csv(
    data_dir/"emp.csv",
    try_parse_dates=True,
)

print(tl_emp.collect())
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

print(tl_emp.collect_schema())
# Schema({'id': Int64, 'name': String, 'salary': Float64, 'start_date': Date, 'dept': String})

# =========================================================================================
# 1. Explicit column selection and reordering
# =========================================================================================

##-------------------------------------##
## tl.select(["col3", "col1", "col2"]) ##
##-------------------------------------##
'''
Important:
+ The order you write is the order of the output columns.
+ select() returns a new frame.
+ Polars has no custom row index, so there is no row-index side effect.
'''

# Reorder all columns.
print(
    tl_emp
    .select(["dept", "name", "salary", "id", "start_date"])
    .collect()
)
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
print(
    tl_emp
    .select(["salary", "id", "dept"])
    .collect()
)
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

##-----------------------------------##
## tl.select("col3", "col1", "col2") ##
##-----------------------------------##

# Equivalent positional-argument style.
print(
    tl_emp
    .select("salary", "id", "dept")
    .collect()
)
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
## tl.select(f.colnames[slice_of_indices]) ##
##-----------------------------------------##
'''
tl.select(f.colnames[slice_of_indices])
-> to select columns by slice of indices

NOTE: this requires collect_schema() internaly for TibbleLazy

For example:
    + tl.select(f.colnames()[::2]
    + tl.select(f.colnames()[-1]
'''

print(
    tl_emp
    .select(f.colnames[::2])
    .collect()
)
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

print(
    tl_emp
    .select(f.colnames[-1])
    .collect()
)
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
## tl.select(tp.nth(list_of_indices)) ##
##------------------------------------##
'''
tl.select(tp.nth(list_of_indices, strict=True)) to select columns by discrete indices

For example: tl.select(tp.nth([0, 2, 4])) or just tl.select(tp.nth(0, 2, 4))

if set strict=False, out-of-bounds indices are ignored.
if set strict=True, out-of-bounds indices cause error (default)
'''

print(
    tl_emp
    .select(tp.nth([0, 2, 4]))
    .collect()
)
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

print(
    tl_emp
    .select(tp.nth(1, 3))
    .collect()
)
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

##----------------------------------##
## tl.select(f("*"))                ##
## tl.select(f("*").exclude("ham")) ##
## tl.select(f("^ham.*$"))          ##
##----------------------------------##
'''
Inside tl.select(...), f(...) can select columns by name,
wildcard, or regular-expression pattern.

Common multi-column patterns:
+ f("*") selects all columns.
+ f("*").exclude("ham") selects all columns except "ham".
+ f("^ham.*$") selects columns whose names match the regex pattern.

Regex note:
+ For column-name regex selection, use a pattern that starts with ^ and ends with $.
+ "^ham.*$" means: column names that start with "ham".
'''

tl_select_pattern = tp.TibbleLazy(
    {
        "ham": [1, 2, 3],
        "hamburger": [10, 20, 30],
        "hammer": [100, 200, 300],
        "spam": [4, 5, 6],
        "eggs": [7, 8, 9],
    }
)
print(tl_select_pattern.collect())
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
print(
    tl_select_pattern
    .select(f("*"))
    .collect()
)
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
print(
    tl_select_pattern
    .select(f("*").exclude("ham"))
    .collect()
)
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
print(
    tl_select_pattern
    .select(f("^ham.*$"))
    .collect()
)
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
## tf[["col3", "col1", "col2"]] ##
##------------------------------##
'''
TibbleFrame also supports bracket selection for eager DataFrames.
However, df.select(...) is the recommended teaching style because it is also
the style used in expressions and LazyFrame pipelines.

ONLY DATA FRAME CAN DO THIS (lazy frame does not)
'''

tf_emp = tl_emp.collect()

# This is accepted for eager DataFrames, but is less Polars-idiomatic.
print(tf_emp[["salary", "id", "dept"]])
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

##------------------------------------##
## Single column: Series vs DataFrame ##
##------------------------------------##
'''
A common beginner question:

+ df_emp["name"] or df_emp.get_column("name") returns a Series.
+ df_emp.select("name") returns a DataFrame with one column.
'''

df_emp = tl_emp.collect()

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
