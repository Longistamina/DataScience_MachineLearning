'''
1. Detect missing values:
   + df.isna() or df.isnull(): Returns a DataFrame of the same shape as df, with True for missing values
   + df.isna().sum() or df.isnull().sum(): Returns the count of missing values in each column
   + df.info(): Provides a summary of the DataFrame, including non-null counts

2. Detect non-missing values:
   + df.notna() or df.notnull(): Returns a DataFrame of the same shape as df, with True for non-missing values
   + df.notna().sum() or df.notnull().sum(): Returns the count of non-missing values in each column

3. Drop missing values along columns:
   + df.dropna(axis=1, how=...)
   + df.dropna(axis=1, thresh=...): drop columns having too much missing values
  
4. Drop missing values along rows:
   + df.dropna(axis=0, how=...)
   + df.dropna(axis=0, subset=...)

5. Fill missing values:
   + df.fillna(value): Returns a DataFrame with missing values filled with the specified value
   + df.fillna({dictionary}): Fill different columns with different values
   + df.fillna(df.mean()): Fill missing values with the mean of each column
   + df.ffill(): Fill missing values using forward fill method
   + df.bfill(): Fill missing values using backward fill method

6. Interpolate missing values:
  + df.interpolate(axis=0, limit_direction='both'): linear interpolation
  + df.interpolate(method = "polynomial", order = n): polynomial interpolation of order n
  + df.interpolate(method = "spline", order = n): spline interpolation of order n
  + df.interpolate(method = "time"): time-based interpolation (requires a datetime index)
  + df.interpolate(method = "nearest"): nearest neighbor interpolation

7. Conditional filling: df['C'] = np.where(df['C'].isna(), df['A'] + df['B'], df['C'])

8. Group-based filling, transform
  + df_group_filled = df_missing.fillna(df_missing.groupby("week").transform("mean"))
'''

import pandas as pd
import numpy as np

df_mkt = (
    pd.read_csv(
        filepath_or_buffer = "05_Pandas_DataR_dataframe/data/marketing_data.csv",
        dtype = {"week": "category", "Year": "category"}
    )
    .pipe(
        lambda df: df.set_axis(
            df.columns.str.lower().str.strip().str.replace(r"[^a-zA-Z]", "_", regex = True), 
            axis = 1
        )
    )
)

print(df_mkt.info())
# RangeIndex: 156 entries, 0 to 155
# Data columns (total 26 columns):
#  #   Column                     Non-Null Count  Dtype   
# ---  ------                     --------------  -----   
#  0   week                       156 non-null    category
#  1   year                       156 non-null    category
#  2   market_share               156 non-null    float64 
#  3   av_price_per_kg            156 non-null    float64 
#  4   non_promo_price_per_kg     156 non-null    float64 
#  5   promo_vol_share            156 non-null    float64 
#  6   total_weigh                156 non-null    int64   
#  7   share_of_ean_weigh         156 non-null    float64 
#  8   avg_price_vs_plb           156 non-null    float64 
#  9   non_promo_price_vs_plb     156 non-null    float64 
#  10  promo_vol_sh_index_vs_plb  156 non-null    float64 
#  11  total_cm_shelf             156 non-null    float64 
#  12  shelf_share                156 non-null    float64 
#  13  top_of_mind                123 non-null    float64 
#  14  spontaneous                123 non-null    float64 
#  15  aided                      123 non-null    float64 
#  16  penetration                123 non-null    float64 
#  17  competitor                 111 non-null    float64 
#  18  grp_radio                  14 non-null     float64 
#  19  reach_radio                14 non-null     float64 
#  20  grp_tv                     52 non-null     float64 
#  21  reach_tv                   52 non-null     float64 
#  22  reach_cinema               18 non-null     float64 
#  23  grp_outdoor                1 non-null      float64 
#  24  grp_print                  22 non-null     float64 
#  25  share_of_spend             116 non-null    float64 
# dtypes: category(2), float64(23), int64(1)
# memory usage: 32.2 KB


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. Detect missing values --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##############################
## df.isna() or df.isnull() ##
##############################
'''Returns a DataFrame of the same shape as df, with True for missing values'''

