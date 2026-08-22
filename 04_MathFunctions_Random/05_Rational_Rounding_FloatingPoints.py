'''
1. Rational routines
   + np.lcm(): returns the lowest common multiple of |x1| and |x2|.
   + np.gcd(): returns the greatest common divisor of |x1| and |x2|.

2. Rounding
   + np.around() or np.round(): evenly rounds to the given number of decimals.
   + np.rint(): rounds elements of the array to the nearest integer.
   + np.floor(): returns the floor of the input, element-wise.
   + np.ceil(): returns the ceiling of the input, element-wise.
   + np.trunc(): returns the truncated value of the input, element-wise.

3. Floating point routines
   + np.signbit(): returns element-wise True where signbit is set (less than zero).
   + np.copysign(): changes the sign of x1 to that of x2, element-wise.
   + np.frexp(): decomposes the elements of x into mantissa and twos exponent.
   + np.ldexp(): returns x1 * 2**x2, element-wise.
   + np.nextafter(): returns the next floating-point value after x1 towards x2, element-wise.
   + np.spacing(): returns the distance between x and the nearest adjacent number.
'''

import numpy as np

np.random.seed(7)
v1 = np.random.randint(1, 25, 5) # array([16,  5, 23,  4, 20])
v2 = np.random.randint(33, 57, 5) # array([56, 40, 47, 56, 41])
# array([15, 24, 12, 20, 21])

np.random.seed(8)
M1 = np.random.randint(1, 25, (2, 3))
M2 = np.random.randint(33, 57, (2, 3))

print(M1)
# [[ 4 21 18]
#  [10  6  9]]

print(M2)
# [[52 41 49]
#  [46 54 50]]


# =========================================================================================
# 1. Rational routines
# =========================================================================================

##----------##
## np.lcm() ##
##----------##
'''
np.lcm() returns the lowest common multiple (LCM) of |x1| and |x2|.
The LCM is the smallest positive integer that is divisible by both x1 and x2.
'''

print(np.lcm(12, 8))
# 24

print(np.lcm(v1, v2))
# [ 112   40 1081   56  820]

print(np.lcm(M1, M2))
# [[ 52 861 882]
#  [230  54 450]]

# Check: LCM is divisible by both numbers
lcm_val = np.lcm(v1, v2)

print(lcm_val % v1)  # Should be all zeros
# [0 0 0 0 0]

print(lcm_val % v2)  # Should be all zeros
# [0 0 0 0 0]

##----------##
## np.gcd() ##
##----------##
'''
np.gcd() returns the greatest common divisor (GCD) of |x1| and |x2|.
The GCD is the largest positive integer that divides both x1 and x2.
'''

print(np.gcd(12, 8))
# 4

print(np.gcd(v1, v2))
# [8 5 1 4 1]

print(np.gcd(M1, M2))
# [[4 1 1]
#  [2 6 1]]

# Check: Relationship between GCD and LCM

# For positive integers: x1 * x2 = gcd(x1, x2) * lcm(x1, x2)

print(v1 * v2 == np.gcd(v1, v2) * np.lcm(v1, v2))
# [ True  True  True  True  True]


# =========================================================================================
# 2. Rounding
# =========================================================================================

# Create arrays with decimal values for rounding examples
np.random.seed(9)
v_float = np.random.uniform(-10, 10, 5)
# array([-9.79251692,  0.03749184, -0.08453414, -7.32340942, -7.15777829])

M_float = np.random.uniform(-10, 10, (2, 3))
# array([[-5.62882649, -1.62983639, -5.03797663],
#        [-8.31880698, -3.0900272 , -6.66447307]])

##---------------------------##
## np.around() or np.round() ##
##---------------------------##
'''
np.around() or np.round() evenly rounds to the given number of decimals.
Rounds to the nearest even value when exactly halfway between two values.
'''

print(np.around(v_float))
# [-10.   0.  -0.  -7.  -7.]

print(np.around(v_float, decimals=2))
# [-9.79  0.04 -0.08 -7.32 -7.16]

print(np.round(M_float, decimals=1))
# [[-5.6 -1.6 -5. ]
#  [-8.3 -3.1 -6.7]]

