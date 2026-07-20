# FILE VERSION: 07_sql_functions_string_numeric_datetime_v1
'''
Polars SQL functions: string, numeric/math, and datetime functions.

This file continues the Polars SQL mini-guide after:
    04_sql_select_from_alias_identifiers.py
    05_sql_where_filter_predicates.py
    06_sql_expressions_cast_case.py

The goal is NOT to list every SQL function one-by-one.
Instead, this file shows practical groups of functions and compares them with
native Polars expressions.

Main ideas:
1. SQL functions are used inside SELECT, WHERE, GROUP BY, ORDER BY, etc.
2. String functions cover case conversion, trimming, length, substring, replacement,
   regex tests, concatenation, splitting, and string-to-date/time parsing.
3. Numeric functions cover rounding, absolute value, sign, integer division,
   modulo/remainder, powers, roots, logs, and constants like PI().
4. Temporal functions cover extracting parts from Date/Datetime values and formatting
   Date/Datetime/Time values back to strings.
5. In native Polars, the equivalents usually live under:
      + c("name").str....
      + c("value").round(), .abs(), .sqrt(), .log(), ...
      + c("date").dt....

Important Polars SQL notes:
+ Frame-level .sql(...) registers the frame as the SQL table named self.
+ LazyFrame.sql(...) returns a LazyFrame, so call .collect() to materialize.
+ SQL functions are not always named exactly the same as native Polars expression methods.
+ Some string positions in SQL are 1-indexed, such as SUBSTR(..., start, ...) and SPLIT_PART(..., n).
+ DATE_PART('dayofweek', ...) uses Sunday=0 to Saturday=6, while DATE_PART('isodow', ...)
  uses Monday=1 to Sunday=7.
'''

import datetime as dt

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(20)
pl.Config.set_tbl_cols(24)
pl.Config.set_float_precision(4)
pl.Config.set_tbl_width_chars(160)


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
print(df_orders.schema)


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. String case functions -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Common SQL string case functions:
+ LOWER(expr)
+ UPPER(expr)
+ INITCAP(expr)

Native Polars equivalents:
+ c("customer").str.to_lowercase()
+ c("customer").str.to_uppercase()
+ c("customer").str.to_titlecase()
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        customer,
        LOWER(customer) AS customer_lower,
        UPPER(customer) AS customer_upper,
        INITCAP(customer) AS customer_title
    FROM self
    """
)

print(out_sql.collect())

out_native = lf_orders.select(
    "order_id",
    "customer",
    c("customer").str.to_lowercase().alias("customer_lower"),
    c("customer").str.to_uppercase().alias("customer_upper"),
    c("customer").str.to_titlecase().alias("customer_title"),
)

print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------- 2. Trimming and padding strings ---------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Common SQL whitespace/string cleanup functions:
+ TRIM(expr)
+ LTRIM(expr)
+ RTRIM(expr)
+ TRIM(LEADING char FROM expr)
+ TRIM(TRAILING char FROM expr)
+ LPAD(expr, length, fill)
+ RPAD(expr, length, fill)

Native Polars equivalents use the .str namespace.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        comment,
        TRIM(comment) AS comment_trimmed,
        LTRIM(comment) AS comment_left_trimmed,
        RTRIM(comment) AS comment_right_trimmed,
        LPAD(region, 8, '.') AS region_left_padded,
        RPAD(region, 8, '.') AS region_right_padded
    FROM self
    """
)

print(out_sql.collect())

out_native = lf_orders.select(
    "order_id",
    "comment",
    c("comment").str.strip_chars().alias("comment_trimmed"),
    c("comment").str.strip_chars_start().alias("comment_left_trimmed"),
    c("comment").str.strip_chars_end().alias("comment_right_trimmed"),
    c("region").str.pad_start(8, ".").alias("region_left_padded"),
    c("region").str.pad_end(8, ".").alias("region_right_padded"),
)

print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------- 3. String length, byte length, and bit length -------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
String length functions:
+ LENGTH(expr)       -> character length
+ OCTET_LENGTH(expr) -> byte length
+ BIT_LENGTH(expr)   -> bit length

For ASCII text, byte length is usually the same as character length.
For non-ASCII text, byte length can be larger than character length.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        product,
        LENGTH(product) AS n_chars,
        OCTET_LENGTH(product) AS n_bytes,
        BIT_LENGTH(product) AS n_bits
    FROM self
    """
)

print(out_sql.collect())

out_native = lf_orders.select(
    "order_id",
    "product",
    c("product").str.len_chars().alias("n_chars"),
    c("product").str.len_bytes().alias("n_bytes"),
    (c("product").str.len_bytes() * 8).alias("n_bits"),
)

print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 4. Substrings and positions --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Useful SQL substring/location functions:
+ LEFT(expr, n)
+ RIGHT(expr, n)
+ SUBSTR(expr, start, length)
+ SUBSTRING(expr FROM start FOR length)
+ STRPOS(expr, substring)
+ POSITION(substring IN expr)

Important:
+ SQL SUBSTR/SUBSTRING start positions are 1-indexed.
+ STRPOS returns 1-indexed positions; 0 means not found.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        product_code,
        LEFT(product_code, 2) AS code_prefix,
        RIGHT(product_code, 2) AS country_code,
        SUBSTR(product_code, 4, 3) AS middle_digits,
        SUBSTRING(product_code FROM 4 FOR 3) AS middle_digits_alt,
        STRPOS(product, 'a') AS first_a_position
    FROM self
    """
)

