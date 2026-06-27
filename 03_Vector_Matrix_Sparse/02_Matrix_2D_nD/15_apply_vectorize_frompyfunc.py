'''
1. np.apply_along_axis(func, axis, arr): Applies a function to 1D slices along the specified axis of a 2D matrix

2. np.apply_over_axes(func, arr, axes): Applies a function over multiple axes

3. np.vectorize(func): Vectorizes a function to apply it element-wise on arrays

4. np.frompyfunc(func, nin, nout): Creates a ufunc from a Python function

5. Examples for 3D and 4D matrices
'''

import numpy as np
import math


#-------------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. np.apply_along_axis() -------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
'''
This function applies a given function to 1D slices along the specified axis of an array.

For 2D matrices: axis=0 applies function down columns, axis=1 applies function across rows.

NOTE: the function must accept arrays and return arrays.
'''

np.random.seed(0)
matrix_nums = np.random.randint(10, 100, size=(4, 5))

print(matrix_nums)
# [[54 57 74 77 77]
#  [19 93 31 46 97]
#  [80 98 98 22 68]
#  [75 49 97 56 98]]

print(np.apply_along_axis(np.mean, axis=0, arr=matrix_nums))
# [57.   74.25 75.   50.25 85.  ]  # Mean along axis=0

print(np.apply_along_axis(np.mean, axis=1, arr=matrix_nums))
# [67.8 57.2 73.2 75. ]  # Mean along axis=1

print(np.apply_along_axis(lambda x: x.max() - x.min(), axis=0, arr=matrix_nums))
# [61 49 67 55 30]  # Range along axis=0

print(np.apply_along_axis(lambda x: x.max() - x.min(), axis=1, arr=matrix_nums))
# [23 78 76 49]  # Range along axis=1

def normalize(x):
    return (x - x.mean()) / x.std()

print(np.apply_along_axis(normalize, axis=0, arr=matrix_nums))
# [[-0.12494578 -0.80194617 -0.03682298  1.3524814  -0.61998741]
#  [-1.58264657  0.87168062 -1.62021133 -0.21488022  0.92998111]
#  [ 0.95791766  1.10412878  0.84692865 -1.42832148 -1.31747324]
#  [ 0.74967469 -1.17386323  0.81010566  0.2907203   1.00747954]]

print(np.apply_along_axis(math.log2, axis=0, arr=matrix_nums))
'''TypeError: only length-1 arrays can be converted to Python scalars'''
# It returns an error because math.log2 expects a single scalar value, not an array.


#-------------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 2. np.apply_over_axes() ---------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
'''
This function applies a function repeatedly over multiple axes.

The function must keep the number of dimensions and accept an axis argument.

Useful for cumulative operations like sum, mean, etc. over multiple axes.
'''

np.random.seed(5)
matrix_data = np.random.randint(1, 10, size=(4, 5))

print(matrix_data)
# [[4 7 7 1 9]
#  [5 8 1 1 8]
#  [2 6 8 1 2]
#  [5 7 3 2 3]]

# Apply sum over axis 0 (columns)
result_axis0 = np.apply_over_axes(np.sum, matrix_data, axes=[0])
print(result_axis0)
# [[16 28 19  5 22]]  # Sum of each column, shape maintained as (1, 5)

# Apply sum over axis 1 (rows)
result_axis1 = np.apply_over_axes(np.sum, matrix_data, axes=[1])
print(result_axis1)
# [[28]
#  [23]
#  [19]
#  [20]]  # Sum of each row, shape maintained as (4, 1)

# Apply sum over both axes
result_both = np.apply_over_axes(np.sum, matrix_data, axes=[0, 1])
print(result_both)
# [[90]]  # Total sum, shape maintained as (1, 1)

# Apply mean over axis 0
result_mean = np.apply_over_axes(np.mean, matrix_data, axes=[0])
print(result_mean)
# [[4.   7.   4.75 1.25 5.5 ]]


#-------------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 3. np.vectorize() -----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
'''
This function vectorizes a given function to apply it element-wise on arrays.

It's useful for functions that are not inherently vectorized (only accept scalars).
'''

np.random.seed(10)
matrix_values = np.random.randint(1, 50, size=(3, 4))

print(matrix_values)
# [[10 37 16  1]
#  [29 26 30 49]
#  [30  9 10  1]]

#-------#

