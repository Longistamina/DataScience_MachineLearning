'''
The Series.sparse accessor in pandas provides specialized functionality 
for working with sparse data structures.

Sparse Series are designed to efficiently store data 
where a significant portion of values are identical (typically zeros or NaN), 
offering substantial memory savings for such datasets.

###############################

0. Create a Sparse Series

1. Attributes:
   + .sparse.density
   + .sparse.fill_value
   + .sparse.npoints
   + .sparse.sp_values

3. Methods:
   + .sparse.from_coo()
   + .sparse.to_coo()   
'''

import pandas as pd
import numpy as np

#--------------------------------------------------------------------------------------------------------#
#----------------------------------- 0. Create a Sparse Series ------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

s_sparse_int = pd.Series([0, 0, 1, 0, 2, 0, 0, 3], dtype="Sparse[int]")
print(s_sparse_int)
# 0    0
# 1    0
# 2    1
# 3    0
# 4    2
# 5    0
# 6    0
# 7    3
# dtype: Sparse[int64, 0]

s_sparse_float = pd.Series([np.nan, 0.0, 1.5, np.nan, 2.5, 0.0, 0.0, 3.5], dtype="Sparse[float]")
print(s_sparse_float)
# 0    NaN
# 1    0.0
# 2    1.5
# 3    NaN
# 4    2.5
# 5    0.0
# 6    0.0
# 7    3.5
# dtype: Sparse[float64, nan]


#--------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. Attributes --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

s_sparse_int = pd.Series([0, 0, 1, 0, 2, 0, 0, 3], dtype="Sparse[int]")
s_sparse_float = pd.Series([np.nan, 0.0, 1.5, np.nan, 2.5, 0.0, 0.0, 3.5], dtype="Sparse[float]")
s_sparse_nan = pd.Series([np.nan, np.nan, 1.5, np.nan, 2.5, np.nan, np.nan, 3.5], dtype="Sparse[float]")

#####################
## .sparse.density ##
#####################
'''
Density = (Number of non-fill values) / (Total number of values)

fill values: 0, 0.0, np.nan, ...
non-fill values: other values (1, 2, 3, 1.5, 2.5, 3.5, ...)
'''

print(s_sparse_int.sparse.density)   # 0.375 (= 3/8)
print(s_sparse_float.sparse.density) # 0.75  (= 6/8)
print(s_sparse_nan.sparse.density)   # 0.375 (= 3/8)

'''
NOTE: here, the s_sparse_float only treats NaN as sparse value,
      so the density also includes the 0.0 values.

=> USE ONLY ONE TYPE OF SPARSE VALUE (EITHER NaN OR 0.0)
'''

########################
## .sparse.fill_value ##
########################
'''Returns the fill value used in the sparse representation of the Series.'''

print(s_sparse_int.sparse.fill_value)   # 0
print(s_sparse_float.sparse.fill_value) # nan

#####################
## .sparse.npoints ##
#####################
'''The number of non-fill values in the Series.'''

print(s_sparse_int.sparse.npoints)   # 3
print(s_sparse_float.sparse.npoints) # 6
print(s_sparse_nan.sparse.npoints)   # 3

#######################
## .sparse.sp_values ##
#######################
'''The unique non-fill values in the Series.'''

print(s_sparse_int.sparse.sp_values)   # [1 2 3]
print(s_sparse_float.sparse.sp_values) # [0.  1.5 2.5 0.  0.  3.5]
print(s_sparse_nan.sparse.sp_values)   # [1.5 2.5 3.5]


#--------------------------------------------------------------------------------------------------------#
#---------------------------------------- 3. Methods ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

s_sparse_int = pd.Series([0, 0, 1, 0, 2, 0, 0, 3], dtype="Sparse[int]")
s_sparse_float = pd.Series([np.nan, np.nan, 1.5, np.nan, 2.5, np.nan, np.nan, 3.5], dtype="Sparse[float]")

########################
## .sparse.from_coo() ##
########################
'''Create a Series with sparse values from a scipy.sparse.coo_matrix.'''

from scipy import sparse

sparse_matrix = sparse.coo_matrix(
    ([3.0, 1.0, 2.0], ([1, 0, 0], [0, 2, 3])), shape=(3, 4)
)
print(sparse_matrix.todense())
# [[0. 0. 1. 2.]
#  [3. 0. 0. 0.]
#  [0. 0. 0. 0.]]

# Convert the sparse matrix to a sparse Series
sparse_series = pd.Series.sparse.from_coo(sparse_matrix)
print(sparse_series)
# 0  2    1.0
#    3    2.0
# 1  0    3.0
# dtype: Sparse[float64, nan]

'''
0  2   1.0 => row 0, column 2 of the matrix has value 1.0
   3   2.0 => row 0, column 3 of the matrix has value 2.0
1  0   3.0 => row 1, column 0 of the matrix has value 3.0
'''

#######################
## .sparse.to_coo()  ##
#######################
'''Convert a Sparse Series to a scipy.sparse.coo_matrix.'''

s_sparse = pd.Series([3.0, np.nan, 1.0, 3.0, np.nan, np.nan])
s_sparse.index = pd.MultiIndex.from_tuples(
    [
        (1, 2, "a", 0),
        (1, 2, "a", 1),
        (1, 1, "b", 0),
        (1, 1, "b", 1),
        (2, 1, "b", 0),
        (2, 1, "b", 1)
    ],
    names=["A", "B", "C", "D"],
)
s_sparse = s_sparse.astype("Sparse[float]")

print(s_sparse)
# A  B  C  D
# 1  2  a  0    3.0
#          1    NaN
#    1  b  0    1.0
#          1    3.0
# 2  1  b  0    NaN
#          1    NaN
# dtype: Sparse[float64, nan]

# Convert the sparse Series to a sparse matrix
sparse_matrix, rows, columns = s_sparse.sparse.to_coo(
    row_levels=["A", "B"], column_levels=["C", "D"], sort_labels=True
)

print(sparse_matrix.todense())
# [[0. 0. 1. 3.]
#  [3. 0. 0. 0.]
#  [0. 0. 0. 0.]]

'''
         ('a', 0)  ('a', 1)  ('b', 0)  ('b', 1)
(1, 1)     0.0       0.0       1.0       3.0
(1, 2)     3.0       0.0       0.0       0.0
(2, 1)     0.0       0.0       0.0       0.0
'''

print(rows)
# [(1, 1), (1, 2), (2, 1)]

print(columns)
# [('a', 0), ('a', 1), ('b', 0), ('b', 1)]