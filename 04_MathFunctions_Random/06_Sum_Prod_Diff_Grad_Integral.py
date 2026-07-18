'''
1. np.prod(): returns the product of array elements over a given axis.

2. np.sum(): returns the sum of array elements over a given axis.

3. np.nanprod(): returns the product of array elements over a given axis treating NaNs as ones.

4. np.nansum(): returns the sum of array elements over a given axis treating NaNs as zero.

5. np.cumsum(): returns the cumulative sum of the elements along a given axis.

6. np.cumprod(): returns the cumulative product of elements along a given axis.

7. np.nancumsum(): returns the cumulative sum of array elements over a given axis treating NaNs as zero.

8. np.nancumprod(): returns the cumulative product of array elements over a given axis treating NaNs as one.

9. np.diff(): calculates the n-th discrete difference along the given axis.

10. np.ediff1d(): calculates the differences between consecutive elements of an array.

11. np.gradient(): returns the gradient of an N-dimensional array.

12. np.cross(): returns the cross product of two (arrays of) vectors.

13. np.trapezoid(): integrates along the given axis using the composite trapezoidal rule.
'''

import numpy as np

np.random.seed(5)
v1 = np.random.randint(1, 10, 5)
# array([4, 7, 7, 1, 9])

np.random.seed(5)
v2 = np.random.randint(11, 20, 5)
# array([14, 17, 17, 11, 19])

np.random.seed(6)
M1 = np.random.randint(1, 10, (3, 4))
M2 = np.random.randint(10, 20, (3, 4))

print(M1)
# [[4 5 1 2]
#  [2 5 2 9]
#  [3 5 3 6]]

print(M2)
# [[19 16 12 15]
#  [15 11 14 15]
#  [10 12 12 13]]


#----------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. np.prod() ---------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.prod() returns the product of array elements over a given axis.
If axis is None, it returns the product of all elements in the array.
'''

print(np.prod(v1))
# 1764 (= 4 * 7 * 7 * 1 * 9)

print(np.prod(M1))
# 1944000

print(np.prod(M1, axis=0))  # Product vertical (down each column)
# [ 24 125   6 108]

print(np.prod(M1, axis=1))  # Product horizontal (across each row)
# [ 40 180 270]


#----------------------------------------------------------------------------------------------------#
#------------------------------------------ 2. np.sum() ---------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.sum() returns the sum of array elements over a given axis.
If axis is None, it returns the sum of all elements in the array.
'''

print(np.sum(v1))
# 28

print(np.sum(M1))
# 47

print(np.sum(M1, axis=0))  # Sum along columns (down each column)
# [ 9 15  6 17]

print(np.sum(M1, axis=1))  # Sum along rows (across each row)
# [12 18 17]


#----------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. np.nanprod() --------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.nanprod() returns the product of array elements over a given axis treating NaNs as ones.
This is useful when you have NaN values that you want to ignore in the product calculation.
'''

v_with_nan = np.array([2.0, np.nan, 3.0, 4.0])

print(np.prod(v_with_nan)) # nan
print(np.nanprod(v_with_nan)) # 24.0

##############

M_with_nan = np.array([[1.0, 2.0, np.nan],
                       [4.0, np.nan, 6.0]])

print(np.nanprod(M_with_nan))
# 48.0

print(np.nanprod(M_with_nan, axis=0))
# [4. 2. 6.]

print(np.nanprod(M_with_nan, axis=1))
# [ 2. 24.]


#----------------------------------------------------------------------------------------------------#
#--------------------------------------- 4. np.nansum() ---------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.nansum() returns the sum of array elements over a given axis treating NaNs as zero.
This is useful when you have NaN values that you want to ignore in the sum calculation.
'''

v_with_nan = np.array([2.0, np.nan, 3.0, 4.0])

print(np.sum(v_with_nan))
# nan

print(np.nansum(v_with_nan))
# 9.0

###############

M_with_nan = np.array([[1.0, 2.0, np.nan],
                       [4.0, np.nan, 6.0]])

