"""
There are many ways to change the column names of the frame.

About row names, frames from polars and tidypyrs don't have index system.
Therefore, if we want to create row names, we need to treat them as a column of the frames.

1. Change Column names:
    + tf.as_polars().columns = new_names
    + tl.set_names(new_names)
    + tl.rename({...})
    + tl.select(f(old).alias(new) for old, new in pairs)
    + tl.rename(dict(zip(old_names, new_names)))
    + tl.rename(mapping, strict=False)
    + tl.rename(function)
    + tl.rename(lambda x: ...)
    + tl.select(f.all().name.replace(...))
    + tl.select(f.all().name.map(function))
    + tl.select(f.all().name.prefix('pre_'))
    + tl.select(f.all().name.suffix('_suf'))
    + Example: clean Pokemon dataframe column names (lazyframe implementation)

2. Change Row names:
    + tl.row_index(name='row_id', offset=0)
    + Create row index with `row_index` then modify it
"""

import re
from pathlib import Path

import polars as pl
import tidypyrs as tp
from tidypyrs import f

pl.Config(tbl_width_chars=120)
data_dir = next(Path("/home").glob("**/DataScience*/data"))

# ==============================================================================
# 1. Change column names
# ==============================================================================

tf_lifexp = tp.read_csv(data_dir/"life_expectancy.csv", schema_overrides={"Population":pl.Float64})
tl_lifexp = tf_lifexp.lazy()

print(tf_lifexp.glimpse(max_items_per_column=5, return_type="string"))
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

