'''
Window expressions and Python functions applied to groups in Polars.

1. `expr.over(...)`: compute group-wise values and keep the original rows.

2. `lf.group_by(...).map_groups(...)`:
    run a Python function for each ordinary group.

3. `lf.group_by_dynamic(...).map_groups(...)`:
    run a Python function for each time window (optionally split further by keys).

Prefer native expressions for both `over` and `.agg(...)`. `map_groups` is a
specialized escape hatch: the Python callback gets materialized DataFrames,
so it prevents many lazy optimizations and is generally slower.
'''

from pathlib import Path

import polars as pl
from polars import col as c
from polars import selectors as cs

# Optional display settings
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(14)
pl.Config.set_tbl_width_chars(120)

data_dir = next(Path('/home').rglob('*/DataScience_MachineLearning/data'))

# =========================================================================================
# 0. Setup Data
# =========================================================================================

# Pokemon
lf_pokemon = (
    pl.scan_csv(data_dir/"pokemon.csv")
    .drop('#')
    .select(pl.all().name.replace(r"\s+", "_").name.replace(".", "", literal=True).name.to_lowercase())
    .with_columns(cs.string().exclude("name").cast(pl.Categorical))
    .pipe(lambda lf: lf.with_columns(
        c.generation.cast(pl.String).cast(pl.Enum(
            lf.select("generation").collect().to_series().cast(pl.String).unique().sort()
        ))
    ))
)
print(lf_pokemon.head(5).collect())
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

# air quality
lf_aq = (
    pl.scan_csv(data_dir/"air_quality_no2_long.csv")
    .rename({"date.utc": "date"})
    .with_columns(
        c.date.str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S%z")
    )
)
print(lf_aq.head(5).collect())
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

# =========================================================================================
# 1. `expr.over(...)`
# =========================================================================================
'''
An expression followed by `.over("type_1")` computes within each type_1 group
and maps the result back onto the rows that belong to that group.

Unlike `group_by().agg(...)`, this usually keeps the input row count.
Think of it as a SQL window expression: it combines a group calculation
                                        with row-level columns in the same result.
'''

##-------------------------------------------##
## Add group statistics to every Pokémon row ##
##-------------------------------------------##

print(
    lf_pokemon
    .select(
        "name", "type_1", "attack",
        c.attack.mean().over("type_1").alias("type_mean_attack"),
        c.attack.max().over("type_1").alias("type_max_attack"),
        (c.attack / c.attack.sum().over("type_1")).alias("share_of_type_attack"),
    )
    .filter(c.type_1 == "Fire")
    .sort("attack", descending=True)
    .head(8)
    .collect()
)
# shape: (8, 6)
# ┌───────────────────────────┬────────┬────────┬──────────────────┬─────────────────┬──────────────────────┐
# │ name                      ┆ type_1 ┆ attack ┆ type_mean_attack ┆ type_max_attack ┆ share_of_type_attack │
# │ ---                       ┆ ---    ┆ ---    ┆ ---              ┆ ---             ┆ ---                  │
# │ str                       ┆ cat    ┆ i64    ┆ f64              ┆ i64             ┆ f64                  │
# ╞═══════════════════════════╪════════╪════════╪══════════════════╪═════════════════╪══════════════════════╡
# │ BlazikenMega Blaziken     ┆ Fire   ┆ 160    ┆ 84.769231        ┆ 160             ┆ 0.036298             │
# │ DarmanitanStandard Mode   ┆ Fire   ┆ 140    ┆ 84.769231        ┆ 160             ┆ 0.03176              │
# │ CharizardMega Charizard X ┆ Fire   ┆ 130    ┆ 84.769231        ┆ 160             ┆ 0.029492             │
# │ Flareon                   ┆ Fire   ┆ 130    ┆ 84.769231        ┆ 160             ┆ 0.029492             │
# │ Ho-oh                     ┆ Fire   ┆ 130    ┆ 84.769231        ┆ 160             ┆ 0.029492             │
# │ Emboar                    ┆ Fire   ┆ 123    ┆ 84.769231        ┆ 160             ┆ 0.027904             │
# │ Blaziken                  ┆ Fire   ┆ 120    ┆ 84.769231        ┆ 160             ┆ 0.027223             │
# │ CameruptMega Camerupt     ┆ Fire   ┆ 120    ┆ 84.769231        ┆ 160             ┆ 0.027223             │
# └───────────────────────────┴────────┴────────┴──────────────────┴─────────────────┴──────────────────────┘

