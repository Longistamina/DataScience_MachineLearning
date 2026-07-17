import polars as pl
from polars import col as c
from pathlib import Path

data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

##################################
## Read the Air Quality dataset ##
##################################

lf_aq = (
    pl.scan_csv(data_dir/"air_quality_no2_long.csv")
    .rename(mapping={"date.utc": "date"})
)

print(lf_aq.head().collect())
# shape: (5, 7)
# ┌───────┬─────────┬───────────────────────────┬──────────┬───────────┬───────┬───────┐
# │ city  ┆ country ┆ date                      ┆ location ┆ parameter ┆ value ┆ unit  │
# │ ---   ┆ ---     ┆ ---                       ┆ ---      ┆ ---       ┆ ---   ┆ ---   │
# │ str   ┆ str     ┆ str                       ┆ str      ┆ str       ┆ f64   ┆ str   │
# ╞═══════╪═════════╪═══════════════════════════╪══════════╪═══════════╪═══════╪═══════╡
# │ Paris ┆ FR      ┆ 2019-06-21 00:00:00+00:00 ┆ FR04014  ┆ no2       ┆ 20.0  ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 23:00:00+00:00 ┆ FR04014  ┆ no2       ┆ 21.8  ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 22:00:00+00:00 ┆ FR04014  ┆ no2       ┆ 26.5  ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 21:00:00+00:00 ┆ FR04014  ┆ no2       ┆ 24.9  ┆ µg/m³ │
# │ Paris ┆ FR      ┆ 2019-06-20 20:00:00+00:00 ┆ FR04014  ┆ no2       ┆ 21.4  ┆ µg/m³ │
# └───────┴─────────┴───────────────────────────┴──────────┴───────────┴───────┴───────┘
'''date is still str, not datetime datatype yet'''

#########################################
## Convert the date column to datetime ##
#########################################

