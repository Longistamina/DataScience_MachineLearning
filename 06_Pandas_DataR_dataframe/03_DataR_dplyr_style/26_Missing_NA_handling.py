'''
1. dr.complete()

2. Drop columns having too much NA (>1/3)

3. dr.drop_na()

4. dr.replace_na()

5. dr.fill()

6. dr.coalesce()

7. Using Pandas method with dr.pipe()
'''

import re

import datar.all as dr
from datar import f
import pandas as pd

from pipda import register_verb
dr.filter = register_verb(func=dr.filter_)

###################################################

tb_mkt = dr.tibble(
    pd.read_csv('05_Pandas_DataR_dataframe/data/marketing_data.csv')
    >> dr.rename_with(lambda col: re.sub("\\s+|\\.", "_", col.strip().lower()))
)


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 1. dr.complete() ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Turns implicit missing values into explicit missing values 
by expanding your data frame to include all possible combinations of specified columns.

Parameters:
# data: Your data frame
# *args: Columns to expand (all combinations will be generated)
# fill: A dict specifying values to use instead of NA for missing combinations
# explict: Boolean (default True) - whether to fill both implicit and explicit NAs
'''

tb_na = dr.tibble(
    year = [2010, 2010, 2012, 2012],
    quarter = [1, 2, 1, 3],
    value = [10, 20, 30, 40]
)

print(tb_na)
#      year  quarter   value
#   <int64>  <int64> <int64>
# 0    2010        1      10
# 1    2010        2      20
# 2    2012        1      30
# 3    2012        3      40

###################################
##         dr.complete()         ##
###################################

print(
    tb_na
    >> dr.complete(f.year, f.quarter)
)
#      year  quarter     value
#   <int64>  <int64> <float64>
# 0    2010        1      10.0
# 1    2010        2      20.0
# 2    2010        3       NaN
# 3    2012        1      30.0
# 4    2012        2       NaN
# 5    2012        3      40.0
'''dr.complete() expanded the data frame to include all combinations of year and quarter.'''

###################################
##       dr.complete(fill=)      ##
###################################

print(
    tb_na
    >> dr.complete(f.year, f.quarter, fill={"value": 'unknown'})
)
#      year  quarter    value
#   <int64>  <int64> <object>
# 0    2010        1     10.0
# 1    2010        2     20.0
# 2    2010        3  unknown
# 3    2012        1     30.0
# 4    2012        2  unknown
# 5    2012        3     40.0


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 2. Drop columns having too much NA (>1/3) ----------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#########################
##   NA count check    ##
#########################

print(tb_mkt.shape[1])
# 26 columns

print(
    tb_mkt
    >> dr.pipe(lambda f: f.isna().sum())
    >> dr.pipe(lambda s: s[s > 0]) # Show only columns with NAs
)
# top_of_mind                   33
# spontaneous                   33
# aided                         33
# penetration                   33
# competitor                    45
# grp_radio                    142
# reach_radio                  142
# grp_tv                       104
# reach_tv                     104
# reach_cinema                 138
# grp_outdoor                  155
# grp_print                    134
# share_of_spend                40
# dtype: int64

##########################################
##   Drop columns having too much NA    ##
##########################################

print(
    tb_mkt
    >> dr.select(
        dr.where(
            lambda col: (col.isna().sum() / len(col)) <= (1/3)
        )
    )
    >> dr.slice_tail(n=5)
)
#        week    year  market_share  av_price_per_kg  non-promo_price_per_kg       spontaneous     aided  penetration  competitor  share_of_spend
#     <int64> <int64>     <float64>        <float64>               <float64>  ...    <float64> <float64>    <float64>   <float64>       <float64>
# 151      14    2013         33.26             7.63                    7.66  ...         83.7      99.5         71.6         4.6             NaN
# 152      15    2013         33.99             7.59                    7.64  ...         83.7      99.5         71.6         4.7             NaN
# 153      16    2013         30.57             7.66                    7.68  ...         83.7      99.5         71.6         4.6             NaN
# 154      17    2013         32.24             7.63                    7.66  ...         83.7      99.5         71.6         4.7             NaN
# 155      18    2013         34.63             7.61                    7.61  ...         83.7      99.5         71.6         5.0             NaN

# [5 rows x 19 columns]

'''
grp_radio, reach_radio, grp_tv, reach_tv, reach_cinema, grp_outdoor, grp_print columns are dropped 
as they have more than 1/3 NA values.
'''


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 3. dr.drop_na() --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

tb_mkt_dropped = (
    tb_mkt
    >> dr.select(
        dr.where(
            lambda col: (col.isna().sum() / len(col)) <= (1/3)
        )
    )
)

print(tb_mkt_dropped.shape)
# (156, 19)

'''
Purpose: Drop rows containing missing values in specified columns.

