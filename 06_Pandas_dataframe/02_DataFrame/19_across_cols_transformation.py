'''
1. df.apply() across columns to modify values

2. df.apply() with aggregation functions to reduce values

3. df.pipe(), df.assign() and df.select_dtypes().columns
=>  df.pipe(
        lambda df: df.assign(**{
            col: df[col].str.lower()
            for col in df.select_dtypes(include=["object", "category"]).columns
            if (conditions like: (col != "name") and (df[col] != "some_value"))
        })
    )
'''

from pathlib import Path

import numpy as np
import pandas as pd

data_dir = Path.home().rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

# ===========================================================
# 0. Data setup
# ===========================================================

##----------------##
## Boston Housing ##
##----------------##

df_boston = (
    pd.read_csv(data_dir/"BostonHousing.csv")
    .drop(columns=["CHAS", "RAD", "CAT. MEDV"])
    .pipe(lambda df: df.set_axis(df.columns.str.lower(), axis=1))
)

print(df_boston.head())
#       crim    zn  indus    nox     rm   age     dis  tax  ptratio  lstat  medv
# 0  0.00632  18.0   2.31  0.538  6.575  65.2  4.0900  296     15.3   4.98  24.0
# 1  0.02731   0.0   7.07  0.469  6.421  78.9  4.9671  242     17.8   9.14  21.6
# 2  0.02729   0.0   7.07  0.469  7.185  61.1  4.9671  242     17.8   4.03  34.7
# 3  0.03237   0.0   2.18  0.458  6.998  45.8  6.0622  222     18.7   2.94  33.4
# 4  0.06905   0.0   2.18  0.458  7.147  54.2  6.0622  222     18.7   5.33  36.2

print(df_boston.columns)
# Index(['crim', 'zn', 'indus', 'nox', 'rm', 'age', 'dis', 'tax', 'ptratio',
#        'lstat', 'medv'],
#       dtype='object')

##----------##
## Baseball ##
##----------##

df_baseball = (
    pd.read_csv(
        filepath_or_buffer=data_dir/"baseball.csv",
        dtype={"Team": "category", "Position": "category", "PosCategory": "category"}
    )
    .rename(columns=lambda col: col.lower())
)

print(df_baseball.head())
#               name team       position  height  weight    age poscategory
# 0    Adam_Donachie  BAL        Catcher      74     180  22.99     Catcher
# 1        Paul_Bako  BAL        Catcher      74     215  34.69     Catcher
# 2  Ramon_Hernandez  BAL        Catcher      72     210  30.78     Catcher
# 3     Kevin_Millar  BAL  First_Baseman      72     210  35.43   Infielder
# 4      Chris_Gomez  BAL  First_Baseman      73     188  35.71   Infielder

print(df_baseball.dtypes)
# name                str
# team           category
# position       category
# height            int64
# weight            int64
# age             float64
# poscategory    category
# dtype: object

# =========================================================================================
# 1. df.apply() across columns to modify values
# =========================================================================================
'''Using df.apply() will modify all the columns of the dataframe with the same function'''

##---------------------------------------------------##
## Use df.apply() with UDF min-max scale all columns ##
##---------------------------------------------------##

def min_max_scaler(series):
    series = pd.Series(series)  # Ensure input is a pandas Series
    return (series - series.min()) / (series.max() - series.min())

print(
    df_boston
    .apply(min_max_scaler)
    .head()
)
#        crim    zn     indus       nox        rm       age       dis       tax   ptratio     lstat      medv
# 0  0.000000  0.18  0.067815  0.314815  0.577505  0.641607  0.269203  0.208015  0.287234  0.089680  0.422222
# 1  0.000236  0.00  0.242302  0.172840  0.547998  0.782698  0.348962  0.104962  0.553191  0.204470  0.368889
# 2  0.000236  0.00  0.242302  0.172840  0.694386  0.599382  0.348962  0.104962  0.553191  0.063466  0.660000
# 3  0.000293  0.00  0.063050  0.150206  0.658555  0.441813  0.448545  0.066794  0.648936  0.033389  0.631111
# 4  0.000705  0.00  0.063050  0.150206  0.687105  0.528321  0.448545  0.066794  0.648936  0.099338  0.693333

