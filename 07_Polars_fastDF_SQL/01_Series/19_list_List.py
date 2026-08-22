'''
In Polars, pl.List is the variable-length nested data type.
It is different from pl.Array, which is fixed-width and uses the `.arr` namespace.

Key Differences from pl.Array:
1. pl.List: sub-lists can have different lengths row by row.
2. pl.Array: every sub-array must have the same fixed width.
3. pl.List operations use the `.list` namespace.
4. Expressions inside a list use `pl.element()` to refer to each inner value.
5. `.list.to_array(width)` only works when every sub-list has exactly that width.

Covered commands from polars.Series.list:
agg, all, any, arg_max, arg_min, concat, contains, count_matches, diff,
drop_nulls, eval, explode, filter, first, gather, gather_every, get, head,
item, join, last, len, max, mean, median, min, n_unique, reverse, sample,
set_difference, set_intersection, set_symmetric_difference, set_union,
shift, slice, sort, std, sum, tail, to_array, to_struct, unique, var

##--------------------------------------------------##
0. Creation: pl.List(inner_type)
1. Aggregation & Reduction (sum, mean, median, min, max, std, var, len, n_unique)
2. Boolean Aggregation (all, any)
3. Element Access & Indexing (first, last, get, item, arg_min, arg_max, head, tail, slice, gather, gather_every)
4. Searching, Counting, and Cleaning (contains, count_matches, drop_nulls, diff)
5. Expression Logic (eval, agg, filter)
6. Combining and Set Operations (concat, set_difference, set_intersection, set_symmetric_difference, set_union)
7. Ordering and Sampling (sort, reverse, shift, sample, unique)
8. Structural Operations (explode, join, to_array, to_struct)
9. Real applications
'''

import polars as pl


# =========================================================================================
# 0. Creation
# =========================================================================================
'''
Polars can infer List dtype from nested Python lists.
For production code, explicitly defining the inner dtype with pl.List(...) is often clearer.
'''

s_inferred = pl.Series("values", [[1, 2, 3], [4, 5], [], [6]])
print(s_inferred)
# shape: (4,)
# Series: 'values' [list[i64]]
# [
# 	[1, 2, 3]
# 	[4, 5]
# 	[]
# 	[6]
# ]

s_nums = pl.Series(
    "nums",
    [[1, 2, 3], [4, 5, 6], [10, 0, -10]],
    dtype=pl.List(pl.Int64)
)
print(s_nums)
# shape: (3,)
# Series: 'nums' [list[i64]]
# [
# 	[1, 2, 3]
# 	[4, 5, 6]
# 	[10, 0, -10]
# ]

'''
Compare with pl.Array:
+ pl.List allows different list lengths.
+ pl.Array requires the same width for every row.
'''

s_variable = pl.Series("variable", [[1], [1, 2], [1, 2, 3]], dtype=pl.List(pl.Int64))
print(s_variable)
# This is valid because pl.List is variable-length.


# =========================================================================================
# 1. Aggregation & Reduction
# =========================================================================================
'''
These methods reduce every sub-list into one scalar value per row.
They are the list equivalents of row-wise nested aggregation.
'''

s_nums = pl.Series(
    "nums",
    [[1, 2, 3], [4, 5, 6], [10, 0, -10]],
    dtype=pl.List(pl.Int64)
)

##-------------##
## .list.sum() ##
##-------------##

print(s_nums.list.sum())
# shape: (3,)
# Series: 'nums' [i64]
# [
# 	6
# 	15
# 	0
# ]

##--------------##
## .list.mean() ##
##--------------##

print(s_nums.list.mean())
# [2.0, 5.0, 0.0]

##----------------##
## .list.median() ##
##----------------##

print(s_nums.list.median())
# [2.0, 5.0, 0.0]

##-------------##
## .list.min() ##
##-------------##

print(s_nums.list.min())
# [1, 4, -10]

##-------------##
## .list.max() ##
##-------------##

print(s_nums.list.max())
# [3, 6, 10]

