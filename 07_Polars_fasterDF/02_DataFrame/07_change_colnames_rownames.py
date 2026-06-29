'''
Polars column-name changes and row-name/index-like replacements.

This file is adapted from the pandas workflow:

1. Changing Column Names:
   + pandas df.set_axis(new_names, axis=1)       -> Polars df.columns = new_names, or df.rename(dict(zip(...)))
   + pandas df.columns = new_names               -> Polars df.columns = new_names
   + pandas df.columns.str.replace(...)          -> Polars df.rename(function) or df.select(pl.all().name.replace(...))
   + pandas df.columns.map(function)             -> Polars df.rename(function) or df.select(pl.all().name.map(function))
   + pandas df.rename(columns={...})             -> Polars df.rename({...})
   + pandas df.rename(columns=lambda col: ...)   -> Polars df.rename(lambda col: ...)
   + pandas df.add_prefix('pre_')                -> Polars df.select(pl.all().name.prefix('pre_'))
   + pandas df.add_suffix('_suf')                -> Polars df.select(pl.all().name.suffix('_suf'))
   + pandas MultiIndex columns                   -> Polars uses normal flat names or Struct columns.
   + Example: clean Pokemon dataframe column names (lazyframe implementation)

2. Changing Row Names / Index:
   + Polars does NOT have pandas-style custom row indexes or MultiIndex.
   + Rows are addressed by integer position.
   + Index-like labels should be stored as normal columns.
   + pandas df.set_index('col')                  -> Polars keep that column and use it explicitly.
   + pandas df.reset_index(drop=True)            -> Usually no-op in Polars; add/drop a visible row-id column if needed.
   + pandas df.rename(index={...})               -> Rename/update values in an explicit row-label column.
   + pandas MultiIndex rows                      -> Use multiple normal key columns, e.g. Country and Year.
'''

import re
from pathlib import Path

import polars as pl
pl.Config.set_tbl_width_chars(120)


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------------- 0. Example Data -------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
This guide uses the same idea as the pandas version:
    + life_expectancy.csv has messy column names, useful for column-name cleaning.
    + emp.csv is a small employee table, useful for row-label examples.
'''

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

df_lifexp = pl.read_csv(data_dir/"life_expectancy.csv", schema_overrides={"Population":pl.Float64})
df_emp = pl.read_csv(data_dir/"emp.csv")

print(df_lifexp.head())
# shape: (5, 22)
# ┌─────────────┬──────┬────────────┬─────────────┬───┬──────────────────────┬──────────────┬────────────────┬───────────┐
# │ Country     ┆ Year ┆ Status     ┆ Life        ┆ … ┆ thinness  1-19 years ┆ thinness 5-9 ┆ Income         ┆ Schooling │
# │ ---         ┆ ---  ┆ ---        ┆ expectancy  ┆   ┆ ---                  ┆ years        ┆ composition of ┆ ---       │
# │ str         ┆ i64  ┆ str        ┆ ---         ┆   ┆ f64                  ┆ ---          ┆ resource…      ┆ f64       │
# │             ┆      ┆            ┆ f64         ┆   ┆                      ┆ f64          ┆ ---            ┆           │
# │             ┆      ┆            ┆             ┆   ┆                      ┆              ┆ f64            ┆           │
# ╞═════════════╪══════╪════════════╪═════════════╪═══╪══════════════════════╪══════════════╪════════════════╪═══════════╡
# │ Afghanistan ┆ 2015 ┆ Developing ┆ 65.0        ┆ … ┆ 17.2                 ┆ 17.3         ┆ 0.479          ┆ 10.1      │
# │ Afghanistan ┆ 2014 ┆ Developing ┆ 59.9        ┆ … ┆ 17.5                 ┆ 17.5         ┆ 0.476          ┆ 10.0      │
# │ Afghanistan ┆ 2013 ┆ Developing ┆ 59.9        ┆ … ┆ 17.7                 ┆ 17.7         ┆ 0.47           ┆ 9.9       │
# │ Afghanistan ┆ 2012 ┆ Developing ┆ 59.5        ┆ … ┆ 17.9                 ┆ 18.0         ┆ 0.463          ┆ 9.8       │
# │ Afghanistan ┆ 2011 ┆ Developing ┆ 59.2        ┆ … ┆ 18.2                 ┆ 18.2         ┆ 0.454          ┆ 9.5       │
# └─────────────┴──────┴────────────┴─────────────┴───┴──────────────────────┴──────────────┴────────────────┴───────────┘

print(df_emp)
# shape: (8, 5)
# ┌─────┬──────────┬────────┬────────────┬────────────┐
# │ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ i64 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞═════╪══════════╪════════╪════════════╪════════════╡
# │ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# │ 4   ┆ Ryan     ┆ 729.0  ┆ 2014-05-11 ┆ HR         │
# │ 5   ┆ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# │ 6   ┆ Nina     ┆ 578.0  ┆ 2013-05-21 ┆ IT         │
# │ 7   ┆ Simon    ┆ 632.8  ┆ 2013-07-30 ┆ Operations │
# │ 8   ┆ Guru     ┆ 722.5  ┆ 2014-06-17 ┆ Finance    │
# └─────┴──────────┴────────┴────────────┴────────────┘

#----------------------
## MultiIndex-like example in Polars
#----------------------
'''
Polars does not have pandas MultiIndex columns or MultiIndex rows.
Use normal columns for row keys, and use flat column names or Struct columns for nested data.
'''

df_country_year = pl.DataFrame(
    {
        "Country": ["Argentina", "Argentina", "Brazil", "Brazil"],
        "Year": [2018, 2019, 2018, 2019],
        "Economic__GDP (bn $)": [54.88, 60.28, 42.37, 43.76],
        "Demographic__Population (m)": [71.52, 54.49, 64.59, 89.18],
    }
)

print(df_country_year)
# shape: (4, 4)
# ┌───────────┬──────┬──────────────────────┬─────────────────────────────┐
# │ Country   ┆ Year ┆ Economic__GDP (bn $) ┆ Demographic__Population (m) │
# │ ---       ┆ ---  ┆ ---                  ┆ ---                         │
# │ str       ┆ i64  ┆ f64                  ┆ f64                         │
# ╞═══════════╪══════╪══════════════════════╪═════════════════════════════╡
# │ Argentina ┆ 2018 ┆ 54.88                ┆ 71.52                       │
# │ Argentina ┆ 2019 ┆ 60.28                ┆ 54.49                       │
# │ Brazil    ┆ 2018 ┆ 42.37                ┆ 64.59                       │
# │ Brazil    ┆ 2019 ┆ 43.76                ┆ 89.18                       │
# └───────────┴──────┴──────────────────────┴─────────────────────────────┘


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 1. Changing Column Names ----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

#################################
## df.columns = new_names_list ##
#################################
'''
Polars DataFrame.columns can be used to get or set the full list of column names.

