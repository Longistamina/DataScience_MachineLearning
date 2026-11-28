'''
1. Sorting: sort along any axis, descending order, flattening, kind.
2. Indirect sorting: argsort(), argmax(), argmin(), argpartition().
3. Multiple keys: np.lexsort(); last key is primary.
'''

import numpy as np

# Deterministic, unsorted values with the same 4D shape as earlier demos.
arr = (np.arange(360) * 7 % 361).reshape(3, 4, 5, 6)
print(arr.shape)
# (3, 4, 5, 6)

print(arr[0, 1, 3, :])
# [336 343 350 357   3  10]

# =========================================================================================
# 1. Sorting
# =========================================================================================
'''
np.sort(arr) returns a sorted copy; arr.sort() modifies in place, returns None.
Along axis k, sort each 1D slice independently; the shape stays unchanged.
Default axis=-1. These operations do not reorder whole nD blocks together.
'''

arr_demo = arr.copy()
arr_demo.sort(axis=1)
print(arr_demo.shape)
# (3, 4, 5, 6)

print(np.sort(arr, axis=0).shape)
# (3, 4, 5, 6)

print(np.sort(arr, axis=-1)[0, 1, 3, :])
# [  3  10 336 343 350 357]

##-----------------##
## Descending sort ##
##-----------------##

print(np.sort(arr, axis=-1)[..., ::-1][0, 1, 3, :])
# [357 350 343 336  10   3]

# For any axis, reverse that SAME axis with np.flip().
axis = 2
print(np.flip(np.sort(arr, axis=axis), axis=axis).shape)
# (3, 4, 5, 6)

##------------------##
## Flatten and sort ##
##------------------##

print(np.sort(arr, axis=None).shape)
# (360,)

flat = arr.flatten()
flat.sort()  # In-place method alternative for the flattened copy
print(flat.shape)
# (360,)

##------------------##
## Sorting kind     ##
##------------------##

print(np.sort(arr, axis=1, kind='stable').shape)
# (3, 4, 5, 6)
# kind: 'quicksort', 'mergesort', 'heapsort', 'stable'.
# Stable sorting preserves the original order of equal keys.

# =========================================================================================
# 2. Indirect sorting and selection
# =========================================================================================

##---------------------##
## argsort(): indices  ##
##---------------------##

indices = arr.argsort(axis=-1)  # Also: np.argsort(arr, axis=-1)
print(indices.shape)
# (3, 4, 5, 6): indices refer to positions along the selected axis

print(indices[0, 1, 3, :])
# [4 5 0 1 2 3]

sorted_arr = np.take_along_axis(arr, indices, axis=-1)
print(sorted_arr[0, 1, 3, :])
# [  3  10 336 343 350 357]

indices_desc = np.flip(indices, axis=-1)
print(np.take_along_axis(arr, indices_desc, axis=-1)[0, 1, 3, :])
# [357 350 343 336  10   3]
# Reversing ascending indices also reverses ties, even after a stable sort.

print(np.argsort(arr, axis=1, kind='stable').shape)
# (3, 4, 5, 6)

##---------------------##
## argmax() / argmin() ##
##---------------------##

print(arr.argmax(axis=1).shape)
# (3, 5, 6): the selected axis is removed

indices_max = np.argmax(arr, axis=-1, keepdims=True)
print(indices_max.shape)
# (3, 4, 5, 1): keepdims allows direct use with take_along_axis()

print(np.take_along_axis(arr, indices_max, axis=-1)[0, 1, 3, :])
# [357]

indices_min = arr.argmin(axis=-1, keepdims=True)
print(np.take_along_axis(arr, indices_min, axis=-1)[0, 1, 3, :])
# [3]

flat_index = arr.argmax()  # axis=None: index into the C-order flattened array
print(arr.flat[flat_index])
# 360

print(len(np.unravel_index(flat_index, arr.shape)))
# 4: converts the flat index to one coordinate per axis
# argmax/argmin accept one axis or None, not a tuple of axes.

##--------------------------------##
## argpartition(): k smallest     ##
##--------------------------------##

k = 2
indices_k = np.argpartition(arr, kth=k - 1, axis=-1)[..., :k]
smallest = np.take_along_axis(arr, indices_k, axis=-1)
print(smallest.shape)
# (3, 4, 5, 2)

print(np.sort(smallest, axis=-1)[0, 1, 3, :])
# [ 3 10]
# kth is zero-based. The first k positions contain the k smallest values,
# but their internal order is NOT guaranteed; sort them if needed.
# Method equivalent: arr.argpartition(kth=k - 1, axis=-1).

# =========================================================================================
# 3. np.lexsort(): sort using multiple keys
# =========================================================================================
'''
Each key can be nD; all keys must have the same shape.
The last key is primary; earlier keys break ties.
The axis refers to an axis WITHIN each key array.
'''

primary = arr % 3
secondary = arr
indices_lex = np.lexsort((secondary, primary), axis=-1)
print(indices_lex.shape)
# (3, 4, 5, 6)

print(np.take_along_axis(arr, indices_lex, axis=-1)[0, 1, 3, :])
# [  3 336 357  10 343 350]
# Ordered by arr % 3 first, then by arr within each group.
