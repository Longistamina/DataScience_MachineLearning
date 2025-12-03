'''
1. Ranking and Sorting methods
    + .rank() 
    + .sort_values(), .sort_index(), .argsort() 
    

2. N-Largest and N-Smallest methods
   + .nlargest()
   + .nsmallest()
'''

import numpy as np
import pandas as pd

s_demo = pd.Series([5.8, 4.6, 2, np.nan, 14, 4.6, 25.2, np.nan, 9.3, 10.5])


#----------------------------------------------------------------------------------------------------------------#
#------------------------------------- 1. Ranking and Sorting methods -------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

#############
## .rank() ##
#############
# .rank() returns the ranks of the values in the Series, with ties getting the average rank.
print(s_demo.rank())
# 0    4.0
# 1    2.5
# 2    1.0
# 3    NaN
# 4    7.0
# 5    2.5
# 6    8.0
# 7    NaN
# 8    5.0
# 9    6.0

'''
method{"average", "min", "max", "first", "dense"}, default "average"

How to rank the group of records that have the same value (i.e. ties):
+ average: average rank of the group
+ min: lowest rank in the group
+ max: highest rank in the group
+ first: ranks assigned in order they appear in the array
+ dense: like 'min', but rank always increases by 1 between groups.

Default is "average", which is the most common method used for ranking.
'''

print(s_demo.rank(method = 'min'))
# 0    4.0
# 1    2.0
# 2    1.0
# 3    NaN
# 4    7.0
# 5    2.0
# 6    8.0
# 7    NaN
# 8    5.0
# 9    6.0

print(s_demo.rank(method = 'max'))
# 0    4.0
# 1    3.0
# 2    1.0
# 3    NaN
# 4    7.0
# 5    3.0
# 6    8.0
# 7    NaN
# 8    5.0
# 9    6.0
# dtype: float64


####################
## .sort_values() ##
####################
# .sort_values() sorts the values in the Series in ascending order by default.
print(s_demo.sort_values())
# 2     2.0
# 1     4.6
# 5     4.6
# 0     5.8
# 8     9.3
# 9    10.5
# 4    14.0
# 6    25.2
# 3     NaN
# 7     NaN
# dtype: float64

print(s_demo.sort_values(ascending=False))
# 6    25.2
# 4    14.0
# 9    10.5
# 8     9.3
# 0     5.8
# 1     4.6
# 5     4.6
# 2     2.0
# 3     NaN
# 7     NaN
# dtype: float64


###################
## .sort_index() ##
###################
# .sort_index() sorts the Series by its index in ascending order by default.
s_demo_indexed = pd.Series([5.8, 4.6, 2, 14, 4.6, 25.2],
                           index = [3, 1, 0, 4, 5, 2])

print(s_demo_indexed)
# 3     5.8
# 1     4.6
# 0     2.0
# 4    14.0
# 5     4.6
# 2    25.2
# dtype: float64

# .sort_index() sorts the Series by its index in ascending order by default.
print(s_demo_indexed.sort_index())
# 0     2.0
# 1     4.6
# 2    25.2
# 3     5.8
# 4    14.0
# 5     4.6
# dtype: float64

# .sort_index() sorts the Series by its index in descending order.
print(s_demo_indexed.sort_index(ascending=False))
# 5     4.6
# 4    14.0
# 3     5.8
# 2    25.2
# 1     4.6
# 0     2.0
# dtype: float64


################
## .argsort() ##
################
s_demo_default_index = pd.Series([5.8, 4.6, 2, 14, 4.6, 25.2]) 

# .argsort() returns the indices that would sort the Series in ascending order.
print(s_demo_default_index.argsort())
# 0    2 (index of value 2)
# 1    1 (index of value 4.6)
# 2    4 (index of value 4.6 duplicate)
# 3    0 (index of value 5.8)
# 4    3 (index of value 14)
# 5    5 (index of value 25.2)

'''
For all the sorting and ranking methods, if the data is string or object type,
=> the sorting is done lexicographically based on Unicode code points.
=> The sorting is case-sensitive, meaning uppercase letters come before lowercase letters.
For example, 'A' < 'a', 'B' < 'b', etc.
This means that 'A' will be sorted before 'a', and 'B' will be sorted before 'b'.
This behavior is consistent with the default sorting behavior in Python.
This is important to keep in mind when working with string data, as it can affect the order of the sorted values.
'''

#----------------------------------------------------------------------------------------------------------------#
#------------------------------------- 2. N-Largest and N-Smallest methods --------------------------------------#
#----------------------------------------------------------------------------------------------------------------#
#################
## .nlargest() ##
#################
# .nlargest(n) returns the n largest values in the Series.
print(s_demo_default_index.nlargest(3))
# 5    25.2
# 3    14.0
# 0     5.8
# dtype: float64


##################
## .nsmallest() ##
##################
# .nsmallest(n) returns the n smallest values in the Series.
print(s_demo_default_index.nsmallest(3))
# 2    2.0
# 1    4.6
# 4    4.6
# dtype: float64