def categorize(x):
    if x < 15:
        return "Low"
    elif x < 35:
        return "Medium"
    else:
        return "High"

categorize_vectorized = np.vectorize(categorize)

print(categorize_vectorized(matrix_values))
# [['Low' 'High' 'Medium' 'Low']
#  ['Medium' 'Medium' 'Medium' 'High']
#  ['Medium' 'Low' 'Low' 'Low']]

#-------#

def scale_by_position(x):
    return x * 1.5 if x % 2 == 0 else x * 2.0

scale_vectorized = np.vectorize(scale_by_position)

print(scale_vectorized(matrix_values))
# [[15. 74. 24.  2.]
#  [58. 39. 45. 98.]
#  [45. 18. 15.  2.]]


#-------------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 4. np.frompyfunc() ------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
'''
Creates a universal function (ufunc) from any Python function, enabling broadcasting.

NOTE: Unlike vectorize(), you must specify the number of inputs (nin) and outputs (nout).
'''

#################################
## Single input, Single output ##
#################################

hex(42)
# '0x2a'
# This function converts an integer to its hexadecimal string representation.

hex_ufunc = np.frompyfunc(hex, nin=1, nout=1)

matrix_hex = np.array([[10, 20, 30], [40, 50, 60]])

print(hex_ufunc(matrix_hex))
# [['0xa' '0x14' '0x1e']
#  ['0x28' '0x32' '0x3c']]

'''hex_ufunc() takes ONLY ONE array-like input and returns ONE array-like output.'''

####################################
## Multiple inputs, Single output ##
####################################

def weighted_sum(a, b, c, w1, w2, w3):
    return a*w1 + b*w2 + c*w3

weighted_sum_func = np.frompyfunc(weighted_sum, 6, 1)

matrix_a = np.array([[1, 2], [3, 4]])
matrix_b = np.array([[5, 6], [7, 8]])
matrix_c = np.array([[9, 10], [11, 12]])
weights = (0.5, 0.3, 0.2)

result = weighted_sum_func(matrix_a, matrix_b, matrix_c, *weights)
print(result.astype(float))
# [[3.8 4.8]
#  [5.8 6.8]]

'''
weighted_sum_func() takes SIX array-like inputs and returns ONE array-like output.

3.8 = 1*0.5 + 5*0.3 + 9*0.2
4.8 = 2*0.5 + 6*0.3 + 10*0.2
5.8 = 3*0.5 + 7*0.3 + 11*0.2
6.8 = 4*0.5 + 8*0.3 + 12*0.2
'''

####################################
## Single input, Multiple outputs ##
####################################

def matrix_stats(x):
    return x, x**2, np.sqrt(x)

stats_func = np.frompyfunc(matrix_stats, 1, 3)

matrix_input = np.array([[4, 9, 16], [25, 36, 49]])

vals, squares, sqrts = stats_func(matrix_input)

print("Values:\n", vals.astype(int))
# [[4  9 16]
#  [25 36 49]]

print("Squares:\n", squares.astype(int))
# [[16  81  256]
#  [625 1296 2401]]

print("Square roots:\n", sqrts.astype(float))
# [[2. 3. 4.]
#  [5. 6. 7.]]

'''stats_func() takes ONE array-like input and returns THREE array-like outputs.'''

#######################################
## Multiple inputs, Multiple outputs ##
#######################################

def matrix_operations(x, y):
    return x + y, x - y, x * y, x / y

op_func = np.frompyfunc(matrix_operations, 2, 4)

a = np.array([[10, 20], [30, 40]])

b = np.array([[2, 4], [5, 8]])

sums, diffs, prods, divs = op_func(a, b)

print("Sums:\n", sums.astype(int))
# [[12 24]
#  [35 48]]

print("Differences:\n", diffs.astype(int))
# [[8 16]
#  [25 32]]

print("Products:\n", prods.astype(int))
# [[20  80]
#  [150 320]]

print("Divisions:\n", divs.astype(float))
# [[5.  5. ]
#  [6.  5. ]]

'''op_func() takes TWO array-like inputs and returns FOUR array-like outputs.'''


#-------------------------------------------------------------------------------------------------------------------#
#---------------------------------- 5. Examples for 3D and 4D Matrices ---------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
'''
For higher-dimensional arrays, the same functions work with appropriate axis specifications.

axis=0: first dimension, axis=1: second dimension, axis=2: third dimension, etc.
'''

##############
## 3D Array ##
##############

