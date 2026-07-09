'''
In Polars, time series data is handled fundamentally differently than in pandas:
1. Scalars: Polars does NOT have custom `pl.Timestamp` or `pl.Timedelta` classes.
   Instead, it relies on standard Python `datetime.datetime`, `datetime.date`, and `datetime.timedelta`.
2. Series Types: `pl.Datetime`, `pl.Date`, `pl.Duration`.
3. Expressions: All time manipulation is vectorized via the `.dt` namespace.
4. Grouping: Time-based grouping uses `group_by_dynamic()` instead of `pd.Grouper`.

######################################################
1. Scalars: Standard Python datetime & timedelta
2. Creating Time Series: pl.date_range(), pl.datetime_range(), pl.duration()
3. The `.dt` Namespace (Properties & Extraction)
4. Datetime to String
5. Time Rounding and Normalization (truncate, round)
6. Timezone Handling (replace_time_zone, convert_time_zone)
7. Timedelta / Duration Handling (Arithmetic & Components)
8. Time-Based Grouping: group_by_dynamic() (Equivalent to pd.Grouper)
9. Rolling Window by Time (rolling_*_by)
'''

import polars as pl
import datetime as dt


#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. Scalars --------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Because Polars delegates scalar time objects to the Python standard library,
you create single timestamps and durations using `datetime` and `timedelta`.
'''

# Python datetime (Equivalent to pd.Timestamp)
ts = dt.datetime(2023, 3, 15, 14, 30, 45)
print(ts)
# 2023-03-15 14:30:45
print(type(ts))
# <class 'datetime.datetime'>

# Python timedelta (Equivalent to pd.Timedelta)
td = dt.timedelta(days=5, hours=3, minutes=15)
print(td)
# 5 days, 3:15:00
print(type(td))
# <class 'datetime.timedelta'>

# Extracting a scalar from a Polars Series returns a standard Python object!
s = pl.Series([dt.datetime(2023, 1, 1), dt.datetime(2023, 1, 2)])
print(s.item(0))
# 2023-01-01 00:00:00
print(type(s.item(0)))
# <class 'datetime.datetime'>


#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 2. Creating Time Series -------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Instead of pd.date_range() or pd.timedelta_range(), Polars provides
pl.date_range(), pl.datetime_range(), and pl.duration().
Note: Setting `eager=True` evaluates the expression immediately into a Series.
'''

#####################
## pl.date_range() ##
#####################

s_dates = pl.date_range(
    start=dt.date(2023, 1, 1),
    end=dt.date(2023, 1, 5),
    interval="1d",
    eager=True
)
print(s_dates)
# shape: (5,)
# Series: '' [date]
# [
# 	2023-01-01
# 	2023-01-02
# 	2023-01-03
# 	2023-01-04
# 	2023-01-05
# ]

#########################
## pl.datetime_range() ##
#########################

s_datetimes = pl.datetime_range(
    start=dt.datetime(2023, 1, 1, 8, 30, 15),
    end=dt.datetime(2023, 1, 3, 8, 30, 15),
    interval="12h",
    eager=True
)
print(s_datetimes)
# shape: (5,)
# Series: '' [datetime[μs]]
# [
# 	2023-01-01 08:30:15
# 	2023-01-01 20:30:15
# 	2023-01-02 08:30:15
# 	2023-01-02 20:30:15
# 	2023-01-03 08:30:15
# ]

###################
## pl.duration() ##
###################

# Creates a single Duration scalar or Series
s_durations = pl.Series([
    pl.duration(days=1, hours=8),
    pl.duration(days=2, hours=12),
    pl.duration(days=3, hours=5)
])
print(s_durations)
# shape: (3,)
# Series: '' [duration[μs]]
# [
# 	1d 8h
# 	2d 12h
# 	3d 5h
# ]


#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. The `.dt` Namespace --------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Just like pandas `.dt`, Polars uses the `.dt` namespace for vectorized datetime operations.
Note: Polars methods are functions (e.g., `.dt.year()`), not properties (e.g., `.dt.year`).
'''

s_dt = pl.Series([
    dt.datetime(2023, 1, 1, 8, 30, 15),
    dt.datetime(2023, 3, 15, 14, 45, 30),
    dt.datetime(2024, 12, 31, 23, 59, 59) # Leap year
])

# Basic properties
print(s_dt.dt.year())      # [2023, 2023, 2024]
print(s_dt.dt.month())     # [1, 3, 12]
print(s_dt.dt.day())       # [1, 15, 31]
print(s_dt.dt.hour())      # [8, 14, 23]
print(s_dt.dt.minute())    # [30, 45, 59]
print(s_dt.dt.second())    # [15, 30, 59]

# Extended properties
print(s_dt.dt.weekday())
# [7, 3, 2]
# NOTE: Polars weekday() returns 1-7 (Monday=1, Sunday=7).
# Python's datetime.weekday() and pandas .dt.weekday return 0-6.

print(s_dt.dt.ordinal_day())
# [1, 74, 366] (Equivalent to pandas .dt.dayofyear)

# Boolean properties
print(s_dt.dt.is_leap_year())
# [false, false, true]

'''
NOTE: Polars does NOT have native boolean properties like .is_month_start or .is_month_end.
To achieve this, you typically compare the date to its truncated version or use string formatting.
'''


#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 4. String Representation ------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Instead of .strftime() or .day_name(), Polars uses .dt.to_string() with standard chrono format codes.
https://docs.rs/chrono/latest/chrono/format/strftime/index.html
'''

