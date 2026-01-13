'''
1. arr.reshape(dimension):
   + arr.reshape((m, n)): reshape to m rows and n columns
   + arr.reshape(-1, n): set columns to n, automatically calculate the other dimension based on n columns
   + arr.reshape(n, -1): set rows to n, automatically calculate the other dimension based on n rows
   + arr.reshape(-1, 1): convert to column vector
   + arr.reshape(1, -1): convert to row vector
   + arr.reshape(-1): convert back to 1D vector
   + np.reshape(arr, newshape): similar to arr.reshape(newshape)

2. Flatten and Ravel: convert back to 1D vector
   + arr.flatten(): convert back to 1D vector, returns a copy
   + arr.ravel(): convert back to 1D vector, returns a view whenever possible (same id, same memory location)
   + np.ravel(arr): similar to arr.ravel()
   
3. arr.resize(dimension): Similar to reshape, 
                          But if the new array is larger than the original array,   
                          then the new array is filled with repeated copies of 0
   + np.resize(arr, newshape): resize with repeated copies of the original array

4. arr.transpose() or arr.T: Transpose the array (swap rows and columns)
   + np.transpose(arr) or np.T(arr): similar to arr.transpose() or arr.T

5. Squeeze:
   + arr.squeeze(): Remove single-dimensional entries from the shape of an array
   + np.squeeze(arr): similar to arr.squeeze()
   
6. Expand dims:
   + np.expand_dims(arr, axis): Expand the shape of an array by inserting a new axis at the specified position
   + arr[np.newaxis, :]: equivalent to np.expand_dims(arr, axis=0)
   + arr[:, np.newaxis]: equivalent to np.expand_dims(arr, axis=1)
   
'''

import numpy as np


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. arr.reshape(dimension) ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

np.random.seed(0)
vector = np.random.randn(12).round(2)
print(vector)
# [ 1.76  0.4   0.98  2.24  1.87 -0.98  0.95 -0.15 -0.1   0.41  0.14  1.45]

print(vector.shape) # (12,)

'''
Possible ways to reshape 1D vector of size 12:

12 = 2x2x3 = 3x2x2 = 2x3x2 (3D matrices)
   = 4x3
   = 3x4
   = 6x2
   = 2x6
   = 12x1
   = 1x12
'''

#######################
## arr.reshape(m, n) ##
#######################

matrix_4x3 = vector.reshape((4, 3))
print(matrix_4x3)
# [[ 1.76  0.4   0.98]
#  [ 2.24  1.87 -0.98]
#  [ 0.95 -0.15 -0.1 ]
#  [ 0.41  0.14  1.45]]

print(vector.reshape((3, 4)))
# [[ 1.76  0.4   0.98  2.24]
#  [ 1.87 -0.98  0.95 -0.15]
#  [-0.1   0.41  0.14  1.45]]

print(vector.reshape((6, 2)))
# [[ 1.76  0.4 ]
#  [ 0.98  2.24]
#  [ 1.87 -0.98]
#  [ 0.95 -0.15]
#  [-0.1   0.41]
#  [ 0.14  1.45]]

print(vector.reshape((2, 6)))
# [[ 1.76  0.4   0.98  2.24  1.87 -0.98]
#  [ 0.95 -0.15 -0.1   0.41  0.14  1.45]]

print(vector.reshape((12, 1)))
# [[ 1.76]
#  [ 0.4 ]
#  [ 0.98]
#  [ 2.24]
#  [ 1.87]
#  [-0.98]
#  [ 0.95]
#  [-0.15]
#  [-0.1 ]
#  [ 0.41]
#  [ 0.14]
#  [ 1.45]]

print(vector.reshape((1, 12)))
# [[ 1.76  0.4   0.98  2.24  1.87 -0.98  0.95 -0.15 -0.1   0.41  0.14  1.45]]

print(vector.reshape((2, 2, 3)))
# [[[ 1.76  0.4   0.98]
#   [ 2.24  1.87 -0.98]]

#  [[ 0.95 -0.15 -0.1 ]
#   [ 0.41  0.14  1.45]]]

