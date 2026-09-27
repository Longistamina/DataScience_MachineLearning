'''
1. Categorical encoding with `s.cast(pl.Categorical).to_physical()`

2. `.to_dummies()`: one-hot encoding
    + Series: s.to_dummies()
    + DataFrame: df.to_dummies(columns=[...])

3. `bin_ranks()`: Bin values by their position in sorted order.
   + Series: s.bin_ranks(ranks=..., labels=..., include_intervals=False)
   + DataFrame expression: pl.col("x").bin_ranks(...)

4. `bin_quantiles()`: Bin values into discrete intervals delimited by quantiles of the data.
    + Series: s.bin_quantiles(quantiles=..., labels=..., include_intervals=False, right_closed=False)
    + DataFrame expression: pl.col("x").bin_quantiles(...)

5. `bin_intervals()`: Bin values into discrete intervals delimited by breakpoints.
    + Series: s.bin_intervals(intervals=..., labels=..., include_intervals=False, right_closed=False)
    + DataFrame expression: pl.col("x").bin_intervals(...)
'''

import numpy as np
import polars as pl

np.random.seed(42)  # For reproducibility
s_quantitative = pl.Series(
    "score",
    np.round(np.random.normal(loc=5, scale=2, size=20), 6),
)

df_quantitative = (
    s_quantitative
    .to_frame()
    .with_row_index(name="id", offset=1)
    .with_columns(
        id = (pl.lit("id") + pl.col("id").cast(pl.String).str.zfill(pl.col("id").max().log10().ceil().cast(pl.Int64)))
    )
)

# =========================================================================================
# 1. Categorical encoding with `s.cast(pl.Categorical).to_physical()`
# =========================================================================================
'''
Categorical Encoding is the process of converting categorical variables into numerical representations.
This is useful for machine learning algorithms that require numerical input.

For example:
    ["A", "C", "C", "B"] -> [0, 2, 2, 1]
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

# Use `s.cast(pl.Categorical).to_physical()` to convert to categories and get numeric codes
print(
    s_gender
    .cast(pl.Categorical)
    .to_physical()
)
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

# Use `s.cast(pl.Categorical).unique()` to get the mapping
print(
    s_gender
    .cast(pl.Categorical)
    .unique()
)
# shape: (3,)
# Series: 'gender' [cat]
# [
# 	"M"
# 	"F"
# 	"LGBTQ"
# ]

# =========================================================================================
# 2. `.to_dummies()`: one-hot encoding
# =========================================================================================
'''
.to_dummies() creates a DataFrame with one UInt8 indicator column for each category.
Each column contains 1 if the row belongs to that category, otherwise 0.

This execution is called "one-hot encoding"
'''

##----------------##
## s.to_dummies() ##
##----------------##

# Without dropping the first category
print(
    s_gender.to_dummies()
)
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
print(
    s_gender.to_dummies(separator="__")
)
# Columns: gender__F, gender__LGBTQ, gender__M

# With dropping the first category
'''
If we have n categories, we often only need n-1 dummy columns.
The omitted category can be inferred when all dummy columns are 0.

This is commonly used to avoid perfect multicollinearity in linear models.
'''
print(
    s_gender.to_dummies(drop_first=True)
)
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

##------------------------------##
## df.to_dummies(columns=[...]) ##
##------------------------------##
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

print(
    df_people.to_dummies(columns=["gender", "city"])
)
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

# Use with drop_first=True
print(
    df_people.to_dummies(columns=["gender", "city"], drop_first=True)
)
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

# =========================================================================================
# 3. `bin_ranks()`: Bin values by their position in sorted order.
# =========================================================================================
'''
Parameters
----------
ranks
    Non-decreasing cumulative fractions in `[0, 1]`, or a positive integer
    giving the number of near-equal-sized bins. Two equal fractions delimit an
    empty bin. For an integer, earlier bins receive any remainder.
labels
    One label per bin, or `False` to return the integer bin index.
include_intervals
    Return a struct with fields `bin`, `left`, and `right`. Boundaries are input
    values, not ranks; the first bin's left and last bin's right boundary are
    null.