##-------------##
## .list.std() ##
##-------------##

print(s_nums.list.std())
# [1., 1., 10.]
# Standard deviation per sub-list.
# The default is sample standard deviation, similar to many Polars std operations.

##-------------##
## .list.var() ##
##-------------##

print(s_nums.list.var())
# [1., 1., 100.]
# Variance per sub-list.

##-------------##
## .list.len() ##
##-------------##

s_lengths = pl.Series("items", [[1, 2, 3], [4], [], None], dtype=pl.List(pl.Int64))
print(s_lengths.list.len())
# [3, 1, 0, null]

##------------------##
## .list.n_unique() ##
##------------------##

s_dups = pl.Series("dups", [[1, 1, 2, 3], [3, 3, 2], [], None], dtype=pl.List(pl.Int64))
print(s_dups.list.n_unique())
# [3, 2, 0, null]
# Number of distinct values in each sub-list.


# =========================================================================================
# 2. Boolean Aggregation
# =========================================================================================

s_bools = pl.Series(
    "flags",
    [[True, True], [False, True], [None], [], None],
    dtype=pl.List(pl.Boolean)
)

##-------------##
## .list.all() ##
##-------------##
'''
By default, ignore_nulls=True.
+ If ignore_nulls=True, null values are ignored.
+ If ignore_nulls=False, Polars uses Kleene logic, so null can propagate.
'''

print(s_bools.list.all())
# shape: (5,)
# Series: 'flags' [bool]
# [
# 	true
# 	false
# 	true
# 	true
# 	null
# ]

print(s_bools.list.all(ignore_nulls=False))
# shape: (5,)
# Series: 'flags' [bool]
# [
# 	true
# 	false
# 	null
# 	true
# 	null
# ]

##-------------##
## .list.any() ##
##-------------##
'''
By default, ignore_nulls=True.
+ If ignore_nulls=True, null values are ignored.
+ If ignore_nulls=False, Polars uses Kleene logic, so null can propagate.
'''

print(s_bools.list.any())
# shape: (5,)
# Series: 'flags' [bool]
# [
# 	true
# 	true
# 	false
# 	false
# 	null
# ]

print(s_bools.list.any(ignore_nulls=False))
# shape: (5,)
# Series: 'flags' [bool]
# [
# 	true
# 	true
# 	null
# 	false
# 	null
# ]


# =========================================================================================
# 3. Element Access & Indexing
# =========================================================================================

s_vals = pl.Series(
    "vals",
    [[10, 20, 30], [40, 5], [7], []],
    dtype=pl.List(pl.Int64)
)

##---------------##
## .list.first() ##
##---------------##

print(s_vals.list.first())
# [10, 40, 7, null]
# First element of each list

##--------------##
## .list.last() ##
##--------------##

print(s_vals.list.last())
# [30, 5, 7, null]
# Last element of each list

##-------------##
## .list.get() ##
##-------------##
'''
Get an element by index from every sub-list.
+ 0 is the first element.
+ -1 is the last element.
+ null_on_oob=True returns null instead of raising for out-of-bounds indices.
'''

print(s_vals.list.get(1, null_on_oob=True))
# [20, 5, null, null]

print(s_vals.list.get(-1, null_on_oob=True))
# [30, 5, 7, null]

##--------------##
## .list.item() ##
##--------------##
'''
Use item() only when every sub-list has exactly one element.
This is useful when list operations intentionally produce singletons.
'''

s_singletons = pl.Series("singletons", [[10], [20], [None]], dtype=pl.List(pl.Int64))
print(s_singletons.list.item())
# [10, 20, null]

##-----------------##
## .list.arg_min() ##
##-----------------##

print(s_vals.list.arg_min())
# [0, 1, 0, null]

##-----------------##
## .list.arg_max() ##
##-----------------##

print(s_vals.list.arg_max())
# [2, 0, 0, null]

##--------------##
## .list.head() ##
##--------------##

print(s_vals.list.head(2))
# [[10, 20], [40, 5], [7], []]

