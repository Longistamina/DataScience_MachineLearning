'''
In Polars, the main tool for both modifying existing columns or deriving new columns is:

    df.with_columns(...)

Important Polars ideas:
+ Polars DataFrames are immutable-style: methods return a new DataFrame.
+ Use df = df.with_columns(...) instead of pandas inplace assignment.
+ Added columns replace existing columns with the same name.
+ Use c("column_name") or c.column_name to refer to existing columns.
+ Use c("column name") when the column name contains spaces, dots, punctuation, or special characters.
+ If a new column depends on another new column created in the same step, usually chain another .with_columns(...).

This file intentionally ignores pandas df.eval(), because Polars does not use a pandas-style eval string API.
Polars uses expressions instead.
'''

from pathlib import Path

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_float_precision(4)


data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

lf_baseball = pl.scan_csv(
    data_dir / "baseball.csv",
    schema_overrides={"Team": pl.Categorical},
).select("Name", "Team", "Height", "Weight")

print(lf_baseball.head(3).collect())
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬────────┐
# │ Name            ┆ Team ┆ Height ┆ Weight │
# │ ---             ┆ ---  ┆ ---    ┆ ---    │
# │ str             ┆ cat  ┆ i64    ┆ i64    │
# ╞═════════════════╪══════╪════════╪════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    │
# └─────────────────┴──────┴────────┴────────┘

print(lf_baseball.collect().schema)
# Schema({'Name': String, 'Team': Categorical, 'Height': Int64, 'Weight': Int64})


# =========================================================================================
# 1. Polars equivalent of df["col_name"] = ...
# =========================================================================================

##---------------------------------##
##     Modify existing columns     ##
##---------------------------------##
'''
Pandas:
    df["Height"] = df["Height"] * 2.54

Polars:
    df = df.with_columns(c("Height") * 2.54)

If the expression keeps the same column name, it replaces the existing column.
'''

# ## Modify a single column: Height from inches to cm
# 
lf_demo = lf_baseball.with_columns(
    (c("Height") * 2.54).alias("Height")
)

print(lf_demo.head(3).collect())
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬────────┐
# │ Name            ┆ Team ┆ Height ┆ Weight │
# │ ---             ┆ ---  ┆ ---    ┆ ---    │
# │ str             ┆ cat  ┆ f64    ┆ i64    │
# ╞═════════════════╪══════╪════════╪════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 187.96 ┆ 180    │
# │ Paul_Bako       ┆ BAL  ┆ 187.96 ┆ 215    │
# │ Ramon_Hernandez ┆ BAL  ┆ 182.88 ┆ 210    │
# └─────────────────┴──────┴────────┴────────┘

# ## Modify a string/categorical column: Team to lowercase
# '''
For string operations, use the .str namespace.
Because Team is categorical here, cast to String first, transform, then cast back to Categorical.
'''

lf_demo = lf_baseball.with_columns(
    c("Team").cast(pl.String).str.to_lowercase().cast(pl.Categorical).alias("Team")
)

print(lf_demo.head(3).collect())
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬────────┐
# │ Name            ┆ Team ┆ Height ┆ Weight │
# │ ---             ┆ ---  ┆ ---    ┆ ---    │
# │ str             ┆ cat  ┆ i64    ┆ i64    │
# ╞═════════════════╪══════╪════════╪════════╡
# │ Adam_Donachie   ┆ bal  ┆ 74     ┆ 180    │
# │ Paul_Bako       ┆ bal  ┆ 74     ┆ 215    │
# │ Ramon_Hernandez ┆ bal  ┆ 72     ┆ 210    │
# └─────────────────┴──────┴────────┴────────┘

# ## Modify multiple existing columns
# 
lf_demo = lf_baseball.with_columns(
    (c("Height") * 2.54).alias("Height"),
    (c("Weight") * 0.453592).alias("Weight"),
    c("Team").cast(pl.String).str.to_lowercase().cast(pl.Categorical).alias("Team"),
)

print(lf_demo.head(3).collect())
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬─────────┐
# │ Name            ┆ Team ┆ Height ┆ Weight  │
# │ ---             ┆ ---  ┆ ---    ┆ ---     │
# │ str             ┆ cat  ┆ f64    ┆ f64     │
# ╞═════════════════╪══════╪════════╪═════════╡
# │ Adam_Donachie   ┆ bal  ┆ 187.96 ┆ 81.6466 │
# │ Paul_Bako       ┆ bal  ┆ 187.96 ┆ 97.5223 │
# │ Ramon_Hernandez ┆ bal  ┆ 182.88 ┆ 95.2543 │
# └─────────────────┴──────┴────────┴─────────┘

##----------------------------##
##     Derive new columns     ##
##----------------------------##
'''
Pandas:
    df["Height_m"] = df["Height"] * 0.0254

