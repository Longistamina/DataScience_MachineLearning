# FILE VERSION: 06_sql_expressions_cast_case_v1
'''
Polars SQL expressions, literals, CAST / TRY_CAST, and CASE expressions.

This file continues the Polars SQL mini-guide after SELECT/FROM and WHERE.
The goal is to show how to write computed columns in SQL, and how those SQL
expressions map back to normal Polars expressions.

Main ideas:
1. SQL expressions in SELECT are similar to Polars expressions inside select().
2. SQL literals such as numbers, strings, booleans, and NULL are broadcast per row.
3. Arithmetic expressions follow SQL/Python-like operator precedence; use parentheses
   when the intended calculation should be explicit.
4. CAST converts data types and errors if conversion is invalid.
5. TRY_CAST converts data types but returns NULL when conversion fails.
6. CASE WHEN is the SQL equivalent of pl.when(...).then(...).otherwise(...).

Important Polars SQL notes:
+ Frame-level .sql(...) registers the frame as the SQL table named self.
+ LazyFrame.sql(...) returns a LazyFrame, so call .collect() to materialize the result.
+ SQL single quotes are for string literals: 'small'.
+ SQL double quotes are for identifiers/column names: "unit price".
+ In native Polars, plain strings in pl.when().then()/otherwise() can be parsed as
  column names, so use pl.lit("text") for string literal outputs.
'''

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(20)
pl.Config.set_tbl_cols(9)
pl.Config.set_float_precision(3)
pl.Config.set_tbl_width_chars(140)


# =========================================================================================
# 0. Setup data
# =========================================================================================
'''
The examples are self-contained so this file can run without external datasets.

We keep both:
+ a LazyFrame, because SQL queries normally fit naturally into lazy pipelines;
+ an eager DataFrame, to show that DataFrame.sql(...) can also be used.
'''

df_orders = pl.DataFrame(
    {
        "order_id": [1001, 1002, 1003, 1004, 1005, 1006],
        "customer": ["Alice", "Bob", "Alice", "Diana", "Evan", "Fiona"],
        "region": ["East", "West", "East", "North", "West", "South"],
        "quantity": [2, 1, 5, 3, 4, 2],
        "unit_price": [120.0, 80.0, 45.0, 150.0, 20.0, 200.0],
        "discount_rate": [0.10, 0.00, 0.20, 0.15, 0.00, 0.25],
        "shipping_fee": [5.0, 7.5, 0.0, 12.0, 4.0, 10.0],
        "status": ["paid", "pending", "paid", "paid", "cancelled", "paid"],
        "is_priority": [True, False, False, True, False, True],
        "promo_code": ["SPRING", None, "VIP", None, "", "VIP"],
        "score_text": ["95.5", "82.0", "bad", "88.5", None, "91.0"],
        "order_date_text": [
            "2024-01-03",
            "2024-01-05",
            "2024-02-10",
            "2024-02-12",
            "2024-03-01",
            "2024-03-15",
        ],
    }
)

lf_orders = df_orders.lazy()

print(df_orders)
# shape: (6, 12)
# ┌──────────┬──────────┬────────┬──────────┬────────────┬───┬─────────────┬────────────┬────────────┬─────────────────┐
# │ order_id ┆ customer ┆ region ┆ quantity ┆ unit_price ┆ … ┆ is_priority ┆ promo_code ┆ score_text ┆ order_date_text │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---        ┆   ┆ ---         ┆ ---        ┆ ---        ┆ ---             │
# │ i64      ┆ str      ┆ str    ┆ i64      ┆ f64        ┆   ┆ bool        ┆ str        ┆ str        ┆ str             │
# ╞══════════╪══════════╪════════╪══════════╪════════════╪═══╪═════════════╪════════════╪════════════╪═════════════════╡
# │ 1001     ┆ Alice    ┆ East   ┆ 2        ┆ 120.000    ┆ … ┆ true        ┆ SPRING     ┆ 95.5       ┆ 2024-01-03      │
# │ 1002     ┆ Bob      ┆ West   ┆ 1        ┆ 80.000     ┆ … ┆ false       ┆ null       ┆ 82.0       ┆ 2024-01-05      │
# │ 1003     ┆ Alice    ┆ East   ┆ 5        ┆ 45.000     ┆ … ┆ false       ┆ VIP        ┆ bad        ┆ 2024-02-10      │
# │ 1004     ┆ Diana    ┆ North  ┆ 3        ┆ 150.000    ┆ … ┆ true        ┆ null       ┆ 88.5       ┆ 2024-02-12      │
# │ 1005     ┆ Evan     ┆ West   ┆ 4        ┆ 20.000     ┆ … ┆ false       ┆            ┆ null       ┆ 2024-03-01      │
# │ 1006     ┆ Fiona    ┆ South  ┆ 2        ┆ 200.000    ┆ … ┆ true        ┆ VIP        ┆ 91.0       ┆ 2024-03-15      │
# └──────────┴──────────┴────────┴──────────┴────────────┴───┴─────────────┴────────────┴────────────┴─────────────────┘

