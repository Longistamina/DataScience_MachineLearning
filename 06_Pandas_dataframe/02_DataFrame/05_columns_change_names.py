'''
Changing Column Names:
   + df = df.set_axis(new_names_list, axis=1, copy=True/False)
   + df = df.set_axis(df.columns.str.strip().str.replace(r"\s+", "_", regex=True), axis=1, copy=True/False) # using str methods
   + df = df.pipe(lambda df: df.set_axis(df.columns.str.strip().str.replace(r"\s+", "_", regex=True), axis=1, copy=True/False)) # using str methods in pipe
   + df.columns = new_names_list
   + df.columns = df.columns.str.replace(old_pat, new_pat)
   + df.columns = df.columns.map(string_methods)
   + df.columns = [f'col_{i+1}' for i in range(df.shape[1])]
   + df.rename(columns={'old_name': 'new_name'}, inplace=True/False)
   + df.rename(columns=lambda col: re.sub(r"\s+", "_", col.strip().lower()), inplace=True/False)
   + df.add_prefix('pre_')
   + df.add_suffix('_suf')
   + df.rename(columns={'old1':'new1'}, level=0, inplace=True/False) # for MultiIndex
'''

from pathlib import Path

import numpy as np
import pandas as pd

data_dir = Path("/home").rglob("*/DataScience_MachineLearning/data")
data_dir = next(data_dir)

df_lifexp = pd.read_csv(data_dir/"life_expectancy.csv")
print(df_lifexp.dtypes)
# Country                             object
# Year                                 int64
# Status                              object
# Life expectancy                    float64
# Adult Mortality                    float64
# infant deaths                        int64
# Alcohol                            float64
# percentage expenditure             float64
# Hepatitis B                        float64
# Measles                              int64
#  BMI                               float64
# under-five deaths                    int64
# Polio                              float64
# Total expenditure                  float64
# Diphtheria                         float64
#  HIV/AIDS                          float64
# GDP                                float64
# Population                         float64
#  thinness  1-19 years              float64
#  thinness 5-9 years                float64
# Income composition of resources    float64
# Schooling                          float64

##----------------------------------------------------##

df_emp = pd.read_csv(data_dir/"emp.csv")
print(df_emp)
#    id      name  salary  start_date        dept
# 0   1      Rick  623.30  2012-01-01          IT
# 1   2       Dan  515.20  2013-09-23  Operations
# 2   3  Michelle  611.00  2014-11-15          IT
# 3   4      Ryan  729.00  2014-05-11          HR
# 4   5      Gary  843.25  2015-03-27     Finance
# 5   6      Nina  578.00  2013-05-21          IT
# 6   7     Simon  632.80  2013-07-30  Operations
# 7   8      Guru  722.50  2014-06-17     Finance

##----------------------------------------------------##

# ## Create MultiIndex DataFrame
#
rows = pd.MultiIndex.from_tuples(
    [('Argentina', 2018), ('Argentina', 2019), ('Brazil', 2018), ('Brazil', 2019)],
    names=['Country', 'Year']
)
cols = pd.MultiIndex.from_tuples(
    [('Economic', 'GDP (bn $)'), ('Demographic', 'Population (m)')],
    names=['Domain', 'Metric']
)
np.random.seed(0)
df_multindex = pd.DataFrame(np.round(np.random.rand(len(rows), len(cols)) * 100, 2), index=rows, columns=cols)
print(df_multindex)
# Domain           Economic    Demographic
# Metric         GDP (bn $) Population (m)
# Country   Year
# Argentina 2018      54.88          71.52
#           2019      60.28          54.49
# Brazil    2018      42.37          64.59
#           2019      43.76          89.18

##-----------------------------------------------------##
## df = df.set_axis(new_names_list, axis=1, copy=True) ##
##-----------------------------------------------------##

