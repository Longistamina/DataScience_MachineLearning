'''
1. np.positive(): returns an array with the positive values of the input array.
2. np.negative(): returns an array with the negative values of the input array.
3. np.add(): adds arrays element-wise.
4. np.subtract(): subtracts arrays element-wise.
5. np.multiply(): multiplies arrays element-wise.
6. np.divide() or np.true_divide(): divides arrays element-wise.
7. np.reciprocal(): computes the reciprocal (1/x) of each element in the array.
8. np.floor_divide(): performs floor division on arrays element-wise.
9. np.remainder() or np.mod(): computes the element-wise remainder of division (modulus).
10. np.divmod(): returns the quotient and remainder of division of the input arrays.
11. np.fmod(): computes the element-wise remainder of division, similar to np.remainder().
12. np.modf(): returns the fractional and integral parts of an array.
13. np.power() or np.pow(): raises elements of one array to the powers of another array element-wise.
14. np.float_power(): raises elements of one array to the powers of another array element-wise, using float precision.
15. np.absolute() or np.abs(): computes the absolute values of each element in the array.
16. np.fabs(): computes the absolute values of each element in the array (don't handle complex).
17. np.square(): computes the square of each element in the array.
18. np.sqrt(): computes the square root of each element in the array.
19. np.cbrt(): computes the cube root of each element in the array.
20. np.sign(): returns an array indicating the sign of each element in the input array.
'''

import numpy as np

np.random.seed(1)
v1 = np.random.randint(-10, 11, 5)   # array([-5,  1,  2, -2, -1])
v2 = np.random.randint(-5, 5, 5) + 1 # array([ 1, -4, -4, -3,  3])

np.random.seed(2)
M1 = np.random.randint(-10, 11, (2, 3))
M2 = np.random.randint(-5, 5, (2, 3)) + 2

print(M1)
# array([[-2,  5,  3],
#        [-2,  1,  8]])

print(M2)
# array([[ 5,  4, -1],
#        [-2,  2,  1]])


#-------------------------------------------------------------------------------------------------#
#-------------------------------------- 1. np.positive() -----------------------------------------#
#-------------------------------------------------------------------------------------------------#
'''
np.positive() returns an array with the positive values of the input array.

=> Typically like: array * (+1) = that same array
'''

print(np.positive(v1))
# [-5  1  2 -2 -1]

print(np.positive(M1))
# [[-2  5  3]
#  [-2  1  8]]


#-------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. np.negative() -----------------------------------------#
#-------------------------------------------------------------------------------------------------#
'''
np.negative() returns an array with the negative values of the input array.

=> Typically like: array * (-1) = negative of that array
'''

print(np.negative(v1))
# [ 5 -1 -2  2  1]

print(np.negative(M1))
# [[ 2 -5 -3]
#  [ 2 -1 -8]]


#------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. np.add() --------------------------------------------#
#------------------------------------------------------------------------------------------------#
'''
np.add() adds arrays element-wise.

=> Equivalent to the + operator: array1 + array2
'''

print(np.add(v1, v2))
# [-4 -3 -2 -5  2]

print(np.add(M1, M2))
# [[ 3  9  2]
#  [-4  3  9]]

print(M1 + M2)
# [[ 3  9  2]
#  [-4  3  9]]


#------------------------------------------------------------------------------------------------#
#------------------------------------- 4. np.subtract() -----------------------------------------#
#------------------------------------------------------------------------------------------------#
'''
np.subtract() subtracts arrays element-wise.

=> Equivalent to the - operator: array1 - array2
'''

print(np.subtract(v1, v2))
# [-6  5  6  1 -4]

print(np.subtract(M1, M2))
# [[ -7   1   4]
#  [  0  -1   7]]

print(M1 - M2)
# [[ -7   1   4]
#  [  0  -1   7]]


#------------------------------------------------------------------------------------------------#
#------------------------------------- 5. np.multiply() -----------------------------------------#
#------------------------------------------------------------------------------------------------#
'''
np.multiply() multiplies arrays element-wise.

=> Equivalent to the * operator: array1 * array2
'''

print(np.multiply(v1, v2))
# [-5 -4 -8  6 -3]

print(np.multiply(M1, M2))
# [[ -10   20   -3]
#  [   4    2    8]]

print(M1 * M2)
# [[ -10   20   -3]
#  [   4    2    8]]


#------------------------------------------------------------------------------------------------#
#---------------------------- 6. np.divide() or np.true_divide() --------------------------------#
#------------------------------------------------------------------------------------------------#
'''
np.divide() or np.true_divide() divides arrays element-wise.

=> Equivalent to the / operator: array1 / array2
'''

print(np.divide(v1, v2))
# [-5.         -0.25       -0.5        0.66666667 -0.33333333]

print(np.divide(M1, M2))
# [[-0.4   1.25 -3.  ]
#  [ 1.    0.5   8.  ]]