print(df_orders.schema)


# =========================================================================================
# 1. Arithmetic expressions in SELECT
# =========================================================================================
'''
SQL expressions are written directly in the SELECT list.

Native Polars equivalent:
    lf.select((c.quantity * c.unit_price).alias("gross_sales"))

SQL equivalent:
    SELECT quantity * unit_price AS gross_sales FROM self
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        customer,
        quantity,
        unit_price,
        quantity * unit_price AS gross_sales,
        quantity * unit_price * (1 - discount_rate) AS discounted_sales,
        quantity * unit_price * (1 - discount_rate) + shipping_fee AS net_sales
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 7)
# ┌──────────┬──────────┬──────────┬────────────┬─────────────┬──────────────────┬───────────┐
# │ order_id ┆ customer ┆ quantity ┆ unit_price ┆ gross_sales ┆ discounted_sales ┆ net_sales │
# │ ---      ┆ ---      ┆ ---      ┆ ---        ┆ ---         ┆ ---              ┆ ---       │
# │ i64      ┆ str      ┆ i64      ┆ f64        ┆ f64         ┆ f64              ┆ f64       │
# ╞══════════╪══════════╪══════════╪════════════╪═════════════╪══════════════════╪═══════════╡
# │ 1001     ┆ Alice    ┆ 2        ┆ 120.000    ┆ 240.000     ┆ 216.000          ┆ 221.000   │
# │ 1002     ┆ Bob      ┆ 1        ┆ 80.000     ┆ 80.000      ┆ 80.000           ┆ 87.500    │
# │ 1003     ┆ Alice    ┆ 5        ┆ 45.000     ┆ 225.000     ┆ 180.000          ┆ 180.000   │
# │ 1004     ┆ Diana    ┆ 3        ┆ 150.000    ┆ 450.000     ┆ 382.500          ┆ 394.500   │
# │ 1005     ┆ Evan     ┆ 4        ┆ 20.000     ┆ 80.000      ┆ 80.000           ┆ 84.000    │
# │ 1006     ┆ Fiona    ┆ 2        ┆ 200.000    ┆ 400.000     ┆ 300.000          ┆ 310.000   │
# └──────────┴──────────┴──────────┴────────────┴─────────────┴──────────────────┴───────────┘

out_native = lf_orders.select(
    "order_id",
    "customer",
    "quantity",
    "unit_price",
    (c.quantity * c.unit_price).alias("gross_sales"),
    (c.quantity * c.unit_price * (1 - c.discount_rate)).alias("discounted_sales"),
    (c.quantity * c.unit_price * (1 - c.discount_rate) + c.shipping_fee).alias("net_sales"),
)
print(out_native.collect())


# =========================================================================================
# 2. Literal values
# =========================================================================================
'''
SQL literals are constant values.
They are repeated/broadcast for each output row.

Common SQL literals:
+ numeric: 1, 1.5
+ string: 'online'
+ boolean: TRUE, FALSE
+ missing value: NULL

