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
   -> f("name"), f.name,
      f("*"), f("*").exclude(...),
      regex patterns such as f("^ham.*$"),
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

##------------------------------------##
## Single column: Series vs DataFrame ##
##------------------------------------##
'''
A common beginner question:

+ `tl_emp.pull("name")` returns a Series.
+ `tl_emp.select("name").collect()` returns a DataFrame with one column.
'''

print(tl_emp.pull("name"))
# shape: (8,)
# Series: 'name' [str]
# [
# 	"Rick"
# 	"Dan"
# 	"Michelle"
# 	"Ryan"
# 	"Gary"
# 	"Nina"
# 	"Simon"
# 	"Guru"
# ]

print(tl_emp.select("name").collect())
# shape: (8, 1)
# ┌──────────┐
# │ name     │
# │ ---      │
# │ str      │
# ╞══════════╡
# │ Rick     │
# │ Dan      │
# │ Michelle │
# │ Ryan     │
# │ Gary     │
# │ Nina     │
# │ Simon    │
# │ Guru     │
# └──────────┘

# =========================================================================================
# 2. Selecting all except some columns
# =========================================================================================

##--------------##
## tl.drop(...) ##
##--------------##
'''
For "all columns except these", tl.drop(...) is the most direct Polars method.
'''

print(
    tl_emp
    .drop("start_date")
    .collect()
)
# shape: (8, 4)
# columns: id, name, salary, dept

print(
    tl_emp
    .drop("id", "start_date") # or `.drop(["id", "start_date"])`
    .collect()
)
# shape: (8, 3)
# columns: name, salary, dept

##----------------------------------------##
## tp.exclude(...) / f.all().exclude(...) ##
##----------------------------------------##
'''
Inside select(), you can also use expressions.

Useful patterns:
+ tp.exclude("col")
+ f.all().exclude("col")
+ f.all().exclude("col1", "col2")
'''

print(
    tl_emp
    .select(tp.exclude("start_date"))
    .collect()
)
# shape: (8, 4)
# columns: id, name, salary, dept

print(
    tl_emp
    .select(f.all().exclude("id", "start_date")) # or `.exclude(["id", "start_date"])`
    .collect()
)
# shape: (8, 3)
# columns: name, salary, dept

# =========================================================================================
# 3. Programmatic reordering patterns
# =========================================================================================

##------------------------------------##
## Move selected columns to the front ##
##------------------------------------##

front_cols = ["dept", "name"]

print(
    tl_emp
    .select(*front_cols, tp.exclude(front_cols))
    .collect()
)
# dept and name first; all other columns keep their original relative order.
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

print(
    tl_emp
    .select(tp.exclude(end_cols), *end_cols)
    .collect()
)
# id and start_date last; all other columns keep their original relative order.
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
print(
    tl_emp
    .select(f.colnames.sort())
    .collect()
)
# columns: dept, id, name, salary, start_date

# Reverse the current column order.
print(
    tl_emp
    .select(f.colnames.reverse())
    .collect()
)
# columns: dept, start_date, salary, name, id

# Put columns matching a rule first.
print(
    tl_emp
    .select(f("^.*_date$"), tp.exclude("^.*_date$"))
    .collect()
)
# columns: start_date, id, name, salary, dept

# =========================================================================================
# 4. Expression selection and light transformation
# =========================================================================================
'''
Unlike pandas df[[...]], Polars select() can select columns AND create transformed
columns in the same call because it accepts expressions.
'''

##---------------------------------------------##
## Select raw columns and a transformed column ##
##---------------------------------------------##

print(
    tl_emp
    .select(
        "name",
        "dept",
        f("salary").round(0).alias("salary_rounded"),
    )
    .collect()
)
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

##------------------------##
## Rename while selecting ##
##------------------------##

print(
    tl_emp
    .select(
        f("id").alias("employee_id"),
        f("name").alias("employee_name"),
        "dept",
    )
    .collect()
)
# shape: (8, 3)
# columns: employee_id, employee_name, dept

# Select all columns and add a suffix to their names.
print(
    tl_emp
    .select(f.all().name.suffix("_raw"))
    .collect()
)
# columns: id_raw, name_raw, salary_raw, start_date_raw, dept_raw

# =========================================================================================
# 5. `f()`: Create an expression representing column(s) in a DataFrame
# =========================================================================================
'''
f(...) creates an Expr, not an immediate Series.

That expression is evaluated only inside a Polars context such as:
+ tl.select(...)
+ tl.with_columns(...)
+ tl.filter(...)
+ tl.group_by(...).agg(...)

In `tl.select("salary")`, the string "salary" is convenient shorthand for selecting a column.
However, as soon as you want to transform, compare, aggregate, rename, or reuse a column,
use `f("salary")`
'''

##-------------------------------------##
## f("col_name") -- safest / idiomatic ##
##-------------------------------------##
'''
The call syntax f("col_name") is the safest and most explicit form.
It works for every valid column name, including names with spaces and punctuation.
'''

tl_col_demo = tp.TibbleLazy(
    {
        "col_name": [10, 20, 30],
        "other_col": [1, 2, 3],
        "dept": ["IT", "HR", "IT"],
    }
)

