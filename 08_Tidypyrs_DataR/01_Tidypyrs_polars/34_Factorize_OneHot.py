'''
There are 2 main ways to encoding categorical data into numeric codes:
    1. Factorize: `f('col').cast(tp.Categorical).to_physical()`
    2. One-Hot encoding: `tl.collect().to_dummies(collumns=[...], drop_fist=True)`
                         (`to_dummies` is available for eager DataFrame only)
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
    tp.scan_csv(data_dir/'pokemon.csv')
    .rename(lambda name: name.strip())
    .select(f.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .select('name', 'type_1', 'type_2')
    .mutate(
        f('type_1', 'type_2').cast(tp.Categorical)
    )
)

print(tl_pokemon.collect())
# shape: (800, 3)
# ┌───────────────────────┬─────────┬────────┐
# │ name                  ┆ type_1  ┆ type_2 │
# │ ---                   ┆ ---     ┆ ---    │
# │ str                   ┆ cat     ┆ cat    │
# ╞═══════════════════════╪═════════╪════════╡
# │ Bulbasaur             ┆ Grass   ┆ Poison │
# │ Ivysaur               ┆ Grass   ┆ Poison │
# │ Venusaur              ┆ Grass   ┆ Poison │
# │ VenusaurMega Venusaur ┆ Grass   ┆ Poison │
# │ Charmander            ┆ Fire    ┆ null   │
# │ …                     ┆ …       ┆ …      │
# │ Diancie               ┆ Rock    ┆ Fairy  │
# │ DiancieMega Diancie   ┆ Rock    ┆ Fairy  │
# │ HoopaHoopa Confined   ┆ Psychic ┆ Ghost  │
# │ HoopaHoopa Unbound    ┆ Psychic ┆ Dark   │
# │ Volcanion             ┆ Fire    ┆ Water  │
# └───────────────────────┴─────────┴────────┘

# ====================================================================================
# 1. Factorize: `f('col').cast(tp.Categorical).to_physical()`
# ====================================================================================

print(
    tl_pokemon
    .mutate(
        f('type_1').cast(tp.Categorical).to_physical().alias('type_1_enc'),
        f('type_2').cast(tp.Categorical).to_physical().alias('type_2_enc'),
    )
    .collect()
)
# shape: (800, 5)
# ┌───────────────────────┬─────────┬────────┬────────────┬────────────┐
# │ name                  ┆ type_1  ┆ type_2 ┆ type_1_enc ┆ type_2_enc │
# │ ---                   ┆ ---     ┆ ---    ┆ ---        ┆ ---        │
# │ str                   ┆ cat     ┆ cat    ┆ u32        ┆ u32        │
# ╞═══════════════════════╪═════════╪════════╪════════════╪════════════╡
# │ Bulbasaur             ┆ Grass   ┆ Poison ┆ 0          ┆ 6          │
# │ Ivysaur               ┆ Grass   ┆ Poison ┆ 0          ┆ 6          │
# │ Venusaur              ┆ Grass   ┆ Poison ┆ 0          ┆ 6          │
# │ VenusaurMega Venusaur ┆ Grass   ┆ Poison ┆ 0          ┆ 6          │
# │ Charmander            ┆ Fire    ┆ null   ┆ 2          ┆ null       │
# │ …                     ┆ …       ┆ …      ┆ …          ┆ …          │
# │ Diancie               ┆ Rock    ┆ Fairy  ┆ 13         ┆ 9          │
# │ DiancieMega Diancie   ┆ Rock    ┆ Fairy  ┆ 13         ┆ 9          │
# │ HoopaHoopa Confined   ┆ Psychic ┆ Ghost  ┆ 11         ┆ 12         │
# │ HoopaHoopa Unbound    ┆ Psychic ┆ Dark   ┆ 11         ┆ 10         │
# │ Volcanion             ┆ Fire    ┆ Water  ┆ 2          ┆ 3          │
# └───────────────────────┴─────────┴────────┴────────────┴────────────┘

# =================================================================================
# 2. One-Hot encoding: `tl.collect().to_dummies(collumns=[...], drop_fist=True)`
# =================================================================================
'''
`to_dummies` is available for eager DataFrame only
'''

print(
    tl_pokemon
    .collect()
    .to_dummies(columns='type_1', drop_first=True)
    .select(tp.nth(range(5))) # show first 5 columns only
)
# shape: (800, 5)
# ┌───────────────────────┬────────────┬─────────────┬───────────────┬─────────────────┐
# │ name                  ┆ type_1_Bug ┆ type_1_Dark ┆ type_1_Dragon ┆ type_1_Electric │
# │ ---                   ┆ ---        ┆ ---         ┆ ---           ┆ ---             │
# │ str                   ┆ u8         ┆ u8          ┆ u8            ┆ u8              │
# ╞═══════════════════════╪════════════╪═════════════╪═══════════════╪═════════════════╡
# │ Bulbasaur             ┆ 0          ┆ 0           ┆ 0             ┆ 0               │
# │ Ivysaur               ┆ 0          ┆ 0           ┆ 0             ┆ 0               │
# │ Venusaur              ┆ 0          ┆ 0           ┆ 0             ┆ 0               │
# │ VenusaurMega Venusaur ┆ 0          ┆ 0           ┆ 0             ┆ 0               │
# │ Charmander            ┆ 0          ┆ 0           ┆ 0             ┆ 0               │
# │ …                     ┆ …          ┆ …           ┆ …             ┆ …               │
# │ Diancie               ┆ 0          ┆ 0           ┆ 0             ┆ 0               │
# │ DiancieMega Diancie   ┆ 0          ┆ 0           ┆ 0             ┆ 0               │
# │ HoopaHoopa Confined   ┆ 0          ┆ 0           ┆ 0             ┆ 0               │
# │ HoopaHoopa Unbound    ┆ 0          ┆ 0           ┆ 0             ┆ 0               │
# │ Volcanion             ┆ 0          ┆ 0           ┆ 0             ┆ 0               │
# └───────────────────────┴────────────┴─────────────┴───────────────┴─────────────────┘
'''Column `type_2` is pushed very far behind to the right'''

print(
    tl_pokemon
    .collect()
    .to_dummies(columns='type_1', drop_first=True)
    .select('name', 'type_2', tp.nth(range(2, 6))) # show 5 columns only
)
# shape: (800, 6)
# ┌───────────────────────┬────────┬─────────────┬───────────────┬─────────────────┬──────────────┐
# │ name                  ┆ type_2 ┆ type_1_Dark ┆ type_1_Dragon ┆ type_1_Electric ┆ type_1_Fairy │
# │ ---                   ┆ ---    ┆ ---         ┆ ---           ┆ ---             ┆ ---          │
# │ str                   ┆ cat    ┆ u8          ┆ u8            ┆ u8              ┆ u8           │
# ╞═══════════════════════╪════════╪═════════════╪═══════════════╪═════════════════╪══════════════╡
# │ Bulbasaur             ┆ Poison ┆ 0           ┆ 0             ┆ 0               ┆ 0            │
# │ Ivysaur               ┆ Poison ┆ 0           ┆ 0             ┆ 0               ┆ 0            │
# │ Venusaur              ┆ Poison ┆ 0           ┆ 0             ┆ 0               ┆ 0            │
# │ VenusaurMega Venusaur ┆ Poison ┆ 0           ┆ 0             ┆ 0               ┆ 0            │
# │ Charmander            ┆ null   ┆ 0           ┆ 0             ┆ 0               ┆ 0            │
# │ …                     ┆ …      ┆ …           ┆ …             ┆ …               ┆ …            │
# │ Diancie               ┆ Fairy  ┆ 0           ┆ 0             ┆ 0               ┆ 0            │
# │ DiancieMega Diancie   ┆ Fairy  ┆ 0           ┆ 0             ┆ 0               ┆ 0            │
# │ HoopaHoopa Confined   ┆ Ghost  ┆ 0           ┆ 0             ┆ 0               ┆ 0            │
# │ HoopaHoopa Unbound    ┆ Dark   ┆ 0           ┆ 0             ┆ 0               ┆ 0            │
# │ Volcanion             ┆ Water  ┆ 0           ┆ 0             ┆ 0               ┆ 0            │
# └───────────────────────┴────────┴─────────────┴───────────────┴─────────────────┴──────────────┘

print(
    tl_pokemon
    .collect()
    .to_dummies(columns=['type_1', 'type_2'], drop_first=True)
    .select(tp.nth(0, 1, 2, 3, -3, -2, -1))
)
# shape: (800, 7)
# ┌───────────────────────┬────────────┬─────────────┬───────────────┬──────────────┬──────────────┬─────────────┐
# │ name                  ┆ type_1_Bug ┆ type_1_Dark ┆ type_1_Dragon ┆ type_2_Steel ┆ type_2_Water ┆ type_2_null │
# │ ---                   ┆ ---        ┆ ---         ┆ ---           ┆ ---          ┆ ---          ┆ ---         │
# │ str                   ┆ u8         ┆ u8          ┆ u8            ┆ u8           ┆ u8           ┆ u8          │
# ╞═══════════════════════╪════════════╪═════════════╪═══════════════╪══════════════╪══════════════╪═════════════╡
# │ Bulbasaur             ┆ 0          ┆ 0           ┆ 0             ┆ 0            ┆ 0            ┆ 0           │
# │ Ivysaur               ┆ 0          ┆ 0           ┆ 0             ┆ 0            ┆ 0            ┆ 0           │
# │ Venusaur              ┆ 0          ┆ 0           ┆ 0             ┆ 0            ┆ 0            ┆ 0           │
# │ VenusaurMega Venusaur ┆ 0          ┆ 0           ┆ 0             ┆ 0            ┆ 0            ┆ 0           │
# │ Charmander            ┆ 0          ┆ 0           ┆ 0             ┆ 0            ┆ 0            ┆ 1           │
# │ …                     ┆ …          ┆ …           ┆ …             ┆ …            ┆ …            ┆ …           │
# │ Diancie               ┆ 0          ┆ 0           ┆ 0             ┆ 0            ┆ 0            ┆ 0           │
# │ DiancieMega Diancie   ┆ 0          ┆ 0           ┆ 0             ┆ 0            ┆ 0            ┆ 0           │
# │ HoopaHoopa Confined   ┆ 0          ┆ 0           ┆ 0             ┆ 0            ┆ 0            ┆ 0           │
# │ HoopaHoopa Unbound    ┆ 0          ┆ 0           ┆ 0             ┆ 0            ┆ 0            ┆ 0           │
# │ Volcanion             ┆ 0          ┆ 0           ┆ 0             ┆ 0            ┆ 1            ┆ 0           │
# └───────────────────────┴────────────┴─────────────┴───────────────┴──────────────┴──────────────┴─────────────┘
