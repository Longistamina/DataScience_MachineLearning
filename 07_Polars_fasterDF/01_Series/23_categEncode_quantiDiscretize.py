'''
In Polars, categorical encoding and numerical discretization are handled with
strongly typed Series/DataFrame operations.

Pandas -> Polars equivalents:
1. pd.factorize(s)
   + Fast Polars equivalent: s.cast(pl.Categorical).to_physical()
   + Stable first-appearance codes: build a lookup table from s.unique(maintain_order=True)

2. pd.get_dummies(s) / pd.get_dummies(df)
   + Series: s.to_dummies()
   + DataFrame: df.to_dummies(columns=[...])

3. pd.cut(x, bins=[...])
   + Series: s.cut(breaks=[...], labels=[...])
   + DataFrame expression: pl.col("x").cut(...)

4. pd.cut(x, bins=3)
   + Polars does NOT automatically create equal-width bins from an integer.
   + Calculate the internal breakpoints yourself, then call .cut().

5. pd.qcut(x, q=4)
   + Series: s.qcut(4, labels=[...])
   + DataFrame expression: pl.col("x").qcut(4, labels=[...])

Important differences from pandas:
1. Polars has no custom row index; operations align by row position or by joins.
2. .to_dummies() returns UInt8 indicator columns, not boolean columns.
3. .cut() takes INTERNAL breakpoints, not the full list of bin edges.
   For example, pandas bins=[0, 2, 4, 6] corresponds most closely to
   Polars breaks=[2, 4], with separate logic if you need values outside 0..6 to become null.
4. .cut() returns Enum by default; .qcut() returns Categorical by default.
5. .cut() and .qcut() are currently documented as unstable Polars features.

######################################################
1. Categorical Encoding
   + Factorize-style integer codes
   + One-hot / dummy encoding
   + DataFrame dummy encoding

2. Binning and Discretization
   + .cut() with custom breakpoints
   + .cut() with manually calculated equal-width breakpoints
   + .cut(include_breaks=True)
   + left_closed=True
   + .qcut() with quantile bins
   + .qcut(include_breaks=True)
   + Duplicate quantile handling

3. Real applications
'''

import numpy as np
import polars as pl


#---------------------------------------------------------------------------------------------------#
#------------------------------------ 1. Categorical Encoding --------------------------------------#
#---------------------------------------------------------------------------------------------------#
'''
Categorical Encoding is the process of converting categorical variables into numerical representations.
This is useful for machine learning algorithms that require numerical input.

In Polars, there are two common choices:
1. Integer codes: cast to pl.Categorical, then use .to_physical().
2. One-hot columns: use .to_dummies() on a Series or DataFrame.
'''

s_gender = pl.Series("gender", ["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"])

print(s_gender)
# shape: (10,)
# Series: 'gender' [str]
# [
# 	"M"
# 	"M"
# 	"F"
# 	"M"
# 	"LGBTQ"
# 	"F"
# 	"M"
# 	"F"
# 	"LGBTQ"
# 	"M"
# ]

#######################################
##  Factorize-style with Categorical ##
#######################################
'''
Pandas:
    pd.factorize(s_gender)

Polars fast equivalent:
    s_gender.cast(pl.Categorical).to_physical()

The result is an integer representation of the categorical values.

IMPORTANT:
Polars docs warn that physical representations are implementation details and are not
promised to be stable forever. This is fine for many internal/temporary workflows, but
if you need pandas-like stable first-appearance codes, see the next section.
'''

s_gender_cat = s_gender.cast(pl.Categorical)

print(s_gender_cat)
# shape: (10,)
# Series: 'gender' [cat]
# [
# 	"M"
# 	"M"
# 	"F"
# 	"M"
# 	"LGBTQ"
# 	"F"
# 	"M"
# 	"F"
# 	"LGBTQ"
# 	"M"
# ]

# Integer physical codes for the categorical Series
s_gender_codes = s_gender_cat.to_physical()
print(s_gender_codes)
# shape: (10,)
# Series: 'gender' [u32]
# [
# 	0
# 	0
# 	1
# 	0
# 	2
# 	1
# 	0
# 	1
# 	2
# 	0
# ]

# The categories stored in the categorical mapping
categories = s_gender_cat.cat.get_categories()
print(categories)
# shape: (3,)
# Series: 'gender' [str]
# [
# 	"M"
# 	"F"
# 	"LGBTQ"
# ]

# Assign the two results to separate variables, similar to pandas factorize output
codes = s_gender_cat.to_physical()
uniques = s_gender_cat.cat.get_categories()

