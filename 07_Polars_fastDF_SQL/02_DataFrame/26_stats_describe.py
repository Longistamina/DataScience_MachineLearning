'''
LazyFrame description / summary statistics in Polars.

1. `lf.describe()`: summary statistics for all columns, with dtype-dependent output.
2. `lf.select(cs.numeric()).describe()`: describe only numeric columns:
3. `lf.select(cs.string() | cs.categorical()).describe(): describe string and categorical columns
4. `lf.select(~(cs...() | cs...())).describe(): exclude specific dtypes
5. Custom describe for categorical columns with `pipe` and `concat`
'''

from pathlib import Path

import polars as pl
from polars import col as c
from polars import selectors as cs

# Optional display settings
pl.Config.set_tbl_rows(20)
pl.Config.set_tbl_cols(20)
pl.Config.set_tbl_width_chars(125)

data_dir = next(Path('/home').rglob('*/DataScience_MachineLearning/data'))

 # =========================================================================================
 # 0. Setup Data
 # =========================================================================================

lf_pokemon = (
    pl.scan_csv(data_dir / "pokemon.csv")
    .drop('#')
    .rename(lambda name: name.strip()) # remove trailing space characters
    .select(
        pl.all()
        .name.replace(r"\s+", "_") # replace " " or "  " (or more consecutive space characters) with just one "_"
        .name.replace(".", "", literal=True) # replace "." with empty string (remove it), literal=True to deactive regex
        .name.to_lowercase()
    )
    .with_columns(cs.string().exclude("Name").cast(pl.Categorical))
    .pipe(lambda lf: lf.with_columns(
        c.generation.cast(pl.String).cast(pl.Enum(lf.select("generation").collect().to_series().cast(pl.String).unique().sort())))
    )
)

print(lf_pokemon.head().collect())
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

print(lf_pokemon.collect_schema())

# =========================================================================================
# 1. `lf.describe()`: summary statistics for all columns, with dtype-dependent output.
# =========================================================================================

##---------------##
## Default usage ##
##---------------##
'''
Polars `LazyFrame.describe()` returns summary statistics for the DataFrame.
Unlike pandas, Polars includes all columns by default, and fills unsupported
statistics with nulls depending on the dtype.
'''

