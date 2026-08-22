'''
1. np.sin(): computes the sine of each element in the array.
2. np.cos(): computes the cosine of each element in the array.
3. np.tan(): computes the tangent of each element in the array.

4. np.arcsin() or np.asin(): computes the inverse sine (arcsine) of each element in the array.
5. np.arccos() or np.acos(): computes the inverse cosine (arccosine) of each element in the array.
6. np.arctan() or np.atan(): computes the inverse tangent (arctangent) of each element in the array.
7. np.hypot(): computes the hypotenuse given the legs of a right triangle.
8. np.arctan2() or np.atan2(): computes the element-wise arc tangent of x1/x2 choosing the quadrant correctly.

9. np.degrees() or np.rad2deg(): converts angles from radians to degrees.
10. np.radians() or np.deg2rad(): converts angles from degrees to radians.
11. np.unwrap(): unwraps by taking the complement of large deltas with respect to the period.
'''

import numpy as np

np.random.seed(3)
v1 = np.random.uniform(-np.pi, np.pi, 5)
# array([ 0.31917264,  1.30783134, -1.31378427,  0.06803185,  2.46895853])

np.random.seed(3)
v2 = np.random.uniform(0, 2*np.pi, 5)
# array([3.46076529, 4.44942399, 1.82780838, 3.2096245 , 5.61055118])

np.random.seed(4)
M1 = np.random.uniform(-np.pi/2, np.pi/2, (2, 3))
M2 = np.random.uniform(0, np.pi, (2, 3))

print(M1)
# [[ 1.46721751  0.14838449  1.48498171]
#  [ 0.67486435  0.62118342 -0.89193115]]

print(M2)
# [[3.06705666 0.01957292 0.79476753]
#  [1.36593788 2.44850366 0.62104598]]


# =========================================================================================
# 1. np.sin()
# =========================================================================================
'''
np.sin() computes the sine of each element in the array.
Input is in radians.
'''

print(np.sin(v1))
# [ 0.31378109  0.96562349 -0.96715381  0.06797938  0.62304851]

print(np.sin(M1))
# [[ 0.99464051  0.14784057  0.99632019]
#  [ 0.62479141  0.58199792 -0.77828579]]


# =========================================================================================
# 2. np.cos()
# =========================================================================================
'''
np.cos() computes the cosine of each element in the array.
Input is in radians.
'''

print(np.cos(v1))
# [ 0.94949535  0.25994475  0.25419189  0.99768673 -0.78218319]

print(np.cos(M1))
# [[0.10339371 0.98901121 0.08570933]
#  [0.78079171 0.81319028 0.62791021]]


# =========================================================================================
# 3. np.tan()
# =========================================================================================
'''
np.tan() computes the tangent of each element in the array.
Input is in radians.
=> tan(x) = sin(x) / cos(x)
'''

print(np.tan(v1))
# [ 0.33047143  3.71472588 -3.80481774  0.068137   -0.79655063]

print(np.tan(M1))
# [[ 9.61993284  0.14948321 11.6244079 ]
#  [ 0.8002024   0.71569709 -1.23948581]]

# Check
print(np.sin(v1) / np.cos(v1))
# [ 0.33047143  3.71472588 -3.80481774  0.068137   -0.79655063]

##-------------------##
## Compute cotangent ##
##-------------------##

print(1 / np.tan(v1))
# [ 3.02598017  0.26919887 -0.26282468 14.67631334 -1.25541299]

print(np.reciprocal(np.tan(v1)))
# [ 3.02598017  0.26919887 -0.26282468 14.67631334 -1.25541299]


# =========================================================================================
# 4. np.arcsin() or np.asin()
# =========================================================================================
'''
np.arcsin() or np.asin() computes the inverse sine (arcsine) of each element in the array.
Returns values in the range [-π/2, π/2].
Input values must be in the range [-1, 1].
'''

v1_normalized = v1 / np.pi  # Normalize to [-1, 1]
# array([ 0.10159581,  0.41629565, -0.41819052,  0.02165521,  0.78589391])

