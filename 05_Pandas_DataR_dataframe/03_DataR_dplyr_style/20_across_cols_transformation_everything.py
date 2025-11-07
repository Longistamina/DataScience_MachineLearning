'''
1. dr.across() with dr.mutate()
   + dr.across(f.col1 | f.col2): apply functions to specific columns
   + dr.across(dr.where() | &): apply functions to columns that meet certain conditions
   + dr.across(dr.everything()): apply a function to all columns

2. dr.across() with dr.summarise()
   + dr.across(dr.c(f.col1, f.col2))): apply functions to specific columns
   + dr.across(dr.where() & |): apply functions to columns that meet certain conditions
   + dr.across(dr.everything()): apply a function to all columns

3. dr.across() with dr.reframe()

dr.across(
   cols,
   func = lambda col: ...,
    _names = "{_col}_new" # _col is a placeholder for the original
)
'''

import datar.all as dr
from datar import f
import pandas as pd
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
#                     Name   Type_1   Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed  Generation  Legendary
                                                                                                                          
# #               <object> <object> <object> <int64> <int64> <int64>  <int64> <int64> <int64> <int64>     <int64>     <bool>
# 1              Bulbasaur    Grass   Poison     318      45      49       49      65      65      45           1      False
# 2                Ivysaur    Grass   Poison     405      60      62       63      80      80      60           1      False
# 3               Venusaur    Grass   Poison     525      80      82       83     100     100      80           1      False
# 3  VenusaurMega Venusaur    Grass   Poison     625      80     100      123     122     120      80           1      False
# 4             Charmander     Fire      NaN     309      39      52       43      60      50      65           1      False


#---------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 1. dr.across() with dr.mutate() ----------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

###########################################################
## dr.across(f.col1 | f.col2) to modify specific columns ##
###########################################################


#--------------------------------
## Use dr.across(f.col1 | f.col2) to lowercase
#--------------------------------

print(
    tb_pokemon
    >> dr.mutate(
        dr.across(
            f.Name | f.Type_1 | f.Type_2, # Apply to specific columns
            dr.tolower # Function to apply (lowercase)
        )
    )
    >> dr.slice_head(n=5)
    >> dr.select(f.Name, f.Type_1, f.Type_2) # Only show modified columns
)
#                     Name   Type_1   Type_2
                                          
# #               <object> <object> <object>
# 1              bulbasaur    grass   poison
# 2                ivysaur    grass   poison
# 3               venusaur    grass   poison
# 3  venusaurmega venusaur    grass   poison
# 4             charmander     fire      NaN

################################################################

print(tb_pokemon >> dr.where(dr.is_character))
# ['Name', 'Type_1']
'''Only "Name" and "Type_1" are character, because "Type_2" has NaN values, so dr does not consider it as character'''

tb_pkm_chr = (
    tb_pokemon
    >> dr.mutate(
        dr.across(
            f.Name | f.Type_1 | f.Type_2, # Apply to specific columns
            dr.as_character # Convert all these columns to character
        )
    )
)

print(tb_pkm_chr >> dr.where(dr.is_character))
# ['Name', 'Type_1', 'Type_2']
'''Now "Type_2" is also character'''

#--------------------------------
## Use dr.across(f.col1 | f.col2) to convert to float
#--------------------------------

print(
    tb_pokemon
    >> dr.mutate(
        dr.across(
            f.HP | f.Attack | f.Defense, # Apply to specific
            lambda col: col.astype(float) # Function to apply (convert to float)
        )
    )
    >> dr.slice_head(n=5)
    >> dr.select(f.HP, f.Attack, f.Defense) # Only show modified columns
)
#          HP    Attack   Defense
                               
# # <float64> <float64> <float64>
# 1      45.0      49.0      49.0
# 2      60.0      62.0      63.0
# 3      80.0      82.0      83.0
# 3      80.0     100.0     123.0
# 4      39.0      52.0      43.0

#--------------------------------
## Use dr.across(f.col1 | f.col2) to convert to ordered categorical
#--------------------------------

print(
    tb_pokemon
    >> dr.mutate(
        dr.across(
            f.Generation | f.Legendary, # Apply to specific columns
            dr.as_ordered # Convert to ordered categorical
        )
    )
    >> dr.slice_head(n=5)
    >> dr.select(f.Name, f.Generation, f.Legendary)
)
#                     Name Generation  Legendary
                                              
# #               <object> <category> <category>
# 1              Bulbasaur          1      False
# 2                Ivysaur          1      False
# 3               Venusaur          1      False
# 3  VenusaurMega Venusaur          1      False
# 4             Charmander          1      False

#######################################################################
## Use dr.across(dr.where() | &) to modify cols satisfied conditions ##
#######################################################################

def min_max_scaler(series):
    series = pd.Series(series)  # Ensure input is a pandas Series
    return (series - series.min()) / (series.max() - series.min())

#--------------------------------
## Use dr.across(dr.where(dr.is_numeric) & ~f["Generation", "Legendary"])
#--------------------------------