Important:
    + The new list must have exactly the same length as the number of columns.
    + This mutates that DataFrame object.
    + Use df.clone() first if you do not want to change your original variable.
'''

new_colnames = [
    "country",
    "year",
    "status",
    "life_expectancy",
    "adult_mortality",
    "infant_deaths",
    "alcohol",
    "percentage_expenditure",
    "hepatitis_b",
    "measles",
    "bmi",
    "under_five_deaths",
    "polio",
    "total_expenditure",
    "diphtheria",
    "hiv_aids",
    "gdp",
    "population",
    "thinness_1_19_years",
    "thinness_5_9_years",
    "income_composition_of_resources",
    "schooling",
]

df_new_cols = df_lifexp.clone()
df_new_cols.columns = new_colnames

print(df_new_cols.head(3))
# shape: (3, 22)
# ┌─────────────┬──────┬────────────┬─────────────────┬───┬────────────────┬────────────────┬────────────────┬───────────┐
# │ country     ┆ year ┆ status     ┆ life_expectancy ┆ … ┆ thinness_1_19_ ┆ thinness_5_9_y ┆ income_composi ┆ schooling │
# │ ---         ┆ ---  ┆ ---        ┆ ---             ┆   ┆ years          ┆ ears           ┆ tion_of_resour ┆ ---       │
# │ str         ┆ i64  ┆ str        ┆ f64             ┆   ┆ ---            ┆ ---            ┆ ce…            ┆ f64       │
# │             ┆      ┆            ┆                 ┆   ┆ f64            ┆ f64            ┆ ---            ┆           │
# │             ┆      ┆            ┆                 ┆   ┆                ┆                ┆ f64            ┆           │
# ╞═════════════╪══════╪════════════╪═════════════════╪═══╪════════════════╪════════════════╪════════════════╪═══════════╡
# │ Afghanistan ┆ 2015 ┆ Developing ┆ 65.0            ┆ … ┆ 17.2           ┆ 17.3           ┆ 0.479          ┆ 10.1      │
# │ Afghanistan ┆ 2014 ┆ Developing ┆ 59.9            ┆ … ┆ 17.5           ┆ 17.5           ┆ 0.476          ┆ 10.0      │
# │ Afghanistan ┆ 2013 ┆ Developing ┆ 59.9            ┆ … ┆ 17.7           ┆ 17.7           ┆ 0.47           ┆ 9.9       │
# └─────────────┴──────┴────────────┴─────────────────┴───┴────────────────┴────────────────┴────────────────┴───────────┘

print(df_new_cols.columns[:6])
# ['country', 'year', 'status', 'life_expectancy', 'adult_mortality', 'infant_deaths']

################################################
## df.rename(dict(zip(old_names, new_names))) ##
################################################
'''
If you prefer a method-chaining style, build a mapping from old names to new names
and pass it to df.rename(). This returns a new DataFrame.

This is close to pandas df.set_axis(new_names, axis=1, copy=True), but it uses
an explicit mapping.
'''

rename_all_mapping = dict(zip(df_lifexp.columns, new_colnames))
print(rename_all_mapping)
# {'Country': 'country', 'Year': 'year', 'Status': 'status', 'Life expectancy ': 'life_expectancy', 'Adult Mortality': 'adult_mortality', 'infant deaths': 'infant_deaths', 'Alcohol': 'alcohol', 'percentage expenditure': 'percentage_expenditure', 'Hepatitis B': 'hepatitis_b', 'Measles ': 'measles', ' BMI ': 'bmi', 'under-five deaths ': 'under_five_deaths', 'Polio': 'polio', 'Total expenditure': 'total_expenditure', 'Diphtheria ': 'diphtheria', ' HIV/AIDS': 'hiv_aids', 'GDP': 'gdp', 'Population': 'population', ' thinness  1-19 years': 'thinness_1_19_years', ' thinness 5-9 years': 'thinness_5_9_years', 'Income composition of resources': 'income_composition_of_resources', 'Schooling': 'schooling'}

df_new_cols = df_lifexp.rename(rename_all_mapping)

print(df_new_cols.select("country", "year", "life_expectancy").head(3))
# shape: (3, 3)
# ┌─────────────┬──────┬─────────────────┐
# │ country     ┆ year ┆ life_expectancy │
# │ ---         ┆ ---  ┆ ---             │
# │ str         ┆ i64  ┆ f64             │
# ╞═════════════╪══════╪═════════════════╡
# │ Afghanistan ┆ 2015 ┆ 65.0            │
# │ Afghanistan ┆ 2014 ┆ 59.9            │
# │ Afghanistan ┆ 2013 ┆ 59.9            │
# └─────────────┴──────┴─────────────────┘

#########################################
## df.rename({'old_name': 'new_name'}) ##
#########################################
'''
Use df.rename({...}) to rename one or more specific columns.

