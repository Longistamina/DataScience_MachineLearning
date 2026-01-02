'''
CSV (Comma-Separated Values) files are plain text files that store tabular data 
using specific delimiters to separate values and newlines to indicate new rows. 

Each line represents a row of data, with values typically separated by commas, 
though other delimiters like semicolons, tabs, or pipes can be used. 

The first row often contains column headers, making the data structure self-documenting

#############################

csv delimiter: ","
tsv delimiter: "\t"

others: ';' or '|'

these are called "dialect"

##############################

Python offers "csv" built-in module for working with comma-separated values files (and also other dialects), 
providing robust functionality for reading, writing, and manipulating tabular data.

Another package is Pandas also very powerful for handling .csv file, but we will deal with it later

##############################

Table of Contents:
1. Read .csv and .tsv files
2. Write .csv and .tsv files
3. "quoting" parameter in csv.writer
'''


#-------------------------------------------------------------------------------#
#----------------------- Read .csv and .tsv files ------------------------------#
#-------------------------------------------------------------------------------#

parent_dir = "/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/csv_tsv_files"

import csv

##############################
## Read a classic .csv file ##
##############################

with open(file=f"{parent_dir}/drinks.csv", mode="r", newline="", encoding="utf-8") as file_pointer:
    # newline = "" parameter is crucial to prevent issues with line endings across different operating systems
    # encoding = "utf-8" means interpret the file using the utf8 encoding
    csv_read_object = csv.reader(file_pointer)

    print(csv_read_object) # <_csv.reader object at 0x7f91d9449000>
                           # It returns a reader object, not the actual data or conent of the .csv file

    # To access the data, we need to iterate over the reader object
    for row in csv_read_object:
        print(row)  # Each row is a list of values from the .csv file

        # ['', 'country', 'beer_servings', 'spirit_servings', 'wine_servings', 'total_litres_of_pure_alcohol', 'continent']
        # ['0', 'Afghanistan', '0', '0', '0', '0.0', 'AS']
        # ['1', 'Albania', '89', '132', '54', '4.9', 'EU']
        # ['2', 'Algeria', '25', '0', '14', '0.7', 'AF']
        # ['3', 'Andorra', '245', '138', '312', '12.4', 'EU']

# The first row of a .csv file is often the header row, which contains the names of the columns.

'''
NOTE: everything must be indented inside the "with" block, otherwise it will not work
      because outside the "with" block, the file is already closed, and hence the reader object is no longer valid
'''

###########################################
## Read .csv file without the header row ##
###########################################

with open(file=f"{parent_dir}/drinks.csv", mode="r", newline="", encoding="utf-8") as file_pointer:
    csv_read_object = csv.reader(file_pointer)
    _ = next(csv_read_object)  # This will skip the first row (header row)
                               # Assign to _ (underscore) to indicate that we don't need this value (first row)
    for row in csv_read_object:
        print(row)  # Now it will print only the data rows, without the header row

# ['0', 'Afghanistan', '0', '0', '0', '0.0', 'AS']
# ['1', 'Albania', '89', '132', '54', '4.9', 'EU']
# ['2', 'Algeria', '25', '0', '14', '0.7', 'AF']
# ['3', 'Andorra', '245', '138', '312', '12.4', 'EU']
# ['4', 'Angola', '217', '57', '45', '5.9', 'AF']

#############################################
## Read a .tsv file (Tab-Separated Values) ##
#############################################

# The process is similar, just need to specify the delimiter as a tab character ("\t")

with open(file=f"{parent_dir}/weather.tsv", mode="r", newline="", encoding="utf-8") as file_pointer:
    tsv_read_object = csv.reader(file_pointer, delimiter="\t")
    for row in tsv_read_object:
        print(row)  # Each row is a list of values from the .tsv file

        # ['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine', 'WindGustDir', 'WindGustSpeed', 'WindDir9am', 'WindDir3pm', 'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am', 'Temp3pm', 'RainToday', 'RISK_MM', 'RainTomorrow']
        # ['8', '24.3', '0', '3.4', '6.3', 'NW', '30', 'SW', 'NW', '6', '20', '68', '29', '1019.7', '1015', '7', '7', '14.4', '23.6', 'No', '3.6', 'Yes']
        # ['14', '26.9', '3.6', '4.4', '9.7', 'ENE', '39', 'E', 'W', '4', '17', '80', '36', '1012.4', '1008.4', '5', '3', '17.5', '25.7', 'Yes', '3.6', 'Yes']
        # ['13.7', '23.4', '3.6', '5.8', '3.3', 'NW', '85', 'N', 'NNE', '6', '6', '82', '69', '1009.5', '1007.2', '8', '7', '15.4', '20.2', 'Yes', '39.8', 'Yes']

