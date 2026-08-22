# FILE VERSION: 18_lit_literal_v1
'''
Polars literals with pl.lit(...).

This file explains how to use literal values inside Polars expressions.

Main idea:
    pl.lit(value) creates an expression that represents a fixed literal value.

Why this matters:
+ Polars expressions usually describe computations on columns.
+ Sometimes you need a fixed value inside the expression system:
    - a constant column such as "USD"
    - a numeric constant such as 0.08
    - a typed null such as pl.lit(None, dtype=pl.Float64)
    - a string result inside pl.when(...).then(...).otherwise(...)
    - a date/datetime cutoff value
    - a list literal

Important mental model:
+ pl.col("amount") means "use the amount column".
+ pl.lit(10) means "use the fixed value 10".
+ pl.lit("high") means "use the fixed string value 'high'".

In many arithmetic expressions, Python scalars are automatically treated as literals.
For example:
    pl.col("amount") * 1.08
is usually equivalent to:
    pl.col("amount") * pl.lit(1.08)

However, explicit pl.lit(...) is clearer and is sometimes necessary, especially
for string values in conditional expressions.
'''

import datetime as dt

import polars as pl
from polars import col as c

# Optional display settings for tutorial output.
pl.Config.set_tbl_rows(12)
pl.Config.set_tbl_cols(14)
pl.Config.set_float_precision(4)
pl.Config.set_tbl_width_chars(120)


# =========================================================================================
# 0. Example Data
# =========================================================================================
'''
The examples are self-contained so the file can run without external data files.

We create both:
+ an eager DataFrame: df_sales
+ a LazyFrame:        lf_sales
'''

df_sales = pl.DataFrame(
    {
        "order_id": [1, 2, 3, 4, 5, 6],
        "customer": ["Alice", "Bob", "Alice", "Diana", "Bob", "Evan"],
        "region": ["East", "West", "East", "North", "West", "North"],
        "amount": [120.0, 80.0, 220.0, 150.0, 90.0, 310.0],
        "quantity": [2, 1, 3, 2, 1, 4],
        "discount_rate": [0.10, None, 0.15, 0.00, None, 0.20],
        "date": [
            "2024-01-03",
            "2024-01-05",
            "2024-02-10",
            "2024-02-12",
            "2024-03-01",
            "2024-03-15",
        ],
    },
    schema_overrides={"region": pl.Categorical, "date": pl.Date}
)

lf_sales = df_sales.lazy()

print(df_sales)
# shape: (6, 7)
# ┌──────────┬──────────┬────────┬──────────┬──────────┬───────────────┬────────────┐
# │ order_id ┆ customer ┆ region ┆ amount   ┆ quantity ┆ discount_rate ┆ date       │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---      ┆ ---           ┆ ---        │
# │ i64      ┆ str      ┆ cat    ┆ f64      ┆ i64      ┆ f64           ┆ date       │
# ╞══════════╪══════════╪════════╪══════════╪══════════╪═══════════════╪════════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0000 ┆ 2        ┆ 0.1000        ┆ 2024-01-03 │
# │ 2        ┆ Bob      ┆ West   ┆ 80.0000  ┆ 1        ┆ null          ┆ 2024-01-05 │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0000 ┆ 3        ┆ 0.1500        ┆ 2024-02-10 │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0000 ┆ 2        ┆ 0.0000        ┆ 2024-02-12 │
# │ 5        ┆ Bob      ┆ West   ┆ 90.0000  ┆ 1        ┆ null          ┆ 2024-03-01 │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0000 ┆ 4        ┆ 0.2000        ┆ 2024-03-15 │
# └──────────┴──────────┴────────┴──────────┴──────────┴───────────────┴────────────┘

print(df_sales.schema)


# =========================================================================================
# 1. What does pl.lit(...) create?
# =========================================================================================
'''
pl.lit(...) creates a Polars expression.

The expression does not compute anything by itself. It needs an execution context
such as select(), with_columns(), filter(), group_by().agg(), etc.
'''

literal_expr = pl.lit(100).alias("literal_100")
print(literal_expr)
# lit(100).alias("literal_100")

