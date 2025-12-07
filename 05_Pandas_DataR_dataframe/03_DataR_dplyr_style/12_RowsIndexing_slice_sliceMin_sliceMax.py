'''
1. dr.slice(): allows selecting rows by their positions (indices).
   + Basic usage: dr.slice_(index1, index2, ...)
   + Range indexing: dr.slice_(dr.c[start:end]) to select rows from start to end-1.

2. dr.slice_min(): allows selecting rows with the smallest values in a specified column.

3. dr.slice_max(): allows selecting rows with the largest values in a specified column.
'''

import datar.all as dr
from datar import f

import pandas as pd

########################

df_baseball = pd.read_csv(
    filepath_or_buffer="05_Pandas_DataR_dataframe/data/baseball.csv",
    dtype={
        "Team": "category",
        "Position": "category",
        "PosCategory": "category"
    }
)

print(df_baseball.head())
#               Name       Team       Position  Height  Weight       Age PosCategory
#           <object> <category>     <category> <int64> <int64> <float64>  <category>
# 0    Adam_Donachie        BAL        Catcher      74     180     22.99     Catcher
# 1        Paul_Bako        BAL        Catcher      74     215     34.69     Catcher
# 2  Ramon_Hernandez        BAL        Catcher      72     210     30.78     Catcher
# 3     Kevin_Millar        BAL  First_Baseman      72     210     35.43   Infielder
# 4      Chris_Gomez        BAL  First_Baseman      73     188     35.71   Infielder


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. dr.slice(...) -----------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

from pipda import register_verb

dr.slice = register_verb(func=dr.slice_)

'''
dr.slice_() to avoid conflict with Python built-in function slice()
=> Use registter_verb to bring it back as dr.slice()
'''

#################
## Basic usage ##
#################

print(
    df_baseball 
    >> dr.slice(0)
)
#             Name       Team   Position  Height  Weight       Age PosCategory
#         <object> <category> <category> <int64> <int64> <float64>  <category>
# 0  Adam_Donachie        BAL    Catcher      74     180     22.99     Catcher

print(
    df_baseball 
    >> dr.slice(0, 2, 5, 9)
)
#               Name       Team        Position  Height  Weight       Age PosCategory
#           <object> <category>      <category> <int64> <int64> <float64>  <category>
# 0    Adam_Donachie        BAL         Catcher      74     180     22.99     Catcher
# 2  Ramon_Hernandez        BAL         Catcher      72     210     30.78     Catcher
# 5    Brian_Roberts        BAL  Second_Baseman      69     176     29.39   Infielder
# 9       Adam_Stern        BAL      Outfielder      71     180     27.05  Outfielder

print(
    df_baseball 
    >> dr.slice(-1, -2)
)
#                Name       Team        Position  Height  Weight       Age PosCategory
#            <object> <category>      <category> <int64> <int64> <float64>  <category>
# 1014    Josh_Kinney        STL  Relief_Pitcher      73     195     27.92     Pitcher
# 1013  Randy_Keisler        STL  Relief_Pitcher      75     190     31.01     Pitcher

####################
## Range indexing ##
####################

print(
    df_baseball 
    >> dr.slice(dr.c[0:4])
)
#               Name       Team       Position  Height  Weight       Age PosCategory
#           <object> <category>     <category> <int64> <int64> <float64>  <category>
# 0    Adam_Donachie        BAL        Catcher      74     180     22.99     Catcher
# 1        Paul_Bako        BAL        Catcher      74     215     34.69     Catcher
# 2  Ramon_Hernandez        BAL        Catcher      72     210     30.78     Catcher
# 3     Kevin_Millar        BAL  First_Baseman      72     210     35.43   Infielder

print(
    df_baseball 
    >> dr.slice(dr.c[:3])
)
#               Name       Team   Position  Height  Weight       Age PosCategory
#           <object> <category> <category> <int64> <int64> <float64>  <category>
# 0    Adam_Donachie        BAL    Catcher      74     180     22.99     Catcher
# 1        Paul_Bako        BAL    Catcher      74     215     34.69     Catcher
# 2  Ramon_Hernandez        BAL    Catcher      72     210     30.78     Catcher

