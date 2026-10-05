'''
In Polars, the main tool for both modifying existing columns or deriving new columns is:

    lf.with_columns(...)

NOTE: we also have `expr.map_elements()` but it is less optimized

1. `lf.with_columns(expr.alias("name"))`
2. `lf.with_columns(name = expr)`
3. `lf.with_columns(expr.map_elements(func/lambda))`: map a custom/user-defined function (UDF) to each element of a column.
4. `lf.with_columns(**{"name": expr})`: avoid overlapping with Python keywords
'''

from pathlib import Path

import numpy as np
import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(12)
pl.Config.set_float_precision(4)

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

lf_baseball = (
     pl.scan_csv(
        data_dir/"baseball.csv",
        schema_overrides={"Team": pl.Categorical},
    )
    .select("Name", "Team", "Height", "Weight")
    .select(pl.all().name.to_lowercase())
)

print(lf_baseball.head(3).collect())
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬────────┐
# │ name            ┆ team ┆ height ┆ weight │
# │ ---             ┆ ---  ┆ ---    ┆ ---    │
# │ str             ┆ cat  ┆ i64    ┆ i64    │
# ╞═════════════════╪══════╪════════╪════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    │
# └─────────────────┴──────┴────────┴────────┘

print(lf_baseball.collect().schema)
# Schema({'name': String, 'team': Categorical, 'height': Int64, 'weight': Int64})

# =========================================================================================
# 1. `lf.with_columns(expr.alias("name"))`
# =========================================================================================

##---------------------------------##
##     Modify existing columns     ##
##---------------------------------##

print(
    lf_baseball
    .with_columns(
        (c("height") * 2.54).alias("height")
    )
    .head(3)
    .collect()
)
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬────────┐
# │ name            ┆ team ┆ height ┆ weight │
# │ ---             ┆ ---  ┆ ---    ┆ ---    │
# │ str             ┆ cat  ┆ f64    ┆ i64    │
# ╞═════════════════╪══════╪════════╪════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 187.96 ┆ 180    │
# │ Paul_Bako       ┆ BAL  ┆ 187.96 ┆ 215    │
# │ Ramon_Hernandez ┆ BAL  ┆ 182.88 ┆ 210    │
# └─────────────────┴──────┴────────┴────────┘

print(
    lf_baseball
    .with_columns(
        c("team").cast(pl.String).str.to_lowercase().cast(pl.Categorical).alias("team")
    )
    .head(3)
    .collect()
)
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬────────┐
# │ name            ┆ team ┆ height ┆ weight │
# │ ---             ┆ ---  ┆ ---    ┆ ---    │
# │ str             ┆ cat  ┆ i64    ┆ i64    │
# ╞═════════════════╪══════╪════════╪════════╡
# │ Adam_Donachie   ┆ bal  ┆ 74     ┆ 180    │
# │ Paul_Bako       ┆ bal  ┆ 74     ┆ 215    │
# │ Ramon_Hernandez ┆ bal  ┆ 72     ┆ 210    │
# └─────────────────┴──────┴────────┴────────┘

# Modify multiple existing columns
print(
    lf_baseball.with_columns(
        (c("height") * 2.54).alias("height"),
        (c("weight") * 0.453592).alias("weight"),
        c("team").cast(pl.String).str.to_lowercase().cast(pl.Categorical).alias("team"),
    )
    .head(3)
    .collect()
)
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬─────────┐
# │ name            ┆ team ┆ height ┆ weight  │
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

print(
    lf_baseball
    .with_columns(
        (c("height") * 2.54).alias("height_m")
    )
    .head(3)
    .collect()
)
# shape: (3, 5)
# ┌─────────────────┬──────┬────────┬────────┬──────────┐
# │ name            ┆ team ┆ height ┆ weight ┆ height_m │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---      │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64      │
# ╞═════════════════╪══════╪════════╪════════╪══════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 1.8796   │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 1.8796   │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 1.8288   │
# └─────────────────┴──────┴────────┴────────┴──────────┘

# Derive multiple independent new columns
print(
    lf_baseball.with_columns(
        (c("height") * 2.54).alias("height_m"),
        (c("weight") * 0.453592).alias("weight_kg"),
        c("team").cast(pl.String).str.to_lowercase().cast(pl.Categorical).alias("team"),
    )
    .head(3)
    .collect()
)
# shape: (3, 6)
# ┌─────────────────┬──────┬────────┬────────┬──────────┬───────────┐
# │ name            ┆ team ┆ height ┆ weight ┆ height_m ┆ weight_kg │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---      ┆ ---       │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64      ┆ f64       │
# ╞═════════════════╪══════╪════════╪════════╪══════════╪═══════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 1.8796   ┆ 81.6466   │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 1.8796   ┆ 97.5223   │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 1.8288   ┆ 95.2543   │
# └─────────────────┴──────┴────────┴────────┴──────────┴───────────┘

