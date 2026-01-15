'''
1. Statistical reduction methods:
   + arr.sum(axis=...): Computes the sum along the specified axis. 
                     axis=None sums all elements, 
                     axis=0 sums vertically (column-wise), 
                     axis=1 sums horizontall (row-wise).
   + arr.mean(axis=...): Computes the mean along the specified axis.
   + arr.prod(axis=...): Computes the product along the specified axis.
   + arr.max(axis=...): Finds the maximum value along the specified axis.
   + arr.min(axis=...): Finds the minimum value along the specified axis.
   + np.ptp(arr, axis=...): Computes the peak-to-peak (max - min) value along the specified axis.
   + arr.var(axis=...): Computes the variance along the specified axis.
   + arr.std(axis=...): Computes the standard deviation along the specified axis.

2. Cumulative methods:
   + arr.cumsum(axis=...): Computes the cumulative sum along the specified axis.
   + arr.cumprod(axis=...): Computes the cumulative product along the specified axis.

3. Rounding and clipping methods:
   + arr.round(decimals=...): Rounds each element in the matrix to the specified number of decimals.
   + arr.clip(min=..., max=...): Clips (limits) the values in the matrix to be within the specified minimum and maximum bounds.

4. Complex number methods:
   + arr.real: Returns a new matrix containing the real parts of the complex numbers.
   + arr.imag: Returns a new matrix containing the imaginary parts of the complex numbers.
   + arr.conj(): Returns a new matrix containing the complex conjugates of the complex numbers.
   + arr.conjugate(): same as arr.conj().

5. Matrix multiplication and transpose:
   + arr1.dot(arr2): Computes the matrix multiplication between two matrices with compatible dimensions.
   + arr1 @ arr2: Another syntax to compute the matrix multiplication between two matrices with compatible dimensions.
   + arr.T: Returns the transpose of the matrix (rows become columns and vice versa).
   + arr.transpose(): Another method to get the transpose of the matrix.

6. Examples for 3D and 4D matrices:
   + Operations on higher-dimensional arrays follow similar patterns with additional axis parameters.
   + axis=0, axis=1, axis=2, etc. specify which dimension to operate along.
'''

import numpy as np

np.random.seed(42)
matrix = np.random.uniform(1, 8.1, size=(3, 4)).round(2)

print(matrix)
# [[3.66 7.75 6.2  5.25]
#  [2.11 2.11 1.41 7.15]
#  [5.27 6.03 1.15 7.89]]


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. Statistical reduction methods --------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

###############
## arr.sum() ##
###############
'''Computes the sum along the specified axis.'''

print(matrix.sum())
# 55.98 (sum of all elements)

print(matrix.sum(axis=0))
# [11.04 15.89  8.76 20.29] (sum vertically, i.e., column-wise)
'''
11.04 = 3.66 + 2.11 + 5.27
15.89 = 7.75 + 4.88 + 3.26
8.76  = 6.20 + 8.10 + 1.69
20.29 = 5.25 + 7.32 + 7.72
'''

print(matrix.sum(axis=1))
# [22.86 12.78 20.34] (sum horizontally, i.e., row-wise)
'''
22.86 = 3.66 + 7.75 + 6.20 + 5.25
12.78 = 2.11 + 4.88 + 8.10 + 7.32
20.34 = 5.46 + 3.38 + 1.69 + 5.25
'''

################
## arr.mean() ##
################
'''Computes the mean along the specified axis.'''

print(matrix.mean())
# 4,665 (mean of all elements)

print(matrix.mean(axis=0))
# [3.68   5.2967 2.92   6.7633] (mean vertically, i.e., column-wise)

print(matrix.mean(axis=1))
# [5.715  3.395  5.085 ] (mean horizontally, i.e., row-wise)

################
## arr.prod() ##
################
'''Computes the product along the specified axis.'''

print(matrix.prod())
# 11948863.963780865 (product of all elements)

print(matrix.prod(axis=0))
# [ 40.698102  98.605575  10.0533   296.170875] (product vertically, i.e., column-wise)

print(matrix.prod(axis=1))
# [923.28075     44.88384615 288.33859035] (product horizontally, i.e., row-wise)

###############
## arr.max() ##
###############
'''Finds the maximum value along the specified axis.'''

print(matrix.max())
# 7.89 (maximum of all elements)

print(matrix.max(axis=0))
# [5.27 7.75 6.2  7.89] (maximum vertically, i.e., column-wise)

print(matrix.max(axis=1))
# [7.75 7.15 7.89] (maximum horizontally, i.e., row-wise)

###############
## arr.min() ##
###############
'''Finds the minimum value along the specified axis.'''

print(matrix.min())
# 1.15 (minimum of all elements)

