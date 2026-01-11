'''
1. df.head(n=5): Returns the first n rows of the DataFrame (default is 5) 

2. df.tail(n=5): Returns the last n rows of the DataFrame (default is 5)

3. Memory and Performance attributes:
   + df.info(memory_usage='deep'): Provides a concise summary of the DataFrame
   + df.memory_usage(deep=True): Returns memory usage of each column
'''

import pandas as pd

df_medals = pd.read_csv(
    filepath_or_buffer = "05_Pandas_DataR_dataframe/data/medals.csv",
    skiprows = 4
)


#-------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 1. df.head() ---------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

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


#-------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2. df.tail() ---------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

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


#-------------------------------------------------------------------------------------------------------#
#-------------------------------------- 3. Memory and Performance --------------------------------------#
#-------------------------------------------------------------------------------------------------------#

###############
## df.info() ##
###############
'''df.info(memory_usage='deep'): Provides a concise summary of the DataFrame'''

df_medals.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 2311 entries, 0 to 2310
# Data columns (total 8 columns):
#  #   Column        Non-Null Count  Dtype 
# ---  ------        --------------  ----- 
#  0   Year          2311 non-null   int64 
#  1   City          2311 non-null   object
#  2   Sport         2311 non-null   object
#  3   Discipline    2311 non-null   object
#  4   NOC           2311 non-null   object
#  5   Event         2311 non-null   object
#  6   Event gender  2311 non-null   object
#  7   Medal         2311 non-null   object
# dtypes: int64(1), object(7)
# memory usage: 144.6+ KB

df_medals.info(memory_usage='deep')
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 2311 entries, 0 to 2310
# Data columns (total 8 columns):
#  #   Column        Non-Null Count  Dtype 
# ---  ------        --------------  ----- 
#  0   Year          2311 non-null   int64 
#  1   City          2311 non-null   object
#  2   Sport         2311 non-null   object
#  3   Discipline    2311 non-null   object
#  4   NOC           2311 non-null   object
#  5   Event         2311 non-null   object
#  6   Event gender  2311 non-null   object
#  7   Medal         2311 non-null   object
# dtypes: int64(1), object(7)
# memory usage: 896.6 KB
'''
With deep memory introspection, 
a real memory usage calculation is performed at the cost of computational resources
'''

#######################
## df.memory_usage() ##
#######################
'''df.memory_usage(deep=True): Returns memory usage of each column'''

df_medals.memory_usage()
# Index             132
# Year            18488
# City            18488
# Sport           18488
# Discipline      18488
# NOC             18488
# Event           18488
# Event gender    18488
# Medal           18488
# dtype: int64

df_medals.memory_usage(deep=True)
# Index              132
# Year             18488
# City            135105
# Sport           128667
# Discipline      141544
# NOC             120172
# Event           132875
# Event gender    115550
# Medal           125557
# dtype: int64