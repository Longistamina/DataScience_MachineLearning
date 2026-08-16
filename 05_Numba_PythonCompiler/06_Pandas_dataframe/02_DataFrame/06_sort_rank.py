'''
1. Sort:
   + df.sort_values(by=..., ascending=..., inplace=...)
   + df.sort_index(axis=..., ascending=..., inplace=...)

2. Rank:
   + df.rank(method="average", ascending=True, axis=0)
   + df.rank(method="max", ascending=True, axis=0)
   + df.rank(method="min", ascending=True, axis=0)
   + df.rank(method="dense", ascending=True, axis=0)
   + df.rank(method="first", ascending=True, axis=0)
   + rank UNIQUE values
   + df.rank(pct=True)
'''

import pandas as pd

#--------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 1. Sort ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

df_raw_sort = pd.DataFrame(
    {
        "name": ["Alice", "Alice", "Alice", "Bob", "Bob", "Charlie"],
        "subject": ["Math", "English", "Science", "Math", "English", "Math"],
        "score": [85, 90, 78, 92, 88, 95],
        "age": [20, 20, 20, 22, 22, 23],
    }
)

df_raw_idx = pd.DataFrame(
    {
        "Numbers":[1, 2, 3, 4, 5],
        "Letters":["a", "b", "c", "d", "e"]
    }, 
    index=[100, 29, 234, 1, 150],
)

########################
##  df.sort_values()  ##
########################

#---------------
## Sort by single column
#---------------

df_sorted = df_raw_sort.sort_values(by="score", ascending=False, inplace=False)
print(df_sorted)
#       name  subject  score  age
# 5  Charlie     Math     95   23
# 3      Bob     Math     92   22
# 1    Alice  English     90   20
# 4      Bob  English     88   22
# 0    Alice     Math     85   20
# 2    Alice  Science     78   20

#---------------
## Sort by multiple columns and orders
#---------------

df_sorted = df_raw_sort.sort_values(by=["name", "score"], ascending=[False, True], inplace=False)
print(df_sorted)
#       name  subject  score  age
# 5  Charlie     Math     95   23
# 4      Bob  English     88   22
# 3      Bob     Math     92   22
# 2    Alice  Science     78   20
# 0    Alice     Math     85   20
# 1    Alice  English     90   20

#######################
##  df.sort_index()  ##
#######################

print(df_raw_idx)
#      Numbers Letters
# 100        1       a
# 29         2       b
# 234        3       c
# 1          4       d
# 150        5       e

#---------------
## Sort by axis=0 (row names), ascending=True
#---------------

df_sorted = df_raw_idx.sort_index(axis=0, ascending=True, inplace=False)

print(df_sorted)
#      Numbers Letters
# 1          4       d
# 29         2       b
# 100        1       a
# 150        5       e
# 234        3       c

#---------------
## Sort by axis=1 (column names), ascending=False
#---------------

df_sorted = df_raw_idx.sort_index(axis=0, ascending=False, inplace=False)

print(df_sorted)
#      Numbers Letters
# 234        3       c
# 150        5       e
# 100        1       a
# 29         2       b
# 1          4       d

#---------------
## Sort by axis=1 (column names), ascending=True
#---------------

df_sorted = df_raw_idx.sort_index(axis=1, ascending=True, inplace=False)

print(df_sorted)
#     Letters  Numbers
# 100       a        1
# 29        b        2
# 234       c        3
# 1         d        4
# 150       e        5

#--------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2. Rank ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

'''NOTE: when using df.rank() for DataFrame, must always set axis=0'''

df_raw_rank = pd.DataFrame(
    {
        "name": ["Alice", "Bob", "Charlie", "David", "Eva", "Freddy", "George", "Hannah"],
        "score": [85, 92, 85, 88, 90, 66, 66, 66]
    }
)

print(df_raw_rank)
#       name  score
# 0    Alice     85
# 1      Bob     92
# 2  Charlie     85
# 3    David     88
# 4      Eva     90
# 5   Freddy     66
# 6   George     66
# 7   Hannah     66

#######################################################
## df.rank(method="average", ascending=True, axis=1) ##
#######################################################

df_ranked = df_raw_rank.copy()

print(df_ranked["score"].rank(method="average", ascending=True, axis=0))
# 0    4.5
# 1    8.0
# 2    4.5
# 3    6.0
# 4    7.0
# 5    2.0
# 6    2.0
# 7    2.0
# Name: score, dtype: float64