##--------------##
## .list.tail() ##
##--------------##

print(s_vals.list.tail(2))
# [[20, 30], [40, 5], [7], []]

##---------------##
## .list.slice() ##
##---------------##
'''
Polars list slicing follows the same idea as Series slicing:
.list.slice(offset, length)

``offset`` is the start index

This is not pandas-style start/stop slicing.
'''

print(s_vals.list.slice(1, 2))
# [[20, 30], [5], [], []]

##----------------##
## .list.gather() ##
##----------------##
'''
Take elements by index positions from each sub-list.
Use null_on_oob=True when some lists are shorter than the requested index.
'''

print(s_vals.list.gather([0, 2], null_on_oob=True))
# [[10, 30], [40, null], [7, null], [null, null]]

##----------------------##
## .list.gather_every() ##
##----------------------##
'''
Take every nth element from each sub-list, starting at offset.
'''

print(s_vals.list.gather_every(2))
# [[10, 30], [40], [7], []]

print(s_vals.list.gather_every(2, offset=1))
# [[20], [5], [], []]


# =========================================================================================
# 4. Searching, Counting, and Cleaning
# =========================================================================================

s_search = pl.Series(
    "vals",
    [[1, 2, 2], [3, 4, 5], [2, 2, 2], []],
    dtype=pl.List(pl.Int64)
)

##------------------##
## .list.contains() ##
##------------------##
'''
Check whether each sub-list contains the given item.
By default, nulls_equal=True means null is treated as a distinct value
rather than causing the result to become null.
'''

print(s_search.list.contains(2))
# [true, false, true, false]

s_with_null = pl.Series("vals", [[1, None], [2, 3], [None]], dtype=pl.List(pl.Int64))
print(s_with_null.list.contains(None))
# Finds null as a value when nulls_equal=True.

##-----------------------##
## .list.count_matches() ##
##-----------------------##

print(s_search.list.count_matches(2))
# [2, 0, 3, 0]

##--------------------##
## .list.drop_nulls() ##
##--------------------##

s_messy = pl.Series(
    "messy",
    [[1, None, 2], [None], [], [3, None]],
    dtype=pl.List(pl.Int64)
)
print(s_messy.list.drop_nulls())
# [[1, 2], [], [], [3]]

##--------------##
## .list.diff() ##
##--------------##
'''
Compute the difference between consecutive elements within every sub-list.
+ n controls how far back to subtract.
+ null_behavior="ignore" keeps the null placeholders.
+ null_behavior="drop" removes the null placeholders produced by differencing.
'''

s_trend = pl.Series("trend", [[1, 2, 4, 7], [10, 8, 3]], dtype=pl.List(pl.Int64))
print(s_trend.list.diff())
# [[null, 1, 2, 3], [null, -2, -5]]

print(s_trend.list.diff(n=2, null_behavior="drop"))
# [[3, 5], [-7]]


# =========================================================================================
# 5. Expression Logic
# =========================================================================================
'''
The most powerful List methods are .list.eval(), .list.agg(), and .list.filter().
Inside these methods, `pl.element()` refers to the values inside each sub-list.
'''

s_scores = pl.Series("scores", [[1, 4], [8, 5], [3, 2]], dtype=pl.List(pl.Int64))

##--------------##
## .list.eval() ##
##--------------##
'''
Run an expression against the elements inside every sub-list.
This usually returns another List Series.
'''

print(s_scores.list.eval(pl.element() * 10))
# [[10, 40], [80, 50], [30, 20]]

print(s_scores.list.eval(pl.element().rank()))
# shape: (3,)
# Series: 'scores' [list[f64]]
# [
# 	[1.0, 2.0]
# 	[2.0, 1.0]
# 	[2.0, 1.0]
# ]
# Rank values within each sub-list.

##-------------##
## .list.agg() ##
##-------------##
'''
Run an aggregation expression against every sub-list.
Unlike .list.eval(), this is intended for expressions that aggregate or otherwise
summarize the inner values.
'''

