'''
Column-wise selection, transformation, summarisation, and reframing in Polars

This file demonstrates common Polars patterns for applying one idea across many
columns. Polars does not need a special "across" API because expressions and
selectors already work column-wise.

Core Polars APIs used here:

1. `pl.all()`
   - Select every column inside an expression context.

2. `polars.selectors` as `cs`
   - Select columns by dtype or name pattern.
   - Examples: `cs.numeric()`, `cs.string()`, `cs.boolean()`.

3. `.with_columns(...)`
   - Add or replace columns while preserving the original row count.
   - Use this for transformations.

4. `.select(...)`
   - Select, reorder, or aggregate columns.
   - Use this for summaries and column selection.

5. `pl.concat([...])`
   - Stack several LazyFrames/DataFrames vertically.
   - Useful when summary statistics should become rows.

6. `.pipe(...)`
   - Keep method chaining when the next step is easier to express with custom
     Python-side logic or schema-driven expression generation.
'''

from pathlib import Path

import polars as pl
import polars.selectors as cs

# Optional display settings
pl.Config.set_tbl_rows(10)
pl.Config.set_tbl_cols(20)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(120)


# =========================================================================================
# 0. Setup Data
# =========================================================================================

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

lf_pokemon = (
    pl.scan_csv(data_dir / "pokemon.csv")
    .drop('#')
    .rename(lambda name: name.strip()) # remove trailing space characters
    .select(
        pl.all()
        .name.replace(r"\s+", "_") # replace " " or "  " (or more consecutive space characters) with just one "_"
        .name.replace(".", "", literal=True) # replace "." with empty string (remove it), literal=True to deactive regex
    )
)

print(lf_pokemon.head(5).collect())
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name           ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---            ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str            ┆ str    ┆ str    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ i64        ┆ bool      │
# ╞════════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur      ┆ Grass  ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Ivysaur        ┆ Grass  ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Venusaur       ┆ Grass  ┆ Poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ VenusaurMega   ┆ Grass  ┆ Poison ┆ 625   ┆ 80  ┆ 100    ┆ 123     ┆ 122    ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ Venusaur       ┆        ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Charmander     ┆ Fire   ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# └────────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

print(lf_pokemon.collect_schema())
# Schema({'Name': String, 'Type_1': String, 'Type_2': String, 'Total': Int64, 'HP': Int64, 'Attack': Int64, 'Defense': Int64, 'Sp_Atk': Int64, 'Sp_Def': Int64, 'Speed': Int64, 'Generation': Int64, 'Legendary': Boolean})


# =========================================================================================
# 1. Select every column with `pl.all()`
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

lf_null_check = lf_pokemon.select(
    pl.all().is_null().sum()
)

print(lf_null_check.collect())
# shape: (1, 12)
# ┌──────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---  ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ u32  ┆ u32    ┆ u32    ┆ u32   ┆ u32 ┆ u32    ┆ u32     ┆ u32    ┆ u32    ┆ u32   ┆ u32        ┆ u32       │
# ╞══════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ 0    ┆ 0      ┆ 386    ┆ 0     ┆ 0   ┆ 0      ┆ 0       ┆ 0      ┆ 0      ┆ 0     ┆ 0          ┆ 0         │
# └──────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##-------------------------------------##
## Count unique values in every column ##
##-------------------------------------##

lf_unique_count = lf_pokemon.select(
    pl.all().n_unique()
)

print(lf_unique_count.collect())
# shape: (1, 12)
# ┌──────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---  ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ u32  ┆ u32    ┆ u32    ┆ u32   ┆ u32 ┆ u32    ┆ u32     ┆ u32    ┆ u32    ┆ u32   ┆ u32        ┆ u32       │
# ╞══════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ 800  ┆ 18     ┆ 19     ┆ 200   ┆ 94  ┆ 111    ┆ 103     ┆ 105    ┆ 92     ┆ 108   ┆ 6          ┆ 2         │
# └──────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘


# =========================================================================================
# 2. Transform columns selected by dtype
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

##-------------------------------------------------------##
## Log-transform all numeric columns except `Generation` ##
##-------------------------------------------------------##

lf_log_scale = lf_pokemon.with_columns(
    cs.numeric().exclude('Generation').log()
)

