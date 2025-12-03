'''
1. .filter(): Index-based Filtering

2. .where(): Conditional Filtering and Replacement
'''

import pandas as pd
import numpy as np

#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 1. .filter() --------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

'''
The filter() method subsets Series based on index labels, not content.

Key Features:
+ Filters based on INDEX LABELS, not values
+ Supports items, like, and regex parameters
+ Cannot be used for content-based filtering
'''

s_birds_flight = pd.Series(
    data = [390., 350., 30., 20., 55],
    index = ['Bird_1', 'Bird_2', 'Bird_3', 'Bird_4', 'Sparrow']
)

#########################
## Filter using items= ##
#########################

s_filtered = s_birds_flight.filter(items = ['Bird_1', 'Bird_2'])  # Filtering by index labels
print(s_filtered)
# Bird_1    390.0
# Bird_2    350.0
# dtype: float64


#########################
## Filter using regex= ##
#########################

s_filtered = s_birds_flight.filter(regex = '[24]$')  # Filtering by index labels ending with '2' or '4'
print(s_filtered)
# Bird_2    350.0
# Bird_4     20.0
# dtype: float64


########################
## Filter using like= ##
########################

s_filtered = s_birds_flight.filter(like = 'rd_')  # Filtering by index labels containing 'Bird'
print(s_filtered)
# Bird_1    390.0
# Bird_2    350.0
# Bird_3     30.0
# Bird_4     20.0
# dtype: float64


#---------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 2. .where() ---------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

'''
The where() method replaces values where conditions are False.

Key Features:
+ Keeps original values where condition is True
+ Replaces with specified values where condition is False
+ Supports broadcasting and callable conditions
'''

np.random.seed(42)

s_nums = pd.Series(np.random.normal(loc = 3, scale = 2, size = 5)).round(2)
print(s_nums)
# 0    3.99
# 1    2.72
# 2    4.30
# 3    6.05
# 4    2.53
# dtype: float64

#################################################
## Using where() and dropna() to filter values ##
#################################################

s_where = s_nums.where(s_nums <= 3)
print(s_where)
# 0     NaN
# 1    2.72
# 2     NaN
# 3     NaN
# 4    2.53
# dtype: float64

s_where = s_nums.where(s_nums <= 3).dropna()
print(s_where)
# 1    2.72
# 4    2.53
# dtype: float64

s_where = s_nums.where(s_nums <= 3).dropna(ignore_index = True)
print(s_where)
# 0    2.72
# 1    2.53
# dtype: float64


#####################################################
## Using where() to replace False-condition values ##
#####################################################

s_where = s_nums.where(s_nums <= 3, other = 0)  # Replacing values greater than 3 with 0
print(s_where)
# 0    0.00
# 1    2.72
# 2    0.00
# 3    0.00
# 4    2.53
# dtype: float64

#-----------------

s_mixed = pd.Series(["apple", "banana", "cherry", 42, 3.14, None])

is_string = is_string = s_mixed.apply(lambda x: isinstance(x, str))

s_where = s_mixed.where(is_string, other = "Unknown")
print(s_where)
# 0      apple
# 1     banana
# 2     cherry
# 3    Unknown
# 4    Unknown
# 5    Unknown
# dtype: object
