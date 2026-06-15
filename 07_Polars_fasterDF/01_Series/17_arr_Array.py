'''
In Polars, there are TWO distinct nested data types:
1. pl.List: Variable-length lists (accessed via the `.list` namespace).
2. pl.Array: Fixed-length arrays (accessed via the `.arr` namespace).

The `.arr` namespace is specifically for `pl.Array`, where EVERY sub-array
in the column MUST have the exact same predefined width (e.g., 3D coordinates, RGB colors, embeddings).
Because the width is fixed and known at compile time, `.arr` operations are
highly optimized, strictly typed, and memory-efficient compared to `.list` operations.

######################################################
0. Creation: pl.Array(inner_type, width)
1. Aggregation & Reduction (sum, mean, min, max, etc.)
2. Boolean Aggregation (all, any)
3. Element Access & Indexing (first, last, get, arg_min, arg_max)
4. Searching & Counting (contains, count_matches, n_unique, unique)
5. Transformation & Manipulation (sort, reverse, shift, join, eval)
6. Structural Operations (len, explode, to_list)
'''

import polars as pl


#-------------------------------------------------------------------------------------------------#
#-------------------------------------- 0. Creation ----------------------------------------------#
#-------------------------------------------------------------------------------------------------#
'''
To create a fixed-size Array Series, you must explicitly define the dtype
using pl.Array(inner_dtype, width).
'''

# Create a fixed-size Array Series (e.g., 3D coordinates)
s_coords = pl.Series(
    "coords",
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    dtype=pl.Array(pl.Int64, 3)
)
print(s_coords)
# shape: (3,)
# Series: 'coords' [array[i64, 3]]
# [
# 	[1, 2, 3]
# 	[4, 5, 6]
# 	[7, 8, 9]
# ]


#-------------------------------------------------------------------------------------------------#
#-------------------------------- 1. Aggregation & Reduction -------------------------------------#
#-------------------------------------------------------------------------------------------------#

s_nums = pl.Series(
    "nums",
    [[1, 2, 3], [4, 5, 6], [10, 0, -10]],
    dtype=pl.Array(pl.Int64, 3)
)

# Compute the sum values of the sub-arrays
print(s_nums.arr.sum())
# [6, 15, 0]

# Compute the mean of the values of the sub-arrays
print(s_nums.arr.mean())
# [2.0, 5.0, 0.0]

# Compute the median of the values of the sub-arrays
print(s_nums.arr.median())
# [2.0, 5.0, 0.0]

# Compute the min/max values of the sub-arrays
print(s_nums.arr.min()) # [1, 4, -10]
print(s_nums.arr.max()) # [3, 6, 10]


# Compute the var/std of the values of the sub-arrays
print(s_nums.arr.var())
print(s_nums.arr.std())


#-------------------------------------------------------------------------------------------------#
#----------------------------------- 2. Boolean Aggregation --------------------------------------#
#-------------------------------------------------------------------------------------------------#

s_bools = pl.Series(
    "bools",
    [[True, True], [False, True], [False, False]],
    dtype=pl.Array(pl.Boolean, 2)
)

# Evaluate whether ALL boolean values are true for every subarray
print(s_bools.arr.all())
# [true, false, false]

# Evaluate whether ANY boolean value is true for every subarray
print(s_bools.arr.any())
# [true, true, false]


#-------------------------------------------------------------------------------------------------#
#--------------------------- 3. Element Access & Indexing ----------------------------------------#
#-------------------------------------------------------------------------------------------------#

s_nums = pl.Series(
    "nums",
    [[10, 20, 30], [40, 5, 60], [7, 80, 9]],
    dtype=pl.Array(pl.Int64, 3)
)

# Get the first value of the sub-arrays
print(s_nums.arr.first())
# [10, 40, 7]

# Get the last value of the sub-arrays
print(s_nums.arr.last())
# [30, 60, 9]

# Get the value by specific index (0-based) in the sub-arrays
print(s_nums.arr.get(1))
# [20, 5, 80]

# Retrieve the index of the minimal value in every sub-array
print(s_nums.arr.arg_min())
# [0, 1, 0]  (10 is at idx 0; 5 is at idx 1; 7 is at idx 0)