print(matrix.min(axis=0))
# [2.11 2.11 1.15 5.25] (minimum vertically, i.e., column-wise)

print(matrix.min(axis=1))
# [3.66 1.41 1.15] (minimum horizontally, i.e., row-wise)

#################
## np.ptp(arr) ##
#################
'''Computes the peak-to-peak (max - min) value along the specified axis.'''

print(np.ptp(matrix))
# 6.74 (peak-to-peak of all elements: 7.89 - 1.15)

print(np.ptp(matrix, axis=0))
# [3.16 5.64 5.05 2.64] (range vertically, i.e., column-wise)

print(np.ptp(matrix, axis=1))
# [4.09 5.74 6.74] (range horizontally, i.e., row-wise)

###############
## arr.var() ##
###############
'''Computes the variance along the specified axis.'''

print(matrix.var())
# 5.669758333333334 (variance of all elements)

print(matrix.var(axis=0))
# [1.66446667 5.57048889 5.39046667 1.23635556] (variance vertically, i.e., column-wise)

print(matrix.var(axis=1))
# [2.203925 5.295675 6.069875] (variance horizontally, i.e., row-wise)

###############
## arr.std() ##
###############
'''Computes the standard deviation along the specified axis.'''

print(matrix.std())
# 2.381125434187232 (standard deviation of all elements)

print(matrix.std(axis=0))
# [1.29014211 2.36018832 2.32173785 1.11191526] (standard deviation vertically, i.e., column-wise)

print(matrix.std(axis=1))
# [1.48456223 2.30123336 2.46371163] (standard deviation horizontally, i.e., row-wise)


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 2. Cumulative methods -----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

print(matrix)
# [[3.66 7.75 6.2  5.25]
#  [2.11 2.11 1.41 7.15]
#  [5.27 6.03 1.15 7.89]]

##################
## arr.cumsum() ##
##################
'''Computes the cumulative sum along the specified axis.'''

print(matrix.cumsum())
# [ 3.66 11.41 17.61 22.86 24.97 27.08 28.49 35.64 40.91 46.94 48.09 55.98]
# (cumulative sum of flattened matrix)

print(matrix.cumsum(axis=0))
# [[ 3.66  7.75  6.2   5.25]
#  [ 5.77  9.86  7.61 12.4 ]
#  [11.04 15.89  8.76 20.29]]
'''
Row 0: [3.66, 7.75, 6.20, 5.25]
Row 1: [3.66+2.11, 7.75+4.88, 6.20+8.10, 5.25+7.32]
Row 2: [5.77+5.46, 12.63+3.38, 15.71+1.69, 12.4+7.89]
'''

print(matrix.cumsum(axis=1))
# [[ 3.66 11.41 17.61 22.86]
#  [ 2.11  4.22  5.63 12.78]
#  [ 5.27 11.3  12.45 20.34]]
'''
Row 0: [3.66, 3.66+7.75, 11.41+6.20, 17.61+5.25]
Row 1: [2.11, 2.11+4.88, 7.99+8.10, 15.09+7.32]
Row 2: [5.46, 5.46+3.38, 8.84+1.69, 10.53+5.25]
'''

###################
## arr.cumprod() ##
###################
'''Computes the cumulative product along the specified axis.'''

print(matrix.cumprod())
# [3.66000000e+00 2.83650000e+01 1.75863000e+02 9.23280750e+02
#  1.94812238e+03 4.11053823e+03 5.79585890e+03 4.14403911e+04
#  2.18390861e+05 1.31689689e+06 1.51443143e+06 1.19488640e+07]
# (cumulative product of flattened matrix)

print(matrix.cumprod(axis=0))
# [[  3.66       7.75       6.2        5.25    ]
#  [  7.7226    16.3525     8.742     37.5375  ]
#  [ 40.698102  98.605575  10.0533   296.170875]]
'''
Row 0: [3.66, 7.75, 6.20, 5.25]
Row 1: [3.66*2.11, 7.75*4.88, 6.20*8.10, 5.25*7.32]
Row 2: [7.7226*5.46, 16.3525*3.38, 8.742*1.69, 37.5375*7.89]
'''

print(matrix.cumprod(axis=1))
# [[  3.66        28.365      175.863      923.28075   ]
#  [  2.11         4.4521       6.277461    44.88384615]
#  [  5.27        31.7781      36.544815   288.33859035]]
'''
Row 0: [3.66, 3.66*7.75, 28.365*6.20, 175.863*5.25]
Row 1: [2.11, 2.11*4.88, 10.2968*8.10, 83.41848*7.32]
Row 2: [5.46, 5.46*3.38, 18.4548*1.69, 31.1696*5.25]
'''


#---------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 3. Rounding and clipping methods ---------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

