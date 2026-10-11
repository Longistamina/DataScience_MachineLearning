'''
Aggregation and reduction in Polars with a LazyFrame-first workflow.

LazyFrame reductions are usually expressed as:
    - lf.select(... aggregation expressions ...).collect()
    - lf.mean().collect(), lf.sum().collect(), lf.min().collect(), etc.

Content flow:
1. Single reductions with `lf.select(...).collect()
2. Direct LazyFrame reduction methods: `lf.mean()`, `lf.median()`, ...
3. Multiple reductions with expression aliases: `col_expr.agg_func().alias("name")`
4. Vertical summary table using `pl.concat()` and `getattr()`
5. Quantiles and custom percentile labels
6. `lf.count()`, `lf.null_count()`, and `lf.select(pl.all().n_unique())`
7. Boolean and string reductions in lazy queries
8. Eager-only fallback for DataFrame-only aggregation helpers
9. Categorized API list
'''

from pathlib import Path

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_float_precision(3)

# =========================================================================================
# 0. Example data
# =========================================================================================

data_dir = next(Path.home().rglob("*/DataScience_MachineLearning/data"))

lf_baseball = (
    pl.scan_csv(data_dir/"baseball.csv")
    .select(pl.all().name.to_lowercase())
    .select("name", "team", "height", "weight")
    .with_columns(
        c.height * 2.54, # convert height from inches to cm and weight from pounds to kg.
        c.weight * 0.453592,
        c.team.cast(pl.Categorical), # Cast Team to Categorical to match the pandas tutorial's category dtype.
    )
)

print(lf_baseball.head(3).collect())
# shape: (3, 4)
# ┌─────────────────┬──────┬─────────┬────────┐
# │ name            ┆ team ┆ height  ┆ weight │
# │ ---             ┆ ---  ┆ ---     ┆ ---    │
# │ str             ┆ cat  ┆ f6ount
# ╞═════════════════╪══════╪═════════╪════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 187.960 ┆ 81.647 │
# │ Paul_Bako       ┆ BAL  ┆ 187.960 ┆ 97.522 │
# │ Ramon_Hernandez ┆ BAL  ┆ 182.880 ┆ 95.254 │
# └─────────────────┴──────┴─────────┴────────┘

print(lf_baseball.collect_schema())
# Schema({'name': String, 'team': Categorical, 'height': Float64, 'weight': Float64})

# =========================================================================================
# 1. Single reductions with `lf.select(...).collect()
# =========================================================================================

##----------------------------------##
## Mean of selected numeric columns ##
##----------------------------------##

print(
    lf_baseball
    .select(
        c.height.mean(),
        c.weight.mean(),
    )
    .collect()
)
# shape: (1, 2)
# ┌─────────┬────────┐
# │ height  ┆ weight │
# │ ---     ┆ ---    │
# │ f64     ┆ f64    │
# ╞═════════╪════════╡
# │ 187.172 ┆ 91.330 │
# └─────────┴────────┘

##------------------------------------##
## Median of selected numeric columns ##
##------------------------------------##

print(
    lf_baseball
    .select(
        c.height.median(),
        c.weight.median(),
    )
    .collect()
)
# shape: (1, 2)
# ┌─────────┬────────┐
# │ height  ┆ weight │
# │ ---     ┆ ---    │
# │ f64     ┆ f64    │
# ╞═════════╪════════╡
# │ 187.960 ┆ 90.718 │
# └─────────┴────────┘

##-------------------------------##
## Min and max in the same query ##
##-------------------------------##

print(
    lf_baseball
    .select(
        c.height.min().alias("height_min"),
        c.height.max().alias("height_max"),
        c.weight.min().alias("weight_min"),
        c.weight.max().alias("weight_max"),
    )
    .collect()
)
# shape: (1, 4)
# ┌────────────┬────────────┬────────────┬────────────┐
# │ height_min ┆ height_max ┆ weight_min ┆ weight_max │
# │ ---        ┆ ---        ┆ ---        ┆ ---        │
# │ f64        ┆ f64        ┆ f64        ┆ f64        │
# ╞════════════╪════════════╪════════════╪════════════╡
# │ 170.180    ┆ 210.820    ┆ 68.039     ┆ 131.542    │
# └────────────┴────────────┴────────────┴────────────┘

