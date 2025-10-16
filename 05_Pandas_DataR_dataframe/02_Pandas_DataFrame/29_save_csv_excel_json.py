'''
1. df.to_csv('file_name.csv')  # Save DataFrame to CSV file
2. df.to_excel('file_name.xlsx')  # Save DataFrame to Excel file
3. df.to_json('file_name.json')  # Save DataFrame to JSON file
'''

import pandas as pd
import numpy as np

df = pd.DataFrame(
    {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, np.nan],
        'City': ['New York', 'Paris', 'Berlin', 'Tokyo'],
        'Salary': [50000.75, 60000.50, 75000.25, 90000.00],
        'Date': pd.date_range('2023-01-01', periods=4, freq='M')
    }
)

print(df)
#       Name   Age      City    Salary       Date
# 0    Alice  25.0  New York  50000.75 2023-01-31
# 1      Bob  30.0     Paris  60000.50 2023-02-28
# 2  Charlie  35.0    Berlin  75000.25 2023-03-31
# 3    David   NaN     Tokyo  90000.00 2023-04-30


#-----------------------------------------------------------------------------------------------------------#
#-------------------------------------- 1. df.to_csv('file_name.csv') --------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

df.to_csv(
    path_or_buf = '05_Pandas_DataR_dataframe/save/df_to.csv',
    sep = ',',      # Column separator
    index = False, # Do not write row indices
    na_rep = 'NaN'  # Represent NaN values as 'NaN' in the CSV file
)


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------ 2. df.to_excel('file_name.xlsx') -------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

df.to_excel(
    excel_writer = '05_Pandas_DataR_dataframe/save/df_to.xlsx',
    sheet_name = 'Sheet1',  # Name of the sheet in the Excel file
    index = False,         # Do not write row indices
    na_rep = np.nan         # Represent NaN values as np.nan (empty) in the Excel file
)


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------- 3. df.to_json('file_name.json') -------------------------------------#
#-----------------------------------------------------------------------------------------------------------#

df.to_json(
    path_or_buf = '05_Pandas_DataR_dataframe/save/df_to.json',
    orient = 'records',  # Format of the JSON file,
    indent = 4,
    lines = False,      # Do not write JSON objects line by line
    date_format = 'iso' # Format dates in ISO format
)