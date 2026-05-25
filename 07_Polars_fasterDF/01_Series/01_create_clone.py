'''
Polars Series is a one-dimensional labeled array capable of holding any data type
(integers, strings, floating point numbers, Python objects, etc.).

It is similar to a column in a spreadsheet or a SQL table.

Sometimes, can consider it as a dictionary-like structure where each element has a unique label (index).
Or like numpy 1D array with additional features like labels.

NOTE: polars series do not support multi-level index like pandas

################################################

1. Creating a Series:
   + from a list
   + from a ndarray

2. Clone a Series: s.clone()
'''

import polars as pl
import numpy as np


#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. Creating a Series -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

#################
## from a list ##
#################

s = pl.Series(values=[1, 2, 3, 4])
print(s)
# shape: (4,)
# Series: '' [i64]
# [
# 	1
# 	2
# 	3
# 	4
# ]

s = pl.Series(
    name='list_series',
    values=[10, 20, 30, None, 50],
    dtype=pl.Float16,
    nan_to_null=True
)
print(s)
# shape: (5,)
# Series: 'list_series' [f16]
# [
# 	10.0
# 	20.0
# 	30.0
# 	null
# 	50.0
# ]

####################
## from a ndarray ##
####################

np.random.seed(42)
arr = np.random.uniform(20, 30, 10).round(3)
print(arr)
# [23.745 29.507 27.32  25.987 21.56  21.56  20.581 28.662 26.011 27.081]

s = pl.Series(
    name='array_series',
    values=arr,
    dtype=pl.Int16,
    nan_to_null=False
)
print(s)
# shape: (10,)
# Series: 'array_series' [i16]
# [
# 	23
# 	29
# 	27
# 	25
# 	21
# 	21
# 	20
# 	28
# 	26
# 	27
# ]


#-----------------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. Clone a Series ------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''``polars.Series.clone()`` is a cheap operation, it does not truly copy data (still share memory)'''

s_original = pl.Series(values=[10, 20, 30, 40, 50])

s_clone = s_original.clone()
print(s_clone)
# shape: (5,)
# Series: '' [i64]
# [
# 	10
# 	20
# 	30
# 	40
# 	50
# ]

print(np.shares_memory(s_original.to_numpy(), s_clone.to_numpy()))
# True
