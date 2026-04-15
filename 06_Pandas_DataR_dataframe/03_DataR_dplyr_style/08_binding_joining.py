'''
1. Binding:
  + dr.bind_rows()
  + dr.bind_cols()

2. Joining:
  + dr.inner_join()
  + dr.left_join()
  + dr.right_join()
  + dr.full_join()
  + dr.semi_join()
  + dr.anti_join()
  + dr.cross_join()
  + dr.nest_join()
'''

import datar.all as dr
from datar import f
import pandas as pd


#-----------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 1. Binding ------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

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

####################
## dr.bind_rows() ##
####################

# Original DataFrame
print(df_origin)
#     A   B   C
# 0  A0  B0  C0
# 1  A1  B1  C1
# 2  A2  B2  C2
# 3  A3  B3  C3

df_bind_rows = dr.bind_rows(df_origin, df_ver_1)
print(df_bind_rows)
#          A        B        C
#   <object> <object> <object>
# 0       A0       B0       C0
# 1       A1       B1       C1
# 2       A2       B2       C2
# 3       A3       B3       C3
# 4       A4       B4       C4
# 5       A5       B5       C5
# 6       A6       B6       C6
# 7       A7       B7       C7

df_bind_rows = dr.bind_rows(df_origin, df_ver_1, df_ver_2)
print(df_bind_rows)
#          A        B        C
#    <object> <object> <object>
# 0        A0       B0       C0
# 1        A1       B1       C1
# 2        A2       B2       C2
# 3        A3       B3       C3
# 4        A4       B4       C4
# 5        A5       B5       C5
# 6        A6       B6       C6
# 7        A7       B7       C7
# 8        A8       B8       C8
# 9        A9       B9       C9
# 10      A10      B10      C10
# 11      A11      B11      C11

####################
## dr.bind_cols() ##
####################

# Original DataFrame
print(df_origin)
#     A   B   C
# 0  A0  B0  C0
# 1  A1  B1  C1
# 2  A2  B2  C2
# 3  A3  B3  C3

df_bind_cols = dr.bind_cols(df_origin, df_hor_1)
print(df_bind_cols)
#          A        B        C        D        E        F
#   <object> <object> <object> <object> <object> <object>
# 0       A0       B0       C0       D0       E0       F0
# 1       A1       B1       C1       D1       E1       F1
# 2       A2       B2       C2       D2       E2       F2
# 3       A3       B3       C3       D3       E3       F3

df_bind_cols = dr.bind_cols(df_origin, df_hor_1, df_hor_2)
print(df_bind_cols)
#          A        B        C        D        E        F        G        H        I
#   <object> <object> <object> <object> <object> <object> <object> <object> <object>
# 0       A0       B0       C0       D0       E0       F0       G0       H0       I0
# 1       A1       B1       C1       D1       E1       F1       G1       H1       I1
# 2       A2       B2       C2       D2       E2       F2       G2       H2       I2
# 3       A3       B3       C3       D3       E3       F3       G3       H3       I3


#-----------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 2. Joining ------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

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

#####################
## dr.inner_join() ##
#####################
'''
only keeps rows whose keys are present in both DataFrames/Tibbles

by= column name(s) to join on. If NULL, the default, joins on columns with the same names in x and y.
suffix= suffix to append to overlapping column names in x and y.
'''

print(
    customers 
    >> dr.inner_join(orders, by="customer_id")
)
#    customer_id     name    city_x  order_id  amount   city_y
#        <int64> <object>  <object>   <int64> <int64> <object>
# 0            1    Alice  New York       101     250      NYC
# 1            1    Alice  New York       103     320      NYC
# 2            2      Bob    Boston       102     180      BOS

print(
    customers 
    >> dr.inner_join(orders, by="customer_id", suffix=["_cst", "_ord"])
)
#    customer_id     name  city_cst  order_id  amount city_ord
#        <int64> <object>  <object>   <int64> <int64> <object>
# 0            1    Alice  New York       101     250      NYC
# 1            1    Alice  New York       103     320      NYC
# 2            2      Bob    Boston       102     180      BOS

####################
## dr.left_join() ##
####################
'''keeps all rows from the left DataFrame and matches from the right DataFrame'''

