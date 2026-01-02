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


#--------------------------------------------------#
#-------------- Multithreading --------------------#
#--------------------------------------------------#

# GIL = Global Interpreter Lock

'''
Concept: Multiple threads run concurrently within the same process, 
SHARING the SAME memory space (code, data, files) but each thread has its own register and stack.

Use case: Best suited for I/O-bound tasks such as network operations, file reading, 
or waiting for user input, where the program spends time waiting and can switch between threads efficiently.

Performance: Due to Python’s GIL, only one thread executes Python bytecode at a time, 
so multithreading achieves concurrency but not true parallelism for CPU-bound tasks. 
This means multithreading does not speed up CPU-intensive operations in pure Python code.

Advantages: Lightweight, less overhead than multiprocessing, 
efficient for tasks that are I/O-bound, and allows sharing of memory and data easily among threads.

Disadvantages: Requires careful synchronization to avoid race conditions, deadlocks, and data corruption 
since threads share memory.

Implementation: Python provides the "threading" module 
and higher-level interfaces like "concurrent.futures.ThreadPoolExecutor" to manage threads
'''

############ Example WITH multithreading ##################

import time
import threading
import os

print("Number of logical CPUs (threads):", os.cpu_count()) # 16 threads ~ 8 cores

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

thread1 = threading.Thread(target = calc_square, args = (arr, )) # Create thread1 to handle calc_square function
thread2 = threading.Thread(target = calc_cube, args = (arr, ))   # Create thread2 to handle calc_cube function
                                                                 # (arr, ) means that this is a tuple, not just arr itself

thread1.start() # activate thread1 to execute calc_square
thread2.start() # activate thread2 to execute calc_cube

thread1.join() # tell the main program to wait until thread1 terminates its process.
thread2.join() # tell the main program to wait until thread2 terminates its process.
               # This ensures that the main program (or the next lines of code) will only proceed 
               # after the specified thread has completed its task.

# 2² = 4 (the output of thread1 shows up first because it started first, slept first and finished the process first)
# 2³ = 8
# 3² = 9
# 3³ = 27
# 8² = 64
# 8³ = 512
# 9² = 81
# 9³ = 729

print("\nDone double-thread calculating in:", time.time() - t0)
# Done double-thread calculating in: 0.8486087322235107

# In this example, the calc_square and calc_cube functions both have 0.2s sleeping time (time.sleep(0.2))
# thread1 calc_square started first, but then encountered 0.2s sleeping time
# while thread1 is sleeping, the program jumps into thread2 to execute calc_cube function
# So, by jumping back and forth between thread1 and thread2 while the other is sleeping, 
# multithreading helps accelerate the program
# => faster and more EFFICIENT (not truely parrallel)

# This example uses 2 THREADS ~ 1 CORE (not true parallelism, only efficiency here)
# Real-life example: ONE CHEFT, while waiting for the water to be boiled, he can preprocess other foods

# NOTE: since this is multithreading, thread1 and thread2 SHARE THE SAME memory and ressoruce for its process
#       like ONE WORKER handle many tasks but in an efficient way, not one-by-one

# If we defined more threads like 6, then we have 6/2 = 3 CORES (can achive true parallelism)


###################### Dynamic Multithread process using "threading" and "ThreadPoolExecutor" #########################
###################### Enable defining the maximum number of threads (worker) to use          #########################
###################### Automatically create thread, start thread and join thread              #########################

##### Return an output list #####

import threading
from concurrent.futures import ThreadPoolExecutor

def target_function(single_block):
    # Replace with your actual processing logic
    # For demonstration, this target_function return the reversed version of the input as single_block
    return single_block[::-1]

def multithread_process(input_blocks, max_threads=4):
    """
    input_blocks: List of input blocks (2D list, each element of this list is a single_block input list)
    max_threads: maximum number of concurrent threads
    Returns: List of output blocks corresponding to input blocks
    """
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(fn=target_function, single_block=block) for block in input_blocks]
        output_blocks = [future.result() for future in futures]

    return output_blocks

# Example usage:
inputs = [
    [1, 2, 3],
    ['a', 'b', 'c'],
    [10, 20, 30, 40],
    [100, 200],
    ['x', 'y', 'z']
]

outputs = multithread_process(input_blocks=inputs, max_threads=4)
print(outputs)
# Output: [[3, 2, 1], ['c', 'b', 'a'], [40, 30, 20, 10], [200, 100], ['z', 'y', 'x']]


##### Write outputs into  files #####

from concurrent.futures import ThreadPoolExecutor

def target_function(single_block):
    # Replace with your actual processing logic
    # For demonstration, return the reversed version of the input block as a string
    return str(single_block[::-1])

def write_output_file(idx, single_block, output_dir):
    import os
    result = target_function(single_block)
    output_file = os.path.join(output_dir, f"output_{idx}.txt")
    with open(output_file, "w") as f:
        f.write(result)

def multithread_process(input_blocks, max_threads=4, output_dir="outputs"):
    import os
    os.makedirs(output_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(fn=write_output_file, idx=index, single_block=block, output_dir=output_dir) 
                   for index, block in enumerate(input_blocks)]
        
        for future in futures:
            future.result()  # Wait for all threads to finish

# Example usage:
inputs = [
    [1, 2, 3],
    ['a', 'b', 'c'],
    [10, 20, 30, 40],
    [100, 200],
    ['x', 'y', 'z']
]

multithread_process(input_blocks=inputs, max_threads=4, output_dir="output_files")

# After running, you will find files output_0.txt, output_1.txt, ..., output_4.txt in the "output_files" folder,
# each containing the reversed block as a string.


#-------------------------------------------------------------#
#-------------- using a list of tuples as argument -----------#
#-------------------------------------------------------------#

from concurrent.futures import ThreadPoolExecutor

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
    with ThreadPoolExecutor(max_workers=4) as executor:
        results_multi = list(executor.map(lambda args: add_numbers(*args), multi_arg_inputs))
    print(f"Multi-arg results: {results_multi}")  # [3, 7, 11]
    
    # ✅ Single-argument inputs using list comprehension (note the comma for tuple)
    single_arg_inputs = [(i,) for i in range(2, 6)]  # [(2,), (3,), (4,), (5,)]
    with ThreadPoolExecutor(max_workers=4) as executor:
        results_single = list(executor.map(lambda args: square(*args), single_arg_inputs))
    print(f"Single-arg results: {results_single}")  # [4, 9, 16, 25]
    
    # ✅ Three-argument inputs using list comprehension
    three_arg_inputs = [(i, i*2, i+1) for i in range(1, 4)]  # [(1, 2, 2), (2, 4, 3), (3, 6, 4)]
    with ThreadPoolExecutor(max_workers=4) as executor:
        results_three = list(executor.map(lambda args: calculate(*args), three_arg_inputs))
    print(f"Three-arg results: {results_three}")  # [4, 11, 22]


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
