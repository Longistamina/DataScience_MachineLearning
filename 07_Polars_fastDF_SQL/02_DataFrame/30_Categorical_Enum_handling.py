'''
1. Categorical: unordered categories
2. Enum: ordered categories
3. Boolean: binary True/False
'''

from pathlib import Path

import polars as pl
from polars import col as c

# Optional display settings
pl.Config.set_tbl_rows(10)
pl.Config.set_tbl_cols(20)
pl.Config.set_tbl_width_chars(125)

data_dir = next(Path('/home').rglob('*/DataScience_MachineLearning/data'))

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
)

print(lf_pokemon.head(5).collect())
# shape: (5, 12)
# ┌──────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ name         ┆ type_1 ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ ---          ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ str          ┆ str    ┆ str    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ i64        ┆ bool      │
# ╞══════════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ Bulbasaur    ┆ Grass  ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ Ivysaur      ┆ Grass  ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ Venusaur     ┆ Grass  ┆ Poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ VenusaurMega ┆ Grass  ┆ Poison ┆ 625   ┆ 80  ┆ 100    ┆ 123     ┆ 122    ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ Venusaur     ┆        ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ Charmander   ┆ Fire   ┆ null   ┆ 309   ┆ 39  ┆ 52     ┆ 43      ┆ 60     ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# └──────────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

# ================================================================================
# 1. Categorical: unordered categories
# ================================================================================

print(
    lf_pokemon
    .with_columns(
        c('type_1', 'type_2').cast(pl.Categorical) # or `.cast(pl.String).cast(pl.Categorical)` would be safer
    )
    .select(pl.nth(range(4))) # first 4 columns
    .head(5)
    .collect()
)
# shape: (5, 4)
# ┌───────────────────────┬────────┬────────┬───────┐
# │ name                  ┆ type_1 ┆ type_2 ┆ total │
# │ ---                   ┆ ---    ┆ ---    ┆ ---   │
# │ str                   ┆ cat    ┆ cat    ┆ i64   │
# ╞═══════════════════════╪════════╪════════╪═══════╡
# │ Bulbasaur             ┆ Grass  ┆ Poison ┆ 318   │
# │ Ivysaur               ┆ Grass  ┆ Poison ┆ 405   │
# │ Venusaur              ┆ Grass  ┆ Poison ┆ 525   │
# │ VenusaurMega Venusaur ┆ Grass  ┆ Poison ┆ 625   │
# │ Charmander            ┆ Fire   ┆ null   ┆ 309   │
# └───────────────────────┴────────┴────────┴───────┘

# ================================================================================
# 2. Enum: ordered categories
# ================================================================================

##-------------##
## Basic usage ##
##-------------##

print(
    lf_pokemon
    .with_columns(
        c('generation').cast(pl.String).cast(pl.Enum([str(gen) for gen in range(1, 7)])) # pl.Enum(["1", "2", "3", "4", "5", "6"])
    )
    .select("name", "generation")
    .head(5)
    .collect()
)
# shape: (5, 2)
# ┌───────────────────────┬────────────┐
# │ name                  ┆ generation │
# │ ---                   ┆ ---        │
# │ str                   ┆ enum       │
# ╞═══════════════════════╪════════════╡
# │ Bulbasaur             ┆ 1          │
# │ Ivysaur               ┆ 1          │
# │ Venusaur              ┆ 1          │
# │ VenusaurMega Venusaur ┆ 1          │
# │ Charmander            ┆ 1          │
# └───────────────────────┴────────────┘

##---------------------------------------------------##
## Convert to Enum with `lf.pipe` and `with_columns` ##
##---------------------------------------------------##

print(
    lf_pokemon
    .pipe(
        lambda lf: lf.with_columns(
            c("generation").cast(pl.String).cast(pl.Enum(lf.select("generation").collect().to_series().cast(pl.String).unique().sort())),
        )
    )
    .select("name", "generation")
    .head(5)
    .collect()
)
# shape: (5, 2)
# ┌───────────────────────┬────────────┐
# │ name                  ┆ generation │
# │ ---                   ┆ ---        │
# │ str                   ┆ enum       │
# ╞═══════════════════════╪════════════╡
# │ Bulbasaur             ┆ 1          │
# │ Ivysaur               ┆ 1          │
# │ Venusaur              ┆ 1          │
# │ VenusaurMega Venusaur ┆ 1          │
# │ Charmander            ┆ 1          │
# └───────────────────────┴────────────┘

##----------------------------------------------------------##
## Convert to Enum with `pl.Expr.pipe` and a standalone UDF ##
##----------------------------------------------------------##

def as_enum(column: pl.Expr, lf: pl.LazyFrame) -> pl.Expr:
    return  column.cast(pl.String).cast(pl.Enum(lf.select(column).collect().to_series().cast(pl.String).unique().sort()))

print(
    lf_pokemon
    .with_columns(
        c('generation').pipe(as_enum, lf_pokemon)
    )
    .select("name", "generation")
    .head(5)
    .collect()
)
# shape: (5, 2)
# ┌───────────────────────┬────────────┐
# │ name                  ┆ generation │
# │ ---                   ┆ ---        │
# │ str                   ┆ enum       │
# ╞═══════════════════════╪════════════╡
# │ Bulbasaur             ┆ 1          │
# │ Ivysaur               ┆ 1          │
# │ Venusaur              ┆ 1          │
# │ VenusaurMega Venusaur ┆ 1          │
# │ Charmander            ┆ 1          │
# └───────────────────────┴────────────┘