# Add a new column "rank_average" to df_ranked
df_ranked["rank_average"] = df_ranked["score"].rank(method="average", ascending=True, axis=0)
print(df_ranked)
#       name  score  rank_average
# 0    Alice     85           4.5
# 1      Bob     92           8.0
# 2  Charlie     85           4.5
# 3    David     88           6.0
# 4      Eva     90           7.0
# 5   Freddy     66           2.0
# 6   George     66           2.0
# 7   Hannah     66           2.0
'''
Freddy, George and Hannah have the same score of 66, 
=> share rank = (1+2+3)/3 = 2.0.

Alice and Charlie have the same score of 85,
=> share rank = (4+5)/2 = 4.5

David has the score of 88 (unique),
=> rank = 6
'''

###################################################
## df.rank(method="max", ascending=True, axis=1) ##
###################################################

df_ranked = df_raw_rank.copy()

df_ranked["rank_max"] = df_ranked["score"].rank(method="max", ascending=True, axis=0)
print(df_ranked)
# 0    Alice     85       5.0
# 1      Bob     92       8.0
# 2  Charlie     85       5.0
# 3    David     88       6.0
# 4      Eva     90       7.0
# 5   Freddy     66       3.0
# 6   George     66       3.0
# 7   Hannah     66       3.0
'''
Freddy, George and Hannah have the same score of 66,
=> share rank = max(1, 2, 3) = 3.0

Alice and Charlie have the same score of 85,
=> share rank = max(4, 5) = 5.0

David has the score of 88 (unique),
=> rank = 6
'''

###################################################
## df.rank(method="min", ascending=True, axis=1) ##
###################################################

df_ranked = df_raw_rank.copy()

df_ranked["rank_min"] = df_ranked["score"].rank(method="min", ascending=True, axis=0)
print(df_ranked)
#       name  score  rank_min
# 0    Alice     85       4.0
# 1      Bob     92       8.0
# 2  Charlie     85       4.0
# 3    David     88       6.0
# 4      Eva     90       7.0
# 5   Freddy     66       1.0
# 6   George     66       1.0
# 7   Hannah     66       1.0
'''
Freddy, George and Hannah have the same score of 66,
=> share rank = min(1, 2, 3) = 1.0

Alice and Charlie have the same score of 85,
=> share rank = min(4, 5) = 4.0

David has the score of 88 (unique),
=> rank = 6
'''

#####################################################
## df.rank(method="dense", ascending=True, axis=1) ##
#####################################################

df_ranked = df_raw_rank.copy()

df_ranked["rank_dense"] = df_ranked["score"].rank(method="dense", ascending=True, axis=0)
print(df_ranked)
#       name  score  rank_dense
# 0    Alice     85         2.0
# 1      Bob     92         5.0
# 2  Charlie     85         2.0
# 3    David     88         3.0
# 4      Eva     90         4.0
# 5   Freddy     66         1.0
# 6   George     66         1.0
# 7   Hannah     66         1.0
'''
It works like "min" method, but rank always increases by 1 between groups

Freddy, George and Hannah have the same score of 66,
=> share rank = min(1, 2, 3) = 1.0

Alice and Charlie have the same score of 85,
=> min rank = min(4, 5) = 4
=> DENSE rank = 2.0 (rank increases by 1 from previous group)

David has the score of 88 (unique),
=> min rank = 6
=> DENSE rank = 3.0 (rank increases by 1 from previous group)
'''

#####################################################
## df.rank(method="first", ascending=True, axis=1) ##
#####################################################

df_ranked = df_raw_rank.copy()

df_ranked["rank_first"] = df_ranked["score"].rank(method="first", ascending=True, axis=0)
print(df_ranked)
#       name  score  rank_first
# 0    Alice     85         4.0
# 1      Bob     92         8.0
# 2  Charlie     85         5.0
# 3    David     88         6.0
# 4      Eva     90         7.0
# 5   Freddy     66         1.0
# 6   George     66         2.0
# 7   Hannah     66         3.0
'''
Freddy, George and Hannah have the same score of 66,
=> rank based on their order of appearance in the array: 1, 2, 3
(Freddy appears first, hence it ranks 1)

Alice and Charlie have the same score of 85,
=> rank based on their order of appearance in the array: 4, 5

David has the score of 88 (unique),
=> rank = 6
'''

##############################
## Rank UNIQUE values only  ##
##############################

df_raw_unique = pd.DataFrame(
    {
        "name": ["Alice", "Bob", "Charlie", "David", "Eva", "Freddy", "George", "Hannah"],
        "score": [85, 92, 86, 88, 90, 54, 25, 42]
    }
)
print(df_raw_unique)
#       name  score
# 0    Alice     85
# 1      Bob     92
# 2  Charlie     86
# 3    David     88
# 4      Eva     90
# 5   Freddy     54
# 6   George     25
# 7   Hannah     42

