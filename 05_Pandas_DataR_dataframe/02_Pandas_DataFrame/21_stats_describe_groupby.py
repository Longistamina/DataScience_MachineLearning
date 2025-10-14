'''
1. df.describe(): Get summary statistics of DataFrame columns.
   + Default usage
   + df.describe(include = [object, category, "all"]): Include specific data types.
   + df.describe(exclude = [category, bool]): Exclude specific data types.

2. df.group.agg(): Aggregate data using specified functions.
   + df.groupby(sort=True/False): Sort group keys.
   + df.groupby(dropna=True/False): Include/exclude NaN values in group keys.

3. df.groupby.apply(): Apply a function to each group.
'''

import pandas as pd

df_pokemon = (
    pd.read_csv(
        filepath_or_buffer = "05_Pandas_DataR_dataframe/data/pokemon.csv",
        index_col = "#",
        dtype = {
            "Type 1": "category",
            "Type 2": "category",
            "Generation": "category",
            "Legendary": "bool"
        }
    )
    .pipe(lambda df: df.set_axis(df.columns.str.strip().str.replace(r"\s+", "_", regex = True).str.replace(".", ""), axis=1))
    .assign(Generation = lambda df: df['Generation'].cat.as_ordered())
)

print(df_pokemon.info())
# Index: 800 entries, 1 to 721
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
# memory usage: 60.8+ KB


#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 1. df.describe() -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

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


#------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 2. df.groupby.agg() ----------------------------------------------#
#------------------------------------------------------------------------------------------------------------#

#################################
## df.groupby(sort=True/False) ##
#################################
'''Sort group keys in ascending order by default.'''

print(
    df_pokemon
    .groupby(by = 'Type_1', sort = True, observed=False) # observed=False to include all categories in the group keys
    .agg(
        min_HP = ('HP', 'min'),
        max_HP = ('HP', 'max'),
        mean_HP = ('HP', 'mean')
    )
)
#           min_HP  max_HP    mean_HP
# Type_1                             
# Bug            1      86  56.884058
# Dark          35     126  66.806452
# Dragon        41     125  83.312500
# Electric      20      90  59.795455
# Fairy         35     126  74.117647
# Fighting      30     144  69.851852
# Fire          38     115  69.903846
# Flying        40      85  70.750000
# Ghost         20     150  64.437500
# Grass         30     123  67.271429
# Ground        10     115  73.781250
# Ice           36     110  72.000000
# Normal        30     255  77.275510
# Poison        35     105  67.250000
# Psychic       20     190  70.631579
# Rock          30     123  65.363636
# Steel         40     100  65.222222
# Water         20     170  72.062500

print(
    df_pokemon
    .groupby(by = 'Type_1', sort = False, observed=False) # observed=False to include all categories in the group keys
    .agg(
        min_HP = ('HP', 'min'),
        max_HP = ('HP', 'max'),
        mean_HP = ('HP', 'mean')
    )
    .reset_index() # Reset index to turn the group keys into a column
)
#       Type_1  min_HP  max_HP    mean_HP
# 0      Grass      30     123  67.271429
# 1       Fire      38     115  69.903846
# 2      Water      20     170  72.062500
# 3        Bug       1      86  56.884058
# 4     Normal      30     255  77.275510
# 5     Poison      35     105  67.250000
# 6   Electric      20      90  59.795455
# 7     Ground      10     115  73.781250
# 8      Fairy      35     126  74.117647
# 9   Fighting      30     144  69.851852
# 10   Psychic      20     190  70.631579
# 11      Rock      30     123  65.363636
# 12     Ghost      20     150  64.437500
# 13       Ice      36     110  72.000000
# 14    Dragon      41     125  83.312500
# 15      Dark      35     126  66.806452
# 16     Steel      40     100  65.222222
# 17    Flying      40      85  70.750000

print(
    df_pokemon
    .groupby(by = ['Type_1', 'Type_2'], sort = True, observed=False) # observed=False to include all categories in the group keys
    .agg(
        min_HP = ('HP', 'min'),
        max_HP = ('HP', 'max'),
        mean_HP = ('HP', 'mean')
    )
    .reset_index() # Reset index to turn the group keys into a column
)
#     Type_1    Type_2  min_HP  max_HP    mean_HP
# 0      Bug       Bug     NaN     NaN        NaN
# 1      Bug      Dark     NaN     NaN        NaN
# 2      Bug    Dragon     NaN     NaN        NaN
# 3      Bug  Electric    50.0    70.0  60.000000
# 4      Bug     Fairy     NaN     NaN        NaN
# ..     ...       ...     ...     ...        ...
# 319  Water    Poison    40.0    80.0  61.666667
# 320  Water   Psychic    60.0    95.0  87.000000
# 321  Water      Rock    54.0   100.0  70.750000
# 322  Water     Steel    84.0    84.0  84.000000
# 323  Water     Water     NaN     NaN        NaN

