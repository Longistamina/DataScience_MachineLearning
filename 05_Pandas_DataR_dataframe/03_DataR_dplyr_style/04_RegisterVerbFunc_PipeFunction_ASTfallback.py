'''
1. register_verb(): Change some function names (dr.filter_(), dr.slice_())

2. register_func(): for chainability
   + Register a single function for another package (like scipy.stats.shapiro)
   + NumPy functions: no need to be registered, they are automatically available in DataR
   + Use np.apply_along_axis() for functions like scipy.stats.shapiro

3. dr.pipe()
   + Apply custom lambda functions (usefull for pandas methods)
   + Apply user-defined functions directly in the pipe chain
   + Apply sicpy.stats functions without registering

4. Set __ast_fallback="normal" to avoid PipeableCallCheckWarning
'''

import datar.all as dr
from datar import f
import pandas as pd

from pipda import register_verb, register_func


#######################
## Datar preparation ##
#######################

df_baseball = pd.read_csv(
    filepath_or_buffer="05_Pandas_DataR_dataframe/data/baseball.csv",
    usecols=["Name", "Team", "Height", "Weight"],
    dtype={"Team": "category"}
)

print(df_baseball >> dr.slice_head(4))
#               Name       Team  Height  Weight
#           <object> <category> <int64> <int64>
# 0    Adam_Donachie        BAL      74     180
# 1        Paul_Bako        BAL      74     215
# 2  Ramon_Hernandez        BAL      72     210
# 3     Kevin_Millar        BAL      72     210


#---------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 1. register_verb() -----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

###################################################
## register_verb() to change some conflict names ##
###################################################

dr.filter = register_verb(func=dr.filter_)

'''
dr.filter_() to avoid conflict with Python built-in function filter()
=> Use registter_verb to bring it back as dr.filter()
'''

print(
    df_baseball 
    >> dr.filter((f.Height > 75) & (f.Weight <= 200))
    >> dr.slice_head(4)
)
#               Name       Team  Height  Weight
#           <object> <category> <int64> <int64>
# 22     Kris_Benson        BAL      76     195
# 30      James_Hoey        BAL      78     200
# 42    Ryan_Sweeney        CWS      76     200
# 57  Mike_MacDougal        CWS      76     195


#---------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 2. register_func() -----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

###################################################
## Register a single function for other packages ##
###################################################

from scipy import stats

# Register scipy.stats.shapiro as dr.shapiro
dr.shapiro = register_func(func=stats.shapiro)

'''MUST USE register_func()'''

print(
    df_baseball
    >> dr.reframe(
        height_shapiro = dr.shapiro(f.Height),
        weight_shapiro = dr.shapiro(f.Weight)
    )
    >> dr.pipe(lambda f: f.set_index(pd.Index(["W-statistic", "p_value"])))
)
#              height_shapiro  weight_shapiro
#                   <float64>       <float64>
# W-statistic    9.805285e-01    9.887039e-01
# p_value        2.075369e-10    4.815328e-07

##############################################
## NumPy functions NO NEED TO BE REGISTERED ##
##############################################

import numpy as np

print(
    df_baseball
    >> dr.reframe(
        height_quantiles = np.quantile(f.Height, q=[0.25, 0.5, 0.75]),
        weight_quantiles = np.quantile(f.Weight, q=[0.25, 0.5, 0.75])
    )
    >> dr.pipe(lambda f: f.set_index(pd.Index(["Q1", "Q2", "Q3"]))) # rename the index
)
#     height_quantiles  weight_quantiles
#            <float64>         <float64>
# Q1              72.0             186.0
# Q2              74.0             200.0
# Q3              75.0             215.0

##############################################
## Use np.apply_along_axis() for functions like scipy.stats.shapiro  ##
##############################################

import numpy as np
from scipy import stats

print(
    df_baseball
    >> dr.reframe(
        height_shapiro = np.apply_along_axis(stats.shapiro, 0, f.Height),
        weight_shapiro = np.apply_along_axis(stats.shapiro, 0, f.Height)
    )
    >> dr.pipe(lambda f: f.set_index(pd.Index(["W-statistic", "p_value"])))
)
#              height_shapiro  weight_shapiro
#                   <float64>       <float64>
# W-statistic    9.805285e-01    9.805285e-01
# p_value        2.075369e-10    2.075369e-10


#---------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 3. dr.pipe() ---------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

##################################################
## dr.pipe() to apply custom functions directly ##
##################################################

