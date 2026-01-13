'''
1. arr.reshape(dimension) for 2D matrix:
   + arr.reshape((m, n)): reshape to m rows and n columns (must keep total elements the same)
   + arr.reshape(-1, n): set columns to n, automatically calculate the other dimension based on n columns
   + arr.reshape(m, -1): set rows to m, automatically calculate the other dimension based on m rows
   + arr.reshape(-1, 1): convert to column vector (still 2D)
   + arr.reshape(1, -1): convert to row vector (still 2D)
   + arr.reshape(-1):   flatten to 1D vector
   + np.reshape(arr, newshape): similar to arr.reshape(newshape)


2. Flatten and Ravel: convert 2D matrix back to 1D vector
   + arr.flatten(): convert back to 1D vector, returns a copy
   + arr.ravel(): convert back to 1D vector, returns a view whenever possible (same memory when possible)
   + np.ravel(arr): similar to arr.ravel()
   
3. arr.resize(dimension): Similar to reshape, 
                          But if the new array is larger than the original array,   
                          then the new array is filled with zeros
                          (and it modifies the original array in-place)
   + np.resize(arr, newshape): resize with repeated copies of the original array


4. arr.transpose() or arr.T: Transpose the array (swap rows and columns)
   + np.transpose(arr) or np.T(arr): similar to arr.transpose() or arr.T


5. Squeeze:
   + arr.squeeze(): Remove single-dimensional entries from the shape of an array
   + np.squeeze(arr): similar to arr.squeeze()
   
6. Expand dims:
   + np.expand_dims(arr, axis): Expand the shape of an array by inserting a new axis at the specified position
   + arr[np.newaxis, :, :] ||| arr[np.newaxis, ...]: equivalent to np.expand_dims(arr, axis=0)
   + arr[:, np.newaxis, :]: equivalent to np.expand_dims(arr, axis=1)
   + arr[:, :, np.newaxis] ||| arr[..., np.newaxis]: equivalent to np.expand_dims(arr, axis=2

7. swapaxes:
   + np.swapaxes(arr, axis1, axis2): swap two axes of an array; for 2D, swapping 0 and 1 is equivalent to transpose

8. permute_dims:
   + np.permute_dims(arr, axes): permute (reorder) all axes according to axes
                                 Works conceptually like torch.permute (available in newer NumPy / array API)
'''

import numpy as np


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. arr.reshape(dimension) ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#


np.random.seed(0)
matrix = np.random.randint(1, 21, size=(4, 5))
print(matrix)
# [[13 16  1  4  4]
#  [ 8 10 20 19  5]
#  [ 7 13  2  7  8]
#  [15 18  6 14  9]]


print(matrix.shape) # (4, 5)

'''
Possible ways to reshape 2D matrix of size 4x5 (total 20 elements):

20 = 4x5
   = 5x4
   = 2x10
   = 10x2
   = 20x1
   = 1x20
   = 2x2x5
   = 5x2x2
   = 2x5x2
'''

#######################
## arr.reshape(m, n) ##
#######################

matrix_5x4 = matrix.reshape((5, 4))
print(matrix_5x4)
# [[13 16  1  4]
#  [ 4  8 10 20]
#  [19  5  7 13]
#  [ 2  7  8 15]
#  [18  6 14  9]]
# shape: (5, 4)

print(matrix.reshape((2, 10)))
# [[13 16  1  4  4  8 10 20 19  5]
#  [ 7 13  2  7  8 15 18  6 14  9]]
# shape: (2, 10)

print(matrix.reshape((10, 2)))
# shape: (10, 2)

print(matrix.reshape((20, 1)))
# shape: (20, 1)   # column vector (still 2D)

print(matrix.reshape((1, 20)))
# [[13 16  1  4  4  8 10 20 19  5  7 13  2  7  8 15 18  6 14  9]]
# shape: (1, 20)   # row vector (still 2D)