s_nulls = pl.Series("a", [[1, None], [42, 13], [None, None]], dtype=pl.List(pl.Int64))
print(s_nulls.list.agg(pl.element().null_count()))
# [1, 0, 2]

print(s_nulls.list.agg(pl.element().drop_nulls()))
# [[1], [42, 13], []]

##----------------##
## .list.filter() ##
##----------------##
'''
Filter the inner values of every sub-list with a boolean expression.
Because filtering changes lengths, the result is still a variable-length List.
'''

print(s_scores.list.filter(pl.element() > 3))
# [[4], [8, 5], []]


# =========================================================================================
# 6. Combining and Set Operations
# =========================================================================================

s_left = pl.Series("left", [[1, 2], [3], []], dtype=pl.List(pl.Int64))
s_right = pl.Series("right", [[10], [20, 30], [40]], dtype=pl.List(pl.Int64))

##----------------##
## .list.concat() ##
##----------------##

print(s_left.list.concat(s_right))
# [[1, 2, 10], [3, 20, 30], [40]]

##------------------------##
## .list.set_difference() ##
##------------------------##
'''
Return values that are in the left sub-list but not in the right sub-list.
Set operations remove duplicates. Use .list.sort() afterward if you need stable display order.
'''

s_a = pl.Series("a", [[1, 2, 3], [1, 2], [1, 1, 2]], dtype=pl.List(pl.Int64))
s_b = pl.Series("b", [[2, 3, 4], [2, 5], [1, 3]], dtype=pl.List(pl.Int64))

print(s_a.list.set_difference(s_b))
# shape: (3,)
# Series: 'a' [list[i64]]
# [
# 	[1]
# 	[1]
# 	[2]
# ]
# Values from a that are not in b, row by row.

##--------------------------##
## .list.set_intersection() ##
##--------------------------##

print(s_a.list.set_intersection(s_b))
# shape: (3,)
# Series: 'a' [list[i64]]
# [
# 	[2, 3]
# 	[2]
# 	[1]
# ]
# Values shared by both lists, row by row.

##----------------------------------##
## .list.set_symmetric_difference() ##
##----------------------------------##

print(s_a.list.set_symmetric_difference(s_b))
# shape: (3,)
# Series: 'a' [list[i64]]
# [
# 	[1, 4]
# 	[1, 5]
# 	[2, 3]
# ]
# Values that appear in either list but not both, row by row.

##-------------------##
## .list.set_union() ##
##-------------------##

print(s_a.list.set_union(s_b))
# shape: (3,)
# Series: 'a' [list[i64]]
# [
# 	[1, 2, … 4]
# 	[1, 2, 5]
# 	[1, 2, 3]
# ]
# Distinct values from both lists, row by row.

# Stable display order for set outputs if desired:
print(s_a.list.set_union(s_b).list.sort())


# =========================================================================================
# 7. Ordering and Sampling
# =========================================================================================

s_order = pl.Series(
    "vals",
    [[3, 1, 2], [6, 4, 5], [None, 2, 1]],
    dtype=pl.List(pl.Int64)
)

##--------------##
## .list.sort() ##
##--------------##

print(s_order.list.sort())
# shape: (3,)
# Series: 'vals' [list[i64]]
# [
# 	[1, 2, 3]
# 	[4, 5, 6]
# 	[null, 1, 2]
# ]
# Sort values inside each sub-list.

print(s_order.list.sort(descending=True, nulls_last=True))
# shape: (3,)
# Series: 'vals' [list[i64]]
# [
# 	[3, 2, 1]
# 	[6, 5, 4]
# 	[2, 1, null]
# ]
# Descending sort, with nulls placed last.

##-----------------##
## .list.reverse() ##
##-----------------##

print(s_order.list.reverse())
# shape: (3,)
# Series: 'vals' [list[i64]]
# [
# 	[2, 1, 3]
# 	[5, 4, 6]
# 	[1, 2, null]
# ]
# Reverse the order inside each sub-list.