print(vector.reshape((5, 3)))
'''ValueError: cannot reshape array of size 12 into shape (5,3)'''

########################
## arr.reshape(-1, n) ##
########################

print(vector.reshape(-1, 6))
# [[ 1.76  0.4   0.98  2.24  1.87 -0.98]
#  [ 0.95 -0.15 -0.1   0.41  0.14  1.45]]
'''set columns to 6, automatically calculate the other dimension based on 6 columns'''

print(vector.reshape(-1, 4))
# [[ 1.76  0.4   0.98  2.24]
#  [ 1.87 -0.98  0.95 -0.15]
#  [-0.1   0.41  0.14  1.45]]
'''set columns to 4, automatically calculate the other dimension based on 4 columns'''

########################
## arr.reshape(n, -1) ##
########################

print(vector.reshape(4, -1))
# [[ 1.76  0.4   0.98]
#  [ 2.24  1.87 -0.98]
#  [ 0.95 -0.15 -0.1 ]
#  [ 0.41  0.14  1.45]]
'''set rows to 4, automatically calculate the other dimension based on 4 rows'''

print(vector.reshape(2, -1))
# [[ 1.76  0.4   0.98  2.24  1.87 -0.98]
#  [ 0.95 -0.15 -0.1   0.41  0.14  1.45]]
'''set rows to 2, automatically calculate the other dimension based on 2 rows'''

########################
## arr.reshape(-1, 1) ##
########################

print(vector.reshape(-1, 1))
# [[ 1.76]
#  [ 0.4 ]
#  [ 0.98]
#  [ 2.24]
#  [ 1.87]
#  [-0.98]
#  [ 0.95]
#  [-0.15]
#  [-0.1 ]
#  [ 0.41]
#  [ 0.14]
#  [ 1.45]]
'''convert to column vector'''

print(vector.reshape(-1, 1).ndim) # 2 (Still counted as 2D matrix)

########################
## arr.reshape(1, -1) ##
########################

print(vector.reshape(1, -1))
# [[ 1.76  0.4   0.98  2.24  1.87 -0.98  0.95 -0.15 -0.1   0.41  0.14  1.45]]
'''convert to row vector'''

print(vector.reshape(1, -1).ndim) # 2 (Still counted as 2D matrix)

#####################
## arr.reshape(-1) ##
#####################

print(vector.reshape(-1))
# [ 1.76  0.4   0.98  2.24  1.87 -0.98  0.95 -0.15 -0.1   0.41  0.14  1.45]
'''convert back to 1D vector'''

print(vector.reshape(-1).ndim) # 1

###############################
## np.reshape(arr, newshape) ##
###############################
'''Works similarly to arr.reshape(newshape)'''

print(np.reshape(vector, (3, 4)))
# [[ 1.76  0.4   0.98  2.24]
#  [ 1.87 -0.98  0.95 -0.15]
#  [-0.1   0.41  0.14  1.45]]


#--------------------------------------------------------------------------------------------------------------#
#------------------------------- 2. Flatten and Ravel: convert back to 1D vector ------------------------------#
#--------------------------------------------------------------------------------------------------------------#

np.random.seed(0)
matrix = np.random.randint(1, 21, size=(4, 5))
print(matrix)
# [[13 16  1  4  4]
#  [ 8 10 20 19  5]
#  [ 7 13  2  7  8]
#  [15 18  6 14  9]]

###################
## arr.flatten() ##
###################
'''
Convert back to 1D vector, returns a copy (with different id, different memory location)
=> Modifying flattened will not affect the original matrix
=> Less memory efficient, slower processing speed
=> But safer to use when you want to ensure the original data remains unchanged
'''

flattened = matrix.flatten()
print(flattened)
# [13 16  1  4  4  8 10 20 19  5  7 13  2  7  8 15 18  6 14  9]

print(np.shares_memory(matrix, flattened)) # False (different memory location)

#################
## arr.ravel() ##
#################
'''
Convert back to 1D vector, returns a view whenever possible (same id, same memory location)
=> Modifying raveled will affect the original matrix
=> More memory efficient, faster processing speed
=> But be cautious when modifying the raveled array, as it will change the original data
'''