# A select containing only literals returns a one-row DataFrame.
print(
    df_sales.select(
        pl.lit(100).alias("int_literal"),
        pl.lit(5.5).alias("float_literal"),
        pl.lit("hello").alias("string_literal"),
        pl.lit(True).alias("bool_literal"),
        pl.lit(None).alias("null_literal"),
    )
)
# shape: (1, 5)
# ┌─────────────┬───────────────┬────────────────┬──────────────┬──────────────┐
# │ int_literal ┆ float_literal ┆ string_literal ┆ bool_literal ┆ null_literal │
# │ ---         ┆ ---           ┆ ---            ┆ ---          ┆ ---          │
# │ i32         ┆ f64           ┆ str            ┆ bool         ┆ null         │
# ╞═════════════╪═══════════════╪════════════════╪══════════════╪══════════════╡
# │ 100         ┆ 5.5000        ┆ hello          ┆ true         ┆ null         │
# └─────────────┴───────────────┴────────────────┴──────────────┴──────────────┘

# A literal used alongside real columns is broadcast to every output row.
print(
    df_sales.select(
        "order_id",
        "customer",
        pl.lit("online").alias("sales_channel"),
        pl.lit("USD").alias("currency"),
    )
)
# shape: (6, 4)
# ┌──────────┬──────────┬───────────────┬──────────┐
# │ order_id ┆ customer ┆ sales_channel ┆ currency │
# │ ---      ┆ ---      ┆ ---           ┆ ---      │
# │ i64      ┆ str      ┆ str           ┆ str      │
# ╞══════════╪══════════╪═══════════════╪══════════╡
# │ 1        ┆ Alice    ┆ online        ┆ USD      │
# │ 2        ┆ Bob      ┆ online        ┆ USD      │
# │ 3        ┆ Alice    ┆ online        ┆ USD      │
# │ 4        ┆ Diana    ┆ online        ┆ USD      │
# │ 5        ┆ Bob      ┆ online        ┆ USD      │
# │ 6        ┆ Evan     ┆ online        ┆ USD      │
# └──────────┴──────────┴───────────────┴──────────┘


# =========================================================================================
# 2. Constant columns with with_columns()
# =========================================================================================
'''
Use pl.lit(...) inside with_columns(...) to add constant columns.

This works in both eager DataFrame and LazyFrame pipelines.
The literal is broadcast to match the number of rows in the DataFrame.
'''

out_eager = df_sales.with_columns(
    pl.lit("USD").alias("currency"),
    pl.lit(0.08).alias("tax_rate"),
    pl.lit(True).alias("is_active"),
)
print(out_eager)
# shape: (6, 10)
# ┌──────────┬──────────┬────────┬──────────┬──────────┬───────────────┬────────────┬──────────┬──────────┬───────────┐
# │ order_id ┆ customer ┆ region ┆ amount   ┆ quantity ┆ discount_rate ┆ date       ┆ currency ┆ tax_rate ┆ is_active │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---      ┆ ---           ┆ ---        ┆ ---      ┆ ---      ┆ ---       │
# │ i64      ┆ str      ┆ cat    ┆ f64      ┆ i64      ┆ f64           ┆ date       ┆ str      ┆ f64      ┆ bool      │
# ╞══════════╪══════════╪════════╪══════════╪══════════╪═══════════════╪════════════╪══════════╪══════════╪═══════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0000 ┆ 2        ┆ 0.1000        ┆ 2024-01-03 ┆ USD      ┆ 0.0800   ┆ true      │
# │ 2        ┆ Bob      ┆ West   ┆ 80.0000  ┆ 1        ┆ null          ┆ 2024-01-05 ┆ USD      ┆ 0.0800   ┆ true      │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0000 ┆ 3        ┆ 0.1500        ┆ 2024-02-10 ┆ USD      ┆ 0.0800   ┆ true      │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0000 ┆ 2        ┆ 0.0000        ┆ 2024-02-12 ┆ USD      ┆ 0.0800   ┆ true      │
# │ 5        ┆ Bob      ┆ West   ┆ 90.0000  ┆ 1        ┆ null          ┆ 2024-03-01 ┆ USD      ┆ 0.0800   ┆ true      │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0000 ┆ 4        ┆ 0.2000        ┆ 2024-03-15 ┆ USD      ┆ 0.0800   ┆ true      │
# └──────────┴──────────┴────────┴──────────┴──────────┴───────────────┴────────────┴──────────┴──────────┴───────────┘

