'''
In Python, a lazy iterable (iterator) is an object that computes its elements one at a time only when requested,
rather than storing them all in memory upfront.
This behavior is known as lazy evaluation.

While common iterables like lists and tuples are "eager"
(meaning they store all their data in RAM immediately),
lazy iterables (iterators) use a "just-in-time" approach.
This makes them essential for handling massive datasets or infinite sequences
that would otherwise crash your program due to memory limits.

##------------------##

1. ``yield`` and next()
2. iter() converts iterable to iterator
3. use "class" to create custom Iterable and Iterator
4. Example: loading big 3D shapes efficiently and batch-wise
'''


# =========================================================================================
# 1. ``yield`` and next()
# =========================================================================================
'''
In Python, yield is a keyword used to create generators.
Unlike a standard return statement, which exits a function and destroys its local state,
yield pauses the function, saves all of its variables, and sends a value back to the caller.
When the function is called again, it resumes exactly where it left off.

##----------------------##

The next() function is a built-in Python tool used to manually retrieve the subsequent item from an iterator
(like a generator, map object, or any object created with iter()
'''

##----------------------##
## simple yield example ##
##----------------------##

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
'''TypeError: 'generator' object is not subscriptable'''

##-----------------##
## yield with loop ##
##-----------------##

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

# =========================================================================================

def for_yield(n):
    for i in range(n):
        yield i

for_gen = for_yield(3)

print(next(for_gen))  # Output: 0
print(next(for_gen))  # Output: 1
print(next(for_gen))  # Output: 2
print(next(for_gen))  # Raises StopIteration, as there are no more items to yield

##-------------------------------------------##
## Use ``()`` expression to create generator ##
##-------------------------------------------##

# List comprehension — realized immediately, subscriptable
squares_list = [x**2 for x in range(5)]
print(squares_list) # [0, 1, 4, 9, 16]

# Generator expression — lazy, uses () instead of []
squares_gen = (x**2 for x in range(5))
print(squares_gen) # <generator object <genexpr> at 0x7f7b083ba810>

next(squares_gen)   # 0
next(squares_gen)   # 1
list(squares_gen)   # [4, 9, 16]  (0 and 1 already consumed!)

##---------------------##
## Realize a generator ##
##---------------------##

def fibonacci_gen(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

fib_gen = fibonacci_gen(10)

fib_series = list(fib_gen) # can be tuple(), set(), dict() etc. as well
print(fib_series)
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# =========================================================================================
# 2. iter() converts iterable to iterator
# =========================================================================================
'''
In Python, the iter() function is a built-in tool that takes an object and turns it into an iterator.

To understand iter(), it helps to know the difference between two key Python concepts:
+ Iterable: A collection of items you can loop over (like a list, string, dictionary, or tuple).
+ Iterator: An engine that knows how to fetch items from an iterable one by one.
            (Note: All generators are iterators, but not all iterators are generators!)
            It remembers its current state and uses the next() function to get the next item
            until there are no items left.
'''

##----------------##
## iter() example ##
##----------------##

fruits = ["apple", "banana", "cherry"]
print(fruits[1]) # banana

fruits_iter = iter(fruits)  # Convert the list to an iterator
print(fruits_iter) # <list_iterator object at 0x7217285f9810>
print(next(fruits_iter))  # apple
print(fruits_iter[0]) # TypeError: 'list_iterator' object is not subscriptable

##----------------------------------##
## iter(callable, sentinel) example ##
##----------------------------------##

import random

def roll_dice(): # A callable that simulates rolling a six-sided die
    return random.randint(1, 6)

def roll_until_n(n):
    # assert 1 <= n <= 6, "n must be between 1 and 6"
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

'''
NOTE: if the sentinel is not in the value domain of the callable, it will run forever
'''

##------------------------------------------------##
## iter(callable, sentinel) with lambda (Pro-Tip) ##
##------------------------------------------------##
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


# =========================================================================================
# 3. use "class" to create custom Iterable and Iterator
# =========================================================================================
'''
Can use "class" with "__iter__" and "__next__" methods to create a custom iterator.
=> better control over the iteration process,
   and can maintain internal state across iterations.
'''

##------------------##
## Iterator example ##
##------------------##

class MyRange:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self): # This allows iter(instance)
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

