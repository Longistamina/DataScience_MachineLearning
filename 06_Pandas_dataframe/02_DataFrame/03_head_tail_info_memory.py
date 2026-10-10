'''
1. df.head(n=5): Returns the first n rows of the DataFrame (default is 5)

2. df.tail(n=5): Returns the last n rows of the DataFrame (default is 5)

3. Memory and Performance attributes:
   + df.info(memory_usage='deep'): Provides a concise summary of the DataFrame
   + df.memory_usage(deep=True): Returns memory usage of each column
'''

from pathlib import Path

import pandas as pd

data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

df_medals = pd.read_csv(
    filepath_or_buffer=data_dir/"medals.csv",
    skiprows=4
)

# =========================================================================================
# 1. df.head()
# =========================================================================================
'''df.head(n=5): Returns the first n rows of the DataFrame (default is 5)'''

df_medals.head()
#    Year      City       Sport      Discipline  NOC       Event Event gender   Medal
# 0  1924  Chamonix     Skating  Figure skating  AUT  individual            M  Silver
# 1  1924  Chamonix     Skating  Figure skating  AUT  individual            W    Gold
# 2  1924  Chamonix     Skating  Figure skating  AUT       pairs            X    Gold
# 3  1924  Chamonix   Bobsleigh       Bobsleigh  BEL    four-man            M  Bronze
# 4  1924  Chamonix  Ice Hockey      Ice Hockey  CAN  ice hockey            M    Gold

df_medals.head(3)
#    Year      City    Sport      Discipline  NOC       Event Event gender   Medal
# 0  1924  Chamonix  Skating  Figure skating  AUT  individual            M  Silver
# 1  1924  Chamonix  Skating  Figure skating  AUT  individual            W    Gold
# 2  1924  Chamonix  Skating  Figure skating  AUT       pairs            X    Gold

# =========================================================================================
# 2. df.tail()
# =========================================================================================
'''df.tail(n=5): Returns the last n rows of the DataFrame (default is 5)'''

df_medals.tail()
#       Year   City   Sport Discipline  NOC            Event Event gender   Medal
# 2306  2006  Turin  Skiing  Snowboard  USA        Half-pipe            M  Silver
# 2307  2006  Turin  Skiing  Snowboard  USA        Half-pipe            W    Gold
# 2308  2006  Turin  Skiing  Snowboard  USA        Half-pipe            W  Silver
# 2309  2006  Turin  Skiing  Snowboard  USA  Snowboard Cross            M    Gold
# 2310  2006  Turin  Skiing  Snowboard  USA  Snowboard Cross            W  Silver

df_medals.tail(3)
#       Year   City   Sport Discipline  NOC            Event Event gender   Medal
# 2308  2006  Turin  Skiing  Snowboard  USA        Half-pipe            W  Silver
# 2309  2006  Turin  Skiing  Snowboard  USA  Snowboard Cross            M    Gold
# 2310  2006  Turin  Skiing  Snowboard  USA  Snowboard Cross            W  Silver

# =========================================================================================
# 3. Memory and Performance
# =========================================================================================

##-----------##
## df.info() ##
##-----------##
'''df.info(memory_usage='deep'): Provides a concise summary of the DataFrame'''

df_medals.info()
# <class 'pandas.DataFrame'>
# RangeIndex: 2311 entries, 0 to 2310
# Data columns (total 8 columns):
#  #   Column        Non-Null Count  Dtype
# ---  ------        --------------  -----
#  0   Year          2311 non-null   int64
#  1   City          2311 non-null   str
#  2   Sport         2311 non-null   str
#  3   Discipline    2311 non-null   str
#  4   NOC           2311 non-null   str
#  5   Event         2311 non-null   str
#  6   Event gender  2311 non-null   str
#  7   Medal         2311 non-null   str
# dtypes: int64(1), str(7)
# memory usage: 248.9 KB

df_medals.info(memory_usage='deep')
# <class 'pandas.DataFrame'>
# RangeIndex: 2311 entries, 0 to 2310
# Data columns (total 8 columns):
#  #   Column        Non-Null Count  Dtype
# ---  ------        --------------  -----
#  0   Year          2311 non-null   int64
#  1   City          2311 non-null   str
#  2   Sport         2311 non-null   str
#  3   Discipline    2311 non-null   str
#  4   NOC           2311 non-null   str
#  5   Event         2311 non-null   str
#  6   Event gender  2311 non-null   str
#  7   Medal         2311 non-null   str
# dtypes: int64(1), str(7)
# memory usage: 248.9 KB
'''
With deep memory introspection,
a real memory usage calculation is performed at the cost of computational resources
'''

##-------------------##
## df.memory_usage() ##
##-------------------##
'''df.memory_usage(deep=True): Returns memory usage of each column'''

df_medals.memory_usage()
# Index             132
# Year            18488
# City            40354
# Sport           33916
# Discipline      46793
# NOC             25421
# Event           38124
# Event gender    20799
# Medal           30806
# dtype: int64

df_medals.memory_usage(deep=True)
# Index             132
# Year            18488
# City            40354
# Sport           33916
# Discipline      46793
# NOC             25421
# Event           38124
# Event gender    20799
# Medal           30806
# dtype: int64
