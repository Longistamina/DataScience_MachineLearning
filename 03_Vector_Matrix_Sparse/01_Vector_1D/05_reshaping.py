'''
1. arr.reshape(dimension):
   + Reshape to 2D matrix with specified dimensions
   + arr.reshape(-1, n): set columns to n, automatically calculate the other dimension based on n columns
   + arr.reshape(n, -1): set rows to n, automatically calculate the other dimension based on n rows
   + arr.reshape(-1, 1): convert to column vector
   + arr.reshape(1, -1): convert to row vector
   + arr.reshape(-1): convert back to 1D vector

2. Flatten and Ravel: convert back to 1D vector
   + arr.flatten(): convert back to 1D vector, returns a copy
   + arr.ravel(): convert back to 1D vector, returns a view whenever possible (same id, same memory location)

3. arr.resize(dimension): Similar to reshape, 
                          But if the new array is larger than the original array, 
'''

import numpy as np


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. arr.reshape(dimension) ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

np.random.seed(0)
vector = np.random.randn(12).round(2)
print(vector)
# [ 1.76  0.4   0.98  2.24  1.87 -0.98  0.95 -0.15 -0.1   0.41  0.14  1.45]

###################
## arr.reshape() ##
###################

matrix_3x4 = vector.reshape((3, 4))
print(matrix_3x4)
# [[ 1.76  0.4   0.98  2.24]
#  [ 1.87 -0.98  0.95 -0.15]
#  [-0.1   0.41  0.14  1.45]]

print(vector.reshape((4, 3)))
# [[ 1.76  0.4   0.98]
#  [ 2.24  1.87 -0.98]
#  [ 0.95 -0.15 -0.1 ]
#  [ 0.41  0.14  1.45]]

########################
## arr.reshape(-1, n) ##
########################

print(vector.reshape(-1, 6))
# [[ 1.76  0.4   0.98  2.24  1.87 -0.98]
#  [ 0.95 -0.15 -0.1   0.41  0.14  1.45]]
'''set columns to 6, automatically calculate the other dimension based on 6 columns'''

########################
## arr.reshape(n, -1) ##
########################

print(vector.reshape(4, -1))
# [[ 1.76  0.4   0.98]
#  [ 2.24  1.87 -0.98]
#  [ 0.95 -0.15 -0.1 ]
#  [ 0.41  0.14  1.45]]
'''set rows to 4, automatically calculate the other dimension based on 4 rows'''

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


#--------------------------------------------------------------------------------------------------------------#
#------------------------------- 3. arr.resize(dimension): similar to reshape ---------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
arr.resize(a, dimension): Similar to reshape,
But if the new array is larger than the original array,
then the new array is filled with repeated copies of a

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

'''NOT vector = vector.resize(18)'''

####################################
## arr.resize() with smaller size ##
####################################

vector.resize(5)
print(vector)
# [1.76 0.4  0.98 2.24 1.87]