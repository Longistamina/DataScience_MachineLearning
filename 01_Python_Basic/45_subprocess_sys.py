'''

Python has subprocess module which is used to spawn new processes, connect to their input/output/error pipes,
and obtain their return codes. 

The subprocess module allows you to run external commands and programs from within Python.

subprocess is the recommended way to run external commands in Python. 
It replaces older methods like os.system() and os.popen().

The subprocess module provides several functions and classes to work with subprocesses:
# subprocess.run() - Recommended for most use cases. Runs a command and waits for it to complete (Python 3.5+).
# subprocess.Popen() - Advanced class for more complex subprocess management with fine-grained control.


Important parameters for subprocess.run():
# args - Command to execute (list or string).
# capture_output - If True, captures stdout and stderr (Python 3.7+).
# stdout - Redirect stdout (subprocess.PIPE, subprocess.DEVNULL, or file object).
# stderr - Redirect stderr (subprocess.PIPE, subprocess.DEVNULL, subprocess.STDOUT, or file object).
# stdin - Redirect stdin (subprocess.PIPE, subprocess.DEVNULL, or file object).
# shell - If True, executes command through the shell (security risk with untrusted input).
# text - If True, decodes stdout/stderr as text strings (Python 3.7+).
# encoding - Specifies encoding for text mode (e.g., 'utf-8').
# timeout - Maximum seconds to wait for the command to complete.
# check - If True, raises CalledProcessError if the command returns non-zero exit code.
# cwd - Sets the working directory for the command.
# env - Dictionary of environment variables for the subprocess.

######################################

Table of Contents:

1. Basic subprocess usage - subprocess.run()
- Running a simple command
- Capturing output with capture_output=True
- Using shell=False vs shell=True (for pipe with "|", must use shell=True)
- Checking return codes
- Using check=True for error handling

2. Working with input/output
- Redirecting stdout and stderr
- Providing input to a subprocess (stdin)
- Decoding output with text=True
- Reading output line by line

3. Advanced subprocess.Popen()
- Creating a Popen object
- Communicating with subprocess using communicate()
- Using poll() to check if process is running
- Using wait() with timeout
- Sending signals to subprocess (terminate, kill)

4. Error handling and security
- Handling CalledProcessError
- Handling TimeoutExpired
- Security considerations with shell=True
- Safely passing arguments

5. Advanced patterns
- Running commands in a different directory (cwd)
- Setting environment variables
- Piping between multiple commands
- Running background processes

'''

import subprocess
import sys
import os

#---------------------------------------------------------------------------------------------#
#--------------------------- Basic subprocess usage - subprocess.run() -----------------------#
#---------------------------------------------------------------------------------------------#

##############################
## Running a simple command ##
##############################
'''
subprocess.run() is the recommended way to run external commands
It runs the command and waits for it to complete, then returns a CompletedProcess object
'''

#----
## Example 1: Run 'echo' command (cross-platform example)
#----

result = subprocess.run(['echo', 'Hello, World!'])
# Hello, World!

print(result)
# CompletedProcess(args=['echo', 'Hello, World!'], returncode=0)

print(type(result))
# <class 'subprocess.CompletedProcess'>

print(result.returncode)
# 0
# (Return code 0 means the command executed successfully)

#----
## Example 2: List directory contents (Linux/Mac)
#----

result = subprocess.run(['ls', '-l'])
# (This will print directory contents to the terminal)
'''
total 19468
drwxr-xr-x 5 longdpt longdpt     4096 Nov 20 22:12 00_Course_Intro
drwxr-xr-x 4 longdpt longdpt     4096 Jan  1 21:27 01_Python_Basic
drwxr-xr-x 3 longdpt longdpt     4096 Nov 20 22:12 02_Python_class_OOP
drwxr-xr-x 3 longdpt longdpt     4096 Nov 21 21:06 03_Vector_Matrix_Sparse
drwxr-xr-x 7 longdpt longdpt     4096 Nov  8 23:21 05_Pandas_DataR_dataframe
drwxr-xr-x 5 longdpt longdpt     4096 Nov  8 23:21 11_Convex_Optimization_CVXPY
-rwxr-xr-x 1 longdpt longdpt     3990 Nov 21 21:06 Curriculum.txt
-rw-rw-r-- 1 longdpt longdpt      689 Jan  1 11:51 demo.py
-rwxr-xr-x 1 longdpt longdpt     4635 Dec 23 23:01 Libraries_Installation.txt
-rwxr-xr-x 1 longdpt longdpt 19879373 Nov 21 21:06 Python_Coding_Methodology.pdf
-rwxr-xr-x 1 longdpt longdpt     1215 Dec 28 00:07 README.md
-rw-rw-r-- 1 longdpt longdpt     1781 Dec 24 19:29 test.py
-rwxr-xr-x 1 longdpt longdpt     1777 Dec 18 17:23 vscode_install_settings.txt
'''