print(df_mkt.isna().head())
#     week   year  market_share  av_price_per_kg  ...  reach_cinema  grp_outdoor  grp_print  share_of_spend
# 0  False  False         False            False  ...          True         True       True            True
# 1  False  False         False            False  ...          True         True       True            True
# 2  False  False         False            False  ...          True         True       True            True
# 3  False  False         False            False  ...          True         True       True            True
# 4  False  False         False            False  ...          True         True       True            True

print(df_mkt.isnull().head())
#     week   year  market_share  av_price_per_kg  ...  reach_cinema  grp_outdoor  grp_print  share_of_spend
# 0  False  False         False            False  ...          True         True       True            True
# 1  False  False         False            False  ...          True         True       True            True
# 2  False  False         False            False  ...          True         True       True            True
# 3  False  False         False            False  ...          True         True       True            True
# 4  False  False         False            False  ...          True         True       True            True

##########################################
## df.isna().sum() or df.isnull().sum() ##
##########################################
'''Returns the count of missing values in each column'''

print(df_mkt.isna().sum())
# week                           0
# year                           0
# market_share                   0
# av_price_per_kg                0
# non_promo_price_per_kg         0
# promo_vol_share                0
# total_weigh                    0
# share_of_ean_weigh             0
# avg_price_vs_plb               0
# non_promo_price_vs_plb         0
# promo_vol_sh_index_vs_plb      0
# total_cm_shelf                 0
# shelf_share                    0
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

print(df_mkt.isnull().sum())
# week                           0
# year                           0
# market_share                   0
# av_price_per_kg                0
# non_promo_price_per_kg         0
# promo_vol_share                0
# total_weigh                    0
# share_of_ean_weigh             0
# avg_price_vs_plb               0
# non_promo_price_vs_plb         0
# promo_vol_sh_index_vs_plb      0
# total_cm_shelf                 0
# shelf_share                    0
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

###############
## df.info() ##
###############
'''Provides a summary of the DataFrame, including non-null counts'''

print(df_mkt.info())
# RangeIndex: 156 entries, 0 to 155
# Data columns (total 26 columns):
#  #   Column                     Non-Null Count  Dtype   
# ---  ------                     --------------  -----   
#  0   week                       156 non-null    category
#  1   year                       156 non-null    category
#  2   market_share               156 non-null    float64 
#  3   av_price_per_kg            156 non-null    float64 
#  4   non_promo_price_per_kg     156 non-null    float64 
#  5   promo_vol_share            156 non-null    float64 
#  6   total_weigh                156 non-null    int64   
#  7   share_of_ean_weigh         156 non-null    float64 
#  8   avg_price_vs_plb           156 non-null    float64 
#  9   non_promo_price_vs_plb     156 non-null    float64 
#  10  promo_vol_sh_index_vs_plb  156 non-null    float64 
#  11  total_cm_shelf             156 non-null    float64 
#  12  shelf_share                156 non-null    float64 
#  13  top_of_mind                123 non-null    float64 
#  14  spontaneous                123 non-null    float64 
#  15  aided                      123 non-null    float64 
#  16  penetration                123 non-null    float64 
#  17  competitor                 111 non-null    float64 
#  18  grp_radio                  14 non-null     float64 
#  19  reach_radio                14 non-null     float64 
#  20  grp_tv                     52 non-null     float64 
#  21  reach_tv                   52 non-null     float64 
#  22  reach_cinema               18 non-null     float64 
#  23  grp_outdoor                1 non-null      float64 
#  24  grp_print                  22 non-null     float64 
#  25  share_of_spend             116 non-null    float64 
# dtypes: category(2), float64(23), int64(1)
# memory usage: 32.2 KB


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. Detect non-missing values ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#################################
## df.notna() or df.notnull()  ##
#################################
'''Returns a DataFrame of the same shape as df, with True for non-missing values'''

