'''
Polars has two concepts that are worth learning early:

1. Expression
   + A lazy description of a column transformation.
   + Examples: pl.col("amount") * 2, pl.col("name").str.to_uppercase(), pl.col("x").mean()
   + Expressions do not compute anything by themselves. They need an execution context.

2. LazyFrame
   + A lazy query plan for a whole table.
   + You build the plan first, then execute it with .collect().
   + It lets Polars optimize the whole query before reading/computing data.

####################################################################################################

Important mental model:

Pandas style:
    often immediate execution, step by step

Polars style:
    expression = what to calculate for one or more columns
    context    = where to run the expression
    LazyFrame  = a full query plan that can be optimized before execution

Common execution contexts for expressions:
+ df.select(...)          choose/compute output columns
+ df.with_columns(...)    add or replace columns
+ df.filter(...)          keep rows where a boolean expression is true
+ df.group_by(...).agg(...) aggregate by groups
+ lazy_frame.select(...), lazy_frame.with_columns(...), lazy_frame.filter(...), etc.
'''

import polars as pl

# Create a small self-contained demo dataset.
# This avoids depending on an external data folder.
df_sales = pl.DataFrame(
    {
        "order_id": [1, 2, 3, 4, 5, 6],
        "customer": ["Alice", "Bob", "Alice", "Diana", "Bob", "Evan"],
        "region": ["East", "West", "East", "North", "West", "North"],
        "amount": [120.0, 80.0, 220.0, 150.0, 90.0, 310.0],
        "quantity": [2, 1, 3, 2, 1, 4],
        "date": [
            "2024-01-03",
            "2024-01-05",
            "2024-02-10",
            "2024-02-12",
            "2024-03-01",
            "2024-03-15",
        ],
    }
)

print(df_sales)
# shape: (6, 6)
# ┌──────────┬──────────┬────────┬────────┬──────────┬────────────┐
# │ order_id ┆ customer ┆ region ┆ amount ┆ quantity ┆ date       │
# │ ---      ┆ ---      ┆ ---    ┆ ---    ┆ ---      ┆ ---        │
# │ i64      ┆ str      ┆ str    ┆ f64    ┆ i64      ┆ str        │
# ╞══════════╪══════════╪════════╪════════╪══════════╪════════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0  ┆ 2        ┆ 2024-01-03 │
# │ 2        ┆ Bob      ┆ West   ┆ 80.0   ┆ 1        ┆ 2024-01-05 │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0  ┆ 3        ┆ 2024-02-10 │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0  ┆ 2        ┆ 2024-02-12 │
# │ 5        ┆ Bob      ┆ West   ┆ 90.0   ┆ 1        ┆ 2024-03-01 │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0  ┆ 4        ┆ 2024-03-15 │
# └──────────┴──────────┴────────┴────────┴──────────┴────────────┘
# columns: order_id, customer, region, amount, quantity, date


#--------------------------------------------------------------------------------------------------#
#------------------------------- 1. What is a Polars Expression? ----------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
An expression is a symbolic instruction.
It says WHAT should happen, but it does not run immediately by itself.

The most common expression constructors are:
+ pl.col("column_name")  -> refer to an existing column
+ pl.lit(value)          -> create a literal value expression
+ pl.all()               -> refer to all columns
+ pl.when(...).then(...).otherwise(...) -> conditional expression

Think of an expression like a recipe:
    pl.col("amount") * pl.col("quantity")

This recipe means:
    take the amount column, multiply it row-wise by the quantity column.

But the recipe is not cooked until it is placed in a context like select() or with_columns().
'''

revenue_expr = (pl.col("amount") * pl.col("quantity")).alias("revenue")

print(revenue_expr)
# [(col("amount")) * (col("quantity"))].alias("revenue")

'''
Nothing has been computed yet.
The expression object only stores the computation that Polars should perform later.
'''


#--------------------------------------------------------------------------------------------------#
#----------------------------- 2. Expressions need execution contexts -----------------------------#
#--------------------------------------------------------------------------------------------------#
'''
A context is where Polars knows how to apply expressions to data.

