'''
+ lf.join(other, on="key"): pandas pd.merge(on="key") equivalent.
+ lf.join(other, suffix="_right"): suffix for duplicate column names from the RIGHT LazyFrame.
+ lf.join(other, how="inner"): only keys present in both LazyFrames.
+ lf.join(other, how="full"): pandas how="outer" equivalent.
+ lf.join(other, how="left"): keep all rows from the left LazyFrame.
+ lf.join(other, how="right"): keep all rows from the right LazyFrame.
+ lf.join(other, left_on="key1", right_on="key2"): join on different key names.
+ Polars has no custom row index; use an explicit column for pandas left_index/right_index logic.
+ lf.join(other, how="cross"): Cartesian product.
+ lf.join_where(): non-equi joins
+ Polars also supports how="semi" and how="anti" joins.
'''

import polars as pl

# Create sample LazyFrames for joining.
customers = pl.LazyFrame(
    {
        "customer_id": [1, 2, 3, 4],
        "name"       : ["Alice", "Bob", "Charlie", "Diana"],
        "city"       : ["New York", "Boston", "Chicago", "Miami"],
    }
)

orders = pl.LazyFrame(
    {
        "order_id"   : [101, 102, 103, 105],
        "customer_id": [1, 2, 1, 5],
        "amount"     : [250, 180, 320, 150],
        "city"       : ["NYC", "BOS", "NYC", "MIA"],
    }
)

##---------------------##
##    lf.join(on=)     ##
##---------------------##
'''
Join LazyFrames based on a common column/key.

Pandas:
    pd.merge(customers, orders, on="customer_id")

Polars:
    customers.join(orders, on="customer_id")
'''

# Default how="inner".
# maintain_order="left" is used here so the printed result is predictable.
print(
    customers.join(
        orders,
        on="customer_id",
        maintain_order="left",
    )
    .collect()
)
# shape: (3, 6)
# ┌─────────────┬───────┬──────────┬──────────┬────────┬────────────┐
# │ customer_id ┆ name  ┆ city     ┆ order_id ┆ amount ┆ city_right │
# │ ---         ┆ ---   ┆ ---      ┆ ---      ┆ ---    ┆ ---        │
# │ i64         ┆ str   ┆ str      ┆ i64      ┆ i64    ┆ str        │
# ╞═════════════╪═══════╪══════════╪══════════╪════════╪════════════╡
# │ 1           ┆ Alice ┆ New York ┆ 101      ┆ 250    ┆ NYC        │
# │ 1           ┆ Alice ┆ New York ┆ 103      ┆ 320    ┆ NYC        │
# │ 2           ┆ Bob   ┆ Boston   ┆ 102      ┆ 180    ┆ BOS        │
# └─────────────┴───────┴──────────┴──────────┴────────┴────────────┘

'''
NOTE:
Both LazyFrames have a column named "city".
Polars keeps the left column name as "city" and appends the suffix to the right duplicate column.
The default suffix is "_right".
'''

##----------------------##
##    lf.join(suffix)   ##
##----------------------##
'''Add a suffix to overlapping column names from the RIGHT LazyFrame.'''

# In pandas, suffixes=('_cst', '_odr') lets you suffix both left and right.
# In Polars, suffix="_odr" applies to duplicate columns from the RIGHT LazyFrame only.
print(
    customers.join(
        orders,
        on="customer_id",
        suffix="_odr",
        maintain_order="left",
    )
    .collect()
)
# shape: (3, 6)
# ┌─────────────┬───────┬──────────┬──────────┬────────┬──────────┐
# │ customer_id ┆ name  ┆ city     ┆ order_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---   ┆ ---      ┆ ---      ┆ ---    ┆ ---      │
# │ i64         ┆ str   ┆ str      ┆ i64      ┆ i64    ┆ str      │
# ╞═════════════╪═══════╪══════════╪══════════╪════════╪══════════╡
# │ 1           ┆ Alice ┆ New York ┆ 101      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice ┆ New York ┆ 103      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob   ┆ Boston   ┆ 102      ┆ 180    ┆ BOS      │
# └─────────────┴───────┴──────────┴──────────┴────────┴──────────┘

##------------------------##
##    lf.join(inner)      ##
##------------------------##
'''
how="inner": only keeps rows whose keys are present in both LazyFrames.
This is the default join strategy.
'''