print(np.arcsin(v1_normalized))
# [ 0.1017714   0.42936733 -0.43145238  0.0216569   0.90414041]

print(np.arcsin(np.sin(M1)))
# [[ 1.46721751  0.14838449  1.48498171]
#  [ 0.67486435  0.62118342 -0.89193115]]

print(np.asin(v1_normalized))
# [ 0.1017714   0.42936733 -0.43145238  0.0216569   0.90414041]


# =========================================================================================
# 5. np.arccos() or np.acos()
# =========================================================================================
'''
np.arccos() or np.acos() computes the inverse cosine (arccosine) of each element in the array.
Returns values in the range [0, π].
Input values must be in the range [-1, 1].
'''

v2_normalized = v2 / (2*np.pi)  # Normalize to [-1, 1]
# array([0.5507979 , 0.70814782, 0.29090474, 0.51082761, 0.89294695])

print(np.arccos(v2_normalized))
# [0.9874764  0.78392482 1.27562399 1.03464913 0.46694664]

print(np.arccos(np.cos(M2)))
# [[3.06705666 0.01957292 0.79476753]
#  [1.36593788 2.44850366 0.62104598]]

print(np.acos(v2_normalized))
# [0.9874764  0.78392482 1.27562399 1.03464913 0.46694664]


# =========================================================================================
# 6. np.arctan() or np.atan()
# =========================================================================================
'''
np.arctan() or np.atan() computes the inverse tangent (arctangent) of each element in the array.
Returns values in the range [-π/2, π/2].
'''

print(np.arctan(v1))
# [ 0.30895225  0.91800099 -0.92019101  0.06792718  1.18596207]

print(np.arctan(M1))
# [[ 0.9725522   0.14730961  0.97814049]
#  [ 0.59365647  0.5558501  -0.72833925]]

print(np.atan(v1))
# [ 0.30895225  0.91800099 -0.92019101  0.06792718  1.18596207]

##-----------------------##
## Calculate arcotangent ##
##-----------------------##

print(np.arctan(1 / v1))
# [ 1.26184407  0.65279533 -0.65060532  1.50286914  0.38483426]

print(np.pi/2 - np.arctan(v1))
# [ 1.26184407  0.65279533 -0.65060532  1.50286914  0.38483426]


# =========================================================================================
# 7. np.hypot()
# =========================================================================================

'''
np.hypot() computes the hypotenuse given the legs of a right triangle.
=> hypot(a, b) = sqrt(a^2 + b^2)
'''

print(np.hypot(v1, v2))
# [4.98043082 6.12084926 2.18145313 4.24840267 2.26894031]

print(np.hypot(M1, M2))
# [[2.42594894 1.32770698 1.75170169]
#  [1.56207178 1.43932092 0.67598886]]

# Check
print(np.sqrt(v1**2 + v2**2))
# [4.98043082 6.12084926 2.18145313 4.24840267 2.26894031]

# =========================================================================================
# 8. np.arctan2() or np.atan2()
# =========================================================================================
'''
np.arctan2() or np.atan2() computes the element-wise arc tangent of x1/x2 choosing the quadrant correctly.
Returns values in the range [-π, π].
=> arctan2(y, x) returns the angle θ such that x = r*cos(θ) and y = r*sin(θ)

NOTE: The order is arctan2(y, x), not arctan2(x, y).
Unlike np.arctan(y/x), this function correctly handles all four quadrants.
'''

print(np.arctan2(v1, v2))
# [ 0.09196587  0.28588124 -0.62321628  0.02119303  0.41455406]

print(np.arctan2(M1, M2))
# [[ 0.44620222  1.43964666  1.07938406]
#  [ 0.45888967  0.24845722 -0.9625622 ]]

print(np.atan2(v1, v2))
# [ 0.09196587  0.28588124 -0.62321628  0.02119303  0.41455406]

# Comparison with np.arctan()
print(np.arctan(v1 / v2))  # This does NOT give the correct angle in all quadrants
# [ 0.09196587  0.28588124 -0.62321628  0.02119303  0.41455406]

