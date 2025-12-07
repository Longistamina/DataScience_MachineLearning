'''
Pandas offers many functions to read data from various file formats into DataFrames.

##################################################################

1. pd.read_csv() - Read CSV files
   + Basic Usage: df = pd.read_csv('path/to/file.csv')
   + Specify index_col=: df = pd.read_csv('path/to/file.csv', index_col='column_name'/column_index)
   + Specify usecols=: df = pd.read_csv('path/to/file.csv', usecols=['col1', 'col2']/col_index_list)
   + Specify dtype=: df = pd.read_csv('path/to/file.csv', dtype={'col1': 'str', 'col2': 'float64'})
   + Specify parse_dates=: df = pd.read_csv('path/to/file.csv', parse_dates=['date_col']/True)
   + With header= and names=: df = pd.read_csv('path/to/file.csv', header=0, names=['col1', 'col2'])
   + Read TSV file with sep='\t': df = pd.read_csv('path/to/file.tsv', sep='\t')
   + Handle NA values: df = pd.read_csv('path/to/file.csv', na_values=['?'])
   + Read with skiprows= and nrows=: df = pd.read_csv('path/to/file.csv', skiprows=2, nrows=5)
   + Read with skipfooter=: df = pd.read_csv('path/to/file.csv', skipfooter=2, engine='python')

2. pd.read_excel() - Read Excel files
   + Installation: conda install -c conda-forge openpyxl / pip3 install openpyxl
   + Basic Usage: df = pd.read_excel('path/to/file.xlsx')
   + Specify sheet_name=: df = pd.read_excel('path/to/file.xlsx', sheet_name='Sheet_Name'/Sheet_Index)

3. pd.read_json() - Read JSON files
   + Basic Usage: df = pd.read_json('path/to/file.json')
   + Normalize json object/dataframe: df = pd.json_normalize(data=json_obj, record_path=['path', 'to', 'list'])

4. pd.read_xml() - Read XML files
   + Installation: conda install -c conda-forge lxml / pip3 install lxml
'''

import pandas as pd

#---------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. pd.read_csv() ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

'''
read_csv() is the most commonly used pandas I/O function, designed to read CSV files into DataFrames. 
It supports over 50 parameters for comprehensive data control.

Detailed documentation: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv

File parameters:
+ filepath_or_buffer: Accepts file paths, URLs, or file-like objects
+ sep/delimiter: Field separator (default: ',')
+ encoding: Text encoding (utf-8, latin-1, etc.)
+ compression: Automatic detection ('infer') or specific formats ('gzip', 'bz2', 'zip')
+ skiprows: Number of rows to skip at the start
+ skipfooter: Number of rows to skip at the end
+ nrows: Number of rows to read

Data Structure Control parameters:
+ header: Row number(s) for column names ('infer', int, list, None)
+ names: Custom column names list
+ index_col: Column(s) to use as row labels
+ usecols: Subset of columns to return

NA values handling:
+ na_values: Additional strings to recognize as NA/NaN
+ keep_default_na: Whether to include default NA values
+ na_filter: Detect missing values (default: True)

Data Type Management
+ dtype: Specify data types for columns
+ converters: Custom functions for value conversion
+ parse_dates: Parse date columns automatically
'''

#################
## Basic Usage ##
#################

df = pd.read_csv('05_Pandas_DataR_dataframe/data/emp.csv')

print(df)
#    id      name  salary  start_date        dept
# 0   1      Rick  623.30  2012-01-01          IT
# 1   2       Dan  515.20  2013-09-23  Operations
# 2   3  Michelle  611.00  2014-11-15          IT
# 3   4      Ryan  729.00  2014-05-11          HR
# 4   5      Gary  843.25  2015-03-27     Finance
# 5   6      Nina  578.00  2013-05-21          IT
# 6   7     Simon  632.80  2013-07-30  Operations
# 7   8      Guru  722.50  2014-06-17     Finance

########################
## Specify index_col= ##
########################

df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp.csv', 
    index_col='id'
)

print(df)
#         name  salary  start_date        dept
# id                                          
# 1       Rick  623.30  2012-01-01          IT
# 2        Dan  515.20  2013-09-23  Operations
# 3   Michelle  611.00  2014-11-15          IT
# 4       Ryan  729.00  2014-05-11          HR
# 5       Gary  843.25  2015-03-27     Finance
# 6       Nina  578.00  2013-05-21          IT
# 7      Simon  632.80  2013-07-30  Operations
# 8       Guru  722.50  2014-06-17     Finance
'''Now the 'id' column is set as the DataFrame index.'''