Parameters:
# _data: Your data frame
# *columns: Columns to inspect for missing values (if none specified, checks all columns)
# how_: Either 'any' (default) or 'all'
        'any': Drop row if ANY specified column has NA
        'all': Drop row only if ALL specified columns have NA
'''

#####################################
##     dr.drop_na(how_='any')      ##
#####################################

#---
## All columns
#---

print(
    tb_mkt_dropped
    >> dr.drop_na(how_='any')
)
#        week    year  market_share  av_price_per_kg  non-promo_price_per_kg       spontaneous     aided  penetration  competitor  share_of_spend
#     <int64> <int64>     <float64>        <float64>               <float64>  ...    <float64> <float64>    <float64>   <float64>       <float64>
# 0        12    2011         39.05             7.34                    7.69  ...         68.6      95.7         70.0         0.0       63.886185
# 1        13    2011         37.52             7.37                    7.67  ...         68.6      95.7         70.0         0.2       79.064596
# 2        14    2011         33.80             7.39                    7.55  ...         78.7      98.0         71.8         0.2       92.590148
# 3        15    2011         35.40             7.35                    7.55  ...         78.7      98.0         71.8         0.4       13.358451
# ..      ...     ...           ...              ...                     ...  ...          ...       ...          ...         ...             ...
# 4        16    2011         35.29             7.37                    7.54  ...         78.7      98.0         71.8         0.5        8.708819
# 100       8    2013         33.45             7.65                    7.69  ...         77.5      99.5         71.2         6.1       45.222828
# 101       9    2013         34.57             7.64                    7.67  ...         77.5      99.5         71.2         5.8       82.679470
# 102      10    2013         32.03             7.65                    7.69  ...         76.0      98.2         62.4         5.1       97.452067
# 103      11    2013         32.17             7.67                    7.70  ...         76.0      98.2         62.4         5.0       68.861555
# 104      12    2013         33.81             7.65                    7.74  ...         76.0      98.2         62.4         4.7       84.546201

# [105 rows x 19 columns]

#---
## Specified columns
#---

print(
    tb_mkt_dropped
    >> dr.drop_na(f.competitor, f.share_of_spend, how_='any')
)
#        week    year  market_share  av_price_per_kg  non-promo_price_per_kg       spontaneous     aided  penetration  competitor  share_of_spend
#     <int64> <int64>     <float64>        <float64>               <float64>  ...    <float64> <float64>    <float64>   <float64>       <float64>
# 0        12    2011         39.05             7.34                    7.69  ...         68.6      95.7         70.0         0.0       63.886185
# 1        13    2011         37.52             7.37                    7.67  ...         68.6      95.7         70.0         0.2       79.064596
# 2        14    2011         33.80             7.39                    7.55  ...         78.7      98.0         71.8         0.2       92.590148
# 3        15    2011         35.40             7.35                    7.55  ...         78.7      98.0         71.8         0.4       13.358451
# ..      ...     ...           ...              ...                     ...  ...          ...       ...          ...         ...             ...
# 4        16    2011         35.29             7.37                    7.54  ...         78.7      98.0         71.8         0.5        8.708819
# 100       8    2013         33.45             7.65                    7.69  ...         77.5      99.5         71.2         6.1       45.222828
# 101       9    2013         34.57             7.64                    7.67  ...         77.5      99.5         71.2         5.8       82.679470
# 102      10    2013         32.03             7.65                    7.69  ...         76.0      98.2         62.4         5.1       97.452067
# 103      11    2013         32.17             7.67                    7.70  ...         76.0      98.2         62.4         5.0       68.861555
# 104      12    2013         33.81             7.65                    7.74  ...         76.0      98.2         62.4         4.7       84.546201

# [105 rows x 19 columns]

#####################################
##     dr.drop_na(how_='all')      ##
#####################################

#---
## All columns
#---

print(
    tb_mkt_dropped
    >> dr.drop_na(how_='all')
)
# [156 rows x 19 columns]
'''No rows are dropped as there is no row with all NAs.'''

#---
## Specified columns
#---

print(
    tb_mkt_dropped
    >> dr.drop_na(f.competitor, f.share_of_spend, how_='all')
)
#        week    year  market_share  av_price_per_kg  non-promo_price_per_kg       spontaneous     aided  penetration  competitor  share_of_spend
#     <int64> <int64>     <float64>        <float64>               <float64>  ...    <float64> <float64>    <float64>   <float64>       <float64>
# 0         1    2011         33.35             7.50                    7.61  ...         77.9      98.1          0.0         NaN       79.185402
# 1         2    2011         30.94             7.48                    7.60  ...         77.9      98.1          0.0         NaN      100.000000
# 2         3    2011         36.00             7.38                    7.60  ...         77.9      98.1          0.0         NaN      100.000000
# 3         4    2011         34.41             7.46                    7.56  ...         77.9      98.1          0.0         NaN       99.015859
# ..      ...     ...           ...              ...                     ...  ...          ...       ...          ...         ...             ...
# 4         5    2011         34.25             7.46                    7.52  ...         77.9      98.1          0.0         NaN       77.376728
# 117      14    2013         33.26             7.63                    7.66  ...         83.7      99.5         71.6         4.6             NaN
# 118      15    2013         33.99             7.59                    7.64  ...         83.7      99.5         71.6         4.7             NaN
# 119      16    2013         30.57             7.66                    7.68  ...         83.7      99.5         71.6         4.6             NaN
# 120      17    2013         32.24             7.63                    7.66  ...         83.7      99.5         71.6         4.7             NaN
# 121      18    2013         34.63             7.61                    7.61  ...         83.7      99.5         71.6         5.0             NaN

# [122 rows x 19 columns]
'''Rows where both competitor and share_of_spend are NA are dropped.'''


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 4. dr.replace_na() -------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Purpose: Replace NA values with specified values.

Parameters:
# data: Data frame or vector
# data_or_replace: When used as a verb, this is the data; otherwise it's the replacement value
# replace: Dict (for data frames) mapping column names to replacement values, or scalar (for vectors)

Important note: For data frames, replace must be a dict like {'column_name': value}. 
You cannot replace all NAs at once with a single scalar value (unlike some pandas methods).
'''

