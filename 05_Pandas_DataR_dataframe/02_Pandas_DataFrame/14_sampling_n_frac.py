'''
df.sample() allows randomly sampling rows (observations) from a DataFrame.

####################

1. df.sample(n=..., random_state=...)
2. df.sample(frac=..., random_state=...)
'''

import pandas as pd

df_baseball = pd.read_csv(
    filepath_or_buffer="05_Pandas_DataR_dataframe/data/baseball.csv",
    dtype={
        "Team": "category",
        "Position": "category",
        "PosCategory": "category"
    }
)

print(df_baseball.info())
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
#----------------------------------- 1. df.sample(n=..., random_state=...) ----------------------------------#
#------------------------------------------------------------------------------------------------------------#

'''
The n=... argument specifies the number of rows to return in the sample.
'''

df_sample_n = df_baseball.sample(n=5, random_state=42) # random_state=... ensures reproducibility (like .seed(42))
print(df_sample_n)
#                   Name Team        Position  Height  Weight    Age PosCategory
# 752     Wilson_Betemit   LA   Third_Baseman      75     190  26.59   Infielder
# 519        Mark_DeRosa  CHC      Outfielder      73     205  32.01  Outfielder
# 210       Miguel_Cairo  NYY  Second_Baseman      73     208  32.82   Infielder
# 611  Edwin_Encarnacion  CIN   Third_Baseman      73     195  24.15   Infielder
# 914      Humberto_Cota  PIT         Catcher      72     210  28.06     Catcher


#------------------------------------------------------------------------------------------------------------#
#--------------------------------- 2. df.sample(frac=..., random_state=...) ---------------------------------#
#------------------------------------------------------------------------------------------------------------#

'''
The frac=... argument specifies the fraction of rows to return in the sample.

frac should be between 0 and 1.

If fract > 1, should set replace=True => Upsampling with replacement.
'''

df_sample_frac = df_baseball.sample(frac=0.01, random_state=40) # 1% of the rows
print(df_sample_frac)
#                  Name Team          Position  Height  Weight    Age PosCategory
# 997      Chris_Duncan  STL        Outfielder      77     210  25.82  Outfielder
# 649     Willy_Taveras  COL        Outfielder      72     160  25.18  Outfielder
# 287        Mike_Morse  SEA        Outfielder      76     220  24.94  Outfielder
# 478       Willy_Aybar  ATL     Third_Baseman      72     175  23.98   Infielder
# 561  Enrique_Gonzalez  ARZ  Starting_Pitcher      70     210  24.57     Pitcher
# 79        Terry_Evans  ANA        Outfielder      75     200  25.11  Outfielder
# 383        Sammy_Sosa  TEX        Outfielder      72     220  38.30  Outfielder
# 526        Juan_Mateo  CHC  Starting_Pitcher      74     180  24.20     Pitcher
# 176     Marco_Scutaro  OAK         Shortstop      70     170  31.33   Infielder
# 269  Wilfredo_Ledezma  DET    Relief_Pitcher      76     212  26.11     Pitcher

print(df_sample_frac.shape)
# (10, 7)

#############################

df_upsample = df_baseball.sample(frac=1.5, replace=True, random_state=1) # 150% of the rows with replacement

print(df_upsample.shape)
# (1522, 7)