Polars does not use inplace=True/False. Most Polars methods return a new DataFrame.
Assign the result back to the same variable if you want to overwrite it.
'''

df_new_cols = df_lifexp.rename(
    {
        "Life expectancy ": "life_expectancy",
        "Adult Mortality": "adult_mortality",
        "infant deaths": "infant_deaths",
    }
)

print(df_new_cols.select("Country", "Year", "life_expectancy", "adult_mortality", "infant_deaths").head(3))
# shape: (3, 5)
# ┌─────────────┬──────┬─────────────────┬─────────────────┬───────────────┐
# │ Country     ┆ Year ┆ life_expectancy ┆ adult_mortality ┆ infant_deaths │
# │ ---         ┆ ---  ┆ ---             ┆ ---             ┆ ---           │
# │ str         ┆ i64  ┆ f64             ┆ i64             ┆ i64           │
# ╞═════════════╪══════╪═════════════════╪═════════════════╪═══════════════╡
# │ Afghanistan ┆ 2015 ┆ 65.0            ┆ 263             ┆ 62            │
# │ Afghanistan ┆ 2014 ┆ 59.9            ┆ 271             ┆ 64            │
# │ Afghanistan ┆ 2013 ┆ 59.9            ┆ 268             ┆ 66            │
# └─────────────┴──────┴─────────────────┴─────────────────┴───────────────┘

######################################
## df.rename(mapping, strict=False) ##
######################################
'''
By default, Polars validates that every key in the rename mapping exists.
Set strict=False if your mapping is shared across several datasets and some columns
may be absent.
'''

safe_mapping = {
    "name": "employee_name",
    "salary": "monthly_salary",
    "not_in_this_dataframe": "ignored_name",
}

df_safe = df_emp.rename(safe_mapping, strict=False)

print(df_safe.head(3))
# shape: (3, 5)
# ┌─────┬───────────────┬────────────────┬────────────┬────────────┐
# │ id  ┆ employee_name ┆ monthly_salary ┆ start_date ┆ dept       │
# │ --- ┆ ---           ┆ ---            ┆ ---        ┆ ---        │
# │ i64 ┆ str           ┆ f64            ┆ str        ┆ str        │
# ╞═════╪═══════════════╪════════════════╪════════════╪════════════╡
# │ 1   ┆ Rick          ┆ 623.3          ┆ 2012-01-01 ┆ IT         │
# │ 2   ┆ Dan           ┆ 515.2          ┆ 2013-09-23 ┆ Operations │
# │ 3   ┆ Michelle      ┆ 611.0          ┆ 2014-11-15 ┆ IT         │
# └─────┴───────────────┴────────────────┴────────────┴────────────┘

################################
## df.rename(lambda col: ...) ##
################################
'''
Use a function when you want to clean every column name.
This is the closest Polars equivalent to pandas patterns such as:
    df.columns.str.strip().str.replace(...)
    df.columns.map(...)
    df.rename(columns=lambda col: ...)
'''

def clean_column_name(column_name: str) -> str:
    """Convert messy column names to snake_case."""
    column_name = column_name.strip().lower()
    column_name = re.sub(r"\s+", "_", column_name)
    column_name = column_name.replace("-", "_").replace("/", "_")
    return column_name

df_clean_cols = df_lifexp.rename(clean_column_name)
print(df_clean_cols.columns)
# ['country', 'year', 'status', 'life_expectancy', 'adult_mortality',
#  'infant_deaths', 'alcohol', 'percentage_expenditure', 'hepatitis_b',
#  'measles', 'bmi', 'under_five_deaths', 'polio', 'total_expenditure',
#  'diphtheria', 'hiv_aids', 'gdp', 'population', 'thinness_1_19_years',
#  'thinness_5_9_years', 'income_composition_of_resources', 'schooling']

#############################################
## df.pipe(lambda df: df.rename(function)) ##
#############################################
'''
Polars also has df.pipe(), so you can keep a long cleaning workflow readable.
This is similar to pandas pipe-based method chaining.
'''

df_clean_cols_pipe = df_lifexp.pipe(lambda df: df.rename(clean_column_name))

print(df_clean_cols_pipe.select("country", "year", "bmi", "hiv_aids").head(3))
# shape: (3, 4)
# country      year  bmi   hiv_aids
# Afghanistan  2015  19.1  0.1

##############################################
## df.select(pl.all().name.replace(r"...")) ##
##############################################
'''
The expression name namespace can rename selected output columns.

