'''
Aggregation and reduction in Polars with a LazyFrame-first workflow.

This file is adapted from pandas workflows such as:
+ df[["Height", "Weight"]].agg("mean")
+ df[["Height", "Weight"]].agg(["mean", "median", "std"])
+ df.agg({"Height": ["min", "max", "mean"], "Weight": ["median", "var", "std"]})
+ df.agg(mean_height=("Height", "mean"), median_weight=("Weight", "median"))

Important Polars differences:
+ LazyFrame does not use pandas-style df.agg(...).
+ LazyFrame reductions are usually expressed as:
    - lf.select(... aggregation expressions ...).collect()
    - lf.mean().collect(), lf.sum().collect(), lf.min().collect(), etc.
+ Most examples in this file stay lazy until .collect().
+ Eager DataFrame is used only in the final section for APIs that are available
  as direct DataFrame aggregation methods but not as direct LazyFrame methods.

Content flow:
1. Example data with pl.scan_csv(...)
2. Single reductions with LazyFrame.select(...).collect()
3. Direct LazyFrame reduction methods
4. Multiple reductions with expression aliases
5. Dictionary-style aggregation replacement
6. Named aggregation-style output with alias(...)
7. Quantiles and custom percentile labels
8. Count, null_count, and distinct-count style summaries
9. Boolean and string reductions in lazy queries
10. Eager-only fallback for DataFrame-only aggregation helpers
11. Categorized API list
'''

from pathlib import Path

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_float_precision(3)


#---------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. Example data ----------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
'''
The pandas source file uses baseball.csv with Name, Team, Height, and Weight.
Here we load the same file lazily with pl.scan_csv(...).
'''

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

lf_baseball = pl.scan_csv(
    data_dir / "baseball.csv",
).select("Name", "Team", "Height", "Weight")

# Convert Height from inches to cm and Weight from pounds to kg.
# Cast Team to Categorical to match the pandas tutorial's category dtype.
lf_baseball = lf_baseball.with_columns(
    c.Height * 2.54,
    c.Weight * 0.453592,
    c.Team.cast(pl.Categorical),
)

print(lf_baseball.head(3).collect())
# shape: (3, 4)
# ┌─────────────────┬──────┬─────────┬────────┐
# │ Name            ┆ Team ┆ Height  ┆ Weight │
# │ ---             ┆ ---  ┆ ---     ┆ ---    │
# │ str             ┆ cat  ┆ f64     ┆ f64    │
# ╞═════════════════╪══════╪═════════╪════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 187.960 ┆ 81.647 │
# │ Paul_Bako       ┆ BAL  ┆ 187.960 ┆ 97.522 │
# │ Ramon_Hernandez ┆ BAL  ┆ 182.880 ┆ 95.254 │
# └─────────────────┴──────┴─────────┴────────┘

print(lf_baseball.collect_schema())
# Schema({'Name': String, 'Team': Categorical, 'Height': Float64, 'Weight': Float64})

# A reusable lazy subset for numeric columns.
lf_hw = lf_baseball.select("Height", "Weight")


#---------------------------------------------------------------------------------------------------------------#
#---------------------------- 2. Single reductions with LazyFrame.select(...).collect() -------------------------#
#---------------------------------------------------------------------------------------------------------------#

######################################
## Mean of selected numeric columns ##
######################################
'''
Pandas:
    df[["Height", "Weight"]].agg("mean")

Polars LazyFrame:
    Use aggregation expressions inside select(...), then collect().
'''

print(
    lf_baseball
    .select(
        c.Height.mean(),
        c.Weight.mean(),
    )
    .collect()
)
# shape: (1, 2)
# ┌─────────┬────────┐
# │ Height  ┆ Weight │
# │ ---     ┆ ---    │
# │ f64     ┆ f64    │
# ╞═════════╪════════╡
# │ 187.172 ┆ 91.330 │
# └─────────┴────────┘

########################################
## Median of selected numeric columns ##
########################################

print(
    lf_baseball
    .select(
        c.Height.median(),
        c.Weight.median(),
    )
    .collect()
)
# shape: (1, 2)
# columns: Height, Weight

###################################
## Min and max in the same query ##
###################################