print(df_mkt.notna().head())
#    week  year  market_share  av_price_per_kg  ...  reach_cinema  grp_outdoor  grp_print  share_of_spend
# 0  True  True          True             True  ...         False        False      False           False
# 1  True  True          True             True  ...         False        False      False           False
# 2  True  True          True             True  ...         False        False      False           False
# 3  True  True          True             True  ...         False        False      False           False
# 4  True  True          True             True  ...         False        False      False           False

print(df_mkt.notnull().head())
#    week  year  market_share  av_price_per_kg  ...  reach_cinema  grp_outdoor  grp_print  share_of_spend
# 0  True  True          True             True  ...         False        False      False           False
# 1  True  True          True             True  ...         False        False      False           False
# 2  True  True          True             True  ...         False        False      False           False
# 3  True  True          True             True  ...         False        False      False           False
# 4  True  True          True             True  ...         False        False      False           False

############################################
## df.notna().sum() or df.notnull().sum() ##
############################################
'''Returns the count of non-missing values in each column'''

print(df_mkt.notna().sum())
# week                         156
# year                         156
# market_share                 156
# av_price_per_kg              156
# non_promo_price_per_kg       156
# promo_vol_share              156
# total_weigh                  156
# share_of_ean_weigh           156
# avg_price_vs_plb             156
# non_promo_price_vs_plb       156
# promo_vol_sh_index_vs_plb    156
# total_cm_shelf               156
# shelf_share                  156
# top_of_mind                  123
# spontaneous                  123
# aided                        123
# penetration                  123
# competitor                   111
# grp_radio                     14
# reach_radio                   14
# grp_tv                        52
# reach_tv                      52
# reach_cinema                  18
# grp_outdoor                    1
# grp_print                     22
# share_of_spend               116
# dtype: int64

print(df_mkt.notnull().sum())
# week                         156
# year                         156
# market_share                 156
# av_price_per_kg              156
# non_promo_price_per_kg       156
# promo_vol_share              156
# total_weigh                  156
# share_of_ean_weigh           156
# avg_price_vs_plb             156
# non_promo_price_vs_plb       156
# promo_vol_sh_index_vs_plb    156
# total_cm_shelf               156
# shelf_share                  156
# top_of_mind                  123
# spontaneous                  123
# aided                        123
# penetration                  123
# competitor                   111
# grp_radio                     14
# reach_radio                   14
# grp_tv                        52
# reach_tv                      52
# reach_cinema                  18
# grp_outdoor                    1
# grp_print                     22
# share_of_spend               116
# dtype: int64


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------- 3. Drop missing values along columns ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

################################
## df.dropna(axis=1, how=...) ##
################################
'''how='any' (default): Drop rows with any missing values
   how='all': Drop rows where all values are missing'''

#----
## how='all'
#----

print(
    df_mkt
    .dropna(axis = 1, how = 'all')
    .head()
)
#   week  year  market_share  av_price_per_kg  non_promo_price_per_kg  promo_vol_share  ...  grp_tv  reach_tv  reach_cinema  grp_outdoor  grp_print  share_of_spend
# 0   19  2010         38.40             7.61                    7.77            26.87  ...     NaN       NaN           NaN          NaN        NaN             NaN
# 1   20  2010         36.80             7.60                    7.80            29.42  ...     NaN       NaN           NaN          NaN        NaN             NaN
# 2   21  2010         35.21             7.63                    7.85            27.27  ...     NaN       NaN           NaN          NaN        NaN             NaN
# 3   22  2010         35.03             7.22                    7.76            52.48  ...     NaN       NaN           NaN          NaN        NaN             NaN
# 4   23  2010         32.37             7.70                    7.78            16.11  ...     NaN       NaN           NaN          NaN        NaN             NaN

# [5 rows x 26 columns]
'''No columns are dopped because no columns have all NA values'''

#----
## how='any'
#----