Polars:
    df = df.with_columns((c("Height") * 0.0254).alias("Height_m"))

If the alias is a new name, Polars adds a new column.
'''

# ## Derive a single new column
# 
lf_demo = lf_baseball.with_columns(
    (c("Height") * 0.0254).alias("Height_m")
)

print(lf_demo.head(3).collect())
# shape: (3, 5)
# ┌─────────────────┬──────┬────────┬────────┬──────────┐
# │ Name            ┆ Team ┆ Height ┆ Weight ┆ Height_m │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---      │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64      │
# ╞═════════════════╪══════╪════════╪════════╪══════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 1.8796   │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 1.8796   │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 1.8288   │
# └─────────────────┴──────┴────────┴────────┴──────────┘

# ## Derive multiple independent new columns
# 
lf_demo = lf_baseball.with_columns(
    (c("Height") * 0.0254).alias("Height_m"),
    (c("Weight") * 0.453592).alias("Weight_kg"),
)

print(lf_demo.head(3).collect())
# shape: (3, 6)
# ┌─────────────────┬──────┬────────┬────────┬──────────┬───────────┐
# │ Name            ┆ Team ┆ Height ┆ Weight ┆ Height_m ┆ Weight_kg │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---      ┆ ---       │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64      ┆ f64       │
# ╞═════════════════╪══════╪════════╪════════╪══════════╪═══════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 1.8796   ┆ 81.6466   │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 1.8796   ┆ 97.5223   │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 1.8288   ┆ 95.2543   │
# └─────────────────┴──────┴────────┴────────┴──────────┴───────────┘

# ## Derive a column from original columns directly
# '''
BMI can be computed directly from original Height and Weight.
This avoids needing to refer to newly-created intermediate columns.
'''

lf_demo = lf_baseball.with_columns(
    (
        (c("Weight") * 0.453592) / ((c("Height") * 0.0254) ** 2)
    ).alias("BMI")
)

print(lf_demo.head(3).collect())
# shape: (3, 5)
# ┌─────────────────┬──────┬────────┬────────┬─────────┐
# │ Name            ┆ Team ┆ Height ┆ Weight ┆ BMI     │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---     │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64     │
# ╞═════════════════╪══════╪════════╪════════╪═════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 23.1104 │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 27.6041 │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 28.4808 │
# └─────────────────┴──────┴────────┴────────┴─────────┘

# ## Derive columns that depend on newly-created columns
# '''
Important Polars pattern:
If BMI depends on Height_m and Weight_kg, use a second .with_columns(...).

