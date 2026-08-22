'''
1. np.asarray()
2. np.asmatrix()
3. np.asarray_chkfinite()
'''

import numpy as np


# =========================================================================================
# 1. np.asarray()
# =========================================================================================
'''
np.asarray() is used to convert the input to an array.
It is similar to np.array(), but it does not copy the data if the input is already an array.
This can be more efficient in terms of memory and performance.

BUT: when the new created array is modified, the original array will also be modified, since they share the same memory location.
-> in those cases, for safety, use np.array() since it always creates a copy of the data.
'''

lst = [1, 2, 3]

arr_lst = np.asarray(lst)
print(arr_lst) # [1 2 3]

# 
tup = (
    (1, 2, 3),
    (4, 5, 6)
)

arr_tup = np.asarray(tup)
print(arr_tup)
# [[1 2 3]
#  [4 5 6]]

# 
arr = np.arange(0, 24).reshape(2, 3, 4)

arr_asarr = np.asarray(arr)
print(arr_asarr)
# [[[ 0  1  2  3]
#   [ 4  5  6  7]
#   [ 8  9 10 11]]

#  [[12 13 14 15]
#   [16 17 18 19]
#   [20 21 22 23]]]


# =========================================================================================
# 2. np.asmatrix()
# =========================================================================================
'''
np.asmatrix() is used to convert the input to a matrix.
It is similar to np.asarray(), but it always returns a 2D array (matrix).

NOTE: if the dimension is greater than 2, it will raise a ValueError: shape too large to be a matrix.
'''

lst = [1, 2, 3]

mat_lst = np.asmatrix(lst)
print(mat_lst) # [[1 2 3]]

# 
tup = (
    (1, 2, 3),
    (4, 5, 6)
)

mat_tup = np.asmatrix(tup)
print(mat_tup)
# [[1 2 3]
#  [4 5 6]]

# 
arr = np.arange(0, 24).reshape(2, 3, 4)

mat_arr = np.asmatrix(arr)
print(mat_arr)
'''ValueError: shape too large to be a matrix.'''


# =========================================================================================
# 3. np.asarray_chkfinite()
# =========================================================================================
'''
np.asarray_chkfinite() is used to convert the input to an array, but it also checks for NaN and Inf values.
If the input contains NaN or Inf values, it will raise a ValueError: array must not contain infs or NaNs.
'''

arr_nan = np.array([1, 2, 3, np.nan])
arr_chkfinite = np.asarray_chkfinite(arr_nan)
'''ValueError: array must not contain infs or NaNs'''

arr_inf = np.array([1, 2, 3, np.inf])
arr_chkfinite = np.asarray_chkfinite(arr_inf)
'''ValueError: array must not contain infs or NaNs'''

arr_normal = np.array([1, 2, 3, 4])
arr_chkfinite = np.asarray_chkfinite(arr_normal)
print(arr_chkfinite) # [1 2 3 4]
