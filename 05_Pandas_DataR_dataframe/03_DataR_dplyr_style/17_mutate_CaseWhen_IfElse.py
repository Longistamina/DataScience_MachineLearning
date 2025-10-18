'''
1. dr.mutate(): 
   + Modify existing columns
   + Derive new cols from existing columns 
   + Create completely new columns
   + Apply pandas methods inside dr.mutate()

2. dr.if_else(): vectorized conditional function, similar to numpy.where
   
3. dr.case_when(): vectorized multiple dr.if_else() statements
'''

import datar.all as dr
from datar import f
import pandas as pd
import numpy as np

# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")

########################

df_baseball = pd.read_csv(
    filepath_or_buffer = "05_Pandas_DataR_dataframe/data/baseball.csv",
    usecols = ["Name", "Team", "Height", "Weight"],
    dtype = {"Team": "category"}
)

print(df_baseball >> dr.slice_head(4))
#               Name       Team  Height  Weight
#           <object> <category> <int64> <int64>
# 0    Adam_Donachie        BAL      74     180
# 1        Paul_Bako        BAL      74     215
# 2  Ramon_Hernandez        BAL      72     210
# 3     Kevin_Millar        BAL      72     210


#-------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 1. dr.mutate() ----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

#############################
## Modify existing columns ##
#############################
'''Use existing col names to modify them'''

#---------------
## Single column modification
#---------------

print(
    df_baseball
    >> dr.mutate(Height = f.Height * 2.54)  # inch to cm
    >> dr.slice_head(4)
)
#               Name       Team    Height  Weight
#           <object> <category> <float64> <int64>
# 0    Adam_Donachie        BAL    187.96     180
# 1        Paul_Bako        BAL    187.96     215
# 2  Ramon_Hernandez        BAL    182.88     210
# 3     Kevin_Millar        BAL    182.88     210

#---------------
## Multiple columns modification
#---------------

print(
    df_baseball
    >> dr.mutate(
        Height = f.Height * 2.54,  # inch to cm
        Weight = f.Weight / 2.205   # lbs to kg
    )
    >> dr.slice_head(4)
)
#               Name       Team    Height     Weight
#           <object> <category> <float64>  <float64>
# 0    Adam_Donachie        BAL    187.96  81.632653
# 1        Paul_Bako        BAL    187.96  97.505669
# 2  Ramon_Hernandez        BAL    182.88  95.238095
# 3     Kevin_Millar        BAL    182.88  95.238095

###########################################
## Derive new columns from existing ones ##
###########################################
'''Use existing col names to create new ones'''

#---------------
## Derive single new column
#---------------

print(
    df_baseball
    >> dr.mutate(BMI = f.Weight / (f.Height**2))  # BMI formula
    >> dr.slice_head(4)
)
#               Name       Team  Height  Weight       BMI
#           <object> <category> <int64> <int64> <float64>
# 0    Adam_Donachie        BAL      74     180  0.032871
# 1        Paul_Bako        BAL      74     215  0.039262
# 2  Ramon_Hernandez        BAL      72     210  0.040509
# 3     Kevin_Millar        BAL      72     210  0.040509

#---------------
## Derive multiple new columns
#---------------

print(
    df_baseball
    >> dr.mutate(
        Height_cm = f.Height * 2.54,  # inch to cm
        Weight_kg = f.Weight / 2.205,   # lbs to kg
        BMI = f.Weight_kg / (f.Height_cm**2)  # BMI formula
    )
    >> dr.slice_head(4)
)
#               Name       Team  Height  Weight  Height_cm  Weight_kg       BMI
#           <object> <category> <int64> <int64>  <float64>  <float64> <float64>
# 0    Adam_Donachie        BAL      74     180     187.96  81.632653  0.002311
# 1        Paul_Bako        BAL      74     215     187.96  97.505669  0.002760
# 2  Ramon_Hernandez        BAL      72     210     182.88  95.238095  0.002848
# 3     Kevin_Millar        BAL      72     210     182.88  95.238095  0.002848