Reason:
Expressions in the same .with_columns(...) call are normally evaluated from the input DataFrame.
So a brand-new column is not the best thing to reference immediately in the same call.
'''

lf_demo = (
    lf_baseball
    .with_columns(
        (c("Height") * 0.0254).alias("Height_m"),
        (c("Weight") * 0.453592).alias("Weight_kg"),
    )
    .with_columns(
        (c("Weight_kg") / (c("Height_m") ** 2)).alias("BMI")
    )
)

print(lf_demo.head(3).collect())
# shape: (3, 7)
# ┌─────────────────┬──────┬────────┬────────┬──────────┬───────────┬─────────┐
# │ Name            ┆ Team ┆ Height ┆ Weight ┆ Height_m ┆ Weight_kg ┆ BMI     │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---      ┆ ---       ┆ ---     │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64      ┆ f64       ┆ f64     │
# ╞═════════════════╪══════╪════════╪════════╪══════════╪═══════════╪═════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 1.8796   ┆ 81.6466   ┆ 23.1104 │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 1.8796   ┆ 97.5223   ┆ 27.6041 │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 1.8288   ┆ 95.2543   ┆ 28.4808 │
# └─────────────────┴──────┴────────┴────────┴──────────┴───────────┴─────────┘


# =========================================================================================
# 2. Polars equivalent of df.assign()
# =========================================================================================

##---------------------------------##
##     Modify existing columns     ##
##---------------------------------##
'''
Pandas:
    df.assign(Weight=lambda df: df["Weight"] * 0.453592)

Polars:
    df.with_columns(Weight=c("Weight") * 0.453592)

Keyword syntax is concise when the output column name is a valid Python identifier.
'''

# ## Modify a single column using keyword syntax
# 
lf_demo = lf_baseball.with_columns(
    Weight=c("Weight") * 0.453592
)

print(lf_demo.head(3).collect())
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬─────────┐
# │ Name            ┆ Team ┆ Height ┆ Weight  │
# │ ---             ┆ ---  ┆ ---    ┆ ---     │
# │ str             ┆ cat  ┆ i64    ┆ f64     │
# ╞═════════════════╪══════╪════════╪═════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 81.6466 │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 97.5223 │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 95.2543 │
# └─────────────────┴──────┴────────┴─────────┘

# ## Modify multiple columns using keyword syntax
# 
lf_demo = lf_baseball.with_columns(
    Height=c("Height") * 2.54,
    Weight=c("Weight") * 0.453592,
    Team=c("Team").cast(pl.String).str.to_lowercase().cast(pl.Categorical),
)

print(lf_demo.head(3).collect())
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬─────────┐
# │ Name            ┆ Team ┆ Height ┆ Weight  │
# │ ---             ┆ ---  ┆ ---    ┆ ---     │
# │ str             ┆ cat  ┆ f64    ┆ f64     │
# ╞═════════════════╪══════╪════════╪═════════╡
# │ Adam_Donachie   ┆ bal  ┆ 187.96 ┆ 81.6466 │
# │ Paul_Bako       ┆ bal  ┆ 187.96 ┆ 97.5223 │
# │ Ramon_Hernandez ┆ bal  ┆ 182.88 ┆ 95.2543 │
# └─────────────────┴──────┴────────┴─────────┘

##----------------------------##
##     Derive new columns     ##
##----------------------------##

# ## Derive a single new column using keyword syntax
# 
lf_demo = lf_baseball.with_columns(
    BMI=(c("Weight") * 0.453592) / ((c("Height") * 0.0254) ** 2)
)

print(lf_demo.head(3).collect())
# shape: (3, 5)
# columns: Name, Team, Height, Weight, BMI

# ## Add a literal/scalar column
# '''
Non-expression values are often wrapped with pl.lit(...).
A scalar literal is broadcast to every row.
'''

lf_demo = lf_baseball.with_columns(
    Raise=pl.lit(True)
)

print(lf_demo.head(3).collect())
# shape: (3, 5)
# columns: Name, Team, Height, Weight, Raise

# ## Add a column from a Python list
# '''
For row-by-row values from Python, pass a Series or a list literal.
Make sure the list length matches the DataFrame height.
'''

raise_values = [i % 2 == 0 for i in range(lf_baseball.collect().height)]

lf_demo = lf_baseball.with_columns(
    pl.Series("Raise", raise_values)
)

print(lf_demo.head(3).collect())
# shape: (3, 5)
# ┌─────────────────┬──────┬────────┬────────┬───────┐
# │ Name            ┆ Team ┆ Height ┆ Weight ┆ Raise │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---   │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ bool  │
# ╞═════════════════╪══════╪════════╪════════╪═══════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ true  │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ false │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ true  │
# └─────────────────┴──────┴────────┴────────┴───────┘

# ## Derive multiple new columns
# 
lf_demo = (
    lf_baseball
    .with_columns(
        Height_cm=c("Height") * 2.54,
        Height_m=c("Height") * 0.0254,
        Weight_kg=c("Weight") * 0.453592,
    )
    .with_columns(
        BMI=c("Weight_kg") / (c("Height_m") ** 2)
    )
)

print(lf_demo.head(3).collect())
# shape: (3, 8)
# columns: Name, Team, Height, Weight, Height_cm, Height_m, Weight_kg, BMI

##---------------------------------------------------------------##
## Using **{...} for names that are not valid Python identifiers ##
##---------------------------------------------------------------##
'''
Keyword syntax only works for valid Python identifiers:

    df.with_columns(height_cm=...)