Use this when you are already inside select()/with_columns() and want to rename
columns with expression logic. For simple whole-DataFrame renaming, df.rename(...)
is usually easier.
'''

df_regex_cols = df_lifexp.select(
    pl.all()
    .name.replace(r"^\s+|\s+$", "")   # remove leading/trailing whitespace in names
    .name.replace(r"\s+", "_")        # replace inner whitespace with underscore
    # .name.to_lowercase()
)

print(df_regex_cols.columns)
# ['Country', 'Year', 'Status', 'Life_expectancy', 'Adult_Mortality', ...]

############################################
## df.select(pl.all().name.map(function)) ##
############################################
'''
Expr.name.map applies a Python function to the root column name of an expression.
This is useful for more customized naming inside a select expression.
'''

df_mapped_names = df_lifexp.select(
    pl.all().name.map(clean_column_name)
)

print(df_mapped_names.columns[:8])
# ['country', 'year', 'status', 'life_expectancy', 'adult_mortality',
#  'infant_deaths', 'alcohol', 'percentage_expenditure']

##########################################################
## df.columns = [f'col_{i+1}' for i in range(df.width)] ##
##########################################################
'''
Programmatic column names are often useful when reading files without trustworthy
headers, or when you want temporary positional names.
'''

df_numbered = df_lifexp.clone()
df_numbered.columns = [f"col_{i + 1}" for i in range(df_numbered.width)]

print(df_numbered.head(3))
# shape: (3, 22)
# ┌─────────────┬───────┬────────────┬───────┬───┬────────┬────────┬────────┬────────┐
# │ col_1       ┆ col_2 ┆ col_3      ┆ col_4 ┆ … ┆ col_19 ┆ col_20 ┆ col_21 ┆ col_22 │
# │ ---         ┆ ---   ┆ ---        ┆ ---   ┆   ┆ ---    ┆ ---    ┆ ---    ┆ ---    │
# │ str         ┆ i64   ┆ str        ┆ f64   ┆   ┆ f64    ┆ f64    ┆ f64    ┆ f64    │
# ╞═════════════╪═══════╪════════════╪═══════╪═══╪════════╪════════╪════════╪════════╡
# │ Afghanistan ┆ 2015  ┆ Developing ┆ 65.0  ┆ … ┆ 17.2   ┆ 17.3   ┆ 0.479  ┆ 10.1   │
# │ Afghanistan ┆ 2014  ┆ Developing ┆ 59.9  ┆ … ┆ 17.5   ┆ 17.5   ┆ 0.476  ┆ 10.0   │
# │ Afghanistan ┆ 2013  ┆ Developing ┆ 59.9  ┆ … ┆ 17.7   ┆ 17.7   ┆ 0.47   ┆ 9.9    │
# └─────────────┴───────┴────────────┴───────┴───┴────────┴────────┴────────┴────────┘

#############################################################
## df.select(pl.col(old).alias(new) for old, new in pairs) ##
#############################################################
'''
.alias() is the expression-level way to name outputs.
It is useful when you are selecting a subset of columns and renaming them at the same time.
'''

df_selected_alias = df_lifexp.select(
    pl.col("Country").alias("country"),
    pl.col("Year").alias("year"),
    pl.col("Life expectancy ").alias("life_expectancy"),
    pl.col("Adult Mortality").alias("adult_mortality"),
)

print(df_selected_alias.head(3))
# shape: (3, 4)
# ┌─────────────┬──────┬─────────────────┬─────────────────┐
# │ country     ┆ year ┆ life_expectancy ┆ adult_mortality │
# │ ---         ┆ ---  ┆ ---             ┆ ---             │
# │ str         ┆ i64  ┆ f64             ┆ i64             │
# ╞═════════════╪══════╪═════════════════╪═════════════════╡
# │ Afghanistan ┆ 2015 ┆ 65.0            ┆ 263             │
# │ Afghanistan ┆ 2014 ┆ 59.9            ┆ 271             │
# │ Afghanistan ┆ 2013 ┆ 59.9            ┆ 268             │
# └─────────────┴──────┴─────────────────┴─────────────────┘

#########################################################
## Add prefix: df.select(pl.all().name.prefix('pre_')) ##
#########################################################
'''
Polars does not have DataFrame.add_prefix().
Use the expression name namespace instead.
'''

df_prefixed = df_emp.select(pl.all().name.prefix("pre_"))

print(df_prefixed.head(3))
# shape: (3, 5)
# ┌────────┬──────────┬────────────┬────────────────┬────────────┐
# │ pre_id ┆ pre_name ┆ pre_salary ┆ pre_start_date ┆ pre_dept   │
# │ ---    ┆ ---      ┆ ---        ┆ ---            ┆ ---        │
# │ i64    ┆ str      ┆ f64        ┆ str            ┆ str        │
# ╞════════╪══════════╪════════════╪════════════════╪════════════╡
# │ 1      ┆ Rick     ┆ 623.3      ┆ 2012-01-01     ┆ IT         │
# │ 2      ┆ Dan      ┆ 515.2      ┆ 2013-09-23     ┆ Operations │
# │ 3      ┆ Michelle ┆ 611.0      ┆ 2014-11-15     ┆ IT         │
# └────────┴──────────┴────────────┴────────────────┴────────────┘

#########################################################
## Add suffix: df.select(pl.all().name.suffix('_suf')) ##
#########################################################
'''
Polars does not have DataFrame.add_suffix().
Use the expression name namespace instead.
'''

df_suffixed = df_emp.select(pl.all().name.suffix("_suf"))

print(df_suffixed.head(3))
# shape: (3, 5)
# ┌────────┬──────────┬────────────┬────────────────┬────────────┐
# │ id_suf ┆ name_suf ┆ salary_suf ┆ start_date_suf ┆ dept_suf   │
# │ ---    ┆ ---      ┆ ---        ┆ ---            ┆ ---        │
# │ i64    ┆ str      ┆ f64        ┆ str            ┆ str        │
# ╞════════╪══════════╪════════════╪════════════════╪════════════╡
# │ 1      ┆ Rick     ┆ 623.3      ┆ 2012-01-01     ┆ IT         │
# │ 2      ┆ Dan      ┆ 515.2      ┆ 2013-09-23     ┆ Operations │
# │ 3      ┆ Michelle ┆ 611.0      ┆ 2014-11-15     ┆ IT         │
# └────────┴──────────┴────────────┴────────────────┴────────────┘

#############################################################
## MultiIndex-column equivalent: use flat names or Structs ##
#############################################################
'''
Pandas can rename one level of MultiIndex columns.
Polars does not have MultiIndex columns.

Common Polars replacements:
    1. Use flat column names with a separator, such as 'Economic__GDP_billion_usd'.
    2. Use Struct columns when you truly want nested fields.