# =========================================================================================
# 2. Direct LazyFrame reduction methods: `lf.mean()`, `lf.median()`, ...
# =========================================================================================
'''
LazyFrame also has direct aggregation methods.
These are concise when you want the same reduction applied to compatible columns.

Because lf_hw contains only numeric columns, methods like mean(), median(), std(),
var(), min(), max(), sum(), and quantile() are straightforward.
'''

lf_hw = lf_baseball.select("height", "weight")

print(lf_hw.mean().collect())
# one-row result with the mean of Height and Weight

print(lf_hw.median().collect())
# one-row result with the median of Height and Weight

print(lf_hw.std().collect())
# one-row result with the sample standard deviation of Height and Weight

print(lf_hw.var().collect())
# one-row result with the variance of Height and Weight

print(lf_hw.min().collect())
# one-row result with column minimums

print(lf_hw.max().collect())
# one-row result with column maximums

print(lf_hw.sum().collect())
# one-row result with column sums

print(lf_hw.quantile(0.25).collect())
# one-row result with the 25th percentile of each numeric column

print(lf_baseball.count().collect())
# count of non-null values for each column

print(lf_baseball.null_count().collect())
# count of null values for each column

# =========================================================================================
# 3. Multiple reductions with expression aliases: `col_expr.agg_func().alias("name")`
# =========================================================================================

print(
    lf_baseball
    .select(
        c.height.mean().alias("height_mean"),
        c.height.median().alias("height_median"),
        c.height.std().alias("height_std"),
        c.weight.mean().alias("weight_mean"),
        c.weight.median().alias("weight_median"),
        c.weight.std().alias("weight_std"),
    )
    .collect()
)
# shape: (1, 6)
# ┌─────────────┬───────────────┬────────────┬─────────────┬───────────────┬────────────┐
# │ height_mean ┆ height_median ┆ height_std ┆ weight_mean ┆ weight_median ┆ weight_std │
# │ ---         ┆ ---           ┆ ---        ┆ ---         ┆ ---           ┆ ---        │
# │ f64         ┆ f64           ┆ f64        ┆ f64         ┆ f64           ┆ f64        │
# ╞═════════════╪═══════════════╪════════════╪═════════════╪═══════════════╪════════════╡
# │ 187.172     ┆ 187.960       ┆ 5.877      ┆ 91.330      ┆ 90.718        ┆ 9.445      │
# └─────────────┴───────────────┴────────────┴─────────────┴───────────────┴────────────┘

# =========================================================================================
# 4. Vertical summary table using `pl.concat()` and `getattr()`
# =========================================================================================
'''
If you prefer pandas-like rows such as mean/median/std, create one lazy query
per metric and concatenate the lazy results.
'''

##------------------------##
## Explicit `pl.concat()` ##
##------------------------##

lf_summary_long = pl.concat(
    [
        lf_baseball.select(
            pl.lit("mean").alias("metric"),
            c.height.mean().alias("height"),
            c.weight.mean().alias("weight"),
        ),
        lf_baseball.select(
            pl.lit("median").alias("metric"),
            c.height.median().alias("height"),
            c.weight.median().alias("weight"),
        ),
        lf_baseball.select(
            pl.lit("std").alias("metric"),
            c.height.std().alias("height"),
            c.weight.std().alias("weight"),
        ),
    ],
    how="vertical_relaxed" # use "vertical_relaxed" because it's safer
)

print(lf_summary_long.collect())
# shape: (3, 3)
# ┌────────┬─────────┬────────┐
# │ metric ┆ Height  ┆ Weight │
# │ ---    ┆ ---     ┆ ---    │
# │ str    ┆ f64     ┆ f64    │
# ╞════════╪═════════╪════════╡
# │ mean   ┆ 187.172 ┆ 91.330 │
# │ median ┆ 187.960 ┆ 90.718 │
# │ std    ┆ 5.877   ┆ 9.445  │
# └────────┴─────────┴────────┘

##-----------------------------------##
## Use `pl.concat()` and `getattr()` ##
##-----------------------------------##

print(getattr(c("height"), "mean"))
# <bound method Expr.mean of <Expr ['col("height")'] at 0x7F41CDFC2300>>

print(
    getattr(c("height"), "mean")()
)
# col("height").mean()

print(
    getattr(c("height", "weight"), "median")()
)
# cs.by_name('height', 'weight', require_all=true).median()