# Derive a column from original columns directly
print(
    lf_baseball
    .with_columns(
        ((c("weight") * 0.453592) / ((c("height") * 0.0254) ** 2)).alias("bmi")
    )
    .head(3)
    .collect()
)
# shape: (3, 5)
# ┌─────────────────┬──────┬────────┬────────┬─────────┐
# │ name            ┆ team ┆ height ┆ weight ┆ bmi     │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---     │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64     │
# ╞═════════════════╪══════╪════════╪════════╪═════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 23.1104 │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 27.6041 │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 28.4808 │
# └─────────────────┴──────┴────────┴────────┴─────────┘

# Derive columns that depend on newly-created columns
'''
Important Polars pattern:
if bmi depends on height_m and weight_kg, use a second .with_columns(...).

Reason:
Expressions in the same .with_columns(...) call are normally evaluated in parallel.
Therefore, if a derived column depends on another not yet present derived column,
it will fail.
'''

print(
    lf_baseball
    .with_columns(
        (c("height") * 0.0254).alias("height_m"),
        (c("weight") * 0.453592).alias("weight_kg"),
    )
    .with_columns(
        (c("weight_kg") / (c("height_m") ** 2)).alias("bmi")
    )
    .head(3)
    .collect()
)
# shape: (3, 7)
# ┌─────────────────┬──────┬────────┬────────┬──────────┬───────────┬─────────┐
# │ name            ┆ team ┆ height ┆ weight ┆ height_m ┆ weight_kg ┆ bmi     │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---      ┆ ---       ┆ ---     │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64      ┆ f64       ┆ f64     │
# ╞═════════════════╪══════╪════════╪════════╪══════════╪═══════════╪═════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 1.8796   ┆ 81.6466   ┆ 23.1104 │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 1.8796   ┆ 97.5223   ┆ 27.6041 │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 1.8288   ┆ 95.2543   ┆ 28.4808 │
# └─────────────────┴──────┴────────┴────────┴──────────┴───────────┴─────────┘

# =========================================================================================
# 2. `lf.with_columns(name = expr)`
# =========================================================================================

##---------------------------------##
##     Modify existing columns     ##
##---------------------------------##

print(
    lf_baseball
    .with_columns(
        height = c("height") * 2.54
    )
    .head(3)
    .collect()
)
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬────────┐
# │ name            ┆ team ┆ height ┆ weight │
# │ ---             ┆ ---  ┆ ---    ┆ ---    │
# │ str             ┆ cat  ┆ f64    ┆ i64    │
# ╞═════════════════╪══════╪════════╪════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 187.96 ┆ 180    │
# │ Paul_Bako       ┆ BAL  ┆ 187.96 ┆ 215    │
# │ Ramon_Hernandez ┆ BAL  ┆ 182.88 ┆ 210    │
# └─────────────────┴──────┴────────┴────────┘

print(
    lf_baseball
    .with_columns(
        team = c("team").cast(pl.String).str.to_lowercase().cast(pl.Categorical)
    )
    .head(3)
    .collect()
)
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬────────┐
# │ name            ┆ team ┆ height ┆ weight │
# │ ---             ┆ ---  ┆ ---    ┆ ---    │
# │ str             ┆ cat  ┆ i64    ┆ i64    │
# ╞═════════════════╪══════╪════════╪════════╡
# │ Adam_Donachie   ┆ bal  ┆ 74     ┆ 180    │
# │ Paul_Bako       ┆ bal  ┆ 74     ┆ 215    │
# │ Ramon_Hernandez ┆ bal  ┆ 72     ┆ 210    │
# └─────────────────┴──────┴────────┴────────┘

# Modify multiple existing columns
print(
    lf_baseball.with_columns(
        height = (c("height") * 2.54),
        weight = (c("weight") * 0.453592),
        team = c("team").cast(pl.String).str.to_lowercase().cast(pl.Categorical)
    )
    .head(3)
    .collect()
)
# shape: (3, 4)
# ┌─────────────────┬──────┬────────┬─────────┐
# │ name            ┆ team ┆ height ┆ weight  │
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