print(
    tb_pokemon
    >> dr.mutate(
        dr.across(
            dr.where(dr.is_numeric) & (~f["Generation", "Legendary"]), # Apply to all numeric columns (except "Generation" and "Legendary")
            min_max_scaler # Function to apply
        )
    )
    >> dr.slice_head(n=5)
)
#                     Name   Type_1   Type_2     Total        HP    Attack   Defense    Sp_Atk    Sp_Def     Speed  Generation  Legendary
                                                                                                                                       
# #               <object> <object> <object> <float64> <float64> <float64> <float64> <float64> <float64> <float64>     <int64>     <bool>
# 1              Bulbasaur    Grass   Poison  0.230000  0.173228  0.237838  0.195556  0.298913  0.214286  0.228571           1      False
# 2                Ivysaur    Grass   Poison  0.375000  0.232283  0.308108  0.257778  0.380435  0.285714  0.314286           1      False
# 3               Venusaur    Grass   Poison  0.575000  0.311024  0.416216  0.346667  0.489130  0.380952  0.428571           1      False
# 3  VenusaurMega Venusaur    Grass   Poison  0.741667  0.311024  0.513514  0.524444  0.608696  0.476190  0.428571           1      False
# 4             Charmander     Fire      NaN  0.215000  0.149606  0.254054  0.168889  0.271739  0.142857  0.342857           1      False

#--------------------------------
## Use dr.across(dr.where(dr.is_character) & ~f.Name)
#--------------------------------

print(
    tb_pkm_chr
    >> dr.mutate(
        dr.across(
            dr.where(dr.is_character) & (~f.Name), # Apply to all string columns except the "Name"
            lambda col: col.str.lower() # Function to apply
        )
    )
    >> dr.slice_head(n=5)
)
#                     Name   Type_1   Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed  Generation  Legendary
                                                                                                                          
# #               <object> <object> <object> <int64> <int64> <int64>  <int64> <int64> <int64> <int64>     <int64>     <bool>
# 1              Bulbasaur    grass   poison     318      45      49       49      65      65      45           1      False
# 2                Ivysaur    grass   poison     405      60      62       63      80      80      60           1      False
# 3               Venusaur    grass   poison     525      80      82       83     100     100      80           1      False
# 3  VenusaurMega Venusaur    grass   poison     625      80     100      123     122     120      80           1      False
# 4             Charmander     fire      nan     309      39      52       43      60      50      65           1      False

'''If use tb_pokemon instead of tb_pkm_chr, "Type_2" will not be modified because it has NaN values, not is_character'''

print(
    tb_pokemon
    >> dr.mutate(
        dr.across(
            dr.where(dr.is_character) & (~f.Name), # Apply to all string columns except the "Name"
            dr.tolower # Function to apply
        )
    )
    >> dr.slice_head(n=5)
)
#                     Name   Type_1   Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed  Generation  Legendary
                                                                                                                          
# #               <object> <object> <object> <int64> <int64> <int64>  <int64> <int64> <int64> <int64>     <int64>     <bool>
# 1              Bulbasaur    grass   Poison     318      45      49       49      65      65      45           1      False
# 2                Ivysaur    grass   Poison     405      60      62       63      80      80      60           1      False
# 3               Venusaur    grass   Poison     525      80      82       83     100     100      80           1      False
# 3  VenusaurMega Venusaur    grass   Poison     625      80     100      123     122     120      80           1      False
# 4             Charmander     fire      NaN     309      39      52       43      60      50      65           1      False


######################################################
## dr.across(dr.everything()) to modify all columns ##
######################################################

print(
    tb_pokemon
    >> dr.mutate(
        dr.across(
            dr.everything(), # Apply to all columns
            dr.as_character # Convert all cols to string
        )
    )
    >> dr.slice_head(n=5)
)
#                     Name   Type_1   Type_2    Total       HP   Attack  Defense   Sp_Atk   Sp_Def    Speed Generation Legendary
                                                                                                                              
# #               <object> <object> <object> <object> <object> <object> <object> <object> <object> <object>   <object>  <object>
# 1              Bulbasaur    Grass   Poison      318       45       49       49       65       65       45          1     False
# 2                Ivysaur    Grass   Poison      405       60       62       63       80       80       60          1     False
# 3               Venusaur    Grass   Poison      525       80       82       83      100      100       80          1     False
# 3  VenusaurMega Venusaur    Grass   Poison      625       80      100      123      122      120       80          1     False
# 4             Charmander     Fire      nan      309       39       52       43       60       50       65          1     False


#-----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 2. dr.across() with dr.summarise() ----------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------#

###############################################
## dr.across(f.col1 | f.col2): specific cols ##
###############################################