In native Polars, the equivalent is usually pl.lit(...).
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        'online' AS sales_channel,
        1 AS constant_one,
        0.07 AS tax_rate,
        TRUE AS from_sql,
        NULL AS unknown_value
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 6)
# ┌──────────┬───────────────┬──────────────┬──────────┬──────────┬───────────────┐
# │ order_id ┆ sales_channel ┆ constant_one ┆ tax_rate ┆ from_sql ┆ unknown_value │
# │ ---      ┆ ---           ┆ ---          ┆ ---      ┆ ---      ┆ ---           │
# │ i64      ┆ str           ┆ i32          ┆ f64      ┆ bool     ┆ null          │
# ╞══════════╪═══════════════╪══════════════╪══════════╪══════════╪═══════════════╡
# │ 1001     ┆ online        ┆ 1            ┆ 0.070    ┆ true     ┆ null          │
# │ 1002     ┆ online        ┆ 1            ┆ 0.070    ┆ true     ┆ null          │
# │ 1003     ┆ online        ┆ 1            ┆ 0.070    ┆ true     ┆ null          │
# │ 1004     ┆ online        ┆ 1            ┆ 0.070    ┆ true     ┆ null          │
# │ 1005     ┆ online        ┆ 1            ┆ 0.070    ┆ true     ┆ null          │
# │ 1006     ┆ online        ┆ 1            ┆ 0.070    ┆ true     ┆ null          │
# └──────────┴───────────────┴──────────────┴──────────┴──────────┴───────────────┘

out_native = lf_orders.select(
    "order_id",
    pl.lit("online").alias("sales_channel"),
    pl.lit(1).alias("constant_one"),
    pl.lit(0.07).alias("tax_rate"),
    pl.lit(True).alias("from_sql"),
    pl.lit(None).alias("unknown_value"),
)
print(out_native.collect())


# =========================================================================================
# 3. Operator precedence and parentheses
# =========================================================================================
'''
Multiplication and division are evaluated before addition/subtraction.
Use parentheses to make business logic explicit.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        quantity,
        unit_price,
        quantity + 2 * unit_price AS default_precedence,
        (quantity + 2) * unit_price AS explicit_parentheses
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 5)
# ┌──────────┬──────────┬────────────┬────────────────────┬──────────────────────┐
# │ order_id ┆ quantity ┆ unit_price ┆ default_precedence ┆ explicit_parentheses │
# │ ---      ┆ ---      ┆ ---        ┆ ---                ┆ ---                  │
# │ i64      ┆ i64      ┆ f64        ┆ f64                ┆ f64                  │
# ╞══════════╪══════════╪════════════╪════════════════════╪══════════════════════╡
# │ 1001     ┆ 2        ┆ 120.000    ┆ 242.000            ┆ 480.000              │
# │ 1002     ┆ 1        ┆ 80.000     ┆ 161.000            ┆ 240.000              │
# │ 1003     ┆ 5        ┆ 45.000     ┆ 95.000             ┆ 315.000              │
# │ 1004     ┆ 3        ┆ 150.000    ┆ 303.000            ┆ 750.000              │
# │ 1005     ┆ 4        ┆ 20.000     ┆ 44.000             ┆ 120.000              │
# │ 1006     ┆ 2        ┆ 200.000    ┆ 402.000            ┆ 800.000              │
# └──────────┴──────────┴────────────┴────────────────────┴──────────────────────┘

out_native = lf_orders.select(
    "order_id",
    "quantity",
    "unit_price",
    (c.quantity + 2 * c.unit_price).alias("default_precedence"),
    ((c.quantity + 2) * c.unit_price).alias("explicit_parentheses"),
)
print(out_native.collect())


# =========================================================================================
# 4. Boolean expressions as computed output columns
# =========================================================================================
'''
A boolean condition does not have to be used only in WHERE.
It can be selected as a computed boolean column.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        quantity,
        unit_price,
        quantity >= 3 AS is_bulk_order,
        quantity * unit_price >= 200 AS is_high_gross_value,
        status = 'paid' AND is_priority AS paid_priority_order
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 6)
# ┌──────────┬──────────┬────────────┬───────────────┬─────────────────────┬─────────────────────┐
# │ order_id ┆ quantity ┆ unit_price ┆ is_bulk_order ┆ is_high_gross_value ┆ paid_priority_order │
# │ ---      ┆ ---      ┆ ---        ┆ ---           ┆ ---                 ┆ ---                 │
# │ i64      ┆ i64      ┆ f64        ┆ bool          ┆ bool                ┆ bool                │
# ╞══════════╪══════════╪════════════╪═══════════════╪═════════════════════╪═════════════════════╡
# │ 1001     ┆ 2        ┆ 120.000    ┆ false         ┆ true                ┆ true                │
# │ 1002     ┆ 1        ┆ 80.000     ┆ false         ┆ false               ┆ false               │
# │ 1003     ┆ 5        ┆ 45.000     ┆ true          ┆ true                ┆ false               │
# │ 1004     ┆ 3        ┆ 150.000    ┆ true          ┆ true                ┆ true                │
# │ 1005     ┆ 4        ┆ 20.000     ┆ true          ┆ false               ┆ false               │
# │ 1006     ┆ 2        ┆ 200.000    ┆ false         ┆ true                ┆ true                │
# └──────────┴──────────┴────────────┴───────────────┴─────────────────────┴─────────────────────┘

