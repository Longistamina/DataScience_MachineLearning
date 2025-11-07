'''
1. dr.as_date(): Convert a string or numeric representation of a date into a Date object.

2. Apply Pandas methods or functions

3. Combine with pd.Grouper() for time-based grouping
'''

import datar.all as dr
from datar import f
import pandas as pd

from pipda import register_verb
dr.filter = register_verb(func = dr.filter_)
dr.slice = register_verb(func = dr.slice_)

###############################

tb_aq = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/air_quality_no2_long.csv")
    >> dr.rename(date = f["date.utc"])
)

print(tb_aq >> dr.slice_head(5))
#       city  country                       date location parameter     value     unit
#   <object> <object>                   <object> <object>  <object> <float64> <object>
# 0    Paris       FR  2019-06-21 00:00:00+00:00  FR04014       no2      20.0    µg/m³
# 1    Paris       FR  2019-06-20 23:00:00+00:00  FR04014       no2      21.8    µg/m³
# 2    Paris       FR  2019-06-20 22:00:00+00:00  FR04014       no2      26.5    µg/m³
# 3    Paris       FR  2019-06-20 21:00:00+00:00  FR04014       no2      24.9    µg/m³
# 4    Paris       FR  2019-06-20 20:00:00+00:00  FR04014       no2      21.4    µg/m³


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------- 1. dr.as_date() ----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
'''
Convert strings, numbers, or datetime-like objects to date (no time) format in pandas DataFrames, similar to R's as.Date(). It tries common date formats by default but can be customized.

Arguments:
# x: The object to convert (string, list, number, datetime object, etc.)
# format (optional): A string specifying the exact date format (e.g., "%d-%m-%Y").
# try_formats (optional): List of format strings to try if format is not set. Common defaults include "%Y-%m-%d", "%Y/%m/%d".
# optional (optional): If True, returns np.nan on failure instead of error (default: False).
# tz (optional): Timezone offset or timedelta (names like "UTC" not supported).
# origin (optional): The reference date for numeric input (e.g., days since "1970-01-01").
'''

# format = "%Y-%m-%d" must match the date string format in the "date" column (e.g., "2019-06-21")

print(
    tb_aq
    >> dr.mutate(date = dr.as_date(f.date, format = "%Y-%m-%d %H:%M:%S%z", optional = True))
    >> dr.slice_head(5)
)
#       city  country             date location parameter     value     unit
#   <object> <object> <datetime64[ns]> <object>  <object> <float64> <object>
# 0    Paris       FR       2019-06-21  FR04014       no2      20.0    µg/m³
# 1    Paris       FR       2019-06-20  FR04014       no2      21.8    µg/m³
# 2    Paris       FR       2019-06-20  FR04014       no2      26.5    µg/m³
# 3    Paris       FR       2019-06-20  FR04014       no2      24.9    µg/m³
# 4    Paris       FR       2019-06-20  FR04014       no2      21.4    µg/m³

'''Here, time information is discarded, retaining only the date part.'''


#----------------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 2. Apply Pandas methods or functions ------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

#####################################
## Using .astype('datetime64[ns]') ##
#####################################

print(
    tb_aq
    >> dr.mutate(date = f.date.str.replace("+00:00", "").astype('datetime64[ns]')) # remove timezone info to avoid error
    >> dr.slice_head(5)
)
#       city  country                date location parameter     value     unit
#   <object> <object>    <datetime64[ns]> <object>  <object> <float64> <object>
# 0    Paris       FR 2019-06-21 00:00:00  FR04014       no2      20.0    µg/m³
# 1    Paris       FR 2019-06-20 23:00:00  FR04014       no2      21.8    µg/m³
# 2    Paris       FR 2019-06-20 22:00:00  FR04014       no2      26.5    µg/m³
# 3    Paris       FR 2019-06-20 21:00:00  FR04014       no2      24.9    µg/m³
# 4    Paris       FR 2019-06-20 20:00:00  FR04014       no2      21.4    µg/m³

############################
## Using pd.to_datetime() ##
############################

print(
    tb_aq
    >> dr.mutate(date = dr.pipe(lambda f: pd.to_datetime(f.date, format = "%Y-%m-%d %H:%M:%S%z", errors = 'coerce')))
    >> dr.slice_head(5)
)
#       city  country                      date location parameter     value     unit
#   <object> <object>     <datetime64[ns, UTC]> <object>  <object> <float64> <object>
# 0    Paris       FR 2019-06-21 00:00:00+00:00  FR04014       no2      20.0    µg/m³
# 1    Paris       FR 2019-06-20 23:00:00+00:00  FR04014       no2      21.8    µg/m³
# 2    Paris       FR 2019-06-20 22:00:00+00:00  FR04014       no2      26.5    µg/m³
# 3    Paris       FR 2019-06-20 21:00:00+00:00  FR04014       no2      24.9    µg/m³
# 4    Paris       FR 2019-06-20 20:00:00+00:00  FR04014       no2      21.4    µg/m³


#----------------------------------------------------------------------------------------------------------------------#
#------------------------------- 3. Combine with pd.Grouper() for time-based grouping ---------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

df_aq = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/air_quality_no2_long.csv")
    .rename(columns={"date.utc": "date"})
    .assign(date = lambda df: pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S%z")) # Must be datetime type for pd.Grouper
)

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