print(lf_pokemon.describe())
# shape: (9, 13)
# ┌─────────┬─────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┐
# │ statist ┆ name    ┆ type_1 ┆ type_2 ┆ total  ┆ hp     ┆ attack ┆ defens ┆ sp_atk ┆ sp_def ┆ speed  ┆ genera ┆ legend │
# │ ic      ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---    ┆ ---    ┆ e      ┆ ---    ┆ ---    ┆ ---    ┆ tion   ┆ ary    │
# │ ---     ┆ str     ┆ str    ┆ str    ┆ f64    ┆ f64    ┆ f64    ┆ ---    ┆ f64    ┆ f64    ┆ f64    ┆ ---    ┆ ---    │
# │ str     ┆         ┆        ┆        ┆        ┆        ┆        ┆ f64    ┆        ┆        ┆        ┆ str    ┆ f64    │
# ╞═════════╪═════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╡
# │ count   ┆ 800     ┆ 800    ┆ 414    ┆ 800.0  ┆ 800.0  ┆ 800.0  ┆ 800.0  ┆ 800.0  ┆ 800.0  ┆ 800.0  ┆ 800    ┆ 800.0  │
# │ null_co ┆ 0       ┆ 0      ┆ 386    ┆ 0.0    ┆ 0.0    ┆ 0.0    ┆ 0.0    ┆ 0.0    ┆ 0.0    ┆ 0.0    ┆ 0      ┆ 0.0    │
# │ unt     ┆         ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        │
# │ mean    ┆ null    ┆ null   ┆ null   ┆ 435.10 ┆ 69.258 ┆ 79.001 ┆ 73.842 ┆ 72.82  ┆ 71.902 ┆ 68.277 ┆ null   ┆ 0.0812 │
# │         ┆         ┆        ┆        ┆ 25     ┆ 75     ┆ 25     ┆ 5      ┆        ┆ 5      ┆ 5      ┆        ┆ 5      │
# │ std     ┆ null    ┆ null   ┆ null   ┆ 119.96 ┆ 25.534 ┆ 32.457 ┆ 31.183 ┆ 32.722 ┆ 27.828 ┆ 29.060 ┆ null   ┆ null   │
# │         ┆         ┆        ┆        ┆ 304    ┆ 669    ┆ 366    ┆ 501    ┆ 294    ┆ 916    ┆ 474    ┆        ┆        │
# │ min     ┆ Abomasn ┆ null   ┆ null   ┆ 180.0  ┆ 1.0    ┆ 5.0    ┆ 5.0    ┆ 10.0   ┆ 20.0   ┆ 5.0    ┆ null   ┆ 0.0    │
# │         ┆ ow      ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        │
# │ 25%     ┆ null    ┆ null   ┆ null   ┆ 330.0  ┆ 50.0   ┆ 55.0   ┆ 50.0   ┆ 50.0   ┆ 50.0   ┆ 45.0   ┆ null   ┆ null   │
# │ 50%     ┆ null    ┆ null   ┆ null   ┆ 450.0  ┆ 65.0   ┆ 75.0   ┆ 70.0   ┆ 65.0   ┆ 70.0   ┆ 65.0   ┆ null   ┆ null   │
# │ 75%     ┆ null    ┆ null   ┆ null   ┆ 515.0  ┆ 80.0   ┆ 100.0  ┆ 90.0   ┆ 95.0   ┆ 90.0   ┆ 90.0   ┆ null   ┆ null   │
# │ max     ┆ Zygarde ┆ null   ┆ null   ┆ 780.0  ┆ 255.0  ┆ 190.0  ┆ 230.0  ┆ 194.0  ┆ 230.0  ┆ 180.0  ┆ null   ┆ 1.0    │
# │         ┆ 50%     ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        │
# │         ┆ Forme   ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        ┆        │
# └─────────┴─────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘

# =========================================================================================
# 2. `lf.select(cs.numeric()).describe()`: describe only numeric columns:
# =========================================================================================

##-----------------------------------------------------##
## Equivalent idea: df.describe() for numeric columns  ##
## Polars way: select numeric columns, then describe() ##
##-----------------------------------------------------##

print(
    lf_pokemon
    .select(cs.numeric())
    .describe()
)
# shape: (9, 8)
# ┌────────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┐
# │ statistic  ┆ Total     ┆ HP        ┆ Attack    ┆ Defense   ┆ Sp_Atk    ┆ Sp_Def    ┆ Speed     │
# │ ---        ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       │
# │ str        ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       │
# ╞════════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╡
# │ count      ┆ 800.0     ┆ 800.0     ┆ 800.0     ┆ 800.0     ┆ 800.0     ┆ 800.0     ┆ 800.0     │
# │ null_count ┆ 0.0       ┆ 0.0       ┆ 0.0       ┆ 0.0       ┆ 0.0       ┆ 0.0       ┆ 0.0       │
# │ mean       ┆ 435.1025  ┆ 69.25875  ┆ 79.00125  ┆ 73.8425   ┆ 72.82     ┆ 71.9025   ┆ 68.2775   │
# │ std        ┆ 119.96304 ┆ 25.534669 ┆ 32.457366 ┆ 31.183501 ┆ 32.722294 ┆ 27.828916 ┆ 29.060474 │
# │ min        ┆ 180.0     ┆ 1.0       ┆ 5.0       ┆ 5.0       ┆ 10.0      ┆ 20.0      ┆ 5.0       │
# │ 25%        ┆ 330.0     ┆ 50.0      ┆ 55.0      ┆ 50.0      ┆ 50.0      ┆ 50.0      ┆ 45.0      │
# │ 50%        ┆ 450.0     ┆ 65.0      ┆ 75.0      ┆ 70.0      ┆ 65.0      ┆ 70.0      ┆ 65.0      │
# │ 75%        ┆ 515.0     ┆ 80.0      ┆ 100.0     ┆ 90.0      ┆ 95.0      ┆ 90.0      ┆ 90.0      │
# │ max        ┆ 780.0     ┆ 255.0     ┆ 190.0     ┆ 230.0     ┆ 194.0     ┆ 230.0     ┆ 180.0     │
# └────────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┘

