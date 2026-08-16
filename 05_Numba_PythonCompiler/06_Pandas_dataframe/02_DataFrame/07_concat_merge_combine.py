'''
pd.concat(), pd.merge(), pd.combine() are 3 powerful functions/methods in pandas used for combining DataFrames, 
but they serve different purposes and operate in different ways.

#########################################################

1. Concatenation:
   + pd.concat(axis=0): used to stack DataFrames vertically (row-wise).
   + pd.concat(axis=1): used to stack DataFrames horizontally (column-wise).

2. Merging:
   + pd.merge(on='key'): merges DataFrames based on a common column (key).
   + pd.merge(suffixes=('_left', '_right')): adds suffixes to overlapping column names to differentiate them.
   + pd.merge(how='inner'): only keeps rows whose keys are present in both DataFrames.
   + pd.merge(how='outer'): keeps all rows from both DataFrames, filling in NaNs for missing matches.
   + pd.merge(how='left'): keeps all rows from the left DataFrame and matches from the right DataFrame.
   + pd.merge(how='right'): keeps all rows from the right DataFrame and matches from the left DataFrame.
   + pd.merge(left_on='key1', right_on='key2'): merges DataFrames based on different columns from each DataFrame.
   + pd.merge(left_index=True, right_index=True): merges DataFrames based on their index.
   + pd.merge(how='cross'): creates the Cartesian product of both DataFrames.
   + df.merge(): instance method to merge DataFrames.

3. Combining: Combines a DataFrame with other DataFrame using func to element-wise combine columns.
   + df.combine(): instance method to combine DataFrames.
'''

import pandas as pd
import numpy as np

#------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. Concatenation --------------------------------------------#
#------------------------------------------------------------------------------------------------------#

# Create sample DataFrames
df_origin = pd.DataFrame({
    'A': ['A0', 'A1', 'A2', 'A3'],
    'B': ['B0', 'B1', 'B2', 'B3'],
    'C': ['C0', 'C1', 'C2', 'C3']
})

df_ver_1 = pd.DataFrame({
    'A': ['A4', 'A5', 'A6', 'A7'],
    'B': ['B4', 'B5', 'B6', 'B7'],
    'C': ['C4', 'C5', 'C6', 'C7']
})

df_ver_2 = pd.DataFrame({
    'A': ['A8', 'A9', 'A10', 'A11'],
    'B': ['B8', 'B9', 'B10', 'B11'],
    'C': ['C8', 'C9', 'C10', 'C11']
})

df_hor_1 = pd.DataFrame({
    'D': ['D0', 'D1', 'D2', 'D3'],
    'E': ['E0', 'E1', 'E2', 'E3'],
    'F': ['F0', 'F1', 'F2', 'F3']
})

df_hor_2 = pd.DataFrame({
    'G': ['G0', 'G1', 'G2', 'G3'],
    'H': ['H0', 'H1', 'H2', 'H3'],
    'I': ['I0', 'I1', 'I2', 'I3']
})

#############################
##    pd.concat(axis=0)    ##
#############################
''' Concatenate DataFrames vertically (row-wise) '''

# Original DataFrame
print(df_origin)
#     A   B   C
# 0  A0  B0  C0
# 1  A1  B1  C1
# 2  A2  B2  C2
# 3  A3  B3  C3

# Concatenate df_origin and df_ver_1 vertically
df_stack_ver = pd.concat(
    objs=[df_origin, df_ver_1],
    axis=0,
    ignore_index=True # Reset index in the concatenated DataFrame
)
print(df_stack_ver)
#     A   B   C
# 0  A0  B0  C0
# 1  A1  B1  C1
# 2  A2  B2  C2
# 3  A3  B3  C3
# 4  A4  B4  C4
# 5  A5  B5  C5
# 6  A6  B6  C6
# 7  A7  B7  C7

