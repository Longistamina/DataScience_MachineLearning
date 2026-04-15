'''
1. dr.as_integer(): Convert to Integer

2. dr.as_double(): Convert to Double

3. dr.as_numeric(): Convert to Numeric

4. Use Pandas conversion methods or functions
'''

import datar.all as dr
from datar import f
import pandas as pd

from pipda import register_verb
dr.filter = register_verb(func=dr.filter_)
dr.slice = register_verb(func=dr.slice_)

#####################

s_float = pd.Series([1.0, 2.5, 3.7, 4.2, 5.9])
s_str = pd.Series(['1', '2', '3', '4.6', '5.7'])
s_mixed = pd.Series(['1', 2, '3', 4, 'five'])


#---------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. dr.as_integer() -------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

print(dr.as_integer(s_float))
# 0    1
# 1    2
# 2    3
# 3    4
# 4    5
# dtype: int64

print(dr.as_integer(s_str))
# ValueError: invalid literal for int() with base 10: '4.6'

print(dr.as_integer(s_mixed))
# ValueError: invalid literal for int() with base 10: 'five'


#---------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 2. dr.as_double() -----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

print(dr.as_double(s_float))
# 0    1.0
# 1    2.5
# 2    3.7
# 3    4.2
# 4    5.9
# dtype: float64

print(dr.as_double(s_str))
# 0    1.0
# 1    2.0
# 2    3.0
# 3    4.6
# 4    5.7
# dtype: float64

print(dr.as_double(s_mixed))
# ValueError: could not convert string to float: 'five'


#---------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 3. dr.as_numeric() -----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

print(dr.as_numeric(s_float))
# 0    1
# 1    2
# 2    3
# 3    4
# 4    5
# dtype: int64

print(dr.as_numeric(s_str))
# 0    1.0
# 1    2.0
# 2    3.0
# 3    4.6
# 4    5.7
# dtype: float64

print(dr.as_numeric(s_mixed))
# raise ValueError(f"Cannot convert {x} to numeric")
# ValueError: Cannot convert 0       1


#---------------------------------------------------------------------------------------------------------------#
#-------------------------------- 4. Use Pandas conversion methods or functions --------------------------------#
#---------------------------------------------------------------------------------------------------------------#

df_demo = pd.DataFrame({
    'A': ['1', '2', '3'],
    'B': ['4.1', '5.2', '6.3']
})

###########################
## Using Series.astype() ##
###########################

print(
    df_demo
    >> dr.mutate(
        A = f.A.astype(int),
        B = f.B.astype(float)
    )
)
#         A         B
#   <int64> <float64>
# 0       1       4.1
# 1       2       5.2
# 2       3       6.3

###########################
## Using pd.to_numeric() ##
###########################

print(
    df_demo
    >> dr.mutate(
        A = dr.pipe(lambda f: pd.to_numeric(f.A, errors='raise')),
        B = dr.pipe(lambda f: pd.to_numeric(f.B, errors='raise'))
    )
)
#         A         B
#   <int64> <float64>
# 0       1       4.1
# 1       2       5.2
# 2       3       6.3