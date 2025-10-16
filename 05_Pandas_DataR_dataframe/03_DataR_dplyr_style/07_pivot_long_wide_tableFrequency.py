'''
1. pivot_wider: dr.pivot_wider()
   + basig usage
   + dr.pivot_wider(values_fill = 0)
   + dr.pivot_wider(values_from = [many_cols], names_sep = "_")
   + dr.pivot_wider(values_fn = ...)
   
2. pivot_longer: dr.pivot_longer()
   + basig usage
   + dr.pivot_longer(cols = dr.starts_with())
   + dr.pivot_longer(names_sep=)
   + dr.pivot_longer(names_pattern=)
   + Combine dr.pivot_longer() with dr.pivot_wider()
   + Apply dr.pipe(lambda f: pd.wide_to_long(df = f))

3. crosstab, contigency/frequency table: dr.table()
'''

import datar.all as dr
from datar import f
import pandas as pd
import numpy as np

# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")


#---------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. dr.pivot_wider() ------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

########################
## Create sample data ##
########################

'''
The dr.pivot_wider() converts unique values from one column into multiple columns in the DataFrame.
=> Results in a wider DataFrame than the original.

NOTE: if the chosen "index" column has duplicates => RAISE ERROR
'''

dates = pd.date_range('2024-01-01', periods=30) # 30 days
regions   = ['North', 'South', 'East', 'West']
products  = ['Widget', 'Gadget', 'Doohickey']

np.random.seed(42)
df_sales = pd.DataFrame(
    {   'ID'        : range(1, 201),
        'date'      : np.random.choice(dates, size=200),
        'region'    : np.random.choice(regions, size=200),
        'product'   : np.random.choice(products, size=200),
        'quantity'  : np.random.randint(1, 20, size=200),
        'unit_price': np.round(np.random.uniform(5, 50, size=200), 2)
    }
).assign(sales = lambda f: f.eval("quantity * unit_price")) # Add a column with the total sales amount

df_sales.head()
#    ID       date region    product  quantity  unit_price   sales
# 0   1 2024-01-07   East     Gadget         5        6.19   30.95
# 1   2 2024-01-20  North     Widget        10       21.94  219.40
# 2   3 2024-01-29   East  Doohickey         5       41.47  207.35
# 3   4 2024-01-15   East     Widget         4       49.43  197.72
# 4   5 2024-01-11  North     Widget         2       11.77   23.54

##################################
## dr.pivot_wider() basic usage ##
##################################

print(
    df_sales 
    >> dr.pivot_wider(
        names_from = f.region, 
        values_from = f.sales
        )
    >> dr.slice_head(n = 5)
)
#        ID             date    product  quantity  unit_price      East     North     South      West
#   <int64> <datetime64[ns]>   <object>   <int64>   <float64> <float64> <float64> <float64> <float64>
# 0       1       2024-01-07     Gadget         5        6.19     30.95       NaN       NaN       NaN
# 1       2       2024-01-20     Widget        10       21.94       NaN    219.40       NaN       NaN
# 2       3       2024-01-29  Doohickey         5       41.47    207.35       NaN       NaN       NaN
# 3       4       2024-01-15     Widget         4       49.43    197.72       NaN       NaN       NaN
# 4       5       2024-01-11     Widget         2       11.77       NaN     23.54       NaN       NaN

#####################################
## dr.pivot_wider(values_fill = 0) ##
#####################################

print(
    df_sales  
    >> dr.pivot_wider(
            names_from = f.region, 
            values_from = f.sales,
            values_fill = 0 # Fill NaN with 0
        )
    >> dr.slice_head(n = 5)
)
#        ID             date    product  quantity  unit_price      East     North     South      West
#   <int64> <datetime64[ns]>   <object>   <int64>   <float64> <float64> <float64> <float64> <float64>
# 0       1       2024-01-07     Gadget         5        6.19     30.95      0.00       0.0       0.0
# 1       2       2024-01-20     Widget        10       21.94      0.00    219.40       0.0       0.0
# 2       3       2024-01-29  Doohickey         5       41.47    207.35      0.00       0.0       0.0
# 3       4       2024-01-15     Widget         4       49.43    197.72      0.00       0.0       0.0
# 4       5       2024-01-11     Widget         2       11.77      0.00     23.54       0.0       0.0

