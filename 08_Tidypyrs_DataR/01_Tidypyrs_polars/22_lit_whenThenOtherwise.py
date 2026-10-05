'''
Tidypyrs literals with tp.lit(...).

Main idea:
    tp.lit(value) creates an expression that represents a fixed literal value.

Why this matters:
+ Tidypyrs expressions usually describe computations on columns.
+ Sometimes you need a fixed value inside the expression system:
    - a constant column such as "USD"
    - a numeric constant such as 0.08
    - a typed null such as tp.lit(None, dtype=tp.Float64)
    - a string result inside tp.when(...).then(...).otherwise(...)
    - a date/datetime cutoff value
    - a list literal

Important mental model:
+ tp.col("amount") means "use the amount column".
+ tp.lit(10) means "use the fixed value 10".
+ tp.lit("high") means "use the fixed string value 'high'".

In many arithmetic expressions, Python scalars are automatically treated as literals.
For examtpe:
    tp.col("amount") * 1.08
is usually equivalent to:
    tp.col("amount") * tp.lit(1.08)

However, explicit tp.lit(...) is clearer and is sometimes necessary,
especially for string values in conditional expressions.

-------------------------------------------------------------------------------------

1. What does tp.lit(...) create?
2. Constant columns with with_columns()
3. Scalars can sometimes be implicit literals
4. dtype inference and dtype=
5. String literals in when-then-otherwise
6. Literal nulls and fill_null()
7. Literal date/datetime values
8. Literal lists and Series
9. tp.lit(...) inside structs
10. Grouped summaries with literals
11. Evaluate a literal expression alone
'''

import datetime as dt

import tidypyrs as tp
from tidypyrs import f

# Optional display settings for tutorial output.
tp.Config.set_tbl_rows(12)
tp.Config.set_tbl_cols(14)
tp.Config.set_float_precision(4)
tp.Config.set_tbl_width_chars(120)

# =========================================================================================
# 0. Example Data
# =========================================================================================

tl_sales = tp.TibbleLazy(
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
    schema_overrides={"region": tp.Categorical, "date": tp.Date}
)

print(tl_sales.collect())
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

# =========================================================================================
# 1. What does tp.lit(...) create?
# =========================================================================================
'''
tp.lit(...) creates a Tidypyrs expression.

The expression does not compute anything by itself. It needs an execution context
such as select(), with_columns(), filter(), group_by().agg(), etc.
'''

literal_expr = tp.lit(100).alias("literal_100")
print(literal_expr)
# lit(100).alias("literal_100")

