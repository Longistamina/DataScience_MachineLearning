'''
A cross-tabulation, or contingency table,
displays the frequency distribution of categorical variables.

1. Create basic cross-table with counts
2. Add margin column and margin row (sum of all values along columns and rows)
3. Normalize along rows
4. Normalize along columns
5. Normalize the whole table
6. Cross-table with more than 2 variables with `pl.concat_str`
7. Long-form table as a fall-back
'''

import numpy as np
import polars as pl
import polars.selectors as cs
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(8)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(130)

# ===================================================================
# 0. Create example LazyFrame
# ===================================================================

n_resp = 250

np.random.seed(42)
lf_survey = pl.LazyFrame(
    {
        "respondent_id": range(1, n_resp + 1),
        "gender": np.random.choice(
            ["Male", "Female", "Other"],
            size=n_resp,
            p=[0.48, 0.48, 0.04],
        ),
        "favorite_color": np.random.choice(
            ["Red", "Blue", "Green", "Yellow", "Purple"],
            size=n_resp,
        ),
        "purchase_intent": np.random.choice(
            ["Definitely", "Probably", "Maybe", "Unlikely", "Never"],
            size=n_resp,
            p=[0.15, 0.25, 0.30, 0.20, 0.10],
        ),
    }
)

print(lf_survey.head().collect())
# shape: (5, 4)
# ┌───────────────┬────────┬────────────────┬─────────────────┐
# │ respondent_id ┆ gender ┆ favorite_color ┆ purchase_intent │
# │ ---           ┆ ---    ┆ ---            ┆ ---             │
# │ i64           ┆ str    ┆ str            ┆ str             │
# ╞═══════════════╪════════╪════════════════╪═════════════════╡
# │ 1             ┆ Male   ┆ Purple         ┆ Probably        │
# │ 2             ┆ Female ┆ Purple         ┆ Unlikely        │
# │ 3             ┆ Female ┆ Red            ┆ Never           │
# │ 4             ┆ Female ┆ Green          ┆ Never           │
# │ 5             ┆ Male   ┆ Blue           ┆ Unlikely        │
# └───────────────┴────────┴────────────────┴─────────────────┘

# =========================================================================================
# 1. Create basic cross-table with counts
# =========================================================================================

print(
    lf_survey
    .group_by(['gender', 'favorite_color'])
    .agg(pl.len().alias('count')) # get the count first
    .pipe(
        lambda lf:
            lf
            .pivot( # then pivot
                on='favorite_color',
                on_columns=lf.select('favorite_color').unique().collect().to_series(),
                values='count',
                aggregate_function='first'
            )
    )
    .fill_null(value=0)
    .collect()
)
# shape: (3, 6)
# ┌────────┬──────┬───────┬────────┬─────┬────────┐
# │ gender ┆ Blue ┆ Green ┆ Purple ┆ Red ┆ Yellow │
# │ ---    ┆ ---  ┆ ---   ┆ ---    ┆ --- ┆ ---    │
# │ str    ┆ i64  ┆ i64   ┆ i64    ┆ i64 ┆ i64    │
# ╞════════╪══════╪═══════╪════════╪═════╪════════╡
# │ Female ┆ 24   ┆ 19    ┆ 31     ┆ 21  ┆ 26     │
# │ Male   ┆ 35   ┆ 15    ┆ 25     ┆ 23  ┆ 21     │
# │ Other  ┆ 1    ┆ 4     ┆ 2      ┆ 3   ┆ 0      │
# └────────┴──────┴───────┴────────┴─────┴────────┘

# =========================================================================================
# 2. Add margin column and margin row (sum of all values along columns and rows)
# =========================================================================================