The same expression idea is used in both eager DataFrames and LazyFrames.
This section uses eager DataFrames first because the results are easy to see immediately.
'''

#################
## df.select() ##
#################
'''
df.select(...) creates a new DataFrame from the expressions you pass in.
It is often used to choose columns and compute new output columns.
'''

out = df_sales.select(
    pl.col("order_id"),
    pl.col("customer"),
    revenue_expr,
)
print(out)
# shape: (6, 3)
# ┌──────────┬──────────┬─────────┐
# │ order_id ┆ customer ┆ revenue │
# │ ---      ┆ ---      ┆ ---     │
# │ i64      ┆ str      ┆ f64     │
# ╞══════════╪══════════╪═════════╡
# │ 1        ┆ Alice    ┆ 240.0   │
# │ 2        ┆ Bob      ┆ 80.0    │
# │ 3        ┆ Alice    ┆ 660.0   │
# │ 4        ┆ Diana    ┆ 300.0   │
# │ 5        ┆ Bob      ┆ 90.0    │
# │ 6        ┆ Evan     ┆ 1240.0  │
# └──────────┴──────────┴─────────┘

#######################
## df.with_columns() ##
#######################
'''
df.with_columns(...) adds new columns or replaces existing columns.
It keeps the original columns unless you overwrite them by using the same column name.
'''

out = df_sales.with_columns(
    revenue_expr,
    pl.col("date").str.to_date().alias("date_parsed"),
)
print(out)
# shape: (6, 8)
# ┌──────────┬──────────┬────────┬────────┬──────────┬────────────┬─────────┬─────────────┐
# │ order_id ┆ customer ┆ region ┆ amount ┆ quantity ┆ date       ┆ revenue ┆ date_parsed │
# │ ---      ┆ ---      ┆ ---    ┆ ---    ┆ ---      ┆ ---        ┆ ---     ┆ ---         │
# │ i64      ┆ str      ┆ str    ┆ f64    ┆ i64      ┆ str        ┆ f64     ┆ date        │
# ╞══════════╪══════════╪════════╪════════╪══════════╪════════════╪═════════╪═════════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0  ┆ 2        ┆ 2024-01-03 ┆ 240.0   ┆ 2024-01-03  │
# │ 2        ┆ Bob      ┆ West   ┆ 80.0   ┆ 1        ┆ 2024-01-05 ┆ 80.0    ┆ 2024-01-05  │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0  ┆ 3        ┆ 2024-02-10 ┆ 660.0   ┆ 2024-02-10  │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0  ┆ 2        ┆ 2024-02-12 ┆ 300.0   ┆ 2024-02-12  │
# │ 5        ┆ Bob      ┆ West   ┆ 90.0   ┆ 1        ┆ 2024-03-01 ┆ 90.0    ┆ 2024-03-01  │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0  ┆ 4        ┆ 2024-03-15 ┆ 1240.0  ┆ 2024-03-15  │
# └──────────┴──────────┴────────┴────────┴──────────┴────────────┴─────────┴─────────────┘

#################
## df.filter() ##
#################
'''
df.filter(...) expects a boolean expression.
Rows are kept where the expression evaluates to True.
'''

out = df_sales.filter(
    (pl.col("amount") >= 100) & (pl.col("region").is_in(["East", "North"]))
)
print(out)
shape: (4, 6)
# ┌──────────┬──────────┬────────┬────────┬──────────┬────────────┐
# │ order_id ┆ customer ┆ region ┆ amount ┆ quantity ┆ date       │
# │ ---      ┆ ---      ┆ ---    ┆ ---    ┆ ---      ┆ ---        │
# │ i64      ┆ str      ┆ str    ┆ f64    ┆ i64      ┆ str        │
# ╞══════════╪══════════╪════════╪════════╪══════════╪════════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0  ┆ 2        ┆ 2024-01-03 │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0  ┆ 3        ┆ 2024-02-10 │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0  ┆ 2        ┆ 2024-02-12 │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0  ┆ 4        ┆ 2024-03-15 │
# └──────────┴──────────┴────────┴────────┴──────────┴────────────┘
# keeps rows where amount >= 100 and region is East/North

#########################
## df.group_by().agg() ##
#########################
'''
group_by(...).agg(...) uses aggregation expressions.
Each expression describes one output summary per group.
'''

out = df_sales.group_by("region").agg(
    pl.len().alias("n_orders"),
    pl.col("amount").sum().alias("total_amount"),
    pl.col("amount").mean().alias("avg_amount"),
)
print(out)
# shape: (3, 4)
# ┌────────┬──────────┬──────────────┬────────────┐
# │ region ┆ n_orders ┆ total_amount ┆ avg_amount │
# │ ---    ┆ ---      ┆ ---          ┆ ---        │
# │ str    ┆ u32      ┆ f64          ┆ f64        │
# ╞════════╪══════════╪══════════════╪════════════╡
# │ East   ┆ 2        ┆ 340.0        ┆ 170.0      │
# │ West   ┆ 2        ┆ 170.0        ┆ 85.0       │
# │ North  ┆ 2        ┆ 460.0        ┆ 230.0      │
# └────────┴──────────┴──────────────┴────────────┘
# one row per region, with aggregate columns


#--------------------------------------------------------------------------------------------------#
#------------------------------- 3. Expression chaining and aliasing ------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
Expressions are composable.
Most expression methods return another expression, so you can chain them.

Common chain pattern:
    1. start with pl.col(...)
    2. apply transformations
    3. give the result a name with .alias(...)
'''