# A select containing only literals returns a one-row frame.
print(
    tl_sales
    .select(
        tp.lit(100).alias("int_literal"),
        tp.lit(5.5).alias("float_literal"),
        tp.lit("hello").alias("string_literal"),
        tp.lit(True).alias("bool_literal"),
        tp.lit(None).alias("null_literal"),
    )
    .collect()
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
    tl_sales
    .select(
        "order_id",
        "customer",
        tp.lit("online").alias("sales_channel"),
        tp.lit("USD").alias("currency"),
    )
    .collect()
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
Use tp.lit(...) inside with_columns(...) to add constant columns.

This works in both eager DataFrame and LazyFrame pipelines.
The literal is broadcast to match the number of rows in the DataFrame.
'''

print(
    tl_sales
    .mutate(
        tp.lit("USD").alias("currency"),
        tp.lit(0.08).alias("tax_rate"),
        tp.lit("v1").alias("report_version"),
    )
    .collect()
)
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

# =========================================================================================
# 3. Scalars can sometimes be implicit literals
# =========================================================================================
'''
In many arithmetic expressions, ordinary Python scalars are accepted directly.
Tidypyrs treats them as literal values.

These two expressions are usually equivalent:
    f("amount") * 1.08
    f("amount") * tp.lit(1.08)

The explicit tp.lit(...) version is often clearer in teaching code.
'''

print(
    tl_sales
    .select(
        "order_id",
        "amount",
        (f("amount") * 1.08).alias("amount_times_1_08_implicit"),
        (f("amount") * tp.lit(1.08)).alias("amount_times_1_08_explicit"),
    )
    .collect()
)
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
# 4. dtype inference and dtype=
# =========================================================================================
'''
By default, Tidypyrs infers the dtype of the literal from the Python value.

You can also specify dtype= explicitly.
This is especially useful for:
+ smaller integer / float types
+ typed null values
+ dates, datetimes, and durations
'''

print(
    tl_sales
    .select(
        tp.lit(1).alias("inferred_int"),
        tp.lit(1, dtype=tp.Int32).alias("int32_literal"),
        tp.lit(1.5).alias("inferred_float"),
        tp.lit(1.5, dtype=tp.Float32).alias("float32_literal"),
        tp.lit(None).alias("untyped_null"),
        tp.lit(None, dtype=tp.Float64).alias("typed_null_float"),
        tp.lit(dt.date(2024, 1, 1)).alias("date_literal"),
        tp.lit(dt.datetime(2024, 1, 1, 12, 30, 0)).alias("datetime_literal"),
        tp.lit(dt.timedelta(days=7)).alias("duration_literal"),
    )
    .collect()
)
# shape: (1, 9)
# ┌─────────────┬─────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┐
# │ inferred_in ┆ int32_liter ┆ inferred_f ┆ float32_li ┆ untyped_nu ┆ typed_null ┆ date_liter ┆ datetime_l ┆ duration_l │
# │ t           ┆ al          ┆ loat       ┆ teral      ┆ ll         ┆ _float     ┆ al         ┆ iteral     ┆ iteral     │
# │ ---         ┆ ---         ┆ ---        ┆ ---        ┆ ---        ┆ ---        ┆ ---        ┆ ---        ┆ ---        │
# │ i32         ┆ i32         ┆ f64        ┆ f32        ┆ null       ┆ f64        ┆ date       ┆ datetime[μ ┆ duration[μ │
# │             ┆             ┆            ┆            ┆            ┆            ┆            ┆ s]         ┆ s]         │
# ╞═════════════╪═════════════╪════════════╪════════════╪════════════╪════════════╪════════════╪════════════╪════════════╡
# │ 1           ┆ 1           ┆ 1.5000     ┆ 1.5000     ┆ null       ┆ null       ┆ 2024-01-01 ┆ 2024-01-01 ┆ 7d         │
# │             ┆             ┆            ┆            ┆            ┆            ┆            ┆ 12:30:00   ┆            │
# └─────────────┴─────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┘

# =========================================================================================
# 5. String literals in when-then-otherwise
# =========================================================================================
'''
This is one of the most important practical uses of tp.lit(...).

In many Tidypyrs expression contexts, a bare string can mean "column name".
So when you want to return a fixed string from a conditional expression, use tp.lit("...").

Good:
    tp.when(condition).then(tp.lit("high")).otherwise(tp.lit("normal"))

Avoid:
    tp.when(condition).then("high").otherwise("normal")

The second version can be interpreted as looking for columns named "high" and "normal".
'''

print(
    tl_sales
    .mutate(
        tp.when(f("amount") >= 200)
        .then(tp.lit("high"))
        .when(f("amount") >= 100)
        .then(tp.lit("medium"))
        .otherwise(tp.lit("low"))
        .alias("amount_band")
    )
    .collect()
)
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

# Numeric branches can also use tp.lit(...), though Python numeric scalars often work directly.
print(
    tl_sales
    .mutate(
        tp.when(f("region") == "East")
        .then(tp.lit(1))
        .otherwise(tp.lit(0))
        .alias("is_east_int")
    )
    .collect()
)
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
# 6. Literal nulls and fill_null()
# =========================================================================================
'''
tp.lit(None) creates a null literal.

For fill_null(...), Python scalar values are usually accepted directly, but using
tp.lit(...) keeps the expression style explicit.
'''

print(
    tl_sales
    .mutate(
        f("discount_rate").fill_null(tp.lit(0.0)).alias("discount_rate_filled"),
        tp.when(f("discount_rate").is_null())
        .then(tp.lit("missing_discount"))
        .otherwise(tp.lit("has_discount"))
        .alias("discount_status"),
    )
    .select("order_id", "discount_rate", "discount_rate_filled", "discount_status")
    .collect()
)
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
print(
    tl_sales
    .mutate(
        tp.lit(None, dtype=tp.String).alias("future_note"),
        tp.lit(None, dtype=tp.Float64).alias("future_score"),
    )
    .collect()
)
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
# 7. Literal date/datetime values
# =========================================================================================
'''
Use tp.lit(date_or_datetime) when comparing a parsed date/datetime column to a fixed cutoff.
'''

print(
    tl_sales
    .filter(f("date") >= tp.lit(dt.date(2024, 2, 1)))
    .select(
        "order_id",
        "customer",
        "date",
        "amount",
        tp.lit(dt.date(2024, 2, 1)).alias("cutoff_date"),
    )
    .collect()
)
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
# 8. Literal lists and Series
# =========================================================================================
'''
tp.lit(...) can also hold list-like data.

Useful distinction:
+ tp.lit([1, 2, 3]) creates a list literal value.
+ tp.lit(tp.Series([1, 2, 3])) creates a Series literal.

The list-literal form is commonly useful when you want the same list value in each row.
The Series-literal form is more like providing a whole column of values.
'''

print(
    tp.select(
        tp.lit([1, 2, 3]).alias("list_literal"),
        tp.lit([]).alias("empty_list_literal"),
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
    tp.select(
        tp.lit(tp.Series("series_values", [10, 20, 30])).alias("series_literal")
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
print(
    tl_sales
    .select(
        "order_id",
        tp.lit(["new", "repeat", "vip"]).alias("available_tags"),
    )
    .collect()
)
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
# 9. tp.lit(...) inside structs
# =========================================================================================
'''
tp.lit(...) is also useful when building struct columns.

Here, schema_version and source are fixed literal fields, while order_id and customer
come from existing columns.
'''

print(
    tl_sales
    .select(
        tp.struct(
            f("order_id"),
            f("customer"),
            tp.lit("manual_demo").alias("source"),
            tp.lit(1).alias("schema_version"),
        ).alias("metadata")
    )
    .collect()
)
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
# 10. Grouped summaries with literals
# =========================================================================================
'''
Literals can appear inside aggregation queries too.

This is useful for adding fixed metadata to summary tables, such as a report label
or metric name.
'''

print(
    tl_sales
    .group_by("region")
    .agg(
        tp.len().alias("n_orders"),
        f("amount").mean().alias("avg_amount"),
        f("amount").sum().alias("sum_amount"),
    )
    .mutate(
        tp.lit("region_summary").alias("report_type"),
        tp.lit("USD").alias("currency"),
    )
    .sort("region")
    .collect()
)
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
# 11. Evaluate a literal expression alone
# =========================================================================================
'''
Because tp.lit(...) returns an expression, you cannot use it like a normal Python value.

For example:
    float(tp.lit(0.5))
will not work because tp.lit(0.5) is an Expr, not a Python float.

If you truly need to evaluate a literal expression by itself, put it in an expression
context such as tp.select(...), then extract the scalar with .item().
'''

expr = tp.lit(0.5).alias("x")

print(tp.select(expr))
# shape: (1, 1)
# ┌────────┐
# │ x      │
# │ ---    │
# │ f64    │
# ╞════════╡
# │ 0.5000 │
# └────────┘

print(tp.select(expr).item())
# 0.5
