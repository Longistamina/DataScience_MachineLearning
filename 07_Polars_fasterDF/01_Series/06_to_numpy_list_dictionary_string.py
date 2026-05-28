'''
The below methods convert a Polars Series to completely different data types,
such as NumPy array, list, dictionary, or string representation.

NOTE: Because Polars Series DO NOT have custom index labels (they are strictly
1D arrays with positional row numbers), some pandas methods like .to_dict()
or .to_string(index=False) do not have direct 1:1 method equivalents.
Workarounds are provided below.

##########################################

1. .to_numpy()
2. .to_list()
3. Dictionary conversion (Workarounds)
4. String representation (Workarounds)
'''

import polars as pl
import numpy as np


#------------------------------------------------------------------------------------------#
#----------------------------------- Setup Data -------------------------------------------#
#------------------------------------------------------------------------------------------#
'''
Pandas allows mixed types natively (dtype: object).
Polars is strictly typed. To force mixed types, you must explicitly use pl.Object,
though this bypasses Polars' Rust-based performance optimizations and is generally discouraged.
'''

s_mixed = pl.Series("mixed", [1, 2.5, 'three', None, True], dtype=pl.Object)

# Create a numeric Series
np.random.seed(42)  # For reproducibility
s_numeric = pl.Series("numeric", np.random.normal(loc=2, scale=1, size=10)).round(2)
print(s_numeric)
# shape: (10,)
# Series: 'numeric' [f64]
# [
# 	2.5
# 	1.86
# 	2.65
# 	3.52
# 	1.77
# 	1.77
# 	3.58
# 	2.77
# 	1.53
# 	2.54
# ]


#------------------------------------------------------------------------------------------#
#----------------------------------- 1. .to_numpy() ---------------------------------------#
#------------------------------------------------------------------------------------------#

np_mixed = s_mixed.to_numpy()
print(np_mixed) # [1 2.5 'three' None True]
print(type(np_mixed))  # <class 'numpy.ndarray'>

##########################################

np_numeric = s_numeric.to_numpy()
print(np_numeric)  # [2.5  1.86 2.65 3.52 1.77 1.77 3.58 2.77 1.53 2.54]
print(type(np_numeric))  # <class 'numpy.ndarray'>
'''
As we can see, in ndarray, there are no "," separators between elements.
Note: If a Polars numeric Series contains nulls, ``.to_numpy()`` will return an Object array
or raise an error unless you specify how to handle nulls (e.g., filling them first).
'''


#------------------------------------------------------------------------------------------#
#----------------------------------- 2. .to_list() ----------------------------------------#
# -----------------------------------------------------------------------------------------#

list_mixed = s_mixed.to_list()
print(list_mixed)  # [1, 2.5, 'three', None, True]
print(type(list_mixed))  # <class 'list'>

##########################################

list_numeric = s_numeric.to_list()
print(list_numeric) # [2.5, 1.86, 2.65, 3.52, 1.77, 1.77, 3.58, 2.77, 1.53, 2.54]
print(type(list_numeric))  # <class 'list'>
'''
As we can see, in list, there are "," separators between elements.
Polars natively represents missing values as Python `None` in lists.
'''


#------------------------------------------------------------------------------------------#
#----------------------------------- 3. Dictionary Conversion -----------------------------#
# -----------------------------------------------------------------------------------------#
'''
Polars Series DO NOT have a .to_dict() method because they lack an index.
In pandas, s.to_dict() maps the index labels to the values.
'''

###########################################
## Workaround 1: Emulating default integer index (Positional mapping)
###########################################

dict_numeric = dict(enumerate(s_numeric.to_list()))
print(dict_numeric)
# {0: 2.5, 1: 1.86, 2: 2.65, 3: 3.52, 4: 1.77, 5: 1.77, 6: 3.58, 7: 2.77, 8: 1.53, 9: 2.54}

######################################################
## Workaround 2: Key-Value mapping (The Polars Way) ##
######################################################
'''
If you have keys and values, you should use a Polars DataFrame.
DataFrames DO have a .to_dict() method, and you can use standard Python
zip() to create a key-value dictionary.
'''

df_kv = pl.DataFrame({
    "keys": ["a", "b", "c", "d", "e"],
    "values": [0, 3.2, 'three', None, False]
}, strict=False)

# DataFrame .to_dict() returns column-oriented lists (like pandas orient='list')
print(df_kv.to_dict(as_series=False))
# {'keys': ['a', 'b', 'c', 'd', 'e'], 'values': [0, 3.2, 'three', None, False]}

# To get a pandas-like {index: value} dictionary mapping:
dict_indexed = dict(zip(df_kv["keys"], df_kv["values"]))
print(dict_indexed)
# {'a': 0, 'b': 3.2, 'c': 'three', 'd': None, 'e': False}


#------------------------------------------------------------------------------------------#
#----------------------------------- 4. String Representation -----------------------------#
# -----------------------------------------------------------------------------------------#
'''
Polars Series DO NOT have a .to_string() method like pandas.
To get a raw newline-separated string of values (equivalent to pandas' s.to_string(index=False)),
you should cast the Series to pl.String and join the resulting list.
'''

################################################
## Numeric Series to Newline-Separated String ##
################################################

# Cast to string, convert to list, and join with newline
string_numeric = "\n".join(s_numeric.cast(pl.String).to_list())
print(string_numeric)
# 2.5
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
# '2.5\n1.86\n2.65\n3.52\n1.77\n1.77\n3.58\n2.77\n1.53\n2.54'

print(string_numeric.split('\n'))
# ['2.5', '1.86', '2.65', '3.52', '1.77', '1.77', '3.58', '2.77', '1.53', '2.54']

print(type(string_numeric))  # <class 'str'>

####################################
## Standard Polars Representation ##
####################################
'''
If you just want the formatted table string that Polars prints to the console,
you can simply use Python's built-in str() or repr() functions on the Series.
'''

print(str(s_numeric))
# shape: (10,)
# Series: 'numeric' [f64]
# [
# 	2.5
# 	1.86
# 	2.65
# 	3.52
# 	1.77
# 	1.77
# 	3.58
# 	2.77
# 	1.53
# 	2.54
# ]