print(np.true_divide(M1, M2))
# [[-0.4   1.25 -3.  ]
#  [ 1.    0.5   8.  ]]

print(M1 / M2)
# [[-0.4   1.25 -3.  ]
#  [ 1.    0.5   8.  ]]


#------------------------------------------------------------------------------------------------#
#------------------------------------ 7. np.reciprocal() ----------------------------------------#
#------------------------------------------------------------------------------------------------#
'''np.reciprocal() computes the reciprocal (1/x) of each element in the array.'''

print(np.reciprocal(v1, dtype=float)) # set dtype=float to avoid integer division
# [-0.2  1.   0.5 -0.5 -1. ]

print(np.reciprocal(M1, dtype=float))
# [[-0.5         0.2         0.33333333]
#  [-0.5         1.          0.125     ]]

# Check:
print(v1 * np.reciprocal(v1, dtype=float))
# [1. 1. 1. 1. 1.]


#------------------------------------------------------------------------------------------------#
#------------------------------------ 8. np.floor_divide() --------------------------------------#
#------------------------------------------------------------------------------------------------#
'''
np.floor_divide() performs floor division on arrays element-wise.

=> Equivalent to the // operator: array1 // array2
'''

print(np.floor_divide(v1, v2))
# [-5 -1 -1  0 -1]
'''The result is the largest integer less than or equal to the division result.'''

print(np.floor_divide(M1, M2))
# [[-1  1 -3]
#  [ 1  0  8]]

