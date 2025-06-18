'''
Exercise 1: handle dictionary

# Given these configuration dictionaries:
base_config = {
    "database": {"host": "localhost", "port": 5432},
    "logging": {"level": "INFO", "file": "app.log"},
    "features": {"auth": True, "cache": False}
}

user_config = {
    "database": {"port": 8080, "username": "admin"},
    "logging": {"level": "DEBUG"},
    "features": {"cache": True, "notifications": True}
}

environment_overrides = {
    "database": {"host": "prod-server.com"},
    "features": {"auth": False}
}

Q1: Use dictionary comprehension to create a new dictionary 
    containing only the "database" sections from all three configs

Q2: Merge user_config into base_config using the | operator (Python 3.9+) or .update() method

Q3: Extract all keys from the nested "features" dictionaries and store them in a set

Q4: Use nested dictionary access to print the final database host after applying environment overrides

Q5: Create a list of tuples showing (config_name, total_nested_keys) for each configuration
'''

############################################################

'''
Exercise 2: Unpacking Operators

# Given this data:
api_data = [
    {"method": "GET", "endpoint": "/users", "params": {"page": 1, "limit": 10}},
    {"method": "POST", "endpoint": "/users", "data": {"name": "John", "email": "john@example.com"}},
]

headers = {"Content-Type": "application/json", "Authorization": "Bearer token"}
additional_params = {"timeout": 30, "verify": True}

Q1: Use ** to unpack headers and additional_params into a single dictionary using {**headers, **additional_params}

Q2: Print each API request by unpacking the dictionary values: print(*api_data.values())

Q3: Create a list using unpacking where you combine multiple lists: [*list1, *list2, *list3]

Q4: Use dictionary unpacking to merge the "params" or "data" from each API request with the headers

Q5: Demonstrate unpacking in a print statement to display all configuration keys: print("Config keys:", *base_config.keys())
'''