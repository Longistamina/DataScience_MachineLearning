'''
1. df.groupby().agg(): Aggregate data using specified functions.
   + count the group size: count = ('column_name', 'size')
   + df.groupby(sort=True/False): Sort group keys.
   + df.groupby().dropna(): drop NaN values in group keys.

2. df.groupby().apply(): Apply a function to each group.

3. pd.Grouper(): Flexible grouping by time, frequency, or other criteria.
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


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. df.groupby().agg() ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##########################
## Count the group size ##
##########################

print(
    df_pokemon
    .groupby(by = 'Type_1', observed=False) # observed=False to include all categories in the group keys
    .agg(
        count = ('HP', 'size'),  # Count the number of entries in each group
        avg_HP = ('HP', 'mean')  # Calculate the mean of the 'HP' column for each group
    )
)
#            count     avg_HP
                           
# Type_1   <int64>  <float64>
# Bug           69  56.884058
# Dark          31  66.806452
# Dragon        32  83.312500
# Electric      44  59.795455
# Fairy         17  74.117647
# Fighting      27  69.851852
# Fire          52  69.903846
# Flying         4  70.750000
# Ghost         32  64.437500
# Grass         70  67.271429
# Ground        32  73.781250
# Ice           24  72.000000
# Normal        98  77.275510
# Poison        28  67.250000
# Psychic       57  70.631579
# Rock          44  65.363636
# Steel         27  65.222222
# Water        112  72.062500

print(
    df_pokemon
    .groupby(by = 'Type_1', observed=False) # observed=False to include all categories in the group keys
    .agg(
        count = ('HP', 'size'),  # Count the number of entries in each group
        avg_HP = ('HP', 'mean')  # Calculate the mean of the 'HP' column for each group
    )
    .reset_index() # Reset index to turn the group keys into a column
)
#        Type_1   count     avg_HP
#    <category> <int64>  <float64>
# 0         Bug      69  56.884058
# 1        Dark      31  66.806452
# 2      Dragon      32  83.312500
# 3    Electric      44  59.795455
# 4       Fairy      17  74.117647
# 5    Fighting      27  69.851852
# 6        Fire      52  69.903846
# 7      Flying       4  70.750000
# 8       Ghost      32  64.437500
# 9       Grass      70  67.271429
# 10     Ground      32  73.781250
# 11        Ice      24  72.000000
# 12     Normal      98  77.275510
# 13     Poison      28  67.250000
# 14    Psychic      57  70.631579
# 15       Rock      44  65.363636
# 16      Steel      27  65.222222
# 17      Water     112  72.062500

#################################
## df.groupby(sort=True/False) ##
#################################

'''Single grouping key, sort = False'''

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

'''Multiple grouping keys, sort = True'''

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

###########################
## df.groupby().dropna() ##
###########################

print(
    df_pokemon
    .groupby(by = ['Type_1', 'Type_2'], dropna = True, observed=False)
    .agg(
        min_HP = ('HP', 'min'),
        max_HP = ('HP', 'max'),
        mean_HP = ('HP', 'mean')
    )
    .dropna() # Drop rows with NaN values in the result
    .reset_index() # Reset index to turn the group keys into a column
)
#     Type_1    Type_2  min_HP  max_HP    mean_HP
# 0      Bug  Electric    50.0    70.0  60.000000
# 1      Bug  Fighting    80.0    80.0  80.000000
# 2      Bug      Fire    55.0    85.0  70.000000
# 3      Bug    Flying    30.0    86.0  63.000000
# 4      Bug     Ghost     1.0     1.0   1.000000
# ..     ...       ...     ...     ...        ...
# 131  Water       Ice    50.0   130.0  90.000000
# 132  Water    Poison    40.0    80.0  61.666667
# 133  Water   Psychic    60.0    95.0  87.000000
# 134  Water      Rock    54.0   100.0  70.750000
# 135  Water     Steel    84.0    84.0  84.000000


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. df.groupby().apply() ---------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

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


#----------------------------------------------------------------------------------------------------------#
#------------------------------------------- 3. pd.Grouper() ----------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

##################################
## Read the Air Quality dataset ##
##################################

df_aq = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/air_quality_no2_long.csv")
    .rename(columns={"date.utc": "date"})
    .assign(date = lambda df: pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S%z"))
)

print(df_aq.head())
#     city country                       date location parameter  value   unit
# 0  Paris      FR  2019-06-21 00:00:00+00:00  FR04014       no2   20.0  µg/m³
# 1  Paris      FR  2019-06-20 23:00:00+00:00  FR04014       no2   21.8  µg/m³
# 2  Paris      FR  2019-06-20 22:00:00+00:00  FR04014       no2   26.5  µg/m³
# 3  Paris      FR  2019-06-20 21:00:00+00:00  FR04014       no2   24.9  µg/m³
# 4  Paris      FR  2019-06-20 20:00:00+00:00  FR04014       no2   21.4  µg/m³

print(df_aq.info())
# RangeIndex: 2068 entries, 0 to 2067
# Data columns (total 7 columns):
#  #   Column     Non-Null Count  Dtype              
# ---  ------     --------------  -----              
#  0   city       2068 non-null   object             
#  1   country    2068 non-null   object             
#  2   date       2068 non-null   datetime64[ns, UTC]        # MUST BE datetime TYPE (NOT object)
#  3   location   2068 non-null   object             
#  4   parameter  2068 non-null   object             
#  5   value      2068 non-null   float64            
#  6   unit       2068 non-null   object             
# dtypes: datetime64[ns, UTC](1), float64(1), object(5)

###############################################################################
## Groupby using pd.Grouper, calculate the mean every 5 days, and by country ##
###############################################################################

'''NOTE: pd.Grouper requires the "date" column to be datetime type.'''

df_aq_grouped_5d = (
    df_aq.copy()
    .groupby([pd.Grouper(key="date", freq="5D"), "country"])
    .agg({"value": "mean"})
    .reset_index() # to turn the index back into columns
)

print(df_aq_grouped_5d)
#                         date country      value
# 0  2019-05-07 00:00:00+00:00      BE  24.900000
# 1  2019-05-07 00:00:00+00:00      FR  29.314655
# 2  2019-05-07 00:00:00+00:00      GB  31.800000
# 3  2019-05-12 00:00:00+00:00      BE  18.722222
# 4  2019-05-12 00:00:00+00:00      FR  21.440336
# 5  2019-05-12 00:00:00+00:00      GB  28.983193
# 6  2019-05-17 00:00:00+00:00      BE  24.177083
# 7  2019-05-17 00:00:00+00:00      FR  32.217500
# 8  2019-05-17 00:00:00+00:00      GB  31.966667
# 9  2019-05-22 00:00:00+00:00      BE  47.500000
# 10 2019-05-22 00:00:00+00:00      FR  34.037607
# 11 2019-05-22 00:00:00+00:00      GB  29.949580
# 12 2019-05-27 00:00:00+00:00      BE  11.800000
# 13 2019-05-27 00:00:00+00:00      FR  22.678333
# 14 2019-05-27 00:00:00+00:00      GB  18.336134
# 15 2019-06-01 00:00:00+00:00      BE  33.750000
# 16 2019-06-01 00:00:00+00:00      FR  29.729060
# 17 2019-06-01 00:00:00+00:00      GB  21.725000
# 18 2019-06-06 00:00:00+00:00      BE  14.250000
# 19 2019-06-06 00:00:00+00:00      FR  21.750485
# 20 2019-06-06 00:00:00+00:00      GB  17.991304
# 21 2019-06-11 00:00:00+00:00      BE  22.200000
# 22 2019-06-11 00:00:00+00:00      FR  30.191453
# 23 2019-06-11 00:00:00+00:00      GB  20.330357
# 24 2019-06-16 00:00:00+00:00      BE  40.833333
# 25 2019-06-16 00:00:00+00:00      FR  27.820270
# 26 2019-06-16 00:00:00+00:00      GB  15.057143
# 27 2019-06-21 00:00:00+00:00      FR  20.000000