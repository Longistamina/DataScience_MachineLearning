############ Example WITHOUT multithreading or multiprocessing ##############

import time

def calc_square(numbers):
    print("Calculate square numbers:")
    for n in numbers:
        time.sleep(0.2) # delay 0.2s in each loop
        print(f"{n}{chr(178)} = {n**2}")

def calc_cube(numbers):
    print("Calculate cube of numbers:")
    for n in numbers:
        time.sleep(0.2) # delay 0.2s in each loop
        print(f"{n}{chr(179)} = {n**3}")

arr = [2, 3, 8, 9]

t0 = time.time() # Return the current time in second (before calculating)
calc_square(arr)
print()
calc_cube(arr)

print("\nDone single-thread calculating in:", time.time() - t0) # Get the current time after calculating
                                                                # Then subtract t0 (before calculating)
                                                                # => results in the processing time
                                                                # Done single-thread calculating in: 1.6027076244354248

# In this example, the calc_square and calc_cube functions both have 0.2s sleeping time (time.sleep(0.2))
# function calc_square will keep processing, then sleeping, then processing, then sleeping .... til the end
# After function calc_square terminates its process, function calc_cube will jump in
# Then, like before, calc_cube will also keep processing, then sleeping, then processing, ... til the end
# => Make the total processing time delayed and cost upto 1.602s to finish


#--------------------------------------------------------#
#---------------- Multiprocessing -----------------------#
#--------------------------------------------------------#

# GIL = Global Interpreter Lock

'''
Concept: Multiple processes run in parallel, each with its SEPARATE memory space, code, and data. 
This isolates processes from each other, avoiding shared memory issues.

Use case: Ideal for CPU-bound tasks that require heavy computation 
and can benefit from multiple CPU cores running in parallel.

Performance: Multiprocessing bypasses the GIL by running separate Python interpreters in each process, 
enabling true parallelism.

Advantages: Avoids GIL limitations, improves performance for CPU-intensive tasks, provides process isolation which enhances reliability and data integrity.

Disadvantages: Higher overhead due to process creation and inter-process communication, more memory consumption, and more complex implementation for sharing data between processes.

Implementation: Python’s "multiprocessing" module allows creation of processes similar to threading, 
with APIs like "Process" and "Pool" for managing multiple processes
'''

############ Example WITH multiprocessing ##################

import time
import multiprocessing
import os

print("Number of logical CPUs (threads):", os.cpu_count()) # 16 threads ~ 8 cores

def calc_square(numbers):
    print("Calculate square numbers:")
    for n in numbers:
        time.sleep(0.2) # delay 0.2s in each loop (can set to 10s then go to task manager to check the core usage)
        print(f"{n}{chr(178)} = {n**2}")

def calc_cube(numbers):
    print("Calculate cube of numbers:")
    for n in numbers:
        time.sleep(0.2) # delay 0.2s in each loop (can set to 10s then go to task manager to check the core usage)
        print(f"{n}{chr(179)} = {n**3}")

arr = [2, 3, 8, 9]

t0 = time.time() # Return the current time in second (before calculating)

processor1 = multiprocessing.Process(target = calc_square, args = (arr, )) # Create processor1 to handle calc_square function
processor2 = multiprocessing.Process(target = calc_cube, args = (arr, ))   # Create processor2 to handle calc_cube function
                                                                           # (arr, ) means that this is a tuple, not just arr itself
                                                                           # Processor here is one CPU CORE

processor1.start() # activate processor1 to execute calc_square
processor2.start() # activate processor2 to execute calc_cube

processor1.join() # tell the main program to wait until processor1 terminates its process.
processor2.join() # tell the main program to wait until processor2 terminates its process.
                  # This ensures that the main program (or the next lines of code) will only proceed 
                  # after the specified processor has completed its task.


###################### Dynamic Multitprocess using "Pool" from "multiprocessing"          #########################
###################### Enable defining the maximum number of processors (cores) to use    #########################
###################### Automatically create processor, start processor and join processor #########################

###### Return an output list ######

from multiprocessing import Pool

def target_function(single_block):
    # Replace with your actual processing logic
    # For demonstration, return the reversed version of the input block
    return single_block[::-1]

def multicore_process(input_blocks, max_processes=4):
    """
    input_blocks: List of input blocks (2D list)
    max_processes: maximum number of concurrent processes
    Returns: List of output blocks corresponding to input blocks
    """
    with Pool(processes=max_processes) as pool:
        # map applies target_function to each input block in parallel
        output_blocks = pool.map(func=target_function, iterable=input_blocks)
    return output_blocks

