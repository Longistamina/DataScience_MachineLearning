'''
1. np.exp(): calculates the exponential of all elements in the input array.
2. np.expm1(): calculates exp(x) - 1 for all elements in the input array.
3. np.exp2(): calculates 2^x for all elements in the input array.

4. np.log(): computes the natural logarithm (base e) of each element in the array.
5. np.log10(): computes the base 10 logarithm of each element in the array.
6. np.log2(): computes the base 2 logarithm of each element in the array.
7. np.log1p(): computes the natural logarithm of (1 + x) for each element in the array.

8. np.logaddexp(): computes the logarithm of the sum of exponentiations of the inputs.
9. np.logaddexp2(): computes the logarithm of the sum of exponentiations of the inputs in base-2.
'''

import numpy as np

np.random.seed(5)
v1 = np.random.uniform(0.1, 5, 5)
# array([1.18776654, 4.3665883 , 1.11292386, 4.60119345, 2.49321483])

np.random.seed(5)
v2 = np.random.uniform(0.5, 3, 5)
# array([1.05498293, 2.67683077, 1.01679789, 2.79652727, 1.72102797])

np.random.seed(6)
M1 = np.random.uniform(0.5, 10, (2, 3))
M2 = np.random.uniform(1, 5, (2, 3))

print(M1)
# [[8.98217144 3.65380815 8.30167667]
#  [0.89611794 1.52273846 6.15299461]]

print(M2)
# [[3.11926945 2.67522971 2.3416314 ]
#  [3.49007773 2.7525657  3.94352843]]


# =========================================================================================
# 1. np.exp()
# =========================================================================================
'''
np.exp() calculates the exponential of all elements in the input array.
=> exp(x) = e^x where e ≈ 2.71828...
'''

print(np.exp(v1))
# [ 3.27974783 78.77441806  3.04324342 99.60311597 12.10011341]

print(np.exp(M1))
# [[7.95989779e+03 3.86214627e+01 4.03062476e+03]
#  [2.45007330e+00 4.58476321e+00 4.70123116e+02]]

# Common usage: exponential growth
initial_value = 100
growth_rate = 0.05
time = np.array([0, 1, 2, 5, 10])
print(initial_value * np.exp(growth_rate * time))
# [100.         105.12710964 110.51709181 128.40254167 164.87212707]

##------------------------------##
## Calculate a^x (example: 3^x) ##
##------------------------------##

print(3 ** v1)
# [  3.68730159 121.16915763   3.39624982 156.79318838  15.47268862]

print(np.power(3, v1))
# [  3.68730159 121.16915763   3.39624982 156.79318838  15.47268862]

print(np.exp(v1 * np.log(3)))
# [  3.68730159 121.16915763   3.39624982 156.79318838  15.47268862]

# =========================================================================================
# 2. np.expm1()
# =========================================================================================
'''
np.expm1() calculates exp(x) - 1 for all elements in the input array.
=> expm1(x) = e^x - 1

This function provides more accurate results for small values of x where exp(x) ≈ 1.
'''

print(np.expm1(v1))
# [ 2.27974783 77.77441806  2.04324342 98.60311597 11.10011341]

print(np.expm1(M1))
# [[7.95889779e+03 3.76214627e+01 4.02962476e+03]
#  [1.45007330e+00 3.58476321e+00 4.69123116e+02]]

# Advantage for small values
small_values = np.array([1e-10, 1e-8, 1e-6])
print(np.exp(small_values) - 1)
# [1.00000008e-10 9.99999994e-09 1.00000050e-06]

print(np.expm1(small_values))
# [1.00000000e-10 1.00000001e-08 1.00000050e-06]  # More accurate!

# Check
print(np.allclose(np.expm1(v1), np.exp(v1) - 1))
# True


# =========================================================================================
# 3. np.exp2()
# =========================================================================================
'''
np.exp2() calculates 2^x for all elements in the input array.
=> exp2(x) = 2^x
'''

print(np.exp2(3))
# 8.0

print(np.exp2(v1))
# [ 2.27799809 20.62880436  2.16283538 24.27153504  5.63031182]

print(np.exp2(M1))
# [[505.71173233  12.58652526 315.53946997]
#  [  1.86105146   2.87335941  71.16000022]]