##----------------------##
## Iterator vs Iterable ##
##----------------------##

class MyRangeIterator:
    """Iterator — tracks position, one-use"""
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self): # This allows iter(instance)
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        val = self.i
        self.i += 1
        return val

r_iterator = MyRangeIterator(5)

print(next(r_iterator))  # Output: 0
print(next(r_iterator))  # Output: 1
print(list(r_iterator))  # Output: [2, 3, 4] (0 and 1 already consumed)
print(list(r_iterator))  # Output: [] (already exhausted)

# =========================================================================================

class MyRangeIterable:
    """Iterable — can be looped multiple times"""
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return MyRangeIterator(self.n) # returns a NEW iterator each time calling iter(instance)

r_iterable = MyRangeIterable(5)

print(list(r_iterable))  # Output: [0, 1, 2, 3, 4]
print(list(r_iterable))  # Output: [0, 1, 2, 3, 4] (new iterator created each time)

active_iterator = iter(r_iterable) # Must use iter() to convert iterable into iterator first before next()
print(next(active_iterator)) # 0, then 1, then 2, ...
print(next(r_iterable)) # TypeError: 'MyRangeIterable' object is not an iterator

for item in r_iterable:
    print(item)
# 0
# 1
# 2
# 3
# 4
# This doesn't break like next(r_iterable)
# because when using for loop, Python implicitly does iter(r_iterable) for us

'''
Because the MyRangeIterable class computes each item one by one
-> more memory efficient for large datasets, as it doesn't store all items in memory at once.
'''


# =========================================================================================
# 4. Example: loading big 3D shapes efficiently
# =========================================================================================

from pathlib import Path
import numpy as np
from plotly import graph_objects as go

data_dir = Path("/home/").glob("**/3D_structures/")  # Create a generator that yields matching directories
data_dir = next(data_dir)  # Get the first matching directory

##---------------------------------##
## Utilize the generator from Path ##
##---------------------------------##

data_iterator = data_dir.glob("*.npy")

def plot_iterator_single(iterator):
    path = next(iterator)
    structure = np.load(path)
    structure = structure - structure.mean(axis=0) # center the structure to origin

    shared_range = [structure.min(), structure.max()]

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=structure[:, 0],
        y=structure[:, 1],
        z=structure[:, 2],
        mode='markers+lines',
        marker=dict(size=5, color='green'),
        line=dict(color='brown', width=2)
    ))

    fig.update_layout(
        title=f'{path.stem}',
        # width=800,
        # height=600,
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis',
            xaxis=dict(range=shared_range),
            yaxis=dict(range=shared_range),
            zaxis=dict(range=shared_range)
        )
    )

    fig.show()

# =========================================================================================

plot_iterator_single(data_iterator)

##-------------------------------------------------------------##
## Create custom Iterator with class to yield multiple objects ##
##-------------------------------------------------------------##

import random

class StructureLoader():
    def __init__(self, entries: list[Path], batch_size: int = 1, shuffle: bool = False):
        if not isinstance(entries, list):
            entries = sorted(list(entries))

        self.entries = entries
        self.shuffle = shuffle
        self.entries = entries
        self.batch_size = batch_size

    def __iter__(self):
        if self.shuffle:
            random.shuffle(self.entries)
        return StructureIterator(self.entries, self.batch_size)

class StructureIterator():
    def __init__(self, entries: list[Path], batch_size: int = 1):
        self.batch_size = batch_size
        self.entries = entries
        self.n = len(entries)
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration

        start = self.i
        end = self.i + self.batch_size
        entries_batched = self.entries[start:end]
        # entries_batched = self.entries[self.i:self.i + self.batch_size]

        self.i += self.batch_size # update iterator indices

        # Load structures from entries_batched
        batch = []
        for entry in entries_batched:
            structure = np.load(entry)
            structure = structure - structure.mean(0)
            batch.append(structure)

        return batch

# =========================================================================================

