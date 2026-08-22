'''
1. np.angle(): returns the angle (phase) of the complex argument.

2. np.real(): returns the real part of the complex argument.

3. np.imag(): returns the imaginary part of the complex argument.

4. np.conj() or np.conjugate(): returns the complex conjugate, element-wise.
'''

import numpy as np

np.random.seed(5)
v1 = np.random.uniform(-5, 5, 5) + 1j * np.random.uniform(-5, 5, 5)
# array([-2.78006829+1.11743863j,  3.70732306+2.65907856j,
#        -2.93280845+0.18417988j,  4.18610908-2.03199498j,
#        -0.11588811-3.12278771j])

np.random.seed(5)
v2 = np.random.uniform(-3, 3, 5) + 1j * np.random.uniform(-3, 3, 5)
# array([-1.66804097+0.67046318j,  2.22439384+1.59544714j,
#        -1.75968507+0.11050793j,  2.51166545-1.21919699j,
#        -0.06953287-1.87367263j])

np.random.seed(6)
M1 = np.random.uniform(-4, 4, (2, 3)) + 1j * np.random.uniform(-4, 4, (2, 3))
M2 = np.random.uniform(-2, 2, (2, 3)) + 1j * np.random.uniform(-2, 2, (2, 3))

print(M1)
# [[ 3.14288121+0.2385389j  -1.34416156-0.64954057j  2.56983298-1.31673721j]
#  [-3.66642699+0.98015546j -3.13874656-0.49486859j  0.76041651+1.88705685j]]

print(M2)
# [[ 0.07214565+1.50507062j  0.3154344 +1.29503773j  0.58142038-1.78210197j]
#  [ 1.96089709+0.87454895j  1.27943279+1.20868225j -0.34719626+0.94562658j]]


# =========================================================================================
# 1. np.angle()
# =========================================================================================
'''
np.angle() returns the angle (phase) of the complex argument.
The angle is in radians by default, but can be returned in degrees with deg=True.
=> For a complex number z = x + yj, angle(z) = arctan2(y, x)
'''

print(np.angle(v1))
# [ 2.75940941  0.62220977  3.07887518 -0.45191068 -1.60788977]

print(np.angle(v1, deg=True))
# [158.10251338  35.64999373 176.40655366 -25.89257472 -92.12529788]

print(np.angle(M1))
# [[ 0.07575292 -2.69144999 -0.47350439]
#  [ 2.88036864 -2.98521552  1.18773715]]

print(np.angle(M1, deg=True))
# [[   4.34032275 -154.20872532  -27.12980325]
#  [ 165.03296674 -171.04025019   68.05232569]]

# Check: angle is arctan2(imag, real)

print(np.arctan2(v1.imag, v1.real))
# [ 2.75940941  0.62220977  3.07887518 -0.45191068 -1.60788977]


# =========================================================================================
# 2. np.real()
# =========================================================================================
'''
np.real() returns the real part of the complex argument.
=> For a complex number z = x + yj, real(z) = x
'''

print(np.real(v1))
# [-2.78006829  3.70732306 -2.93280845  4.18610908 -0.11588811]

print(np.real(M1))
# [[ 3.14288121 -1.34416156  2.56983298]
#  [-3.66642699 -3.13874656  0.76041651]]

# Can also use the .real attribute
print(v1.real)
# [-2.78006829  3.70732306 -2.93280845  4.18610908 -0.11588811]

# Works with real numbers too
real_array = np.array([1, 2, 3, 4, 5])
print(np.real(real_array))
# [1 2 3 4 5]


# =========================================================================================
# 3. np.imag()
# =========================================================================================
'''
np.imag() returns the imaginary part of the complex argument.
=> For a complex number z = x + yj, imag(z) = y
'''

print(np.imag(v1))
# [ 1.11743863  2.65907856  0.18417988 -2.03199498 -3.12278771]

print(np.imag(M1))
# [[ 0.2385389  -0.64954057 -1.31673721]
#  [ 0.98015546 -0.49486859  1.88705685]]

# Can also use the .imag attribute
print(v1.imag)
# [ 1.11743863  2.65907856  0.18417988 -2.03199498 -3.12278771]

# Works with real numbers too (returns zero)
real_array = np.array([1, 2, 3, 4, 5])
print(np.imag(real_array))
# [0 0 0 0 0]


# =========================================================================================
# 4. np.conj() or np.conjugate()
# =========================================================================================
'''
np.conj() or np.conjugate() returns the complex conjugate, element-wise.
=> For a complex number z = x + yj, conj(z) = x - yj
The conjugate reflects the complex number across the real axis.
'''

print(np.conj(v1))
# [-2.78006829-1.11743863j  3.70732306-2.65907856j -2.93280845-0.18417988j
#   4.18610908+2.03199498j -0.11588811+3.12278771j]

print(np.conjugate(v1))
# [-2.78006829-1.11743863j  3.70732306-2.65907856j -2.93280845-0.18417988j
#   4.18610908+2.03199498j -0.11588811+3.12278771j]

print(np.conj(M1))
# [[ 3.14288121-0.2385389j  -1.34416156+0.64954057j  2.56983298+1.31673721j]
#  [-3.66642699-0.98015546j -3.13874656+0.49486859j  0.76041651-1.88705685j]]

# Can also use the .conj() method
print(v1.conj())
# [-2.78006829-1.11743863j  3.70732306-2.65907856j -2.93280845-0.18417988j
#   4.18610908+2.03199498j -0.11588811+3.12278771j]

# Check: real part stays same, imaginary part changes sign

print(np.real(np.conj(v1)) == np.real(v1))
# [ True  True  True  True  True]

print(np.imag(np.conj(v1)) == -np.imag(v1))
# [ True  True  True  True  True]