raveled = matrix.ravel()
print(raveled)
# [13 16  1  4  4  8 10 20 19  5  7 13  2  7  8 15 18  6 14  9]

print(np.shares_memory(matrix, raveled)) # True (same memory location)

###################
## np.ravel(arr) ##
###################
'''Works similarly to arr.ravel()'''

raveled_np = np.ravel(matrix)
print(raveled_np)
# [13 16  1  4  4  8 10 20 19  5  7 13  2  7  8 15 18  6 14  9]

'''NOTE: np.flatten(arr) does not exist'''


#--------------------------------------------------------------------------------------------------------------#
#------------------------------- 3. arr.resize(dimension): similar to reshape ---------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
arr.resize(dimension): Similar to reshape,
But if the new array is larger than the original array,
then the new array is filled with repeated copies of 0

NOTE: this operation modifies the original array in-place and does not return a new array.
      (new_arr = arr.resize(...) will assign None to new_arr)
'''

np.random.seed(0)
vector = np.random.randn(12).round(2)
print(vector)
# [ 1.76  0.4   0.98  2.24  1.87 -0.98  0.95 -0.15 -0.1   0.41  0.14  1.45]

###################################
## arr.resize() with larger size ##
###################################

vector.resize(18)
print(vector)
# [ 1.76  0.4   0.98  2.24  1.87 -0.98  0.95 -0.15 -0.1   0.41  0.14  1.45
#   0.    0.    0.    0.    0.    0.  ]

vector.resize(3, 8)
print(vector)
# [[ 1.76  0.4   0.98  2.24  1.87 -0.98  0.95 -0.15]
#  [-0.1   0.41  0.14  1.45  0.    0.    0.    0.  ]
#  [ 0.    0.    0.    0.    0.    0.    0.    0.  ]]
'''NOT vector = vector.resize(18)'''

####################################
## arr.resize() with smaller size ##
####################################

vector.resize(5)
print(vector)
# [1.76 0.4  0.98 2.24 1.87]

##############################
## np.resize(arr, newshape) ##
##############################
'''
Works similarly to arr.resize(newshape)

BUT if the new array is larger than the original array,
then the new array is filled with repeated copies of the original array
'''

vector = np.random.randn(12).round(2)
print(vector)
# [ 1.76  0.4   0.98  2.24  1.87 -0.98  0.95 -0.15 -0.1   0.41  0.14  1.45]

print(np.resize(vector, 18))
# [ 0.18 -0.46 -1.09  0.64 -0.39 -0.78  1.   -1.93  0.25 -0.03 -0.14 -0.19
#   0.18 -0.46 -1.09  0.64 -0.39 -0.78]

print(np.resize(vector, (3, 8)))
# [[ 0.76  0.12  0.44  0.33  1.49 -0.21  0.31 -0.85]
#  [-2.55  0.65  0.86 -0.74  0.76  0.12  0.44  0.33]
#  [ 1.49 -0.21  0.31 -0.85 -2.55  0.65  0.86 -0.74]]


#--------------------------------------------------------------------------------------------------------------#
#---------------------------- 4. arr.transpose() or arr.T: Transpose the array --------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
arr.transpose() or arr.T: Transpose the array (swap rows and columns)

(n, 1) -->  (1, n)
(1, n) -->  (n, 1)
'''

########################
## with (n, 1) vector ##
########################

np.random.seed(0)
col_vector = np.random.randn(5,1).round(2)

#---
## Before transpose
#---

print(col_vector)
# [[1.76]
#  [0.4 ]
#  [0.98]
#  [2.24]
#  [1.87]]

#---
## After transpose
#---

print(col_vector.transpose())
# [[1.76 0.4  0.98 2.24 1.87]]

print(col_vector.T)
# [[1.76 0.4  0.98 2.24 1.87]]

########################
## with (1, n) vector ##
########################

np.random.seed(0)
row_vector = np.random.randn(1,5).round(2)

#---
## Before transpose
#---

