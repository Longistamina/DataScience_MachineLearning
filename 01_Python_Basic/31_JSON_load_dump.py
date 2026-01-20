'''
JSON stands for JavaScript Object Notation.
It is a lightweight data interchange format that is easy for humans to read and write,
and easy for machines to parse and generate.

JSON is language-independent, with code parsers available for many programming languages, including Python.

JSON is often used to transmit data between a server and a web application, as an alternative to XML.

JSON data is represented as key-value pairs, similar to Python dictionaries.

In Python, the `json` module provides methods to work with JSON data.
The `json` module can be used to convert Python objects into JSON strings and vice versa.

#################################

Table of Contents:
1. json.loads() and json.load()
2. json.dumps() and json.dump()
3. Data Conversion between JSON and Python
'''

import json
#print(dir(json)) # List of methods in the json module

parent_dir = "/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files"

#------------------------------------------------------------#
#------------ json.loads() and json.load() ------------------#
#------------------------------------------------------------#

##################
## json.loads() ##
##################
'''
json.loads() is used to parse a JSON string and convert it into a Python dictionary.
The 's' in 'loads' stands for 'string'.
'''

json_string = '''
{
    "People":[
        {
            "Name": "John",
            "Age": 30,
            "City": "New York"
        },
        {
            "Name": "Anna",
            "Age": 22,
            "City": "London"
        },
        {
            "Name": "Mike",
            "Age": 32,
            "City": "Chicago"
        }
    ]
}
'''
print(type(json_string))  #  <class 'str'>

# json.loads() converts the JSON string into a Python dictionary
python_dict = json.loads(json_string)

print(python_dict)
# {'People': [{'Name': 'John', 'Age': 30, 'City': 'New York'}, 
#             {'Name': 'Anna', 'Age': 22, 'City': 'London'}, 
#              {'Name': 'Mike', 'Age': 32, 'City': 'Chicago'}]}

print(type(python_dict))  # <class 'dict'>

print(python_dict['People'][0]['Age']) # 30

print(type(python_dict['People'][0]['Age'])) # <class 'int'>

'''
Though the JSON string represents numbers as strings, json.loads() converts them to Python integers.
Check the data conversion table below for more details.
'''

#################
## json.load() ##
#################
'''
json.load() is used to read a JSON file and convert it into a Python dictionary.
The 'load' in 'json.load()' stands for 'load from file'.
'''

with open (f"{parent_dir}/emps.json", "r") as file: # Open the JSON file in read mode
    python_dict_from_file = json.load(file) # Convert the JSON file into a Python dictionary

print(python_dict_from_file)
# {'ID': ['1', '2', '3', '4', '5', '6', '7', '8'], 
# 'Name': ['Rick', 'Dan', 'Michelle', 'Ryan', 'Gary', 'Nina', 'Simon', 'Guru'], 
# 'Salary': ['623.3', '515.2', '611', '729', '843.25', '578', '632.8', '722.5'], 
# 'StartDate': ['1/1/2012', '9/23/2013', '11/15/2014', '5/11/2014', '3/27/2015', '5/21/2013', '7/30/2013', '6/17/2014'], 
# 'Dept': ['IT', 'Operations', 'IT', 'HR', 'Finance', 'IT', 'Operations', 'Finance']}


#------------------------------------------------------------#
#------------ json.dumps() and json.dump() ------------------#
#------------------------------------------------------------#

##################
## json.dumps() ##
##################

# json.dumps() is used to convert a Python object (like a dictionary) into a JSON string.
python_dict_to_convert = {
    "Name": "Alice",
    "Age": 28,
    "City": "Los Angeles"
}

# Convert to JSON string with indentation for readability
json_string_converted = json.dumps(python_dict_to_convert, indent=4)
print(json_string_converted)
# {
#     "Name": "Alice",
#     "Age": 28,
#     "City": "Los Angeles"
# }

# Without indentation
json_string_converted = json.dumps(python_dict_to_convert)
print(json_string_converted)  # {"Name": "Alice", "Age": 28, "City": "Los Angeles"}

# Custom separators
json_string_converted = json.dumps(python_dict_to_convert, indent=4, separators=(';', '__')) 
print(json_string_converted)
# {
#     "Name"__"Alice";
#     "Age"__28;
#     "City"__"Los Angeles"
# }

#################
## json.dump() ##
#################

# json.dump() is used to write a Python object (like a dictionary) into a JSON file.
dictionary_to_write = {
    "Name": "Bob",
    "Age": 35,
    "City": "San Francisco"
}

# Open the JSON file in write mode
with open(f"{parent_dir}/new_written_jsondump.json", "w") as json_pointer:
    json.dump(dictionary_to_write, json_pointer, indent=4)


#---------------------------------------------#
#------------ data conversion ----------------#
#---------------------------------------------#
'''
JSON         Python
----------------------------
null         None
true         True
false        False
string       str
number       int or float
array        list
object       dict
'''