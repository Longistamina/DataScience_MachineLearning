'''
Change Column Names:
   + df.columns = new_names
   + lf.rename({...})
   + lf.select(pl.col(old).alias(new) for old, new in pairs)
   + lf.rename(dict(zip(old_names, new_names)))
   + lf.rename(mapping, strict=False)
   + lf.rename(lambda x: ...)
   + lf.select(pl.all().name.replace(...))
   + lf.select(pl.all().name.prefix('pre_'))
   + lf.select(pl.all().name.suffix('_suf'))
   + Example: clean Pokemon dataframe column names (lazyframe implementation)
'''

import re
from pathlib import Path

import polars as pl
from polars import col as c

pl.Config.set_tbl_width_chars(120)
data_dir = next(Path("/home").glob("**/DataScience*/data"))

df_lifexp = pl.read_csv(data_dir/"life_expectancy.csv", schema_overrides={"Population":pl.Float64})
lf_lifexp = df_lifexp.lazy()

print(df_lifexp.glimpse(max_items_per_column=5, return_type="string"))
# Rows: 2938
# Columns: 22
# $ Country                         <str> 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan'
# $ Year                            <i64> 2015, 2014, 2013, 2012, 2011
# $ Status                          <str> 'Developing', 'Developing', 'Developing', 'Developing', 'Developing'
# $ Life expectancy                 <f64> 65.0, 59.9, 59.9, 59.5, 59.2
# $ Adult Mortality                 <i64> 263, 271, 268, 272, 275
# $ infant deaths                   <i64> 62, 64, 66, 69, 71
# $ Alcohol                         <f64> 0.01, 0.01, 0.01, 0.01, 0.01
# $ percentage expenditure          <f64> 71.27962362, 73.52358168, 73.21924272, 78.1842153, 7.097108703
# $ Hepatitis B                     <i64> 65, 62, 64, 67, 68
# $ Measles                         <i64> 1154, 492, 430, 2787, 3013
# $  BMI                            <f64> 19.1, 18.6, 18.1, 17.6, 17.2
# $ under-five deaths               <i64> 83, 86, 89, 93, 97
# $ Polio                           <i64> 6, 58, 62, 67, 68
# $ Total expenditure               <f64> 8.16, 8.18, 8.13, 8.52, 7.87
# $ Diphtheria                      <i64> 65, 62, 64, 67, 68
# $  HIV/AIDS                       <f64> 0.1, 0.1, 0.1, 0.1, 0.1
# $ GDP                             <f64> 584.25921, 612.696514, 631.744976, 669.959, 63.537231
# $ Population                      <f64> 33736494.0, 327582.0, 31731688.0, 3696958.0, 2978599.0
# $  thinness  1-19 years           <f64> 17.2, 17.5, 17.7, 17.9, 18.2
# $  thinness 5-9 years             <f64> 17.3, 17.5, 17.7, 18.0, 18.2
# $ Income composition of resources <f64> 0.479, 0.476, 0.47, 0.463, 0.454
# $ Schooling                       <f64> 10.1, 10.0, 9.9, 9.8, 9.5
'''Very bad column names!!!'''

##-----------------------------##
## df.columns = new_names_list ##
##-----------------------------##
'''
Polars DataFrame.columns can be used to get or set the full list of column names.

NOTE: this method only works with DataFrame

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

df_new = df_lifexp.clone()
df_new.columns = new_colnames

print(df_new.head(2))
# shape: (2, 22)
# ┌─────────────┬──────┬────────────┬─────────────────┬───┬────────────────┬────────────────┬────────────────┬───────────┐
# │ country     ┆ year ┆ status     ┆ life_expectancy ┆ … ┆ thinness_1_19_ ┆ thinness_5_9_y ┆ income_composi ┆ schooling │
# │ ---         ┆ ---  ┆ ---        ┆ ---             ┆   ┆ years          ┆ ears           ┆ tion_of_resour ┆ ---       │
# │ str         ┆ i64  ┆ str        ┆ f64             ┆   ┆ ---            ┆ ---            ┆ ce…            ┆ f64       │
# │             ┆      ┆            ┆                 ┆   ┆ f64            ┆ f64            ┆ ---            ┆           │
# │             ┆      ┆            ┆                 ┆   ┆                ┆                ┆ f64            ┆           │
# ╞═════════════╪══════╪════════════╪═════════════════╪═══╪════════════════╪════════════════╪════════════════╪═══════════╡
# │ Afghanistan ┆ 2015 ┆ Developing ┆ 65.0            ┆ … ┆ 17.2           ┆ 17.3           ┆ 0.479          ┆ 10.1      │
# │ Afghanistan ┆ 2014 ┆ Developing ┆ 59.9            ┆ … ┆ 17.5           ┆ 17.5           ┆ 0.476          ┆ 10.0      │
# └─────────────┴──────┴────────────┴─────────────────┴───┴────────────────┴────────────────┴────────────────┴───────────┘


print(df_new.columns[:6])
# ['country', 'year', 'status', 'life_expectancy', 'adult_mortality', 'infant_deaths']

##-------------------------------------##
## lf.rename({'old_name': 'new_name'}) ##
##-------------------------------------##
'''
Use df.rename({...}) to rename one or more specific columns.

