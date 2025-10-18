'''
tibble() function from DataR library creates a DataFrame in a more user-friendly way 
compared to the traditional pandas DataFrame constructor.

DataR offers the "f" expression syntax, which allows for a more concise and readable way to manipulate DataFrames.

#############################

1. Create dataframe using datar.tibble.tibble()

2. Convert pandas DataFrame to datar tibble
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
