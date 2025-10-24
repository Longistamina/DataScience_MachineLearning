'''
In dataR (as well as R), categorical variables are often represented as factors.

#################################

1. Create factor variable
   + dr.factor()
   + dr.ordered()

2. Convert to factor variable
   + dr.as_factor()
   + dr.as_ordered()

3. Inspect core properties:
   + dr.nlevels()
   + dr.levels()
   + dr.is_factor()
   + dr.is_ordered()
   + dr.fct_unique()
   + dr.fct_count()
   + dr.fct_match()

4. Add levels:
   + dr.factor(levels=..., labels=...)
   + dr.fct_expand()

5. Remove levels:
   + dr.droplevels()
   + dr.fct_drop()

6. Reorder levels:
   + Manual reordering: dr.fct_relevel()
   + Automatic reordering: dr.fct_inorder(), dr.fct_infreq(), dr.fct_inseq()
   + Reordering by another variable: dr.fct_reorder(), dr.fct_reorder2()
   + Reverse/shift: dr.fct_rev(), dr.fct_shift()

7. Rename levels:
   + Manual renaming: dr.fct_recode()
   + Combine multiple levels into one: dr.fct_collapse()
   + Lumping infrequent levels: dr.fct_lump(), dr.fct_lump_min(), dr.fct_lump_prop(), dr.fct_lump_n(), dr.fct_lump_lowfreq()
   + Replacing with "other": dr.fct_other()
   + Automatic relabeling: dr.fct_relabel()

8. Handle multiple factors:
   + Concatenate factors: dr.fct_c()
   + Cross factors: dr.fct_cross()
   + Unify levels: dr.fct_unify(), dr.lvls_union()

9. Special Operations:
   + Handle missing levels: dr.fct_explicit_na()
   + Anonymize levels: dr.fct_anon()

10. Low-level operations:
   + dr.lvls_reorder()
   + dr.lvls_revalue()
   + dr.lvls_expand() 
'''

import datar.all as dr
from datar import f
import pandas as pd

from pipda import register_verb
dr.filter = register_verb(func = dr.filter_)

# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")

########################

tb_pokemon = dr.tibble(
    pd.read_csv("05_Pandas_DataR_dataframe/data/pokemon.csv")
    >> dr.rename_with(lambda col: col.strip().replace(" ", "_").replace(".", "")) # Clean column names
    >> dr.select(f.Name, f.Type_1, f.Type_2, f.Speed, f.Generation, f.Legendary)
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
#                     Name     Type_1     Type_2   Speed Generation  Legendary
#                 <object> <category> <category> <int64> <category>     <bool>
# 0              Bulbasaur      Grass     Poison      45          1      False
# 1                Ivysaur      Grass     Poison      60          1      False
# 2               Venusaur      Grass     Poison      80          1      False
# 3  VenusaurMega Venusaur      Grass     Poison      80          1      False
# 4             Charmander       Fire        NaN      65          1      False


#------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. Create factor variable -----------------------------------------#
#------------------------------------------------------------------------------------------------------------#

#################
## dr.factor() ##
#################
'''Create a factor (categorical variable) from a list-like object.'''

fct_gender = dr.factor(
    x = ["M", "F", "F", "M", "Others", "F", "M", "M", "F", "Others"],
    ordered = False # non-ordered factor
)

print(fct_gender)
# ['M', 'F', 'F', 'M', 'Others', 'F', 'M', 'M', 'F', 'Others']
# Categories (3, object): ['F', 'M', 'Others']

##################
## dr.ordered() ##
##################
'''Create an ordered factor (ordered categorical variable) from a list-like object.'''

#----
## Example 1
#----

ord_degree = dr.ordered(
      x = ["Bachelors", "Masters", "PhD", "Bachelors", "PhD", "Masters", "Bachelors", "AssociateProf"],
      levels = ["Bachelors", "Masters", "PhD", "AssociateProf"]  # specify the order of levels
)

print(ord_degree)
# ['Bachelors', 'Masters', 'PhD', 'Bachelors', 'PhD', 'Masters', 'Bachelors', 'AssociateProf']
# Categories (4, object): ['Bachelors' < 'Masters' < 'PhD' < 'AssociateProf']

#----
## Example 2
#----

ord_size = dr.ordered(
    x = [39, 42, 36, 40, 38, 41, 39, 37, 42, 40],
    levels = [36, 37, 38, 39, 40, 41, 42]  # specify the order of levels
)

print(ord_size)
# [39, 42, 36, 40, 38, 41, 39, 37, 42, 40]
# Categories (7, int64): [36 < 37 < 38 < 39 < 40 < 41 < 42]


#------------------------------------------------------------------------------------------------------------#
#------------------------------------- 2. Convert to factor variable ----------------------------------------#
#------------------------------------------------------------------------------------------------------------#

####################
## dr.as_factor() ##
####################
'''Convert an existing variable to a factor (categorical variable).'''

lst_gender = ["M", "F", "F", "M", "Others", "F", "M", "M", "F", "Others"]

fct_gender2 = dr.as_factor(lst_gender)

print(fct_gender2)
# ['M', 'F', 'F', 'M', 'Others', 'F', 'M', 'M', 'F', 'Others']
# Categories (3, object): ['F', 'M', 'Others']

#####################
## dr.as_ordered() ##
#####################
'''Convert an existing variable to an ordered factor (ordered categorical variable).'''

#----
## Example 1
#----

lst_degree = ["Bachelors", "Masters", "PhD", "Bachelors", "PhD", "Masters", "Bachelors", "AssociateProf"]

ord_degree2 = dr.as_ordered(lst_degree)

print(ord_degree2)
# ['Bachelors', 'Masters', 'PhD', 'Bachelors', 'PhD', 'Masters', 'Bachelors', 'AssociateProf']
# Categories (4, object): ['AssociateProf' < 'Bachelors' < 'Masters' < 'PhD']

'''
NOTE: dr.as_ordered() DOES NOT allow specifying levels.
      it will set the order automatically like A-Z, 0-9 based on unique values.
'''

#----
## Example 2
#----

lst_size = [39, 42, 36, 40, 38, 41, 39, 37, 42, 40]

ord_size2 = dr.as_ordered(lst_size)

print(ord_size2)
# [39, 42, 36, 40, 38, 41, 39, 37, 42, 40]
# Categories (7, int64): [36 < 37 < 38 < 39 < 40 < 41 < 42]


#------------------------------------------------------------------------------------------------------------#
#-------------------------- 3. Inspect core properties of factor variable -----------------------------------#
#------------------------------------------------------------------------------------------------------------#