print(row_vector)
# [[1.76 0.4  0.98 2.24 1.87]]

#---
## After transpose
#---

print(row_vector.transpose())
# [[1.76]
#  [0.4 ]
#  [0.98]
#  [2.24]
#  [1.87]]

print(row_vector.T)
# [[1.76]
#  [0.4 ]
#  [0.98]
#  [2.24]
#  [1.87]]

#--------------------------------------------------------------------------------------------------------------#
#--------------------------- 5. arr.squeeze(): remove single-dimensional entries ------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
arr.squeeze(): Remove single-dimensional entries from the shape of an array

(n, 1) -->  (n,)
(1, n) -->  (n,)
'''

########################
## with (n, 1) vector ##
########################

np.random.seed(0)
col_vector = np.random.randn(5,1).round(2)

#---
## Before squeeze
#---

print(col_vector)
# [[1.76]
#  [0.4 ]
#  [0.98]
#  [2.24]
#  [1.87]]

print(col_vector.shape) # (5, 1)
print(col_vector.ndim)  # 2

#---
## After squeeze
#---

squeezed_col_vector = col_vector.squeeze()

print(squeezed_col_vector)
# [1.76 0.4  0.98 2.24 1.87]

print(squeezed_col_vector.shape) # (5,)
print(squeezed_col_vector.ndim)  # 1

########################
## with (1, n) vector ##
########################

np.random.seed(0)
row_vector = np.random.randn(1,5).round(2)

#---
## Before squeeze
#---

print(row_vector)
# [[1.76 0.4  0.98 2.24 1.87]]

print(row_vector.shape) # (1, 5)
print(row_vector.ndim)  # 2

#---
## After squeeze
#---

squeezed_row_vector = row_vector.squeeze()

print(squeezed_row_vector)
# [1.76 0.4  0.98 2.24 1.87]

print(squeezed_row_vector.shape) # (5,)
print(squeezed_row_vector.ndim)  # 1


#--------------------------------------------------------------------------------------------------------------#
#------------------------ 6. np.expand_dims(): expand shape by inserting new axis -----------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
np.expand_dims(arr, axis): Expand the shape of an array 
by inserting a new axis at the specified position
'''

np.random.seed(0)
vector = np.random.randn(12).round(2)
print(vector)
# [ 1.76  0.4   0.98  2.24  1.87 -0.98  0.95 -0.15 -0.1   0.41  0.14  1.45]

####################################
## axis=0 (convert to row vector) ##
####################################

print(np.expand_dims(vector, axis=0))
# [[ 0.76  0.12  0.44  0.33  1.49 -0.21  0.31 -0.85 -2.55  0.65  0.86 -0.74]]

print(np.expand_dims(vector, axis=0).shape) # (1, 12)

#######################################
## axis=1 (convert to column vector) ##
#######################################

print(np.expand_dims(vector, axis=1))
# [[ 0.76]
#  [ 0.12]
#  [ 0.44]
#  [ 0.33]
#  [ 1.49]
#  [-0.21]
#  [ 0.31]
#  [-0.85]
#  [-2.55]
#  [ 0.65]
#  [ 0.86]
#  [-0.74]]

print(np.expand_dims(vector, axis=1).shape) # (12, 1)

######################
## Using np.newaxis ##
######################
'''np.newaxis can be used to increase the dimensions of the existing array by one more dimension,'''

print(vector[np.newaxis, :])
# [[ 1.76  0.4   0.98  2.24  1.87 -0.98  0.95 -0.15 -0.1   0.41  0.14  1.45]]
# shape: (1, 12)
# equivalent to np.expand_dims(vector, axis=0)

print(vector[:, np.newaxis])
# [[ 1.76]
#  [ 0.4 ]
#  [ 0.98]
#  [ 2.24]
#  [ 1.87]
#  [-0.98]
#  [ 0.95]
#  [-0.15]
#  [-0.1 ]
#  [ 0.41]
#  [ 0.14]
#  [ 1.45]]
# shape: (12, 1)
# equivalent to np.expand_dims(vector, axis=1)