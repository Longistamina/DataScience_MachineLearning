'''
`.unique()` method helps filter out duplicate values.

If use with multiple columns, it keeps the unique combinations (rows)
'''

import polars as pl
from polars import col as c

lf_duplicate = pl.select(
    pl.int_range(0, 10).sample(n=100, with_replacement=True, seed=42).alias("x"),
    pl.int_range(0, 10).sample(n=100, with_replacement=True, seed=43).alias("y"),
    eager=False, # return as LazyFrame
)

print(lf_duplicate.collect())
# shape: (100, 2)
# ┌─────┬─────┐
# │ x   ┆ y   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 8   ┆ 1   │
# │ 3   ┆ 5   │
# │ 9   ┆ 8   │
# │ 7   ┆ 9   │
# │ 7   ┆ 4   │
# │ …   ┆ …   │
# │ 5   ┆ 6   │
# │ 1   ┆ 0   │
# │ 7   ┆ 9   │
# │ 2   ┆ 4   │
# │ 1   ┆ 7   │
# └─────┴─────┘
'''
As you can see, there are some duplicate values in column 'x' (e.g., 6, 7, 4) and
'''

# ===========================================================
# 1. `lf.select(pl.col("x")).unique()` on single column
# ===========================================================

print(
    lf_duplicate
    .select(c("x"))
    .unique()
    .collect()
)
# shape: (10, 1)
# ┌─────┐
# │ x   │
# │ --- │
# │ i64 │
# ╞═════╡
# │ 8   │
# │ 9   │
# │ 7   │
# │ 3   │
# │ 1   │
# │ 5   │
# │ 0   │
# │ 4   │
# │ 2   │
# │ 6   │
# └─────┘
'''Many duplicate values in column 'x' are removed, and only unique values are kept (from 0 - 9)'''

print(
    lf_duplicate
    .select(c.y)  # Unique combinations of 'y'
    .unique()
    .collect().get_columns() # Extract the 'y' column as a Series
)
# [shape: (10,)
# Series: 'y' [i64]
# [
# 	7
# 	3
# 	5
# 	2
# 	0
# 	1
# 	4
# 	8
# 	6
# 	9
# ]]

# =================================================================
# 2. `lf.select(pl.col("x", "y")).unique()` on multiple columns
# =================================================================

print(
    lf_duplicate
    .select(c("x", "y"))
    .unique()
    .collect()
)
# shape: (66, 2)
# ┌─────┬─────┐
# │ x   ┆ y   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 8   ┆ 3   │
# │ 4   ┆ 7   │
# │ 1   ┆ 4   │
# │ 9   ┆ 2   │
# │ 8   ┆ 5   │
# │ …   ┆ …   │
# │ 8   ┆ 6   │
# │ 6   ┆ 0   │
# │ 4   ┆ 2   │
# │ 9   ┆ 5   │
# │ 7   ┆ 4   │
# └─────┴─────┘
'''Keeps only unique combinations between "x" and "y"'''
