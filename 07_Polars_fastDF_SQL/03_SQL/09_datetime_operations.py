'''
Main ideas:
# Temporal functions cover extracting parts from Date/Datetime values and formatting
  Date/Datetime/Time values back to strings.

# In native Polars, the equivalents usually live under: c("date").dt....

Important Polars SQL notes:
+ Frame-level .sql(...) registers the frame as the SQL table named self.
+ LazyFrame.sql(...) returns a LazyFrame, so call .collect() to materialize.
+ SQL functions are not always named exactly the same as native Polars expression methods.
+ DATE_PART('dayofweek', ...) uses Sunday=0 to Saturday=6, while DATE_PART('isodow', ...)
  uses Monday=1 to Sunday=7.
'''

import datetime as dt

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(20)
pl.Config.set_tbl_cols(9)
pl.Config.set_float_precision(4)
pl.Config.set_tbl_width_chars(120)


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 0. Setup data --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The examples are self-contained so this file can run without external datasets.

We use one table that contains:
+ string columns with whitespace, case variation, delimiters, and product codes;
+ numeric columns with positive/negative/decimal values;
+ Date, Datetime, Time, and text date/time columns.
'''

df_orders = pl.DataFrame(
    {
        "order_id": [1001, 1002, 1003, 1004, 1005, 1006],
        "customer": [" Alice ", "bob", "CHARLIE", "Diana", "evan", "FIONA"],
        "region": ["East", "West", "East", "North", "West", "South"],
        "product": ["alpha keyboard", "Beta Mouse", "gamma monitor", "Alpha Dock", "delta cable", "Pro Stand"],
        "product_code": ["KB-001-US", "MS-002-EU", "MN-003-US", "DK-004-AP", "CB-005-EU", "ST-006-US"],
        "comment": [
            "  fast delivery  ",
            "Need invoice",
            "VIP customer",
            " delayed shipment ",
            "",
            None,
        ],
        "quantity": [2, 1, 5, 3, 4, 2],
        "unit_price": [120.125, 80.0, 45.555, 150.49, 20.0, 200.755],
        "discount_rate": [0.10, 0.00, 0.20, 0.15, 0.00, 0.25],
        "profit_change": [12.5, -4.0, 0.0, 31.8, -2.25, 50.0],
        "score": [95.5, 82.0, 67.25, 88.5, 72.0, 91.0],
        "order_date": [
            dt.date(2024, 1, 3),
            dt.date(2024, 1, 5),
            dt.date(2024, 2, 10),
            dt.date(2024, 2, 12),
            dt.date(2024, 3, 1),
            dt.date(2024, 3, 15),
        ],
        "order_time": [
            dt.time(9, 30, 0),
            dt.time(13, 5, 10),
            dt.time(8, 45, 30),
            dt.time(16, 20, 0),
            dt.time(11, 0, 0),
            dt.time(20, 15, 45),
        ],
        "order_dt": [
            dt.datetime(2024, 1, 3, 9, 30, 0),
            dt.datetime(2024, 1, 5, 13, 5, 10),
            dt.datetime(2024, 2, 10, 8, 45, 30),
            dt.datetime(2024, 2, 12, 16, 20, 0),
            dt.datetime(2024, 3, 1, 11, 0, 0),
            dt.datetime(2024, 3, 15, 20, 15, 45),
        ],
        "date_text_iso": [
            "2024-01-03",
            "2024-01-05",
            "2024-02-10",
            "2024-02-12",
            "2024-03-01",
            "2024-03-15",
        ],
        "date_text_long": [
            "03 January 2024",
            "05 January 2024",
            "10 February 2024",
            "12 February 2024",
            "01 March 2024",
            "15 March 2024",
        ],
        "time_text": ["09.30.00", "13.05.10", "08.45.30", "16.20.00", "11.00.00", "20.15.45"],
    }
)

lf_orders = df_orders.lazy()

print(df_orders)
# shape: (6, 17)
# ┌──────────┬──────────┬────────┬──────────────┬──────────────┬───┬─────────────┬─────────────┬─────────────┬───────────┐
# │ order_id ┆ customer ┆ region ┆ product      ┆ product_code ┆ … ┆ order_dt    ┆ date_text_i ┆ date_text_l ┆ time_text │
# │ ---      ┆ ---      ┆ ---    ┆ ---          ┆ ---          ┆   ┆ ---         ┆ so          ┆ ong         ┆ ---       │
# │ i64      ┆ str      ┆ str    ┆ str          ┆ str          ┆   ┆ datetime[μs ┆ ---         ┆ ---         ┆ str       │
# │          ┆          ┆        ┆              ┆              ┆   ┆ ]           ┆ str         ┆ str         ┆           │
# ╞══════════╪══════════╪════════╪══════════════╪══════════════╪═══╪═════════════╪═════════════╪═════════════╪═══════════╡
# │ 1001     ┆  Alice   ┆ East   ┆ alpha        ┆ KB-001-US    ┆ … ┆ 2024-01-03  ┆ 2024-01-03  ┆ 03 January  ┆ 09.30.00  │
# │          ┆          ┆        ┆ keyboard     ┆              ┆   ┆ 09:30:00    ┆             ┆ 2024        ┆           │
# │ 1002     ┆ bob      ┆ West   ┆ Beta Mouse   ┆ MS-002-EU    ┆ … ┆ 2024-01-05  ┆ 2024-01-05  ┆ 05 January  ┆ 13.05.10  │
# │          ┆          ┆        ┆              ┆              ┆   ┆ 13:05:10    ┆             ┆ 2024        ┆           │
# │ 1003     ┆ CHARLIE  ┆ East   ┆ gamma        ┆ MN-003-US    ┆ … ┆ 2024-02-10  ┆ 2024-02-10  ┆ 10 February ┆ 08.45.30  │
# │          ┆          ┆        ┆ monitor      ┆              ┆   ┆ 08:45:30    ┆             ┆ 2024        ┆           │
# │ 1004     ┆ Diana    ┆ North  ┆ Alpha Dock   ┆ DK-004-AP    ┆ … ┆ 2024-02-12  ┆ 2024-02-12  ┆ 12 February ┆ 16.20.00  │
# │          ┆          ┆        ┆              ┆              ┆   ┆ 16:20:00    ┆             ┆ 2024        ┆           │
# │ 1005     ┆ evan     ┆ West   ┆ delta cable  ┆ CB-005-EU    ┆ … ┆ 2024-03-01  ┆ 2024-03-01  ┆ 01 March    ┆ 11.00.00  │
# │          ┆          ┆        ┆              ┆              ┆   ┆ 11:00:00    ┆             ┆ 2024        ┆           │
# │ 1006     ┆ FIONA    ┆ South  ┆ Pro Stand    ┆ ST-006-US    ┆ … ┆ 2024-03-15  ┆ 2024-03-15  ┆ 15 March    ┆ 20.15.45  │
# │          ┆          ┆        ┆              ┆              ┆   ┆ 20:15:45    ┆             ┆ 2024        ┆           │
# └──────────┴──────────┴────────┴──────────────┴──────────────┴───┴─────────────┴─────────────┴─────────────┴───────────┘

print(df_orders.schema)
# Schema({'order_id': Int64, 'customer': String, 'region': String, 'product': String, 'product_code': String, 'comment': String, 'quantity': Int64, 'unit_price': Float64, 'discount_rate': Float64, 'profit_change': Float64, 'score': Float64, 'order_date': Date, 'order_time': Time, 'order_dt': Datetime(time_unit='us', time_zone=None), 'date_text_iso': String, 'date_text_long': String, 'time_text': String})


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. Parse strings into dates/times -----------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
SQL string-to-temporal functions:
+ DATE(text)
+ DATE(text, format)
+ STRPTIME(text, format)
+ TIMESTAMP(text)
+ TIMESTAMP(text, format)
+ DATE 'yyyy-mm-dd' typed literal
+ TIMESTAMP 'yyyy-mm-dd hh:mm:ss' typed literal

Notes:
+ DATE(...) returns Date.
+ STRPTIME(...) and TIMESTAMP(...) return Datetime.
+ The format strings follow chrono/strftime-style patterns.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        date_text_iso,
        date_text_long,
        time_text,
        DATE(date_text_iso) AS parsed_iso_date,
        DATE(date_text_long, '%d %B %Y') AS parsed_long_date,
        STRPTIME(date_text_iso || ' ' || time_text, '%Y-%m-%d %H.%M.%S') AS parsed_datetime,
        DATE '2024-01-01' AS typed_date_literal,
        TIMESTAMP '2024-01-01 12:30:45' AS typed_timestamp_literal
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 9)
# ┌──────────┬─────────────┬─────────────┬───────────┬─────────────┬─────────────┬─────────────┬────────────┬────────────┐
# │ order_id ┆ date_text_i ┆ date_text_l ┆ time_text ┆ parsed_iso_ ┆ parsed_long ┆ parsed_date ┆ typed_date ┆ typed_time │
# │ ---      ┆ so          ┆ ong         ┆ ---       ┆ date        ┆ _date       ┆ time        ┆ _literal   ┆ stamp_lite │
# │ i64      ┆ ---         ┆ ---         ┆ str       ┆ ---         ┆ ---         ┆ ---         ┆ ---        ┆ ral        │
# │          ┆ str         ┆ str         ┆           ┆ date        ┆ date        ┆ datetime[μs ┆ date       ┆ ---        │
# │          ┆             ┆             ┆           ┆             ┆             ┆ ]           ┆            ┆ datetime[μ │
# │          ┆             ┆             ┆           ┆             ┆             ┆             ┆            ┆ s]         │
# ╞══════════╪═════════════╪═════════════╪═══════════╪═════════════╪═════════════╪═════════════╪════════════╪════════════╡
# │ 1001     ┆ 2024-01-03  ┆ 03 January  ┆ 09.30.00  ┆ 2024-01-03  ┆ 2024-01-03  ┆ 2024-01-03  ┆ 2024-01-01 ┆ 2024-01-01 │
# │          ┆             ┆ 2024        ┆           ┆             ┆             ┆ 09:30:00    ┆            ┆ 12:30:45   │
# │ 1002     ┆ 2024-01-05  ┆ 05 January  ┆ 13.05.10  ┆ 2024-01-05  ┆ 2024-01-05  ┆ 2024-01-05  ┆ 2024-01-01 ┆ 2024-01-01 │
# │          ┆             ┆ 2024        ┆           ┆             ┆             ┆ 13:05:10    ┆            ┆ 12:30:45   │
# │ 1003     ┆ 2024-02-10  ┆ 10 February ┆ 08.45.30  ┆ 2024-02-10  ┆ 2024-02-10  ┆ 2024-02-10  ┆ 2024-01-01 ┆ 2024-01-01 │
# │          ┆             ┆ 2024        ┆           ┆             ┆             ┆ 08:45:30    ┆            ┆ 12:30:45   │
# │ 1004     ┆ 2024-02-12  ┆ 12 February ┆ 16.20.00  ┆ 2024-02-12  ┆ 2024-02-12  ┆ 2024-02-12  ┆ 2024-01-01 ┆ 2024-01-01 │
# │          ┆             ┆ 2024        ┆           ┆             ┆             ┆ 16:20:00    ┆            ┆ 12:30:45   │
# │ 1005     ┆ 2024-03-01  ┆ 01 March    ┆ 11.00.00  ┆ 2024-03-01  ┆ 2024-03-01  ┆ 2024-03-01  ┆ 2024-01-01 ┆ 2024-01-01 │
# │          ┆             ┆ 2024        ┆           ┆             ┆             ┆ 11:00:00    ┆            ┆ 12:30:45   │
# │ 1006     ┆ 2024-03-15  ┆ 15 March    ┆ 20.15.45  ┆ 2024-03-15  ┆ 2024-03-15  ┆ 2024-03-15  ┆ 2024-01-01 ┆ 2024-01-01 │
# │          ┆             ┆ 2024        ┆           ┆             ┆             ┆ 20:15:45    ┆            ┆ 12:30:45   │
# └──────────┴─────────────┴─────────────┴───────────┴─────────────┴─────────────┴─────────────┴────────────┴────────────┘

out_native = lf_orders.select(
    "order_id",
    "date_text_iso",
    "date_text_long",
    "time_text",
    c("date_text_iso").str.to_date().alias("parsed_iso_date"),
    c("date_text_long").str.strptime(pl.Date, "%d %B %Y").alias("parsed_long_date"),
    pl.concat_str(c("date_text_iso"), pl.lit(" "), c("time_text")).str.strptime(pl.Datetime, "%Y-%m-%d %H.%M.%S").alias("parsed_datetime"),
    pl.lit(dt.date(2024, 1, 1)).alias("typed_date_literal"),
    pl.lit(dt.datetime(2024, 1, 1, 12, 30, 45)).alias("typed_timestamp_literal"),
)
print(out_native.collect())


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 2. Extract date/time parts ------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
Polars SQL supports two styles for extracting temporal parts:

1. DATE_PART('part', temporal_column)
2. EXTRACT(part FROM temporal_column)

Common parts:
+ year, quarter, month, day
+ hour, minute, second
+ week / isoweek
+ dayofweek / dow / weekday       -> Sunday=0 to Saturday=6
+ isodow                          -> Monday=1 to Sunday=7
+ epoch                           -> seconds since Unix epoch
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        order_date,
        order_dt,
        DATE_PART('year', order_dt) AS year_part,
        DATE_PART('month', order_dt) AS month_part,
        DATE_PART('day', order_dt) AS day_part,
        DATE_PART('hour', order_dt) AS hour_part,
        DATE_PART('minute', order_dt) AS minute_part,
        DATE_PART('isodow', order_dt) AS iso_weekday,
        EXTRACT(quarter FROM order_date) AS quarter_part,
        EXTRACT(week FROM order_date) AS iso_week
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 11)
# ┌──────────┬────────────┬─────────────┬───────────┬────────────┬───┬─────────────┬─────────────┬────────────┬──────────┐
# │ order_id ┆ order_date ┆ order_dt    ┆ year_part ┆ month_part ┆ … ┆ minute_part ┆ iso_weekday ┆ quarter_pa ┆ iso_week │
# │ ---      ┆ ---        ┆ ---         ┆ ---       ┆ ---        ┆   ┆ ---         ┆ ---         ┆ rt         ┆ ---      │
# │ i64      ┆ date       ┆ datetime[μs ┆ i32       ┆ i8         ┆   ┆ i8          ┆ i8          ┆ ---        ┆ i8       │
# │          ┆            ┆ ]           ┆           ┆            ┆   ┆             ┆             ┆ i8         ┆          │
# ╞══════════╪════════════╪═════════════╪═══════════╪════════════╪═══╪═════════════╪═════════════╪════════════╪══════════╡
# │ 1001     ┆ 2024-01-03 ┆ 2024-01-03  ┆ 2024      ┆ 1          ┆ … ┆ 30          ┆ 3           ┆ 1          ┆ 1        │
# │          ┆            ┆ 09:30:00    ┆           ┆            ┆   ┆             ┆             ┆            ┆          │
# │ 1002     ┆ 2024-01-05 ┆ 2024-01-05  ┆ 2024      ┆ 1          ┆ … ┆ 5           ┆ 5           ┆ 1          ┆ 1        │
# │          ┆            ┆ 13:05:10    ┆           ┆            ┆   ┆             ┆             ┆            ┆          │
# │ 1003     ┆ 2024-02-10 ┆ 2024-02-10  ┆ 2024      ┆ 2          ┆ … ┆ 45          ┆ 6           ┆ 1          ┆ 6        │
# │          ┆            ┆ 08:45:30    ┆           ┆            ┆   ┆             ┆             ┆            ┆          │
# │ 1004     ┆ 2024-02-12 ┆ 2024-02-12  ┆ 2024      ┆ 2          ┆ … ┆ 20          ┆ 1           ┆ 1          ┆ 7        │
# │          ┆            ┆ 16:20:00    ┆           ┆            ┆   ┆             ┆             ┆            ┆          │
# │ 1005     ┆ 2024-03-01 ┆ 2024-03-01  ┆ 2024      ┆ 3          ┆ … ┆ 0           ┆ 5           ┆ 1          ┆ 9        │
# │          ┆            ┆ 11:00:00    ┆           ┆            ┆   ┆             ┆             ┆            ┆          │
# │ 1006     ┆ 2024-03-15 ┆ 2024-03-15  ┆ 2024      ┆ 3          ┆ … ┆ 15          ┆ 5           ┆ 1          ┆ 11       │
# │          ┆            ┆ 20:15:45    ┆           ┆            ┆   ┆             ┆             ┆            ┆          │
# └──────────┴────────────┴─────────────┴───────────┴────────────┴───┴─────────────┴─────────────┴────────────┴──────────┘

out_native = lf_orders.select(
    "order_id",
    "order_date",
    "order_dt",
    c("order_dt").dt.year().alias("year_part"),
    c("order_dt").dt.month().alias("month_part"),
    c("order_dt").dt.day().alias("day_part"),
    c("order_dt").dt.hour().alias("hour_part"),
    c("order_dt").dt.minute().alias("minute_part"),
    c("order_dt").dt.weekday().alias("iso_weekday"),
    c("order_date").dt.quarter().alias("quarter_part"),
    c("order_date").dt.week().alias("iso_week"),
)
print(out_native.collect())


#-------------------------------------------------------------------------------------------------------------#
#------------------------------------- 3. Format temporal values as strings ----------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
STRFTIME(temporal_column, format) formats Date/Datetime/Time values as strings.

Native Polars equivalent:
    c("order_dt").dt.strftime(format)
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        order_date,
        order_time,
        order_dt,
        STRFTIME(order_date, '%Y-%m') AS year_month,
        STRFTIME(order_date, '%B %d, %Y') AS pretty_date,
        STRFTIME(order_time, '%H:%M:%S') AS pretty_time,
        STRFTIME(order_dt, '%Y-%m-%d %H:%M') AS pretty_datetime
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 8)
# ┌──────────┬────────────┬────────────┬──────────────────┬────────────┬─────────────────┬─────────────┬─────────────────┐
# │ order_id ┆ order_date ┆ order_time ┆ order_dt         ┆ year_month ┆ pretty_date     ┆ pretty_time ┆ pretty_datetime │
# │ ---      ┆ ---        ┆ ---        ┆ ---              ┆ ---        ┆ ---             ┆ ---         ┆ ---             │
# │ i64      ┆ date       ┆ time       ┆ datetime[μs]     ┆ str        ┆ str             ┆ str         ┆ str             │
# ╞══════════╪════════════╪════════════╪══════════════════╪════════════╪═════════════════╪═════════════╪═════════════════╡
# │ 1001     ┆ 2024-01-03 ┆ 09:30:00   ┆ 2024-01-03       ┆ 2024-01    ┆ January 03,     ┆ 09:30:00    ┆ 2024-01-03      │
# │          ┆            ┆            ┆ 09:30:00         ┆            ┆ 2024            ┆             ┆ 09:30           │
# │ 1002     ┆ 2024-01-05 ┆ 13:05:10   ┆ 2024-01-05       ┆ 2024-01    ┆ January 05,     ┆ 13:05:10    ┆ 2024-01-05      │
# │          ┆            ┆            ┆ 13:05:10         ┆            ┆ 2024            ┆             ┆ 13:05           │
# │ 1003     ┆ 2024-02-10 ┆ 08:45:30   ┆ 2024-02-10       ┆ 2024-02    ┆ February 10,    ┆ 08:45:30    ┆ 2024-02-10      │
# │          ┆            ┆            ┆ 08:45:30         ┆            ┆ 2024            ┆             ┆ 08:45           │
# │ 1004     ┆ 2024-02-12 ┆ 16:20:00   ┆ 2024-02-12       ┆ 2024-02    ┆ February 12,    ┆ 16:20:00    ┆ 2024-02-12      │
# │          ┆            ┆            ┆ 16:20:00         ┆            ┆ 2024            ┆             ┆ 16:20           │
# │ 1005     ┆ 2024-03-01 ┆ 11:00:00   ┆ 2024-03-01       ┆ 2024-03    ┆ March 01, 2024  ┆ 11:00:00    ┆ 2024-03-01      │
# │          ┆            ┆            ┆ 11:00:00         ┆            ┆                 ┆             ┆ 11:00           │
# │ 1006     ┆ 2024-03-15 ┆ 20:15:45   ┆ 2024-03-15       ┆ 2024-03    ┆ March 15, 2024  ┆ 20:15:45    ┆ 2024-03-15      │
# │          ┆            ┆            ┆ 20:15:45         ┆            ┆                 ┆             ┆ 20:15           │
# └──────────┴────────────┴────────────┴──────────────────┴────────────┴─────────────────┴─────────────┴─────────────────┘

out_native = lf_orders.select(
    "order_id",
    "order_date",
    "order_time",
    "order_dt",
    c("order_date").dt.strftime("%Y-%m").alias("year_month"),
    c("order_date").dt.strftime("%B %d, %Y").alias("pretty_date"),
    c("order_time").dt.strftime("%H:%M:%S").alias("pretty_time"),
    c("order_dt").dt.strftime("%Y-%m-%d %H:%M").alias("pretty_datetime"),
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 4. Quick map ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Temporal:
    DATE(text)                  -> c("text").str.to_date()
    STRPTIME(text, fmt)         -> c("text").str.strptime(pl.Datetime, fmt)
    DATE_PART('year', dt)       -> c("dt").dt.year()
    EXTRACT(month FROM dt)      -> c("dt").dt.month()
    STRFTIME(dt, fmt)           -> c("dt").dt.strftime(fmt)
'''
