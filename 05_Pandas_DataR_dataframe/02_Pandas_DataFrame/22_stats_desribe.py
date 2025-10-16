'''
df.describe(): Get summary statistics of DataFrame columns.
   + Default usage
   + df.describe(include = [object, category, "all"]): Include specific data types.
   + df.describe(exclude = [category, bool]): Exclude specific data types.
'''

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

df_pokemon = (
    pd.read_csv(
        filepath_or_buffer = "05_Pandas_DataR_dataframe/data/pokemon.csv",
        dtype = {
            "Type 1": "category",
            "Type 2": "category",
            "Generation": "category",
            "Legendary": "bool"
        }
    )
    .drop(columns = ["#"])
    .pipe(lambda df: df.set_axis(df.columns.str.strip().str.replace(r"\s+", "_", regex = True).str.replace(".", ""), axis=1))
    .assign(Generation = lambda df: df['Generation'].cat.as_ordered())
)

print(df_pokemon.info())
# RangeIndex: 800 entries, 0 to 799
# Data columns (total 12 columns):
#  #   Column      Non-Null Count  Dtype   
# ---  ------      --------------  -----   
#  0   Name        800 non-null    object  
#  1   Type_1      800 non-null    category
#  2   Type_2      414 non-null    category
#  3   Total       800 non-null    int64   
#  4   HP          800 non-null    int64   
#  5   Attack      800 non-null    int64   
#  6   Defense     800 non-null    int64   
#  7   Sp_Atk      800 non-null    int64   
#  8   Sp_Def      800 non-null    int64   
#  9   Speed       800 non-null    int64   
#  10  Generation  800 non-null    category
#  11  Legendary   800 non-null    bool    
# dtypes: bool(1), category(3), int64(7), object(1)
# memory usage: 54.7+ KB


#----------------------------------------------------------------------------------------------------------#
#-------------------------------------------- df.describe() -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

###################
## Default usage ##
###################

print(df_pokemon.describe())
#            Total          HP      Attack     Defense      Sp_Atk      Sp_Def       Speed
# count  800.00000  800.000000  800.000000  800.000000  800.000000  800.000000  800.000000
# mean   435.10250   69.258750   79.001250   73.842500   72.820000   71.902500   68.277500
# std    119.96304   25.534669   32.457366   31.183501   32.722294   27.828916   29.060474
# min    180.00000    1.000000    5.000000    5.000000   10.000000   20.000000    5.000000
# 25%    330.00000   50.000000   55.000000   50.000000   49.750000   50.000000   45.000000
# 50%    450.00000   65.000000   75.000000   70.000000   65.000000   70.000000   65.000000
# 75%    515.00000   80.000000  100.000000   90.000000   95.000000   90.000000   90.000000
# max    780.00000  255.000000  190.000000  230.000000  194.000000  230.000000  180.000000

####################################################
## df.describe(include=[object, category, "all"]) ##
####################################################

print(df_pokemon.describe(include = ['object', 'category']))
#           Name Type_1  Type_2 Generation
# count      800    800     414        800
# unique     800     18      18          6
# top     Skrelp  Water  Flying          1
# freq         1    112      97        166

print(df_pokemon.describe(include = 'all'))
#           Name Type_1  Type_2      Total          HP  ...      Sp_Atk      Sp_Def       Speed  Generation  Legendary
# count      800    800     414  800.00000  800.000000  ...  800.000000  800.000000  800.000000         800        800
# unique     800     18      18        NaN         NaN  ...         NaN         NaN         NaN           6          2
# top     Skrelp  Water  Flying        NaN         NaN  ...         NaN         NaN         NaN           1      False
# freq         1    112      97        NaN         NaN  ...         NaN         NaN         NaN         166        735
# mean       NaN    NaN     NaN  435.10250   69.258750  ...   72.820000   71.902500   68.277500         NaN        NaN
# std        NaN    NaN     NaN  119.96304   25.534669  ...   32.722294   27.828916   29.060474         NaN        NaN
# min        NaN    NaN     NaN  180.00000    1.000000  ...   10.000000   20.000000    5.000000         NaN        NaN
# 25%        NaN    NaN     NaN  330.00000   50.000000  ...   49.750000   50.000000   45.000000         NaN        NaN
# 50%        NaN    NaN     NaN  450.00000   65.000000  ...   65.000000   70.000000   65.000000         NaN        NaN
# 75%        NaN    NaN     NaN  515.00000   80.000000  ...   95.000000   90.000000   90.000000         NaN        NaN
# max        NaN    NaN     NaN  780.00000  255.000000  ...  194.000000  230.000000  180.000000         NaN        NaN

###########################################
## df.describe(exclude=[category, bool]) ##
###########################################

print(df_pokemon.describe(exclude = ['category', 'bool']))
#           Name      Total          HP      Attack     Defense      Sp_Atk      Sp_Def       Speed
# count      800  800.00000  800.000000  800.000000  800.000000  800.000000  800.000000  800.000000
# unique     800        NaN         NaN         NaN         NaN         NaN         NaN         NaN
# top     Skrelp        NaN         NaN         NaN         NaN         NaN         NaN         NaN
# freq         1        NaN         NaN         NaN         NaN         NaN         NaN         NaN
# mean       NaN  435.10250   69.258750   79.001250   73.842500   72.820000   71.902500   68.277500
# std        NaN  119.96304   25.534669   32.457366   31.183501   32.722294   27.828916   29.060474
# min        NaN  180.00000    1.000000    5.000000    5.000000   10.000000   20.000000    5.000000
# 25%        NaN  330.00000   50.000000   55.000000   50.000000   49.750000   50.000000   45.000000
# 50%        NaN  450.00000   65.000000   75.000000   70.000000   65.000000   70.000000   65.000000
# 75%        NaN  515.00000   80.000000  100.000000   90.000000   95.000000   90.000000   90.000000
# max        NaN  780.00000  255.000000  190.000000  230.000000  194.000000  230.000000  180.000000