print(
    df_baseball 
    >> dr.slice(dr.c[1010:])
)
#                 Name       Team        Position  Height  Weight       Age PosCategory
#             <object> <category>      <category> <int64> <int64> <float64>  <category>
# 1010   Brad_Thompson        STL  Relief_Pitcher      73     190     25.08     Pitcher
# 1011   Tyler_Johnson        STL  Relief_Pitcher      74     180     25.73     Pitcher
# 1012  Chris_Narveson        STL  Relief_Pitcher      75     205     25.19     Pitcher
# 1013   Randy_Keisler        STL  Relief_Pitcher      75     190     31.01     Pitcher
# 1014     Josh_Kinney        STL  Relief_Pitcher      73     195     27.92     Pitcher

print(
    df_baseball 
    >> dr.slice(dr.c[0:10:2])
)
#               Name       Team       Position  Height  Weight       Age PosCategory
#           <object> <category>     <category> <int64> <int64> <float64>  <category>
# 0    Adam_Donachie        BAL        Catcher      74     180     22.99     Catcher
# 2  Ramon_Hernandez        BAL        Catcher      72     210     30.78     Catcher
# 4      Chris_Gomez        BAL  First_Baseman      73     188     35.71   Infielder
# 6    Miguel_Tejada        BAL      Shortstop      69     209     30.77   Infielder
# 8      Aubrey_Huff        BAL  Third_Baseman      76     231     30.19   Infielder


#------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 2. dr.slice_min(...) ----------------------------------------------#
#------------------------------------------------------------------------------------------------------------#
'''2. dr.slice_min(): allows selecting rows with the smallest values in a specified column.'''

print(
    df_baseball 
    >> dr.slice_min(f.Age, n=3) # Select 3 rows with the smallest Age
)
#                 Name       Team          Position  Height  Weight       Age PosCategory
#             <object> <category>        <category> <int64> <int64> <float64>  <category>
# 288  Felix_Hernandez        SEA  Starting_Pitcher      75     225     20.90     Pitcher
# 318     Delmon_Young         TB        Outfielder      75     205     21.46  Outfielder
# 289  Ryan_Feierabend        SEA  Starting_Pitcher      75     190     21.52     Pitcher

print(
    df_baseball 
    >> dr.slice_min(f.Age, n=5, with_ties=True) # Include ties
)
#                 Name       Team          Position  Height  Weight       Age PosCategory
#             <object> <category>        <category> <int64> <int64> <float64>  <category>
# 288  Felix_Hernandez        SEA  Starting_Pitcher      75     225     20.90     Pitcher
# 318     Delmon_Young         TB        Outfielder      75     205     21.46  Outfielder
# 289  Ryan_Feierabend        SEA  Starting_Pitcher      75     190     21.52     Pitcher
# 285       Adam_Jones        SEA        Outfielder      74     200     21.58  Outfielder
# 267    Andrew_Miller        DET    Relief_Pitcher      78     210     21.78     Pitcher


#------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 3. dr.slice_max(...) ----------------------------------------------#
#------------------------------------------------------------------------------------------------------------#
'''3. dr.slice_max(): allows selecting rows with the largest values in a specified column.'''

print(
    df_baseball 
    >> dr.slice_max(f.Height, n=3) # Select 3 rows with the largest Height
)
#               Name       Team          Position  Height  Weight       Age PosCategory
#           <object> <category>        <category> <int64> <int64> <float64>  <category>
# 909      Jon_Rauch        WAS    Relief_Pitcher      83     260     28.42     Pitcher
# 558  Randy_Johnson        ARZ  Starting_Pitcher      82     231     43.47     Pitcher
# 862    Chris_Young         SD  Starting_Pitcher      82     250     27.77     Pitcher

print(
    df_baseball 
    >> dr.slice_max(f.Height, n=5, with_ties=True) # Include ties
)
#                  Name       Team          Position  Height  Weight       Age PosCategory
#              <object> <category>        <category> <int64> <int64> <float64>  <category>
# 909         Jon_Rauch        WAS    Relief_Pitcher      83     260     28.42     Pitcher
# 558     Randy_Johnson        ARZ  Starting_Pitcher      82     231     43.47     Pitcher
# 862       Chris_Young         SD  Starting_Pitcher      82     250     27.77     Pitcher
# 59       Andrew_Sisco        CWS    Relief_Pitcher      81     260     24.13     Pitcher
# 764  Mark_Hendrickson         LA  Starting_Pitcher      81     230     32.69     Pitcher
