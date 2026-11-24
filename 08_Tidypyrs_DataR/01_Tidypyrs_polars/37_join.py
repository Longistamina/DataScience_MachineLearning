'''
+ tl.join(other, on="key"): pandas pd.merge(on="key") equivalent.
+ tl.join(other, suffix="_right"): suffix for duplicate column names from the RIGHT TibbleLazy.
+ tl.join(other, how="inner"): only keys present in both TibbleLazy frames.
+ tl.join(other, how="full"): pandas how="outer" equivalent.
+ tl.join(other, how="left"): keep all rows from the left TibbleLazy.
+ tl.join(other, how="right"): keep all rows from the right TibbleLazy.
+ tl.join(other, left_on="key1", right_on="key2"): join on different key names.
+ Polars has no custom row index; use an explicit column for pandas left_index/right_index logic.
+ tl.join(other, how="cross"): Cartesian product.
+ tl.join_where(): non-equi joins
+ Polars also supports how="semi" and how="anti" joins.
'''

import tidypyrs as tp
from tidypyrs import f

# Optional display settings
tp.Config.set_tbl_rows(12)
tp.Config.set_tbl_cols(12)
tp.Config.set_tbl_width_chars(120)

# Create sample TibbleLazy frames for joining.
customers = tp.TibbleLazy(
    {
        "customer_id": [1, 2, 3, 4],
        "name"       : ["Alice", "Bob", "Charlie", "Diana"],
        "city"       : ["New York", "Boston", "Chicago", "Miami"],
    }
)

orders = tp.TibbleLazy(
    {
        "order_id"   : [101, 102, 103, 105],
        "customer_id": [1, 2, 1, 5],
        "amount"     : [250, 180, 320, 150],
        "city"       : ["NYC", "BOS", "NYC", "MIA"],
    }
)

##---------------------##
##    tl.join(on=)     ##
##---------------------##
'''
Join TibbleLazy frames based on a common column/key.

    customers.join(orders, on="customer_id")

Tidypyrs can infer all common column names when keys are omitted.
Here both customer_id and city are shared, so specify on="customer_id"
to avoid also requiring the differently formatted city values to match.
'''

