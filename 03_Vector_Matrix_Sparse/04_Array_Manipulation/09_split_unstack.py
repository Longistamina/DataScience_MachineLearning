"""
1. np.split(): Split an array into multiple sub-arrays (not allow unequal sections)
2. np.array_split(): Split an array into multiple sub-arrays (allow unequal sections)
4. np.vsplit(): Split an array into multiple sub-arrays vertically (2D matrix only)
3. np.hsplit(): Split an array into multiple sub-arrays horizontally (2D matrix only)
5. np.dsplit(): Split an array into multiple sub-arrays along the third axis (3D tensor or greater only)
6. np.unstack(): Split an array into a sequence of arrays along the given axis.

NOTE:
    + indices_or_sections=int(something) -> split into int(something) equal parts
    + indices_or_sections=[list_of_indices] -> split based on given indices
"""

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


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. np.split() --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''NOTE: np.split() does not allow unequal splits using sections'''

##################
## split vector ##
##################

print(vector.shape)
# (10,)

# Split a vector into 2 equal parts
vect_split = np.split(ary=vector, indices_or_sections=2)
print(vect_split)
# [array([1, 2, 3, 4, 5]), array([ 6,  7,  8,  9, 10])]

# Split a vector into 5 equal parts
vect_split = np.split(vector, 5)
print(vect_split)
# [array([1, 2]), array([3, 4]), array([5, 6]), array([7, 8]), array([ 9, 10])]

# Unequal split with error
try:
    vect_split = np.split(vector, 3)
except ValueError as e:
    print(e) # array split does not result in an equal division

# Split a vector at specific indices
vect_split = np.split(vector, [3, 7])
print(vect_split)
# [array([1, 2, 3]), array([4, 5, 6, 7]), array([ 8,  9, 10])]
# [array[:3],        array[3:7],          array[7:]]
# 2 indices given -> 3 parts

##################
## split matrix ##
##################

print(matrix.shape)
# (20, 5)

# Split a matrix into 4 equal submatrices (row-wise)
mat_split = np.split(matrix, 4)
print(mat_split)
# [array([[0, 1, 2, 3, 4]]), array([[5, 6, 7, 8, 9]]), array([[10, 11, 12, 13, 14]]), array([[15, 16, 17, 18, 19]])]

# Split a matrix into 2 submatrices (row-wise)
mat_split = np.split(matrix, 2)
print(mat_split)
# [array([[0, 1, 2, 3, 4],
#        [5, 6, 7, 8, 9]]),
# array([[10, 11, 12, 13, 14],
#        [15, 16, 17, 18, 19]])]

# Split a matrix with specified row indices and axis=0
mat_split = np.split(matrix, [1, 3], axis=0)
print(mat_split)
# [array([[0, 1, 2, 3, 4]]), array([[ 5,  6,  7,  8,  9],
#        [10, 11, 12, 13, 14]]), array([[15, 16, 17, 18, 19]])]

# Split a matrix column wise with axis=1
mat_split = np.split(matrix, [1, 3], axis=1)
print(mat_split)
# [array([[ 0],
#        [ 5],
#        [10],
#        [15]]),
# array([[ 1,  2],
#        [ 6,  7],
#        [11, 12],
#        [16, 17]]),
# array([[ 3,  4],
#        [ 8,  9],
#        [13, 14],
#        [18, 19]])]

##################
## split tensor ##
##################

print(tensor.shape)
# (2, 3, 5)

# Split a tensor along the last dimension using sections (axis=-1 or axis=2)
tensor_split = np.split(tensor, 5, axis=-1)
print(tensor_split)
# [array([[[ 0],
#         [ 5],
#         [10]],
#        [[15],
#         [20],
#         [25]]]),
# array([[[ 1],
#         [ 6],
#         [11]],
#        [[16],
#         [21],
#         [26]]]),
# .........
# array([[[ 4],
#         [ 9],
#         [14]],
#        [[19],
#         [24],
#         [29]]])]
# Each one is a subtensor with dimensions (2, 3, 1)

# Split a tensor along the last dimension using indices (axis=-1, or axis=2)
tensor_split = np.split(tensor, [1, 3], axis=-1)
print(tensor_split)
# [array([[[ 0],
#         [ 5],
#         [10]],
#        [[15],                   tensor[:, :, :1]
#         [20],
#         [25]]]),
# array([[[ 1,  2],
#         [ 6,  7],
#         [11, 12]],              tensor[:, :, 1:3]
#        [[16, 17],
#         [21, 22],
#         [26, 27]]]),
# array([[[ 3,  4],
#         [ 8,  9],
#         [13, 14]],              tensor[:, :, 3:]
#        [[18, 19],
#         [23, 24],
#         [28, 29]]])]


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 2. np.array_split() ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
NOTE: np.array_split() allows unequal splits using sections

Given an array with length L, and number of sections N.
It returns L%N subarrays of size = (L // N + 1).
And the rest of size = (L // N).
'''

print(matrix.shape)
# (4, 5)

array_split = np.array_split(matrix, 3, axis=1)
print(array_split)
# [array([[ 0,  1],
#        [ 5,  6],
#        [10, 11],
#        [15, 16]]),
# array([[ 2,  3],
#        [ 7,  8],
#        [12, 13],
#        [17, 18]]),
# array([[ 4],
#        [ 9],
#        [14],
#        [19]])]

