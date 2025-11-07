'''
1. dr.group_by()
   + use with dr.summarise() and dr.n()
   + combine with dr.arrange() to sort keys
   + multiple grouping variables

2. combine with pd.Grouper for time-based grouping

3. dr.group_split(): split a groupped DataFrame into a list of DataFrames
'''

import datar.all as dr
from datar import f
import pandas as pd
import numpy as np

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


#--------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 1. dr.group_by() ----------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

###########################################
## Use with dr.summarise() - basic usage ##
###########################################

print(
    tb_pokemon
    >> dr.group_by(f.Type_1)
    >> dr.summarise(
        count = dr.n(), # Get the current group size
        avg_total = np.mean(f.Total),
        max_speed = np.max(f.Speed)
    )
)
#        Type_1   count   avg_total  max_speed
#    <category> <int64>   <float64>    <int64>
# 0       Grass      70  421.142857        145
# 1        Fire      52  458.076923        126
# 2       Water     112  430.455357        122
# 3         Bug      69  378.927536        160
# 4      Normal      98  401.683673        135
# 5      Poison      28  399.142857        130
# 6    Electric      44  443.409091        140
# 7      Ground      32  437.500000        120
# 8       Fairy      17  413.176471         99
# 9    Fighting      27  416.444444        118
# 10    Psychic      57  475.947368        180
# 11       Rock      44  453.750000        150
# 12      Ghost      32  439.562500        130
# 13        Ice      24  433.458333        110
# 14     Dragon      32  550.531250        120
# 15       Dark      31  445.741935        125
# 16      Steel      27  487.703704        110
# 17     Flying       4  485.000000        123

############################################
## Combine with dr.arrange() to sort keys ##
############################################

'''Ascending order'''

print(
    tb_pokemon
    >> dr.group_by(f.Type_2)
    >> dr.summarise(
        count = dr.n(),
        avg_atk = np.mean(f.Attack),
        medn_def = np.max(f.Defense)
    )
    >> dr.arrange(f.Type_2)
)
#        Type_2   count     avg_atk  medn_def
#    <category> <int64>   <float64>   <int64>
# 17        Bug       3   90.000000       100
# 12       Dark      20  109.800000       150
# 3      Dragon      18   94.444444       120
# 14   Electric       6   72.666667       120
# 5       Fairy      23   61.608696       150
# 7    Fighting      26  112.846154       129
# 15       Fire      12   81.250000       160
# 2      Flying      97   80.288660       140
# 16      Ghost      14   84.142857       150
# 6       Grass      25   74.160000       122
# 4      Ground      35   89.857143       230
# 10        Ice      14   98.000000       180
# 18     Normal       4   52.750000        72
# 0      Poison      34   67.588235       123
# 8     Psychic      33   74.696970       180
# 11       Rock      14   84.000000       230
# 9       Steel      22   92.590909       168
# 13      Water      14   70.142857       125
# 1         NaN     386   74.525907       230

'''Descending order'''

print(
    tb_pokemon
    >> dr.group_by(f.Type_2)
    >> dr.summarise(
        count = dr.n(),
        avg_atk = np.mean(f.Attack),
        medn_def = np.max(f.Defense)
    )
    >> dr.arrange(dr.desc(f.Type_2))
)
#        Type_2   count     avg_atk  medn_def
#    <category> <int64>   <float64>   <int64>
# 13      Water      14   70.142857       125
# 9       Steel      22   92.590909       168
# 11       Rock      14   84.000000       230
# 8     Psychic      33   74.696970       180
# 0      Poison      34   67.588235       123
# 18     Normal       4   52.750000        72
# 10        Ice      14   98.000000       180
# 4      Ground      35   89.857143       230
# 6       Grass      25   74.160000       122
# 16      Ghost      14   84.142857       150
# 2      Flying      97   80.288660       140
# 15       Fire      12   81.250000       160
# 7    Fighting      26  112.846154       129
# 5       Fairy      23   61.608696       150
# 14   Electric       6   72.666667       120
# 3      Dragon      18   94.444444       120
# 12       Dark      20  109.800000       150
# 17        Bug       3   90.000000       100
# 1         NaN     386   74.525907       230

#################################
## Multiple grouping variables ##
#################################

print(
    tb_pokemon
    >> dr.group_by(f.Type_1, f.Legendary)
    >> dr.summarise(
        count = dr.n(),
        avg_total = np.mean(f.Total)
    )
    >> dr.arrange(f.Type_1, f.Legendary)
)
#        Type_1  Legendary   count   avg_total
#    <category>     <bool> <int64>   <float64>
# 0         Bug      False      69  378.927536
# 1        Dark      False      29  432.344828
# 2        Dark       True       2  640.000000
# 3      Dragon      False      20  476.850000
# 4      Dragon       True      12  673.333333
# 5    Electric      False      40  429.750000
# 6    Electric       True       4  580.000000