print(codes)
print(uniques)

#########################################################
##  Stable pandas-like factorize with first-appearance ##
#########################################################
'''
Pandas pd.factorize() assigns integers in the order of first appearance.

To make this behavior explicit in Polars, create a lookup table from
unique(maintain_order=True), then join it back to the original data.

This is a DataFrame-based solution because joins are the idiomatic way to map values
while keeping an explicit, inspectable category-code table.
'''

categories_in_order = s_gender.unique(maintain_order=True)
lookup = pl.DataFrame(
    {
        "gender": categories_in_order,
        "gender_code": list(range(len(categories_in_order))),
    }
)

print(lookup)
# shape: (3, 2)
# ┌────────┬─────────────┐
# │ gender ┆ gender_code │
# │ ---    ┆ ---         │
# │ str    ┆ i64         │
# ╞════════╪═════════════╡
# │ M      ┆ 0           │
# │ F      ┆ 1           │
# │ LGBTQ  ┆ 2           │
# └────────┴─────────────┘

factorized_df = s_gender.to_frame().join(lookup, on="gender", how="left")
print(factorized_df)
# shape: (10, 2)
# ┌────────┬─────────────┐
# │ gender ┆ gender_code │
# │ ---    ┆ ---         │
# │ str    ┆ i64         │
# ╞════════╪═════════════╡
# │ M      ┆ 0           │
# │ M      ┆ 0           │
# │ F      ┆ 1           │
# │ M      ┆ 0           │
# │ LGBTQ  ┆ 2           │
# │ F      ┆ 1           │
# │ M      ┆ 0           │
# │ F      ┆ 1           │
# │ LGBTQ  ┆ 2           │
# │ M      ┆ 0           │
# └────────┴─────────────┘


#########################################
##            .to_dummies()            ##
#########################################
'''
Pandas:
    pd.get_dummies(s_gender, prefix="gender")

Polars:
    s_gender.to_dummies()

.to_dummies() creates a DataFrame with one UInt8 indicator column for each category.
Each column contains 1 if the row belongs to that category, otherwise 0.
'''

#-----------------
## Without dropping the first category
#-----------------

s_gender_dummies = s_gender.to_dummies()
print(s_gender_dummies)
# shape: (10, 3)
# ┌──────────┬──────────────┬──────────┐
# │ gender_F ┆ gender_LGBTQ ┆ gender_M │
# │ ---      ┆ ---          ┆ ---      │
# │ u8       ┆ u8           ┆ u8       │
# ╞══════════╪══════════════╪══════════╡
# │ 0        ┆ 0            ┆ 1        │
# │ 0        ┆ 0            ┆ 1        │
# │ 1        ┆ 0            ┆ 0        │
# │ 0        ┆ 0            ┆ 1        │
# │ 0        ┆ 1            ┆ 0        │
# │ 1        ┆ 0            ┆ 0        │
# │ 0        ┆ 0            ┆ 1        │
# │ 1        ┆ 0            ┆ 0        │
# │ 0        ┆ 1            ┆ 0        │
# │ 0        ┆ 0            ┆ 1        │
# └──────────┴──────────────┴──────────┘

# You can change the separator used in generated column names
print(s_gender.to_dummies(separator="__"))
# Columns: gender__F, gender__LGBTQ, gender__M

#-----------------
## With dropping the first category
#-----------------
'''
If we have n categories, we often only need n-1 dummy columns.
The omitted category can be inferred when all dummy columns are 0.

This is commonly used to avoid perfect multicollinearity in linear models.
'''

s_gender_dummies_drop = s_gender.to_dummies(drop_first=True)
print(s_gender_dummies_drop)
# shape: (10, 2)
# ┌──────────────┬──────────┐
# │ gender_LGBTQ ┆ gender_M │
# │ ---          ┆ ---      │
# │ u8           ┆ u8       │
# ╞══════════════╪══════════╡
# │ 0            ┆ 1        │
# │ 0            ┆ 1        │
# │ 0            ┆ 0        │  <- inferred as F
# │ 0            ┆ 1        │
# │ 1            ┆ 0        │
# │ 0            ┆ 0        │  <- inferred as F
# │ 0            ┆ 1        │
# │ 0            ┆ 0        │  <- inferred as F
# │ 1            ┆ 0        │
# │ 0            ┆ 1        │
# └──────────────┴──────────┘

'''
Rows where gender_LGBTQ = 0 and gender_M = 0 are the dropped category.
In this example, the dropped category is F.
'''