out_lazy = (
    lf_sales
    .with_columns(
        pl.lit("USD").alias("currency"),
        pl.lit(0.08).alias("tax_rate"),
        pl.lit("v1").alias("report_version"),
    )
    .collect()
)
print(out_lazy)


# =========================================================================================
# 3. Scalars can sometimes be implicit literals
# =========================================================================================
'''
In many arithmetic expressions, ordinary Python scalars are accepted directly.
Polars treats them as literal values.

These two expressions are usually equivalent:
    c("amount") * 1.08
    c("amount") * pl.lit(1.08)

The explicit pl.lit(...) version is often clearer in teaching code.
'''

out = df_sales.select(
    "order_id",
    "amount",
    (c("amount") * 1.08).alias("amount_times_1_08_implicit"),
    (c("amount") * pl.lit(1.08)).alias("amount_times_1_08_explicit"),
)
print(out)
# shape: (6, 4)
# ┌──────────┬──────────┬────────────────────────────┬────────────────────────────┐
# │ order_id ┆ amount   ┆ amount_times_1_08_implicit ┆ amount_times_1_08_explicit │
# │ ---      ┆ ---      ┆ ---                        ┆ ---                        │
# │ i64      ┆ f64      ┆ f64                        ┆ f64                        │
# ╞══════════╪══════════╪════════════════════════════╪════════════════════════════╡
# │ 1        ┆ 120.0000 ┆ 129.6000                   ┆ 129.6000                   │
# │ 2        ┆ 80.0000  ┆ 86.4000                    ┆ 86.4000                    │
# │ 3        ┆ 220.0000 ┆ 237.6000                   ┆ 237.6000                   │
# │ 4        ┆ 150.0000 ┆ 162.0000                   ┆ 162.0000                   │
# │ 5        ┆ 90.0000  ┆ 97.2000                    ┆ 97.2000                    │
# │ 6        ┆ 310.0000 ┆ 334.8000                   ┆ 334.8000                   │
# └──────────┴──────────┴────────────────────────────┴────────────────────────────┘


# =========================================================================================
# 4. Derive columns using literal constants
# =========================================================================================
'''
A common use of pl.lit(...) is to combine a fixed value with one or more columns.
'''

out = df_sales.with_columns(
    (c("amount") * c("quantity")).alias("gross_revenue"),
).with_columns(
    (c("gross_revenue") * pl.lit(0.08)).alias("tax"),
    (c("gross_revenue") * (pl.lit(1.0) + pl.lit(0.08))).alias("gross_plus_tax"),
)
print(out)
# shape: (6, 10)
# ┌──────────┬──────────┬────────┬──────────┬──────────┬──────────────┬────────────┬─────────────┬─────────┬─────────────┐
# │ order_id ┆ customer ┆ region ┆ amount   ┆ quantity ┆ discount_rat ┆ date       ┆ gross_reven ┆ tax     ┆ gross_plus_ │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---      ┆ e            ┆ ---        ┆ ue          ┆ ---     ┆ tax         │
# │ i64      ┆ str      ┆ cat    ┆ f64      ┆ i64      ┆ ---          ┆ date       ┆ ---         ┆ f64     ┆ ---         │
# │          ┆          ┆        ┆          ┆          ┆ f64          ┆            ┆ f64         ┆         ┆ f64         │
# ╞══════════╪══════════╪════════╪══════════╪══════════╪══════════════╪════════════╪═════════════╪═════════╪═════════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0000 ┆ 2        ┆ 0.1000       ┆ 2024-01-03 ┆ 240.0000    ┆ 19.2000 ┆ 259.2000    │
# │ 2        ┆ Bob      ┆ West   ┆ 80.0000  ┆ 1        ┆ null         ┆ 2024-01-05 ┆ 80.0000     ┆ 6.4000  ┆ 86.4000     │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0000 ┆ 3        ┆ 0.1500       ┆ 2024-02-10 ┆ 660.0000    ┆ 52.8000 ┆ 712.8000    │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0000 ┆ 2        ┆ 0.0000       ┆ 2024-02-12 ┆ 300.0000    ┆ 24.0000 ┆ 324.0000    │
# │ 5        ┆ Bob      ┆ West   ┆ 90.0000  ┆ 1        ┆ null         ┆ 2024-03-01 ┆ 90.0000     ┆ 7.2000  ┆ 97.2000     │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0000 ┆ 4        ┆ 0.2000       ┆ 2024-03-15 ┆ 1240.0000   ┆ 99.2000 ┆ 1339.2000   │
# └──────────┴──────────┴────────┴──────────┴──────────┴──────────────┴────────────┴─────────────┴─────────┴─────────────┘