print(out_sql.collect())

out_native = lf_orders.select(
    "order_id",
    "product_code",
    c("product_code").str.slice(0, 2).alias("code_prefix"),
    c("product_code").str.tail(2).alias("country_code"),
    c("product_code").str.slice(3, 3).alias("middle_digits"),
    c("product_code").str.slice(3, 3).alias("middle_digits_alt"),
    # Native Polars string positions are usually 0-indexed; add 1 for SQL-like positions.
    (c("product").str.find("a") + 1).fill_null(0).alias("first_a_position"),
)

print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 5. Replace, regex, starts/ends with -------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Useful SQL string predicates/transforms:
+ REPLACE(expr, old, new)
+ STARTS_WITH(expr, prefix)
+ ENDS_WITH(expr, suffix)
+ REGEXP_LIKE(expr, pattern)

REGEXP_LIKE is useful in SELECT as a boolean computed column, not only inside WHERE.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        product,
        REPLACE(product, ' ', '_') AS product_underscore,
        STARTS_WITH(LOWER(product), 'alpha') AS starts_alpha,
        ENDS_WITH(product_code, 'US') AS ships_to_us,
        REGEXP_LIKE(product_code, '^[A-Z]{2}-[0-9]{3}-[A-Z]{2}$') AS valid_code_pattern
    FROM self
    """
)

print(out_sql.collect())

out_native = lf_orders.select(
    "order_id",
    "product",
    c("product").str.replace_all(" ", "_").alias("product_underscore"),
    c("product").str.to_lowercase().str.starts_with("alpha").alias("starts_alpha"),
    c("product_code").str.ends_with("US").alias("ships_to_us"),
    c("product_code").str.contains(r"^[A-Z]{2}-[0-9]{3}-[A-Z]{2}$").alias("valid_code_pattern"),
)

print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 6. Concatenating strings ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Common SQL string concatenation patterns:
+ expr || expr
+ CONCAT(expr1, expr2, ...)
+ CONCAT_WS(separator, expr1, expr2, ...)

CONCAT_WS is convenient when you want a separator between pieces.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        customer,
        region,
        TRIM(customer) || ' from ' || region AS customer_region_text,
        CONCAT(product_code, ': ', product) AS product_label,
        CONCAT_WS(' / ', region, product_code, status_text) AS route_label
    FROM (
        SELECT
            *,
            CASE WHEN discount_rate > 0 THEN 'discounted' ELSE 'regular' END AS status_text
        FROM self
    )
    """
)

print(out_sql.collect())

out_native = (
    lf_orders
    .with_columns(
        pl.when(c("discount_rate") > 0)
        .then(pl.lit("discounted"))
        .otherwise(pl.lit("regular"))
        .alias("status_text")
    )
    .select(
        "order_id",
        "customer",
        "region",
        pl.concat_str(c("customer").str.strip_chars(), pl.lit(" from "), c("region")).alias("customer_region_text"),
        pl.concat_str(c("product_code"), pl.lit(": "), c("product")).alias("product_label"),
        pl.concat_str(c("region"), c("product_code"), c("status_text"), separator=" / ").alias("route_label"),
    )
)

print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 7. Splitting strings ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Useful SQL splitting functions:
+ SPLIT_PART(expr, delimiter, n)
+ STRING_TO_ARRAY(expr, delimiter)

