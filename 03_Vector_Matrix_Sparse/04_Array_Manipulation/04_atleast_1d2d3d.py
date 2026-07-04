'''
1. np.atleast_1d()
2. np.atleast_2d()
3. np.atleast_3d()
'''

import numpy as np

scalar = 5
vector = np.array([1, 2, 3])

matrix = np.array([[1, 2, 3], [4, 5, 6]])
# [[1, 2, 3],
#  [4, 5, 6]]

tensor = np.array([[[1, 2, 3, 4], [5, 6, 7, 8]], [[9, 10, 11, 12], [13, 14, 15, 16]]])
# [[[ 1,  2,  3,  4],
#   [ 5,  6,  7,  8]],
#
#  [[ 9, 10, 11, 12],
#   [13, 14, 15, 16]]]


#--------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. np.atleast_1d() ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
np.atleast_1d() converts the input to an array with at least one dimension.
If the input is a scalar, it will be converted to a 1D array.
If the input is already an array with one or more dimensions, it will be returned unchanged.
'''

print(np.atleast_1d(scalar))  # [5]
print(np.atleast_1d(vector))  # [1 2 3]

print(np.atleast_1d(matrix))
# [[1 2 3]
#  [4 5 6]]

print(np.atleast_1d(tensor))
# [[[ 1  2  3  4]
#   [ 5  6  7  8]]

#  [[ 9 10 11 12]
#   [13 14 15 16]]]


#--------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. np.atleast_2d() ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
np.atleast_2d() converts the input to an array with at least two dimensions.
If the input is a scalar, it will be converted to a 2D array with shape (1, 1).
If the input is a 1D array, it will be converted to a 2D array with shape (1, N), where N is the length of the input array.
If the input is already an array with two or more dimensions, it will be returned unchanged.
'''

print(np.atleast_2d(scalar)) # [[5]]
print(np.atleast_2d(vector)) # [[1 2 3]]

print(np.atleast_2d(matrix))
# [[1 2 3]
#  [4 5 6]]

print(np.atleast_2d(tensor))
# [[[ 1  2  3  4]
#   [ 5  6  7  8]]

#  [[ 9 10 11 12]
#   [13 14 15 16]]]


#--------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. np.atleast_3d() ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
'''
np.atleast_3d() converts the input to an array with at least three dimensions.
If the input is a scalar, it will be converted to a 3D array with shape (1, 1, 1).
If the input is a 1D array, it will be converted to a 3D array with shape (1, N, 1), where N is the length of the input array.
If the input is a 2D array, it will be converted to a 3D array with shape (M, N, 1), where M and N are the dimensions of the input array.
If the input is already an array with three or more dimensions, it will be returned unchanged.
'''

print(np.atleast_3d(scalar)) # [[[5]]]

print(np.atleast_3d(vector))
# [[[1]
#   [2]
#   [3]]]

print(np.atleast_3d(matrix))
# [[[1]
#   [2]
#   [3]]

#  [[4]
#   [5]
#   [6]]]

print(np.atleast_3d(tensor))
# [[[ 1  2  3  4]
#   [ 5  6  7  8]]

#  [[ 9 10 11 12]
#   [13 14 15 16]]]