print(
    lf_survey
    .group_by(['gender', 'favorite_color'])
    .agg(pl.len().alias('count')) # get the count first
    .pipe(
        lambda lf:
            lf
            .pivot( # then pivot
                on='favorite_color',
                on_columns=lf.select('favorite_color').unique().collect().to_series(),
                values='count',
                aggregate_function='first'
            )
    )
    .fill_null(value=0)
    .with_columns(pl.sum_horizontal(cs.integer()).alias('All')) # add column 'All' with horizontal sum
    .pipe(
        lambda lf:
            pl.concat( # add rown 'All' with vertical sum
                [
                    lf,
                    lf.select(
                        pl.lit('All').alias('gender'),
                        cs.integer().sum()
                    )
                ],
                how='vertical_relaxed'
            )
    )
    .collect()
)
# shape: (4, 7)
# ┌────────┬──────┬───────┬────────┬─────┬────────┬─────┐
# │ gender ┆ Blue ┆ Green ┆ Purple ┆ Red ┆ Yellow ┆ All │
# │ ---    ┆ ---  ┆ ---   ┆ ---    ┆ --- ┆ ---    ┆ --- │
# │ str    ┆ i64  ┆ i64   ┆ i64    ┆ i64 ┆ i64    ┆ i64 │
# ╞════════╪══════╪═══════╪════════╪═════╪════════╪═════╡
# │ Female ┆ 24   ┆ 19    ┆ 31     ┆ 21  ┆ 26     ┆ 121 │
# │ Male   ┆ 35   ┆ 15    ┆ 25     ┆ 23  ┆ 21     ┆ 119 │
# │ Other  ┆ 1    ┆ 4     ┆ 2      ┆ 3   ┆ 0      ┆ 10  │
# │ All    ┆ 60   ┆ 38    ┆ 58     ┆ 47  ┆ 47     ┆ 250 │
# └────────┴──────┴───────┴────────┴─────┴────────┴─────┘

# =========================================================================================
# 3. Normalize along rows
# =========================================================================================
'''Sum within rows = 1'''

print(
    lf_survey
    .group_by(['gender', 'purchase_intent'])
    .agg(pl.len().alias('count')) # get the count first
    .pipe(
        lambda lf:
            lf
            .pivot( # then pivot
                on='purchase_intent',
                on_columns=lf.select('purchase_intent').unique().collect().to_series(),
                values='count',
                aggregate_function='first'
            )
    )
    .fill_null(value=0)
    .with_columns(pl.sum_horizontal(cs.integer()).alias('All')) # add column 'All' with horizontal sum
    .with_columns(cs.numeric() / c('All')) # divide by the all column
    .collect()
)
# shape: (3, 7)
# ┌────────┬───────┬───────┬────────────┬──────────┬──────────┬───────┐
# │ gender ┆ Maybe ┆ Never ┆ Definitely ┆ Probably ┆ Unlikely ┆ All   │
# │ ---    ┆ ---   ┆ ---   ┆ ---        ┆ ---      ┆ ---      ┆ ---   │
# │ str    ┆ f64   ┆ f64   ┆ f64        ┆ f64      ┆ f64      ┆ f64   │
# ╞════════╪═══════╪═══════╪════════════╪══════════╪══════════╪═══════╡
# │ Male   ┆ 0.319 ┆ 0.109 ┆ 0.134      ┆ 0.252    ┆ 0.185    ┆ 1.000 │
# │ Female ┆ 0.289 ┆ 0.132 ┆ 0.190      ┆ 0.240    ┆ 0.149    ┆ 1.000 │
# │ Other  ┆ 0.300 ┆ 0.100 ┆ 0.100      ┆ 0.500    ┆ 0.000    ┆ 1.000 │
# └────────┴───────┴───────┴────────────┴──────────┴──────────┴───────┘
# Each row sums to approximately 1.0.

# =========================================================================================
# 4. Normalize along columns
# =========================================================================================
'''Sum within columns = 1'''