################################################################
## dr.pivot_wider(values_from = [many_cols], names_sep = "_") ##
################################################################

print(
    df_sales  
    >> dr.pivot_wider(
            names_from = f.region, 
            values_from = [f.sales, f.quantity], # Pivot multiple columns
            names_sep = "_", # Separator between the new column names
            values_fill = 0 # Fill NaN with 0
        )
    >> dr.slice_head(n = 5)
)
#        ID             date    product  unit_price       sales_East  sales_North  sales_South  sales_West
#   <int64> <datetime64[ns]>   <object>   <float64>  ...   <float64>    <float64>    <float64>   <float64>
# 0       1       2024-01-07     Gadget        6.19  ...       30.95         0.00          0.0         0.0
# 1       2       2024-01-20     Widget       21.94  ...        0.00       219.40          0.0         0.0
# 2       3       2024-01-29  Doohickey       41.47  ...      207.35         0.00          0.0         0.0
# 3       4       2024-01-15     Widget       49.43  ...      197.72         0.00          0.0         0.0
# 4       5       2024-01-11     Widget       11.77  ...        0.00        23.54          0.0         0.0

#####################################
## dr.pivot_wider(values_fn = ...) ##
#####################################
'''
values_fn: function to aggregate values 
           if there are multiple entries for the same index/column combination.
           (e.g., sum, mean, len, etc.)
'''

print(
    df_sales
    >> dr.select(f.product, f.region, f.sales) # Select only relevant columns
    >> dr.pivot_wider(
            names_from = f.product, 
            values_from = f.sales,
            values_fill = 0, # Fill NaN with 0
            values_fn = np.mean # Aggregate by sum if there are duplicates
        )
)
#     region   Doohickey      Gadget      Widget
#   <object>   <float64>   <float64>   <float64>
# 0     East  179.994000  283.253750  237.328889
# 1    North  248.782857  290.524737  239.141429
# 2    South  284.672000  183.286000  244.672500
# 3     West  256.096111  209.636957  409.786818


#----------------------------------------------------------------------------------------------------------#
#------------------------------------------ 2. dr.pivot_longer() ------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

n_patients = 8
patient_ids = [f"P{i:03d}" for i in range(1, n_patients+1)]

np.random.seed(42)
df_measurements = pd.DataFrame({
    'patient_id' : patient_ids,
    'age'        : np.random.randint(20, 80, size=n_patients),
    # Day‑specific columns (wide format)
    'BP_day1'    : np.random.randint(110, 150, size=n_patients), # BP = Blood Pressure
    'HR_day1'    : np.random.randint(60, 100, size=n_patients), # HR = Heart Rate
    'BP_day2'    : np.random.randint(110, 150, size=n_patients),
    'HR_day2'    : np.random.randint(60, 100, size=n_patients),
    'BP_day3'    : np.random.randint(110, 150, size=n_patients),
    'HR_day3'    : np.random.randint(60, 100, size=n_patients)
})

print(df_measurements)
#   patient_id  age  BP_day1  HR_day1  BP_day2  HR_day2  BP_day3  HR_day3
# 0       P001   58      128       62      142       62      134       67
# 1       P002   71      132       81      121       96      123       94
# 2       P003   48      120       61      131       66      118       73
# 3       P004   34      120       83      134       80      135       76
# 4       P005   62      133       89      136       68      111       95
# 5       P006   27      145       97      137       98      129       99
# 6       P007   40      149       61      125       77      137       63
# 7       P008   58      133       80      124       63      116       61

###################################
## dr.pivot_longer() basic usage ##
###################################

print(
    df_measurements 
    >> dr.pivot_longer(
        cols = f[f.BP_day1 : f.HR_day3], # Specify columns to pivot
        names_to = 'measurement_day', # New column names
        values_to = 'value' # Name of the new value column
        )
    >> dr.slice_head(n = 10)
)
#    HR_day3     age patient_id measurement_day   value
#    <int64> <int64>   <object>        <object> <int64>
# 0       67      58       P001         BP_day1     128
# 1       94      71       P002         BP_day1     132
# 2       73      48       P003         BP_day1     120
# 3       76      34       P004         BP_day1     120
# 4       95      62       P005         BP_day1     133
# 5       99      27       P006         BP_day1     145
# 6       63      40       P007         BP_day1     149
# 7       61      58       P008         BP_day1     133
# 8       67      58       P001         HR_day1      62
# 9       94      71       P002         HR_day1      81

