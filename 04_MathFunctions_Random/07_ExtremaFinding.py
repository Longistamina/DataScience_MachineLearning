'''
1. np.maximum(): computes the element-wise maximum of array elements.
2. np.amax() or np.max(): returns the maximum of an array or maximum along an axis.
3. np.fmax(): computes the element-wise maximum of array elements (propagates non-NaN values).
4. np.nanmax(): returns the maximum of an array or maximum along an axis, ignoring any NaNs.
5. np.minimum(): computes the element-wise minimum of array elements.
6. np.amin() or np.min(): returns the minimum of an array or minimum along an axis.
7. np.fmin(): computes the element-wise minimum of array elements (propagates non-NaN values).
8. np.nanmin(): returns the minimum of an array or minimum along an axis, ignoring any NaNs.
9. np.argmax(): returns the indices of the maximum values along an axis.
10. np.argmin(): returns the indices of the minimum values along an axis.
11. np.nanargmax(): returns the indices of the maximum values along an axis, ignoring NaNs.
12. np.nanargmin(): returns the indices of the minimum values along an axis, ignoring NaNs.
13. np.ptp(): returns the range (maximum - minimum) of values along an axis.
'''

import numpy as np

np.random.seed(5)
v1 = np.random.randint(-10, 11, 5)
# array([-7,  4,  5, -4,  6])

np.random.seed(6)
v2 = np.random.randint(-10, 11, 5)
# array([ 0, -1, -7, 10,  0])

np.random.seed(7)
M1 = np.random.randint(-10, 11, (2, 3))
# array([[ 5, -6, -7],
#        [ 9, -3,  4]])

np.random.seed(8)
M2 = np.random.randint(-10, 11, (2, 3))
# array([[-7, 10,  7],
#        [-1, -5, -2]])


#----------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. np.maximum() -------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.maximum() computes the element-wise maximum of array elements.
Compares two arrays element-by-element and returns the maximum value at each position.
'''

print(np.maximum(v1, v2))
# [ 0  4  5 10  6]

print(np.maximum(M1, M2))
# [[ 5 10  7]
#  [ 9 -3  4]]

#----- Check -----#

print(v1)
# [-7  4  5 -4  6]
print(v2)
# [ 0 -1 -7 10  0]

# Element-wise: max(-7, 0)=0, max(4, -1)=4, max(5, -7)=5, max(-4, 10)=10, max(6, 0)=6


#----------------------------------------------------------------------------------------------------#
#----------------------------------- 2. np.amax() or np.max() ---------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.amax() or np.max() returns the maximum of an array or maximum along an axis.
Without axis parameter: returns the global maximum.
With axis parameter: returns the maximum along the specified axis.
'''

print(np.amax(v1))
# 6

print(np.amax(M1))
# 9

print(np.max(M1))
# 9

#----- With axis parameter -----#
print(np.amax(M1, axis=0))  # Maximum veritcally (down each column)
# [ 9 -3  4]

print(np.amax(M1, axis=1))  # Maximum horizontally (across each row)
# [5 9]

print(np.amax(M1, axis=1, keepdims=True))  # Keep dimensions
# [[5]
#  [9]]


#----------------------------------------------------------------------------------------------------#
#----------------------------------------- 3. np.fmax() ---------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.fmax() computes the element-wise maximum of array elements.
Unlike np.maximum(), it propagates non-NaN values.
If one element is NaN, fmax returns the non-NaN value.
'''

v1_with_nan = np.array([4.0, np.nan, np.nan, -5.0, 3.0])
v2_with_nan = np.array([-7.0, 9.0, np.nan, 7.0, 3.0])

print(np.maximum(v1_with_nan, v2_with_nan))
# [ 4. nan nan  7.  3.]

print(np.fmax(v1_with_nan, v2_with_nan))
# [4. 9. nan 7. 3.]
# Notice: fmax ignores NaNs and returns the non-NaN value


#----------------------------------------------------------------------------------------------------#
#---------------------------------------- 4. np.nanmax() --------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.nanmax() returns the maximum of an array or maximum along an axis, ignoring any NaNs.
Useful when working with data containing NaN values.
'''

M_with_nan = np.array([[1.0, np.nan, 3.0],
                        [4.0, 5.0, np.nan]])

print(np.amax(M_with_nan))
# nan

print(np.nanmax(M_with_nan))
# 5.0

print(np.nanmax(M_with_nan, axis=0))
# [4. 5. 3.]

print(np.nanmax(M_with_nan, axis=1))
# [3. 5.]

print(np.nanmax(M_with_nan, axis=1, keepdims=True))
# [[3.]
#  [5.]]


#----------------------------------------------------------------------------------------------------#
#---------------------------------------- 5. np.minimum() -------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.minimum() computes the element-wise minimum of array elements.
Compares two arrays element-by-element and returns the minimum value at each position.
'''

print(np.minimum(v1, v2))
# [-7 -1 -7 -4  0]

print(np.minimum(M1, M2))
# [[-7 -6 -7]
#  [-1 -5 -2]]

#----- Check -----#

print(v1)
# [-7  4  5 -4  6]

print(v2)
# [ 0 -1 -7 10  0]

# Element-wise: min(-7, 0)=-7, min(4, -1)=-1, min(5, -7)=-7, min(-4, 10)=-4, min(6, 0)=0


#----------------------------------------------------------------------------------------------------#
#----------------------------------- 6. np.amin() or np.min() ---------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.amin() or np.min() returns the minimum of an array or minimum along an axis.
Without axis parameter: returns the global minimum.
With axis parameter: returns the minimum along the specified axis.
'''

