'''
Python magic methods, also known as dunder methods (due to their double underscore prefix and suffix), 
are special methods that allow you to define or customize the behavior of your classes in Python

__new__()     Called a new instance of a class (subclass).
__init__()    Called when an object is instantiated to initialize it.
__repr__()    Called by repr() to get an official string representation useful for debugging.
__str__()     Called by str() to define the “informal” string representation of an instance
__len__()     Called by len() to return the lenght of an object via len(obj)
__getitem__() Called to enable bracket access (obj[key]).
__setitem__() Called to enable item assignment (obj[key]=value).
__eq__()      Called to enable equality comparison (obj1 == obj2)
__add__()     Called to enable arithmetic addition (obj1 + obj2)
__call__()    Makes an instance callable like a function
__enter__()   Called to define the behavior of a context manager (open)
__exit__()    Called to define the behavior of a context manager (close)
__del__()     Called to add behavior when an object is about to be destroyed

Difference between __repr__() and __str__():
## __repr__()
   Purpose: Developer-oriented, unambiguous
   Output: 'Hello, world!' (with quotes ' ' or double quotes " ")
   When you print a list of objects, Python calls __repr()__ and NOT __str()__
   
## __str__()
   Purpose: User-oriented, readable
   Ouput:   Hello, world! (no quotes)
   When you print an object directly (e.g., print(phone1)), Python calls __str__() if it exists

At the end of this file are the list of many other magic methods.
'''
#-------------------------------------#
#-------- __new__() method -----------#
#-------------------------------------#

# __new__() called a new instance of a class (subclass).

# without __new__()
class IntClass:
    def __init__(self, value):
        self.value = value

obj = IntClass(10)
print(obj.value)  # Output: 10

# with __new__()
class EvenIntClass(int):
    def __new__(cls, value): # cls is the keyword to refer to the class itself (like self for instance)
        value = value if value % 2 == 0 else value + 1
        return super().__new__(cls, value)

e = EvenIntClass(3)
print(e)  # Output: 4

#--------------------------------------#
#-------- __str__() method ------------#
#--------------------------------------#

# __str__() Called by str() to define the “informal” string representation of an instance

# without __str__()
class Book:
    def __init__(self, title):
        self.title = title

b = Book("Python 101")
print(b)  # Output: <__main__.Book object at 0x...>

# with __str__()
class Book:
    def __init__(self, title):
        self.title = title
    def __str__(self):
        return f"Book: {self.title}"

b = Book("Python 101")
print(b)  # Output: Book: Python 101


#--------------------------------------#
#-------- __len__() method ------------#
#--------------------------------------#

# __len__() Called by len() to return the lenght of an object via len(obj)

# without __len__()
class Team:
    def __init__(self, players):
        self.players = players

t = Team(['Alice', 'Bob'])
print(len(t)) # TypeError: object of type 'Team' has no len()


# with __len__()
class Team:
    def __init__(self, players):
        self.players = players
    def __len__(self):
        return len(self.players)

t = Team(['Alice', 'Bob'])
print(len(t))  # Output: 2


#------------------------------------------#
#-------- __getitem__() method ------------#
#------------------------------------------#

# __getitem__() Called to enable bracket access (obj[key]).

# without __getitem__()
class Colors:
    def __init__(self, colors):
        self.colors = colors

c = Colors(['red', 'blue'])
print(c[0])  # TypeError: 'Colors' object is not subscriptable

# with __getitem__()
class Colors:
    def __init__(self, colors):
        self.colors = colors
    def __getitem__(self, index):
        return self.colors[index]

c = Colors(['red', 'blue'])
print(c[0])  # Output: red


#------------------------------------------#
#-------- __setitem__() method ------------#
#------------------------------------------#

# __setitem__() Called to enable item assignment (obj[key]=value).

# without __setitem__()
class Basket:
    def __init__(self):
        self.items = {}

b = Basket()
b['apple'] = 3  # TypeError: 'Basket' object does not support item assignment

# with __setitem__()
class Basket:
    def __init__(self):
        self.items = {}
    def __setitem__(self, key, value):
        self.items[key] = value

b = Basket()
b['apple'] = 3
print(b.items)    # Output: {'apple': 3}
print(b["apple"]) # Output: 3


#-------------------------------------#
#-------- __eq__() method ------------#
#-------------------------------------#

# __eq__()      Called to enable equality comparison (obj1 == obj2)

# without __eq__()
class Point:
    def __init__(self, x):
        self.x = x

