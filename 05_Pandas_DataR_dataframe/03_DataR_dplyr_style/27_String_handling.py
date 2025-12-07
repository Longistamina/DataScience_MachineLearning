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
   + dr.chartr(): Character translation.
   
7. Substring extraction:
   + dr.substr(): Get substring from start to stop.
   + dr.substring(): Get substring with a start only (to stop).

8. String splitting:
   + dr.strsplit(): Split strings into substrings based on a specified separator.
   + dr.strsplit() with RegEx: Split strings using regular expressions.

9. String concatenation: 
   + dr.paste() 
   + dr.paste0()

10. Trimming whitespace:
    + dr.trimws(texts): trim both sides (as default)
    + dr.trimws(texts, which="left"): trim left side
    + dr.trimws(texts, which="right"): trim right side

11. Extract, Separate, and Unite:
    + dr.extract(): Extract substrings into multiple columns using regular expressions with capturing groups.
    + dr.separate(): Separate a single string column into multiple columns based on a specified separator.
    + dr.separate_rows(): Separate a single string column into multiple rows based on a specified separator.
    + dr.unite(): Unite multiple string columns into a single column with a specified separator.
    
12. Apply Pandas f.str methods

13. Some applications:
    + Data cleaning pipeline
    + Email validation
'''

import datar.all as dr
from datar import f
import pandas as pd

from pipda import register_verb
dr.filter = register_verb(func=dr.filter_)
dr.slice = register_verb(func=dr.slice_)

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


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 5. Pattern matching and searching -----------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

###############
## dr.grep() ##
###############
'''
Test if pattern exists in strings
Returns the INDICES of the elements that contain the pattern

dr.grep(pattern, x)
'''

#-----
## Demo
#-----

print(dr.grep(pattern="Mega", x=tb_pokemon.Name))
# [  3   7   8  12  19  23  71  87 102 124 137 141 154 163 164 168 196 224
#  229 232 248 268 275 279 283 306 327 329 333 336 339 349 354 366 387 393
#  397 409 413 418 420 426 476 494 498 511 527 591 796]

#-----
## Slice using dr.grep()
#-----

print(
    tb_pokemon
    >> dr.slice_(dr.grep("Mega", tb_pokemon.Name))
    >> dr.select(f.Name)
    >> dr.slice_head(n=5)
)
#                          Name
#                      <object>
# 3       VenusaurMega Venusaur
# 7   CharizardMega Charizard X
# 8   CharizardMega Charizard Y
# 12    BlastoiseMega Blastoise
# 19      BeedrillMega Beedrill

################
## dr.grepl() ##
################
'''
Like dr.grep(), but returns a boolean array

dr.grepl(pattern, x)
'''

#-----
## Demo
#-----

print(
    tb_pokemon
    >> dr.mutate(
        Has_Mega = dr.grepl("Mega", f.Name)
    )
    >> dr.select(f.Name, f.Has_Mega)
    >> dr.slice_head(n=5)
)
#                     Name  Has_Mega
#                 <object>    <bool>
# 0              Bulbasaur     False
# 1                Ivysaur     False
# 2               Venusaur     False
# 3  VenusaurMega Venusaur      True
# 4             Charmander     False

#-----
## Filter using dr.grepl()
#-----

print(
    tb_pokemon
    >> dr.filter(dr.grepl("Mega", f.Name))
    >> dr.select(f.Name)
    >> dr.slice_head(n=5)
)
#                          Name
#                      <object>
# 3       VenusaurMega Venusaur
# 7   CharizardMega Charizard X
# 8   CharizardMega Charizard Y
# 12    BlastoiseMega Blastoise
# 19      BeedrillMega Beedrill

#####################
## dr.startswith() ##
#####################
'''
Check if strings start with a specified prefix

dr.startswith(x, prefix)
'''

print(
    tb_pokemon
    >> dr.filter(dr.startswith(f.Type_1, 'F'))
    >> dr.select(f.Name, f.Type_1, f.Type_2)
    >> dr.slice_tail(n=5)
)
#           Name     Type_1     Type_2
#       <object> <category> <category>
# 771   Hawlucha   Fighting     Flying
# 790     Noibat     Flying     Dragon
# 791    Noivern     Flying     Dragon
# 792    Xerneas      Fairy        NaN
# 799  Volcanion       Fire      Water

###################
## dr.endswith() ##
###################
'''
Check if strings end with a specified suffix

