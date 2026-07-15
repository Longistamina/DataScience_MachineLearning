'''
Sometime, the dataframe workflow results in a single-column dataframe, like this:


Though it has only one column, its type is still polars.DataFrame, not polars.Series.
So if you mistake a single-column dataframe with a series, and you try to use series method,
it could lead to errors.

This script shows some cases when it:
   + results in a single-column dataframe,
   + or results in a series

Then shows how to convert a 2D single-column dataframe into a 1D series

#######################################

1. Single-column DataFrame (2D) vs Series (1D)
2. Convert single-column DataFrame to a Series
'''

from pathlib import Path

import polars as pl
from polars import col as c

data_dir = next(Path("/home").rglob("*/DataScience_MachineLearning/data"))

df_emp = pl.read_csv(
    data_dir / "emp.csv",
    try_parse_dates=True,
)

print(df_emp)
# shape: (8, 5)
# ┌─────┬──────────┬────────┬────────────┬────────────┐
# │ id  ┆ name     ┆ salary ┆ start_date ┆ dept       │
# │ --- ┆ ---      ┆ ---    ┆ ---        ┆ ---        │
# │ i64 ┆ str      ┆ f64    ┆ date       ┆ str        │
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


#--------------------------------------------------------------------------------------------------------------#
#------------------------------- 1. Single-column DataFrame (2D) vs Series (1D) -------------------------------#
#--------------------------------------------------------------------------------------------------------------#

##################################
## Single-column DataFrame (2D) ##
##################################
'''
df_emp.select("name") returns a DataFrame with one column.

Can work with lazyframe
'''

df_name = df_emp.select("name")
print(df_name)
# shape: (8, 1)
# ┌──────────┐
# │ name     │
# │ ---      │
# │ str      │
# ╞══════════╡
# │ Rick     │
# │ Dan      │
# │ Michelle │
# │ Ryan     │
# │ Gary     │
# │ Nina     │
# │ Simon    │
# │ Guru     │
# └──────────┘

print(len(df_name.shape))
# 2

#################
## Series (1D) ##
#################
'''
df["col_name"] and df.get_column("col_name") returns a 1D Series

NOTE: but they only work for EAGER DATAFRAME, not lazyframe
'''

s_name = df_emp["name"]
print(s_name)
# shape: (8,)
# Series: 'name' [str]
# [
# 	"Rick"
# 	"Dan"
# 	"Michelle"
# 	"Ryan"
# 	"Gary"
# 	"Nina"
# 	"Simon"
# 	"Guru"
# ]
'''NOTE: only works with eager dataframe, not lazyframe'''

s_name = df_emp.get_column("name")
print(s_name)
# shape: (8,)
# Series: 'name' [str]
# [
# 	"Rick"
# 	"Dan"
# 	"Michelle"
# 	"Ryan"
# 	"Gary"
# 	"Nina"
# 	"Simon"
# 	"Guru"
# ]
'''NOTE: only works with eager dataframe, not lazyframe'''


#---------------------------------------------------------------------------------------------------------#
#----------------------------- 2. Convert single-column DataFrame to a Series ----------------------------#
#---------------------------------------------------------------------------------------------------------#
'''
So, df.select("single_col_name") works with both eager and lazy dataframe,
but it results in a 2D single-column dataframe, how could we convert it to a series?

Unfortunately, polars does not support converting a single-column lazyframe into a series
(because there is no equivalent class like ``LazySeries`` for it to convert to).

So, for a single-column lazyframe, we have to ``collect()`` it first, then ``to_series()``

Or, we can ``collect()`` a multiple-columns lazyframe first, then use ``get_column()`` or subscript ``df["col_name"]``
to get that column as a 1D series
'''

lf_emp = df_emp.lazy()

s_name = (
    lf_emp
    .select("name")
    .collect()
    .to_series()
)
print(s_name)
# shape: (8,)
# Series: 'name' [str]
# [
# 	"Rick"
# 	"Dan"
# 	"Michelle"
# 	"Ryan"
# 	"Gary"
# 	"Nina"
# 	"Simon"
# 	"Guru"
# ]

s_dept = (
    lf_emp
    .collect()
    .get_column("dept")
)
print(s_dept)
# shape: (8,)
# Series: 'dept' [str]
# [
# 	"IT"
# 	"Operations"
# 	"IT"
# 	"HR"
# 	"Finance"
# 	"IT"
# 	"Operations"
# 	"Finance"
# ]