'''

# Flat-name approach: rename pieces of the column names.
df_flat_renamed = df_country_year.rename(
    lambda col: (
        col.replace("GDP (bn $)", "GDP_billion_usd")
        .replace("Population (m)", "Population_million")
        .replace(" ", "_")
    )
)
print(df_flat_renamed)
# shape: (4, 4)
# ┌───────────┬──────┬───────────────────────────┬─────────────────────────────────┐
# │ Country   ┆ Year ┆ Economic__GDP_billion_usd ┆ Demographic__Population_millio… │
# │ ---       ┆ ---  ┆ ---                       ┆ ---                             │
# │ str       ┆ i64  ┆ f64                       ┆ f64                             │
# ╞═══════════╪══════╪═══════════════════════════╪═════════════════════════════════╡
# │ Argentina ┆ 2018 ┆ 54.88                     ┆ 71.52                           │
# │ Argentina ┆ 2019 ┆ 60.28                     ┆ 54.49                           │
# │ Brazil    ┆ 2018 ┆ 42.37                     ┆ 64.59                           │
# │ Brazil    ┆ 2019 ┆ 43.76                     ┆ 89.18                           │
# └───────────┴──────┴───────────────────────────┴─────────────────────────────────┘

# Struct approach: keep nested concepts in Struct columns.
df_struct_like = df_flat_renamed.select(
    "Country",
    "Year",
    pl.struct(
        pl.col("Economic__GDP_billion_usd").alias("GDP_billion_usd")
    ).alias("Economic"),
    pl.struct(
        pl.col("Demographic__Population_million").alias("Population_million")
    ).alias("Demographic"),
)
print(df_struct_like)
# shape: (4, 4)
# ┌───────────┬──────┬───────────┬─────────────┐
# │ Country   ┆ Year ┆ Economic  ┆ Demographic │
# │ ---       ┆ ---  ┆ ---       ┆ ---         │
# │ str       ┆ i64  ┆ struct[1] ┆ struct[1]   │
# ╞═══════════╪══════╪═══════════╪═════════════╡
# │ Argentina ┆ 2018 ┆ {54.88}   ┆ {71.52}     │
# │ Argentina ┆ 2019 ┆ {60.28}   ┆ {54.49}     │
# │ Brazil    ┆ 2018 ┆ {42.37}   ┆ {64.59}     │
# │ Brazil    ┆ 2019 ┆ {43.76}   ┆ {89.18}     │
# └───────────┴──────┴───────────┴─────────────┘

############################################################################################
##        Example: clean Pokemon dataframe column names (lazyframe implementation)        ##
############################################################################################

lf_pokemon = (
    pl.scan_csv(data_dir/"pokemon.csv")
    .rename(lambda name: name.strip()) # remove trailing space characters
    .select(
        pl.all()
        .name.replace(r"\s+", "_") # replace " " or "  " (or more consecutive space characters) with just one "_"
        .name.replace(".", "", literal=True) # replace "." with empty string (remove it), literal=True to deactive regex
    )
)

print(lf_pokemon.collect())
# shape: (800, 13)
# ┌─────┬───────────────────────┬─────────┬────────┬───┬────────┬───────┬────────────┬───────────┐
# │ #   ┆ Name                  ┆ Type_1  ┆ Type_2 ┆ … ┆ Sp_Def ┆ Speed ┆ Generation ┆ Legendary │
# │ --- ┆ ---                   ┆ ---     ┆ ---    ┆   ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
# │ i64 ┆ str                   ┆ str     ┆ str    ┆   ┆ i64    ┆ i64   ┆ i64        ┆ bool      │
# ╞═════╪═══════════════════════╪═════════╪════════╪═══╪════════╪═══════╪════════════╪═══════════╡
# │ 1   ┆ Bulbasaur             ┆ Grass   ┆ Poison ┆ … ┆ 65     ┆ 45    ┆ 1          ┆ false     │
# │ 2   ┆ Ivysaur               ┆ Grass   ┆ Poison ┆ … ┆ 80     ┆ 60    ┆ 1          ┆ false     │
# │ 3   ┆ Venusaur              ┆ Grass   ┆ Poison ┆ … ┆ 100    ┆ 80    ┆ 1          ┆ false     │
# │ 3   ┆ VenusaurMega Venusaur ┆ Grass   ┆ Poison ┆ … ┆ 120    ┆ 80    ┆ 1          ┆ false     │
# │ 4   ┆ Charmander            ┆ Fire    ┆ null   ┆ … ┆ 50     ┆ 65    ┆ 1          ┆ false     │
# │ …   ┆ …                     ┆ …       ┆ …      ┆ … ┆ …      ┆ …     ┆ …          ┆ …         │
# │ 719 ┆ Diancie               ┆ Rock    ┆ Fairy  ┆ … ┆ 150    ┆ 50    ┆ 6          ┆ true      │
# │ 719 ┆ DiancieMega Diancie   ┆ Rock    ┆ Fairy  ┆ … ┆ 110    ┆ 110   ┆ 6          ┆ true      │
# │ 720 ┆ HoopaHoopa Confined   ┆ Psychic ┆ Ghost  ┆ … ┆ 130    ┆ 70    ┆ 6          ┆ true      │
# │ 720 ┆ HoopaHoopa Unbound    ┆ Psychic ┆ Dark   ┆ … ┆ 130    ┆ 80    ┆ 6          ┆ true      │
# │ 721 ┆ Volcanion             ┆ Fire    ┆ Water  ┆ … ┆ 90     ┆ 70    ┆ 6          ┆ true      │
# └─────┴───────────────────────┴─────────┴────────┴───┴────────┴───────┴────────────┴───────────┘



#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 2. Changing Row Names / Index ----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The most important Polars concept in this section:

    Polars has no pandas-style row index.

So there are no true row names to change. When you need row labels, create an
ordinary column such as 'row_id', 'row_name', 'id', 'Country', or 'Year'.
Because these are normal columns, you can select, filter, join, group, rename,
and update them explicitly.
'''

