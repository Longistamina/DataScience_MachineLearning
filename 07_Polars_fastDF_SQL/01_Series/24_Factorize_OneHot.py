'''
Categorical Encoding is the process of converting categorical variables into numerical representations.
This is useful for machine learning algorithms that require numerical input.

Categorical Encoding with:
    1. Factorize: `s.cast(pl.Categorical).to_physical()`

    2. One-Hot encoding: `.to_dummies()`
        + Series: s.to_dummies()
        + DataFrame: df.to_dummies(columns=[...])
'''

import polars as pl

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

# =========================================================================================
# 1. Factorize: `s.cast(pl.Categorical).to_physical()`
# =========================================================================================
'''
For example:
    ["A", "C", "C", "B"] -> [0, 2, 2, 1]
'''

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
# 2. One-Hot encoding: `.to_dummies()`
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