Important:
+ SPLIT_PART(..., n) is 1-indexed.
+ STRING_TO_ARRAY returns a List/String column in Polars.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        product_code,
        SPLIT_PART(product_code, '-', 1) AS category_code,
        SPLIT_PART(product_code, '-', 2) AS numeric_code,
        SPLIT_PART(product_code, '-', 3) AS market_code,
        STRING_TO_ARRAY(product_code, '-') AS code_parts
    FROM self
    """
)

print(out_sql.collect())

out_native = lf_orders.select(
    "order_id",
    "product_code",
    c("product_code").str.split("-").list.get(0).alias("category_code"),
    c("product_code").str.split("-").list.get(1).alias("numeric_code"),
    c("product_code").str.split("-").list.get(2).alias("market_code"),
    c("product_code").str.split("-").alias("code_parts"),
)

print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 8. Numeric rounding functions ---------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
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

out_native = lf_orders.select(
    "order_id",
    "unit_price",
    c("unit_price").round(0).alias("price_round_0"),
    c("unit_price").round(2).alias("price_round_2"),
    c("unit_price").ceil().alias("price_ceil"),
    c("unit_price").floor().alias("price_floor"),
    c("unit_price").trunc().alias("price_trunc_0"),
    c("unit_price").round(1, mode="towards_zero").alias("price_trunc_1"),
)

print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 9. Numeric sign, absolute value, modulo --------------------------------#
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


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 10. Powers, roots, logs, PI ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
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


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 11. Parse strings into dates/times -----------------------------------#
#--------------------------------------------------------------------------------------------------------------#
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

out_native = lf_orders.select(
    "order_id",
    "date_text_iso",
    "date_text_long",
    "time_text",
    c("date_text_iso").str.to_date().alias("parsed_iso_date"),
    c("date_text_long").str.strptime(pl.Date, "%d %B %Y").alias("parsed_long_date"),
    pl.concat_str(c("date_text_iso"), pl.lit(" "), c("time_text"))
    .str.strptime(pl.Datetime, "%Y-%m-%d %H.%M.%S")
    .alias("parsed_datetime"),
    pl.lit(dt.date(2024, 1, 1)).alias("typed_date_literal"),
    pl.lit(dt.datetime(2024, 1, 1, 12, 30, 45)).alias("typed_timestamp_literal"),
)

print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 12. Extract date/time parts ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
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


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 13. Format temporal values as strings ----------------------------------#
#--------------------------------------------------------------------------------------------------------------#
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
#-------------------------------- 14. Use functions inside WHERE and ORDER BY --------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
SQL functions are not limited to SELECT output columns.
They can also appear inside WHERE, ORDER BY, GROUP BY, HAVING, etc.

Example:
+ Filter products whose lowercased name starts with 'alpha'.
+ Sort by rounded gross sales.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        product,
        quantity,
        unit_price,
        ROUND(quantity * unit_price, 2) AS gross_sales
    FROM self
    WHERE STARTS_WITH(LOWER(product), 'alpha')
       OR DATE_PART('month', order_date) = 3
    ORDER BY ROUND(quantity * unit_price, 2) DESC
    """
)

print(out_sql.collect())

out_native = (
    lf_orders
    .filter(
        c("product").str.to_lowercase().str.starts_with("alpha")
        | (c("order_date").dt.month() == 3)
    )
    .select(
        "order_id",
        "product",
        "quantity",
        "unit_price",
        (c("quantity") * c("unit_price")).round(2).alias("gross_sales"),
    )
    .sort("gross_sales", descending=True)
)

print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 15. SQLContext example -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The same function syntax works through SQLContext when the table has a real name.
This is useful when your SQL query combines multiple registered tables.
'''

ctx = pl.SQLContext(orders=lf_orders)

out_sql = ctx.execute(
    """
    SELECT
        order_id,
        INITCAP(TRIM(customer)) AS clean_customer,
        product_code,
        SPLIT_PART(product_code, '-', 1) AS category_code,
        ROUND(quantity * unit_price, 2) AS gross_sales,
        DATE_PART('month', order_date) AS order_month
    FROM orders
    WHERE REGEXP_LIKE(product_code, 'US$')
    ORDER BY gross_sales DESC
    """
)

print(out_sql.collect())


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 16. Quick map ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Quick SQL -> native Polars map:

String:
    LOWER(x)                    -> c("x").str.to_lowercase()
    UPPER(x)                    -> c("x").str.to_uppercase()
    INITCAP(x)                  -> c("x").str.to_titlecase()
    TRIM(x)                     -> c("x").str.strip_chars()
    LENGTH(x)                   -> c("x").str.len_chars()
    OCTET_LENGTH(x)             -> c("x").str.len_bytes()
    LEFT(x, n)                  -> c("x").str.slice(0, n)
    RIGHT(x, n)                 -> c("x").str.tail(n)
    REPLACE(x, old, new)        -> c("x").str.replace_all(old, new)
    STARTS_WITH(x, prefix)      -> c("x").str.starts_with(prefix)
    ENDS_WITH(x, suffix)        -> c("x").str.ends_with(suffix)
    REGEXP_LIKE(x, pattern)     -> c("x").str.contains(pattern)
    STRING_TO_ARRAY(x, delim)   -> c("x").str.split(delim)

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

Temporal:
    DATE(text)                  -> c("text").str.to_date()
    STRPTIME(text, fmt)         -> c("text").str.strptime(pl.Datetime, fmt)
    DATE_PART('year', dt)       -> c("dt").dt.year()
    EXTRACT(month FROM dt)      -> c("dt").dt.month()
    STRFTIME(dt, fmt)           -> c("dt").dt.strftime(fmt)
'''
