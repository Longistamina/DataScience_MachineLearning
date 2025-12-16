'''
1. arr.tolist(): Converts a NumPy array to a Python list.

2. tuple(arr): Converts a NumPy array to a Python tuple.

3. set(arr): Converts a NumPy array to a Python set.

4. pd.Series(arr): Converts a NumPy array to a Pandas Series.
'''

import numpy as np
import pandas as pd

np.random.seed(0)
vector = np.random.uniform(0, 11, 7).round(2)

print(vector)
# [6.04 7.87 6.63 5.99 4.66 7.1  4.81]


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 1. arr.tolist() -------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

print(vector.tolist())
# [6.04, 7.87, 6.63, 5.99, 4.66, 7.1, 4.81]

list_vector = vector.tolist()
print(type(list_vector)) # <class 'list'>
print(list_vector)       # [6.04, 7.87, 6.63, 5.99, 4.66, 7.1, 4.81]


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2. tuple(arr) ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

print(tuple(vector))
# (np.float64(6.04), np.float64(7.87), np.float64(6.63), np.float64(5.99), np.float64(4.66), np.float64(7.1), np.float64(4.81))

tuple_vector = tuple(vector)
print(type(tuple_vector)) # <class 'tuple'>
print(tuple_vector)       # (np.float64(6.04), np.float64(7.87), np.float64(6.63), np.float64(5.99), np.float64(4.66), np.float64(7.1), np.float64(4.81))


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 3. set(arr) -----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

print(set(vector))
# {np.float64(4.66), np.float64(5.99), np.float64(6.63), np.float64(6.04), np.float64(7.87), np.float64(7.1), np.float64(4.81)}

set_vector = set(vector)
print(type(set_vector)) # <class 'set'>
print(set_vector)       # {np.float64(4.66), np.float64(5.99), np.float64(6.63), np.float64(6.04), np.float64(7.87), np.float64(7.1), np.float64(4.81)}

'''NOTE: Set will remove duplicates if there are any.'''


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 4. pd.Series(arr) -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

print(pd.Series(vector))
# 0    6.04
# 1    7.87
# 2    6.63
# 3    5.99
# 4    4.66
# 5    7.10
# 6    4.81
# dtype: float64

series_vector = pd.Series(vector)
print(type(series_vector)) # <class 'pandas.core.series.Series'>
print(series_vector)
# 0    6.04
# 1    7.87
# 2    6.63
# 3    5.99
# 4    4.66
# 5    7.10
# 6    4.81
# dtype: float64