print(
    df_mkt
    .dropna(axis = 1, how = 'any')
    .head()
)
#   week  year  market_share  av_price_per_kg  ...  non_promo_price_vs_plb  promo_vol_sh_index_vs_plb  total_cm_shelf  shelf_share
# 0   19  2010         38.40             7.61  ...                    2.20                       2.02        754253.0         0.25
# 1   20  2010         36.80             7.60  ...                    2.19                       1.59        752248.7         0.25
# 2   21  2010         35.21             7.63  ...                    2.23                       1.03        750244.4         0.25
# 3   22  2010         35.03             7.22  ...                    2.12                       1.04        748240.1         0.25
# 4   23  2010         32.37             7.70  ...                    2.15                       0.66        746235.8         0.25

# [5 rows x 13 columns]
'''Any rows having at least one NA value are dropped.'''

###################################
## df.dropna(axis=1, thresh=...) ##
###################################

print(
    df_mkt
    .dropna(axis = 1, thresh = 2/3 * df_mkt.shape[0]) # Keep columns with at least 2/3 non-missing values
    .head()
)
#   week  year  market_share  av_price_per_kg  non_promo_price_per_kg  ...  spontaneous  aided  penetration  competitor  share_of_spend
# 0   19  2010         38.40             7.61                    7.77  ...          NaN    NaN          NaN         NaN             NaN
# 1   20  2010         36.80             7.60                    7.80  ...          NaN    NaN          NaN         NaN             NaN
# 2   21  2010         35.21             7.63                    7.85  ...          NaN    NaN          NaN         NaN             NaN
# 3   22  2010         35.03             7.22                    7.76  ...          NaN    NaN          NaN         NaN             NaN
# 4   23  2010         32.37             7.70                    7.78  ...          NaN    NaN          NaN         NaN             NaN

# [5 rows x 19 columns]


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------- 4. Drop missing values along rows ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

df_mkt2 = df_mkt.dropna(axis = 1, thresh = 2/3 * df_mkt.shape[0]) # Keep columns with at least 2/3 non-missing values

print(df_mkt2.shape) # (156, 19)

print(df_mkt2.isna().sum().pipe(lambda x: x[x > 0])) # Count missing values, return only columns having missing values
# top_of_mind       33
# spontaneous       33
# aided             33
# penetration       33
# competitor        45
# share_of_spend    40
# dtype: int64

###########################
## df.dropna(how=...)    ##
###########################
'''how='any' (default): Drop rows with any missing values
   how='all': Drop rows where all values are missing'''

#----
## how='any'
#----

print(
    df_mkt2
    .dropna(axis = 0, how = 'any')
)
#     week  year  market_share  av_price_per_kg  non_promo_price_per_kg  ...  spontaneous  aided  penetration  competitor  share_of_spend
# 45    12  2011         39.05             7.34                    7.69  ...         68.6   95.7         70.0         0.0       63.886185
# 46    13  2011         37.52             7.37                    7.67  ...         68.6   95.7         70.0         0.2       79.064596
# 47    14  2011         33.80             7.39                    7.55  ...         78.7   98.0         71.8         0.2       92.590148
# 48    15  2011         35.40             7.35                    7.55  ...         78.7   98.0         71.8         0.4       13.358451
# 49    16  2011         35.29             7.37                    7.54  ...         78.7   98.0         71.8         0.5        8.708819
# ..   ...   ...           ...              ...                     ...  ...          ...    ...          ...         ...             ...
# 145    8  2013         33.45             7.65                    7.69  ...         77.5   99.5         71.2         6.1       45.222828
# 146    9  2013         34.57             7.64                    7.67  ...         77.5   99.5         71.2         5.8       82.679470
# 147   10  2013         32.03             7.65                    7.69  ...         76.0   98.2         62.4         5.1       97.452067
# 148   11  2013         32.17             7.67                    7.70  ...         76.0   98.2         62.4         5.0       68.861555
# 149   12  2013         33.81             7.65                    7.74  ...         76.0   98.2         62.4         4.7       84.546201

# [105 rows x 19 columns]
'''Here, 51 rows are dropped because they have at least one missing value.'''

#----
## how='all'
#----