# Example where they differ:
x, y = -1, -1
print(f"arctan2({y}, {x}) = {np.arctan2(y, x)}")  # -2.356... (3rd quadrant)
print(f"arctan({y}/{x}) = {np.arctan(y/x)}")      # 0.785... (1st quadrant - WRONG!)


# =========================================================================================
# 9. np.degrees() or np.rad2deg()
# =========================================================================================
'''
np.degrees() or np.rad2deg() converts angles from radians to degrees.
=> degrees = radians * 180 / π
'''

print(np.degrees(v1))
# [ 18.28724493  74.93321614 -75.27429399   3.89793787 141.46090357]

print(np.degrees(M1))
# [[ 84.06537102   8.50180485  85.08318479]
#  [ 38.66687886  35.59118843 -51.1038908 ]]

print(np.rad2deg(v1))
# [ 18.28724493  74.93321614 -75.27429399   3.89793787 141.46090357]


# =========================================================================================
# 10. np.radians() or np.deg2rad()
# =========================================================================================
'''
np.radians() or np.deg2rad() converts angles from degrees to radians.
=> radians = degrees * π / 180
'''

degrees_array = np.array([0, 30, 45, 60, 90, 180, 270, 360])

print(np.radians(degrees_array))
# [0.         0.52359878 0.78539816 1.04719755 1.57079633 3.14159265
#  4.71238898 6.28318531]

print(np.deg2rad(degrees_array))
# [0.         0.52359878 0.78539816 1.04719755 1.57079633 3.14159265
#  4.71238898 6.28318531]

# Check
print(np.radians(np.degrees(v1)))
# [ 0.31917264  1.30783134 -1.31378427  0.06803185  2.46895853]
# Same as v1!


# =========================================================================================
# 11. np.unwrap()
# =========================================================================================
'''
np.unwrap() unwraps a phase angle array by taking the complement of large deltas with respect to the period.
This is useful for processing phase data that wraps around at ±π (default period = 2π).
'''

# Create a wrapped phase array with jumps
wrapped_phase = np.array([0.1, 0.5, 0.9, -2.8, -2.4, -2.0])  # Jump from 0.9 to -2.8 (~2π jump)

print(np.unwrap(wrapped_phase))
# [ 0.1         0.5         0.9         3.48318531  3.88318531  4.28318531]
# The -2.8 is unwrapped to 3.48... (= -2.8 + 2π)

# Another example with continuous phase
angles = np.linspace(0, 3*np.pi, 10)
wrapped = (angles + np.pi) % (2*np.pi) - np.pi  # Wrap to [-π, π]

print(wrapped)
# [ 0.          1.04719755  2.0943951  -3.14159265 -2.0943951  -1.04719755
#   0.          1.04719755  2.0943951  -3.14159265]

print(np.unwrap(wrapped))
# [0.         1.04719755 2.0943951  3.14159265 4.1887902  5.23598776
#  6.28318531 7.33038286 8.37758041 9.42477796]

##---------------------------------------##
## Common Trigonometric Identities Check ##
##---------------------------------------##
'''np.allclose() is used to check if two arrays are element-wise equal within a tolerance.'''

# sin²(x) + cos²(x) = 1
print(np.allclose(np.sin(v1)**2 + np.cos(v1)**2, 1))
# True

# tan(x) = sin(x) / cos(x)
print(np.allclose(np.tan(M1), np.sin(M1) / np.cos(M1)))
# True

# arcsin(sin(x)) = x (for x in [-π/2, π/2])
x_range = np.linspace(-np.pi/2, np.pi/2, 5)
print(np.allclose(np.arcsin(np.sin(x_range)), x_range))
# True

# arctan2(sin(x), cos(x)) = x (for x in [-π, π])
x_range2 = np.linspace(-np.pi, np.pi, 5)
print(np.allclose(np.arctan2(np.sin(x_range2), np.cos(x_range2)), x_range2))
# True