'''

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

##---------------------------------------------------------------------##
## Series: s.bin_ranks(ranks=..., labels=..., include_intervals=False) ##
##---------------------------------------------------------------------##

print(
    s_quantitative
    .bin_ranks(
        ranks=[0.25, 0.75],
        labels=["Small", "Medium", "Big"]
    )
)
# shape: (20,)
# Series: 'score' [enum]
# [
# 	"Medium"
# 	"Medium"
# 	"Big"
# 	"Big"
# 	"Medium"
# 	…
# 	"Medium"
# 	"Small"
# 	"Medium"
# 	"Small"
# 	"Small"
# ]

# With `labels=False`: Polars returns interval text as an Enum
print(
    s_quantitative
    .bin_ranks(
        ranks=[0.25, 0.75],
        labels=False
    )
)
# shape: (20,)
# Series: 'score' [u32]
# [
# 	1
# 	1
# 	2
# 	2
# 	1
# 	…
# 	1
# 	0
# 	1
# 	0
# 	0
# ]

# Use ranks=number_of_bins:
print(
    s_quantitative
    .bin_ranks(
        ranks=5,
        labels=False
    )
)
# shape: (20,)
# Series: 'score' [u32]
# [
# 	3
# 	2
# 	4
# 	4
# 	2
# 	…
# 	1
# 	0
# 	3
# 	1
# 	0
# ]

##--------------------------------------------------##
## DataFrame expression: pl.col("x").bin_ranks(...) ##
##--------------------------------------------------##

print(df_quantitative)
# shape: (20, 2)
# ┌──────┬──────────┐
# │ id   ┆ score    │
# │ ---  ┆ ---      │
# │ str  ┆ f64      │
# ╞══════╪══════════╡
# │ id01 ┆ 5.993428 │
# │ id02 ┆ 4.723471 │
# │ id03 ┆ 6.295377 │
# │ id04 ┆ 8.04606  │
# │ id05 ┆ 4.531693 │
# │ …    ┆ …        │
# │ id16 ┆ 3.875425 │
# │ id17 ┆ 2.974338 │
# │ id18 ┆ 5.628495 │
# │ id19 ┆ 3.183952 │
# │ id20 ┆ 2.175393 │
# └──────┴──────────┘

# `bin_ranks()` the score column
print(
    df_quantitative
    .with_columns(
        pl.col("score").bin_ranks(ranks=[0.25, 0.75], labels=["low", "medium", "high"]).alias("level")
    )
)
# shape: (20, 3)
# ┌──────┬──────────┬────────┐
# │ id   ┆ score    ┆ level  │
# │ ---  ┆ ---      ┆ ---    │
# │ str  ┆ f64      ┆ enum   │
# ╞══════╪══════════╪════════╡
# │ id01 ┆ 5.993428 ┆ medium │
# │ id02 ┆ 4.723471 ┆ medium │
# │ id03 ┆ 6.295377 ┆ high   │
# │ id04 ┆ 8.04606  ┆ high   │
# │ id05 ┆ 4.531693 ┆ medium │
# │ …    ┆ …        ┆ …      │
# │ id16 ┆ 3.875425 ┆ medium │
# │ id17 ┆ 2.974338 ┆ low    │
# │ id18 ┆ 5.628495 ┆ medium │
# │ id19 ┆ 3.183952 ┆ low    │
# │ id20 ┆ 2.175393 ┆ low    │
# └──────┴──────────┴────────┘

# ==============================================================================================
# 4. `bin_quantiles()`: Bin values into discrete intervals delimited by quantiles of the data
# ==============================================================================================
'''
Parameters
----------
quantiles
    Non-decreasing quantiles in `[0, 1]`, or a positive integer giving the
    number of bins. Two equal quantiles delimit an empty bin. Input must be
    numeric. For quantile `q`, the value of the breakpoint is the sorted value
    at `floor(q * (len - 1))`.
labels
    One label per bin, or `False` to return the integer bin index.
include_intervals
    Return a struct with fields `bin`, `left`, and `right`. The first bin's left
    and last bin's right boundary are null.
right_closed
    Use right-closed `(left, right]` rather than left-closed `[left, right)` bins.