# Concatenate df_ver_1, df_origin, and df_ver_2 vertically
df_stack_ver = pd.concat(
    objs=[df_ver_1, df_origin, df_ver_2],
    axis=0,
    ignore_index=True # Reset index in the concatenated DataFrame
)
print(df_stack_ver)
#       A    B    C
# 0    A4   B4   C4
# 1    A5   B5   C5
# 2    A6   B6   C6
# 3    A7   B7   C7
# 4    A0   B0   C0
# 5    A1   B1   C1
# 6    A2   B2   C2
# 7    A3   B3   C3
# 8    A8   B8   C8
# 9    A9   B9   C9
# 10  A10  B10  C10
# 11  A11  B11  C11

#############################
##    pd.concat(axis=1)    ##
#############################
''' Concatenate DataFrames horizontally (column-wise) '''

# Original DataFrame
print(df_origin)
#     A   B   C
# 0  A0  B0  C0
# 1  A1  B1  C1
# 2  A2  B2  C2
# 3  A3  B3  C3

# Concatenate df_origin and df_hor_1 horizontally
df_stack_hor = pd.concat(
    objs=[df_origin, df_hor_1],
    axis=1
)
print(df_stack_hor)
#     A   B   C   D   E   F
# 0  A0  B0  C0  D0  E0  F0
# 1  A1  B1  C1  D1  E1  F1
# 2  A2  B2  C2  D2  E2  F2
# 3  A3  B3  C3  D3  E3  F3

# Concatenate df_hor_1, df_origin, and df_hor_2 horizontally
df_stack_hor = pd.concat(
    objs=[df_hor_1, df_origin, df_hor_2],
    axis=1
)
print(df_stack_hor)
#     D   E   F   A   B   C   G   H   I
# 0  D0  E0  F0  A0  B0  C0  G0  H0  I0
# 1  D1  E1  F1  A1  B1  C1  G1  H1  I1
# 2  D2  E2  F2  A2  B2  C2  G2  H2  I2
# 3  D3  E3  F3  A3  B3  C3  G3  H3  I3


#------------------------------------------------------------------------------------------------------#
#------------------------------------------- 2. Merging -----------------------------------------------#
#------------------------------------------------------------------------------------------------------#

# Create sample DataFrames for merging
customers = pd.DataFrame(
    {
        "customer_id": [1, 2, 3, 4],
        "name"       : ["Alice", "Bob", "Charlie", "Diana"],
        "city"       : ["New York", "Boston", "Chicago", "Miami"]
    }
)

orders = pd.DataFrame(
    {
        "order_id": [101, 102, 103, 105],
        "customer_id": [1, 2, 1, 5],
        "amount"  : [250, 180, 320, 150],
        "city"    : ["NYC", "BOS", "NYC", "MIA"]
    }
)

##############################
##    pd.merge(on='key')    ##
##############################
'''
Merge DataFrames based on a common column (key)
'''

# Merge customers and orders on 'customer_id'
df_merged_on = pd.merge(
    left=customers,
    right=orders,
    on='customer_id' # Common column to merge on
)

print(df_merged_on)
#    customer_id   name    city_x  order_id  amount city_y
# 0            1  Alice  New York       101     250    NYC
# 1            1  Alice  New York       103     320    NYC
# 2            2    Bob    Boston       102     180    BOS
'''
NOTE: The 'city' column appears twice in the merged DataFrame, once from each original DataFrame.
To differentiate them, pandas appends suffixes '_x' and '_y' by default.
'''


##############################
##    pd.merge(suffixes)    ##
##############################
'''
Add suffixes to overlapping column names to differentiate them
'''

df_merged_on = pd.merge(
    left=customers,
    right=orders,
    on='customer_id',
    suffixes=('_cst', '_odr') # Custom suffixes for overlapping columns
)

print(df_merged_on)
#    customer_id   name  city_cst  order_id  amount city_odr
# 0            1  Alice  New York       101     250      NYC
# 1            1  Alice  New York       103     320      NYC
# 2            2    Bob    Boston       102     180      BOS

#################################
##    pd.merge(how='inner')    ##
#################################
'''
how='inner': only keeps rows whose keys are present in both DataFrames
By default, pd.merge() uses how='inner' if not specified.
'''