'''
Can also set delimiter to other characters like ';' or '|', just specify it in the "delimiter" parameter
'''

####################################
## Read .csv file as a dictionary ##
####################################

#------
## use csv.DictReader() to read a .csv file as a dictionary
#------

with open(file=f"{parent_dir}/medals.csv", mode="r", newline="", encoding="utf-8") as file_pointer:
    csv_dict_reader = csv.DictReader(file_pointer)
    for row in csv_dict_reader:
        print(row)  # Each row is a dictionary with column headers as keys

        # {'Year': '1998', 'City': 'Nagano', 'Sport': 'Skiing', 'Discipline': 'Alpine Skiing', 'NOC': 'SUI', 'Event': 'giant slalom', 'Event gender': 'M', 'Medal': 'Bronze'}
        # {'Year': '1998', 'City': 'Nagano', 'Sport': 'Skiing', 'Discipline': 'Alpine Skiing', 'NOC': 'SUI', 'Event': 'super-G', 'Event gender': 'M', 'Medal': 'Silver'}
        # {'Year': '1998', 'City': 'Nagano', 'Sport': 'Skiing', 'Discipline': 'Freestyle Ski.', 'NOC': 'SUI', 'Event': 'aerials', 'Event gender': 'W', 'Medal': 'Bronze'}
        # {'Year': '1998', 'City': 'Nagano', 'Sport': 'Skiing', 'Discipline': 'Snowboard', 'NOC': 'SUI', 'Event': 'giant-slalom', 'Event gender': 'M', 'Medal': 'Bronze'}

#------
## Specify fieldnames using "fieldnames=[...]"
#------
'''If not specfiied, the first row of the .csv file will be used as the field names (keys) for the dictionary.'''

with open(file=f"{parent_dir}/medals.csv", mode="r", newline="", encoding="utf-8") as file_pointer:
    csv_dict_reader = csv.DictReader(file_pointer, fieldnames=["Y", "C", "S", "D", "N", "E", "EG", "M"])
    for row in csv_dict_reader:
        print(row)  # Each row is a dictionary with specified keys

        # {'Y': '1992', 'C': 'Albertville', 'S': 'Biathlon', 'D': 'Biathlon', 'N': 'EUN', 'E': '15km', 'EG': 'W', 'M': 'Silver'}
        # {'Y': '1992', 'C': 'Albertville', 'S': 'Biathlon', 'D': 'Biathlon', 'N': 'EUN', 'E': '20km', 'EG': 'M', 'M': 'Gold'}
        # {'Y': '1992', 'C': 'Albertville', 'S': 'Biathlon', 'D': 'Biathlon', 'N': 'EUN', 'E': '3x7.5km relay', 'EG': 'W', 'M': 'Bronze'}
        # {'Y': '1992', 'C': 'Albertville', 'S': 'Biathlon', 'D': 'Biathlon', 'N': 'EUN', 'E': '4x7.5km relay', 'EG': 'M', 'M': 'Silver'}

#################################################
## (ADVANCED) Read .csv or .tsv file in chunks ##
#################################################
'''
Can read large .csv files in chunks to avoid memory issues, especially with very large datasets.
This is useful when dealing with large datasets that cannot fit into memory all at once.
'''

import csv

def process_csv_chunks(file_path, chunk_size=1000):
    """Generator function to process CSV file in chunks."""
    with open(file=file_path, mode="r", newline="", encoding="utf-8") as file_pointer:
        reader = csv.DictReader(file_pointer, delimiter="\t")
        chunk = []
        for row in reader:
            chunk.append(row)
            if len(chunk) >= chunk_size:
                # Process chunk
                yield chunk
                chunk = []
        if chunk:  # Process remaining rows
            yield chunk