print(
    customers.join(
        orders,
        on="customer_id",
        how="inner",
        suffix="_odr",
        maintain_order="left",
    )
    .collect()
)
# shape: (3, 6)
# ┌─────────────┬───────┬──────────┬──────────┬────────┬──────────┐
# │ customer_id ┆ name  ┆ city     ┆ order_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---   ┆ ---      ┆ ---      ┆ ---    ┆ ---      │
# │ i64         ┆ str   ┆ str      ┆ i64      ┆ i64    ┆ str      │
# ╞═════════════╪═══════╪══════════╪══════════╪════════╪══════════╡
# │ 1           ┆ Alice ┆ New York ┆ 101      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice ┆ New York ┆ 103      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob   ┆ Boston   ┆ 102      ┆ 180    ┆ BOS      │
# └─────────────┴───────┴──────────┴──────────┴────────┴──────────┘
'''Only customer_id 1 and 2 are returned, because only those keys exist in both LazyFrames.'''

##-----------------------##
##    lf.join(full)      ##
##-----------------------##
'''
Polars how="full" is the closest equivalent to pandas how="outer".
It keeps all rows from both LazyFrames and fills missing matches with null.

NOTE:
For full joins, Polars does not coalesce join columns by default.
Use coalesce=True if you want one shared join-key column.
'''

print(
    customers.join(
        orders,
        on="customer_id",
        how="full",
        suffix="_odr",
        coalesce=True,
        maintain_order="left_right",
    )
    .collect()
)
# shape: (6, 6)
# ┌─────────────┬─────────┬──────────┬──────────┬────────┬──────────┐
# │ customer_id ┆ name    ┆ city     ┆ order_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---     ┆ ---      ┆ ---      ┆ ---    ┆ ---      │
# │ i64         ┆ str     ┆ str      ┆ i64      ┆ i64    ┆ str      │
# ╞═════════════╪═════════╪══════════╪══════════╪════════╪══════════╡
# │ 1           ┆ Alice   ┆ New York ┆ 101      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice   ┆ New York ┆ 103      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob     ┆ Boston   ┆ 102      ┆ 180    ┆ BOS      │
# │ 3           ┆ Charlie ┆ Chicago  ┆ null     ┆ null   ┆ null     │
# │ 4           ┆ Diana   ┆ Miami    ┆ null     ┆ null   ┆ null     │
# │ 5           ┆ null    ┆ null     ┆ 105      ┆ 150    ┆ MIA      │
# └─────────────┴─────────┴──────────┴──────────┴────────┴──────────┘
'''Here, customer_id 3, 4, and 5 are included, although they are not present in both LazyFrames.'''

##-----------------------##
##    lf.join(left)      ##
##-----------------------##
'''how="left": keeps all rows from the left LazyFrame and matched rows from the right LazyFrame.'''

print(
    customers.join(
        orders,
        on="customer_id",
        how="left",
        suffix="_odr",
        maintain_order="left",
    )
    .collect()
)
# shape: (5, 6)
# ┌─────────────┬─────────┬──────────┬──────────┬────────┬──────────┐
# │ customer_id ┆ name    ┆ city     ┆ order_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---     ┆ ---      ┆ ---      ┆ ---    ┆ ---      │
# │ i64         ┆ str     ┆ str      ┆ i64      ┆ i64    ┆ str      │
# ╞═════════════╪═════════╪══════════╪══════════╪════════╪══════════╡
# │ 1           ┆ Alice   ┆ New York ┆ 101      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice   ┆ New York ┆ 103      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob     ┆ Boston   ┆ 102      ┆ 180    ┆ BOS      │
# │ 3           ┆ Charlie ┆ Chicago  ┆ null     ┆ null   ┆ null     │
# │ 4           ┆ Diana   ┆ Miami    ┆ null     ┆ null   ┆ null     │
# └─────────────┴─────────┴──────────┴──────────┴────────┴──────────┘

##------------------------##
##    lf.join(right)      ##
##------------------------##
'''how="right": keeps all rows from the right LazyFrame and matched rows from the left LazyFrame.'''