##-----------------------------##
## Rank rows within each group ##
##-----------------------------##
'''
`.rank()` can be used as a window expression. The ranking restarts for each
Type_1 value. `descending=True` assigns rank 1 to the largest Attack value.
'''

print(
    lf_pokemon
    .select(
        "name", "type_1", "attack",
        c.attack.rank(method="dense", descending=True)
        .over("type_1")
        .alias("attack_rank_in_type1"),
    )
    .filter(c.type_1.is_in(["Fire", "Water"]))
    .sort(["type_1", "attack_rank_in_type1", "name"])
    .collect()
)

##----------------------------------------##
## Multiple keys and window ordering      ##
##----------------------------------------##
'''
Pass multiple keys to make one window per key combination. `order_by` controls
the order used by order-sensitive expressions such as `rank`, `shift`, and
cumulative calculations; it does not sort the final LazyFrame.
'''

print(
    lf_pokemon
    .select(
        "name", "type_1", "type_2", "attack",
        c.attack.rank(method="ordinal", descending=True)
        .over(["type_1", "type_2"], order_by="name")
        .alias("rank_in_type_pair"),
    )
    .head(20)
    .collect()
)

##---------------------------##
## `over` mapping strategies ##
##---------------------------##
'''
By default, `over` maps results back to the original row positions.
The `mapping_strategy="explode"` option is useful when the output is meant to be
grouped/contiguous; it changes row ordering and should be used only when that
mapping is appropriate for the query.
'''

print(
    lf_pokemon
    .with_row_index()
    .select(
        c("index", "name", "type_1", "total").head(3).over("type_1", mapping_strategy="explode")
    )
    .collect()
)
# shape: (54, 4)
# ┌───────┬─────────────────────────┬────────┬───────┐
# │ index ┆ name                    ┆ type_1 ┆ total │
# │ ---   ┆ ---                     ┆ ---    ┆ ---   │
# │ u32   ┆ str                     ┆ cat    ┆ i64   │
# ╞═══════╪═════════════════════════╪════════╪═══════╡
# │ 0     ┆ Bulbasaur               ┆ Grass  ┆ 318   │
# │ 1     ┆ Ivysaur                 ┆ Grass  ┆ 405   │
# │ 2     ┆ Venusaur                ┆ Grass  ┆ 525   │
# │ 4     ┆ Charmander              ┆ Fire   ┆ 309   │
# │ 5     ┆ Charmeleon              ┆ Fire   ┆ 405   │
# │ 6     ┆ Charizard               ┆ Fire   ┆ 534   │
# │ …    ┆ …                       ┆ …      ┆ …     │
# │ 223   ┆ Steelix                 ┆ Steel  ┆ 510   │
# │ 224   ┆ SteelixMega Steelix     ┆ Steel  ┆ 610   │
# │ 245   ┆ Skarmory                ┆ Steel  ┆ 465   │
# │ 702   ┆ TornadusIncarnate Forme ┆ Flying ┆ 580   │
# │ 703   ┆ TornadusTherian Forme   ┆ Flying ┆ 580   │
# │ 790   ┆ Noibat                  ┆ Flying ┆ 245   │
# └───────┴─────────────────────────┴────────┴───────┘

##----------------------------------##
## `over` with time window grouping ##
##----------------------------------##
'''
`expr.over()` groups rows by existing key values and maps each group’s result back to its rows.
It doesn’t create time windows with `every, period, or offset` the way `group_by_dynamic()` does.

=> Create an intermediate column named `window` to use as grouping key
'''