def plot_iterator_multi(iterator, colors):
    structures = next(iterator)
    num_structures = len(structures)

    colors = colors[:num_structures]

    fig = go.Figure()
    min_values = []
    max_values = []

    for idx, (structure, color) in enumerate(zip(structures, colors), start=1):

        min_values.append(structure.min())
        max_values.append(structure.max())

        fig.add_trace(go.Scatter3d(
            x=structure[:, 0],
            y=structure[:, 1],
            z=structure[:, 2],
            mode='markers+lines',
            marker=dict(size=5, color=color),
            line=dict(color='black', width=2),
            name=f"Structure {idx}"
        ))

    shared_range = [min(min_values), max(max_values)]

    fig.update_layout(
        title=f'3D structure visualization',
        # width=800,
        # height=600,
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis',
            xaxis=dict(range=shared_range),
            yaxis=dict(range=shared_range),
            zaxis=dict(range=shared_range)
        )
    )

    fig.show()

# =========================================================================================

entries = data_dir.glob("*.npy")

structure_loader = StructureLoader(entries, 2, True)
structure_iterator = iter(structure_loader) # convert the loader(iterable) into iterator for next()
for entry in structure_iterator.entries:
    print(entry.stem)

colors = ["#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a"]
random.shuffle(colors)
plot_iterator_multi(structure_iterator, colors)

##---------------------------------------##
## Create a MiniLoader for batching data ##
##---------------------------------------##

class MiniLoader:
    def __init__(
        self, data: list[np.ndarray],
        batch_size: int = 1,
        n_subset=None,
        shuffle: bool = True,
    ):
        self.data = data
        self.batch_size = batch_size
        self.n_subset = n_subset
        self.shuffle = shuffle

    def __iter__(self):
        data = self.data
        if self.shuffle:
            random.shuffle(data)
        return MiniIterator(data[:self.n_subset], self.batch_size)

class MiniIterator:
    def __init__(self, data: list[np.ndarray], batch_size: int = 1):
        self.data = data
        self.batch_size = batch_size
        self.n = len(data)
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration

        start = self.i
        end = self.i + self.batch_size

        batch = self.data[start:end]

        self.i += self.batch_size

        return batch

# =========================================================================================

entries = data_dir.glob("*.npy")
structures_list = []
for entry in entries:
    structure = np.load(entry)
    structure = structure - structure.mean(axis=0)
    structures_list.append(structure)

loader = MiniLoader(
    data=structures_list,
    batch_size=3,
    shuffle=True,
    n_subset=6
)

for batch_idx, batch in enumerate(loader, start=1):
    print(f"Batch: {batch_idx}")
    print(batch)
    print("="*30)

##----------------------------------------------------------------##
## SourceContainer - TargetContainer - PairContainer - DataLoader ##
##----------------------------------------------------------------##

from pathlib import Path
import numpy as np
from plotly import graph_objects as go
from sklearn.mixture import GaussianMixture
import joblib

data_dir = Path("/home/longdpt/").rglob("*/data/3D_structures")
data_dir = next(data_dir)
entries = sorted(list(data_dir.glob("*.npy")))

data_list = []
for entry in entries:
    data = {
        "path": entry,
        "structure": np.load(entry)
    }
    data_list.append(data)

# =========================================================================================

class SourceContainer:
    def __init__(self, data: list[dict[Path, np.ndarray]]):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        arr = self.data[idx]["structure"]
        arr = arr - arr.mean(axis=0)
        arr = arr.astype(np.float32)

        shape_name = self.data[idx]["path"].stem
        return {"shape_name": shape_name, "coords": arr}

# =========================================================================================