print(
    customers.join(
        orders,
        on="customer_id",
        how="right",
        suffix="_odr",
        maintain_order="right",
    )
    .collect()
)
# shape: (4, 6)
# ┌───────┬──────────┬─────────────┬──────────┬────────┬──────────┐
# │ name  ┆ city     ┆ customer_id ┆ order_id ┆ amount ┆ city_odr │
# │ ---   ┆ ---      ┆ ---         ┆ ---      ┆ ---    ┆ ---      │
# │ str   ┆ str      ┆ i64         ┆ i64      ┆ i64    ┆ str      │
# ╞═══════╪══════════╪═════════════╪══════════╪════════╪══════════╡
# │ Alice ┆ New York ┆ 1           ┆ 101      ┆ 250    ┆ NYC      │
# │ Bob   ┆ Boston   ┆ 2           ┆ 102      ┆ 180    ┆ BOS      │
# │ Alice ┆ New York ┆ 1           ┆ 103      ┆ 320    ┆ NYC      │
# │ null  ┆ null     ┆ 5           ┆ 105      ┆ 150    ┆ MIA      │
# └───────┴──────────┴─────────────┴──────────┴────────┴──────────┘

##----------------------------------##
##    lf.join(left_on, right_on)    ##
##----------------------------------##
'''Join LazyFrames based on different key names from each LazyFrame.'''

customers_key = pl.LazyFrame(
    {
        "customer_id": [1, 2, 3, 4],
        "name"       : ["Alice", "Bob", "Charlie", "Diana"],
        "city"       : ["New York", "Boston", "Chicago", "Miami"],
    }
)

orders_key = pl.LazyFrame(
    {
        "order_id": [101, 102, 103, 105],
        "cst_id"  : [1, 2, 1, 5],
        "amount"  : [250, 180, 320, 150],
        "city"    : ["NYC", "BOS", "NYC", "MIA"],
    }
)

# coalesce=False keeps both key columns: customer_id and cst_id.
print(
    customers_key.join(
        orders_key,
        left_on="customer_id",
        right_on="cst_id",
        how="inner",
        suffix="_odr",
        coalesce=False,
        maintain_order="left",
    )
    .collect()
)
# shape: (3, 7)
# ┌─────────────┬───────┬──────────┬──────────┬────────┬────────┬──────────┐
# │ customer_id ┆ name  ┆ city     ┆ order_id ┆ cst_id ┆ amount ┆ city_odr │
# │ ---         ┆ ---   ┆ ---      ┆ ---      ┆ ---    ┆ ---    ┆ ---      │
# │ i64         ┆ str   ┆ str      ┆ i64      ┆ i64    ┆ i64    ┆ str      │
# ╞═════════════╪═══════╪══════════╪══════════╪════════╪════════╪══════════╡
# │ 1           ┆ Alice ┆ New York ┆ 101      ┆ 1      ┆ 250    ┆ NYC      │
# │ 1           ┆ Alice ┆ New York ┆ 103      ┆ 1      ┆ 320    ┆ NYC      │
# │ 2           ┆ Bob   ┆ Boston   ┆ 102      ┆ 2      ┆ 180    ┆ BOS      │
# └─────────────┴───────┴──────────┴──────────┴────────┴────────┴──────────┘

##-----------------------##
##    lf.join(cross)     ##
##-----------------------##
'''
how="cross": creates the Cartesian product of both LazyFrames.
Do not specify on=, left_on=, or right_on= with a cross join.
'''

lf_left = pl.LazyFrame({"left": ["foo", "bar"]})
print(lf_left)
# shape: (2, 1)
# ┌──────┐
# │ left │
# │ ---  │
# │ str  │
# ╞══════╡
# │ foo  │
# │ bar  │
# └──────┘

lf_right = pl.LazyFrame({"right": [7, 8]})
print(lf_right)
# shape: (2, 1)
# ┌───────┐
# │ right │
# │ ---   │
# │ i64   │
# ╞═══════╡
# │ 7     │
# │ 8     │
# └───────┘

print(
    lf_left.join(
        lf_right,
        how="cross",
    )
    .collect()
)
# shape: (4, 2)
# ┌──────┬───────┐
# │ left ┆ right │
# │ ---  ┆ ---   │
# │ str  ┆ i64   │
# ╞══════╪═══════╡
# │ foo  ┆ 7     │
# │ foo  ┆ 8     │
# │ bar  ┆ 7     │
# │ bar  ┆ 8     │
# └──────┴───────┘

##-----------------------##
##    lf.join(semi)      ##
##-----------------------##
'''
how="semi": keep rows from the left LazyFrame that have a match in the right LazyFrame.
Unlike inner joins, semi joins do NOT include columns from the right LazyFrame.
'''

