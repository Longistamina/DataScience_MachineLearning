#--------------------------------------------#
#-------- __init__ explanation --------------#
#--------------------------------------------#

# __init__() method is a method that forces the definition of specific attributes when created an object from a class
# Those attributes required by __init__() if somehow are not defined will result in unsucessful object creation

class Item:
    def __init__(self, name):
        self.name = name    # define a new attribute 'name' for instance 'self' as 'self.name'
                            # assign the value of argument "name" into attribute "self.name"

item1 = Item("Phone") # "Phone" is passed into as the value of attribute 'self.name'
                      # This is equivalent to "item1.name = 'Phone'" 
                      # An instance is created: Phone

print(item1.name)     # "Phone"

item2 = Item("Laptop")
print(item2.name)     # "Laptop"

# By using __init__, we can assign the values for compulsory attributes via "item = Item(value1, valu2, ...)"
# Instead of:
#             item.attribute1 = value1
#             item.attribute2 = value2


item_no_name = Item()
# => TypeError: Item.__init__() missing 1 required positional argument: 'name'
# => This case raises error because the __init__() require us to define the value for attribute 'name'
#                                                 (but we didn't)



#------------------------------------------------------------#
#------------- __innit__ additional example -----------------#
#------------------------------------------------------------#

################ Explicit example #################
class ItemExplicit:
    def __init__(self, name_input, price_input, quantity_input):
        self.name = name_input           # Attribute self.name takes the value of name_input variable
        self.price = price_input         # Attribute self.price takes the value of price_input variable
        self.quantity = quantity_input   # Attribute self.quantity takes the value of quantity_input variable

item_extend_1 = ItemExplicit(
    name_input = "Phone",
    price_input = 1000,
    quantity_input = 5
)

print(item_extend_1.name)      # "Phone"
print(item_extend_1.price)     # 1000
print(item_extend_1.quantity)  # 5


################ Concise example #################
class ItemConcise:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

item_extend_2 = ItemConcise("Laptop", 1500, 3)

print(item_extend_2.name)      # "Laptop"
print(item_extend_2.price)     # 1500
print(item_extend_2.quantity)  # 3


#---------------------------------------------------------#
#------------- __innit__ add constraints -----------------#
#---------------------------------------------------------#

class ItemWithConstraints:
    def __init__(self, name: str, price: float, quantity: int):
        # "name: string" means the name of the item must be a string
        # "price: float" means the price of the item must be a float
        # "quantity: int" means the quantity of the item must be an integer

        # Adding constraints to ensure valid values for attributes
        assert isinstance(name, str), "Name must be a string" # isinstance(name, str) checks if the type of 'name' is string
        assert price >= 0, "Price must be greater than zero"
        assert quantity >= 0, "Quantity must be greater than or equal to zero"

        # Assigning values to attributes of the instance
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def calculate_total_price(self): # no need to pass method(self, price, quantity) as the method is bound to the instance
        # Method to calculate total price of the item
        return self.price * self.quantity

# Example usage
item_with_constraints = ItemWithConstraints("Tablet", 300, 10)
print(item_with_constraints.name)      # "Tablet"
print(item_with_constraints.price)     # 300
print(item_with_constraints.quantity)  # 10
print(item_with_constraints.calculate_total_price())  # 3000

# Attempting to create an item with invalid constraints
try:
    invalid_item = ItemWithConstraints("Invalid Item", -100, 5)
except AssertionError as e:
    print(f"Error: {e}") # Output: Error: Price must be greater than zero


# Attempting to create an item with invalid quantity
try:
    invalid_item = ItemWithConstraints("Invalid Item", 100, -5)
except AssertionError as e:
    print(f"Error: {e}") # Output: Error: Quantity must be greater than or equal to zero


# Attempting to create an item with invalid type for name
try:
    invalid_item = ItemWithConstraints(123, 100, 5)
except AssertionError as e:
    print(f"Error: {e}") # Output: Error: Name must be a string
