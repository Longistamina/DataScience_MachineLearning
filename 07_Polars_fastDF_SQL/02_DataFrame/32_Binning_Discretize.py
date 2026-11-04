'''
There are 3 main ways to discretize/bin numeric data
into categorical data in Polars:
    1. `bin_ranks()`: Bin values by their position in sorted order.
        pl.col("x").bin_ranks(ranks=..., labels=..., include_intervals=False)

    2. `bin_quantiles()`: Bin values into discrete intervals delimited by quantiles of the data.
        pl.col("x").bin_quantiles(quantiles=..., labels=..., include_intervals=False, right_closed=False)

    3. `bin_intervals()`: Bin values into discrete intervals delimited by breakpoints.
        pl.col("x").bin_intervals(intervals=..., labels=..., include_intervals=False, right_closed=False)
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
    pl.scan_csv(data_dir/'pokemon.csv')
    .rename(lambda name: name.strip())
    .select(pl.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
    .select('name', 'total')
)

print(lf_pokemon.collect())
# shape: (800, 2)
# ┌───────────────────────┬───────┐
# │ name                  ┆ total │
# │ ---                   ┆ ---   │
# │ str                   ┆ i64   │
# ╞═══════════════════════╪═══════╡
# │ Bulbasaur             ┆ 318   │
# │ Ivysaur               ┆ 405   │
# │ Venusaur              ┆ 525   │
# │ VenusaurMega Venusaur ┆ 625   │
# │ Charmander            ┆ 309   │
# │ …                     ┆ …     │
# │ Diancie               ┆ 600   │
# │ DiancieMega Diancie   ┆ 700   │
# │ HoopaHoopa Confined   ┆ 600   │
# │ HoopaHoopa Unbound    ┆ 680   │
# │ Volcanion             ┆ 600   │
# └───────────────────────┴───────┘

# =========================================================================================
# 1. `bin_ranks()`: Bin values by their position in sorted order.
# =========================================================================================
'''
Parameters
----------
ranks
    Non-decreasing cumulative fractions in `[0, 1]`, or a positive integer
    giving the number of near-equal-sized bins. Two equal fractions delimit an
    empty bin. For an integer, earlier bins receive any remainder.
labels
    One label per bin, or `False` to return the integer bin index.
include_intervals
    Return a struct with fields `bin`, `left`, and `right`. Boundaries are input
    values, not ranks; the first bin's left and last bin's right boundary are
    null.
'''

print(
    lf_pokemon
    .with_columns(
        c("total").bin_ranks(ranks=[0.25, 0.75], labels=["low", "medium", "high"]).alias("bin_ranks")
    )
    .collect()
)
# shape: (800, 3)
# ┌───────────────────────┬───────┬───────────┐
# │ name                  ┆ total ┆ bin_ranks │
# │ ---                   ┆ ---   ┆ ---       │
# │ str                   ┆ i64   ┆ enum      │
# ╞═══════════════════════╪═══════╪═══════════╡
# │ Bulbasaur             ┆ 318   ┆ low       │
# │ Ivysaur               ┆ 405   ┆ medium    │
# │ Venusaur              ┆ 525   ┆ high      │
# │ VenusaurMega Venusaur ┆ 625   ┆ high      │
# │ Charmander            ┆ 309   ┆ low       │
# │ …                     ┆ …     ┆ …         │
# │ Diancie               ┆ 600   ┆ high      │
# │ DiancieMega Diancie   ┆ 700   ┆ high      │
# │ HoopaHoopa Confined   ┆ 600   ┆ high      │
# │ HoopaHoopa Unbound    ┆ 680   ┆ high      │
# │ Volcanion             ┆ 600   ┆ high      │
# └───────────────────────┴───────┴───────────┘

# ==============================================================================================
# 2. `bin_quantiles()`: Bin values into discrete intervals delimited by quantiles of the data
# ==============================================================================================
'''
Parameters
----------
quantiles
    Non-decreasing quantiles in `[0, 1]`, or a positive integer giving the
    number of bins. Two equal quantiles delimit an empty bin. Input must be
    numeric. For quantile `q`, the value of the breakpoint is the sorted value
    at `floor(q * (len - 1))`.
