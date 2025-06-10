# Class methods are the methods that are bound to the class, not the instance of the class.

import csv

class Employee:
    @classmethod # This line indicates the below method is a class method, not an instance method
    def demo_class_method(cls): # always set "cls" as the first argument for class method, like "self" for instance method
        print("This is a demo class method of the class Item")

    @classmethod
    def construct_from_csv(cls, file_path: str): #A function to construct an instance of the class from a .csv file
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f) # Read .csv file as a dictionary
            employees = list(reader)

        return employees

print(Employee.demo_class_method()) # Execute a class method
                                    # This is a demo class method of the class Item
                                    # None (this is because we did not define the return value for the demo method)

csv_path = "/home/longdpt/Documents/Academic/DataScience_MachineLearning_Python_SQL/01_Python_Basic/class_OOP/class_method_employees.csv"

lst_employees = Employee.construct_from_csv(file_path = csv_path)
print(lst_employees)
# {'Name': 'Alice', 'Age': '30', 'City': 'New York'}
# {'Name': 'Bob', 'Age': '25', 'City': 'Los Angeles'}
# {'Name': 'Charlie', 'Age': '35', 'City': 'Chicago'}