######################
## Specify usecols= ##
######################

df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp.csv', 
    usecols=['name', 'salary', 'dept']
)

print(df)
#        name  salary        dept
# 0      Rick  623.30          IT
# 1       Dan  515.20  Operations
# 2  Michelle  611.00          IT
# 3      Ryan  729.00          HR
# 4      Gary  843.25     Finance
# 5      Nina  578.00          IT
# 6     Simon  632.80  Operations
# 7      Guru  722.50     Finance

#-------

df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp.csv', 
    usecols=[1, 2, 4]
)

print(df)
#        name  salary        dept
# 0      Rick  623.30          IT
# 1       Dan  515.20  Operations
# 2  Michelle  611.00          IT
# 3      Ryan  729.00          HR
# 4      Gary  843.25     Finance
# 5      Nina  578.00          IT
# 6     Simon  632.80  Operations
# 7      Guru  722.50     Finance

####################
## Specify dtype= ##
####################

df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp.csv', 
    usecols=['name', 'salary', 'dept', 'start_date'],
    dtype={
        'name': 'str', # If set as 'string', it will be "string[python]", not "object"
        'salary': 'float64',
        'dept': 'category'
    }
)

print(df.dtypes)
# name            object
# salary         float64
# start_date      object
# dept          category
# dtype: object

##########################
## Specify parse_dates= ##
##########################

#-----------
## parse_dates = ['col1', 'col2'] or 'col1'
#-----------

df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp.csv', 
    dtype={
        'name': 'str', # If set as 'string', it will be "string[python]", not "object"
        'salary': 'float64',
        'dept': 'category'
    },
    parse_dates=["start_date"]
)

print(df.dtypes)
# id                     int64
# name                  object
# salary               float64
# start_date    datetime64[ns]
# dept                category
# dtype: object

#-----------
## parse_dates=True with index_col="date_col"
#-----------

df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp.csv', 
    dtype={
        'name': 'str', # If set as 'string', it will be "string[python]", not "object"
        'salary': 'float64',
        'dept': 'category'
    },
    index_col="start_date",
    parse_dates=True
)

print(df)
#             id      name  salary        dept
# start_date                                  
# 2012-01-01   1      Rick  623.30          IT
# 2013-09-23   2       Dan  515.20  Operations
# 2014-11-15   3  Michelle  611.00          IT
# 2014-05-11   4      Ryan  729.00          HR
# 2015-03-27   5      Gary  843.25     Finance
# 2013-05-21   6      Nina  578.00          IT
# 2013-07-30   7     Simon  632.80  Operations
# 2014-06-17   8      Guru  722.50     Finance
'''The 'start_date' column is now the index and parsed as datetime.'''

#############################
## With header= and names= ##
#############################
'''
This is useful when the CSV file lacks a header row.
Or when you want to override the existing header.

If the original CSV does not have a header row, set "header=None".
'''

df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp.csv', 
    header=0, # The first row (0-indexed) is the header
    names=["ID", "NAME", "SALARY", "START_DATE", "DEPT"] # Custom column names
)

print(df)
#    ID      NAME  SALARY  START_DATE        DEPT
# 0   1      Rick  623.30  2012-01-01          IT
# 1   2       Dan  515.20  2013-09-23  Operations
# 2   3  Michelle  611.00  2014-11-15          IT
# 3   4      Ryan  729.00  2014-05-11          HR
# 4   5      Gary  843.25  2015-03-27     Finance
# 5   6      Nina  578.00  2013-05-21          IT
# 6   7     Simon  632.80  2013-07-30  Operations
# 7   8      Guru  722.50  2014-06-17     Finance

#################################
## Read TSV file with sep='\t' ##
#################################

df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp.tsv', 
    sep='\t' # Tab-separated values
)

print(df)
#   Unnamed: 0      name  salary  start_date        dept
# 0          1      Rick  623.30  2012-01-01          IT
# 1          2       Dan  515.20  2013-09-23  Operations
# 2          3  Michelle  611.00  2014-11-15          IT
# 3          4      Ryan  729.00  2014-05-11          HR
# 4          ?      Gary  843.25  2015-03-27     Finance
# 5          6      Nina  578.00  2013-05-21          IT
# 6          7     Simon  632.80  2013-07-30  Operations
# 7          8      Guru  722.50  2014-06-17     Finance

#-------