##-----------------------------------------------------------------------------##
## Filter enum with relationship operators (>, <, =, >=, <=, !=, is_between()) ##
##-----------------------------------------------------------------------------##

print(
    lf_pokemon
    .with_columns(
        c('generation').cast(pl.String).cast(pl.Enum([str(gen) for gen in range(1, 7)])) # pl.Enum(["1", "2", "3", "4", "5", "6"])
    )
    .select('name', 'generation')
    .filter(c('generation') > '3')
    .collect()
)
# shape: (368, 2)
# ┌─────────────────────┬────────────┐
# │ name                ┆ generation │
# │ ---                 ┆ ---        │
# │ str                 ┆ enum       │
# ╞═════════════════════╪════════════╡
# │ Turtwig             ┆ 4          │
# │ Grotle              ┆ 4          │
# │ Torterra            ┆ 4          │
# │ Chimchar            ┆ 4          │
# │ Monferno            ┆ 4          │
# │ …                   ┆ …          │
# │ Diancie             ┆ 6          │
# │ DiancieMega Diancie ┆ 6          │
# │ HoopaHoopa Confined ┆ 6          │
# │ HoopaHoopa Unbound  ┆ 6          │
# │ Volcanion           ┆ 6          │
# └─────────────────────┴────────────┘

print(
    lf_pokemon
    .with_columns(
        c('generation').cast(pl.String).cast(pl.Enum([str(gen) for gen in range(1, 7)])) # pl.Enum(["1", "2", "3", "4", "5", "6"])
    )
    .select('name', 'generation')
    .filter(c('generation').is_between(pl.lit("3"), pl.lit("5"), closed="both")) # don't forget pl.lit()
    .collect()
)
# shape: (446, 2)
# ┌─────────────────────────┬────────────┐
# │ name                    ┆ generation │
# │ ---                     ┆ ---        │
# │ str                     ┆ enum       │
# ╞═════════════════════════╪════════════╡
# │ Treecko                 ┆ 3          │
# │ Grovyle                 ┆ 3          │
# │ Sceptile                ┆ 3          │
# │ SceptileMega Sceptile   ┆ 3          │
# │ Torchic                 ┆ 3          │
# │ …                       ┆ …          │
# │ KeldeoOrdinary Forme    ┆ 5          │
# │ KeldeoResolute Forme    ┆ 5          │
# │ MeloettaAria Forme      ┆ 5          │
# │ MeloettaPirouette Forme ┆ 5          │
# │ Genesect                ┆ 5          │
# └─────────────────────────┴────────────┘

# ================================================================================
# 3. Boolean: binary True/False
# ================================================================================

##--------------------##
## Convert to Boolean ##
##--------------------##

print(
    lf_pokemon
    .with_columns(
        c('legendary').cast(pl.Boolean)
    )
    .select('name', 'generation', 'legendary')
    .collect()
)
# shape: (800, 3)
# ┌───────────────────────┬────────────┬───────────┐
# │ name                  ┆ generation ┆ legendary │
# │ ---                   ┆ ---        ┆ ---       │
# │ str                   ┆ i64        ┆ bool      │
# ╞═══════════════════════╪════════════╪═══════════╡
# │ Bulbasaur             ┆ 1          ┆ false     │
# │ Ivysaur               ┆ 1          ┆ false     │
# │ Venusaur              ┆ 1          ┆ false     │
# │ VenusaurMega Venusaur ┆ 1          ┆ false     │
# │ Charmander            ┆ 1          ┆ false     │
# │ …                     ┆ …          ┆ …         │
# │ Diancie               ┆ 6          ┆ true      │
# │ DiancieMega Diancie   ┆ 6          ┆ true      │
# │ HoopaHoopa Confined   ┆ 6          ┆ true      │
# │ HoopaHoopa Unbound    ┆ 6          ┆ true      │
# │ Volcanion             ┆ 6          ┆ true      │
# └───────────────────────┴────────────┴───────────┘

##----------------------------------------##
## Use Boolean column as filter condition ##
##----------------------------------------##

print(
    lf_pokemon
    .with_columns(
        c('legendary').cast(pl.Boolean)
    )
    .select('name', 'generation', 'legendary')
    .filter('legendary') # or `.filter(c('legendary'))`
    .collect()
)
# shape: (65, 3)
# ┌─────────────────────┬────────────┬───────────┐
# │ name                ┆ generation ┆ legendary │
# │ ---                 ┆ ---        ┆ ---       │
# │ str                 ┆ i64        ┆ bool      │
# ╞═════════════════════╪════════════╪═══════════╡
# │ Articuno            ┆ 1          ┆ true      │
# │ Zapdos              ┆ 1          ┆ true      │
# │ Moltres             ┆ 1          ┆ true      │
# │ Mewtwo              ┆ 1          ┆ true      │
# │ MewtwoMega Mewtwo X ┆ 1          ┆ true      │
# │ …                   ┆ …          ┆ …         │
# │ Diancie             ┆ 6          ┆ true      │
# │ DiancieMega Diancie ┆ 6          ┆ true      │
# │ HoopaHoopa Confined ┆ 6          ┆ true      │
# │ HoopaHoopa Unbound  ┆ 6          ┆ true      │
# │ Volcanion           ┆ 6          ┆ true      │
# └─────────────────────┴────────────┴───────────┘
