'''
1. np.moveaxis(a, source, destination)
2. np.rollaxis(a, axis, start)
3. np.swapaxes(a, axis1, axis2)
4. np.transpose(a, axes=None) and ndarray.T
5. np.permute_dims(a, axes)
6. np.matrix.transpose(a, axes=None)
'''

import numpy as np

matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
print("Original Matrix:")
print(matrix)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]
#  [10 11 12]]

tensor = np.arange(0, 30).reshape(2, 3, 5)
print("\nOriginal Tensor:")
print(tensor)
# [[[ 0  1  2  3  4]
#   [ 5  6  7  8  9]
#   [10 11 12 13 14]]

#  [[15 16 17 18 19]
#   [20 21 22 23 24]
#   [25 26 27 28 29]]]


# =========================================================================================
# 1. np.moveaxis()
# =========================================================================================
'''
np.moveaxis(a, source, destination): moves axes of an array to new positions
                                     while other axes remain in their original order.
                                     Source: the original positions of the axes to move. These must be unique.
                                     Destination: the destination positions for each of the original axes. These must also be unique.
'''

moved = np.moveaxis(a=matrix, source=0, destination=1)
print("\nMoved Matrix:")
print(moved)
# [[ 1  4  7 10]
#  [ 2  5  8 11]
#  [ 3  6  9 12]]
# axis 0 moved to position 1, so (4, 3) -> (3, 4)
'''NOTE: looks like transpose but not exactly, because the order of the other axes is preserved.'''

moved = np.moveaxis(tensor, 0, 2)
print("\nMoved Tensor:")
print(moved)
# [[[ 0 15]
#   [ 1 16]
#   [ 2 17]
#   [ 3 18]
#   [ 4 19]]

#  [[ 5 20]
#   [ 6 21]
#   [ 7 22]
#   [ 8 23]
#   [ 9 24]]

#  [[10 25]
#   [11 26]
#   [12 27]
#   [13 28]
#   [14 29]]]
# axis 0 moved to position 2, so (2, 3, 5) -> (3, 5, 2)


# =========================================================================================
# 2. np.rollaxis()
# =========================================================================================
'''
np.rollaxis(a, axis, start): Rolls the specified axis backwards until it lies in a given position.
                            The other axes remain in their original order.
                            Axis: the axis to roll. This must be an integer.
                            Start: the position to roll the axis to. This must be an integer.
if start <= axis, then roll the axis backwards until it lies in the start position.
if start > axis, then roll the axis backwards until it lies in the start-1 position
'''

rolled = np.rollaxis(matrix, 0, 2)
print("\nRolled Matrix:")
print(rolled)
# [[ 1  4  7 10]
#  [ 2  5  8 11]
#  [ 3  6  9 12]]
# axis 0 rolled to position 2, so (4, 3) -> (3, 4)

rolled = np.rollaxis(tensor, 0, 2)
print("\nRolled Tensor:")
print(rolled)
# [[[ 0  1  2  3  4]
#   [15 16 17 18 19]]

#  [[ 5  6  7  8  9]
#   [20 21 22 23 24]]

#  [[10 11 12 13 14]
#   [25 26 27 28 29]]]
# axis 0 rolled to position 2, so (2, 3, 5) -> (3, 5, 2) -> (3, 2, 5)

tensor_4d = np.arange(0, 120).reshape(2, 3, 4, 5)
print(np.rollaxis(tensor_4d, 0, 3).shape) # (3, 4, 2, 5)
'''
The roll happens like this:
(2, 3, 4, 5) -> (3, 4, 5, 2) -> (3, 4, 2, 5)

It stops at position 3-1 = 2, not position 3, because start > axis
'''

'''NOTE: should prefer np.moveaxis() over np.rollaxis()'''


# =========================================================================================
# 3. np.swapaxes()
# =========================================================================================
'''np.swapaxes(a, axis1, axis2): Interchange two axes of an array.'''

swapped = np.swapaxes(matrix, 0, 1)
print("\nSwapped Matrix:")
print(swapped)
# [[ 1  4  7 10]
#  [ 2  5  8 11]
#  [ 3  6  9 12]]
# axis 0 and axis 1 swapped, so (4, 3) -> (3, 4)

swapped = np.swapaxes(tensor, 0, 2)
print("\nSwapped Tensor:")
print(swapped)
# [[[ 0 15]
#   [ 5 20]
#   [10 25]]

#  [[ 1 16]
#   [ 6 21]
#   [11 26]]

#  [[ 2 17]
#   [ 7 22]
#   [12 27]]

#  [[ 3 18]
#   [ 8 23]
#   [13 28]]

#  [[ 4 19]
#   [ 9 24]
#   [14 29]]]
# axis 0 and axis 2 swapped, so (2, 3, 5) -> (5, 3, 2)