print(matrix.reshape((2, 2, 5))) # 3D matrix
# [[[13 16  1  4  4]
#   [ 8 10 20 19  5]]

#  [[ 7 13  2  7  8]
#   [15 18  6 14  9]]]
# shape: (2, 2, 5)

print(matrix.reshape((3, 7)))
'''ValueError: cannot reshape array of size 20 into shape (3,7)'''

########################
## arr.reshape(-1, n) ##
########################

print(matrix.reshape((-1, 4)))
# [[13 16  1  4]
#  [ 4  8 10 20]
#  [19  5  7 13]
#  [ 2  7  8 15]
#  [18  6 14  9]]
# set columns to 4, automatically calculate the other dimension (5, 4)

print(matrix.reshape((-1, 2)))
# [[13 16]
#  [ 1  4]
#  [ 4  8]
#  [10 20]
#  [19  5]
#  [ 7 13]
#  [ 2  7]
#  [ 8 15]
#  [18  6]
#  [14  9]]
# set columns to 2, automatically calculate rows (10, 2)

########################
## arr.reshape(m, -1) ##
########################

print(matrix.reshape((4, -1)))
# [[13 16  1  4  4]
#  [ 8 10 20 19  5]
#  [ 7 13  2  7  8]
#  [15 18  6 14  9]]
# set rows to 4, automatically calculate columns (4, 5)

print(matrix.reshape((2, -1)))
# [[13 16  1  4  4  8 10 20 19  5]
#  [ 7 13  2  7  8 15 18  6 14  9]]
# set rows to 2, automatically calculate columns (2, 10)

########################
## arr.reshape(-1, 1) ##
########################

col_vector = matrix.reshape((-1, 1))
print(col_vector) # shape (20, 1)
print(col_vector.ndim)  # 2  (still counted as 2D matrix)

########################
## arr.reshape(1, -1) ##
########################

row_vector = matrix.reshape((1, -1))
print(row_vector) # shape (1, 20)
print(row_vector.ndim)  # 2  (still counted as 2D matrix)

#####################
## arr.reshape(-1) ##
#####################

flat_vector = matrix.reshape(-1)

print(flat_vector)
# [13 16  1  4  4  8 10 20 19  5  7 13  2  7  8 15 18  6 14  9]

print(flat_vector.ndim)  # 1 (1D vector)

###############################
## np.reshape(arr, newshape) ##
###############################

print(np.reshape(matrix, (5, 4)))
# Works similarly to arr.reshape(newshape)


#--------------------------------------------------------------------------------------------------------------#
#------------------------------- 2. Flatten and Ravel: convert back to 1D vector ------------------------------#
#--------------------------------------------------------------------------------------------------------------#


np.random.seed(1)
matrix2 = np.random.randint(1, 21, size=(4, 5))

print(matrix2)
# [[ 6 12 13  9 10]
#  [12  6 16  1 17]
#  [ 2 13  8 14  7]
#  [19  6 19 12 11]]

#################
## arr.flatten ##
#################

flattened = matrix2.flatten()

print(flattened)
# [ 6 12 13  9 10 12  6 16  1 17  2 13  8 14  7 19  6 19 12 11]
# Convert back to 1D vector, returns a copy

print(np.shares_memory(matrix2, flattened))  # False (different memory location)


###############
## arr.ravel ##
###############

raveled = matrix2.ravel()

print(raveled)
# [ 6 12 13  9 10 12  6 16  1 17  2 13  8 14  7 19  6 19 12 11]
# Convert back to 1D vector, returns a view whenever possible (same memory)

print(np.shares_memory(matrix2, raveled))  # True whenever possible

################
## np.ravel() ##
################

raveled_np = np.ravel(matrix2)
print(raveled_np)
# Works similarly to arr.ravel()


#--------------------------------------------------------------------------------------------------------------#
#------------------------------- 3. arr.resize(dimension): similar to reshape ---------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
arr.resize(dimension):
   Similar to reshape, but:
   - modifies the original array in-place
   - if the new size is larger, fills with zeros
   - returns None