df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp.tsv', 
    sep='\t', # Tab-separated values
    index_col=0 # Set the first column as index
)

print(df)
#        name  salary  start_date        dept
# 1      Rick  623.30  2012-01-01          IT
# 2       Dan  515.20  2013-09-23  Operations
# 3  Michelle  611.00  2014-11-15          IT
# 4      Ryan  729.00  2014-05-11          HR
# ?      Gary  843.25  2015-03-27     Finance
# 6      Nina  578.00  2013-05-21          IT
# 7     Simon  632.80  2013-07-30  Operations
# 8      Guru  722.50  2014-06-17     Finance

#######################
## Handle NA values  ##
#######################
'''
By default the following values are interpreted as NaN: 

“ “, “#N/A”, “#N/A N/A”, “#NA”, “-1.#IND”, “-1.#QNAN”, 
“-NaN”, “-nan”, “1.#IND”, “1.#QNAN”, “<NA>”, “N/A”, 
“NA”, “NULL”, “NaN”, “None”, “n/a”, “nan”, “null “.
'''

df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp.tsv', 
    sep='\t', # Tab-separated values
    na_values=['?'], # Additional strings to recognize as NA/NaN
    index_col=0 # Set the first column as index
)

print(df)
#          name  salary  start_date        dept
# 1.0      Rick  623.30  2012-01-01          IT
# 2.0       Dan  515.20  2013-09-23  Operations
# 3.0  Michelle  611.00  2014-11-15          IT
# 4.0      Ryan  729.00  2014-05-11          HR
# NaN      Gary  843.25  2015-03-27     Finance
# 6.0      Nina  578.00  2013-05-21          IT
# 7.0     Simon  632.80  2013-07-30  Operations
# 8.0      Guru  722.50  2014-06-17     Finance
'''The '?' in the index column is now treated as NaN.'''

####################################
## Read with skiprows= and nrows= ##
####################################

# No skip the rows
df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp_skiprows.tsv',
    sep='\t', # Tab-separated values
)
'''pandas.errors.ParserError: Error tokenizing data. C error: Expected 1 fields in line 3, saw 5'''

#-------

# Skip the first 2 corrupted rows
df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp_skiprows.tsv',
    sep='\t', # Tab-separated values
    skiprows=2 # Skip the first 2 rows
)

print(df)
#   Unnamed: 0      name  salary  start_date        dept
# 0          1      Rick  623.30  2012-01-01          IT
# 1          2       Dan  515.20  2013-09-23  Operations
# 2          3  Michelle  611.00  2014-11-15          IT
# 3          4      Ryan  729.00  2014-05-11          HR
# 4                 Gary  843.25  2015-03-27     Finance
# 5          6      Nina  578.00  2013-05-21          IT
# 6          7     Simon  632.80  2013-07-30  Operations
# 7          8      Guru  722.50  2014-06-17     Finance

#-------

# skiprows= and nrows=
df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp_skiprows.tsv',
    sep='\t', # Tab-separated values
    skiprows=2, # Skip the first 2 rows
    nrows=4, # Read only 4 rows
    index_col=0 # Set the first column as index
)

print(df)
#        name  salary  start_date        dept
# 1      Rick   623.3  2012-01-01          IT
# 2       Dan   515.2  2013-09-23  Operations
# 3  Michelle   611.0  2014-11-15          IT
# 4      Ryan   729.0  2014-05-11          HR

###########################
## Read with skipfooter= ##
###########################

# No skip the footer
df = pd.read_csv(
    filepath_or_buffer = '05_Pandas_DataR_dataframe/data/emp_skipfooter.csv'
)

print(df)
#                    id      name  salary  start_date        dept
# 0                   1      Rick  623.30  2012-01-01          IT
# 1                   2       Dan  515.20  2013-09-23  Operations
# 2                   3  Michelle  611.00  2014-11-15          IT
# 3                   4      Ryan  729.00  2014-05-11          HR
# 4                          Gary  843.25  2015-03-27     Finance
# 5                   6      Nina  578.00  2013-05-21          IT
# 6                   7     Simon  632.80  2013-07-30  Operations
# 7                   8      Guru  722.50  2014-06-17     Finance
# 8  # Footer to skip 1       NaN     NaN         NaN         NaN
# 9  # Footer to skip 2       NaN     NaN         NaN         NaN

#-------

# Skip the last 2 footer rows
df = pd.read_csv(
    filepath_or_buffer='05_Pandas_DataR_dataframe/data/emp_skipfooter.csv',
    skipfooter=2, # Skip the last 2 rows
    engine='python', # 'python' engine is required when using skipfooter
    na_values=[" "],
    index_col=0 # Set the first column as index
)