# Default how="inner".
# maintain_order="left" is used here so the printed result is predictable.
print(
    customers
    .join(
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
Both TibbleLazy frames have a column named "city".
Tidypyrs keeps the left column name as "city" and appends the suffix to the right duplicate column.
The default suffix is "_right".
'''

##----------------------##
##    tl.join(suffix)   ##
##----------------------##
'''Add a suffix to overlapping column names from the RIGHT TibbleLazy.'''

# In pandas, suffixes=('_cst', '_odr') lets you suffix both left and right.
# In tidypyrs, suffix="_odr" applies to duplicate columns from the RIGHT TibbleLazy only.
print(
    customers
    .join(
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
##    tl.join(inner)      ##
##------------------------##
'''
how="inner": only keeps rows whose keys are present in both TibbleLazy frames.
This is the default join strategy.
'''

print(
    customers
    .join(
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
'''Only customer_id 1 and 2 are returned, because only those keys exist in both TibbleLazy frames.'''

##-----------------------##
##    tl.join(full)      ##
##-----------------------##
'''
Tidypyrs how="full" is the closest equivalent to pandas how="outer".
It keeps all rows from both TibbleLazy frames and fills missing matches with null.

NOTE:
For full joins, Polars does not coalesce join columns by default.
Use coalesce=True if you want one shared join-key column.
'''

print(
    customers
    .join(
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
'''Here, customer_id 3, 4, and 5 are included, although they are not present in both TibbleLazy frames.'''

##-----------------------##
##    tl.join(left)      ##
##-----------------------##
'''how="left": keeps all rows from the left TibbleLazy and matched rows from the right TibbleLazy.'''

print(
    customers
    .join(
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
##    tl.join(right)      ##
##------------------------##
'''how="right": keeps all rows from the right TibbleLazy and matched rows from the left TibbleLazy.'''

print(
    customers
    .join(
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
##    tl.join(left_on, right_on)    ##
##----------------------------------##
'''Join TibbleLazy frames based on different key names from each TibbleLazy.'''

customers_key = tp.TibbleLazy(
    {
        "customer_id": [1, 2, 3, 4],
        "name"       : ["Alice", "Bob", "Charlie", "Diana"],
        "city"       : ["New York", "Boston", "Chicago", "Miami"],
    }
)

orders_key = tp.TibbleLazy(
    {
        "order_id": [101, 102, 103, 105],
        "cst_id"  : [1, 2, 1, 5],
        "amount"  : [250, 180, 320, 150],
        "city"    : ["NYC", "BOS", "NYC", "MIA"],
    }
)

# coalesce=False keeps both key columns: customer_id and cst_id.
print(
    customers_key
    .join(
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
##    tl.join(cross)     ##
##-----------------------##
'''
how="cross": creates the Cartesian product of both TibbleLazy frames.
Do not specify on=, left_on=, or right_on= with a cross join.
'''

tl_left = tp.TibbleLazy({"left": ["foo", "bar"]})
print(tl_left.collect())
# shape: (2, 1)
# ┌──────┐
# │ left │
# │ ---  │
# │ str  │
# ╞══════╡
# │ foo  │
# │ bar  │
# └──────┘

tl_right = tp.TibbleLazy({"right": [7, 8]})
print(tl_right.collect())
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
    tl_left
    .join(
        tl_right,
        how="cross",
        maintain_order="left_right",
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
##    tl.join(semi)      ##
##-----------------------##
'''
how="semi": keep rows from the left TibbleLazy that have a match in the right TibbleLazy.
Unlike inner joins, semi joins do NOT include columns from the right TibbleLazy.
'''

print(
    customers
    .join(
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
##    tl.join(anti)      ##
##-----------------------##
'''
how="anti": keep rows from the left TibbleLazy that have NO match in the right TibbleLazy.
Useful for finding unmatched records.
'''

print(
    customers
    .join(
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

##------------------------------##
##    TibbleLazy .join() only   ##
##------------------------------##
'''
Use TibbleLazy.join() directly rather than a pandas-style pd.merge().
The same method supports all the equality-join strategies shown above.
'''

print(
    customers
    .join(
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
##    tl.join_where()    ##
##-----------------------##
'''
Tidypyrs `join_where()` is used for "non-equi" joins.
Unlike standard joins that require strict equality on specific keys (on="key"),
`join_where()` supports non-equality predicates, such as inequalities
(<, >) and range overlaps. It is separate from join(how=...).

This is incredibly powerful for tasks like:
+ Finding overlapping time ranges / events.
+ Matching records within a certain tolerance or distance.
+ As-of style inequality matching.

NOTE: Multiple expressions passed to join_where() are implicitly combined with AND (&).
'''
# Example: Finding overlapping events
events_a = tp.TibbleLazy({
    "event_a": ["A1", "A2", "A3"],
    "start_a": [1, 5, 20],
    "end_a": [10, 15, 30]
})
events_b = tp.TibbleLazy({
    "event_b": ["B1", "B2", "B3"],
    "start_b": [2, 12, 25],
    "end_b": [8, 20, 35]
})

# Two events overlap if: start_a < end_b AND start_b < end_a
print(
    events_a
    .join_where(
        events_b,
        f("start_a") < f("end_b"),
        f("start_b") < f("end_a")
    )
    .sort(["event_a", "event_b"])
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
If both TibbleLazy frames share column names (e.g., both have "value"), Tidypyrs applies
the suffix (default "_right") to the right TibbleLazy's columns in the evaluation context.
To avoid ambiguity in your expressions, it is highly recommended to either:
1. Use distinct column names before joining (as shown above).
2. Reference the right-side columns using the suffix in your expression:
   `f("value") < f("value_right")`
'''
