'''
1. Preserving Shape & Group-wise Transform (.over)
2. Aggregation Functions (.agg in DataFrame context)
3. Grouping Data (.group_by)
'''

import numpy as np
import polars as pl

# Setup data
np.random.seed(42)
s_nums = pl.Series("nums", np.random.normal(loc=3, scale=2, size=5)).round(2)
print(s_nums)
# shape: (5,)
# Series: 'nums' [f64]
# [
# 	3.99
# 	2.72
# 	4.3
# 	6.05
# 	2.53
# ]

# =========================================================================================
# 1. Transform & .over()
# =========================================================================================
'''
Pandas uses .transform() to apply functions while preserving shape, especially with groupby().

In Polars, you use expressions inside .with_columns() and the .over() method
for group-wise transformations.

NOTE: pandas.Series can perform .groupby().transform() because it has index system.
      polars.Series does not have index system, so we have to use a DataFrame to illustrate
'''

##-----------------##
## .with_columns() ##
##-----------------##

df_date_value = pl.DataFrame({
    "Date": ["1st", "2nd", "3rd", "4th", "1st", "2nd", "3rd", "4th"],
    "Data": [5, 8, 6, 1, 50, 100, 60, 120],
})

# Apply multiple transformations preserving shape (No groupby)
df_transformed = df_date_value.with_columns(
    (pl.col("Data") + 1).alias("Data_plus_1"),
    (pl.col("Data") * 2).alias("Data_times_2")
)
print(df_transformed)
# shape: (8, 4)
# ┌──────┬──────┬─────────────┬──────────────┐
# │ Date ┆ Data ┆ Data_plus_1 ┆ Data_times_2 │
# │ ---  ┆ ---  ┆ ---         ┆ ---          │
# │ str  ┆ i64  ┆ i64         ┆ i64          │
# ╞══════╪══════╪═════════════╪══════════════╡
# │ 1st  ┆ 5    ┆ 6           ┆ 10           │
# │ 2nd  ┆ 8    ┆ 9           ┆ 16           │
# │ 3rd  ┆ 6    ┆ 7           ┆ 12           │
# │ 4th  ┆ 1    ┆ 2           ┆ 2            │
# │ 1st  ┆ 50   ┆ 51          ┆ 100          │
# │ 2nd  ┆ 100  ┆ 101         ┆ 200          │
# │ 3rd  ┆ 60   ┆ 61          ┆ 120          │
# │ 4th  ┆ 120  ┆ 121         ┆ 240          │
# └──────┴──────┴─────────────┴──────────────┘

##---------##
## .over() ##
##---------##
'''
Group-wise transform (Equivalent to pandas df.groupby("Date").transform("sum"))
The `.over()` method calculates the aggregation per group but broadcasts
the result back to the original shape of the DataFrame!
'''

df_group_transformed = df_date_value.with_columns(
    pl.col("Data").sum().over("Date").alias("Data_group_sum")
)
print(df_group_transformed)
# shape: (8, 3)
# ┌──────┬──────┬────────────────┐
# │ Date ┆ Data ┆ Data_group_sum │
# │ ---  ┆ ---  ┆ ---            │
# │ str  ┆ i64  ┆ i64            │
# ╞══════╪══════╪════════════════╡
# │ 1st  ┆ 5    ┆ 55             │
# │ 2nd  ┆ 8    ┆ 108            │
# │ 3rd  ┆ 6    ┆ 66             │
# │ 4th  ┆ 1    ┆ 121            │
# │ 1st  ┆ 50   ┆ 55             │
# │ 2nd  ┆ 100  ┆ 108            │
# │ 3rd  ┆ 60   ┆ 66             │
# │ 4th  ┆ 120  ┆ 121            │
# └──────┴──────┴────────────────┘

# =========================================================================================
# 2. .agg() & .group_by()
# =========================================================================================
'''
In Polars, aggregation and grouping are combined into a single, highly expressive
DataFrame API: .group_by().agg().
Unlike pandas, Polars does not create messy MultiIndex columns. You explicitly
name your output columns using .alias().
'''

##------------------------------##
## Simple aggregation on Series ##
##------------------------------##

# Multiple aggregations on a Series (Using pl.select)
s_agg = pl.select(
    pl.col("nums").mean(),
    pl.col("nums").std(),
    pl.col("nums").min(),
    pl.col("nums").max()
).with_columns(pl.lit(s_nums).alias("dummy")) # Just to show how to apply to series context

# Actually, simpler for a standalone series:
print(pl.select(
    pl.lit(s_nums.mean()).alias("mean"),
    pl.lit(s_nums.std()).alias("std"),
    pl.lit(s_nums.min()).alias("min"),
    pl.lit(s_nums.max()).alias("max")
))
# shape: (1, 4)
# ┌───────┬──────────┬──────┬──────┐
# │ mean  ┆ std      ┆ min  ┆ max  │
# │ ---   ┆ ---      ┆ ---  ┆ ---  │
# │ f64   ┆ f64      ┆ f64  ┆ f64  │
# ╞═══════╪══════════╪══════╪══════╡
# │ 3.918 ┆ 1.419355 ┆ 2.53 ┆ 6.05 │
# └───────┴──────────┴──────┴──────┘

##-------------------##
## .group_by().agg() ##
##-------------------##

# Groupby and Aggregation (Equivalent to pandas df.groupby("Date").agg(...))
df_agg = df_date_value.group_by("Date", maintain_order=True).agg(
    pl.col("Data").count().alias("Data_count"),
    pl.col("Data").mean().alias("Data_mean"),
    pl.col("Data").sum().alias("Data_sum"),
    # Custom aggregation function using standard expressions
    (pl.col("Data").max() - pl.col("Data").min()).alias("Data_range")
)
print(df_agg)
# shape: (4, 5)
# ┌──────┬────────────┬───────────┬──────────┬────────────┐
# │ Date ┆ Data_count ┆ Data_mean ┆ Data_sum ┆ Data_range │
# │ ---  ┆ ---        ┆ ---       ┆ ---      ┆ ---        │
# │ str  ┆ u32        ┆ f64       ┆ i64      ┆ i64        │
# ╞══════╪════════════╪═══════════╪══════════╪════════════╡
# │ 1st  ┆ 2          ┆ 27.5      ┆ 55       ┆ 45         │
# │ 2nd  ┆ 2          ┆ 54.0      ┆ 108      ┆ 92         │
# │ 3rd  ┆ 2          ┆ 33.0      ┆ 66       ┆ 54         │
# │ 4th  ┆ 2          ┆ 60.5      ┆ 121      ┆ 119        │
# └──────┴────────────┴───────────┴──────────┴────────────┘
