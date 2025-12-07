'''
To read dataframe, just use pandas.read.....() functions, then convert to datar tibble if needed.
'''

import datar.all as dr
import pandas as pd


#--------------------------------------------------------------------------------------------------------------------#
#------------------------------------- Read dataframe using pandas.read...() ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

########################
## Read from CSV file ##
########################

tb_csv = dr.tibble(pd.read_csv('05_Pandas_DataR_dataframe/data/air_quality_no2_long.csv'))
print(tb_csv.head())
#       city  country                   date.utc location parameter     value     unit
#   <object> <object>                   <object> <object>  <object> <float64> <object>
# 0    Paris       FR  2019-06-21 00:00:00+00:00  FR04014       no2      20.0    µg/m³
# 1    Paris       FR  2019-06-20 23:00:00+00:00  FR04014       no2      21.8    µg/m³
# 2    Paris       FR  2019-06-20 22:00:00+00:00  FR04014       no2      26.5    µg/m³
# 3    Paris       FR  2019-06-20 21:00:00+00:00  FR04014       no2      24.9    µg/m³
# 4    Paris       FR  2019-06-20 20:00:00+00:00  FR04014       no2      21.4    µg/m³

##########################
## Read from Excel file ##
##########################

tb_excel = dr.tibble(pd.read_excel("05_Pandas_DataR_dataframe/data/emp_sheetname.xlsx", sheet_name='emp'))
print(tb_excel)
#         id      name    salary       start_date        dept
#   <object>  <object> <float64> <datetime64[ns]>    <object>
# 0        1      Rick    623.30       2012-01-01          IT
# 1        2       Dan    515.20       2013-09-23  Operations
# 2        3  Michelle    611.00       2014-11-15          IT
# 3        4      Ryan    729.00       2014-05-11          HR
# 4               Gary    843.25       2015-03-27     Finance
# 5        6      Nina    578.00       2013-05-21          IT
# 6        7     Simon    632.80       2013-07-30  Operations
# 7        8      Guru    722.50       2014-06-17     Finance

############################
## Read with more options ##
############################

tb_pokemon = dr.tibble(
    pd.read_csv(
        filepath_or_buffer="05_Pandas_DataR_dataframe/data/pokemon.csv",
        dtype={
            "Type 1": "category",
            "Type 2": "category",
            "Generation": "category",
            "Legendary": "bool"
        }
    )
    .drop(columns=["#"])
    .pipe(lambda f: f.set_axis(f.columns.str.strip().str.replace(r"\s+", "_", regex=True).str.replace(".", ""), axis=1))
    .assign(Generation = lambda f: f['Generation'].cat.as_ordered())
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