print(
    lf_aq
    .select("country", c("date").dt.truncate("5d").alias("window"), "value")
    .with_columns(
        c("value").sum().over(["country", "window"])
    )
    .unique(subset=["country", "window"], keep="first")
    .sort(["country", "window"])
    .collect()
)
# shape: (28, 3)
# ┌─────────┬─────────────────────────┬────────┐
# │ country ┆ window                  ┆ value  │
# │ ---     ┆ ---                     ┆ ---    │
# │ str     ┆ datetime[μs, UTC]       ┆ f64    │
# ╞═════════╪═════════════════════════╪════════╡
# │ BE      ┆ 2019-05-04 00:00:00 UTC ┆ 139.0  │
# │ BE      ┆ 2019-05-09 00:00:00 UTC ┆ 176.5  │
# │ BE      ┆ 2019-05-14 00:00:00 UTC ┆ 357.5  │
# │ BE      ┆ 2019-05-19 00:00:00 UTC ┆ 986.0  │
# │ BE      ┆ 2019-05-24 00:00:00 UTC ┆ 178.0  │
# │ BE      ┆ 2019-05-29 00:00:00 UTC ┆ 90.0   │
# │ …       ┆ …                       ┆ …      │
# │ GB      ┆ 2019-05-19 00:00:00 UTC ┆ 3818.0 │
# │ GB      ┆ 2019-05-24 00:00:00 UTC ┆ 3095.0 │
# │ GB      ┆ 2019-05-29 00:00:00 UTC ┆ 2604.0 │
# │ GB      ┆ 2019-06-03 00:00:00 UTC ┆ 2015.0 │
# │ GB      ┆ 2019-06-08 00:00:00 UTC ┆ 2359.0 │
# │ GB      ┆ 2019-06-13 00:00:00 UTC ┆ 1669.0 │
# └─────────┴─────────────────────────┴────────┘

# =========================================================================================
# 2. `lf.group_by(...).map_groups(...)`
# =========================================================================================
'''
`map_groups` passes a materialized `DataFrame` for each group to a Python
function. It can return a different number of rows from each group, which is
useful for custom procedures that are awkward to express as Polars expressions.

However, it is still recommended to prefer using native Polars expression
'''

pokemon_schema = lf_pokemon.collect_schema()

##----------------------##
## map_groups(function) ##
##----------------------##

def top_custom_offense(group: pl.DataFrame) -> pl.DataFrame:
    return (
        group
        .with_columns((c.attack + c.sp_atk).alias("_offense_score"))
        .sort(["_offense_score", "name"], descending=[True, False])
        .head(2)
        .drop("_offense_score")
    )

print(
    lf_pokemon
    .group_by("type_1")
    .map_groups(top_custom_offense, schema=pokemon_schema)
    .select("name", "type_1", "attack", "sp_atk", "total")
    .sort(["type_1", "attack"], descending=[False, True])
    .collect()
)
# shape: (36, 5)
# ┌─────────────────────────┬────────┬────────┬────────┬───────┐
# │ name                    ┆ type_1 ┆ attack ┆ sp_atk ┆ total │
# │ ---                     ┆ ---    ┆ ---    ┆ ---    ┆ ---   │
# │ str                     ┆ cat    ┆ i64    ┆ i64    ┆ i64   │
# ╞═════════════════════════╪════════╪════════╪════════╪═══════╡
# │ HeracrossMega Heracross ┆ Bug    ┆ 185    ┆ 40     ┆ 600   │
# │ Genesect                ┆ Bug    ┆ 120    ┆ 120    ┆ 600   │
# │ AbsolMega Absol         ┆ Dark   ┆ 150    ┆ 115    ┆ 565   │
# │ Yveltal                 ┆ Dark   ┆ 131    ┆ 131    ┆ 680   │
# │ RayquazaMega Rayquaza   ┆ Dragon ┆ 180    ┆ 180    ┆ 780   │
# │ Rayquaza                ┆ Dragon ┆ 150    ┆ 150    ┆ 680   │
# │ …                       ┆ …      ┆ …      ┆ …      ┆ …     │
# │ TyranitarMega Tyranitar ┆ Rock   ┆ 164    ┆ 95     ┆ 700   │
# │ DiancieMega Diancie     ┆ Rock   ┆ 160    ┆ 160    ┆ 700   │
# │ AegislashBlade Forme    ┆ Steel  ┆ 150    ┆ 150    ┆ 520   │
# │ Dialga                  ┆ Steel  ┆ 120    ┆ 150    ┆ 680   │
# │ KyogrePrimal Kyogre     ┆ Water  ┆ 150    ┆ 180    ┆ 770   │
# │ Palkia                  ┆ Water  ┆ 120    ┆ 150    ┆ 680   │
# └─────────────────────────┴────────┴────────┴────────┴───────┘