np.resize(arr, newshape):
   - returns a new array
   - if newshape is larger, fills with repeated copies of the original data
'''

np.random.seed(2)
matrix3 = np.random.randint(1, 21, size=(4, 5))

print(matrix3)
# [[ 9 16 14  9 12]
#  [19 12  9  8  3]
#  [18 12 16  6  8]
#  [ 4  7  5 11 12]]
# shape: (4, 5)

########################
## arr.resize (bigger)##
########################

matrix3.resize((6, 5))
print(matrix3)
# [[ 9 16 14  9 12]
#  [19 12  9  8  3]
#  [18 12 16  6  8]
#  [ 4  7  5 11 12]
#  [ 0  0  0  0  0]
#  [ 0  0  0  0  0]]
# shape: (6, 5)
# original modified in-place, extra rows filled with zeros

##########################
## arr.resize (smaller) ##
##########################

matrix3.resize((3, 4))
print(matrix3)
# [[ 9 16 14  9]
#  [12 19 12  9]
#  [ 8  3 18 12]]
# shape: (3, 4)
# truncated in-place

#################
## np.resize() ##
#################

np.random.seed(3)
matrix4 = np.random.randint(1, 21, size=(4, 5))
print(matrix4)
# [[11  4  9  1 20]
#  [11 12 10 11  7]
#  [ 1 13  8 15 18]
#  [ 3  3  2 20  6]]
# original remains unchanged


print(np.resize(matrix4, (6, 5)))
# [[11  4  9  1 20]
#  [11 12 10 11  7]
#  [ 1 13  8 15 18]
#  [ 3  3  2 20  6]
#  [11  4  9  1 20]
#  [11 12 10 11  7]]
# shape: (6, 5)
# repeated copies of original data to fill larger size


print(np.resize(matrix4, (3, 8)))
# [[11  4  9  1 20 11 12 10]
#  [11  7  1 13  8 15 18  3]
#  [ 3  2 20  6 11  4  9  1]]
# shape: (3, 8)
# repeated copies with new shape


print(matrix4)
# original matrix4 is unchanged


#--------------------------------------------------------------------------------------------------------------#
#---------------------------- 4. arr.transpose() or arr.T: Transpose the array --------------------------------#
#--------------------------------------------------------------------------------------------------------------#

np.random.seed(4)
matrix5 = np.random.randint(1, 21, size=(3, 4))

print(matrix5)
# [[15  6  2  9]
#  [ 9 19 10  8]
#  [14  9  5 19]]
# shape: (3, 4)

#####################
## arr.transpose() ##
#####################

print(matrix5.transpose())
# [[15  9 14]
#  [ 6 19  9]
#  [ 2 10  5]
#  [ 9  8 19]]
# shape: (4, 3)

###########
## arr.T ##
###########

print(matrix5.T)
# [[15  9 14]
#  [ 6 19  9]
#  [ 2 10  5]
#  [ 9  8 19]]
# shape: (4, 3)

#######################
## np.transpose(arr) ##
#######################

print(np.transpose(matrix5))
# [[15  9 14]
#  [ 6 19  9]
#  [ 2 10  5]
#  [ 9  8 19]]
# same result as arr.T or arr.transpose()


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 5. Squeeze: remove 1-sized dims --------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
For 2D shapes:
   (1, n) -> (n,)
   (n, 1) -> (n,)
   (m, n, 1) -> (m, n)
   (1, m, n) -> (m, n)
   
   (n,) -> unchanged
   (m, n) with m>1 and n>1 -> unchanged
'''

###############
## row (1,n) ##
###############

row_vector_2d = np.arange(1, 6).reshape(1, 5)
print(row_vector_2d)
# [[1 2 3 4 5]]
# shape (1, 5)