print(
    lf_baseball
    .with_columns(
        height_m = c("height") * 2.54
    )
    .head(3)
    .collect()
)
# shape: (3, 5)
# ┌─────────────────┬──────┬────────┬────────┬──────────┐
# │ name            ┆ team ┆ height ┆ weight ┆ height_m │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---      │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64      │
# ╞═════════════════╪══════╪════════╪════════╪══════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 1.8796   │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 1.8796   │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 1.8288   │
# └─────────────────┴──────┴────────┴────────┴──────────┘

# Derive multiple independent new columns
print(
    lf_baseball.with_columns(
        height_m = c("height") * 2.54,
        weight_kg = c("weight") * 0.453592,
        team = c("team").cast(pl.String).str.to_lowercase().cast(pl.Categorical),
    )
    .head(3)
    .collect()
)
# shape: (3, 6)
# ┌─────────────────┬──────┬────────┬────────┬──────────┬───────────┐
# │ name            ┆ team ┆ height ┆ weight ┆ height_m ┆ weight_kg │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---      ┆ ---       │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64      ┆ f64       │
# ╞═════════════════╪══════╪════════╪════════╪══════════╪═══════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 1.8796   ┆ 81.6466   │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 1.8796   ┆ 97.5223   │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 1.8288   ┆ 95.2543   │
# └─────────────────┴──────┴────────┴────────┴──────────┴───────────┘

# Derive a column from original columns directly
print(
    lf_baseball
    .with_columns(
        bmi = (c("weight") * 0.453592) / ((c("height") * 0.0254) ** 2)
    )
    .head(3)
    .collect()
)
# shape: (3, 5)
# ┌─────────────────┬──────┬────────┬────────┬─────────┐
# │ name            ┆ team ┆ height ┆ weight ┆ bmi     │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---     │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64     │
# ╞═════════════════╪══════╪════════╪════════╪═════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 23.1104 │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 27.6041 │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 28.4808 │
# └─────────────────┴──────┴────────┴────────┴─────────┘

# Derive columns that depend on newly-created columns
'''
Important Polars pattern:
if bmi depends on height_m and weight_kg, use a second .with_columns(...).
'''

print(
    lf_baseball
    .with_columns(
        height_m = c("height") * 0.0254,
        weight_kg = c("weight") * 0.453592,
    )
    .with_columns(
        bmi = c("weight_kg") / (c("height_m") ** 2)
    )
    .head(3)
    .collect()
)
# shape: (3, 7)
# ┌─────────────────┬──────┬────────┬────────┬──────────┬───────────┬─────────┐
# │ name            ┆ team ┆ height ┆ weight ┆ height_m ┆ weight_kg ┆ bmi     │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---      ┆ ---       ┆ ---     │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ f64      ┆ f64       ┆ f64     │
# ╞═════════════════╪══════╪════════╪════════╪══════════╪═══════════╪═════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ 1.8796   ┆ 81.6466   ┆ 23.1104 │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ 1.8796   ┆ 97.5223   ┆ 27.6041 │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ 1.8288   ┆ 95.2543   ┆ 28.4808 │
# └─────────────────┴──────┴────────┴────────┴──────────┴───────────┴─────────┘

# =========================================================================================
# 3. `lf.with_columns(expr.map_elements(func/lambda))`
# =========================================================================================
'''
`pl.col("name").map_elements()`:
Map a custom/user-defined function (UDF) to each element of a column.

To create a brandnew column from existing columns,
wrap existing columns into a struct, then apply `.map_elements` on that struct
'''

