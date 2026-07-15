'''
1. Series.dtype: Data type of the Series

2. Some important Series attributes: .shape, .flags

3. ``s.name`` and ``s.rename()``: getting and setting name for a series
'''

import polars as pl
import numpy as np


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. Series.dtype  -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''Dtype is the data type of the Series, which can be checked using the .dtype attribute.'''

s_nums = pl.Series(values=[1, 2, 3, 4, 5])
print(s_nums.dtype)  # Output: Int64

s_floats = pl.Series(values=[1.0, 2.0, 3.0, 4.0, 5.0])
print(s_floats.dtype)  # Output: Float64

s_strings = pl.Series(values=['a', 'b', 'c', 'd', 'e'])
print(s_strings.dtype)  # Output: String

s_mixed_string = pl.Series(values=[1, 'a', 3.0], strict=False)
print(s_mixed_string.dtype)  # Output: String

s_mixed_None = pl.Series(values=[1, None, 3.0], strict=False)
print(s_mixed_None.dtype)  # Output: Float64

s_mixed_Null = pl.Series(values=[1, pl.Null, 3.0], strict=False)
print(s_mixed_Null.dtype) # Output: Object

s_mixed_nan = pl.Series(values=[1, np.nan, 3.0], strict=False)
print(s_mixed_nan.dtype)  # Output: Float64


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 2. Some important Series attributes ----------------------------------#
#--------------------------------------------------------------------------------------------------------------#

s = pl.Series("a", [1, 2, 3])

############
## .shape ##
############
'''Number of elements the series has'''

print(s.shape)
# (3,)


############
## .flags ##
############
'''
Get flags that are set on the Series.
Telling whether the series are sorted in ascending or descending order, or not sorted yet
'''

print(s.flags)
# {'SORTED_ASC': False, 'SORTED_DESC': False}


#----------------------------------------------------------------------------------------------------------------#
#------------------ 3. ``s.name`` and ``s.rename()``: getting and setting name for a series ---------------------#
#----------------------------------------------------------------------------------------------------------------#

s = pl.Series("a", [1.2, 2.3, 3.4])

###########
## .name ##
###########
'''The ``.name`` attribute allows you to get the name of the Series.'''

print(s.name)
# a
'''Get series' name'''

###############
## .rename() ##
###############
'''
Use ``.rename()`` to set new name for a series

NOTE: it's an out-place method, so it does not modify the name of the current series
-> Use another variable to store the new renamed series
'''

s_renamed = s.rename("My Series")
print(s_renamed.name)
