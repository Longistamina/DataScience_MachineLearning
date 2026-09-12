'''
In Polars, Series DO NOT have custom index labels and are designed around a
functional/immutable paradigm. Most "modifying" operations return a NEW Series
rather than mutating the original in place.

1. Updating elements: indexing-assignment, .scatter(), conditional updates with pl.when()
2. Add new elements: append and prepend with .append, insert with pl.concat
3. Deleting elements: .gather() (positional drop), .filter() (boolean masks)
'''

import polars as pl

# =========================================================================================
# 1. Updating elements
# =========================================================================================

##---------------------##
## indexing-assignment ##
##---------------------##

s_old = pl.Series("my_series", [10, 20, 30, 40, 50])

s_new = s_old.clone()
s_new[0, 3] = 5, 9
print(s_new.to_list())
# [5, 20, 30, 9, 50]

# s_new[2:] = 999
# print(s_new.to_list())
# THIS WILL FAIL!!!

##------------------##
## Using .scatter() ##
##------------------##
'''
.scatter(indices, values) is the Polars equivalent of pandas' iloc-assignment.
It returns a NEW Series with the specified positions replaced.
The original Series is NOT modified in place.
'''

s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
s_new = s_old.scatter([0], [100])  # Updating the first element
print(s_new.to_list())
# [100, 20, 30, 40, 50]

s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
s_new = s_old.scatter([1, 2], [200, 300])  # Updating a range of elements by position
print(s_new.to_list())
# [10, 200, 300, 40, 50]

s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
s_new = s_old.scatter([0, 4], [500, 600])  # Updating multiple specific positions
print(s_new.to_list())
# [500, 20, 30, 40, 600]

# Broadcast a single value to multiple positions
s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
s_new = s_old.scatter([1, 2, 3], 999)
print(s_new.to_list())
# [10, 999, 999, 999, 50]

##-------------------------------##
## Conditional updates (pl.when) ##
##-------------------------------##
'''
To update values based on a condition (e.g., "set all values > 25 to 999"),
Polars uses pl.when().then().otherwise() expressions.
'''

# Approach 1: Using .scatter() with a boolean mask's true-indices
s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
mask_indices = (s_old > 25).arg_true()  # Get positions where condition is True
s_conditional = s_old.scatter(mask_indices, 999)
print(s_conditional.to_list())
# [10, 20, 999, 999, 999]

# Approach 2: Using pl.when() inside a DataFrame/select context (more idiomatic for complex logic)
s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
s_conditional = pl.select(
    pl.when(pl.lit(s_old) > 25).then(999).otherwise(pl.lit(s_old))
).to_series()
print(s_conditional.to_list())
# [10, 20, 999, 999, 999]

# =========================================================================================
# 2. Add new elements
# =========================================================================================

##-------------------------------##
## Append: s_old.append(s_extra) ##
##-------------------------------##

# Append many elements
s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
print(s_old.append(pl.Series([8, 9])).to_list())
# [10, 20, 30, 40, 50, 8, 9]

# Append a single element
s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
print(s_old.append(pl.Series([9999])).to_list())
# [10, 20, 30, 40, 50, 9999]

##-------------------------------------------------##
## Prepending: pl.Series([new_vals]).append(s_old) ##
##-------------------------------------------------##

s_old = pl.Series("my_series", [10, 20, 30, 40, 50])
print(pl.Series([-8, -25]).append(s_old).to_list())
# [-8, -25, 10, 20, 30, 40, 50]

##----------------------------##
## Inserting: use pl.concat() ##
##----------------------------##

insert_at = 2
s_inserted = pl.concat([
    s_old.slice(0, insert_at),
    pl.Series("my_series", [111, 222]),
    s_old.slice(insert_at)
])

print(s_inserted.to_list())
# [10, 20, 111, 222, 30, 40, 50]

# =========================================================================================
# 3. Deleting elements
# =========================================================================================

s_old = pl.Series("my_series", [10, 20, 30, 40, 50])

##----------------------------------##
## Drop by POSITION using .gather() ##
##----------------------------------##
'''
Polars has no .drop() method like pandas. To drop by position, gather all
indices EXCEPT the ones you want to remove.
'''

# Drop the element at position 0
keep_idx = [i for i in range(len(s_old)) if i != 0]
print(keep_idx) # [1, 2, 3, 4]
s_dropped = s_old.gather(keep_idx)
print(s_dropped.to_list())
# [20, 30, 40, 50]


# Drop elements at positions 1 and 3
keep_idx = [i for i in range(len(s_old)) if i not in {1, 3}]
print(keep_idx) # [0, 2, 4]
s_dropped = s_old.gather(keep_idx)
print(s_dropped.to_list())
# [10, 30, 50]

##-------------------------------------##
##    Drop by VALUE using .filter()    ##
##-------------------------------------##
'''
Use boolean masks with .filter() to drop elements matching specific values.
This is conceptually similar to pandas' s[s != value] pattern.
'''

# Drop all elements equal to 30
s_dropped = s_old.filter(s_old != 30)
print(s_dropped.to_list())
# [10, 20, 40, 50]

# Drop multiple specific values using is_in() with negation (~)
s_dropped = s_old.filter(~s_old.is_in([20, 40]))
print(s_dropped.to_list())
# [10, 30, 50]

# Drop based on a condition (e.g., drop all values > 25)
s_dropped = s_old.filter(s_old <= 25)
print(s_dropped.to_list())
# [10, 20]

##-------------------------------------##
##         Drop null values            ##
##-------------------------------------##

s_with_nulls = pl.Series("my_series", [10, None, 30, None, 50])
print(
    s_with_nulls
    .drop_nulls()
    .to_list()
)
# [10, 30, 50]