##-------------------------------------------##
## Use df.apply() with lambda to all columns ##
##-------------------------------------------##

print(
    df_boston
    .apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    .head()
)
#        crim    zn     indus       nox        rm       age       dis       tax   ptratio     lstat      medv
# 0  0.000000  0.18  0.067815  0.314815  0.577505  0.641607  0.269203  0.208015  0.287234  0.089680  0.422222
# 1  0.000236  0.00  0.242302  0.172840  0.547998  0.782698  0.348962  0.104962  0.553191  0.204470  0.368889
# 2  0.000236  0.00  0.242302  0.172840  0.694386  0.599382  0.348962  0.104962  0.553191  0.063466  0.660000
# 3  0.000293  0.00  0.063050  0.150206  0.658555  0.441813  0.448545  0.066794  0.648936  0.033389  0.631111
# 4  0.000705  0.00  0.063050  0.150206  0.687105  0.528321  0.448545  0.066794  0.648936  0.099338  0.693333

# =========================================================================================
# 2. df.apply() with aggregation functions to reduce values
# =========================================================================================
'''Using df.apply() with aggregation functions to reduce values'''

##--------------------------------------------##
## Apply aggregation functions to all columns ##
##--------------------------------------------##

print(
    df_boston
    .apply(np.mean, axis=0) # Mean of all columns, axis=0 means apply function across rows for each column
)
# crim         3.613524
# zn          11.363636
# indus       11.136779
# nox          0.554695
# rm           6.284634
# age         68.574901
# dis          3.795043
# tax        408.237154
# ptratio     18.455534
# lstat       12.653063
# medv        22.532806
# dtype: float64

print(
    df_boston
    .apply(lambda x: x.mean())
)

print(
    df_boston
    .apply(np.std, axis=0) # std of all columns, axis=0 means apply function across rows for each column
)
# crim         8.593041
# zn          23.299396
# indus        6.853571
# nox          0.115763
# rm           0.701923
# age         28.121033
# dis          2.103628
# tax        168.370495
# ptratio      2.162805
# lstat        7.134002
# medv         9.188012
# dtype: float64

# =========================================================================================
# 3. df.pipe(), df.assign() and df.select_dtypes().columns
# =========================================================================================
'''Using df.pipe(), df.assign() and df.select_dtypes().columns to modify specific type of columns'''

##--------------------------------------------------------------------------------------##
## Use df.pipe(), df.assign() and df.select_dtypes().columns to log all numeric columns ##
##--------------------------------------------------------------------------------------##

print(
    df_baseball
    .pipe(
        lambda df: df.assign(**{
                col: df[col].apply(np.log) for col in df.select_dtypes(include=np.number).columns
            }
        )
    )
    .head()
)
#               name team       position    height    weight       age poscategory
# 0    Adam_Donachie  BAL        Catcher  4.304065  5.192957  3.135059     Catcher
# 1        Paul_Bako  BAL        Catcher  4.304065  5.370638  3.546451     Catcher
# 2  Ramon_Hernandez  BAL        Catcher  4.276666  5.347108  3.426865     Catcher
# 3     Kevin_Millar  BAL  First_Baseman  4.276666  5.347108  3.567559   Infielder
# 4      Chris_Gomez  BAL  First_Baseman  4.290459  5.236442  3.575431   Infielder

##---------------------------------------------------------------------------------------------##
## Use df.pipe(), df.assign() and df.select_dtypes().columns lowercase all str and cat columns ##
##---------------------------------------------------------------------------------------------##

print(
    df_baseball
    .pipe(
        lambda df: df.assign(**{
            col: df[col].str.lower() # Lowercase string values
            for col in df.select_dtypes(include=["string", "category"]).columns # For all str and cat columns
            if (col != "name") # But exclude "name" column
        })
    )
    .head()
)
#               name team       position  height  weight    age poscategory
# 0    Adam_Donachie  bal        catcher      74     180  22.99     catcher
# 1        Paul_Bako  bal        catcher      74     215  34.69     catcher
# 2  Ramon_Hernandez  bal        catcher      72     210  30.78     catcher
# 3     Kevin_Millar  bal  first_baseman      72     210  35.43   infielder
# 4      Chris_Gomez  bal  first_baseman      73     188  35.71   infielder
