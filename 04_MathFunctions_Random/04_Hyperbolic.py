'''
1. np.sinh(): computes the hyperbolic sine of each element in the array.

2. np.cosh(): computes the hyperbolic cosine of each element in the array.

3. np.tanh(): computes the hyperbolic tangent of each element in the array.

4. np.arcsinh() or np.asinh(): computes the inverse hyperbolic sine of each element in the array.

5. np.arccosh() or np.acosh(): computes the inverse hyperbolic cosine of each element in the array.

6. np.arctanh() or np.atanh(): computes the inverse hyperbolic tangent of each element in the array.

7. coth(): computes the hyperbolic cotangent of each element in the array (custom function).

8. sech(): computes the hyperbolic secant of each element in the array (custom function).

9. csch(): computes the hyperbolic cosecant of each element in the array (custom function).

10. arccoth(): computes the inverse hyperbolic cotangent of each element in the array (custom function).

11. arcsech(): computes the inverse hyperbolic secant of each element in the array (custom function).

12. arccsch(): computes the inverse hyperbolic cosecant of each element in the array (custom function).
'''

import numpy as np

np.random.seed(5)
v1 = np.random.uniform(-2, 2, 5)
# array([-1.11202732,  1.48292922, -1.17312338,  1.67444363, -0.04635524])

np.random.seed(5)
v2 = np.random.uniform(0, 3, 5)
# array([0.66597951, 2.61219692, 0.62015747, 2.75583272, 1.46523357])

np.random.seed(6)
M1 = np.random.uniform(-1, 1, (2, 3))
M2 = np.random.uniform(0, 2, (2, 3))

print(M1)
# [[ 0.7857203  -0.33604039  0.64245825]
#  [-0.91660675 -0.78468664  0.19010413]]

print(M2)
# [[1.05963472 0.83761486 0.6708157 ]
#  [1.24503886 0.87628285 1.47176421]]


# =========================================================================================
# 1. np.sinh()
# =========================================================================================
'''
np.sinh() computes the hyperbolic sine of each element in the array.
=> sinh(x) = (e^x - e^(-x)) / 2
'''

print(np.sinh(v1))
# [-1.35581236  2.0894303  -1.46133641  2.57420661 -0.04637185]

print(np.sinh(M1))
# [[ 0.86909772 -0.34240065  0.68757541]
#  [-1.05045828 -0.86772869  0.19125125]]

# Check
print((np.exp(v1) - np.exp(-v1)) / 2)
# [-1.35581236  2.0894303  -1.46133641  2.57420661 -0.04637185]


# =========================================================================================
# 2. np.cosh()
# =========================================================================================
'''
np.cosh() computes the hyperbolic cosine of each element in the array.
=> cosh(x) = (e^x + e^(-x)) / 2

NOTE: cosh(x) is always >= 1 for all real x.
'''

print(np.cosh(v1))
# [1.68470388 2.31640217 1.77073547 2.76161903 1.0010746 ]

print(np.cosh(M1))
# [[1.32488899 1.05699489 1.21357322]
#  [1.45033189 1.32399134 1.01812427]]

# Check
print((np.exp(v1) + np.exp(-v1)) / 2)
# [1.68470388 2.31640217 1.77073547 2.76161903 1.0010746 ]


# =========================================================================================
# 3. np.tanh()
# =========================================================================================
'''
np.tanh() computes the hyperbolic tangent of each element in the array.
=> tanh(x) = sinh(x) / cosh(x) = (e^x - e^(-x)) / (e^x + e^(-x))

NOTE: tanh(x) is bounded between -1 and 1.
'''

print(np.tanh(v1))
# [-0.80477785  0.90201535 -0.82527087  0.93213676 -0.04632207]

print(np.tanh(M1))
# [[ 0.65597776 -0.32393785  0.56657102]
#  [-0.7242882  -0.65538849  0.18784666]]

# Check
print(np.sinh(v1) / np.cosh(v1))
# [-0.80477785  0.90201535 -0.82527087  0.93213676 -0.04632207]