################################################
##        DataFrame-level dummy encoding      ##
################################################
'''
For real modeling datasets, you usually work with DataFrames rather than isolated Series.
Use df.to_dummies(columns=[...]) to one-hot encode selected columns only.
'''

df_people = pl.DataFrame(
    {
        "gender": ["M", "M", "F", "M", "LGBTQ", "F"],
        "city": ["Seoul", "Busan", "Seoul", "Jeju", "Busan", "Seoul"],
        "age": [29, 35, 42, 31, 28, 39],
    }
)

print(df_people)
# shape: (6, 3)
# ┌────────┬───────┬─────┐
# │ gender ┆ city  ┆ age │
# │ ---    ┆ ---   ┆ --- │
# │ str    ┆ str   ┆ i64 │
# ╞════════╪═══════╪═════╡
# │ M      ┆ Seoul ┆ 29  │
# │ M      ┆ Busan ┆ 35  │
# │ F      ┆ Seoul ┆ 42  │
# │ M      ┆ Jeju  ┆ 31  │
# │ LGBTQ  ┆ Busan ┆ 28  │
# │ F      ┆ Seoul ┆ 39  │
# └────────┴───────┴─────┘

print(df_people.to_dummies(columns=["gender", "city"]))
# shape: (6, 7)
# ┌──────────┬──────────────┬──────────┬────────────┬───────────┬────────────┬─────┐
# │ gender_F ┆ gender_LGBTQ ┆ gender_M ┆ city_Busan ┆ city_Jeju ┆ city_Seoul ┆ age │
# │ ---      ┆ ---          ┆ ---      ┆ ---        ┆ ---       ┆ ---        ┆ --- │
# │ u8       ┆ u8           ┆ u8       ┆ u8         ┆ u8        ┆ u8         ┆ i64 │
# ╞══════════╪══════════════╪══════════╪════════════╪═══════════╪════════════╪═════╡
# │ 0        ┆ 0            ┆ 1        ┆ 0          ┆ 0         ┆ 1          ┆ 29  │
# │ 0        ┆ 0            ┆ 1        ┆ 1          ┆ 0         ┆ 0          ┆ 35  │
# │ 1        ┆ 0            ┆ 0        ┆ 0          ┆ 0         ┆ 1          ┆ 42  │
# │ 0        ┆ 0            ┆ 1        ┆ 0          ┆ 1         ┆ 0          ┆ 31  │
# │ 0        ┆ 1            ┆ 0        ┆ 1          ┆ 0         ┆ 0          ┆ 28  │
# │ 1        ┆ 0            ┆ 0        ┆ 0          ┆ 0         ┆ 1          ┆ 39  │
# └──────────┴──────────────┴──────────┴────────────┴───────────┴────────────┴─────┘
# One-hot encodes only gender and city; keeps age as a normal numeric column.

print(df_people.to_dummies(columns=["gender", "city"], drop_first=True))
# shape: (6, 5)
# ┌──────────┬──────────────┬────────────┬───────────┬─────┐
# │ gender_F ┆ gender_LGBTQ ┆ city_Busan ┆ city_Jeju ┆ age │
# │ ---      ┆ ---          ┆ ---        ┆ ---       ┆ --- │
# │ u8       ┆ u8           ┆ u8         ┆ u8        ┆ i64 │
# ╞══════════╪══════════════╪════════════╪═══════════╪═════╡
# │ 0        ┆ 0            ┆ 0          ┆ 0         ┆ 29  │
# │ 0        ┆ 0            ┆ 1          ┆ 0         ┆ 35  │
# │ 1        ┆ 0            ┆ 0          ┆ 0         ┆ 42  │
# │ 0        ┆ 0            ┆ 0          ┆ 1         ┆ 31  │
# │ 0        ┆ 1            ┆ 1          ┆ 0         ┆ 28  │
# │ 1        ┆ 0            ┆ 0          ┆ 0         ┆ 39  │
# └──────────┴──────────────┴────────────┴───────────┴─────┘
# Drops the first generated dummy for each encoded column.


#----------------------------------------------------------------------------------------------------#
#---------------------------------- 2. Binning and Discretization -----------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
Binning and Discretization convert continuous numerical data into discrete categories.
This is useful for simplifying analysis, reporting, and feature engineering.

Pandas:
    pd.cut()
    pd.qcut()

Polars:
    Series.cut() / Expr.cut()
    Series.qcut() / Expr.qcut()