np.random.seed(20)
array_3d = np.random.randint(1, 100, size=(3, 4, 5))

# Apply mean along axis 0 (across the first dimension)
print(np.apply_along_axis(np.mean, axis=0, arr=array_3d))
# [[39.33333333 39.66666667 60.33333333 24.66666667 49.66666667]
#  [34.33333333 33.         60.66666667 39.33333333 69.        ]
#  [61.         78.33333333 49.66666667 72.         52.        ]
#  [62.         65.33333333 17.66666667 29.66666667 62.33333333]]

# Apply mean along axis 1 (across the second dimension)
print(np.apply_along_axis(np.mean, axis=1, arr=array_3d))
# [[40.75 54.5  57.5  50.25 67.75]
#  [63.75 63.25 30.5  30.5  55.75]
#  [43.   44.5  53.25 43.5  51.25]]

# Apply mean along axis 2 (across the third dimension)
print(np.apply_along_axis(np.mean, axis=2, arr=array_3d))
# [[64.6 40.4 70.  41.6]
#  [31.  48.  71.6 44.4]
#  [32.6 53.4 46.2 56.2]]

# Apply sum over multiple axes using apply_over_axes
result_3d = np.apply_over_axes(np.sum, array_3d, axes=[0, 1])
print(result_3d)
# [[[590 649 565 497 699]]]
# (1, 1, 5) - sum over first two dimensions, keeps dimensionality

result_3d_all = np.apply_over_axes(np.sum, array_3d, axes=[0, 1, 2])
print(result_3d_all)
# [[[3000]]]
# (1, 1, 1) - sum over all dimensions, keeps dimensionality

#----------
## Vectorize a function for 3D arrays
#----------

def threshold_3d(x):
    return 1 if x > 50 else 0

threshold_func_3d = np.vectorize(threshold_3d)

binary_3d = threshold_func_3d(array_3d)

print(binary_3d)
# [[[1 0 1 0 1]
#   [0 0 1 0 1]
#   [0 1 0 1 1]
#   [0 1 0 1 0]]

#  [[0 1 0 0 0]
#   [1 1 0 0 1]
#   [1 1 1 1 1]
#   [1 0 0 0 1]]

#  [[0 0 1 0 0]
#   [0 0 1 1 1]
#   [1 1 0 0 0]
#   [1 1 0 0 1]]]

##############
## 4D Array ##
##############

np.random.seed(30)
array_4d = np.random.randint(1, 50, size=(2, 3, 4, 5))

# Apply standard deviation along axis 3
result_4d_axis3 = np.apply_along_axis(np.std, axis=3, arr=array_4d)
print(result_4d_axis3)
# [[[12.13919272 16.06735821 18.18130908  9.06862724]
#   [19.13530768  9.15641851  8.54634425 12.38709005]
#   [15.21052267  7.44580419 14.82430437  6.24179461]]

#  [[11.01635148 11.72006826 11.36661779 12.11610498]
#   [15.47126368 13.89388355 10.76289924 10.93617849]
#   [12.90891165 10.06777036  7.25534286  5.38887743]]]

# Apply over axes 0 and 1
result_4d_multi = np.apply_over_axes(np.mean, array_4d, axes=[0, 1])
print(result_4d_multi)
# [[[[24.         26.33333333 38.83333333 30.83333333 26.        ]
#    [30.83333333 26.5        24.         32.83333333 29.66666667]
#    [34.33333333 18.66666667 19.33333333 24.16666667 28.16666667]
#    [25.33333333 27.5        26.         23.5        31.16666667]]]]

#----------
## Vectorize for 4D arrays
#----------

def scale_4d(x):
    return x * 2 if x < 25 else x * 0.5

scale_func_4d = np.vectorize(scale_4d)

scaled_4d = scale_func_4d(array_4d)

print(scaled_4d)
# .... (output too large to display here) ....

print(scaled_4d.shape)
# (2, 3, 4, 5)

#----------
## Using frompyfunc with 4D arrays
#----------

def clip_range(x, min_val, max_val):
    return max(min_val, min(x, max_val))

clip_func = np.frompyfunc(clip_range, 3, 1)

clipped_4d = clip_func(array_4d, 10, 40)

print(clipped_4d.astype(int)[:, :, 0, 0])
# [[38 10 12]
#  [40 18 24]]
'''all values clipped to be within the range [10, 40]'''
