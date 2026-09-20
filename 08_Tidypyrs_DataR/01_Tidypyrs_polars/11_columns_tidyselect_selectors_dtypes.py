'''
tidypyrs provides several functions to facilitate collumn selection,
especially for selecting based on columns' name string pattern or dtypes.

tidypyrs also reexports `polars.selectors` as `tidypyrs.selectors`
for anyone prefers polars APIs.

1. Selecting based on name's pattern:
    + tp.starts_with()
    + tp.ends_with()
    + tp.contains()

2. Selecting based on dtypes: tp.where()

3. Selecting all: tp.everything()

4. Selecting with set operations

5. Selecting with `tp.selectors`: works like `polars.selectors`
'''

from pathlib import Path

import tidypyrs as tp  # noqa: I001
from tidypyrs import f
from tidypyrs import selectors as cs

tp.Config(tbl_width_chars=130, tbl_rows=5, tbl_cols=13)
data_dir = next(Path("/home").glob("**/DataScience*/data"))

tl_pokemon = (
    tp.scan_csv(data_dir/"pokemon.csv")
    .drop("#")
    .row_index()
    .select(f.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .mutate(
        f("type_1", "type_2").cast(tp.Categorical),
        f("generation").pipe(tp.as_enum, f.pull("generation"))
    )
)

print(tl_pokemon.collect())
# shape: (800, 13)
# ┌───────┬────────────┬─────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ index ┆ name       ┆ type_1  ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ ---   ┆ ---        ┆ ---     ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ u32   ┆ str        ┆ cat     ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═══════╪════════════╪═════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ 0     ┆ Bulbasaur  ┆ Grass   ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 1     ┆ Ivysaur    ┆ Grass   ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 2     ┆ Venusaur   ┆ Grass   ┆ Poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ …    ┆ …          ┆ …      ┆ …     ┆ …     ┆ …  ┆ …      ┆ …      ┆ …      ┆ …     ┆ …    ┆ …          ┆ …        │
# │ 798   ┆ HoopaHoopa ┆ Psychic ┆ Dark   ┆ 680   ┆ 80  ┆ 160    ┆ 60      ┆ 170    ┆ 130    ┆ 80    ┆ 6          ┆ true      │
# │       ┆ Unbound    ┆         ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ 799   ┆ Volcanion  ┆ Fire    ┆ Water  ┆ 600   ┆ 80  ┆ 110    ┆ 120     ┆ 130    ┆ 90     ┆ 70    ┆ 6          ┆ true      │
# └───────┴────────────┴─────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

# =======================================================================
# 1. Selecting based on name's pattern
# =======================================================================

##------------------##
## tp.starts_with() ##
##------------------##

print(
    tl_pokemon
    .select(tp.starts_with("type_"))
    .collect()
)
# shape: (800, 2)
# ┌─────────┬────────┐
# │ type_1  ┆ type_2 │
# │ ---     ┆ ---    │
# │ cat     ┆ cat    │
# ╞═════════╪════════╡
# │ Grass   ┆ Poison │
# │ Grass   ┆ Poison │
# │ Grass   ┆ Poison │
# │ …      ┆ …      │
# │ Psychic ┆ Dark   │
# │ Fire    ┆ Water  │
# └─────────┴────────┘

##----------------##
## tp.ends_with() ##
##----------------##

print(
    tl_pokemon
    .select(tp.ends_with("e"))
    .collect()
)
# shape: (800, 2)
# ┌────────────────────┬─────────┐
# │ name               ┆ defense │
# │ ---                ┆ ---     │
# │ str                ┆ i64     │
# ╞════════════════════╪═════════╡
# │ Bulbasaur          ┆ 49      │
# │ Ivysaur            ┆ 63      │
# │ Venusaur           ┆ 83      │
# │ …                 ┆ …       │
# │ HoopaHoopa Unbound ┆ 60      │
# │ Volcanion          ┆ 120     │
# └────────────────────┴─────────┘

##---------------##
## tp.contains() ##
##---------------##

print(
    tl_pokemon
    .select(tp.contains("ta")) # Only supports literal string, not regex pattern
    .collect()
)
# shape: (800, 2)
# ┌───────┬────────┐
# │ total ┆ attack │
# │ ---   ┆ ---    │
# │ i64   ┆ i64    │
# ╞═══════╪════════╡
# │ 318   ┆ 49     │
# │ 405   ┆ 62     │
# │ 525   ┆ 82     │
# │ …    ┆ …      │
# │ 680   ┆ 160    │
# │ 600   ┆ 110    │
# └───────┴────────┘

# =======================================================================
# 2. Selecting based on dtypes: tp.where()
# =======================================================================
'''
Currently, `tp.where()` supports these dtype inputs
(and its `polars.selectors` counterparts)

_col_types = {
    "date": cs.date(),
    "datetime": cs.datetime(),
    "temporal": cs.temporal(),
    "float": cs.float(),
    "integer": cs.integer(),
    "numeric": cs.numeric(),
    "string": cs.string(),
    "categorical": cs.categorical(),
    "factor": cs.categorical(),
    "ordered": cs.enum(),
    "enum": cs.enum(),
}
'''

print(
    tl_pokemon
    .select(tp.where("numeric"))
    .collect()
)
# shape: (800, 8)
# ┌───────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┐
# │ index ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed │
# │ ---   ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   │
# │ u32   ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   │
# ╞═══════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╡
# │ 0     ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    │
# │ 1     ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    │
# │ 2     ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    │
# │ …    ┆ …     ┆ …  ┆ …      ┆ …       ┆ …      ┆ …      ┆ …     │
# │ 798   ┆ 680   ┆ 80  ┆ 160    ┆ 60      ┆ 170    ┆ 130    ┆ 80    │
# │ 799   ┆ 600   ┆ 80  ┆ 110    ┆ 120     ┆ 130    ┆ 90     ┆ 70    │
# └───────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┘

print(
    tl_pokemon
    .select(tp.where("categorical"))
    .collect()
)
# shape: (800, 2)
# ┌─────────┬────────┐
# │ type_1  ┆ type_2 │
# │ ---     ┆ ---    │
# │ cat     ┆ cat    │
# ╞═════════╪════════╡
# │ Grass   ┆ Poison │
# │ Grass   ┆ Poison │
# │ Grass   ┆ Poison │
# │ …      ┆ …      │
# │ Psychic ┆ Dark   │
# │ Fire    ┆ Water  │
# └─────────┴────────┘

# =======================================================================
# 3. Selecting all: tp.everything()
# =======================================================================

print(
    tl_pokemon
    .select(tp.everything()) # select all columns
    .collect()
)
# shape: (800, 13)
# ┌───────┬────────────┬─────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ index ┆ name       ┆ type_1  ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ ---   ┆ ---        ┆ ---     ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ u32   ┆ str        ┆ cat     ┆ cat    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═══════╪════════════╪═════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
# │ 0     ┆ Bulbasaur  ┆ Grass   ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 1     ┆ Ivysaur    ┆ Grass   ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 2     ┆ Venusaur   ┆ Grass   ┆ Poison ┆ 525   ┆ 80  ┆ 82     ┆ 83      ┆ 100    ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ …     ┆ …         ┆ …       ┆ …      ┆ …     ┆ …   ┆ …      ┆ …       ┆ …      ┆ …      ┆ …     ┆ …          ┆ …         │
# │ 798   ┆ HoopaHoopa ┆ Psychic ┆ Dark   ┆ 680   ┆ 80  ┆ 160    ┆ 60      ┆ 170    ┆ 130    ┆ 80    ┆ 6          ┆ true      │
# │       ┆ Unbound    ┆         ┆        ┆       ┆     ┆        ┆         ┆        ┆        ┆       ┆            ┆           │
# │ 799   ┆ Volcanion  ┆ Fire    ┆ Water  ┆ 600   ┆ 80  ┆ 110    ┆ 120     ┆ 130    ┆ 90     ┆ 70    ┆ 6          ┆ true      │
# └───────┴────────────┴─────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘

# =======================================================================
# 4. Selecting with set operations
# =======================================================================
'''
+ A | B  -> union
+ A & B  -> intersection
+ A - B  -> difference
+ A ^ B  -> symmetric difference
+ ~A     -> complement
'''

print(
    tl_pokemon
    .select(tp.contains("e") & tp.where("numeric"))
    .collect()
)
# shape: (800, 4)
# ┌───────┬─────────┬────────┬───────┐
# │ index ┆ defense ┆ sp_def ┆ speed │
# │ ---   ┆ ---     ┆ ---    ┆ ---   │
# │ u32   ┆ i64     ┆ i64    ┆ i64   │
# ╞═══════╪═════════╪════════╪═══════╡
# │ 0     ┆ 49      ┆ 65     ┆ 45    │
# │ 1     ┆ 63      ┆ 80     ┆ 60    │
# │ 2     ┆ 83      ┆ 100    ┆ 80    │
# │ …     ┆ …       ┆ …      ┆ …     │
# │ 798   ┆ 60      ┆ 130    ┆ 80    │
# │ 799   ┆ 120     ┆ 90     ┆ 70    │
# └───────┴─────────┴────────┴───────┘


print(
    tl_pokemon
    .select(tp.where("categorical") | tp.where("enum"))
    .collect()
)
# shape: (800, 3)
# ┌─────────┬────────┬────────────┐
# │ type_1  ┆ type_2 ┆ generation │
# │ ---     ┆ ---    ┆ ---        │
# │ cat     ┆ cat    ┆ enum       │
# ╞═════════╪════════╪════════════╡
# │ Grass   ┆ Poison ┆ 1          │
# │ Grass   ┆ Poison ┆ 1          │
# │ Grass   ┆ Poison ┆ 1          │
# │ …       ┆ …      ┆ …          │
# │ Psychic ┆ Dark   ┆ 6          │
# │ Fire    ┆ Water  ┆ 6          │
# └─────────┴────────┴────────────┘

# =======================================================================
# 5. Selecting with `tp.selectors`: works like `polars.selectors`
# =======================================================================

print(
    tl_pokemon
    .select(cs.contains("e") & cs.numeric())
    .collect()
)
# shape: (800, 4)
# ┌───────┬─────────┬────────┬───────┐
# │ index ┆ defense ┆ sp_def ┆ speed │
# │ ---   ┆ ---     ┆ ---    ┆ ---   │
# │ u32   ┆ i64     ┆ i64    ┆ i64   │
# ╞═══════╪═════════╪════════╪═══════╡
# │ 0     ┆ 49      ┆ 65     ┆ 45    │
# │ 1     ┆ 63      ┆ 80     ┆ 60    │
# │ 2     ┆ 83      ┆ 100    ┆ 80    │
# │ …     ┆ …       ┆ …      ┆ …     │
# │ 798   ┆ 60      ┆ 130    ┆ 80    │
# │ 799   ┆ 120     ┆ 90     ┆ 70    │
# └───────┴─────────┴────────┴───────┘

print(
    tl_pokemon
    .select(cs.categorical() | cs.enum())
    .collect()
)
# shape: (800, 3)
# ┌─────────┬────────┬────────────┐
# │ type_1  ┆ type_2 ┆ generation │
# │ ---     ┆ ---    ┆ ---        │
# │ cat     ┆ cat    ┆ enum       │
# ╞═════════╪════════╪════════════╡
# │ Grass   ┆ Poison ┆ 1          │
# │ Grass   ┆ Poison ┆ 1          │
# │ Grass   ┆ Poison ┆ 1          │
# │ …       ┆ …      ┆ …          │
# │ Psychic ┆ Dark   ┆ 6          │
# │ Fire    ┆ Water  ┆ 6          │
# └─────────┴────────┴────────────┘
