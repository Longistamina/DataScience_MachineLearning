'''
Flow of contents:
1. pd.concat(): Concatenation of Series
2. pd.combine(): Element-wise Merging
'''

import pandas as pd

#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 1. pd.concat() --------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

'''
The concat() function concatenates Series along a specified axis.

Key Features:
+ Combines multiple Series into one
+ Supports ignore_index to reset index
'''

s1 = pd.Series(['a', 'b'])
s2 = pd.Series(['c', 'd'])

###################################
## Basic concatenation of Series ##
###################################

s_concat = pd.concat([s1, s2])
print(s_concat)
# 0    a
# 1    b
# 0    c
# 1    d
# dtype: object


######################################
## Concatenation with ignore_index= ##
######################################

s_concat = pd.concat([s1, s2], ignore_index = True)
print(s_concat)
# 0    a
# 1    b
# 2    c
# 3    d
# dtype: object


##############################
## Concatenation with keys= ##
##############################

s_concat = pd.concat([s1, s2], keys = ['first', 'second'])
print(s_concat)
# first   0    a
#         1    b
# second  0    c
#         1    d
# dtype: object


#-----------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 2. pd.combine() -------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

'''
The combine() method combines Series with another Series or scalar using a function.
(works like merging two dataframes)

Key Features:
+ Performs element-wise operations between two Series
+ Handles missing values with fill_value parameter
+ Can combine with scalars or other Series
'''

s1 = pd.Series({'falcon': 330.0, 'eagle': 160.0})
s2 = pd.Series({'falcon': 345.0, 'eagle': 200.0, 'duck': 30.0})

#########################################
## Basic combine with other= and func= ##
#########################################

s_combined = s1.combine(other = s2, func = max)
print(s_combined)
# duck        NaN
# eagle     200.0
# falcon    345.0
# dtype: float64

'''MUST always specify the func= parameter, otherwise it will raise an error.'''


############################################
## Combine with fill_value= to handle NaN ##
############################################

s_combined = s1.combine(other = s2, func = max, fill_value = 0)
print(s_combined)
# duck       30.0
# eagle     200.0
# falcon    345.0
# dtype: float64

'''
In this case, since s1 does not have a value for 'duck', 
it is filled with 0.

Therefore, the max function compares 0 with 30.0,
resulting in 'duck' having a value of 30.0.
'''
