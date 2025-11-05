'''
1. String type checking:
   + dr.is_character(): Check if the input is of string type.

2. Converion:
   + dr.as_character(): Convert the input to string type.
   + dr.strtoi(): Convert numeric strings to integers.

3. Get properties:
   + dr.nchar(): Get the number of characters of each string element.
   + dr.nzchar(): Test if each string element is not empty

4. Case transformation:
   + dr.tolower(): Convert strings to lowercase.
   + dr.toupper(): Convert strings to uppercase.

5. Pattern matching and searching:
   + dr.grep(): Test if pattern exists in strings.
   + dr.grepl(): Like dr.grep(), but returns a boolean array.
   + dr.startswith(): Check if strings start with a specified prefix.
   + dr.endswith(): Check if strings end with a specified suffix.

6. String replacement:
   + dr.sub(): Replace first occurrence.
   + dr.gsub(): Replace all occurrences.
   
7. Substring extraction:
   + dr.substr(): Get substring.
   + dr.substring(): Get substring with a start only.

8. String splitting: dr.strsplit()

9. String concatenation: 
   + dr.paste() 
   + dr.paste0()

10. Trimming whitespace:
    + dr.trimws(texts): trim both sides (as default)
    + dr.trimws(texts, which="left"): trim left side
    + dr.trimws(texts, which="right"): trim right side

11. Some applications:
    + Data cleaning pipeline
    + Email validation
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


#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 1. String type checking -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

#######################
## dr.is_character() ##
#######################

print(dr.is_character(tb_pokemon.Name)) # True

print(dr.is_character(tb_pokemon.Total)) # False


#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 2. Converion ----------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

#######################
## dr.as_character() ##
#######################

#-----
## Demo
#-----

print(dr.as_character(tb_pokemon.Generation))
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
# Name: Generation, Length: 800, dtype: object

#-----
## Apply in pipeline
#-----

print(
    tb_pokemon
    >> dr.mutate(Total = dr.as_character(f.Total))
    >> dr.select(f.Name, f.Total)
    >> dr.slice_head(n=5)
)
#                     Name    Total
#                 <object> <object>
# 0              Bulbasaur      318
# 1                Ivysaur      405
# 2               Venusaur      525
# 3  VenusaurMega Venusaur      625
# 4             Charmander      309

#################
## dr.strtoi() ##
#################
'''
Convert numeric strings to integers

NOTE: only accepts ingeger strings, not float strings like "10.5"
      in that case, use "dr.as_numeric()" instead
'''

s_str = dr.c("10", "20", "30", "45", "50")

print(s_str) # ['10', '20', '30', '45', '50']

print(dr.strtoi(s_str)) # [10 20 30 45 50]


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ 3. Get properties ---------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

################
## dr.nchar() ##
################
'''Get the number of characters of each string element'''

print(
    tb_pokemon
    >> dr.select(f.Name)
    >> dr.mutate(Name_length = dr.nchar(f.Name))
    >> dr.slice_head(n=5)
)
#                     Name  Name_length
#                 <object>      <int64>
# 0              Bulbasaur            9
# 1                Ivysaur            7
# 2               Venusaur            8
# 3  VenusaurMega Venusaur           21
# 4             Charmander           10

#################
## dr.nzchar() ##
#################
'''Test if each string element is not empty'''

s_nzchar = dr.c("Hello", "", "DataR", " ", "Pandas")
print(dr.nzchar(s_nzchar)) 
# [ True False  True  True  True]

#-----
## Apply in pipeline
#-----

print(
    tb_pokemon
    >> dr.mutate(
        Type_1_nonempty = dr.nzchar(f.Type_1),
        Type_2_nonempty = dr.nzchar(f.Type_2)
    )
    >> dr.filter(f.Type_1_nonempty == False | f.Type_2_nonempty == False)
    >> dr.select(f.Name, f.Type_1, f.Type_2, f.Type_1_nonempty, f.Type_2_nonempty)
    >> dr.slice_tail(n=5)
)
#          Name     Type_1     Type_2  Type_1_nonempty  Type_2_nonempty
#      <object> <category> <category>           <bool>           <bool>
# 775   Sliggoo     Dragon        NaN             True            False
# 776    Goodra     Dragon        NaN             True            False
# 788  Bergmite        Ice        NaN             True            False
# 789   Avalugg        Ice        NaN             True            False
# 792   Xerneas      Fairy        NaN             True            False

#-----
## Cleaner way
#-----

print(
    tb_pokemon
    >> dr.filter(dr.nzchar(f.Type_1) == False | dr.nzchar(f.Type_2) == False)
    >> dr.select(f.Name, f.Type_1, f.Type_2)
    >> dr.slice_tail(n=5)
)
#          Name     Type_1     Type_2
#      <object> <category> <category>
# 775   Sliggoo     Dragon        NaN
# 776    Goodra     Dragon        NaN
# 788  Bergmite        Ice        NaN
# 789   Avalugg        Ice        NaN
# 792   Xerneas      Fairy        NaN


#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 4. Case transformation ------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

##################
## dr.tolower() ##
##################
'''Convert strings to lowercase'''

print(
    tb_pokemon
    >> dr.select(f.Name)
    >> dr.mutate(Name_lower = dr.tolower(f.Name))
    >> dr.slice_head(n=5)
)
#                     Name             Name_lower
#                 <object>               <object>
# 0              Bulbasaur              bulbasaur
# 1                Ivysaur                ivysaur
# 2               Venusaur               venusaur
# 3  VenusaurMega Venusaur  venusaurmega venusaur
# 4             Charmander             charmander

##################
## dr.toupper() ##
##################
'''Convert strings to uppercase'''

print(
    tb_pokemon
    >> dr.select(f.Name)
    >> dr.mutate(Name_upper = dr.toupper(f.Name))
    >> dr.slice_head(n=5)
)
#                     Name             Name_upper
#                 <object>               <object>
# 0              Bulbasaur              BULBASAUR
# 1                Ivysaur                IVYSAUR
# 2               Venusaur               VENUSAUR
# 3  VenusaurMega Venusaur  VENUSAURMEGA VENUSAUR
# 4             Charmander             CHARMANDER