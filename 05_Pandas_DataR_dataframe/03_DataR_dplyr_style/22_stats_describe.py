'''
f.describe(): Get summary statistics of DataFrame columns.
   + Default usage
   + f.describe(include = [object, category, "all"]): Include specific data types.
   + f.describe(exclude = [category, bool]): Exclude specific data types.
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


#----------------------------------------------------------------------------------------------------------#
#--------------------------------------------- f.describe() -----------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

###################
## Default usage ##
###################

print(
    tb_pokemon
    >> dr.pipe(lambda f: f.describe())
)
#            Total          HP      Attack     Defense      Sp_Atk      Sp_Def       Speed
#        <float64>   <float64>   <float64>   <float64>   <float64>   <float64>   <float64>
# count  800.00000  800.000000  800.000000  800.000000  800.000000  800.000000  800.000000
# mean   435.10250   69.258750   79.001250   73.842500   72.820000   71.902500   68.277500
# std    119.96304   25.534669   32.457366   31.183501   32.722294   27.828916   29.060474
# min    180.00000    1.000000    5.000000    5.000000   10.000000   20.000000    5.000000
# 25%    330.00000   50.000000   55.000000   50.000000   49.750000   50.000000   45.000000
# 50%    450.00000   65.000000   75.000000   70.000000   65.000000   70.000000   65.000000
# 75%    515.00000   80.000000  100.000000   90.000000   95.000000   90.000000   90.000000
# max    780.00000  255.000000  190.000000  230.000000  194.000000  230.000000  180.000000

###################################################
## f.describe(include=[object, category, "all"]) ##
###################################################

print(
    tb_pokemon
    >> dr.pipe(lambda f: f.describe(include = [object, "category"]))
)
#            Name   Type_1   Type_2  Generation
#        <object> <object> <object>     <int64>
# count       800      800      414         800
# unique      800       18       18           6
# top      Skrelp    Water   Flying           1
# freq          1      112       97         166

print(
    tb_pokemon
    >> dr.pipe(lambda f: f.describe(include = "all"))
)
#            Name   Type_1   Type_2      Total          HP      Attack     Defense      Sp_Atk      Sp_Def       Speed  Generation Legendary
#        <object> <object> <object>  <float64>   <float64>   <float64>   <float64>   <float64>   <float64>   <float64>   <float64>  <object>
# count       800      800      414  800.00000  800.000000  800.000000  800.000000  800.000000  800.000000  800.000000       800.0       800
# unique      800       18       18        NaN         NaN         NaN         NaN         NaN         NaN         NaN         6.0         2
# top      Skrelp    Water   Flying        NaN         NaN         NaN         NaN         NaN         NaN         NaN         1.0     False
# freq          1      112       97        NaN         NaN         NaN         NaN         NaN         NaN         NaN       166.0       735
# mean        NaN      NaN      NaN  435.10250   69.258750   79.001250   73.842500   72.820000   71.902500   68.277500         NaN       NaN
# std         NaN      NaN      NaN  119.96304   25.534669   32.457366   31.183501   32.722294   27.828916   29.060474         NaN       NaN
# min         NaN      NaN      NaN  180.00000    1.000000    5.000000    5.000000   10.000000   20.000000    5.000000         NaN       NaN
# 25%         NaN      NaN      NaN  330.00000   50.000000   55.000000   50.000000   49.750000   50.000000   45.000000         NaN       NaN
# 50%         NaN      NaN      NaN  450.00000   65.000000   75.000000   70.000000   65.000000   70.000000   65.000000         NaN       NaN
# 75%         NaN      NaN      NaN  515.00000   80.000000  100.000000   90.000000   95.000000   90.000000   90.000000         NaN       NaN
# max         NaN      NaN      NaN  780.00000  255.000000  190.000000  230.000000  194.000000  230.000000  180.000000         NaN       NaN

##########################################
## f.describe(exclude=[category, bool]) ##
##########################################

print(
    tb_pokemon
    >> dr.pipe(lambda f: f.describe(exclude = ["category", bool]))
)
#            Name      Total          HP      Attack     Defense      Sp_Atk      Sp_Def       Speed
#        <object>  <float64>   <float64>   <float64>   <float64>   <float64>   <float64>   <float64>
# count       800  800.00000  800.000000  800.000000  800.000000  800.000000  800.000000  800.000000
# unique      800        NaN         NaN         NaN         NaN         NaN         NaN         NaN
# top      Skrelp        NaN         NaN         NaN         NaN         NaN         NaN         NaN
# freq          1        NaN         NaN         NaN         NaN         NaN         NaN         NaN
# mean        NaN  435.10250   69.258750   79.001250   73.842500   72.820000   71.902500   68.277500
# std         NaN  119.96304   25.534669   32.457366   31.183501   32.722294   27.828916   29.060474
# min         NaN  180.00000    1.000000    5.000000    5.000000   10.000000   20.000000    5.000000
# 25%         NaN  330.00000   50.000000   55.000000   50.000000   49.750000   50.000000   45.000000
# 50%         NaN  450.00000   65.000000   75.000000   70.000000   65.000000   70.000000   65.000000
# 75%         NaN  515.00000   80.000000  100.000000   90.000000   95.000000   90.000000   90.000000
# max         NaN  780.00000  255.000000  190.000000  230.000000  194.000000  230.000000  180.000000