out_native = lf_orders.select(
    "order_id",
    "quantity",
    "unit_price",
    (c.quantity >= 3).alias("is_bulk_order"),
    (c.quantity * c.unit_price >= 200).alias("is_high_gross_value"),
    ((c.status == "paid") & c.is_priority).alias("paid_priority_order"),
)
print(out_native.collect())


# =========================================================================================
# 5. CAST: strict conversion
# =========================================================================================
'''
CAST changes the data type of an expression.

If the conversion is invalid, CAST raises an error.
Therefore, use CAST when you expect the values to be valid.

This example casts:
+ integer quantity      -> floating point
+ ISO date string       -> Date
+ boolean is_priority   -> integer

Polars SQL supports the common CAST(expr AS type) form. It also supports the compact
PostgreSQL-style expr::type syntax, shown in the next section.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        CAST(quantity AS float8) AS quantity_f64,
        CAST(order_date_text AS date) AS order_date,
        CAST(is_priority AS int4) AS priority_as_int
    FROM self
    """
)
print(out_sql.collect())
print(out_sql.collect_schema())
# shape: (6, 4)
# ┌──────────┬──────────────┬────────────┬─────────────────┐
# │ order_id ┆ quantity_f64 ┆ order_date ┆ priority_as_int │
# │ ---      ┆ ---          ┆ ---        ┆ ---             │
# │ i64      ┆ f64          ┆ date       ┆ i32             │
# ╞══════════╪══════════════╪════════════╪═════════════════╡
# │ 1001     ┆ 2.000        ┆ 2024-01-03 ┆ 1               │
# │ 1002     ┆ 1.000        ┆ 2024-01-05 ┆ 0               │
# │ 1003     ┆ 5.000        ┆ 2024-02-10 ┆ 0               │
# │ 1004     ┆ 3.000        ┆ 2024-02-12 ┆ 1               │
# │ 1005     ┆ 4.000        ┆ 2024-03-01 ┆ 0               │
# │ 1006     ┆ 2.000        ┆ 2024-03-15 ┆ 1               │
# └──────────┴──────────────┴────────────┴─────────────────┘

out_native = lf_orders.select(
    "order_id",
    c.quantity.cast(pl.Float64).alias("quantity_f64"),
    c.order_date_text.cast(pl.Date).alias("order_date"),
    c.is_priority.cast(pl.Int32).alias("priority_as_int"),
)
print(out_native.collect())
print(out_native.collect_schema())


# =========================================================================================
# 6. PostgreSQL-style shorthand casts
# =========================================================================================
'''
Polars SQL also supports compact PostgreSQL-style casts:

    expression::type