out = df_sales.select(
    pl.col("customer").str.to_uppercase().alias("CUSTOMER"),
    pl.col("amount").round(0).cast(pl.Int64).alias("amount_int"),
    (pl.col("amount") / pl.col("quantity")).round(2).alias("unit_price"),
)
print(out)
# shape: (6, 3)
# ┌──────────┬────────────┬────────────┐
# │ CUSTOMER ┆ amount_int ┆ unit_price │
# │ ---      ┆ ---        ┆ ---        │
# │ str      ┆ i64        ┆ f64        │
# ╞══════════╪════════════╪════════════╡
# │ ALICE    ┆ 120        ┆ 60.0       │
# │ BOB      ┆ 80         ┆ 80.0       │
# │ ALICE    ┆ 220        ┆ 73.33      │
# │ DIANA    ┆ 150        ┆ 75.0       │
# │ BOB      ┆ 90         ┆ 90.0       │
# │ EVAN     ┆ 310        ┆ 77.5       │
# └──────────┴────────────┴────────────┘
# customer transformed to uppercase, amount converted, unit price calculated


#--------------------------------------------------------------------------------------------------#
#---------------------------------- 4. Conditional expressions ------------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
Use pl.when(...).then(...).otherwise(...) for vectorized if/else logic.

Important:
+ Use pl.lit("some string") when the result is a literal string.
+ A bare string in many Polars expression positions can be interpreted as a column name.
'''

out = df_sales.with_columns(
    pl.when(pl.col("amount") >= 200)
    .then(pl.lit("high"))
    .when(pl.col("amount") >= 100)
    .then(pl.lit("medium"))
    .otherwise(pl.lit("low"))
    .alias("amount_band")
)
print(out)
# shape: (6, 7)
# ┌──────────┬──────────┬────────┬────────┬──────────┬────────────┬─────────────┐
# │ order_id ┆ customer ┆ region ┆ amount ┆ quantity ┆ date       ┆ amount_band │
# │ ---      ┆ ---      ┆ ---    ┆ ---    ┆ ---      ┆ ---        ┆ ---         │
# │ i64      ┆ str      ┆ str    ┆ f64    ┆ i64      ┆ str        ┆ str         │
# ╞══════════╪══════════╪════════╪════════╪══════════╪════════════╪═════════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0  ┆ 2        ┆ 2024-01-03 ┆ medium      │
# │ 2        ┆ Bob      ┆ West   ┆ 80.0   ┆ 1        ┆ 2024-01-05 ┆ low         │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0  ┆ 3        ┆ 2024-02-10 ┆ high        │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0  ┆ 2        ┆ 2024-02-12 ┆ medium      │
# │ 5        ┆ Bob      ┆ West   ┆ 90.0   ┆ 1        ┆ 2024-03-01 ┆ low         │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0  ┆ 4        ┆ 2024-03-15 ┆ high        │
# └──────────┴──────────┴────────┴────────┴──────────┴────────────┴─────────────┘
# adds amount_band: low / medium / high


#--------------------------------------------------------------------------------------------------#
#----------------------------------- 5. Window expressions ----------------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
Window expressions calculate values over groups while keeping the original row count.

Use .over(...) when you want a group calculation attached back to each original row.
This is similar in spirit to pandas groupby(...).transform(...).
'''