tb_empty = dr.tibble(
    x=[1, 2, None],
    y=['a', None, 'b']
)

print(tb_empty)
#           x        y
#   <float64> <object>
# 0       1.0        a
# 1       2.0     None
# 2       NaN        b

##############################
##     dr.replace_na()      ##
##############################

print(
    tb_empty
    >> dr.replace_na(replace={ 'x': 0, 'y': 'unknown' })
)
#           x        y
#   <float64> <object>
# 0       1.0        a
# 1       2.0  unknown
# 2       0.0        b

print(
    tb_empty
    >> dr.mutate(x = dr.replace_na(f.x, replace='empty')) # Single column replacement
)
#          x        y
#   <object> <object>
# 0      1.0        a
# 1      2.0     None
# 2    empty        b


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 5. dr.fill() -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Fill missing values using the previous or next non-NA value (forward fill or backward fill).

Parameters:
# _data: Your data frame
# *columns: Columns to fill
# _direction: Direction to fill - 'down' (default), 'up', 'downup', or 'updown'
'''

tb_fill = dr.tibble(
    group = [None, 'A', None, 'B', None],
    value = [1, 2, 3, 4, 5]
)

print(tb_fill)
#      group   value
#   <object> <int64>
# 0     None       1
# 1        A       2
# 2     None       3
# 3        B       4
# 4     None       5

###########################################
##       dr.fill(_direction='down')      ##
###########################################

print(
    tb_fill
    >> dr.fill(f.group, _direction='down')
)
#      group   value
#   <object> <int64>
# 0     None       1
# 1        A       2
# 2        A       3
# 3        B       4
# 4        B       5

###########################################
##        dr.fill(_direction='up')       ##
###########################################

print(
    tb_fill
    >> dr.fill(f.group, _direction='up')
)
#      group   value
#   <object> <int64>
# 0        A       1
# 1        A       2
# 2        B       3
# 3        B       4
# 4     None       5

##########################################
##     dr.fill(_direction='downup')     ##
##########################################

print(
    tb_fill
    >> dr.fill(f.group, _direction='downup')
)
#      group   value
#   <object> <int64>
# 0        A       1
# 1        A       2
# 2        A       3
# 3        B       4
# 4        B       5

'''First fills downwards, then upwards.'''

###########################################
##      dr.fill(_direction='updown')     ##
###########################################

print(
    tb_fill
    >> dr.fill(f.group, _direction='updown')
)
#      group   value
#   <object> <int64>
# 0        A       1
# 1        A       2
# 2        B       3
# 3        B       4
# 4        B       5

'''First fills upwards, then downwards.'''


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 6. dr.coalesce() ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Replace missing values with the given values in order.

Parameters:
# x: A vector
# *replace: Values to replace missing values with.
'''

