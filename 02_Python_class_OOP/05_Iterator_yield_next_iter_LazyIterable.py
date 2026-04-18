'''
In Python, a lazy iterable (iterator) is an object that computes its elements one at a time only when requested, 
rather than storing them all in memory upfront. 
This behavior is known as lazy evaluation. 

While common iterables like lists and tuples are "eager" 
(meaning they store all their data in RAM immediately), 
lazy iterables (iterators) use a "just-in-time" approach. 
This makes them essential for handling massive datasets or infinite sequences 
that would otherwise crash your program due to memory limits. 
'''


#-------------------------------------------------------------------------------#
#--------------------------- 1. yield and next() -------------------------------#
#-------------------------------------------------------------------------------#
'''
In Python, yield is a keyword used to create generators. 
Unlike a standard return statement, which exits a function and destroys its local state, 
yield pauses the function, saves all of its variables, and sends a value back to the caller. 
When the function is called again, it resumes exactly where it left off.

##########################

The next() function is a built-in Python tool used to manually retrieve the subsequent item from an iterator 
(like a generator, map object, or any object created with iter()
'''

##########################
## simple yield example ##
##########################

def simple_generator():
    yield 1
    yield "Hello"
    yield "Aloha"
    yield 3.14

simple_gen = simple_generator()

print(next(simple_gen))  # Output: 1
print(next(simple_gen))  # Output: Hello
print(next(simple_gen))  # Output: Aloha
print(next(simple_gen))  # Output: 3.14

print(simple_gen[0])
# TypeError: 'generator' object is not subscriptable

#####################
## yield with loop ##
#####################

def while_yield(n):
    i = 0
    while i < n:
        yield i   # pauses here, sends value out, resumes on next()
        i += 1

while_gen = while_yield(6)

print(next(while_gen))  # Output: 0
print(next(while_gen))  # Output: 1
print(next(while_gen))  # Output: 2
print(next(while_gen))  # Output: 3
print(next(while_gen))  # Output: 4
print(next(while_gen))  # Output: 5
print(next(while_gen))  # Raises StopIteration, as there are no more items to yield

#------#

def for_yield(n):
    for i in range(n):
        yield i

for_gen = for_yield(3)

print(next(for_gen))  # Output: 0
print(next(for_gen))  # Output: 1
print(next(for_gen))  # Output: 2
print(next(for_gen))  # Raises StopIteration, as there are no more items to yield

###########################################
## Use () expression to create generator ##
###########################################

# List comprehension — realized immediately, subscriptable
squares_list = [x**2 for x in range(5)]   # [0, 1, 4, 9, 16]

# Generator expression — lazy, uses () instead of []
squares_gen = (x**2 for x in range(5))    # <generator object>

next(squares_gen)   # 0
next(squares_gen)   # 1
list(squares_gen)   # [4, 9, 16]  (0 and 1 already consumed!)

#########################
## Realize a generator ##
#########################