print(matrix)
# [[3.66 7.75 6.2  5.25]
#  [2.11 2.11 1.41 7.15]
#  [5.27 6.03 1.15 7.89]]

#################
## arr.round() ##
#################
'''Rounds each element in the matrix to the specified number of decimals.'''

print(matrix.round(decimals=1))
# [[3.7 7.8 6.2 5.2]
#  [2.1 2.1 1.4 7.2]
#  [5.3 6.  1.2 7.9]]

print(matrix.round(decimals=0))
# [[4. 8. 6. 5.]
#  [2. 2. 1. 7.]
#  [5. 6. 1. 8.]]

################
## arr.clip() ##
################
'''Clips (limits) the values in the matrix to be within the specified minimum and maximum bounds.'''

print(matrix.clip(min=4.0, max=7.0))
# [[4.   7.   6.2  5.25]
#  [4.   4.   4.   7.  ]
#  [5.27 6.03 4.   7.  ]]
'''Values less than 4.0 are set to 4.0, and values greater than 7.0 are set to 7.0.'''


#---------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 4. Complex number methods --------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

matrix_complex = np.array([[3+4j, 1-2j], [-5+0j, 0+6j], [-3-3j, 2+1j]])

print(matrix_complex)
# [[ 3.+4.j  1.-2.j]
#  [-5.+0.j  0.+6.j]
#  [-3.-3.j  2.+1.j]]

##############
## arr.real ##
##############
'''Returns a new matrix containing the real parts of the complex numbers.'''

print(matrix_complex.real)
# [[ 3.  1.]
#  [-5.  0.]
#  [-3.  2.]]

##############
## arr.imag ##
##############
'''Returns a new matrix containing the imaginary parts of the complex numbers.'''

print(matrix_complex.imag)
# [[ 4. -2.]
#  [ 0.  6.]
#  [-3.  1.]]

################
## arr.conj() ##
################
'''
Returns a new matrix containing the complex conjugates of the complex numbers.
The complex conjugate of a complex number is obtained by changing the sign of its imaginary part.
For example, the complex conjugate of a + bj is a - bj.
'''

print(matrix_complex.conj())
# [[ 3.-4.j  1.+2.j]
#  [-5.-0.j  0.-6.j]
#  [-3.+3.j  2.-1.j]]

#####################
## arr.conjugate() ##
#####################
'''Works the same as arr.conj().'''

print(matrix_complex.conjugate())
# [[ 3.-4.j  1.+2.j]
#  [-5.-0.j  0.-6.j]
#  [-3.+3.j  2.-1.j]]


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------- 5. Matrix multiplication and transpose ------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

matrix1 = np.array([[1, 2, 3],
                    [4, 5, 6]])

matrix2 = np.array([[7, 8],
                    [9, 10],
                    [11, 12]])

print(matrix1)
# [[1 2 3]
#  [4 5 6]]

print(matrix2)
# [[ 7  8]
#  [ 9 10]
#  [11 12]]

####################
## arr1.dot(arr2) ##
####################
'''Computes the matrix multiplication between two matrices with compatible dimensions.'''

print(matrix1.dot(matrix2))
# [[ 58  64]
#  [139 154]]

'''
Result[0,0] = 1*7 + 2*9 + 3*11 = 58
Result[0,1] = 1*8 + 2*10 + 3*12 = 64
Result[1,0] = 4*7 + 5*9 + 6*11 = 139
Result[1,1] = 4*8 + 5*10 + 6*12 = 154
'''

#################
## arr1 @ arr2 ##
#################
'''Another syntax to compute the matrix multiplication between two matrices with compatible dimensions.'''

print(matrix1 @ matrix2)
# [[ 58  64]
#  [139 154]]

###########
## arr.T ##
###########
'''Returns the transpose of the matrix (rows become columns and vice versa).'''

print(matrix1)
# [[1 2 3]
#  [4 5 6]]

print(matrix1.T)
# [[1 4]
#  [2 5]
#  [3 6]]
'''Original shape (2, 3) becomes (3, 2) after transpose.'''

#####################
## arr.transpose() ##
#####################
'''Another method to get the transpose of the matrix.'''

print(matrix2)
# [[ 7  8]
#  [ 9 10]
#  [11 12]]

print(matrix2.transpose())
# [[ 7  9 11]
#  [ 8 10 12]]


#---------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 6. Examples for 3D and 4D matrices -------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

#######################
## 3D Matrix Example ##
#######################

np.random.seed(100)
matrix_3d = np.random.uniform(1, 10, size=(2, 3, 4)).round(2)

print(matrix_3d)
# [[[5.89 3.51 4.82 8.6 ]
#   [1.04 2.09 7.04 8.43]
#   [2.23 6.18 9.02 2.88]]

