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
    output_blocks = [None] * len(input_blocks) # Create initial ouput_blocks = [None, None, None .... None]

    def worker(idx, single_block): # worker here is thread
        output_blocks[idx] = target_function(single_block)
        # replace each None with the corresponding output of target_function(single_block)

    with ThreadPoolExecutor(max_workers=max_threads) as executor: 
        # create an executer object (from class ThreadPoolExecutor)
        # this is like "thread_name = threading.Thread()"" but more advanced
        # this executor's thread pool has the maximum number of threads = max_workers = max_threads
        
        futures = [] # This futures list will store all the workers (threads) created by the executor.submit() below
        for idx, single_block in enumerate(input_blocks):
            futures.append(executor.submit(worker, idx, single_block))
            # executor submits tasks defined with arguments like worker, idx and single_block to the thread pool
            # so executor.submit() is like thread_name.start()
            # then add the created thread/worker to the futures list

        for future in futures:
            future.result() # Wait for all threads/workers to complete before moving on the next part
                            # this is like thread_name.join()

    return output_blocks

# Example usage:
inputs = [
    [1, 2, 3],
    ['a', 'b', 'c'],
    [10, 20, 30, 40],
    [100, 200],
    ['x', 'y', 'z']
]

outputs = multithread_process(input_blocks = inputs, max_threads=4)
print(outputs)
# Output: [[3, 2, 1], ['c', 'b', 'a'], [40, 30, 20, 10], [200, 100], ['z', 'y', 'x']]


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
        time.sleep(0.2) # delay 0.2s in each loop
        print(f"{n}{chr(178)} = {n**2}")

def calc_cube(numbers):
    print("Calculate cube of numbers:")
    for n in numbers:
        time.sleep(0.2) # delay 0.2s in each loop
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
                  # after the specified process has completed its task.


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