dr.endswith(x, suffix)
'''

print(
    tb_pokemon
    >> dr.filter(dr.endswith(f.Name, 'ion'))
    >> dr.select(f.Name, f.Type_1, f.Type_2)
)
#            Name     Type_1     Type_2
#        <object> <category> <category>
# 171  Typhlosion       Fire        NaN
# 502     Drapion     Poison       Dark
# 639     Duosion    Psychic        NaN
# 699    Cobalion      Steel   Fighting
# 700   Terrakion       Rock   Fighting
# 701    Virizion      Grass   Fighting
# 799   Volcanion       Fire      Water


#----------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------- 6. String replacement ---------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

names = ["John  Hans Smith", "Jane  Mary Doe", "Alice   Bob Johnson"]

##############
## dr.sub() ##
##############
'''
Replace first occurrence

dr.sub(pattern, replacement, x)
'''

print(dr.sub(r"\s+", "_", names))
# ['John_Hans Smith' 'Jane_Mary Doe' 'Alice_Bob Johnson']

'''Only the first r"\s+" (space character) is replaced with "_" in each string element'''

###############
## dr.gsub() ##
###############
'''
Replace all occurrences

dr.gsub(pattern, replacement, x)
'''

print(dr.gsub(r"\s+", "-", names))
# ['John-Hans-Smith' 'Jane-Mary-Doe' 'Alice-Bob-Johnson']

'''All r"\s+" (space character) are replaced with "-" in each string element'''

#################
## dr.chartr() ##
#################
'''
Character translation.

dr.chartr(old, new, x)
'''

print(dr.chartr("aeiou", "12345", names))
# ['J4hn  H1ns Sm3th' 'J1n2  M1ry D42' 'Al3c2   B4b J4hns4n']


#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 7. Substring extraction -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

names = ["John_Hans_Smith", "Jane_Mary_Doe", "Alice_Bob_Johnson"]

#################
## dr.substr() ##
#################
'''
Get substring from start to stop.

dr.substr(x, start, stop)

NOTE: stop is still INDCLUDED
'''

print(dr.substr(names, 0, 6))
# ['John_H' 'Jane_M' 'Alice_']

####################
## dr.substring() ##
####################
'''
Get substring with a start only (to stop).

dr.substring(x, first, last=None)
If last is None, goes to the end of the string.
'''

print(dr.substring(names, 5))
# ['Hans_Smith' 'Mary_Doe' '_Bob_Johnson']

print(dr.substring(names, 5, 9))
# ['Hans' 'Mary' '_Bob']


#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------- 8. String splitting --------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

###################
## dr.strsplit() ##
###################

names = ["John_Hans_Smith", "Jane_Mary_Doe", "Alice_Bob_Johnson"]

print(dr.strsplit(names, "_"))
# [
#   list(['John', 'Hans', 'Smith']) 
#   list(['Jane', 'Mary', 'Doe'])
#   list(['Alice', 'Bob', 'Johnson'])
# ]

##############################
## dr.strsplit() with RegEx ##
##############################

names2 = ["John-Hans.Smith", "Jane_Mary-Doe", "Alice.Bob_Johnson"]

print(dr.strsplit(names2, r"[-._]"))
# [
#   list(['John', 'Hans', 'Smith']) 
#   list(['Jane', 'Mary', 'Doe'])
#   list(['Alice', 'Bob', 'Johnson'])
# ]

print(dr.strsplit(names2, r"\W+")) # \W+ matches any non-word character
# [
#   list(['John', 'Hans', 'Smith']) 
#   list(['Jane', 'Mary', 'Doe'])
#   list(['Alice', 'Bob', 'Johnson'])
# ]


#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 9. String concatenation -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

firts = dr.c("John", "Jane", "Alice")
lasts = dr.c("Smith", "Doe", "Johnson")

################
## dr.paste() ##
################
'''
Concatenate strings with a separator (default is space " ")

