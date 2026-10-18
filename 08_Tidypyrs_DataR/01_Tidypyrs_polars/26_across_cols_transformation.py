'''
This file demonstrates common Tidypyrs patterns
for applying one idea across many columns using `tp.across` and `tp.where`.

1. Apply one operation to every column with `tp.everything() or f.all()`
2. Transform columns selected by dtype using `tp.where` or selectors `cs`
3. Summarize columns selected by dtype with `tp.where` or selector `cs`
4. Use `tp.select_dtypes` as alternative for `tp.where`
5. Using `tp.across(cols, fn=lambda x: x, names_prefix=None)`
'''

from pathlib import Path

import tidypyrs as tp
from tidypyrs import f

# Optional display settings
tp.Config.set_tbl_rows(10)
tp.Config.set_tbl_cols(20)
tp.Config.set_float_precision(3)
tp.Config.set_tbl_width_chars(200)

# =========================================================================================
# 0. Setup Data
# =========================================================================================

data_dir = next(Path.home().rglob("*/DataScience_MachineLearning/data"))

tl_pokemon = (
    tp.scan_csv(data_dir / "pokemon.csv")
    .drop("#")
    .rename(lambda name: name.strip())
    .select(f.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .mutate(
        f("type_1", "type_2").cast(tp.Categorical),
        f("legendary").cast(tp.Boolean),
        f("generation").pipe(tp.as_enum, f.pull("generation"))
    )
)

print(tl_pokemon.head(5).collect())
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
# 1. Apply one operation to every column with `tp.everything() or f.all()`
# =========================================================================================
'''
Concept:
Apply one operation to every column.

Tidypyrs:
Use `tp.everything()` or `f.all()` when the expression should target every column.
'''

##-----------------------------------##
## Count null values in every column ##
##-----------------------------------##

print(
    tl_pokemon
    .summarise(
        tp.everything().is_null().sum() # or `f.all().is_null.sum()`
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
    tl_pokemon
    .summarise(
        tp.everything().n_unique().sum() # or `f.all().n_unique().sum()`
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
# 2. Transform columns selected by dtype using `tp.where` or selectors `cs`
# =========================================================================================
'''
Concept:
Apply a transformation only to columns that satisfy a condition, such as numeric,
string, or boolean columns.

Tidypyrs:
Use `tp.where` or `cs` for dtype-based column selection.

For example: `tp.where("numeric")` is equivalent to `cs.numeric()`
'''

##--------------------------------------------------##
## Log-transform all numeric columns except `total` ##
##--------------------------------------------------##

print(
    tl_pokemon.
    mutate(
        tp.where("numeric").exclude('total').log() # or `cs.numeric().exclude('total').log()`
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

##------------------------------------------------------------------------------##
## Convert categorical-like columns to Tidypyrs Categorical dtype except `name` ##
##------------------------------------------------------------------------------##

print(
    tl_pokemon.
    with_columns(
        (tp.where("string").exclude("name") | tp.where("enum") | tp.where("bool")) # (cs.string().exclude("name") | cs.enum() | cs.boolean())
        .cast(tp.String)
        .cast(tp.Categorical)
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
    tl_pokemon
    .mutate(tp.where("factor").cast(tp.String)) # cast these factor/categorical to string for demonstration
    .mutate(tp.where("string").exclude("name").str.to_lowercase())
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
    tl_pokemon.
    mutate(
        (tp.where("numeric") - tp.where("numeric").mean()) / tp.where("numeric").std()
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

Tidypyrs:
Use `.summarise(...)` with selector expressions. When expressions like `.mean()`,
`.std()`, `.min()`, or `.max()` reduce each selected column to one value, the
result is a one-row DataFrame.
'''

##-------------------------------------------##
## Calculate the mean of all numeric columns ##
##-------------------------------------------##

print(
    tl_pokemon
    .summarise(
        tp.where("numeric").mean()
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
    tl_pokemon
    .summarise(
        tp.where("numeric").std()
    )
    .collect()
)

##-------------------------------------------------------------------##
## Calculate multiple summary statistics and suffix the output names ##
##-------------------------------------------------------------------##

print(
    tl_pokemon.select(
        tp.where("string").str.len_chars().mean().name.suffix('_mean_char_counts'),
        tp.where("numeric").mean().name.suffix('_mean'),
    )
    .collect()
)
# shape: (1, 8)
# ┌───────────────────────┬────────────┬─────────┬─────────────┬──────────────┬─────────────┬─────────────┬────────────┐
# │ name_mean_char_counts ┆ total_mean ┆ hp_mean ┆ attack_mean ┆ defense_mean ┆ sp_atk_mean ┆ sp_def_mean ┆ speed_mean │
# │ ---                   ┆ ---        ┆ ---     ┆ ---         ┆ ---          ┆ ---         ┆ ---         ┆ ---        │
# │ f64                   ┆ f64        ┆ f64     ┆ f64         ┆ f64          ┆ f64         ┆ f64         ┆ f64        │
# ╞═══════════════════════╪════════════╪═════════╪═════════════╪══════════════╪═════════════╪═════════════╪════════════╡
# │ 8.841                 ┆ 435.103    ┆ 69.259  ┆ 79.001      ┆ 73.843       ┆ 72.820      ┆ 71.903      ┆ 68.278     │
# └───────────────────────┴────────────┴─────────┴─────────────┴──────────────┴─────────────┴─────────────┴────────────┘

# =========================================================================================
# 4. Reframe summaries into rows with `tp.bind_rows()` and `getattr()`
# =========================================================================================
'''
Concept:
Return a result with a different number of rows than the original data.

Example:
For each selected numeric column, calculate Min, Q1, Median, Q3, and Max. The
summary names become rows.

Tidypyrs:
Use `tp.bind_rows([...])` to stack multiple one-row summaries. This keeps the
calculation lazy and uses native Tidypyrs expressions.
'''

##-----------------------------------------##
## `tp.bind_rows()` for multiple quantiles ##
##-----------------------------------------##

qs = [0.00, 0.25, 0.50, 0.75, 1.00]
labels = ['Min', 'Q1', 'Median', 'Q3', 'Max']

tl_percentile = tp.bind_rows([
    tl_pokemon.select(
        tp.lit(label).alias('index'),
        tp.where("numeric").exclude('Generation').quantile(q)
    )
    for q, label in zip(qs, labels)
])

print(tl_percentile.collect())
# shape: (5, 8)
# ┌────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
# │ index  ┆ total   ┆ hp      ┆ attack  ┆ defense ┆ sp_atk  ┆ sp_def  ┆ speed   │
# │ ---    ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     ┆ ---     │
# │ str    ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     ┆ f64     │
# ╞════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╪═════════╡
# │ Min    ┆ 180.000 ┆ 1.000   ┆ 5.000   ┆ 5.000   ┆ 10.000  ┆ 20.000  ┆ 5.000   │
# │ Q1     ┆ 330.000 ┆ 50.000  ┆ 55.000  ┆ 50.000  ┆ 50.000  ┆ 50.000  ┆ 45.000  │
# │ Median ┆ 450.000 ┆ 65.000  ┆ 75.000  ┆ 70.000  ┆ 65.000  ┆ 70.000  ┆ 65.000  │
# │ Q3     ┆ 515.000 ┆ 80.000  ┆ 100.000 ┆ 90.000  ┆ 95.000  ┆ 90.000  ┆ 90.000  │
# │ Max    ┆ 780.000 ┆ 255.000 ┆ 190.000 ┆ 230.000 ┆ 194.000 ┆ 230.000 ┆ 180.000 │
# └────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

##------------------------------------------------------------------------##
## `tp.bind_rows()` and `getattr()` to wrap aggregated results vertically ##
##------------------------------------------------------------------------##

summaries = ["mean", "std", "min", "max"]
aggs = [getattr(tp.Expr, summary) for summary in summaries]
print(
    tp.bind_rows(
        [
            tl_pokemon.select(tp.where("numeric").pipe(agg))
            for agg in aggs
        ],
    )
    .select(tp.Series("summary", summaries), f.all())
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

# =========================================================================================
# 4. Use `tp.select_dtypes` as alternative for `tp.where`
# =========================================================================================

print(
    tl_pokemon
    .mutate(
        tp.select_dtypes(tp.String).str.to_lowercase(),
        tp.select_dtypes(tp.Int64).cast(tp.Float64)
    )
    .head(5)
    .collect()
)

##-----------------------------##

summaries = ["mean", "std", "min", "max"]
aggs = [getattr(tp.Expr, summary) for summary in summaries]
print(
    tp.bind_rows(
        [
            tl_pokemon.select(tp.select_dtypes(tp.Int64).pipe(agg))
            for agg in aggs
        ],
    )
    .select(tp.Series("summary", summaries), f.all())
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

# =========================================================================================
# 5. Using `tp.across(cols, fn=lambda x: x, names_prefix=None)`
# =========================================================================================

##-----------------------------------------------------##
## Same log transformation, written with `tp.across()` ##
##-----------------------------------------------------##

print(
    tl_pokemon
    .mutate(
        tp.across(tp.where("numeric").exclude("Generation"), lambda x: x.log())
    )
    .head(5)
    .collect()
)
# shape: (5, 12)
# ┌──────────────┬────────┬────────┬───────┬───────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ name         ┆ type_1 ┆ type_2 ┆ total ┆ hp    ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
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

print(
    tl_pokemon
    .mutate(
        f("type_1", "type_2").cast(tp.String),
        tp.across(tp.where("string").exclude("name"), lambda x: x.str.to_lowercase()),
        parallel=False
    )
    .head(5)
    .collect()
)
# shape: (5, 12)
# ┌───────────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ name                  ┆ type_1 ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ ---                   ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str                   ┆ str    ┆ str    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═══════════════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur             ┆ grass  ┆ poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Ivysaur               ┆ grass  ┆ poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Venusaur              ┆ grass  ┆ poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ VenusaurMega Venusaur ┆ grass  ┆ poison ┆ 625   ┆ 80  ┆ 100    ┆ 123     ┆ 122    ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ Charmander            ┆ fire   ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# └───────────────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

##---------------------------------------------------------------------##
## Select non-numeric columns and rename numeric columns with a suffix ##
##---------------------------------------------------------------------##

print(
    tl_pokemon
    .mutate(
        tp.across(tp.where("numeric").name.suffix("_numeric"))
    )
    .head(5)
    .collect()
)
# shape: (5, 12)
# ┌──────────┬────────┬────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
# │ name     ┆ type_1 ┆ type_2 ┆ legenda ┆ total_n ┆ hp_nume ┆ attack_ ┆ defense ┆ sp_atk_ ┆ sp_def_ ┆ speed_n ┆ generat │
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

##----------------------------------##
## `tl.summarise()` and `tp.across` ##
##----------------------------------##

print(
    tl_pokemon
    .summarise(
        tp.across(tp.where("string").str.len_chars().mean().name.suffix("_mean_char_counts")),
        tp.across(tp.where("numeric").mean().name.suffix("_mean")),
    )
    .collect()
)
# shape: (1, 8)
# ┌───────────────────────┬────────────┬─────────┬─────────────┬──────────────┬─────────────┬─────────────┬────────────┐
# │ name_mean_char_counts ┆ total_mean ┆ hp_mean ┆ attack_mean ┆ defense_mean ┆ sp_atk_mean ┆ sp_def_mean ┆ speed_mean │
# │ ---                   ┆ ---        ┆ ---     ┆ ---         ┆ ---          ┆ ---         ┆ ---         ┆ ---        │
# │ f64                   ┆ f64        ┆ f64     ┆ f64         ┆ f64          ┆ f64         ┆ f64         ┆ f64        │
# ╞═══════════════════════╪════════════╪═════════╪═════════════╪══════════════╪═════════════╪═════════════╪════════════╡
# │ 8.841                 ┆ 435.103    ┆ 69.259  ┆ 79.001      ┆ 73.843       ┆ 72.820      ┆ 71.903      ┆ 68.278     │
# └───────────────────────┴────────────┴─────────┴─────────────┴──────────────┴─────────────┴─────────────┴────────────┘
