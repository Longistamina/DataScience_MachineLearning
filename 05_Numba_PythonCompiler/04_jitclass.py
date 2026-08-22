'''
``@jitclass`` is used for compiling Python class (numba.experimental.jitclass).

All methods of a jitclass are compiled into nopython functions.

The data of a jitclass instance is allocated on the heap as a C-compatible structure
so that any compiled functions can have direct access to the underlying data, bypassing the interpreter.
'''

import numba as nb
from numba.experimental import jitclass

from numba.typed import List as NumbaList

import numpy as np

from typing import List


# =========================================================================================
# 1. Manual signatures specifying
# =========================================================================================

spec = [
    ('value', nb.int32),     # a simple scalar field
    ('array', nb.float32[:]) # an array field
]
'''
The tuples contain the name of the field and the Numba type of the field.

Alternatively, user can use a dictionary (an OrderedDict preferably for stable field ordering),
which maps field names to types.
'''

@jitclass(spec)
class Bag(object):
    def __init__(self, value):
        self.value = value
        self.array = np.zeros(value, dtype=np.float32)

    @property
    def size(self):
        return self.array.size

    def increment(self, val):
        for i in range(self.size):
            self.array[i] += val
        return self.array

    @staticmethod
    def add(x, y):
        return x + y

bag_shape = 5
mybag = Bag(bag_shape)
print(mybag.array)
# [0. 0. 0. 0. 0.]

mybag.increment(3.5)
print(mybag.array)
# [3.5 3.5 3.5 3.5 3.5]


# =========================================================================================
# 2. Automatic specs inference
# =========================================================================================
'''
Normally, when creating a jitclass, you have to explicitly write out a spec list
matching every single class variable to its specific Numba type.
-> This can get tedious :(((

This feature allows Numba to look at your standard Python type hints (annotations)
and automatically build that spec for you behind the scenes using a function called ``as_numba_type``

NOTE: ``np.ndarray`` is not allowed
(Numba requires knowing the dtype and rank of NumPy arrays, which cannot currently be expressed with type annotations)
-> Must use ``spec = [('array', nb.float32[:])]``
'''

@jitclass # No need ``spec`` (excepts Numpy arrays)
class Counter:
    value: int # Python type hint (annotation)

    def __init__(self):
        self.value = 0

    def get(self) -> int:
        ret = self.value
        self.value += 1
        return ret # every ``.get()`` call will increase ``ret`` by 1

@jitclass
class ListLoopIterator:
    counter: Counter
    items: List[float]
    # z: np.ndarray (THIS IS NOT ALLOWED)

    def __init__(self, items): # No need ``items: List[float]``, numba will ignore this
        self.counter = Counter()
        self.items = items

    def get(self) -> float:
        idx = self.counter.get() % len(self.items) # ``%`` to loop back to the first element when idx exceeds len
        return self.items[idx]

items = NumbaList([3.14, 2.718, 0.123, -4.])
loop_itr = ListLoopIterator(items)

print(loop_itr.get())
# 3.14, then 2.718,... then back to 3.14, ...


# =========================================================================================
# 3. Other containers: numba.typed.Dict and numba.typed.List
# =========================================================================================

##------------------##
## numba.typed.List ##
##------------------##

nb_list = nb.typed.List() # create empty numba list

nb_list.extend(np.random.randn(10).round(2)) # Update values for the empty numba list
print(nb_list)
# [0.65, 1.82, 0.4, 0.04, 0.41, -0.64, -0.91, -0.93, 2.47, -0.91]

# Custom Container -------------

inner_list_type = nb.types.ListType(nb.types.float64)

class NumbaListContainer:
    def __init__(self, raw_matrix):

        self.matrix = nb.typed.List.empty_list(inner_list_type) # Create empty numba list

        for row in raw_matrix:
            # Convert regular integers/floats to explicit float values
            float_row = [float(item) for item in row]

            # Create the inner Numba Typed List instance
            numba_row = nb.typed.List(float_row)

            # Safely append it to our outer list
            self.matrix.append(numba_row)

# Mixed integer and float matrix
data = [
    [1.1, 2.2, 3.3],
    [4, 5, 6, 7],      # Dynamic lengths are fine for lists!
    [-1.5, 0.0]
]

list_container = NumbaListContainer(data)
print(list_container.matrix)
# [[1.1, 2.2, 3.3], [4.0, 5.0, 6.0, 7.0], [-1.5, 0.0]]

##------------------##
## numba.typed.Dict ##
##------------------##

nb_dict = nb.typed.Dict()

input_dict = {"one": 1, "two": 2, "three": 3}

nb_dict.update(input_dict)
print(nb_dict)
# {one: 1, two: 2, three: 3}

# Custom Container -------------

# key and value types
kv_types = (nb.types.unicode_type, nb.types.ListType(nb.types.float64))
# ``nb.types.unicode_type`` for key string
# ``nb.types.ListType(nb.types.float64)`` is for list of float values

class NumbaDictContainer:
    def __init__(self, kwargs):
        self.dict = nb.typed.Dict.empty(*kv_types) # Create empty dict with specified kv types

        for k, v in kwargs.items(): # Put inputs kv into the empty dict
            float_values = [float(item) for item in v] # Force all to become float
            self.dict[k] = nb.typed.List(float_values)

dict_container = NumbaDictContainer({
    "Real": [1.2, 3.5, -6.7, 8.9],
    "Quotient": [2, -2, 4, 4, 0]
})

print(dict_container.dict)
# {Real: [1.2, 3.5, -6.7, 8.9], Quotient: [2.0, -2.0, 4.0, 4.0, 0.0]}