print(
    tb_pokemon
    >> dr.summarise(
        dr.across(
            f.HP | f.Attack | f.Defense | f.Sp_Atk | f.Sp_Def | f.Speed,
            dr.mean,
            _names = "avg_{_col}" # _col is a placeholder for the original column name
        )
    )
)
#      avg_HP  avg_Attack  avg_Defense  avg_Sp_Atk  avg_Sp_Def  avg_Speed
#   <float64>   <float64>    <float64>   <float64>   <float64>  <float64>
# 0  69.25875    79.00125      73.8425       72.82     71.9025    68.2775

#################################################
## dr.across(dr.where() & |): conditional cols ##
#################################################

print(
    tb_pokemon
    >> dr.summarise(
        dr.across(
            dr.where(dr.is_numeric) & (~f.Legendary), # All numeric columns except 'Legendary'
            lambda col: np.quantile(col, [0.25, 0.5, 0.75]),
            _names = "quantile_{_col}" # _col is a placeholder for the original column name
        )
    )
    >> dr.mutate(id = ["Q1", "Median", "Q3"]) # Add an id column for the quantiles
    >> dr.column_to_rownames("id") # Set the id column as row names
)
#         quantile_Total  quantile_HP  quantile_Attack       quantile_Sp_Def  quantile_Speed  quantile_Generation
#              <float64>    <float64>        <float64>  ...        <float64>       <float64>            <float64>
# Q1               330.0         50.0             55.0  ...             50.0            45.0                  2.0
# Median           450.0         65.0             75.0  ...             70.0            65.0                  3.0
# Q3               515.0         80.0            100.0  ...             90.0            90.0                  5.0

#################################################################
## dr.across(dr.everything()): apply a function to all columns ##
#################################################################

#------------------------
## Count NA values in each column
#------------------------

print(
    tb_pokemon
    >> dr.summarise(
        dr.across(
            dr.everything(), # Apply to all columns
            lambda col: col.isna().sum() # Function to apply (count NA values in each column)
        )
    )
)
#      Name  Type_1  Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed  Generation  Legendary
#   <int64> <int64> <int64> <int64> <int64> <int64>  <int64> <int64> <int64> <int64>     <int64>    <int64>
# 0       0       0     386       0       0       0        0       0       0       0           0          0

#------------------------
## Count unique values in each column
#------------------------

print(
    tb_pokemon
    >> dr.summarise(
        dr.across(
            dr.everything(), # Apply to all columns
            lambda col: len(col.unique()) # Function to apply (count unique values in each column)
        )
    )
)
#      Name  Type_1  Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed  Generation  Legendary
#   <int64> <int64> <int64> <int64> <int64> <int64>  <int64> <int64> <int64> <int64>     <int64>    <int64>
# 0     800      18      19     200      94     111      103     105      92     108           6          2


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------- 3. dr.across() with dr.reframe() -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''Apply the same reframing function to multiple columns of the DataFrame.'''

from scipy import stats

tb_pokemon = dr.tibble(
    pd.read_csv(
        filepath_or_buffer = "05_Pandas_DataR_dataframe/data/pokemon.csv",
        dtype = {
            "Type 1": "category",
            "Type 2": "category",
            "Generation": "category"
        }
    )
    .pipe(lambda f: f.set_axis(f.columns.str.strip().str.replace(r"\s+", "_", regex = True).str.replace(".", ""), axis=1))
    .drop(columns = ["Total", "#", "Sp_Atk", "Sp_Def", "Legendary"])
    .assign(Generation = lambda f: f['Generation'].cat.as_ordered())
)

#################################################################
## Example 1: calculate the Shapiro-Wilk test for some columns ##
#################################################################

print(
    tb_pokemon
    >> dr.reframe(
        dr.across(
            f.Defense | f.Speed | f.Attack, # specify multiple columns with | (bitwise or)
            lambda col: stats.shapiro(col),
            _names = "{_col}_normality" # _col is a placeholder for the original column name
        )
    )
    >> dr.pipe(lambda f: f.set_axis(["W-statistic", "p-value"], axis=0)) # rename the index
)
#              Defense_normality  Speed_normality  Attack_normality
#                      <float64>        <float64>         <float64>
# W-statistic       9.380628e-01     9.841602e-01      9.789301e-01
# p-value           9.923172e-18     1.309542e-07      2.472154e-09

#####################################################
## Example 2: calculate quantiles for some columns ##
#####################################################

print(
    tb_pokemon
    >> dr.reframe(
        dr.across(
            dr.where(dr.is_numeric),
            lambda col: np.quantile(col, q=[0.25, 0.5, 0.75, 1]),
            _names = "{_col}_quantiles"
        )
    )
    >> dr.pipe(lambda f: f.set_axis(["Q1", "Q2", "Q3", "Q4"], axis=0)) # rename the index
)
#     HP_quantiles  Attack_quantiles  Defense_quantiles  Speed_quantiles
#        <float64>         <float64>          <float64>        <float64>
# Q1        19.975            9.9875             9.9875           9.9875
# Q2        20.000           10.0000            15.0000          10.0000
# Q3        20.000           19.9625            15.0000          15.0000
# Q4        24.950           20.0000            20.0000          15.0000