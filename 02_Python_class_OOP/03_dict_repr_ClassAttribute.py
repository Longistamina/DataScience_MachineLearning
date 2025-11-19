#-----------------------------------------------------------#
#-------- class attributes and instance attributes ---------#
#-----------------------------------------------------------#

class Item:

    discount_rate = 0.2 # this is a Class attribute, shared by all instances of the class

    def __init__(self, name: str, price: float, quantity: int):
        assert isinstance(name, str), "Name must be a string"
        assert price >= 0, "Price must be greater than zero"
        assert quantity >= 0, "Quantity must be greater than or equal to zero"

        self.name = name          # This is an instance attribute, which means it is unique to each instance of the class
        self.price = price        # This is also an instance attribute
        self.quantity = quantity  # This is also an instance attribute
    
    def calculate_total_price(self):
        return self.price * self.quantity
    
    def apply_discount_ClassAttribute(self):
        # Using the class attribute discount_rate to calculate the discounted price
        discount_amount = self.price * Item.discount_rate
        return self.price - discount_amount
    
    def apply_discount_instanceAttribute(self):
        # Using the instance attribute discount_rate to calculate the discounted price
        # So when the discount_rate of a specific instance is changed, it will use that value
        discount_amount = self.price * self.discount_rate
        return self.price - discount_amount


item1 = Item("Laptop", 1500, 3)
item2 = Item("Phone", 1000, 5)


print(Item.discount_rate)  # Accessing the class attribute directly from the class => 0.2
print(item1.discount_rate) # Accessing the class attribute from an instance        => 0.2
print(item2.discount_rate) # Accessing the class attribute from another instance   => 0.2
# ==> all instances share the same class attribute

print(item1.apply_discount_ClassAttribute())  # Applying discount on item1 => 1200.0


############ ATTENTION ############

# If you change the class attribute, it will affect all instances
# for example:
Item.discount_rate = 0.3   # This changes will be applied to all instances of the class Item
print(item1.discount_rate) # 0.3

# If you only change the class attribute of an instance, only that instance will be affected
item2.discount_rate = 0.25 # This applies only to item2, while item1 discount_rate remains 0.3
print(item2.discount_rate)  # 0.25
print(item1.discount_rate)  # 0.3

print(item1.apply_discount_instanceAttribute()) # Applying discount_rate 0.3 on item1 => 1050.0
print(item2.apply_discount_instanceAttribute()) # Applying discount_rate 0.25 on item2 => 750.0


#---------------------------------------------#
#-------- __dict__ to see attributes ---------#
#---------------------------------------------#

# .__dict__ is a special attribute that stores the name of the attributes of both class and instance
print(Item.__dict__)  # Show all the attributes of the class Item
print(item1.__dict__) # Show all the attributes of the instance item1


#-------------------------------------#
#-------- __repr__() method  ---------#
#-------------------------------------#

# "repr" stands for "representation"
# __repr__() method is used to define a string nickname for the class


# Imagine we want to create a list to store all the items (instances of Item class)

class ItemNoRepr:

    all_items = [] # This Class attribute will store all the instances (items) created by the user

    def __init__(self, name: str, price: float, quantity: int):
        assert isinstance(name, str), "Name must be a string"
        assert price >= 0, "Price must be greater than zero"
        assert quantity >= 0, "Quantity must be greater than or equal to zero"

        self.name = name          
        self.price = price        
        self.quantity = quantity

        ItemNoRepr.all_items.append(self) # Add a created instance to the all_items list

item1 = ItemNoRepr("Laptop", 1500, 3)
item2 = ItemNoRepr("Phone", 1000, 5)
item3 = ItemNoRepr("Tablet", 800, 2)

print(ItemNoRepr.all_items) # Print out the list of all the items created
# [<__main__.ItemNoRepr object at 0x7f9ef73979e0>, <__main__.ItemNoRepr object at 0x7f9ef7236c60>, <__main__.ItemNoRepr object at 0x7f9ef7237b30>]
# The output shows the memory address of each instance, which is not very "friendly" for our eyes


######## Using __reper__() method ########

class ItemWithRepr:

    all_items = [] # This Class attribute will store all the instances (items) created by the user

    def __init__(self, name: str, price: float, quantity: int):
        assert isinstance(name, str), "Name must be a string"
        assert price >= 0, "Price must be greater than zero"
        assert quantity >= 0, "Quantity must be greater than or equal to zero"

        self.name = name          
        self.price = price        
        self.quantity = quantity

        ItemWithRepr.all_items.append(self) # Add a created instance to the all_items list

    def __repr__(self):
        # This method returns a string representation of the instance (self)
        return f"Item({self.name}, {self.price}, {self.quantity})"

item1 = ItemWithRepr("Laptop", 1500, 3)
item2 = ItemWithRepr("Phone", 1000, 5)
item3 = ItemWithRepr("Tablet", 800, 2)

print(ItemWithRepr.all_items) # Print out the list of all the items created
# [Item(Laptop, 1500, 3), Item(Phone, 1000, 5), Item(Tablet, 800, 2)]
# The output now looks really more friendly and informative.