print(
    customers 
    >> dr.left_join(orders, by="customer_id", suffix=["_cst", "_ord"])
)
#    customer_id     name  city_cst  order_id    amount city_ord
#        <int64> <object>  <object> <float64> <float64> <object>
# 0            1    Alice  New York     101.0     250.0      NYC
# 1            1    Alice  New York     103.0     320.0      NYC
# 2            2      Bob    Boston     102.0     180.0      BOS
# 3            3  Charlie   Chicago       NaN       NaN      NaN
# 4            4    Diana     Miami       NaN       NaN      NaN

#####################
## dr.right_join() ##
#####################
'''keeps all rows from the right DataFrame and matches from the left DataFrame'''

print(
    customers 
    >> dr.right_join(orders, by="customer_id", suffix=["_cst", "_ord"])
)
#    customer_id     name  city_cst  order_id  amount city_ord
#        <int64> <object>  <object>   <int64> <int64> <object>
# 0            1    Alice  New York       101     250      NYC
# 1            2      Bob    Boston       102     180      BOS
# 2            1    Alice  New York       103     320      NYC
# 3            5      NaN       NaN       105     150      MIA

####################
## dr.full_join() ##
####################
'''keeps all rows from both DataFrames, filling in NaNs where there are no matches'''

print(
    customers 
    >> dr.full_join(orders, by="customer_id", suffix=["_cst", "_ord"])
)
#    customer_id     name  city_cst  order_id    amount city_ord
#        <int64> <object>  <object> <float64> <float64> <object>
# 0            1    Alice  New York     101.0     250.0      NYC
# 1            1    Alice  New York     103.0     320.0      NYC
# 2            2      Bob    Boston     102.0     180.0      BOS
# 3            3  Charlie   Chicago       NaN       NaN      NaN
# 4            4    Diana     Miami       NaN       NaN      NaN
# 5            5      NaN       NaN     105.0     150.0      MIA

####################
## dr.semi_join() ##
####################
'''
# semi_join(x, y) return all rows from x with a match in y
# (meaning the output only shows the information of x)
'''

print(
    customers 
    >> dr.semi_join(orders, by="customer_id")
)
#    customer_id     name      city
#        <int64> <object>  <object>
# 0            1    Alice  New York
# 1            2      Bob    Boston

####################
## dr.anti_join() ##
####################
'''
# anti_join(x, y) return all rows from x without a match in y
# (meaning the output only shows the information of x)
'''

print(
    customers 
    >> dr.anti_join(orders, by="customer_id")
)
#    customer_id     name     city
#        <int64> <object> <object>
# 3            3  Charlie  Chicago
# 4            4    Diana    Miami

#####################
## dr.cross_join() ##
#####################
'''creates the Cartesian product of both DataFrames'''

print(
    customers 
    >> dr.cross_join(orders, suffix=["_cst", "_ord"])
)
#     customer_id_cst     name  city_cst  order_id  customer_id_ord  amount city_ord
#             <int64> <object>  <object>   <int64>          <int64> <int64> <object>
# 0                 1    Alice  New York       101                1     250      NYC
# 1                 1    Alice  New York       102                2     180      BOS
# 2                 1    Alice  New York       103                1     320      NYC
# 3                 1    Alice  New York       105                5     150      MIA
# 4                 2      Bob    Boston       101                1     250      NYC
# 5                 2      Bob    Boston       102                2     180      BOS
# 6                 2      Bob    Boston       103                1     320      NYC
# 7                 2      Bob    Boston       105                5     150      MIA
# 8                 3  Charlie   Chicago       101                1     250      NYC
# 9                 3  Charlie   Chicago       102                2     180      BOS
# 10                3  Charlie   Chicago       103                1     320      NYC
# 11                3  Charlie   Chicago       105                5     150      MIA
# 12                4    Diana     Miami       101                1     250      NYC
# 13                4    Diana     Miami       102                2     180      BOS
# 14                4    Diana     Miami       103                1     320      NYC
# 15                4    Diana     Miami       105                5     150      MIA

####################
## dr.nest_join() ##
####################
'''
# nest_join(x, y) leaves x almost unchanged, except that it adds a new list-column, 
# where each element contains the rows from y that match the corresponding row in x
'''

print(
    customers 
    >> dr.nest_join(orders, by="customer_id", name="orders_data")
)
#    customer_id     name      city orders_data
#        <int64> <object>  <object>    <object>
# 0            1    Alice  New York    <DF 2x3>
# 1            2      Bob    Boston    <DF 1x3>
# 2            3  Charlie   Chicago    <DF 0x3>
# 3            4    Diana     Miami    <DF 0x3>

'''
# It creates a new columns named "orders_data" defined by "name = ..." parameter
# This column stores a list of y indices where y matches x
'''