print(df_emp)
# shape: (8, 5)
# ┌─────┬──────────┬────────┬────────────┬────────────┐
# │ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ i64 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞═════╪══════════╪════════╪════════════╪════════════╡
# │ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# │ 4   ┆ Ryan     ┆ 729.0  ┆ 2014-05-11 ┆ HR         │
# │ 5   ┆ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# │ 6   ┆ Nina     ┆ 578.0  ┆ 2013-05-21 ┆ IT         │
# │ 7   ┆ Simon    ┆ 632.8  ┆ 2013-07-30 ┆ Operations │
# │ 8   ┆ Guru     ┆ 722.5  ┆ 2014-06-17 ┆ Finance    │
# └─────┴──────────┴────────┴────────────┴────────────┘

################################################
## df.with_row_index(name='row_id', offset=0) ##
################################################
'''
Use with_row_index() when you need visible row positions.
The result is an ordinary column, not a special index.
'''

df_with_row_id = df_emp.with_row_index(name="row_id")

print(df_with_row_id.head(3))
# shape: (3, 6)
# ┌────────┬─────┬──────────┬────────┬────────────┬────────────┐
# │ row_id ┆ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---    ┆ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ u32    ┆ i64 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞════════╪═════╪══════════╪════════╪════════════╪════════════╡
# │ 0      ┆ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 1      ┆ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ 2      ┆ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# └────────┴─────┴──────────┴────────┴────────────┴────────────┘

###################################
## with_row_index(..., offset=1) ##
###################################
'''Use offset=1 if you want row numbers that start at 1.'''

df_with_row_num = df_emp.with_row_index(name="row_num", offset=1)

print(df_with_row_num.head(3))
# shape: (3, 6)
# ┌─────────┬─────┬──────────┬────────┬────────────┬────────────┐
# │ row_num ┆ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---     ┆ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ u32     ┆ i64 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞═════════╪═════╪══════════╪════════╪════════════╪════════════╡
# │ 1       ┆ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 2       ┆ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ 3       ┆ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# └─────────┴─────┴──────────┴────────┴────────────┴────────────┘

#####################################
## Create custom row-label strings ##
#####################################
'''
This is the Polars equivalent of assigning row names like:
    df.index = [f'row_{i+1}' for i in range(len(df))]

In Polars, make those labels an ordinary column.
'''

df_row_labels = (
    df_emp.with_row_index("row_nr")
    .with_columns(
        pl.format("row_{}", pl.col("row_nr") + 1).alias("row_name")
    )
    .drop("row_nr")
    .select("row_name", pl.exclude("row_name"))
)

print(df_row_labels.head(3))
# shape: (3, 6)
# ┌──────────┬─────┬──────────┬────────┬────────────┬────────────┐
# │ row_name ┆ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---      ┆ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ str      ┆ i64 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞══════════╪═════╪══════════╪════════╪════════════╪════════════╡
# │ row_1    ┆ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ row_2    ┆ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ row_3    ┆ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# └──────────┴─────┴──────────┴────────┴────────────┴────────────┘

########################################################
## Transform row-label column with string expressions ##
########################################################
'''
This replaces pandas examples such as:
    df.index = df.index.astype(str).str.replace(...)
    df.index = df.index.astype(str).map(...)

Because row labels are a normal String column, use the Polars .str namespace.
'''

df_row_label_cleaned = df_row_labels.with_columns(
    pl.col("row_name").str.replace_all(r"\d+", "label").alias("row_name")
)
print(df_row_label_cleaned.head(3))
# shape: (3, 6)
# ┌───────────┬─────┬──────────┬────────┬────────────┬────────────┐
# │ row_name  ┆ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---       ┆ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ str       ┆ i64 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞═══════════╪═════╪══════════╪════════╪════════════╪════════════╡
# │ row_label ┆ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ row_label ┆ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ row_label ┆ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# └───────────┴─────┴──────────┴────────┴────────────┴────────────┘

# Add underscores around a row number, similar in spirit to pandas string map/center.
df_row_label_centered = (
    df_emp.with_row_index("row_nr")
    .with_columns(
        (pl.lit("_") + pl.col("row_nr").cast(pl.String) + pl.lit("_")).alias("row_name")
    )
    .drop("row_nr")
    .select("row_name", pl.exclude("row_name"))
)
print(df_row_label_centered.head(3))
# shape: (3, 6)
# ┌──────────┬─────┬──────────┬────────┬────────────┬────────────┐
# │ row_name ┆ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---      ┆ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ str      ┆ i64 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞══════════╪═════╪══════════╪════════╪════════════╪════════════╡
# │ _0_      ┆ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ _1_      ┆ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ _2_      ┆ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# └──────────┴─────┴──────────┴────────┴────────────┴────────────┘

###############################
## pandas df.set_index('id') ##
###############################
'''
There is no df.set_index() in Polars because there is no special index.
Keep the key as a normal column and use it explicitly.

This is usually clearer than hidden index state.
'''

# Put id first, if you want it visually to behave like a key column.
df_key_first = df_emp.select("id", pl.exclude("id"))

print(df_key_first.head(3))
# shape: (3, 5)
# ┌─────┬──────────┬────────┬────────────┬────────────┐
# │ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ i64 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞═════╪══════════╪════════╪════════════╪════════════╡
# │ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# └─────┴──────────┴────────┴────────────┴────────────┘