'''

np.random.seed(42)  # For reproducibility
s_quantitative = pl.Series(
    "score",
    np.round(np.random.normal(loc=5, scale=2, size=20), 6),
)

print(s_quantitative)
# shape: (20,)
# Series: 'score' [f64]
# [
# 	5.993428
# 	4.723471
# 	6.295377
# 	8.046060
# 	4.531693
# 	4.531726
# 	8.158426
# 	6.534869
# 	4.061051
# 	6.085120
# 	4.073165
# 	4.068540
# 	5.483925
# 	1.173440
# 	1.550164
# 	3.875425
# 	2.974338
# 	5.628495
# 	3.183952
# 	2.175393
# ]

####################################
##              .cut()            ##
####################################
'''
Polars .cut() bins continuous values into categories using INTERNAL breakpoints.

Important pandas difference:
    pandas pd.cut(x, bins=[0, 2, 4, 6, 8, 10]) receives all bin edges.
    polars s.cut(breaks=[2, 4, 6, 8]) receives only the internal cut points.

Polars automatically creates the outer intervals:
    (-inf, 2], (2, 4], (4, 6], (6, 8], (8, inf]

If labels are given, the number of labels must equal len(breaks) + 1.
'''

#-----------------
## Custom breakpoints: [2, 4, 6, 8]
#-----------------

s_bins = s_quantitative.cut(
    breaks=[2, 4, 6, 8],
    labels=["Very Low", "Low", "Medium", "High", "Very High"],
)

print(s_bins)
# shape: (20,)
# Series: 'score' [enum]
# [
# 	"Medium"
# 	"Medium"
# 	"High"
# 	"Very High"
# 	"Medium"
# 	"Medium"
# 	"Very High"
# 	"High"
# 	"Medium"
# 	"High"
# 	"Medium"
# 	"Medium"
# 	"Medium"
# 	"Very Low"
# 	"Very Low"
# 	"Low"
# 	"Low"
# 	"Medium"
# 	"Low"
# 	"Low"
# ]

# Quick frequency table of the bins
print(s_bins.value_counts())
# shape: (5, 2)
# ┌───────────┬───────┐
# │ score     ┆ count │
# │ ---       ┆ ---   │
# │ enum      ┆ u32   │
# ╞═══════════╪═══════╡
# │ Very Low  ┆ 2     │
# │ Low       ┆ 4     │
# │ Medium    ┆ 9     │
# │ High      ┆ 3     │
# │ Very High ┆ 2     │
# └───────────┴───────┘

#-----------------
## Without labels: Polars returns interval text as an Enum
#-----------------

print(s_quantitative.cut(breaks=[2, 4, 6, 8]))
# shape: (20,)
# Series: 'score' [enum]
# [
# 	"(4, 6]"
# 	"(4, 6]"
# 	"(6, 8]"
# 	"(8, inf]"
# 	"(4, 6]"
# 	…
# 	"(2, 4]"
# 	"(2, 4]"
# 	"(4, 6]"
# 	"(2, 4]"
# 	"(2, 4]"
# ]

#####################################################
##  pandas-like bounded bins: values outside range ##
#####################################################
'''
Because Polars .cut() automatically uses -inf and inf for outer bins, it will NOT
turn out-of-range values into null just because your pandas bin edges had a minimum
or maximum.

If you want pandas-like bounded behavior, combine .cut() with a condition.
Example: only assign labels to values in [0, 10]; otherwise return null.
'''

s_with_outliers = pl.Series("score", [-1.0, 1.5, 3.0, 5.5, 7.5, 10.5])
df_with_outliers = s_with_outliers.to_frame()

bounded_cut = df_with_outliers.with_columns(
    pl.when(pl.col("score").is_between(0, 10, closed="both"))
    .then(
        pl.col("score").cut(
            breaks=[2, 4, 6, 8],
            labels=["Very Low", "Low", "Medium", "High", "Very High"],
        )
    )
    .otherwise(None)
    .alias("bounded_bin")
)

print(bounded_cut)
# shape: (6, 2)
# ┌───────┬─────────────┐
# │ score ┆ bounded_bin │
# │ ---   ┆ ---         │
# │ f64   ┆ enum        │
# ╞═══════╪═════════════╡
# │ -1.0  ┆ null        │
# │ 1.5   ┆ Very Low    │
# │ 3.0   ┆ Low         │
# │ 5.5   ┆ Medium      │
# │ 7.5   ┆ High        │
# │ 10.5  ┆ null        │
# └───────┴─────────────┘

###################################################
## Equal-width bins: pandas pd.cut(bins=3) style ##
###################################################
'''
Pandas:
    pd.cut(x=s_quantitative, bins=3, labels=["Low", "Medium", "High"])

