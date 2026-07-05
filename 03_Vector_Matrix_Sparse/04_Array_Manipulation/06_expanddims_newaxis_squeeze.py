'''
1. np.expand_dims()
2. Expand dimension with np.newaxis or None
3. np.squeeze()
'''

import numpy as np

scalar = np.array(42)
vector = np.array([1, 2, 3])

matrix = np.array([[1, 2, 3], [4, 5, 6]])
# [[1, 2, 3],
#  [4, 5, 6]]


#------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 1. np.expand_dims() -------------------------------------------------#
#------------------------------------------------------------------------------------------------------------#
'''np.expand_dims(a, axis) is used to add a new axis to an array, effectively increasing its dimensions.'''

###################################
## Expand a scalar to a 1D array ##
###################################

scalr_expanded = np.expand_dims(scalar, axis=0)
print(scalr_expanded) # [42]

scalar_expanded = np.expand_dims(scalar, axis=1)
'''AxisError: axis 1 is out of bounds for array of dimension 1'''

#################################
## Expand a vector to a matrix ##
#################################

vector_expanded = np.expand_dims(vector, axis=0)
print(vector_expanded)
# [[1 2 3]]
# (3,) -> (1, 3)

vector_expanded = np.expand_dims(vector, axis=1)
print(vector_expanded)
# [[1]
#  [2]
#  [3]]
# (3,) -> (3, 1)

vector_expanded = np.expand_dims(vector, axis=-1)
print(vector_expanded)
# [[1]
#  [2]
#  [3]]

vector_expanded = np.expand_dims(vector, axis=2)
'''AxisError: axis 2 is out of bounds for array of dimension 2'''

###################################
## Expand a matrix to a 3D array ##
###################################

matrix_expanded = np.expand_dims(matrix, axis=0)
print(matrix_expanded)
# [[[1 2 3]
#   [4 5 6]]]
# (2, 3) -> (1, 2, 3)

matrix_expanded = np.expand_dims(matrix, axis=1)
print(matrix_expanded)
# [[[1 2 3]]

#  [[4 5 6]]]
# (2, 3) -> (2, 1, 3)

matrix_expanded = np.expand_dims(matrix, axis=2)
print(matrix_expanded)
# [[[1]
#   [2]
#   [3]]

#  [[4]
#   [5]
#   [6]]]
# (2, 3) -> (2, 3, 1)


#------------------------------------------------------------------------------------------------------------#
#------------------------------- 2. Expand dimension with newaxis and None ----------------------------------#
#------------------------------------------------------------------------------------------------------------#
'''np.newaxis and None are used to add a new axis to an array, similar to np.expand_dims().'''

################
## np.newaxis ##
################

print(scalar[np.newaxis]) # [42]
print(scalar[np.newaxis, np.newaxis]) # [[42]]
print(scalar[np.newaxis, np.newaxis, np.newaxis]) # [[[42]]]

#-----------------

print(vector[np.newaxis]) # [[1 2 3]] <-> (1, 3)
print(vector[np.newaxis, :]) # [[1 2 3]] <-> (1, 3)

print(vector[:, np.newaxis])
# [[1]
# [2]
# [3]]
# (3, 1)

print(vector[np.newaxis, np.newaxis]) # [[[1 2 3]]] <-> (1, 1, 3)
                                      # equivalent to vector[np.newaxis, np.newaxis, :]

print(vector[np.newaxis, :, np.newaxis])
# [[1]
#  [2]
#  [3]]
# (1, 3, 1)

print(vector[:, np.newaxis, np.newaxis, np.newaxis])
# [[[[1]]]


#  [[[2]]]


#  [[[3]]]]
# (3, 1, 1, 1)

#-----------------

print(matrix[np.newaxis])
# [[[1 2 3]
#   [4 5 6]]]
# (1, 2, 3)

print(matrix[np.newaxis, :]) # also equivalent to matrix[np.newaxis, :, :]
# [[[1 2 3]
#   [4 5 6]]]
# (1, 2, 3)

print(matrix[:, np.newaxis])
# [[[1 2 3]]

#  [[4 5 6]]]
# (2, 1, 3)

print(matrix[:, np.newaxis, :])
# [[[1 2 3]]

#  [[4 5 6]]]
# (2, 1, 3)

print(matrix[:, np.newaxis, np.newaxis])
# [[[[1 2 3]]]


#  [[[4 5 6]]]]
# (2, 1, 1, 3)

print(matrix[np.newaxis, np.newaxis])
# [[[[1 2 3]
#    [4 5 6]]]]
# (1, 1, 2, 3)
# equivalent to matrix[np.newaxis, np.newaxis, :, :]

##################
##     None     ##
##################
'''Using None is equivalent to using np.newaxis.'''

print(scalar[None]) # [42]
print(scalar[None, None]) # [[42]]
print(scalar[None, None, None]) # [[[42]]]

#-----------------

print(vector[None]) # [[1 2 3]] <-> (1, 3)
print(vector[None, :]) # [[1 2 3]] <-> (1, 3)

print(vector[:, None])
# [[1]
# [2]
# [3]]
# (3, 1)

print(vector[None, None]) # [[[1 2 3]]] <-> (1, 1, 3)
                          # equivalent to vector[None, None, :]

print(vector[None, :, None])
# [[1]
#  [2]
#  [3]]
# (1, 3, 1)

print(vector[:, None, None, None])
# [[[[1]]]

#  [[[2]]]

#  [[[3]]]]
# (3, 1, 1, 1)

#-----------------

print(matrix[None])
# [[[1 2 3]
#   [4 5 6]]]
# (1, 2, 3)

print(matrix[None, :]) # also equivalent to matrix[None, :, :]
# [[[1 2 3]
#   [4 5 6]]]
# (1, 2, 3)

print(matrix[:, None])
# [[[1 2 3]]

#  [[4 5 6]]]
# (2, 1, 3)

print(matrix[:, None, :])
# [[[1 2 3]]

#  [[4 5 6]]]
# (2, 1, 3)

print(matrix[:, None, None])
# [[[[1 2 3]]]

#  [[[4 5 6]]]]
# (2, 1, 1, 3)

print(matrix[None, None])
# [[[[1 2 3]
#    [4 5 6]]]]
# (1, 1, 2, 3)
# equivalent to matrix[None, None, :, :]


#------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 3. np.squeeze() --------------------------------------------------#
#------------------------------------------------------------------------------------------------------------#
'''np.squeeze() is used to remove single-dimensional entries from the shape of an array.'''

matrix_excessive = np.array([[[1, 2, 3]], [[4, 5, 6]]]) # (2, 1, 3)
print(matrix_excessive)
# [[[1 2 3]]

#  [[4 5 6]]]

matrix_squeezed = np.squeeze(matrix_excessive)
print(matrix_squeezed)
# [[1 2 3]
#  [4 5 6]]
# (2, 3)

#-------------------

vector_excessive = np.array([1, 2, 3])[:, np.newaxis, np.newaxis, np.newaxis] # (3, 1, 1, 1)
print(vector_excessive)
# [[[[1]]]


#  [[[2]]]


#  [[[3]]]]

vector_squeezed = np.squeeze(vector_excessive)
print(vector_squeezed) # [1 2 3]