print(df)
#          name  salary  start_date        dept
# id                                           
# 1.0      Rick  623.30  2012-01-01          IT
# 2.0       Dan  515.20  2013-09-23  Operations
# 3.0  Michelle  611.00  2014-11-15          IT
# 4.0      Ryan  729.00  2014-05-11          HR
# NaN      Gary  843.25  2015-03-27     Finance
# 6.0      Nina  578.00  2013-05-21          IT
# 7.0     Simon  632.80  2013-07-30  Operations
# 8.0      Guru  722.50  2014-06-17     Finance


#---------------------------------------------------------------------------------------------------------#
#----------------------------------------- 2. pd.read_excel() --------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

'''
read_excel() handles Microsoft Excel files (.xlsx, .xls, .xlsb) 
with support for multiple sheets and complex formatting.

Detailed documentation: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html#pandas.read_excel

Key Parameters:
+ io: File path or file-like object
+ sheet_name: Sheet selection (int, str, list, or None for all)
+ engine: Parser engine ('openpyxl', 'calamine', 'odf', 'pyxlsb')

Also supports many parameters similar to read_csv() for data control like:
+ header
+ names
+ index_col
+ usecols
+ dtype
+ na_values
'''

# conda install -c conda-forge openpyxl
# pip3 install openpyxl

#################
## Basic Usage ##
#################

df = pd.read_excel("05_Pandas_DataR_dataframe/data/emp_sheetname.xlsx")

print(df)
#   id      name  salary start_date        dept
# 0  1      Rick  623.30 2012-01-01          IT
# 1  2       Dan  515.20 2013-09-23  Operations
# 2  3  Michelle  611.00 2014-11-15          IT
# 3  4      Ryan  729.00 2014-05-11          HR
# 4         Gary  843.25 2015-03-27     Finance
# 5  6      Nina  578.00 2013-05-21          IT
# 6  7     Simon  632.80 2013-07-30  Operations
# 7  8      Guru  722.50 2014-06-17     Finance

'''By default, it reads the first sheet (indexed 0 or specific name).'''

#########################
## Specify sheet_name= ##
#########################

df = pd.read_excel(
    io="05_Pandas_DataR_dataframe/data/emp_sheetname.xlsx", 
    sheet_name='city' # Specify the sheet name
)

print(df)
#        name     city
# 0      Rick  Seattle
# 1       Dan    Tampa
# 2  Michelle  Chicago
# 3      Ryan  Seattle
# 4      Gary  Houston
# 5      Nina   Boston
# 6     Simon   Mumbai
# 7      Guru   Dallas

#-------

df = pd.read_excel(
    io="05_Pandas_DataR_dataframe/data/emp_sheetname.xlsx", 
    sheet_name=1 # Specify the sheet index (1 means the second sheet)
)

print(df)
#        name     city
# 0      Rick  Seattle
# 1       Dan    Tampa
# 2  Michelle  Chicago
# 3      Ryan  Seattle
# 4      Gary  Houston
# 5      Nina   Boston
# 6     Simon   Mumbai
# 7      Guru   Dallas


#---------------------------------------------------------------------------------------------------------#
#----------------------------------------- 3. pd.read_json() ---------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

'''
read_json() supports multiple JSON orientations and structures, 
making it versatile for API data and nested records.

Detailed documentation: https://pandas.pydata.org/docs/reference/api/pandas.read_json.html#pandas.read_json

"orient" Parameter Options:
+ "records": List of dictionaries format
+ "index": Dictionary with row indices as keys
+ "split": Dictionary with separate index, columns, and data
+ "columns": Dictionary with column names as keys
+ "values": Array of arrays format
'''

#################
## Basic Usage ##
#################

'''
{ 
   "ID":["1","2","3","4","5","6","7","8" ],
   "Name":["Rick","Dan","Michelle","Ryan","Gary","Nina","Simon","Guru" ],
   "Salary":["623.3","515.2","611","729","843.25","578","632.8","722.5" ],
   
   "StartDate":[ "1/1/2012","9/23/2013","11/15/2014","5/11/2014","3/27/2015","5/21/2013",
      "7/30/2013","6/17/2014"],
   "Dept":[ "IT","Operations","IT","HR","Finance","IT","Operations","Finance"]
}
'''

df = pd.read_json("05_Pandas_DataR_dataframe/data/emps.json")