new_colnames = ['country', 'year', 'status', 'life_expectancy', 'adult_mortality', 'infant_deaths', 'alcohol',
                'percentage_expenditure', 'hepatitis_b', 'measles', 'bmi', 'under_five_deaths', 'polio',
                'total_expenditure', 'diphtheria', 'hiv_aids', 'gdp', 'population', 'thinness_1_19_years',
                'thinness_5_9_years', 'income_composition_of_resources', 'schooling']

# Change column names (set copy=True to return a copied DataFrame)
df_new_cols = df_lifexp.set_axis(new_colnames, axis=1, copy=True)

print(df_new_cols.head(3))
#        country  year      status  ...  thinness_5_9_years  income_composition_of_resources  schooling
# 0  Afghanistan  2015  Developing  ...                17.3                            0.479       10.1
# 1  Afghanistan  2014  Developing  ...                17.5                            0.476       10.0
# 2  Afghanistan  2013  Developing  ...                17.7                            0.470        9.9

##--------------------------------------------------------------##
## df = df.set_axis(df.columns.str.method(), axis=1, copy=True) ##
##--------------------------------------------------------------##

df_new_cols = df_lifexp.set_axis(df_lifexp.columns.str.strip().str.replace(r"\s+", "_", regex=True), axis=1, copy=True)

print(df_new_cols.head(3))
#        Country  Year      Status  ...  thinness_5-9_years  Income_composition_of_resources  Schooling
# 0  Afghanistan  2015  Developing  ...                17.3                            0.479       10.1
# 1  Afghanistan  2014  Developing  ...                17.5                            0.476       10.0
# 2  Afghanistan  2013  Developing  ...                17.7                            0.470        9.9

##-------------------------------------------------------------------------------##
## df = df.pipe(lambda df: set_axis(df.columns.str.method(), axis=1, copy=True)) ##
##-------------------------------------------------------------------------------##

df_new_cols_pipe = df_lifexp.pipe(
    lambda df: df.set_axis(df.columns.str.strip().str.replace(r"\s+", "_", regex=True), axis=1)
)

print(df_new_cols_pipe.head(3))
#        Country  Year      Status  ...  thinness_5-9_years  Income_composition_of_resources  Schooling
# 0  Afghanistan  2015  Developing  ...                17.3                            0.479       10.1
# 1  Afghanistan  2014  Developing  ...                17.5                            0.476       10.0
# 2  Afghanistan  2013  Developing  ...                17.7                            0.470        9.9

##-----------------------------##
## df.columns = new_names_list ##
##-----------------------------##

df_new_cols = df_lifexp.copy()

new_colnames = ['country', 'year', 'status', 'life_expectancy', 'adult_mortality', 'infant_deaths', 'alcohol',
                'percentage_expenditure', 'hepatitis_b', 'measles', 'bmi', 'under_five_deaths', 'polio',
                'total_expenditure', 'diphtheria', 'hiv_aids', 'gdp', 'population', 'thinness_1_19_years',
                'thinness_5_9_years', 'income_composition_of_resources', 'schooling']

# Change column names
df_new_cols.columns = new_colnames

print(df_new_cols.head(3))
#        country  year      status  ...  thinness_5_9_years  income_composition_of_resources  schooling
# 0  Afghanistan  2015  Developing  ...                17.3                            0.479       10.1
# 1  Afghanistan  2014  Developing  ...                17.5                            0.476       10.0
# 2  Afghanistan  2013  Developing  ...                17.7                            0.470        9.9

# [3 rows x 22 columns]

##-------------------------------------------------------##
## df.columns = df.columns.str.replace(old_pat, new_pat) ##
##-------------------------------------------------------##

df_new_cols = df_lifexp.copy()

# Change column names
df_new_cols.columns = df_new_cols.columns.str.strip().str.replace(r"\s+", "_", regex=True)

print(df_new_cols.dtypes)
# BMI                                float64
# HIV/AIDS                           float64
# thinness_1-19_years                float64
# thinness_5-9_years                 float64

##---------------------------------------------##
## df.columns = df.columns.map(string_methods) ##
##---------------------------------------------##