#------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. combine with pd.Grouper() ----------------------------------------#
#------------------------------------------------------------------------------------------------------------#

df_aq = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/air_quality_no2_long.csv")
    .rename(columns={"date.utc": "date"})
    .assign(date = lambda df: pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S%z")) # Must be datetime type for pd.Grouper
)

print(df_aq.head(3))
#       city  country                      date location parameter     value     unit
#   <object> <object>     <datetime64[ns, UTC]> <object>  <object> <float64> <object>
# 0    Paris       FR 2019-06-21 00:00:00+00:00  FR04014       no2      20.0    µg/m³
# 1    Paris       FR 2019-06-20 23:00:00+00:00  FR04014       no2      21.8    µg/m³
# 2    Paris       FR 2019-06-20 22:00:00+00:00  FR04014       no2      26.5    µg/m³

#####################################
## dr.group_by() with pd.Grouper() ##
#####################################

print(
    df_aq
    >> dr.group_by(pd.Grouper(key="date", freq="5D"))
    >> dr.summarize(value_mean = f.value.mean()) # Calculate the mean of "value" column every 5 days
)
#                        date  value_mean
#       <datetime64[ns, UTC]>   <float64>
# 0 2019-05-07 00:00:00+00:00   30.286017
# 1 2019-05-12 00:00:00+00:00   24.975304
# 2 2019-05-17 00:00:00+00:00   30.772917
# 3 2019-05-22 00:00:00+00:00   32.298340
# 4 2019-05-27 00:00:00+00:00   20.337705
# 5 2019-06-01 00:00:00+00:00   25.743933
# 6 2019-06-06 00:00:00+00:00   19.717273
# 7 2019-06-11 00:00:00+00:00   25.300855
# 8 2019-06-16 00:00:00+00:00   25.027119
# 9 2019-06-21 00:00:00+00:00   20.000000


#------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 3. dr.group_split() ------------------------------------------------#
#------------------------------------------------------------------------------------------------------------#
'''
Split a groupped DataFrame into a list of DataFrames
MUST WRAP INSIDE list() TO PRINT THE RESULT
'''

print(
    list(
        tb_pokemon
        >> dr.group_by(f.Legendary)
        >> dr.group_split()
    )
)
# [                      Name     Type_1     Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed Generation  Legendary
#                   <object> <category> <category> <int64> <int64> <int64>  <int64> <int64> <int64> <int64> <category>     <bool>
# 0                Bulbasaur      Grass     Poison     318      45      49       49      65      65      45          1      False
# 1                  Ivysaur      Grass     Poison     405      60      62       63      80      80      60          1      False
# 2                 Venusaur      Grass     Poison     525      80      82       83     100     100      80          1      False
# 3    VenusaurMega Venusaur      Grass     Poison     625      80     100      123     122     120      80          1      False
# ..                     ...        ...        ...     ...     ...     ...      ...     ...     ...     ...        ...        ...
# 4               Charmander       Fire        NaN     309      39      52       43      60      50      65          1      False
# 730    GourgeistSuper Size      Ghost      Grass     494      85     100      122      58      75      54          6      False
# 731               Bergmite        Ice        NaN     304      55      69       85      32      35      28          6      False
# 732                Avalugg        Ice        NaN     514      95     117      184      44      46      28          6      False
# 733                 Noibat     Flying     Dragon     245      40      30       35      45      40      55          6      False
# 734                Noivern     Flying     Dragon     535      85      70       80      97      80     123          6      False

# [735 rows x 12 columns],                    Name     Type_1     Type_2   Total      HP  Attack  Defense  Sp_Atk  Sp_Def   Speed Generation  Legendary
#                <object> <category> <category> <int64> <int64> <int64>  <int64> <int64> <int64> <int64> <category>     <bool>
# 0              Articuno        Ice     Flying     580      90      85      100      95     125      85          1       True
# 1                Zapdos   Electric     Flying     580      90      90       85     125      90     100          1       True
# 2               Moltres       Fire     Flying     580      90     100       90     125      85      90          1       True
# 3                Mewtwo    Psychic        NaN     680     106     110       90     154      90     130          1       True
# ..                  ...        ...        ...     ...     ...     ...      ...     ...     ...     ...        ...        ...
# 4   MewtwoMega Mewtwo X    Psychic   Fighting     780     106     190      100     154     100     130          1       True
# 60              Diancie       Rock      Fairy     600      50     100      150     100     150      50          6       True
# 61  DiancieMega Diancie       Rock      Fairy     700      50     160      110     160     110     110          6       True
# 62  HoopaHoopa Confined    Psychic      Ghost     600      80     110       60     150     130      70          6       True
# 63   HoopaHoopa Unbound    Psychic       Dark     680      80     160       60     170     130      80          6       True
# 64            Volcanion       Fire      Water     600      80     110      120     130      90      70          6       True

# [65 rows x 12 columns]]