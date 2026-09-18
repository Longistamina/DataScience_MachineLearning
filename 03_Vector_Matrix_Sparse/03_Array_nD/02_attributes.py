'''
Core attributes:
- arr.ndim: number of dimensions (axes) of the array.
- arr.shape: tuple representing the size of the array along each dimension.
- arr.size: total number of elements in the array.
- arr.dtype: data type of the elements in the array.
- arr.itemsize: size (in bytes) of each element in the array.
- arr.nbytes: total number of bytes consumed by the array's elements.
'''

import numpy as np

arr_3d = np.random.rand(2, 3, 4)
arr_4d = np.random.rand(3, 2, 4, 5)

##----------##
## arr.ndim ##
##----------##

print(arr_3d.ndim)
# 3

print(arr_4d.ndim)
# 4

##-----------##
## arr.shape ##
##-----------##

print(arr_3d.shape)
# (2, 3, 4)

print(arr_4d.shape)
# (3, 2, 4, 5)

##----------##
## arr.size ##
##----------##

print(arr_3d.size)
# 24

print(arr_4d.size)
# 120

##-----------##
## arr.dtype ##
##-----------##

print(arr_3d.dtype)
# float64

print(arr_4d.dtype)
# float64

##--------------##
## arr.itemsize ##
##--------------##

print(arr_3d.itemsize)
# 8
# (each float64 element takes 8 bytes)

print(arr_4d.itemsize)
# 8

##------------##
## arr.nbytes ##
##------------##

print(arr_3d.nbytes)
# 192
# (Total bytes = 24 elements * 8 bytes = 192 bytes)

print(arr_4d.nbytes)
# 960
