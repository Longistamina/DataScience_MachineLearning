'''
Summarise (aggregation) in Tidypyrs with a TibbleLazy-first workflow.

TibbleLazy reductions are usually expressed as:
    - tl.summarise(... aggregation expressions ...).collect()
    - tl.summarize(... aggregation expressions ...).collect()
    - tl.select(... aggregation expressions ...).collect()

All three of them produce the same outcomes.
But this script focus on `tl.summarise()`

Content flow:
1. Single reductions with `tl.summarise(...).collect()
2. Whole frame reduction methods: `tl.summarise(f.all().mean())`, `tl.summarise(f.all().median())`, ...
3. Multiple reductions with expression aliases: `col_expr.agg_func().alias("name")`
4. Vertical summary table using `tp.bind_rows()` and `getattr()`
5. Quantiles and custom percentile labels
6. `tl.count()`, `tl.null_count()`, and `tl.select(f.all().n_unique())`
7. Boolean and string reductions in lazy queries
'''

from pathlib import Path

import tidypyrs as tp
from tidypyrs import f

# Optional display settings for tutorial output.
tp.Config.set_tbl_rows(12)
tp.Config.set_tbl_cols(12)
tp.Config.set_float_precision(3)

# =========================================================================================
# 0. Example data
# =========================================================================================

data_dir = next(Path.home().rglob("*/DataScience_MachineLearning/data"))

tl_baseball = (
    tp.scan_csv(data_dir/"baseball.csv")
    .select(f.all().name.to_lowercase())
    .select("name", "team", "height", "weight")
    .mutate(
        f.height * 2.54, # convert height from inches to cm and weight from pounds to kg.
        f.weight * 0.453592,
        f.team.cast(tp.Categorical), # Cast Team to Categorical to match the pandas tutorial's category dtype.
    )
)

print(tl_baseball.head(3).collect())
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

print(tl_baseball.collect_schema())
# Schema({'name': String, 'team': Categorical, 'height': Float64, 'weight': Float64})

# =========================================================================================
# 1. Single reductions with `tl.summarise(...).collect()
# =========================================================================================

##----------------------------------##
## Mean of selected numeric columns ##
##----------------------------------##

