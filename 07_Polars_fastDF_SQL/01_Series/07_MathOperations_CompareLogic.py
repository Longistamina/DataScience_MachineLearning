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

import polars as pl
import numpy as np


# =========================================================================================
# 1. Mathematical Operations
# =========================================================================================

# Generate a Series of random numbers
np.random.seed(42)  # For reproducibility
s1 = pl.Series("Numbers", np.random.normal(15.6, 5, 10))
s2 = pl.Series("Numbers", np.random.normal(20, 5, 10))

print(s1)
# shape: (10,)
# Series: 'Numbers' [f64]
# [
# 	18.083571
# 	14.908678
# 	18.838443
# 	23.215149
# 	14.429233
# 	14.429315
# 	23.496064
# 	19.437174
# 	13.252628
# 	18.312800
# ]

print(s2)
# shape: (10,)
# Series: 'Numbers' [f64]
# [
# 	17.682912
# 	17.671351
# 	21.209811
# 	10.433599
# 	11.375411
# 	17.188562
# 	14.935844
# 	21.571237
# 	15.459880
# 	12.938481
# ]

##---------##
## round() ##
##---------##

print(s1.round(2))  # Round to 2 decimal places
# shape: (10,)
# Series: 'Numbers' [f64]
# [
# 	18.08
# 	14.91
# 	18.84
# 	23.22
# 	14.43
# 	14.43
# 	23.5
# 	19.44
# 	13.25
# 	18.31
# ]

print(s2.round(1))  # Round to 1 decimal place
# shape: (10,)
# Series: 'Numbers' [f64]
# [
# 	17.7
# 	17.7
# 	21.2
# 	10.4
# 	11.4
# 	17.2
# 	14.9
# 	21.6
# 	15.5
# 	12.9
# ]

##-------##
##   +   ##
##-------##

print(s1 + 3)
# shape: (10,)
# Series: 'Numbers' [f64]
# [
# 	21.083571
# 	17.908678
# ...

print(s1 + s2)
# shape: (10,)
# Series: 'Numbers' [f64]
# [
# 	35.766483
# 	32.580029
# ...

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
