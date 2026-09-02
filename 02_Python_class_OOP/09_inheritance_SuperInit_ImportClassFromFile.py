# Create Item class

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

    @property
    def total_price(self):
        return self.price * self.quantity


# =========================================================================================
# 1. Why need Inheritance?
# =========================================================================================
'''
Imagine our item list have many types of phones.
We want to determine whether the phone is broken or not for selling.
If we set a new attribute like ``self.broken_phone`` in side the Item class,
it will be applied to all the items, not just phones.

=> Create a new class Phone that inherits from Item
'''

class Phone(Item): # The "Item" inside the parentheses means that Phone is inheriting from Item
    def __init__(self, name: str, price: float, quantity: int, broken_phone: bool=False):
        super().__init__(name, price, quantity)
        # This links to the __init__ method of Item
        # So that we don't have to set "self.attributes = arguments" again and again

        self.broken_phone = broken_phone  # New attribute specific to Phone class

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.price}, {self.quantity}, Broken: {self.broken_phone})"
        # Redefine __repr__() to include ``self.broken_phone`` attribute.


phone1 = Phone("iPhone 14", 1200, 5, broken_phone=True)
phone2 = Phone("Samsung Galaxy S23", 1000, 3)

print(phone1)  # Output: Phone(iPhone 14, 1200, 5, Broken: True)
print(phone2)  # Output: Phone(Samsung Galaxy S23, 1000, 3, Broken: False)
               # Here, __repr__() method is inherited from Item class

print(phone1.broken_phone)  # Output: True

print(phone1.total_price)  # Output: 6000 (1200 * 5)
                                       # It inherits the method calculate_total_price() from Item

print(Phone.all_items)
# Output: [Phone(iPhone 14, 1200, 5, True), Phone(iPhone 14, 1200, 5, Broken: True), Phone(Samsung Galaxy S23, 1000, 3, Broken: False)]


# =========================================================================================
# 2. Inheritance from other .py file
# =========================================================================================
'''We can also import the Item class from another file like item.py and inherit from it'''

import os
from pathlib import Path

dir_path = next(Path("/home").glob("**/item.py")).parent
print(dir_path) # /home/longdpt/Documents/Academic/DataScience_MachineLearning/02_Python_class_OOP

os.chdir(dir_path)
os.getcwd() # '/home/longdpt/Documents/Academic/DataScience_MachineLearning/02_Python_class_OOP'

from item import (
    Item as ItemCSV,  # Make sure file ``item.py`` is in the same directory or adjust the import path accordingly
)

                                 # ``as ItemCSV`` to avoid overlapping with the Item class above

class Fruit(ItemCSV):
    def __init__(self, name: str, price: float, quantity: int, is_organic: bool=False):
        super().__init__(name, price, quantity)
        self.is_organic = is_organic  # New attribute specific to Fruit class

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.price}, {self.quantity}, Organic: {self.is_organic})"
        # Redefine __repre__() to include ``self.broken_phone`` attribute.


fruit1 = Fruit("Apple", 2.5, 10, is_organic=True)
fruit2 = Fruit("Banana", 1.5, 20)

print(fruit1)  # Output: Fruit(Apple, 2.5, 10, Organic: True)
print(fruit2)  # Output: Fruit(Banana, 1.5, 20, Organic: False)

print(fruit1.is_organic)  # Output: True

print(fruit1.total_price)  # Output: 25.0 (2.5 * 10)

print(Fruit.all_items)
# [Fruit(Apple, 2.5, 10, Organic: True), Fruit(Banana, 1.5, 20, Organic: False), Fruit(Apple, 2.5, 10, Organic: True), Fruit(Banana, 1.5, 20, Organic: False)]
# It inherits the all_items attribute and the __repr__() method from Item
