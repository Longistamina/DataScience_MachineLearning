'''
1. Updating elements: s.iloc[]=, dictionary style s[]=, s.update()

2. Add new elements: s[]=, pd.concat()

3. Deleting elements: s.drop(), s.pop()
'''

import pandas as pd

#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. Updating elements -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_old = pd.Series(data = [10, 20, 30, 40, 50])
s_old_index = pd.Series(data = [10, 20, 30, 40, 50], index = ['a', 'b', 'c', 'd', 'e'])


#########################################
##            Using .iloc[]            ##
#########################################

s_new = s_old.copy()

s_new.iloc[0] = 100  # Updating the first element
print(s_new)
# 0    100
# 1     20
# 2     30
# 3     40
# 4     50
# dtype: int64

s_new.iloc[1:3] = [200, 300]  # Updating a range of elements
print(s_new)
# 0    100
# 1    200
# 2    300
# 3     40
# 4     50
# dtype: int64


#########################################
##        Using dictionary style       ##
#########################################

s_new_index = s_old_index.copy()

s_new_index['a'] = 100  # Updating the element with index label 'a'
print(s_new_index)
# a    100
# b     20
# c     30
# d     40
# e     50
# dtype: int64

s_new_index['b':'d'] = [200, 300, 400]  # Updating a range of elements by index labels (inclusive)
print(s_new_index)
# a    100
# b    200
# c    300
# d    400
# e     50
# dtype: int64

s_new_index[['a', 'e']] = [500, 600]  # Updating multiple elements by index labels
print(s_new_index)
# a    500
# b    200
# c    300
# d    400
# e    600
# dtype: int64


########################################
##          Using .update()           ##
########################################

#------------------------
## With non-indexed Series
#------------------------

s_update = s_old.copy()

s_update.update(pd.Series(data = [100, 200]))
print(s_update)
# 0    100
# 1    200
# 2     30
# 3     40
# 4     50
# dtype: int64
'''Here, 100 takes the place of 10 (index 0), and 200 takes the place of 20 (index 1).'''

s_update.update(pd.Series(data = [300, 500], index = [2, 4]))
print(s_update)
# 0    100
# 1    200
# 2    300
# 3     40
# 4    500
# dtype: int64
'''Here, 300 replaces the value at index 2, and 500 replaces the value at index 4.'''

#------------------------
## With indexed Series
#------------------------

s_update_index = s_old_index.copy()

s_update_index.update(pd.Series(data = [200, 500], index = ['b', 'e']))
print(s_update_index)
# a     10
# b    200
# c     30
# d     40
# e    500
# dtype: int64
'''Here, 200 replaces the value at index 'b', and 500 replaces the value at index 'e'.'''


#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. Add new elements ------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_old = pd.Series(data = [10, 20, 30, 40, 50])
s_old_index = pd.Series(data = [10, 20, 30, 40, 50], index = ['a', 'b', 'c', 'd', 'e'])

#####################################
##            Using s[]            ##
#####################################

#---------------
## With non-indexed Series
#---------------

s_new = s_old.copy()
s_new[5] = 60  # Adding a new element at index 5
print(s_new)
# 0    10
# 1    20
# 2    30
# 3    40
# 4    50
# 5    60
# dtype: int64

s_new[9] = 900 # Adding a new element at index 9
print(s_new)
# 0     10
# 1     20
# 2     30
# 3     40
# 4     50
# 5     60
# 9    900
# dtype: int64

s_new[[7,8]] = [700, 800]
'''
Raise ERROR
'''

#----------------
## With indexed Series
#----------------

s_new_index = s_old_index.copy()

s_new_index['f'] = 60  # Adding a new element with index label 'f'
print(s_new_index)
# a    10
# b    20
# c    30
# d    40
# e    50
# f    60
# dtype: int64

s_new_index['m'] = 8000  # Adding a new element with index label 'm'
print(s_new_index)
# a      10
# b      20
# c      30
# d      40
# e      50
# f      60
# m    8000
# dtype: int64

s_new_index[['x', 'y']] = [9000, 10000]
'''
Raise ERROR
'''

########################################
##          Using pd.concat()         ##
########################################

#---------------
## With non-indexed Series
#---------------

s_new = pd.concat(
    objs = [s_old, pd.Series(data = [600, 700, 800], dtype = s_old.dtype)], # Ensure the same dtype
    ignore_index = True  # Reindex the resulting Series
)