This is shorter, but CAST(expression AS type) is usually clearer for beginners.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        quantity::float4 AS quantity_f32,
        order_date_text::date AS order_date
    FROM self
    """
)
print(out_sql.collect())
print(out_sql.collect_schema())
# shape: (6, 3)
# ┌──────────┬──────────────┬────────────┐
# │ order_id ┆ quantity_f32 ┆ order_date │
# │ ---      ┆ ---          ┆ ---        │
# │ i64      ┆ f32          ┆ date       │
# ╞══════════╪══════════════╪════════════╡
# │ 1001     ┆ 2.000        ┆ 2024-01-03 │
# │ 1002     ┆ 1.000        ┆ 2024-01-05 │
# │ 1003     ┆ 5.000        ┆ 2024-02-10 │
# │ 1004     ┆ 3.000        ┆ 2024-02-12 │
# │ 1005     ┆ 4.000        ┆ 2024-03-01 │
# │ 1006     ┆ 2.000        ┆ 2024-03-15 │
# └──────────┴──────────────┴────────────┘


# =========================================================================================
# 7. TRY_CAST: safe conversion
# =========================================================================================
'''
TRY_CAST is useful for dirty string data.
If conversion fails, the result is NULL instead of an exception.

In this dataset, score_text contains values such as:
+ "95.5"
+ "bad"
+ None

CAST(score_text AS float8) would fail on "bad".
TRY_CAST(score_text AS float8) returns NULL for invalid rows.

Native Polars equivalent:
    c.score_text.cast(pl.Float64, strict=False)
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        score_text,
        TRY_CAST(score_text AS float8) AS score
    FROM self
    """
)
print(out_sql.collect())
print(out_sql.collect_schema())
# shape: (6, 3)
# ┌──────────┬────────────┬────────┐
# │ order_id ┆ score_text ┆ score  │
# │ ---      ┆ ---        ┆ ---    │
# │ i64      ┆ str        ┆ f64    │
# ╞══════════╪════════════╪════════╡
# │ 1001     ┆ 95.5       ┆ 95.500 │
# │ 1002     ┆ 82.0       ┆ 82.000 │
# │ 1003     ┆ bad        ┆ null   │
# │ 1004     ┆ 88.5       ┆ 88.500 │
# │ 1005     ┆ null       ┆ null   │
# │ 1006     ┆ 91.0       ┆ 91.000 │
# └──────────┴────────────┴────────┘


out_native = lf_orders.select(
    "order_id",
    "score_text",
    c.score_text.cast(pl.Float64, strict=False).alias("score"),
)
print(out_native.collect())
print(out_native.collect_schema())


# =========================================================================================
# 8. Searched CASE WHEN expression
# =========================================================================================
'''
Searched CASE evaluates independent boolean conditions.
This is the SQL equivalent of a pl.when(...).then(...).otherwise(...) chain.

Pattern:
    CASE
      WHEN condition_1 THEN value_1
      WHEN condition_2 THEN value_2
      ELSE value_3
    END AS new_column
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        status,
        quantity * unit_price AS gross_sales,
        CASE
            WHEN status = 'cancelled' THEN 'cancelled'
            WHEN quantity * unit_price >= 400 THEN 'very_large'
            WHEN quantity * unit_price >= 200 THEN 'large'
            ELSE 'regular'
        END AS order_size
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 4)
# ┌──────────┬───────────┬─────────────┬────────────┐
# │ order_id ┆ status    ┆ gross_sales ┆ order_size │
# │ ---      ┆ ---       ┆ ---         ┆ ---        │
# │ i64      ┆ str       ┆ f64         ┆ str        │
# ╞══════════╪═══════════╪═════════════╪════════════╡
# │ 1001     ┆ paid      ┆ 240.000     ┆ large      │
# │ 1002     ┆ pending   ┆ 80.000      ┆ regular    │
# │ 1003     ┆ paid      ┆ 225.000     ┆ large      │
# │ 1004     ┆ paid      ┆ 450.000     ┆ very_large │
# │ 1005     ┆ cancelled ┆ 80.000      ┆ cancelled  │
# │ 1006     ┆ paid      ┆ 400.000     ┆ very_large │
# └──────────┴───────────┴─────────────┴────────────┘

out_native = lf_orders.select(
    "order_id",
    "status",
    (c.quantity * c.unit_price).alias("gross_sales"),
    pl.when(c.status == "cancelled")
    .then(pl.lit("cancelled"))
    .when(c.quantity * c.unit_price >= 400)
    .then(pl.lit("very_large"))
    .when(c.quantity * c.unit_price >= 200)
    .then(pl.lit("large"))
    .otherwise(pl.lit("regular"))
    .alias("order_size"),
)
print(out_native.collect())


# =========================================================================================
# 9. Simple CASE expression
# =========================================================================================
'''
Simple CASE compares one expression against several possible values.