print(lf_log_scale.head(5).collect())
# shape: (5, 12)
# ┌──────────────┬────────┬────────┬───────┬───────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name         ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP    ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---          ┆ ---    ┆ ---    ┆ ---   ┆ ---   ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str          ┆ str    ┆ str    ┆ f64   ┆ f64   ┆ f64    ┆ f64     ┆ f64    ┆ f64    ┆ f64   ┆ f64        ┆ bool      │
# ╞══════════════╪════════╪════════╪═══════╪═══════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur    ┆ Grass  ┆ Poison ┆ 5.762 ┆ 3.807 ┆ 3.892  ┆ 3.892   ┆ 4.174  ┆ 4.174  ┆ 3.807 ┆ 0.000      ┆ false     │
# │ Ivysaur      ┆ Grass  ┆ Poison ┆ 6.004 ┆ 4.094 ┆ 4.127  ┆ 4.143   ┆ 4.382  ┆ 4.382  ┆ 4.094 ┆ 0.000      ┆ false     │
# │ Venusaur     ┆ Grass  ┆ Poison ┆ 6.263 ┆ 4.382 ┆ 4.407  ┆ 4.419   ┆ 4.605  ┆ 4.605  ┆ 4.382 ┆ 0.000      ┆ false     │
# │ VenusaurMega ┆ Grass  ┆ Poison ┆ 6.438 ┆ 4.382 ┆ 4.605  ┆ 4.812   ┆ 4.804  ┆ 4.787  ┆ 4.382 ┆ 0.000      ┆ false     │
# │ Venusaur     ┆        ┆        ┆       ┆       ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Charmander   ┆ Fire   ┆ null   ┆ 5.733 ┆ 3.664 ┆ 3.951  ┆ 3.761   ┆ 4.094  ┆ 3.912  ┆ 4.174 ┆ 0.000      ┆ false     │
# └──────────────┴────────┴────────┴───────┴───────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##------------------------------------------------------------------------------##
## Convert categorical-like columns to Polars Categorical dtype except ``Name`` ##
##------------------------------------------------------------------------------##

lf_categorical_convert = lf_pokemon.with_columns(
    (cs.string().exclude("Name") | cs.by_name('Generation', 'Legendary'))
    .cast(pl.String)
    .cast(pl.Categorical)
)

print(lf_categorical_convert.head(5).collect())
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name           ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
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
## Lowercase all string columns except `Name` ##
##--------------------------------------------##

lf_lower_strings = lf_pokemon.with_columns(
    cs.string().exclude('Name').str.to_lowercase()
)

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

##-----------------------------------------------------------------##
## Example: transform selected columns and keep the original names ##
##-----------------------------------------------------------------##

lf_standardized_numeric = lf_pokemon.with_columns(
    ((cs.numeric().exclude('Generation') - cs.numeric().exclude('Generation').mean()) /
     cs.numeric().exclude('Generation').std())
)

print(lf_standardized_numeric.head(5).collect())
# shape: (5, 12)
# ┌────────────┬────────┬────────┬────────┬────────┬────────┬─────────┬────────┬────────┬────────┬───────────┬───────────┐
# │ Name       ┆ Type_1 ┆ Type_2 ┆ Total  ┆ HP     ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed  ┆ Generatio ┆ Legendary │
# │ ---        ┆ ---    ┆ ---    ┆ ---    ┆ ---    ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ n         ┆ ---       │
# │ str        ┆ str    ┆ str    ┆ f64    ┆ f64    ┆ f64    ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ ---       ┆ bool      │
# │            ┆        ┆        ┆        ┆        ┆        ┆         ┆        ┆        ┆        ┆ i64       ┆           │
# ╞════════════╪════════╪════════╪════════╪════════╪════════╪═════════╪════════╪════════╪════════╪═══════════╪═══════════╡
# │ Bulbasaur  ┆ Grass  ┆ Poison ┆ -0.976 ┆ -0.950 ┆ -0.924 ┆ -0.797  ┆ -0.239 ┆ -0.248 ┆ -0.801 ┆ 1         ┆ false     │
# │ Ivysaur    ┆ Grass  ┆ Poison ┆ -0.251 ┆ -0.363 ┆ -0.524 ┆ -0.348  ┆ 0.219  ┆ 0.291  ┆ -0.285 ┆ 1         ┆ false     │
# │ Venusaur   ┆ Grass  ┆ Poison ┆ 0.749  ┆ 0.421  ┆ 0.092  ┆ 0.294   ┆ 0.831  ┆ 1.010  ┆ 0.403  ┆ 1         ┆ false     │
# │ VenusaurMe ┆ Grass  ┆ Poison ┆ 1.583  ┆ 0.421  ┆ 0.647  ┆ 1.576   ┆ 1.503  ┆ 1.728  ┆ 0.403  ┆ 1         ┆ false     │
# │ ga         ┆        ┆        ┆        ┆        ┆        ┆         ┆        ┆        ┆        ┆           ┆           │
# │ Venusaur   ┆        ┆        ┆        ┆        ┆        ┆         ┆        ┆        ┆        ┆           ┆           │
# │ Charmander ┆ Fire   ┆ null   ┆ -1.051 ┆ -1.185 ┆ -0.832 ┆ -0.989  ┆ -0.392 ┆ -0.787 ┆ -0.113 ┆ 1         ┆ false     │
# └────────────┴────────┴────────┴────────┴────────┴────────┴─────────┴────────┴────────┴────────┴───────────┴───────────┘


