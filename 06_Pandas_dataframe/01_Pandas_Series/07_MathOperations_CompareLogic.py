'''
Pandas Series also support various vectorized operations similar to NumPy arrays.
These operations can be performed on Series objects, allowing for efficient data manipulation.

##########################################

1. Mathematical Operations: 
   round(), 
   + add(), - sub(), 
   * mul(), / div(), 
   // floordiv(), % mod(), 
   ** pow()

2. Logic Boolean Comparisons: 
   < lt(), <= le(), 
   > gt(), >= ge(), 
   between(left, right, inclusive='both'), 
   == eq(), != ne()
   Boolean to Binary 0/1 (using astype(int))
'''

import pandas as pd
import numpy as np

#--------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. Mathematical Operations -------------------------------------#
#--------------------------------------------------------------------------------------------------------#

# Generate a Series of random numbers

np.random.seed(42)  # For reproducibility

s1 = pd.Series(np.random.normal(15.6, 5, 10), name='Numbers') # Normal distribution with mean=15.6, std=2, size=10
s2 = pd.Series(np.random.normal(20, 5, 10), name='Numbers') # Normal distribution with mean=20, std=2, size=10

print(s1)
# 0    18.083571
# 1    14.908678
# 2    18.838443
# 3    23.215149
# 4    14.429233
# 5    14.429315
# 6    23.496064
# 7    19.437174
# 8    13.252628
# 9    18.312800
# Name: Numbers, dtype: float64

print(s2)
# 0    17.682912
# 1    17.671351
# 2    21.209811
# 3    10.433599
# 4    11.375411
# 5    17.188562
# 6    14.935844
# 7    21.571237
# 8    15.459880
# 9    12.938481
# Name: Numbers, dtype: float64


#############
## round() ##
#############

print(s1.round(2))  # Round to 2 decimal places
# 0    18.08
# 1    14.91
# 2    18.84
# 3    23.22
# 4    14.43
# 5    14.43

print(s2.round(1))  # Round to 1 decimal place
# 0    17.7
# 1    17.7
# 2    21.2
# 3    10.4
# 4    11.4
# 5    17.2


#############
## + add() ##
#############

print(s1 + 3) # s1.add(3)
# 0    21.083571
# 1    17.908678
# 2    21.838443
# 3    26.215149
# 4    17.429233
# 5    17.429315

print(s1 + s2) # s1.add(s2)
# 0    35.766482
# 1    32.580030
# 2    40.048254
# 3    33.648748
# 4    25.804644
# 5    31.617878


#############
## - sub() ##
#############

print(s1 - 3) # s2.sub(3)
# 0    15.083571
# 1    11.908678
# 2    15.838443
# 3    20.215149
# 4    11.429233
# 5    11.429315

print(s1 - s2) # s1.sub(s2)
# 0     0.400659
# 1    -2.762673
# 2    -2.371369
# 3    12.781551
# 4     3.053822


#############
## * mul() ##
#############

print(s1 * 3) # s1.mul(3)
# 0    54.250712
# 1    44.726035
# 2    56.515328
# 3    69.645448
# 4    43.287699
# 5    43.287946

print(s1 * s2) # s1.mul(s2)
# 0    319.770182
# 1    263.456494
# 2    399.559816
# 3    242.217553
# 4    164.138455


#############
## / div() ##
#############

print(s1 / 3) # s1.div(3)
# 0    6.027857
# 1    4.969559
# 2    6.279481
# 3    7.738383
# 4    4.809744
# 5    4.809772

print(s1 / s2) # s1.div(s2)
# 0    1.022658
# 1    0.843664
# 2    0.888195
# 3    2.225038
# 4    1.268458


###################
## // floordiv() ##
###################

