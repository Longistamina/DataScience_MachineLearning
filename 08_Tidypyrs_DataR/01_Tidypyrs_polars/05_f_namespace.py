'''
tidypyrs provides a very convenient `f` namespace to allow fast selecting and accessing columns.
This pushes `polars.col()` one step further from a mere column expression.

1. `f.x` -> `pl.col("x")`
1. `f("x")` and `f("x", "y", "z")`
2. `f["x"]` and `f["x", "y", "z"]`
3. `f.select("x")` designed for `tp.as_enum()` and `tp.as_ordered()`
4. `f.pull("x")` designed for `tp.as_enum()` and `tp.as_ordered()`
'''

import tidypyrs as tp  # noqa: I001
import polars as pl
from tidypyrs import f
from pathlib import Path

pl.Config(tbl_width_chars=120, tbl_rows=5)
data_dir = next(Path("/home").glob("**/DataScience*/data"))

tl_pokemon = (
    tp.scan_csv(data_dir/"pokemon.csv")
    .select(f.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .mutate(f.generation.pipe(tp.as_enum, f.pull("generation")))
)

print(tl_pokemon.collect())
# shape: (800, 13)
# ┌─────┬────────────────────┬─────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ name               ┆ type_1  ┆ type_2 ┆ … ┆ sp_def ┆ speed ┆ generation ┆ legendary │
# │ --- ┆ ---                ┆ ---     ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                ┆ cat     ┆ str    ┆   ┆ i64    ┆ i64   ┆ enum       ┆ bool      │
# ╞═════╪════════════════════╪═════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 1   ┆ Bulbasaur          ┆ Grass   ┆ Poison ┆ … ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 2   ┆ Ivysaur            ┆ Grass   ┆ Poison ┆ … ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 3   ┆ Venusaur           ┆ Grass   ┆ Poison ┆ … ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ …  ┆ …                  ┆ …      ┆ …     ┆ … ┆ …     ┆ …    ┆ …         ┆ …         │
# │ 720 ┆ HoopaHoopa Unbound ┆ Psychic ┆ Dark   ┆ … ┆ 130    ┆ 80    ┆ 6          ┆ true      │
# │ 721 ┆ Volcanion          ┆ Fire    ┆ Water  ┆ … ┆ 90     ┆ 70    ┆ 6          ┆ true      │
# └─────┴────────────────────┴─────────┴────────┴───┴────────┴───────┴────────────┴───────────┘


# ===========================================================
# 1. `f.x` -> `pl.col("x")`
# ===========================================================

print(
    tl_pokemon.select(f.total).collect()
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
# │ 625   │
# │ 309   │
# │ …     │
# │ 600   │
# │ 700   │
# │ 600   │
# │ 680   │
# │ 600   │
# └───────┘

print(
    tl_pokemon.select(f.name).collect()
)