# =========================================================================================
# 3. Summarize columns selected by dtype
# =========================================================================================
'''
Concept:
Apply aggregation functions to many selected columns.

Polars:
Use `.select(...)` with selector expressions. When expressions like `.mean()`,
`.std()`, `.min()`, or `.max()` reduce each selected column to one value, the
result is a one-row DataFrame.
'''

##---------------------------------------------------------------##
## Calculate the mean of all numeric columns except `Generation` ##
##---------------------------------------------------------------##

lf_mean_quantitative = lf_pokemon.select(
    cs.numeric().exclude('Generation').mean()
)

print(lf_mean_quantitative.collect())
# shape: (1, 7)
# ┌─────────┬────────┬────────┬─────────┬────────┬────────┬────────┐
# │ Total   ┆ HP     ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed  │
# │ ---     ┆ ---    ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---    │
# │ f64     ┆ f64    ┆ f64    ┆ f64     ┆ f64    ┆ f64    ┆ f64    │
# ╞═════════╪════════╪════════╪═════════╪════════╪════════╪════════╡
# │ 435.103 ┆ 69.259 ┆ 79.001 ┆ 73.843  ┆ 72.820 ┆ 71.903 ┆ 68.278 │
# └─────────┴────────┴────────┴─────────┴────────┴────────┴────────┘

##-----------------------------------------------------------------------------##
## Calculate the standard deviation of all numeric columns except `Generation` ##
##-----------------------------------------------------------------------------##

lf_std_quantitative = lf_pokemon.select(
    cs.numeric().exclude('Generation').std()
)

print(lf_std_quantitative.collect())

##-------------------------------------------------------------------##
## Calculate multiple summary statistics and suffix the output names ##
##-------------------------------------------------------------------##

lf_numeric_summary_wide = lf_pokemon.select(
    cs.numeric().exclude('Generation').mean().name.suffix('_mean'),
    cs.numeric().exclude('Generation').std().name.suffix('_std'),
    cs.numeric().exclude('Generation').min().name.suffix('_min'),
    cs.numeric().exclude('Generation').max().name.suffix('_max'),
)

print(lf_numeric_summary_wide.collect())


# =========================================================================================
# 4. Reframe summaries into rows
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


# =========================================================================================
# 6. Pattern summary
# =========================================================================================
'''
Pattern summary:

1. Select every column
   - Use `pl.all()`.

2. Select columns by dtype
   - Use `polars.selectors`:
     - `cs.numeric()`
     - `cs.string()`
     - `cs.boolean()`
     - `cs.categorical()`

3. Transform selected columns while preserving rows
   - Use `.with_columns(...)`.

4. Summarize selected columns into one row
   - Use `.select(...)` with aggregations such as `.mean()`, `.std()`, `.sum()`,
     `.min()`, and `.max()`.

5. Return summary statistics as rows
   - Use `pl.concat([...])` with one LazyFrame per summary row.

6. Keep a dynamic workflow readable
   - Use `.pipe(...)` when you need Python-side logic to generate expressions.

Best practice:
- Prefer native Polars expressions and selectors whenever possible.
- Use `.pipe(...)` for readability or custom dynamic expression construction.
- Avoid collecting to eager DataFrames unless an external Python library requires
  materialized data.
'''