# Banker's rounding (round half to even)
halfway_values = np.array([0.5, 1.5, 2.5, 3.5, 4.5])
print(np.around(halfway_values))
# [0. 2. 2. 4. 4.]  # Note: 0.5->0, 1.5->2, 2.5->2, 3.5->4, 4.5->4

##-----------##
## np.rint() ##
##-----------##
'''
np.rint() rounds elements of the array to the nearest integer.
Similar to np.around() with decimals=0, but returns a float type.
'''

print(np.rint(v_float))
# [-10.   0.  -0.  -7.  -7.]

print(np.rint(M_float))
# [[-6. -2. -5.]
#  [-8. -3. -7.]]

##------------##
## np.floor() ##
##------------##
'''
np.floor() returns the floor of the input, element-wise.
The floor is the smallest integer less than or equal to the input.
'''

print(np.floor(v_float))
# [-10.   0.  -1.  -8.  -8.]

print(np.floor(M_float))
# [[-6. -2. -6.]
#  [-9. -4. -7.]]

##-----------##
## np.ceil() ##
##-----------##
'''
np.ceil() returns the ceiling of the input, element-wise.
The ceiling is the largest integer greater than or equal to the input.
'''

print(np.ceil(v_float))
# [-9.  1. -0. -7. -7.]

print(np.ceil(M_float))
# [[-5. -1. -5.]
#  [-8. -3. -6.]]

##------------##
## np.trunc() ##
##------------##
'''
np.trunc() rounds to nearest integer towards zero, element-wise.
Positive values are rounded down, negative values are rounded up.
'''

print(np.trunc(v_float))
# [-9.  0. -0. -7. -7.]

print(np.trunc(M_float))
# [[-5. -1. -5.]
#  [-8. -3. -6.]]

test_vals = np.array([-2.7, -2.3, 2.3, 2.7])
print(f"trunc:    {np.trunc(test_vals)}")  # [-2. -2.  2.  2.]
print(f"floor:    {np.floor(test_vals)}")  # [-3. -3.  2.  2.]
print(f"ceil:     {np.ceil(test_vals)}")   # [-2. -2.  3.  3.]
# trunc rounds towards zero


# =========================================================================================
# 3. Floating point routines
# =========================================================================================

v_signed = np.array([-3.5, 0.0, 2.8, -0.0, 5.1])

M_signed = np.array([[-2.5, 3.1, -0.5],
                     [1.2, -4.8, 0.0]])

##--------------##
## np.signbit() ##
##--------------##
'''
np.signbit() returns element-wise True where signbit is set (less than zero).
This correctly handles negative zero (-0.0) unlike simple comparison with 0.
'''

print(np.signbit(v_signed))
# [ True False False  True False]

print(np.signbit(M_signed))
# [[ True False  True]
#  [False  True False]]

# Distinguishes -0.0 from +0.0
print(np.signbit(-0.0))
# True

print(np.signbit(0.0))
# False

##---------------##
## np.copysign() ##
##---------------##
'''
np.copysign() changes the sign of x1 to that of x2, element-wise.
Returns values with the magnitude of x1 and the sign of x2.
'''

magnitudes = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
signs = np.array([1.0, -1.0, 1.0, -1.0, -1.0])

print(np.copysign(magnitudes, signs))
# [ 1. -2.  3. -4. -5.]

print(np.copysign(M1, M_signed))
# [[ -6. 11. -22.]
#  [ 12. -24.  18.]]

# Make all values positive
print(np.copysign(v_signed, 1.0))
# [3.5 0.  2.8 0.  5.1]

# Make all values negative
print(np.copysign(v_signed, -1.0))
# [-3.5 -0.  -2.8 -0.  -5.1]

##------------##
## np.frexp() ##
##------------##
'''
np.frexp() decomposes the elements of x into mantissa and twos exponent.
Returns (mantissa, exponent) where x = mantissa * 2**exponent.

The mantissa is in the range [0.5, 1) for non-zero values.
'''

values = np.array([1.0, 2.0, 4.0, 8.0, 3.0])
mantissa, exponent = np.frexp(values)

print(mantissa)
# [0.5   0.5   0.5   0.5   0.75 ]

print(exponent)
# [1 2 3 4 2]

# Check: reconstruct original values

reconstructed = mantissa * 2**exponent
print(reconstructed) # [1. 2. 4. 8. 3.]
print(np.allclose(values, reconstructed)) # True

