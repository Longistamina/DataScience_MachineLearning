'''
In Polars, Series DO NOT have custom index labels and are designed around a
functional/immutable paradigm. Most "modifying" operations return a NEW Series
rather than mutating the original in place.

1. Updating elements: .scatter(), conditional updates with pl.when()
2. Add new elements: pl.concat()
3. Deleting elements: .filter() (boolean masks), .gather() (positional drop)

NOTE: Polars has NO equivalents for:
  - s['label'] = value   (no custom indices)
  - s.update()           (use .scatter() or pl.when() instead)
  - s.pop()              (use .item() + .gather() manually if needed)
  - s.drop(labels=...)   (use boolean masks or .gather() instead)
'''

import polars as pl


# =========================================================================================
# 1. Updating elements
# =========================================================================================

##-------------------------------------##
##          Using .scatter()           ##
##-------------------------------------##
'''
.scatter(indices, values) is the Polars equivalent of pandas' iloc-assignment.
It returns a NEW Series with the specified positions replaced.
The original Series is NOT modified in place.
'''

s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
s_new = s_old.scatter([0], [100])  # Updating the first element
print(s_new)
# shape: (5,)
# Series: 'my_series' [i64]
# [
# 	100
# 	20
# 	30
# 	40
# 	50
# ]

s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
s_new = s_old.scatter([1, 2], [200, 300])  # Updating a range of elements by position
print(s_new)
# shape: (5,)
# Series: 'my_series' [i64]
# [
# 	10
# 	200
# 	300
# 	40
# 	50
# ]

s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
s_new = s_old.scatter([0, 4], [500, 600])  # Updating multiple specific positions
print(s_new)
# shape: (5,)
# Series: 'my_series' [i64]
# [
# 	500
# 	20
# 	30
# 	40
# 	600
# ]

# Broadcast a single value to multiple positions
s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
s_new = s_old.scatter([1, 2, 3], 999)
print(s_new)
# shape: (5,)
# Series: 'my_series' [i64]
# [
# 	10
# 	999
# 	999
# 	999
# 	50
# ]

##-------------------------------------##
##   Conditional updates (pl.when)     ##
##-------------------------------------##
'''
To update values based on a condition (e.g., "set all values > 25 to 999"),
Polars uses pl.when().then().otherwise() expressions.
'''

# Approach 1: Using .scatter() with a boolean mask's true-indices
s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
mask_indices = (s_old > 25).arg_true()  # Get positions where condition is True
s_conditional = s_old.scatter(mask_indices, 999)
print(s_conditional)
# shape: (5,)
# Series: 'my_series' [i64]
# [
# 	10
# 	20
# 	999
# 	999
# 	999
# ]

# Approach 2: Using pl.when() inside a DataFrame/select context (more idiomatic for complex logic)
s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
s_conditional = pl.select(
    pl.when(pl.lit(s_old) > 25).then(999).otherwise(pl.lit(s_old))
).to_series()
print(s_conditional)
# shape: (5,)
# Series: '' [i64]
# [
# 	10
# 	20
# 	999
# 	999
# 	999
# ]


# =========================================================================================
# 2. Add new elements
# =========================================================================================

s_old = pl.Series("my_series", [10, 20, 30, 40, 50])

##-------------------------------------##
##          Using pl.concat()          ##
##-------------------------------------##
'''
pl.concat() is the ONLY idiomatic way to append elements to a Polars Series.
There is no s[new_idx] = value syntax because Polars has no custom index labels.
'''

s_extra = pl.Series("my_series", [600, 700, 800])
s_new = pl.concat([s_old, s_extra])
print(s_new)
# shape: (8,)
# Series: 'my_series' [i64]
# [
# 	10
# 	20
# 	30
# 	40
# 	50
# 	600
# 	700
# 	800
# ]

# Append a single element by wrapping it in a 1-length Series
s_new = pl.concat([s_old, pl.Series("my_series", [9999])])
print(s_new)
# shape: (6,)
# Series: 'my_series' [i64]
# [
# 	10
# 	20
# 	30
# 	40
# 	50
# 	9999
# ]