print(
    lf_baseball
    .with_columns(
        c("height").map_elements(lambda x: x * 0.0254),
        c("weight").map_elements(lambda x: x * 0.453592)
    )
    .with_columns(
        bmi = pl.struct(["height","weight"]).map_elements(
            lambda s: s.get("weight") / (s.get("height") ** 2),
            return_dtype=pl.Float64 # MUST HAVE DTYPE
        )#.alias("bmi")
    )
    .collect()
)
# shape: (1_015, 5)
# ┌─────────────────┬──────┬────────┬─────────┬─────────┐
# │ name            ┆ team ┆ height ┆ weight  ┆ bmi     │
# │ ---             ┆ ---  ┆ ---    ┆ ---     ┆ ---     │
# │ str             ┆ cat  ┆ f64    ┆ f64     ┆ f64     │
# ╞═════════════════╪══════╪════════╪═════════╪═════════╡
# │ Adam_Donachie   ┆ BAL  ┆ 1.8796 ┆ 81.6466 ┆ 23.1104 │
# │ Paul_Bako       ┆ BAL  ┆ 1.8796 ┆ 97.5223 ┆ 27.6041 │
# │ Ramon_Hernandez ┆ BAL  ┆ 1.8288 ┆ 95.2543 ┆ 28.4808 │
# │ Kevin_Millar    ┆ BAL  ┆ 1.8288 ┆ 95.2543 ┆ 28.4808 │
# │ Chris_Gomez     ┆ BAL  ┆ 1.8542 ┆ 85.2753 ┆ 24.8033 │
# │ Brian_Roberts   ┆ BAL  ┆ 1.7526 ┆ 79.8322 ┆ 25.9904 │
# │ …               ┆ …    ┆ …      ┆ …       ┆ …       │
# │ Josh_Hancock    ┆ STL  ┆ 1.9050 ┆ 92.9864 ┆ 25.6230 │
# │ Brad_Thompson   ┆ STL  ┆ 1.8542 ┆ 86.1825 ┆ 25.0672 │
# │ Tyler_Johnson   ┆ STL  ┆ 1.8796 ┆ 81.6466 ┆ 23.1104 │
# │ Chris_Narveson  ┆ STL  ┆ 1.9050 ┆ 92.9864 ┆ 25.6230 │
# │ Randy_Keisler   ┆ STL  ┆ 1.9050 ┆ 86.1825 ┆ 23.7481 │
# │ Josh_Kinney     ┆ STL  ┆ 1.8542 ┆ 88.4504 ┆ 25.7269 │
# └─────────────────┴──────┴────────┴─────────┴─────────┘
# /tmp/ipykernel_85139/1261794888.py:4: PolarsInefficientMapWarning:
# Expr.map_elements is significantly slower than the native expressions API.
# Only use if you absolutely CANNOT implement your logic otherwise.
# Replace this expression...
#   - pl.col("height").map_elements(lambda x: ...)
# with this one instead:
#   + pl.col("height") * 0.0254
#   c("height").map_elements(lambda x: x * 0.0254),
# /tmp/ipykernel_85139/1261794888.py:5: PolarsInefficientMapWarning:
# Expr.map_elements is significantly slower than the native expressions API.
# Only use if you absolutely CANNOT implement your logic otherwise.
# Replace this expression...
#   - pl.col("weight").map_elements(lambda x: ...)
# with this one instead:
#   + pl.col("weight") * 0.453592
#   c("weight").map_elements(lambda x: x * 0.453592)

# =========================================================================================
# 4. `lf.with_columns(**{"name": expr})`: avoid overlapping with Python keywords
# =========================================================================================

print(
    lf_baseball
    .with_columns(**{
        "raise": c("height").map_elements(lambda _: np.random.rand() > 0.5) # True if > 0.5, else False
    })
    .collect()
)
# shape: (1_015, 5)
# ┌─────────────────┬──────┬────────┬────────┬───────┐
# │ name            ┆ team ┆ height ┆ weight ┆ raise │
# │ ---             ┆ ---  ┆ ---    ┆ ---    ┆ ---   │
# │ str             ┆ cat  ┆ i64    ┆ i64    ┆ bool  │
# ╞═════════════════╪══════╪════════╪════════╪═══════╡
# │ Adam_Donachie   ┆ BAL  ┆ 74     ┆ 180    ┆ false │
# │ Paul_Bako       ┆ BAL  ┆ 74     ┆ 215    ┆ false │
# │ Ramon_Hernandez ┆ BAL  ┆ 72     ┆ 210    ┆ false │
# │ Kevin_Millar    ┆ BAL  ┆ 72     ┆ 210    ┆ true  │
# │ Chris_Gomez     ┆ BAL  ┆ 73     ┆ 188    ┆ true  │
# │ Brian_Roberts   ┆ BAL  ┆ 69     ┆ 176    ┆ true  │
# │ …               ┆ …    ┆ …      ┆ …      ┆ …     │
# │ Josh_Hancock    ┆ STL  ┆ 75     ┆ 205    ┆ true  │
# │ Brad_Thompson   ┆ STL  ┆ 73     ┆ 190    ┆ false │
# │ Tyler_Johnson   ┆ STL  ┆ 74     ┆ 180    ┆ false │
# │ Chris_Narveson  ┆ STL  ┆ 75     ┆ 205    ┆ true  │
# │ Randy_Keisler   ┆ STL  ┆ 75     ┆ 190    ┆ false │
# │ Josh_Kinney     ┆ STL  ┆ 73     ┆ 195    ┆ true  │
# └─────────────────┴──────┴────────┴────────┴───────┘
