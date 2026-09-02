'''
Polars GPU execution is used through the Lazy API.

Main idea:
    Build a LazyFrame query as usual, then execute it with:

        q.collect(engine="gpu")

This keeps the normal Polars expression/query style. Only the execution engine changes.

##------------------------------------##

0. Installation
1. Example: Lazy query executed on GPU
'''

from pathlib import Path

import polars as pl
from polars import col as c

# =========================================================================================
# 0. Installation
# =========================================================================================
'''
Install Polars with GPU support in an environment that has a supported NVIDIA GPU:

    pip install "polars[gpu]"

Then use the LazyFrame API normally, and execute the query with:

    q.collect(engine="gpu")
'''

print(pl.__version__)


# =========================================================================================
# 1. Example: Lazy query executed on GPU
# =========================================================================================
'''
The GPU engine is selected at collection time.
The query construction remains normal Polars lazy code.
'''

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

q = (
    pl.scan_csv(data_dir / "pokemon.csv")
    .drop("#")
    .rename(lambda name: name.strip())
    .select(pl.all().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .with_columns(
        c("Type_1", "Type_2").cast(pl.Categorical),
        c("Legendary").cast(pl.Boolean),
    )
    .pipe(lambda f: f.with_columns(
        c("Generation").cast(pl.String).cast(pl.Enum(f.select("Generation").collect().to_series().cast(pl.String).unique().sort())),
    ))                                               # Must use .collect() to realize the dataframe, to access the values for Enum casting
)

# The only GPU-specific line in the workflow.
# If your environment does not have Polars GPU support installed, use `.collect()` instead.
result = q.collect(engine="gpu")

print(result) # result of q.head().collect()
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ Name           ┆ Type_1 ┆ Type_2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp_Atk ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
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
