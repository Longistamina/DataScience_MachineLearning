'''
1. Statistical reduction methods:
   + arr.sum(): Computes the sum of all elements in the vector.
   + arr.mean(): Computes the mean of all elements in the vector.
   + arr.prod(): Computes the product of all elements in the vector.
   + arr.max(): Finds the maximum value in the vector.
   + arr.min(): Finds the minimum value in the vector.
   + np.ptp(arr): Computes the peak-to-peak (max - min) value of the vector. (i.e., range)
   + arr.var(): Computes the variance of the elements in the vector.
   + arr.std(): Computes the standard deviation of the elements in the vector.

2. Cumulative methods:
   + arr.cumsum(): Computes the cumulative sum of the elements in the vector.
   + arr.cumprod(): Computes the cumulative product of the elements in the vector.

3. Rounding and clipping methods:
   + arr.round(decimals=...): Rounds each element in the vector to the specified
   + arr.clip(min=..., max=...): Clips (limits) the values in the vector to be within the specified minimum and maximum bounds.

4. Complex number methods:
   + arr.real: Returns a new vector containing the real parts of the complex numbers.
   + arr.imag: Returns a new vector containing the imaginary parts of the complex numbers.
   + arr.conj(): Returns a new vector containing the complex conjugates of the complex numbers.
   + arr.conjugate(): same as arr.conj().

5. Dot product:
   + arr1.dot(arr2): Computes the dot product between two vectors of the same length.
   + arr1 @ arr2: Another syntax to compute the dot product between two vectors of the same length.
   + Between row_vector and column_vector: can result in either a scalar or a matrix depending on the order of multiplication.
'''

import numpy as np

np.random.seed(42)
vector = np.random.uniform(1, 8.1, size=5).round(2)

print(vector)
# [3.66 7.75 6.2  5.25 2.11]


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. Statistical reduction methods --------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

###############
## arr.sum() ##
###############
'''Computes the sum of all elements in the vector.'''

print(vector.sum())
# 24.97

################
## arr.mean() ##
################
'''Computes the mean of all elements in the vector.'''

print(vector.mean())
# 4.994

################
## arr.prod() ##
################
'''Computes the product of all elements in the vector.'''

print(vector.prod())
# 1948.1223825000002 (= 3.66 * 7.75 * 6.2 * 5.25 * 2.11)

###############
## arr.max() ##
###############
'''Finds the maximum value in the vector.'''

print(vector.max())
# 7.75

###############
## arr.min() ##
###############
'''Finds the minimum value in the vector.'''

print(vector.min())
# 2.11

#################
## np.ptp(arr) ##
#################
'''Computes the peak-to-peak (max - min) value of the vector. (i.e., range)'''

print(np.ptp(vector))
# 5.640000000000001 (= 7.75 - 2.11)

###############
## arr.var() ##
###############
'''Computes the variance of the elements in the vector.'''

print(vector.var())
# 3.8425040000000004

###############
## arr.std() ##
###############
'''Computes the standard deviation of the elements in the vector.'''

print(vector.std())
# 1.9602305986796555


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 2. Cumulative methods -----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

print(vector)
# [3.66 7.75 6.2  5.25 2.11]

##################
## arr.cumsum() ##
##################
'''Computes the cumulative sum of the elements in the vector.'''

print(vector.cumsum())
# [ 3.66 11.41 17.61 22.86 24.97]
'''
3.66 = 3.66
11.41 = 3.66 + 7.75
17.61 = 3.66 + 7.75 + 6.2
22.86 = 3.66 + 7.75 + 6.2 + 5.25
24.97 = 3.66 + 7.75 + 6.2 + 5.25 + 2.11
'''

###################
## arr.cumprod() ##
###################
'''Computes the cumulative product of the elements in the vector.'''

print(vector.cumprod())
# [   3.66        28.365      175.863      923.28075   1948.1223825]
'''
3.66 = 3.66
28.365 = 3.66 * 7.75
175.863 = 3.66 * 7.75 * 6.2
923.28075 = 3.66 * 7.75 * 6.2 * 5.25
1948.1223825 = 3.66 * 7.75 * 6.2 * 5.25 * 2.11
'''


