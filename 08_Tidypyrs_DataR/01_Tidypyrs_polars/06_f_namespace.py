'''
tidypyrs provides a very convenient `f` namespace to allow fast selecting and accessing columns.
This pushes `polars.col()` one step further from a mere column expression.

1. `f.x` -> `pl.col("x")`
2. `f("x")` and `f("x", "y", "z")`
3. `f["x"]` and `f["x", "y", "z"]`
4. `f.select("x")` designed for `tp.as_enum()` and `tp.as_ordered()`
5. `f.pull("x")` designed for `tp.as_enum()` and `tp.as_ordered()`
6. `f` namespace with `numpy` functions
'''

from pathlib import Path

import numpy as np
import polars as pl
import tidypyrs as tp  # noqa: I001
from tidypyrs import f

pl.Config(tbl_width_chars=120, tbl_rows=5)
data_dir = next(Path("/home").glob("**/DataScience*/data"))

tl_pokemon = (
    tp.scan_csv(data_dir/"pokemon.csv")
    .select(f.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .mutate(
        f("type_1", "type_2").pipe(tp.as_categorical)
    )
)

print(tl_pokemon.collect())
# shape: (800, 13)
# ┌─────┬────────────────────┬─────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name               ┆ type_1  ┆ type_2 ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---                ┆ ---     ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                ┆ cat     ┆ cat    ┆   ┆ i64    ┆ i64   ┆ i64        ┆ bool      │
# ╞═════╪════════════════════╪═════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 1   ┆ Bulbasaur          ┆ Grass   ┆ Poison ┆ … ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 2   ┆ Ivysaur            ┆ Grass   ┆ Poison ┆ … ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 3   ┆ Venusaur           ┆ Grass   ┆ Poison ┆ … ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ …   ┆ …                  ┆ …       ┆ …      ┆ … ┆ …      ┆ …     ┆ …          ┆ …         │
# │ 720 ┆ HoopaHoopa Unbound ┆ Psychic ┆ Dark   ┆ … ┆ 130    ┆ 80    ┆ 6          ┆ true      │
# │ 721 ┆ Volcanion          ┆ Fire    ┆ Water  ┆ … ┆ 90     ┆ 70    ┆ 6          ┆ true      │
# └─────┴────────────────────┴─────────┴────────┴───┴────────┴───────┴────────────┴───────────┘

print(tl_pokemon.collect_schema())
# Schema({'#': Int64, 'name': String, 'type_1': Categorical, 'type_2': Categorical, 'total': Int64, 'hp': Int64, 'attack': Int64,
# 'defense': Int64, 'sp_atk': Int64, 'sp_def': Int64, 'speed': Int64, 'generation': Enum(categories=['1', '2', '3', '4', '5', '6']
# ), 'legendary': Boolean})

# =========================================================================================
# 1. `f.x` -> `pl.col("x")`
# =========================================================================================

print(
    tl_pokemon.select(f.total)
    .collect()
)
# shape: (800, 1)
# ┌───────┐
# │ total │
# │ ---   │
# │ i64   │
# ╞═══════╡
# │ 318   │
# │ 405   │
# │ 525   │
# │ …     │
# │ 680   │
# │ 600   │
# └───────┘

print(
    tl_pokemon.select(f.name)
    .collect()
)
# shape: (800, 1)
# ┌────────────────────┐
# │ name               │
# │ ---                │
# │ str                │
# ╞════════════════════╡
# │ Bulbasaur          │
# │ Ivysaur            │
# │ Venusaur           │
# │ …                  │
# │ HoopaHoopa Unbound │
# │ Volcanion          │
# └────────────────────┘

# =========================================================================================
# 2. `f("x")` and `f("x", "y", "z")`
# =========================================================================================

print(
    tl_pokemon
    .select(f("generation"))
    .collect()
)
# shape: (800, 1)
# ┌────────────┐
# │ generation │
# │ ---        │
# │ enum       │
# ╞════════════╡
# │ 1          │
# │ 1          │
# │ 1          │
# │ …          │
# │ 6          │
# │ 6          │
# └────────────┘

print(
    tl_pokemon
    .select(f("name", "hp", "speed"))
    .mutate(
        f("hp", "speed").mul(2).name.suffix("_doubble")
    )
    .collect()
)
# shape: (800, 5)
# ┌────────────────────┬─────┬───────┬────────────┬───────────────┐
# │ name               ┆ hp  ┆ speed ┆ hp_doubble ┆ speed_doubble │
# │ ---                ┆ --- ┆ ---   ┆ ---        ┆ ---           │
# │ str                ┆ i64 ┆ i64   ┆ i64        ┆ i64           │
# ╞════════════════════╪═════╪═══════╪════════════╪═══════════════╡
# │ Bulbasaur          ┆ 45  ┆ 45    ┆ 90         ┆ 90            │
# │ Ivysaur            ┆ 60  ┆ 60    ┆ 120        ┆ 120           │
# │ Venusaur           ┆ 80  ┆ 80    ┆ 160        ┆ 160           │
# │ …                  ┆ …   ┆ …     ┆ …          ┆ …             │
# │ HoopaHoopa Unbound ┆ 80  ┆ 80    ┆ 160        ┆ 160           │
# │ Volcanion          ┆ 80  ┆ 70    ┆ 160        ┆ 140           │
# └────────────────────┴─────┴───────┴────────────┴───────────────┘

# =========================================================================================
# 3. `f["x"]` and `f["x", "y", "z"]`
# =========================================================================================

print(
    tl_pokemon
    .select(f["legendary"])
    .collect()
)
# shape: (800, 1)
# ┌───────────┐
# │ legendary │
# │ ---       │
# │ bool      │
# ╞═══════════╡
# │ false     │
# │ false     │
# │ false     │
# │ …         │
# │ true      │
# │ true      │
# └───────────┘

print(
    tl_pokemon
    .select(f["name", "attack", "defense"])
    .mutate(
        f("attack", "defense").truediv(2).name.suffix("_half")
    )
    .collect()
)
# shape: (800, 5)
# ┌────────────────────┬────────┬─────────┬─────────────┬──────────────┐
# │ name               ┆ attack ┆ defense ┆ attack_half ┆ defense_half │
# │ ---                ┆ ---    ┆ ---     ┆ ---         ┆ ---          │
# │ str                ┆ i64    ┆ i64     ┆ f64         ┆ f64          │
# ╞════════════════════╪════════╪═════════╪═════════════╪══════════════╡
# │ Bulbasaur          ┆ 49     ┆ 49      ┆ 24.5        ┆ 24.5         │
# │ Ivysaur            ┆ 62     ┆ 63      ┆ 31.0        ┆ 31.5         │
# │ Venusaur           ┆ 82     ┆ 83      ┆ 41.0        ┆ 41.5         │
# │ …                  ┆ …      ┆ …       ┆ …           ┆ …         │
# │ HoopaHoopa Unbound ┆ 160    ┆ 60      ┆ 80.0        ┆ 30.0         │
# │ Volcanion          ┆ 110    ┆ 120     ┆ 55.0        ┆ 60.0         │
# └────────────────────┴────────┴─────────┴─────────────┴──────────────┘

# ============================================================================
# 4. `f.select("x")` designed for `tp.as_enum()` and `tp.as_ordered()`
# ============================================================================
'''
For now, the only situation where you need to use `f.select()`
is when you are trying converting into Enum with `tp.as_enum`
                                         or with `tp.as_ordered`

It should be use with `.mutate()` like below
'''

# with `tp.as_enum`
print(
    tl_pokemon
    .mutate(
        generation_enum = tp.as_enum(f.select("generation"))
    )
    .select(f("name", "generation", "generation_enum"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬─────────────────┐
# │ name               ┆ generation ┆ generation_enum │
# │ ---                ┆ ---        ┆ ---             │
# │ str                ┆ i64        ┆ enum            │
# ╞════════════════════╪════════════╪═════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1               │
# │ Ivysaur            ┆ 1          ┆ 1               │
# │ Venusaur           ┆ 1          ┆ 1               │
# │ …                  ┆ …          ┆ …               │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6               │
# │ Volcanion          ┆ 6          ┆ 6               │
# └────────────────────┴────────────┴─────────────────┘

# with `tp.as_ordered`
print(
    tl_pokemon
    .mutate(
        generation_ordered = tp.as_ordered(f.select("generation"), reverse=True)
    )
    .select(f("name", "generation", "generation_ordered"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬────────────────────┐
# │ name               ┆ generation ┆ generation_ordered │
# │ ---                ┆ ---        ┆ ---                │
# │ str                ┆ i64        ┆ enum               │
# ╞════════════════════╪════════════╪════════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1                  │
# │ Ivysaur            ┆ 1          ┆ 1                  │
# │ Venusaur           ┆ 1          ┆ 1                  │
# │ …                  ┆ …          ┆ …                  │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6                  │
# │ Volcanion          ┆ 6          ┆ 6                  │
# └────────────────────┴────────────┴────────────────────┘

# =========================================================================================
# 5. `f.pull("x")` designed for `tp.as_enum()` and `tp.as_ordered()`
# =========================================================================================
'''
For now, the only situation where you need to use `f.pull()`
is when you are trying converting into Enum with `tp.as_enum`
                                         or with `tp.as_ordered`

It could be used with `.pipe()` or `.mutate()`
like below to provide `categories`
'''

##------------------------------------------##
## f("col").pipe(tp.as_enum, f.pull("col")) ##
##------------------------------------------##

# with `tp.as_enum`
print(
    tl_pokemon
    .mutate(
        f("generation").pipe(tp.as_enum, f.pull("generation")).alias("generation_enum")
    )
    .select(f("name", "generation", "generation_enum"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬─────────────────┐
# │ name               ┆ generation ┆ generation_enum │
# │ ---                ┆ ---        ┆ ---             │
# │ str                ┆ i64        ┆ enum            │
# ╞════════════════════╪════════════╪═════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1               │
# │ Ivysaur            ┆ 1          ┆ 1               │
# │ Venusaur           ┆ 1          ┆ 1               │
# │ …                  ┆ …          ┆ …               │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6               │
# │ Volcanion          ┆ 6          ┆ 6               │
# └────────────────────┴────────────┴─────────────────┘

# with `tp.as_ordered`
print(
    tl_pokemon
    .mutate(
        f("generation").pipe(tp.as_ordered, f.pull("generation"), reverse=True).alias("generation_ordered")
    )
    .select(f("name", "generation", "generation_ordered"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬────────────────────┐
# │ name               ┆ generation ┆ generation_ordered │
# │ ---                ┆ ---        ┆ ---                │
# │ str                ┆ i64        ┆ enum               │
# ╞════════════════════╪════════════╪════════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1                  │
# │ Ivysaur            ┆ 1          ┆ 1                  │
# │ Venusaur           ┆ 1          ┆ 1                  │
# │ …                  ┆ …          ┆ …                  │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6                  │
# │ Volcanion          ┆ 6          ┆ 6                  │
# └────────────────────┴────────────┴────────────────────┘

##---------------------------------------------------##
## mutate(new_col = tp.as_enum("col", f.pull("col")) ##
##---------------------------------------------------##

# with `tp.as_enum`
print(
    tl_pokemon
    .mutate(
        generation_enum = tp.as_enum("generation", f.pull("generation"))
    )
    .select(f("name", "generation", "generation_enum"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬─────────────────┐
# │ name               ┆ generation ┆ generation_enum │
# │ ---                ┆ ---        ┆ ---             │
# │ str                ┆ i64        ┆ enum            │
# ╞════════════════════╪════════════╪═════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1               │
# │ Ivysaur            ┆ 1          ┆ 1               │
# │ Venusaur           ┆ 1          ┆ 1               │
# │ …                  ┆ …          ┆ …               │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6               │
# │ Volcanion          ┆ 6          ┆ 6               │
# └────────────────────┴────────────┴─────────────────┘

# with `tp.as_ordered`
print(
    tl_pokemon
    .mutate(
        generation_ordered = tp.as_ordered("generation", f.pull("generation"), reverse=True)
    )
    .select(f("name", "generation", "generation_ordered"))
    .collect()
)
# shape: (800, 3)
# ┌────────────────────┬────────────┬────────────────────┐
# │ name               ┆ generation ┆ generation_ordered │
# │ ---                ┆ ---        ┆ ---                │
# │ str                ┆ i64        ┆ enum               │
# ╞════════════════════╪════════════╪════════════════════╡
# │ Bulbasaur          ┆ 1          ┆ 1                  │
# │ Ivysaur            ┆ 1          ┆ 1                  │
# │ Venusaur           ┆ 1          ┆ 1                  │
# │ …                 ┆ …          ┆ …                 │
# │ HoopaHoopa Unbound ┆ 6          ┆ 6                  │
# │ Volcanion          ┆ 6          ┆ 6                  │
# └────────────────────┴────────────┴────────────────────┘

# =========================================================================================
# 6. `f` namespace with `numpy` functions
# =========================================================================================

print(
    tl_pokemon
    .select(f("name", "speed"))
    .mutate(
        speed_log = np.log(f("speed")),
        speed_log10 = np.log10(f("speed")),
    )
    .collect()
)
# shape: (800, 4)
# ┌────────────────────┬───────┬───────────┬─────────────┐
# │ name               ┆ speed ┆ speed_log ┆ speed_log10 │
# │ ---                ┆ ---   ┆ ---       ┆ ---         │
# │ str                ┆ i64   ┆ f64       ┆ f64         │
# ╞════════════════════╪═══════╪═══════════╪═════════════╡
# │ Bulbasaur          ┆ 45    ┆ 3.806662  ┆ 1.653213    │
# │ Ivysaur            ┆ 60    ┆ 4.094345  ┆ 1.778151    │
# │ Venusaur           ┆ 80    ┆ 4.382027  ┆ 1.90309     │
# │ …                  ┆ …     ┆ …         ┆ …           │
# │ HoopaHoopa Unbound ┆ 80    ┆ 4.382027  ┆ 1.90309     │
# │ Volcanion          ┆ 70    ┆ 4.248495  ┆ 1.845098    │
# └────────────────────┴───────┴───────────┴─────────────┘

print(
    tl_pokemon
    .select(f("name", "total"))
    .mutate(
        f("total").pipe(np.sin).alias("total_sin"),
        f("total").pipe(np.cos).alias("total_cos"),
    )
    .collect()
)
# shape: (800, 4)
# ┌────────────────────┬───────┬───────────┬───────────┐
# │ name               ┆ total ┆ total_sin ┆ total_cos │
# │ ---                ┆ ---   ┆ ---       ┆ ---       │
# │ str                ┆ i64   ┆ f64       ┆ f64       │
# ╞════════════════════╪═══════╪═══════════╪═══════════╡
# │ Bulbasaur          ┆ 318   ┆ -0.643561 ┆ -0.765395 │
# │ Ivysaur            ┆ 405   ┆ 0.262346  ┆ -0.964974 │
# │ Venusaur           ┆ 525   ┆ -0.346678 ┆ -0.937984 │
# │ …                  ┆ …     ┆ …         ┆ …         │
# │ HoopaHoopa Unbound ┆ 680   ┆ 0.988041  ┆ 0.154192  │
# │ Volcanion          ┆ 600   ┆ 0.044182  ┆ -0.999023 │
# └────────────────────┴───────┴───────────┴───────────┘

print(
    tl_pokemon
    .select(
        f("total").pipe(np.mean).alias("total_mean"),
        f("hp").pipe(np.max).alias("hp_max")
    )
    .collect()
)
'''Raise Error!!!'''