###################################
## Create completely new columns ##
###################################
'''Do not use existing col names'''

np.random.seed(0)

print(
    df_baseball
    >> dr.mutate(Raise = np.random.choice([True, False], size=len(df_baseball)))  # Randomly assign True or False
    >> dr.slice_head(4)
)
#               Name       Team  Height  Weight  Raise
#           <object> <category> <int64> <int64> <bool>
# 0    Adam_Donachie        BAL      74     180   True
# 1        Paul_Bako        BAL      74     215  False
# 2  Ramon_Hernandez        BAL      72     210  False
# 3     Kevin_Millar        BAL      72     210   True

#############################################
## Apply pandas methods inside dr.mutate() ##
#############################################

print(
    df_baseball
    >> dr.mutate(Team = f.Team.str.lower())  # Convert Team names to lowercase)
    >> dr.slice_head(4)
)
#               Name     Team  Height  Weight
#           <object> <object> <int64> <int64>
# 0    Adam_Donachie      bal      74     180
# 1        Paul_Bako      bal      74     215
# 2  Ramon_Hernandez      bal      72     210
# 3     Kevin_Millar      bal      72     210


#------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2. dr.if_else() -----------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------#

#############################
## Single-branch condition ##
#############################
'''If condition is True, return x; otherwise, return y'''

print(
    df_baseball
    >> dr.mutate(
        Weight_Status = dr.if_else(f.Weight >= 200, "Heavy", "Light")
    )
    >> dr.slice_head(6)
)
#               Name       Team  Height  Weight Weight_Status
#           <object> <category> <int64> <int64>      <object>
# 0    Adam_Donachie        BAL      74     180         Light
# 1        Paul_Bako        BAL      74     215         Heavy
# 2  Ramon_Hernandez        BAL      72     210         Heavy
# 3     Kevin_Millar        BAL      72     210         Heavy
# 4      Chris_Gomez        BAL      73     188         Light
# 5    Brian_Roberts        BAL      69     176         Light

############################
## Multi-branch condition ##
############################
'''
If condition1 is True, return x1; 
    else if condition2 is True, return x2; 
    else return y
'''

print(
    df_baseball
    >> dr.mutate(
        Weight_Status = dr.if_else(
            f.Weight < 150, "Light",
            dr.if_else(f.Weight <= 200, "Medium", "Heavy")
        )
    )
    >> dr.slice_head(6)
)
#               Name       Team  Height  Weight Weight_Status
#           <object> <category> <int64> <int64>      <object>
# 0    Adam_Donachie        BAL      74     180        Medium
# 1        Paul_Bako        BAL      74     215         Heavy
# 2  Ramon_Hernandez        BAL      72     210         Heavy
# 3     Kevin_Millar        BAL      72     210         Heavy
# 4      Chris_Gomez        BAL      73     188        Medium
# 5    Brian_Roberts        BAL      69     176        Medium


#------------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 3. dr.case_when() -----------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------#
'''Vectorise multiple dr.if_else() statements.'''

print(
    df_baseball
    >> dr.mutate(
        Height_Status = dr.case_when(
            f.Height < 68, "Short",
            f.Height <= 72, "Medium",
            f.Height > 72, "Tall"
        )
    )
    >> dr.slice_head(6)
)
#               Name       Team  Height  Weight Height_Status
#           <object> <category> <int64> <int64>      <object>
# 0    Adam_Donachie        BAL      74     180          Tall
# 1        Paul_Bako        BAL      74     215          Tall
# 2  Ramon_Hernandez        BAL      72     210        Medium
# 3     Kevin_Millar        BAL      72     210        Medium
# 4      Chris_Gomez        BAL      73     188          Tall
# 5    Brian_Roberts        BAL      69     176        Medium