print(np.nansum(M_with_nan))
# 13.0

print(np.nansum(M_with_nan, axis=0))
# [5. 2. 6.]

print(np.nansum(M_with_nan, axis=1))
# [ 3. 10.]


#----------------------------------------------------------------------------------------------------#
#--------------------------------------- 5. np.cumsum() ---------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.cumsum() returns the cumulative sum of the elements along a given axis.
The i-th element of the output is the sum of elements 0 through i of the input.
'''

print(np.cumsum(v1))
# [ 4 11 18 19 28]
'''
4 = 4
11 = 4 + 7
18 = 4 + 7 + 7
19 = 4 + 7 + 7 + 1
28 = 4 + 7 + 7 + 1 + 9
'''

print(np.cumsum(M1))  # Flattened cumulative sum
# [ 4  9 10 12 14 19 21 30 33 38 41 47]

print(np.cumsum(M1, axis=0))  # Cumulative sum down columns (vertical)
# [[ 4  5  1  2]
#  [ 6 10  3 11]
#  [ 9 15  6 17]]

print(np.cumsum(M1, axis=1))  # Cumulative sum across rows (horizontal)
# [[ 4  9 10 12]
#  [ 2  7  9 18]
#  [ 3  8 11 17]]


#----------------------------------------------------------------------------------------------------#
#-------------------------------------- 6. np.cumprod() ---------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.cumprod() returns the cumulative product of elements along a given axis.
The i-th element of the output is the product of elements 0 through i of the input.
'''

print(np.cumprod(v1))
# [   4   28  196  196 1764]
'''
4 = 4
28 = 4 * 7
196 = 4 * 7 * 7
196 = 4 * 7 * 7 * 1
1764 = 4 * 7 * 7 * 1 * 9
'''

print(np.cumprod(M1))  # Flattened cumulative product
# [      4      20      20      40      80     400     800    7200   21600   108000  324000 1944000]

print(np.cumprod(M1, axis=0))  # Cumulative product down columns
# [[  4   5   1   2]
#  [  8  25   2  18]
#  [ 24 125   6 108]]

print(np.cumprod(M1, axis=1))  # Cumulative product across rows
# [[  4  20  20  40]
#  [  2  10  20 180]
#  [  3  15  45 270]]


#----------------------------------------------------------------------------------------------------#
#------------------------------------ 7. np.nancumsum() ---------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''np.nancumsum() returns the cumulative sum of array elements over a given axis treating NaNs as zero.'''

v_with_nan = np.array([2.0, np.nan, 3.0, 4.0])

print(np.cumsum(v_with_nan))
# [ 2. nan nan nan]

print(np.nancumsum(v_with_nan))
# [2. 2. 5. 9.]

################################

M_with_nan = np.array([[1.0, 2.0, np.nan],
                       [4.0, np.nan, 6.0]])

print(np.nancumsum(M_with_nan, axis=0))
# [[1. 2. 0.]
#  [5. 2. 6.]]

print(np.nancumsum(M_with_nan, axis=1))
# [[1. 3. 3.]
#  [4. 4. 10.]]


#----------------------------------------------------------------------------------------------------#
#------------------------------------ 8. np.nancumprod() --------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''np.nancumprod() returns the cumulative product of array elements over a given axis treating NaNs as one.'''

v_with_nan = np.array([2.0, np.nan, 3.0, 4.0])

print(np.cumprod(v_with_nan))
# [ 2. nan nan nan]

print(np.nancumprod(v_with_nan))
# [ 2.  2.  6. 24.]

################################

M_with_nan = np.array([[1.0, 2.0, np.nan],
                       [4.0, np.nan, 6.0]])

print(np.nancumprod(M_with_nan, axis=0))
# [[1. 2. 1.]
#  [4. 2. 6.]]

print(np.nancumprod(M_with_nan, axis=1))
# [[1. 2. 2.]
#  [4. 4. 24.]]