print(
    getattr(lf_baseball.select(c.height), "std")()
)
# lf_baseball.select(c.height).std()

# SHORTEN the summary query with `getattr`
metrics = ["mean", "median", "std"]
lf_summary_short = (
    pl.concat(
        [
            lf_baseball.select(getattr(c("height", "weight"), metric)()) # or `getattr(lf_baseball.select("height", "weight"), metric)()`
            for metric in metrics
        ],
        how="vertical_relaxed"
    )
    .select(pl.Series("metrics", metrics), pl.all())
)
print(lf_summary_short.collect())
# shape: (3, 3)
# ┌─────────┬─────────┬────────┐
# │ metrics ┆ height  ┆ weight │
# │ ---     ┆ ---     ┆ ---    │
# │ str     ┆ f64     ┆ f64    │
# ╞═════════╪═════════╪════════╡
# │ mean    ┆ 187.172 ┆ 91.330 │
# │ median  ┆ 187.960 ┆ 90.718 │
# │ std     ┆ 5.877   ┆ 9.445  │
# └─────────┴─────────┴────────┘

# =========================================================================================
# 5. Quantiles and custom percentile labels
# =========================================================================================

##--------------------------------##
## Quantiles from a single column ##
##--------------------------------##

print(
    lf_baseball
    .select(
        c.height.quantile(0.25).alias("height_q1"),
        c.height.quantile(0.50).alias("height_q2"),
        c.height.quantile(0.75).alias("height_q3"),
        c.height.quantile(1.00).alias("height_q4"),
        c.weight.quantile(0.25).alias("weight_q1"),
        c.weight.quantile(0.50).alias("weight_q2"),
        c.weight.quantile(0.75).alias("weight_q3"),
        c.weight.quantile(1.00).alias("weight_q4"),
    )
    .collect()
)
# shape: (1, 8)
# ┌───────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┐
# │ height_q1 ┆ height_q2 ┆ height_q3 ┆ height_q4 ┆ weight_q1 ┆ weight_q2 ┆ weight_q3 ┆ weight_q4 │
# │ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       │
# │ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       │
# ╞═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╡
# │ 182.880   ┆ 187.960   ┆ 190.500   ┆ 210.820   ┆ 84.368    ┆ 90.718    ┆ 97.522    ┆ 131.542   │
# └───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┘

##---------------------------------##
## Quantiles as rows, still lazily ##
##---------------------------------##

quantile_rows = [
    ("q1", 0.25),
    ("q2", 0.50),
    ("q3", 0.75),
    ("q4", 1.00),
]

lf_quantiles_long = pl.concat(
    [
        lf_baseball.select(
            pl.lit(label).alias("quantile"),
            c.height.quantile(q).alias("height"),
            c.weight.quantile(q).alias("weight"),
        )
        for label, q in quantile_rows
    ],
    how="vertical"
)

print(lf_quantiles_long.collect())
# shape: (4, 3)
# ┌──────────┬─────────┬─────────┐
# │ quantile ┆ height  ┆ weight  │
# │ ---      ┆ ---     ┆ ---     │
# │ str      ┆ f64     ┆ f64     │
# ╞══════════╪═════════╪═════════╡
# │ q1       ┆ 182.880 ┆ 84.368  │
# │ q2       ┆ 187.960 ┆ 90.718  │
# │ q3       ┆ 190.500 ┆ 97.522  │
# │ q4       ┆ 210.820 ┆ 131.542 │
# └──────────┴─────────┴─────────┘

# =========================================================================================
# 6. `lf.count()`, `lf.null_count()`, and `lf.select(pl.all().n_unique())`
# =========================================================================================

##----------------##
## Count non-null ##
##----------------##

print(lf_baseball.count().collect())
# non-null count for every column
# shape: (1, 4)
# ┌──────┬──────┬────────┬────────┐
# │ name ┆ team ┆ height ┆ weight │
# │ ---  ┆ ---  ┆ ---    ┆ ---    │
# │ u32  ┆ u32  ┆ u32    ┆ u32    │
# ╞══════╪══════╪════════╪════════╡
# │ 1015 ┆ 1015 ┆ 1015   ┆ 1015   │
# └──────┴──────┴────────┴────────┘

##-------------##
## Null counts ##
##-------------##

