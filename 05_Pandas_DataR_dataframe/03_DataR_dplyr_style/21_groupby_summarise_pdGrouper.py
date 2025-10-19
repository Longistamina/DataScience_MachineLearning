'''
1. dr.group_by()
   + use with dr.summarise() and dr.n()
   + combine with dr.arrange() to sort keys
   + multiple grouping variables

2. dr.group_trim(): remove groups with all NA values

3. dr.group_map(): apply a function to all the groups

4. combine with pd.Grouper for time-based grouping

5. dr.group_split(): split a groupped DataFrame into a list of DataFrames
'''

import datar.all as dr
from datar import f
import pandas as pd
import numpy as np

# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")

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


#--------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 1. dr.group_by() ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

###########################################
## Use with dr.summarise() - basic usage ##
###########################################

print(
    tb_pokemon
    >> dr.group_by(f.Type_1)
    >> dr.summarise(
        count = dr.n(), # Get the current group size
        avg_total = np.mean(f.Total),
        max_speed = np.max(f.Speed)
    )
)
#        Type_1   count   avg_total  max_speed
#    <category> <int64>   <float64>    <int64>
# 0       Grass      70  421.142857        145
# 1        Fire      52  458.076923        126
# 2       Water     112  430.455357        122
# 3         Bug      69  378.927536        160
# 4      Normal      98  401.683673        135
# 5      Poison      28  399.142857        130
# 6    Electric      44  443.409091        140
# 7      Ground      32  437.500000        120
# 8       Fairy      17  413.176471         99
# 9    Fighting      27  416.444444        118
# 10    Psychic      57  475.947368        180
# 11       Rock      44  453.750000        150
# 12      Ghost      32  439.562500        130
# 13        Ice      24  433.458333        110
# 14     Dragon      32  550.531250        120
# 15       Dark      31  445.741935        125
# 16      Steel      27  487.703704        110
# 17     Flying       4  485.000000        123

############################################
## Combine with dr.arrange() to sort keys ##
############################################

'''Ascending order'''

print(
    tb_pokemon
    >> dr.group_by(f.Type_2)
    >> dr.summarise(
        count = dr.n(),
        avg_atk = np.mean(f.Attack),
        medn_def = np.max(f.Defense)
    )
    >> dr.arrange(f.Type_2)
)
#        Type_2   count     avg_atk  medn_def
#    <category> <int64>   <float64>   <int64>
# 17        Bug       3   90.000000       100
# 12       Dark      20  109.800000       150
# 3      Dragon      18   94.444444       120
# 14   Electric       6   72.666667       120
# 5       Fairy      23   61.608696       150
# 7    Fighting      26  112.846154       129
# 15       Fire      12   81.250000       160
# 2      Flying      97   80.288660       140
# 16      Ghost      14   84.142857       150
# 6       Grass      25   74.160000       122
# 4      Ground      35   89.857143       230
# 10        Ice      14   98.000000       180
# 18     Normal       4   52.750000        72
# 0      Poison      34   67.588235       123
# 8     Psychic      33   74.696970       180
# 11       Rock      14   84.000000       230
# 9       Steel      22   92.590909       168
# 13      Water      14   70.142857       125
# 1         NaN     386   74.525907       230

'''Descending order'''

print(
    tb_pokemon
    >> dr.group_by(f.Type_2)
    >> dr.summarise(
        count = dr.n(),
        avg_atk = np.mean(f.Attack),
        medn_def = np.max(f.Defense)
    )
    >> dr.arrange(dr.desc(f.Type_2))
)
#        Type_2   count     avg_atk  medn_def
#    <category> <int64>   <float64>   <int64>
# 13      Water      14   70.142857       125
# 9       Steel      22   92.590909       168
# 11       Rock      14   84.000000       230
# 8     Psychic      33   74.696970       180
# 0      Poison      34   67.588235       123
# 18     Normal       4   52.750000        72
# 10        Ice      14   98.000000       180
# 4      Ground      35   89.857143       230
# 6       Grass      25   74.160000       122
# 16      Ghost      14   84.142857       150
# 2      Flying      97   80.288660       140
# 15       Fire      12   81.250000       160
# 7    Fighting      26  112.846154       129
# 5       Fairy      23   61.608696       150
# 14   Electric       6   72.666667       120
# 3      Dragon      18   94.444444       120
# 12       Dark      20  109.800000       150
# 17        Bug       3   90.000000       100
# 1         NaN     386   74.525907       230

#################################
## Multiple grouping variables ##
#################################

print(
    tb_pokemon
    >> dr.group_by(f.Type_1, f.Legendary)
    >> dr.summarise(
        avg_total = dr.mean(f.Total)
    )
    >> dr.arrange(f.Type_1, f.Legendary)
)
# ValueError: operands could not be broadcast together with shapes (36,) (33,)

print(
    tb_pokemon
    .groupby(['Type_1', 'Legendary'], dropna=False)
    .agg(
        count=('Total', 'size'),
        avg_total=('Total', 'mean')
    )
    .reset_index()
    .rename(columns={'Total': 'avg_total'})
    .sort_values(['Type_1','Legendary'])
)
#        Type_1  Legendary   count   avg_total
#    <category>     <bool> <int64>   <float64>
# 0         Bug      False      69  378.927536
# 1         Bug       True       0         NaN
# 2        Dark      False      29  432.344828
# 3        Dark       True       2  640.000000
# 4      Dragon      False      20  476.850000
# 5      Dragon       True      12  673.333333