p1 = Point(1)
p2 = Point(1)
print(p1 == p2)  # Output: False (compares memory addresses)

# with __eq__()
class Point:
    def __init__(self, x):
        self.x = x
    def __eq__(self, other):
        return self.x == other.x

p1 = Point(1)
p2 = Point(1)
print(p1 == p2)  # Output: True

# Other comparison magic methods:
# __lt__(self, other): Less than <
# __le__(self, other): Less than or equal <=
# __eq__(self, other): Equal ==
# __ne__(self, other): Not equal !=
# __gt__(self, other): Greater than >
# __ge__(self, other): Greater than or equal >=


#--------------------------------------#
#-------- __add__() method ------------#
#--------------------------------------#

# __add__() called to enable arithmetic addition (obj1 + obj2)

# without __add__()
class Vector:
    def __init__(self, x):
        self.x = x

v1 = Vector(2)
v2 = Vector(3)
print(v1 + v2)  # TypeError: unsupported operand type(s)

# with __add__()
class Vector:
    def __init__(self, x):
        self.x = x
    def __add__(self, other):
        return Vector(self.x + other.x)
    def __str__(self):
        return f"Vector({self.x})"

v1 = Vector(2)
v2 = Vector(3)
print(v1 + v2)  # Output: Vector(5)

# Other arithmetic magic methods:
# __sub__(self, other)	            Defines behavior for self - other.
# __mul__(self, other)	            Defines behavior for self * other.
# __truediv__(self, other)	        Defines behavior for self / other.
# __floordiv__(self, other)	        Defines behavior for self // other.
# __mod__(self, other)	            Defines behavior for self % other.
# __pow__(self, other[, modulo])	Defines behavior for self ** other.


#---------------------------------------#
#-------- __call__() method ------------#
#---------------------------------------#

# __call__() Makes an instance callable like a function

# without __call__()
class Greeter:
    def __init__(self, name):
        self.name = name

g = Greeter("Alice")
g()  # TypeError: 'Greeter' object is not callable

# with __call__()
class Greeter:
    def __init__(self, name):
        self.name = name
    def __call__(self):
        print(f"Hello, {self.name}!")

g = Greeter("Alice")
g()  # Output: Hello, Alice!


#---------------------------------------------#
#-------- __enter__() and __exit__() ---------#
#---------------------------------------------#

# __enter__() and __exit__() are used to define the behavior of a context manager

# without __enter__() and __exit__()
class FileOpener:
    def __init__(self, filename):
        self.filename = filename
with FileOpener("test.txt") as f:  # TypeError: 'FileOpener' object does not support the context manager protocol
    pass

# with __enter__() and __exit__()
class FileOpener:
    def __init__(self, filename):
        self.filename = filename
    def __enter__(self):
        self.file = open(self.filename, 'w')
        return self.file
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

with FileOpener("test.txt") as f:
    f.write("Check __enter__() and __exit__() methods")
    print("File opened successfully")
# Output: File opened successfully
#         The file "test.txt" is created with the given content


#-----------------------------------#
#-------- __del__() method ---------#
#-----------------------------------#

# __del__() is called to add behavior when an object is about to be destroyed

# without __del__()
class Temp:
    def __init__(self, name):
        self.name = name

t = Temp("A")
del t # No output

# with __del__()
class Temp:
    def __init__(self, name):
        self.name = name
    def __del__(self):
        print(f"{self.name} is being deleted")

t = Temp("A")
del t  # Output: A is being deleted



'''
Other magic methods:

__format__(self, format_spec): Defines behavior for the format() function and formatted string literals.

__getattr__(self, name): Called when an attribute is not found.
__setattr__(self, name, value): Called when an attribute is set.
__delattr__(self, name): Called when an attribute is deleted.
__getattribute__(self, name): Called for every attribute access 

- Reflected versions: __radd__, __rsub__, __rmul__, __rtruediv__, etc.
- In-place versions: __iadd__, __isub__, __imul__, __itruediv__, etc.
- Bitwise operators: __and__, __or__, __xor__, __lshift__, __rshift__ and their reflected and in-place counterparts.

__int__(self): Converts to int.
__float__(self): Converts to float.
__complex__(self): Converts to complex.
__bool__(self): Converts to bool.
__index__(self): Used for slicing and other operations requiring an integer index

__sizeof__(self): Returns the size of the object in memory.
__hash__(self): Returns the hash value of the object.
__bool__(self): Boolean value of the object.
__copy__(self), __deepcopy__(self, memo): Support for copying.
'''