print(lf_baseball.null_count().collect())
# null count for every column
# shape: (1, 4)
# ┌──────┬──────┬────────┬────────┐
# │ name ┆ team ┆ height ┆ weight │
# │ ---  ┆ ---  ┆ ---    ┆ ---    │
# │ u32  ┆ u32  ┆ u32    ┆ u32    │
# ╞══════╪══════╪════════╪════════╡
# │ 0    ┆ 0    ┆ 0      ┆ 0      │
# └──────┴──────┴────────┴────────┘

##--------------##
## `n_unique()` ##
##--------------##
'''
There is no direct LazyFrame.n_unique() aggregation method in the LazyFrame
aggregation page, but distinct counts are common expression reductions.
'''

print(
    lf_baseball
    .select(
        c.name.n_unique().alias("unique_names"),
        c.team.n_unique().alias("unique_teams"),
        c.height.n_unique().alias("unique_heights"),
        c.weight.n_unique().alias("unique_weights"),
    )
    .collect()
)
# shape: (1, 4)
# ┌──────────────┬──────────────┬────────────────┬────────────────┐
# │ unique_names ┆ unique_teams ┆ unique_heights ┆ unique_weights │
# │ ---          ┆ ---          ┆ ---            ┆ ---            │
# │ u32          ┆ u32          ┆ u32            ┆ u32            │
# ╞══════════════╪══════════════╪════════════════╪════════════════╡
# │ 1013         ┆ 30           ┆ 17             ┆ 88             │
# └──────────────┴──────────────┴────────────────┴────────────────┘
# shape: (1, 4)

# Shorter version
print(
    lf_baseball
    .select(pl.all().n_unique())
    .select(pl.all().name.prefix("unique_").name.suffix("s")) # Must split this into another `select` block
    .collect()
)
# shape: (1, 4)
# ┌──────────────┬──────────────┬────────────────┬────────────────┐
# │ unique_names ┆ unique_teams ┆ unique_heights ┆ unique_weights │
# │ ---          ┆ ---          ┆ ---            ┆ ---            │
# │ u32          ┆ u32          ┆ u32            ┆ u32            │
# ╞══════════════╪══════════════╪════════════════╪════════════════╡
# │ 1013         ┆ 30           ┆ 17             ┆ 88             │
# └──────────────┴──────────────┴────────────────┴────────────────┘

# =========================================================================================
# 7. Boolean and string reductions in lazy queries
# =========================================================================================

##-------------------##
## Boolean summaries ##
##-------------------##
'''
Boolean conditions can be aggregated just like boolean columns:
+ sum() counts True values.
+ mean() returns the proportion of True values.
+ all() checks whether all rows satisfy the condition.
+ any() checks whether at least one row satisfies the condition.
'''

print(
    lf_baseball
    .select(
        (c.height > 190).sum().alias("n_height_gt_190"),
        (c.height > 190).mean().alias("pct_height_gt_190"),
        (c.weight > 100).any().alias("any_weight_gt_100"),
        (c.weight > 100).all().alias("all_weight_gt_100"),
    )
    .collect()
)
# shape: (1, 4)
# ┌─────────────────┬───────────────────┬───────────────────┬───────────────────┐
# │ n_height_gt_190 ┆ pct_height_gt_190 ┆ any_weight_gt_100 ┆ all_weight_gt_100 │
# │ ---             ┆ ---               ┆ ---               ┆ ---               │
# │ u32             ┆ f64               ┆ bool              ┆ bool              │
# ╞═════════════════╪═══════════════════╪═══════════════════╪═══════════════════╡
# │ 362             ┆ 0.357             ┆ true              ┆ false             │
# └─────────────────┴───────────────────┴───────────────────┴───────────────────┘

##----------------##
## String summary ##
##----------------##

print(
    lf_baseball
    .select(
        c.team.n_unique().alias("n_teams"),
        c.team.first().alias("first_team"),
        c.team.last().alias("last_team"),
    )
    .collect()
)
# shape: (1, 3)
# ┌─────────┬────────────┬───────────┐
# │ n_teams ┆ first_team ┆ last_team │
# │ ---     ┆ ---        ┆ ---       │
# │ u32     ┆ cat        ┆ cat       │
# ╞═════════╪════════════╪═══════════╡
# │ 30      ┆ BAL        ┆ STL       │
# └─────────┴────────────┴───────────┘

