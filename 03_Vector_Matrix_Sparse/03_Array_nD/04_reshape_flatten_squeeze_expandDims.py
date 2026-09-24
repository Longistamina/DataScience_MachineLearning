'''
1. arr.reshape(dimension) for 2D matrix:
   + arr.reshape()
   + arr.reshape(d1, d2, ..., -1)
   + arr.reshape(-1, d2, d3, ..., dn)
   + arr.reshape(d1, d2, ..., -1, ..., dn)
   + arr.reshape(-1, 1): convert to column vector
   + arr.reshape(1, -1): convert to row vector
   + arr.reshape(-1):   flatten to 1D vector
   + np.reshape(arr, newshape): similar to arr.reshape(newshape)

2. Flatten and Ravel: convert back to 1D vector
   + arr.flatten(): convert back to 1D vector, returns a copy
   + arr.ravel(): convert back to 1D vector, returns a view whenever possible (same memory when possible)
   + np.ravel(arr): similar to arr.ravel()

3. arr.resize(dimension): Similar to reshape,
                          But if the new array is larger than the original array,
                          then the new array is filled with zeros
                          (and it modifies the original array in-place)
   + np.resize(arr, newshape): resize with repeated copies of the original array

4. Squeeze:
    + arr.squeeze(): Remove single-dimensional entries from the shape of an array
    + np.squeeze(arr): similar to arr.squeeze()

5. Expand dimensions with `np.expand_dims`:
    + np.expand_dims(arr, axis): Expand the shape of an array by inserting a new axis at the specified position

6. Expand dimensions with `np.newaxis` and `None`:
    + arr[np.newaxis, :, :] ||| arr[np.newaxis, ...]: equivalent to np.expand_dims(arr, axis=0)
    + arr[:, np.newaxis, :]: equivalent to np.expand_dims(arr, axis=1)
    + arr[:, :, np.newaxis] ||| arr[..., np.newaxis]: equivalent to np.expand_dims(arr, axis=2)
    + arr[:, None, :]: use None instead of np.newaxis also works
'''

import numpy as np

np.random.seed(42)
arr = np.random.rand(2, 3, 4, 5)

print(arr.shape)
# (2, 3, 4, 5)

# =========================================================================================
# 1. arr.reshape(dimension)
# =========================================================================================

##---------------##
## arr.reshape() ##
##---------------##

print(
    arr.reshape(2, 12, 5)
    .shape
)
# (2, 12, 5)

print(
    arr.reshape(8, 15)
    .shape
)
# (8, 15)

##------------------------------##
## arr.reshape(d1, d2, ..., -1) ##
##------------------------------##

print(
    arr.reshape(2, 3, -1)
    .shape
)
# (2, 3, 20)

##-----------------------------------##
## arr.reshape(-1, d2, d3, ..., dn ) ##
##-----------------------------------##

print(
    arr.reshape(-1, 2, 2, 3)
    .shape
)
# (10, 2, 2, 3)

##---------------------------------------##
## arr.reshape(d1, d2, ..., -1, ..., dn) ##
##---------------------------------------##

print(
    arr.reshape(2, 2, -1, 5)
    .shape
)
# (2, 2, 6, 5)

##----------------------------------------------##
## arr.reshape(-1, 1): convert to column vector ##
##----------------------------------------------##

print(
    arr.reshape(-1, 1)
    .shape
)
# (120, 1)

##-------------------------------------------##
## arr.reshape(1, -1): convert to row vector ##
##-------------------------------------------##

print(
    arr.reshape(1, -1)
    .shape
)
# (1, 120)

##-----------------------------------------##
## arr.reshape(-1):   flatten to 1D vector ##
##-----------------------------------------##

print(
    arr.reshape(-1)
    .shape
)
# (120,)

##-------------------------------------------------------------##
## np.reshape(arr, newshape): similar to arr.reshape(newshape) ##
##-------------------------------------------------------------##

print(
    np.reshape(arr, (2, 2, -1, 5))
    .shape
)
# (2, 2, 6, 5)

# =========================================================================================
# 2. Flatten and Ravel: convert back to 1D vector
# =========================================================================================

##-------------##
## arr.flatten ##
##-------------##

print(
    arr.flatten()
    .shape
)
# (120,)

##-----------##
## arr.ravel ##
##-----------##

print(
    arr.ravel()
    .shape
)
# (120,)

##------------##
## np.ravel() ##
##------------##

print(
    np.ravel(arr)
    .shape
)
# (120,)