Polars does not use inplace=True/False. Most Polars methods return a new DataFrame.
Assign the result back to the same variable if you want to overwrite it.
'''

print(
    lf_lifexp
    .rename({
        "Life expectancy ": "life_expectancy",
        "Adult Mortality": "adult_mortality",
        "infant deaths": "infant_deaths",
    })
    .select("life_expectancy", "adult_mortality", "infant_deaths")
    .head(2)
    .collect()
)
# shape: (2, 3)
# ┌─────────────────┬─────────────────┬───────────────┐
# │ life_expectancy ┆ adult_mortality ┆ infant_deaths │
# │ ---             ┆ ---             ┆ ---           │
# │ f64             ┆ i64             ┆ i64           │
# ╞═════════════════╪═════════════════╪═══════════════╡
# │ 65.0            ┆ 263             ┆ 62            │
# │ 59.9            ┆ 271             ┆ 64            │
# └─────────────────┴─────────────────┴───────────────┘

##---------------------------------------------------------##
## lf.select(pl.col(old).alias(new) for old, new in pairs) ##
##---------------------------------------------------------##
'''
.alias() is the expression-level way to name outputs.
It is useful when you are selecting a subset of columns and renaming them at the same time.
'''

print(
    lf_lifexp
    .select(
        c("Country").alias("country"),
        c("Year").alias("year"),
        c("Life expectancy ").alias("life_expectancy"),
        c("Adult Mortality").alias("adult_mortality"),
    )
    .head(2)
    .collect()
)
# shape: (2, 4)
# ┌─────────────┬──────┬─────────────────┬─────────────────┐
# │ country     ┆ year ┆ life_expectancy ┆ adult_mortality │
# │ ---         ┆ ---  ┆ ---             ┆ ---             │
# │ str         ┆ i64  ┆ f64             ┆ i64             │
# ╞═════════════╪══════╪═════════════════╪═════════════════╡
# │ Afghanistan ┆ 2015 ┆ 65.0            ┆ 263             │
# │ Afghanistan ┆ 2014 ┆ 59.9            ┆ 271             │
# └─────────────┴──────┴─────────────────┴─────────────────┘
'''Only contains the 4 columns specified in `.select()`'''

##--------------------------------------------##
## lf.rename(dict(zip(old_names, new_names))) ##
##--------------------------------------------##
'''
If you prefer a method-chaining style, build a mapping from old names to new names
and pass it to `lf.rename()`. This returns a new DataFrame.