df_merged_inner = pd.merge(
    left=customers,
    right=orders,
    on='customer_id',
    how='inner', # Only keep rows with matching keys in both DataFrames
    suffixes=('_cst', '_odr')
)

print(df_merged_inner)
#    customer_id   name  city_cst  order_id  amount city_odr
# 0            1  Alice  New York       101     250      NYC
# 1            1  Alice  New York       103     320      NYC
# 2            2    Bob    Boston       102     180      BOS
'''Here, only customer id "1" and "2" are returned, as they exist in both DataFrames.'''

#################################
##    pd.merge(how='outer')    ##
#################################
'''how='outer': keeps all rows from both DataFrames, filling in NaNs for missing matches'''

df_merged_outer = pd.merge(
    left=customers,
    right=orders,
    on='customer_id',
    how='outer', # Keep all rows from both DataFrames
    suffixes=('_cst', '_odr')
)

print(df_merged_outer)
#    customer_id     name  city_cst  order_id  amount city_odr
# 0            1    Alice  New York     101.0   250.0      NYC
# 1            1    Alice  New York     103.0   320.0      NYC
# 2            2      Bob    Boston     102.0   180.0      BOS
# 3            3  Charlie   Chicago       NaN     NaN      NaN
# 4            4    Diana     Miami       NaN     NaN      NaN
# 5            5      NaN       NaN     105.0   150.0      MIA
'''Here, the "3", "4" and "5" customer_ids are included, though they are not present in both DataFrames.'''

################################
##    pd.merge(how='left')    ##
################################
'''how='left': keeps all rows from the left DataFrame and matches from the right DataFrame'''

df_merged_left = pd.merge(
    left=customers,
    right=orders,
    on='customer_id',
    how='left', # Keep all rows from the left DataFrame
    suffixes=('_cst', '_odr')
)

print(df_merged_left)
#    customer_id     name  city_cst  order_id  amount city_odr
# 0            1    Alice  New York     101.0   250.0      NYC
# 1            1    Alice  New York     103.0   320.0      NYC
# 2            2      Bob    Boston     102.0   180.0      BOS
# 3            3  Charlie   Chicago       NaN     NaN      NaN
# 4            4    Diana     Miami       NaN     NaN      NaN

#################################
##    pd.merge(how='right')    ##
#################################
'''how='right': keeps all rows from the right DataFrame and matches from the left DataFrame'''

df_merged_right = pd.merge(
    left=customers,
    right=orders,
    on='customer_id',
    how='right', # Keep all rows from the right DataFrame
    suffixes=('_cst', '_odr')
)

print(df_merged_right)
#    customer_id   name  city_cst  order_id  amount city_odr
# 0            1  Alice  New York       101     250      NYC
# 1            2    Bob    Boston       102     180      BOS
# 2            1  Alice  New York       103     320      NYC
# 3            5    NaN       NaN       105     150      MIA

#######################################
##    pd.merge(left_on, right_on)    ##
#######################################
'''Merge DataFrames based on different columns from each DataFrame'''

# Create sample DataFrames with matchiing keys in different columns
customers_key = pd.DataFrame(
    {
        "customer_id": [1, 2, 3, 4],
        "name"       : ["Alice", "Bob", "Charlie", "Diana"],
        "city"       : ["New York", "Boston", "Chicago", "Miami"]
    }
)

orders_key = pd.DataFrame(
    {
        "order_id": [101, 102, 103, 105],
        "cst_id": [1, 2, 1, 5],
        "amount"  : [250, 180, 320, 150],
        "city"    : ["NYC", "BOS", "NYC", "MIA"]
    }
)

# Merge customers and orders where 'customer_id' in customers matches 'cst_id' in orders
df_merged_diff_keys = pd.merge(
    left=customers_key,
    right=orders_key,
    left_on='customer_id',  # Key column from the left DataFrame
    right_on='cst_id',      # Key column from the right DataFrame
    how='inner',            # Only keep rows with matching keys in both DataFrames
    suffixes=('_cst', '_odr')
)