squeezed_row = row_vector_2d.squeeze()
print(squeezed_row)
# [1 2 3 4 5]
# shape (5,)

##############
## col (n,1)##
##############

col_vector_2d = np.arange(1, 6).reshape(5, 1)
print(col_vector_2d)
# [[1]
#  [2]
#  [3]
#  [4]
#  [5]]
# shape (5, 1)


squeezed_col = col_vector_2d.squeeze()
print(squeezed_col)
# [1 2 3 4 5]
# shape (5,)

################
## 3D (m,n,1) ##
################

np.random.seed(4)
matrix_3d = np.random.randint(1, 21, size=(2, 3, 1))
print(matrix_3d)
# [[[15]
#   [ 6]
#   [ 2]]

#  [[ 9]
#   [ 9]
#   [19]]]
# shape: (2, 3, 1)

squeezed_3d = matrix_3d.squeeze()
print(squeezed_3d)
# [[15  6  2]
#  [ 9  9 19]]
# shape: (2, 3)

#######################
## no singleton dims ##
#######################

mat_2x3 = np.arange(1, 7).reshape(2, 3)
print(mat_2x3)
# [[1 2 3]
#  [4 5 6]]
# shape (2, 3)

print(mat_2x3.squeeze())
# [[1 2 3]
#  [4 5 6]]


#--------------------------------------------------------------------------------------------------------------#
#------------------------ 6. np.expand_dims: expand shape by inserting new axis -------------------------------#
#--------------------------------------------------------------------------------------------------------------#

np.random.seed(5)
matrix6 = np.random.randint(1, 21, size=(3, 4))

print(matrix6)
# [[ 4 15 16  7]
#  [17 10  9  5]
#  [ 8 17 17  8]]
# shape: (3, 4)

#######################
## axis=0: (1, 3, 4) ##
#######################

#-------
## np.expand_dims()
#-------

expanded_axis0 = np.expand_dims(matrix6, axis=0)

print(expanded_axis0)
# [[[ 4 15 16  7]
#   [17 10  9  5]
#   [ 8 17 17  8]]]

print(expanded_axis0.shape) # (1, 3, 4)

#-------
## arr[np.newaxis, :, :]
#-------

print(matrix6[np.newaxis, :, :])
# [[[ 4 15 16  7]
#   [17 10  9  5]
#   [ 8 17 17  8]]]

#-------
## arr[np.newaxis, ...]
#-------

print(matrix6[np.newaxis, ...])
# [[[ 4 15 16  7]
#   [17 10  9  5]
#   [ 8 17 17  8]]]

#######################
## axis=1: (3, 1, 4) ##
#######################

#-------
## np.expand_dims()
#-------

expanded_axis1 = np.expand_dims(matrix6, axis=1)

print(expanded_axis1)
# [[[ 4 15 16  7]]

#  [[17 10  9  5]]

#  [[ 8 17 17  8]]]

print(expanded_axis1.shape) # (3, 1, 4)

#-------
## arr[:, np.newaxis, :]
#-------

print(matrix6[:, np.newaxis, :])
# [[[ 4 15 16  7]]

#  [[17 10  9  5]]

#  [[ 8 17 17  8]]]

#######################
## axis=2: (3, 4, 1) ##
#######################

expanded_axis2 = np.expand_dims(matrix6, axis=2)

print(expanded_axis2)
# [[[ 4]
#   [15]
#   [16]
#   [ 7]]

#  [[17]
#   [10]
#   [ 9]
#   [ 5]]

#  [[ 8]
#   [17]
#   [17]
#   [ 8]]]

print(expanded_axis2.shape) # (3, 4, 1)

#-------
## arr[:, :, np.newaxis]
#-------

print(matrix6[:, :, np.newaxis])
# [[[ 4]
#   [15]
#   [16]
#   [ 7]]

#  [[17]
#   [10]
#   [ 9]
#   [ 5]]

#  [[ 8]
#   [17]
#   [17]
#   [ 8]]]

