'''
The agg() method applies aggregation functions to Series or DataFrame, returning a single value or a Series of values.

Key Features:
+ Can apply single or multiple aggregation functions
+ Returns scalar, Series, or DataFrame depending on input
+ Supports both string function names and custom functions

#################

+ Single Function
+ Multiple Functions
+ Dictionary Style
+ Rename Row-Names
'''

import pandas as pd
import numpy as np

df_baseball = pd.read_csv(
    filepath_or_buffer = "05_Pandas_DataR_dataframe/data/baseball.csv",
    usecols = ["Name", "Team", "Height", "Weight"],
    dtype = {"Team": "category"}
).copy().assign(
    Height = lambda df: df["Height"] * 2.54,
    Weight = lambda df: df["Weight"] * 0.453592,
    Team = lambda df: df["Team"].astype("category")
)

print(df_baseball.head(3))
#               Name Team  Height    Weight
# 0    Adam_Donachie  BAL  187.96  81.64656
# 1        Paul_Bako  BAL  187.96  97.52228
# 2  Ramon_Hernandez  BAL  182.88  95.25432

####################################
## Aggregate with Single Function ##
####################################

print(
    df_baseball[["Height", "Weight"]].agg("mean")
)
# Height    187.171724
# Weight     91.330191
# dtype: float64

print(
    df_baseball[["Height", "Weight"]]
    .agg(np.median)
)
# Height    187.9600
# Weight     90.7184
# dtype: float64

print(
    df_baseball[["Height", "Weight"]]
    .agg(lambda col: np.quantile(col, q=[0.25, 0.5, 0.75, 1]))
    .set_axis(["Q1", "Q2", "Q3", "Q4"], axis=0)
)
#     Height      Weight
# Q1  182.88   84.368112
# Q2  187.96   90.718400
# Q3  190.50   97.522280
# Q4  210.82  131.541680

#######################################
## Aggregate with Multiple Functions ##
#######################################

print(
    df_baseball[["Height", "Weight"]]
    .agg(["mean", "median", "std"])
)
#             Height     Weight
# mean    187.171724  91.330191
# median  187.960000  90.718400
# std       5.877387   9.445198

############################
## Using dictionary style ##
############################

print(
    df_baseball
    .agg({
        "Height": ["min", "max", "mean"],
        "Weight": ["median", "var", np.std]
    })
)
#             Height     Weight
# min     170.180000        NaN
# max     210.820000        NaN
# mean    187.171724        NaN
# median         NaN  90.718400
# var            NaN  89.211770
# std            NaN   9.445198

######################
## Rename row-names ##
######################

print(
    df_baseball[["Height", "Weight"]]
    .agg(
        mean_height = ("Height", "mean"),
        median_weight = ("Weight", "median"),
        std_weight = ("Weight", np.std) 
    )
)
#                    Height     Weight
# mean_height    187.171724        NaN
# median_weight         NaN  90.718400
# std_weight            NaN   9.445198