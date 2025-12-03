'''
1. Series.dtype: Data type of the Series

2. Some important Series attributes: .index, .values, .shape, .size, .ndim, .is_unique, .hasnans, .empty.

3. 'name' attribute: setting and getting the name of the Series.
'''

import pandas as pd

#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. Series.dtype  -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

# Dtype is the data type of the Series, which can be checked using the .dtype attribute.

s_nums = pd.Series(data = [1, 2, 3, 4, 5])
print(s_nums.dtype)  # Output: int64

s_floats = pd.Series(data = [1.0, 2.0, 3.0, 4.0, 5.0])
print(s_floats.dtype)  # Output: float64

s_strings = pd.Series(data = ['a', 'b', 'c', 'd', 'e'])
print(s_strings.dtype)  # Output: object

s_mixed_string = pd.Series(data = [1, 'a', 3.0])
print(s_mixed_string.dtype)  # Output: object

s_mixed_None = pd.Series(data = [1, None, 3.0])
print(s_mixed_None.dtype)  # Output: float64

s_mixed_NA = pd.Series(data = [1, pd.NA, 3.0])
print(s_mixed_NA.dtype)  # Output: object

import numpy as np
s_mixed_nan = pd.Series(data = [1, np.nan, 3.0])
print(s_mixed_nan.dtype)  # Output: float64


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. Some important Series attributes ---------------------------------#
#--------------------------------------------------------------------------------------------------------------#

############
## .index ##
############

# .index: Returns the index labels of the Series. ##
s = pd.Series(data = [1, 2, 3, 4, 5], index = ['a', 'b', 'c', 'd', 'e'])
print(s.index)
# Index(['a', 'b', 'c', 'd', 'e'], dtype='object')


#############
## .values ##
#############

# .values: Returns the values of the Series as a numpy array
s = pd.Series(data = [1, 2, 3, 4, 5], index = ['a', 'b', 'c', 'd', 'e'])
print(s.values)
# [1 2 3 4 5]

print(type(s.values))
# <class 'numpy.ndarray'>


############
## .shape ##
############

# .shape: Returns a tuple representing the dimensions of the Series (number of elements).
s = pd.Series(data = [1, 2, 3, 4, 5], index = ['a', 'b', 'c', 'd', 'e'])
print(s.shape)
# (5,)


###########
## .size ##
###########

# .size: Returns the number of elements in the Series.
s = pd.Series(data = [1, 2, 3, 4, 5], index = ['a', 'b', 'c', 'd', 'e'])
print(s.size)
# 5


###########
## .ndim ##
###########

# .ndim: Returns the number of dimensions of the Series (always 1 for a Series).
s = pd.Series(data = [1, 2, 3, 4, 5], index = ['a', 'b', 'c', 'd', 'e'])
print(s.ndim)
# 1


################
## .is_unique ##
################

# .is_unique: Returns True if all elements in the Series are unique, otherwise False.

s_unique = pd.Series(data = [1, 2, 3, 4, 5])
print(s_unique.is_unique)
# True

s_not_unique = pd.Series(data = ["a", "b", "c", "a", "e"])
print(s_not_unique.is_unique)
# False


##############
## .hasnans ##
##############

# .hasnans: Returns True if the Series contains any NaN (Not a Number) values, otherwise False.
s_with_nan = pd.Series(data = [1, 2, np.nan, 4, 5])
s_with_NA = pd.Series(data = [1, 2, pd.NA, 4, 5])
s_no_misisng = pd.Series(data = [1, 2, 3, 4, 5])

print(s_with_nan.hasnans) # True
print(s_with_NA.hasnans) # True
print(s_no_misisng.hasnans) # False


############
## .empty ##
############

# .empty: Returns True if the Series is empty (contains no elements), otherwise False.
s_empty = pd.Series(dtype='float64')
s_not_empty = pd.Series(data = [1, 2, 3, 4, 5])

print(s_empty.empty)  # True
print(s_not_empty.empty)  # False


#----------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 3. 'name' attribute ---------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

# The 'name' attribute allows you to set or get the name of the Series.

s = pd.Series(data = [1, 2, 3, 4, 5], index = ['a', 'b', 'c', 'd', 'e'])

# Get the default name of the Series (None)
print(s.name)  # Output: None

# Setting the name of a Series
s.name = 'My Series'

print(s.name)  # Output: My Series

print(s)
# a    1
# b    2
# c    3
# d    4
# e    5
# Name: My Series, dtype: int64
