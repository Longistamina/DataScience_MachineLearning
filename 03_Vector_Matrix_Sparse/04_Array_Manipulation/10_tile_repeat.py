'''
1. np.tile() - Repeat an array along specified axes
2. np.repeat() - Repeat elements of an array
'''

import numpy as np

vector = np.array([1, 2, 3])

matrix = np.array([[4, 5, 6], [7, 8, 9]])
print(matrix)
# [[4 5 6]
#  [7 8 9]]


#-------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. np.tile() --------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
'''
np.tile(A, reps): Repeat array A according to reps

reps can be array_like, or integer

if reps has length d, the result will have dimension of max(d, A.ndim)

if A.ndim > d, the result will have dimension of A.ndim, example:
+ A.ndim = (2, 3, 4, 5) = 4 dimensions
+ reps = (2, 2) = 2 dimensions
+ reps is treated as (1, 1, 2, 2) by prepending 1s to make it 4-dimensional
+ A.ndim x reps = (2, 3, 4, 5) x (1, 1, 2, 2) = (2, 3, 8, 10) = 4 dimensions

if A.ndim < d, the result will have dimension of d, example:
+ A.ndim = (2, 3) = 2 dimensions
+ reps = (2, 2, 3) = 3 dimensions
+ A.ndim is treated as (1, 2, 3) by prepending new axes to make it 3-dimensional
+ A.ndim x reps = (1, 2, 3) x (2, 2, 3) = (2, 4, 9) = 4 dimensions
'''

#####################
## reps as integer ##
#####################

result = np.tile(vector, 3)
print(result)
# [1 2 3 1 2 3 1 2 3]
# vector = (3,)
# reps = 3
# => result = (3,) * 3 = (9,)

result = np.tile(matrix, 2) # consider as (1, 2)
print(result)
# [[4 5 6 4 5 6]
#  [7 8 9 7 8 9]]
# matrix = (2, 3)
# reps = 2 -> (1, 2)
# => result = (2, 3) * (1, 2) = (2, 6)

########################
## reps as array_like ##
########################

result = np.tile(vector, (2, 3))
print(result)
# [[1 2 3 1 2 3 1 2 3]
#  [1 2 3 1 2 3 1 2 3]]
# vector = (3,) -> (1, 3)
# reps = (2, 3) -> (2, 3)
# => result = (1, 3) * (2, 3) = (2, 9)

result = np.tile(matrix, (2, 3))
print(result)
# [[4 5 6 4 5 6 4 5 6]
#  [7 8 9 7 8 9 7 8 9]
#  [4 5 6 4 5 6 4 5 6]
#  [7 8 9 7 8 9 7 8 9]]
# matrix = (2, 3)
# reps = (2, 3) -> (2, 3)
# => result = (2, 3) * (2, 3) = (4, 9)

result = np.tile(matrix, (1, 3))
print(result)
# [[4 5 6 4 5 6 4 5 6]
#  [7 8 9 7 8 9 7 8 9]]
# matrix = (2, 3)
# reps = (1, 3) -> (1, 3)
# => result = (2, 3) * (1, 3) = (2, 9)

result = np.tile(matrix, (3, 1))
print(result)
# [[4 5 6]
#  [7 8 9]
#  [4 5 6]
#  [7 8 9]
#  [4 5 6]
#  [7 8 9]]
# matrix = (2, 3)
# reps = (3, 1) -> (3, 1)
# => result = (2, 3) * (3, 1) = (6, 3)


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 2. np.repeat() --------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#
'''
np.repeat(a, repeats, axis=None)

a: array_like
    Input array.
repeats: int or array_like of ints
    The number of repetitions for each element.
axis: int, optional
    The axis along which to repeat values. By default, use the flattened input array, and return a flat output array.

NOTE: axis must be in range of dimension
'''

########################
## Repeat with vector ##
########################

print(vector)
# [1 2 3]

result = np.repeat(vector, 3)
print(result)
# [1 1 1 2 2 2 3 3 3]

result = np.repeat(matrix, 2, axis=0)
print(result)
# [[4 5 6]
#  [4 5 6]
#  [7 8 9]
#  [7 8 9]]

result = np.repeat(vector, 2, axis=1)
'''Error: axis=1 is out of range'''

########################
## Repeat with matrix ##
########################

print(matrix)
# [[4 5 6]
#  [7 8 9]]

result = np.repeat(matrix, 2)
print(result)
# [4 4 5 5 6 6 7 7 8 8 9 9]
'''If axis=None or not specified -> return a flattened array'''

result = np.repeat(matrix, 2, axis=0)
print(result)
# [[4 5 6]
#  [4 5 6]
#  [7 8 9]
#  [7 8 9]]

result = np.repeat(matrix, 2, axis=1)
print(result)
# [[4 4 5 5 6 6]
#  [7 7 8 8 9 9]]