# Common in computer science (powers of 2)
bits = np.array([0, 1, 2, 3, 4, 8, 16])
print(np.exp2(bits))
# [1.0000e+00 2.0000e+00 4.0000e+00 8.0000e+00 1.6000e+01 2.5600e+02 6.5536e+04]

# Check
print(np.allclose(np.exp2(v1), 2**v1))
# True

print(np.allclose(np.exp2(v1), np.power(2, v1)))
# True


# =========================================================================================
# 4. np.log()
# =========================================================================================
'''
np.log() computes the natural logarithm (base e) of each element in the array.
=> log(x) = ln(x) (logarithm base e)

Input values must be positive (x > 0).
'''

print(np.log(2.71828183)) # ln(e) = 1
# 1.0000000005668856

print(np.log(v1))
# [0.17207469 1.47398199 0.10699066 1.52631572 0.91357297]

print(np.log(M1))
# [[ 2.19524166  1.29576995  2.1164575 ]
#  [-0.10968324  0.42051033  1.81693889]]

# Check: log is inverse of exp
print(np.allclose(np.log(np.exp(v1)), v1))
# True

print(np.allclose(np.exp(np.log(v1)), v1))
# True

##--------------------##
## Calculate log_b(x) ##
##--------------------##

base = 3
print(np.log(v1) / np.log(base))
# [0.15662913 1.34167623 0.0973871  1.38931244 0.83156996]

print(np.log(M1) / np.log(base))
# [[ 1.99819507  1.17946064  1.92648264]
#  [-0.09983799  0.382765    1.65384905]]

print(np.log(10000000) / np.log(10))  # log10(10^7) = 7
# 7.0


# =========================================================================================
# 5. np.log10()
# =========================================================================================
'''
np.log10() computes the base 10 logarithm of each element in the array.
=> log10(x) = log₁₀(x)

Input values must be positive (x > 0).
'''

print(np.log10(1000))  # log10(10^3) = 3
# 3.0

print(np.log10(v1))
# [0.07473109 0.64014225 0.04646545 0.66287049 0.3967597 ]

print(np.log10(M1))
# [[ 0.95338134  0.56274574  0.91916581]
#  [-0.04763483  0.18262532  0.78908653]]

# Common usage: measuring orders of magnitude
powers_of_10 = np.array([1, 10, 100, 1000, 10000])
print(np.log10(powers_of_10))
# [0. 1. 2. 3. 4.]

# Calculate pH in chemistry
hydrogen_ion_concentration = np.array([1e-7, 1e-5, 1e-3, 1e-1])
pH = -np.log10(hydrogen_ion_concentration)
print(pH)
# [7. 5. 3. 1.]

# Check: relationship with natural log
print(np.allclose(np.log10(v1), np.log(v1) / np.log(10)))
# True


# =========================================================================================
# 6. np.log2()
# =========================================================================================
'''
np.log2() computes the base 2 logarithm of each element in the array.
=> log2(x) = log₂(x)

Input values must be positive (x > 0).
'''

print(np.log2(8))  # log2(2^3) = 3
# 3.0

print(np.log2(v1))
# [0.24825129 2.12650651 0.1543549  2.20200811 1.3180072 ]

print(np.log2(M1))
# [[ 3.16706426  1.86940088  3.05340274]
#  [-0.15823947  0.60666817  2.62128873]]

# Common in computer science (powers of 2)
powers_of_2 = np.array([1, 2, 4, 8, 16, 32, 64, 128])
print(np.log2(powers_of_2))
# [0. 1. 2. 3. 4. 5. 6. 7.]

# Check: relationship with natural log
print(np.allclose(np.log2(v1), np.log(v1) / np.log(2)))
# True

# Check: log2 is inverse of exp2
print(np.allclose(np.log2(np.exp2(v1)), v1))
# True


# =========================================================================================
# 7. np.log1p()
# =========================================================================================
'''
np.log1p() computes the natural logarithm of (1 + x) for each element in the array.
=> log1p(x) = ln(1 + x)

This function provides more accurate results for small values of x where 1 + x ≈ 1.
Input values must be greater than -1 (x > -1).
'''

print(np.log1p(v1))
# [0.78288118 1.68019238 0.7480727  1.72297969 1.25082247]

