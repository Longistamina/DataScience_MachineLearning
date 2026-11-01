'''
There are 2 main ways to discretize/bin numeric data
into categorical data:
    1. `pd.cut()`: Bin values into discrete intervals.
    2. `pd.qcut()`: Quantile-based discretization function.
'''

from pathlib import Path

import numpy as np  # import numpy to use np.inf
import pandas as pd

data_dir = next(Path('/home').rglob('*/DataScience_MachineLearning/data'))

df_pokemon = (
    pd.read_csv(data_dir/"pokemon.csv")
    .pipe(lambda df: df.set_axis(df.columns.str.strip().str.replace(r"\s+", "_", regex=True).str.replace(".", "").str.lower(), axis=1))
    .reindex(columns=['name', 'total'])
)

print(df_pokemon.head())
#                     name  total
# 0              Bulbasaur    318
# 1                Ivysaur    405
# 2               Venusaur    525
# 3  VenusaurMega Venusaur    625
# 4             Charmander    309

print(
    df_pokemon
    .reindex(columns=['total'])
    .quantile(q=[0.05, 0.25, 0.5, 0.75, 0.95])
    .reset_index()
    .rename(columns={'index': 'q'})
)
#       q  total
# 0  0.05  250.0
# 1  0.25  330.0
# 2  0.50  450.0
# 3  0.75  515.0
# 4  0.95  630.0

# ===========================================================
# 1. `pd.cut()`: Bin values into discrete intervals.
# ===========================================================

##---------------------##
## bins=number_of_bins ##
##---------------------##

print(
    df_pokemon
    .assign(
        total_bin = lambda df: pd.cut(x=df['total'], bins=3, labels=['low', 'medium', 'hight'])
    )
)
# name  total total_bin
# 0                Bulbasaur    318       low
# 1                  Ivysaur    405    medium
# 2                 Venusaur    525    medium
# 3    VenusaurMega Venusaur    625     hight
# 4               Charmander    309       low
# ..                     ...    ...       ...
# 795                Diancie    600     hight
# 796    DiancieMega Diancie    700     hight
# 797    HoopaHoopa Confined    600     hight
# 798     HoopaHoopa Unbound    680     hight
# 799              Volcanion    600     hight
# [800 rows x 3 columns]

##----------------------------------##
## bins=[list_of_defined_intervals] ##
##----------------------------------##

print(
    df_pokemon
    .assign(
        total_bin = lambda df: pd.cut(x=df['total'], bins=[-np.inf, 300, 500, np.inf], labels=['low', 'medium', 'hight'])
    )
)
#                       name  total total_bin
# 0                Bulbasaur    318    medium
# 1                  Ivysaur    405    medium
# 2                 Venusaur    525     hight
# 3    VenusaurMega Venusaur    625     hight
# 4               Charmander    309    medium
# ..                     ...    ...       ...
# 795                Diancie    600     hight
# 796    DiancieMega Diancie    700     hight
# 797    HoopaHoopa Confined    600     hight
# 798     HoopaHoopa Unbound    680     hight
# 799              Volcanion    600     hight
# [800 rows x 3 columns]
'''
(-np.inf, 300] -> low
(300, 500] -> medium
(500, np.inf] -> hight

the right boundary is included because of `right=True`
'''

# ===========================================================
# 2. `pd.qcut()`: Quantile-based discretization function.
# ===========================================================

##-----------------------##
## q=number_of_quantiles ##
##-----------------------##
'''
q=4 -> quartiles
q=10 -> deciles
'''

# quartiles
print(
    df_pokemon
    .assign(
        total_qs = lambda df: pd.qcut(x=df['total'], q=4, labels=['tiny', 'low', 'medium', 'hight'])
    )
)
#                       name  total total_qs
# 0                Bulbasaur    318     tiny
# 1                  Ivysaur    405      low
# 2                 Venusaur    525    hight
# 3    VenusaurMega Venusaur    625    hight
# 4               Charmander    309     tiny
# ..                     ...    ...      ...
# 795                Diancie    600    hight
# 796    DiancieMega Diancie    700    hight
# 797    HoopaHoopa Confined    600    hight
# 798     HoopaHoopa Unbound    680    hight
# 799              Volcanion    600    hight
# [800 rows x 3 columns]

# deciles
print(
    df_pokemon
    .assign(
        total_qs = lambda df: pd.qcut(x=df['total'], q=10, labels=[f'q{i}' for i in range(1, 11)])
    )
)
#                       name  total total_qs
# 0                Bulbasaur    318       q3
# 1                  Ivysaur    405       q4
# 2                 Venusaur    525       q8
# 3    VenusaurMega Venusaur    625      q10
# 4               Charmander    309       q2
# ..                     ...    ...      ...
# 795                Diancie    600       q9
# 796    DiancieMega Diancie    700      q10
# 797    HoopaHoopa Confined    600       q9
# 798     HoopaHoopa Unbound    680      q10
# 799              Volcanion    600       q9
# [800 rows x 3 columns]

##-----------------------##
## q=[list_of_quantiles] ##
##-----------------------##

print(
    df_pokemon
    .assign(
        total_qs = lambda df: pd.qcut(x=df['total'], q=[0., 0.35, 0.7, 1.], labels=['low', 'medium', 'high'])
    )
)
#                       name  total total_qs
# 0                Bulbasaur    318      low
# 1                  Ivysaur    405   medium
# 2                 Venusaur    525     high
# 3    VenusaurMega Venusaur    625     high
# 4               Charmander    309      low
# ..                     ...    ...      ...
# 795                Diancie    600     high
# 796    DiancieMega Diancie    700     high
# 797    HoopaHoopa Confined    600     high
# 798     HoopaHoopa Unbound    680     high
# 799              Volcanion    600     high
# [800 rows x 3 columns]