class TargetContainer:
    def __init__(
        self,
        input_data: list[dict[Path, np.ndarray]],
        n_components: int = 50,
        random_state: int = None
    ):
        self.gmm = []
        self.gmm_paths = []

        for data in input_data:
            coords = data["structure"].astype(np.float64)

            path = data["path"]
            gmm_path = path.parent / f"{path.stem}.pkl"
            self.gmm_paths.append(gmm_path)

            if gmm_path.is_file():
                gmm = joblib.load(gmm_path)
            else:
                gmm = GaussianMixture(n_components=n_components, max_iter=500, tol=1e-4, reg_covar=1e-4, random_state=random_state)
                gmm = gmm.fit(coords)
                joblib.dump(value=gmm, filename=gmm_path)

            self.gmm.append(gmm)

    def __len__(self):
        return len(self.gmm)

    def __getitem__(self, idx):
        gmm = self.gmm[idx]

        n_points = np.random.randint(300, 400)
        target, _ = gmm.sample(n_points)

        target = target - target.mean(axis=0)
        target = target.astype(np.float32)

        return {"gmm_path": self.gmm_paths[idx], "coords": target}

# =========================================================================================

class PairContainer:
    def __init__(self, source: SourceContainer, target: TargetContainer):
        self.source = source
        self.target = target

    def __len__(self):
        return min(len(self.source), len(self.target))

    def __getitem__(self, idx):
        source_item = self.source[idx]
        target_item = self.target[idx]

        return source_item, target_item

# =========================================================================================

class DataLoader:
    def __init__(self, data, batch_size=2, n_subset=None, shuffle=True, collate_fn=None):
        self.data = data
        self.batch_size = batch_size
        self.n_subset = n_subset
        self.shuffle = shuffle
        self.collate_fn = collate_fn

        self.indices = list(range(len(data)))

    def __len__(self):
        n = len(self.indices) if self.n_subset is None else min(self.n_subset, len(self.indices))
        return (n + self.batch_size - 1) // self.batch_size

    def __iter__(self):
        if self.shuffle:
            random.shuffle(self.indices)

        data = [self.data[idx] for idx in self.indices[:self.n_subset]]
        return DataIterator(data, self.indices, self.batch_size, self.collate_fn)
       # [pair0, pair1, pair2, pair3, pair4] -> 0, 1, 2, 3, 4 -> 0, 3, 1, 2, 4 -> 0, 3, 1, 2 -> [pair0, pair3, pair1, pair2]

class DataIterator:
    def __init__(self, data, indices, batch_size, collate_fn):
        self.data = data # [pair0, pair3, pair1, pair2]
        self.indices = indices
        self.batch_size = batch_size
        self.collate_fn = collate_fn

        self.n = len(self.indices)
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration

        batch_indices = self.indices[self.i:self.i + self.batch_size]
        batch = [self.data[idx] for idx in batch_indices] # [pair0, pair3], then [pair1, pair2]

        self.i += self.batch_size

        if self.collate_fn is not None:
            return self.collate_fn(batch) # collate_fn([pair0, pair3]), then collate_fn([pair1, pair2])

        return batch

# =========================================================================================

def collate_fn_flat(batch):
    src_batch = []
    tgt_batch = []

    src_counts = []
    tgt_counts = []

    src_idx_list = []
    tgt_idx_list = []

    for batch_idx, (source, target) in enumerate(batch): # pair = (source, target), pair0 <-> batch_idx=0, pair3 <-> batch_idx=1, ...
        src_len = len(source["coords"])
        tgt_len = len(target["coords"])

        src_counts.append(src_len)
        tgt_counts.append(tgt_len)

        src_idx_list.append(np.full((src_len,), batch_idx, dtype=np.int64))
        tgt_idx_list.append(np.full((tgt_len,), batch_idx, dtype=np.int64))

        src_batch.append(source["coords"])
        tgt_batch.append(target["coords"])

    return {
        "source": {
            "coords": np.concatenate(src_batch, axis=0),
            "batch_idx": np.concatenate(src_idx_list, axis=0),
            "counts": np.array(src_counts)
        },

        "target": {
            "coords": np.concatenate(tgt_batch, axis=0),
            "batch_idx": np.concatenate(tgt_idx_list, axis=0),
            "counts": np.array(tgt_counts)
        }
    }

# =========================================================================================

source_container = SourceContainer(data_list)
target_container = TargetContainer(data_list, n_components=50)
pair_container = PairContainer(source_container, target_container)

data_loader = DataLoader(pair_container, batch_size=2, shuffle=True, collate_fn=collate_fn_flat)

data_iter = iter(data_loader)

batch = next(data_iter)
print(batch)