print(
    df_mkt2
    .dropna(axis = 0, how = 'all')
)
#     week  year  market_share  av_price_per_kg  non_promo_price_per_kg  ...  spontaneous  aided  penetration  competitor  share_of_spend
# 0     19  2010         38.40             7.61                    7.77  ...          NaN    NaN          NaN         NaN             NaN
# 1     20  2010         36.80             7.60                    7.80  ...          NaN    NaN          NaN         NaN             NaN
# 2     21  2010         35.21             7.63                    7.85  ...          NaN    NaN          NaN         NaN             NaN
# 3     22  2010         35.03             7.22                    7.76  ...          NaN    NaN          NaN         NaN             NaN
# 4     23  2010         32.37             7.70                    7.78  ...          NaN    NaN          NaN         NaN             NaN
# ..   ...   ...           ...              ...                     ...  ...          ...    ...          ...         ...             ...
# 151   14  2013         33.26             7.63                    7.66  ...         83.7   99.5         71.6         4.6             NaN
# 152   15  2013         33.99             7.59                    7.64  ...         83.7   99.5         71.6         4.7             NaN
# 153   16  2013         30.57             7.66                    7.68  ...         83.7   99.5         71.6         4.6             NaN
# 154   17  2013         32.24             7.63                    7.66  ...         83.7   99.5         71.6         4.7             NaN
# 155   18  2013         34.63             7.61                    7.61  ...         83.7   99.5         71.6         5.0             NaN

# [156 rows x 19 columns]
'''No rows are dropped because no rows have all NA values.'''

###########################
## df.dropna(subset=...) ##
###########################
'''subset=[col1, col2, ...]: Drop rows with missing values in the specified columns'''

print(
    df_mkt2
    .dropna(axis = 0, subset = ['top_of_mind', 'spontaneous']) # Drop rows with missing values in the 'top_of_mind' or 'spontaneous' columns
    .isna().sum()
    .pipe(lambda x: x[x > 0])
)
# competitor        12
# share_of_spend     7
# dtype: int64

print(
    df_mkt2
    .dropna(axis = 0, subset = ['top_of_mind', 'spontaneous'])
    .shape
)
# (123, 19)
'''Here 33 rows are dropped because they have missing values in the 'top_of_mind' or 'spontaneous' columns.'''


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 5. Fill missing values --------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

# Drop "category" columns before filling NA with 0, avoid error
df_missing = df_mkt.drop(["week", "year"], axis = 1)

#################
## df.fillna() ##
#################
'''Returns a DataFrame with missing values filled with the specified value'''

print(
    df_missing
    .fillna(0, inplace = False)
    .head()
)
#    market_share  av_price_per_kg  non_promo_price_per_kg  ...  grp_outdoor  grp_print  share_of_spend
# 0         38.40             7.61                    7.77  ...          0.0        0.0             0.0
# 1         36.80             7.60                    7.80  ...          0.0        0.0             0.0
# 2         35.21             7.63                    7.85  ...          0.0        0.0             0.0
# 3         35.03             7.22                    7.76  ...          0.0        0.0             0.0
# 4         32.37             7.70                    7.78  ...          0.0        0.0             0.0

#############################
## df.fillna({dictionary}) ##
#############################
'''Fill different columns with different values'''

print(
    df_missing
    .fillna(
        {
            'top_of_mind': df_missing['top_of_mind'].mean(),
            'spontaneous': df_missing['spontaneous'].median(),
            'aided': df_missing['aided'].min(),
            'penetration': df_missing['penetration'].max()
        },
        inplace = False
    )
    .reindex(columns = ['top_of_mind', 'spontaneous', 'aided', 'penetration'])
)
#      top_of_mind  spontaneous  aided  penetration
# 0      50.465041         78.2   95.7         76.8
# 1      50.465041         78.2   95.7         76.8
# 2      50.465041         78.2   95.7         76.8
# 3      50.465041         78.2   95.7         76.8
# 4      50.465041         78.2   95.7         76.8
# ..           ...          ...    ...          ...
# 151    50.200000         83.7   99.5         71.6
# 152    50.200000         83.7   99.5         71.6
# 153    50.200000         83.7   99.5         71.6
# 154    50.200000         83.7   99.5         71.6
# 155    50.200000         83.7   99.5         71.6

