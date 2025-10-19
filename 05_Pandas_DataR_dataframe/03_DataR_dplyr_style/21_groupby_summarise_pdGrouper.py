'''
1. dr.group_by()
   + use with dr.summarise() to perform group-wise operations
   + combine with dr.arrange() to sort keys before grouping
   + combine with f.sort_values() to sort keys before grouping
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