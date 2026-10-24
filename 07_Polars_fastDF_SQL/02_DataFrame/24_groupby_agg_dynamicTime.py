'''
1. group_by().agg(): Aggregate data using specified expressions.
   + Count the group size with pl.len().
   + Aggregate one or more columns with min(), max(), mean(), etc.
   + Use maintain_order=True to preserve the first-seen order of group keys.
   + Use .sort(...) after aggregation when sorted group keys are desired.
   + Use .drop_nulls(...) before or after grouping when null group keys/results should be removed.

2. Time-based grouping with group_by_dynamic():
   + Polars uses group_by_dynamic(index_column=..., every=...) for time-window grouping.
   + This is the Polars way to group records into regular datetime windows.
   + Extra grouping keys can be included with group_by=... .
'''

from pathlib import Path

import polars as pl
from polars import col as c
from polars import selectors as cs

# Optional display settings
pl.Config.set_tbl_rows(20)
pl.Config.set_tbl_cols(20)
pl.Config.set_tbl_width_chars(120)

data_dir = next(Path('/home').rglob('*/DataScience_MachineLearning/data'))

# =========================================================================================
# 0. Setup Data
# =========================================================================================

##---------##
## Pokemon ##
##---------##

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
    .with_columns(cs.string().exclude("name").cast(pl.Categorical))
    .pipe(lambda lf: lf.with_columns(
        c.generation.cast(pl.String).cast(pl.Enum(lf.select("generation").collect().to_series().cast(pl.String).unique().sort())))
    )
)

print(lf_pokemon.head().collect())
# shape: (5, 12)
# ┌────────────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
# │ name           ┆ type_1 ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
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

print(lf_pokemon.collect_schema())

##-------------##
## Air quality ##
##-------------##

lf_aq = (
    pl.scan_csv(data_dir / 'air_quality_no2_long.csv')
    .rename({'date.utc': 'date'})
    .with_columns(
        c('date').str.strptime(pl.Datetime, format='%Y-%m-%d %H:%M:%S%z')
    )
)

print(lf_aq.head().collect())
# shape: (5, 7)
# ┌───────┬─────────┬─────────────────────────┬──────────┬───────────┬───────┬───────┐
# │ city  ┆ country ┆ date                    ┆ location ┆ parameter ┆ value ┆ unit  │
# │ ---   ┆ ---     ┆ ---                     ┆ ---      ┆ ---       ┆ ---   ┆ ---   │
# │ str   ┆ str     ┆ datetime[μs, UTC]       ┆ str      ┆ str       ┆ f64   ┆ str   │
# ╞═══════╪═════════╪═════════════════════════╪══════════╪═══════════╪═══════╪═══════╡
# │ Paris ┆ FR      ┆ 2019-06-21 00:00:00 UTC ┆ FR04014  ┆ no2       ┆ 20.0  ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 23:00:00 UTC ┆ FR04014  ┆ no2       ┆ 21.8  ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 22:00:00 UTC ┆ FR04014  ┆ no2       ┆ 26.5  ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 21:00:00 UTC ┆ FR04014  ┆ no2       ┆ 24.9  ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 20:00:00 UTC ┆ FR04014  ┆ no2       ┆ 21.4  ┆ µg/m³ │
# └───────┴─────────┴─────────────────────────┴──────────┴───────────┴───────┴───────┘

print(lf_aq.collect_schema())

# =========================================================================================
# 1. group_by().agg()
# =========================================================================================
'''
Polars:
Use `.group_by(...).agg(...)` with expression syntax.
Unlike pandas, group keys stay as ordinary columns in the output, so there is no
`.reset_index()` step.
'''

##----------------------##
## Count the group size ##
##----------------------##

print(
    lf_pokemon
    .group_by('type_1')
    .agg(
        pl.len().alias('count'),             # Number of rows in each group
        c('hp').mean().alias('avg_hp'),      # mean hp in each group
    )
    .sort('type_1')
    .collect()
)

##----------------------------------------##
## Preserve first-seen order of group key ##
##----------------------------------------##
'''
Polars does not use `sort=True/False` on group_by in the same way.

- Use `maintain_order=True` to keep the first-seen order of group keys.
- Use `.sort(...)` after aggregation when sorted output is desired.
'''

print(
    lf_pokemon
    .group_by('type_1', maintain_order=True)
    .agg(
        c('hp').min().alias('min_hp'),
        c('hp').max().alias('max_hp'),
        c('hp').mean().alias('mean_hp'),
    )
    .collect()
)

##---------------------------------------##
## Multiple grouping keys, sorted output ##
##---------------------------------------##

print(
    lf_pokemon
    .group_by(['type_1', 'type_2'])
    .agg(
        c('hp').min().alias('min_hp'),
        c('hp').max().alias('max_hp'),
        c('hp').mean().alias('mean_hp'),
    )
    .sort(['type_1', 'type_2'])
    .collect()
)

