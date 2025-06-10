# Create the Item class in a separate file named item.py

import csv

class Item:

    all_items = []

    def __init__(self, name: str, price: float, quantity: int):
        assert isinstance(name, str), "Name must be a string"
        assert price >= 0, "Price must be greater than zero"
        assert quantity >= 0, "Quantity must be greater than or equal to zero"

        self.name = name          
        self.price = price        
        self.quantity = quantity

        Item.all_items.append(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.price}, {self.quantity})"
        # Use self.__class__.name__ to get the class name dynamically
      
    def calculate_total_price(self):
        return self.price * self.quantity
    
    @classmethod
    def construct_from_csv(cls, file_path: str): #A function to construct an instance of the class from a .csv file
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f) # Read .csv file as a dictionary
            items = list(reader)

        return items