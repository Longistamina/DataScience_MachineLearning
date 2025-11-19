# Static methods are like class method, but with some main differences:
# 1. Static methods DO NOT require "cls" as the first argument, i.e not bound or refer to the class
# 2. Static methods DO NOT require a return value either, hence not return None if not defined

# @staticmethod is a decorator that indicates the below method is a static method

# When to use: we should use static methods to do something that is related to the class
#              but does not need to be unique per instance
#              and IS NOT involved in creating new instances of the class

class DemoClass:
    @staticmethod
    def demo_static_method(): #No need any compulsory arguments like "cls" or "self"
        print("This demo static method has been executed successfully!")

    @staticmethod
    def add_numbers(addend_1: float, addend_2: float): #No need any compulsory arguments like "cls" or "self"
        return addend_1 + addend_2

# Execute a static method
DemoClass.demo_static_method() # Output: This demo static method has been executed successfully!
                               # It does not return None like the case of class method

# Execute a static method with return value without "cls" or "self" arguments
add_result = DemoClass.add_numbers(10, 35.5)
print(add_result) # Output: 45.5

### NOT RECOMMEND: static methods can be called from an instance, but should not do so