##-------------------------------------##
##       Prepending / Inserting        ##
##-------------------------------------##
'''Prepend: just swap the order in pl.concat()'''

s_prepend = pl.concat([pl.Series("my_series", [0, 1]), s_old])
print(s_prepend)
# shape: (7,)
# Series: 'my_series' [i64]
# [
# 	0
# 	1
# 	10
# 	20
# 	30
# 	40
# 	50
# ]

# Insert in the middle: slice + concat
insert_at = 2
s_inserted = pl.concat([
    s_old.slice(0, insert_at),
    pl.Series("my_series", [111, 222]),
    s_old.slice(insert_at)
])
print(s_inserted)
# shape: (7,)
# Series: 'my_series' [i64]
# [
# 	10
# 	20
# 	111
# 	222
# 	30
# 	40
# 	50
# ]


# =========================================================================================
# 3. Deleting elements
# =========================================================================================

s_old = pl.Series("my_series", [10, 20, 30, 40, 50])

##-------------------------------------##
##    Drop by POSITION using .gather() ##
##-------------------------------------##
'''
Polars has no .drop() method like pandas. To drop by position, gather all
indices EXCEPT the ones you want to remove.
'''

# Drop the element at position 0
keep_idx = [i for i in range(len(s_old)) if i != 0]
s_dropped = s_old.gather(keep_idx)
print(s_dropped)
# shape: (4,)
# Series: 'my_series' [i64]
# [
# 	20
# 	30
# 	40
# 	50
# ]

# Drop elements at positions 1 and 3
drop_positions = {1, 3}
keep_idx = [i for i in range(len(s_old)) if i not in drop_positions]
s_dropped = s_old.gather(keep_idx)
print(s_dropped)
# shape: (3,)
# Series: 'my_series' [i64]
# [
# 	10
# 	30
# 	50
# ]

##-------------------------------------##
##    Drop by VALUE using .filter()    ##
##-------------------------------------##
'''
Use boolean masks with .filter() to drop elements matching specific values.
This is conceptually similar to pandas' s[s != value] pattern.
'''

# Drop all elements equal to 30
s_dropped = s_old.filter(s_old != 30)
print(s_dropped)
# shape: (4,)
# Series: 'my_series' [i64]
# [
# 	10
# 	20
# 	40
# 	50
# ]

# Drop multiple specific values using is_in() with negation (~)
s_dropped = s_old.filter(~s_old.is_in([20, 40]))
print(s_dropped)
# shape: (3,)
# Series: 'my_series' [i64]
# [
# 	10
# 	30
# 	50
# ]

# Drop based on a condition (e.g., drop all values > 25)
s_dropped = s_old.filter(s_old <= 25)
print(s_dropped)
# shape: (2,)
# Series: 'my_series' [i64]
# [
# 	10
# 	20
# ]

##-------------------------------------##
##         Drop null values            ##
##-------------------------------------##

s_with_nulls = pl.Series("my_series", [10, None, 30, None, 50])
print(s_with_nulls.drop_nulls())
# shape: (3,)
# Series: 'my_series' [i64]
# [
# 	10
# 	30
# 	50
# ]

##-------------------------------------##
##      Emulating pandas' s.pop()      ##
##-------------------------------------##
'''
Polars has no .pop() method. To emulate it, extract the value with .item(idx)
and then drop that position with .gather().
'''

def polars_pop(series, idx):
    """Emulate pandas' s.pop(idx): returns (popped_value, new_series)."""
    value = series.item(idx)
    keep_idx = [i for i in range(len(series)) if i != (idx % len(series))]
    return value, series.gather(keep_idx)

popped_value, s_after_pop = polars_pop(s_old, 0)
print(popped_value)   # 10
print(s_after_pop)
# shape: (4,)
# Series: 'my_series' [i64]
# [
# 	20
# 	30
# 	40
# 	50
# ]
