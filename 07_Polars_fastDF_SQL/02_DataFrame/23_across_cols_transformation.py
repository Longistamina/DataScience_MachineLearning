'''
Column-wise selection, transformation, summarisation, and reframing in Polars

This file demonstrates common Polars patterns for applying one idea across many
columns. Polars does not need a special "across" API because expressions and
selectors already work column-wise.

1. Apply one operation to every column with `pl.all()`
2. Transform columns selected by dtype using selectors `cs`
3. Summarize columns selected by dtype with selector `cs`
4. Reframe summaries into rows with `pl.concat()` and `getattr()`
5. Dynamic column selection with `.pipe()`
'''

from pathlib import Path

import polars as pl
import polars.selectors as cs
from polars import col as c

# Optional display settings
pl.Config.set_tbl_rows(10)
pl.Config.set_tbl_cols(20)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(130)

# =========================================================================================
# 0. Setup Data
# =========================================================================================

data_dir = next(Path.home().rglob("*/DataScience_MachineLearning/data"))

lf_pokemon = (
    pl.scan_csv(data_dir / "pokemon.csv")
    .drop("#")
    .rename(lambda name: name.strip())
    .select(pl.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .with_columns(
        c("type_1", "type_2").cast(pl.Categorical),
        c("legendary").cast(pl.Boolean),
    )
    .pipe(lambda f: f.with_columns(
        c("generation").cast(pl.String).cast(pl.Enum(f.select("generation").collect().to_series().cast(pl.String).unique().sort())),
    ))                                               # Must use .collect() to realize the dataframe, to access the values for Enum casting
)

print(lf_pokemon.head(5).collect())
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ name           ┆ type_1 ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
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

# =========================================================================================
# 1. Apply one operation to every column with `pl.all()`
# =========================================================================================
'''
Concept:
Apply one operation to every column.

Polars:
Use `pl.all()` when the expression should target every column.

Notes:
- Use `.select(...)` when you are producing a selected/summary result.
- Use `.with_columns(...)` when you want to replace columns but keep the same
  row count.
- For dtype metadata, use `.collect_schema()` instead of collecting the full data.
'''

##-----------------------------------##
## Count null values in every column ##
##-----------------------------------##

print(
    lf_pokemon
    .select(
        pl.all().is_null().sum()
    )
    .collect()
)
# shape: (1, 12)
# ┌──────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ name ┆ type_1 ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ ---  ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ u32  ┆ u32    ┆ u32    ┆ u32   ┆ u32 ┆ u32    ┆ u32     ┆ u32    ┆ u32    ┆ u32   ┆ u32        ┆ u32       │
# ╞══════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ 0    ┆ 0      ┆ 386    ┆ 0     ┆ 0   ┆ 0      ┆ 0       ┆ 0      ┆ 0      ┆ 0     ┆ 0          ┆ 0         │
# └──────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##-------------------------------------##
## Count unique values in every column ##
##-------------------------------------##

print(
    lf_pokemon
    .select(
        pl.all().n_unique().sum()
    )
    .collect()
)
# shape: (1, 12)
# ┌──────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ name ┆ type_1 ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ ---  ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ u32  ┆ u32    ┆ u32    ┆ u32   ┆ u32 ┆ u32    ┆ u32     ┆ u32    ┆ u32    ┆ u32   ┆ u32        ┆ u32       │
# ╞══════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ 800  ┆ 18     ┆ 19     ┆ 200   ┆ 94  ┆ 111    ┆ 103     ┆ 105    ┆ 92     ┆ 108   ┆ 6          ┆ 2         │
# └──────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

# =========================================================================================
# 2. Transform columns selected by dtype using selectors `cs`
# =========================================================================================
'''
Concept:
Apply a transformation only to columns that satisfy a condition, such as numeric,
string, or boolean columns.

Polars:
Use `polars.selectors` for dtype-based column selection.

Common selectors:
- `cs.numeric()` selects numeric columns.
- `cs.string()` selects string columns.
- `cs.boolean()` selects boolean columns.
- `.exclude(...)` removes columns from a selector.

Use `.with_columns(...)` for row-preserving transformations.
'''

##--------------------------------------------------##
## Log-transform all numeric columns except `total` ##
##--------------------------------------------------##

print(
    lf_pokemon.
    with_columns(
        cs.numeric().exclude('total').log()
    )
    .head(5)
    .collect()
)
# shape: (5, 12)
# ┌──────────────┬────────┬────────┬───────┬───────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ name         ┆ type_1 ┆ type_2 ┆ total ┆ hp    ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ ---          ┆ ---    ┆ ---    ┆ ---   ┆ ---   ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str          ┆ cat    ┆ cat    ┆ i64   ┆ f64   ┆ f64    ┆ f64     ┆ f64    ┆ f64    ┆ f64   ┆ enum       ┆ bool      │
# ╞══════════════╪════════╪════════╪═══════╪═══════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur    ┆ Grass  ┆ Poison ┆ 318   ┆ 3.807 ┆ 3.892  ┆ 3.892   ┆ 4.174  ┆ 4.174  ┆ 3.807 ┆ 1          ┆ false     │
# │ Ivysaur      ┆ Grass  ┆ Poison ┆ 405   ┆ 4.094 ┆ 4.127  ┆ 4.143   ┆ 4.382  ┆ 4.382  ┆ 4.094 ┆ 1          ┆ false     │
# │ Venusaur     ┆ Grass  ┆ Poison ┆ 525   ┆ 4.382 ┆ 4.407  ┆ 4.419   ┆ 4.605  ┆ 4.605  ┆ 4.382 ┆ 1          ┆ false     │
# │ VenusaurMega ┆ Grass  ┆ Poison ┆ 625   ┆ 4.382 ┆ 4.605  ┆ 4.812   ┆ 4.804  ┆ 4.787  ┆ 4.382 ┆ 1          ┆ false     │
# │ Venusaur     ┆        ┆        ┆       ┆       ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Charmander   ┆ Fire   ┆ null   ┆ 309   ┆ 3.664 ┆ 3.951  ┆ 3.761   ┆ 4.094  ┆ 3.912  ┆ 4.174 ┆ 1          ┆ false     │
# └──────────────┴────────┴────────┴───────┴───────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##----------------------------------------------------------------------------##
## Convert categorical-like columns to Polars Categorical dtype except `name` ##
##----------------------------------------------------------------------------##

print(
    lf_pokemon.
    with_columns(
        (cs.string().exclude("name") | cs.by_name('generation', 'legendary'))
        .cast(pl.String)
        .cast(pl.Categorical)
    )
    .head(5)
    .collect()
)
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ name           ┆ type_1 ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ ---            ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str            ┆ cat    ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ cat        ┆ cat       │
# ╞════════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur      ┆ Grass  ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Ivysaur        ┆ Grass  ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Venusaur       ┆ Grass  ┆ Poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ VenusaurMega   ┆ Grass  ┆ Poison ┆ 625   ┆ 80  ┆ 100    ┆ 123     ┆ 122    ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ Venusaur       ┆        ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Charmander     ┆ Fire   ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# └────────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##--------------------------------------------##
## Lowercase all string columns except `name` ##
##--------------------------------------------##

print(
    lf_pokemon
    .with_columns(cs.categorical().cast(pl.String)) # cast these to string for demonstration
    .with_columns(cs.string().exclude("name").str.to_lowercase())
    .head(5)
    .collect()
)
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ name           ┆ type_1 ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ ---            ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str            ┆ str    ┆ str    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞════════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur      ┆ grass  ┆ poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Ivysaur        ┆ grass  ┆ poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Venusaur       ┆ grass  ┆ poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ VenusaurMega   ┆ grass  ┆ poison ┆ 625   ┆ 80  ┆ 100    ┆ 123     ┆ 122    ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ Venusaur       ┆        ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Charmander     ┆ fire   ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# └────────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##-----------------------------------------------------------------##
## Example: transform selected columns and keep the original names ##
##-----------------------------------------------------------------##

print(
    lf_pokemon.
    with_columns(
        (cs.numeric() - cs.numeric().mean()) / cs.numeric().std()
    )
    .head(5)
    .collect()
)
# shape: (5, 12)
# ┌──────────────┬────────┬────────┬────────┬────────┬────────┬─────────┬────────┬────────┬────────┬────────────┬───────────┐
# │ name         ┆ type_1 ┆ type_2 ┆ total  ┆ hp     ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed  ┆ generation ┆ legendary │
# │ ---          ┆ ---    ┆ ---    ┆ ---    ┆ ---    ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---        ┆ ---       │
# │ str          ┆ cat    ┆ cat    ┆ f64    ┆ f64    ┆ f64    ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ enum       ┆ bool      │
# ╞══════════════╪════════╪════════╪════════╪════════╪════════╪═════════╪════════╪════════╪════════╪════════════╪═══════════╡
# │ Bulbasaur    ┆ Grass  ┆ Poison ┆ -0.976 ┆ -0.950 ┆ -0.924 ┆ -0.797  ┆ -0.239 ┆ -0.248 ┆ -0.801 ┆ 1          ┆ false     │
# │ Ivysaur      ┆ Grass  ┆ Poison ┆ -0.251 ┆ -0.363 ┆ -0.524 ┆ -0.348  ┆ 0.219  ┆ 0.291  ┆ -0.285 ┆ 1          ┆ false     │
# │ Venusaur     ┆ Grass  ┆ Poison ┆ 0.749  ┆ 0.421  ┆ 0.092  ┆ 0.294   ┆ 0.831  ┆ 1.010  ┆ 0.403  ┆ 1          ┆ false     │
# │ VenusaurMega ┆ Grass  ┆ Poison ┆ 1.583  ┆ 0.421  ┆ 0.647  ┆ 1.576   ┆ 1.503  ┆ 1.728  ┆ 0.403  ┆ 1          ┆ false     │
# │ Venusaur     ┆        ┆        ┆        ┆        ┆        ┆         ┆        ┆        ┆        ┆            ┆           │
# │ Charmander   ┆ Fire   ┆ null   ┆ -1.051 ┆ -1.185 ┆ -0.832 ┆ -0.989  ┆ -0.392 ┆ -0.787 ┆ -0.113 ┆ 1          ┆ false     │
# └──────────────┴────────┴────────┴────────┴────────┴────────┴─────────┴────────┴────────┴────────┴────────────┴───────────┘

# =========================================================================================
# 3. Summarize columns selected by dtype with selector `cs` and `getattr`
# =========================================================================================
'''
Concept:
Apply aggregation functions to many selected columns.

Polars:
Use `.select(...)` with selector expressions. When expressions like `.mean()`,
`.std()`, `.min()`, or `.max()` reduce each selected column to one value, the
result is a one-row DataFrame.
'''

##-------------------------------------------##
## Calculate the mean of all numeric columns ##
##-------------------------------------------##

print(
    lf_pokemon
    .select(
        cs.numeric().mean()
    )
    .collect()
)
# shape: (1, 7)
# ┌─────────┬────────┬────────┬─────────┬────────┬────────┬────────┐
# │ total   ┆ hp     ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed  │
# │ ---     ┆ ---    ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---    │
# │ f64     ┆ f64    ┆ f64    ┆ f64     ┆ f64    ┆ f64    ┆ f64    │
# ╞═════════╪════════╪════════╪═════════╪════════╪════════╪════════╡
# │ 435.103 ┆ 69.259 ┆ 79.001 ┆ 73.843  ┆ 72.820 ┆ 71.903 ┆ 68.278 │
# └─────────┴────────┴────────┴─────────┴────────┴────────┴────────┘

##---------------------------------------------------------##
## Calculate the standard deviation of all numeric columns ##
##---------------------------------------------------------##

print(
    lf_pokemon
    .select(
        cs.numeric().std()
    )
    .collect()
)

##-------------------------------------------------------------------##
## Calculate multiple summary statistics and suffix the output names ##
##-------------------------------------------------------------------##

print(
    lf_pokemon.select(
        cs.numeric().mean().name.suffix('_mean'),
        cs.numeric().std().name.suffix('_std'),
        cs.numeric().min().name.suffix('_min'),
        cs.numeric().max().name.suffix('_max'),
    )
    .collect()
)


# =========================================================================================
# 4. Reframe summaries into rows with `pl.concat()` and `getattr()`
# =========================================================================================
'''
Concept:
Return a result with a different number of rows than the original data.

Example:
For each selected numeric column, calculate Min, Q1, Median, Q3, and Max. The
summary names become rows.

Polars:
Use `pl.concat([...])` to stack multiple one-row summaries. This keeps the
calculation lazy and uses native Polars expressions.
'''

##--------------------------------------##
## `pl.concat()` for multiple quantiles ##
##--------------------------------------##

qs = [0.00, 0.25, 0.50, 0.75, 1.00]
labels = ['Min', 'Q1', 'Median', 'Q3', 'Max']

lf_percentile = pl.concat([
    lf_pokemon.select(
        pl.lit(label).alias('index'),
        cs.numeric().exclude('Generation').quantile(q)
    )
    for q, label in zip(qs, labels)
])

print(lf_percentile.collect())
# shape: (5, 8)
# ┌────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
# │ index  ┆ Total   ┆ HP      ┆ Attack  ┆ Defense ┆ Sp_Atk  ┆ Sp_Def  ┆ Speed   │
# │ ---    ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     │
# │ str    ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     │
# ╞════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╡
# │ Min    ┆ 180.000 ┆ 1.000   ┆ 5.000   ┆ 5.000   ┆ 10.000  ┆ 20.000  ┆ 5.000   │
# │ Q1     ┆ 330.000 ┆ 50.000  ┆ 55.000  ┆ 50.000  ┆ 50.000  ┆ 50.000  ┆ 45.000  │
# │ Median ┆ 450.000 ┆ 65.000  ┆ 75.000  ┆ 70.000  ┆ 65.000  ┆ 70.000  ┆ 65.000  │
# │ Q3     ┆ 515.000 ┆ 80.000  ┆ 100.000 ┆ 90.000  ┆ 95.000  ┆ 90.000  ┆ 90.000  │
# │ Max    ┆ 780.000 ┆ 255.000 ┆ 190.000 ┆ 230.000 ┆ 194.000 ┆ 230.000 ┆ 180.000 │
# └────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

##---------------------------------------------------------------------##
## `pl.concat()` and `getattr()` to wrap aggregated results vertically ##
##---------------------------------------------------------------------##

aggs = ["mean", "std", "min", "max"]
print(
    pl.concat(
        [
            lf_pokemon.select(getattr(cs.numeric(), agg)())
            for agg in aggs
        ],
        how="vertical_relaxed",
    )
    .select(pl.Series("summary", aggs), pl.all())
    .collect()
)
# shape: (4, 8)
# ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
# │ summary ┆ total   ┆ hp      ┆ attack  ┆ defense ┆ sp_atk  ┆ sp_def  ┆ speed   │
# │ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     │
# │ str     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     │
# ╞═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╡
# │ mean    ┆ 435.103 ┆ 69.259  ┆ 79.001  ┆ 73.843  ┆ 72.820  ┆ 71.903  ┆ 68.278  │
# │ std     ┆ 119.963 ┆ 25.535  ┆ 32.457  ┆ 31.184  ┆ 32.722  ┆ 27.829  ┆ 29.060  │
# │ min     ┆ 180.000 ┆ 1.000   ┆ 5.000   ┆ 5.000   ┆ 10.000  ┆ 20.000  ┆ 5.000   │
# │ max     ┆ 780.000 ┆ 255.000 ┆ 190.000 ┆ 230.000 ┆ 194.000 ┆ 230.000 ┆ 180.000 │
# └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

print(getattr(cs.numeric(), "mean")())
# cs.numeric().mean()

# =========================================================================================
# 5. Dynamic column selection with `.pipe()`
# =========================================================================================
'''
Concept:
Sometimes the selected columns are easier to compute from schema metadata or
custom Python logic. `.pipe(...)` lets you keep the method chain while building
expressions dynamically.

This is not necessary for simple dtype selection because selectors such as
`cs.numeric()` are usually cleaner. Use `.pipe(...)` when the expression list
needs custom Python-side logic.
'''

##------------------------------------------------------------------------------------##
## Same log transformation, written with `.pipe()` and schema-driven column selection ##
##------------------------------------------------------------------------------------##

lf_log_scale_pipe = (
    lf_pokemon
    .pipe(
        lambda lf: lf.with_columns(
            pl.col(col).log()
            for col, dtype in lf.collect_schema().items()
            if dtype.is_numeric() and col != 'Generation'
        )
    )
)

print(lf_log_scale_pipe.head(5).collect())
# shape: (5, 12)
# ┌──────────────┬────────┬────────┬───────┬───────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name         ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP    ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---          ┆ ---    ┆ ---    ┆ ---   ┆ ---   ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str          ┆ str    ┆ str    ┆ f64   ┆ f64   ┆ f64    ┆ f64     ┆ f64    ┆ f64    ┆ f64   ┆ i64        ┆ bool      │
# ╞══════════════╪════════╪════════╪═══════╪═══════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur    ┆ Grass  ┆ Poison ┆ 5.762 ┆ 3.807 ┆ 3.892  ┆ 3.892   ┆ 4.174  ┆ 4.174  ┆ 3.807 ┆ 1          ┆ false     │
# │ Ivysaur      ┆ Grass  ┆ Poison ┆ 6.004 ┆ 4.094 ┆ 4.127  ┆ 4.143   ┆ 4.382  ┆ 4.382  ┆ 4.094 ┆ 1          ┆ false     │
# │ Venusaur     ┆ Grass  ┆ Poison ┆ 6.263 ┆ 4.382 ┆ 4.407  ┆ 4.419   ┆ 4.605  ┆ 4.605  ┆ 4.382 ┆ 1          ┆ false     │
# │ VenusaurMega ┆ Grass  ┆ Poison ┆ 6.438 ┆ 4.382 ┆ 4.605  ┆ 4.812   ┆ 4.804  ┆ 4.787  ┆ 4.382 ┆ 1          ┆ false     │
# │ Venusaur     ┆        ┆        ┆       ┆       ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Charmander   ┆ Fire   ┆ null   ┆ 5.733 ┆ 3.664 ┆ 3.951  ┆ 3.761   ┆ 4.094  ┆ 3.912  ┆ 4.174 ┆ 1          ┆ false     │
# └──────────────┴────────┴────────┴───────┴───────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##----------------------------------------------------------------------##
## Lowercase selected string columns using custom Python-side filtering ##
##----------------------------------------------------------------------##

lf_lower_strings_pipe = (
    lf_pokemon
    .pipe(
        lambda lf: lf.with_columns(
            pl.col(col).str.to_lowercase()
            for col, dtype in lf.collect_schema().items()
            if dtype == pl.String and col != 'Name'
        )
    )
)

print(lf_lower_strings_pipe.head(5).collect())
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name           ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---            ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str            ┆ str    ┆ str    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ i64        ┆ bool      │
# ╞════════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur      ┆ grass  ┆ poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Ivysaur        ┆ grass  ┆ poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Venusaur       ┆ grass  ┆ poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ VenusaurMega   ┆ grass  ┆ poison ┆ 625   ┆ 80  ┆ 100    ┆ 123     ┆ 122    ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ Venusaur       ┆        ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Charmander     ┆ fire   ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# └────────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##---------------------------------------------------------------------##
## Select non-numeric columns and rename numeric columns with a suffix ##
##---------------------------------------------------------------------##

lf_numeric_suffix_pipe = (
    lf_pokemon
    .pipe(
        lambda lf: lf.select(
            cs.exclude(cs.numeric()),
            *[
                pl.col(col).alias(f'{col}_numeric')
                for col, dtype in lf.collect_schema().items()
                if dtype.is_numeric()
            ]
        )
    )
)

print(lf_numeric_suffix_pipe.head(5).collect())
# shape: (5, 12)
# ┌──────────┬────────┬────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
# │ Name     ┆ Type_1 ┆ Type_2 ┆ Legenda ┆ Total_n ┆ HP_nume ┆ Attack_ ┆ Defense ┆ Sp_Atk_ ┆ Sp_Def_ ┆ Speed_n ┆ Generat │
# │ ---      ┆ ---    ┆ ---    ┆ ry      ┆ umeric  ┆ ric     ┆ numeric ┆ _numeri ┆ numeric ┆ numeric ┆ umeric  ┆ ion_num │
# │ str      ┆ str    ┆ str    ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ c       ┆ ---     ┆ ---     ┆ ---     ┆ eric    │
# │          ┆        ┆        ┆ bool    ┆ i64     ┆ i64     ┆ i64     ┆ ---     ┆ i64     ┆ i64     ┆ i64     ┆ ---     │
# │          ┆        ┆        ┆         ┆         ┆         ┆         ┆ i64     ┆         ┆         ┆         ┆ i64     │
# ╞══════════╪════════╪════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╡
# │ Bulbasau ┆ Grass  ┆ Poison ┆ false   ┆ 318     ┆ 45      ┆ 49      ┆ 49      ┆ 65      ┆ 65      ┆ 45      ┆ 1       │
# │ r        ┆        ┆        ┆         ┆         ┆         ┆         ┆         ┆         ┆         ┆         ┆         │
# │ Ivysaur  ┆ Grass  ┆ Poison ┆ false   ┆ 405     ┆ 60      ┆ 62      ┆ 63      ┆ 80      ┆ 80      ┆ 60      ┆ 1       │
# │ Venusaur ┆ Grass  ┆ Poison ┆ false   ┆ 525     ┆ 80      ┆ 82      ┆ 83      ┆ 100     ┆ 100     ┆ 80      ┆ 1       │
# │ Venusaur ┆ Grass  ┆ Poison ┆ false   ┆ 625     ┆ 80      ┆ 100     ┆ 123     ┆ 122     ┆ 120     ┆ 80      ┆ 1       │
# │ Mega     ┆        ┆        ┆         ┆         ┆         ┆         ┆         ┆         ┆         ┆         ┆         │
# │ Venusaur ┆        ┆        ┆         ┆         ┆         ┆         ┆         ┆         ┆         ┆         ┆         │
# │ Charmand ┆ Fire   ┆ null   ┆ false   ┆ 309     ┆ 39      ┆ 52      ┆ 43      ┆ 60      ┆ 50      ┆ 65      ┆ 1       │
# │ er       ┆        ┆        ┆         ┆         ┆         ┆         ┆         ┆         ┆         ┆         ┆         │
# └──────────┴────────┴────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
