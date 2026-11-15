'''
There are 2 main ways to encoding categorical data into numeric codes:
    1. Factorize: `pd.factorize()` or `pd.col('column').astype('category').cat.codes`
    2. One-Hot encoding: `pd.get_dummies()`
'''

from pathlib import Path

import pandas as pd
from pandas import col as c

pd.set_option("display.width", 150)

data_dir = next(Path('/home').rglob('*/DataScience_MachineLearning/data'))

df_pokemon = (
    pd.read_csv(data_dir/"pokemon.csv")
    .pipe(lambda df: df.set_axis(df.columns.str.strip().str.replace(r"\s+", "_", regex=True).str.replace(".", "").str.lower(), axis=1))
    .reindex(columns=['name', 'type_1', 'type_2'])
    .assign(
        type_1 = c('type_1').astype('category'),
        type_2 = c('type_2').astype('category'),
    )
)

print(df_pokemon.head())
#                     name type_1  type_2
# 0              Bulbasaur  Grass  Poison
# 1                Ivysaur  Grass  Poison
# 2               Venusaur  Grass  Poison
# 3  VenusaurMega Venusaur  Grass  Poison
# 4             Charmander   Fire     NaN

print(df_pokemon.info())
# <class 'pandas.DataFrame'>
# RangeIndex: 800 entries, 0 to 799
# Data columns (total 3 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   name    800 non-null    str
#  1   type_1  800 non-null    category
#  2   type_2  414 non-null    category
# dtypes: category(2), str(1)
# memory usage: 15.3 KB
# None

# ====================================================================================
# 1. Factorize: `pd.factorize()` or `pd.col('column').astype('category').cat.codes`
# ====================================================================================

##------------------##
## `pd.factorize()` ##
##------------------##

print(
    df_pokemon
    .assign(
        type_1_enc = lambda df: pd.factorize(df['type_1'])[0],
        type_2_enc = lambda df: pd.factorize(df['type_2'])[0],
    )
)
#                       name   type_1  type_2  type_1_enc  type_2_enc
# 0                Bulbasaur    Grass  Poison           0           0
# 1                  Ivysaur    Grass  Poison           0           0
# 2                 Venusaur    Grass  Poison           0           0
# 3    VenusaurMega Venusaur    Grass  Poison           0           0
# 4               Charmander     Fire     NaN           1          -1
# ..                     ...      ...     ...         ...         ...
# 795                Diancie     Rock   Fairy          11           4
# 796    DiancieMega Diancie     Rock   Fairy          11           4
# 797    HoopaHoopa Confined  Psychic   Ghost          10          15
# 798     HoopaHoopa Unbound  Psychic    Dark          10          11
# 799              Volcanion     Fire   Water           1          12
# [800 rows x 5 columns]
'''
The `pd.factorize()` returns a tuple of 2 objects like this:
```
print(pd.factorize(s_gender))
# (array([0, 0, 1, 0, 2, 1, 0, 1, 2, 0]), Index(['M', 'F', 'LGBTQ'], dtype='object'))
```

Therefore, must use `pd.factorize(input)[0]` to get the encoded values
'''

##-------------------------------------------------##
## `pd.col('column').astype('category').cat.codes` ##
##-------------------------------------------------##

print(
    df_pokemon
    .assign(
        type_1_enc = c('type_1').astype('category').cat.codes,
        type_2_enc = c('type_2').astype('category').cat.codes,
    )
)
#                       name   type_1  type_2  type_1_enc  type_2_enc
# 0                Bulbasaur    Grass  Poison           9          13
# 1                  Ivysaur    Grass  Poison           9          13
# 2                 Venusaur    Grass  Poison           9          13
# 3    VenusaurMega Venusaur    Grass  Poison           9          13
# 4               Charmander     Fire     NaN           6          -1
# ..                     ...      ...     ...         ...         ...
# 795                Diancie     Rock   Fairy          15           4
# 796    DiancieMega Diancie     Rock   Fairy          15           4
# 797    HoopaHoopa Confined  Psychic   Ghost          14           8
# 798     HoopaHoopa Unbound  Psychic    Dark          14           1
# 799              Volcanion     Fire   Water           6          17
# [800 rows x 5 columns]

# =================================================================================
# 2. One-Hot encoding: `pd.get_dummies()`
# =================================================================================

print(
    df_pokemon
    .pipe(
        lambda df: pd.get_dummies(df, columns=['type_1'], drop_first=True)
    )
    .iloc[:, :5] # show first 5 columns only
)
#                       name  type_2  type_1_Dark  type_1_Dragon  type_1_Electric
# 0                Bulbasaur  Poison        False          False            False
# 1                  Ivysaur  Poison        False          False            False
# 2                 Venusaur  Poison        False          False            False
# 3    VenusaurMega Venusaur  Poison        False          False            False
# 4               Charmander     NaN        False          False            False
# ..                     ...     ...          ...            ...              ...
# 795                Diancie   Fairy        False          False            False
# 796    DiancieMega Diancie   Fairy        False          False            False
# 797    HoopaHoopa Confined   Ghost        False          False            False
# 798     HoopaHoopa Unbound    Dark        False          False            False
# 799              Volcanion   Water        False          False            False
# [800 rows x 5 columns]

print(
    df_pokemon
    .pipe(
        lambda df: pd.get_dummies(df, columns=['type_1', 'type_2'], drop_first=True, dtype='int')
    )
    .iloc[:, [0, 1, 2, 3, -3, -2, -1]]
)
#                       name  type_1_Dark  type_1_Dragon  type_1_Electric  type_2_Rock  type_2_Steel  type_2_Water
# 0                Bulbasaur            0              0                0            0             0             0
# 1                  Ivysaur            0              0                0            0             0             0
# 2                 Venusaur            0              0                0            0             0             0
# 3    VenusaurMega Venusaur            0              0                0            0             0             0
# 4               Charmander            0              0                0            0             0             0
# ..                     ...          ...            ...              ...          ...           ...           ...
# 795                Diancie            0              0                0            0             0             0
# 796    DiancieMega Diancie            0              0                0            0             0             0
# 797    HoopaHoopa Confined            0              0                0            0             0             0
# 798     HoopaHoopa Unbound            0              0                0            0             0             0
# 799              Volcanion            0              0                0            0             0             1
# [800 rows x 7 columns]