Polars .cut() does not accept an integer number of bins.
To create equal-width bins, calculate breakpoints manually.

For n bins, you need n - 1 internal breakpoints.
'''

n_bins = 3
minimum = s_quantitative.min()
maximum = s_quantitative.max()
width = (maximum - minimum) / n_bins

breaks_equal_width = [minimum + width * i for i in range(1, n_bins)]
print(breaks_equal_width)
# Example: [3.501768666666667, 5.830097333333333]

s_equal_width = s_quantitative.cut(
    breaks=breaks_equal_width,
    labels=["Low", "Medium", "High"],
)

print(s_equal_width)
# shape: (20,)
# Series: 'score' [enum]
# [
# 	"High"
# 	"Medium"
# 	"High"
# 	"High"
# 	"Medium"
# 	"Medium"
# 	"High"
# 	"High"
# 	"Medium"
# 	"High"
# 	"Medium"
# 	"Medium"
# 	"Medium"
# 	"Low"
# 	"Low"
# 	"Medium"
# 	"Low"
# 	"Medium"
# 	"Low"
# 	"Low"
# ]

print(s_equal_width.value_counts())
# shape: (3, 2)
# ┌────────┬───────┐
# │ score  ┆ count │
# │ ---    ┆ ---   │
# │ enum   ┆ u32   │
# ╞════════╪═══════╡
# │ High   ┆ 6     │
# │ Medium ┆ 9     │
# │ Low    ┆ 5     │
# └────────┴───────┘
# Frequency table for Low / Medium / High bins

#############################################
##        .cut(include_breaks=True)        ##
#############################################
'''
include_breaks=True returns a Struct containing:
1. breakpoint: the right endpoint of the bin
2. category: the bin/category label

Use .unnest() to expand the Struct into normal DataFrame columns.
'''

df_cut_breaks = s_quantitative.to_frame().with_columns(
    pl.col("score")
    .cut(breaks=[2, 4, 6, 8], include_breaks=True)
    .alias("cut")
).unnest("cut")

print(df_cut_breaks)
# shape: (20, 3)
# ┌──────────┬────────────┬────────────┐
# │ score    ┆ breakpoint ┆ category   │
# │ ---      ┆ ---        ┆ ---        │
# │ f64      ┆ f64        ┆ enum       │
# ╞══════════╪════════════╪════════════╡
# │ 5.993428 ┆ 6.0        ┆ (4, 6]     │
# │ 4.723471 ┆ 6.0        ┆ (4, 6]     │
# │ 6.295377 ┆ 8.0        ┆ (6, 8]     │
# │ 8.04606  ┆ inf        ┆ (8, inf]   │
# │ ...      ┆ ...        ┆ ...        │
# └──────────┴────────────┴────────────┘

#######################################
##          left_closed=True         ##
#######################################
'''
By default, Polars intervals are right-closed:
    (-inf, 2], (2, 4], (4, inf]

With left_closed=True, intervals become left-closed:
    [-inf, 2), [2, 4), [4, inf)

This matters for values exactly equal to a breakpoint.
'''

s_boundary = pl.Series("x", [2.0, 4.0, 6.0])

print(s_boundary.cut([2.0, 4.0], labels=["Low", "Medium", "High"]))
# shape: (3,)
# Series: 'x' [enum]
# [
# 	"Low"       # 2.0 belongs to (-inf, 2]
# 	"Medium"    # 4.0 belongs to (2, 4]
# 	"High"
# ]

print(s_boundary.cut([2.0, 4.0], labels=["Low", "Medium", "High"], left_closed=True))
# shape: (3,)
# Series: 'x' [enum]
# [
# 	"Medium"    # 2.0 belongs to [2, 4)
# 	"High"      # 4.0 belongs to [4, inf)
# 	"High"
# ]


######################################
##              .qcut()             ##
######################################
'''
qcut means quantile-based discretization.

Pandas:
    pd.qcut(x=s_quantitative, q=4, labels=["Q1", "Q2", "Q3", "Q4"])

Polars:
    s_quantitative.qcut(4, labels=["Q1", "Q2", "Q3", "Q4"])