# Use the key column explicitly for filtering.
print(df_emp.filter(pl.col("id") == 3))
# shape: (1, 5)
# ┌─────┬──────────┬────────┬────────────┬──────┐
# │ id  ┆ name     ┆ salary ┆ start_date ┆ dept │
# │ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---  │
# │ i64 ┆ str      ┆ f64    ┆ str        ┆ str  │
# ╞═════╪══════════╪════════╪════════════╪══════╡
# │ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT   │
# └─────┴──────────┴────────┴────────────┴──────┘

# Use the key column explicitly for grouping.
print(df_emp.group_by("dept").agg(pl.col("salary").mean().alias("avg_salary")))
# shape: (4, 2)
# ┌────────────┬────────────┐
# │ dept       ┆ avg_salary │
# │ ---        ┆ ---        │
# │ str        ┆ f64        │
# ╞════════════╪════════════╡
# │ Operations ┆ 574.0      │
# │ Finance    ┆ 782.875    │
# │ HR         ┆ 729.0      │
# │ IT         ┆ 604.1      │
# └────────────┴────────────┘

######################################
## pandas df.reset_index(drop=True) ##
######################################
'''
In pandas, filtering keeps the original index labels, so reset_index(drop=True)
is often used to make row labels 0, 1, 2, ... again.

In Polars, row labels are not preserved because they do not exist.
So after filtering, there is normally nothing to reset.
If you want a visible fresh row number, add it with with_row_index().
'''

df_lifexp_2014 = df_lifexp.filter(pl.col("Year") == 2014)
print(df_lifexp_2014.select("Country", "Year", "Status").head())
# shape: (5, 3)
# ┌─────────────────────┬──────┬────────────┐
# │ Country             ┆ Year ┆ Status     │
# │ ---                 ┆ ---  ┆ ---        │
# │ str                 ┆ i64  ┆ str        │
# ╞═════════════════════╪══════╪════════════╡
# │ Afghanistan         ┆ 2014 ┆ Developing │
# │ Albania             ┆ 2014 ┆ Developing │
# │ Algeria             ┆ 2014 ┆ Developing │
# │ Angola              ┆ 2014 ┆ Developing │
# │ Antigua and Barbuda ┆ 2014 ┆ Developing │
# └─────────────────────┴──────┴────────────┘

# Add a fresh visible row id after filtering.
df_lifexp_2014_with_row_id = df_lifexp_2014.with_row_index("row_id")
print(df_lifexp_2014_with_row_id.select("row_id", "Country", "Year", "Status").head())
# shape: (5, 4)
# ┌────────┬─────────────────────┬──────┬────────────┐
# │ row_id ┆ Country             ┆ Year ┆ Status     │
# │ ---    ┆ ---                 ┆ ---  ┆ ---        │
# │ u32    ┆ str                 ┆ i64  ┆ str        │
# ╞════════╪═════════════════════╪══════╪════════════╡
# │ 0      ┆ Afghanistan         ┆ 2014 ┆ Developing │
# │ 1      ┆ Albania             ┆ 2014 ┆ Developing │
# │ 2      ┆ Algeria             ┆ 2014 ┆ Developing │
# │ 3      ┆ Angola              ┆ 2014 ┆ Developing │
# │ 4      ┆ Antigua and Barbuda ┆ 2014 ┆ Developing │
# └────────┴─────────────────────┴──────┴────────────┘

#######################################################
## pandas df.rename(index={'old': 'new'}) equivalent ##
#######################################################
'''
To rename row labels in Polars, update an explicit row-label column.
Use replace() for simple mapping, or when/then/otherwise for conditional logic.
'''

row_name_mapping = {
    "row_1": "employee_1",
    "row_2": "employee_2",
    "row_3": "employee_3",
}

df_row_labels_renamed = df_row_labels.with_columns(
    pl.col("row_name").replace(row_name_mapping).alias("row_name")
)
print(df_row_labels_renamed.head(5))
# shape: (5, 6)
# ┌────────────┬─────┬──────────┬────────┬────────────┬────────────┐
# │ row_name   ┆ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---        ┆ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ str        ┆ i64 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞════════════╪═════╪══════════╪════════╪════════════╪════════════╡
# │ employee_1 ┆ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ employee_2 ┆ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ employee_3 ┆ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# │ row_4      ┆ 4   ┆ Ryan     ┆ 729.0  ┆ 2014-05-11 ┆ HR         │
# │ row_5      ┆ 5   ┆ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# └────────────┴─────┴──────────┴────────┴────────────┴────────────┘

# Conditional row-label update.
df_row_labels_conditional = df_row_labels.with_columns(
    pl.when(pl.col("dept") == "IT")
    .then(pl.lit("it_employee"))
    .otherwise(pl.col("row_name"))
    .alias("row_name")
)
print(df_row_labels_conditional.head(5))
# shape: (5, 6)
# ┌─────────────┬─────┬──────────┬────────┬────────────┬────────────┐
# │ row_name    ┆ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---         ┆ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ str         ┆ i64 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞═════════════╪═════╪══════════╪════════╪════════════╪════════════╡
# │ it_employee ┆ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ row_2       ┆ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ it_employee ┆ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# │ row_4       ┆ 4   ┆ Ryan     ┆ 729.0  ┆ 2014-05-11 ┆ HR         │
# │ row_5       ┆ 5   ┆ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# └─────────────┴─────┴──────────┴────────┴────────────┴────────────┘

#########################################################
## MultiIndex-row equivalent: use multiple key columns ##
#########################################################
'''
Pandas MultiIndex rows often store several pieces of key information in the index,
for example Country and Year.

In Polars, keep them as normal columns. This makes grouping, filtering, joining,
and renaming explicit.
'''