print(df_merged_diff_keys)
#    customer_id   name  city_cst  order_id  cst_id  amount city_odr
# 0            1  Alice  New York       101       1     250      NYC
# 1            1  Alice  New York       103       1     320      NYC
# 2            2    Bob    Boston       102       2     180      BOS

#############################################
##    pd.merge(left_index, right_index)    ##
#############################################
'''Merge DataFrames based on their index'''

# Create sample DataFrames with matching indices
customers_idx = pd.DataFrame(
    {
        "name"       : ["Alice", "Bob", "Charlie", "Diana"],
        "city"       : ["New York", "Boston", "Chicago", "Miami"]
    },
    index=[1, 2, 3, 4] # Set custom index
)

orders_idx = pd.DataFrame(
    {
        "order_id": [101, 102, 103, 105],
        "amount"  : [250, 180, 320, 150],
        "city"    : ["NYC", "BOS", "NYC", "MIA"]
    },
    index=[1, 2, 1, 5] # Set custom index
)

# Merge customers and orders based on their index
df_merged_index = pd.merge(
    left=customers_idx,
    right=orders_idx,
    left_index=True,   # Use index from the left DataFrame
    right_index=True,  # Use index from the right DataFrame
    how='inner',       # Only keep rows with matching indices in both DataFrames
    suffixes=('_cst', '_odr')
)

print(df_merged_index)
#     name  city_cst  order_id  amount city_odr
# 1  Alice  New York       101     250      NYC
# 1  Alice  New York       103     320      NYC
# 2    Bob    Boston       102     180      BOS

#################################
##    pd.merge(how='cross')    ##
#################################
'''
how='cross': creates the Cartesian product of both DataFrames

NOTE: This option does not allow specifying 'on', 'left_on', 'right_on', 'left_index', or 'right_index'.
'''

df_left = pd.DataFrame({'left': ['foo', 'bar']})
print(df_left)
#   left
# 0  foo
# 1  bar

df_right = pd.DataFrame({'right': [7, 8]})
print(df_right)
#    right
# 0      7
# 1      8

# Merge df_left and df_right to create Cartesian product
df_merged_cross = pd.merge(
    left=df_left,
    right=df_right,
    how='cross' # Create Cartesian product of both DataFrames
)

print(df_merged_cross)
#   left  right
# 0  foo      7
# 1  foo      8
# 2  bar      7
# 3  bar      8

#######################
##    df.merge()     ##
#######################
''' Instance method to merge DataFrames '''

# customers.merge(order,...)
print(customers.merge(orders, on='customer_id', how='inner', suffixes=('_cst', '_odr')))
#    customer_id   name  city_cst  order_id  amount city_odr
# 0            1  Alice  New York       101     250      NYC
# 1            1  Alice  New York       103     320      NYC
# 2            2    Bob    Boston       102     180      BOS


#------------------------------------------------------------------------------------------------------#
#----------------------------------------- 3. Combining -----------------------------------------------#
#------------------------------------------------------------------------------------------------------#

df1 = pd.DataFrame({'A': [0, 0], 'B': [4, 4]})
print(df1)
#    A  B
# 0  0  4
# 1  0  4

df2 = pd.DataFrame({'A': [1, 1], 'B': [3, 3]})
print(df2)
#    A  B
# 0  1  3
# 1  1  3

#######################
##    df.combine()   ##
#######################
''' Combines a DataFrame with other DataFrame using func to element-wise combine columns '''

# Combine df1 and df2 by taking the maximum value for each element
df_combined = df1.combine(
    other=df2,
    func=np.maximum # Function to apply element-wise
)
print(df_combined)
#    A  B
# 0  1  4
# 1  1  4

# Combine df1 and df2 by taking the mean value for each element
df_combined = df1.combine(
    other=df2,
    func=lambda s1, s2: (s1 + s2) / 2 # Custom function to compute mean
)
print(df_combined)
#      A    B
# 0  0.5  3.5
# 1  0.5  3.5