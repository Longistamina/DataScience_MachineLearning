'''
1. dr.slice_head() - Return the first n rows.

2. dr.slice_tail() - Return the last n rows.

3. dr.glimpse() - Transpose print of tibble, showing data types and a preview of data (like df.info())
'''

import datar.all as dr
from datar import f
import pandas as pd


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

#--------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 1. dr.slice_head() ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

###########################
## Show the first 3 rows ##
############################

print(
    tb_pokemon >> dr.slice_head(n=3)
)
#         Name     Type_1     Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed Generation  Legendary
#     <object> <category> <category> <int64> <int64> <int64>  <int64> <int64> <int64> <int64> <category>     <bool>
# 0  Bulbasaur      Grass     Poison     318      45      49       49      65      65      45          1      False
# 1    Ivysaur      Grass     Poison     405      60      62       63      80      80      60          1      False
# 2   Venusaur      Grass     Poison     525      80      82       83     100     100      80          1      False

####################################
## Show the first 1 row (default) ##
####################################

print(
    tb_pokemon 
    >> dr.slice_head()
)
#         Name     Type_1     Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed Generation  Legendary
#     <object> <category> <category> <int64> <int64> <int64>  <int64> <int64> <int64> <int64> <category>     <bool>
# 0  Bulbasaur      Grass     Poison     318      45      49       49      65      65      45          1      False


#--------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------- 2. dr.slice_tail() ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

##########################
## Show the last 3 rows ##
##########################

print(
    tb_pokemon >> dr.slice_tail(n=3)
)
#                     Name     Type_1     Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed Generation  Legendary
#                 <object> <category> <category> <int64> <int64> <int64>  <int64> <int64> <int64> <int64> <category>     <bool>
# 797  HoopaHoopa Confined    Psychic      Ghost     600      80     110       60     150     130      70          6       True
# 798   HoopaHoopa Unbound    Psychic       Dark     680      80     160       60     170     130      80          6       True
# 799            Volcanion       Fire      Water     600      80     110      120     130      90      70          6       True

####################################
## Show the last 1 rows (default) ##
####################################

print(
    tb_pokemon 
    >> dr.slice_tail()
)
#                     Name     Type_1     Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed Generation  Legendary
                                                                                                                             
# #               <object> <category> <category> <int64> <int64> <int64>  <int64> <int64> <int64> <int64> <category>     <bool>
# 721            Volcanion       Fire      Water     600      80     110      120     130      90      70          6       True


#--------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ 3. dr.glimpse() ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

# Glimpse of the dataframe
tb_pokemon >> dr.glimpse()
# Rows: 800
# Columns: 12
# . Name       <object>   'Bulbasaur', 'Ivysaur', 'Venusaur', 'VenusaurMega Venusaur', 'Charmander', 'Charmeleon', 'Charizard',…
# . Type_1     <category> 'Grass', 'Grass', 'Grass', 'Grass', 'Fire', 'Fire', 'Fire', 'Fire', 'Fire', 'Water', 'Water', 'Water',…
# . Type_2     <category> 'Poison', 'Poison', 'Poison', 'Poison', nan, nan, 'Flying', 'Dragon', 'Flying', nan, nan, nan, nan, nan, nan,…
# . Total      <int64>    318, 405, 525, 625, 309, 405, 534, 634, 634, 314, 405, 530, 630, 195, 205, 395, 195, 205, 395, 495, 251, 349,…
# . HP         <int64>    45, 60, 80, 80, 39, 58, 78, 78, 78, 44, 59, 79, 79, 45, 50, 60, 40, 45, 65, 65, 40, 63, 83, 83, 30, 55, 40,…
# . Attack     <int64>    49, 62, 82, 100, 52, 64, 84, 130, 104, 48, 63, 83, 103, 30, 20, 45, 35, 25, 90, 150, 45, 60, 80, 80, 56, 81,…
# . Defense    <int64>    49, 63, 83, 123, 43, 58, 78, 111, 78, 65, 80, 100, 120, 35, 55, 50, 30, 50, 40, 40, 40, 55, 75, 80, 35, 60,…
# . Sp_Atk     <int64>    65, 80, 100, 122, 60, 80, 109, 130, 159, 50, 65, 85, 135, 20, 25, 90, 20, 25, 45, 15, 35, 50, 70, 135, 25, 50,…
# . Sp_Def     <int64>    65, 80, 100, 120, 50, 65, 85, 85, 115, 64, 80, 105, 115, 20, 25, 80, 20, 25, 80, 80, 35, 50, 70, 80, 35, 70,…
# . Speed      <int64>    45, 60, 80, 80, 65, 80, 100, 100, 100, 43, 58, 78, 78, 45, 30, 70, 50, 35, 75, 145, 56, 71, 101, 121, 72, 97,…
# . Generation <category> '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',…
# . Legendary  <bool>     False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,…

'''
dr.glimpse(tb_pokemon) DOES NOT WORK, must use the pipe operator (>>)
'''