##-------------------------------##
## map_groups(lambda group: ...) ##
##-------------------------------##

print(
    lf_pokemon
    .group_by("type_1")
    .map_groups(lambda group: group.select(c("type_1").first(), cs.numeric().std()), schema=pokemon_schema)
    .collect()
)
# shape: (18, 8)
# ┌─────────┬────────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┐
# │ type_1  ┆ total      ┆ hp        ┆ attack    ┆ defense   ┆ sp_atk    ┆ sp_def    ┆ speed     │
# │ ---     ┆ ---        ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       ┆ ---       │
# │ cat     ┆ f64        ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       ┆ f64       │
# ╞═════════╪════════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╪═══════════╡
# │ Dragon  ┆ 146.267538 ┆ 23.795415 ┆ 33.742622 ┆ 24.102938 ┆ 42.25736  ┆ 29.884843 ┆ 23.239961 │
# │ Water   ┆ 113.188266 ┆ 27.487026 ┆ 28.377192 ┆ 27.773809 ┆ 29.030128 ┆ 28.460493 ┆ 23.019353 │
# │ Normal  ┆ 115.733038 ┆ 36.23343  ┆ 30.295862 ┆ 23.771833 ┆ 23.946395 ┆ 25.142801 ┆ 28.406157 │
# │ Steel   ┆ 115.420907 ┆ 16.04401  ┆ 30.388276 ┆ 44.806548 ┆ 31.458606 ┆ 29.018758 ┆ 25.846578 │
# │ Rock    ┆ 108.059227 ┆ 20.833884 ┆ 35.325458 ┆ 36.447209 ┆ 28.24967  ┆ 32.265965 ┆ 29.90358  │
# │ Grass   ┆ 106.650626 ┆ 19.516564 ┆ 25.38052  ┆ 24.485192 ┆ 27.244864 ┆ 21.446645 ┆ 28.506456 │
# │ …       ┆ …          ┆ …         ┆ …         ┆ …         ┆ …         ┆ …         ┆ …         │
# │ Fire    ┆ 109.760496 ┆ 19.404123 ┆ 28.769275 ┆ 23.6582   ┆ 30.042121 ┆ 22.619908 ┆ 25.245783 │
# │ Poison  ┆ 92.358687  ┆ 19.665019 ┆ 19.63001  ┆ 21.066128 ┆ 19.322657 ┆ 19.887348 ┆ 22.631392 │
# │ Dark    ┆ 109.126217 ┆ 21.078297 ┆ 25.774247 ┆ 25.121982 ┆ 33.200952 ┆ 24.79902  ┆ 27.768203 │
# │ Ghost   ┆ 110.072685 ┆ 31.685895 ┆ 29.629687 ┆ 32.551138 ┆ 32.561217 ┆ 26.038414 ┆ 28.02028  │
# │ Psychic ┆ 139.026645 ┆ 28.42134  ┆ 42.309265 ┆ 28.359401 ┆ 38.53934  ┆ 31.126329 ┆ 37.335412 │
# │ Ice     ┆ 108.281027 ┆ 21.286861 ┆ 27.289511 ┆ 34.387708 ┆ 26.604967 ┆ 37.213227 ┆ 24.49841  │
# └─────────┴────────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┘

# =========================================================================================
# 3. `lf.group_by_dynamic(...).map_groups(...)`
# =========================================================================================

##----------------------##
## map_groups(function) ##
##----------------------##

def peak_observation_per_window(group: pl.DataFrame) -> pl.DataFrame:
    peak = group.sort(["value", "location"], descending=[True, False]).head(1)
    return peak.select("country", "date", "location", "value")

dynamic_result_schema = {
    "country": pl.String,
    "date": pl.Datetime("us", "UTC"),
    "location": pl.String,
    "value": pl.Float64,
}

