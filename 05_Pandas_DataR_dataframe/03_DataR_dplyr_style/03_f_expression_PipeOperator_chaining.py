'''
1. "f" expression syntax for DataFrame manipulation

3. Pipe Operator ">>" allows a feature like method chaining in pandas.
'''

import datar.all as dr
from datar import f
import pandas as pd

# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")

#---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 1. "f" expression ----------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

######################
## Data Preparation ##
######################

tb = dr.tibble(
    x = [1, 2, 3],
    y = ["a", "b", "c"],
    z = [True, False, True]
)
print(tb)
#         x        y      z
#   <int64> <object> <bool>
# 0       1        a   True
# 1       2        b  False
# 2       3        c   True

#-------------------------------------#

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['x', 'y', 'z'],
    'C': [True, False, True]
})
print(df)
#         A        B      C
#   <int64> <object> <bool>
# 0       1        x   True
# 1       2        y  False
# 2       3        z   True

'''
"f" expression syntax allows for more intuitive and readable DataFrame operations,
it liberates us from typing the DataFrame name repeatedly (like df[df['A'] > 1])

This also supports pandas DataFrame
'''

#################
## with tibble ##
#################

filtered_tb = tb >> dr.filter_(f.x > 1)
print(filtered_tb)
#         x        y      z
#   <int64> <object> <bool>
# 1       2        b  False
# 2       3        c   True

selected_tb = tb >> dr.select(f['y'], f['z'])
print(selected_tb)
#          y      z
#   <object> <bool>
# 0        a   True
# 1        b  False
# 2        c   True

selected_tb2 = tb >> dr.select(f[['x', 'z']])
print(selected_tb2)
#         x      z
#   <int64> <bool>
# 0       1   True
# 1       2  False
# 2       3   True

'''
filtered_tb = tb[f.x > 1, f.y]

THIS WILL NOT WORK
'''

####################
## with pandas df ##
####################

filtered_df = df >> dr.filter_(f.A > 1)
print(filtered_df)
#         A        B      C
#   <int64> <object> <bool>
# 1       2        y  False
# 2       3        z   True

selected_df = df >> dr.select(f['B'], f['C'])
print(selected_df)
#          B      C
#   <object> <bool>
# 0        x   True
# 1        y  False
# 2        z   True

selected_df2 = df >> dr.select(f[['A', 'C']])
print(selected_df2)
#         A      C
#   <int64> <bool>
# 0       1   True
# 1       2  False
# 2       3   True


#---------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ 2. Pipe Operator ">>" ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#

'''
Pipe Operator ">>" allows chaining multiple DataFrame operations in a readable manner.
'''

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

###################

print(
    tb_pokemon
    >> dr.slice_head(n=5)
)
#                     Name     Type_1     Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed Generation  Legendary
#                 <object> <category> <category> <int64> <int64> <int64>  <int64> <int64> <int64> <int64> <category>     <bool>
# 0              Bulbasaur      Grass     Poison     318      45      49       49      65      65      45          1      False
# 1                Ivysaur      Grass     Poison     405      60      62       63      80      80      60          1      False
# 2               Venusaur      Grass     Poison     525      80      82       83     100     100      80          1      False
# 3  VenusaurMega Venusaur      Grass     Poison     625      80     100      123     122     120      80          1      False
# 4             Charmander       Fire        NaN     309      39      52       43      60      50      65          1      False

#########################

print(
    tb_pokemon
    >> dr.pull(f.Generation)
)
# 0      1
# 1      1
# 2      1
# 3      1
# 4      1
#       ..
# 795    6
# 796    6
# 797    6
# 798    6
# 799    6
# Name: Generation, Length: 800, dtype: category
# Categories (6, int64): [1 < 2 < 3 < 4 < 5 < 6]