#----
## Example 3: List directory contents (Windows)
#----

result = subprocess.run(['dir'], shell=True)  # Windows requires shell=True for 'dir'
# (This will print directory contents to the terminal)
'''
00_Course_Intro            11_Convex_Optimization_CVXPY   README.md
01_Python_Basic            Curriculum.txt                 test.py
02_Python_class_OOP        demo.py                        vscode_install_settings.txt
03_Vector_Matrix_Sparse    Libraries_Installation.txt
05_Pandas_DataR_dataframe  Python_Coding_Methodology.pdf
'''

#----
## Example 4: Cross-platform directory listing using Python's sys module
#----

if sys.platform.startswith('win'):
    result = subprocess.run(['dir'], shell=True)
else:
    result = subprocess.run(['ls', '-l'])

###############################################
## Capturing output with capture_output=True ##
###############################################
'''
By default, subprocess.run() sends output directly to the terminal
Use capture_output=True to capture stdout and stderr
'''

result = subprocess.run(['echo', 'Hello, World!'], capture_output=True)
'''(No output printed to terminal)'''

print(result.stdout)
# b'Hello, World!\n'
'''(Output is captured as bytes)'''

print(result.stderr)
# b''
'''(No error output)'''

#----
## Decode bytes to string using .decode()
#----

result = subprocess.run(['echo', 'Hello, World!'], capture_output=True)
output_string = result.stdout.decode('utf-8')
print(output_string)
# Hello, World!

print(type(output_string))
# <class 'str'>

#----
## Or use text=True to automatically decode output as string
#----

result = subprocess.run(['echo', 'Hello, World!'], capture_output=True, text=True)
print(result.stdout)
# Hello, World!

print(type(result.stdout))
# <class 'str'>

##############################################################################
## Using shell=False vs shell=True (for pipe with "|", must use shell=True) ##
##############################################################################
'''
shell=False (default, RECOMMENDED):
- Safer and more secure
- Command must be a list: ['command', 'arg1', 'arg2']
- Does not invoke shell, runs command directly
- Protects against shell injection attacks

shell=True (USE WITH CAUTION):
- Required for shell built-ins (like 'cd', 'dir' on Windows, pipes, wildcards)
- Command can be a string: 'command arg1 arg2'
- Invokes shell to run command
- Security risk if command contains untrusted input
'''

#----
## RECOMMENDED: shell=False with list arguments
#----

result = subprocess.run(['echo', 'Hello, World!'], capture_output=True, text=True)
print(result.stdout)
# Hello, World!

#----
## shell=True with string command (be careful with user input!)
#----

result = subprocess.run('echo Hello, World!', shell=True, capture_output=True, text=True)
print(result.stdout)
# Hello, World!

#----
## Using shell features like pipes (requires shell=True)
#----

result = subprocess.run('echo Hello | grep Hello', shell=True, capture_output=True, text=True)
print(result.stdout)
# Hello
'''(Without shell=True, pipes won't work)'''

###########################
## Checking return codes ##
###########################
'''
Return code (exit code) indicates if command succeeded:
- 0: Success
- Non-zero: Error or failure
'''

#----
## Successful command (return code 0)
#----

result = subprocess.run(['echo', 'Success'], capture_output=True, text=True)
print(result.returncode)
# 0

if result.returncode == 0:
    print("Command executed successfully!")
# Command executed successfully!

#----
## Failed command (non-zero return code)
#----

result = subprocess.run(['ls', 'nonexistent_file'], capture_output=True, text=True)
print(result.returncode)
# 2
# (Non-zero means error occurred)

print(result.stderr)
# ls: cannot access 'nonexistent_file': No such file or directory

#########################################
## Using check=True for error handling ##
#########################################
'''
check=True raises CalledProcessError if command returns non-zero exit code
This is useful when you want to treat non-zero exit as an exception
'''

#----
## Successful command with check=True
#----

result = subprocess.run(['echo', 'Success'], capture_output=True, text=True, check=True)
print(result.stdout)
# Success

