'''
Pandas Series is a one-dimensional labeled array capable of holding any data type (integers, strings, floating point numbers, Python objects, etc.). 
It is similar to a column in a spreadsheet or a SQL table.

Sometimes, can consider it as a dictionary-like structure where each element has a unique label (index).
Or like numpy 1D array with additional features like labels.

################################################

1. Creating a Series: 
   + from a list, dictionary, ndarray or scalar value; 
   + with indexing, MultiLevel Indexed Series

2. Copying a Series: s.copy()
'''

import pandas as pd

#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. Creating a Series -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

#################
## From a list ##
#################

#---------------
## Without index labels, 
## pandas will create a default integer index starting from 0.
#----------------

s = pd.Series(data = [1, 2, 3, 4, 5])

print(s)
# 0    1
# 1    2
# 2    3
# 3    4
# 4    5
# dtype: int64

#----------------
## With custom index labels
#----------------

s = pd.Series(data = [1, 2, 3, 4, 5], index = ['one', 'two', 'three', 'four', 'five'])

print(s)
# one      1
# two      2
# three    3
# four     4
# five     5
# dtype: int64


####################
## From a ndarray ##
####################

import numpy as np

s = pd.Series(data = np.random.rand(5), index = ['a', 'b', 'c', 'd', 'e'])

print(s)
# a    0.503145
# b    0.622401
# c    0.766209
# d    0.962831
# e    0.794495
# dtype: float64


#######################
## From a dictionary ##
#######################

# The keys will be used as index labels, and the values will be the data in the Series.
s = pd.Series(data = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})

print(s)
# a    1
# b    2
# c    3
# d    4
# e    5
# dtype: int64


#########################
## From a scalar value ##
#########################

s = pd.Series(data = 5, index = ['a', 'b', 'c', 'd', 'e'])

print(s)
# a    5
# b    5
# c    5
# d    5
# e    5
# dtype: int64


################################
## Multi-Level Indexed Series ##
################################

# Create a multi-level index object using pd.MultiIndex
multi_index = pd.MultiIndex(
    levels = [
        ['llama', 'cow', 'falcon'], # Level 0 labels
        ['speed', 'weight', 'length'] # Level 1 labels
    ],
    codes = [
        [0, 0, 0, 1, 1, 1, 2, 2, 2], # Integers for each level designating which label at each location
        [0, 1, 2, 0, 1, 2, 0, 1, 2]
    ]
)

# Use the multi-level indexed object to create a Series
s_multi_index = pd.Series([45, 200, 1.2, 30, 250, 1.5, 320, 1, 0.3], index = multi_index)

print(s_multi_index)
# llama   speed      45.0
#         weight    200.0
#         length      1.2
# cow     speed      30.0
#         weight    250.0
#         length      1.5
# falcon  speed     320.0
#         weight      1.0
#         length      0.3
# dtype: float64


#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. Copying a Series ------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_original = pd.Series(data = [10, 20, 30, 40, 50])

s_copy = s_original.copy()  # Creating a copy of the Series
print(s_copy)
# 0    10
# 1    20
# 2    30
# 3    40
# 4    50
# dtype: int64

s_copy_index = s_original.copy(deep = True)  # Creating a deep copy of the Series
print(s_copy_index)
# 0    10
# 1    20
# 2    30
# 3    40
# 4    50
# dtype: int64