print((np.exp(v1) - np.exp(-v1)) / (np.exp(v1) + np.exp(-v1)))
# [-0.80477785  0.90201535 -0.82527087  0.93213676 -0.04632207]


# =========================================================================================
# 4. np.arcsinh() or np.asinh()
# =========================================================================================
'''
np.arcsinh() or np.asinh() computes the inverse hyperbolic sine of each element in the array.
Returns the value y such that sinh(y) = x.
=> arcsinh(x) = ln(x + sqrt(x^2 + 1))

NOTE: Defined for all real numbers.
'''

print(np.arcsinh(v1))
# [-0.95841322  1.1852566  -0.99865277  1.28779003 -0.04633866]

print(np.arcsinh(M1))
# [[ 0.72147881 -0.33001724  0.60489009]
#  [-0.82115978 -0.72066582  0.18897731]]

print(np.asinh(v1))
# [-0.95841322  1.1852566  -0.99865277  1.28779003 -0.04633866]

# Check
print(np.sinh(np.arcsinh(v1)))
# [-1.11202732  1.48292922 -1.17312338  1.67444363 -0.04635524]
# Same as v1!

print(np.log(v1 + np.sqrt(v1**2 + 1)))
# [-0.95841322  1.1852566  -0.99865277  1.28779003 -0.04633866]


# =========================================================================================
# 5. np.arccosh() or np.acosh()
# =========================================================================================
'''
np.arccosh() or np.acosh() computes the inverse hyperbolic cosine of each element in the array.
Returns the value y such that cosh(y) = x.
=> arccosh(x) = ln(x + sqrt(x^2 - 1))
NOTE: Only defined for x >= 1. Returns NaN for x < 1.
'''

v1_valid = np.abs(v1) + 1  # Ensure all values >= 1
# array([2.11202732, 2.48292922, 2.17312338, 2.67444363, 1.04635524])

print(np.arccosh(v1_valid))
# [1.37934831 1.55931848 1.41159472 1.63994713 0.30331987]

print(np.arccosh(M2))
# [[0.34366046        nan        nan]
#  [0.68649551        nan 0.9367287 ]]
'''nan values occur because some elements in M2 are < 1.'''

print(np.acosh(v1_valid))
# [1.37934831 1.55931848 1.41159472 1.63994713 0.30331987]

# Check
print(np.cosh(np.arccosh(v1_valid)))
# [2.11202732 2.48292922 2.17312338 2.67444363 1.04635524]
# Same as v1_valid!

print(np.log(v1_valid + np.sqrt(v1_valid**2 - 1)))
# [1.37934831 1.55931848 1.41159472 1.63994713 0.30331987]


# =========================================================================================
# 6. np.arctanh() or np.atanh()
# =========================================================================================
'''
np.arctanh() or np.atanh() computes the inverse hyperbolic tangent of each element in the array.
Returns the value y such that tanh(y) = x.
=> arctanh(x) = 0.5 * ln((1 + x) / (1 - x))
NOTE: Only defined for -1 < x < 1. Returns inf for x = ±1 and NaN for |x| > 1.
'''

v1_normalized = v1 / 3  # Normalize to (-1, 1)
# array([-0.37067577,  0.49430974, -0.39104113,  0.55814788, -0.01545175])

print(np.arctanh(v1_normalized))
# [-0.38920629  0.54174766 -0.41302851  0.63013894 -0.01545298]

print(np.arctanh(M1))
# [[ 1.06014749 -0.34962213  0.76234859]
#  [-1.5673721  -1.05745184  0.1924452 ]]

print(np.atanh(v1_normalized))
# [-0.38920629  0.54174766 -0.41302851  0.63013894 -0.01545298]

# Check
print(np.tanh(np.arctanh(v1_normalized)))
# [-0.37067577  0.49430974 -0.39104113  0.55814788 -0.01545175]
# Same as v1_normalized!

print(0.5 * np.log((1 + v1_normalized) / (1 - v1_normalized)))
# [-0.38920629  0.54174766 -0.41302851  0.63013894 -0.01545298]