print(np.log1p(M1))
# [[2.30080065 1.53768584 2.23019467]
#  [0.63980861 0.925345   1.9675311 ]]

# Advantage for small values
small_values = np.array([1e-10, 1e-8, 1e-6])
print(np.log(1 + small_values))
# [1.00000008e-10 9.99999989e-09 9.99999500e-07]

print(np.log1p(small_values))
# [1.00000000e-10 9.99999995e-09 9.99999500e-07]  # More accurate!

# Check
print(np.allclose(np.log1p(v1), np.log(1 + v1)))
# True


# =========================================================================================
# 8. np.logaddexp()
# =========================================================================================
'''
np.logaddexp() computes the logarithm of the sum of exponentiations of the inputs.
=> logaddexp(x1, x2) = log(exp(x1) + exp(x2))

This function is numerically stable and avoids overflow for large values.
It's commonly used in machine learning (e.g., log-sum-exp trick).
'''

print(np.logaddexp(v1, v2))
# [1.81672423 4.5359633  1.75916264 4.75351048 2.8730213 ]

print(np.logaddexp(M1, M2))
# [[8.98501039 3.97287624 8.30425314]
#  [3.56214121 3.00902261 6.25713769]]

# For large values, direct computation would overflow
large_values = np.array([1000, 1001])
print(np.logaddexp(large_values[0], large_values[1]))
# 1001.3132616875182

# Direct computation would fail:
np.log(np.exp(1000) + np.exp(1001))  # Results in inf!
'''
<stdin>:1: RuntimeWarning: overflow encountered in exp
np.float64(inf)
'''

# Check for small values
small_v1 = v1 / 100
small_v2 = v2 / 100
print(np.allclose(np.logaddexp(small_v1, small_v2),
                  np.log(np.exp(small_v1) + np.exp(small_v2))))
# True


# =========================================================================================
# 9. np.logaddexp2()
# =========================================================================================
'''
np.logaddexp2() computes the logarithm of the sum of exponentiations of the inputs in base-2.
=> logaddexp2(x1, x2) = log2(2^x1 + 2^x2)

This is the base-2 version of logaddexp, useful for information theory and bit-level computations.
'''

print(np.logaddexp2(v1, v2))
# [2.12290185 4.756132   2.06566133 4.96436146 3.15817932]

print(np.logaddexp2(M1, M2))
# [[9.00675023 4.24594657 8.32466763]
#  [3.71118825 3.26491245 6.43539206]]

# For large values, direct computation would overflow
large_values = np.array([1000, 1001])
print(np.logaddexp2(large_values[0], large_values[1]))
# 1001.5849625007212

# Check: relationship with logaddexp
print(np.allclose(np.logaddexp2(v1, v2),
                  np.logaddexp(v1 * np.log(2), v2 * np.log(2)) / np.log(2)))
# True

# Check for small values
small_v1 = v1 / 10
small_v2 = v2 / 10
print(np.allclose(np.logaddexp2(small_v1, small_v2),
                  np.log2(np.exp2(small_v1) + np.exp2(small_v2))))
# True

##----------------------------------##
## Common Logarithm and Exponential ##
## Properties Check                 ##
##----------------------------------##

# exp(log(x)) = x
print(np.allclose(np.exp(np.log(v1)), v1))
# True

# log(exp(x)) = x
print(np.allclose(np.log(np.exp(v1)), v1))
# True

# log(x * y) = log(x) + log(y)
print(np.allclose(np.log(v1 * v2), np.log(v1) + np.log(v2)))
# True

# log(x / y) = log(x) - log(y)
print(np.allclose(np.log(v1 / v2), np.log(v1) - np.log(v2)))
# True

# log(x^y) = y * log(x)
print(np.allclose(np.log(v1**2), 2 * np.log(v1)))
# True

# exp(x + y) = exp(x) * exp(y)
print(np.allclose(np.exp(v1 + v2), np.exp(v1) * np.exp(v2)))
# True

# exp(x - y) = exp(x) / exp(y)
print(np.allclose(np.exp(v1 - v2), np.exp(v1) / np.exp(v2)))
# True

# Change of base formula: log_b(x) = log(x) / log(b)
base = 5
print(np.allclose(np.log(v1) / np.log(base),
                  np.log10(v1) / np.log10(base)))
# True