If quantiles is an integer, Polars creates bins with uniform probability.
For q=4, the bins are quartiles.
'''

#-----------------
## q = 4 (quartiles)
#-----------------

s_qcut = s_quantitative.qcut(
    4,
    labels=["Q1", "Q2", "Q3", "Q4"],
)

print(s_qcut)
# shape: (20,)
# Series: 'score' [cat]
# [
# 	"Q3"
# 	"Q3"
# 	"Q4"
# 	"Q4"
# 	"Q2"
# 	"Q3"
# 	"Q4"
# 	"Q4"
# 	"Q2"
# 	"Q4"
# 	"Q2"
# 	"Q2"
# 	"Q3"
# 	"Q1"
# 	"Q1"
# 	"Q2"
# 	"Q1"
# 	"Q3"
# 	"Q1"
# 	"Q1"
# ]

print(s_qcut.value_counts())
# shape: (4, 2)
# ┌───────┬───────┐
# │ score ┆ count │
# │ ---   ┆ ---   │
# │ cat   ┆ u32   │
# ╞═══════╪═══════╡
# │ Q1    ┆ 5     │
# │ Q3    ┆ 5     │
# │ Q2    ┆ 5     │
# │ Q4    ┆ 5     │
# └───────┴───────┘
# Each quartile should contain approximately the same number of values.

#-----------------
## Explicit quantile probabilities
#-----------------
'''
You can also pass explicit probabilities between 0 and 1.
For two cut points [0.25, 0.75], you need three labels.
'''

s_qcut_three_groups = s_quantitative.qcut(
    [0.25, 0.75],
    labels=["Low 25%", "Middle 50%", "High 25%"],
)

print(s_qcut_three_groups)
# shape: (20,)
# Series: 'score' [cat]
# [
# 	"Middle 50%"
# 	"Middle 50%"
# 	"High 25%"
# 	"High 25%"
# 	"Middle 50%"
# 	…
# 	"Middle 50%"
# 	"Low 25%"
# 	"Middle 50%"
# 	"Low 25%"
# 	"Low 25%"
# ]
# Groups values by the 25th and 75th percentile boundaries.

##########################################
##       .qcut(include_breaks=True)     ##
##########################################
'''
include_breaks=True works with qcut too.
It returns a Struct, so use .unnest() to see the breakpoint and category columns.
'''

df_qcut_breaks = s_quantitative.to_frame().with_columns(
    pl.col("score")
    .qcut(4, include_breaks=True)
    .alias("qcut")
).unnest("qcut")

print(df_qcut_breaks)
# shape: (20, 3)
# ┌──────────┬────────────┬─────────────────────────┐
# │ score    ┆ breakpoint ┆ category                │
# │ ---      ┆ ---        ┆ ---                     │
# │ f64      ┆ f64        ┆ cat                     │
# ╞══════════╪════════════╪═════════════════════════╡
# │ 5.993428 ┆ 6.016351   ┆ (4.5317095, 6.016351]   │
# │ 4.723471 ┆ 6.016351   ┆ (4.5317095, 6.016351]   │
# │ 6.295377 ┆ inf        ┆ (6.016351, inf]         │
# │ 8.04606  ┆ inf        ┆ (6.016351, inf]         │
# │ 4.531693 ┆ 4.5317095  ┆ (3.70255675, 4.5317095] │
# │ …        ┆ …          ┆ …                       │
# │ 3.875425 ┆ 4.5317095  ┆ (3.70255675, 4.5317095] │
# │ 2.974338 ┆ 3.702557   ┆ (-inf, 3.70255675]      │
# │ 5.628495 ┆ 6.016351   ┆ (4.5317095, 6.016351]   │
# │ 3.183952 ┆ 3.702557   ┆ (-inf, 3.70255675]      │
# │ 2.175393 ┆ 3.702557   ┆ (-inf, 3.70255675]      │
# └──────────┴────────────┴─────────────────────────┘

#######################################################
##       Duplicate quantiles: allow_duplicates       ##
#######################################################
'''
When many values are repeated, different quantile cut points can become identical.
By default, this may raise a DuplicateError.