labels
    One label per bin, or `False` to return the integer bin index.
include_intervals
    Return a struct with fields `bin`, `left`, and `right`. The first bin's left
    and last bin's right boundary are null.
right_closed
    Use right-closed `(left, right]` rather than left-closed `[left, right)` bins.
'''

print(
    lf_pokemon
    .with_columns(
        c("total").bin_quantiles([0.25, 0.5, 0.75], labels=["q1", "q2", "q3", "q4"]).alias("bin_quantiles")
    )
    .collect()
)
# shape: (800, 3)
# ┌───────────────────────┬───────┬───────────────┐
# │ name                  ┆ total ┆ bin_quantiles │
# │ ---                   ┆ ---   ┆ ---           │
# │ str                   ┆ i64   ┆ enum          │
# ╞═══════════════════════╪═══════╪═══════════════╡
# │ Bulbasaur             ┆ 318   ┆ q1            │
# │ Ivysaur               ┆ 405   ┆ q2            │
# │ Venusaur              ┆ 525   ┆ q4            │
# │ VenusaurMega Venusaur ┆ 625   ┆ q4            │
# │ Charmander            ┆ 309   ┆ q1            │
# │ …                     ┆ …     ┆ …             │
# │ Diancie               ┆ 600   ┆ q4            │
# │ DiancieMega Diancie   ┆ 700   ┆ q4            │
# │ HoopaHoopa Confined   ┆ 600   ┆ q4            │
# │ HoopaHoopa Unbound    ┆ 680   ┆ q4            │
# │ Volcanion             ┆ 600   ┆ q4            │
# └───────────────────────┴───────┴───────────────┘

# ==============================================================================================
# 3. `bin_intervals()`: Bin values into discrete intervals delimited by breakpoints.
# ==============================================================================================
'''
Parameters
----------
intervals
    Strictly ascending breakpoints, or a positive integer giving the number of
    equal-width bins over `[min, max]`. Explicit breakpoints may have any
    orderable (non-nested) data type; an integer requires numeric input.
labels
    One label per bin, or `False` to return the integer bin index.
include_intervals
    Return a struct with fields `bin`, `left`, and `right`. The first bin's left
    and last bin's right boundary are null.
right_closed
    Use right-closed `(left, right]` rather than left-closed `[left, right)` bins.
'''

print(
    lf_pokemon
    .with_columns(
        c("total").bin_intervals([350, 700], labels=["l1", "l2", "l3"]).alias("bin_intervals")
    )
    .collect()
)
# shape: (800, 3)
# ┌───────────────────────┬───────┬───────────────┐
# │ name                  ┆ total ┆ bin_intervals │
# │ ---                   ┆ ---   ┆ ---           │
# │ str                   ┆ i64   ┆ enum          │
# ╞═══════════════════════╪═══════╪═══════════════╡
# │ Bulbasaur             ┆ 318   ┆ l1            │
# │ Ivysaur               ┆ 405   ┆ l2            │
# │ Venusaur              ┆ 525   ┆ l2            │
# │ VenusaurMega Venusaur ┆ 625   ┆ l2            │
# │ Charmander            ┆ 309   ┆ l1            │
# │ …                     ┆ …     ┆ …             │
# │ Diancie               ┆ 600   ┆ l2            │
# │ DiancieMega Diancie   ┆ 700   ┆ l3            │
# │ HoopaHoopa Confined   ┆ 600   ┆ l2            │
# │ HoopaHoopa Unbound    ┆ 680   ┆ l2            │
# │ Volcanion             ┆ 600   ┆ l2            │
# └───────────────────────┴───────┴───────────────┘
