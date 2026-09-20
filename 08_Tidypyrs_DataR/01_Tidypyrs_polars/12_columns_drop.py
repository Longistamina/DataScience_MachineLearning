'''
Here are several ways to drop columns in Polars.
    + `tl.drop(...)` to drop specified
    + `tl.drop(..., strict=False)` to tolerate missing columns
    + `tl.select(tp.exclude(...))` can also be used to drop columns
    + `tl.drop(tl.where(...)` or `tl.drop(cs...)` can also be used to drop columns
'''

from pathlib import Path

import tidypyrs as tp
from tidypyrs import f
from tidypyrs import selectors as cs

# Optional display settings for tutorial output.
tp.Config.set_tbl_cols(12)
tp.Config.set_float_precision(2)

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

##---------------------------------##
## Drop one column: tl.drop("col") ##
##---------------------------------##

print(
    tl_emp
    .drop("dept")
    .collect()
)
# shape: (8, 4)
# ┌─────┬──────────┬────────┬────────────┐
# │ id  ┆ name     ┆ salary ┆ start_date │
# │ --- ┆ ---      ┆ ---    ┆ ---        │
# │ i64 ┆ str      ┆ f64    ┆ date       │
# ╞═════╪══════════╪════════╪════════════╡
# │ 1   ┆ Rick     ┆ 623.30 ┆ 2012-01-01 │
# │ 2   ┆ Dan      ┆ 515.20 ┆ 2013-09-23 │
# │ 3   ┆ Michelle ┆ 611.00 ┆ 2014-11-15 │
# │ 4   ┆ Ryan     ┆ 729.00 ┆ 2014-05-11 │
# │ 5   ┆ Gary     ┆ 843.25 ┆ 2015-03-27 │
# │ 6   ┆ Nina     ┆ 578.00 ┆ 2013-05-21 │
# │ 7   ┆ Simon    ┆ 632.80 ┆ 2013-07-30 │
# │ 8   ┆ Guru     ┆ 722.50 ┆ 2014-06-17 │
# └─────┴──────────┴────────┴────────────┘

##--------------------------------------------##
## Drop multiple columns: tl.drop("c1", "c2") ##
##--------------------------------------------##

print(
    tl_emp
    .drop("start_date", "dept") # `.drop(["start_date", "dept"])` also works
    .collect()
)
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

##----------------------------------------------------------##
## `tl.drop(..., strict=False)` to tolerate missing columns ##
##----------------------------------------------------------##
'''
By default, tidypyrs checks that all requested column names exist.

This raises an error:
    `tl_emp.drop("bonus")`

Use `strict=False` when a column may or may not exist.
This is useful in cleaning pipelines where some files have extra columns.
'''

# Safe: "bonus" does not exist, but strict=False ignores it.
print(
    tl_emp
    .drop("bonus", strict=False)
    .collect()
)
# shape: (8, 5)
# Same as df_emp because "bonus" was not present.

# Drop the existing column and ignore the missing one.
print(
    tl_emp
    .drop("dept", "bonus", strict=False)
    .collect()
)
# shape: (8, 4)
# ┌─────┬──────────┬────────┬────────────┐
# │ id  ┆ name     ┆ salary ┆ start_date │
# │ --- ┆ ---      ┆ ---    ┆ ---        │
# │ i64 ┆ str      ┆ f64    ┆ date       │
# ╞═════╪══════════╪════════╪════════════╡
# │ 1   ┆ Rick     ┆ 623.30 ┆ 2012-01-01 │
# │ 2   ┆ Dan      ┆ 515.20 ┆ 2013-09-23 │
# │ 3   ┆ Michelle ┆ 611.00 ┆ 2014-11-15 │
# │ 4   ┆ Ryan     ┆ 729.00 ┆ 2014-05-11 │
# │ 5   ┆ Gary     ┆ 843.25 ┆ 2015-03-27 │
# │ 6   ┆ Nina     ┆ 578.00 ┆ 2013-05-21 │
# │ 7   ┆ Simon    ┆ 632.80 ┆ 2013-07-30 │
# │ 8   ┆ Guru     ┆ 722.50 ┆ 2014-06-17 │
# └─────┴──────────┴────────┴────────────┘

##----------------------------------##
## Drop columns with `tp.exclude()` ##
##----------------------------------##
'''
For column-selection style, `pl.exclude(...)` means:
"select all columns except these".

This is not exactly the same method as `tl.drop(...)`, but the result is often the same.
It is useful when you are already writing a select(...) expression pipeline.
'''

print(
    tl_emp
    .select(tp.exclude("start_date"))
    .collect()
)
# shape: (8, 4)
# columns: id, name, salary, dept

# Exclude multiple columns.
print(
    tl_emp
    .select(tp.exclude("id", "start_date")) # `pl.exclude(["id", "start_date"])` also works
    .collect()
)
# shape: (8, 3)
# columns: name, salary, dept

##---------------------------------------------------------------##
## Drop columns with `tl.drop(tl.where(...)` or `tl.drop(cs...)` ##
##---------------------------------------------------------------##

# Drop all temporal columns, such as Date and Datetime.
print(
    tl_emp
    .drop(cs.temporal())
    .collect()
)
# shape: (8, 4)
# columns: id, name, salary, dept

# Drop all string columns.
print(
    tl_emp
    .drop(tp.where("string"))
    .collect()
)
# shape: (8, 3)
# columns: id, salary, start_date

# Drop columns whose names end with "date".
print(
    tl_emp
    .drop(cs.ends_with("date"))
    .collect()
)
# shape: (8, 4)
# columns: id, name, salary, dept
