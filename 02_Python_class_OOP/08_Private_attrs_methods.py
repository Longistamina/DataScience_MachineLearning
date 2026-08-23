import random

'''
1. _attribute or _method() (Single Underscore)

    Convention: Indicates the attribute is intended for internal use (a "protected" member).

    Not enforced: You can still access it from outside the class.

    Usage: Signals to other programmers:
           "This is for internal use, don't touch unless you know what you're doing."
'''

class DemoSingleUnderscore:
    def __init__(self):
        self._internal = 42

    def _change_internal(self):
        self._internal = random.randint(10, 20)


obj = DemoSingleUnderscore()
print(obj._internal)  # Output: 42 (can access, but should not)

obj._change_internal()
print(obj._internal) # other values between [10, 20)


'''
2. __attribute and __method() (Double Underscores)

    Name Mangling: Python changes the attribute name internally to _ClassName__attribute
                   to avoid accidental access and name clashes in subclasses.
    (meaning to access it, you must write something like obj._DemoClass__internal)

    Purpose: Makes it harder (not impossible) to access from outside the class.

    Usage: For "private" attributes.
'''

class DemoDoubleUnderscore:
    def __init__(self):
        self.__private = 99

    def __change_private(self):
        self.__private = random.randint(10, 20)

obj = DemoDoubleUnderscore()

print(obj.__private)  # AttributeError: 'MyClass' object has no attribute '__private'

print(obj._DemoDoubleUnderscore__private)  # Output: 99 (can access using name mangling)
                                           # harder to access, but still possible

obj._DemoDoubleUnderscore__change_private()
print(obj._DemoDoubleUnderscore__private) # other values between [10, 20)

'''
The above conventions also apply to methods:

_method(): internal-use method (single underscore)
           Example: def _method_name()

__method(): private method (double underscore)
            Example: def __method_name()
'''