print(df_country_year)
# shape: (4, 4)
# ┌───────────┬──────┬──────────────────────┬─────────────────────────────┐
# │ Country   ┆ Year ┆ Economic__GDP (bn $) ┆ Demographic__Population (m) │
# │ ---       ┆ ---  ┆ ---                  ┆ ---                         │
# │ str       ┆ i64  ┆ f64                  ┆ f64                         │
# ╞═══════════╪══════╪══════════════════════╪═════════════════════════════╡
# │ Argentina ┆ 2018 ┆ 54.88                ┆ 71.52                       │
# │ Argentina ┆ 2019 ┆ 60.28                ┆ 54.49                       │
# │ Brazil    ┆ 2018 ┆ 42.37                ┆ 64.59                       │
# │ Brazil    ┆ 2019 ┆ 43.76                ┆ 89.18                       │
# └───────────┴──────┴──────────────────────┴─────────────────────────────┘

# Rename values in one key column, similar to renaming one level of a pandas MultiIndex.
df_year_labels = df_country_year.with_columns(
    pl.col("Year")
    .cast(pl.String)
    .replace({"2018": "Year_2018", "2019": "Year_2019"})
    .alias("Year")
)
print(df_year_labels)
# shape: (4, 4)
# ┌───────────┬───────────┬──────────────────────┬─────────────────────────────┐
# │ Country   ┆ Year      ┆ Economic__GDP (bn $) ┆ Demographic__Population (m) │
# │ ---       ┆ ---       ┆ ---                  ┆ ---                         │
# │ str       ┆ str       ┆ f64                  ┆ f64                         │
# ╞═══════════╪═══════════╪══════════════════════╪═════════════════════════════╡
# │ Argentina ┆ Year_2018 ┆ 54.88                ┆ 71.52                       │
# │ Argentina ┆ Year_2019 ┆ 60.28                ┆ 54.49                       │
# │ Brazil    ┆ Year_2018 ┆ 42.37                ┆ 64.59                       │
# │ Brazil    ┆ Year_2019 ┆ 43.76                ┆ 89.18                       │
# └───────────┴───────────┴──────────────────────┴─────────────────────────────┘

# Or combine multiple key columns into one explicit label column.
df_country_year_label = df_country_year.with_columns(
    pl.concat_str([pl.col("Country"), pl.col("Year").cast(pl.String)], separator="_").alias("country_year")
).select("country_year", pl.exclude("country_year"))
print(df_country_year_label)
# shape: (4, 5)
# ┌────────────────┬───────────┬──────┬──────────────────────┬─────────────────────────────┐
# │ country_year   ┆ Country   ┆ Year ┆ Economic__GDP (bn $) ┆ Demographic__Population (m) │
# │ ---            ┆ ---       ┆ ---  ┆ ---                  ┆ ---                         │
# │ str            ┆ str       ┆ i64  ┆ f64                  ┆ f64                         │
# ╞════════════════╪═══════════╪══════╪══════════════════════╪═════════════════════════════╡
# │ Argentina_2018 ┆ Argentina ┆ 2018 ┆ 54.88                ┆ 71.52                       │
# │ Argentina_2019 ┆ Argentina ┆ 2019 ┆ 60.28                ┆ 54.49                       │
# │ Brazil_2018    ┆ Brazil    ┆ 2018 ┆ 42.37                ┆ 64.59                       │
# │ Brazil_2019    ┆ Brazil    ┆ 2019 ┆ 43.76                ┆ 89.18                       │
# └────────────────┴───────────┴──────┴──────────────────────┴─────────────────────────────┘


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 3. LazyFrame Notes ------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
The same naming ideas work in lazy pipelines.
For lazy CSV scans, rename columns before collecting the query.
'''

lf_emp = df_emp.lazy()

lf_clean = (
    lf_emp
    .rename(lambda col: col.upper())
    .with_row_index("row_id")
)

print(lf_clean.collect().head(3))
# shape: (3, 6)
# ┌────────┬─────┬──────────┬────────┬────────────┬────────────┐
# │ row_id ┆ ID  ┆ NAME     ┆ SALARY ┆ START_DATE ┆ DEPT       │
# │ ---    ┆ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ u32    ┆ i64 ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞════════╪═════╪══════════╪════════╪════════════╪════════════╡
# │ 0      ┆ 1   ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 1      ┆ 2   ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ 2      ┆ 3   ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# └────────┴─────┴──────────┴────────┴────────────┴────────────┘


#--------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 4. Quick Pandas-to-Polars Map -----------------------------------------#
#--------------------------------------------------------------------------------------------------------------#
'''
Quick map:

Pandas                                             Polars
------                                             ------
df.set_axis(new_names, axis=1)                     df.columns = new_names
                                                   df.rename(dict(zip(df.columns, new_names)))

df.columns = new_names                             df.columns = new_names

df.columns.str.strip().str.replace(...)           df.rename(clean_function)
                                                   df.select(pl.all().name.replace(...))

df.columns.map(function)                           df.rename(function)
                                                   df.select(pl.all().name.map(function))

df.rename(columns={'old': 'new'})                  df.rename({'old': 'new'})

df.rename(columns=lambda col: ...)                 df.rename(lambda col: ...)

df.add_prefix('pre_')                              df.select(pl.all().name.prefix('pre_'))

df.add_suffix('_suf')                              df.select(pl.all().name.suffix('_suf'))

df.rename(columns={...}, level=...)                No MultiIndex columns; use flat names or Structs.

df.set_axis(new_indices, axis=0)                   No row names; create a normal column.

df.index = new_indices                             Add/update a normal row-label column.

df.set_index('id')                                 Keep 'id' as a normal key column.

df.reset_index(drop=True)                          Usually no-op; add fresh row ids with with_row_index().

df.rename(index={'old': 'new'})                    Update values in a row-label column with replace().

df.rename(index={...}, level=...)                  No MultiIndex rows; use multiple normal key columns.
'''
