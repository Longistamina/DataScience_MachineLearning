'''
In Polars, categorical data is handled using two distinct, strictly typed data types:
1. pl.Categorical: Unordered, dictionary-encoded strings. Optimized for memory and speed.
2. pl.Enum: Ordered, fixed set of categories. Enforces a strict schema and meaningful sorting.

Unlike pandas, Polars does NOT have an extensive `.cat` accessor for mutating categories in-place.
Instead, category manipulation is done by defining `pl.Enum` schemas or casting to/from `pl.String`.

##--------------------------------------------------##
PART 1: pl.Categorical (Unordered)
0. Creation
1. Core attributes (Categories, Codes)
2. Manipulating Categories (via String casting)
3. Exploring (unique, value_counts)

PART 2: pl.Enum (Ordered)
4. Creation and Ordering
5. Fast trick to convert to Enum without specifying list of categories
6. Convert a LazyFrame categorical Column to Enum (Pokemon dataframe example)
7. Meaningful Sorting, Min, and Max
8. Reordering and Renaming (via Enum schema)
'''

import polars as pl
from polars import selectors as cs
from polars import col as c
from pathlib import Path

# Optional display settings
pl.Config.set_tbl_rows(10)
pl.Config.set_tbl_cols(20)
pl.Config.set_float_precision(6)
pl.Config.set_tbl_width_chars(120)

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))


# =========================================================================================
# PART 1: pl.Categorical (Unordered)
# =========================================================================================

lst_gender = ["M", "M", "F", "M", "LGBTQ", "F", "M", "F", "LGBTQ", "M"]

##--------------------------------##
## 0. Create a Categorical Series ##
##--------------------------------##

# Using dtype=pl.Categorical
s_cat = pl.Series("gender", lst_gender, dtype=pl.Categorical)
print(s_cat)
# shape: (10,)
# Series: 'gender' [cat]
# [
# 	"M"
# 	"M"
# 	"F"
# ...

# Or using .cast()
s_cat = pl.Series("gender", lst_gender).cast(pl.Categorical)

##--------------------##
## 1. Core attributes ##
##--------------------##

# Get categories
print(s_cat.cat.get_categories())
# shape: (3,)
# Series: 'gender' [str]
# [
# 	"M"
# 	"F"
# 	"LGBTQ"
# ]

# Get integer codes (physical representation)
print(s_cat.to_physical())
# shape: (10,)
# Series: 'gender' [u32]
# [
# 	0
# 	0
# 	1
# ...

##----------------------------##
## 2. Manipulating Categories ##
##----------------------------##
'''
Polars Categoricals infer categories directly from the data.
To add, remove, or rename categories, the idiomatic way is to cast to String,
manipulate, and cast back (or cast to an Enum).
'''

# Renaming categories (Equivalent to pandas .cat.rename_categories)
s_renamed = (
    s_cat.cast(pl.String)
    .replace({"F": "Female", "M": "Male", "LGBTQ": "Other"})
    .cast(pl.Categorical)
)
print(s_renamed.cat.get_categories())
# ["Male", "Female", "Other"]

# Removing unused categories
# Polars automatically drops unused categories if you cast to String and back to Categorical
s_subset = s_cat.filter(s_cat != "LGBTQ")
s_cleaned = s_subset.cast(pl.String).cast(pl.Categorical)
print(s_cleaned.cat.get_categories())
# ["M", "F"]  (LGBTQ is gone)

##--------------------------##
## 3. Exploring Categorical ##
##--------------------------##

# .unique() returns a Series of unique values
print(s_cat.unique())
# shape: (3,)
# Series: 'gender' [cat]
# [
# 	"M"
# 	"F"
# 	"LGBTQ"
# ]

# .value_counts() returns a DataFrame!
print(s_cat.value_counts())
# shape: (3, 2)
# ┌────────┬───────┐
# │ gender ┆ count │
# │ ---    ┆ ---   │
# │ cat    ┆ u32   │
# ╞════════╪═══════╡
# │ M      ┆ 5     │
# │ F      ┆ 3     │
# │ LGBTQ  ┆ 2     │
# └────────┴───────┘


# =========================================================================================
# PART 2: pl.Enum (Ordered)
# =========================================================================================

##--------------------------##
## 4. Creation and Ordering ##
##--------------------------##
'''
To create an ordered categorical type in Polars, you MUST use `pl.Enum`.
You define the exact order of categories in a list.
'''

# Define the ordered schema
gender_enum = pl.Enum(["LGBTQ", "F", "M"])

# Cast the Series to the Enum type
s_enum = pl.Series("gender", lst_gender).cast(gender_enum)
print(s_enum)
# shape: (10,)
# Series: 'gender' [enum]
# [
# 	"M"
# 	"M"
# 	"F"
# ...

# Check if it's ordered (It is an Enum)
print(isinstance(s_enum.dtype, pl.Enum))
# True

##------------------------------------------------------------------------##
## 5. Fast trick to convert to Enum without specifying list of categories ##
##------------------------------------------------------------------------##