s_dt = pl.datetime_range(dt.datetime(2023, 1, 1), dt.datetime(2023, 1, 3), "1d", eager=True)

# Custom formatting
print(s_dt.dt.to_string("%Y-%m-%d"))
# ["2023-01-01", "2023-01-02", "2023-01-03"]

print(s_dt.dt.to_string("%A, %B %d, %Y"))
# ["Sunday, January 01, 2023", "Monday, January 02, 2023", "Tuesday, January 03, 2023"]

# Day and Month names
print(s_dt.dt.to_string("%A")) # Day names ["Sunday", "Monday", "Tuesday"]
print(s_dt.dt.to_string("%B")) # Month names ["January", "January", "January"]


#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 5. Time Rounding & Normalization ----------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Pandas: .dt.round(), .dt.floor(), .dt.ceil(), .dt.normalize()
Polars: .dt.round(), .dt.truncate() (equivalent to floor/normalize)
'''
s_dt = pl.Series([dt.datetime(2023, 1, 1, 8, 45, 23)])

# Round to nearest frequency
print(s_dt.dt.round("1h"))
# 2023-01-01 09:00:00

print(s_dt.dt.round("15m"))
# 2023-01-01 08:45:00

# Truncate (Floor / Normalize)
print(s_dt.dt.truncate("1h")) # Floor to hour
# 2023-01-01 08:00:00

print(s_dt.dt.truncate("1d")) # Equivalent to pandas .dt.normalize() (midnight)
# 2023-01-01 00:00:00


#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 6. Timezone Handling ----------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Pandas: .dt.tz_localize(), .dt.tz_convert()
Polars: .dt.replace_time_zone(), .dt.convert_time_zone()
'''

s_naive = pl.Series([dt.datetime(2023, 1, 1, 12, 0, 0)])

# Localize (Assign timezone to naive datetime)
s_utc = s_naive.dt.replace_time_zone("UTC")
print(s_utc)
# 2023-01-01 12:00:00 UTC

# Convert between timezones
s_tokyo = s_utc.dt.convert_time_zone("Asia/Tokyo")
print(s_tokyo)
# 2023-01-01 21:00:00 JST

# Remove timezone (make naive again)
s_naive_again = s_tokyo.dt.replace_time_zone(None)
print(s_naive_again)
# 2023-01-01 21:00:00


#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 7. Timedelta / Duration Handling ----------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Polars handles durations via the `pl.Duration` type.
Unlike pandas (which has `.dt.days`, `.dt.seconds` for individual components), Polars provides
`total_*` methods that return the ENTIRE duration expressed in that unit.
It does NOT have built-in remainder/component extractors.
'''

s_durations = pl.Series([
    dt.timedelta(days=1, hours=8, minutes=30, seconds=15),
    dt.timedelta(days=2, hours=12, minutes=45, seconds=30)
])

#################################
## The Polars Way: Total Units ##
#################################
# Returns the total duration expressed in the specified unit (as Intt64)

print(s_durations.dt.total_days())
# [1.3543402777777778, 2.53125]

print(s_durations.dt.total_hours())
# [32.50416666666667, 60.75]

print(s_durations.dt.total_minutes())
# [1950.25, 3645.0]

print(s_durations.dt.total_seconds())
# [117015.0, 218730.0]

#####################################
## Emulating pandas .dt.components ##
#####################################
'''
If you strictly need the broken-down remainder components (Days, Hours, Minutes, Seconds)
exactly like pandas `.dt.components`, you must calculate them manually using
`.dt.total_seconds()` and modulo arithmetic inside a DataFrame context.
'''

df_dur = s_durations.to_frame("dur")

df_components = df_dur.with_columns(
    (pl.col("dur").dt.total_seconds() // 86400).cast(pl.Int64).alias("days"),
    ((pl.col("dur").dt.total_seconds() % 86400) // 3600).cast(pl.Int64).alias("hours"),
    ((pl.col("dur").dt.total_seconds() % 3600) // 60).cast(pl.Int64).alias("minutes"),
    (pl.col("dur").dt.total_seconds() % 60).cast(pl.Int64).alias("seconds")
)
print(df_components)
# shape: (2, 5)
# ┌───────────────┬──────┬───────┬─────────┬─────────┐
# │ dur           ┆ days ┆ hours ┆ minutes ┆ seconds │
# │ ---           ┆ ---  ┆ ---   ┆ ---     ┆ ---     │
# │ duration[μs]  ┆ i64  ┆ i64   ┆ i64     ┆ i64     │
# ╞═══════════════╪══════╪═══════╪═════════╪═════════╡
# │ 1d 8h 30m 15s ┆ 1    ┆ 8     ┆ 30      ┆ 15      │
# │ 2d 12h 45m 30s┆ 2    ┆ 12    ┆ 45      ┆ 30      │
# └───────────────┴──────┴───────┴─────────┴─────────┘

##########################################
##            Arithmetic                ##
##########################################

s_dates = pl.Series([dt.datetime(2023, 1, 1), dt.datetime(2023, 2, 1)])

# Add Duration to Datetime
print(s_dates + pl.duration(days=5, hours=3))
# 2023-01-06 03:00:00
# 2023-02-06 03:00:00

# Subtract Datetimes to get Duration
diff = s_dates - s_dates.shift(1)
print(diff)
# [null, 31d]

# Calendar-aware offsetting (respects DST and month lengths)
print(s_dates.dt.offset_by("1mo")) # Adds exactly 1 calendar month
# 2023-02-01
# 2023-03-01


#-----------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 8. Time-Based Grouping ---------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Pandas: df.groupby(pd.Grouper(key="date", freq="3D"))
Polars: df.group_by_dynamic(index_column="date", every="3d")

group_by_dynamic is one of Polars' most powerful features for time series.
'''