lf_aq_window_peaks = (
    lf_aq
    .sort("date")
    .group_by_dynamic(index_column="date", every="5d", group_by="country", closed="left")
    .map_groups(peak_observation_per_window, schema=dynamic_result_schema)
    .sort(["date", "country"])
)
print(lf_aq_window_peaks.collect())
# shape: (28, 4)
# ┌─────────┬─────────────────────────┬────────────────────┬───────┐
# │ country ┆ date                    ┆ location           ┆ value │
# │ ---     ┆ ---                     ┆ ---                ┆ ---   │
# │ str     ┆ datetime[μs, UTC]       ┆ str                ┆ f64   │
# ╞═════════╪═════════════════════════╪════════════════════╪═══════╡
# │ BE      ┆ 2019-05-07 01:00:00 UTC ┆ BETR801            ┆ 50.5  │
# │ FR      ┆ 2019-05-07 06:00:00 UTC ┆ FR04014            ┆ 77.7  │
# │ GB      ┆ 2019-05-08 18:00:00 UTC ┆ London Westminster ┆ 40.0  │
# │ GB      ┆ 2019-05-09 15:00:00 UTC ┆ London Westminster ┆ 97.0  │
# │ FR      ┆ 2019-05-10 08:00:00 UTC ┆ FR04014            ┆ 60.7  │
# │ BE      ┆ 2019-05-11 01:00:00 UTC ┆ BETR801            ┆ 26.5  │
# │ …       ┆ …                       ┆ …                  ┆ …     │
# │ FR      ┆ 2019-06-11 22:00:00 UTC ┆ FR04014            ┆ 59.4  │
# │ BE      ┆ 2019-06-12 01:00:00 UTC ┆ BETR801            ┆ 21.0  │
# │ FR      ┆ 2019-06-13 23:00:00 UTC ┆ FR04014            ┆ 78.3  │
# │ GB      ┆ 2019-06-16 17:00:00 UTC ┆ London Westminster ┆ 29.0  │
# │ BE      ┆ 2019-06-17 07:00:00 UTC ┆ BETR801            ┆ 45.0  │
# │ FR      ┆ 2019-06-18 00:00:00 UTC ┆ FR04014            ┆ 66.2  │
# └─────────┴─────────────────────────┴────────────────────┴───────┘

##-------------------------------##
## map_groups(lambda group: ...) ##
##-------------------------------##

print(
    lf_aq
    .sort("date")
    .group_by_dynamic(index_column="date", every="3d", group_by="country", closed="left")
    .map_groups(lambda group: group.select(c("country", "date").first(), c("value").mean()), schema=lf_aq.collect_schema())
    .collect()
)
# shape: (46, 3)
# ┌─────────┬─────────────────────────┬───────────┐
# │ country ┆ date                    ┆ value     │
# │ ---     ┆ ---                     ┆ ---       │
# │ str     ┆ datetime[μs, UTC]       ┆ f64       │
# ╞═════════╪═════════════════════════╪═══════════╡
# │ BE      ┆ 2019-05-07 01:00:00 UTC ┆ 47.75     │
# │ BE      ┆ 2019-05-08 01:00:00 UTC ┆ 17.666667 │
# │ BE      ┆ 2019-05-11 01:00:00 UTC ┆ 19.0      │
# │ BE      ┆ 2019-05-14 01:00:00 UTC ┆ 20.4      │
# │ BE      ┆ 2019-05-18 01:00:00 UTC ┆ 24.112903 │
# │ BE      ┆ 2019-05-20 00:00:00 UTC ┆ 24.083333 │
# │ …       ┆ …                       ┆ …         │
# │ GB      ┆ 2019-06-01 00:00:00 UTC ┆ 24.875    │
# │ GB      ┆ 2019-06-04 00:00:00 UTC ┆ 15.239437 │
# │ GB      ┆ 2019-06-07 00:00:00 UTC ┆ 16.0      │
# │ GB      ┆ 2019-06-10 00:00:00 UTC ┆ 26.811594 │
# │ GB      ┆ 2019-06-13 00:00:00 UTC ┆ 17.044776 │
# │ GB      ┆ 2019-06-16 00:00:00 UTC ┆ 15.057143 │
# └─────────┴─────────────────────────┴───────────┘
