'''
dr.distinct() function in DataR is used to filter out duplicate rows from a DataFrame, 
returning only unique rows based on specified columns. 

It is similar to the SQL DISTINCT keyword and is useful for data cleaning 
and ensuring that analyses are performed on unique data points.
'''

import datar.all as dr
from datar import f
import numpy as np

########################

np.random.seed(42)

tb_duplicate = dr.tibble(
  x = dr.sample(range(10), 100, replace=True),
  y = dr.sample(range(10), 100, replace=True)
)

print(
    tb_duplicate
    >> dr.slice_head(n=10)
)
#         x       y
#   <int64> <int64>
# 0       6       1
# 1       3       0
# 2       7       6
# 3       4       6
# 4       6       7
# 5       9       4
# 6       2       2
# 7       6       7
# 8       7       5
# 9       4       2
'''
As you can see, there are some duplicate values in column 'x' (e.g., 6, 7, 4) and
'''

########################################################################
##                  Use dr.distinct(f.col) function                   ##
########################################################################

print(
    tb_duplicate
    >> dr.distinct(f.x)  # Unique values in column 'x'
)
# 0        6
# 1        3
# 2        7
# 3        4
# 5        9
# 6        2
# 14       5
# 16       1
# 21       0
# 24       8
'''Many duplicate values in column 'x' are removed, and only unique values are kept (from 0 - 9)'''

print(
    tb_duplicate
    >> dr.distinct(f.y)  # Unique combinations of 'x'
    >> dr.pull() # Extract the 'y' column as a Series
)
# 0     1
# 1     0
# 2     6
# 4     7
# 5     4
# 6     2
# 8     5
# 16    9
# 19    8
# 25    3
# Name: y, dtype: int64
'''The same for column 'y', only unique values are kept (from 0 - 9)'''

########################################################################
##          Use dr.distinct(f.col, _keep_all=True) function           ##
########################################################################

print(
    tb_duplicate
    >> dr.distinct(f.x, _keep_all=True)  # Unique values in column 'x', keep all columns
)
#          x       y
#    <int64> <int64>
# 0        6       1
# 1        3       0
# 2        7       6
# 3        4       6
# 5        9       4
# 6        2       2
# 14       5       0
# 16       1       9
# 21       0       9
# 24       8       0
'''Only unique values in column 'x' are kept, but all columns are retained in the output DataFrame.'''

print(
    tb_duplicate
    >> dr.distinct(f.y, _keep_all=True)  # Unique values in column 'y', keep all columns
)
#          x       y
#    <int64> <int64>
# 0        6       1
# 1        3       0
# 2        7       6
# 4        6       7
# 5        9       4
# 6        2       2
# 8        7       5
# 16       1       9
# 19       1       8
# 25       0       3