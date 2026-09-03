'''
tidypyrs supports:
    + `as_tf()`: convert from polars and pandas dataframe to `TibbleFrame`
    + `as_tl()`: convert from polars and pandas dataframe to `TibbleLazy`
'''

import pandas as pd
import polars as pl
import tidypyrs as tp

pdf = pd.DataFrame({
    "x": [1, 2, 3],
    "y": [3, 2, 1]
})

plf = pl.DataFrame({
    "a": [4, 5, 6],
    "b": [6, 5, 4]
})


# ==============================================================
# 1. `as_tf()`: convert to `TibbleFrame`
# ==============================================================

# From pandas dataframe to TibbleFrame
tf = tp.as_tf(pdf)
print(tf)
# shape: (3, 2)
# ┌─────┬─────┐
# │ x   ┆ y   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 1   ┆ 3   │
# │ 2   ┆ 2   │
# │ 3   ┆ 1   │
# └─────┴─────┘

# From polars dataframe to TibbleFrame
tf = tp.as_tf(plf)
print(tf)
# shape: (3, 2)
# ┌─────┬─────┐
# │ a   ┆ b   │
# │ --- ┆ --- │
# │ i64 ┆ i64 │
# ╞═════╪═════╡
# │ 4   ┆ 6   │
# │ 5   ┆ 5   │
# │ 6   ┆ 4   │
# └─────┴─────┘


# ==============================================================
# 2. `as_tl()`: convert to `TibbleLazy`
# ==============================================================

# From pandas dataframe to TibbleLazy
tl = tp.as_tl(pdf)
print(tl)
# naive plan: (run LazyFrame.explain(optimized=True) to see the optimized plan)
# DF ["x", "y"]; PROJECT */2 COLUMNS

# From polars dataframe to TibbleLazy
tl = tp.as_tl(plf)
print(tl)
# naive plan: (run LazyFrame.explain(optimized=True) to see the optimized plan)
# DF ["a", "b"]; PROJECT */2 COLUMNS
