'''
Polars Series natively support vectorized mathematical and logical operations using standard Python operators.
Unlike pandas, Polars DOES NOT use method aliases like .add(), .sub(), .lt(), .gt() on Series objects.
You simply use the standard operators (+, -, *, /, <, >, ==, etc.).

##--------------------------------------##
1. Mathematical Operations:
    round(),
    + (Addition), - (Subtraction),
    * (Multiplication), / (Division),
    // (Floor Division), % (Modulus),
    ** (Power)

2. Logic Boolean Comparisons:
    < , <= ,
    > , >= ,
    .is_between(lower, upper, closed='both'),
    == , !=
    Boolean to Binary 0/1 (using .cast(pl.Int8))
'''

import numpy as np
import polars as pl

# =========================================================================================
# 1. Mathematical Operations
# =========================================================================================

# Generate a Series of random numbers
np.random.seed(42)  # For reproducibility
s1 = pl.Series("Numbers", np.random.normal(15.6, 5, 10)).round(3)
s2 = pl.Series("Numbers", np.random.normal(20, 5, 10)).round(3)

print(s1.to_list())
# [18.084, 14.909, 18.838, 23.215, 14.429, 14.429, 23.496, 19.437, 13.253, 18.313]

print(s2.to_list())
# [17.683, 17.671, 21.21, 10.434, 11.375, 17.189, 14.936, 21.571, 15.46, 12.938]

##---------##
## round() ##
##---------##

print(s1.round(2).to_list())  # Round to 2 decimal places
# [18.08, 14.91, 18.84, 23.22, 14.43, 14.43, 23.5, 19.44, 13.25, 18.31]

print(s2.round(1).to_list())  # Round to 1 decimal place
# [17.7, 17.7, 21.2, 10.4, 11.4, 17.2, 14.9, 21.6, 15.5, 12.9]

##-------##
##   +   ##
##-------##

print((s1 + 3.).to_list())
# [21.084, 17.909, 21.838, 26.215, 17.429000000000002, 17.429000000000002, 26.496, 22.437, 16.253, 21.313]

print((s1 + s2).to_list())
# [35.766999999999996, 32.58, 40.048, 33.649, 25.804000000000002, 31.618000000000002, 38.432, 41.008, 28.713, 31.250999999999998]

##-------##
##   -   ##
##-------##

print(s1 - 3)
print(s1 - s2)

##-------##
##   *   ##
##-------##

print(s1 * 3)
print(s1 * s2)

##-------##
##   /   ##
##-------##
'''
NOTE: In Polars, the / operator ALWAYS returns a Float64 series,
even if both inputs are integers.
'''

print(s1 / 3)
print(s1 / s2)

##---------##
##   //    ##
##---------##

print(s1 // 3)
print(s1 // s2)

##-------##
##   %   ##
##-------##

print(s1 % 3)
print(s1 % s2)

##--------##
##   **   ##
##--------##

print(s1 ** 3)
print(s1 ** s2)

# =========================================================================================
# 2. Logic Boolean Comparisons
# =========================================================================================
'''With string comparison, it compares lexicographically based on Unicode code points.'''

s1 = pl.Series([10, 20, 30, 40, 50])
s2 = pl.Series([5, 25, 20, 44, 48])
s1_str = pl.Series(['a', 'b', 'c', 'd', 'e'])
s2_str = pl.Series(['a', 'a', 'd', 'f', 'e'])

##-------##
##   <   ##
##-------##

print(s1 < 30)
# shape: (5,)
# Series: '' [bool]
# [
# 	true
# 	true
# 	false
# 	false
# 	false
# ]

print(s1 < s2)
# shape: (5,)
# Series: '' [bool]
# [
# 	false
# 	true
# 	false
# 	true
# 	false
# ]

# print(s1 < s1_str) # Raises InvalidOperationError: cannot compare Int64 with String in Polars
print(s1_str < s2_str)
# shape: (5,)
# Series: '' [bool]
# [
# 	false
# 	false
# 	true
# 	true
# 	false
# ]

##--------##
##   <=   ##
##--------##

print(s1 <= 30)
print(s1 <= s2)
print(s1_str <= s2_str)

##-------##
##   >   ##
##-------##

print(s1 > 30)
print(s1 > s2)
print(s1_str > s2_str)

##--------##
##   >=   ##
##--------##

print(s1 >= 30)
print(s1 >= s2)
print(s1_str >= s2_str)

##---------------##
## .is_between() ##
##---------------##
'''
In pandas this is .between(). In Polars it is .is_between().
closed = "both" (default): [left, right] or left <= x <= right
closed = "none": (left, right) or left < x < right  <-- Note: "none" in Polars is "neither" in pandas
closed = "left": [left, right) or left <= x < right
closed = "right": (left, right] or left < x <= right
'''

print(s1.is_between(20, 40))  # Default closed='both'
# shape: (5,)
# Series: '' [bool]
# [
# 	false
# 	true
# 	true
# 	true
# 	false
# ]

print(s2.is_between(20, 40, closed="none"))
# shape: (5,)
# Series: '' [bool]
# [
# 	false
# 	false
# 	false
# 	false
# 	false
# ]

##-------##
##   ==  ##
##-------##

print(s1 == 30)
print(s1 == s2)
print(s1_str == s2_str)

##--------##
##   !=   ##
##--------##

print(s1 != 30)
print(s1 != s2)
print(s1_str != s2_str)

##---------------------------------------##
## Boolean to Binary 0/1 - .cast(pl.Int8)##
##---------------------------------------##
'''
In pandas, you use .astype(int).
In Polars, you use .cast() with an integer type.
pl.Int8 is the most memory-efficient integer type for 0/1 binary flags.
'''

print((s1 < s2).cast(pl.Int8))
# shape: (5,)
# Series: '' [i8]
# [
# 	0
# 	1
# 	0
# 	1
# 	0
# ]

print(s1 < s2)
# shape: (5,)
# Series: '' [bool]
# [
# 	false
# 	true
# 	false
# 	true
# 	false
# ]