tb_coalesce = dr.tibble(
    x=[1, None, None, 4],
    y=[None, 2, None, 5],
    z=[10, 20, 30, 40]
)

print(tb_coalesce)
#           x         y       z
#   <float64> <float64> <int64>
# 0       1.0       NaN      10
# 1       NaN       2.0      20
# 2       NaN       NaN      30
# 3       4.0       5.0      40

##############################
##      dr.coalesce()       ##
##############################

print(
    tb_coalesce
    >> dr.mutate(y = dr.coalesce(f.y, 'empty'))
)
#           x        y       z
#   <float64> <object> <int64>
# 0       1.0    empty      10
# 1       NaN      2.0      20
# 2       NaN    empty      30
# 3       4.0      5.0      40

print(
    tb_coalesce
    >> dr.mutate(x = dr.coalesce(f.x, f.z)) # Replace NA in x with values from z
)
#           x         y       z
#   <float64> <float64> <int64>
# 0       1.0       NaN      10
# 1      20.0       2.0      20
# 2      30.0       NaN      30
# 3       4.0       5.0      40

print(
    tb_coalesce
    >> dr.mutate(x = dr.coalesce(f.x, f.y, f.z)) # Replace NA in x with values from y, then z
)
#           x         y       z
#   <float64> <float64> <int64>
# 0       1.0       NaN      10
# 1       2.0       2.0      20
# 2      30.0       NaN      30
# 3       4.0       5.0      40

#--------------------------------------------------------------------------------------------------------------#
#------------------------------------ 7. Using Pandas method with dr.pipe() -----------------------------------#
#--------------------------------------------------------------------------------------------------------------#

print(
    tb_mkt_dropped
    >> dr.pipe(lambda f: f.ffill().bfill())  # Fill NAs using Pandas interpolate()
    >> dr.slice_head(n=5)
)
#      week    year  market_share  av_price_per_kg  non-promo_price_per_kg       spontaneous     aided  penetration  competitor  share_of_spend
#   <int64> <int64>     <float64>        <float64>               <float64>  ...    <float64> <float64>    <float64>   <float64>       <float64>
# 0      19    2010         38.40             7.61                    7.77  ...         77.9      98.1          0.0         0.0       79.185402
# 1      20    2010         36.80             7.60                    7.80  ...         77.9      98.1          0.0         0.0       79.185402
# 2      21    2010         35.21             7.63                    7.85  ...         77.9      98.1          0.0         0.0       79.185402
# 3      22    2010         35.03             7.22                    7.76  ...         77.9      98.1          0.0         0.0       79.185402
# 4      23    2010         32.37             7.70                    7.78  ...         77.9      98.1          0.0         0.0       79.185402