dr.paste(..., sep=" ")
'''

print(dr.paste(firts, lasts))
# ['John Smith' 'Jane Doe' 'Alice Johnson']

print(dr.paste(firts, lasts, sep="_"))
# ['John_Smith' 'Jane_Doe' 'Alice_Johnson']

#################
## dr.paste0() ##
#################
'''
Concatenate strings without any separator

dr.paste0(...)
'''

print(dr.paste0(firts, lasts))
# ['JohnSmith' 'JaneDoe' 'AliceJohnson']


#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 10. Trimming whitespace -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

texts = ["   Hello World   ", "   DataR is great!   ", "   Pandas and DataR   "]

#################
## dr.trimws() ##
#################
'''Trim whitespace from both sides (as default)'''

print(dr.trimws(texts))
# ['Hello World' 'DataR is great!' 'Pandas and DataR']

#############################
## dr.trimws(which='left') ##
#############################
'''Trim whitespace from left side'''

print(dr.trimws(texts, which="left"))
# ['Hello World   ' 'DataR is great!   ' 'Pandas and DataR   ']

##############################
## dr.trimws(which='right') ##
##############################
'''Trim whitespace from right side'''

print(dr.trimws(texts, which="right"))
# ['   Hello World' '   DataR is great!' '   Pandas and DataR']


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 11. Extract, Separate, and Unite ------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

##################
## dr.extract() ##
##################
'''
Extract based on REGULAR EXPRESSIONS with capturing groups

dr.extract(data, col, regex, into)
'''

df_extract = pd.DataFrame({
    'id': ['A-001', 'B-002', 'C-003']
})

print(df_extract)
#         id
#   <object>
# 0    A-001
# 1    B-002
# 2    C-003

#-----
## Extract into multiple columns
#-----

print(
    df_extract
    >> dr.extract(f.id, regex=r'([A-Z])-(\d+)', into=['prefix', 'number'])
)
#     prefix   number
#   <object> <object>
# 0        A      001
# 1        B      002
# 2        C      003

#-----
## remove=False to keep original column
#-----

print(
    df_extract
    >> dr.extract(f.id, regex=r'([A-Z])-(\d+)', into=['prefix', 'number'], remove=False)
)
#         id   prefix   number
#   <object> <object> <object>
# 0    A-001        A      001
# 1    B-002        B      002
# 2    C-003        C      003

###################
## dr.separate() ##
###################
'''
Separate a single string column into multiple columns based on a specified SEPARATOR.

dr.separate(data, col, into, sep)
'''

df_separate = pd.DataFrame({
    'name_age': ['John_25', 'Jane_30', 'Bob_35']
})

print(df_separate)
#   name_age
#   <object>
# 0  John_25
# 1  Jane_30
# 2   Bob_35

#-----
## Separate into multiple columns
#-----

print(
    df_separate
    >> dr.separate(f.name_age, into=['name', 'age'], sep='_')
)
#       name      age
#   <object> <object>
# 0     John       25
# 1     Jane       30
# 2      Bob       35

#-----
## remove=False to keep original column
#-----

print(
    df_separate
    >> dr.separate(f.name_age, into=['name', 'age'], sep='_', remove=False)
)
#   name_age     name      age
#   <object> <object> <object>
# 0  John_25     John       25
# 1  Jane_30     Jane       30
# 2   Bob_35      Bob       35

########################
## dr.separate_rows() ##
########################
'''
Separate collapsed values into multiple rows

dr.separate_rows(data, col, sep)
'''

df_sep_rows = pd.DataFrame({
    'id': [1, 2],
    'values': ['a,b,c', 'x,y,z']
})

print(df_sep_rows)
#        id   values
#   <int64> <object>
# 0       1    a,b,c
# 1       2    x,y,z

#-----
## Separate into multiple rows
#-----

print(
    df_sep_rows
    >> dr.separate_rows(f.values, sep=',')
)
#        id   values
#   <int64> <object>
# 0       1        a
# 1       1        b
# 2       1        c
# 3       2        x
# 4       2        y
# 5       2        z

################
## dr.unite() ##
################
'''
Unite multiple columns into one