###################################
## df.groupby(dropna=True/False) ##
###################################
'''By default, dropna=True, which excludes NaN values in the group keys.'''

print(
    df_pokemon
    .groupby(by = 'Type_2', dropna = True, observed=False) # observed=False to include all categories in the group keys
    .agg(
        min_HP = ('HP', 'min'),
        max_HP = ('HP', 'max'),
        mean_HP = ('HP', 'mean')
    )
    .reset_index() # Reset index to turn the group keys into a column
)
#       Type_2  min_HP  max_HP    mean_HP
# 0        Bug      40      75  53.333333
# 1       Dark      45     103  75.550000
# 2     Dragon      40     150  82.166667
# 3   Electric      50     125  88.166667
# 4      Fairy      20     140  64.304348
# 5   Fighting      48     110  79.461538
# 6       Fire      45     100  71.250000
# 7     Flying      30     150  71.391753
# 8      Ghost       1     100  59.142857
# 9      Grass      35     100  62.640000
# 10    Ground      31     111  77.228571
# 11       Ice      50     130  90.000000
# 12    Normal      44      86  63.500000
# 13    Poison      30     114  58.764706
# 14   Psychic      30     105  72.212121
# 15      Rock      20     115  68.071429
# 16     Steel      25     110  64.636364
# 17     Water      30     110  62.714286

print(
    df_pokemon
    .groupby(by = ['Type_1', 'Type_2'], dropna = True, observed=False)
    .agg(
        min_HP = ('HP', 'min'),
        max_HP = ('HP', 'max'),
        mean_HP = ('HP', 'mean')
    )
    .reset_index() # Reset index to turn the group keys into a column
)
#     Type_1    Type_2  min_HP  max_HP    mean_HP
# 0      Bug       Bug     NaN     NaN        NaN
# 1      Bug      Dark     NaN     NaN        NaN
# 2      Bug    Dragon     NaN     NaN        NaN
# 3      Bug  Electric    50.0    70.0  60.000000
# 4      Bug     Fairy     NaN     NaN        NaN
# ..     ...       ...     ...     ...        ...
# 319  Water    Poison    40.0    80.0  61.666667
# 320  Water   Psychic    60.0    95.0  87.000000
# 321  Water      Rock    54.0   100.0  70.750000
# 322  Water     Steel    84.0    84.0  84.000000
# 323  Water     Water     NaN     NaN        NaN


#------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 3. df.groupby.apply() ---------------------------------------------#
#------------------------------------------------------------------------------------------------------------#

def atk_stats(group):
    return pd.Series({
        'min_ATK': group['Attack'].min(),
        'max_ATK': group['Attack'].max(),
        'mean_ATK': group['Attack'].mean()
    })

print(
    df_pokemon
    .groupby(by = 'Type_1', observed=False) # observed=False to include all categories in the group keys
    .apply(atk_stats, include_groups = False) # include_groups=False to exclude group keys in the result index
    .reset_index() # Reset index to turn the group keys into a column
)
#       Type_1  min_ATK  max_ATK    mean_ATK
# 0        Bug     10.0    185.0   70.971014
# 1       Dark     50.0    150.0   88.387097
# 2     Dragon     50.0    180.0  112.125000
# 3   Electric     30.0    123.0   69.090909
# 4      Fairy     20.0    131.0   61.529412
# 5   Fighting     35.0    145.0   96.777778
# 6       Fire     30.0    160.0   84.769231
# 7     Flying     30.0    115.0   78.750000
# 8      Ghost     30.0    165.0   73.781250
# 9      Grass     27.0    132.0   73.214286
# 10    Ground     40.0    180.0   95.750000
# 11       Ice     30.0    130.0   72.750000
# 12    Normal      5.0    160.0   73.469388
# 13    Poison     43.0    106.0   74.678571
# 14   Psychic     20.0    190.0   71.456140
# 15      Rock     40.0    165.0   92.863636
# 16     Steel     24.0    150.0   92.703704
# 17     Water     10.0    155.0   74.151786