df_ranked = (
    df_raw_unique.copy()
    .assign(
        rank_average = lambda df: df["score"].rank(method="average", ascending=True, axis=0),
        rank_max = lambda df: df["score"].rank(method="max", ascending=True, axis=0),
        rank_min = lambda df: df["score"].rank(method="min", ascending=True, axis=0),
        rank_dense = lambda df: df["score"].rank(method="dense", ascending=True, axis=0),
        rank_first = lambda df: df["score"].rank(method="first", ascending=True, axis=0),
    )
)

print(df_ranked)
#       name  score  rank_average  rank_max  rank_min  rank_dense  rank_first
# 0    Alice     85           4.0       4.0       4.0         4.0         4.0
# 1      Bob     92           8.0       8.0       8.0         8.0         8.0
# 2  Charlie     86           5.0       5.0       5.0         5.0         5.0
# 3    David     88           6.0       6.0       6.0         6.0         6.0
# 4      Eva     90           7.0       7.0       7.0         7.0         7.0
# 5   Freddy     54           3.0       3.0       3.0         3.0         3.0
# 6   George     25           1.0       1.0       1.0         1.0         1.0
# 7   Hannah     42           2.0       2.0       2.0         2.0         2.0
'''When all teh values are UNIQUE, all methods give the SAME result'''

#######################
## df.rank(pct=True) ##
#######################
'''Rank in percentage (from 0 to 1)'''

#---------------
## With UNIQUE values
#---------------

df_ranked = (
    df_raw_unique.copy()
    .assign(rank_pct=lambda df: df["score"].rank(method="average", ascending=True, axis=0, pct=True))
)

print(df_ranked)
#       name  score  rank_pct
# 0    Alice     85     0.500
# 1      Bob     92     1.000
# 2  Charlie     86     0.625
# 3    David     88     0.750
# 4      Eva     90     0.875
# 5   Freddy     54     0.375
# 6   George     25     0.125
# 7   Hannah     42     0.250
'''
Alice has the score of 85,
=> rank = 4 (because there are 3 scores lower than 85: 25, 42, 54)
=> rank_pct = 4/8 = 0.5

Bob has the score of 92 (highest, unique),
=> rank = 8 
=> rank_pct = 8/8 = 1.0
'''

#---------------
## With DUPLICATE values
#---------------

df_ranked = (
    df_raw_rank.copy()
    .assign(
        rank_average = lambda df: df["score"].rank(method="average", ascending=True, axis=0, pct=True),
        rank_min = lambda df: df["score"].rank(method="min", ascending=True, axis=0, pct=True),
        rank_max = lambda df: df["score"].rank(method="max", ascending=True, axis=0, pct=True),
        rank_dense = lambda df: df["score"].rank(method="dense", ascending=True, axis=0, pct=True),
        rank_first = lambda df: df["score"].rank(method="first", ascending=True, axis=0, pct=True),
    )
)

print(df_ranked)
#       name  score  rank_average  rank_min  rank_max  rank_dense  rank_first
# 0    Alice     85        0.5625     0.500     0.625         0.4       0.500
# 1      Bob     92        1.0000     1.000     1.000         1.0       1.000
# 2  Charlie     85        0.5625     0.500     0.625         0.4       0.625
# 3    David     88        0.7500     0.750     0.750         0.6       0.750
# 4      Eva     90        0.8750     0.875     0.875         0.8       0.875
# 5   Freddy     66        0.2500     0.125     0.375         0.2       0.125
# 6   George     66        0.2500     0.125     0.375         0.2       0.250
# 7   Hannah     66        0.2500     0.125     0.375         0.2       0.375
'''
AVERAGE:
Freddy, George and Hannah have the same score of 66,
=> share rank = (1+2+3)/3 = 2.0
=> rank_pct = 2/8 = 0.25

MIN: Freddy, George and Hannah have the same score of 66,
=> share rank = min(1, 2, 3) = 1.0
=> rank_pct = 1/8 = 0.125

MAX: 
Freddy, George and Hannah have the same score of 66,
=> share rank = max(1, 2, 3) = 3.0
=> rank_pct = 3/8 = 0.375

--------------------
DENSE: 

Freddy, George and Hannah have the same score of 66,
=> share rank = min(1, 2, 3) = 1.0
=> dense rank = 1 (rank increases by 1 from previous group)
=> rank_pct = 1/5 = 0.2 (because there are 5 distinct ranks: 1, 2, 3, 4, 5)

Alice and Charlie have the same score of 85,
=> min rank = min(4, 5) = 4
=> DENSE rank = 2.0 (rank increases by 1 from previous group)
=> rank_pct = 2/5 = 0.4

--------------------
FIRST:
Freddy, George and Hannah have the same score of 66,

=> rank based on their order of appearance in the array: 1, 2, 3
   (Freddy appears first, hence it ranks 1)

=> rank_pct = 1/8 = 0.125 (Freddy)
              2/8 = 0.25  (George)
              3/8 = 0.375 (Hannah)
'''