'''
Un like dr.mutate() and dr.summarise(), dr.reframe() allows returning a new DataFrame with a totally different shape.

(dr.mutate() requires the same number of rows as the original DataFrame,
 dr.summarise() returns a DataFrame the same number of columns as the original DataFrame.)

####################################

1. dr.reframe() - how to use

2. dr.reframe() and dr.across(): apply the same reframing function to multiple columns of the DataFrame.

3. dr.reframe() with different reframing functions
'''

import datar.all as dr
from datar import f
import pandas as pd

from scipy import stats
import numpy as np

########################

tb_pokemon = dr.tibble(
    pd.read_csv("05_Pandas_DataR_dataframe/data/pokemon.csv")
    >> dr.rename_with(lambda col: col.strip().replace(" ", "_").replace(".", "")) # Clean column names
    >> dr.select(~f["#"]) # Drop the "#" column
    >> dr.mutate(
        Type_1 = f.Type_1.astype("category"),      # convert to category (pandas style)
        Type_2 = dr.as_factor(f.Type_2),           # convert to category (datar style)
        Generation = dr.as_ordered(f.Generation),  # convert to ordered category (datar style)
        Legendary = dr.as_logical(f.Legendary)     # convert to boolean (datar style)
    )
)

print(
    tb_pokemon
    >> dr.slice_head(n=5)
)
#                     Name     Type_1     Type_2      HP  Attack  Defense   Speed Generation
#                 <object> <category> <category> <int64> <int64>  <int64> <int64> <category>
# 0              Bulbasaur      Grass     Poison      45      49       49      45          1
# 1                Ivysaur      Grass     Poison      60      62       63      60          1
# 2               Venusaur      Grass     Poison      80      82       83      80          1
# 3  VenusaurMega Venusaur      Grass     Poison      80     100      123      80          1
# 4             Charmander       Fire        NaN      39      52       43      65          1


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 1. dr.reframe() - how to use ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#####################################################
## Example 2: calculate quantiles for some columns ##
#####################################################

print(
    tb_pokemon
    >> dr.reframe(
        HP_quantiles = np.quantile(f.HP, q=[0.25, 0.5, 0.75, 1]),            
        Attack_quantiles = np.quantile(f['Attack'], q=[0.25, 0.5, 0.75, 1]),    
        Defense_quantiles = np.quantile(f.Defense, q=[0.25, 0.5, 0.75, 1])
    )
    >> dr.pipe(lambda f: f.set_axis(["Q1", "Q2", "Q3", "Q4"], axis=0)) # rename the index
)
#     HP_quantiles  Attack_quantiles  Defense_quantiles
#        <float64>         <float64>          <float64>
# Q1          50.0              55.0               50.0
# Q2          65.0              75.0               70.0
# Q3          80.0             100.0               90.0
# Q4         255.0             190.0              230.0

#################################################################
## Example 1: calculate the Shapiro-Wilk test for some columns ##
#################################################################

from pipda import register_func
dr.shapiro = register_func(stats.shapiro)

print(
    tb_pokemon
    >> dr.reframe(
        HP_normality = dr.shapiro(f.HP),            
        Attack_normality = dr.shapiro(f['Attack']),    
        Defense_normality = dr.shapiro(f['Defense']),  
        Speed_normality = dr.shapiro(f.Speed)       
    )
    >> dr.pipe(lambda f: f.set_axis(["W-statistic", "p-value"], axis=0)) # rename the index
)
#              HP_normality  Attack_normality  Defense_normality  Speed_normality
#                 <float64>         <float64>          <float64>        <float64>
# W-statistic  9.158321e-01      9.789301e-01       9.380628e-01     9.841602e-01
# p-value      1.152364e-20      2.472154e-09       9.923172e-18     1.309542e-07


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 2. dr.reframe() and dr.across() ------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''Apply the same reframing function to multiple columns of the DataFrame.'''

#####################################################
## Example 1: calculate quantiles for some columns ##
#####################################################

print(
    tb_pokemon
    >> dr.reframe(
        dr.across(
            dr.where(dr.is_numeric),
            lambda col: np.quantile(col, q=[0.25, 0.5, 0.75, 1]),
            _names="{_col}_quantiles"
        )
    )
    >> dr.pipe(lambda f: f.set_axis(["Q1", "Q2", "Q3", "Q4"], axis=0)) # rename the index
)
#     HP_quantiles  Attack_quantiles  Defense_quantiles  Speed_quantiles
#        <float64>         <float64>          <float64>        <float64>
# Q1          50.0              55.0               50.0             45.0
# Q2          65.0              75.0               70.0             65.0
# Q3          80.0             100.0               90.0             90.0
# Q4         255.0             190.0              230.0            180.0

#################################################################
## Example 2: calculate the Shapiro-Wilk test for some columns ##
#################################################################

print(
    tb_pokemon
    >> dr.reframe(
        dr.across(
            f.Defense | f.Speed | f.Attack, # specify multiple columns with | (bitwise or)
            lambda col: stats.shapiro(col),
            _names="{_col}_normality" # _col is a placeholder for the original column name
        )
    )
    >> dr.pipe(lambda f: f.set_axis(["W-statistic", "p-value"], axis=0)) # rename the index
)
#              Defense_normality  Speed_normality  Attack_normality
#                      <float64>        <float64>         <float64>
# W-statistic       9.380628e-01     9.841602e-01      9.789301e-01
# p-value           9.923172e-18     1.309542e-07      2.472154e-09


#--------------------------------------------------------------------------------------------------------------#
#-------------------------- 3. dr.reframe() with different reframing functions --------------------------------#
#--------------------------------------------------------------------------------------------------------------#

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
but for different distributions: normal, exponential and gamma.

HP ~ normal distribution
Attack ~ exponential distribution
Defense ~ gamma distribution
'''

print(
    tb_pokemon
    >> dr.reframe(
        HP_norm = dr.pipe(lambda f: stats.norm.ppf(q=[0.25, 0.5, 0.75, 1], loc=f['HP'].mean(), scale=f['HP'].std())),
        Attack_exp = dr.pipe(lambda f: stats.expon.ppf(q=[0.25, 0.5, 0.75, 1], scale=f['Attack'].mean())),
        Defense_gamma = dr.pipe(lambda f: stats.gamma.ppf(q=[0.25, 0.5, 0.75, 1], a=2, scale=f['Defense'].mean() / 2))
    )
    >> dr.pipe(lambda f: f.set_axis(["ppf_25th", "ppf_50th", "ppf_75th", "ppf_100th"], axis=0)) # rename the index
)
#              HP_norm  Attack_exp  Defense_gamma
#            <float64>   <float64>      <float64>
# ppf_25th   52.035877   22.727243      35.491614
# ppf_50th   69.258750   54.759494      61.966669
# ppf_75th   86.481623  109.518987      99.415433
# ppf_100th        inf         inf            inf