print(np.amin(v1))
# -7

print(np.amin(M1))
# -7

print(np.min(M1))
# -7

#----- With axis parameter -----#
print(np.amin(M1, axis=0))  # Minimum vertically (down each column)
# [ 5 -6 -7]

print(np.amin(M1, axis=1))  # Minimum horizontally (across each row)
# [-7 -3]

print(np.amin(M1, axis=1, keepdims=True))  # Keep dimensions
# [[-7]
#  [-3]]


#----------------------------------------------------------------------------------------------------#
#----------------------------------------- 7. np.fmin() ---------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.fmin() computes the element-wise minimum of array elements.
Unlike np.minimum(), it propagates non-NaN values.
If one element is NaN, fmin returns the non-NaN value.
'''

print(np.minimum(v1_with_nan, v2_with_nan))
# [-7. nan nan -5.  3.]

print(np.fmin(v1_with_nan, v2_with_nan))
# [-7.  9.  nan -5.  3.]
# Notice: fmin ignores NaNs and returns the non-NaN value


#----------------------------------------------------------------------------------------------------#
#---------------------------------------- 8. np.nanmin() --------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.nanmin() returns the minimum of an array or minimum along an axis, ignoring any NaNs.
Useful when working with data containing NaN values.
'''

print(np.amin(M_with_nan))
# nan

print(np.nanmin(M_with_nan))
# 1.0

print(np.nanmin(M_with_nan, axis=0))
# [1. 5. 3.]

print(np.nanmin(M_with_nan, axis=1))
# [1. 4.]

print(np.nanmin(M_with_nan, axis=1, keepdims=True))
# [[1.]
#  [4.]]


#----------------------------------------------------------------------------------------------------#
#---------------------------------------- 9. np.argmax() --------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.argmax() returns the indices of the maximum values along an axis.
Without axis parameter: returns the index of the global maximum (flattened array).
With axis parameter: returns indices of maximum values along the specified axis.
'''

print(np.argmax(v1))
# 4  (index of value 6, v1[4] = 6)

print(np.argmax(M1))
# 3  (flattened index: M1.flat[3] = 9)

print(M1.flatten())
# [ 5 -6 -7  9 -3  4]

#----- With axis parameter -----#
print(np.argmax(M1, axis=0))  # Index of maximum in each column
# [1 1 1]

print(np.argmax(M1, axis=1))  # Index of maximum in each row
# [0 0]

#----- Check -----#

print(M1)
# [[ 5 -6 -7]
#  [ 9 -3  4]]
# Row 0: max is 5 at index 0
# Row 1: max is 9 at index 0


#----------------------------------------------------------------------------------------------------#
#---------------------------------------- 10. np.argmin() -------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.argmin() returns the indices of the minimum values along an axis.
Without axis parameter: returns the index of the global minimum (flattened array).
With axis parameter: returns indices of minimum values along the specified axis.
'''

print(np.argmin(v1))
# 0  (index of value -7, v1[0] = -7)

print(np.argmin(M1))
# 2  (flattened index: M1.flat[2] = -6)

print(M1.flatten())
# [ 5 -6 -7  9 -3  4]

#----- With axis parameter -----#
print(np.argmin(M1, axis=0))  # Index of minimum in each column
# [0 0 0]

print(np.argmin(M1, axis=1))  # Index of minimum in each row
# [2 1]

#----- Check -----#

print(M1)
# [[ 5 -6 -7]
#  [ 9 -3  4]]
# Row 0: min is -7 at index 2
# Row 1: min is -3 at index 1


#----------------------------------------------------------------------------------------------------#
#--------------------------------------- 11. np.nanargmax() -----------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.nanargmax() returns the indices of the maximum values along an axis, ignoring NaNs.
Useful when working with data containing NaN values.
'''

print(np.argmax(M_with_nan))
# 1  (returns index of NaN in flattened array)

print(np.nanargmax(M_with_nan))
# 4  (index of 5.0, ignoring NaNs)

print(np.nanargmax(M_with_nan, axis=0))
# [1 1 0]

print(np.nanargmax(M_with_nan, axis=1))
# [2 1]


#----------------------------------------------------------------------------------------------------#
#--------------------------------------- 12. np.nanargmin() -----------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.nanargmin() returns the indices of the minimum values along an axis, ignoring NaNs.
Useful when working with data containing NaN values.
'''

print(np.argmin(M_with_nan))
# 1  (returns index of NaN in flattened array)

print(np.nanargmin(M_with_nan))
# 0  (index of 1.0, ignoring NaNs)

print(np.nanargmin(M_with_nan, axis=0))
# [0 1 0]

print(np.nanargmin(M_with_nan, axis=1))
# [0 0]


#----------------------------------------------------------------------------------------------------#
#------------------------------------------ 13. np.ptp() --------------------------------------------#
#----------------------------------------------------------------------------------------------------#
'''
np.ptp() returns the range (peak-to-peak, i.e., maximum - minimum) of values along an axis.
ptp stands for "peak to peak".
=> ptp(x) = max(x) - min(x)
'''

print(np.ptp(v1))
# 13  (max=6, min=-7, so 6-(-7)=13)

print(np.ptp(M1))
# 16 (max=9, min=-7, so 9-(-7)=16)

print(np.ptp(M1, axis=0))  # Range in each column
# [4 3 11]

print(np.ptp(M1, axis=1))  # Range in each row
# [12 12]

#----- Check -----#

print(np.amax(M1, axis=1) - np.amin(M1, axis=1))
# [12 12]  # Same as np.ptp(M1, axis=1)