Pattern:
    CASE expression
      WHEN value_1 THEN result_1
      WHEN value_2 THEN result_2
      ELSE result_3
    END

Native Polars equivalent:
Use chained when/then conditions, or use replace(...) for simple value mapping.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        region,
        CASE region
            WHEN 'East' THEN 'eastern_team'
            WHEN 'West' THEN 'western_team'
            WHEN 'North' THEN 'northern_team'
            ELSE 'other_team'
        END AS sales_team
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 3)
# ┌──────────┬────────┬───────────────┐
# │ order_id ┆ region ┆ sales_team    │
# │ ---      ┆ ---    ┆ ---           │
# │ i64      ┆ str    ┆ str           │
# ╞══════════╪════════╪═══════════════╡
# │ 1001     ┆ East   ┆ eastern_team  │
# │ 1002     ┆ West   ┆ western_team  │
# │ 1003     ┆ East   ┆ eastern_team  │
# │ 1004     ┆ North  ┆ northern_team │
# │ 1005     ┆ West   ┆ western_team  │
# │ 1006     ┆ South  ┆ other_team    │
# └──────────┴────────┴───────────────┘

out_native = lf_orders.select(
    "order_id",
    "region",
    c.region.replace(
        {
            "East": "eastern_team",
            "West": "western_team",
            "North": "northern_team",
        },
        default="other_team",
    ).alias("sales_team"),
)
print(out_native.collect())


# =========================================================================================
# 10. CASE without ELSE returns NULL when no match
# =========================================================================================
'''
If CASE has no ELSE, unmatched rows return NULL.
This is useful when you only want to mark some rows and leave all other rows missing.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        promo_code,
        CASE
            WHEN promo_code = 'VIP' THEN 'vip_customer'
        END AS promo_segment
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 3)
# ┌──────────┬────────────┬───────────────┐
# │ order_id ┆ promo_code ┆ promo_segment │
# │ ---      ┆ ---        ┆ ---           │
# │ i64      ┆ str        ┆ str           │
# ╞══════════╪════════════╪═══════════════╡
# │ 1001     ┆ SPRING     ┆ null          │
# │ 1002     ┆ null       ┆ null          │
# │ 1003     ┆ VIP        ┆ vip_customer  │
# │ 1004     ┆ null       ┆ null          │
# │ 1005     ┆            ┆ null          │
# │ 1006     ┆ VIP        ┆ vip_customer  │
# └──────────┴────────────┴───────────────┘

out_native = lf_orders.select(
    "order_id",
    "promo_code",
    pl.when(c.promo_code == "VIP")
    .then(pl.lit("vip_customer"))
    .otherwise(None)
    .alias("promo_segment"),
)
print(out_native.collect())


# =========================================================================================
# 11. Conditional helper functions related to CASE
# =========================================================================================
'''
Polars SQL also supports conditional helper functions.
A later functions-focused SQL file can go deeper, but these are useful here:

+ COALESCE(a, b, c): first non-null value
+ IF(condition, true_value, false_value): compact CASE WHEN
+ IFNULL(value, fallback): fallback if value is NULL
+ NULLIF(a, b): NULL if a == b, otherwise a
+ GREATEST(a, b, ...): row-wise greatest value
+ LEAST(a, b, ...): row-wise smallest value