##---------------##
## .list.shift() ##
##---------------##
'''
Shift inner values by n positions.
Positive n shifts right and pads with nulls.
Negative n shifts left and pads with nulls.
'''

print(s_order.list.shift(1))
# [[null, 3, 1], [null, 6, 4], [null, null, 2]]

print(s_order.list.shift(-1))
# [[1, 2, null], [4, 5, null], [2, 1, null]]

##----------------##
## .list.sample() ##
##----------------##
'''
Sample values from every sub-list.
Use seed for reproducibility.
`n` and `fraction` are mutually exclusive.
'''

s_sample = pl.Series("vals", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=pl.List(pl.Int64))

print(s_sample.list.sample(n=2, seed=42))
# shape: (3,)
# Series: 'vals' [list[i64]]
# [
# 	[1, 2]
# 	[4, 5]
# 	[7, 8]
# ]
# Randomly sample 2 values from each sub-list.

print(s_sample.list.sample(fraction=0.5, seed=42))
# shape: (3,)
# Series: 'vals' [list[i64]]
# [
# 	[3]
# 	[6]
# 	[9]
# ]
# Randomly sample a fraction of each sub-list.

# You can also provide a Series for per-row sample sizes.
s_n = pl.Series("n", [1, 2, 1])
print(s_sample.list.sample(n=s_n, seed=42))
# shape: (3,)
# Series: 'vals' [list[i64]]
# [
# 	[3]
# 	[4, 5]
# 	[9]
# ]

##----------------##
## .list.unique() ##
##----------------##

s_dups = pl.Series("dups", [[1, 1, 2, 3], [3, 3, 2], []], dtype=pl.List(pl.Int64))
print(s_dups.list.unique())
# shape: (3,)
# Series: 'dups' [list[i64]]
# [
# 	[1, 2, 3]
# 	[3, 2]
# 	[]
# ]
# Unique values in each sub-list. Order is not guaranteed unless maintain_order=True.

print(s_dups.list.unique(maintain_order=True))
# Unique values while preserving first-seen order.


# =========================================================================================
# 8. Structural Operations
# =========================================================================================

##-----------------##
## .list.explode() ##
##-----------------##
'''
Explode list values so every inner value becomes its own row.
This is similar to DataFrame.explode(), but called directly from the Series.list namespace.

Parameters:
+ empty_as_null=True: empty lists produce a null row by default.
+ keep_nulls=True: null list rows are kept by default.
'''

s_explode = pl.Series("nums", [[1, 2], [], None, [3]], dtype=pl.List(pl.Int64))
print(s_explode.list.explode())
# [1, 2, null, null, 3]

print(s_explode.list.explode(empty_as_null=False, keep_nulls=False))
# [1, 2, 3]
# Empty lists and null list rows are not emitted as null rows.

##--------------##
## .list.join() ##
##--------------##
'''
Join string values inside each sub-list into one string.
This only works for List(String).
'''

s_words = pl.Series(
    "words",
    [["apple", "banana"], ["dog", None], []],
    dtype=pl.List(pl.String)
)
print(s_words.list.join("-"))
# ["apple-banana", "dog", ""]

print(s_words.list.join("-", ignore_nulls=False))
# ["apple-banana", null, ""]
# If a sub-list contains null and ignore_nulls=False, that row becomes null.

##------------------##
## .list.to_array() ##
##------------------##
'''
Convert a List Series to a fixed-width Array Series.
Every sub-list must have exactly `width` elements.
'''

s_fixed = pl.Series("pair", [[1, 2], [3, 4], [5, 6]], dtype=pl.List(pl.Int64))
print(s_fixed.list.to_array(2))
# shape: (3,)
# Series: 'pair' [array[i64, 2]]
# [
# 	[1, 2]
# 	[3, 4]
# 	[5, 6]
# ]