# Usage example
parent_dir = "/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/csv_tsv_files"
chunk_size = 1000

for chunk in process_csv_chunks(f"{parent_dir}/weather.tsv", chunk_size=chunk_size):
    print(f"Processing chunk with {len(chunk)} rows")
    # Process your chunk here
    for row in chunk:
        print(row)  # Or whatever processing you need


#--------------------------------------------------------------------------------#
#----------------------- Write .csv and .tsv files ------------------------------#
#--------------------------------------------------------------------------------#

parent_dir = "/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/csv_tsv_files"

import csv

##################################
## write a .csv file using list ##
##################################

data = [
    ['Name', 'Age', 'City'],
    ['Alice', 28, 'New York'],
    ['Bob', 35, 'Chicago']
]

with open(f'{parent_dir}/write_list.csv', 'w', newline='', encoding='utf-8') as file_pointer:
    writer = csv.writer(file_pointer)
    writer.writerows(data)

########################################
## write a .csv file using dictionary ##
########################################

fields = ['ID', 'Name', 'Gender', 'Age']
data = [
    {'ID': '1', 'Name': 'Alice', 'Gender': 'Female', 'Age': '28'},
    {'ID': '2', 'Name': 'Bob', 'Gender': "Male", 'Age': '35'},
    {'ID': '3', 'Name': 'Charlie', 'Gender': 'Female', 'Age': '30'}
]

with open(f'{parent_dir}/write_dictionary.csv', 'w', newline='') as file_pointer:
    writer = csv.DictWriter(file_pointer, fieldnames=fields, delimiter=",")
    writer.writeheader() # Write the header row
    writer.writerows(data) # Write the data rows

#######################
## write a .tsv file ##
#######################

data = [
    ['Name', 'Subject', 'Score'],
    ['Alice', 'Math', 85],
    ['Bob', 'Science', 90],
    ['Charlie', 'History', 88]
]

with open(f'{parent_dir}/write_tsv.tsv', 'w', newline='', encoding='utf-8') as file_pointer:
    writer = csv.writer(file_pointer, delimiter='\t')  # Specify tab as the delimiter
    writer.writerows(data)  # Write the data rows


#---------------------------------------------------------------------------#
#----------------------- "quoting" parameter in csv.writer -----------------#
#---------------------------------------------------------------------------#

# "quoting" means enclosing fields in quotes ("" or '') when writing to a .csv file.

'''
The "quoting" parameter in csv.writer controls how special characters are handled in the output.
It can take values from the csv module's QUOTE_* constants:

- csv.QUOTE_MINIMAL: Only quote fields that contain special characters (default).
- csv.QUOTE_ALL: Quote all fields.
- csv.QUOTE_NONNUMERIC: Quote all non-numeric fields.
- csv.QUOTE_NONE: Do not quote any fields (use with caution, as it may lead to issues with special characters).
'''

import csv

data = [
    ['Place', 'Humidity', 'Temperature'],
    ['New York', 0.6, '25°C'],
    ['Los Angeles', 0.5, '30°C'],
    ['Chicago', 0.7, '20°C']
]

#############################################################
## Example of using the "quoting" parameter with QUOTE_ALL ##
#############################################################

with open(f'{parent_dir}/write_quoting_all.csv', 'w', newline='', encoding='utf-8') as file_pointer:
    writer = csv.writer(file_pointer, quoting=csv.QUOTE_ALL)  # Quote all fields
    writer.writerows(data)

# "Place","Humidity","Temperature"
# "New York","0.6","25°C"
# "Los Angeles","0.5","30°C"
# "Chicago","0.7","20°C"

####################################################################
## Example of using the "quoting" parameter with QUOTE_NONNUMERIC ##
####################################################################

with open(f'{parent_dir}/write_quoting_non_numeric.csv', 'w', newline='', encoding='utf-8') as file_pointer:
    writer = csv.writer(file_pointer, quoting=csv.QUOTE_NONNUMERIC)  # Quote all non-numeric fields
    writer.writerows(data)

# "Place","Humidity","Temperature"
# "New York",0.6,"25°C"
# "Los Angeles",0.5,"30°C"
# "Chicago",0.7,"20°C"