# =========================================================================================
# 7. coth()
# =========================================================================================
'''
coth() computes the hyperbolic cotangent of each element in the array.
=> coth(x) = cosh(x) / sinh(x) = 1 / tanh(x)

NOTE: NumPy does not have a built-in coth function.
'''

def coth(x):
    return 1 / np.tanh(x) # or np.cosh(x) / np.sinh(x)
                          # or np.reciprocal(np.tanh(x))

print(coth(v1))
# [ -1.24257893   1.10862859  -1.21172336   1.07280395 -21.58798149]

print(coth(M1))
# [[ 1.52444192 -3.08701193  1.76500379]
#  [-1.38066587 -1.52581257  5.32349092]]

# Check
print(np.cosh(v1) / np.sinh(v1))
# [ -1.24257893   1.10862859  -1.21172336   1.07280395 -21.58798149]


# =========================================================================================
# 8. sech()
# =========================================================================================
'''
sech() computes the hyperbolic secant of each element in the array.
=> sech(x) = 1 / cosh(x) = 2 / (e^x + e^(-x))

NOTE: NumPy does not have a built-in sech function.
'''

def sech(x):
    return 1 / np.cosh(x) # or np.reciprocal(np.cosh(x))

print(sech(v1))
# [0.59357613 0.43170397 0.56473709 0.36210643 0.99892656]

print(sech(M1))
# [[0.75478022 0.94607836 0.82401291]
#  [0.68949735 0.75529195 0.98219837]]

# Check
print(2 / (np.exp(v1) + np.exp(-v1)))
# [0.59357613 0.43170397 0.56473709 0.36210643 0.99892656]


# =========================================================================================
# 9. csch()
# =========================================================================================
'''
csch() computes the hyperbolic cosecant of each element in the array.
=> csch(x) = 1 / sinh(x) = 2 / (e^x - e^(-x))

NOTE: NumPy does not have a built-in csch function.
'''

def csch(x):
    return 1 / np.sinh(x) # or np.reciprocal(np.sinh(x))

print(csch(v1))
# [ -0.73756519   0.47859936  -0.68430513   0.38846921 -21.56480801]

print(csch(M1))
# [[ 1.1506186  -2.9205552   1.45438592]
#  [-0.95196546 -1.15243395  5.22872409]]
# Check
print(2 / (np.exp(v1) - np.exp(-v1)))
# [ -0.73756519   0.47859936  -0.68430513   0.38846921 -21.56480801]


# =========================================================================================
# 10. arccoth()
# =========================================================================================
'''
arccoth() computes the inverse hyperbolic cotangent of each element in the array.
Returns the value y such that coth(y) = x.
=> arccoth(x) = 0.5 * ln((x + 1) / (x - 1))

NOTE: Only defined for |x| > 1. NumPy does not have a built-in arccoth function.
'''

def arccoth(x):
    return 0.5 * np.log((x + 1) / (x - 1))

v1_coth_valid = np.abs(v1) + 1.1  # Ensure all |x| > 1
# array([2.21202732, 2.58292922, 2.27312338, 2.77444363, 1.14635524])

print(arccoth(v1_coth_valid))
# [0.48730394 0.40845181 0.47213573 0.37738303 1.3427448 ]

print(arccoth(M2))
# [[1.77102295        nan        nan]
#  [1.10753064        nan 0.82810406]]
'''nan values occur because some elements in M2 have |x| <= 1.'''

# Check
print(coth(arccoth(v1_coth_valid)))
# [2.21202732 2.58292922 2.27312338 2.77444363 1.14635524]
# Same as v1_coth_valid!


# =========================================================================================
# 11. arcsech()
# =========================================================================================
'''
arcsech() computes the inverse hyperbolic secant of each element in the array.
Returns the value y such that sech(y) = x.
=> arcsech(x) = ln((1 + sqrt(1 - x^2)) / x)

NOTE: Only defined for 0 < x <= 1. NumPy does not have a built-in arcsech function.
'''

def arcsech(x):
    return np.log((1 + np.sqrt(1 - x**2)) / x)

v1_sech_valid = np.abs(v1_normalized)  # Use absolute values in (0, 1)
# array([0.37067577, 0.49430974, 0.39104113, 0.55814788, 0.01545175])