print(
    df_baseball 
    >> dr.filter((f.Height > 75) & (f.Weight <= 200))
    >> dr.pipe(lambda f: f.set_axis(f.columns.str.upper(), axis=1)) # rename the columns to uppercase (use pandas method)
    >> dr.slice_head(4)
)
#               NAME       TEAM  HEIGHT  WEIGHT
#           <object> <category> <int64> <int64>
# 22     Kris_Benson        BAL      76     195
# 30      James_Hoey        BAL      78     200
# 42    Ryan_Sweeney        CWS      76     200
# 57  Mike_MacDougal        CWS      76     195

###########################################
## dr.pipe() with user-defined functions ##
###########################################

def bmi_calculate(df):
    bmi = df.Weight / (df.Height ** 2) * 703
    return df.assign(BMI = bmi)

print(
    df_baseball 
    >> dr.pipe(bmi_calculate)  # apply user-defined function directly in the pipe chain
    >> dr.slice_head(4)
)
#               Name       Team  Height  Weight        BMI
#           <object> <category> <int64> <int64>  <float64>
# 0    Adam_Donachie        BAL      74     180  23.108108
# 1        Paul_Bako        BAL      74     215  27.601351
# 2  Ramon_Hernandez        BAL      72     210  28.478009
# 3     Kevin_Millar        BAL      72     210  28.478009

##########################################
## dr.pipe() with scipy.stats functions ##
##########################################

'''
The cumulative distribution function (CDF) takes a value and returns the probability 
that a random variable is less than or equal to that value; 

The percent-point function (PPF), also called the inverse CDF or quantile function, 
takes a probability and returns the corresponding value whose CDF equals that probability. 

In short: CDF input is a value and output is a probability in; 
PPF input is a probability in and output is a value on the distribution's scale.

########################

In this example,  for the sake of reframing demonstration,
we will calculate the PPF values for the 25th, 50th, 75th, and 100th percentiles,
but for different distributions: normal and gamma.

height ~ normal distribution
weight ~ gamma distribution
'''

from scipy import stats

print(
    df_baseball
    >> dr.reframe(
        height_norm = dr.pipe(lambda f: stats.norm.ppf(q=[0.25, 0.5, 0.75, 1], loc=f['Height'].mean(), scale=f['Height'].std())),
        weight_gamma = dr.pipe(lambda f: stats.gamma.ppf(q=[0.25, 0.5, 0.75, 1], a=2, scale=f['Weight'].mean() / 2))
    )
    >> dr.pipe(lambda f: f.set_axis(["ppf_25th", "ppf_50th", "ppf_75th", "ppf_100th"], axis=0)) # rename the index
)
#            height_norm  weight_gamma
#              <float64>     <float64>
# ppf_25th     72.128932     96.776148
# ppf_50th     73.689655    168.966550
# ppf_75th     75.250379    271.079323
# ppf_100th          inf           inf


#-------------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 4. Set __ast_fallback="normal" --------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
'''
While using Pipe Operator ">>", you might encounter PipeableCallCheckWarning for some complex expressions.

To avoid this warning, you can set the argument __ast_fallback="normal" in the function called.
'''

####################################
## Cause PipeableCallCheckWarning ##
####################################

print(
    df_baseball
    >> dr.mutate(Team = dr.as_factor(f.Team))
    >> dr.slice_head(4)
)
# /home/longdpt/miniconda3/envs/data/lib/python3.12/site-packages/pipda/utils.py:82: PipeableCallCheckWarning: Failed to detect AST node calling `as_factor`, assuming a normal call.
#   warnings.warn(
#               Name       Team  Height  Weight
#           <object> <category> <int64> <int64>
# 0    Adam_Donachie        BAL      74     180
# 1        Paul_Bako        BAL      74     215
# 2  Ramon_Hernandez        BAL      72     210
# 3     Kevin_Millar        BAL      72     210

#############################################
## Set __ast_fallback="normal" to avoid it ##
#############################################

print(
    df_baseball
    >> dr.mutate(Team = dr.as_factor(f.Team, __ast_fallback="normal"))
    >> dr.slice_head(4)
)
#               Name       Team  Height  Weight
#           <object> <category> <int64> <int64>
# 0    Adam_Donachie        BAL      74     180
# 1        Paul_Bako        BAL      74     215
# 2  Ramon_Hernandez        BAL      72     210
# 3     Kevin_Millar        BAL      72     210

'''No more PipeableCallCheckWarning'''