out = df_sales.with_columns(
    pl.col("amount").sum().over("region").alias("region_total_amount"),
    pl.col("amount").rank(descending=True).over("region").alias("rank_within_region"),
)
print(out)
# shape: (6, 8)
# ┌──────────┬──────────┬────────┬────────┬──────────┬────────────┬─────────────────┬────────────────┐
# │ order_id ┆ customer ┆ region ┆ amount ┆ quantity ┆ date       ┆ region_total_am ┆ rank_within_re │
# │ ---      ┆ ---      ┆ ---    ┆ ---    ┆ ---      ┆ ---        ┆ ount            ┆ gion           │
# │ i64      ┆ str      ┆ str    ┆ f64    ┆ i64      ┆ str        ┆ ---             ┆ ---            │
# │          ┆          ┆        ┆        ┆          ┆            ┆ f64             ┆ f64            │
# ╞══════════╪══════════╪════════╪════════╪══════════╪════════════╪═════════════════╪════════════════╡
# │ 1        ┆ Alice    ┆ East   ┆ 120.0  ┆ 2        ┆ 2024-01-03 ┆ 340.0           ┆ 2.0            │
# │ 2        ┆ Bob      ┆ West   ┆ 80.0   ┆ 1        ┆ 2024-01-05 ┆ 170.0           ┆ 2.0            │
# │ 3        ┆ Alice    ┆ East   ┆ 220.0  ┆ 3        ┆ 2024-02-10 ┆ 340.0           ┆ 1.0            │
# │ 4        ┆ Diana    ┆ North  ┆ 150.0  ┆ 2        ┆ 2024-02-12 ┆ 460.0           ┆ 2.0            │
# │ 5        ┆ Bob      ┆ West   ┆ 90.0   ┆ 1        ┆ 2024-03-01 ┆ 170.0           ┆ 1.0            │
# │ 6        ┆ Evan     ┆ North  ┆ 310.0  ┆ 4        ┆ 2024-03-15 ┆ 460.0           ┆ 1.0            │
# └──────────┴──────────┴────────┴────────┴──────────┴────────────┴─────────────────┴────────────────┘
# original rows are preserved, with group-level values added to each row


#--------------------------------------------------------------------------------------------------#
#------------------------------- 6. Namespace expressions (.str, .dt, .list) ----------------------#
#--------------------------------------------------------------------------------------------------#
'''
Polars uses namespaces to organize type-specific expression methods.

Examples:
+ .str   string operations
+ .dt    date/datetime/duration operations
+ .list  variable-length list operations
+ .arr   fixed-size array operations
+ .struct struct-field operations
+ .cat   categorical operations
+ .bin   binary operations
'''

out = df_sales.select(
    pl.col("customer").str.to_lowercase().alias("customer_lower"),
    pl.col("date").str.to_date().dt.month().alias("month"),
)
print(out)
# shape: (6, 2)
# ┌────────────────┬───────┐
# │ customer_lower ┆ month │
# │ ---            ┆ ---   │
# │ str            ┆ i8    │
# ╞════════════════╪═══════╡
# │ alice          ┆ 1     │
# │ bob            ┆ 1     │
# │ alice          ┆ 2     │
# │ diana          ┆ 2     │
# │ bob            ┆ 3     │
# │ evan           ┆ 3     │
# └────────────────┴───────┘
# customer_lower and extracted month

# A tiny list-column example.
df_items = pl.DataFrame(
    {
        "order_id": [1, 2, 3],
        "items": [["apple", "banana"], ["coffee"], ["tea", "cake", "milk"]],
    }
)
out = df_items.with_columns(
    pl.col("items").list.len().alias("n_items"),
    pl.col("items").list.first().alias("first_item"),
)
print(out)
# shape: (3, 4)
# ┌──────────┬─────────────────────────┬─────────┬────────────┐
# │ order_id ┆ items                   ┆ n_items ┆ first_item │
# │ ---      ┆ ---                     ┆ ---     ┆ ---        │
# │ i64      ┆ list[str]               ┆ u32     ┆ str        │
# ╞══════════╪═════════════════════════╪═════════╪════════════╡
# │ 1        ┆ ["apple", "banana"]     ┆ 2       ┆ apple      │
# │ 2        ┆ ["coffee"]              ┆ 1       ┆ coffee     │
# │ 3        ┆ ["tea", "cake", "milk"] ┆ 3       ┆ tea        │
# └──────────┴─────────────────────────┴─────────┴────────────┘
# adds n_items and first_item


#--------------------------------------------------------------------------------------------------#
#------------------------- 7. Expression expansion: one expression, many columns ------------------#
#--------------------------------------------------------------------------------------------------#
'''
Expression expansion means one expression can expand to many output expressions.

Examples:
+ pl.all() selects all columns.
+ pl.col(pl.Float64) selects all Float64 columns.
+ pl.col("^amount|quantity$") can select by regex when used appropriately.

This is one reason Polars code can be concise for wide tables.
'''