#---------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 3. Rounding and clipping methods ---------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

print(vector)
# [3.66 7.75 6.2  5.25 2.11]

#################
## arr.round() ##
#################
'''Rounds each element in the vector to the specified number of decimals.'''

print(vector.round(decimals=1))
# [3.7 7.8 6.2 5.3 2.1]

print(vector.round(decimals=4))
# [3.66 7.75 6.2  5.25 2.11]
'''Stay the same since the original vector has only 2 decimal places.'''

################
## arr.clip() ##
################
'''Clips (limits) the values in the vector to be within the specified minimum and maximum bounds.'''

print(vector.clip(min=4.0, max=7.0))
# [4.   7.   6.2  5.25 4.  ]
'''Values less than 4.0 are set to 4.0, and values greater than 7.0 are set to 7.0.'''


#---------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 4. Complex number methods --------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

vector_complex = np.array([3+4j, 1-2j, -5+0j, 0+6j, -3-3j])
print(vector_complex)
# [ 3.+4.j  1.-2.j -5.+0.j  0.+6.j -3.-3.j]

##############
## arr.real ##
##############
'''Returns a new vector containing the real parts of the complex numbers.'''

print(vector_complex.real)
# [ 3.  1. -5.  0. -3.]

##############
## arr.imag ##
##############
'''Returns a new vector containing the imaginary parts of the complex numbers.'''

print(vector_complex.imag)
# [ 4. -2.  0.  6. -3.]

################
## arr.conj() ##
################
'''
Returns a new vector containing the complex conjugates of the complex numbers.

The complex conjugate of a complex number is obtained by changing the sign of its imaginary part.
For example, the complex conjugate of a + bj is a - bj.
'''

print(vector_complex.conj())
# [ 3.-4.j  1.+2.j -5.-0.j  0.-6.j -3.+3.j]

#####################
## arr.conjugate() ##
#####################
'''Works the same as arr.conj().'''

print(vector_complex.conjugate())
# [ 3.-4.j  1.+2.j -5.-0.j  0.-6.j -3.+3.j]


#---------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 5. Dot product ---------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

vector1 = np.array([1, 2, 3])
vector2 = np.array([4, 5, 6])

####################
## arr1.dot(arr2) ##
####################
'''Computes the dot product between two vectors of the same length.'''

print(vector1.dot(vector2))
# 32 (= 1*4 + 2*5 + 3*6)

#################
## arr1 @ arr2 ##
#################
'''Another syntax to compute the dot product between two vectors of the same length.'''

print(vector1 @ vector2)
# 32 (= 1*4 + 2*5 + 3*6)

##########################################
## Between row_vector and column_vector ##
##########################################
'''
Dot product can also be computed between a row vector and a column vector.
However, the result might be different depending on the order of multiplication.
'''

np.random.seed(42)
row_vector = np.random.uniform(1, 8.1, size=(1, 5)).round(2)
column_vector = np.random.uniform(12, 19.2, size=(5, 1)).round(2)

print(row_vector)
# [[3.66 7.75 6.2  5.25 2.11]]

print(column_vector)
# [[13.12]
#  [12.42]
#  [18.24]
#  [16.33]
#  [17.1 ]]

'''Row vector @ Column vector => (1, 5) @ (5, 1) = (1, 1) => Scalar'''
print(row_vector @ column_vector)
# [[  389.2057]]

'''Column vector @ Row vector => (5, 1) @ (1, 5) = (5, 5) => Matrix'''
print(column_vector @ row_vector)
# [[ 48.0192 101.68    81.344   68.88    27.6832]
#  [ 45.4572  96.255   77.004   65.205   26.2062]
#  [ 66.7584 141.36   113.088   95.76    38.4864]
#  [ 59.7678 126.5575 101.246   85.7325  34.4563]
#  [ 62.586  132.525  106.02    89.775   36.081 ]]