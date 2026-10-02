'''
`.distinct()` method helps filter out duplicate values.

If use with multiple columns, it keeps the unique combinations (rows)
'''

import numpy as np
import tidypyrs as tp
from tidypyrs import f

np.random.seed(42)
tl_duplicate = tp.TibbleLazy({
    "x": np.random.randint(10, size=(100,)),
    "y": np.random.randint(10, size=(100,)),
})

print(tl_duplicate.collect())
# shape: (100, 2)
# ┌─────┬─────┐
# │ x   ┆ y   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 6   ┆ 1   │
# │ 3   ┆ 0   │
# │ 7   ┆ 6   │
# │ 4   ┆ 6   │
# │ 6   ┆ 7   │
# │ …   ┆ …   │
# │ 9   ┆ 7   │
# │ 8   ┆ 4   │
# │ 6   ┆ 3   │
# │ 8   ┆ 1   │
# │ 7   ┆ 5   │
# └─────┴─────┘
'''
As you can see, there are some duplicate values in column 'x' (e.g., 6, 7, 4) and
'''

# ===========================================================
# 1. `tl.distinct()` on single colume
# ===========================================================

print(
    tl_duplicate
    .distinct(f.x)
    .collect()
)
# shape: (10, 1)
# ┌─────┐
# │ x   │
# │ --- │
# │ i64 │
# ╞═════╡
# │ 2   │
# │ 4   │
# │ 8   │
# │ 1   │
# │ 7   │
# │ 3   │
# │ 5   │
# │ 0   │
# │ 9   │
# │ 6   │
# └─────┘
'''Many duplicate values in column 'x' are removed, and only unique values are kept (from 0 - 9)'''

print(
    tl_duplicate
    .distinct(f.y)  # Unique combinations of 'y'
    .pull() # Extract the 'y' column as a Series
)
# shape: (10,)
# Series: 'y' [i64]
# [
# 	0
# 	8
# 	6
# 	3
# 	2
# 	7
# 	1
# 	5
# 	4
# 	9
# ]

# ===========================================================
# 2. `tl.distinct()` on multiple columns
# ===========================================================

print(
    tl_duplicate
    .distinct(f.x, f("y"))
    .collect()
)
# shape: (64, 2)
# ┌─────┬─────┐
# │ x   ┆ y   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 9   ┆ 8   │
# │ 7   ┆ 8   │
# │ 3   ┆ 3   │
# │ 5   ┆ 7   │
# │ 1   ┆ 9   │
# │ …   ┆ …   │
# │ 8   ┆ 0   │
# │ 0   ┆ 0   │
# │ 4   ┆ 7   │
# │ 4   ┆ 4   │
# │ 9   ┆ 2   │
# └─────┴─────┘
'''Keeps only unique combinations between "x" and "y"'''