# =========================================================================================
# 5. dtype inference and dtype=
# =========================================================================================
'''
By default, Polars infers the dtype of the literal from the Python value.

You can also specify dtype= explicitly.
This is especially useful for:
+ smaller integer / float types
+ typed null values
+ dates, datetimes, and durations
'''

out = df_sales.select(
    pl.lit(1).alias("inferred_int"),
    pl.lit(1, dtype=pl.Int32).alias("int32_literal"),
    pl.lit(1.5).alias("inferred_float"),
    pl.lit(1.5, dtype=pl.Float32).alias("float32_literal"),
    pl.lit(None).alias("untyped_null"),
    pl.lit(None, dtype=pl.Float64).alias("typed_null_float"),
    pl.lit(dt.date(2024, 1, 1)).alias("date_literal"),
    pl.lit(dt.datetime(2024, 1, 1, 12, 30, 0)).alias("datetime_literal"),
    pl.lit(dt.timedelta(days=7)).alias("duration_literal"),
)
print(out)
print(out.schema)


# =========================================================================================
# 6. String literals in when-then-otherwise
# =========================================================================================
'''
This is one of the most important practical uses of pl.lit(...).

In many Polars expression contexts, a bare string can mean "column name".
So when you want to return a fixed string from a conditional expression, use pl.lit("...").

Good:
    pl.when(condition).then(pl.lit("high")).otherwise(pl.lit("normal"))

Avoid:
    pl.when(condition).then("high").otherwise("normal")

The second version can be interpreted as looking for columns named "high" and "normal".
'''

out = df_sales.with_columns(
    pl.when(c("amount") >= 200)
    .then(pl.lit("high"))
    .when(c("amount") >= 100)
    .then(pl.lit("medium"))
    .otherwise(pl.lit("low"))
    .alias("amount_band")
)
print(out)
# shape: (6, 8)
# ┌──────────┬──────────┬────────┬──────────┬──────────┬───────────────┬────────────┬─────────────┐
# │ order_id ┆ customer ┆ region ┆ amount   ┆ quantity ┆ discount_rate ┆ date       ┆ amount_band │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---      ┆ ---           ┆ ---        ┆ ---         │
# │ i64      ┆ str      ┆ cat    ┆ f64      ┆ i64      ┆ f64           ┆ date       ┆ str         │
# ╞══════════╪══════════╪════════╪══════════╪══════════╪═══════════════╪════════════╪═════════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0000 ┆ 2        ┆ 0.1000        ┆ 2024-01-03 ┆ medium      │
# │ 2        ┆ Bob      ┆ West   ┆ 80.0000  ┆ 1        ┆ null          ┆ 2024-01-05 ┆ low         │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0000 ┆ 3        ┆ 0.1500        ┆ 2024-02-10 ┆ high        │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0000 ┆ 2        ┆ 0.0000        ┆ 2024-02-12 ┆ medium      │
# │ 5        ┆ Bob      ┆ West   ┆ 90.0000  ┆ 1        ┆ null          ┆ 2024-03-01 ┆ low         │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0000 ┆ 4        ┆ 0.2000        ┆ 2024-03-15 ┆ high        │
# └──────────┴──────────┴────────┴──────────┴──────────┴───────────────┴────────────┴─────────────┘