Note: an empty string '' is not the same as NULL. Use NULLIF(promo_code, '') to turn
empty strings into NULL before COALESCE/IFNULL if that is the desired behavior.
'''

out_sql = lf_orders.sql(
    """
    SELECT
        order_id,
        promo_code,
        COALESCE(NULLIF(promo_code, ''), 'NO_PROMO') AS cleaned_promo_code,
        IF(is_priority, 'priority', 'normal') AS priority_label,
        GREATEST(quantity * unit_price, shipping_fee) AS greatest_amount,
        LEAST(quantity * unit_price, shipping_fee) AS least_amount
    FROM self
    """
)
print(out_sql.collect())
# shape: (6, 6)
# ┌──────────┬────────────┬────────────────────┬────────────────┬─────────────────┬──────────────┐
# │ order_id ┆ promo_code ┆ cleaned_promo_code ┆ priority_label ┆ greatest_amount ┆ least_amount │
# │ ---      ┆ ---        ┆ ---                ┆ ---            ┆ ---             ┆ ---          │
# │ i64      ┆ str        ┆ str                ┆ str            ┆ f64             ┆ f64          │
# ╞══════════╪════════════╪════════════════════╪════════════════╪═════════════════╪══════════════╡
# │ 1001     ┆ SPRING     ┆ SPRING             ┆ priority       ┆ 240.000         ┆ 5.000        │
# │ 1002     ┆ null       ┆ NO_PROMO           ┆ normal         ┆ 80.000          ┆ 7.500        │
# │ 1003     ┆ VIP        ┆ VIP                ┆ normal         ┆ 225.000         ┆ 0.000        │
# │ 1004     ┆ null       ┆ NO_PROMO           ┆ priority       ┆ 450.000         ┆ 12.000       │
# │ 1005     ┆            ┆ NO_PROMO           ┆ normal         ┆ 80.000          ┆ 4.000        │
# │ 1006     ┆ VIP        ┆ VIP                ┆ priority       ┆ 400.000         ┆ 10.000       │
# └──────────┴────────────┴────────────────────┴────────────────┴─────────────────┴──────────────┘

out_native = lf_orders.select(
    "order_id",
    "promo_code",
    c.promo_code.replace("", None).fill_null("NO_PROMO").alias("cleaned_promo_code"),
    pl.when(c.is_priority).then(pl.lit("priority")).otherwise(pl.lit("normal")).alias("priority_label"),
    pl.max_horizontal(c.quantity * c.unit_price, c.shipping_fee).alias("greatest_amount"),
    pl.min_horizontal(c.quantity * c.unit_price, c.shipping_fee).alias("least_amount"),
)
print(out_native.collect())


# =========================================================================================
# 12. Using SQL expressions in an eager DataFrame
# =========================================================================================
'''
DataFrame.sql(...) can also run SQL directly on an eager DataFrame.
Depending on the Polars version and context, DataFrame.sql(...) usually returns an eager
DataFrame, while LazyFrame.sql(...) returns a LazyFrame.

For consistency in tutorial code, the earlier examples used lf_orders.sql(...).collect().
'''

out_eager_sql = df_orders.sql(
    """
    SELECT
        order_id,
        customer,
        quantity * unit_price AS gross_sales,
        CASE WHEN is_priority THEN 'priority' ELSE 'normal' END AS priority_label
    FROM self
    """
)
print(out_eager_sql)
print(type(out_eager_sql))


# =========================================================================================
# 13. Quick summary
# =========================================================================================
'''
Quick SQL -> native Polars map:

1. Arithmetic expression
   SQL:     quantity * unit_price AS gross_sales
   Polars:  (c.quantity * c.unit_price).alias("gross_sales")

2. Literal value
   SQL:     'online' AS sales_channel
   Polars:  pl.lit("online").alias("sales_channel")

3. Strict cast
   SQL:     CAST(order_date_text AS date) AS order_date
   Polars:  c.order_date_text.cast(pl.Date).alias("order_date")

4. Safe cast
   SQL:     TRY_CAST(score_text AS float8) AS score
   Polars:  c.score_text.cast(pl.Float64, strict=False).alias("score")

5. Searched CASE
   SQL:     CASE WHEN condition THEN value ELSE fallback END
   Polars:  pl.when(condition).then(pl.lit(value)).otherwise(pl.lit(fallback))

6. Simple CASE
   SQL:     CASE region WHEN 'East' THEN 'eastern_team' ELSE 'other_team' END
   Polars:  c.region.replace({...}, default="other_team")

Main habit:
Use SQL for readability when it is convenient, but remember that native Polars expressions
are still the primary and most complete API.
'''
