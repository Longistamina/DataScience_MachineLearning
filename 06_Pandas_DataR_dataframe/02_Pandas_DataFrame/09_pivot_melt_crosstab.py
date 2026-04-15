'''
Pivot, Melt and Cross-Table are powerful techniques allowing you to reshape

####################################

1. Pivot: long to wide
   + pd.pivot() || df.pivot()
   + pd.pivot_table() || df.pivot_table()

2. Melt: wide to long
   + pd.metl() || df.melt()
   + pd.wide_to_long(): support more complex reshaping (BR_day1, BR_day2, HR_day1, HR_day2 => "BR", "HR" and "day" columns)

3. Cross-Table
   + pd.crosstab()
'''

import pandas as pd
import numpy as np

#---------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. Pivot: long to wide ----------------------------------------#
#---------------------------------------------------------------------------------------------------------#

####################################
##    pd.pivot() || df.pivot()    ##
####################################
'''
The .pivot() converts unique values from one column into multiple columns in the DataFrame.
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
).assign(sales = lambda df: df.eval("quantity * unit_price")) # Add a column with the total sales amount

df_sales.head()
#    ID       date region    product  quantity  unit_price   sales
# 0   1 2024-01-07   East     Gadget         5        6.19   30.95
# 1   2 2024-01-20  North     Widget        10       21.94  219.40
# 2   3 2024-01-29   East  Doohickey         5       41.47  207.35
# 3   4 2024-01-15   East     Widget         4       49.43  197.72
# 4   5 2024-01-11  North     Widget         2       11.77   23.54

#--------
## Basic usage
#--------

df_pivoted = pd.pivot(
    data=df_sales,
    index="ID", # The column to be kept intact, becomes the new index
    columns="region", # The column whose unique values will become new columns
    values="sales" # The column whose values will fill the new DataFrame
)

print(df_pivoted.head())
# region    East   North  South  West
# ID                                 
# 1        30.95     NaN    NaN   NaN
# 2          NaN  219.40    NaN   NaN
# 3       207.35     NaN    NaN   NaN
# 4       197.72     NaN    NaN   NaN
# 5          NaN   23.54    NaN   NaN

#--------
## Using multiple variables for columns=
#--------

df_pivoted_multi = pd.pivot(
    data=df_sales,
    index="ID",
    columns=["region", "product"], # Multiple columns for new columns
    values="sales"
)

print(df_pivoted_multi.head())
# region    East   North      East           West  North  South   West     North      West  South          
# product Gadget  Widget Doohickey  Widget Gadget Gadget Widget Widget Doohickey Doohickey Gadget Doohickey
# ID                                                                                                       
# 1        30.95     NaN       NaN     NaN    NaN    NaN    NaN    NaN       NaN       NaN    NaN       NaN
# 2          NaN  219.40       NaN     NaN    NaN    NaN    NaN    NaN       NaN       NaN    NaN       NaN
# 3          NaN     NaN    207.35     NaN    NaN    NaN    NaN    NaN       NaN       NaN    NaN       NaN
# 4          NaN     NaN       NaN  197.72    NaN    NaN    NaN    NaN       NaN       NaN    NaN       NaN
# 5          NaN   23.54       NaN     NaN    NaN    NaN    NaN    NaN       NaN       NaN    NaN       NaN

#--------
## Using multiple variables for values=
#--------

df_pivoted_multi = pd.pivot(
    data=df_sales,
    index="ID",
    columns="region",
    values=["sales", "date"] # Multiple columns for values
)

print(df_pivoted_multi.head())
#          sales                         date                      
# region    East  North South West       East      North South West
# ID                                                               
# 1        30.95    NaN   NaN  NaN 2024-01-07        NaT   NaT  NaT
# 2          NaN  219.4   NaN  NaN        NaT 2024-01-20   NaT  NaT
# 3       207.35    NaN   NaN  NaN 2024-01-29        NaT   NaT  NaT
# 4       197.72    NaN   NaN  NaN 2024-01-15        NaT   NaT  NaT
# 5          NaN  23.54   NaN  NaN        NaT 2024-01-11   NaT  NaT

#---------
## Join column names after pivoting
#---------

df_pivoted_multi = pd.pivot(
    data=df_sales,
    index="ID",
    columns="region",
    values=["sales", "date"] # Multiple columns for values
)

print(df_pivoted_multi.columns)
# MultiIndex([('sales',  'East'),
#             ('sales', 'North'),
#             ('sales', 'South'),
#             ('sales',  'West'),
#             ( 'date',  'East'),
#             ( 'date', 'North'),
#             ( 'date', 'South'),
#             ( 'date',  'West')],
#            names=[None, 'region'])

df_pivoted_multi.columns = ['_'.join(col).strip() for col in df_pivoted_multi.columns.values]
print(df_pivoted_multi.head())
#    sales_East sales_North sales_South sales_West  date_East date_North date_South date_West
# ID                                                                                         
# 1       30.95         NaN         NaN        NaN 2024-01-07        NaT        NaT       NaT
# 2         NaN       219.4         NaN        NaN        NaT 2024-01-20        NaT       NaT
# 3      207.35         NaN         NaN        NaN 2024-01-29        NaT        NaT       NaT
# 4      197.72         NaN         NaN        NaN 2024-01-15        NaT        NaT       NaT
# 5         NaN       23.54         NaN        NaN        NaT 2024-01-11        NaT       NaT

#--------
## Using df.pivot()
#--------

df_pivoted = df_sales.pivot(
    index="ID",
    columns="region",
    values="sales"
)

print(df_pivoted.head())
# region    East   North  South  West
# ID                                 
# 1        30.95     NaN    NaN   NaN
# 2          NaN  219.40    NaN   NaN
# 3       207.35     NaN    NaN   NaN
# 4       197.72     NaN    NaN   NaN
# 5          NaN   23.54    NaN   NaN

###########################################
## pd.pivot_table() || df.pivot_table()  ##
###########################################
'''
The .pivot_table() is a more flexible version of .pivot(), 
=> allowing you to aggregate data when there are duplicate values.
'''

df_duplicates = pd.DataFrame(
    {
        "ID": ["one", "one", "one", "two", "two", "one", "one", "two", "two"],
        "class": ["foo", "foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar"],
        "size": ["small", "large", "large", "small", "small", "large", "small", "small", "large"],
        "scores": [1, 2, 2, 3, 3, 4, 5, 6, 7],
        "measurements": [2, 4, 5, 5, 6, 6, 8, 9, 9]
    }
)

print(df_duplicates)
#     ID class   size  scores  measurements
# 0  one   foo  small       1             2
# 1  one   foo  large       2             4
# 2  one   foo  large       2             5
# 3  two   foo  small       3             5
# 4  two   foo  small       3             6
# 5  one   bar  large       4             6
# 6  one   bar  small       5             8
# 7  two   bar  small       6             9
# 8  two   bar  large       7             9

df_duplicates.pivot(index="ID", columns="class", values="scores")
'''ValueError: Index contains duplicate entries, cannot reshap'''

#-------------
## Use pd.pivot_table() to handle duplicates
#-------------

df_pivoted_tbl = pd.pivot_table(
    data=df_duplicates,
    index="ID",
    columns="class",
    values="scores",
    aggfunc="mean", # aggfunc to handle duplicates (default is 'mean')
)

print(df_pivoted_tbl)
# class  bar       foo
# ID                  
# one    4.5  1.666667
# two    6.5  3.000000

#-------------
## Use multiple aggfunc
#-------------

df_pivoted_tbl = pd.pivot_table(
    data=df_duplicates,
    index="ID",
    columns="size",
    values="measurements",
    aggfunc=["mean", "sum"] # Multiple aggfunc
)

print(df_pivoted_tbl)
#       mean             sum      
# size large     small large small
# ID                              
# one    5.0  5.000000    15    10
# two    9.0  6.666667     9    20

#-------------
## Use multiple values
#-------------

df_pivoted_tbl = pd.pivot_table(
    data=df_duplicates,
    index="ID",
    columns="size",
    values=["scores", "measurements"], # Multiple values
    aggfunc="mean"
)

print(df_pivoted_tbl)
#      measurements              scores      
# size        large     small     large small
# ID                                         
# one           5.0  5.000000  2.666667   3.0
# two           9.0  6.666667  7.000000   4.0

#-------------
## Use multiple grouping columns
#-------------

df_pivoted_tbl = pd.pivot_table(
    data=df_duplicates,
    index="ID", # Multiple grouping columns
    columns=["size", "class"],
    values="scores",
    aggfunc=np.std, # Standard deviation as aggfunc
    dropna=False # Keep NaN columns
)

print(df_pivoted_tbl)
# size  large      small     
# class   bar  foo   bar  foo
# ID                         
# one     NaN  0.0   NaN  NaN
# two     NaN  NaN   NaN  0.0

#-------------
## Use df.pivot_table()
#-------------

df_pivoted_tbl = df_duplicates.pivot_table(
    index="ID",
    columns="class",
    values="scores",
    aggfunc="mean"
)

print(df_pivoted_tbl)
# class  bar       foo
# ID                  
# one    4.5  1.666667
# two    6.5  3.000000


#---------------------------------------------------------------------------------------------------------#
#------------------------------------------ 2. Melt: wide to long ----------------------------------------#
#---------------------------------------------------------------------------------------------------------#

##############################
## Create example DataFrame ##
##############################

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

####################################
##     pd.melt() || df.melt()     ##
####################################

#--------
## pd.melt()
#--------

df_melted = pd.melt(
    frame=df_measurements,
    id_vars=['patient_id', 'age'], # Columns to keep intact
    value_vars=[col for col in df_measurements.columns if col.startswith(('BP_', 'HR_'))], # Columns to melt
    var_name='measurement_day', # Name for the new variable column
    value_name='mearsured_value' # Name for the new value column
)

print(df_melted.head())
#   patient_id  age measurement_day  mearsured_value
# 0       P001   58         BP_day1              128
# 1       P002   71         BP_day1              132
# 2       P003   48         BP_day1              120
# 3       P004   34         BP_day1              120
# 4       P005   62         BP_day1              133

#--------
## df.melt()
#--------

df_melted = df_measurements.melt(
    id_vars=['patient_id', 'age'],
    value_vars=[col for col in df_measurements.columns if col.startswith(('BP_', 'HR_'))],
    var_name='measurement_day',
    value_name='mearsured_value'
)

print(df_melted.head())
#   patient_id  age measurement_day  mearsured_value
# 0       P001   58         BP_day1              128
# 1       P002   71         BP_day1              132
# 2       P003   48         BP_day1              120
# 3       P004   34         BP_day1              120
# 4       P005   62         BP_day1              133

###############################
##     pd.wide_to_long()     ##
###############################

#----------
## Basic usage
#----------

df_wtl = pd.wide_to_long(
    df=df_measurements,
    stubnames=['BP', 'HR'], # The prefixes of the columns to be melted
    i=['patient_id', 'age'], # Columns to keep intact (as index)
    j='day', # The suffix that will become the new variable column
    sep='_', # Separator between stubname and suffix (ONE CHARACTER ONLY)
    suffix=r"\w+" # Suffix pattern (r"\w+" means any word characters, including "day" and digits "1", "2", "3")
)
# BP_day1: 
# + sep is "_" 
# + stubname is "BP" 
# + j is "day"
# + suffix is "day1" (matches r"\w+")

print(df_wtl.head())
#                       BP  HR
# patient_id age day          
# P001       58  day1  128  62
#                day2  142  62
#                day3  134  67
# P002       71  day1  132  81
#                day2  121  96

#-----------
## Use .reset_index() to turn index into columns
#-----------

df_wtl = pd.wide_to_long(
    df=df_measurements,
    stubnames=['BP', 'HR'], 
    i=['patient_id', 'age'], 
    j='day', 
    sep='_', 
    suffix=r"\w+"
).reset_index()

print(df_wtl.head())
#   patient_id  age   day   BP  HR
# 0       P001   58  day1  128  62
# 1       P001   58  day2  142  62
# 2       P001   58  day3  134  67
# 3       P002   71  day1  132  81
# 4       P002   71  day2  121  96

#-----------
## Apply chaining methods
#-----------

df_wtl = (
    pd.wide_to_long(
        df=df_measurements,
        stubnames=['BP', 'HR'], 
        i=['patient_id', 'age'], 
        j='day', 
        sep='_', 
        suffix=r"\w+"
    )
    .reset_index()
    .assign(day = lambda df: df['day'].str.replace('day', '').astype(int)) # Convert 'day' column to integer
)

print(df_wtl.head(10))
#   patient_id  age  day   BP  HR
# 0       P001   58    1  128  62
# 1       P001   58    2  142  62
# 2       P001   58    3  134  67
# 3       P002   71    1  132  81
# 4       P002   71    2  121  96
# 5       P002   71    3  123  94
# 6       P003   48    1  120  61
# 7       P003   48    2  131  66
# 8       P003   48    3  118  73
# 9       P004   34    1  120  83


#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------- 3. Cross-Table -------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
A cross-tabulation (or cross-tab) is a table that displays the frequency distribution of variables.
It is used to analyze the relationship between two or more categorical variables (Chi-squared test).
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
#    respondent_id  gender favorite_color purchase_intent
# 0              1    Male         Purple        Probably
# 1              2  Female         Purple        Unlikely
# 2              3  Female            Red           Never
# 3              4  Female          Green           Never
# 4              5    Male           Blue        Unlikely

################################
##        pd.crosstab()       ##
################################

#----------
## Basic usage
#----------

contigency_table = pd.crosstab(
    index=df_survey['gender'], # Values to group by in the rows.
    columns=df_survey['favorite_color'], # Values to group by in the columns.
    dropna=False # Keep NaN columns
)

print(contigency_table)
# favorite_color  Blue  Green  Purple  Red  Yellow
# gender                                          
# Female            24     19      31   21      26
# Male              35     15      25   23      21
# Other              1      4       2    3       0

#----------
## With margins=True
#----------

contigency_table = pd.crosstab(
    index=df_survey['gender'], 
    columns=df_survey['favorite_color'], 
    margins=True, # Add row and column totals (named "All")
    dropna=False 
)

print(contigency_table)
# favorite_color  Blue  Green  Purple  Red  Yellow  All
# gender                                               
# Female            24     19      31   21      26  121
# Male              35     15      25   23      21  119
# Other              1      4       2    3       0   10
# All               60     38      58   47      47  250

#----------
## With normalize='index'
#----------

contigency_table = pd.crosstab(
    index=df_survey["gender"], 
    columns=df_survey["purchase_intent"],
    normalize='index', # Normalize by row (index)
    dropna=False
)

print(contigency_table)
# purchase_intent  Definitely     Maybe     Never  Probably  Unlikely
# gender                                                             
# Female             0.190083  0.289256  0.132231  0.239669  0.148760
# Male               0.134454  0.319328  0.109244  0.252101  0.184874
# Other              0.100000  0.300000  0.100000  0.500000  0.000000
'''Normalize to percentages within rows(index), so that each row sums to 1.'''

#----------
## With normalize='columns'
#----------

contigency_table = pd.crosstab(
    index=df_survey["gender"], 
    columns=df_survey["purchase_intent"],
    normalize='columns', # Normalize by columns
    dropna=False
)

print(contigency_table)
# purchase_intent  Definitely     Maybe     Never  Probably  Unlikely
# gender                                                             
# Female                0.575  0.460526  0.533333  0.453125      0.45
# Male                  0.400  0.500000  0.433333  0.468750      0.55
# Other                 0.025  0.039474  0.033333  0.078125      0.00
'''Normalize to percentages within columns, so that each column sums to 1.'''

#----------
## With normalize='all'
#----------

contigency_table = pd.crosstab(
    index=df_survey["gender"], 
    columns=df_survey["purchase_intent"],
    normalize='all', # Normalize by all values
    dropna=False
)

print(contigency_table)
# purchase_intent  Definitely  Maybe  Never  Probably  Unlikely
# gender                                                       
# Female                0.092  0.140  0.064     0.116     0.072
# Male                  0.064  0.152  0.052     0.120     0.088
# Other                 0.004  0.012  0.004     0.020     0.000
'''Normalize to percentages of the total, so that the entire table sums to 1.'''

#----------
## With multiple columns=
#----------

contigency_table = pd.crosstab(
    index=df_survey["gender"], 
    columns=[df_survey["favorite_color"], df_survey["purchase_intent"]],
    dropna=False
)

print(contigency_table)
# favorite_color        Blue                                    Green        ...      Red              Yellow                              
# purchase_intent Definitely Maybe Never Probably Unlikely Definitely Maybe  ... Probably Unlikely Definitely Maybe Never Probably Unlikely
# gender                                                                     ...                                                           
# Female                   7     7     1        4        5          2     7  ...        4        4          6     8     4        8        0
# Male                     3    10     4       12        6          0     4  ...        4        5          3     9     3        1        5
# Other                    0     0     1        0        0          1     2  ...        2        0          0     0     0        0        0

######

contigency_table = (
    pd.crosstab(
        index=df_survey["gender"],
        columns=[df_survey["favorite_color"], df_survey["purchase_intent"]],
        dropna=False
    )
    .pipe(
        lambda df: df.set_axis(
            df.columns.map(lambda tup_col: "_".join(tup_col)), # Join multi-level columns with "_"
            axis=1
        )
    )
)

print(contigency_table)
#         Blue_Definitely  Blue_Maybe  Blue_Never  Blue_Probably  ...  Yellow_Maybe  Yellow_Never  Yellow_Probably  Yellow_Unlikely
# gender                                                          ...                                                              
# Female                7           7           1              4  ...             8             4                8                0
# Male                  3          10           4             12  ...             9             3                1                5
# Other                 0           0           1              0  ...             0             0                0                0