##-------------------##
## .list.to_struct() ##
##-------------------##
'''
Convert each sub-list into a Struct.
You can then unnest the struct into multiple columns.

Common options:
+ fields=[...] gives explicit field names.
+ fields=lambda idx: ... generates field names programmatically.
+ n_field_strategy="first_non_null" uses the first non-null list width.
+ n_field_strategy="max_width" scans for the maximum list width.
'''

s_rgb = pl.Series("rgb", [[255, 0, 0], [0, 255, 0], [0, 0, 255]], dtype=pl.List(pl.Int64))
print(s_rgb.list.to_struct(fields=["red", "green", "blue"]).struct.unnest())
# shape: (3, 3)
# ┌─────┬───────┬──────┐
# │ red ┆ green ┆ blue │
# │ --- ┆ ---   ┆ ---  │
# │ i64 ┆ i64   ┆ i64  │
# ╞═════╪═══════╪══════╡
# │ 255 ┆ 0     ┆ 0    │
# │ 0   ┆ 255   ┆ 0    │
# │ 0   ┆ 0     ┆ 255  │
# └─────┴───────┴──────┘

s_channels = pl.Series("channels", [[1, 2], [3, 4, 5], [6]], dtype=pl.List(pl.Int64))
print(
    s_channels
    .list.to_struct(
        n_field_strategy="max_width",
        fields=lambda idx: f"channel_{idx}",
    )
    .struct.unnest()
)
# Expands to channel_0, channel_1, channel_2.
# shape: (3, 3)
# ┌───────────┬───────────┬───────────┐
# │ channel_0 ┆ channel_1 ┆ channel_2 │
# │ ---       ┆ ---       ┆ ---       │
# │ i64       ┆ i64       ┆ i64       │
# ╞═══════════╪═══════════╪═══════════╡
# │ 1         ┆ 2         ┆ null      │
# │ 3         ┆ 4         ┆ 5         │
# │ 6         ┆ null      ┆ null      │
# └───────────┴───────────┴───────────┘


# =========================================================================================
# 9. Real applications
# =========================================================================================

##----------------------##
## Cleaning token lists ##
##----------------------##

tags = pl.Series(
    "tags",
    [[" Python ", "POLARS", None], ["Data", "data", "Frame"], []],
    dtype=pl.List(pl.String)
)

clean_tags = (
    tags
    .list.drop_nulls()
    .list.eval(pl.element().str.strip_chars().str.to_lowercase())
    .list.unique(maintain_order=True)
)
print(clean_tags)
# [["python", "polars"], ["data", "frame"], []]

##---------------------------------##
## Feature engineering from scores ##
##---------------------------------##

scores = pl.Series("scores", [[10, 20, 30], [5, 5, 10], [100]], dtype=pl.List(pl.Int64))

features = pl.DataFrame({"scores": scores}).with_columns(
    pl.col("scores").list.len().alias("n_scores"),
    pl.col("scores").list.mean().alias("avg_score"),
    pl.col("scores").list.max().alias("max_score"),
    pl.col("scores").list.eval(pl.element() - pl.element().mean()).alias("centered_scores"),
)
print(features)
# shape: (3, 5)
# ┌──────────────┬──────────┬───────────┬───────────┬─────────────────────────────────┐
# │ scores       ┆ n_scores ┆ avg_score ┆ max_score ┆ centered_scores                 │
# │ ---          ┆ ---      ┆ ---       ┆ ---       ┆ ---                             │
# │ list[i64]    ┆ u32      ┆ f64       ┆ i64       ┆ list[f64]                       │
# ╞══════════════╪══════════╪═══════════╪═══════════╪═════════════════════════════════╡
# │ [10, 20, 30] ┆ 3        ┆ 20.0      ┆ 30        ┆ [-10.0, 0.0, 10.0]              │
# │ [5, 5, 10]   ┆ 3        ┆ 6.666667  ┆ 10        ┆ [-1.666667, -1.666667, 3.33333… │
# │ [100]        ┆ 1        ┆ 100.0     ┆ 100       ┆ [0.0]                           │
# └──────────────┴──────────┴───────────┴───────────┴─────────────────────────────────┘