out = df_sales.select(
    pl.col(pl.Float64).mean().name.suffix("_mean"),
    pl.col(pl.Int64).sum().name.suffix("_sum"),
)
print(out)
# shape: (1, 3)
# ┌─────────────┬──────────────┬──────────────┐
# │ amount_mean ┆ order_id_sum ┆ quantity_sum │
# │ ---         ┆ ---          ┆ ---          │
# │ f64         ┆ i64          ┆ i64          │
# ╞═════════════╪══════════════╪══════════════╡
# │ 161.666667  ┆ 21           ┆ 13           │
# └─────────────┴──────────────┴──────────────┘
# amount_mean plus sums of integer columns such as order_id and quantity


#--------------------------------------------------------------------------------------------------#
#----------------------------- 8. Reusing expressions as variables --------------------------------#
#--------------------------------------------------------------------------------------------------#
'''
Since expressions are just objects, you can store and reuse them.
This is useful when the same business logic is needed in many pipelines.
'''

is_large_order = pl.col("amount") >= 150
revenue = (pl.col("amount") * pl.col("quantity")).alias("revenue")

out = df_sales.filter(is_large_order).select(
    "order_id",
    "customer",
    "amount",
    revenue,
)
print(out)
# shape: (3, 4)
# ┌──────────┬──────────┬────────┬─────────┐
# │ order_id ┆ customer ┆ amount ┆ revenue │
# │ ---      ┆ ---      ┆ ---    ┆ ---     │
# │ i64      ┆ str      ┆ f64    ┆ f64     │
# ╞══════════╪══════════╪════════╪═════════╡
# │ 3        ┆ Alice    ┆ 220.0  ┆ 660.0   │
# │ 4        ┆ Diana    ┆ 150.0  ┆ 300.0   │
# │ 6        ┆ Evan     ┆ 310.0  ┆ 1240.0  │
# └──────────┴──────────┴────────┴─────────┘
# filters with one reusable expression and calculates another reusable expression


