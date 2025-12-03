'''
dr.slice_sample() allows randomly sampling rows (observations) from a DataFrame.

####################

1. dr.slice_sample(n=..., random_state=...)

2. dr.slice_sample(prop=..., random_state=...)
'''

import datar.all as dr
from datar import f

import pandas as pd

########################

df_baseball = pd.read_csv(
    filepath_or_buffer = "05_Pandas_DataR_dataframe/data/baseball.csv",
    dtype = {
        "Team": "category",
        "Position": "category",
        "PosCategory": "category"
    }
)

print(df_baseball.info())
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 1015 entries, 0 to 1014
# Data columns (total 7 columns):
#  #   Column       Non-Null Count  Dtype   
# ---  ------       --------------  -----   
#  0   Name         1015 non-null   object  
#  1   Team         1015 non-null   category
#  2   Position     1015 non-null   category
#  3   Height       1015 non-null   int64   
#  4   Weight       1015 non-null   int64   
#  5   Age          1015 non-null   float64 
#  6   PosCategory  1015 non-null   category
# dtypes: category(3), float64(1), int64(2), object(1)
# memory usage: 36.5+ KB


#------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. dr.slice_sample(n=...) ------------------------------------------#
#------------------------------------------------------------------------------------------------------------#

'''
The n=... argument specifies the number of rows to return in the sample.
'''

print(
    df_baseball >>
    dr.slice_sample(n=5, random_state=42) # random_state=... ensures reproducibility (like .seed(42))
)
#                   Name       Team        Position  Height  Weight       Age PosCategory
#               <object> <category>      <category> <int64> <int64> <float64>  <category>
# 752     Wilson_Betemit         LA   Third_Baseman      75     190     26.59   Infielder
# 519        Mark_DeRosa        CHC      Outfielder      73     205     32.01  Outfielder
# 210       Miguel_Cairo        NYY  Second_Baseman      73     208     32.82   Infielder
# 611  Edwin_Encarnacion        CIN   Third_Baseman      73     195     24.15   Infielder
# 914      Humberto_Cota        PIT         Catcher      72     210     28.06     Catcher


#------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. dr.slice_sample(prop=...) ----------------------------------------#
#------------------------------------------------------------------------------------------------------------#

'''
The frac=... argument specifies the fraction of rows to return in the sample.

frac should be between 0 and 1.

If fract > 1, should set replace=True => Upsampling with replacement.
'''

print(
    df_baseball >>
    dr.slice_sample(prop=0.01, random_state=41) # 1%
)
#                 Name       Team          Position  Height  Weight       Age PosCategory
#             <object> <category>        <category> <int64> <int64> <float64>  <category>
# 149   David_Dellucci        CLE        Outfielder      71     190     33.33  Outfielder
# 296  George_Sherrill        SEA    Relief_Pitcher      72     210     29.86     Pitcher
# 848  Adrian_Gonzalez         SD     First_Baseman      74     220     24.81   Infielder
# 294      Jeff_Weaver        SEA  Starting_Pitcher      77     200     30.52     Pitcher
# 884  Cristian_Guzman        WAS         Shortstop      72     205     28.94   Infielder
# 194      Alan_Embree        OAK    Relief_Pitcher      74     190     37.10     Pitcher
# 524    Carlos_Marmol        CHC  Starting_Pitcher      74     180     24.38     Pitcher
# 704       Jorge_Sosa        NYM    Relief_Pitcher      74     170     29.84     Pitcher
# 283      Jeremy_Reed        SEA        Outfielder      72     185     25.71  Outfielder
# 379    Michael_Young        TEX         Shortstop      73     190     30.36   Infielder

'''
0.01 * 1015 = 10.15 => 10 rows
'''