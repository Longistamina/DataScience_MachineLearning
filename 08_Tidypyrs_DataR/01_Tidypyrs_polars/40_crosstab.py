'''
A cross-tabulation, or contingency table,
displays the frequency distribution of categorical variables.

1. Create basic cross-table with counts
2. Add margin column and margin row with margins=True
3. Normalize along rows
4. Normalize along columns
5. Normalize the whole table
6. Cross-table with multiple column variables
7. Long-form table as a fall-back
'''

import numpy as np
import tidypyrs as tp
from tidypyrs import f

# Counts below use UInt64 in the built-in implementation.
# Output tables illustrate values; group ordering is unspecified unless arranged.
# Optional display settings for tutorial output.
tp.Config.set_tbl_rows(12)
tp.Config.set_tbl_cols(8)
tp.Config.set_float_precision(3)
tp.Config.set_tbl_width_chars(130)

# ===================================================================
# 0. Create example TibbleLazy
# ===================================================================

n_resp = 250

np.random.seed(42)
tl_survey = tp.TibbleLazy(
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

print(tl_survey.head().collect())
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
    tl_survey
    .crosstab(index="gender", columns="favorite_color")
    .arrange("gender")
    .collect()
)
# shape: (3, 6)
# ┌────────┬──────┬───────┬────────┬─────┬────────┐
# │ gender ┆ Blue ┆ Green ┆ Purple ┆ Red ┆ Yellow │
# │ ---    ┆ ---  ┆ ---   ┆ ---    ┆ --- ┆ ---    │
# │ str    ┆ u64  ┆ u64   ┆ u64    ┆ u64 ┆ u64    │
# ╞════════╪══════╪═══════╪════════╪═════╪════════╡
# │ Female ┆ 24   ┆ 19    ┆ 31     ┆ 21  ┆ 26     │
# │ Male   ┆ 35   ┆ 15    ┆ 25     ┆ 23  ┆ 21     │
# │ Other  ┆ 1    ┆ 4     ┆ 2      ┆ 3   ┆ 0      │
# └────────┴──────┴───────┴────────┴─────┴────────┘

'''
column_levels is optional. Omitting it discovers and sorts categories by
executing a query immediately; the returned result remains a TibbleLazy.
Collecting it runs the crosstab query separately and may read the source again.
Supply column_levels to avoid discovery and control the output-column order.
Only included categories contribute to counts, margins, and normalization.
'''

print(
    tl_survey
    .crosstab(
        index="gender",
        columns="favorite_color",
        column_levels=["Blue", "Green", "Purple", "Red", "Yellow"],
    )
    .arrange("gender")
    .collect()
)
# Same counts as above, with an explicit category order and no discovery query.

# =========================================================================================
# 2. Add margin column and margin row (sum of all values along columns and rows)
# =========================================================================================

print(
    tl_survey
    .crosstab(
        index="gender",
        columns="favorite_color",
        margins=True,
    )
    .collect()
)
# shape: (4, 7)
# ┌────────┬──────┬───────┬────────┬─────┬────────┬─────┐
# │ gender ┆ Blue ┆ Green ┆ Purple ┆ Red ┆ Yellow ┆ All │
# │ ---    ┆ ---  ┆ ---   ┆ ---    ┆ --- ┆ ---    ┆ --- │
# │ str    ┆ u64  ┆ u64   ┆ u64    ┆ u64 ┆ u64    ┆ u64 │
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
    tl_survey
    .crosstab(
        index="gender",
        columns="purchase_intent",
        normalize="index",
        margins=True
    )
    .arrange("gender")
    .collect()
)
# shape: (3, 6)
# gender + five purchase-intent proportion columns; no margins by default.
# Each row sums to approximately 1.0 across purchase-intent categories.
# For example: Female/Definitely = 23 / 121, Male/Definitely = 16 / 119.

# =========================================================================================
# 4. Normalize along columns
# =========================================================================================
'''Sum within columns = 1'''

print(
    tl_survey
    .crosstab(
        index="gender",
        columns="purchase_intent",
        normalize="columns",
        margins=True
    )
    .collect()
)
# shape: (3, 6)
# Each purchase-intent column sums to approximately 1.0.
# For example: Female/Definitely = 23 / 40 = 0.575.
# No total row or column is added unless margins=True.

# =========================================================================================
# 5. Normalize the whole table
# =========================================================================================
'''
Divide cell counts by the grand total. normalize=True is equivalent to "all".
With margins=True, the total row contains category shares and the total column
contains row shares. Neither margin participates in the denominator.
'''

print(
    tl_survey
    .crosstab(
        index="gender",
        columns="purchase_intent",
        normalize="all",
        margins=True,
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
# Interior cells (excluding the All row and All column) sum to approximately 1.0.
# All/All is 1.0. Margins are proportions, not additional observations.

# =========================================================================================
# 6. Cross-table with multiple column variables
# =========================================================================================
'''
Pass multiple column names directly to columns=.
The built-in method combines favorite_color and purchase_intent into flat labels
such as Blue_Definitely; no manual concat_str or pivot is needed.

Null column-category values are excluded. Combined labels use "_", so values
containing that separator may produce ambiguous labels.
'''

print(
    tl_survey
    .crosstab(
        index="gender",
        columns=["favorite_color", "purchase_intent"],
    )
    .collect()
)
# shape: (3, 26)
# gender + 25 observed color/intent combinations, sorted by their combined labels.
# For example: Blue_Definitely, Blue_Maybe, ..., Yellow_Unlikely.
# Cells are counts; missing combinations within a row receive zero.


### Multiple row variables ###
print(
    tl_survey
    .crosstab(
        index=["gender", "favorite_color"],
        columns="purchase_intent",
    )
    .arrange("gender", "favorite_color")
    .collect()
)
# One row per observed gender/color pair, with purchase intent as wide columns.

# =========================================================================================
# 7. Long-form table as a fall-back
# =========================================================================================
'''
For statistical modeling and plotting,
long-form counts are often more useful than a very wide crosstab.
'''

print(
    tl_survey
    .group_by(["gender", "favorite_color", "purchase_intent"])
    .summarise(f("respondent_id").len().alias("count"))
    .arrange("gender", "favorite_color", "purchase_intent")
    .head(10)
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

# =========================================================================================
# 8. Normalized margins and eager TibbleFrame
# =========================================================================================
'''
margins=True adds both a total row and a total column.
With normalize="index", each interior row sums to 1; the total row shows
overall category proportions. With normalize="columns", each interior column
sums to 1; the total column shows overall row proportions.

A custom margins_name must not conflict with output column names.
Choose a label distinct from real row-key values to avoid ambiguity.
'''

print(
    tl_survey
    .crosstab(
        index="gender",
        columns="purchase_intent",
        normalize="index",
        margins=True,
        margins_name="Total",
    )
    .collect()
)

print(
    tl_survey
    .crosstab(
        index="gender",
        columns="purchase_intent",
        normalize="columns",
        margins=True,
    )
    .collect()
)

# The eager API returns a TibbleFrame directly; no final collect() is needed.
tf_survey = tl_survey.collect()
print(
    tf_survey
    .crosstab(index="gender", columns="favorite_color")
    .arrange("gender")
)