print(tl_col_demo.collect())
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

# Select one column using f("col_name").
print(
    tl_col_demo
    .select(f("col_name"))
    .collect()
)
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

# Select and transform using f("col_name").
print(
    tl_col_demo
    .select(
        f("col_name"),
        (f("col_name") + f("other_col")).alias("col_sum"),
        f("dept").str.to_lowercase().alias("dept_lower"),
    )
    .collect()
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

# Use f(...) in filter().
print(
    tl_col_demo
    .filter(f("col_name") >= 20)
    .collect()
)
# shape: (2, 3)
# ┌──────────┬───────────┬──────┐
# │ col_name ┆ other_col ┆ dept │
# │ ---      ┆ ---       ┆ ---  │
# │ i64      ┆ i64       ┆ str  │
# ╞══════════╪═══════════╪══════╡
# │ 20       ┆ 2         ┆ HR   │
# │ 30       ┆ 3         ┆ IT   │
# └──────────┴───────────┴──────┘

# Use f(...) in with_columns().
print(
    tl_col_demo
    .with_columns(
        (f("col_name") * 2).alias("col_name_x2")
    )
    .collect()
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

##----------------------------------------------##
## f("*"), f("*").exclude(...), and regex names ##
##----------------------------------------------##
'''
f(...) is not limited to one exact column name.
It can also create multi-column expressions.

Three very common patterns are:
+ f("*")
  Select all columns.

+ f("*").exclude("ham")
  Start from all columns, then remove one or more columns.

+ f("^ham.*$")
  Select columns whose names match a regular expression.

Again, regex column-name patterns should be written as full-name patterns:
+ start with ^
+ end with $
'''

tl_col_pattern = tp.TibbleLazy(
    {
        "ham": [1, 2, 3],
        "hamburger": [10, 20, 30],
        "hammer": [100, 200, 300],
        "spam": [4, 5, 6],
        "eggs": [7, 8, 9],
    }
)

print(tl_col_pattern.collect())
# shape: (3, 5)
# columns: ham, hamburger, hammer, spam, eggs

# f("*") selects every column.
print(
    tl_col_pattern
    .select(f("*"))
    .collect()
)
# shape: (3, 5)
# columns: ham, hamburger, hammer, spam, eggs

# f("*").exclude("ham") selects every column except "ham".
print(
    tl_col_pattern
    .select(f("*").exclude("ham"))
    .collect()
)
# shape: (3, 4)
# columns: hamburger, hammer, spam, eggs

# f("^ham.*$") selects columns matching the regex pattern.
print(
    tl_col_pattern
    .select(f("^ham.*$"))
    .collect()
)
# shape: (3, 3)
# columns: ham, hamburger, hammer

# You can also combine wildcard/regex selection with transformations.
print(
    tl_col_pattern
    .select(
        f("^ham.*$") * 10,
    )
    .collect()
)
# shape: (3, 3)
# columns: ham, hamburger, hammer
# values are multiplied by 10

##-----------------------------------------##
## f.col_name -- convenient attribute form ##
##-----------------------------------------##
'''
For simple column names that are valid Python identifiers,
tidypyrs also allows attribute-style column access:

    f.col_name

This creates the same kind of expression as f("col_name").
It is convenient for quick examples, but the call syntax is more robust.
'''

print(
    tl_col_demo
    .select(f.col_name)
    .collect()
)
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
    tl_col_demo
    .select(
        f.col_name,
        (f.col_name + f.other_col).alias("col_sum"),
    )
    .collect()
)
# shape: (3, 2)
# columns: col_name, col_sum

##---------------------------------------##
## Special characters: use f("col name") ##
##---------------------------------------##
'''
Column names often contain spaces, punctuation, leading digits, or other characters
that cannot be written with Python dot syntax.

For these columns, use the call syntax:
    f("col name")

Do NOT use attribute syntax for these cases.
'''

tl_special_names = tp.TibbleLazy(
    {
        "col name": [10, 20, 30],      # contains a space
        "sales($)": [100.5, 200.0, 150.25],  # contains punctuation
        "2024 score": [90, 85, 95],   # starts with digits and contains a space
        "class.level": ["A", "B", "A"],  # contains a dot
    }
)

print(tl_special_names.collect())
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
    tl_special_names
    .select(
        f("col name"),
        f("sales($)").round(0).alias("sales_rounded"),
        f("2024 score").alias("score_2024"),
        f("class.level").alias("class_level"),
    )
    .collect()
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
# f.col name        # invalid Python syntax because of the space
# f.2024_score      # invalid Python syntax because attributes cannot start with digits
# f.sales($)        # invalid Python syntax because of punctuation
# f.class.level     # invalid/ambiguous because class is a Python keyword and dot is not literal

##----------------------------------##
## Practical recommendation summary ##
##----------------------------------##
'''
Recommended habit:

1. Use f("column_name") is prioritized
2. Use f.column_name only for quick code with clean column names.
3. Use f("*") for all-column wildcard selection.
4. Use f("*").exclude("name") for all except some columns.
5. Use f("^pattern$") for regex column-name selection.
6. Always use f("col name") when the column name has spaces,
   punctuation, leading digits, dots, or other special characters.
'''