#--------------------------------------------------------------------------------------------------#
#---------------------------- 9. Categorized API list for Expressions -----------------------------#
#--------------------------------------------------------------------------------------------------#
'''
The lists below are a categorized map of the Polars expression API.
They are included for orientation, not for memorization.

Detailed documentation:
https://docs.pola.rs/api/python/stable/reference/expressions/index.html

A. Core expression constructors and expression functions
+ pl.col
+ pl.lit
+ pl.all
+ pl.exclude
+ pl.len
+ pl.first
+ pl.last
+ pl.nth
+ pl.head
+ pl.tail
+ pl.when
+ pl.select
+ pl.sql
+ pl.sql_expr
+ pl.struct
+ pl.field
+ pl.element
+ pl.groups
+ pl.format
+ pl.coalesce
+ pl.fold
+ pl.reduce
+ pl.cum_fold
+ pl.cum_reduce
+ pl.concat_str
+ pl.concat_list
+ pl.concat_arr
+ pl.max_horizontal
+ pl.min_horizontal
+ pl.sum_horizontal
+ pl.mean_horizontal
+ pl.all_horizontal
+ pl.any_horizontal
+ pl.arg_where
+ pl.arg_sort_by
+ pl.arange
+ pl.int_range
+ pl.int_ranges
+ pl.linear_space
+ pl.linear_spaces
+ pl.repeat
+ pl.ones
+ pl.zeros
+ pl.date
+ pl.time
+ pl.datetime
+ pl.duration
+ pl.date_range
+ pl.date_ranges
+ pl.time_range
+ pl.time_ranges
+ pl.datetime_range
+ pl.datetime_ranges
+ pl.business_day_count
+ pl.from_epoch
+ pl.arctan2
+ pl.arctan2d
+ pl.corr
+ pl.cov
+ pl.rolling_corr
+ pl.rolling_cov
+ pl.map_batches
+ pl.map_groups
+ pl.row_index
+ pl.implode
+ pl.count
+ pl.approx_n_unique
+ pl.n_unique
+ pl.max
+ pl.min
+ pl.mean
+ pl.median
+ pl.quantile
+ pl.std
+ pl.var
+ pl.sum
+ pl.cum_count
+ pl.cum_sum

B. Expr aggregation methods
+ Expr.agg_groups
+ Expr.all
+ Expr.any
+ Expr.approx_n_unique
+ Expr.arg_max
+ Expr.arg_min
+ Expr.bitwise_and
+ Expr.bitwise_or
+ Expr.bitwise_xor
+ Expr.count
+ Expr.first
+ Expr.has_nulls
+ Expr.implode
+ Expr.is_empty
+ Expr.last
+ Expr.len
+ Expr.max
+ Expr.max_by
+ Expr.mean
+ Expr.median
+ Expr.min
+ Expr.min_by
+ Expr.n_unique
+ Expr.nan_max
+ Expr.nan_min
+ Expr.null_count
+ Expr.product
+ Expr.quantile
+ Expr.std
+ Expr.sum
+ Expr.var

C. Expr boolean and predicate methods
+ Expr.all
+ Expr.any
+ Expr.has_nulls
+ Expr.is_between
+ Expr.is_close
+ Expr.is_duplicated
+ Expr.is_empty
+ Expr.is_finite
+ Expr.is_first_distinct
+ Expr.is_in
+ Expr.is_infinite
+ Expr.is_last_distinct
+ Expr.is_nan
+ Expr.is_not_nan
+ Expr.is_not_null
+ Expr.is_null
+ Expr.is_unique
+ Expr.not_

D. Expr operators
+ Expr.and_
+ Expr.or_
+ Expr.eq
+ Expr.eq_missing
+ Expr.ge
+ Expr.gt
+ Expr.le
+ Expr.lt
+ Expr.ne
+ Expr.ne_missing
+ Expr.add
+ Expr.floordiv
+ Expr.mod
+ Expr.mul
+ Expr.neg
+ Expr.pow
+ Expr.sub
+ Expr.truediv
+ Expr.xor

E. Expr columns, names, and output-name control
+ Expr.alias
+ Expr.exclude
+ Expr.name.keep
+ Expr.name.map
+ Expr.name.map_fields
+ Expr.name.prefix
+ Expr.name.prefix_fields
+ Expr.name.replace
+ Expr.name.suffix
+ Expr.name.suffix_fields
+ Expr.name.to_lowercase
+ Expr.name.to_uppercase

F. Expr computation methods
+ Expr.abs
+ Expr.approx_n_unique
+ Expr.arccos
+ Expr.arccosh
+ Expr.arcsin
+ Expr.arcsinh
+ Expr.arctan
+ Expr.arctanh
+ Expr.arg_unique
+ Expr.bitwise_count_ones
+ Expr.bitwise_count_zeros
+ Expr.bitwise_leading_ones
+ Expr.bitwise_leading_zeros
+ Expr.bitwise_trailing_ones
+ Expr.bitwise_trailing_zeros
+ Expr.cbrt
+ Expr.cos
+ Expr.cosh
+ Expr.cot
+ Expr.cum_count
+ Expr.cum_max
+ Expr.cum_min
+ Expr.cum_prod
+ Expr.cum_sum
+ Expr.cumulative_eval
+ Expr.degrees
+ Expr.diff
+ Expr.dot
+ Expr.entropy
+ Expr.ewm_mean
+ Expr.ewm_mean_by
+ Expr.ewm_std
+ Expr.ewm_var
+ Expr.exp
+ Expr.hash
+ Expr.hist
+ Expr.index_of
+ Expr.kurtosis
+ Expr.log
+ Expr.log10
+ Expr.log1p
+ Expr.mode
+ Expr.n_unique
+ Expr.pct_change
+ Expr.peak_max
+ Expr.peak_min
+ Expr.radians
+ Expr.rank
+ Expr.rolling_kurtosis
+ Expr.rolling_map
+ Expr.rolling_max
+ Expr.rolling_max_by
+ Expr.rolling_mean
+ Expr.rolling_mean_by
+ Expr.rolling_median
+ Expr.rolling_median_by
+ Expr.rolling_min
+ Expr.rolling_min_by
+ Expr.rolling_quantile
+ Expr.rolling_quantile_by
+ Expr.rolling_rank
+ Expr.rolling_rank_by
+ Expr.rolling_skew
+ Expr.rolling_std
+ Expr.rolling_std_by
+ Expr.rolling_sum
+ Expr.rolling_sum_by
+ Expr.rolling_var
+ Expr.rolling_var_by
+ Expr.search_sorted
+ Expr.sign
+ Expr.sin
+ Expr.sinh
+ Expr.skew
+ Expr.sqrt
+ Expr.tan
+ Expr.tanh
+ Expr.unique
+ Expr.unique_counts
+ Expr.value_counts

G. Expr manipulation, selection, and reshaping methods
+ Expr.append
+ Expr.arg_sort
+ Expr.arg_true
+ Expr.backward_fill
+ Expr.bottom_k
+ Expr.bottom_k_by
+ Expr.cast
+ Expr.ceil
+ Expr.clip
+ Expr.cut
+ Expr.drop_nans
+ Expr.drop_nulls
+ Expr.explode
+ Expr.extend_constant
+ Expr.fill_nan
+ Expr.fill_null
+ Expr.filter
+ Expr.flatten
+ Expr.floor
+ Expr.forward_fill
+ Expr.gather
+ Expr.gather_every
+ Expr.get
+ Expr.head
+ Expr.inspect
+ Expr.interpolate
+ Expr.interpolate_by
+ Expr.item
+ Expr.limit
+ Expr.lower_bound
+ Expr.map_batches
+ Expr.map_elements
+ Expr.pipe
+ Expr.qcut
+ Expr.rechunk
+ Expr.reinterpret
+ Expr.repeat_by
+ Expr.replace
+ Expr.replace_strict
+ Expr.reshape
+ Expr.reverse
+ Expr.rle
+ Expr.rle_id
+ Expr.round
+ Expr.round_sig_figs
+ Expr.sample
+ Expr.shift
+ Expr.shrink_dtype
+ Expr.shuffle
+ Expr.slice
+ Expr.sort
+ Expr.sort_by
+ Expr.tail
+ Expr.to_physical
+ Expr.top_k
+ Expr.top_k_by
+ Expr.truncate
+ Expr.upper_bound
+ Expr.where

H. Expr string namespace: Expr.str.*
+ Expr.str.concat
+ Expr.str.contains
+ Expr.str.contains_any
+ Expr.str.count_matches
+ Expr.str.decode
+ Expr.str.encode
+ Expr.str.ends_with
+ Expr.str.escape_regex
+ Expr.str.explode
+ Expr.str.extract
+ Expr.str.extract_all
+ Expr.str.extract_groups
+ Expr.str.extract_many
+ Expr.str.find
+ Expr.str.find_many
+ Expr.str.head
+ Expr.str.join
+ Expr.str.json_decode
+ Expr.str.json_path_match
+ Expr.str.len_bytes
+ Expr.str.len_chars
+ Expr.str.normalize
+ Expr.str.pad_end
+ Expr.str.pad_start
+ Expr.str.replace
+ Expr.str.replace_all
+ Expr.str.replace_many
+ Expr.str.reverse
+ Expr.str.slice
+ Expr.str.split
+ Expr.str.split_exact
+ Expr.str.splitn
+ Expr.str.starts_with
+ Expr.str.strip_chars
+ Expr.str.strip_chars_start
+ Expr.str.strip_chars_end
+ Expr.str.strip_prefix
+ Expr.str.strip_suffix
+ Expr.str.strptime
+ Expr.str.tail
+ Expr.str.to_date
+ Expr.str.to_datetime
+ Expr.str.to_decimal
+ Expr.str.to_integer
+ Expr.str.to_lowercase
+ Expr.str.to_time
+ Expr.str.to_titlecase
+ Expr.str.to_uppercase
+ Expr.str.zfill

I. Expr temporal namespace: Expr.dt.*
+ Expr.dt.add_business_days
+ Expr.dt.base_utc_offset
+ Expr.dt.cast_time_unit
+ Expr.dt.century
+ Expr.dt.combine
+ Expr.dt.convert_time_zone
+ Expr.dt.date
+ Expr.dt.datetime
+ Expr.dt.day
+ Expr.dt.days_in_month
+ Expr.dt.dst_offset
+ Expr.dt.epoch
+ Expr.dt.hour
+ Expr.dt.is_business_day
+ Expr.dt.is_leap_year
+ Expr.dt.iso_year
+ Expr.dt.microsecond
+ Expr.dt.millennium
+ Expr.dt.millisecond
+ Expr.dt.minute
+ Expr.dt.month
+ Expr.dt.month_end
+ Expr.dt.month_start
+ Expr.dt.nanosecond
+ Expr.dt.offset_by
+ Expr.dt.ordinal_day
+ Expr.dt.quarter
+ Expr.dt.replace
+ Expr.dt.replace_time_zone
+ Expr.dt.round
+ Expr.dt.second
+ Expr.dt.strftime
+ Expr.dt.time
+ Expr.dt.timestamp
+ Expr.dt.to_string
+ Expr.dt.total_days
+ Expr.dt.total_hours
+ Expr.dt.total_microseconds
+ Expr.dt.total_milliseconds
+ Expr.dt.total_minutes
+ Expr.dt.total_nanoseconds
+ Expr.dt.total_seconds
+ Expr.dt.truncate
+ Expr.dt.week
+ Expr.dt.weekday
+ Expr.dt.with_time_unit
+ Expr.dt.year

J. Expr list namespace: Expr.list.*
+ Expr.list.__getitem__
+ Expr.list.agg
+ Expr.list.all
+ Expr.list.any
+ Expr.list.arg_max
+ Expr.list.arg_min
+ Expr.list.concat
+ Expr.list.contains
+ Expr.list.count_matches
+ Expr.list.diff
+ Expr.list.drop_nulls
+ Expr.list.eval
+ Expr.list.explode
+ Expr.list.filter
+ Expr.list.first
+ Expr.list.gather
+ Expr.list.gather_every
+ Expr.list.get
+ Expr.list.head
+ Expr.list.item
+ Expr.list.join
+ Expr.list.last
+ Expr.list.len
+ Expr.list.max
+ Expr.list.mean
+ Expr.list.median
+ Expr.list.min
+ Expr.list.n_unique
+ Expr.list.reverse
+ Expr.list.sample
+ Expr.list.set_difference
+ Expr.list.set_intersection
+ Expr.list.set_symmetric_difference
+ Expr.list.set_union
+ Expr.list.shift
+ Expr.list.slice
+ Expr.list.sort
+ Expr.list.std
+ Expr.list.sum
+ Expr.list.tail
+ Expr.list.to_array
+ Expr.list.to_struct
+ Expr.list.unique
+ Expr.list.var

K. Expr array namespace: Expr.arr.*
+ Expr.arr.agg
+ Expr.arr.all
+ Expr.arr.any
+ Expr.arr.arg_max
+ Expr.arr.arg_min
+ Expr.arr.contains
+ Expr.arr.count_matches
+ Expr.arr.explode
+ Expr.arr.eval
+ Expr.arr.first
+ Expr.arr.get
+ Expr.arr.join
+ Expr.arr.last
+ Expr.arr.len
+ Expr.arr.max
+ Expr.arr.mean
+ Expr.arr.median
+ Expr.arr.min
+ Expr.arr.n_unique
+ Expr.arr.reverse
+ Expr.arr.shift
+ Expr.arr.sort
+ Expr.arr.std
+ Expr.arr.sum
+ Expr.arr.to_list
+ Expr.arr.to_struct
+ Expr.arr.unique
+ Expr.arr.var

L. Expr struct namespace: Expr.struct.*
+ Expr.struct.__getitem__
+ Expr.struct.field
+ Expr.struct.unnest
+ Expr.struct.json_encode
+ Expr.struct.rename_fields
+ Expr.struct.with_fields

M. Expr categorical namespace: Expr.cat.*
+ Expr.cat.ends_with
+ Expr.cat.get_categories
+ Expr.cat.len_bytes
+ Expr.cat.len_chars
+ Expr.cat.starts_with

N. Expr binary namespace: Expr.bin.*
+ Expr.bin.contains
+ Expr.bin.decode
+ Expr.bin.encode
+ Expr.bin.ends_with
+ Expr.bin.get
+ Expr.bin.head
+ Expr.bin.reinterpret
+ Expr.bin.size
+ Expr.bin.slice
+ Expr.bin.starts_with
+ Expr.bin.tail

O. Expr extension namespace: Expr.ext.*
+ Expr.ext.storage
+ Expr.ext.to

P. Expr window methods
+ Expr.over
+ Expr.rolling

Q. Expr meta namespace: Expr.meta.*
+ Expr.meta.as_expression
+ Expr.meta.eq
+ Expr.meta.has_multiple_outputs
+ Expr.meta.is_column
+ Expr.meta.is_column_selection
+ Expr.meta.is_literal
+ Expr.meta.is_regex_projection
+ Expr.meta.ne
+ Expr.meta.output_name
+ Expr.meta.pop
+ Expr.meta.root_names
+ Expr.meta.serialize
+ Expr.meta.show_graph
+ Expr.meta.tree_format
+ Expr.meta.undo_aliases
+ Expr.meta.write_json

R. Expr serialization and sortedness
+ Expr.deserialize
+ Expr.from_json
+ Expr.set_sorted

S. Related expression-style APIs in the docs
+ Selectors: polars.selectors, usually imported as import polars.selectors as cs
+ Data type expressions:
  - pl.dtype_of
  - pl.self_dtype
  - DataType.to_dtype_expr
  - DataTypeExpr.list.inner_dtype
  - DataTypeExpr.arr.inner_dtype
  - DataTypeExpr.arr.width
  - DataTypeExpr.arr.shape
  - DataTypeExpr.struct.field_dtype
  - DataTypeExpr.struct.field_names
'''