print(
    lf_survey
    .group_by(['gender', 'purchase_intent'])
    .agg(pl.len().alias('count')) # get the count first
    .pipe(
        lambda lf:
            lf
            .pivot( # then pivot
                on='purchase_intent',
                on_columns=lf.select('purchase_intent').unique().collect().to_series(),
                values='count',
                aggregate_function='first'
            )
    )
    .fill_null(value=0)
    .with_columns(cs.integer() / cs.integer().sum()) # divide each integer column by the sum of its own
    .pipe(
        lambda lf:
            pl.concat( # add rown 'All' with vertical sum
                [
                    lf,
                    lf.select(
                        pl.lit('All').alias('gender'),
                        cs.float().sum() # use the float because after normalizing, all integer columns become float
                    )
                ],
                how='vertical_relaxed'
            )
    )
    .collect()
)
# shape: (4, 6)
# ┌────────┬──────────┬──────────┬───────┬────────────┬───────┐
# │ gender ┆ Probably ┆ Unlikely ┆ Never ┆ Definitely ┆ Maybe │
# │ ---    ┆ ---      ┆ ---      ┆ ---   ┆ ---        ┆ ---   │
# │ str    ┆ f64      ┆ f64      ┆ f64   ┆ f64        ┆ f64   │
# ╞════════╪══════════╪══════════╪═══════╪════════════╪═══════╡
# │ Male   ┆ 0.469    ┆ 0.550    ┆ 0.433 ┆ 0.400      ┆ 0.500 │
# │ Female ┆ 0.453    ┆ 0.450    ┆ 0.533 ┆ 0.575      ┆ 0.461 │
# │ Other  ┆ 0.078    ┆ 0.000    ┆ 0.033 ┆ 0.025      ┆ 0.039 │
# │ All    ┆ 1.000    ┆ 1.000    ┆ 1.000 ┆ 1.000      ┆ 1.000 │
# └────────┴──────────┴──────────┴───────┴────────────┴───────┘
# Each purchase_intent column sums to approximately 1.0.

# =========================================================================================
# 5. Normalize the whole table
# =========================================================================================
'''
Divide all integer values for the grand total (sum of all cells)
'''

print(
    lf_survey
    .group_by(['gender', 'purchase_intent'])
    .agg(pl.len().alias('count')) # get the count first
    .pipe(
        lambda lf:
            lf
            .pivot( # then pivot
                on='purchase_intent',
                on_columns=lf.select('purchase_intent').unique().collect().to_series(),
                values='count',
                aggregate_function='first'
            )
    )
    .fill_null(value=0)
    .with_columns(cs.integer() / pl.sum_horizontal(cs.integer()).sum()) # divide each integer column by the grand total (sum_horizontal(cols).sum())
    .with_columns(pl.sum_horizontal(cs.float()).alias('All')) # add column 'All' with horizontal sum
    .pipe(
        lambda lf:
            pl.concat( # add row 'All' with vertical sum
                [
                    lf,
                    lf.select(
                        pl.lit('All').alias('gender'),
                        cs.float().sum() # use the float because after normalizing, all integer columns become float
                    )
                ],
                how='vertical_relaxed'
            )
    )
    .collect()
)
# shape: (4, 7)
# ┌────────┬────────────┬───────┬──────────┬───────┬──────────┬───────┐
# │ gender ┆ Definitely ┆ Maybe ┆ Unlikely ┆ Never ┆ Probably ┆ All   │
# │ ---    ┆ ---        ┆ ---   ┆ ---      ┆ ---   ┆ ---      ┆ ---   │
# │ str    ┆ f64        ┆ f64   ┆ f64      ┆ f64   ┆ f64      ┆ f64   │
# ╞════════╪════════════╪═══════╪══════════╪═══════╪══════════╪═══════╡
# │ Male   ┆ 0.064      ┆ 0.152 ┆ 0.088    ┆ 0.052 ┆ 0.120    ┆ 0.476 │
# │ Female ┆ 0.092      ┆ 0.140 ┆ 0.072    ┆ 0.064 ┆ 0.116    ┆ 0.484 │
# │ Other  ┆ 0.004      ┆ 0.012 ┆ 0.000    ┆ 0.004 ┆ 0.020    ┆ 0.040 │
# │ All    ┆ 0.160      ┆ 0.304 ┆ 0.160    ┆ 0.120 ┆ 0.256    ┆ 1.000 │
# └────────┴────────────┴───────┴──────────┴───────┴──────────┴───────┘
# The entire numeric part sums to approximately 1.0.

