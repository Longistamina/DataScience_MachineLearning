import pandas as pd

##################################
## Read the Air Quality dataset ##
##################################

df_aq = (
    pd.read_csv("05_Pandas_DataR_dataframe/data/air_quality_no2_long.csv")
    .rename(columns={"date.utc": "date"})
)

print(df_aq.head())
#     city country                       date location parameter  value   unit
# 0  Paris      FR  2019-06-21 00:00:00+00:00  FR04014       no2   20.0  µg/m³
# 1  Paris      FR  2019-06-20 23:00:00+00:00  FR04014       no2   21.8  µg/m³
# 2  Paris      FR  2019-06-20 22:00:00+00:00  FR04014       no2   26.5  µg/m³
# 3  Paris      FR  2019-06-20 21:00:00+00:00  FR04014       no2   24.9  µg/m³
# 4  Paris      FR  2019-06-20 20:00:00+00:00  FR04014       no2   21.4  µg/m³

print(df_aq.info())
# RangeIndex: 2068 entries, 0 to 2067
# Data columns (total 7 columns):
#  #   Column     Non-Null Count  Dtype  
# ---  ------     --------------  -----  
#  0   city       2068 non-null   object 
#  1   country    2068 non-null   object 
#  2   date       2068 non-null   object 
#  3   location   2068 non-null   object 
#  4   parameter  2068 non-null   object 
#  5   value      2068 non-null   float64
#  6   unit       2068 non-null   object 
# dtypes: float64(1), object(6)

#########################################
## Convert the date column to datetime ##
#########################################

df_aq["date"] = pd.to_datetime(df_aq["date"], format="%Y-%m-%d %H:%M:%S%z")

print(df_aq.dtypes)
# city                      object
# country                   object
# date         datetime64[ns, UTC]
# location                  object
# parameter                 object
# value                    float64
# unit                      object
# dtype: object

###########################################
## df["date"].min() and df["date"].max() ##
###########################################
'''
The df["date"].min() returns the earliest date in the "date" column, 
    df["date"].max() returns the latest date.
'''

print(df_aq["date"].min())  # 2019-05-07 01:00:00+00:00
print(df_aq["date"].max())  # 2019-06-21 00:00:00+00:00

################################################
## Extract some properties of the date column ##
################################################

print(df_aq["date"].dt.month)
# 0       6
# 1       6
# 2       6
# 3       6
# 4       6
#        ..
# 2063    5
# 2064    5
# 2065    5
# 2066    5
# 2067    5
# Name: date, Length: 2068, dtype: int32

print(df_aq["date"].dt.year.unique())  # [2019]

# Create a new column "month" in the DataFrame, using .month property
df_aq["month"] = df_aq["date"].dt.month

print(df_aq.head())
#     city country                      date location parameter  value   unit  month
# 0  Paris      FR 2019-06-21 00:00:00+00:00  FR04014       no2   20.0  µg/m³      6
# 1  Paris      FR 2019-06-20 23:00:00+00:00  FR04014       no2   21.8  µg/m³      6
# 2  Paris      FR 2019-06-20 22:00:00+00:00  FR04014       no2   26.5  µg/m³      6
# 3  Paris      FR 2019-06-20 21:00:00+00:00  FR04014       no2   24.9  µg/m³      6
# 4  Paris      FR 2019-06-20 20:00:00+00:00  FR04014       no2   21.4  µg/m³      6

############################################
## Groupby statistics on time series data ##
############################################

#----------------
## Groupby weekday and location, compute the mean value
#----------------

df_aq_grouped = df_aq.groupby([df_aq["date"].dt.weekday, "location"]).agg({"value": "mean"})

print(df_aq_grouped.head())
#                              value
# date location                     
# 0    BETR801             27.875000
#      FR04014             24.856250
#      London Westminster  23.969697
# 1    BETR801             22.214286
#      FR04014             30.999359

#----------------
## Groupby using pd.Grouper, calculate the mean every 5 days, and by country
#----------------