# Numeric branches can also use pl.lit(...), though Python numeric scalars often work directly.
out = df_sales.with_columns(
    pl.when(c("region") == "East")
    .then(pl.lit(1))
    .otherwise(pl.lit(0))
    .alias("is_east_int")
)
print(out)
# shape: (6, 8)
# ┌──────────┬──────────┬────────┬──────────┬──────────┬───────────────┬────────────┬─────────────┐
# │ order_id ┆ customer ┆ region ┆ amount   ┆ quantity ┆ discount_rate ┆ date       ┆ is_east_int │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---      ┆ ---           ┆ ---        ┆ ---         │
# │ i64      ┆ str      ┆ cat    ┆ f64      ┆ i64      ┆ f64           ┆ date       ┆ i32         │
# ╞══════════╪══════════╪════════╪══════════╪══════════╪═══════════════╪════════════╪═════════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0000 ┆ 2        ┆ 0.1000        ┆ 2024-01-03 ┆ 1           │
# │ 2        ┆ Bob      ┆ West   ┆ 80.0000  ┆ 1        ┆ null          ┆ 2024-01-05 ┆ 0           │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0000 ┆ 3        ┆ 0.1500        ┆ 2024-02-10 ┆ 1           │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0000 ┆ 2        ┆ 0.0000        ┆ 2024-02-12 ┆ 0           │
# │ 5        ┆ Bob      ┆ West   ┆ 90.0000  ┆ 1        ┆ null          ┆ 2024-03-01 ┆ 0           │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0000 ┆ 4        ┆ 0.2000        ┆ 2024-03-15 ┆ 0           │
# └──────────┴──────────┴────────┴──────────┴──────────┴───────────────┴────────────┴─────────────┘


# =========================================================================================
# 7. Literal nulls and fill_null()
# =========================================================================================
'''
pl.lit(None) creates a null literal.

For fill_null(...), Python scalar values are usually accepted directly, but using
pl.lit(...) keeps the expression style explicit.
'''

out = df_sales.with_columns(
    c("discount_rate").fill_null(pl.lit(0.0)).alias("discount_rate_filled"),
    pl.when(c("discount_rate").is_null())
    .then(pl.lit("missing_discount"))
    .otherwise(pl.lit("has_discount"))
    .alias("discount_status"),
)
print(out.select("order_id", "discount_rate", "discount_rate_filled", "discount_status"))
# shape: (6, 4)
# ┌──────────┬───────────────┬──────────────────────┬──────────────────┐
# │ order_id ┆ discount_rate ┆ discount_rate_filled ┆ discount_status  │
# │ ---      ┆ ---           ┆ ---                  ┆ ---              │
# │ i64      ┆ f64           ┆ f64                  ┆ str              │
# ╞══════════╪═══════════════╪══════════════════════╪══════════════════╡
# │ 1        ┆ 0.1000        ┆ 0.1000               ┆ has_discount     │
# │ 2        ┆ null          ┆ 0.0000               ┆ missing_discount │
# │ 3        ┆ 0.1500        ┆ 0.1500               ┆ has_discount     │
# │ 4        ┆ 0.0000        ┆ 0.0000               ┆ has_discount     │
# │ 5        ┆ null          ┆ 0.0000               ┆ missing_discount │
# │ 6        ┆ 0.2000        ┆ 0.2000               ┆ has_discount     │
# └──────────┴───────────────┴──────────────────────┴──────────────────┘

# A typed null column can be useful when you want to create a placeholder column.
out = df_sales.with_columns(
    pl.lit(None, dtype=pl.String).alias("future_note"),
    pl.lit(None, dtype=pl.Float64).alias("future_score"),
)
print(out)
# shape: (6, 9)
# ┌──────────┬──────────┬────────┬──────────┬──────────┬───────────────┬────────────┬─────────────┬──────────────┐
# │ order_id ┆ customer ┆ region ┆ amount   ┆ quantity ┆ discount_rate ┆ date       ┆ future_note ┆ future_score │
# │ ---      ┆ ---      ┆ ---    ┆ ---      ┆ ---      ┆ ---           ┆ ---        ┆ ---         ┆ ---          │
# │ i64      ┆ str      ┆ cat    ┆ f64      ┆ i64      ┆ f64           ┆ date       ┆ str         ┆ f64          │
# ╞══════════╪══════════╪════════╪══════════╪══════════╪═══════════════╪════════════╪═════════════╪══════════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0000 ┆ 2        ┆ 0.1000        ┆ 2024-01-03 ┆ null        ┆ null         │
# │ 2        ┆ Bob      ┆ West   ┆ 80.0000  ┆ 1        ┆ null          ┆ 2024-01-05 ┆ null        ┆ null         │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0000 ┆ 3        ┆ 0.1500        ┆ 2024-02-10 ┆ null        ┆ null         │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0000 ┆ 2        ┆ 0.0000        ┆ 2024-02-12 ┆ null        ┆ null         │
# │ 5        ┆ Bob      ┆ West   ┆ 90.0000  ┆ 1        ┆ null          ┆ 2024-03-01 ┆ null        ┆ null         │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0000 ┆ 4        ┆ 0.2000        ┆ 2024-03-15 ┆ null        ┆ null         │
# └──────────┴──────────┴────────┴──────────┴──────────┴───────────────┴────────────┴─────────────┴──────────────┘


