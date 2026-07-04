'''
1. np.reshape()
2. np.ravel()
'''


import numpy as np

#-----------------------------------------------------------------------------------#
#--------------------------------- 1. np.reshape() ---------------------------------#
#-----------------------------------------------------------------------------------#
'''Gives a new shape to an array without changing its data.'''

##############
## 1D to 2D ##
##############

vector = np.array([1, 2, 3, 4, 5, 6])
# [1 2 3 4 5 6]
# (6,)

matrix = np.reshape(vector, (2, 3)) # only positional arguments
print(matrix)
# [[1 2 3]
#  [4 5 6]]

matrix = np.reshape(vector, (3, 2))
print(matrix)
# [[1 2]
#  [3 4]
#  [5 6]]

matrix = np.reshape(vector, (6, 1)) # similar to np.reshape(vector, (-1, 1))
print(matrix)
# [[1]
#  [2]
#  [3]
#  [4]
#  [5]
#  [6]]

matrix = np.reshape(vector, (1, 6)) # similar to np.reshape(vector, (1, -1))
print(matrix)
# [[1 2 3 4 5 6]]

##############
## 2D to 3D ##
##############

matrix = np.arange(0, 24).reshape(6, 4)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]
#  [12 13 14 15]
#  [16 17 18 19]
#  [20 21 22 23]]

tensor = np.reshape(matrix, (2, 3, 4))
print(tensor)
# [[[ 0  1  2  3]
#   [ 4  5  6  7]
#   [ 8  9 10 11]]

#  [[12 13 14 15]
#   [16 17 18 19]
#   [20 21 22 23]]]

tensor = np.reshape(matrix, (-1, 2, 4))
print(tensor)
# [[[ 0  1  2  3]
#   [ 4  5  6  7]]

#  [[ 8  9 10 11]
#   [12 13 14 15]]

#  [[16 17 18 19]
#   [20 21 22 23]]]


#---------------------------------------------------------------------------------#
#--------------------------------- 2. np.ravel() ---------------------------------#
#---------------------------------------------------------------------------------#
'''Returns a contiguous flattened array.'''

matrix = np.array([[1, 2, 3], [4, 5, 6]])
# [[1 2 3]
#  [4 5 6]]

vector = np.ravel(matrix)
print(vector)
# [1 2 3 4 5 6]

#-----------#

tensor = np.array([[[ 0,  1,  2,  3],
                    [ 4,  5,  6,  7],
                    [ 8,  9, 10, 11]],
                     [[12, 13, 14, 15],
                      [16, 17, 18, 19],
                      [20, 21, 22, 23]]])
# shape: (2, 3, 4)

vector = np.ravel(tensor)
# [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23]