s_level = pl.Series(name="level", values=[2, 1, 3, 3, 1, 4, 6, 2, 5, 3, 1, 5, 4])
print(s_level.dtype) # Int64

# convert from pl.Categorical to pl.Enum without specifying list of categories
s_level_enum = (
    s_level
    .cast(pl.String) # MUST cast to String first (if the original Series is already a String or Categorical, can skip this)
    .cast(
        pl.Enum(
            s_level
            .cast(pl.String) # MUST also need a cast here (can only skip if it is a String already)
            .unique()        # Then call unique() to get unique levels
            .sort()          # Then sort() the unique levels to get the order
            # => This list of sorted unique levels will be fed into pl.Enum() to create a corresponding Enum type
        )
    )
)

# One-liner version 1
s_level_enum = s_level.cast(pl.String).cast(pl.Enum(s_level.cast(pl.String).unique().sort()))

# One-liner version 2: here we use ```(lambda s: ...)(s_level_categ)``` to avoid typing the long series name repeatedly
s_level_enum = (lambda s: s.cast(pl.String).cast(pl.Enum(s.cast(pl.String).unique().sort())))(s_level)
print(s_level_enum)
# shape: (13,)
# Series: 'level' [enum]
# [
# 	"2"
# 	"1"
# 	"3"
# 	"3"
# 	"1"
# 	…
# 	"5"
# 	"3"
# 	"1"
# 	"5"
# 	"4"
# ]

##-------------------------------------------------------------------------------##
## 6. Convert a LazyFrame categorical Column to Enum (Pokemon dataframe example) ##
##-------------------------------------------------------------------------------##

lf_pokemon = (
    pl.scan_csv(data_dir / "pokemon.csv")
    .drop('#')
    .rename(lambda name: name.strip()) # remove trailing space characters
    .select(
        pl.all()
        .name.replace(r"\s+", "_") # replace " " or "  " (or more consecutive space characters) with just one "_"
        .name.replace(".", "", literal=True) # replace "." with empty string (remove it), literal=True to deactive regex
    )
    .with_columns(cs.string().exclude("Name").cast(pl.Categorical))
    .pipe(lambda lf: lf.with_columns(
        c.Generation.cast(pl.String).cast(pl.Enum(lf.select("Generation").collect().to_series().cast(pl.String).unique().sort())))
    )
)

print(lf_pokemon.head(5).collect())
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name           ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---            ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str            ┆ cat    ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞════════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur      ┆ Grass  ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Ivysaur        ┆ Grass  ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Venusaur       ┆ Grass  ┆ Poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ VenusaurMega   ┆ Grass  ┆ Poison ┆ 625   ┆ 80  ┆ 100    ┆ 123     ┆ 122    ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ Venusaur       ┆        ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Charmander     ┆ Fire   ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# └────────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##-------------------------------------##
## 7. Meaningful Sorting, Min, and Max ##
##-------------------------------------##
'''
Because pl.Enum has a defined order, sorting, min(), and max() respect that order,
NOT alphabetical order!
Order defined: "LGBTQ" < "F" < "M"
'''

print(s_enum.sort())
# shape: (10,)
# Series: 'gender' [enum]
# [
# 	"LGBTQ"
# 	"LGBTQ"
# 	"F"
# 	"F"
# 	"F"
# 	"M"
# 	"M"
# 	"M"
# 	"M"
# 	"M"
# ]

print(s_enum.min()) # "LGBTQ"
print(s_enum.max()) # "M"

##---------------------------------------##
## 8. Reordering and Renaming (via Enum) ##
##---------------------------------------##
'''
To reorder or rename categories in Polars, you simply define a NEW `pl.Enum`
schema and cast the existing string/categorical data to it.
'''

# Rename and Reorder simultaneously
new_schema = pl.Enum(["Other", "Female", "Male"])

# Must cast to String first to map the old values to new string values, then to new Enum
s_renamed_enum = (
    s_enum.cast(pl.String)
    .replace({"LGBTQ": "Other", "F": "Female", "M": "Male"})
    .cast(new_schema)
)
print(s_renamed_enum.sort())
# shape: (10,)
# Series: 'gender' [enum]
# [
# 	"Other"
# 	"Other"
# 	"Female"
# ...

'''Numeric Example with Nulls (Equivalent to pandas ordered price levels)'''

lst_price_levels = [1, 1, 3, 2, 5, 2, None, 4, 4, None, 3]
s_price = pl.Series("price", lst_price_levels)

# Polars Enum requires String categories.
# So we cast numbers to strings, define the Enum, and cast.
price_enum_dtype = pl.Enum(["1", "2", "3", "4", "5"])
s_price_enum = s_price.cast(pl.String).cast(price_enum_dtype)

print(s_price_enum.sort())
# Nulls are placed at the end by default in Polars sorting
# shape: (11,)
# Series: 'price' [enum]
# [
# 	"1"
# 	"1"
# 	"2"
# 	"2"
# 	"3"
# 	"3"
# 	"4"
# 	"4"
# 	"5"
# 	null
# 	null
# ]