# =========================================================================================
# 10. Eager-only fallback for direct DataFrame aggregation helpers
# =========================================================================================
'''
Most of this file stays lazy. This section intentionally collects to an eager
DataFrame because some direct aggregation helpers are available as DataFrame
methods but not as direct LazyFrame aggregation methods.

Examples include:
+ product()
+ sum_horizontal()
+ mean_horizontal()
+ min_horizontal()
+ max_horizontal()

If you are already working lazily and do not need these direct DataFrame methods,
you can often express similar logic with expressions. This section exists only
to document the DataFrame-only API difference.
'''

df_hw = lf_baseball.select("height", "weight").collect()

print(df_hw.product())
# direct DataFrame product over columns

print(df_hw.sum_horizontal())
# row-wise Height + Weight

print(df_hw.mean_horizontal())
# row-wise mean of Height and Weight

print(df_hw.min_horizontal())
# row-wise min of Height and Weight

print(df_hw.max_horizontal())
# row-wise max of Height and Weight

# Put horizontal reductions back into a DataFrame for easier viewing.
df_hw_horizontal = df_hw.with_columns(
    row_sum=df_hw.sum_horizontal(),
    row_mean=df_hw.mean_horizontal(),
    row_min=df_hw.min_horizontal(),
    row_max=df_hw.max_horizontal(),
)

print(df_hw_horizontal.head(5))
# shape: (5, 6)
# ┌─────────┬────────┬─────────┬──────────┬─────────┬─────────┐
# │ Height  ┆ Weight ┆ row_sum ┆ row_mean ┆ row_min ┆ row_max │
# │ ---     ┆ ---    ┆ ---     ┆ ---      ┆ ---     ┆ ---     │
# │ f64     ┆ f64    ┆ f64     ┆ f64      ┆ f64     ┆ f64     │
# ╞═════════╪════════╪═════════╪══════════╪═════════╪═════════╡
# │ 187.960 ┆ 81.647 ┆ 269.607 ┆ 134.803  ┆ 81.647  ┆ 187.960 │
# │ 187.960 ┆ 97.522 ┆ 285.482 ┆ 142.741  ┆ 97.522  ┆ 187.960 │
# │ 182.880 ┆ 95.254 ┆ 278.134 ┆ 139.067  ┆ 95.254  ┆ 182.880 │
# │ 182.880 ┆ 95.254 ┆ 278.134 ┆ 139.067  ┆ 95.254  ┆ 182.880 │
# │ 185.420 ┆ 85.275 ┆ 270.695 ┆ 135.348  ┆ 85.275  ┆ 185.420 │
# └─────────┴────────┴─────────┴──────────┴─────────┴─────────┘

# =========================================================================================
# 11. Categorized API list
# =========================================================================================
'''
A. LazyFrame aggregation APIs

These are direct LazyFrame aggregation/reduction methods:
+ lf.count()
+ lf.max()
+ lf.mean()
+ lf.median()
+ lf.min()
+ lf.null_count()
+ lf.quantile(...)
+ lf.std()
+ lf.sum()
+ lf.var()

B. Common expression reductions used inside LazyFrame.select(...)

These are not direct LazyFrame methods, but they are the main way to write
flexible lazy aggregations:
+ c.column.mean()
+ c.column.median()
+ c.column.std()
+ c.column.var()
+ c.column.min()
+ c.column.max()
+ c.column.sum()
+ c.column.quantile(...)
+ c.column.count()
+ c.column.n_unique()
+ c.column.first()
+ c.column.last()
+ boolean_expr.any()
+ boolean_expr.all()

C. Direct eager DataFrame aggregation APIs

The DataFrame aggregation page includes these direct methods:
+ df.count()
+ df.max()
+ df.max_horizontal()
+ df.mean()
+ df.mean_horizontal()
+ df.median()
+ df.min()
+ df.min_horizontal()
+ df.product()
+ df.quantile(...)
+ df.std()
+ df.sum()
+ df.sum_horizontal()
+ df.var()

D. Teaching summary

+ Use LazyFrame scan + lazy select expressions for most aggregation lessons.
+ Use .collect() only when showing output.
+ Use direct eager DataFrame helpers only when the API exists only there or when
  row-wise horizontal reductions are the lesson topic.
'''
