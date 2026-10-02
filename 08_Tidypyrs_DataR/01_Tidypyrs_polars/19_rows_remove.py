'''
Drop rows in Tidypyrs.

+ `tl.filter(~condition)`: keep rows that do NOT match the drop condition
+ `tl.remove(condition)`: directly remove rows that match the condition
'''

from pathlib import Path

import tidypyrs as tp
from tidypyrs import f

# Optional display settings for tutorial output.
tp.Config.set_tbl_rows(12)
tp.Config.set_tbl_cols(12)
tp.Config.set_float_precision(2)

# =========================================================================================
# Example data
# =========================================================================================

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

tl_emp = tp.scan_csv(
    data_dir / "emp.csv",
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

# =========================================================================================
# 1. `tl.filter(~condition)`: keep rows that do NOT match the drop condition
# =========================================================================================

print(
    tl_emp
    .filter(~f("salary").le(700)) # "le" means less than or equal (<=)
    .collect()
)
# shape: (3, 5)
# ┌─────┬──────┬────────┬────────────┬─────────┐
# │ id  ┆ name ┆ salary ┆ start_date ┆ dept    │
# │ --- ┆ ---  ┆ ---    ┆ ---        ┆ ---     │
# │ i64 ┆ str  ┆ f64    ┆ date       ┆ str     │
# ╞═════╪══════╪════════╪════════════╪═════════╡
# │ 4   ┆ Ryan ┆ 729.00 ┆ 2014-05-11 ┆ HR      │
# │ 5   ┆ Gary ┆ 843.25 ┆ 2015-03-27 ┆ Finance │
# │ 8   ┆ Guru ┆ 722.50 ┆ 2014-06-17 ┆ Finance │
# └─────┴──────┴────────┴────────────┴─────────┘
# Keep rows where salary > 700
# In other words, remove rows where salary <= 700

print(
    tl_emp
    .filter(~(f("salary").le(700) | f.dept.str.contains("HR")))
    .collect()
)
# shape: (2, 5)
# ┌─────┬──────┬────────┬────────────┬─────────┐
# │ id  ┆ name ┆ salary ┆ start_date ┆ dept    │
# │ --- ┆ ---  ┆ ---    ┆ ---        ┆ ---     │
# │ i64 ┆ str  ┆ f64    ┆ date       ┆ str     │
# ╞═════╪══════╪════════╪════════════╪═════════╡
# │ 5   ┆ Gary ┆ 843.25 ┆ 2015-03-27 ┆ Finance │
# │ 8   ┆ Guru ┆ 722.50 ┆ 2014-06-17 ┆ Finance │
# └─────┴──────┴────────┴────────────┴─────────┘
# Remove rows where salary <= 700, and dept is "HR"

# =========================================================================================
# 2.`tl.remove(condition)`: directly remove rows that match the condition
# =========================================================================================

print(
    tl_emp
    .remove(f.salary <= 700)
    .collect()
)
# shape: (3, 5)
# ┌─────┬──────┬────────┬────────────┬─────────┐
# │ id  ┆ name ┆ salary ┆ start_date ┆ dept    │
# │ --- ┆ ---  ┆ ---    ┆ ---        ┆ ---     │
# │ i64 ┆ str  ┆ f64    ┆ date       ┆ str     │
# ╞═════╪══════╪════════╪════════════╪═════════╡
# │ 4   ┆ Ryan ┆ 729.00 ┆ 2014-05-11 ┆ HR      │
# │ 5   ┆ Gary ┆ 843.25 ┆ 2015-03-27 ┆ Finance │
# │ 8   ┆ Guru ┆ 722.50 ┆ 2014-06-17 ┆ Finance │
# └─────┴──────┴────────┴────────────┴─────────┘

print(
    tl_emp
    .remove(f.salary.le(700) | f.dept.str.contains("HR"))
    .collect()
)
# shape: (2, 5)
# ┌─────┬──────┬────────┬────────────┬─────────┐
# │ id  ┆ name ┆ salary ┆ start_date ┆ dept    │
# │ --- ┆ ---  ┆ ---    ┆ ---        ┆ ---     │
# │ i64 ┆ str  ┆ f64    ┆ date       ┆ str     │
# ╞═════╪══════╪════════╪════════════╪═════════╡
# │ 5   ┆ Gary ┆ 843.25 ┆ 2015-03-27 ┆ Finance │
# │ 8   ┆ Guru ┆ 722.50 ┆ 2014-06-17 ┆ Finance │
# └─────┴──────┴────────┴────────────┴─────────┘