print(s1 // 3) # s1.floordiv(3)
# 0    6.0
# 1    4.0
# 2    6.0
# 3    7.0
# 4    4.0

print(s1 // s2) # s1.floordiv(s2)
# 0    1.0
# 1    0.0
# 2    0.0
# 3    2.0
# 4    1.0


#############
## % mod() ##
#############

print(s1 % 3) # s1.mod(3)
# 0    0.083571
# 1    2.908678
# 2    0.838443
# 3    2.215149
# 4    2.429233

print(s1 % s2) # s1.mod(s2)
# 0     0.400659
# 1    14.908678
# 2    18.838443
# 3     2.347952
# 4     3.053822


##############
## ** pow() ##
##############

print(s1 ** 3) # s1.pow(3)
# 0     5913.608507
# 1     3313.732505
# 2     6685.516961
# 3    12511.645825
# 4     3004.206286

print(s1 ** s2) # s1.pow(s2)
# 0    1.707832e+22
# 1    5.448229e+20
# 2    1.105259e+27
# 3    1.777918e+14
# 4    1.537688e+1


#-------------------------------------------------------------------------------------------------------#
#--------------------------------------- 2. Logic Boolean Comparisons ----------------------------------#
#-------------------------------------------------------------------------------------------------------#

s1 = pd.Series([10, 20, 30, 40, 50])
s2 = pd.Series([5, 25, 20, 44, 48])

s1_str = pd.Series(['a', 'b', 'c', 'd', 'e'])
s2_str = pd.Series(['a', 'a', 'd', 'f', 'e'])

'''With string comparison, it compares lexicographically based on Unicode code points.'''

############
## < lt() ##
############

print(s1 < 30) # s1.lt(30)
# 0     True
# 1     True
# 2    False
# 3    False
# 4    False
# dtype: bool

print(s1 < s2) # s1.lt(s2)
# 0    False
# 1     True
# 2    False
# 3     True
# 4    False
# dtype: bool

print(s1 < s1_str) # ERROR

print(s1_str < s2_str) # s1_str.lt(s2_str)
# 0    False
# 1    False
# 2     True
# 3     True
# 4    False


#############
## <= le() ##
#############

print(s1 <= 30) # s1.le(30)
# 0     True
# 1     True
# 2     True
# 3    False
# 4    False
# dtype: bool

print(s1 <= s2) # s1.le(s2)
# 0    False
# 1     True
# 2    False
# 3     True
# 4    False

print(s1 <= s1_str) # ERROR

print(s1_str <= s2_str) # s1_str.le(s2_str)
# 0     True
# 1    False
# 2     True
# 3     True
# 4     True
# dtype: bool


############
## > gt() ##
############

print(s1 > 30) # s1.gt(30)
# 0    False
# 1    False
# 2    False
# 3     True
# 4     True
# dtype: bool

print(s1 > s2) # s1.gt(s2)
# 0     True
# 1    False
# 2     True
# 3    False
# 4     True
# dtype: bool

print(s1 > s1_str) # ERROR

print(s1_str > s2_str) # s1_str.gt(s2_str)
# 0    False
# 1     True
# 2    False
# 3    False
# 4    False
# dtype: bool


#############
## >= ge() ##
#############

print(s1 >= 30) # s1.ge(30)
# 0    False
# 1    False
# 2     True
# 3     True
# 4     True
# dtype: bool

print(s1 >= s2) # s1.ge(s2)
# 0     True
# 1    False
# 2     True
# 3    False
# 4     True
# dtype: bool

print(s1 >= s1_str) # ERROR

print(s1_str >= s2_str) # s1_str.ge(s2_str)
# 0     True
# 1     True
# 2    False
# 3    False
# 4     True
# dtype: bool


###############
## between() ##
###############
'''
inclusive = "both" (default): [left, right] or left <= x <= right
inclusive = "neither": (left, right) or left < x < right
inclusive = "left": [left, right) or left <= x < right
inclusive = "right": (left, right] or left < x <= right
'''

print(s1.between(20, 40))  # Default inclusive='both'
# 0    False
# 1    False
# 2    False
# 3     True
# 4    False
# 5    False

print(s2.between(20, 40, inclusive='neither'))
# 0    False
# 1    False
# 2     True
# 3    False
# 4    False
# 5    False

 
#############
## == eq() ##
#############

print(s1 == 30) # s1.eq(30)
# 0    False
# 1    False
# 2     True
# 3    False
# 4    False
# dtype: bool

print(s1 == s2) # s1.eq(s2)
# 0    False
# 1    False
# 2    False
# 3    False
# 4    False
# dtype: bool

print(s1 == s1_str) # ERROR

print(s1_str == s2_str) # s1_str.eq(s2_str)
# 0     True
# 1    False
# 2    False
# 3    False
# 4     True
# dtype: bool


#############
## != ne() ##
#############

print(s1 != 30) # s1.ne(30)
# 0     True
# 1     True
# 2    False
# 3     True
# 4     True
# dtype: bool

print(s1 != s2) # s1.ne(s2)
# 0    True
# 1    True
# 2    True
# 3    True
# 4    True
# dtype: bool

print(s1 != s1_str) # ERROR

print(s1_str != s2_str) # s1_str.ne(s2_str)
# 0    False
# 1     True
# 2     True
# 3     True
# 4    False
# dtype: bool


#########################################
## Boolean to Binary 0/1 - astype(int) ##
#########################################

s1.lt(s2).astype(int)  # Convert boolean to binary 0/1
# 0    0
# 1    1
# 2    0
# 3    1
# 4    0
# dtype: int64

s1.lt(s2)
# 0    False
# 1     True
# 2    False
# 3     True
# 4    False
# dtype: bool