This is close to pandas df.set_axis(new_names, axis=1, copy=True),
but it uses an explicit mapping.
'''

print(dict(zip(lf_lifexp.collect_schema().names(), new_colnames)))
# {'Country': 'country', 'Year': 'year', 'Status': 'status', 'Life expectancy ': 'life_expectancy', 'Adult Mortality': 'adult_mortality', 'infant deaths': 'infant_deaths', 'Alcohol': 'alcohol', 'percentage expenditure': 'percentage_expenditure', 'Hepatitis B': 'hepatitis_b', 'Measles ': 'measles', ' BMI ': 'bmi', 'under-five deaths ': 'under_five_deaths', 'Polio': 'polio', 'Total expenditure': 'total_expenditure', 'Diphtheria ': 'diphtheria', ' HIV/AIDS': 'hiv_aids', 'GDP': 'gdp', 'Population': 'population', ' thinness  1-19 years': 'thinness_1_19_years', ' thinness 5-9 years': 'thinness_5_9_years', 'Income composition of resources': 'income_composition_of_resources', 'Schooling': 'schooling'}

print(
    lf_lifexp
    .rename(dict(zip(lf_lifexp.collect_schema().names(), new_colnames))) # For DataFrame, use `dict(zip(df.columns, new_colnames))`
    .head(2)
    .collect()
)
# shape: (2, 22)
# ┌─────────────┬──────┬────────────┬─────────────────┬───┬────────────────┬────────────────┬────────────────┬───────────┐
# │ country     ┆ year ┆ status     ┆ life_expectancy ┆ … ┆ thinness_1_19_ ┆ thinness_5_9_y ┆ income_composi ┆ schooling │
# │ ---         ┆ ---  ┆ ---        ┆ ---             ┆   ┆ years          ┆ ears           ┆ tion_of_resour ┆ ---       │
# │ str         ┆ i64  ┆ str        ┆ f64             ┆   ┆ ---            ┆ ---            ┆ ce…            ┆ f64       │
# │             ┆      ┆            ┆                 ┆   ┆ f64            ┆ f64            ┆ ---            ┆           │
# │             ┆      ┆            ┆                 ┆   ┆                ┆                ┆ f64            ┆           │
# ╞═════════════╪══════╪════════════╪═════════════════╪═══╪════════════════╪════════════════╪════════════════╪═══════════╡
# │ Afghanistan ┆ 2015 ┆ Developing ┆ 65.0            ┆ … ┆ 17.2           ┆ 17.3           ┆ 0.479          ┆ 10.1      │
# │ Afghanistan ┆ 2014 ┆ Developing ┆ 59.9            ┆ … ┆ 17.5           ┆ 17.5           ┆ 0.476          ┆ 10.0      │
# └─────────────┴──────┴────────────┴─────────────────┴───┴────────────────┴────────────────┴────────────────┴───────────┘

##----------------------------------##
## lf.rename(mapping, strict=False) ##
##----------------------------------##
'''
By default, Polars validates that every key in the rename mapping exists.
Set strict=False if your mapping is shared across several datasets and some columns may be absent.
'''

safe_mapping = {
    "Country": "country",
    "Year": "year",
    "not_in_this_dataframe": "ignored_name",
}

print(
    lf_lifexp
    .rename(safe_mapping, strict=False) # set `strict=True` and it will raise errors
    .head(2)
    .collect()
)
# shape: (2, 22)
# ┌─────────────┬──────┬────────────┬─────────────┬───┬──────────────────────┬──────────────┬────────────────┬───────────┐
# │ country     ┆ year ┆ Status     ┆ Life        ┆ … ┆ thinness  1-19 years ┆ thinness 5-9 ┆ Income         ┆ Schooling │
# │ ---         ┆ ---  ┆ ---        ┆ expectancy  ┆   ┆ ---                  ┆ years        ┆ composition of ┆ ---       │
# │ str         ┆ i64  ┆ str        ┆ ---         ┆   ┆ f64                  ┆ ---          ┆ resource…      ┆ f64       │
# │             ┆      ┆            ┆ f64         ┆   ┆                      ┆ f64          ┆ ---            ┆           │
# │             ┆      ┆            ┆             ┆   ┆                      ┆              ┆ f64            ┆           │
# ╞═════════════╪══════╪════════════╪═════════════╪═══╪══════════════════════╪══════════════╪════════════════╪═══════════╡
# │ Afghanistan ┆ 2015 ┆ Developing ┆ 65.0        ┆ … ┆ 17.2                 ┆ 17.3         ┆ 0.479          ┆ 10.1      │
# │ Afghanistan ┆ 2014 ┆ Developing ┆ 59.9        ┆ … ┆ 17.5                 ┆ 17.5         ┆ 0.476          ┆ 10.0      │
# └─────────────┴──────┴────────────┴─────────────┴───┴──────────────────────┴──────────────┴────────────────┴───────────┘

##---------------------##
## lf.rename(function) ##
##---------------------##
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

print(
    lf_lifexp
    .rename(clean_column_name)
    .head(2)
    .collect()
)
# shape: (2, 22)
# ┌─────────────┬──────┬────────────┬─────────────────┬───┬────────────────┬────────────────┬────────────────┬───────────┐
# │ country     ┆ year ┆ status     ┆ life_expectancy ┆ … ┆ thinness_1_19_ ┆ thinness_5_9_y ┆ income_composi ┆ schooling │
# │ ---         ┆ ---  ┆ ---        ┆ ---             ┆   ┆ years          ┆ ears           ┆ tion_of_resour ┆ ---       │
# │ str         ┆ i64  ┆ str        ┆ f64             ┆   ┆ ---            ┆ ---            ┆ ce…            ┆ f64       │
# │             ┆      ┆            ┆                 ┆   ┆ f64            ┆ f64            ┆ ---            ┆           │
# │             ┆      ┆            ┆                 ┆   ┆                ┆                ┆ f64            ┆           │
# ╞═════════════╪══════╪════════════╪═════════════════╪═══╪════════════════╪════════════════╪════════════════╪═══════════╡
# │ Afghanistan ┆ 2015 ┆ Developing ┆ 65.0            ┆ … ┆ 17.2           ┆ 17.3           ┆ 0.479          ┆ 10.1      │
# │ Afghanistan ┆ 2014 ┆ Developing ┆ 59.9            ┆ … ┆ 17.5           ┆ 17.5           ┆ 0.476          ┆ 10.0      │
# └─────────────┴──────┴────────────┴─────────────────┴───┴────────────────┴────────────────┴────────────────┴───────────┘

##--------------------------##
## lf.rename(lambda x: ...) ##
##--------------------------##

print(
    lf_lifexp
    .rename(lambda x: x.strip().lower()) # `x` is Python string
    .rename(lambda x: re.sub(r"\s+", "_", x))
    .rename(lambda x: x.replace("-", "_").replace("/", "_"))
    .head(2)
    .collect()
)
# shape: (2, 22)
# ┌─────────────┬──────┬────────────┬─────────────────┬───┬────────────────┬────────────────┬────────────────┬───────────┐
# │ country     ┆ year ┆ status     ┆ life_expectancy ┆ … ┆ thinness_1_19_ ┆ thinness_5_9_y ┆ income_composi ┆ schooling │
# │ ---         ┆ ---  ┆ ---        ┆ ---             ┆   ┆ years          ┆ ears           ┆ tion_of_resour ┆ ---       │
# │ str         ┆ i64  ┆ str        ┆ f64             ┆   ┆ ---            ┆ ---            ┆ ce…            ┆ f64       │
# │             ┆      ┆            ┆                 ┆   ┆ f64            ┆ f64            ┆ ---            ┆           │
# │             ┆      ┆            ┆                 ┆   ┆                ┆                ┆ f64            ┆           │
# ╞═════════════╪══════╪════════════╪═════════════════╪═══╪════════════════╪════════════════╪════════════════╪═══════════╡
# │ Afghanistan ┆ 2015 ┆ Developing ┆ 65.0            ┆ … ┆ 17.2           ┆ 17.3           ┆ 0.479          ┆ 10.1      │
# │ Afghanistan ┆ 2014 ┆ Developing ┆ 59.9            ┆ … ┆ 17.5           ┆ 17.5           ┆ 0.476          ┆ 10.0      │
# └─────────────┴──────┴────────────┴─────────────────┴───┴────────────────┴────────────────┴────────────────┴───────────┘

##---------------------------------------##
## lf.select(pl.all().name.replace(...)) ##
##---------------------------------------##
'''NO NEED `import re` !!!'''

print(
    lf_lifexp
    .select(
        pl.all()
        .name.to_lowercase()
        .name.replace(r"\s+", "_")
        .name.replace("-", "_", literal=True) # `literal=True` to turn off regular expression
        .name.replace("/", "_", literal=True)
    )
    .head(2)
    .collect()
)
# shape: (2, 22)
# ┌─────────────┬──────┬────────────┬─────────────────┬───┬────────────────┬────────────────┬────────────────┬───────────┐
# │ country     ┆ year ┆ status     ┆ life_expectancy ┆ … ┆ _thinness_1_19 ┆ _thinness_5_9_ ┆ income_composi ┆ schooling │
# │ ---         ┆ ---  ┆ ---        ┆ _               ┆   ┆ _years         ┆ years          ┆ tion_of_resour ┆ ---       │
# │ str         ┆ i64  ┆ str        ┆ ---             ┆   ┆ ---            ┆ ---            ┆ ce…            ┆ f64       │
# │             ┆      ┆            ┆ f64             ┆   ┆ f64            ┆ f64            ┆ ---            ┆           │
# │             ┆      ┆            ┆                 ┆   ┆                ┆                ┆ f64            ┆           │
# ╞═════════════╪══════╪════════════╪═════════════════╪═══╪════════════════╪════════════════╪════════════════╪═══════════╡
# │ Afghanistan ┆ 2015 ┆ Developing ┆ 65.0            ┆ … ┆ 17.2           ┆ 17.3           ┆ 0.479          ┆ 10.1      │
# │ Afghanistan ┆ 2014 ┆ Developing ┆ 59.9            ┆ … ┆ 17.5           ┆ 17.5           ┆ 0.476          ┆ 10.0      │
# └─────────────┴──────┴────────────┴─────────────────┴───┴────────────────┴────────────────┴────────────────┴───────────┘

##----------------------------------------##
## lf.select(pl.all().name.map(function)) ##
##----------------------------------------##
'''
Expr.name.map applies a Python function to the root column name of an expression.
This is useful for more customized naming inside a select expression.
'''

print(
    lf_lifexp
    .select(pl.all().name.map(clean_column_name))
    .head(2)
    .collect()
)
# shape: (2, 22)
# ┌─────────────┬──────┬────────────┬─────────────────┬───┬────────────────┬────────────────┬────────────────┬───────────┐
# │ country     ┆ year ┆ status     ┆ life_expectancy ┆ … ┆ thinness_1_19_ ┆ thinness_5_9_y ┆ income_composi ┆ schooling │
# │ ---         ┆ ---  ┆ ---        ┆ ---             ┆   ┆ years          ┆ ears           ┆ tion_of_resour ┆ ---       │
# │ str         ┆ i64  ┆ str        ┆ f64             ┆   ┆ ---            ┆ ---            ┆ ce…            ┆ f64       │
# │             ┆      ┆            ┆                 ┆   ┆ f64            ┆ f64            ┆ ---            ┆           │
# │             ┆      ┆            ┆                 ┆   ┆                ┆                ┆ f64            ┆           │
# ╞═════════════╪══════╪════════════╪═════════════════╪═══╪════════════════╪════════════════╪════════════════╪═══════════╡
# │ Afghanistan ┆ 2015 ┆ Developing ┆ 65.0            ┆ … ┆ 17.2           ┆ 17.3           ┆ 0.479          ┆ 10.1      │
# │ Afghanistan ┆ 2014 ┆ Developing ┆ 59.9            ┆ … ┆ 17.5           ┆ 17.5           ┆ 0.476          ┆ 10.0      │
# └─────────────┴──────┴────────────┴─────────────────┴───┴────────────────┴────────────────┴────────────────┴───────────┘

##-----------------------------------------##
## lf.select(pl.all().name.prefix('pre_')) ##
##-----------------------------------------##
'''The reversal function is `.strip_prefix()`'''

lf_emp = pl.scan_csv(data_dir/"emp.csv")
print(lf_emp.head(2).collect())
# shape: (2, 5)
# ┌─────┬──────┬────────┬────────────┬────────────┐
# │ id  ┆ name ┆ salary ┆ start_date ┆ dept       │
# │ --- ┆ ---  ┆ ---    ┆ ---        ┆ ---        │
# │ i64 ┆ str  ┆ f64    ┆ str        ┆ str        │
# ╞═════╪══════╪════════╪════════════╪════════════╡
# │ 1   ┆ Rick ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 2   ┆ Dan  ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# └─────┴──────┴────────┴────────────┴────────────┘

print(
    lf_emp
    .select(pl.all().name.prefix('pre_'))
    .head(2)
    .collect()
)
# shape: (2, 5)
# ┌────────┬──────────┬────────────┬────────────────┬────────────┐
# │ pre_id ┆ pre_name ┆ pre_salary ┆ pre_start_date ┆ pre_dept   │
# │ ---    ┆ ---      ┆ ---        ┆ ---            ┆ ---        │
# │ i64    ┆ str      ┆ f64        ┆ str            ┆ str        │
# ╞════════╪══════════╪════════════╪════════════════╪════════════╡
# │ 1      ┆ Rick     ┆ 623.3      ┆ 2012-01-01     ┆ IT         │
# │ 2      ┆ Dan      ┆ 515.2      ┆ 2013-09-23     ┆ Operations │
# └────────┴──────────┴────────────┴────────────────┴────────────┘

##-----------------------------------------##
## lf.select(pl.all().name.suffix('_suf')) ##
##-----------------------------------------##
'''The reversal function is `.strip_suffix()`'''

lf_emp = pl.scan_csv(data_dir/"emp.csv")
print(lf_emp.head(2).collect())
# shape: (2, 5)
# ┌─────┬──────┬────────┬────────────┬────────────┐
# │ id  ┆ name ┆ salary ┆ start_date ┆ dept       │
# │ --- ┆ ---  ┆ ---    ┆ ---        ┆ ---        │
# │ i64 ┆ str  ┆ f64    ┆ str        ┆ str        │
# ╞═════╪══════╪════════╪════════════╪════════════╡
# │ 1   ┆ Rick ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 2   ┆ Dan  ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# └─────┴──────┴────────┴────────────┴────────────┘

print(
    lf_emp
    .select(pl.all().name.suffix('_suf'))
    .head(2)
    .collect()
)
# shape: (2, 5)
# ┌────────┬──────────┬────────────┬────────────────┬────────────┐
# │ id_suf ┆ name_suf ┆ salary_suf ┆ start_date_suf ┆ dept_suf   │
# │ ---    ┆ ---      ┆ ---        ┆ ---            ┆ ---        │
# │ i64    ┆ str      ┆ f64        ┆ str            ┆ str        │
# ╞════════╪══════════╪════════════╪════════════════╪════════════╡
# │ 1      ┆ Rick     ┆ 623.3      ┆ 2012-01-01     ┆ IT         │
# │ 2      ┆ Dan      ┆ 515.2      ┆ 2013-09-23     ┆ Operations │
# └────────┴──────────┴────────────┴────────────────┴────────────┘

##----------------------------------------------------------------------------------------##
##        Example: clean Pokemon dataframe column names (lazyframe implementation)        ##
##----------------------------------------------------------------------------------------##

lf_pokemon = pl.scan_csv(data_dir/"pokemon.csv")

with pl.Config(tbl_cols=15, tbl_width_chars=140):
    print(lf_pokemon.head(2).collect())
    # shape: (2, 13)
    # ┌─────┬───────────┬────────┬────────┬───────┬─────┬────────┬─────────┬─────────┬─────────┬───────┬────────────┬───────────┐
    # │ #   ┆ Name      ┆ Type 1 ┆ Type 2 ┆ Total ┆ HP  ┆ Attack ┆ Defense ┆ Sp. Atk ┆ Sp. Def ┆ Speed ┆ Generation ┆ Legendary │
    # │ --- ┆ ---       ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---     ┆ ---     ┆ ---   ┆ ---        ┆ ---       │
    # │ i64 ┆ str       ┆ str    ┆ str    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64     ┆ i64     ┆ i64   ┆ i64        ┆ bool      │
    # ╞═════╪═══════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪═════════╪═════════╪═══════╪════════════╪═══════════╡
    # │ 1   ┆ Bulbasaur ┆ Grass  ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65      ┆ 65      ┆ 45    ┆ 1          ┆ false     │
    # │ 2   ┆ Ivysaur   ┆ Grass  ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80      ┆ 80      ┆ 60    ┆ 1          ┆ false     │
    # └─────┴───────────┴────────┴────────┴───────┴─────┴────────┴─────────┴─────────┴─────────┴───────┴────────────┴───────────┘

with pl.Config(tbl_cols=15, tbl_width_chars=140):
    print(
        lf_pokemon
        .select(pl.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
        .head(2)
        .collect()
    )
    # shape: (2, 13)
    # ┌─────┬───────────┬────────┬────────┬───────┬─────┬────────┬─────────┬────────┬────────┬───────┬────────────┬───────────┐
    # │ #   ┆ name      ┆ type_1 ┆ type_2 ┆ total ┆ hp  ┆ attack ┆ defense ┆ sp_atk ┆ sp_def ┆ speed ┆ generation ┆ legendary │
    # │ --- ┆ ---       ┆ ---    ┆ ---    ┆ ---   ┆ --- ┆ ---    ┆ ---     ┆ ---    ┆ ---    ┆ ---   ┆ ---        ┆ ---       │
    # │ i64 ┆ str       ┆ str    ┆ str    ┆ i64   ┆ i64 ┆ i64    ┆ i64     ┆ i64    ┆ i64    ┆ i64   ┆ i64        ┆ bool      │
    # ╞═════╪═══════════╪════════╪════════╪═══════╪═════╪════════╪═════════╪════════╪════════╪═══════╪════════════╪═══════════╡
    # │ 1   ┆ Bulbasaur ┆ Grass  ┆ Poison ┆ 318   ┆ 45  ┆ 49     ┆ 49      ┆ 65     ┆ 65     ┆ 45    ┆ 1          ┆ false     │
    # │ 2   ┆ Ivysaur   ┆ Grass  ┆ Poison ┆ 405   ┆ 60  ┆ 62     ┆ 63      ┆ 80     ┆ 80     ┆ 60    ┆ 1          ┆ false     │
    # └─────┴───────────┴────────┴────────┴───────┴─────┴────────┴─────────┴────────┴────────┴───────┴────────────┴───────────┘