##-----------------------------------------##
## Drop null group keys before aggregation ##
##-----------------------------------------##
'''
For a multi-key group, rows with null values in the grouping keys can be removed
before the aggregation using `.drop_nulls([...])`.

This is usually the clearest equivalent when you do not want null-key groups.
'''

print(
    lf_pokemon
    .drop_nulls(['type_1', 'type_2'])
    .group_by(['type_1', 'type_2'])
    .agg(
        c('hp').min().alias('min_hp'),
        c('hp').max().alias('max_hp'),
        c('hp').mean().alias('mean_hp'),
    )
    .sort(['type_1', 'type_2'])
    .collect()
)

##------------------------------------------------------------------##
## Include all observed/unobserved category combinations if needed  ##
##------------------------------------------------------------------##
'''
Important difference:
Polars does not automatically expand unobserved categorical combinations during
`group_by().agg()`.

If you want a complete grid of Type_1 x Type_2 combinations, create the grid
explicitly and left-join the observed aggregation result onto it.
'''

type_1_keys = lf_pokemon.select('type_1').unique().sort('type_1')
type_2_keys = lf_pokemon.select('type_2').unique().drop_nulls('type_2').sort('type_2')

all_type_pairs = type_1_keys.join(type_2_keys, how='cross')

observed_type_pair_stats = (
    lf_pokemon
    .drop_nulls(['type_1', 'type_2'])
    .group_by(['type_1', 'type_2'])
    .agg(
        c('hp').min().alias('min_hp'),
        c('hp').max().alias('max_hp'),
        c('hp').mean().alias('mean_hp'),
    )
)

print(
    all_type_pairs
    .join(observed_type_pair_stats, on=['type_1', 'type_2'], how='left')
    .sort(['type_1', 'type_2'])
    .collect()
)

# =========================================================================================
# 2. Time-Based Grouping
# =========================================================================================
'''
Polars uses `group_by_dynamic()` for time-window grouping.

The datetime column must be a Polars Date or Datetime dtype.
For regular time windows, use:

    group_by_dynamic(index_column='date', every='5d')

To also group by another categorical key, add:

    group_by='country'

The output window label is stored in the datetime column itself.
'''

##-------------------------------------------------##
## Mean NO2 value every 5 days, grouped by country ##
##-------------------------------------------------##
'''
The data must be sorted by the dynamic index column before `group_by_dynamic()`.
'''

lf_aq_grouped_5d = (
    lf_aq
    .sort('date')
    .group_by_dynamic(
        index_column='date',
        every='5d',
        group_by='country',
        closed='left',
    )
    .agg(
        c('value').mean().alias('value')
    )
    .sort(['date', 'country'])
)

print(lf_aq_grouped_5d.collect())
# shape: (28, 3)
# ┌─────────┬─────────────────────────┬───────────┐
# │ country ┆ date                    ┆ value     │
# │ ---     ┆ ---                     ┆ ---       │
# │ str     ┆ datetime[μs, UTC]       ┆ f64       │
# ╞═════════╪═════════════════════════╪═══════════╡
# │ BE      ┆ 2019-05-04 00:00:00 UTC ┆ 34.75     │
# │ FR      ┆ 2019-05-04 00:00:00 UTC ┆ 29.404255 │
# │ GB      ┆ 2019-05-04 00:00:00 UTC ┆ 24.454545 │
# │ BE      ┆ 2019-05-09 00:00:00 UTC ┆ 17.65     │
# │ FR      ┆ 2019-05-09 00:00:00 UTC ┆ 25.410256 │
# │ GB      ┆ 2019-05-09 00:00:00 UTC ┆ 33.184211 │
# │ BE      ┆ 2019-05-14 00:00:00 UTC ┆ 29.791667 │
# │ FR      ┆ 2019-05-14 00:00:00 UTC ┆ 26.021008 │
# │ GB      ┆ 2019-05-14 00:00:00 UTC ┆ 30.168067 │
# │ BE      ┆ 2019-05-19 00:00:00 UTC ┆ 22.930233 │
# │ …       ┆ …                       ┆ …         │
# │ BE      ┆ 2019-06-03 00:00:00 UTC ┆ 15.0      │
# │ FR      ┆ 2019-06-03 00:00:00 UTC ┆ 28.5      │
# │ GB      ┆ 2019-06-03 00:00:00 UTC ┆ 17.076271 │
# │ BE      ┆ 2019-06-08 00:00:00 UTC ┆ 14.25     │
# │ FR      ┆ 2019-06-08 00:00:00 UTC ┆ 25.297458 │
# │ GB      ┆ 2019-06-08 00:00:00 UTC ┆ 20.692982 │
# │ BE      ┆ 2019-06-13 00:00:00 UTC ┆ 37.5      │
# │ FR      ┆ 2019-06-13 00:00:00 UTC ┆ 27.973504 │
# │ GB      ┆ 2019-06-13 00:00:00 UTC ┆ 16.362745 │
# │ FR      ┆ 2019-06-18 00:00:00 UTC ┆ 31.07037  │
# └─────────┴─────────────────────────┴───────────┘

