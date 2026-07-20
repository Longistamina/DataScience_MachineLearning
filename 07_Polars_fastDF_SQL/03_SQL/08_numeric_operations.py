# FILE VERSION: 07_sql_functions_string_numeric_datetime_v1
'''
Main ideas:
# Numeric functions cover rounding, absolute value, sign, integer division,
  modulo/remainder, powers, roots, logs, and constants like PI().

# In native Polars, the equivalents usually live under: c("value").round(), .abs(), .sqrt(), .log(), ...

Important Polars SQL notes:
+ Frame-level .sql(...) registers the frame as the SQL table named self.
+ LazyFrame.sql(...) returns a LazyFrame, so call .collect() to materialize.
+ SQL functions are not always named exactly the same as native Polars expression methods.
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
#--------------------------------------- 1. Numeric rounding functions ---------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
Common SQL numeric rounding functions:
+ ROUND(x)       -> round to 0 decimals
+ ROUND(x, n)    -> round to n decimals
+ CEIL(x)        -> ceiling
+ FLOOR(x)       -> floor
+ TRUNC(x)       -> truncate toward zero
+ TRUNC(x, n)    -> truncate toward zero to n decimals

Note:
+ ROUND in Polars SQL rounds away from zero for .5 cases.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        unit_price,
        ROUND(unit_price) AS price_round_0,
        ROUND(unit_price, 2) AS price_round_2,
        CEIL(unit_price) AS price_ceil,
        FLOOR(unit_price) AS price_floor,
        TRUNC(unit_price) AS price_trunc_0,
        TRUNC(unit_price, 1) AS price_trunc_1
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 8)
# ┌──────────┬────────────┬───────────────┬───────────────┬────────────┬─────────────┬───────────────┬───────────────┐
# │ order_id ┆ unit_price ┆ price_round_0 ┆ price_round_2 ┆ price_ceil ┆ price_floor ┆ price_trunc_0 ┆ price_trunc_1 │
# │ ---      ┆ ---        ┆ ---           ┆ ---           ┆ ---        ┆ ---         ┆ ---           ┆ ---           │
# │ i64      ┆ f64        ┆ f64           ┆ f64           ┆ f64        ┆ f64         ┆ f64           ┆ f64           │
# ╞══════════╪════════════╪═══════════════╪═══════════════╪════════════╪═════════════╪═══════════════╪═══════════════╡
# │ 1001     ┆ 120.1250   ┆ 120.0000      ┆ 120.1200      ┆ 121.0000   ┆ 120.0000    ┆ 120.0000      ┆ 120.1000      │
# │ 1002     ┆ 80.0000    ┆ 80.0000       ┆ 80.0000       ┆ 80.0000    ┆ 80.0000     ┆ 80.0000       ┆ 80.0000       │
# │ 1003     ┆ 45.5550    ┆ 46.0000       ┆ 45.5600       ┆ 46.0000    ┆ 45.0000     ┆ 45.0000       ┆ 45.5000       │
# │ 1004     ┆ 150.4900   ┆ 150.0000      ┆ 150.4900      ┆ 151.0000   ┆ 150.0000    ┆ 150.0000      ┆ 150.4000      │
# │ 1005     ┆ 20.0000    ┆ 20.0000       ┆ 20.0000       ┆ 20.0000    ┆ 20.0000     ┆ 20.0000       ┆ 20.0000       │
# │ 1006     ┆ 200.7550   ┆ 201.0000      ┆ 200.7600      ┆ 201.0000   ┆ 200.0000    ┆ 200.0000      ┆ 200.7000      │
# └──────────┴────────────┴───────────────┴───────────────┴────────────┴─────────────┴───────────────┴───────────────┘

out_native = lf_orders.select(
    "order_id",
    "unit_price",
    c("unit_price").round(0).alias("price_round_0"),
    c("unit_price").round(2).alias("price_round_2"),
    c("unit_price").ceil().alias("price_ceil"),
    c("unit_price").floor().alias("price_floor"),
    #c("unit_price").trunc().alias("price_trunc_0"),
    c("unit_price").round(1, mode="half_away_from_zero").alias("price_trunc_1"),
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 2. Numeric sign, absolute value, modulo ---------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Useful SQL numeric functions:
+ ABS(x)
+ SIGN(x)
+ DIV(x, y)      -> integer quotient
+ MOD(x, y)      -> remainder

These are common for feature engineering and simple numeric classification.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        quantity,
        profit_change,
        ABS(profit_change) AS abs_profit_change,
        SIGN(profit_change) AS profit_direction,
        DIV(quantity, 2) AS quantity_div_2,
        MOD(quantity, 2) AS quantity_mod_2
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 7)
# ┌──────────┬──────────┬───────────────┬───────────────────┬──────────────────┬────────────────┬────────────────┐
# │ order_id ┆ quantity ┆ profit_change ┆ abs_profit_change ┆ profit_direction ┆ quantity_div_2 ┆ quantity_mod_2 │
# │ ---      ┆ ---      ┆ ---           ┆ ---               ┆ ---              ┆ ---            ┆ ---            │
# │ i64      ┆ i64      ┆ f64           ┆ f64               ┆ f64              ┆ i64            ┆ i64            │
# ╞══════════╪══════════╪═══════════════╪═══════════════════╪══════════════════╪════════════════╪════════════════╡
# │ 1001     ┆ 2        ┆ 12.5000       ┆ 12.5000           ┆ 1.0000           ┆ 1              ┆ 0              │
# │ 1002     ┆ 1        ┆ -4.0000       ┆ 4.0000            ┆ -1.0000          ┆ 0              ┆ 1              │
# │ 1003     ┆ 5        ┆ 0.0000        ┆ 0.0000            ┆ 0.0000           ┆ 2              ┆ 1              │
# │ 1004     ┆ 3        ┆ 31.8000       ┆ 31.8000           ┆ 1.0000           ┆ 1              ┆ 1              │
# │ 1005     ┆ 4        ┆ -2.2500       ┆ 2.2500            ┆ -1.0000          ┆ 2              ┆ 0              │
# │ 1006     ┆ 2        ┆ 50.0000       ┆ 50.0000           ┆ 1.0000           ┆ 1              ┆ 0              │
# └──────────┴──────────┴───────────────┴───────────────────┴──────────────────┴────────────────┴────────────────┘

out_native = lf_orders.select(
    "order_id",
    "quantity",
    "profit_change",
    c("profit_change").abs().alias("abs_profit_change"),
    c("profit_change").sign().alias("profit_direction"),
    (c("quantity") // 2).alias("quantity_div_2"),
    (c("quantity") % 2).alias("quantity_mod_2"),
)
print(out_native.collect())


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. Powers, roots, logs, PI ------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
Useful SQL math functions:
+ SQRT(x)
+ CBRT(x)
+ POW(x, exponent) / POWER(x, exponent)
+ EXP(x)
+ LN(x)
+ LOG(x, base)
+ LOG2(x)
+ LOG10(x)
+ LOG1P(x)
+ PI()

Keep the input domain in mind:
+ logs need positive values;
+ square roots need non-negative values.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        quantity,
        score,
        SQRT(score) AS sqrt_score,
        CBRT(score) AS cbrt_score,
        POW(quantity, 2) AS quantity_squared,
        POWER(quantity, 3) AS quantity_cubed,
        LN(score) AS ln_score,
        LOG(score, 10) AS log10_score_via_log,
        LOG10(score) AS log10_score,
        LOG1P(quantity) AS log1p_quantity,
        PI() AS pi_constant
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 12)
# ┌──────────┬──────────┬─────────┬────────────┬────────────┬───┬──────────────┬─────────────┬─────────────┬─────────────┐
# │ order_id ┆ quantity ┆ score   ┆ sqrt_score ┆ cbrt_score ┆ … ┆ log10_score_ ┆ log10_score ┆ log1p_quant ┆ pi_constant │
# │ ---      ┆ ---      ┆ ---     ┆ ---        ┆ ---        ┆   ┆ via_log      ┆ ---         ┆ ity         ┆ ---         │
# │ i64      ┆ i64      ┆ f64     ┆ f64        ┆ f64        ┆   ┆ ---          ┆ f64         ┆ ---         ┆ f64         │
# │          ┆          ┆         ┆            ┆            ┆   ┆ f64          ┆             ┆ f64         ┆             │
# ╞══════════╪══════════╪═════════╪════════════╪════════════╪═══╪══════════════╪═════════════╪═════════════╪═════════════╡
# │ 1001     ┆ 2        ┆ 95.5000 ┆ 9.7724     ┆ 4.5709     ┆ … ┆ 1.9800       ┆ 1.9800      ┆ 1.0986      ┆ 3.1416      │
# │ 1002     ┆ 1        ┆ 82.0000 ┆ 9.0554     ┆ 4.3445     ┆ … ┆ 1.9138       ┆ 1.9138      ┆ 0.6931      ┆ 3.1416      │
# │ 1003     ┆ 5        ┆ 67.2500 ┆ 8.2006     ┆ 4.0666     ┆ … ┆ 1.8277       ┆ 1.8277      ┆ 1.7918      ┆ 3.1416      │
# │ 1004     ┆ 3        ┆ 88.5000 ┆ 9.4074     ┆ 4.4564     ┆ … ┆ 1.9469       ┆ 1.9469      ┆ 1.3863      ┆ 3.1416      │
# │ 1005     ┆ 4        ┆ 72.0000 ┆ 8.4853     ┆ 4.1602     ┆ … ┆ 1.8573       ┆ 1.8573      ┆ 1.6094      ┆ 3.1416      │
# │ 1006     ┆ 2        ┆ 91.0000 ┆ 9.5394     ┆ 4.4979     ┆ … ┆ 1.9590       ┆ 1.9590      ┆ 1.0986      ┆ 3.1416      │
# └──────────┴──────────┴─────────┴────────────┴────────────┴───┴──────────────┴─────────────┴─────────────┴─────────────┘

out_native = lf_orders.select(
    "order_id",
    "quantity",
    "score",
    c("score").sqrt().alias("sqrt_score"),
    c("score").cbrt().alias("cbrt_score"),
    c("quantity").pow(2).alias("quantity_squared"),
    c("quantity").pow(3).alias("quantity_cubed"),
    c("score").log().alias("ln_score"),
    c("score").log(10).alias("log10_score_via_log"),
    c("score").log10().alias("log10_score"),
    c("quantity").log1p().alias("log1p_quantity"),
    pl.lit(3.141592653589793).alias("pi_constant"),
)
print(out_native.collect())


#-------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 4. Quick map ------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
Numeric:
    ABS(x)                      -> c("x").abs()
    ROUND(x, n)                 -> c("x").round(n)
    CEIL(x)                     -> c("x").ceil()
    FLOOR(x)                    -> c("x").floor()
    TRUNC(x)                    -> c("x").trunc() or round(..., mode="towards_zero")
    MOD(x, y)                   -> c("x") % y
    SQRT(x)                     -> c("x").sqrt()
    POW(x, p)                   -> c("x").pow(p)
    LN(x)                       -> c("x").log()
    LOG10(x)                    -> c("x").log10()
'''
