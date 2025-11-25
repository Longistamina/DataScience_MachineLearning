'''
# arr.ndim: the number of dimensions (axes) of the array.
# arr.shape: a tuple representing the size of the array along each dimension.
# arr.size: the total number of elements in the array.
# arr.dtype: the data type of the elements in the array.
# arr.itemsize: the size (in bytes) of each element in the array.
# arr.nbytes: the total number of bytes consumed by the array's elements.
'''

import numpy as np

vector = np.load('03_Vector_Matrix_Sparse/01_Vector_1D/data/timeseries.npy')

print(vector)
# [49. 49. 49. 49. 49. 50. 50. 50. 51. 56. 61. 66. 70. 72. 74. 76. 75. 73.
#  70. 67. 64. 62. 60. 59. 57. 56. 54. 53. 52. 52. 51. 50. 50. 49. 49. 49.
#  48. 48. 48. 48. 48. 48. 48. 47. 47. 47. 47. 47. 47. 47. 48. 48. 48. 48.
#  48. 48. 48. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49.
#  49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 49. 50. 50. 50.
#  50. 50. 50. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 50. 50. 50. 51. 51. 51. 51. 51. 51. 50. 50. 50. 50. 51. 51.
#  51. 51. 51. 51. 51. 51. 52. 52. 52. 52. 51. 51. 51. 51. 51. 51. 51. 51.
#  51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 51. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 53. 53. 52. 52. 52. 52.
#  52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52. 52.]

##############
## arr.ndim ##
##############

print(vector.ndim)
# 1 
# (1 dimension, i.e., 1D vector)

###############
## arr.shape ##
###############

print(vector.shape)
# (305,)
# (305 elements along the only 1 dimension)

##############
## arr.size ##
##############

print(vector.size)
# 305
# (Total number of elements in the array)

###############
## arr.dtype ##
###############

print(vector.dtype)
# float64
# (Data type of the elements in the array)

##################
## arr.itemsize ##
##################

print(vector.itemsize)
# 8
# (Each float64 element takes 8 bytes)

################
## arr.nbytes ##
################

print(vector.nbytes)
# 2440
# (Total bytes = 305 elements * 8 bytes/element = 2440 bytes)