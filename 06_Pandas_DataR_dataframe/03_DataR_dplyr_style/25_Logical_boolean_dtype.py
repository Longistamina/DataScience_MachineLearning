'''
1. True/False checking:
   + dr.is_true()
   + dr.is_false()

2. Datatype checking:
   + dr.is_logical()
   + Apply to dr.select(dr.where())
      
3. Conversion:
   + dr.as_logical()
   + Apply to dr.mutate()
'''

import datar.all as dr
from datar import f
import pandas as pd

from pipda import register_verb
dr.filter = register_verb(func=dr.filter_)

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
#                     Name     Type_1     Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed Generation  Legendary
#                 <object> <category> <category> <int64> <int64> <int64>  <int64> <int64> <int64> <int64> <category>     <bool>
# 0              Bulbasaur      Grass     Poison     318      45      49       49      65      65      45          1      False
# 1                Ivysaur      Grass     Poison     405      60      62       63      80      80      60          1      False
# 2               Venusaur      Grass     Poison     525      80      82       83     100     100      80          1      False
# 3  VenusaurMega Venusaur      Grass     Poison     625      80     100      123     122     120      80          1      False
# 4             Charmander       Fire        NaN     309      39      52       43      60      50      65          1      False


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------- 1. True/False checking -------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##################
## dr.is_true() ##
##################

print(dr.is_true(True))    # True
print(dr.is_true(False))   # False

print(dr.is_true(1))       # True
print(dr.is_true(0))       # False

print(dr.is_true([True, True, True]))  # False

print(dr.is_true(True & True & True)) # True
print(dr.is_true(True & True & False)) # False
print(dr.is_true(True | False | False)) # True

###################
## dr.is_false() ##
###################

print(dr.is_false(False))    # True
print(dr.is_false(True))     # False

print(dr.is_false(0))       # True
print(dr.is_false(1))       # False

print(dr.is_false([False, False, False]))  # False

print(dr.is_false(False | False | False)) # True
print(dr.is_false(True & False & True)) # True
print(dr.is_false(True | True | True)) # False


#--------------------------------------------------------------------------------------------------------------#
#----------------------------------------- 2. Datatype checking -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#####################
## dr.is_logical() ##
#####################

print(dr.is_logical(tb_pokemon.Legendary))  # True

print(dr.is_logical(tb_pokemon.Type_1))     # False

####################################
## Apply to dr.select(dr.where()) ##
####################################

print(
    tb_pokemon
    >> dr.select(dr.where(dr.is_logical)) # Select logical columns only
    >> dr.slice_head(n=5)
)
#    Legendary
#       <bool>
# 0      False
# 1      False
# 2      False
# 3      False
# 4      False


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 3. Conversion ---------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#####################
## dr.as_logical() ##
#####################

good = [1, 0, True, False, "True", "False", "true", "false", "TRUE", "FALSE", None]

good_logical = dr.as_logical(good)

print(good_logical)
# [ True False  True False  True  True  True  True  True  True False]

print(dr.is_logical(good_logical))  # True

##########################
## Apply to dr.mutate() ##
##########################

tb_pokemon = (
    tb_pokemon
    >> dr.mutate(
        Legendary = dr.as_logical(f.Legendary) # Convert to logical dtype
    )
)

print(tb_pokemon.Legendary.dtype)  # bool