##########################
## df.fillna(df.mean()) ##
##########################
'''Fill missing values with the mean of each column'''

print(
    df_missing
    .fillna(df_missing.mean(), inplace = False)
    .head()
)
#    market_share  av_price_per_kg  non_promo_price_per_kg  ...  grp_outdoor  grp_print  share_of_spend
# 0         38.40             7.61                    7.77  ...       1127.0  14.904545       45.314027
# 1         36.80             7.60                    7.80  ...       1127.0  14.904545       45.314027
# 2         35.21             7.63                    7.85  ...       1127.0  14.904545       45.314027
# 3         35.03             7.22                    7.76  ...       1127.0  14.904545       45.314027
# 4         32.37             7.70                    7.78  ...       1127.0  14.904545       45.314027

################
## df.ffill() ##
################
'''Fill missing values using forward fill method'''

s_misisng = pd.Series([1, np.nan, np.nan, 4, 5, np.nan, 7])

print(s_misisng.ffill())
# 0    1.0
# 1    1.0
# 2    1.0
# 3    4.0
# 4    5.0
# 5    5.0
# 6    7.0
# dtype: float64

################
## df.bfill() ##
################
'''Fill missing values using backward fill method'''

s_misisng = pd.Series([1, np.nan, np.nan, 4, 5, np.nan, 7])

print(s_misisng.bfill())
# 0    1.0
# 1    4.0
# 2    4.0
# 3    4.0
# 4    5.0
# 5    7.0
# 6    7.0
# dtype: float64


#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 6. Interpolate missing values ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

# Drop "category" columns before interpolation, avoid error
df_missing = df_mkt.drop(["week", "year"], axis = 1)

print(df_missing.isna().sum().pipe(lambda x: x[x > 0]))
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

####################################################
## df.interpolate(axis=0, limit_direction='both') ##
####################################################
'''linear interpolation'''

df_interpolated = df_missing.interpolate(axis=0, inplace = False, limit_direction='both')

print(df_interpolated.isna().sum().pipe(lambda x: x[x > 0]))
# Series([], dtype: int64)
'''All missing values are filled'''

######################################################
## df.interpolate(method = "polynomial", order = n) ##
######################################################
'''
polynomial interpolation of order n (the number of non-missing values must be greater than n)

It only fills missing values between two non-missing values, ignore the boundary missing values
'''

df_interpolated_poly = (
    df_missing
    .drop("grp_outdoor", axis = 1) # Drop "grp_outdoor" column because it has only one non-missing value
    .interpolate(method = "polynomial", order = 2, inplace = False, axis = 0, limit_direction='both')
)

print(df_interpolated_poly.isna().sum().pipe(lambda x: x[x > 0]))
# top_of_mind        33
# spontaneous        33
# aided              33
# penetration        33
# competitor         45
# grp_radio          45
# reach_radio        45
# grp_tv             43
# reach_tv           43
# reach_cinema      138
# grp_print          68
# share_of_spend     40
# dtype: int64
'''Only fills missing values between two non-missing values, ignore the boundary missing values'''

##################################################
## df.interpolate(method = "spline", order = n) ##
##################################################
'''spline interpolation of order n'''

df_interpolated_spline = (
    df_missing
    .drop("grp_outdoor", axis = 1) # Drop "grp_outdoor" column because it has only one non-missing value
    .interpolate(method = "spline", order = 2, inplace = False, axis = 0, limit_direction='both')
)

print(df_interpolated_spline.isna().sum().pipe(lambda x: x[x > 0]))
# Series([], dtype: int64)
'''All missing values are filled'''

#####################################
## df.interpolate(method = "time") ##
#####################################
'''time-based interpolation (requires a datetime index)'''

df_missing_time = (
    df_mkt
    .drop(["week", "year"], axis = 1) # Drop "category" columns before interpolation, avoid error
    .assign(date = pd.date_range(start = "2023-01-01", periods = df_mkt.shape[0], freq = 'W'))
    .set_index('date')
)