lf_aq = (
    lf_aq
    .with_columns(c("date").str.strptime(dtype=pl.Datetime(time_zone="UTC"), format="%Y-%m-%d %H:%M:%S%z"))
    # Use ``pl.Datetime`` to preserve the time information
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

###########################################
## df["date"].min() and df["date"].max() ##
###########################################

print(
    lf_aq
    .select(
        c.date.min().alias("date_min"), # the earliest date in the column
        c.date.max().alias("date_max")  # the latest date in the column
    )
    .collect()
)
# shape: (1, 2)
# ┌─────────────────────────┬─────────────────────────┐
# │ date_min                ┆ date_max                │
# │ ---                     ┆ ---                     │
# │ datetime[μs, UTC]       ┆ datetime[μs, UTC]       │
# ╞═════════════════════════╪═════════════════════════╡
# │ 2019-05-07 01:00:00 UTC ┆ 2019-06-21 00:00:00 UTC │
# └─────────────────────────┴─────────────────────────┘

################################################
## Extract some properties of the date column ##
################################################

print(
    lf_aq
    .select(
        c.date.dt.month().alias("month"),
        c.date.dt.day().alias("day")
    )
    .collect()
)
# shape: (2_068, 2)
# ┌───────┬─────┐
# │ month ┆ day │
# │ ---   ┆ --- │
# │ i8    ┆ i8  │
# ╞═══════╪═════╡
# │ 6     ┆ 21  │
# │ 6     ┆ 20  │
# │ 6     ┆ 20  │
# │ 6     ┆ 20  │
# │ 6     ┆ 20  │
# │ …     ┆ …   │
# │ 5     ┆ 7   │
# │ 5     ┆ 7   │
# │ 5     ┆ 7   │
# │ 5     ┆ 7   │
# │ 5     ┆ 7   │
# └───────┴─────┘

print(
    lf_aq
    .select(c.date.dt.year().unique())
    .collect()
)
# shape: (1, 1)
# ┌──────┐
# │ date │
# │ ---  │
# │ i32  │
# ╞══════╡
# │ 2019 │
# └──────┘

############################################
## Groupby statistics on time series data ##
############################################

#----------------
## Groupby weekday and location, compute the mean value
#----------------

print(
    lf_aq
    .group_by(c.date.dt.weekday(), c.location)
    .agg(c.value.mean().alias("value_mean"))
    .sort(c.date, c.location, c.value_mean)
    .collect()
)
# shape: (21, 3)
# ┌──────┬────────────────────┬────────────┐
# │ date ┆ location           ┆ value_mean │
# │ ---  ┆ ---                ┆ ---        │
# │ i8   ┆ str                ┆ f64        │
# ╞══════╪════════════════════╪════════════╡
# │ 1    ┆ BETR801            ┆ 27.875     │
# │ 1    ┆ FR04014            ┆ 24.85625   │
# │ 1    ┆ London Westminster ┆ 23.969697  │
# │ 2    ┆ BETR801            ┆ 22.214286  │
# │ 2    ┆ FR04014            ┆ 30.999359  │
# │ …    ┆ …                  ┆ …          │
# │ 6    ┆ FR04014            ┆ 25.266154  │
# │ 6    ┆ London Westminster ┆ 24.977612  │
# │ 7    ┆ BETR801            ┆ 21.896552  │
# │ 7    ┆ FR04014            ┆ 23.274306  │
# │ 7    ┆ London Westminster ┆ 24.859155  │
# └──────┴────────────────────┴────────────┘

#----------------
## Groupby using group_by_dynamic, calculate the mean every 5 days, and by country
#----------------

print(
    lf_aq
    .sort(by=[c.date, c.country]) # Must sort first before grouping here
    .group_by_dynamic(
        index_column=c.date,
        every="5d",
        group_by=c.country,
        closed="both"
    )
    .agg(c.value.mean().alias("value_mean"))
    .collect()
)
# shape: (28, 3)
# ┌─────────┬─────────────────────────┬────────────┐
# │ country ┆ date                    ┆ value_mean │
# │ ---     ┆ ---                     ┆ ---        │
# │ str     ┆ datetime[μs, UTC]       ┆ f64        │
# ╞═════════╪═════════════════════════╪════════════╡
# │ BE      ┆ 2019-05-04 00:00:00 UTC ┆ 34.75      │
# │ BE      ┆ 2019-05-09 00:00:00 UTC ┆ 17.65      │
# │ BE      ┆ 2019-05-14 00:00:00 UTC ┆ 29.307692  │
# │ BE      ┆ 2019-05-19 00:00:00 UTC ┆ 22.930233  │
# │ BE      ┆ 2019-05-24 00:00:00 UTC ┆ 35.6       │
# │ …       ┆ …                       ┆ …          │
# │ GB      ┆ 2019-05-24 00:00:00 UTC ┆ 26.226891  │
# │ GB      ┆ 2019-05-29 00:00:00 UTC ┆ 21.694215  │
# │ GB      ┆ 2019-06-03 00:00:00 UTC ┆ 17.168067  │
# │ GB      ┆ 2019-06-08 00:00:00 UTC ┆ 20.765217  │
# │ GB      ┆ 2019-06-13 00:00:00 UTC ┆ 16.362745  │
# └─────────┴─────────────────────────┴────────────┘

############################################################
## rolling_mean_by() and ewm_mean_by() with time (c.date) ##
############################################################

print(
    lf_aq
    .filter(c.city == "Paris")
    .select(
        c.date,
        c.value.rolling_mean_by(by=c.date, window_size="3h").alias("value_rolling_mean"),
        c.value.ewm_mean(span=2, adjust=False).alias("value_ewm_mean")
    )
    .collect()
)
# shape: (1_004, 3)
# ┌─────────────────────────┬────────────────────┬────────────────┐
# │ date                    ┆ value_rolling_mean ┆ value_ewm_mean │
# │ ---                     ┆ ---                ┆ ---            │
# │ datetime[μs, UTC]       ┆ f64                ┆ f64            │
# ╞═════════════════════════╪════════════════════╪════════════════╡
# │ 2019-06-21 00:00:00 UTC ┆ 22.766667          ┆ 20.0           │
# │ 2019-06-20 23:00:00 UTC ┆ 24.4               ┆ 21.2           │
# │ 2019-06-20 22:00:00 UTC ┆ 24.266667          ┆ 24.733333      │
# │ 2019-06-20 21:00:00 UTC ┆ 23.866667          ┆ 24.844444      │
# │ 2019-06-20 20:00:00 UTC ┆ 23.533333          ┆ 22.548148      │
# │ …                       ┆ …                  ┆ …              │
# │ 2019-05-07 05:00:00 UTC ┆ 61.566667          ┆ 72.301851      │
# │ 2019-05-07 04:00:00 UTC ┆ 46.666667          ┆ 65.367284      │
# │ 2019-05-07 03:00:00 UTC ┆ 34.366667          ┆ 55.389095      │
# │ 2019-05-07 02:00:00 UTC ┆ 26.35              ┆ 36.929698      │
# │ 2019-05-07 01:00:00 UTC ┆ 25.0               ┆ 28.976566      │
# └─────────────────────────┴────────────────────┴────────────────┘