##############################################
## dr.pivot_longer(cols = dr.starts_with()) ##
##############################################

print(
    df_measurements 
    >> dr.pivot_longer(
        cols = dr.starts_with(match = ["BP", "HR"]), # Specify columns to pivot
        names_to = 'measurement_day', # New column names
        values_to = 'value' # Name of the new value column
        )
    >> dr.slice_head(n = 10)
)
#       age patient_id measurement_day   value
#   <int64>   <object>        <object> <int64>
# 0      58       P001         BP_day1     128
# 1      71       P002         BP_day1     132
# 2      48       P003         BP_day1     120
# 3      34       P004         BP_day1     120
# 4      62       P005         BP_day1     133
# 5      27       P006         BP_day1     145
# 6      40       P007         BP_day1     149
# 7      58       P008         BP_day1     133
# 8      58       P001         HR_day1      62
# 9      71       P002         HR_day1      81

#################################
## dr.pivot_longer(names_sep=) ##
#################################

print(
    df_measurements 
    >> dr.pivot_longer(
        cols = dr.starts_with(match = ["BP", "HR"]), # Specify columns to pivot
        names_sep = "_", # Separator between the new column names
        names_to = ['measurement', 'day'], # New column names
        values_to = 'value' # Name of the new value column
        )
    >> dr.slice_head(n = 10)
)
#    HR_day3     age patient_id measurement      day   value
#    <int64> <int64>   <object>    <object> <object> <int64>
# 0       67      58       P001          BP     day1     128
# 1       94      71       P002          BP     day1     132
# 2       73      48       P003          BP     day1     120
# 3       76      34       P004          BP     day1     120
# 4       95      62       P005          BP     day1     133
# 5       99      27       P006          BP     day1     145
# 6       63      40       P007          BP     day1     149
# 7       61      58       P008          BP     day1     133
# 8       67      58       P001          HR     day1      62
# 9       94      71       P002          HR     day1      81

#####################################
## dr.pivot_longer(names_pattern=) ##
#####################################

print(
    df_measurements 
    >> dr.pivot_longer(
        cols = dr.starts_with(match = ["BP", "HR"]), # Specify columns to pivot
        names_to = ['measurement', 'day'], # New column names
        names_pattern = r"([A-Z]+)_(day\d+)", # Regex pattern to extract new column names
        values_to = 'value' # Name of the new value column
        )
    >> dr.slice_head(n = 10)
)
#       age patient_id measurement      day   value
#   <int64>   <object>    <object> <object> <int64>
# 0      58       P001          BP     day1     128
# 1      71       P002          BP     day1     132
# 2      48       P003          BP     day1     120
# 3      34       P004          BP     day1     120
# 4      62       P005          BP     day1     133
# 5      27       P006          BP     day1     145
# 6      40       P007          BP     day1     149
# 7      58       P008          BP     day1     133
# 8      58       P001          HR     day1      62
# 9      71       P002          HR     day1      81

print(
    df_measurements 
    >> dr.pivot_longer(
        cols = dr.starts_with(match = ["BP", "HR"]), # Specify columns to pivot
        names_to = ['measurement', 'day'], # New column names
        names_pattern = r"([A-Z]+)_day(\d+)", # Take the integer part of the day only
        values_to = 'value' # Name of the new value column
        )
    >> dr.slice_head(n = 10)
)
#       age patient_id measurement      day   value
#   <int64>   <object>    <object> <object> <int64>
# 0      58       P001          BP        1     128
# 1      71       P002          BP        1     132
# 2      48       P003          BP        1     120
# 3      34       P004          BP        1     120
# 4      62       P005          BP        1     133
# 5      27       P006          BP        1     145
# 6      40       P007          BP        1     149
# 7      58       P008          BP        1     133
# 8      58       P001          HR        1      62
# 9      71       P002          HR        1      81

#####################################################
## Combine dr.pivot_longer() with dr.pivot_wider() ##
#####################################################