# For matrices
mantissa_M, exponent_M = np.frexp(M_float)
print(mantissa_M)
# [[-0.62322457 -0.57057103 -0.56806079]
#  [ 0.92463081  0.71753386 -0.54430617]]

print(exponent_M)
# [[3 3 1]
#  [2 3 4]]

##------------##
## np.ldexp() ##
##------------##
'''
np.ldexp() returns x1 * 2**x2, element-wise.
This is the inverse operation of np.frexp().
'''

mantissa = np.array([0.5, 0.75, 0.625])
exponent = np.array([2, 3, 4])

print(np.ldexp(mantissa, exponent))
# [ 2.  6. 10.]

# Check: inverse of frexp
original = np.array([2.0, 6.0, 10.0])
m, e = np.frexp(original)
reconstructed = np.ldexp(m, e)
print(np.allclose(original, reconstructed))
# True

# Efficient way to multiply/divide by powers of 2
print(np.ldexp(5.0, 3))  # 5 * 2^3 = 40
# 40.0

print(np.ldexp(100.0, -2))  # 100 * 2^-2 = 25
# 25.0

##----------------##
## np.nextafter() ##
##----------------##
'''
np.nextafter() returns the next floating-point value after x1 towards x2, element-wise.
This is useful for understanding floating-point precision and machine epsilon.
'''

print(np.nextafter(1.0, 2.0))  # Next float after 1.0 towards 2.0
# 1.0000000000000002

print(np.nextafter(1.0, 0.0))  # Next float after 1.0 towards 0.0
# 0.9999999999999999

# Array operations
x1 = np.array([1.0, 2.0, 3.0])
x2 = np.array([2.0, 1.0, 3.0])
print(np.nextafter(x1, x2))
# [1.0000000000000002 1.9999999999999998 3.                ]
'''returns [1. 2. 3.] because the errors are too small, so it rounds back to the original values.'''

# Finding machine epsilon
eps = np.nextafter(1.0, 2.0) - 1.0
print(f"Machine epsilon: {eps}") # 2.220446049250313e-16
print(f"np.finfo(float).eps: {np.finfo(float).eps}") # 2.220446049250313e-16
# They should be equal

##--------------##
## np.spacing() ##
##--------------##
'''
np.spacing() returns the distance between x and the nearest adjacent number.
This shows the spacing between representable floating-point numbers at x.
'''

print(np.spacing(1.0))
# 2.220446049250313e-16

print(np.spacing(1000.0))
# 1.1368683772161603e-13

print(np.spacing(1e20))
# 16384.0

# The spacing increases with the magnitude of x (because of how floating-point numbers are represented).
values = np.array([1.0, 10.0, 100.0, 1000.0])
print(np.spacing(values))
# [2.22044605e-16 1.77635684e-15 1.42108547e-14 1.13686838e-13]
'''
That is why in machine learning, we often normalize data to a smaller range
to avoid issues with floating-point precision, i.e to get better precision.
'''

# Relationship with nextafter
x = 5.0
spacing = np.spacing(x)
next_float = np.nextafter(x, np.inf)
print(f"Spacing at {x}: {spacing}") # Spacing at 5.0: 8.881784197001252e-16
print(f"Difference to next float: {next_float - x}") # 8.881784197001252e-16
print(f"Are they equal? {np.isclose(spacing, next_float - x)}")
# True


##-------------------------------##
## Comparisons and Verifications ##
##-------------------------------##

# Rounding comparison
test_val = 2.7
print(f"around:    {np.around(test_val)}") # 3.0
print(f"rint:      {np.rint(test_val)}")   # 3.0
print(f"floor:     {np.floor(test_val)}")  # 2.0
print(f"ceil:      {np.ceil(test_val)}")   # 3.0
print(f"trunc:     {np.trunc(test_val)}")  # 2.0

test_val_neg = -2.7
print(f"around:    {np.around(test_val_neg)}") # -3.0 (rounds to nearest even)
print(f"rint:      {np.rint(test_val_neg)}")   # -3.0 (rounds to nearest even)
print(f"floor:     {np.floor(test_val_neg)}")  # -3.0 (rounds down)
print(f"ceil:      {np.ceil(test_val_neg)}")   # -2.0 (rounds up)
print(f"trunc:     {np.trunc(test_val_neg)}")  # -2.0 (rounds towards zero)
