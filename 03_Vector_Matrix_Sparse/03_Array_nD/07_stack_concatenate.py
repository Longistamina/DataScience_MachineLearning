'''
1. Stack: np.stack(arrays, axis=0)
   + Concatenates a sequence of arrays along a NEW dimension.

2. Concatenate: np.concatenate(arrays, axis=0)
   + Joins a sequence of arrays along an EXISTING dimension.
   + All arrays must have the same shape except in the dimension being concatenated.
'''

import numpy as np

arr1 = np.random.rand(3, 4, 5, 6)
arr2 = np.random.rand(3, 4, 5, 6)

# ==============================================================
# 1. Stack: np.stack(arrays, axis=0)
# ==============================================================

print(
    np.stack((arr1, arr2), axis=0)
    .shape
)
# (2, 3, 4, 5, 6)

print(
    np.stack((arr1, arr2), axis=2)
    .shape
)
# (3, 4, 2, 5, 6)

print(
    np.stack((arr1, arr2), axis=-1)
    .shape
)
# (3, 4, 5, 6, 2)

# ==============================================================
# 2. Concatenate: np.concatenate(arrays, axis=0)
# ==============================================================

print(
    np.concatenate((arr1, arr2), axis=0)
    .shape
)
# (6, 4, 5, 6)

print(
    np.concatenate((arr1, arr2), axis=1)
    .shape
)
# (3, 8, 5, 6)

print(
    np.concatenate((arr1, arr2), axis=-1)
    .shape
)
# (3, 4, 5, 12)