print(arcsech(v1_sech_valid))
# [1.64930605 1.33014941 1.59146209 1.18730604 4.86312061]

print(arcsech(np.abs(M1)))
# [[0.72270481 1.7541638  1.01135213]
#  [0.42339899 0.7248307  2.34417064]]

# Check
print(sech(arcsech(v1_sech_valid)))
# [0.37067577, 0.49430974, 0.39104113, 0.55814788, 0.01545175]
# Same as v1_sech_valid!


# =========================================================================================
# 12. arccsch()
# =========================================================================================
'''
arccsch() computes the inverse hyperbolic cosecant of each element in the array.
Returns the value y such that csch(y) = x.
=> arccsch(x) = ln(1/x + sqrt(1/x^2 + 1))

NOTE: Defined for all x != 0. NumPy does not have a built-in arccsch function.
'''

def arccsch(x):
    return np.log(1/x + np.sqrt(1/x**2 + 1)) # or np.arcsinh(1/x)

print(arccsch(v1))
# [-0.80831567  0.63151925 -0.77308423  0.56643385 -3.76510479]

print(arccsch(M2))
# [[0.8410136  1.01204039 1.1896059 ]
#  [0.73515556 0.97776866 0.63575561]]

# Check
print(csch(arccsch(v1)))
# [-1.11202732  1.48292922 -1.17312338  1.67444363 -0.04635524]
# Same as v1!

# Alternative formula: arccsch(x) = arcsinh(1/x)
print(np.arcsinh(1/v1))
# [-0.80831567  0.63151925 -0.77308423  0.56643385 -3.76510479]

##------------------------------------##
## Common Hyperbolic Identities Check ##
##------------------------------------##

# cosh²(x) - sinh²(x) = 1 (fundamental hyperbolic identity)
print(np.allclose(np.cosh(v1)**2 - np.sinh(v1)**2, 1))
# True

# tanh(x) = sinh(x) / cosh(x)
print(np.allclose(np.tanh(M1), np.sinh(M1) / np.cosh(M1)))
# True

# coth(x) = cosh(x) / sinh(x)
print(np.allclose(coth(v1), np.cosh(v1) / np.sinh(v1)))
# True

# sech²(x) + tanh²(x) = 1
print(np.allclose(sech(v1)**2 + np.tanh(v1)**2, 1))
# True

# coth²(x) - csch²(x) = 1
print(np.allclose(coth(v1)**2 - csch(v1)**2, 1))
# True

# sinh(2x) = 2 * sinh(x) * cosh(x)
x = np.array([0.5, 1.0, 1.5])
print(np.allclose(np.sinh(2*x), 2 * np.sinh(x) * np.cosh(x)))
# True

# cosh(2x) = cosh²(x) + sinh²(x)
print(np.allclose(np.cosh(2*x), np.cosh(x)**2 + np.sinh(x)**2))
# True

# arctanh(tanh(x)) = x (for x in domain)
x_range = np.linspace(-2, 2, 5)
print(np.allclose(np.arctanh(np.tanh(x_range)), x_range))
# True

# arccoth(coth(x)) = x (for x != 0)
x_coth = np.array([0.5, 1.0, 1.5, 2.0])
print(np.allclose(arccoth(coth(x_coth)), x_coth))
# True

# Relationship with trigonometric functions: sinh(ix) = i*sin(x)
x = np.array([0.5, 1.0, 1.5])
print(np.allclose(np.sinh(1j*x), 1j*np.sin(x)))
# True

# Relationship with trigonometric functions: cosh(ix) = cos(x)
print(np.allclose(np.cosh(1j*x), np.cos(x)))
# True

##--------------------------##
## Reciprocal Relationships ##
##--------------------------##

# coth(x) * tanh(x) = 1
print(np.allclose(coth(v1) * np.tanh(v1), 1))
# True

# sech(x) * cosh(x) = 1
print(np.allclose(sech(v1) * np.cosh(v1), 1))
# True

# csch(x) * sinh(x) = 1
print(np.allclose(csch(v1) * np.sinh(v1), 1))
# True
