'''
1. all(): every element is True / non-zero.
2. any(): at least one element is True / non-zero.
3. nonzero(): tuple of coordinate arrays, one per axis.
'''

import numpy as np

arr = np.arange(360).reshape(3, 4, 5, 6)
print(arr.shape)
# (3, 4, 5, 6)

# =========================================================================================
# 1. arr.all() / np.all(arr)
# =========================================================================================
'''
axis=None (default) reduces the whole array to a boolean scalar.
axis=k removes axis k; a tuple reduces multiple axes.
keepdims=True keeps reduced axes with length 1.
'''

print(arr.all())
# False: arr contains a zero

print(np.all(arr >= 0))
# True: every element satisfies the condition

print(arr.all(axis=0).shape)
# (4, 5, 6)

print(arr.all(axis=-1).shape)
# (3, 4, 5)

print(arr.all(axis=(1, 2, 3)))
# [False  True  True]: one boolean per axis-0 block

print(np.all(arr > 0, axis=(2, 3)).shape)
# (3, 4): one boolean per last-two-axis matrix

print(arr.all(axis=(2, 3), keepdims=True).shape)
# (3, 4, 1, 1)

# =========================================================================================
# 2. arr.any() / np.any(arr)
# =========================================================================================

print(arr.any())
# True: at least one element is non-zero

print(np.any(arr < 0))
# False: no element satisfies the condition

print(arr.any(axis=1).shape)
# (3, 5, 6)

print(np.any(arr > 250, axis=(1, 2, 3)))
# [False False  True]

print(np.any(arr > 350, axis=-1, keepdims=True).shape)
# (3, 4, 5, 1)

# Filter complete axis-0 blocks using a 1D reduction mask.
block_mask = np.any(arr > 250, axis=(1, 2, 3))
print(arr[block_mask].shape)
# (1, 4, 5, 6)

# =========================================================================================
# 3. arr.nonzero() / np.nonzero(arr)
# =========================================================================================
'''
For an nD array with N matches, nonzero() returns n arrays of shape (N,).
Entries at the same position form one coordinate tuple.
Coordinates follow C order (last axis varies fastest).
'''

indices = arr.nonzero()  # Also: np.nonzero(arr)
print(len(indices))
# 4: one index array for each axis

print([idx.shape for idx in indices])
# [(359,), (359,), (359,), (359,)]: all elements except zero

print(arr[indices].shape)
# (359,): use the entire tuple directly to extract matching values

##-------------------------------##
## Find positions of a condition ##
##-------------------------------##

mask = arr >= 357
indices = np.nonzero(mask)

for axis_indices in indices:
    print(axis_indices)
# [2 2 2]
# [3 3 3]
# [4 4 4]
# [3 4 5]
# Coordinates: (2, 3, 4, 3), (2, 3, 4, 4), (2, 3, 4, 5)

print(arr[indices])
# [357 358 359]: same as arr[mask]

##---------------------------------##
## Coordinates grouped by element  ##
##---------------------------------##

coordinates = np.argwhere(mask)
print(coordinates)
# [[2 3 4 3]
#  [2 3 4 4]
#  [2 3 4 5]]

print(coordinates.shape)
# (3, 4): (number of matches, ndim)
# argwhere groups coordinates for inspection; use nonzero for indexing.

print(np.flatnonzero(mask))
# [357 358 359]: flat C-order indices, rather than nD coordinates

print(np.count_nonzero(mask))
# 3: count matches without constructing coordinate arrays

print(np.count_nonzero(mask, axis=-1).shape)
# (3, 4, 5): counts along the selected axis