#----------------------------------------------------------------------------------------------------#
#---------------------------------------- 9. np.diff() ----------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.diff() calculates the n-th discrete difference along the given axis.
The first difference is out[i] = a[i+1] - a[i] along the given axis.
Higher differences are calculated by using diff recursively. (default n=1)
'''

print(np.diff(v1))
# [ 3  0 -6  8]
'''
3 = 7 - 4
0 = 7 - 7
-6 = 1 - 7
8 = 9 - 1
'''

print(np.diff(v1, n=2))  # Second order difference
# [-3 -6 14]
'''
from first differences [3, 0, -6, 8]:
-3 = 0 - 3
-6 = -6 - 0
14 = 8 - (-6)
'''

print(np.diff(M1, axis=0))  # Difference between consecutive rows
# [[-2  0  1  7]
#  [ 1  0  1 -3]]

print(np.diff(M1, axis=1))  # Difference between consecutive columns
# [[ 1 -4  1]
#  [ 3 -3  7]
#  [ 2 -2  3]]


#----------------------------------------------------------------------------------------------------#
#-------------------------------------- 10. np.ediff1d() --------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.ediff1d() calculates the differences between consecutive elements of an array.
This is similar to np.diff() but always returns a flattened 1D array.
It also supports prepending and appending values.
'''

print(np.ediff1d(v1))
# [ 3  0 -6  8]

print(np.ediff1d(M1))  # Flattened difference
# [ 1 -4  1  0  3 -3  7 -6  2 -2  3]

# With prepend and append
print(np.ediff1d(v1, to_begin=0, to_end=[100, 200]))
# [  0   3   0  -6   8 100 200]
'''
0 = prepended value
3 = 7 - 4
0 = 7 - 7
-6 = 1 - 7
8 = 9 - 1
100, 200 = appended values
'''


#----------------------------------------------------------------------------------------------------#
#-------------------------------------- 11. np.gradient() -------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.gradient() returns the gradient of an N-dimensional array.
The gradient is computed using second order accurate central differences in the interior points
and either first or second order accurate one-sides (forward or backwards) differences at the boundaries.
'''

# 1D gradient
f = np.array([1, 2, 4, 7, 11, 16])
print(np.gradient(f))
# [1.  1.5 2.5 3.5 4.5 5. ]

'''
1.0 = (2 - 1)
1.5 = (4 - 1) / 2
2.5 = (7 - 2) / 2
3.5 = (11 - 4) / 2
4.5 = (16 - 7) / 2
5.0 = (16 - 11)

first element: (f[1] - f[0]) / h
last element: (f[-1] - f[-2]) / h
middle elements: (f[i+1] - f[i-1]) / (2*h)

default spacing h=1
'''

# 2D gradient
print(np.gradient(M1))
# (array([[-2. ,  0. ,  1. ,  7. ],            # Gradient along axis 0 (vertical)
#        [-0.5,  0. ,  1. ,  2. ],
#        [ 1. ,  0. ,  1. , -3. ]]),
# array([[ 1. , -1.5, -1.5,  1. ],             # Gradient along axis 1 (horizontal)
#        [ 3. ,  0. ,  2. ,  7. ],
#        [ 2. ,  0. ,  0.5,  3. ]]))

##########################################

# With specified spacing
x = np.array([0, 1, 2, 3, 4, 5])
y = x**2  # y = [0, 1, 4, 9, 16, 25]

print(np.gradient(y, x))  # Should approximate dy/dx = 2x
# [1. 2. 4. 6. 8. 9.]

# f'[0] = (1 - 0) / (1 - 0) = dy/dx = 1
# f'[1] = (4 - 0) / (2 - 0)         = 2
# f'[2] = (9 - 1) / (3 - 1)         = 4
# f'[-1] = (25 - 16) / (5 - 4)      = 9
'''
first element: (y[1] - y[0]) / (x[1] - x[0])
last element: (y[-1] - y[-2]) / (x[-1] - x[-2])
middle elements: (y[i+1] - y[i-1]) / (x[i+1] - x[i-1])
'''


#----------------------------------------------------------------------------------------------------#
#--------------------------------------- 12. np.cross() ---------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.cross() returns the cross product of two (arrays of) vectors.
The cross product is only defined for 3D vectors (or 2D vectors treated as 3D with z=0).

##############################

DEFINITION:
-----------
The cross product (also called vector product) of two 3D vectors produces
a NEW vector that is PERPENDICULAR to both input vectors.

Given vectors a and b in 3D space (ℝ³):
    a = [a₁, a₂, a₃]
    b = [b₁, b₂, b₃]

The cross product a x b is calculated as:

    a x b = [a₂b₃ - a₃b₂,  a₃b₁ - a₁b₃,  a₁b₂ - a₂b₁]
            \_____i_____/  \_____j_____/  \_____k_____/

Or using determinant notation:

         | i    j    k  |
a x b =  | a₁   a₂   a₃ |
         | b₁   b₂   b₃ |

where i, j, k are unit vectors in x, y, z directions.


FORMULA BREAKDOWN:
------------------
Component by component:

    x-component (i): a₂b₃ - a₃b₂
    y-component (j): a₃b₁ - a₁b₃
    z-component (k): a₁b₂ - a₂b₁
'''