##------------------------------------##
## tf.as_polars().columns = new_names ##
##------------------------------------##
'''
To use this assignment method, must convert to polars first.
`tf.as_polars().columns = new_names`

NOTE: this method only works with TibbleFrame

Important:
    + The new list must have exactly the same length as the number of columns.
    + This mutates that TibbleFrame object.
    + Use tf.clone() first if you do not want to change your original variable.
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

tf_new = tf_lifexp.clone()

tf_new.as_polars().columns = new_colnames

print(tf_new.head(2))
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

print(tf_new.colnames[:6])
# shape: (6,)
# Series: '' [str]
# [
# 	"country"
# 	"year"
# 	"status"
# 	"life_expectancy"
# 	"adult_mortality"
# 	"infant_deaths"
# ]

##-------------------------##
## tl.set_names(new_names) ##
##-------------------------##

print(
    tl_lifexp
    .set_names(new_colnames)
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

##------------------##
## tl.rename({...}) ##
##------------------##

print(
    tl_lifexp
    .rename({
        " thinness  1-19 years": "thinness_1_19_years",
        "Adult Mortality": "adult_mortality"
    })
    .select(f("thinness_1_19_years", "adult_mortality"))
    .head(2)
    .collect()
)
# shape: (2, 2)
# ┌─────────────────────┬─────────────────┐
# │ thinness_1_19_years ┆ adult_mortality │
# │ ---                 ┆ ---             │
# │ f64                 ┆ i64             │
# ╞═════════════════════╪═════════════════╡
# │ 17.2                ┆ 263             │
# │ 17.5                ┆ 271             │
# └─────────────────────┴─────────────────┘

##--------------------------------------------##
## tl.rename(dict(zip(old_names, new_names))) ##
##--------------------------------------------##

print(
    tl_lifexp
    .rename(dict(zip(tl_lifexp.colnames, new_colnames)))
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
## tl.rename(mapping, strict=False) ##
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
    tl_lifexp
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

##----------------------------------------------------##
## tl.select(f(old).alias(new) for old, new in pairs) ##
##----------------------------------------------------##
'''
.alias() is the expression-level way to name outputs.
It is useful when you are selecting a subset of columns and renaming them at the same time.
'''

print(
    tl_lifexp
    .select(
        f("Country").alias("country"),
        f("Year").alias("year"),
        f("Life expectancy ").alias("life_expectancy"),
        f("Adult Mortality").alias("adult_mortality"),
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


##---------------------##
## tl.rename(function) ##
##---------------------##

def clean_column_name(column_name: str) -> str:
    """Convert messy column names to snake_case."""
    column_name = column_name.strip().lower()
    column_name = re.sub(r"\s+", "_", column_name)
    column_name = column_name.replace("-", "_").replace("/", "_")
    return column_name

print(
    tl_lifexp
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
## tl.rename(lambda x: ...) ##
##--------------------------##

print(
    tl_lifexp
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

##--------------------------------------##
## tl.select(f.all().name.replace(...)) ##
##--------------------------------------##
'''NO NEED `import re` !!!'''

print(
    tl_lifexp
    .select(
        f.all()
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

##---------------------------------------##
## tl.select(f.all().name.map(function)) ##
##---------------------------------------##
'''
Expr.name.map applies a Python function to the root column name of an expression.
This is useful for more customized naming inside a select expression.
'''

print(
    tl_lifexp
    .select(f.all().name.map(clean_column_name))
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

##----------------------------------------##
## tl.select(f.all().name.prefix('pre_')) ##
##----------------------------------------##
'''The reversal function is `.strip_prefix()`'''

tl_emp = tp.scan_csv(data_dir/"emp.csv")
print(tl_emp.head(2).collect())
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
    tl_emp
    .select(f.all().name.prefix('pre_'))
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

##----------------------------------------##
## tl.select(f.all().name.suffix('_suf')) ##
##----------------------------------------##
'''The reversal function is `.strip_suffix()`'''

tl_emp = tp.scan_csv(data_dir/"emp.csv")
print(tl_emp.head(2).collect())
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
    tl_emp
    .select(f.all().name.suffix('_sub'))
    .head(2)
    .collect()
)
# shape: (2, 5)
# ┌────────┬──────────┬────────────┬────────────────┬────────────┐
# │ id_sub ┆ name_sub ┆ salary_sub ┆ start_date_sub ┆ dept_sub   │
# │ ---    ┆ ---      ┆ ---        ┆ ---            ┆ ---        │
# │ i64    ┆ str      ┆ f64        ┆ str            ┆ str        │
# ╞════════╪══════════╪════════════╪════════════════╪════════════╡
# │ 1      ┆ Rick     ┆ 623.3      ┆ 2012-01-01     ┆ IT         │
# │ 2      ┆ Dan      ┆ 515.2      ┆ 2013-09-23     ┆ Operations │
# └────────┴──────────┴────────────┴────────────────┴────────────┘

##--------------------------------------------------------------------------##
## Example: clean Pokemon dataframe column names (lazyframe implementation) ##
##--------------------------------------------------------------------------##

tl_pokemon = tp.scan_csv(data_dir/"pokemon.csv")

with pl.Config(tbl_cols=15, tbl_width_chars=140):
    print(tl_pokemon.head(2).collect())
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
        tl_pokemon
        .select(f.all().name.to_lowercase().name.replace(r"\s+", "_").name.replace(".", "", literal=True))
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

# ==============================================================================
# 2. Change Row Names / Index
# ==============================================================================

tl_emp = tp.scan_csv(data_dir/"emp.csv").drop("id")

print(tl_emp.collect())
# shape: (8, 4)
# ┌──────────┬────────┬────────────┬────────────┐
# │ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ str      ┆ f64    ┆ str        ┆ str        │
# ╞══════════╪════════╪════════════╪════════════╡
# │ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# │ Ryan     ┆ 729.0  ┆ 2014-05-11 ┆ HR         │
# │ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# │ Nina     ┆ 578.0  ┆ 2013-05-21 ┆ IT         │
# │ Simon    ┆ 632.8  ┆ 2013-07-30 ┆ Operations │
# │ Guru     ┆ 722.5  ┆ 2014-06-17 ┆ Finance    │
# └──────────┴────────┴────────────┴────────────┘

##---------------------------------------##
## tl.row_index(name='row_id', offset=0) ##
##---------------------------------------##

print(
    tl_emp
    .row_index()
    .collect()
)
# shape: (8, 5)
# ┌───────┬──────────┬────────┬────────────┬────────────┐
# │ index ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ ---   ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ u32   ┆ str      ┆ f64    ┆ str        ┆ str        │
# ╞═══════╪══════════╪════════╪════════════╪════════════╡
# │ 0     ┆ Rick     ┆ 623.3  ┆ 2012-01-01 ┆ IT         │
# │ 1     ┆ Dan      ┆ 515.2  ┆ 2013-09-23 ┆ Operations │
# │ 2     ┆ Michelle ┆ 611.0  ┆ 2014-11-15 ┆ IT         │
# │ 3     ┆ Ryan     ┆ 729.0  ┆ 2014-05-11 ┆ HR         │
# │ 4     ┆ Gary     ┆ 843.25 ┆ 2015-03-27 ┆ Finance    │
# │ 5     ┆ Nina     ┆ 578.0  ┆ 2013-05-21 ┆ IT         │
# │ 6     ┆ Simon    ┆ 632.8  ┆ 2013-07-30 ┆ Operations │
# │ 7     ┆ Guru     ┆ 722.5  ┆ 2014-06-17 ┆ Finance    │
# └───────┴──────────┴────────┴────────────┴────────────┘

print(
    tl_emp
    .row_index(name="id", offset=1)
    .collect()
)
# shape: (8, 5)
# ┌─────┬──────────┬────────┬────────────┬────────────┐
# │ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ u32 ┆ str      ┆ f64    ┆ str        ┆ str        │
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

##--------------------------------------------------##
## Create row index with `row_index` then modify it ##
##--------------------------------------------------##

tl_pokemon = tp.scan_csv(data_dir/"pokemon.csv")

print(
    tl_pokemon
    .row_index(name="id", offset=1)
    .mutate(
        id = (tp.lit("pkm") + f("id").cast(tp.String).str.zfill(f("id").max().log10().ceil().cast(tp.Int64)))
        # (tp.lit("pkm") + f("id").cast(tp.String).str.zfill(f("id").max().log10().ceil().cast(tp.Int64))).alias("id),
    )
    .collect()
)
# shape: (800, 14)
# ┌────────┬─────┬───────────────────────┬─────────┬───┬─────────┬───────┬────────────┬───────────┐
# │ id     ┆ #   ┆ Name                  ┆ Type 1  ┆ … ┆ Sp. Def ┆ Speed ┆ Generation ┆ Legendary │
# │ ---    ┆ --- ┆ ---                   ┆ ---     ┆   ┆ ---     ┆ ---   ┆ ---        ┆ ---       │
# │ str    ┆ i64 ┆ str                   ┆ str     ┆   ┆ i64     ┆ i64   ┆ i64        ┆ bool      │
# ╞════════╪═════╪═══════════════════════╪═════════╪═══╪═════════╪═══════╪════════════╪═══════════╡
# │ pkm001 ┆ 1   ┆ Bulbasaur             ┆ Grass   ┆ … ┆ 65      ┆ 45    ┆ 1          ┆ false     │
# │ pkm002 ┆ 2   ┆ Ivysaur               ┆ Grass   ┆ … ┆ 80      ┆ 60    ┆ 1          ┆ false     │
# │ pkm003 ┆ 3   ┆ Venusaur              ┆ Grass   ┆ … ┆ 100     ┆ 80    ┆ 1          ┆ false     │
# │ pkm004 ┆ 3   ┆ VenusaurMega Venusaur ┆ Grass   ┆ … ┆ 120     ┆ 80    ┆ 1          ┆ false     │
# │ pkm005 ┆ 4   ┆ Charmander            ┆ Fire    ┆ … ┆ 50      ┆ 65    ┆ 1          ┆ false     │
# │ …      ┆ …   ┆ …                     ┆ …       ┆ … ┆ …       ┆ …     ┆ …          ┆ …         │
# │ pkm796 ┆ 719 ┆ Diancie               ┆ Rock    ┆ … ┆ 150     ┆ 50    ┆ 6          ┆ true      │
# │ pkm797 ┆ 719 ┆ DiancieMega Diancie   ┆ Rock    ┆ … ┆ 110     ┆ 110   ┆ 6          ┆ true      │
# │ pkm798 ┆ 720 ┆ HoopaHoopa Confined   ┆ Psychic ┆ … ┆ 130     ┆ 70    ┆ 6          ┆ true      │
# │ pkm799 ┆ 720 ┆ HoopaHoopa Unbound    ┆ Psychic ┆ … ┆ 130     ┆ 80    ┆ 6          ┆ true      │
# │ pkm800 ┆ 721 ┆ Volcanion             ┆ Fire    ┆ … ┆ 90      ┆ 70    ┆ 6          ┆ true      │
# └────────┴─────┴───────────────────────┴─────────┴───┴─────────┴───────┴────────────┴───────────┘