df_aq_grouped_5d = (
    df_aq.copy()
    .groupby([pd.Grouper(key="date", freq="5D"), "country"]).agg({"value": "mean"})
    .reset_index() # to turn the index back into columns
)

print(df_aq_grouped_5d)
#                         date country      value
# 0  2019-05-07 00:00:00+00:00      BE  24.900000
# 1  2019-05-07 00:00:00+00:00      FR  29.314655
# 2  2019-05-07 00:00:00+00:00      GB  31.800000
# 3  2019-05-12 00:00:00+00:00      BE  18.722222
# 4  2019-05-12 00:00:00+00:00      FR  21.440336
# 5  2019-05-12 00:00:00+00:00      GB  28.983193
# 6  2019-05-17 00:00:00+00:00      BE  24.177083
# 7  2019-05-17 00:00:00+00:00      FR  32.217500
# 8  2019-05-17 00:00:00+00:00      GB  31.966667
# 9  2019-05-22 00:00:00+00:00      BE  47.500000

#####################################################################
## df.rolling(), df.expanding() and df.ewm() on time-serie indexed ##
#####################################################################

df_aq_paris = df_aq.query("city == 'Paris'").set_index("date").sort_index()

print(df_aq_paris.head())
#                             city country location parameter  value   unit  month
# date                                                                            
# 2019-05-07 01:00:00+00:00  Paris      FR  FR04014       no2   25.0  µg/m³      5
# 2019-05-07 02:00:00+00:00  Paris      FR  FR04014       no2   27.7  µg/m³      5
# 2019-05-07 03:00:00+00:00  Paris      FR  FR04014       no2   50.4  µg/m³      5
# 2019-05-07 04:00:00+00:00  Paris      FR  FR04014       no2   61.9  µg/m³      5
# 2019-05-07 05:00:00+00:00  Paris      FR  FR04014       no2   72.4  µg/m³      5

#----------------
## df.rolling()
#----------------

print(df_aq_paris["value"].rolling(window='2h').mean())
# 2019-05-07 01:00:00+00:00    25.00
# 2019-05-07 02:00:00+00:00    26.35
# 2019-05-07 03:00:00+00:00    39.05
# 2019-05-07 04:00:00+00:00    56.15
# 2019-05-07 05:00:00+00:00    67.15

print(df_aq_paris["value"].rolling(window='3h').mean())
# date
# 2019-05-07 01:00:00+00:00    25.000000 
# 2019-05-07 02:00:00+00:00    26.350000
# 2019-05-07 03:00:00+00:00    34.366667
# 2019-05-07 04:00:00+00:00    46.666667
# 2019-05-07 05:00:00+00:00    61.566667

'''Must have datetime-based index for time-based rolling windows like "2h", "3D", etc.'''

#----------------
## df.expanding()
#----------------

print(df_aq_paris["value"].expanding(min_periods=2).mean())
# 2019-05-07 01:00:00+00:00          NaN
# 2019-05-07 02:00:00+00:00    26.350000
# 2019-05-07 03:00:00+00:00    34.366667
# 2019-05-07 04:00:00+00:00    41.250000
# 2019-05-07 05:00:00+00:00    47.480000

print(df_aq_paris["value"].expanding(min_periods=5).mean())
# 2019-05-07 01:00:00+00:00          NaN
# 2019-05-07 02:00:00+00:00          NaN
# 2019-05-07 03:00:00+00:00          NaN
# 2019-05-07 04:00:00+00:00          NaN
# 2019-05-07 05:00:00+00:00    47.480000
#                                ...    
# 2019-06-20 20:00:00+00:00    27.758300
# 2019-06-20 21:00:00+00:00    27.755445

#----------------
## df.ewm()
#----------------

print(df_aq_paris["value"].ewm(span=2, adjust=False).mean())
# 2019-05-07 01:00:00+00:00    25.000000
# 2019-05-07 02:00:00+00:00    26.800000
# 2019-05-07 03:00:00+00:00    42.533333
# 2019-05-07 04:00:00+00:00    55.444444
# 2019-05-07 05:00:00+00:00    66.748148
