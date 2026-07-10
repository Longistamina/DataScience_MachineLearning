'''
1. np.insert(): Insert values along the given axis before the given indices.
2. np.append(): Append values to the end of an array.
3. np.delete(): Return a new array with the specified sub-array removed.
4. np.trim_zeros(): Remove values along a dimension which are zero along all other.
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


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. np.insert() --------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
'''
np.insert(arr, obj, values, axis=None)

arr: input array
obj: index or slice indicating where to insert values
values: values to insert
axis: axis along which to insert values
      if None, arr will be flattened first then inserted
'''

new_vector = np.insert(vector, 2, [10, 20])
print(new_vector)
# [ 1  2 10 20  3  4  5  6  7  8  9 10]

#-----------------#

new_matrix = np.insert(matrix, 1, [10, 20, 30, 40, 50], axis=0)
print(new_matrix)
# [[ 0  1  2  3  4]
#  [10 20 30 40 50]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]]

new_matrix = np.insert(matrix, 2, [10, 20, 30, 40], axis=1)
print(new_matrix)
# [[ 0  1 10  2  3  4]
#  [ 5  6 20  7  8  9]
#  [10 11 30 12 13 14]
#  [15 16 40 17 18 19]]

#-----------------#

inserted_matrix = np.random.randn(3, 5)
new_tensor = np.insert(tensor.astype(np.float32), 1, inserted_matrix, axis=0).round(2)
print(new_tensor)
# [[[ 0.    1.    2.    3.    4.  ]
#   [ 5.    6.    7.    8.    9.  ]
#   [10.   11.   12.   13.   14.  ]]
#
#  [[-0.46  1.47  1.38  0.31  1.2 ]
#   [ 0.45 -0.61 -0.17 -0.81  0.53]
#   [ 1.31 -0.38 -0.69 -0.13  0.76]]
#
#  [[15.   16.   17.   18.   19.  ]
#   [20.   21.   22.   23.   24.  ]
#   [25.   26.   27.   28.   29.  ]]]


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 2. np.append() --------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
'''
np.append(arr, values, axis=None)

arr: input array
values: values to append
axis: axis along which to append values
      if None, arr will be flattened first then appended

NOTE: always append at the end of the array along the specified axis
      the values_array to be appended must be broadcastable with arr along the specified axis
'''

new_vector = np.append(vector, [10, 20])
print(new_vector)
# [ 1  2  3  4  5  6  7  8  9 10 20]

#-----------------#

new_matrix = np.append(matrix, [[10, 20, 30, 40, 50]], axis=0)
print(new_matrix)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]
#  [10 20 30 40 50]]

new_matrix = np.append(matrix, [[10], [20], [30], [40]], axis=1)
print(new_matrix)
# [[ 0  1  2  3  4 10]
#  [ 5  6  7  8  9 20]
#  [10 11 12 13 14 30]
#  [15 16 17 18 19 40]]

#-----------------#

appended_matrix = np.random.randn(3, 5)
new_tensor = np.append(tensor.astype(np.float32), appended_matrix[np.newaxis, :, :], axis=0).round(2)
print(new_tensor)
# [[[ 0.00e+00  1.00e+00  2.00e+00  3.00e+00  4.00e+00]
#   [ 5.00e+00  6.00e+00  7.00e+00  8.00e+00  9.00e+00]
#   [ 1.00e+01  1.10e+01  1.20e+01  1.30e+01  1.40e+01]]
#  [[ 1.50e+01  1.60e+01  1.70e+01  1.80e+01  1.90e+01]
#   [ 2.00e+01  2.10e+01  2.20e+01  2.30e+01  2.40e+01]
#   [ 2.50e+01  2.60e+01  2.70e+01  2.80e+01  2.90e+01]]
#  [[ 6.90e-01 -9.00e-02 -1.29e+00  1.10e-01 -1.43e+00]
#   [-5.00e-02  2.30e-01  8.00e-01  7.10e-01  9.80e-01]
#   [-2.20e+00  8.00e-02 -1.59e+00  2.00e-02 -7.10e-01]]]


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 3. np.delete() --------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
'''
np.delete(arr, obj, axis=None)

