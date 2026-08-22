'''
1. Ranking and Sorting methods
+ .rank()
+ .sort() (equivalent to pandas' .sort_values())
+ .arg_sort() (equivalent to pandas' .argsort())
+ NOTE: .sort_index() does not exist in Polars because Series lack custom indices.

2. N-Largest and N-Smallest methods
+ .sort(descending=True).head(n) (equivalent to pandas' .nlargest())
+ .sort().head(n) (equivalent to pandas' .nsmallest())
'''

import polars as pl

s_demo = pl.Series([5.8, 4.6, 2.0, None, 14.0, 4.6, 25.2, None, 9.3, 10.5])


# =========================================================================================
# 1. Ranking and Sorting methods
# =========================================================================================

##---------##
## .rank() ##
##---------##
'''
.rank() returns the ranks of the values in the Series.
Polars uses snake_case and supports the following methods:
"average" (default), "min", "max", "dense", "ordinal" (equivalent to pandas' "first").
'''

print(s_demo.rank())
# shape: (10,)
# Series: '' [f64]
# [
# 	4.0
# 	2.5
# 	1.0
# 	null
# 	7.0
# 	2.5
# 	8.0
# 	null
# 	5.0
# 	6.0
# ]

print(s_demo.rank(method="min"))
# shape: (10,)
# Series: '' [u32]
# [
# 	4
# 	2
# 	1
# 	null
# 	7
# 	2
# 	8
# 	null
# 	5
# 	6
# ]

print(s_demo.rank(method="ordinal")) # Equivalent to pandas' method="first"
# shape: (10,)
# Series: '' [u32]
# [
# 	4
# 	2
# 	1
# 	null
# 	7
# 	3
# 	8
# 	null
# 	5
# 	6
# ]

##---------##
## .sort() ##
##---------##
'''
In Pandas, you use .sort_values(). In Polars, you simply use .sort().
By default, it sorts in ascending order.
``null`` values are always on the top.
'''

print(s_demo.sort()) # Ascending
# shape: (10,)
# Series: '' [f64]
# [
# 	null
# 	null
# 	2.0
# 	4.6
# 	4.6
# 	5.8
# 	9.3
# 	10.5
# 	14.0
# 	25.2
# ]

print(s_demo.sort(descending=True)) # Descending
# shape: (10,)
# Series: '' [f64]
# [
# 	null
# 	null
# 	25.2
# 	14.0
# 	10.5
# 	9.3
# 	5.8
# 	4.6
# 	4.6
# 	2.0
# ]s

##-------------##
## .arg_sort() ##
##-------------##
'''
In Pandas, you use .argsort(). In Polars, you use .arg_sort().
It returns the integer positions (indices) that would sort the Series.
Nulls are placed at the end of the returned indices by default.
'''

s_demo_no_nulls = pl.Series([5.8, 4.6, 2.0, 14.0, 4.6, 25.2])
print(s_demo_no_nulls.arg_sort())
# shape: (6,)
# Series: '' [u32]
# [
# 	2   (index of value 2.0)
# 	1   (index of value 4.6)
# 	4   (index of value 4.6 duplicate)
# 	0   (index of value 5.8)
# 	3   (index of value 14.0)
# 	5   (index of value 25.2)
# ]

'''
NOTE on String Sorting:
Just like in Pandas, if the data is String type, the sorting is done
lexicographically based on Unicode code points. It is case-sensitive,
meaning uppercase letters come before lowercase letters ('A' < 'a').
'''


# =========================================================================================
# 2. N-Largest and N-Smallest methods
# =========================================================================================
'''
Polars does not have explicit .nlargest() and .nsmallest() methods directly on Series objects.
Instead, the idiomatic Polars approach is to combine .sort() with .head(n).
'''

##---------------##
##   N-Largest   ##
##---------------##

# Equivalent to pandas' .nlargest(3)
print(s_demo_no_nulls.sort(descending=True).head(3))
# shape: (3,)
# Series: '' [f64]
# [
# 	25.2
# 	14.0
# 	5.8
# ]

##----------------##
##   N-Smallest   ##
##----------------##

# Equivalent to pandas' .nsmallest(3)
print(s_demo_no_nulls.sort().head(3))
# shape: (3,)
# Series: '' [f64]
# [
# 	2.0
# 	4.6
# 	4.6
# ]

##--------------------------------------##
## NOTE: Getting original indices       ##
##--------------------------------------##
'''
Pandas' .nlargest() and .nsmallest() return the values ALONG WITH their original custom index labels.
Since Polars has no custom indices, it just returns the values.
If you need the original positional indices of the top N elements, use .arg_sort():
'''

top_3_indices = s_demo_no_nulls.arg_sort(descending=True).head(3)
print(top_3_indices)
# shape: (3,)
# Series: '' [u32]
# [
# 	5
# 	3
# 	0
# ]