print(df)
#    ID      Name  Salary   StartDate        Dept
# 0   1      Rick  623.30    1/1/2012          IT
# 1   2       Dan  515.20   9/23/2013  Operations
# 2   3  Michelle  611.00  11/15/2014          IT
# 3   4      Ryan  729.00   5/11/2014          HR
# 4   5      Gary  843.25   3/27/2015     Finance
# 5   6      Nina  578.00   5/21/2013          IT
# 6   7     Simon  632.80   7/30/2013  Operations
# 7   8      Guru  722.50   6/17/2014     Finance

#####################################
## Normalize json object/dataframe ##
#####################################

df_corrupted = pd.read_json(
    path_or_buf="05_Pandas_DataR_dataframe/data/books.json",
)

print(df_corrupted)
#                                             Mathematics
# book  [{'title': 'Applied Linear Statistical Models'...

'''Let's normalize this nested JSON into a flat table.'''

df_processed = pd.json_normalize(df_corrupted['Mathematics']['book'])

print(df_processed)
#                                                title  ...                                attribute
# 0                  Applied Linear Statistical Models  ...  [Exercises, Illustrations, Readability]
# 1  Mathematical Proofs: A Transition to Advanced ...  ...                 [Exercises, Readability]
# 2      Mathematical Statistics with Resampling and R  ...  [Exercises, Illustrations, Readability]
# [3 rows x 6 columns]

'''Other way'''

import json

with open("05_Pandas_DataR_dataframe/data/books.json", "r", encoding="utf-8") as f:
    json_obj = json.load(f)        # json_obj is a dict, not a DataFrame [1]

df_processed = pd.json_normalize(
    data=json_obj, 
    record_path=["Mathematics", "book"]   # list of dicts to rows [10]
)

print(df_processed)
#                                                title  ...                                attribute
# 0                  Applied Linear Statistical Models  ...  [Exercises, Illustrations, Readability]
# 1  Mathematical Proofs: A Transition to Advanced ...  ...                 [Exercises, Readability]
# 2      Mathematical Statistics with Resampling and R  ...  [Exercises, Illustrations, Readability]
# [3 rows x 6 columns]


#---------------------------------------------------------------------------------------------------------#
#----------------------------------------- 4. pd.read_xml() ----------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

'''
read_xml() handles XML documents with XPath expressions and namespace support.

Core Parameters
+ xpath: XPath expression for node selection (default: './*')
+ namespaces: Namespace dictionary for complex XML
+ parser: XML parser ('lxml', 'etree')
+ attrs_only/elems_only: Parse only attributes or elements
'''

# conda install -c conda-forge lxml
# pip3 install lxml

###############
## Example 1 ##
###############

df_cd = pd.read_xml("05_Pandas_DataR_dataframe/data/cd.xml")

print(df_cd)
#                        TITLE             ARTIST COUNTRY         COMPANY  PRICE  YEAR
# 0           Empire Burlesque          Bob Dylan     USA        Columbia   10.9  1985
# 1            Hide your heart       Bonnie Tyler      UK     CBS Records    9.9  1988
# 2              Greatest Hits       Dolly Parton     USA             RCA    9.9  1982
# 3        Still got the blues         Gary Moore      UK  Virgin records   10.2  1990
# 4                       Eros    Eros Ramazzotti      EU             BMG    9.9  1997
# 5             One night only           Bee Gees      UK         Polydor   10.9  1998
# 6             Sylvias Mother            Dr.Hook      UK             CBS    8.1  1973
# 7                 Maggie May        Rod Stewart      UK        Pickwick    8.5  1990
# 8                    Romanza     Andrea Bocelli      EU         Polydor   10.8  1996
# 9   When a man loves a woman       Percy Sledge     USA        Atlantic    8.7  1987

###############
## Example 2 ##
###############

df_food = pd.read_xml("05_Pandas_DataR_dataframe/data/food.xml")

print(df_food)
#                           name  price                                        description  calories
# 0              Belgian Waffles  $5.95  Two of our famous Belgian Waffles with plenty ...       650
# 1   Strawberry Belgian Waffles  $7.95  Light Belgian waffles covered with strawberrie...       900
# 2  Berry-Berry Belgian Waffles  $8.95  Light Belgian waffles covered with an assortme...       900
# 3                 French Toast  $4.50  Thick slices made from our homemade sourdough ...       600
# 4          Homestyle Breakfast  $6.95  Two eggs, bacon or sausage, toast, and our eve...       950