# =========================================================================================
# 8. Literal date/datetime values
# =========================================================================================
'''
Use pl.lit(date_or_datetime) when comparing a parsed date/datetime column to a fixed cutoff.
'''

out = (
    lf_sales
    .filter(c("date") >= pl.lit(dt.date(2024, 2, 1)))
    .select(
        "order_id",
        "customer",
        "date",
        "amount",
        pl.lit(dt.date(2024, 2, 1)).alias("cutoff_date"),
    )
    .collect()
)
print(out)
# shape: (4, 5)
# ┌──────────┬──────────┬────────────┬──────────┬─────────────┐
# │ order_id ┆ customer ┆ date       ┆ amount   ┆ cutoff_date │
# │ ---      ┆ ---      ┆ ---        ┆ ---      ┆ ---         │
# │ i64      ┆ str      ┆ date       ┆ f64      ┆ date        │
# ╞══════════╪══════════╪════════════╪══════════╪═════════════╡
# │ 3        ┆ Alice    ┆ 2024-02-10 ┆ 220.0000 ┆ 2024-02-01  │
# │ 4        ┆ Diana    ┆ 2024-02-12 ┆ 150.0000 ┆ 2024-02-01  │
# │ 5        ┆ Bob      ┆ 2024-03-01 ┆ 90.0000  ┆ 2024-02-01  │
# │ 6        ┆ Evan     ┆ 2024-03-15 ┆ 310.0000 ┆ 2024-02-01  │
# └──────────┴──────────┴────────────┴──────────┴─────────────┘


# =========================================================================================
# 9. Literal lists and Series
# =========================================================================================
'''
pl.lit(...) can also hold list-like data.

Useful distinction:
+ pl.lit([1, 2, 3]) creates a list literal value.
+ pl.lit(pl.Series([1, 2, 3])) creates a Series literal.

The list-literal form is commonly useful when you want the same list value in each row.
The Series-literal form is more like providing a whole column of values.
'''

print(
    pl.select(
        pl.lit([1, 2, 3]).alias("list_literal"),
        pl.lit([]).alias("empty_list_literal"),
    )
)
# shape: (1, 2)
# ┌──────────────┬────────────────────┐
# │ list_literal ┆ empty_list_literal │
# │ ---          ┆ ---                │
# │ list[i64]    ┆ list[null]         │
# ╞══════════════╪════════════════════╡
# │ [1, 2, 3]    ┆ []                 │
# └──────────────┴────────────────────┘


print(
    pl.select(
        pl.lit(pl.Series("series_values", [10, 20, 30])).alias("series_literal")
    )
)
# shape: (3, 1)
# ┌────────────────┐
# │ series_literal │
# │ ---            │
# │ i64            │
# ╞════════════════╡
# │ 10             │
# │ 20             │
# │ 30             │
# └────────────────┘


# Broadcast the same list to every row in a DataFrame.
out = df_sales.select(
    "order_id",
    pl.lit(["new", "repeat", "vip"]).alias("available_tags"),
)
print(out)
# shape: (6, 2)
# ┌──────────┬──────────────────────────┐
# │ order_id ┆ available_tags           │
# │ ---      ┆ ---                      │
# │ i64      ┆ list[str]                │
# ╞══════════╪══════════════════════════╡
# │ 1        ┆ ["new", "repeat", "vip"] │
# │ 2        ┆ ["new", "repeat", "vip"] │
# │ 3        ┆ ["new", "repeat", "vip"] │
# │ 4        ┆ ["new", "repeat", "vip"] │
# │ 5        ┆ ["new", "repeat", "vip"] │
# │ 6        ┆ ["new", "repeat", "vip"] │
# └──────────┴──────────────────────────┘