#----
## Failed command with check=True (raises exception)
#----

try:
    result = subprocess.run(['ls', 'nonexistent_file'], capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed with return code {e.returncode}")
    print(f"Error output: {e.stderr}")
# Command failed with return code 2
# Error output: ls: cannot access 'nonexistent_file': No such file or directory

#---------------------------------------------------------------------------------------------#
#-------------------------------- Working with input/output ----------------------------------#
#---------------------------------------------------------------------------------------------#

###################################
## Redirecting stdout and stderr ##
###################################
'''
You can redirect stdout and stderr separately:
- subprocess.PIPE: Capture output to access in Python
- subprocess.DEVNULL: Discard output
- subprocess.STDOUT: Redirect stderr to stdout
- File object: Write output to a file
'''

#----
## Capture stdout only
#----

result = subprocess.run(['echo', 'Hello'], stdout=subprocess.PIPE, text=True)
print(result.stdout)
# Hello

#----
## Capture both stdout and stderr separately
#----

result = subprocess.run(['ls', 'file.txt', 'nonexistent'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

print(result.stdout)
# (Nothing)
'''(No stdout since 'file.txt' and 'nonexistent' don'tt exist, encounters error)'''

print(result.stderr)
# ls: cannot access 'file.txt': No such file or directory
# ls: cannot access 'nonexistent': No such file or directory

#----
## Redirect stderr to stdout (combine them)
#----

result = subprocess.run(['ls', 'file.txt', 'nonexistent'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
print(result.stdout)
# (Both stdout and stderr appear in stdout)
'''
ls: cannot access 'file.txt': No such file or directory
ls: cannot access 'nonexistent': No such file or directory
'''

#----
## Discard output using DEVNULL
#----

result = subprocess.run(['echo', 'This will not be captured'], stdout=subprocess.DEVNULL)
# (No output captured or printed)

print(result.stdout)
# None
'''(stdout is None since it was discarded)'''

#----
## Write output to a file
#----

with open('output.txt', 'w') as f:
    result = subprocess.run(['echo', 'Hello, File!'], stdout=f, text=True)

# Check the file content
with open('output.txt', 'r') as f:
    print(f.read())
# Hello, File!

#############################################
## Providing input to a subprocess (stdin) ##
#############################################
'''
You can provide input to a subprocess using the input parameter
The input is sent to the process's stdin
'''

#----
## Send input to a command (e.g., 'cat' reads from stdin)
#----

result = subprocess.run(['cat'], input='Hello from stdin\nLine 2\nLine 3', capture_output=True, text=True)
print(result.stdout)
# Hello from stdin
# Line 2
# Line 3

#----
## Send input to Python script
#----

# If you have a Python script that reads from stdin (e.g., input())
result = subprocess.run([sys.executable, '-c', 'name = input("Enter name: "); print(f"Hello, {name}!")'],
                       input='Alice\n', capture_output=True, text=True)
print(result.stdout)
# Enter name: Hello, Alice!

####################################
## Decoding output with text=True ##
####################################
'''
text=True (or universal_newlines=True in older Python versions):
- Automatically decodes stdout/stderr from bytes to strings
- Encodes input from strings to bytes
- Uses system default encoding (or specify with encoding parameter)
'''

#----
## Without text=True (bytes)
#----

result = subprocess.run(['echo', 'Hello'], capture_output=True)
print(result.stdout)
# b'Hello\n'

print(type(result.stdout))
# <class 'bytes'>

#----
## With text=True (string)
#----

result = subprocess.run(['echo', 'Hello'], capture_output=True, text=True)
print(result.stdout)
# Hello

print(type(result.stdout))
# <class 'str'>

#----
## Specify encoding explicitly
#----

result = subprocess.run(['echo', 'Hello'], capture_output=True, encoding='utf-8')
print(result.stdout)
# Hello

print(type(result.stdout))
# <class 'str'>

#################################
## Reading output line by line ##
#################################
'''
When you capture output, you get the entire output as a single string
You can split it into lines for processing
'''

result = subprocess.run(['ls', '-1'], capture_output=True, text=True)
lines = result.stdout.splitlines()

for line in lines:
    print(f"File: {line}")
'''
File: 00_Course_Intro
File: 01_Python_Basic
File: 02_Python_class_OOP
File: 03_Vector_Matrix_Sparse
File: 05_Pandas_DataR_dataframe
File: 11_Convex_Optimization_CVXPY
File: Curriculum.txt
File: demo.py
File: Libraries_Installation.txt
File: Python_Coding_Methodology.pdf
File: README.md
File: test.py
File: vscode_install_settings.txt
'''

#----
## Process only lines matching a pattern
#----

result = subprocess.run(['ls', '-1'], capture_output=True, text=True)
lines = result.stdout.splitlines()

txt_files = [line for line in lines if line.endswith('.txt')]
print(txt_files)
# ['Curriculum.txt', 'Libraries_Installation.txt', 'vscode_install_settings.txt']


#---------------------------------------------------------------------------------------------#
#------------------------------ Advanced subprocess.Popen() ----------------------------------#
#---------------------------------------------------------------------------------------------#
'''
subprocess.Popen() provides more control than subprocess.run():
- Non-blocking: process runs in background
- Can interact with process while it's running
- Can send signals to the process
- More complex but more powerful
'''

#############################
## Creating a Popen object ##
#############################
'''Popen() starts a process and returns immediately (non-blocking)'''

process = subprocess.Popen(['sleep', '3'])
print("Process started, doing other work...")
# Process started, doing other work...

# (Process runs in background)

# Wait for process to complete
return_code = process.wait()
print(f"Process finished with return code: {return_code}")
# Process finished with return code: 0

#----
## Popen with output capture
#----

process = subprocess.Popen(['echo', 'Hello from Popen'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# Process is running, we can do other things here

# Get output (this blocks until process finishes)
stdout, stderr = process.communicate()

print(stdout)
# Hello from Popen

print(stderr)
# (No error output)

#######################################################
## Communicating with subprocess using communicate() ##
#######################################################
'''
communicate() does three things:
1. Sends input to stdin (if provided)
2. Reads stdout and stderr
3. Waits for process to finish
'''

#----
## Send input and get output
#----

process = subprocess.Popen(['cat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

stdout, stderr = process.communicate(input='Hello\nWorld\n')
print(stdout)
# Hello
# World

#----
## With timeout (raises TimeoutExpired if process takes too long)
#----

process = subprocess.Popen(['sleep', '10'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    stdout, stderr = process.communicate(timeout=2)
except subprocess.TimeoutExpired:
    print("Process timed out!")
    process.kill()  # Kill the process
    stdout, stderr = process.communicate()  # Clean up
# Process timed out!

#################################################
## Using poll() to check if process is running ##
#################################################
'''
poll() checks if process has finished without blocking:
- Returns None if process is still running
- Returns return code if process has finished
'''

process = subprocess.Popen(['sleep', '2'])

while process.poll() is None:
    print("Process is still running...")
    import time
    time.sleep(0.5)

print(f"Process finished with return code: {process.poll()}")
# Process is still running...
# Process is still running...
# Process is still running...
# Process is still running...
# Process finished with return code: 0

###############################
## Using wait() with timeout ##
###############################
'''
wait() blocks until process finishes and returns the return code
Can specify timeout to avoid waiting indefinitely
'''

#----
## Wait without timeout
#----

process = subprocess.Popen(['sleep', '1'])
return_code = process.wait()
print(f"Process finished with return code: {return_code}")
# Process finished with return code: 0

#----
## Wait with timeout
#----

process = subprocess.Popen(['sleep', '10'])

try:
    return_code = process.wait(timeout=2)
except subprocess.TimeoutExpired:
    print("Process did not finish in time!")
    process.kill()
# Process did not finish in time!

#####################################################
## Sending signals to subprocess (terminate, kill) ##
#####################################################
'''
You can send signals to control subprocess:
- terminate(): Sends SIGTERM (graceful shutdown)
- kill(): Sends SIGKILL (forceful termination)
- send_signal(signal): Sends custom signal
'''

#----
## Terminate a long-running process
#----

process = subprocess.Popen(['sleep', '100'])
print(f"Process PID: {process.pid}")
# Process PID: 10279

import time
time.sleep(1)

process.terminate()  # Send SIGTERM

process.wait()  
# -15 
# (means terminate gracefully, allowing it to perform cleanup tasks such as closing open files, sockets, and saving data before exiting.)

print("Process terminated")
# Process terminated

#----
## Kill a process that won't terminate
#----

process = subprocess.Popen(['sleep', '100'])
print(f"Process PID: {process.pid}")
# Process PID: 10279

process.kill()  # Send SIGKILL (immediate termination)
process.wait() 
# -9 
# (means killed forcefully, no cleanup, etc.)

print("Process killed")
# Process killed

#----
## Send custom signal (Unix/Linux only)
#----

import signal

process = subprocess.Popen(['sleep', '100'])
process.send_signal(signal.SIGTERM)
process.wait()
print("Custom signal sent")


#---------------------------------------------------------------------------------------------#
#------------------------------- Error handling and security ---------------------------------#
#---------------------------------------------------------------------------------------------#

#################################
## Handling CalledProcessError ##
#################################
'''
CalledProcessError is raised when check=True and command returns non-zero exit code
The exception contains useful information about the failure
'''

try:
    result = subprocess.run(['ls', 'nonexistent'], capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Command: {e.cmd}")
    print(f"Return code: {e.returncode}")
    print(f"Stdout: {e.stdout}")
    print(f"Stderr: {e.stderr}")
# Command: ['ls', 'nonexistent']
# Return code: 2
# Stdout: 
# Stderr: ls: cannot access 'nonexistent': No such file or directory

#############################
## Handling TimeoutExpired ##
#############################
'''TimeoutExpired is raised when process doesn't finish within specified timeout'''

try:
    result = subprocess.run(['sleep', '10'], timeout=2, capture_output=True)
except subprocess.TimeoutExpired as e:
    print(f"Command timed out after {e.timeout} seconds")
    print(f"Command: {e.cmd}")
    print(f"Output so far: {e.stdout}")
# Command timed out after 2 seconds
# Command: ['sleep', '10']
# Output so far: None

#############################################
## Security considerations with shell=True ##
#############################################
'''
shell=True is DANGEROUS with untrusted input!
It can lead to shell injection attacks.

NEVER do this with user input:
'''

# BAD - Vulnerable to injection
user_input = "file.txt; rm -rf /"  # Malicious input
result = subprocess.run(f'cat {user_input}', shell=True)  # DANGEROUS! DON'T DO THIS
'''"rm -rf /" would DELETE all files on the system if run with sufficient permissions!'''

'''
GOOD - Safe alternatives:
'''

#----
## Use shell=False with list arguments (RECOMMENDED)
#----

user_input = "file.txt"
result = subprocess.run(['cat', user_input], capture_output=True)  # Safe

print(result.stdout)
# b''

#----
## If you must use shell=True, validate/sanitize input
#----

import shlex

user_input = "file with spaces.txt"

# Use shlex.quote() to safely escape arguments
safe_command = f'cat {shlex.quote(user_input)}'
result = subprocess.run(safe_command, shell=True, capture_output=True)

print(result.stdout)
# b''

##############################
## Safely passing arguments ##
##############################
'''
Best practices for passing arguments:
1. Use list format with shell=False
2. Don't concatenate user input into command strings
3. Use shlex.quote() if you must use shell=True
'''

#----
## RECOMMENDED: List format
#----

filename = "user file.txt"
result = subprocess.run(['cat', filename], capture_output=True)  # Spaces handled correctly

#----
## BAD: String concatenation with shell=True
#----

filename = "user file.txt"
result = subprocess.run(f'cat {filename}', shell=True)  # BREAKS with spaces!

#----
## If shell=True is necessary, use shlex.quote()
#----

import shlex
filename = "user file.txt"
result = subprocess.run(f'cat {shlex.quote(filename)}', shell=True, capture_output=True)  # Safe


#---------------------------------------------------------------------------------------------#
#---------------------------------- Advanced patterns ----------------------------------------#
#---------------------------------------------------------------------------------------------#

#####################################################
## Running commands in a different directory (cwd) ##
#####################################################
'''Use cwd parameter to run command in a specific directory'''

#----
## List files in a specific directory
#----

result = subprocess.run(['ls', '-l'], cwd='/home/longdpt/Pictures', capture_output=True, text=True)
print(result.stdout)
'''
drwxr-xr-x 2 longdpt longdpt 4096 Sep 15 13:23 Avatar
drwxr-xr-x 2 longdpt longdpt 4096 Jun 21  2025 Fedora_wallpapers
drwxr-xr-x 2 longdpt longdpt 4096 Dec 30 22:35 Screenshots
'''

#----
## Run Python script from different directory
#----

path = '/home/longdpt/Documents/Academic/DataScience_MachineLearning'

result = subprocess.run([sys.executable, 'demo.py'], cwd=path, capture_output=True, text=True)
# result = subprocess.run([sys.executable, 'demo.py'], cwd='./', capture_output=True, text=True)

print(result.stdout)
'''
         0.5               
          ⌠                
          ⎮     ________   
√3   π    ⎮    /      2    
── + ─ =  ⎮  ╲╱  1 - x   dx
8    2    ⌡                
          0
'''          

###################################
## Setting environment variables ##
###################################
'''Use env parameter to set environment variables for subprocess'''

#----
## Set custom environment variable
#----

my_env = os.environ.copy()  # Copy current environment
my_env['MY_VARIABLE'] = 'my_value'

result = subprocess.run([sys.executable, '-c', 'import os; print(os.environ.get("MY_VARIABLE"))'],
                       env=my_env, capture_output=True, text=True)
print(result.stdout)
# my_value

#----
## Run with minimal environment (only specific variables)
#----

minimal_env = {'PATH': '/usr/bin:/bin', 'HOME': os.environ['HOME']}

result = subprocess.run(['env'], env=minimal_env, capture_output=True, text=True)
print(result.stdout)
# PATH=/usr/bin:/bin
# HOME=/home/user

######################################
## Piping between multiple commands ##
######################################
'''
You can pipe output from one command to another
Two approaches: using shell or chaining Popen objects
'''

#----
## Method 1: Using shell=True with pipe (simple but less secure)
#----

result = subprocess.run('ls -l | grep .txt', shell=True, capture_output=True, text=True)
print(result.stdout)
# (Lists only .txt files)
'''
-rwxr-xr-x 1 longdpt longdpt     3990 Nov 21 21:06 Curriculum.txt
-rwxr-xr-x 1 longdpt longdpt     4635 Dec 23 23:01 Libraries_Installation.txt
-rwxr-xr-x 1 longdpt longdpt     1777 Dec 18 17:23 vscode_install_settings.txt
'''

#----
## Method 2: Chaining Popen objects (RECOMMENDED - more secure)
#----

# First command: ls -l
process1 = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)

# Second command: grep .txt (takes input from process1)
process2 = subprocess.Popen(['grep', '.txt'], stdin=process1.stdout, stdout=subprocess.PIPE, text=True)

# Allow process1 to receive SIGPIPE if process2 exits
process1.stdout.close()

# Get final output
output, _ = process2.communicate()
print(output)
# (Lists only .txt files)
'''
-rwxr-xr-x 1 longdpt longdpt     3990 Nov 21 21:06 Curriculum.txt
-rwxr-xr-x 1 longdpt longdpt     4635 Dec 23 23:01 Libraries_Installation.txt
-rwxr-xr-x 1 longdpt longdpt     1777 Dec 18 17:23 vscode_install_settings.txt
'''

#----
## Three-command pipeline example
#----

p1 = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', '.py'], stdin=p1.stdout, stdout=subprocess.PIPE)
p3 = subprocess.Popen(['wc', '-l'], stdin=p2.stdout, stdout=subprocess.PIPE, text=True)

p1.stdout.close()
p2.stdout.close()

output, _ = p3.communicate()
print(f"Number of Python files: {output.strip()}")
# Number of Python files: 2

##################################
## Running background processes ##
##################################
'''
Use Popen to start processes that run in the background
You can continue working while process runs
'''

#----
## Start a long-running process in background
#----

process = subprocess.Popen(['python', './test_GPU.py'],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

print(f"Started background process with PID: {process.pid}")
# Started background process with PID: 12345

# Do other work here
print("Doing other work while process runs...")

# Later, check if it's done
if process.poll() is None:
    print("Process still running")
else:
    print(f"Process finished with return code: {process.poll()}")

#----
## Start multiple processes in parallel
#----

processes = []

for i in range(5):
    p = subprocess.Popen([sys.executable, '-c', f'import time; time.sleep(2); print("Process {i} done")'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True)
    processes.append(p)

print(f"Started {len(processes)} processes in parallel")
# # Started 5 processes in parallel

# Wait for all processes to complete
for i, p in enumerate(processes):
    stdout, stderr = p.communicate()
    print(f"Process {i}: {stdout.strip()}")
# Process 0: Process 0 done
# Process 1: Process 1 done
# Process 2: Process 2 done
# Process 3: Process 3 done
# Process 4: Process 4 done

#----
## Detached background process (continues after Python exits)
#----

# On Unix/Linux, you can detach a process completely
process = subprocess.Popen(['nohup', 'python', 'daemon.py'],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL,
                          start_new_session=True)

print(f"Started detached process with PID: {process.pid}")
# (Process continues even if this Python script exits)