print(M1 // M2)
# [[-1  1 -3]
#  [ 1  0  8]]


#------------------------------------------------------------------------------------------------#
#----------------------------- 9. np.remainder() or np.mod() ------------------------------------#
#------------------------------------------------------------------------------------------------#
'''
np.remainder() or np.mod() computes the element-wise remainder of division (modulus).

=> Equivalent to the % operator: array1 % array2

NOTE: the result has the same sign as the divisor (second array v2).

Use np.remainder() and np.mod() when you need Python-consistent modulo behavior 
where results stay within [0, divisor) for positive divisors (v2 sign).
'''

print(np.remainder(v1, v2))
# [ 0 -3 -2 -2  2]

print(np.remainder(M1, M2))
# [[3 1 0]
#  [0 1 0]]

print(np.mod(M1, M2))
# [[3 1 0]
#  [0 1 0]]

print(M1 % M2)
# [[3 1 0]
#  [0 1 0]]

#----- Check -----#
remainder = np.remainder(v1, v2)
quotient = np.floor_divide(v1, v2)

print(v1 == quotient * v2 + remainder)
# [ True  True  True  True  True]


#------------------------------------------------------------------------------------------------#
#------------------------------------- 10. np.divmod() ------------------------------------------#
#------------------------------------------------------------------------------------------------#
'''np.divmod() returns the quotient and remainder of division of the input arrays.'''

print(np.divmod(v1, v2))
# (array([-5, -1, -1,  0, -1]), array([ 0, -3, -2, -2,  2]))
'''The first array is the quotient, and the second array is the remainder.'''

print(np.divmod(M1, M2))
# (array([[-1,  1, -3],
#        [ 1,  0,  8]]), array([[3, 1, 0],
#        [0, 1, 0]]))


#------------------------------------------------------------------------------------------------#
#-------------------------------------- 12. np.fmod() -------------------------------------------#
#------------------------------------------------------------------------------------------------#
'''
np.fmod() computes the element-wise remainder of division, similar to np.remainder().

NOTE: the result has the same sign as the dividend (first array v1).

Use np.fmod() when you need the mathematical remainder that preserves the dividend's sign (v1 sign)
(common in signal processing)
'''

print(np.fmod(v1, v2))
# [ 0  1  2 -2 -1]

print(np.fmod(M1, M2))
# [[-2  1  0]
#  [ 0  1  0]]

#----- Check -----#
fmod = np.fmod(v1, v2)
quotient = np.trunc(v1 / v2).astype(int)  # Truncate toward zero
                                          # array([-5,  0,  0,  0,  0])

print(v1 == quotient * v2 + fmod)
# [ True  True  True  True  True]


#------------------------------------------------------------------------------------------------#
#-------------------------------------- 12. np.modf() -------------------------------------------#
#------------------------------------------------------------------------------------------------#
'''np.modf() returns the fractional and integral parts of an array.'''

print(v1 * 1.5) 
# [-7.5  1.5  3.  -3.  -1.5]

print(np.modf(v1 * 1.5)) 
# (array([-0.5,  0.5,  0. , -0. , -0.5]), array([-7.,  1.,  3., -3., -1.]))

print(np.modf(M1 / 2))
# (array([[-0. ,  0.5,  0.5],
#        [-0. ,  0.5,  0. ]]), array([[-1.,  2.,  1.],
#        [-1.,  0.,  4.]]))


#------------------------------------------------------------------------------------------------#
#--------------------------------- 13. np.power() or np.pow() -----------------------------------#
#------------------------------------------------------------------------------------------------#
'''
np.power() or np.pow() raises elements of one array to the powers of another array element-wise.

=> Equivalent to the ** operator: array1 ** array2
'''

v1_float = v1.astype(float)  # Convert to float to handle negative bases with fractional exponents
M1_float = M1.astype(float)

print(np.power(v1_float, v2))
# [-5.      1.      0.0625 -0.125  -1.    ]

print(np.power(M1_float, M2))
# [[-3.20000000e+01  6.25000000e+02  3.33333333e-01]
#  [ 2.50000000e-01  1.00000000e+00  8.00000000e+00]]

print(np.pow(v1_float, v2))
# [-5.      1.      0.0625 -0.125  -1.    ]

print(M1_float ** M2)
# [[-3.20000000e+01  6.25000000e+02  3.33333333e-01]
#  [ 2.50000000e-01  1.00000000e+00  8.00000000e+00]]

print(np.pow(v1, v2))
'''ValueError: Integers to negative integer powers are not allowed.'''


#------------------------------------------------------------------------------------------------#
#---------------------------------- 14. np.float_power() ----------------------------------------#
#------------------------------------------------------------------------------------------------#
'''
np.float_power() raises elements of one array to the powers of another array element-wise, 
using float precision.

=> Similar to np.power(), but always converts inputs to float for computation.
'''

print(np.float_power(v1, v2))
# [-5.      1.      0.0625 -0.125  -1.    ]

print(np.float_power(M1, M2))
# [[-3.20000000e+01  6.25000000e+02  3.33333333e-01]
#  [ 2.50000000e-01  1.00000000e+00  8.00000000e+00]]


#------------------------------------------------------------------------------------------------#
#---------------------------------- 15. np.absolute() or np.abs() -------------------------------#
#------------------------------------------------------------------------------------------------#
'''
np.absolute() or np.abs() computes the absolute values of each element in the array.

Can handle both real and complex numbers.
'''

print(np.absolute(v1))
# [5 1 2 2 1]

print(np.absolute(M1))
# [[2 5 3]
#  [2 1 8]]

print(np.abs(v1))
# [5 1 2 2 1]

complex_array = np.array([-3+4j, 1-1j, -2-2j])
print(np.abs(complex_array))
# [5.         1.41421356 2.82842712]
'''Calculates the magnitude of complex numbers.'''

print(np.absolute(-3+4j))
# 5.0


#------------------------------------------------------------------------------------------------#
#------------------------------------- 16. np.fabs() --------------------------------------------#
#------------------------------------------------------------------------------------------------#
'''
np.fabs() computes the absolute values of each element in the array.

NOTE: always returns a float array and does not handle complex numbers.
'''

print(np.fabs(v1))
# [5. 1. 2. 2. 1.]

print(np.fabs(M1))
# [[2. 5. 3.]
#  [2. 1. 8.]]

complex_array = np.array([-3+4j, 1-1j, -2-2j])
print(np.fabs(complex_array))
'''
TypeError: ufunc 'fabs' not supported for the input types, 
and the inputs could not be safely coerced to any supported types according to the casting rule ''safe''
'''


#------------------------------------------------------------------------------------------------#
#-------------------------------------- 17. np.square() -----------------------------------------#
#------------------------------------------------------------------------------------------------#
'''np.square() computes the square of each element in the array.'''

print(np.square(v1))
# [25  1  4  4  1]

print(np.square(M1))
# [[ 4 25  9]
#  [ 4  1 64]]


#------------------------------------------------------------------------------------------------#
#-------------------------------------- 18. np.sqrt() -------------------------------------------#
#------------------------------------------------------------------------------------------------#
'''np.sqrt() computes the square root of each element in the array.'''

v1_positive = np.abs(v1)  # Take absolute to avoid RuntimeWarning for negative values
M1_positive = np.abs(M1)

print(np.sqrt(v1_positive))
# [2.23606798 1.         1.41421356 1.41421356 1.        ]

print(np.sqrt(M1_positive))
# [[1.41421356 2.23606798 1.73205081]
#  [1.41421356 1.         2.82842712]]


#------------------------------------------------------------------------------------------------#
#-------------------------------------- 19. np.cbrt() -------------------------------------------#
#------------------------------------------------------------------------------------------------#
'''np.cbrt() computes the cube root of each element in the array.'''

print(np.cbrt(v1))
# [-1.70997595  1.          1.25992105 -1.25992105 -1.        ]

print(np.cbrt(M1))
# [[-1.25992105  1.70997595  1.44224957]
#  [-1.25992105  1.          2.        ]]


#------------------------------------------------------------------------------------------------#
#-------------------------------------- 20. np.sign() -------------------------------------------#
#------------------------------------------------------------------------------------------------#
'''np.sign() returns an array indicating the sign of each element in the input array.'''

print(np.sign(v1))
# [-1  1  1 -1 -1]

print(np.sign(M1))
# [[-1  1  1]
#  [-1  1  1]]