#  [[2.67 1.98 2.98 9.81]
#   [8.31 2.55 8.35 3.47]
#   [4.89 9.46 8.36 4.03]]]

print(matrix_3d.shape)
# (2, 3, 4) => 2 matrices of shape (3, 4)

#-------
## Statistical operations with axis parameter
#-------

print(matrix_3d.sum(axis=0))  # Sum along the first dimension (stacks)
# [[ 8.56  5.49  7.8  18.41]
#  [ 9.35  4.64 15.39 11.9 ]
#  [ 7.12 15.64 17.38  6.91]]
'''
8.56 = 5.89 + 2.67
5.49 = 3.51 + 1.98
'''

print(matrix_3d.sum(axis=1))  # Sum along the second dimension (vertically)
# [[ 9.16 11.78 20.88 19.91]
#  [15.87 13.99 19.69 17.31]]
'''
9.16 = 5.89 + 1.04 + 2.23
11.78 = 3.51 + 2.09 + 6.18
'''

print(matrix_3d.sum(axis=2))  # Sum along the third dimension (horizontally)
# [[22.82 18.6  20.31]
#  [17.44 22.68 26.74]]
'''
22.82 = 5.89 + 3.51 + 4.82 + 8.6
18.6  = 1.04 + 2.09 + 7.04 + 8.43
'''

print(matrix_3d.mean(axis=(0, 2)))  # Mean along stacks and horizontally
# [5.0325  5.16    5.88125]
'''
For each row across all matrices, compute the mean of all elements in that row.
5.0325 = (5.89 + 3.51 + 4.82 + 8.6 + 2.67 + 1.98 + 2.98 + 9.81) / 8
'''

#------
## Cumulative methods
#------

print(matrix_3d.cumsum(axis=0))  # Cumulative sum along stacks
# [[[ 2.58  4.36  1.05  3.27]
#   [ 8.16  1.14  6.39  6.43]
#   [ 1.95  4.44  1.33  9.01]]

#  [[12.41  5.9  10.06  9.46]
#   [15.84  7.81 12.63  7.61]
#   [ 4.84 10.34  9.25 12.27]]]
'''
Each element in the second matrix is the sum of the corresponding elements in the first and second matrices.
2.58 = 2.58
12.41 = 2.58 + 9.83
'''

#######################
## 4D Matrix Example ##
#######################

np.random.seed(200)
matrix_4d = np.random.uniform(1, 5, size=(2, 2, 3, 3)).round(2)

print(matrix_4d)
# [[[[4.79 1.91 3.38]
#    [2.71 4.06 1.01]
#    [2.43 4.64 2.82]]

#   [[4.93 4.47 4.94]
#    [4.69 2.21 4.38]
#    [1.48 4.14 2.  ]]]


#  [[[1.38 4.77 4.3 ]
#    [3.07 4.49 3.31]
#    [2.8  3.72 2.68]]

#   [[3.56 3.43 1.42]
#    [4.86 4.03 3.72]
#    [2.32 1.11 4.21]]]]

print(matrix_4d.shape)
# (2, 2, 3, 3) => 2 batches, each with 2 matrices of shape (3, 3)

#-------
## Statistical operations with axis parameter
#-------

print(matrix_4d.mean(axis=0))  # Mean along batches
# [[[3.085 3.34  3.84 ]
#   [2.89  4.275 2.16 ]
#   [2.615 4.18  2.75 ]]

#  [[4.245 3.95  3.18 ]
#   [4.775 3.12  4.05 ]
#   [1.9   2.625 3.105]]]

print(matrix_4d.max(axis=(2, 3)))  # Max vertically and horizontally
# [[4.79 4.94]
#  [4.77 4.86]]
'''
For each (batch, depth), find the maximum value in the (3, 3) matrix.
'''

print(matrix_4d.sum(axis=(0, 1)))  # Sum along batches and depth
# [[14.66 14.58 14.04]
#  [15.33 14.79 12.42]
#  [ 9.03 13.61 11.71]]
'''
Sum all values at each (row, column) position across all batches and depth levels.
'''

#------
## Transpose method for 4D matrices
#------

print(matrix_4d.transpose(0, 3, 1, 2).shape)
# (2, 3, 2, 3) => Swaps depth and columns dimensions

print(matrix_4d.transpose(3, 2, 1, 0).shape)
# (3, 3, 2, 2) => Swaps batches and rows dimensions

'''
Key insights for higher-dimensional arrays:
- axis=0 operates along the first dimension
- axis=1 operates along the second dimension
- axis=-1 operates along the last dimension
- axis=-2 operates along the second-to-last dimension
- Multiple axes can be specified as tuples: axis=(0, 1)
- Broadcasting rules apply for element-wise operations
- Reshape and transpose become increasingly powerful tools
'''