##----------------------------------------------------------------##
## Same idea with additional aggregations inside each time window ##
##----------------------------------------------------------------##

print(
    lf_aq
    .sort('date')
    .group_by_dynamic(
        index_column='date',
        every='5d',
        group_by='country',
        closed='left',
    )
    .agg(
        pl.len().alias('count'),
        c('value').min().alias('min_value'),
        c('value').max().alias('max_value'),
        c('value').mean().alias('mean_value'),
    )
    .sort(['date', 'country'])
    .collect()
)
# shape: (28, 6)
# ┌─────────┬─────────────────────────┬───────┬───────────┬───────────┬────────────┐
# │ country ┆ date                    ┆ count ┆ min_value ┆ max_value ┆ mean_value │
# │ ---     ┆ ---                     ┆ ---   ┆ ---       ┆ ---       ┆ ---        │
# │ str     ┆ datetime[μs, UTC]       ┆ u32   ┆ f64       ┆ f64       ┆ f64        │
# ╞═════════╪═════════════════════════╪═══════╪═══════════╪═══════════╪════════════╡
# │ BE      ┆ 2019-05-04 00:00:00 UTC ┆ 4     ┆ 20.5      ┆ 50.5      ┆ 34.75      │
# │ FR      ┆ 2019-05-04 00:00:00 UTC ┆ 47    ┆ 10.6      ┆ 77.7      ┆ 29.404255  │
# │ GB      ┆ 2019-05-04 00:00:00 UTC ┆ 44    ┆ 16.0      ┆ 40.0      ┆ 24.454545  │
# │ BE      ┆ 2019-05-09 00:00:00 UTC ┆ 10    ┆ 10.5      ┆ 26.5      ┆ 17.65      │
# │ FR      ┆ 2019-05-09 00:00:00 UTC ┆ 117   ┆ 8.7       ┆ 60.7      ┆ 25.410256  │
# │ GB      ┆ 2019-05-09 00:00:00 UTC ┆ 114   ┆ 19.0      ┆ 97.0      ┆ 33.184211  │
# │ BE      ┆ 2019-05-14 00:00:00 UTC ┆ 12    ┆ 11.5      ┆ 41.5      ┆ 29.791667  │
# │ FR      ┆ 2019-05-14 00:00:00 UTC ┆ 119   ┆ 0.0       ┆ 67.5      ┆ 26.021008  │
# │ GB      ┆ 2019-05-14 00:00:00 UTC ┆ 119   ┆ 21.0      ┆ 46.0      ┆ 30.168067  │
# │ BE      ┆ 2019-05-19 00:00:00 UTC ┆ 43    ┆ 9.0       ┆ 60.5      ┆ 22.930233  │
# │ …       ┆ …                       ┆ …     ┆ …         ┆ …         ┆ …          │
# │ BE      ┆ 2019-06-03 00:00:00 UTC ┆ 1     ┆ 15.0      ┆ 15.0      ┆ 15.0       │
# │ FR      ┆ 2019-06-03 00:00:00 UTC ┆ 105   ┆ 9.8       ┆ 59.0      ┆ 28.5       │
# │ GB      ┆ 2019-06-03 00:00:00 UTC ┆ 118   ┆ 0.0       ┆ 40.0      ┆ 17.076271  │
# │ BE      ┆ 2019-06-08 00:00:00 UTC ┆ 4     ┆ 7.5       ┆ 21.0      ┆ 14.25      │
# │ FR      ┆ 2019-06-08 00:00:00 UTC ┆ 118   ┆ 0.0       ┆ 59.4      ┆ 25.297458  │
# │ GB      ┆ 2019-06-08 00:00:00 UTC ┆ 114   ┆ 0.0       ┆ 51.0      ┆ 20.692982  │
# │ BE      ┆ 2019-06-13 00:00:00 UTC ┆ 12    ┆ 17.5      ┆ 45.0      ┆ 37.5       │
# │ FR      ┆ 2019-06-13 00:00:00 UTC ┆ 117   ┆ 8.1       ┆ 78.3      ┆ 27.973504  │
# │ GB      ┆ 2019-06-13 00:00:00 UTC ┆ 102   ┆ 4.0       ┆ 29.0      ┆ 16.362745  │
# │ FR      ┆ 2019-06-18 00:00:00 UTC ┆ 27    ┆ 15.3      ┆ 66.2      ┆ 31.07037   │
# └─────────┴─────────────────────────┴───────┴───────────┴───────────┴────────────┘