print(
    lf_baseball
    .select(
        c.Height.min().alias("height_min"),
        c.Height.max().alias("height_max"),
        c.Weight.min().alias("weight_min"),
        c.Weight.max().alias("weight_max"),
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


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------- 3. Direct LazyFrame reduction methods -------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
'''
LazyFrame also has direct aggregation methods.
These are concise when you want the same reduction applied to compatible columns.

Because lf_hw contains only numeric columns, methods like mean(), median(), std(),
var(), min(), max(), sum(), and quantile() are straightforward.
'''

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


#---------------------------------------------------------------------------------------------------------------#
#------------------------------- 4. Multiple reductions with expression aliases --------------------------------#
#---------------------------------------------------------------------------------------------------------------#

######################################
## Equivalent of agg(["mean", ...]) ##
######################################
'''
Pandas returns function names as row labels.
Polars usually returns one row and uses explicit column names.

This is clearer for downstream processing:
+ height_mean
+ height_median
+ height_std
+ weight_mean
+ weight_median
+ weight_std
'''

print(
    lf_baseball
    .select(
        c.Height.mean().alias("height_mean"),
        c.Height.median().alias("height_median"),
        c.Height.std().alias("height_std"),
        c.Weight.mean().alias("weight_mean"),
        c.Weight.median().alias("weight_median"),
        c.Weight.std().alias("weight_std"),
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

###########################################
## Generate many aggregation expressions ##
###########################################

metrics = {
    "mean": lambda expr: expr.mean(),
    "median": lambda expr: expr.median(),
    "std": lambda expr: expr.std(),
}

exprs = [
    func(c(column)).alias(f"{column.lower()}_{metric}")
    for column in ["Height", "Weight"]
    for metric, func in metrics.items()
]

print(lf_baseball.select(exprs).collect())
# same idea as applying several functions to several columns


#---------------------------------------------------------------------------------------------------------------#
#-------------------------------- 5. Dictionary-style aggregation replacement ----------------------------------#
#---------------------------------------------------------------------------------------------------------------#

#############################
## Pandas dictionary style ##
#############################
'''
Pandas:
    df.agg({
        "Height": ["min", "max", "mean"],
        "Weight": ["median", "var", "std"],
    })

Polars:
    Build an explicit list of expressions.
'''

agg_spec = {
    "Height": ["min", "max", "mean"],
    "Weight": ["median", "var", "std"],
}

operation_map = {
    "min": lambda expr: expr.min(),
    "max": lambda expr: expr.max(),
    "mean": lambda expr: expr.mean(),
    "median": lambda expr: expr.median(),
    "var": lambda expr: expr.var(),
    "std": lambda expr: expr.std(),
}

exprs = [
    operation_map[operation](c(column)).alias(f"{column.lower()}_{operation}")
    for column, operations in agg_spec.items()
    for operation in operations
]

print(lf_baseball.select(exprs).collect())
# shape: (1, 6)
# columns: height_min, height_max, height_mean, weight_median, weight_var, weight_std


#----------------------------------------------------------------------------------------------------------------#
#-------------------------------- 6. Named aggregation-style output with alias ----------------------------------#
#----------------------------------------------------------------------------------------------------------------#

###########################
## Named summary columns ##
###########################
'''
Pandas named aggregation:
    df.agg(mean_height=("Height", "mean"), median_weight=("Weight", "median"))

Polars:
    Put the desired output names directly in alias(...).
'''

print(
    lf_baseball
    .select(
        c.Height.mean().alias("mean_height"),
        c.Weight.median().alias("median_weight"),
        c.Weight.std().alias("std_weight"),
    )
    .collect()
)
# shape: (1, 3)
# columns: mean_height, median_weight, std_weight

##############################
## Long summary table style ##
##############################
'''
If you prefer pandas-like rows such as mean/median/std, create one lazy query
per metric and concatenate the lazy results.
'''

lf_summary_long = pl.concat(
    [
        lf_baseball.select(
            pl.lit("mean").alias("metric"),
            c.Height.mean().alias("Height"),
            c.Weight.mean().alias("Weight"),
        ),
        lf_baseball.select(
            pl.lit("median").alias("metric"),
            c.Height.median().alias("Height"),
            c.Weight.median().alias("Weight"),
        ),
        lf_baseball.select(
            pl.lit("std").alias("metric"),
            c.Height.std().alias("Height"),
            c.Weight.std().alias("Weight"),
        ),
    ]
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


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------- 7. Quantiles and custom percentile labels ---------------------------------#
#---------------------------------------------------------------------------------------------------------------#

####################################
## Quantiles from a single column ##
####################################
'''
Pandas example:
    agg(lambda col: np.quantile(col, q=[0.25, 0.5, 0.75, 1]))

Polars:
    For a small set of quantiles, write each percentile explicitly.
'''

print(
    lf_baseball
    .select(
        c.Height.quantile(0.25).alias("height_q1"),
        c.Height.quantile(0.50).alias("height_q2"),
        c.Height.quantile(0.75).alias("height_q3"),
        c.Height.quantile(1.00).alias("height_q4"),
        c.Weight.quantile(0.25).alias("weight_q1"),
        c.Weight.quantile(0.50).alias("weight_q2"),
        c.Weight.quantile(0.75).alias("weight_q3"),
        c.Weight.quantile(1.00).alias("weight_q4"),
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

#####################################
## Quantiles as rows, still lazily ##
#####################################

quantile_rows = [
    ("Q1", 0.25),
    ("Q2", 0.50),
    ("Q3", 0.75),
    ("Q4", 1.00),
]

lf_quantiles_long = pl.concat(
    [
        lf_baseball.select(
            pl.lit(label).alias("quantile"),
            c.Height.quantile(q).alias("Height"),
            c.Weight.quantile(q).alias("Weight"),
        )
        for label, q in quantile_rows
    ]
)

print(lf_quantiles_long.collect())
# shape: (4, 3)
# ┌──────────┬─────────┬─────────┐
# │ quantile ┆ Height  ┆ Weight  │
# │ ---      ┆ ---     ┆ ---     │
# │ str      ┆ f64     ┆ f64     │
# ╞══════════╪═════════╪═════════╡
# │ Q1       ┆ 182.880 ┆ 84.368  │
# │ Q2       ┆ 187.960 ┆ 90.718  │
# │ Q3       ┆ 190.500 ┆ 97.522  │
# │ Q4       ┆ 210.820 ┆ 131.542 │
# └──────────┴─────────┴─────────┘


#----------------------------------------------------------------------------------------------------------------#
#------------------------------ 8. Count, null_count, and distinct-count style summaries ------------------------#
#----------------------------------------------------------------------------------------------------------------#

####################
## Count non-null ##
####################

print(lf_baseball.count().collect())
# non-null count for every column

#################
## Null counts ##
#################

print(lf_baseball.null_count().collect())
# null count for every column

############################
## Distinct count summary ##
############################
'''
There is no direct LazyFrame.n_unique() aggregation method in the LazyFrame
aggregation page, but distinct counts are common expression reductions.
'''

print(
    lf_baseball
    .select(
        c.Name.n_unique().alias("unique_names"),
        c.Team.n_unique().alias("unique_teams"),
        c.Height.n_unique().alias("unique_heights"),
        c.Weight.n_unique().alias("unique_weights"),
    )
    .collect()
)
# shape: (1, 4)


#----------------------------------------------------------------------------------------------------------------#
#---------------------------------- 9. Boolean and string reductions in lazy queries ----------------------------#
#----------------------------------------------------------------------------------------------------------------#

#######################
## Boolean summaries ##
#######################
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
        (c.Height > 190).sum().alias("n_height_gt_190"),
        (c.Height > 190).mean().alias("pct_height_gt_190"),
        (c.Weight > 100).any().alias("any_weight_gt_100"),
        (c.Weight > 100).all().alias("all_weight_gt_100"),
    )
    .collect()
)
# shape: (1, 4)

####################
## String summary ##
####################

print(
    lf_baseball
    .select(
        c.Team.n_unique().alias("n_teams"),
        c.Team.first().alias("first_team"),
        c.Team.last().alias("last_team"),
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


#----------------------------------------------------------------------------------------------------------------#
#---------------------- 10. Eager-only fallback for direct DataFrame aggregation helpers ------------------------#
#----------------------------------------------------------------------------------------------------------------#
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

df_hw = lf_hw.collect()

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


#----------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 11. Categorized API list ---------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#
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
