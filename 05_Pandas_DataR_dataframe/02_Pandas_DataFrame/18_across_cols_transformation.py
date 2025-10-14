'''
1. df.apply() across columns to modify values

2. df.pipe(), df.assign() and df.select_dtypes().columns
=>  df.pipe(
        lambda df: df.assign(**{
            col: df[col].str.lower() 
            for col in df.select_dtypes(include=["object", "category"]).columns 
            if (conditions like: (col != "Name") and (df[col] != "some_value"))
        })
    )
'''

import pandas as pd

#----------------------------------------------------------------------------------------------------------------#
#--------------------------------- 1. df.apply() across columns to modify values --------------------------------#
#----------------------------------------------------------------------------------------------------------------#
'''Using df.apply() will modify all the columns of the dataframe with the same function'''

df_boston = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/BostonHousing.csv")
    .drop(columns=["CHAS", "RAD", "CAT. MEDV"], axis = 1)
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

def min_max_scaler(series):
    series = pd.Series(series)  # Ensure input is a pandas Series
    return (series - series.min()) / (series.max() - series.min())

#################################################
## Use df.apply() to min-max scale all columns ##
#################################################

df_boston_scaled = df_boston.apply(min_max_scaler)

print(df_boston_scaled.head())
#        crim    zn     indus       nox        rm       age       dis       tax   ptratio     lstat      medv
# 0  0.000000  0.18  0.067815  0.314815  0.577505  0.641607  0.269203  0.208015  0.287234  0.089680  0.422222
# 1  0.000236  0.00  0.242302  0.172840  0.547998  0.782698  0.348962  0.104962  0.553191  0.204470  0.368889
# 2  0.000236  0.00  0.242302  0.172840  0.694386  0.599382  0.348962  0.104962  0.553191  0.063466  0.660000
# 3  0.000293  0.00  0.063050  0.150206  0.658555  0.441813  0.448545  0.066794  0.648936  0.033389  0.631111
# 4  0.000705  0.00  0.063050  0.150206  0.687105  0.528321  0.448545  0.066794  0.648936  0.099338  0.693333


#----------------------------------------------------------------------------------------------------------------#
#--------------------------- 2. df.pipe(), df.assign() and df.select_dtypes().columns ---------------------------#
#----------------------------------------------------------------------------------------------------------------#
'''Using df.pipe(), df.assign() and df.select_dtypes().columns to modify specific type of columns'''

df_baseball = df_baseball = pd.read_csv(
    filepath_or_buffer = "05_Pandas_DataR_dataframe/data/baseball.csv",
    dtype = {
        "Team": "category",
        "Position": "category",
        "PosCategory": "category",
    }
)

print(df_baseball.head())
#               Name Team       Position  Height  Weight    Age PosCategory
# 0    Adam_Donachie  BAL        Catcher      74     180  22.99     Catcher
# 1        Paul_Bako  BAL        Catcher      74     215  34.69     Catcher
# 2  Ramon_Hernandez  BAL        Catcher      72     210  30.78     Catcher
# 3     Kevin_Millar  BAL  First_Baseman      72     210  35.43   Infielder
# 4      Chris_Gomez  BAL  First_Baseman      73     188  35.71   Infielder

print(df_baseball.dtypes)
# Name             object
# Team           category
# Position       category
# Height            int64
# Weight            int64
# Age             float64
# PosCategory    category
# dtype: object

##########################################################################################
## Use df.pipe(), df.assign() and df.select_dtypes().columns to log all numeric columns ##
##########################################################################################

import numpy as np

df_baseball_log = df_baseball.pipe(
    lambda df: df.assign(**{col: np.log(df[col]) for col in df.select_dtypes(include=np.number).columns})
)

print(df_baseball_log.head())
#               Name Team       Position    Height    Weight       Age PosCategory
# 0    Adam_Donachie  BAL        Catcher  4.304065  5.192957  3.135059     Catcher
# 1        Paul_Bako  BAL        Catcher  4.304065  5.370638  3.546451     Catcher
# 2  Ramon_Hernandez  BAL        Catcher  4.276666  5.347108  3.426865     Catcher
# 3     Kevin_Millar  BAL  First_Baseman  4.276666  5.347108  3.567559   Infielder
# 4      Chris_Gomez  BAL  First_Baseman  4.290459  5.236442  3.575431   Infielder

#################################################################################################
## Use df.pipe(), df.assign() and df.select_dtypes().columns lowercase all str and cat columns ##
#################################################################################################

df_baseball_lower = df_baseball.pipe(
    lambda df: df.assign(**{
        col: df[col].str.lower() # Lowercase string values
        for col in df.select_dtypes(include=["object", "category"]).columns # For all str and cat columns
        if (col != "Name") # But exclude "Name" column
    })
)

print(df_baseball_lower.head())
#               Name Team       Position  Height  Weight    Age PosCategory
# 0    Adam_Donachie  bal        catcher      74     180  22.99     catcher
# 1        Paul_Bako  bal        catcher      74     215  34.69     catcher
# 2  Ramon_Hernandez  bal        catcher      72     210  30.78     catcher
# 3     Kevin_Millar  bal  first_baseman      72     210  35.43   infielder
# 4      Chris_Gomez  bal  first_baseman      73     188  35.71   infielder