'''
1. arr.copy(): Creates a copy of the array.

2. arr.astype(new_dtype): Converts the array to a different data type.
'''

import numpy as np

arr_3d = np.random.rand(2, 3, 4)
arr_4d = np.random.rand(3, 2, 4, 5)

# =========================================================================================
# 1. array.copy(): Creates a copy of the array.
# =========================================================================================

copied_arr_3d = arr_3d.copy()
print(id(copied_arr_3d) == id(arr_3d))
# False

copied_arr_4d = arr_4d.copy()
print(id(copied_arr_4d) == id(arr_4d))
# False

'''
By using array.copy(), we create a new array that is a copy of the original array.
So when the original array is modified, the copied array remains unchanged, as they occupy different memory locations.
'''

# =========================================================================================
# 2. array.astype(new_dtype): Converts the array to a different data type.
# =========================================================================================

int_arr_3d = arr_3d.astype(np.int32)
print(int_arr_3d.dtype)
# int32

cmplx_arr_4d = arr_4d.astype(np.complex64)
print(cmplx_arr_4d.dtype)
# complex64

'''
All numpy data types are here: https://numpy.org/doc/stable/user/basics.types.html
'''
