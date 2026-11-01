'''
1. Unordered categories
2. Ordered categories
3. Boolean: binary True/False
'''

from pathlib import Path

import pandas as pd
from pandas import col as c

pd.set_option("display.width", 150)

data_dir = next(Path('/home').rglob('*/DataScience_MachineLearning/data'))

df_pokemon = (
    pd.read_csv(data_dir/"pokemon.csv")
    .drop(columns=["#"])
    .pipe(lambda df: df.set_axis(df.columns.str.strip().str.replace(r"\s+", "_", regex=True).str.replace(".", "").str.lower(), axis=1))
)

print(df_pokemon.head())
#                     name type_1  type_2  total  hp  attack  defense  sp_atk  sp_def  speed  generation  legendary
# 0              Bulbasaur  Grass  Poison    318  45      49       49      65      65     45           1      False
# 1                Ivysaur  Grass  Poison    405  60      62       63      80      80     60           1      False
# 2               Venusaur  Grass  Poison    525  80      82       83     100     100     80           1      False
# 3  VenusaurMega Venusaur  Grass  Poison    625  80     100      123     122     120     80           1      False
# 4             Charmander   Fire     NaN    309  39      52       43      60      50     65           1      False

# ================================================================================
# 1. Unordered categories
# ================================================================================

print(
    df_pokemon
    .assign(
        type_1 = c('type_1').astype('category'),
        type_2 = c('type_2').astype('category'),
    )
    .reindex(columns=['type_1', 'type_2'])
    .info()
)
# <class 'pandas.DataFrame'>
# RangeIndex: 800 entries, 0 to 799
# Data columns (total 2 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   type_1  800 non-null    category
#  1   type_2  414 non-null    category
# dtypes: category(2)
# memory usage: 2.2 KB
# None

# ================================================================================
# 2. Ordered categories
# ================================================================================

##----------------------------------------##
## Simple conversion: `.cat.as_ordered()` ##
##----------------------------------------##

print(
    df_pokemon
    .assign(
        generation = c('generation').astype('category').cat.as_ordered() # must convert `astype('category')` first
    )
    .reindex(columns=['generation'])
    .squeeze()
)
# 0      1
# 1      1
# 2      1
# 3      1
# 4      1
#       ..
# 795    6
# 796    6
# 797    6
# 798    6
# 799    6
# Name: generation, Length: 800, dtype: category
# Categories (6, int64): [1 < 2 < 3 < 4 < 5 < 6]

##--------------------------------------------------------##
## Higher-control conversion: `.cat.reorder_categories()` ##
##--------------------------------------------------------##

print(
    df_pokemon
    .assign(
        generation = c('generation').astype('category').cat.reorder_categories(ordered=True, new_categories=[gen for gen in range(6, 0, -1)])
    )                                                                                                      # [6, 5, ..., 1]
    .reindex(columns=['generation'])
    .squeeze()
)
# 0      1
# 1      1
# 2      1
# 3      1
# 4      1
#       ..
# 795    6
# 796    6
# 797    6
# 798    6
# 799    6
# Name: generation, Length: 800, dtype: category
# Categories (6, int64): [6 < 5 < 4 < 3 < 2 < 1]

##-------------------------------------------------------------------------------------------##
## Filter ordered categories with relationship operators (>, <, =, >=, <=, !=, is_between()) ##
##-------------------------------------------------------------------------------------------##
'''
Should set the categories in ascending order, like:
# Categories (6, int64): [1 < 2 < 3 < 4 < 5 < 6]
'''

print(
    df_pokemon
    .assign(
        generation = c('generation').astype('category').cat.reorder_categories(ordered=True, new_categories=[gen for gen in range(1, 7)])
    )                                                                                                      # [1, 2, ..., 6]
    .reindex(columns=['name', 'generation'])
    .loc[c('generation') > 3]
)
#                     name generation
# 432              Turtwig          4
# 433               Grotle          4
# 434             Torterra          4
# 435             Chimchar          4
# 436             Monferno          4
# ..                   ...        ...
# 795              Diancie          6
# 796  DiancieMega Diancie          6
# 797  HoopaHoopa Confined          6
# 798   HoopaHoopa Unbound          6
# 799            Volcanion          6
# [368 rows x 2 columns]

print(
    df_pokemon
    .assign(
        generation = c('generation').astype('category').cat.reorder_categories(ordered=True, new_categories=[gen for gen in range(1, 7)])
    )                                                                                                      # [1, 2, ..., 6]
    .reindex(columns=['name', 'generation'])
    .loc[c('generation').between(3, 5, inclusive='both')]
)
#                         name generation
# 272                  Treecko          3
# 273                  Grovyle          3
# 274                 Sceptile          3
# 275    SceptileMega Sceptile          3
# 276                  Torchic          3
# ..                       ...        ...
# 713     KeldeoOrdinary Forme          5
# 714     KeldeoResolute Forme          5
# 715       MeloettaAria Forme          5
# 716  MeloettaPirouette Forme          5
# 717                 Genesect          5
# [446 rows x 2 columns]

# ================================================================================
# 3. Boolean: binary True/False
# ================================================================================

##--------------------##
## Convert to Boolean ##
##--------------------##

print(
    df_pokemon
    .assign(
        legendary = c('legendary').astype('bool')
    )
    .reindex(columns=['legendary'])
    .squeeze()
)
# 0      False
# 1      False
# 2      False
# 3      False
# 4      False
#        ...
# 795     True
# 796     True
# 797     True
# 798     True
# 799     True
# Name: legendary, Length: 800, dtype: bool

##----------------------------------------##
## Use Boolean column as filter condition ##
##----------------------------------------##

print(
    df_pokemon
    .assign(
        legendary = c('legendary').astype('bool')
    )
    .reindex(columns=['name', 'generation', 'legendary'])
    .iloc[c('legendary')]
)
#                     name  generation  legendary
# 156             Articuno           1       True
# 157               Zapdos           1       True
# 158              Moltres           1       True
# 162               Mewtwo           1       True
# 163  MewtwoMega Mewtwo X           1       True
# ..                   ...         ...        ...
# 795              Diancie           6       True
# 796  DiancieMega Diancie           6       True
# 797  HoopaHoopa Confined           6       True
# 798   HoopaHoopa Unbound           6       True
# 799            Volcanion           6       True
# [65 rows x 3 columns]

print(
    df_pokemon
    .assign(
        legendary = c('legendary').astype('bool')
    )
    .reindex(columns=['name', 'generation', 'legendary'])
    .iloc[~c('legendary')]
)
#                       name  generation  legendary
# 0                Bulbasaur           1      False
# 1                  Ivysaur           1      False
# 2                 Venusaur           1      False
# 3    VenusaurMega Venusaur           1      False
# 4               Charmander           1      False
# ..                     ...         ...        ...
# 787    GourgeistSuper Size           6      False
# 788               Bergmite           6      False
# 789                Avalugg           6      False
# 790                 Noibat           6      False
# 791                Noivern           6      False
# [735 rows x 3 columns]