# =========================================================================================
# 4. np.transpose() and ndarray.T
# =========================================================================================
'''np.transpose(a, axes=None): Permute the dimensions of an array.'''
'''ndarray.T: same as np.transpose() with axes reversed.'''

'''np.transpose() gives more control over the order of the axes,
while ndarray.T simply reverses the order of the axes.'''

transposed = np.transpose(matrix)
print("\nTransposed Matrix:")
print(transposed)
# [[ 1  4  7 10]
#  [ 2  5  8 11]
#  [ 3  6  9 12]]
# axis 0 and axis 1 transposed, so (4, 3) -> (3, 4)

transposed = np.transpose(tensor)
print("\nTransposed Tensor:")
print(transposed)
# [[[ 0 15]
#   [ 5 20]
#   [10 25]]

#  [[ 1 16]
#   [ 6 21]
#   [11 26]]

#  [[ 2 17]
#   [ 7 22]
#   [12 27]]

#  [[ 3 18]
#   [ 8 23]
#   [13 28]]

#  [[ 4 19]
#   [ 9 24]
#   [14 29]]]
'''
For an n-D array, if axes are given, their order indicates how the axes are permuted.
If axes are not provided, then transpose(a).shape == a.shape[::-1]
-> the dimensions are reversed 180 degrees, so (2, 3, 5) -> (5, 3, 2)
'''

transposed = np.transpose(tensor, (1, 0, 2)) # tranposed n-D array with given axes order
print("\nTransposed Tensor with given axes order:")
print(transposed)
# [[[ 0  1  2  3  4]
#   [15 16 17 18 19]]

#  [[ 5  6  7  8  9]
#   [20 21 22 23 24]]

#  [[10 11 12 13 14]
#   [25 26 27 28 29]]]
# axes order (1, 0, 2) means axis 1 becomes axis 0, axis 0 becomes axis 1, and axis 2 stays the same
# so (2, 3, 5) -> (3, 2, 5)

##-----------##
## ndarray.T ##
##-----------##

transposed = tensor.T
print("\nTransposed Tensor using ndarray.T:")
print(transposed)
# [[[ 0 15]
#   [ 5 20]
#   [10 25]]

#  [[ 1 16]
#   [ 6 21]
#   [11 26]]

#  [[ 2 17]
#   [ 7 22]
#   [12 27]]

#  [[ 3 18]
#   [ 8 23]
#   [13 28]]

#  [[ 4 19]
#   [ 9 24]
#   [14 29]]]

tranposed = matrix.T
print("\nTransposed Matrix using ndarray.T:")
print(tranposed)
# [[ 1  4  7 10]
#  [ 2  5  8 11]
#  [ 3  6  9 12]]


# =========================================================================================
# 5. np.permute_dims()
# =========================================================================================
'''
np.permute_dims(a, axes): Permute the dimensions of an array according to a given pattern.
=> So basically, this is the same as np.transpose()
'''

permuted = np.permute_dims(matrix)
print("\nPermuted Matrix:")
print(permuted)
# [[ 1  4  7 10]
#  [ 2  5  8 11]
#  [ 3  6  9 12]]

permuted = np.permute_dims(tensor)
print("\nPermuted Tensor:")
print(permuted)
# [[[ 0 15]
#   [ 5 20]
#   [10 25]]

#  [[ 1 16]
#   [ 6 21]
#   [11 26]]

#  [[ 2 17]
#   [ 7 22]
#   [12 27]]

#  [[ 3 18]
#   [ 8 23]
#   [13 28]]

#  [[ 4 19]
#   [ 9 24]
#   [14 29]]]


permuted = np.permute_dims(tensor, (1, 0, 2))
print("\nPermuted Tensor:")
print(permuted)
# [[[ 0  1  2  3  4]
#   [15 16 17 18 19]]

#  [[ 5  6  7  8  9]
#   [20 21 22 23 24]]

#  [[10 11 12 13 14]
#   [25 26 27 28 29]]]


# =========================================================================================
# 6. np.matrix_transpose()
# =========================================================================================
'''
np.matrix_tranpose(x, /): Transposes a matrix (or a stack of matrices)

(..., M, N) -> (..., N, M)
'''

mtr_transposed = np.matrix_transpose(matrix)
print("\nMatrix Transposed using np.matrix_transpose():")
print(mtr_transposed)
# [[ 1  4  7 10]
#  [ 2  5  8 11]
#  [ 3  6  9 12]]
# (4, 3) -> (3, 4)

mtr_transposed = np.matrix_transpose(tensor)
print("\nTensor Transposed using np.matrix.transpose():")
print(mtr_transposed)
# [[[ 0  5 10]
#   [ 1  6 11]
#   [ 2  7 12]
#   [ 3  8 13]
#   [ 4  9 14]]
#
#  [[15 20 25]
#   [16 21 26]
#   [17 22 27]
#   [18 23 28]
#   [19 24 29]]]
# (2, 3, 5) -> (2, 5, 3)