# =========================================================================================
# 6. Cross-table with more than 2 variables with `pl.concat_str`
# =========================================================================================
'''
To create a cross-table with all 3 variables ['gender', 'favorite_color', 'purchase_intent'],
we first concat the 'favorite_color' and 'purchase_intent' into one variable using `pl.concat_str`,
let's name it as 'fcolor_pintent', then perform 2-variable cross-tab between 'gender' and 'fcolor_pintent'.

So the general idea is concat variables[1:] into 1 variable,
then cross-tab variables[0] and variables[1:]_concat
'''

print(
    lf_survey
    .with_columns(pl.concat_str(['favorite_color', 'purchase_intent'], separator='_').alias('fcolor_pintent'))
    .group_by(['gender', 'fcolor_pintent'])
    .agg(pl.len().alias('count')) # get the count first
    .pipe(
        lambda lf:
            lf
            .pivot( # then pivot
                on='fcolor_pintent',
                on_columns=lf.select('fcolor_pintent').unique().collect().to_series(),
                values='count',
                aggregate_function='first'
            )
    )
    .fill_null(value=0)
    .collect()
)
# shape: (3, 26)
# ┌────────┬─────────────────┬─────────────────┬───────────┬───┬────────────┬──────────────┬───────────────────┬──────────────┐
# │ gender ┆ Purple_Probably ┆ Purple_Unlikely ┆ Red_Never ┆ … ┆ Blue_Never ┆ Red_Unlikely ┆ Purple_Definitely ┆ Yellow_Never │
# │ ---    ┆ ---             ┆ ---             ┆ ---       ┆   ┆ ---        ┆ ---          ┆ ---               ┆ ---          │
# │ str    ┆ u32             ┆ u32             ┆ u32       ┆   ┆ u32        ┆ u32          ┆ u32               ┆ u32          │
# ╞════════╪═════════════════╪═════════════════╪═══════════╪═══╪════════════╪══════════════╪═══════════════════╪══════════════╡
# │ Male   ┆ 7               ┆ 4               ┆ 2         ┆ … ┆ 4          ┆ 5            ┆ 5                 ┆ 3            │
# │ Female ┆ 9               ┆ 7               ┆ 4         ┆ … ┆ 1          ┆ 4            ┆ 4                 ┆ 4            │
# │ Other  ┆ 2               ┆ 0               ┆ 0         ┆ … ┆ 1          ┆ 0            ┆ 0                 ┆ 0            │
# └────────┴─────────────────┴─────────────────┴───────────┴───┴────────────┴──────────────┴───────────────────┴──────────────┘

# =========================================================================================
# 7. Long-form table as a fall-back
# =========================================================================================
'''
For statistical modeling and plotting,
long-form counts are often more useful than a very wide crosstab.
'''

print(
    lf_survey
    .group_by(["gender", "favorite_color", "purchase_intent"])
    .agg(pl.len().alias("count"))
    .sort(["gender", "favorite_color", "purchase_intent"])
    .collect()
)
# shape: (10, 4)
# ┌────────┬────────────────┬─────────────────┬───────┐
# │ gender ┆ favorite_color ┆ purchase_intent ┆ count │
# │ ---    ┆ ---            ┆ ---             ┆ ---   │
# │ str    ┆ str            ┆ str             ┆ u32   │
# ╞════════╪════════════════╪═════════════════╪═══════╡
# │ Female ┆ Blue           ┆ Definitely      ┆ 7     │
# │ Female ┆ Blue           ┆ Maybe           ┆ 7     │
# │ Female ┆ Blue           ┆ Never           ┆ 1     │
# │ Female ┆ Blue           ┆ Probably        ┆ 4     │
# │ Female ┆ Blue           ┆ Unlikely        ┆ 5     │
# │ Female ┆ Green          ┆ Definitely      ┆ 2     │
# │ Female ┆ Green          ┆ Maybe           ┆ 7     │
# │ Female ┆ Green          ┆ Never           ┆ 4     │
# │ Female ┆ Green          ┆ Probably        ┆ 4     │
# │ Female ┆ Green          ┆ Unlikely        ┆ 2     │
# └────────┴────────────────┴─────────────────┴───────┘