def fibonacci_gen(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

fib_gen = fibonacci_gen(10)

fib_series = list(fib_gen) # can be tuple(), set(), dict() etc. as well
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


#----------------------------------------------------------------------------------#
#-------------------- 2. iter() converts iterable to iterator ---------------------#
#----------------------------------------------------------------------------------#
'''
In Python, the iter() function is a built-in tool that takes an object and turns it into an iterator.

To understand iter(), it helps to know the difference between two key Python concepts:
+ Iterable: A collection of items you can loop over (like a list, string, dictionary, or tuple).
+ Iterator: An engine that knows how to fetch items from an iterable one by one. 
            (Note: All generators are iterators, but not all iterators are generators!)
            It remembers its current state and uses the next() function to get the next item 
            until there are no items left.
'''

####################
## iter() example ##
####################

fruits = ["apple", "banana", "cherry"]
print(fruits[1]) # banana

fruits_iter = iter(fruits)  # Convert the list to an iterator
print(fruits_iter) # <list_iterator object at 0x7217285f9810>
print(next(fruits_iter))  # apple
print(fruits_iter[0]) # TypeError: 'list_iterator' object is not subscriptable

######################################
## iter(callable, sentinel) example ##
######################################

import random

def roll_dice(): # A callable that simulates rolling a six-sided die
    return random.randint(1, 6)

def roll_until_n(n):
    assert 1 <= n <= 6, "n must be between 1 and 6"
    return iter(roll_dice, n) # n is the sentinel value that stops the iteration when roll_dice() returns n

n = 5
roller = roll_until_n(n)
# Create an iterator that keeps rolling the die until it rolls a n=5

for roll in roller:
    print(roll)  # This will print random numbers between 1 and 6 until it rolls a 5
# 6
# 4
# 3
# 1
# 4
# 2

print(f"Rolled a {n} - stopping.")
# Rolled a 5 - stopping.


####################################################
## iter(callable, sentinel) with lambda (Pro-Tip) ##
####################################################
'''
You will often see the sentinel pattern paired with a lambda function.
A common use case is reading a file in chunks until it hits an empty byte string (b'').

with open('large_data.bin', 'rb') as f:
    # lambda f.read(1024) is the callable, b'' is the sentinel
    for block in iter(lambda: f.read(1024), b''): 
        process_block(block)
'''

"""
You rarely need to use this form of iter() manually 
because Python's for loops do this under the hood automatically. 

However, you should use it manually when:
+ You need custom manual iteration: For example, if you want to extract the first item of a collection 
                                    (like a header row in a CSV file) and then process the rest in a standard loop.
+ You are sharing state across loops: Because an iterator remembers where it left off, 
                                      you can pass it to different functions or loops, 
                                      and it will continue exactly where the last one stopped.
"""

#-------------------------------------------------------------------------------#
#-------------------- 3. use "class" to create an Iterator ---------------------#
#-------------------------------------------------------------------------------#
'''
Can use "class" with "__iter__" and "__next__" methods to create a custom iterator.
=> better control over the iteration process, 
   and can maintain internal state across iterations.
'''

######################
## Iterator example ##
######################

class MyRange:
    def __init__(self, n):
        self.n = n
        self.i = 0
        
    def __iter__(self):
        return self  # The object itself is the iterator
    
    def __next__(self):
        if self.i < self.n:
            value = self.i # Store the current value to return
            self.i += 1 # Move to the next value for the next call
            return value
        else:
            raise StopIteration  # Signal that there are no more items to iterate

my_range = MyRange(5)
print(next(my_range))  # Output: 0
print(next(my_range))  # Output: 1

for num in my_range:
    print(num)  # Output: 2, 3, 4 (0 and 1 already consumed)
    
##########################
## Iterable vs Iterator ##
##########################

class MyRangeIterator:
    """Iterator — tracks position, one-use"""
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        val = self.i
        self.i += 1
        return val

class MyRangeIterable:
    """Iterable — can be looped multiple times"""
    def __init__(self, n):
        self.n = n
        
    def __iter__(self):
        return MyRangeIterator(self.n)   # returns a NEW iterator each time

r_iterable = MyRangeIterable(5)
r_iterator = MyRangeIterator(5)

print(next(r_iterator))  # Output: 0
print(next(r_iterator))  # Output: 1
print(list(r_iterator))  # Output: [2, 3, 4] (0 and 1 already consumed)
print(list(r_iterator))  # Output: [] (already exhausted)

print(list(r_iterable))  # Output: [0, 1, 2, 3, 4]
print(list(r_iterable))  # Output: [0, 1, 2, 3, 4] (new iterator created each time)

'''
Because the MyRangeIterable class computes each item one by one
-> more memory efficient for large datasets, as it doesn't store all items in memory at once.
'''


#----------------------------------------------------------------------------------------#
#-------------------- 4. Example: loading big 3D shapes efficiently ---------------------#
#----------------------------------------------------------------------------------------#

