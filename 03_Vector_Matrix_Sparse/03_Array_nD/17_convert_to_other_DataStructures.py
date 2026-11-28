'''
1. tolist(): recursively nested Python lists.
2. Nested tuples: recursively convert every list level.
3. flatten / ravel: 1D arrays, flat lists, tuples, and sets.
4. pandas DataFrame: select a 2D slice or reshape explicitly.
'''

import numpy as np
import pandas as pd

arr = np.arange(360).reshape(3, 4, 5, 6)
print(arr.shape)
# (3, 4, 5, 6)

# =========================================================================================
# 1. arr.tolist(): preserves nesting at every axis
# =========================================================================================

nested_list = arr.tolist()
print([len(nested_list), len(nested_list[0]),
       len(nested_list[0][0]), len(nested_list[0][0][0])])
# [3, 4, 5, 6]

print(nested_list[0][0][0])
# [0, 1, 2, 3, 4, 5]

print(type(nested_list[0][0][0][0]))
# <class 'int'>: tolist() converts these NumPy scalars to Python scalars

# =========================================================================================
# 2. Nested tuples
# =========================================================================================
# tuple(map(tuple, arr)) converts only two levels; deeper arrays remain.


def to_nested_tuple(value):
    if isinstance(value, list):
        return tuple(to_nested_tuple(item) for item in value)
    return value


nested_tuple = to_nested_tuple(arr.tolist())
print(nested_tuple[0][0][0])
# (0, 1, 2, 3, 4, 5)

print(type(nested_tuple[0][0][0]))
# <class 'tuple'>: all container levels are tuples

# =========================================================================================
# 3. Flattening and flat Python containers
# =========================================================================================

print(arr.flatten().shape)
# (360,): always returns a copy

print(arr.ravel().shape)
# (360,): returns a view when possible, otherwise a copy
# Default order='C': last axis varies fastest.

flat_list = arr.ravel().tolist()
flat_tuple = tuple(flat_list)
unique_values = set(flat_list)
print(len(flat_list), len(flat_tuple), len(unique_values))
# 360 360 360
# A set removes duplicates and does not preserve array order or shape.

# =========================================================================================
# 4. pandas DataFrame: needs 2D input
# =========================================================================================
# pd.DataFrame(arr) would fail for a 4D array. Choose a mapping explicitly.

##-----------------------##
## One 2D slice          ##
##-----------------------##

df_slice = pd.DataFrame(arr[0, 0])
print(df_slice.shape)
# (5, 6)

##-----------------------------------##
## Combine leading axes into rows    ##
##-----------------------------------##

df_flat_rows = pd.DataFrame(arr.reshape(-1, arr.shape[-1]))
print(df_flat_rows.shape)
# (60, 6): (3 * 4 * 5) rows, last axis as columns

# Keep original leading coordinates as a MultiIndex.
index = pd.MultiIndex.from_product(
    [range(size) for size in arr.shape[:-1]],
    names=['axis_0', 'axis_1', 'axis_2'],
)
df_indexed = pd.DataFrame(arr.reshape(-1, arr.shape[-1]), index=index)
print(df_indexed.loc[(1, 2, 3)].tolist())
# [198, 199, 200, 201, 202, 203]

##----------------------------------##
## One coordinate and value per row ##
##----------------------------------##

coordinates = np.indices(arr.shape).reshape(arr.ndim, -1).T
df_long = pd.DataFrame(coordinates, columns=['axis_0', 'axis_1', 'axis_2', 'axis_3'])
df_long['value'] = arr.ravel()
print(df_long.shape)
# (360, 5): four coordinate columns plus one value column
# Explicit coordinates preserve how each value maps back to the nD array.