If the new column has spaces, dots, punctuation, or conflicts with a Python keyword,
use positional expressions with .alias("...") or unpack a dictionary with **{...}.
'''

# ## Add a "raise" column
# '''
"raise" is a Python keyword, so it is clearer to use alias(...).
'''

lf_demo = lf_baseball.with_columns(
    pl.Series("raise", raise_values)
)

print(lf_demo.head(3).collect())
# shape: (3, 5)
# columns: Name, Team, Height, Weight, raise

# ## Add columns with spaces/special characters
# 
lf_demo = lf_baseball.with_columns(
    ((c("Height") * 2.54).alias("Height cm")),
    ((c("Weight") * 0.453592).alias("Weight kg")),
)

print(lf_demo.head(3).collect())
# shape: (3, 6)
# columns include: Height cm, Weight kg

# Because these names contain spaces, refer to them with c("...") later.
lf_demo = lf_demo.with_columns(
    (c("Weight kg") / ((c("Height cm") / 100) ** 2)).alias("BMI score")
)

print(lf_demo.head(3).collect())
# shape: (3, 7)
# columns include: Height cm, Weight kg, BMI score

# ## Dictionary unpacking style
# '''
This is the closest visual equivalent to pandas assign(**{...}).
'''

lf_demo = lf_baseball.with_columns(**{
    "height_cm": c("Height") * 2.54,
    "weight_kg": c("Weight") * 0.453592,
})

print(lf_demo.head(3).collect())
# shape: (3, 6)
# columns: Name, Team, Height, Weight, height_cm, weight_kg

# ## Apply the same transformation to several columns
# '''
Pandas often uses assign(**{col: ... for col in cols}).
In Polars, build a list of expressions.
'''

cols_to_float = ["Height", "Weight"]

lf_demo = lf_baseball.with_columns(
    [c(col).cast(pl.Float64).alias(col) for col in cols_to_float]
)

print(lf_demo.head(5).collect())
# shape: (5, 4)
# columns Height and Weight are now Float64

# ## Use c.column_name shorthand when names are simple
# '''
Because we imported:

    from polars import col as c

we can use either:

    c("Height")
    c.Height

For simple column names, c.Height is concise.
For special names, always use c("column name").
'''

lf_demo = lf_baseball.with_columns(
    height_to_weight_ratio=c.Height / c.Weight
)

print(lf_demo.head(3).collect())
# shape: (3, 5)
# columns: Name, Team, Height, Weight, height_to_weight_ratio


# =========================================================================================
# 3. Quick summary
# =========================================================================================
'''
Pandas -> Polars mental map

1. Modify existing column
   pandas: df["Height"] = df["Height"] * 2.54
   polars: df = df.with_columns(Height=c("Height") * 2.54)

2. Add new column
   pandas: df["Height_m"] = df["Height"] * 0.0254
   polars: df = df.with_columns(Height_m=c("Height") * 0.0254)

3. assign(...)
   pandas: df.assign(BMI=lambda df: ...)
   polars: df.with_columns(BMI=...)

4. assign(**{...})
   pandas: df.assign(**{"new col": ...})
   polars: df.with_columns((...).alias("new col"))

5. eval(...)
   pandas: df.eval("BMI = Weight / Height ** 2")
   polars: use expressions with with_columns(...), not eval strings.
'''