df_interpolated_time = df_missing_time.interpolate(method = "time", inplace = False, axis = 0, limit_direction='both')

print(df_interpolated_time.isna().sum().pipe(lambda x: x[x > 0]))
# Series([], dtype: int64)
'''All missing values are filled'''

########################################
## df.interpolate(method = "nearest") ##
########################################
'''
nearest neighbor interpolation

Only fills missing values between two non-missing values, ignore the boundary missing values
'''

df_interpolated_nearest = df_missing.interpolate(method = "nearest", inplace = False, axis = 0, limit_direction='both')

print(df_interpolated_nearest.isna().sum().pipe(lambda x: x[x > 0]))
# top_of_mind        33
# spontaneous        33
# aided              33
# penetration        33
# competitor         45
# grp_radio          45
# reach_radio        45
# grp_tv             43
# reach_tv           43
# reach_cinema      138
# grp_outdoor       155
# grp_print          68
# share_of_spend     40
# dtype: int64
'''Only fills missing values between two non-missing values, ignore the boundary missing values'''


#--------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 7. Conditional filling ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

# Drop "category" columns before filling NA with mean, avoid error
df_missing = df_mkt.drop(["week", "year"], axis = 1)

df_filled = pd.DataFrame(np.where(df_missing.isna(), df_missing.mean(), df_missing), columns = df_missing.columns)

print(df_filled.isna().sum())
# market_share                 0
# av_price_per_kg              0
# non_promo_price_per_kg       0
# promo_vol_share              0
# total_weigh                  0
# share_of_ean_weigh           0
# avg_price_vs_plb             0
# non_promo_price_vs_plb       0
# promo_vol_sh_index_vs_plb    0
# total_cm_shelf               0
# shelf_share                  0
# top_of_mind                  0
# spontaneous                  0
# aided                        0
# penetration                  0
# competitor                   0
# grp_radio                    0
# reach_radio                  0
# grp_tv                       0
# reach_tv                     0
# reach_cinema                 0
# grp_outdoor                  0
# grp_print                    0
# share_of_spend               0
# dtype: int64
'''All missing values are filled'''


#------------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 8. Group-based filling, transform -----------------------------------------#
#------------------------------------------------------------------------------------------------------------------#

df_missing = df_mkt.drop("year", axis = 1)
print(df_missing.isna().sum().pipe(lambda x: x[x > 0]))
# top_of_mind        33
# spontaneous        33
# aided              33
# penetration        33
# competitor         45
# grp_radio         142
# reach_radio       142
# grp_tv            104
# reach_tv          104
# reach_cinema      138
# grp_outdoor       155
# grp_print         134
# share_of_spend     40

#--------------------

# FILL MISSING VALUES WITH THE MEAN OF EACH "week" GROUP
df_group_filled = df_missing.fillna(df_missing.groupby("week").transform("mean"))

#--------------------

print(df_group_filled.isna().sum().pipe(lambda x: x[x > 0]))
# grp_radio       114
# reach_radio     114
# grp_tv           27
# reach_tv         27
# reach_cinema    102
# grp_outdoor     153
# grp_print        96
# dtype: int64

print(df_group_filled.head())
#   week  market_share  av_price_per_kg  non_promo_price_per_kg  promo_vol_share  ...  reach_tv  reach_cinema  grp_outdoor  grp_print  share_of_spend
# 0   19         38.40             7.61                    7.77            26.87  ...       NaN           NaN          NaN        NaN        0.155019
# 1   20         36.80             7.60                    7.80            29.42  ...       NaN           NaN          NaN        NaN        0.000000
# 2   21         35.21             7.63                    7.85            27.27  ...     0.602           NaN          NaN        NaN        0.177186
# 3   22         35.03             7.22                    7.76            52.48  ...    20.382           NaN          NaN        NaN       34.323685
# 4   23         32.37             7.70                    7.78            16.11  ...    40.245           NaN          NaN        NaN       50.000000

'''Cannot fill all missing values because some "week" groups have all NA values in certain columns'''
