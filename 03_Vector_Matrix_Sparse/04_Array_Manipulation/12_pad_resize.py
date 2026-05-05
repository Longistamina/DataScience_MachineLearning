'''
1. np.pad(): pad an array
2. np.resize(): return a new array with the specified shape.
'''

import numpy as np

vector = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

matrix = np.arange(20).reshape(4, 5)
print(matrix)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]]

tensor = np.arange(30).reshape(2, 3, 5)
print(tensor)
# [[[ 0  1  2  3  4]
#   [ 5  6  7  8  9]
#   [10 11 12 13 14]]
#
#  [[15 16 17 18 19]
#   [20 21 22 23 24]
#   [25 26 27 28 29]]]


#------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. np.pad() --------------------------------------------------#
#------------------------------------------------------------------------------------------------------------#
'''
numpy.pad(array, pad_width, mode='constant', **kwargs)

pad_width: Number of values padded to the edges of each axis. ((before_1, after_1), ... (before_N, after_N))
'''

####################
## vector padding ##
####################

vector_padded = np.pad(vector, (2, 3), 'constant') # constant_values=0 by default
print(vector_padded)
# [ 0  0  1  2  3  4  5  6  7  8  9 10  0  0  0]
# (2, 3) -> pad two 0 numbers on the left, three 0 numbers on the right

vector_padded = np.pad(vector, (0, 4), 'constant', constant_values=9)
print(vector_padded)
# [ 1  2  3  4  5  6  7  8  9 10  9  9  9  9]
# (0, 4) -> pad four 9 numbers to the right

vector_padded = np.pad(vector, (2, 3), 'edge')
print(vector_padded)
# [ 1  1  1  2  3  4  5  6  7  8  9 10 10 10 10]
# Use the values on the ends/edges to pad

vector_padded = np.pad(vector, (4, 4), 'minimum')
print(vector_padded)
# [ 1  1  1  1  1  2  3  4  5  6  7  8  9 10  1  1  1  1]
# 'minimum': use min value (along an axis) to pad
# 'maximum': use max value (along an axis) to pad
# 'mean': use mean value (along an axis) to pad
# 'median': use median value (along an axis) to pad

#-------------#

vector_padded = np.pad(vector.reshape(1, -1), ((2, 4), (0, 0)), 'constant', constant_values=1)
print(vector_padded)
# [[ 1  1  1  1  1  1  1  1  1  1]
#  [ 1  1  1  1  1  1  1  1  1  1]
#  [ 1  2  3  4  5  6  7  8  9 10]
#  [ 1  1  1  1  1  1  1  1  1  1]
#  [ 1  1  1  1  1  1  1  1  1  1]
#  [ 1  1  1  1  1  1  1  1  1  1]
#  [ 1  1  1  1  1  1  1  1  1  1]]
'''
((2, 4), (0, 0))

(2, 4) -> dim0
2 -> before_pad dim0
4 -> after_pad dim0
'''

vector_padded = np.pad(vector.reshape(1, -1), ((0, 2), (3, 4)), 'constant', constant_values=((0, 1), (0, 0)))
print(vector_padded)
# [[ 0  0  0  1  2  3  4  5  6  7  8  9 10  0  0  0  0]
#  [ 0  0  0  1  1  1  1  1  1  1  1  1  1  0  0  0  0]
#  [ 0  0  0  1  1  1  1  1  1  1  1  1  1  0  0  0  0]]

'''
((0, 2), (3, 4))

(0, 2) -> dim0
0 -> before_pad dim0 with value=0 (actually no pad)
2 -> after_pad dim0 with value=1

(3, 4) -> dim1
3 -> before_pad dim1 with value=0
4 -> after_pad dim1 with value=0
'''

####################
## matrix padding ##
####################

matrix_padded = np.pad(matrix, ((1, 1), (1, 1)), 'constant', constant_values=0)
print(matrix_padded)
# [[ 0  0  0  0  0  0  0]
#  [ 0  0  1  2  3  4  0]
#  [ 0  5  6  7  8  9  0]
#  [ 0 10 11 12 13 14  0]
#  [ 0 15 16 17 18 19  0]
#  [ 0  0  0  0  0  0  0]]

####################
## tensor padding ##
####################

tensor_padded = np.pad(tensor, ((0, 1), (0, 1), (0, 1)), 'constant', constant_values=0)
print(tensor_padded)
# [[[ 0  1  2  3  4]
#   [ 5  6  7  8  9]
#   [10 11 12 13 14]
#   [ 0  0  0  0  0]]
#
#  [[ 0  1  2  3  4]
#   [ 5  6  7  8  9]
#   [10 11 12 13 14]
#   [ 0  0  0  0  0]]
#
#  [[ 0  1  2  3  4]
#   [ 5  6  7  8  9]
#   [10 11 12 13 14]
#   [ 0  0  0  0  0]]]


#--------------------------------------------------------------------------------------#
#------------------------------------- 2.np.resize() ----------------------------------#
#--------------------------------------------------------------------------------------#
'''
np.resize(a, new_shape)

Returns a new array with the specified shape.
If the new array size is larger than the original array size, then the new array will be populated with repeated copies of a.
'''

resized_vector = np.resize(vector, (15,))
print(resized_vector)
# [ 1  2  3  4  5  6  7  8  9 10  1  2  3  4  5]

resized_matrix = np.resize(matrix, (6, 6))
print(resized_matrix)
# [[ 0  1  2  3  4  5]
#  [ 6  7  8  9 10 11]
#  [12 13 14 15 16 17]
#  [18 19  0  1  2  3]
#  [ 4  5  6  7  8  9]
#  [10 11 12 13 14 15]]