# Retrieve the index of the maximum value in every sub-array
print(s_nums.arr.arg_max())
# [2, 2, 1]  (30 is at idx 2; 60 is at idx 2; 80 is at idx 1)


#-------------------------------------------------------------------------------------------------#
#---------------------------------- 4. Searching & Counting --------------------------------------#
#-------------------------------------------------------------------------------------------------#

s_search = pl.Series(
    "vals",
    [[1, 2, 2], [3, 4, 5], [2, 2, 2]],
    dtype=pl.Array(pl.Int64, 3)
)

# Check if sub-arrays contain the given item (Returns Boolean Series)
print(s_search.arr.contains(2))
# [true, false, true]

# Count how often the given value appears in each sub-array
print(s_search.arr.count_matches(2))
# [2, 0, 3]

# Count the number of unique values in every sub-array
print(s_search.arr.n_unique())
# [2, 3, 1]

# Get the unique/distinct values in the array.
# NOTE: Because the number of unique values varies per row, .arr.unique()
# automatically returns a variable-length pl.List column, NOT a fixed pl.Array!
print(s_search.arr.unique())
# shape: (3,)
# Series: 'vals' [list[i64]]
# [
# 	[1, 2]
# 	[3, 4, 5]
# 	[2]
# ]


#-------------------------------------------------------------------------------------------------#
#----------------------------- 5. Transformation & Manipulation ----------------------------------#
#-------------------------------------------------------------------------------------------------#

s_unsorted = pl.Series(
    "vals",
    [[3, 1, 2], [6, 4, 5], [9, 7, 8]],
    dtype=pl.Array(pl.Int64, 3)
)

# Sort the arrays in this column
print(s_unsorted.arr.sort())
# [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Reverse the arrays in this column
print(s_unsorted.arr.reverse())
# [[2, 1, 3], [5, 4, 6], [8, 7, 9]]

# Shift array values by the given number of indices (pads with nulls)
print(s_unsorted.arr.shift(1))
# [[null, 3, 1], [null, 6, 4], [null, 9, 7]]

####################
## String Joining ##
####################

s_str = pl.Series(
    "words",
    [["a", "b", "c"], ["d", "e", "f"]],
    dtype=pl.Array(pl.String, 3)
)

# Join all string items in a sub-array and place a separator between them
print(s_str.arr.join("-"))
# ["a-b-c", "d-e-f"]

#####################################
## Advanced Evaluation (.arr.eval) ##
#####################################
'''
.arr.eval() allows you to run ANY Polars expression against the elements
inside the sub-arrays. We use pl.element() to reference the inner items.
'''

s_nums = pl.Series("nums", [[1, 2, 3], [4, 5, 6]], dtype=pl.Array(pl.Int64, 3))

# Multiply every element inside the sub-arrays by 10
# (Length preserving -> remains a fixed-width pl.Array)
print(s_nums.arr.eval(pl.element() * 10))
# shape: (2,)
# Series: 'nums' [array[i64, 3]]
# [
# 	[10, 20, 30]
# 	[40, 50, 60]
# ]

# Filter elements inside the sub-arrays
# Because filtering changes the length, the fixed-width Array can no longer hold the result.
# We MUST pass `as_list=True` to tell Polars to output a variable-length pl.List!
print(s_nums.arr.eval(pl.element().filter(pl.element() > 2), as_list=True))
# shape: (2,)
# Series: 'nums' [list[i64]]
# [
# 	[3]
# 	[4, 5, 6]
# ]


#-------------------------------------------------------------------------------------------------#
#---------------------------------- 6. Structural Operations -------------------------------------#
#-------------------------------------------------------------------------------------------------#

s_nums = pl.Series("nums", [[1, 2, 3], [4, 5, 6]], dtype=pl.Array(pl.Int64, 3))

# Return the number of elements in each array (Always returns the fixed width)
print(s_nums.arr.len())
# [3, 3]

# Returns a column with a separate row for every array element (Flattens the Series)
print(s_nums.arr.explode())
# shape: (6,)
# Series: 'nums' [i64]
# [
# 	1
# 	2
# 	3
# 	4
# 	5
# 	6
# ]

# Convert an Array column into a List column with the same inner data type
print(s_nums.arr.to_list())
# shape: (2,)
# Series: 'nums' [list[i64]]
# [
# 	[1, 2, 3]
# 	[4, 5, 6]
# ]