Use allow_duplicates=True to drop duplicate quantile breakpoints.
This is similar in spirit to pandas qcut(..., duplicates="drop").
'''

s_repeated = pl.Series("x", [1, 1, 1, 1, 2, 2, 3, 3])

print(s_repeated.qcut(4, allow_duplicates=True))
# shape: (8,)
# Series: 'x' [cat]
# [
# 	"(-inf, 1]"
# 	"(-inf, 1]"
# 	"(-inf, 1]"
# 	"(-inf, 1]"
# 	"(1.5, 2.25]"
# 	"(1.5, 2.25]"
# 	"(2.25, inf]"
# 	"(2.25, inf]"
# ]
# Duplicate quantile breakpoints are dropped instead of raising an error.

############################################################
##  DataFrame expression style: recommended in workflows  ##
############################################################
'''
For actual feature engineering, use expressions inside .with_columns().
This keeps the workflow lazy-compatible and scales naturally to multiple columns.
'''

df_scores = s_quantitative.to_frame()

df_binned = df_scores.with_columns(
    pl.col("score")
    .cut([2, 4, 6, 8], labels=["Very Low", "Low", "Medium", "High", "Very High"])
    .alias("score_band"),

    pl.col("score")
    .qcut(4, labels=["Q1", "Q2", "Q3", "Q4"])
    .alias("score_quartile"),
)

print(df_binned)
# shape: (20, 3)
# ┌──────────┬────────────┬────────────────┐
# │ score    ┆ score_band ┆ score_quartile │
# │ ---      ┆ ---        ┆ ---            │
# │ f64      ┆ enum       ┆ cat            │
# ╞══════════╪════════════╪════════════════╡
# │ 5.993428 ┆ Medium     ┆ Q3             │
# │ 4.723471 ┆ Medium     ┆ Q3             │
# │ 6.295377 ┆ High       ┆ Q4             │
# │ 8.04606  ┆ Very High  ┆ Q4             │
# │ ...      ┆ ...        ┆ ...            │
# └──────────┴────────────┴────────────────┘


#----------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. Real applications ---------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
A common machine-learning preprocessing workflow:
1. Keep original numerical variables.
2. Create factorized integer codes for compact categorical representation.
3. Create bins from numerical variables.
4. One-hot encode selected categorical/bin columns for model input.
'''

np.random.seed(7)
df_model = pl.DataFrame(
    {
        "gender": ["M", "F", "M", "LGBTQ", "F", "M", "F", "M"],
        "city": ["Seoul", "Busan", "Seoul", "Jeju", "Busan", "Jeju", "Seoul", "Busan"],
        "income": np.round(np.random.normal(loc=5000, scale=1200, size=8), 2),
    }
)

print(df_model)
# shape: (8, 3)
# ┌────────┬───────┬─────────┐
# │ gender ┆ city  ┆ income  │
# │ ---    ┆ ---   ┆ ---     │
# │ str    ┆ str   ┆ f64     │
# ╞════════╪═══════╪═════════╡
# │ M      ┆ Seoul ┆ ...     │
# │ F      ┆ Busan ┆ ...     │
# │ M      ┆ Seoul ┆ ...     │
# │ LGBTQ  ┆ Jeju  ┆ ...     │
# │ ...    ┆ ...   ┆ ...     │
# └────────┴───────┴─────────┘

# ----------------------------
# Step 1: Add categorical codes and binned numerical features
# ----------------------------

df_features = df_model.with_columns(
    pl.col("gender").cast(pl.Categorical).to_physical().alias("gender_code"),
    pl.col("city").cast(pl.Categorical).to_physical().alias("city_code"),

    # Equal-width style income bands from manually selected business breakpoints
    pl.col("income")
    .cut([4000, 5500, 7000], labels=["Very Low", "Low", "Medium", "High"])
    .alias("income_band"),

    # Quantile-based income groups
    pl.col("income")
    .qcut(4, labels=["Q1", "Q2", "Q3", "Q4"])
    .alias("income_quartile"),
)

print(df_features)
# shape: (8, 7)
# ┌────────┬───────┬─────────┬─────────────┬───────────┬─────────────┬─────────────────┐
# │ gender ┆ city  ┆ income  ┆ gender_code ┆ city_code ┆ income_band ┆ income_quartile │
# │ ---    ┆ ---   ┆ ---     ┆ ---         ┆ ---       ┆ ---         ┆ ---             │
# │ str    ┆ str   ┆ f64     ┆ u32         ┆ u32       ┆ enum        ┆ cat             │
# ╞════════╪═══════╪═════════╪═════════════╪═══════════╪═════════════╪═════════════════╡
# │ M      ┆ Seoul ┆ 7028.63 ┆ 0           ┆ 17        ┆ High        ┆ Q4              │
# │ F      ┆ Busan ┆ 4440.88 ┆ 1           ┆ 18        ┆ Low         ┆ Q2              │
# │ M      ┆ Seoul ┆ 5039.38 ┆ 0           ┆ 17        ┆ Low         ┆ Q3              │
# │ LGBTQ  ┆ Jeju  ┆ 5489.02 ┆ 2           ┆ 19        ┆ Low         ┆ Q4              │
# │ F      ┆ Busan ┆ 4053.29 ┆ 1           ┆ 18        ┆ Low         ┆ Q1              │
# │ M      ┆ Jeju  ┆ 5002.48 ┆ 0           ┆ 19        ┆ Low         ┆ Q3              │
# │ F      ┆ Seoul ┆ 4998.93 ┆ 1           ┆ 17        ┆ Low         ┆ Q2              │
# │ M      ┆ Busan ┆ 2894.33 ┆ 0           ┆ 18        ┆ Very Low    ┆ Q1              │
# └────────┴───────┴─────────┴─────────────┴───────────┴─────────────┴─────────────────┘
# Adds gender_code, city_code, income_band, and income_quartile.