print(
    df_measurements 
    >> dr.pivot_longer(
        cols = dr.starts_with(match = ["BP", "HR"]), # Specify columns to pivot
        names_to = ['measurement', 'day'], # New column names
        names_pattern = r"([A-Z]+)_day(\d+)", # Take the integer part of the day only
        values_to = 'value' # Name of the new value column
        )
    >> dr.pivot_wider(
        names_from = f.measurement,
        values_from = f.value
        )
    >> dr.slice_head(n = 10)
)
#       age      day patient_id      BP      HR
#   <int64> <object>   <object> <int64> <int64>
# 0      27        1       P006     145      97
# 1      27        2       P006     137      98
# 2      27        3       P006     129      99
# 3      34        1       P004     120      83
# 4      34        2       P004     134      80
# 5      34        3       P004     135      76
# 6      40        1       P007     149      61
# 7      40        2       P007     125      77
# 8      40        3       P007     137      63
# 9      48        1       P003     120      61


######################################################
## Apply dr.pipe(lambda f: pd.wide_to_long(df = f)) ##
######################################################

print(
    df_measurements 
    >> dr.pipe(
        lambda f: pd.wide_to_long(
            df = f,
            stubnames = ['BP', 'HR'], 
            i = ['patient_id', 'age'], 
            j = 'day', 
            sep = '_', 
            suffix = r"\w+"
        )
    )
    >> dr.pipe(lambda f: f.reset_index()) # Reset index to turn MultiIndex into columns
    >> dr.mutate(day = f.day.str.replace("day", "").astype(int)) # Remove "day" prefix and convert to int
    >> dr.slice_head(n = 10)
)
#   patient_id     age     day      BP      HR
#     <object> <int64> <int64> <int64> <int64>
# 0       P001      58       1     128      62
# 1       P001      58       2     142      62
# 2       P001      58       3     134      67
# 3       P002      71       1     132      81
# 4       P002      71       2     121      96
# 5       P002      71       3     123      94
# 6       P003      48       1     120      61
# 7       P003      48       2     131      66
# 8       P003      48       3     118      73
# 9       P004      34       1     120      83

#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 3. Cross-Table -------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
A cross-tabulation (or cross-tab) is a table that displays the frequency distribution of variables.
It is used to analyze the relationship between two or more categorical variables (Chi-squared test).

A cross-table is also called a contingency table or frequency table.
'''

##############################
## Create example DataFrame ##
##############################

n_resp = 250

np.random.seed(42)
df_survey = pd.DataFrame({
    'respondent_id'   : range(1, n_resp+1),
    
    'gender'          : np.random.choice(['Male', 'Female', 'Other'], size=n_resp,
                                          p=[0.48, 0.48, 0.04]),

    'favorite_color'  : np.random.choice(['Red', 'Blue', 'Green', 'Yellow', 'Purple'],
                                          size=n_resp),

    'purchase_intent' : np.random.choice(['Definitely', 'Probably', 'Maybe', 'Unlikely', 'Never'], 
                                          size=n_resp,
                                         p=[0.15, 0.25, 0.30, 0.20, 0.10])
})

df_survey.head()
#    respondent_id   gender favorite_color purchase_intent
#          <int64> <object>       <object>        <object>
# 0              1     Male         Purple        Probably
# 1              2   Female         Purple        Unlikely
# 2              3   Female            Red           Never
# 3              4   Female          Green           Never
# 4              5     Male           Blue        Unlikely

######################
## dr.table() usage ##
######################

print(
    dr.table(df_survey['gender'], df_survey['favorite_color'])
)
#           Blue   Green  Purple     Red  Yellow
# col_0                                         
# row_0  <int64> <int64> <int64> <int64> <int64>
# Female      24      19      31      21      26
# Male        35      15      25      23      21
# Other        1       4       2       3       0

print(
    dr.table(df_survey[['gender', 'purchase_intent']])
)
#                  Definitely   Maybe   Never  Probably  Unlikely
# purchase_intent                                                
# gender              <int64> <int64> <int64>   <int64>   <int64>
# Female                   23      35      16        29        18
# Male                     16      38      13        30        22
# Other                     1       3       1         5         0

'''
dr.table() cannot handle more than 2 variables at once (only pd.crosstab() can).
'''