print(
    customers.join(
        orders.select("customer_id").unique(),
        on="customer_id",
        how="semi",
        maintain_order="left",
    )
    .collect()
)
# shape: (2, 3)
# ┌─────────────┬───────┬──────────┐
# │ customer_id ┆ name  ┆ city     │
# │ ---         ┆ ---   ┆ ---      │
# │ i64         ┆ str   ┆ str      │
# ╞═════════════╪═══════╪══════════╡
# │ 1           ┆ Alice ┆ New York │
# │ 2           ┆ Bob   ┆ Boston   │
# └─────────────┴───────┴──────────┘

##-----------------------##
##    lf.join(anti)      ##
##-----------------------##
'''
how="anti": keep rows from the left LazyFrame that have NO match in the right LazyFrame.
Useful for finding unmatched records.
'''

print(
    customers.join(
        orders.select("customer_id").unique(),
        on="customer_id",
        how="anti",
        maintain_order="left",
    )
    .collect()
)
# shape: (2, 3)
# ┌─────────────┬─────────┬─────────┐
# │ customer_id ┆ name    ┆ city    │
# │ ---         ┆ ---     ┆ ---     │
# │ i64         ┆ str     ┆ str     │
# ╞═════════════╪═════════╪═════════╡
# │ 3           ┆ Charlie ┆ Chicago │
# │ 4           ┆ Diana   ┆ Miami   │
# └─────────────┴─────────┴─────────┘

##-----------------------------##
##    LazyFrame .join() only   ##
##-----------------------------##
'''
Polars does not have a top-level pl.merge() function like pandas pd.merge().
Use LazyFrame.join() directly.
'''

print(
    customers.join(
        orders,
        on="customer_id",
        how="inner",
        suffix="_odr",
        maintain_order="left",
    )
    .collect()
)
# Same as the previous inner join examples.

##-----------------------##
##    lf.join_where()    ##
##-----------------------##
'''
Polars `join_where()` is used for "non-equi" joins.
Unlike standard joins that require strict equality on specific keys (on="key"),
`join_where()` allows you to join LazyFrames based on ANY arbitrary boolean expression,
such as inequalities (<, >), range overlaps, or complex custom logic.

This is incredibly powerful for tasks like:
+ Finding overlapping time ranges / events.
+ Matching records within a certain tolerance or distance.
+ As-of style inequality matching.

NOTE: Multiple expressions passed to join_where() are implicitly combined with AND (&).
'''
# Example: Finding overlapping events
events_a = pl.LazyFrame({
    "event_a": ["A1", "A2", "A3"],
    "start_a": [1, 5, 20],
    "end_a": [10, 15, 30]
})
events_b = pl.LazyFrame({
    "event_b": ["B1", "B2", "B3"],
    "start_b": [2, 12, 25],
    "end_b": [8, 20, 35]
})

# Two events overlap if: start_a < end_b AND start_b < end_a
print(
    events_a.join_where(
        events_b,
        pl.col("start_a") < pl.col("end_b"),
        pl.col("start_b") < pl.col("end_a")
    )
    .collect()
)
# shape: (4, 6)
# ┌─────────┬─────────┬───────┬─────────┬─────────┬───────┐
# │ event_a ┆ start_a ┆ end_a ┆ event_b ┆ start_b ┆ end_b │
# │ ---     ┆ ---     ┆ ---   ┆ ---     ┆ ---     ┆ ---   │
# │ str     ┆ i64     ┆ i64   ┆ str     ┆ i64     ┆ i64   │
# ╞═════════╪═════════╪═══════╪═════════╪═════════╪═══════╡
# │ A1      ┆ 1       ┆ 10    ┆ B1      ┆ 2       ┆ 8     │
# │ A2      ┆ 5       ┆ 15    ┆ B1      ┆ 2       ┆ 8     │
# │ A2      ┆ 5       ┆ 15    ┆ B2      ┆ 12      ┆ 20    │
# │ A3      ┆ 20      ┆ 30    ┆ B3      ┆ 25      ┆ 35    │
# └─────────┴─────────┴───────┴─────────┴─────────┴───────┘

'''
NOTE ON OVERLAPPING COLUMN NAMES:
If both LazyFrames share column names (e.g., both have "value"), Polars applies
the suffix (default "_right") to the right LazyFrame's columns in the evaluation context.
To avoid ambiguity in your expressions, it is highly recommended to either:
1. Use distinct column names before joining (as shown above).
2. Reference the right-side columns using the suffix in your expression:
   `pl.col("value") < pl.col("value_right")`
'''
