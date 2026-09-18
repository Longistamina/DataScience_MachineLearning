'''
tidypyrs TibbleFrame and TibbleLazy provide `relocate` method
to move a column or columns to a new position.

1. `tl.relocate(*args)`
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

# =========================================================================================
# 1. `tl.relocate(*args)`
# =========================================================================================

print(
    tl_emp
    .relocate(f.dept, f.name, f.salary, f.id, f.start_date)
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

# =========================================================================================
# 2. `tl.relocate(*args, _before="col")`
# =========================================================================================

print(
    tl_emp
    .relocate(f.dept, f.start_date, _before="name")
    .collect()
)
# shape: (8, 5)
# ┌─────┬────────────┬────────────┬──────────┬────────┐
# │ id  ┆ dept       ┆ start_date ┆ name     ┆ salary │
# │ --- ┆ ---        ┆ ---        ┆ ---      ┆ ---    │
# │ i64 ┆ str        ┆ date       ┆ str      ┆ f64    │
# ╞═════╪════════════╪════════════╪══════════╪════════╡
# │ 1   ┆ IT         ┆ 2012-01-01 ┆ Rick     ┆ 623.30 │
# │ 2   ┆ Operations ┆ 2013-09-23 ┆ Dan      ┆ 515.20 │
# │ 3   ┆ IT         ┆ 2014-11-15 ┆ Michelle ┆ 611.00 │
# │ 4   ┆ HR         ┆ 2014-05-11 ┆ Ryan     ┆ 729.00 │
# │ 5   ┆ Finance    ┆ 2015-03-27 ┆ Gary     ┆ 843.25 │
# │ 6   ┆ IT         ┆ 2013-05-21 ┆ Nina     ┆ 578.00 │
# │ 7   ┆ Operations ┆ 2013-07-30 ┆ Simon    ┆ 632.80 │
# │ 8   ┆ Finance    ┆ 2014-06-17 ┆ Guru     ┆ 722.50 │
# └─────┴────────────┴────────────┴──────────┴────────┘
'''`dept` and `start_date` are moved before `name`'''

# =========================================================================================
# 3. `tl.relocate(*args, _after="col")`
# =========================================================================================

print(
    tl_emp
    .relocate(f.dept, f.start_date, _after="name")
    .collect()
)
# shape: (8, 5)
# ┌─────┬──────────┬────────────┬────────────┬────────┐
# │ id  ┆ name     ┆ dept       ┆ start_date ┆ salary │
# │ --- ┆ ---      ┆ ---        ┆ ---        ┆ ---    │
# │ i64 ┆ str      ┆ str        ┆ date       ┆ f64    │
# ╞═════╪══════════╪════════════╪════════════╪════════╡
# │ 1   ┆ Rick     ┆ IT         ┆ 2012-01-01 ┆ 623.30 │
# │ 2   ┆ Dan      ┆ Operations ┆ 2013-09-23 ┆ 515.20 │
# │ 3   ┆ Michelle ┆ IT         ┆ 2014-11-15 ┆ 611.00 │
# │ 4   ┆ Ryan     ┆ HR         ┆ 2014-05-11 ┆ 729.00 │
# │ 5   ┆ Gary     ┆ Finance    ┆ 2015-03-27 ┆ 843.25 │
# │ 6   ┆ Nina     ┆ IT         ┆ 2013-05-21 ┆ 578.00 │
# │ 7   ┆ Simon    ┆ Operations ┆ 2013-07-30 ┆ 632.80 │
# │ 8   ┆ Guru     ┆ Finance    ┆ 2014-06-17 ┆ 722.50 │
# └─────┴──────────┴────────────┴────────────┴────────┘
'''`dept` and `start_date` are moved after `name`'''
