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
8. Horizontal operations: sum, mean, min, max, cum_sum, all, any
'''

from pathlib import Path

import numpy as np
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

print(
    pl.concat(
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
        how="diagonal_relaxed" # use "diagonal_relaxed" because it's the safest
    )
    .collect()
)
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

print(getattr(pl.Expr, "mean"))
# <function Expr.mean at 0x7ff7999bf380>

print(pl.Expr.mean)
# <function Expr.mean at 0x7ff7999bf380>

# SHORTEN the summary query with `getattr`
metrics = ["mean", "median", "std"]
aggs = [getattr(pl.Expr, metric) for metric in metrics] # [pl.Expr.mean, pl.Expr.median, pl.Expr.std]
print(
    pl.concat(
        [
            lf_baseball.select(
                pl.lit(metric).alias("metrics"),
                c("height", "weight").pipe(agg)
            )
            for metric, agg in zip(metrics, aggs)
        ],
        how="diagonal_relaxed"
    )
    #.select(tp.Series("metrics", metrics), f.all())
    .collect()
)
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
# 8. Horizontal operations: sum, mean, min, max, cum_sum, all, any
# =========================================================================================

def random_score(length: int, seed: int):
    np.random.seed(seed)
    return np.random.uniform(0, 10 + 1e-3, length).clip(max=10.)

lf_scores = (
    pl.LazyFrame({
        "math": random_score(5, 42),
        "physics": random_score(5, 43),
        "chemistry": random_score(5, 44)
    })
    .with_row_index("id", offset=1)
    .with_columns(
        (pl.lit("student") + c("id").cast(pl.String).str.zfill(c("id").max().cast(pl.String).str.len_chars())).alias("id")
    )
)

print(lf_scores.collect())
# shape: (5, 4)
# ┌───────────┬───────┬─────────┬───────────┐
# │ id        ┆ math  ┆ physics ┆ chemistry │
# │ ---       ┆ ---   ┆ ---     ┆ ---       │
# │ str       ┆ f64   ┆ f64     ┆ f64       │
# ╞═══════════╪═══════╪═════════╪═══════════╡
# │ student01 ┆ 3.746 ┆ 1.151   ┆ 8.349     │
# │ student02 ┆ 9.508 ┆ 6.091   ┆ 1.048     │
# │ student03 ┆ 7.321 ┆ 1.334   ┆ 7.447     │
# │ student04 ┆ 5.987 ┆ 2.406   ┆ 3.605     │
# │ student05 ┆ 1.560 ┆ 3.272   ┆ 3.593     │
# └───────────┴───────┴─────────┴───────────┘

##---------------------##
## pl.sum_horizontal() ##
##---------------------##

print(
    lf_scores
    .with_columns(
        pl.sum_horizontal("math", "physics", "chemistry").alias("total_score")
    )
    .collect()
)
# shape: (5, 5)
# ┌──────────┬───────┬─────────┬───────────┬─────────────┐
# │ id       ┆ math  ┆ physics ┆ chemistry ┆ total_score │
# │ ---      ┆ ---   ┆ ---     ┆ ---       ┆ ---         │
# │ str      ┆ f64   ┆ f64     ┆ f64       ┆ f64         │
# ╞══════════╪═══════╪═════════╪═══════════╪═════════════╡
# │ student1 ┆ 3.746 ┆ 1.151   ┆ 8.349     ┆ 13.246      │
# │ student2 ┆ 9.508 ┆ 6.091   ┆ 1.048     ┆ 16.647      │
# │ student3 ┆ 7.321 ┆ 1.334   ┆ 7.447     ┆ 16.102      │
# │ student4 ┆ 5.987 ┆ 2.406   ┆ 3.605     ┆ 11.999      │
# │ student5 ┆ 1.560 ┆ 3.272   ┆ 3.593     ┆ 8.426       │
# └──────────┴───────┴─────────┴───────────┴─────────────┘

##----------------------##
## pl.mean_horizontal() ##
##----------------------##

print(
    lf_scores
    .with_columns(
        pl.mean_horizontal(pl.exclude("id")).alias("mean_score")
    )
    .collect()
)
# shape: (5, 5)
# ┌──────────┬───────┬─────────┬───────────┬────────────┐
# │ id       ┆ math  ┆ physics ┆ chemistry ┆ mean_score │
# │ ---      ┆ ---   ┆ ---     ┆ ---       ┆ ---        │
# │ str      ┆ f64   ┆ f64     ┆ f64       ┆ f64        │
# ╞══════════╪═══════╪═════════╪═══════════╪════════════╡
# │ student1 ┆ 3.746 ┆ 1.151   ┆ 8.349     ┆ 4.415      │
# │ student2 ┆ 9.508 ┆ 6.091   ┆ 1.048     ┆ 5.549      │
# │ student3 ┆ 7.321 ┆ 1.334   ┆ 7.447     ┆ 5.367      │
# │ student4 ┆ 5.987 ┆ 2.406   ┆ 3.605     ┆ 4.000      │
# │ student5 ┆ 1.560 ┆ 3.272   ┆ 3.593     ┆ 2.809      │
# └──────────┴───────┴─────────┴───────────┴────────────┘

##---------------------------------------------##
## pl.min_horizontal() and pl.max_horizontal() ##
##---------------------------------------------##

print(
    lf_scores
    .with_columns(
        pl.min_horizontal(pl.exclude("id")).alias("min_score"),
        pl.max_horizontal(c("math", "physics", "chemistry")).alias("max_score"),
    )
    .collect()
)
# shape: (5, 6)
# ┌──────────┬───────┬─────────┬───────────┬───────────┬───────────┐
# │ id       ┆ math  ┆ physics ┆ chemistry ┆ min_score ┆ max_score │
# │ ---      ┆ ---   ┆ ---     ┆ ---       ┆ ---       ┆ ---       │
# │ str      ┆ f64   ┆ f64     ┆ f64       ┆ f64       ┆ f64       │
# ╞══════════╪═══════╪═════════╪═══════════╪═══════════╪═══════════╡
# │ student1 ┆ 3.746 ┆ 1.151   ┆ 8.349     ┆ 1.151     ┆ 8.349     │
# │ student2 ┆ 9.508 ┆ 6.091   ┆ 1.048     ┆ 1.048     ┆ 9.508     │
# │ student3 ┆ 7.321 ┆ 1.334   ┆ 7.447     ┆ 1.334     ┆ 7.447     │
# │ student4 ┆ 5.987 ┆ 2.406   ┆ 3.605     ┆ 2.406     ┆ 5.987     │
# │ student5 ┆ 1.560 ┆ 3.272   ┆ 3.593     ┆ 1.560     ┆ 3.593     │
# └──────────┴───────┴─────────┴───────────┴───────────┴───────────┘

##-------------------------##
## pl.cum_sum_horizontal() ##
##-------------------------##

print(
    lf_scores
    .with_columns(
        pl.cum_sum_horizontal(pl.exclude("id")).alias("cumsum_score"),
    )
    .collect()
)
# shape: (5, 5)
# ┌──────────┬───────┬─────────┬───────────┬───────────────────────┐
# │ id       ┆ math  ┆ physics ┆ chemistry ┆ cumsum_score          │
# │ ---      ┆ ---   ┆ ---     ┆ ---       ┆ ---                   │
# │ str      ┆ f64   ┆ f64     ┆ f64       ┆ struct[3]             │
# ╞══════════╪═══════╪═════════╪═══════════╪═══════════════════════╡
# │ student1 ┆ 3.746 ┆ 1.151   ┆ 8.349     ┆ {3.746,4.896,13.246}  │
# │ student2 ┆ 9.508 ┆ 6.091   ┆ 1.048     ┆ {9.508,15.599,16.647} │
# │ student3 ┆ 7.321 ┆ 1.334   ┆ 7.447     ┆ {7.321,8.655,16.102}  │
# │ student4 ┆ 5.987 ┆ 2.406   ┆ 3.605     ┆ {5.987,8.393,11.999}  │
# │ student5 ┆ 1.560 ┆ 3.272   ┆ 3.593     ┆ {1.560,4.832,8.426}   │
# └──────────┴───────┴─────────┴───────────┴───────────────────────┘

##---------------------------------------------##
## pl.all_horizontal() and pl.any_horizontal() ##
##---------------------------------------------##

print(
    lf_scores
    .with_columns(
        pl.all_horizontal(pl.exclude("id") >= 5).alias("all_>=_5"),
        pl.any_horizontal(pl.exclude("id") >= 5).alias("any_>=_5"),
    )
    .collect()
)
# shape: (5, 6)
# ┌──────────┬───────┬─────────┬───────────┬──────────┬──────────┐
# │ id       ┆ math  ┆ physics ┆ chemistry ┆ all_>=_5 ┆ any_>=_5 │
# │ ---      ┆ ---   ┆ ---     ┆ ---       ┆ ---      ┆ ---      │
# │ str      ┆ f64   ┆ f64     ┆ f64       ┆ bool     ┆ bool     │
# ╞══════════╪═══════╪═════════╪═══════════╪══════════╪══════════╡
# │ student1 ┆ 3.746 ┆ 1.151   ┆ 8.349     ┆ false    ┆ true     │
# │ student2 ┆ 9.508 ┆ 6.091   ┆ 1.048     ┆ false    ┆ true     │
# │ student3 ┆ 7.321 ┆ 1.334   ┆ 7.447     ┆ false    ┆ true     │
# │ student4 ┆ 5.987 ┆ 2.406   ┆ 3.605     ┆ false    ┆ true     │
# │ student5 ┆ 1.560 ┆ 3.272   ┆ 3.593     ┆ false    ┆ false    │
# └──────────┴───────┴─────────┴───────────┴──────────┴──────────┘