df_new_cols = df_lifexp.copy()

# Change column names
df_new_cols.columns = df_new_cols.columns.map(str.lower)

print(df_new_cols.dtypes)
# country                             object
# year                                 int64
# status                              object
# life expectancy                    float64
# adult mortality                    float64

##-------------------------------------------------------##
## df.columns = [f'col_{i}' for i in range(df.shape[1])] ##
##-------------------------------------------------------##

df_new_cols = df_lifexp.copy()

# Change column names
df_new_cols.columns = [f'col_{i+1}' for i in range(df_new_cols.shape[1])]

print(df_new_cols.head(3))
#          col_1  col_2       col_3  col_4  col_5  col_6  col_7  ...  col_16      col_17      col_18  col_19  col_20  col_21  col_22
# 0  Afghanistan   2015  Developing   65.0  263.0     62   0.01  ...     0.1  584.259210  33736494.0    17.2    17.3   0.479    10.1
# 1  Afghanistan   2014  Developing   59.9  271.0     64   0.01  ...     0.1  612.696514    327582.0    17.5    17.5   0.476    10.0
# 2  Afghanistan   2013  Developing   59.9  268.0     66   0.01  ...     0.1  631.744976  31731688.0    17.7    17.7   0.470     9.9

# [3 rows x 22 columns]

##------------------------------------------------------------##
## df.rename(columns={'old_name': 'new_name'}, inplace=False) ##
##------------------------------------------------------------##

df_new_cols = df_lifexp.copy()

# Change column names (set inplace=True to modify the original DataFrame)
df_new_cols.rename(
    columns={'Life expectancy ': 'life_expectancy', 'Adult Mortality': 'adult_mortality'},
      inplace=True
)

print(df_new_cols.dtypes)
# life_expectancy                    float64
# adult_mortality                    float64

##----------------------------------------------------##
## df.rename(columns=lambda col: col.strip().lower()) ##
##----------------------------------------------------##

import re

df_new_cols = df_lifexp.copy()

# Change column names
df_new_cols.rename(
    columns=lambda col: re.sub(r"\s+", "_", col.strip().lower()),
    inplace=True
)

print(df_new_cols.dtypes)
# country                             object
# year                                 int64
# status                              object
# life_expectancy                    float64
# hepatitis_b                        float64
# adult_mortality                    float64
# thinness_1-19_years                float64
# thinness_5-9_years                 float64

##-----------------------##
## df.add_prefix('pre_') ##
##-----------------------##

df_prefixed = df_emp.add_prefix('pre_')

print(df_prefixed.head(3))
#    pre_id  pre_name  pre_salary pre_start_date    pre_dept
# 0       1      Rick       623.3     2012-01-01          IT
# 1       2       Dan       515.2     2013-09-23  Operations
# 2       3  Michelle       611.0     2014-11-15          IT

##-----------------------##
## df.add_suffix('_suf') ##
##-----------------------##

df_suffixed = df_emp.add_suffix('_suf')

print(df_suffixed.head(3))
#    id_suf  name_suf  salary_suf start_date_suf    dept_suf
# 0       1      Rick       623.3     2012-01-01          IT
# 1       2       Dan       515.2     2013-09-23  Operations
# 2       3  Michelle       611.0     2014-11-15          IT

##------------------------------------------------------------##
## df.rename(columns={'old1':'new1'}, level=0, inplace=False) ##
##------------------------------------------------------------##

df_new_cols = df_multindex.copy()

# Change column names (set inplace=True to modify the original DataFrame)
df_new_cols.rename(
    columns={'GDP (bn $)': 'GDP_billion_$', 'Population (m)': 'Population_million'},
    level=1,
    inplace=True
)

print(df_new_cols)
# Domain              Economic        Demographic
# Metric         GDP_billion_$ Population_million
# Country   Year
# Argentina 2018         54.88              71.52
#           2019         60.28              54.49
# Brazil    2018         42.37              64.59
#           2019         43.76              89.18
