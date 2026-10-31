'''
The agg() method applies aggregation functions to Series or DataFrame, returning a single value or a Series of values.

Key Features:
+ Can apply single or multiple aggregation functions
+ Returns scalar, Series, or DataFrame depending on input
+ Supports both string function names and custom functions

##-------------##

+ Single Function
+ Multiple Functions
+ Dictionary Style
+ Rename Row-Names
'''

from pathlib import Path

import numpy as np
import pandas as pd
from pandas import col as c

data_dir = Path.home().rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

df_baseball = (
    pd.read_csv(
        filepath_or_buffer=data_dir/"baseball.csv",
        usecols=["Name", "Team", "Height", "Weight"],
        dtype={"Team": "category"}
    )
    .rename(columns=lambda col: col.lower())
    .assign(
        height = c("height") * 2.54,
        weight = c("weight") * 0.453592,
        team = c("team").astype("category")
    )
)

print(df_baseball.head(3))
#               name team  height    weight
# 0    Adam_Donachie  BAL  187.96  81.64656
# 1        Paul_Bako  BAL  187.96  97.52228
# 2  Ramon_Hernandez  BAL  182.88  95.25432

##--------------------------------##
## Aggregate with Single Function ##
##--------------------------------##

print(df_baseball['height'].agg('mean'))
# 187.17172413793105

print(
    df_baseball
    .reindex(columns=['height', 'weight'])
    .agg('mean')
)
# height    187.171724
# weight     91.330191
# dtype: float64

print(
    df_baseball
    .reindex(columns=['height', 'weight'])
    .agg(np.median)
)
# Height    187.9600
# Weight     90.7184
# dtype: float64

print(
    df_baseball
    .reindex(columns=['height', 'weight'])
    .agg(lambda col: np.quantile(col, q=[0.25, 0.5, 0.75, 1]))
    .set_axis(["Q1", "Q2", "Q3", "Q4"], axis=0)
)
#     height      weight
# Q1  182.88   84.368112
# Q2  187.96   90.718400
# Q3  190.50   97.522280
# Q4  210.82  131.541680

##-----------------------------------##
## Aggregate with Multiple Functions ##
##-----------------------------------##

print(
    df_baseball
    .reindex(columns=['height', 'weight'])
    .agg(["mean", "median", "std"])
)
#             height     weight
# mean    187.171724  91.330191
# median  187.960000  90.718400
# std       5.877387   9.445198

##------------------------##
## Using dictionary style ##
##------------------------##

print(
    df_baseball
    .agg({
        "height": ["min", "max", "mean"],
        "weight": ["median", "var", np.std]
    })
)
#             height     weight
# min     170.180000        NaN
# max     210.820000        NaN
# mean    187.171724        NaN
# median         NaN  90.718400
# var            NaN  89.211770
# std            NaN   9.445198

##------------------##
## Rename row-names ##
##------------------##

print(
    df_baseball
    .reindex(columns=['height', 'weight'])
    .agg(
        mean_height = ("height", "mean"),
        median_weight = ("weight", "median"),
        std_weight = ("weight", np.std)
    )
)
#                    height     weight
# mean_height    187.171724        NaN
# median_weight         NaN  90.718400
# std_weight            NaN   9.445198
