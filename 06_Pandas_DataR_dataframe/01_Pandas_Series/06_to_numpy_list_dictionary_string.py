'''
The below methods convert a pandas Series to a completely different data type, 
such as NumPy array, list, dictionary, or string representation.

##########################################

1. .to_numpy()

2. .to_list()

3. .to_dict()

4. .to_string()
'''

import pandas as pd
import numpy as np

# Create a mixed-type Series
s_mixed = pd.Series([1, 2.5, 'three', np.nan, True])

# Create an indexed Series
s_indexed = pd.Series([0, 3.2, 'three', np.nan, False], index=['a', 'b', 'c', 'd', 'e'])

# Create a numeric Series
np.random.seed(42)  # For reproducibility
s_numeric = pd.Series(np.random.normal(loc=2, scale=1, size=10)).round(2)
print(s_numeric)
# 0    2.50
# 1    1.86
# 2    2.65
# 3    3.52
# 4    1.77
# 5    1.77
# 6    3.58
# 7    2.77
# 8    1.53
# 9    2.54
# dtype: float64


#------------------------------------------------------------------------------------------#
#----------------------------------- 1. .to_numpy() ---------------------------------------#
#------------------------------------------------------------------------------------------#

np_mixed = s_mixed.to_numpy(copy=True) # set copy to True to create a copy version
print(np_mixed) # [1 2.5 'three' nan True]
print(type(np_mixed))  # <class 'numpy.ndarray'>

##########################################

np_numeric = s_numeric.to_numpy(copy=True)
print(np_numeric)  # [2.5  1.86 2.65 3.52 1.77 1.77 3.58 2.77 1.53 2.54]
print(type(np_numeric))  # <class 'numpy.ndarray'>

'''
As we can see, in ndarray, there are no "," separators between elements
'''


#------------------------------------------------------------------------------------------#
#----------------------------------- 2. .to_list() ----------------------------------------#
# -----------------------------------------------------------------------------------------#

list_mixed = s_mixed.to_list()
print(list_mixed)  # [1, 2.5, 'three', nan, True]
print(type(list_mixed))  # <class 'list'>

##########################################

list_numeric = s_numeric.to_list()
print(list_numeric) # [2.5, 1.86, 2.65, 3.52, 1.77, 1.77, 3.58, 2.77, 1.53, 2.54]
print(type(list_numeric))  # <class 'list'>

'''
As we can see, in list, there are "," separators between elements
'''


#------------------------------------------------------------------------------------------#
#----------------------------------- 3. .to_dict() ----------------------------------------#
# -----------------------------------------------------------------------------------------#

dict_mixed = s_mixed.to_dict()
print(dict_mixed)  
# {0: 1, 1: 2.5, 2: 'three', 3: nan, 4: True}

###########################################

dict_indexed = s_indexed.to_dict()
print(dict_indexed)
# {'a': 0, 'b': 3.2, 'c': 'three', 'd': nan, 'e': False}

'''
As we can see, the indexes are used as keys in the dictionary,
and the values are the corresponding elements of the Series.
'''


#------------------------------------------------------------------------------------------#
#----------------------------------- 4. .to_string() --------------------------------------#
# -----------------------------------------------------------------------------------------#

string_mixed = s_mixed.to_string(index=False) # set index to False to not show the index
print(string_mixed)
#     1
#   2.5
# three
#   NaN
#  True

print(repr(string_mixed))
# '    1\n  2.5\nthree\n  NaN\n True'

print(string_mixed.split('\n'))
# ['    1', '  2.5', 'three', '  NaN', ' True']

print(type(string_mixed))  # <class 'str'>

############################################

string_numeric = s_numeric.to_string(index=False)
print(string_numeric)
# 2.50
# 1.86
# 2.65
# 3.52
# 1.77
# 1.77
# 3.58
# 2.77
# 1.53
# 2.54

print(repr(string_numeric))
# '2.50\n1.86\n2.65\n3.52\n1.77\n1.77\n3.58\n2.77\n1.53\n2.54'

print(string_numeric.split('\n'))
# ['2.50', '1.86', '2.65', '3.52', '1.77', '1.77', '3.58', '2.77', '1.53', '2.54']

print(type(string_numeric))  # <class 'str'>