# ====================================================================================================
# 3. `lf.select(cs.string() | cs.categorical()).describe(): describe string and categorical columns
# ====================================================================================================

print(
    lf_pokemon
    .select(cs.string() | cs.categorical())
    .describe()
)
# shape: (9, 4)
# ┌────────────┬──────────────────┬────────┬────────┐
# │ statistic  ┆ Name             ┆ Type_1 ┆ Type_2 │
# │ ---        ┆ ---              ┆ ---    ┆ ---    │
# │ str        ┆ str              ┆ str    ┆ str    │
# ╞════════════╪══════════════════╪════════╪════════╡
# │ count      ┆ 800              ┆ 800    ┆ 414    │
# │ null_count ┆ 0                ┆ 0      ┆ 386    │
# │ mean       ┆ null             ┆ null   ┆ null   │
# │ std        ┆ null             ┆ null   ┆ null   │
# │ min        ┆ Abomasnow        ┆ null   ┆ null   │
# │ 25%        ┆ null             ┆ null   ┆ null   │
# │ 50%        ┆ null             ┆ null   ┆ null   │
# │ 75%        ┆ null             ┆ null   ┆ null   │
# │ max        ┆ Zygarde50% Forme ┆ null   ┆ null   │
# └────────────┴──────────────────┴────────┴────────┘

# =========================================================================================
# 4. `lf.select(~(cs...() | cs...())).describe(): exclude specific dtypes
# =========================================================================================

print(
    lf_pokemon
    .select(~(cs.categorical() | cs.boolean()))
    .describe()
)
# Keeps string + numeric columns, excludes categorical + boolean columns.

# =========================================================================================
# 5. Custom describe for categorical columns with `pipe` and `concat`
# =========================================================================================
'''
Polars `describe()` does not return pandas-style `unique`, `top`, and `freq` rows
for categorical/string columns. If you specifically want those statistics, compute
them directly with expressions.
'''

statistics = {
    "count": lambda expr: expr.count().cast(pl.String),
    "n_unique": lambda expr: expr.n_unique().cast(pl.String),
    "most_occur": lambda expr: expr.mode().first().cast(pl.String) # the value that appears the most
}
print(
    lf_pokemon
    .select(cs.string() | cs.categorical())
    .pipe(
        lambda lf: # use this to avoid typing ``lf_pokemon`` many times
            pl.concat(
                [
                    lf.select(
                        pl.lit(stat).alias("statistic"),
                        pl.all().pipe(agg)
                    )
                    for stat, agg in statistics.items()
                ],
                how="diagonal_relaxed"
            )
    )
    .collect()
)
# shape: (3, 4)
# ┌────────────┬───────────┬────────┬────────┐
# │ statistic  ┆ name      ┆ type_1 ┆ type_2 │
# │ ---        ┆ ---       ┆ ---    ┆ ---    │
# │ str        ┆ str       ┆ str    ┆ str    │
# ╞════════════╪═══════════╪════════╪════════╡
# │ count      ┆ 800       ┆ 800    ┆ 414    │ u32 -> String |
# │ n_unique   ┆ 800       ┆ 18     ┆ 19     │ u32 -> String | => able to concat vertically
# │ most_occur ┆ Bulbasaur ┆ Water  ┆ null   │ cat -> String |
# └────────────┴───────────┴────────┴────────┘
