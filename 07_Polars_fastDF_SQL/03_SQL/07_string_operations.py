'''
Main ideas:
# String operations cover case conversion, trimming, length, substring, replacement,
   regex tests, concatenation, splitting, and string-to-date/time parsing.

# In native Polars, the equivalents usually live under: c("name").str....


Important Polars SQL notes:
+ Frame-level .sql(...) registers the frame as the SQL table named self.
+ LazyFrame.sql(...) returns a LazyFrame, so call .collect() to materialize.
+ SQL functions are not always named exactly the same as native Polars expression methods.
+ Some string positions in SQL are 1-indexed, such as SUBSTR(..., start, ...) and SPLIT_PART(..., n).
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


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. String case functions -------------------------------------------#
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
# shape: (6, 5)
# ┌──────────┬──────────┬────────────────┬────────────────┬────────────────┐
# │ order_id ┆ customer ┆ customer_lower ┆ customer_upper ┆ customer_title │
# │ ---      ┆ ---      ┆ ---            ┆ ---            ┆ ---            │
# │ i64      ┆ str      ┆ str            ┆ str            ┆ str            │
# ╞══════════╪══════════╪════════════════╪════════════════╪════════════════╡
# │ 1001     ┆  Alice   ┆  alice         ┆  ALICE         ┆  Alice         │
# │ 1002     ┆ bob      ┆ bob            ┆ BOB            ┆ Bob            │
# │ 1003     ┆ CHARLIE  ┆ charlie        ┆ CHARLIE        ┆ Charlie        │
# │ 1004     ┆ Diana    ┆ diana          ┆ DIANA          ┆ Diana          │
# │ 1005     ┆ evan     ┆ evan           ┆ EVAN           ┆ Evan           │
# │ 1006     ┆ FIONA    ┆ fiona          ┆ FIONA          ┆ Fiona          │
# └──────────┴──────────┴────────────────┴────────────────┴────────────────┘

out_native = lf_orders.select(
    "order_id",
    "customer",
    c("customer").str.to_lowercase().alias("customer_lower"),
    c("customer").str.to_uppercase().alias("customer_upper"),
    c("customer").str.to_titlecase().alias("customer_title"),
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. Trimming and padding strings ---------------------------------------#
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
# shape: (6, 7)
# ┌──────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┐
# │ order_id ┆ comment         ┆ comment_trimmed ┆ comment_left_tr ┆ comment_right_t ┆ region_left_pad ┆ region_right_pa │
# │ ---      ┆ ---             ┆ ---             ┆ immed           ┆ rimmed          ┆ ded             ┆ dded            │
# │ i64      ┆ str             ┆ str             ┆ ---             ┆ ---             ┆ ---             ┆ ---             │
# │          ┆                 ┆                 ┆ str             ┆ str             ┆ str             ┆ str             │
# ╞══════════╪═════════════════╪═════════════════╪═════════════════╪═════════════════╪═════════════════╪═════════════════╡
# │ 1001     ┆ fast delivery   ┆ fast delivery   ┆ fast delivery   ┆   fast delivery ┆ ....East        ┆ East....        │
# │ 1002     ┆ Need invoice    ┆ Need invoice    ┆ Need invoice    ┆ Need invoice    ┆ ....West        ┆ West....        │
# │ 1003     ┆ VIP customer    ┆ VIP customer    ┆ VIP customer    ┆ VIP customer    ┆ ....East        ┆ East....        │
# │ 1004     ┆ delayed         ┆ delayed         ┆ delayed         ┆ delayed         ┆ ...North        ┆ North...        │
# │          ┆ shipment        ┆ shipment        ┆ shipment        ┆ shipment        ┆                 ┆                 │
# │ 1005     ┆                 ┆                 ┆                 ┆                 ┆ ....West        ┆ West....        │
# │ 1006     ┆ null            ┆ null            ┆ null            ┆ null            ┆ ...South        ┆ South...        │
# └──────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┘

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
#-------------------------------- 3. String length, byte length, and bit length -------------------------------#
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
# shape: (6, 5)
# ┌──────────┬────────────────┬─────────┬─────────┬────────┐
# │ order_id ┆ product        ┆ n_chars ┆ n_bytes ┆ n_bits │
# │ ---      ┆ ---            ┆ ---     ┆ ---     ┆ ---    │
# │ i64      ┆ str            ┆ u32     ┆ u32     ┆ u32    │
# ╞══════════╪════════════════╪═════════╪═════════╪════════╡
# │ 1001     ┆ alpha keyboard ┆ 14      ┆ 14      ┆ 112    │
# │ 1002     ┆ Beta Mouse     ┆ 10      ┆ 10      ┆ 80     │
# │ 1003     ┆ gamma monitor  ┆ 13      ┆ 13      ┆ 104    │
# │ 1004     ┆ Alpha Dock     ┆ 10      ┆ 10      ┆ 80     │
# │ 1005     ┆ delta cable    ┆ 11      ┆ 11      ┆ 88     │
# │ 1006     ┆ Pro Stand      ┆ 9       ┆ 9       ┆ 72     │
# └──────────┴────────────────┴─────────┴─────────┴────────┘

out_native = lf_orders.select(
    "order_id",
    "product",
    c("product").str.len_chars().alias("n_chars"),
    c("product").str.len_bytes().alias("n_bytes"),
    (c("product").str.len_bytes() * 8).alias("n_bits"),
)
print(out_native.collect())


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 4. Substrings and positions -------------------------------------------#
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
# shape: (6, 7)
# ┌──────────┬──────────────┬─────────────┬──────────────┬───────────────┬───────────────────┬──────────────────┐
# │ order_id ┆ product_code ┆ code_prefix ┆ country_code ┆ middle_digits ┆ middle_digits_alt ┆ first_a_position │
# │ ---      ┆ ---          ┆ ---         ┆ ---          ┆ ---           ┆ ---               ┆ ---              │
# │ i64      ┆ str          ┆ str         ┆ str          ┆ str           ┆ str               ┆ u32              │
# ╞══════════╪══════════════╪═════════════╪══════════════╪═══════════════╪═══════════════════╪══════════════════╡
# │ 1001     ┆ KB-001-US    ┆ KB          ┆ US           ┆ 001           ┆ 001               ┆ 1                │
# │ 1002     ┆ MS-002-EU    ┆ MS          ┆ EU           ┆ 002           ┆ 002               ┆ 4                │
# │ 1003     ┆ MN-003-US    ┆ MN          ┆ US           ┆ 003           ┆ 003               ┆ 2                │
# │ 1004     ┆ DK-004-AP    ┆ DK          ┆ AP           ┆ 004           ┆ 004               ┆ 5                │
# │ 1005     ┆ CB-005-EU    ┆ CB          ┆ EU           ┆ 005           ┆ 005               ┆ 5                │
# │ 1006     ┆ ST-006-US    ┆ ST          ┆ US           ┆ 006           ┆ 006               ┆ 7                │
# └──────────┴──────────────┴─────────────┴──────────────┴───────────────┴───────────────────┴──────────────────┘

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
#------------------------------------ 5. Replace, regex, starts/ends with -------------------------------------#
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
# shape: (6, 6)
# ┌──────────┬────────────────┬────────────────────┬──────────────┬─────────────┬────────────────────┐
# │ order_id ┆ product        ┆ product_underscore ┆ starts_alpha ┆ ships_to_us ┆ valid_code_pattern │
# │ ---      ┆ ---            ┆ ---                ┆ ---          ┆ ---         ┆ ---                │
# │ i64      ┆ str            ┆ str                ┆ bool         ┆ bool        ┆ bool               │
# ╞══════════╪════════════════╪════════════════════╪══════════════╪═════════════╪════════════════════╡
# │ 1001     ┆ alpha keyboard ┆ alpha_keyboard     ┆ true         ┆ true        ┆ true               │
# │ 1002     ┆ Beta Mouse     ┆ Beta_Mouse         ┆ false        ┆ false       ┆ true               │
# │ 1003     ┆ gamma monitor  ┆ gamma_monitor      ┆ false        ┆ true        ┆ true               │
# │ 1004     ┆ Alpha Dock     ┆ Alpha_Dock         ┆ true         ┆ false       ┆ true               │
# │ 1005     ┆ delta cable    ┆ delta_cable        ┆ false        ┆ false       ┆ true               │
# │ 1006     ┆ Pro Stand      ┆ Pro_Stand          ┆ false        ┆ true        ┆ true               │
# └──────────┴────────────────┴────────────────────┴──────────────┴─────────────┴────────────────────┘

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
#-------------------------------------- 6. Concatenating strings ----------------------------------------------#
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
# shape: (6, 6)
# ┌──────────┬──────────┬────────┬──────────────────────┬───────────────────────────┬────────────────────────────────┐
# │ order_id ┆ customer ┆ region ┆ customer_region_text ┆ product_label             ┆ route_label                    │
# │ ---      ┆ ---      ┆ ---    ┆ ---                  ┆ ---                       ┆ ---                            │
# │ i64      ┆ str      ┆ str    ┆ str                  ┆ str                       ┆ str                            │
# ╞══════════╪══════════╪════════╪══════════════════════╪═══════════════════════════╪════════════════════════════════╡
# │ 1001     ┆  Alice   ┆ East   ┆ Alice from East      ┆ KB-001-US: alpha keyboard ┆ East / KB-001-US / discounted  │
# │ 1002     ┆ bob      ┆ West   ┆ bob from West        ┆ MS-002-EU: Beta Mouse     ┆ West / MS-002-EU / regular     │
# │ 1003     ┆ CHARLIE  ┆ East   ┆ CHARLIE from East    ┆ MN-003-US: gamma monitor  ┆ East / MN-003-US / discounted  │
# │ 1004     ┆ Diana    ┆ North  ┆ Diana from North     ┆ DK-004-AP: Alpha Dock     ┆ North / DK-004-AP / discounted │
# │ 1005     ┆ evan     ┆ West   ┆ evan from West       ┆ CB-005-EU: delta cable    ┆ West / CB-005-EU / regular     │
# │ 1006     ┆ FIONA    ┆ South  ┆ FIONA from South     ┆ ST-006-US: Pro Stand      ┆ South / ST-006-US / discounted │
# └──────────┴──────────┴────────┴──────────────────────┴───────────────────────────┴────────────────────────────────┘

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
#------------------------------------------- 7. Splitting strings ---------------------------------------------#
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
# shape: (6, 6)
# ┌──────────┬──────────────┬───────────────┬──────────────┬─────────────┬─────────────────────┐
# │ order_id ┆ product_code ┆ category_code ┆ numeric_code ┆ market_code ┆ code_parts          │
# │ ---      ┆ ---          ┆ ---           ┆ ---          ┆ ---         ┆ ---                 │
# │ i64      ┆ str          ┆ str           ┆ str          ┆ str         ┆ list[str]           │
# ╞══════════╪══════════════╪═══════════════╪══════════════╪═════════════╪═════════════════════╡
# │ 1001     ┆ KB-001-US    ┆ KB            ┆ 001          ┆ US          ┆ ["KB", "001", "US"] │
# │ 1002     ┆ MS-002-EU    ┆ MS            ┆ 002          ┆ EU          ┆ ["MS", "002", "EU"] │
# │ 1003     ┆ MN-003-US    ┆ MN            ┆ 003          ┆ US          ┆ ["MN", "003", "US"] │
# │ 1004     ┆ DK-004-AP    ┆ DK            ┆ 004          ┆ AP          ┆ ["DK", "004", "AP"] │
# │ 1005     ┆ CB-005-EU    ┆ CB            ┆ 005          ┆ EU          ┆ ["CB", "005", "EU"] │
# │ 1006     ┆ ST-006-US    ┆ ST            ┆ 006          ┆ US          ┆ ["ST", "006", "US"] │
# └──────────┴──────────────┴───────────────┴──────────────┴─────────────┴─────────────────────┘

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
#------------------------------------------------ 8. Quick map ------------------------------------------------#
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
'''