dr.unite(data, col, cols, sep)
'''

df_unite = pd.DataFrame({
    'first': ['John', 'Jane'],
    'last': ['Doe', 'Smith']
})

print(df_unite)
#      first     last
#   <object> <object>
# 0     John      Doe
# 1     Jane    Smith

#-----
## Unite into single column
#-----

print(
    df_unite
    >> dr.unite('full_name', ['first', 'last'], sep=' ')
)
#     full_name
#      <object>
# 0    John Doe
# 1  Jane Smith

#-----
## remove=False to keep original columns
#-----

print(
    df_unite
    >> dr.unite('full_name', ['first', 'last'], sep='_', remove=False)
)
#     full_name    first     last
#      <object> <object> <object>
# 0    John_Doe     John      Doe
# 1  Jane_Smith     Jane    Smith


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 12. Apply Pandas f.str methods --------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

print(
    tb_pokemon
    >> dr.mutate(
        Name_lower = f.Name.str.lower(),
        Name_length = f.Name.str.len()
    )
    >> dr.select(f.Name, f.Name_lower, f.Name_length)
    >> dr.slice_head(n=5)
)
#                     Name             Name_lower  Name_length
#                 <object>               <object>      <int64>
# 0              Bulbasaur              bulbasaur            9
# 1                Ivysaur                ivysaur            7
# 2               Venusaur               venusaur            8
# 3  VenusaurMega Venusaur  venusaurmega venusaur           21
# 4             Charmander             charmander           10

###################

print(
    tb_pokemon
    >> dr.filter(f.Name.str.contains("Mega"))
    >> dr.select(f.Name)
    >> dr.slice_head(n=5)
)
#                          Name
#                      <object>
# 3       VenusaurMega Venusaur
# 7   CharizardMega Charizard X
# 8   CharizardMega Charizard Y
# 12    BlastoiseMega Blastoise
# 19      BeedrillMega Beedrill


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ 13. Some applications -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

############################
## Data cleaning pipeline ##
############################

messy = ["  john_DOE  ", "JANE-smith", "  Bob JOHNSON  "]

# Clean pipeline
cleaned = (
    messy
    >> dr.pipe(lambda x: dr.trimws(x))  # Trim whitespace
    >> dr.pipe(lambda x: dr.tolower(x))  # Convert to lowercase
    >> dr.pipe(lambda x: dr.gsub("_|-", " ", x))  # Replace delimiters
)

print(cleaned)
# ['john doe' 'jane smith' 'bob johnson']

######################
## Email validation ##
######################

emails = ["user@example.com", "admin@site.org", "invalid.email"]

# Validate email pattern
pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

print(
    dr.tibble(email = emails) # Convert to datar tibble for filter()
    >> dr.filter(dr.grepl(pattern, emails) == True)
    >> dr.separate(col=f, into=['username', 'domain'], sep='@', remove=False)
)
#               email username       domain
#            <object> <object>     <object>
# 0  user@example.com     user  example.com
# 1    admin@site.org    admin     site.org

########################################################
##            Apply with Baccalaureate 2016           ##
########################################################

#---------
## Load raw data
#---------

tb_bac_2016 = dr.tibble(pd.read_excel("05_Pandas_DataR_dataframe/data/Baccalaureate_2016.xlsx"))

print(
    tb_bac_2016
    >> dr.slice_head(n=5)
)
#    SOBAODANH         HO_TEN   NGAY_SINH         TEN_CUMTHI GIOI_TINH                                           DIEM_THI
#     <object>       <object>    <object>           <object>  <object>                                           <object>
# 0  018000001  DƯƠNG VIỆT AN  12/03/1998  Sở GDĐT Bắc Giang       Nam  Toán:   2.00   Ngữ văn:   5.50   Lịch sử:   3....
# 1  018000002      ĐỖ VĂN AN  09/12/1998  Sở GDĐT Bắc Giang       Nam  Toán:   5.50   Ngữ văn:   5.25   Địa lí:   5.5...
# 2  018000003     ĐỖ XUÂN AN  12/08/1997  Sở GDĐT Bắc Giang       Nam  Toán:   4.50   Ngữ văn:   5.50   Địa lí:   3.7...
# 3  018000004   ĐẶNG PHÚC AN  19/03/1998  Sở GDĐT Bắc Giang        Nữ  Toán:   3.00   Ngữ văn:   6.00   Địa lí:   5.5...
# 4  018000005    ĐẶNG VĂN AN  25/10/1998  Sở GDĐT Bắc Giang       Nam  Toán:   2.25   Ngữ văn:   4.75   Địa lí:   5.2...

#---------
## Define dictionaries and functions
#---------

dict_subjects = {
    'Toán':'Math',
    'Ngữ văn':'Literature',
    'Địa lí':'Geography',
    'Lịch sử':'History',
    'Tiếng Anh':'English',
    'Sinh học':'Biology',
    'Vật lí':'Physics',
    'Hóa học':'Chemistry',
}

dict_translate = {
    'Nam': 'Male',
    'Nữ': 'Female',
    'Sở GDĐT Bắc Giang': 'Bac Giang DET', # DET: Dept of Education and Training
    'Sở GDĐT Hoà Bình': 'Hoa Binh DET',
    'Sở GDĐT Thừa Thiên -Huế': 'Thua Thien - Hue DET',
    'Trường Đại học Công nghiệp Tp. HCM': 'IUH' # IUH: Industrial University of Ho Chi Minh City
}

def rename_subjects(subjects_str):
    for viet, eng in dict_subjects.items():
        subjects_str = subjects_str.replace(viet, eng)
    return subjects_str

#---------
## Data cleaning pipeline
#---------

tb_bac_2016_clean = (
    tb_bac_2016
    >> dr.rename( # Rename columns from Vietnamese to English
        ID = f.SOBAODANH,
        FULL_NAME = f.HO_TEN,
        BIRTHDAY = f.NGAY_SINH,
        EXAM_LOCATION = f.TEN_CUMTHI,
        GENDER = f.GIOI_TINH,
        SCORE = f.DIEM_THI
    )
    >> dr.mutate(SCORE = f.SCORE.apply(rename_subjects)) # Rename subjects from Vietnamese to English
    >> dr.pipe(lambda f: f.replace(to_replace=dict_translate)) # Translate other values into English
    >> dr.mutate(
        BIRTHDAY = dr.as_date(f.BIRTHDAY, format="%d/%m/%Y", optional=True), # Convert to date type (optional=True like coerce in pandas)
        EXAM_LOCATION = dr.as_factor(f.EXAM_LOCATION), # Convert to category type
        GENDER = dr.as_factor(f.GENDER)  # Convert to category type
    )
    >> dr.mutate( # Extract subject scores into multiple columns
        **{subject: dr.as_numeric(f.SCORE.str.extract(fr'{subject}:\s*(\d+\.\d+)', expand=False)) for subject in dict_subjects.values()}    
    )
    >> dr.select(~f.SCORE, ~f.BIRTHDAY, ~f.EXAM_LOCATION) # Drop unnecessary columns
    >> dr.pipe(lambda f: f.set_index('ID')) # Set ID as index

    >> dr.mutate(
        dr.across(
            ~f.FULL_NAME & ~f.GENDER,
            lambda col: col.fillna('not_attend') # Fill missing scores with 'not_attended'
        )
    )
)

print(
    tb_bac_2016_clean
    >> dr.slice_head(n=5)
)
#                FULL_NAME     GENDER     Math Literature Geography     History     English     Biology     Physics   Chemistry
                                                                                                                             
# ID              <object> <category> <object>   <object>  <object>    <object>    <object>    <object>    <object>    <object>
# 018000001  DƯƠNG VIỆT AN       Male      2.0        5.5       5.0         3.0  not_attend  not_attend  not_attend  not_attend
# 018000002      ĐỖ VĂN AN       Male      5.5       5.25       5.5  not_attend        3.68  not_attend  not_attend  not_attend
# 018000003     ĐỖ XUÂN AN       Male      4.5        5.5      3.75  not_attend        2.25  not_attend  not_attend  not_attend
# 018000004   ĐẶNG PHÚC AN     Female      3.0        6.0       5.5  not_attend         1.5  not_attend  not_attend  not_attend
# 018000005    ĐẶNG VĂN AN       Male     2.25       4.75      5.25  not_attend         2.0  not_attend  not_attend  not_attend