'''
Here:
    + L = length of axis 1 = 5
    + N = number of sections = 3
    + L//N = 5//3 = 1 (integer division)

L%N = 2 (remainder)
=> returns 2 subarrays of size (L // N + 1) = (1 + 1 = 2)

and the rest of size (L // N) = (1)
'''


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 3. np.vsplit() --------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
"""Works like np.split(axis=0) for 2D matrix"""

print(matrix.shape)
# (4, 5)

vsplit = np.vsplit(matrix, 2) # split into 2 equal sections
print(vsplit)
# [array([[ 0,  1,  2,  3,  4],
#        [ 5,  6,  7,  8,  9]]),
# array([[10, 11, 12, 13, 14],
#        [15, 16, 17, 18, 19]])]

vsplit = np.vsplit(matrix, [2, 3]) # split at indices 2 and 3
print(vsplit)
# [array([[ 0,  1,  2,  3,  4],
#        [ 5,  6,  7,  8,  9]]),
# array([[10, 11, 12, 13, 14]]),
# array([[15, 16, 17, 18, 19]])]


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 4. np.hsplit() --------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
"""Works like np.split(axis=1) for 2D matrix"""

print(matrix.shape)
# (4, 5)

hsplit = np.hsplit(matrix, 5) # split into 5 equal sections
print(hsplit)
# [array([[ 0],
#        [ 5],
#        [10],
#        [15]]),
# array([[ 1],
#        [ 6],
#        [11],
#        [16]]),
# array([[ 2],
#        [ 7],
#        [12],
#        [17]]),
# array([[ 3],
#        [ 8],
#        [13],
#        [18]]),
# array([[ 4],
#        [ 9],
#        [14],
#        [19]])]

hsplit = np.hsplit(matrix, [2, 3]) # split at indices 2 and 3
print(hsplit)
# [array([[ 0,  1],
#        [ 5,  6],
#        [10, 11],
#        [15, 16]]),
# array([[ 2],
#        [ 7],
#        [12],
#        [17]]),
# array([[ 3,  4],
#        [ 8,  9],
#        [13, 14],
#        [18, 19]])]


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 5. np.dsplit() --------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
"""Works like np.split(axis=2) for 3D tensor or greater"""

print(tensor.shape)
# (2, 3, 5)

dsplit = np.dsplit(tensor, 5) # split into 2 equal sections
print(dsplit)
# [array([[[ 0],
#         [ 5],
#         [10]],
#        [[15],
#         [20],
#         [25]]]),
# array([[[ 1],
#         [ 6],
#         [11]],
#        [[16],
#         [21],
#         [26]]]),
# .........
# array([[[ 4],
#         [ 9],
#         [14]],
#        [[19],
#         [24],
#         [29]]])]
# Each one is a subtensor with dimensions (2, 3, 1)

dsplit = np.dsplit(tensor, [2, 3]) # split at indices 2 and 3
print(dsplit)
# [array([[[ 0,  1],
#         [ 5,  6],
#         [10, 11]],
#        [[15, 16],
#         [20, 21],
#         [25, 26]]]),
# array([[[ 2],
#         [ 7],
#         [12]],
#        [[17],
#         [22],
#         [27]]]),
#  array([[[ 3,  4],
#         [ 8,  9],
#         [13, 14]],
#        [[18, 19],
#         [23, 24],
#         [28, 29]]])]


#----------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 6. np.unstack() --------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#
"""
Split an array into a sequence of arrays along the given axis.
-> reverse of stack

For example, unstacking a (2, 3, 5) array along axis 0 gives 2 (3, 5) arrays.
"""

print(tensor.shape)
# (2, 3, 5)

unstack = np.unstack(tensor, axis=0)
print(unstack)
# [array([[ 0,  1,  2,  3,  4],
#         [ 5,  6,  7,  8,  9],
#         [10, 11, 12, 13, 14]]),
#  array([[15, 16, 17, 18, 19],
#         [20, 21, 22, 23, 24],
#         [25, 26, 27, 28, 29]])]
# Each is a (3, 5) array
# (2, 3, 5) -> 2 * (1, 3, 5) -> 2 * (3, 5)

unstack = np.unstack(tensor, axis=1)
print(unstack)
# [array([[ 0,  1,  2,  3,  4],
#         [15, 16, 17, 18, 19]]),
#  array([[ 5,  6,  7,  8,  9],
#         [20, 21, 22, 23, 24]]),
#  array([[10, 11, 12, 13, 14],
#         [25, 26, 27, 28, 29]])]
# Each is a (2, 5) array
# (2, 3, 5) -> 3 * (2, 1, 5) -> 3 * (2, 5)

unstack = np.unstack(tensor, axis=2)
print(unstack)
# [array([[ 0,  5, 10],
#         [15, 20, 25]]),
#  array([[ 1,  6, 11],
#         [16, 21, 26]]),
#  array([[ 2,  7, 12],
#         [17, 22, 27]]),
#  array([[ 3,  8, 13],
#         [18, 23, 28]]),
#  array([[ 4,  9, 14],
#         [19, 24, 29]])]
# Each is a (2, 3) array
# (2, 3, 5) -> 5 * (2, 3, 1) -> 5 * (2, 3)