arr: The input array.
obj: The object(s) to be deleted.
axis: The axis along which to delete the object(s). If None, the array is flattened before deletion.

For example, if we have a matrix (4, 5),
then, np.delete(matrix, 2, axis=0) will delete the third row.
(it goes along the the axis=0, then find the index=2, then delete the matrx[2, :])

np.delete(matrix, [0, 2], axis=0) will delete the first and third row.
(it goes along the the axis=0, then find the index=[0, 2], then delete the matrx[[0, 2], :])
'''

new_vector = np.delete(vector, 2)
print(new_vector)
# [ 1  2  4  5  6  7  8  9 10]

new_vector = np.delete(vector, [0, 2])
print(new_vector)
# [ 2  4  5  6  7  8  9 10]

#-----------------#

new_matrix = np.delete(matrix, 2, axis=0)
print(new_matrix)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [15 16 17 18 19]]

new_matrix = np.delete(matrix, 2, axis=1)
print(new_matrix)
# [[ 0  1  3  4]
#  [ 5  6  8  9]
#  [10 11 13 14]]

new_matrix = np.delete(matrix, [2, 3], axis=1)
print(new_matrix)
# [[ 0  1  4]
#  [ 5  6  9]
#  [10 11 14]
#  [15 16 19]]

#-----------------#

new_tensor = np.delete(tensor, 1, axis=0)
print(new_tensor)
# [[[ 0  1  2  3  4]
#   [ 5  6  7  8  9]
#   [10 11 12 13 14]]]

new_tensor = np.delete(tensor, [0, 3], axis=-1) # delete the 0-index and 3-index along the last axis
print(new_tensor)
# [[[ 1  2  4]
#   [ 6  7  9]
#   [11 12 14]]
#
#  [[16 17 19]
#   [21 22 24]
#   [26 27 29]]]


#-------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 4. np.trim_zeros() --------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
'''
np.trim_zeros(filt, trim='fb', axis=None): Remove values along a dimension which are zero along all other.

filt: Input array

trim: {“fb”, “f”, “b”}, optional
    + "f": trim from front
    + "b": trim from back
    + "fb" trim from both sides (default)

axis: int or sequence, optional
'''

vector_with_zeros = np.array((0, 0, 0, 1, 2, 3, 0, 2, 1, 0))

vector_trimmed = np.trim_zeros(vector_with_zeros)
print(vector_trimmed)
# [1 2 3 0 2 1]

vector_trimmed = np.trim_zeros(vector_with_zeros, "f")
print(vector_trimmed)
# [1 2 3 0 2 1 0]
# The zero at the end is still remained

vector_trimmed = np.trim_zeros(vector_with_zeros, "b")
print(vector_trimmed)
# [0 0 0 1 2 3 0 2 1]
# The zeros at the front are still remained

#--------------------#

matrix_with_zeros = np.array([[0, 0, 2, 3, 0, 0],
                              [0, 1, 0, 3, 0, 0],
                              [0, 0, 0, 0, 0, 0]])

matrix_trimmed = np.trim_zeros(matrix_with_zeros)
print(matrix_trimmed)
# [[0 2 3]
#  [1 0 3]]

matrix_trimmed = np.trim_zeros(matrix_with_zeros, "f")
print(matrix_trimmed)
# [[0 2 3 0 0]
#  [1 0 3 0 0]
#  [0 0 0 0 0]]

matrix_trimmed = np.trim_zeros(matrix_with_zeros, axis=0)
print(matrix_trimmed)
# [[0 0 2 3 0 0]
#  [0 1 0 3 0 0]]

matrix_trimmed = np.trim_zeros(matrix_with_zeros, axis=1)
print(matrix_trimmed)
# [[0 2 3]
#  [1 0 3]
#  [0 0 0]]
