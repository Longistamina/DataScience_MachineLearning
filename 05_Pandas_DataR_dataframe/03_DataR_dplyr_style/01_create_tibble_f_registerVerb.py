'''
tibble() function from DataR library creates a DataFrame in a more user-friendly way 
compared to the traditional pandas DataFrame constructor.

DataR offers the "f" expression syntax, which allows for a more concise and readable way to manipulate DataFrames.

#############################

1. Create dataframe using datar.tibble.tibble()

2. Convert pandas DataFrame to datar tibble

3. "f" expression syntax for DataFrame manipulation
    + register_verb(): dr.filter() = register_verb(func = dr.filter_)
'''

import datar.all as dr
from datar import f
import pandas as pd

# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")

#---------------------------------------------------------------------------------------------------------------------#
#-------------------------------- 1. Create dataframe using datar.tibble.tibble() ------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

tb = dr.tibble(
    x = [1, 2, 3],
    y = ["a", "b", "c"],
    z = [True, False, True]
)

print(type(tb))  # <class 'datar_pandas.tibble.Tibble'>

print(tb)
#         x        y      z
#   <int64> <object> <bool>
# 0       1        a   True
# 1       2        b  False
# 2       3        c   True


#---------------------------------------------------------------------------------------------------------------------#
#----------------------------------- 2. Convert pandas DataFrame to datar tibble -------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['x', 'y', 'z'],
    'C': [True, False, True]
})

tb_from_df = dr.tibble(df)

print(tb_from_df)
#         A        B      C
#   <int64> <object> <bool>
# 0       1        x   True
# 1       2        y  False
# 2       3        z   True


#---------------------------------------------------------------------------------------------------------------------#
#------------------------------- 3. "f" expression syntax for DataFrame manipulation ---------------------------------#
#---------------------------------------------------------------------------------------------------------------------#
'''
"f" expression syntax allows for more intuitive and readable DataFrame operations,
it liberates us from typing the DataFrame name repeatedly (like df[df['A'] > 1])

This also supports pandas DataFrame
'''

#####################
## register_verb() ##
#####################

from pipda import register_verb

dr.filter = register_verb(func = dr.filter_)

'''
dr.filter_() to avoid conflict with Python built-in function filter()
=> Use registter_verb to bring it back as dr.filter()
'''

#################
## with tibble ##
#################

filtered_tb = tb >> dr.filter(f.x > 1)
print(filtered_tb)
#         x        y      z
#   <int64> <object> <bool>
# 1       2        b  False
# 2       3        c   True

selected_tb = tb >> dr.select(f['y'], f['z'])
print(selected_tb)
#          y      z
#   <object> <bool>
# 0        a   True
# 1        b  False
# 2        c   True

selected_tb2 = tb >> dr.select(f[['x', 'z']])
print(selected_tb2)
#         x      z
#   <int64> <bool>
# 0       1   True
# 1       2  False
# 2       3   True

'''
filtered_tb = tb[f.x > 1, f.y]

THIS WILL NOT WORK
'''

####################
## with pandas df ##
####################

filtered_df = df >> dr.filter(f.A > 1)
print(filtered_df)
#         A        B      C
#   <int64> <object> <bool>
# 1       2        y  False
# 2       3        z   True

selected_df = df >> dr.select(f['B'], f['C'])
print(selected_df)
#          B      C
#   <object> <bool>
# 0        x   True
# 1        y  False
# 2        z   True