# =========================================================================================
# 3. arr.resize(dimension): similar to reshape
# =========================================================================================
'''
arr.resize(dimension):
   Similar to reshape, but:
   - modifies the original array in-place
   - if the new size is larger, fills with zeros
   - returns None

np.resize(arr, newshape):
   - returns a new array
   - if newshape is larger, fills with repeated copies of the original data
'''


np.random.seed(2)
matrix3 = np.random.randint(1, 21, size=(4, 5))

print(matrix3)
# [[ 9 16 14  9 12]
#  [19 12  9  8  3]
#  [18 12 16  6  8]
#  [ 4  7  5 11 12]]
# shape: (4, 5)

##--------------------##
## arr.resize (bigger)##
##--------------------##

matrix3.resize((6, 5))
print(matrix3)
# [[ 9 16 14  9 12]
#  [19 12  9  8  3]
#  [18 12 16  6  8]
#  [ 4  7  5 11 12]
#  [ 0  0  0  0  0]
#  [ 0  0  0  0  0]]
# shape: (6, 5)
# original modified in-place, extra rows filled with zeros

##----------------------##
## arr.resize (smaller) ##
##----------------------##

matrix3.resize((3, 4))
print(matrix3)
# [[ 9 16 14  9]
#  [12 19 12  9]
#  [ 8  3 18 12]]
# shape: (3, 4)
# truncated in-place

##-------------##
## np.resize() ##
##-------------##

np.random.seed(3)
matrix4 = np.random.randint(1, 21, size=(4, 5))
print(matrix4)
# [[11  4  9  1 20]
#  [11 12 10 11  7]
#  [ 1 13  8 15 18]
#  [ 3  3  2 20  6]]
# original remains unchanged

print(np.resize(matrix4, (6, 5)))
# [[11  4  9  1 20]
#  [11 12 10 11  7]
#  [ 1 13  8 15 18]
#  [ 3  3  2 20  6]
#  [11  4  9  1 20]
#  [11 12 10 11  7]]
# shape: (6, 5)
# repeated copies of original data to fill larger size

print(np.resize(matrix4, (3, 8)))
# [[11  4  9  1 20 11 12 10]
#  [11  7  1 13  8 15 18  3]
#  [ 3  2 20  6 11  4  9  1]]
# shape: (3, 8)
# repeated copies with new shape

print(matrix4)
# original matrix4 is unchanged

# =========================================================================================
# 4. Squeeze: remove 1-sized dims
# =========================================================================================
'''
Examples:
   (1, n) -> (n,)
   (n, 1) -> (n,)
   (m, n, 1) -> (m, n)
   (1, m, n) -> (m, n)
   (m, 1, n) -> (m, n)
   (1, m, 1, n, 1, 1) -> (m, n)

   (n,) -> unchanged
   (m, n) with m>1 and n>1 -> unchanged
'''

arr_excessive = np.random.rand(1, 3, 1, 1, 2, 4)

print(arr_excessive.squeeze().shape)
# (3, 2, 4)

# =========================================================================================
# 5. Expand dimensions with `np.expand_dims`:
# =========================================================================================

print(
    np.expand_dims(arr, axis=0)
    .shape
)
# (1, 2, 3, 4, 5)

print(
    np.expand_dims(arr, axis=3)
    .shape
)
# (2, 3, 4, 1, 5)

print(
    np.expand_dims(arr, axis=(1, 3))
    .shape
)
# (2, 1, 3, 1, 4, 5)
'''
(2, 3, 4, 5) -> (2, 1, 3, 4, 5) # new axis at index=1 (between 2-3)
(2, 1, 3, 1, 4, 5) -> (2, 1, 3, 4, 5) # new axis at index=3 (between 4-5)
'''

# =========================================================================================
# 6. Expand dimensions with `np.newaxis` and `None`
# =========================================================================================

##-------------------##
## with `np.newaxis` ##
##-------------------##

print(
    arr[:, :, :, np.newaxis, :]
    .shape
)
# (2, 3, 4, 1, 5)

print(
    arr[..., np.newaxis, :]
    .shape
)
# (2, 3, 4, 1, 5)

print(
    arr[np.newaxis, :, np.newaxis, ...]
    .shape
)
# (1, 2, 1, 3, 4, 5)

##-------------##
## with `None` ##
##-------------##

print(
    arr[:, :, :, None, :]
    .shape
)
# (2, 3, 4, 1, 5)

print(
    arr[..., None, :]
    .shape
)
# (2, 3, 4, 1, 5)

print(
    arr[None, :, None, ...]
    .shape
)
# (1, 2, 1, 3, 4, 5)