print(s_new)
# 0     10
# 1     20
# 2     30
# 3     40
# 4     50
# 5    600
# 6    700
# 7    800
# dtype: int64

#----------------
## With indexed Series
#----------------

s_new_index = pd.concat(
    objs = [s_old_index, pd.Series(data = [600, 700, 800], index = ['x', 'y', 'z'], dtype = s_old_index.dtype)], # Ensure the same dtype
    ignore_index = False  # Keep the original index labels
)

print(s_new_index)
# a     10
# b     20
# c     30
# d     40
# e     50
# x    600
# y    700
# z    800
# dtype: int64

'''
NOTE: must use pd.concat() with TWO SERIES or TWO DATAFRAMES
'''


#-------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 3. Deleting elements -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

s_old = pd.Series(data = [10, 20, 30, 40, 50])

s_old_index = pd.Series(data = [10, 20, 30, 40, 50], index = ['a', 'b', 'c', 'd', 'e'])

# Create a multi-level indexed Series
multi_index = pd.MultiIndex(
    levels = [
        ['llama', 'cow', 'falcon'], # Level 0 labels
        ['speed', 'weight', 'length'] # Level 1 labels
    ],
    codes = [
        [0, 0, 0, 1, 1, 1, 2, 2, 2],
        [0, 1, 2, 0, 1, 2, 0, 1, 2]
    ]
)

s_old_multi_index = pd.Series([45, 200, 1.2, 30, 250, 1.5, 320, 1, 0.3], index = multi_index)


######################################
##            Using s.drop()        ##
######################################

#---------------
## With non-indexed Series (index=)
#---------------
'''Use default integer index'''

s_new = s_old.drop(index = 0)  # Deleting the element at index 0
print(s_new)
# 1    20
# 2    30
# 3    40
# 4    50
# dtype: int64

s_new = s_old.drop(index = [1, 3])  # Deleting elements at index 1 and 3
print(s_new)
# 0    10
# 2    30
# 4    50
# dtype: int64

#---------------
## With indexed Series (labels=)
#---------------

s_new_index = s_old_index.drop(labels = 'a')  # Deleting the element with index label 'a'
print(s_new_index)
# b    20
# c    30
# d    40
# e    50
# dtype: int64

s_new_index = s_old_index.drop(labels = ['b', 'd'])  # Deleting elements with index labels 'b' and 'd'
print(s_new_index)
# a    10
# c    30
# e    50
# dtype: int64

#---------------
## With multi-indexed Series (labels=, level=)
#---------------

print(s_old_multi_index)
# llama   speed      45.0
#         weight    200.0
#         length      1.2
# cow     speed      30.0
#         weight    250.0
#         length      1.5
# falcon  speed     320.0
#         weight      1.0
#         length      0.3
# dtype: float64

s_new_multi_index = s_old_multi_index.drop(labels = 'llama', level = 0)  # Deleting all elements under the 'llama' category
print(s_new_multi_index)
# cow     speed      30.0
#         weight    250.0
#         length      1.5
# falcon  speed     320.0
#         weight      1.0
#         length      0.3
# dtype: float64

s_new_multi_index = s_old_multi_index.drop(labels = ['weight', 'length'], level = 1)  # Deleting all 'weight' and 'length' elements across all categories
print(s_new_multi_index)
# llama   speed     45.0
# cow     speed     30.0
# falcon  speed    320.0
# dtype: float64


######################################
##           Using s.pop()          ##
######################################

#---------------
## With non-indexed Series
#---------------

s_old_pop = s_old.copy()

popped_value = s_old_pop.pop(0)  # Removing and returning the element at index 0

print(popped_value)  # 10

print(s_old_pop)
# 1    20
# 2    30
# 3    40
# 4    50
# dtype: int64

#---------------
## With indexed Series
#---------------

s_old_index_pop = s_old_index.copy()

popped_value_index = s_old_index_pop.pop('a')  # Removing and returning the element with index label 'a'

print(popped_value_index)  # 10

print(s_old_index_pop)
# b    20
# c    30
# d    40
# e    50
# dtype: int64

'''
NOTE: s.pop() only removes a single element at a time, specified by its index label or position.
      s.pop() will raise a KeyError if the specified index label does not exist in the Series.
'''