# Example usage:
inputs = [
    [1, 2, 3],
    ['a', 'b', 'c'],
    [10, 20, 30, 40],
    [100, 200],
    ['x', 'y', 'z']
]

outputs = multicore_process(inputs, max_processes=4)
print(outputs)
# Output: [[3, 2, 1], ['c', 'b', 'a'], [40, 30, 20, 10], [200, 100], ['z', 'y', 'x']]


####### save output to multiple files #######

from multiprocessing import Pool
import os

def target_function(single_block, idx):
    # Example: write reversed block to a unique file
    output = str(single_block[::-1])
    output_file = f"output_block_{idx}.txt"
    with open(output_file, "w") as f:
        f.write(output)

def multicore_process(input_blocks, max_processes=4):
    with Pool(processes=max_processes) as pool:
        # Use starmap to pass index along with block
        pool.starmap(funct = target_function, iterable = [(block, i) for i, block in enumerate(input_blocks)])

# Example usage
inputs = [
    [1, 2, 3],
    ['a', 'b', 'c'],
    [10, 20, 30, 40],
]

multicore_process(inputs, max_processes=3)
# This creates files output_block_0.txt, output_block_1.txt, output_block_2.txt


#-------------------------------------------------------------#
#----------- using a list of tuples as argument --------------#
#-------------------------------------------------------------#

import multiprocessing

# Function with two parameters
def add_numbers(x, y):
    return x + y

# Function with single parameter
def square(x):
    return x ** 2

# Function with three parameters
def calculate(x, y, z):
    return x * y + z

if __name__ == '__main__':
    
    # ✅ Multi-argument inputs using list comprehension
    multi_arg_inputs = [(i, i+1) for i in range(1, 7, 2)]  # [(1, 2), (3, 4), (5, 6)]
    with multiprocessing.Pool() as pool:
        results_multi = pool.starmap(func=add_numbers, iterable=multi_arg_inputs)
    print(f"Multi-arg results: {results_multi}")  # [3, 7, 11]
    
    # ✅ Single-argument inputs using list comprehension (note the comma for tuple)
    single_arg_inputs = [(i,) for i in range(2, 6)]  # [(2,), (3,), (4,), (5,)]
    with multiprocessing.Pool() as pool:
        results_single = pool.starmap(func=square, iterable=single_arg_inputs)
    print(f"Single-arg results: {results_single}")  # [4, 9, 16, 25]
    
    # ✅ Three-argument inputs using list comprehension
    three_arg_inputs = [(i, i*2, i+1) for i in range(1, 4)]  # [(1, 2, 2), (2, 4, 3), (3, 6, 4)]
    with multiprocessing.Pool() as pool:
        results_three = pool.starmap(func=calculate, iterable=three_arg_inputs)
    print(f"Three-arg results: {results_three}")  # [4, 11, 22]
    
    # ✅ More complex comprehension examples
    # Creating pairs from two different ranges
    complex_inputs = [(x, y) for x in range(1, 4) for y in range(10, 13)]
    # [(1, 10), (1, 11), (1, 12), (2, 10), (2, 11), (2, 12), (3, 10), (3, 11), (3, 12)]
    
    # Using conditional comprehension
    conditional_inputs = [(i,) for i in range(10) if i % 2 == 0]  # [(0,), (2,), (4,), (6,), (8,)]
    
    print(f"Complex inputs: {complex_inputs[:3]}...")  # Show first 3
    print(f"Conditional inputs: {conditional_inputs}")


#---------------------------------------------------------------------------------#
#----------- difference between Multithreading and Multiprocessing ---------------#
#---------------------------------------------------------------------------------#

'''
Aspect               | Multithreading                       | Multiprocessing
---------------------|--------------------------------------|---------------------------
Execution            | Multiple threads in one process      | Multiple processes with separate memory
Memory Sharing       | Shared memory space                  | Separate memory spaces
GIL Impact           | Limited by GIL, concurrency only     | Not limited by GIL, true parallelism
Best for             | I/O-bound tasks                      | CPU-bound tasks
Overhead             | Lower overhead                       | Higher overhead
Complexity           | Needs synchronization (locks, etc.)  | More complex IPC and data sharing
Performance          | No speedup for CPU-bound Python code | Speedup for CPU-bound tasks
'''
