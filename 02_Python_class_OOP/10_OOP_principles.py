'''
There are four main principles of Object-Oriented Programming (OOP):
1. Encapsulation: Bundling data and methods that operate on that data within a single unit (class).
2. Abstraction: Hiding complex implementation details and showing only the necessary features of an object.
3. Inheritance: Creating new classes based on existing classes to promote code reuse.
4. Polymorphism: Allowing different classes to be treated as instances of the same class through a common interface.
'''

#-------------------------------------------------------#
#---------------- Encapsulation ------------------------#
#-------------------------------------------------------#

'''
Encapsulation in Python's object-oriented programming (OOP) is the concept of bundling data (attributes) 
and the methods (functions) that operate on that data into a single unit called a class. 

It restricts direct access to some of an object's components, 
which helps protect the integrity of the data and prevents accidental modification

Data Hiding: Encapsulation hides the internal state of an object 
and only exposes a controlled interface, usually through methods. 
This means the internal variables of a class can be made private (__attribute) or protected (_attribute) 
to prevent direct access from outside the class
'''

class Person:
    def __init__(self, name, age):
        self.name = name          # public attribute
        self.__age = age          # private attribute

    def get_age(self):
        return self.__age         # getter method

    def set_age(self, age):
        if age > 0:
            self.__age = age      # setter method with validation

p = Person("John", 30)

print(p.name)          # Access public attribute

print(p.__age)         # Attempting to access private attribute directly will raise an AttributeError
                       # AttributeError: 'Person' object has no attribute '__age'

print(p.get_age())     # Access private attribute via getter
p.set_age(35)          # Modify private attribute via setter
print(p.get_age())


# In this example, the __age attribute is private and cannot be accessed directly from outside the class. 
# Instead, the get_age and set_age methods provide controlled access to it

# To sum it up, Encapsulation prevents direct access and direct modification of an object's attributes,
# helps ensure data security and integrity while providing a clean interface for interaction


#-----------------------------------------------------#
#---------------- Abstraction ------------------------#
#-----------------------------------------------------#

'''
Abstraction in Python's object-oriented programming (OOP) is the concept of hiding the internal implementation details 
of a class or method and exposing only the essential features and behaviors to the user. 

It allows you to focus on what an object does rather than how it does it, 
simplifying complex systems by providing a clear and simplified interface

=> Abstraction means "hiding the complexity or unnecessary details" from the user.
'''

class Email():
    def __init__(self, sender, recipient, subject):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject

    def __redact_body(self):
        # This is a private method that redacts the email body
        self.body = """
        Sender: {self.sender}
        Recipient: {self.recipient}
        Subject: {self.subject}
        This is a confidential email.
        Please do not share it with anyone.
        """
        return self.body
    
    @staticmethod
    def __connect_to_server():
        # This is a private static method that connects to the email server
        print("Connecting to email server successfully...")

    def send_email(self):
        self.__redact_body()  # Call the private method to redact the body
        self.__connect_to_server()
        print("Email sent successfully!")

email_demo = Email("Don Quixote", "Sancho Panza", "Adventure Awaits")

email_demo.send_email()  # Output: Email sent successfully!

# In this example, the Email class abstracts the complexity of sending an email.
# The __redact_body and __connect_to_server methods are private, 
# meaning they are not intended to be accessed directly by the user.
# The user interacts with the Email class through the public send_email() method,
# which provides a simplified interface for sending an email without needing to know the details of how it works.


############# Other example of Abstraction #############

from abc import ABC, abstractmethod

# ABC here means Abstract Bas Class, which is a base class for defining abstract classes in Python.
# Abstract classes cannot be instantiated directly and must be subclassed.
# (meaning you cannot create any instance or object from an abstract class)

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    # @abstractmethod This decorator is used to mark methods inside an abstract class as abstract methods. 
    # These methods have no implementation in the abstract class and must be overridden by any subclass.
    # If a subclass does not implement all abstract methods, it cannot be instantiated either.
    
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

circle = Circle(6)
rectangle = Rectangle(5, 7)

print(circle.area())      # Output: 113.09724
print(rectangle.area())   # Output: 35

# In this example, Shape is an abstract class with an abstract method area(). 
# The subclasses Circle and Rectangle implement the area() method, hiding the details of how the area is calculated. 
# Users interact with the shapes through the common interface defined by the abstract class


#-----------------------------------------------------#
#---------------- Inheritance ------------------------#
#-----------------------------------------------------#

'''
Inheritance in Python's object-oriented programming (OOP) is a mechanism that allows one class (called the child or subclass) 
to inherit attributes and methods from another class (called the parent or superclass). 

This promotes code reuse, simplifies maintenance, and helps create a hierarchical relationship between classes.
'''

# Refer to file 07_inheritance.py for detailed examples of inheritance


#-----------------------------------------------------#
#---------------- Polymorphism -----------------------#
#-----------------------------------------------------#

'''
Polymorphism, derived from Greek meaning "many forms," is a feature in object-oriented programming (OOP) 
where objects of different classes can respond to the same method call in their own way. 

This allows you to write code that can work with objects of different types 
without needing to know their specific class. 

Polymorphism enables flexibility and extensibility in your code
'''

friends = ['Joey', 'Rachel', 'Monica']
city = 'New York'

print(len(friends))  # Output: 3 (the number of elements in the list)
print(len(city))     # Output: 8 (the number of characters in the string)
# In this example, the len() function is polymorphic because it can be used with both a list and a string,
# even though they are different types of objects.

### Example of Polymorphism with Classes ###

class Boy:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def gender(self):
        print("M")

class Girl:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def gender(self):
        print("F")

boy1 = Boy("Sam", 20)
girl1 = Girl("Mona", 26)

for person in (boy1, girl1):
    person.gender()
    # M
    # F

# In this example, method .gender() returns different results based on the class of the object calling it.