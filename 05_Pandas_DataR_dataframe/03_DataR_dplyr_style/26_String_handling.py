'''
1. String type checking:
   + dr.is_character(): Check if the input is of string type.
   + dr.is_str(): Alias for dr.is_character().

2. Converion:
   + dr.as_character(): Convert the input to string type.
   + dr.as_str(): Alias for dr.as_character().
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