# 3D vectors
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(np.cross(a, b))
# [-3  6 -3]
'''
-3 = (2*6 - 3*5)
6  = (3*4 - 1*6)
-3 = (1*5 - 2*4)
'''

# Verify: a × b is perpendicular to both a and b
cross_product = np.cross(a, b)
print(np.dot(cross_product, a))  # Should be 0
# 0
print(np.dot(cross_product, b))  # Should be 0
# 0

# Multiple vectors
vectors1 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
vectors2 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])

print(np.cross(vectors1, vectors2))
# [[ 0  0  1]
#  [ 1  0  0]
#  [ 0  1  0]]

# 2D cross product (returns scalar z-component)
# For 2D vectors, manually compute the z-component if needed
# (2D cross product returns scalar: a[0]*b[1] - a[1]*b[0])
a2d = np.array([1, 2])
b2d = np.array([3, 4])
cross_2d_scalar = a2d[0] * b2d[1] - a2d[1] * b2d[0]
print(cross_2d_scalar)
# -2


#----------------------------------------------------------------------------------------------------#
#--------------------------------------- 13. np.trapezoid() -----------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.trapezoid() integrates along the given axis using the composite trapezoidal rule.
This approximates the integral by summing the areas of trapezoids under the curve.

https://matgomes.com/trapezium-rule-with-python/

Area = (y₁ + y₂)/2 * Δx
'''

# Simple integration
y = np.array([1, 2, 3, 4, 5])
print(np.trapezoid(y))  # Default spacing dx=1
# 12.0
'''
12 = (1+2)/2 * 1 + (2+3)/2 * 1 + (3+4)/2 * 1 + (4+5)/2 * 1
'''

# With specified x values
x = np.array([3, 2, 5, 1, 7])
y = np.array([2, 4, 6, 8, 10])
print(np.trapezoid(y, x))
# 38.0
'''
38 = (2+4)/2 * (2-3) + (4+6)/2 * (5-2) + (6+8)/2 * (1-5) + (8+10)/2 * (7-1)
'''

# Integrate x^2 from 0 to 4 (analytical result: 64/3 ≈ 21.33)
x = np.linspace(0, 4, 100)
y = x**2
print(np.trapezoid(y, x))
# 21.334421657653987 (close to analytical result!)

# 2D integration
M = np.array([[1, 2, 3], [4, 5, 6]])
print(np.trapezoid(M, axis=0))  # Integrate along axis 0
# [2.5 3.5 4.5]

print(np.trapezoid(M, axis=1))  # Integrate along axis 1
# [ 4. 10.]

# Integration with different spacing
x = np.array([0, 0.5, 1])
y = np.array([1, 4, 9])  # y = (2x+1)^2 approximately
print(np.trapezoid(y, x))
# 4.5
