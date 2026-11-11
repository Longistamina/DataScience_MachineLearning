'''
1. Categorical: unordered categories
2. Enum: ordered categories
3. Boolean: binary True/False
'''

from pathlib import Path

import tidypyrs as tp
from tidypyrs import f

# Optional display settings
tp.Config.set_tbl_rows(10)
tp.Config.set_tbl_cols(20)
tp.Config.set_tbl_width_chars(125)

data_dir = next(Path('/home').rglob('*/DataScience_MachineLearning/data'))

tl_pokemon = (
    tp.scan_csv(data_dir / "pokemon.csv")
    .drop('#')
    .rename(lambda name: name.strip()) # remove trailing space characters
    .select(
        f.all()
        .name.replace(r"\s+", "_") # replace " " or "  " (or more consecutive space characters) with just one "_"
        .name.replace(".", "", literal=True) # replace "." with empty string (remove it), literal=True to deactive regex
        .name.to_lowercase()
    )
)

print(tl_pokemon.head(5).collect())
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

##-------------------------------##
## f('col').cast(tp.Categorical) ##
##-------------------------------##

print(
    tl_pokemon
    .mutate(
        f('type_1', 'type_2').cast(tp.Categorical) # or `.cast(tp.String).cast(tp.Categorical)` would be safer
    )
    .select(tp.nth(range(4))) # first 4 columns
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

##-----------------------------------------------------------------##
## f('col').pipe(tp.as_categorical) or f('col').pipe(tp.as_factor) ##
##-----------------------------------------------------------------##

print(
    tl_pokemon
    .mutate(
        f('type_1', 'type_2').pipe(tp.as_categorical) # or `pipe(tp.as_factor)`
    )
    .select(tp.nth(range(4))) # first 4 columns
    .head(5)
    .collect()
)

##---------------------------------------------------------##
## col=tp.as_categorical('col') or col=tp.as_factor('col') ##
##---------------------------------------------------------##

print(
    tl_pokemon
    .mutate(
        type_1=tp.as_factor('type_1'),
        type_2=tp.as_factor('type_2')
    )
    .select(tp.nth(range(4))) # first 4 columns
    .head(5)
    .collect()
)

# ================================================================================
# 2. Enum: ordered categories
# ================================================================================

##-----------------------------##
## Conversion with known enums ##
##-----------------------------##

### f('col').cast(tp.Enum([list_of_known_enums])) ###
print(
    tl_pokemon
    .mutate(
        f('generation').cast(tp.String).cast(tp.Enum([str(gen) for gen in range(1, 7)])) # tp.Enum(["1", "2", "3", "4", "5", "6"])
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

### f('col').pipe(tp.as_enum, [list_of_known_enums]) ###
print(
    tl_pokemon
    .mutate(
        f('generation').pipe(tp.as_enum, [str(gen) for gen in range(1, 7)]) # or can use tp.as_ordered
    )
    .select("name", "generation")
    .head(5)
    .collect()
)

### col=tp.as_enum('col', [list_of_known_enums]) ###
print(
    tl_pokemon
    .mutate(
        generation=tp.as_enum('generation', [str(gen) for gen in range(1, 7)]) # or can use tp.as_ordered
    )
    .select("name", "generation")
    .head(5)
    .collect()
)

##-------------------------------------------##
## Conversion with internally inferred enums ##
##-------------------------------------------##
'''
NOTE: the internal inference is based on a-z and 0-9 order.
      If your Enum does not follow this pattern, please don't use the code of this section.

The below code uses `tp.as_enum` to demonstrate,
but `tp.as_ordered` also work the same
'''

### f('col').pipe(tp.as_enum, f.select('col')) ###
print(
    tl_pokemon
    .mutate(
        f('generation').pipe(tp.as_enum, f.select('generation')) # or f.sl('generation')
    )
    .select("name", "generation")
    .head(5)
    .collect()
)

### f('col').pipe(tp.as_enum, f.pull('col')) ###
print(
    tl_pokemon
    .mutate(
        f('generation').pipe(tp.as_enum, f.pull('generation'))
    )
    .select("name", "generation")
    .head(5)
    .collect()
)

### col=tp.as_enum(f.select('col')) ###
print(
    tl_pokemon
    .mutate(
        generation=tp.as_enum(f.select('generation'))
    )
    .select("name", "generation")
    .head(5)
    .collect()
)

##------------------------------------------------------------------------------##
## Filter enums with relationship operators (>, <, =, >=, <=, !=, is_between()) ##
##------------------------------------------------------------------------------##
'''
Should set the categories in ascending order, like:
# Categories (6, int64): [1 < 2 < 3 < 4 < 5 < 6]
'''

print(
    tl_pokemon
    .mutate(
        f('generation').pipe(tp.as_enum, f.pull('generation'))
    )
    .select('name', 'generation')
    .filter(f('generation') > '3')
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
    tl_pokemon
    .mutate(
        f('generation').pipe(tp.as_enum, f.pull('generation'))
    )
    .select('name', 'generation')
    .filter(f('generation').is_between(tp.lit("3"), tp.lit("5"), closed="both")) # don't forget tp.lit()
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
    tl_pokemon
    .mutate(
        f('legendary').cast(tp.Boolean) # or f('col').pipe(tp.as_boolean)
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
    tl_pokemon
    .mutate(
        f('legendary').pipe(tp.as_boolean)
    )
    .select('name', 'generation', 'legendary')
    .filter('legendary') # or `.filter(f('legendary'))`
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

print(
    tl_pokemon
    .mutate(
        f('legendary').cast(tp.Boolean)
    )
    .select('name', 'generation', 'legendary')
    .remove('legendary')
    .filter(~f('legendary')) # or `.remove('legendary')` or `.remove(f('legendary'))`
    .collect()
)
# shape: (735, 3)
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
# │ GourgeistSuper Size   ┆ 6          ┆ false     │
# │ Bergmite              ┆ 6          ┆ false     │
# │ Avalugg               ┆ 6          ┆ false     │
# │ Noibat                ┆ 6          ┆ false     │
# │ Noivern               ┆ 6          ┆ false     │
# └───────────────────────┴────────────┴───────────┘
