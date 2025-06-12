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
