# Static methods are like class method, but they are not bound to the class
# Static methods DO NOT require "cls" as the first argument, i.e not bound or refer to the class
# => hence they cannot access class attributes or other class methods directly

# @staticmethod is a decorator that indicates the below method is a static method

# When to use: we should use static methods to do something that is related to the class
#              but does not need to be unique per instance
#              and IS NOT involved in creating new instances of the class

class DemoStatic:
    
    class_attribute = "I am a class attribute"
    
    @staticmethod
    def demo_static_method(attr=False): #No need any compulsory arguments like "cls" or "self"
        if attr:
            print(DemoStatic.class_attribute)
            '''print(cls.class_attribute) # This will raise an error'''
        else:
            print("This demo static method has been executed successfully!")

    @staticmethod
    def add_numbers(addend_1: float, addend_2: float): # No need any compulsory arguments like "cls" or "self"
        
        DemoStatic.demo_static_method(attr=False) # Call another static method from this static method
        '''cls.demo_static_method(attr=False) # This will raise an error'''
        return addend_1 + addend_2

########################################################################

DemoStatic.demo_static_method() # Execute a static method without "cls" or "self" arguments
# This demo static method has been executed successfully!

DemoStatic.demo_static_method(attr=True) # Execute a static method with "cls" or "self" arguments
# I am a class attribute

########################################################################

# Execute a static method with return value without "cls" or "self" arguments
add_result = DemoStatic.add_numbers(10, 35.5)
print(add_result) # Output: 45.5

'''NOT RECOMMEND: static methods can be called from an instance, but should not do so'''