# =========================================================================================
# 10. pl.lit(...) inside structs
# =========================================================================================
'''
pl.lit(...) is also useful when building struct columns.

Here, schema_version and source are fixed literal fields, while order_id and customer
come from existing columns.
'''

out = df_sales.select(
    pl.struct(
        c("order_id"),
        c("customer"),
        pl.lit("manual_demo").alias("source"),
        pl.lit(1).alias("schema_version"),
    ).alias("metadata")
)
print(out)
# shape: (6, 1)
# ┌─────────────────────────────┐
# │ metadata                    │
# │ ---                         │
# │ struct[4]                   │
# ╞═════════════════════════════╡
# │ {1,"Alice","manual_demo",1} │
# │ {2,"Bob","manual_demo",1}   │
# │ {3,"Alice","manual_demo",1} │
# │ {4,"Diana","manual_demo",1} │
# │ {5,"Bob","manual_demo",1}   │
# │ {6,"Evan","manual_demo",1}  │
# └─────────────────────────────┘


# =========================================================================================
# 11. Grouped summaries with literals
# =========================================================================================
'''
Literals can appear inside aggregation queries too.

This is useful for adding fixed metadata to summary tables, such as a report label
or metric name.
'''

out = (
    lf_sales
    .group_by("region")
    .agg(
        pl.len().alias("n_orders"),
        c("amount").mean().alias("avg_amount"),
        c("amount").sum().alias("sum_amount"),
    )
    .with_columns(
        pl.lit("region_summary").alias("report_type"),
        pl.lit("USD").alias("currency"),
    )
    .sort("region")
    .collect()
)
print(out)
# shape: (3, 6)
# ┌────────┬──────────┬────────────┬────────────┬────────────────┬──────────┐
# │ region ┆ n_orders ┆ avg_amount ┆ sum_amount ┆ report_type    ┆ currency │
# │ ---    ┆ ---      ┆ ---        ┆ ---        ┆ ---            ┆ ---      │
# │ cat    ┆ u32      ┆ f64        ┆ f64        ┆ str            ┆ str      │
# ╞════════╪══════════╪════════════╪════════════╪════════════════╪══════════╡
# │ East   ┆ 2        ┆ 170.0000   ┆ 340.0000   ┆ region_summary ┆ USD      │
# │ North  ┆ 2        ┆ 230.0000   ┆ 460.0000   ┆ region_summary ┆ USD      │
# │ West   ┆ 2        ┆ 85.0000    ┆ 170.0000   ┆ region_summary ┆ USD      │
# └────────┴──────────┴────────────┴────────────┴────────────────┴──────────┘


# =========================================================================================
# 12. Evaluate a literal expression alone
# =========================================================================================
'''
Because pl.lit(...) returns an expression, you cannot use it like a normal Python value.

For example:
    float(pl.lit(0.5))
will not work because pl.lit(0.5) is an Expr, not a Python float.

If you truly need to evaluate a literal expression by itself, put it in an expression
context such as pl.select(...), then extract the scalar with .item().
'''

expr = pl.lit(0.5).alias("x")

print(pl.select(expr))
# shape: (1, 1)
# ┌────────┐
# │ x      │
# │ ---    │
# │ f64    │
# ╞════════╡
# │ 0.5000 │
# └────────┘

print(pl.select(expr).item())
# 0.5


# =========================================================================================
# 13. Quick practical summary
# =========================================================================================
'''
Quick mental map:

1. Refer to a column:
       pl.col("amount")

2. Refer to a fixed value:
       pl.lit(100)
       pl.lit("USD")
       pl.lit(None, dtype=pl.Float64)

3. Add a constant column:
       df.with_columns(pl.lit("USD").alias("currency"))

4. Use a string as a conditional result:
       pl.when(c("amount") > 100).then(pl.lit("big")).otherwise(pl.lit("small"))

5. Compare to a fixed date:
       c("date") >= pl.lit(dt.date(2024, 1, 1))

6. Use a list literal:
       pl.lit([1, 2, 3])

Rule of thumb:
+ If you mean "a column", use pl.col(...).
+ If you mean "a fixed value", use pl.lit(...).
+ If a bare Python scalar works but the code looks ambiguous, use pl.lit(...) for clarity.
'''
