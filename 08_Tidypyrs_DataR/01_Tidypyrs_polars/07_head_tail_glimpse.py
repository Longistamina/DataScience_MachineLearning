'''
tidypyrs TibbleFrame and LazyFrame have these 4 methods:
    + `head(n)` and `slice_head(n)`: shows the first n rows
    + `tail(n)` and `slice_tail(n)`: shows the last n rows

They all have `over` parameter to perform group-by operations

1. `head(n)` and `slice_head(n)`: shows the first n rows
2. `tail(n)` and `slice_tail(n)`: shows the last n rows
3. `glimpse(max_items_per_column, max_colname_length, return_type)`: give an overview of the frame
'''

import tidypyrs as tp  # noqa: I001
from tidypyrs import f
from pathlib import Path

tp.Config(tbl_width_chars=120)
data_dir = next(Path("/home").glob("**/DataScience*/data"))

tl_pokemon = (
    tp.scan_csv(data_dir/"pokemon.csv")
    .select(f.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .mutate(
        f("type_1", "type_2").pipe(tp.as_categorical),
        f("generation").pipe(tp.as_enum, f.pull("generation"))
    )
)

print(tl_pokemon.collect())
# shape: (800, 13)
# ┌─────┬────────────────────┬─────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name               ┆ type_1  ┆ type_2 ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---                ┆ ---     ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                ┆ cat     ┆ cat    ┆   ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═════╪════════════════════╪═════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 1   ┆ Bulbasaur          ┆ Grass   ┆ Poison ┆ … ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 2   ┆ Ivysaur            ┆ Grass   ┆ Poison ┆ … ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 3   ┆ Venusaur           ┆ Grass   ┆ Poison ┆ … ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ …   ┆ …                 ┆ …       ┆ …     ┆ … ┆ …      ┆ …     ┆ …          ┆ …         │
# │ 720 ┆ HoopaHoopa Unbound ┆ Psychic ┆ Dark   ┆ … ┆ 130    ┆ 80    ┆ 6          ┆ true      │
# │ 721 ┆ Volcanion          ┆ Fire    ┆ Water  ┆ … ┆ 90     ┆ 70    ┆ 6          ┆ true      │
# └─────┴────────────────────┴─────────┴────────┴───┴────────┴───────┴────────────┴───────────┘

# ===================================================================================================
# 1. `head(n)` and `slice_head(n)`: shows the first n rows
# ===================================================================================================

##------------------------------------------##
## General usage of `head` and `slice_head` ##
##------------------------------------------##

print(
    tl_pokemon
    .head(4) # It will use n=5 as default if not provided
    .collect()
)
# shape: (4, 13)
# ┌─────┬───────────────────────┬────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name                  ┆ type_1 ┆ type_2 ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---                   ┆ ---    ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                   ┆ cat    ┆ cat    ┆   ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═════╪═══════════════════════╪════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 1   ┆ Bulbasaur             ┆ Grass  ┆ Poison ┆ … ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 2   ┆ Ivysaur               ┆ Grass  ┆ Poison ┆ … ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 3   ┆ Venusaur              ┆ Grass  ┆ Poison ┆ … ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ 3   ┆ VenusaurMega Venusaur ┆ Grass  ┆ Poison ┆ … ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# └─────┴───────────────────────┴────────┴────────┴───┴────────┴───────┴────────────┴───────────┘

print(
    tl_pokemon
    .slice_head(8) # It will use n=5 as default if not provided
    .collect()
)
# shape: (8, 13)
# ┌─────┬───────────────────────────┬────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name                      ┆ type_1 ┆ type_2 ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---                       ┆ ---    ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                       ┆ cat    ┆ cat    ┆   ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═════╪═══════════════════════════╪════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 1   ┆ Bulbasaur                 ┆ Grass  ┆ Poison ┆ … ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 2   ┆ Ivysaur                   ┆ Grass  ┆ Poison ┆ … ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 3   ┆ Venusaur                  ┆ Grass  ┆ Poison ┆ … ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ 3   ┆ VenusaurMega Venusaur     ┆ Grass  ┆ Poison ┆ … ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ 4   ┆ Charmander                ┆ Fire   ┆ null   ┆ … ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# │ 5   ┆ Charmeleon                ┆ Fire   ┆ null   ┆ … ┆ 65     ┆ 80    ┆ 1          ┆ false     │
# │ 6   ┆ Charizard                 ┆ Fire   ┆ Flying ┆ … ┆ 85     ┆ 100   ┆ 1          ┆ false     │
# │ 6   ┆ CharizardMega Charizard X ┆ Fire   ┆ Dragon ┆ … ┆ 85     ┆ 100   ┆ 1          ┆ false     │
# └─────┴───────────────────────────┴────────┴────────┴───┴────────┴───────┴────────────┴───────────┘

##---------------------------##
## Use with `over` parameter ##
##---------------------------##

print(
    tl_pokemon
    .head(2, over="generation")
    .collect()
)
# shape: (12, 13)
# ┌─────┬───────────┬─────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name      ┆ type_1  ┆ type_2 ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---       ┆ ---     ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str       ┆ cat     ┆ cat    ┆   ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═════╪═══════════╪═════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 1   ┆ Bulbasaur ┆ Grass   ┆ Poison ┆ … ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 2   ┆ Ivysaur   ┆ Grass   ┆ Poison ┆ … ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 152 ┆ Chikorita ┆ Grass   ┆ null   ┆ … ┆ 65     ┆ 45    ┆ 2          ┆ false     │
# │ 153 ┆ Bayleef   ┆ Grass   ┆ null   ┆ … ┆ 80     ┆ 60    ┆ 2          ┆ false     │
# │ 252 ┆ Treecko   ┆ Grass   ┆ null   ┆ … ┆ 55     ┆ 70    ┆ 3          ┆ false     │
# │ …   ┆ …         ┆ …       ┆ …      ┆ … ┆ …      ┆ …     ┆ …          ┆ …         │
# │ 388 ┆ Grotle    ┆ Grass   ┆ null   ┆ … ┆ 65     ┆ 36    ┆ 4          ┆ false     │
# │ 494 ┆ Victini   ┆ Psychic ┆ Fire   ┆ … ┆ 100    ┆ 100   ┆ 5          ┆ true      │
# │ 495 ┆ Snivy     ┆ Grass   ┆ null   ┆ … ┆ 55     ┆ 63    ┆ 5          ┆ false     │
# │ 650 ┆ Chespin   ┆ Grass   ┆ null   ┆ … ┆ 45     ┆ 38    ┆ 6          ┆ false     │
# │ 651 ┆ Quilladin ┆ Grass   ┆ null   ┆ … ┆ 58     ┆ 57    ┆ 6          ┆ false     │
# └─────┴───────────┴─────────┴────────┴───┴────────┴───────┴────────────┴───────────┘

print(
    tl_pokemon
    .slice_head(4, over="legendary")
    .collect()
)
# shape: (8, 13)
# ┌─────┬───────────────────────┬──────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name                  ┆ type_1   ┆ type_2 ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---                   ┆ ---      ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                   ┆ cat      ┆ cat    ┆   ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═════╪═══════════════════════╪══════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 1   ┆ Bulbasaur             ┆ Grass    ┆ Poison ┆ … ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 2   ┆ Ivysaur               ┆ Grass    ┆ Poison ┆ … ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 3   ┆ Venusaur              ┆ Grass    ┆ Poison ┆ … ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ 3   ┆ VenusaurMega Venusaur ┆ Grass    ┆ Poison ┆ … ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ 144 ┆ Articuno              ┆ Ice      ┆ Flying ┆ … ┆ 125    ┆ 85    ┆ 1          ┆ true      │
# │ 145 ┆ Zapdos                ┆ Electric ┆ Flying ┆ … ┆ 90     ┆ 100   ┆ 1          ┆ true      │
# │ 146 ┆ Moltres               ┆ Fire     ┆ Flying ┆ … ┆ 85     ┆ 90    ┆ 1          ┆ true      │
# │ 150 ┆ Mewtwo                ┆ Psychic  ┆ null   ┆ … ┆ 90     ┆ 130   ┆ 1          ┆ true      │
# └─────┴───────────────────────┴──────────┴────────┴───┴────────┴───────┴────────────┴───────────┘

# ===================================================================================================
# 2. `tail(n)` and `slice_tail(n)`: shows the last n rows
# ===================================================================================================

##------------------------------------------##
## General usage of `tail` and `slice_tail` ##
##------------------------------------------##

print(
    tl_pokemon
    .tail(4) # It will use n=5 as default if not provided
    .collect()
)
# shape: (4, 13)
# ┌─────┬─────────────────────┬─────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name                ┆ type_1  ┆ type_2 ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---                 ┆ ---     ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                 ┆ cat     ┆ cat    ┆   ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═════╪═════════════════════╪═════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 719 ┆ DiancieMega Diancie ┆ Rock    ┆ Fairy  ┆ … ┆ 110    ┆ 110   ┆ 6          ┆ true      │
# │ 720 ┆ HoopaHoopa Confined ┆ Psychic ┆ Ghost  ┆ … ┆ 130    ┆ 70    ┆ 6          ┆ true      │
# │ 720 ┆ HoopaHoopa Unbound  ┆ Psychic ┆ Dark   ┆ … ┆ 130    ┆ 80    ┆ 6          ┆ true      │
# │ 721 ┆ Volcanion           ┆ Fire    ┆ Water  ┆ … ┆ 90     ┆ 70    ┆ 6          ┆ true      │
# └─────┴─────────────────────┴─────────┴────────┴───┴────────┴───────┴────────────┴───────────┘

print(
    tl_pokemon
    .slice_tail(8) # It will use n=5 as default if not provided
    .collect()
)
# shape: (8, 13)
# ┌─────┬─────────────────────┬─────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name                ┆ type_1  ┆ type_2 ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---                 ┆ ---     ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                 ┆ cat     ┆ cat    ┆   ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═════╪═════════════════════╪═════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 716 ┆ Xerneas             ┆ Fairy   ┆ null   ┆ … ┆ 98     ┆ 99    ┆ 6          ┆ true      │
# │ 717 ┆ Yveltal             ┆ Dark    ┆ Flying ┆ … ┆ 98     ┆ 99    ┆ 6          ┆ true      │
# │ 718 ┆ Zygarde50% Forme    ┆ Dragon  ┆ Ground ┆ … ┆ 95     ┆ 95    ┆ 6          ┆ true      │
# │ 719 ┆ Diancie             ┆ Rock    ┆ Fairy  ┆ … ┆ 150    ┆ 50    ┆ 6          ┆ true      │
# │ 719 ┆ DiancieMega Diancie ┆ Rock    ┆ Fairy  ┆ … ┆ 110    ┆ 110   ┆ 6          ┆ true      │
# │ 720 ┆ HoopaHoopa Confined ┆ Psychic ┆ Ghost  ┆ … ┆ 130    ┆ 70    ┆ 6          ┆ true      │
# │ 720 ┆ HoopaHoopa Unbound  ┆ Psychic ┆ Dark   ┆ … ┆ 130    ┆ 80    ┆ 6          ┆ true      │
# │ 721 ┆ Volcanion           ┆ Fire    ┆ Water  ┆ … ┆ 90     ┆ 70    ┆ 6          ┆ true      │
# └─────┴─────────────────────┴─────────┴────────┴───┴────────┴───────┴────────────┴───────────┘

##---------------------------##
## Use with `over` parameter ##
##---------------------------##

print(
    tl_pokemon
    .tail(2, over="generation")
    .collect()
)
# shape: (12, 13)
# ┌─────┬─────────────────────────┬─────────┬──────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name                    ┆ type_1  ┆ type_2   ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---                     ┆ ---     ┆ ---      ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                     ┆ cat     ┆ cat      ┆   ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═════╪═════════════════════════╪═════════╪══════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 150 ┆ MewtwoMega Mewtwo Y     ┆ Psychic ┆ null     ┆ … ┆ 120    ┆ 140   ┆ 1          ┆ true      │
# │ 151 ┆ Mew                     ┆ Psychic ┆ null     ┆ … ┆ 100    ┆ 100   ┆ 1          ┆ false     │
# │ 250 ┆ Ho-oh                   ┆ Fire    ┆ Flying   ┆ … ┆ 154    ┆ 90    ┆ 2          ┆ true      │
# │ 251 ┆ Celebi                  ┆ Psychic ┆ Grass    ┆ … ┆ 100    ┆ 100   ┆ 2          ┆ false     │
# │ 386 ┆ DeoxysDefense Forme     ┆ Psychic ┆ null     ┆ … ┆ 160    ┆ 90    ┆ 3          ┆ true      │
# │ …   ┆ …                       ┆ …       ┆ …        ┆ … ┆ …      ┆ …     ┆ …          ┆ …         │
# │ 493 ┆ Arceus                  ┆ Normal  ┆ null     ┆ … ┆ 120    ┆ 120   ┆ 4          ┆ true      │
# │ 648 ┆ MeloettaPirouette Forme ┆ Normal  ┆ Fighting ┆ … ┆ 77     ┆ 128   ┆ 5          ┆ false     │
# │ 649 ┆ Genesect                ┆ Bug     ┆ Steel    ┆ … ┆ 95     ┆ 99    ┆ 5          ┆ false     │
# │ 720 ┆ HoopaHoopa Unbound      ┆ Psychic ┆ Dark     ┆ … ┆ 130    ┆ 80    ┆ 6          ┆ true      │
# │ 721 ┆ Volcanion               ┆ Fire    ┆ Water    ┆ … ┆ 90     ┆ 70    ┆ 6          ┆ true      │
# └─────┴─────────────────────────┴─────────┴──────────┴───┴────────┴───────┴────────────┴───────────┘

print(
    tl_pokemon
    .slice_tail(4, over="legendary")
    .collect()
)
# shape: (8, 13)
# ┌─────┬─────────────────────┬─────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name                ┆ type_1  ┆ type_2 ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---                 ┆ ---     ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                 ┆ cat     ┆ cat    ┆   ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═════╪═════════════════════╪═════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 712 ┆ Bergmite            ┆ Ice     ┆ null   ┆ … ┆ 35     ┆ 28    ┆ 6          ┆ false     │
# │ 713 ┆ Avalugg             ┆ Ice     ┆ null   ┆ … ┆ 46     ┆ 28    ┆ 6          ┆ false     │
# │ 714 ┆ Noibat              ┆ Flying  ┆ Dragon ┆ … ┆ 40     ┆ 55    ┆ 6          ┆ false     │
# │ 715 ┆ Noivern             ┆ Flying  ┆ Dragon ┆ … ┆ 80     ┆ 123   ┆ 6          ┆ false     │
# │ 719 ┆ DiancieMega Diancie ┆ Rock    ┆ Fairy  ┆ … ┆ 110    ┆ 110   ┆ 6          ┆ true      │
# │ 720 ┆ HoopaHoopa Confined ┆ Psychic ┆ Ghost  ┆ … ┆ 130    ┆ 70    ┆ 6          ┆ true      │
# │ 720 ┆ HoopaHoopa Unbound  ┆ Psychic ┆ Dark   ┆ … ┆ 130    ┆ 80    ┆ 6          ┆ true      │
# │ 721 ┆ Volcanion           ┆ Fire    ┆ Water  ┆ … ┆ 90     ┆ 70    ┆ 6          ┆ true      │
# └─────┴─────────────────────┴─────────┴────────┴───┴────────┴───────┴────────────┴───────────┘

# ===================================================================================================
# 3. `glimpse()`: give an overview of the frame
# ===================================================================================================
'''
NOTE: Only TibbleFrame has `glimpse()` method.
      For TibbleLazy, uses `.collect().glimpse()`
'''

print(
    tl_pokemon
    .collect()
    .glimpse()
)
# Rows: 800
# Columns: 13
# $ #           <i64> 1, 2, 3, 3, 4
# $ name        <str> 'Bulbasaur', 'Ivysaur', 'Venusaur', 'VenusaurMega Venusaur', 'Charmander'
# $ type_1      <cat> Grass, Grass, Grass, Grass, Fire
# $ type_2      <cat> Poison, Poison, Poison, Poison, null
# $ total       <i64> 318, 405, 525, 625, 309
# $ hp          <i64> 45, 60, 80, 80, 39
# $ attack      <i64> 49, 62, 82, 100, 52
# $ defense     <i64> 49, 63, 83, 123, 43
# $ sp_atk      <i64> 65, 80, 100, 122, 60
# $ sp_def      <i64> 65, 80, 100, 120, 50
# $ speed       <i64> 45, 60, 80, 80, 65
# $ generation <enum> 1, 1, 1, 1, 1
# $ legendary  <bool> False, False, False, False, False
# None

print(
    tl_pokemon
    .collect()
    .glimpse(max_items_per_column=3)
)
# Rows: 800
# Columns: 13
# $ #           <i64> 1, 2, 3
# $ name        <str> 'Bulbasaur', 'Ivysaur', 'Venusaur'
# $ type_1      <cat> Grass, Grass, Grass
# $ type_2      <cat> Poison, Poison, Poison
# $ total       <i64> 318, 405, 525
# $ hp          <i64> 45, 60, 80
# $ attack      <i64> 49, 62, 82
# $ defense     <i64> 49, 63, 83
# $ sp_atk      <i64> 65, 80, 100
# $ sp_def      <i64> 65, 80, 100
# $ speed       <i64> 45, 60, 80
# $ generation <enum> 1, 1, 1
# $ legendary  <bool> False, False, False
# None

print(
    tl_pokemon
    .collect()
    .glimpse(max_colname_length=4)
)
# Rows: 800
# Columns: 13
# $ #     <i64> 1, 2, 3, 3, 4
# $ name  <str> 'Bulbasaur', 'Ivysaur', 'Venusaur', 'VenusaurMega Venusaur', 'Charmander'
# $ typ…  <cat> Grass, Grass, Grass, Grass, Fire
# $ typ…  <cat> Poison, Poison, Poison, Poison, null
# $ tot…  <i64> 318, 405, 525, 625, 309
# $ hp    <i64> 45, 60, 80, 80, 39
# $ att…  <i64> 49, 62, 82, 100, 52
# $ def…  <i64> 49, 63, 83, 123, 43
# $ sp_…  <i64> 65, 80, 100, 122, 60
# $ sp_…  <i64> 65, 80, 100, 120, 50
# $ spe…  <i64> 45, 60, 80, 80, 65
# $ gen… <enum> 1, 1, 1, 1, 1
# $ leg… <bool> False, False, False, False, False
# None

print(
    tl_pokemon
    .collect()
    .glimpse(return_type="frame")
)
# shape: (13, 3)
# ┌────────────┬───────┬─────────────────────────────────┐
# │ column     ┆ dtype ┆ values                          │
# │ ---        ┆ ---   ┆ ---                             │
# │ str        ┆ str   ┆ list[str]                       │
# ╞════════════╪═══════╪═════════════════════════════════╡
# │ #          ┆ i64   ┆ ["1", "2", … "4"]               │
# │ name       ┆ str   ┆ ["'Bulbasaur'", "'Ivysaur'", …… │
# │ type_1     ┆ cat   ┆ ["Grass", "Grass", … "Fire"]    │
# │ type_2     ┆ cat   ┆ ["Poison", "Poison", … null]    │
# │ total      ┆ i64   ┆ ["318", "405", … "309"]         │
# │ …          ┆ …     ┆ …                               │
# │ sp_atk     ┆ i64   ┆ ["65", "80", … "60"]            │
# │ sp_def     ┆ i64   ┆ ["65", "80", … "50"]            │
# │ speed      ┆ i64   ┆ ["45", "60", … "65"]            │
# │ generation ┆ enum  ┆ ["1", "1", … "1"]               │
# │ legendary  ┆ bool  ┆ ["False", "False", … "False"]   │
# └────────────┴───────┴─────────────────────────────────┘

# Use positional arguments
print(
    tl_pokemon
    .collect()
    .glimpse(10, 10, "frame")
)
# shape: (13, 3)
# ┌────────────┬───────┬─────────────────────────────────┐
# │ column     ┆ dtype ┆ values                          │
# │ ---        ┆ ---   ┆ ---                             │
# │ str        ┆ str   ┆ list[str]                       │
# ╞════════════╪═══════╪═════════════════════════════════╡
# │ #          ┆ i64   ┆ ["1", "2", … "7"]               │
# │ name       ┆ str   ┆ ["'Bulbasaur'", "'Ivysaur'", …… │
# │ type_1     ┆ cat   ┆ ["Grass", "Grass", … "Water"]   │
# │ type_2     ┆ cat   ┆ ["Poison", "Poison", … null]    │
# │ total      ┆ i64   ┆ ["318", "405", … "314"]         │
# │ …          ┆ …     ┆ …                               │
# │ sp_atk     ┆ i64   ┆ ["65", "80", … "50"]            │
# │ sp_def     ┆ i64   ┆ ["65", "80", … "64"]            │
# │ speed      ┆ i64   ┆ ["45", "60", … "43"]            │
# │ generation ┆ enum  ┆ ["1", "1", … "1"]               │
# │ legendary  ┆ bool  ┆ ["False", "False", … "False"]   │
# └────────────┴───────┴─────────────────────────────────┘
