"""
About row names, frames from polars and tidypyrs don't have index system.
Therefore, if we want to create row names, we need to treat them as a column of the frames.

Change Row names:
    + tl.row_index(name='row_id', offset=0)
    + Create row index with `row_index` then modify it
"""

import re
from pathlib import Path

import tidypyrs as tp
from tidypyrs import f

tp.Config(tbl_width_chars=120)
data_dir = next(Path("/home").glob("**/DataScience*/data"))

tl_emp = tp.scan_csv(data_dir/"emp.csv").drop("id")
print(tl_emp.collect())
# shape: (8, 4)
# ┌──────────┬────────┬────────────┬────────────┐
# │ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ str      ┆ f64    ┆ str        ┆ str        │
# ╞══════════╪════════╪════════════╪════════════╡
# │ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# │ Ryan     ┆ 729.0  ┆ 2014-05-11 ┆ HR         │
# │ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# │ Nina     ┆ 578.0  ┆ 2013-05-21 ┆ IT         │
# │ Simon    ┆ 632.8  ┆ 2013-07-30 ┆ Operations │
# │ Guru     ┆ 722.5  ┆ 2014-06-17 ┆ Finance    │
# └──────────┴────────┴────────────┴────────────┘

##---------------------------------------##
## tl.row_index(name='row_id', offset=0) ##
##---------------------------------------##

print(
    tl_emp
    .row_index()
    .collect()
)
# shape: (8, 5)
# ┌───────┬──────────┬────────┬────────────┬────────────┐
# │ index ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---   ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ u32   ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞═══════╪══════════╪════════╪════════════╪════════════╡
# │ 0     ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 1     ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ 2     ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# │ 3     ┆ Ryan     ┆ 729.0  ┆ 2014-05-11 ┆ HR         │
# │ 4     ┆ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# │ 5     ┆ Nina     ┆ 578.0  ┆ 2013-05-21 ┆ IT         │
# │ 6     ┆ Simon    ┆ 632.8  ┆ 2013-07-30 ┆ Operations │
# │ 7     ┆ Guru     ┆ 722.5  ┆ 2014-06-17 ┆ Finance    │
# └───────┴──────────┴────────┴────────────┴────────────┘

print(
    tl_emp
    .row_index(name="id", offset=1)
    .collect()
)
# shape: (8, 5)
# ┌─────┬──────────┬────────┬────────────┬────────────┐
# │ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ u32 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞═════╪══════════╪════════╪════════════╪════════════╡
# │ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# │ 4   ┆ Ryan     ┆ 729.0  ┆ 2014-05-11 ┆ HR         │
# │ 5   ┆ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# │ 6   ┆ Nina     ┆ 578.0  ┆ 2013-05-21 ┆ IT         │
# │ 7   ┆ Simon    ┆ 632.8  ┆ 2013-07-30 ┆ Operations │
# │ 8   ┆ Guru     ┆ 722.5  ┆ 2014-06-17 ┆ Finance    │
# └─────┴──────────┴────────┴────────────┴────────────┘

##--------------------------------------------------##
## Create row index with `row_index` then modify it ##
##--------------------------------------------------##

tl_pokemon = tp.scan_csv(data_dir/"pokemon.csv")

print(
    tl_pokemon
    .row_index(name="id", offset=1)
    .mutate(
        id = (tp.lit("pkm") + f("id").cast(tp.String).str.zfill(f("id").max().log10().ceil().cast(tp.Int64)))
        # (tp.lit("pkm") + f("id").cast(tp.String).str.zfill(f("id").max().log10().ceil().cast(tp.Int64))).alias("id),
    )
    .collect()
)
# shape: (800, 14)
# ┌────────┬─────┬───────────────────────┬─────────┬───┬─────────┬───────┬────────────┬───────────┐
# │ id     ┆ #   ┆ Name                  ┆ Type 1  ┆ … ┆ Sp. Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---    ┆ --- ┆ ---                   ┆ ---     ┆   ┆ ---     ┆ ---   ┆ ---        ┆ ---       │
# │ str    ┆ i64 ┆ str                   ┆ str     ┆   ┆ i64     ┆ i64   ┆ i64        ┆ bool      │
# ╞════════╪═════╪═══════════════════════╪═════════╪═══╪═════════╪═══════╪════════════╪═══════════╡
# │ pkm001 ┆ 1   ┆ Bulbasaur             ┆ Grass   ┆ … ┆ 65      ┆ 45    ┆ 1          ┆ false     │
# │ pkm002 ┆ 2   ┆ Ivysaur               ┆ Grass   ┆ … ┆ 80      ┆ 60    ┆ 1          ┆ false     │
# │ pkm003 ┆ 3   ┆ Venusaur              ┆ Grass   ┆ … ┆ 100     ┆ 80    ┆ 1          ┆ false     │
# │ pkm004 ┆ 3   ┆ VenusaurMega Venusaur ┆ Grass   ┆ … ┆ 120     ┆ 80    ┆ 1          ┆ false     │
# │ pkm005 ┆ 4   ┆ Charmander            ┆ Fire    ┆ … ┆ 50      ┆ 65    ┆ 1          ┆ false     │
# │ …      ┆ …   ┆ …                     ┆ …       ┆ … ┆ …       ┆ …     ┆ …          ┆ …         │
# │ pkm796 ┆ 719 ┆ Diancie               ┆ Rock    ┆ … ┆ 150     ┆ 50    ┆ 6          ┆ true      │
# │ pkm797 ┆ 719 ┆ DiancieMega Diancie   ┆ Rock    ┆ … ┆ 110     ┆ 110   ┆ 6          ┆ true      │
# │ pkm798 ┆ 720 ┆ HoopaHoopa Confined   ┆ Psychic ┆ … ┆ 130     ┆ 70    ┆ 6          ┆ true      │
# │ pkm799 ┆ 720 ┆ HoopaHoopa Unbound    ┆ Psychic ┆ … ┆ 130     ┆ 80    ┆ 6          ┆ true      │
# │ pkm800 ┆ 721 ┆ Volcanion             ┆ Fire    ┆ … ┆ 90      ┆ 70    ┆ 6          ┆ true      │
# └────────┴─────┴───────────────────────┴─────────┴───┴─────────┴───────┴────────────┴───────────┘