df = pl.DataFrame({
    "date": pl.date_range(dt.date(2023, 1, 1), dt.date(2023, 1, 7), "1d", eager=True),
    "price": [100, 150, 200, 250, 300, 350, 400]
})

# Group by every 3 days and sum
df_grouped = df.group_by_dynamic(
    index_column="date",
    every="3d",
    closed="left" # Includes the left boundary, excludes right
).agg(
    pl.col("price").sum().alias("total_price"),
    pl.col("price").mean().alias("avg_price")
)
print(df_grouped)
# shape: (3, 3)
# ┌────────────┬─────────────┬───────────┐
# │ date       ┆ total_price ┆ avg_price │
# │ ---        ┆ ---         ┆ ---       │
# │ date       ┆ i64         ┆ f64       │
# ╞════════════╪═════════════╪═══════════╡
# │ 2023-01-01 ┆ 450         ┆ 150.0     │ (100+150+200)
# │ 2023-01-04 ┆ 900         ┆ 300.0     │ (250+300+350)
# │ 2023-01-07 ┆ 400         ┆ 400.0     │ (400)
# └────────────┴─────────────┴───────────┘


#-----------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 9. Rolling Window by Time -----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
'''
Pandas: s.rolling(window="2s").mean()
Polars: pl.col("value").rolling_mean_by(window_size="2s", by="time")

Because Polars Series don't have indexes, time-based rolling operations must
explicitly specify the time column using the `_by` suffix methods inside a DataFrame context.
'''

df_time = pl.DataFrame({
    "time": pl.datetime_range(
        dt.datetime(2013, 1, 1, 9, 0, 0),
        dt.datetime(2013, 1, 1, 9, 0, 6),
        "1s",
        eager=True
    ),
    "value": [3.99, 2.72, 4.30, 6.05, 2.53, 1.10, 8.90]
})

# Calculate rolling mean with a 2-second window
df_rolling = df_time.with_columns(
    pl.col("value").rolling_mean_by(
        by="time",
        window_size="2s",
        closed="right" # Default: includes current row and looks backward
    ).alias("rolling_mean_2s")
)
print(df_rolling)
# shape: (7, 3)
# ┌─────────────────────┬───────┬─────────────────┐
# │ time                ┆ value ┆ rolling_mean_2s │
# │ ---                 ┆ ---   ┆ ---             │
# │ datetime[μs]        ┆ f64   ┆ f64             │
# ╞═════════════════════╪═══════╪═════════════════╡
# │ 2013-01-01 09:00:00 ┆ 3.99  ┆ 3.99            │
# │ 2013-01-01 09:00:01 ┆ 2.72  ┆ 2.72            │ (Only 1 value in the last 2s strictly before 09:00:01)
# │ 2013-01-01 09:00:02 ┆ 4.3   ┆ 3.51            │ (2.72 + 4.30) / 2
# │ 2013-01-01 09:00:03 ┆ 6.05  ┆ 6.05            │
# │ 2013-01-01 09:00:04 ┆ 2.53  ┆ 4.29            │ (6.05 + 2.53) / 2
# │ 2013-01-01 09:00:05 ┆ 1.1   ┆ 1.1             │
# │ 2013-01-01 09:00:06 ┆ 8.9   ┆ 5.0             │ (1.10 + 8.90) / 2
# └─────────────────────┴───────┴─────────────────┘