#-------
## arr[..., np.newaxis]
#-------

print(matrix6[..., np.newaxis])
# [[[ 4]
#   [15]
#   [16]
#   [ 7]]

#  [[17]
#   [10]
#   [ 9]
#   [ 5]]

#  [[ 8]
#   [17]
#   [17]
#   [ 8]]]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 7. np.swapaxes(): swap two axes --------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
np.swapaxes(arr, axis1, axis2):

For 2D (m, n):
   + np.swapaxes(arr, 0, 1) is equivalent to transpose: shape becomes (n, m)

For higher dimensions:
   + only the two specified axes are swapped, others stay in place
'''


np.random.seed(6)
matrix7 = np.random.randint(1, 21, size=(3, 4))

print(matrix7)
# [[11 10  4 11]
#  [14 16 11 17]
#  [ 2 12 14 16]]

print(matrix7.shape)   # (3, 4)


########
## 2D ##
########

swapped_2d = np.swapaxes(matrix7, 0, 1)
print(swapped_2d)
# [[11 14  2]
#  [10 16 12]
#  [ 4 11 14]
#  [11 17 16]]

print(swapped_2d.shape)  # (4, 3), same as transpose

########
## 3D ##
########

tensor3d = np.random.randint(1, 10, size=(2, 3, 4))

print(tensor3d)
# [[[6 7 4 6]
#   [2 3 4 7]
#   [9 1 4 8]]

#  [[5 9 2 3]
#   [5 2 6 6]
#   [7 2 1 6]]]

print(tensor3d.shape)    
# (2, 3, 4)

#--------------------------------#

swapped_3d = np.swapaxes(tensor3d, 0, 2)

print(swapped_3d)
# [[[6 5]
#   [2 5]
#   [9 7]]

#  [[7 9]
#   [3 2]
#   [1 2]]

#  [[4 2]
#   [4 6]
#   [4 1]]

#  [[6 3]
#   [7 6]
#   [8 6]]]

print(swapped_3d.shape)  
# (4, 3, 2)


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 8. np.permute_dims(): permute axes --------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
np.permute_dims(arr, axes):

   + Permute (reorder) all axes according to axes
   + For a 3D tensor with shape (d0, d1, d2):

        np.permute_dims(arr, (1, 0, 2)) -> shape (d1, d0, d2)
        np.permute_dims(arr, (2, 0, 1)) -> shape (d2, d0, d1)

   + In newer NumPy / array API, permute_dims is available; if not, np.transpose(arr, axes) does the same thing.
'''

'''NOTE: when use np.permute_dims(), must specify ALL axes in the new order.'''

np.random.seed(7)
tensor3d_2 = np.random.randint(1, 10, size=(2, 3, 4))

print(tensor3d_2)
# [[[5 7 4 4]
#   [8 8 8 9]
#   [9 8 7 5]]

#  [[1 8 1 8]
#   [7 4 6 9]
#   [9 8 6 1]]]

print(tensor3d_2.shape)  
# (2, 3, 4)

###########################
## (1, 0, 2) permutation ##
###########################

perm_1 = np.permute_dims(tensor3d_2, (1, 0, 2))

print(perm_1)
# [[[5 7 4 4]
#   [1 8 1 8]]

#  [[8 8 8 9]
#   [7 4 6 9]]

#  [[9 8 7 5]
#   [9 8 6 1]]]

print(perm_1.shape)   
# (3, 2, 4)

###########################
## (2, 0, 1) permutation ##
###########################

perm_2 = np.permute_dims(tensor3d_2, (2, 0, 1))

print(perm_2)
# [[[5 8 9]
#   [1 7 9]]

#  [[7 8 8]
#   [8 4 8]]

#  [[4 8 7]
#   [1 6 6]]

#  [[4 9 5]
#   [8 9 1]]]

print(perm_2.shape)   
# (4, 2, 3)