print(
    tl_baseball
    .summarise(
        f.height.mean(),
        f.weight.mean(),
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
    tl_baseball
    .summarise(
        f.height.median(),
        f.weight.median(),
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
    tl_baseball
    .summarise(
        f.height.min().alias("height_min"),
        f.height.max().alias("height_max"),
        f.weight.min().alias("weight_min"),
        f.weight.max().alias("weight_max"),
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

# ==================================================================================================
# 2. Whole frame reduction methods: `tl.summarise(f.all().mean())`, `tl.summarise(f.all().median))`, ...
# ==================================================================================================
'''
TibbleLazy also has direct aggregation methods.
These are concise when you want the same reduction applied to compatible columns.

Because tl_hw contains only numeric columns, methods like mean(), median(), std(),
var(), min(), max(), sum(), and quantile() are straightforward.
'''

tl_hw = tl_baseball.select("height", "weight")

print(tl_hw.summarise(f.all().mean()).collect())
# one-row result with the mean of Height and Weight

print(tl_hw.summarise(f.all().median()).collect())
# one-row result with the median of Height and Weight

print(tl_hw.summarise(f.all().std()).collect())
# one-row result with the sample standard deviation of Height and Weight

print(tl_hw.summarise(f.all().var()).collect())
# one-row result with the variance of Height and Weight

print(tl_hw.summarise(f.all().min()).collect())
# one-row result with column minimums

print(tl_hw.summarise(f.all().max()).collect())
# one-row result with column maximums

print(tl_hw.summarise(f.all().sum()).collect())
# one-row result with column sums

print(tl_hw.summarise(f.all().quantile(0.25)).collect())
# one-row result with the 25th percentile of each numeric column

print(tl_hw.summarise(f.all().count()).collect())
# count of non-null values for each column

print(tl_hw.summarise(f.all().null_count()).collect())
# count of null values for each column

# =========================================================================================
# 3. Multiple reductions with expression aliases: `col_expr.agg_func().alias("name")`
# =========================================================================================

print(
    tl_baseball
    .summarise(
        f.height.mean().alias("height_mean"),
        f.height.median().alias("height_median"),
        f.height.std().alias("height_std"),
        f.weight.mean().alias("weight_mean"),
        f.weight.median().alias("weight_median"),
        f.weight.std().alias("weight_std"),
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
# 4. Vertical summary table using `tp.bind_rows()` and `getattr()`
# =========================================================================================
'''
If you prefer pandas-like rows such as mean/median/std, create one lazy query
per metric and concatenate the lazy results.
'''

##---------------------------##
## Explicit `tp.bind_rows()` ##
##---------------------------##

print(
    tp.bind_rows(
        [
            tl_baseball.summarise(
                tp.lit("mean").alias("metric"),
                f.height.mean().alias("height"),
                f.weight.mean().alias("weight"),
            ),
            tl_baseball.summarise(
                tp.lit("median").alias("metric"),
                f.height.median().alias("height"),
                f.weight.median().alias("weight"),
            ),
            tl_baseball.summarise(
                tp.lit("std").alias("metric"),
                f.height.std().alias("height"),
                f.weight.std().alias("weight"),
            ),
        ]
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

##--------------------------------------##
## Use `tp.bind_rows()` and `getattr()` ##
##--------------------------------------##

print(getattr(tp.Expr, "mean"))
# <function mean at 0x7f1f9b191b20>

print(tp.Expr.mean)
#  <function mean at 0x7f1f9b191b20>

# SHORTEN the summary query with `getattr`
metrics = ["mean", "median", "std"]
aggs = [getattr(tp.Expr, metric) for metric in metrics] # [tp.Expr.mean, tp.Expr.median, tp.Expr.std]
print(
    tp.bind_rows(
        [
            tl_baseball.summarise(
                tp.lit(metric).alias("metrics"),
                f("height", "weight").pipe(agg)
            )
            for metric, agg in zip(metrics, aggs)
        ]
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
    tl_baseball
    .summarise(
        f.height.quantile(0.25).alias("height_q1"),
        f.height.quantile(0.50).alias("height_q2"),
        f.height.quantile(0.75).alias("height_q3"),
        f.height.quantile(1.00).alias("height_q4"),
        f.weight.quantile(0.25).alias("weight_q1"),
        f.weight.quantile(0.50).alias("weight_q2"),
        f.weight.quantile(0.75).alias("weight_q3"),
        f.weight.quantile(1.00).alias("weight_q4"),
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

tl_quantiles_long = tp.bind_rows(
    [
        tl_baseball.summarise(
            tp.lit(label).alias("quantile"),
            f.height.quantile(q).alias("height"),
            f.weight.quantile(q).alias("weight"),
        )
        for label, q in quantile_rows
    ]
)

print(tl_quantiles_long.collect())
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
# 6. `tl.count()`, `tl.null_count()`, and `tl.summarise(f.all().n_unique())`
# =========================================================================================

##----------------##
## Count non-null ##
##----------------##

print(tl_baseball.summarise(f.all().count()).collect())
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

print(tl_baseball.summarise(f.all().null_count()).collect())
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
There is no direct TibbleLazy.n_unique() aggregation method in the TibbleLazy
aggregation page, but distinct counts are common expression reductions.
'''

print(
    tl_baseball
    .summarise(
        f.name.n_unique().alias("unique_names"),
        f.team.n_unique().alias("unique_teams"),
        f.height.n_unique().alias("unique_heights"),
        f.weight.n_unique().alias("unique_weights"),
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
    tl_baseball
    .summarise(f.all().n_unique())
    .select(f.all().name.prefix("unique_").name.suffix("s")) # Must split this into another `select` block
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
    tl_baseball
    .summarise(
        (f.height > 190).sum().alias("n_height_gt_190"),
        (f.height > 190).mean().alias("pct_height_gt_190"),
        (f.weight > 100).any().alias("any_weight_gt_100"),
        (f.weight > 100).all().alias("all_weight_gt_100"),
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
    tl_baseball
    .summarise(
        f.team.n_unique().alias("n_teams"),
        f.team.first().alias("first_team"),
        f.team.last().alias("last_team"),
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