# ----------------------------
# Step 2: One-hot encode selected features
# ----------------------------
# Keep the original income and integer codes, and encode selected categorical columns.

df_model_matrix = df_features.to_dummies(
    columns=["gender", "city", "income_band", "income_quartile"],
    drop_first=True,
)

print(df_model_matrix)
# shape: (8, 12)
# ┌──────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬───────────┐
# │ gender_F ┆ gender_LG ┆ city_Busa ┆ city_Jeju ┆ … ┆ income_ba ┆ income_qu ┆ income_qu ┆ income_qu │
# │ ---      ┆ BTQ       ┆ n         ┆ ---       ┆   ┆ nd_Very   ┆ artile_Q1 ┆ artile_Q2 ┆ artile_Q3 │
# │ u8       ┆ ---       ┆ ---       ┆ u8        ┆   ┆ Low       ┆ ---       ┆ ---       ┆ ---       │
# │          ┆ u8        ┆ u8        ┆           ┆   ┆ ---       ┆ u8        ┆ u8        ┆ u8        │
# │          ┆           ┆           ┆           ┆   ┆ u8        ┆           ┆           ┆           │
# ╞══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪═══════════╡
# │ 0        ┆ 0         ┆ 0         ┆ 0         ┆ … ┆ 0         ┆ 0         ┆ 0         ┆ 0         │
# │ 1        ┆ 0         ┆ 1         ┆ 0         ┆ … ┆ 0         ┆ 0         ┆ 1         ┆ 0         │
# │ 0        ┆ 0         ┆ 0         ┆ 0         ┆ … ┆ 0         ┆ 0         ┆ 0         ┆ 1         │
# │ 0        ┆ 1         ┆ 0         ┆ 1         ┆ … ┆ 0         ┆ 0         ┆ 0         ┆ 0         │
# │ 1        ┆ 0         ┆ 1         ┆ 0         ┆ … ┆ 0         ┆ 1         ┆ 0         ┆ 0         │
# │ 0        ┆ 0         ┆ 0         ┆ 1         ┆ … ┆ 0         ┆ 0         ┆ 0         ┆ 1         │
# │ 1        ┆ 0         ┆ 0         ┆ 0         ┆ … ┆ 0         ┆ 0         ┆ 1         ┆ 0         │
# │ 0        ┆ 0         ┆ 1         ┆ 0         ┆ … ┆ 1         ┆ 1         ┆ 0         ┆ 0         │
# └──────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴───────────┘
# A model-ready DataFrame with UInt8 dummy columns.


#----------------------------------------------------------------------------------------------------#
#--------------------------------------------- Summary ----------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
Summary:

Pandas                                 Polars
------                                 ------
pd.factorize(s)                        s.cast(pl.Categorical).to_physical()
pd.factorize(s) first-appearance       s.unique(maintain_order=True) + join lookup table
pd.get_dummies(s)                      s.to_dummies()
pd.get_dummies(df, columns=[...])      df.to_dummies(columns=[...])
pd.cut(x, bins=[0,2,4,6])              s.cut(breaks=[2,4], labels=[...])
pd.cut(x, bins=3)                      calculate 2 internal breakpoints, then s.cut(...)
pd.qcut(x, q=4)                        s.qcut(4, labels=[...])
pd.qcut(..., duplicates="drop")       s.qcut(..., allow_duplicates=True)
pd.cut/qcut retbins-style output       .cut/.qcut(include_breaks=True).unnest(...)

Remember:
+ .cut() returns Enum by default.
+ .qcut() returns Categorical by default.
+ .to_dummies() returns UInt8 columns.
+ For production DataFrame workflows, prefer expression style:
    df.with_columns(pl.col("x").cut(...).alias("x_bin"))
    df.with_columns(pl.col("x").qcut(...).alias("x_quantile"))
'''