'''

##---------------------------##
## Series: s.bin_quantiles() ##
##---------------------------##

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

print(
    s_quantitative
    .bin_quantiles(
        quantiles=[0.25, 0.5, 0.75],
        labels=["Q1", "Q2", "Q3", "Q4"]
    )
)
# shape: (20,)
# Series: 'score' [enum]
# [
# 	"Q4"
# 	"Q3"
# 	"Q4"
# 	"Q4"
# 	"Q3"
# 	…
# 	"Q2"
# 	"Q1"
# 	"Q3"
# 	"Q2"
# 	"Q1"
# ]

##------------------------------------------------------##
## DataFrame expression: pl.col("x").bin_quantiles(...) ##
##------------------------------------------------------##

print(
    df_quantitative
    .with_columns(
        pl.col("score").bin_quantiles([0.25, 0.5, 0.75], labels=["q1", "q2", "q3", "q4"]).alias("quantile")
    )
)
# shape: (20, 3)
# ┌──────┬──────────┬──────────┐
# │ id   ┆ score    ┆ quantile │
# │ ---  ┆ ---      ┆ ---      │
# │ str  ┆ f64      ┆ enum     │
# ╞══════╪══════════╪══════════╡
# │ id01 ┆ 5.993428 ┆ q4       │
# │ id02 ┆ 4.723471 ┆ q3       │
# │ id03 ┆ 6.295377 ┆ q4       │
# │ id04 ┆ 8.04606  ┆ q4       │
# │ id05 ┆ 4.531693 ┆ q3       │
# │ …    ┆ …        ┆ …        │
# │ id16 ┆ 3.875425 ┆ q2       │
# │ id17 ┆ 2.974338 ┆ q1       │
# │ id18 ┆ 5.628495 ┆ q3       │
# │ id19 ┆ 3.183952 ┆ q2       │
# │ id20 ┆ 2.175393 ┆ q1       │
# └──────┴──────────┴──────────┘

# ==============================================================================================
# 5. `bin_intervals()`: Bin values into discrete intervals delimited by breakpoints.
# ==============================================================================================
'''
Parameters
----------
intervals
    Strictly ascending breakpoints, or a positive integer giving the number of
    equal-width bins over `[min, max]`. Explicit breakpoints may have any
    orderable (non-nested) data type; an integer requires numeric input.
labels
    One label per bin, or `False` to return the integer bin index.
include_intervals
    Return a struct with fields `bin`, `left`, and `right`. The first bin's left
    and last bin's right boundary are null.
right_closed
    Use right-closed `(left, right]` rather than left-closed `[left, right)` bins.
'''

##---------------------------##
## Series: s.bin_intervals() ##
##---------------------------##

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

print(
    s_quantitative
    .bin_intervals(
        intervals=[3.5, 6.5], # use data values as bins' boundaries
        labels=["l1", "l2", "l3"]
    )
)
# shape: (20,)
# Series: 'score' [enum]
# [
# 	"l2"
# 	"l2"
# 	"l2"
# 	"l3"
# 	"l2"
# 	…
# 	"l2"
# 	"l1"
# 	"l2"
# 	"l1"
# 	"l1"
# ]

##------------------------------------------------------##
## DataFrame expression: pl.col("x").bin_intervals(...) ##
##------------------------------------------------------##

print(
    df_quantitative
    .with_columns(
        pl.col("score").bin_intervals([3.0, 6.0], labels=["l1", "l2", "l3"]).alias("interval")
    )
)
# shape: (20, 3)
# ┌──────┬──────────┬──────────┐
# │ id   ┆ score    ┆ interval │
# │ ---  ┆ ---      ┆ ---      │
# │ str  ┆ f64      ┆ enum     │
# ╞══════╪══════════╪══════════╡
# │ id01 ┆ 5.993428 ┆ l2       │
# │ id02 ┆ 4.723471 ┆ l2       │
# │ id03 ┆ 6.295377 ┆ l3       │
# │ id04 ┆ 8.04606  ┆ l3       │
# │ id05 ┆ 4.531693 ┆ l2       │
# │ …    ┆ …        ┆ …        │
# │ id16 ┆ 3.875425 ┆ l2       │
# │ id17 ┆ 2.974338 ┆ l1       │
# │ id18 ┆ 5.628495 ┆ l2       │
# │ id19 ┆ 3.183952 ┆ l2       │
# │ id20 ┆ 2.175393 ┆ l1       │
# └──────┴──────────┴──────────┘
