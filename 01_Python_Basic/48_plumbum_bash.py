'''
Plumbum (Latin for "lead", which was used to create pipes back in the day) is a small yet
feature-rich library for shell script-like programs in Python.

The motto of the library is "Never write shell scripts again".

Plumbum provides a pythonic way to run shell commands with a syntax that mimics shell scripting.
It replaces traditional subprocess calls with more intuitive and readable code.

Plumbum is the recommended way to write shell-like scripts in Python.
It provides better syntax than subprocess and os.system() for common shell operations.

The plumbum library provides several key features:
# Local commands - Run commands on the local machine with shell-like syntax
# Remote commands - Execute commands on remote machines over SSH
# Command chaining - Pipe commands together using | operator
# Redirection - Redirect input/output using <, >, >> operators
# Background execution - Run commands in foreground (FG) or background (BG)

Important concepts in plumbum:
# local - The local machine object for running commands
# remote - Remote machine objects (SshMachine, ParamikoMachine) for SSH operations
# cmd - Import commands directly (e.g., from plumbum.cmd import ls, grep)
# Piping (|) - Chain command output to next command input
# Redirection (<, >, >>) - Redirect stdin, stdout, append to files
# FG and BG - Foreground and background execution modifiers
# Return codes - Access via .run() or check with .run(retcode=0)

##----------------------------------##

Installation: pip3 install plumbum

##----------------------------------##

Before jumping into plumbum, ensure you have a basic understanding of shell commmands:
https://www.w3schools.com/bash/

##----------------------------------##

Table of Contents:

1. Basic plumbum usage - Local commands
   - Importing and running commands
   - Using command arguments with []
   - Capturing output vs printing to terminal
   - Checking return codes
   - Using run() for more control
   - Providing input to a subprocess (stdin)

2. Command chaining and piping
   - Piping commands with |
   - Building complex pipelines
   - Chaining multiple commands

3. Redirection
   - Input redirection with <
   - Output redirection with >
   - Appending output with >>
   - Combining redirection and piping

4. Working with paths and directories
   - Using local.cwd for current directory
   - Changing directories with context managers
   - Path manipulation with local.path()
   - File operations

5. Foreground and background execution
   - Foreground execution with FG
   - Background execution with BG
   - Working with background processes
   - Getting return codes and output

6. Advanced local operations
   - Environment variables
   - Running with different working directory
   - Timeout handling
   - Error handling and return codes

7. Remote commands via SSH
   - Connecting to remote machines
   - Running remote commands
   - Remote piping and redirection
   - File transfer operations

8. Command modifiers and utilities
   - Using modifiers (TF, RETCODE)
   - Command composition
   - Creating reusable command templates
'''

import plumbum as pb
import plumbum.cmd as pcd


# ==============================================================================================
# 1. Basic plumbum usage - Local commands
# ==============================================================================================

##--------------------------------##
## Importing and running commands ##
##--------------------------------##
'''
Plumbum provides multiple ways to access commands:
1. Import directly from plumbum.cmd
2. Use local["command_name"] to get command objects
3. Access common commands via local.cmd
'''

# ## Example 1: Import commands directly (RECOMMENDED)
# 
from plumbum.cmd import ls, echo, grep, cat, wc

print(echo)
# LocalCommand(<LocalPath /usr/bin/echo>)

# Run a command - output goes to terminal by default
echo["Hello", "World"]()
# 'Hello World\n'

# ## Example 2: Get commands from local machine object
# 
from plumbum import local

ls_cmd = local["ls"]
print(ls_cmd)
# LocalCommand(<LocalPath /usr/bin/ls>)

ls_cmd["-la"]()
# (This will print directory contents to the terminal)

# ## Example 3: Access commands via local.cmd (alternative)
# 
pcd.echo["Hello from plumbum"]()
# 'Hello from plumbum\n'

##---------------------------------##
## Using command arguments with [] ##
##---------------------------------##
'''
Plumbum uses [] operator to pass arguments to commands
This is more pythonic than string concatenation
Arguments can be passed as separate items or lists
'''

# ## Single argument
# 
from plumbum.cmd import echo

echo["Hello"]()
# 'Hello\n'

# ## Multiple arguments
# 
echo["Hello", "World", "from", "Plumbum"]()
# 'Hello World from Plumbum\n'

# ## Using list of arguments
# 
args = ["-l", "-a", "-h"]
from plumbum.cmd import ls
ls[args]()
# (Lists directory contents with all flags)

# ## Combining arguments
# 
from plumbum.cmd import find  # Chainable
find[".", "-maxdepth", "1", "-name", "*.py"]()
# './demo.py\n./test_GPU.py\n'

print(find[".", "-maxdepth", "1", "-name", "*.py"]())
# ./demo.py
# ./test_GPU.py

##------------------------------------------##
## Capturing output vs printing to terminal ##
##------------------------------------------##
'''
By default, commands print output to terminal
Use () to execute and capture output as a string
The output includes trailing newline (similar to shell)
'''

# ## Print to terminal (default)
# 
echo["Hello"]()
# Hello
# (Output: 'Hello\n')

# ## Capture output as string
# 
output = echo["Hello"]()
print(output)
# Hello
# (with newline)

print(repr(output))
# 'Hello\n'

print(type(output))
# <class 'str'>

# ## Capture and process output
# 
files = ls["-1"]()
print(files)
# file1.txt
# file2.txt
# directory/
# ...

file_list = files.strip().split('\n')
print(file_list)
# ['file1.txt', 'file2.txt', 'directory']

##-----------------------##
## Checking return codes ##
##-----------------------##
'''
Commands return output by default
Use .run() method to get both return code and output
Return codes: 0 = success, non-zero = error
'''

# ## Successful command
# 
from plumbum.cmd import echo

output = echo["Success"]()
print(output)
# Success

# ## Using run() to get return code and output
# 
return_code, stdout, stderr = echo["Hello"].run()
print(f"Return code: {return_code}")
# Return code: 0

print(f"Stdout: {stdout}")
# Stdout: Hello

print(f"Stderr: {stderr}")
# Stderr:

# ## Command that fails
# 
from plumbum.cmd import ls

return_code, stdout, stderr = ls["nonexistent_file"].run(retcode=None)
# retcode=None allows any return code without raising exception

print(f"Return code: {return_code}")
# Return code: 2

print(f"Error: {stderr}")
# Error: ls: cannot access 'nonexistent_file': No such file or directory

##------------------------------##
## Using run() for more control ##
##------------------------------##
'''
.run() method provides fine-grained control:
- retcode: Expected return code(s), raises ProcessExecutionError if not matched
- timeout: Set execution timeout
- cwd: Change working directory
- env: Set environment variables
'''

# ## Expect specific return code
# 
from plumbum.cmd import echo, ls

return_code, stdout, stderr = echo["Hello"].run(retcode=0)
# Raises exception if return code is not 0

print(stdout)
# Hello

ls["nonexist.txt"].run(retcode=0)
# plumbum.commands.processes.ProcessExecutionError: Unexpected exit code: 2

# ## Allow any return code
# 
return_code, stdout, stderr = ls["nonexistent"].run(retcode=None)
# Won't raise exception regardless of return code

print(f"Command exited with code: {return_code}")
# Command exited with code: 2

##-----------------------------------------##
## Providing input to a subprocess (stdin) ##
##-----------------------------------------##
'''
You can provide input to a subprocess using the << operator
The << operator redirects data to the command's stdin
'''

# ## Send input to a command (e.g., 'cat' reads from stdin)
# 
from plumbum.cmd import cat

result = (cat << "Hello from stdin\nLine 2\nLine 3")()
print(result)
# Hello from stdin
# Line 2
# Line 3

# ## Using << with run() method
# 
return_code, stdout, stderr = (cat << "Hello\nWorld\n").run()
print(stdout)
# Hello
# World

print(f"Return code: {return_code}")
# Return code: 0

# ## Send Python variable to stdin
# 
data = "Line 1\nLine 2\nLine 3"
result = (cat << data)()
print(result)
# Line 1
# Line 2
# Line 3


# ==============================================================================================
# 2. Command chaining and piping
# ==============================================================================================

##------------------------##
## Piping commands with | ##
##------------------------##
'''
Plumbum uses | operator for piping (just like shell)
Output of left command becomes input to right command
Pipes can be chained indefinitely
'''

# ## Basic pipe
# 
from plumbum.cmd import ls, grep

# List files and filter for .py files
result = (ls["-a"] | grep[".py"])()
print(result)
# demo.py
# test_GPU.py

# ## Pipe with command arguments
# 
from plumbum.cmd import ls, wc

# Count number of files
result = (ls["-1"] | wc["-l"])()
print(result)
# 13

# ## Multiple pipes in chain
# 
from plumbum.cmd import ls, grep, wc

# List all files, exclude .py files, count them
pipeline = ls["-a"] | grep["-v", ".py"] | wc["-l"]
print(pipeline)
# /usr/bin/ls -a | /usr/bin/grep -v '\.py' | /usr/bin/wc -l

result = pipeline()
print(result)
# 16

##----------------------------##
## Building complex pipelines ##
##----------------------------##
'''
Pipelines can be built step by step and reused
Parentheses ensure proper operator precedence
Complex pipelines are more readable than subprocess.Popen chains
'''

# ## Build pipeline step by step
# 
from plumbum.cmd import cat, grep, sort, uniq

# Read file, find pattern, sort, get unique lines
cmd1 = (cat << "line1\npattern line2\nline3\npattern line4\nline2\n")
cmd2 = cmd1 | grep["pattern"]
cmd3 = cmd2 | sort
cmd4 = cmd3 | uniq

result = cmd4()
print(result)
# pattern line2
# pattern line4

# ## Reusable pipeline
# 
from plumbum.cmd import ps, grep, wc

# Pipeline to count processes matching a pattern
def count_processes(pattern):
    pipeline = ps["aux"] | grep[pattern] | wc["-l"]
    count = pipeline()
    return int(count.strip())

python_procs = count_processes("python")
print(f"Python processes: {python_procs}")
# Python processes: 5

##----------------------------##
## Chaining multiple commands ##
##----------------------------##
'''
Chains can include multiple operations
Use parentheses to control execution order
Commands can be saved and reused
'''

# ## Complex chain with multiple filters
# 
from plumbum.cmd import ls, grep, sort, head

# Get top 5 .txt files (sorted alphabetically)
chain = ls["./01_Python_Basic", "-1"] | grep[".py"] | sort | head["-n", "5"]
result = chain()
print(result)
# 01_print_end_sep_termcolor.py
# 02_comments_SingleLine_MultipleLines.py
# 03_string_FormatSymbol.py
# 04_variables.py
# 05_TypeConversion_isinstance.py

# ## Conditional pipeline execution
# 
from plumbum.cmd import ls, grep

def find_files(extension, pattern=None):
    cmd = ls["-1"] | grep[f".{extension}"]

    if pattern:
        cmd = cmd | grep[pattern]

    return cmd()

# Find all Python files
py_files = find_files("py")
print(py_files)
# demo.py
# test_GPU.py

# Find Python files with "test" in name
test_files = find_files("py", pattern="test")
print(test_files)
# test_GPU.py


# ==============================================================================================
# 3. Redirection
# ==============================================================================================

##--------------------------##
## Input redirection with < ##
##--------------------------##
'''
Use < operator to redirect file content as input
Similar to shell's stdin redirection
File content is read and passed to command
'''

# ## Read file content as input
# 
from plumbum.cmd import cat, wc

# Count lines in a file
result = (wc["-l"] < "README.md")()
print(result)
# 17

# ## Combine input redirection with piping
# 
from plumbum.cmd import cat, tail

# Read file and get last 5 lines
result = ((cat < "Curriculum.txt") | tail["-n", "5"])()
print(result)
# (Last 5 lines of Curriculum.txt)

##---------------------------##
## Output redirection with > ##
##---------------------------##
'''
Use > operator to redirect output to a file
Overwrites existing file content
Returns empty string (output went to file)
'''

# ## Redirect output to file
# 
from plumbum.cmd import ls, echo

# Save directory listing to file
(ls["-la"] > "directory_list.txt")()

# Verify file was created
result = (cat["directory_list.txt"])()
print(result)
# (Directory listing contents)

# ## Overwrite file with new content
# 
from plumbum.cmd import echo

(echo["First line"] > "output.txt")()
(echo["Second line (overwrites first)"] > "output.txt")()

result = (cat["output.txt"])()
print(result)
# Second line (overwrites first)

##--------------------------##
## Appending output with >> ##
##--------------------------##
'''
Use >> operator to append output to a file
Creates file if it doesn't exist
Does not overwrite existing content
'''

# ## Append to file
# 
from plumbum.cmd import echo

# Create file with first line
(echo["First line"] > "log.txt")()

# Append more lines
(echo["Second line"] >> "log.txt")()
(echo["Third line"] >> "log.txt")()

result = (cat["log.txt"])()
print(result)
# First line
# Second line
# Third line

# ## Append pipeline output
# 
from plumbum.cmd import ls, grep

# Append filtered results to file
(ls["-1"] | grep["\.py"] >> "python_files.txt")()

result = (cat["python_files.txt"])()
print(result)
# (List of Python files)

##----------------------------------##
## Combining redirection and piping ##
##----------------------------------##
'''
Redirections and pipes can be combined
Order matters: pipes first, then redirections
Parentheses control operation order
'''

# ## Input and output redirection with pipe
# 
from plumbum.cmd import cat, grep, wc

# Read file, filter, count, save result
((cat < "data.txt") | grep["pattern"] | wc["-l"] > "count.txt")()

result = (cat["count.txt"])()
print(result)
# 15

# ## Complex combination
# 
from plumbum.cmd import cat, sort, uniq

# Read file, sort, get unique lines, save
((cat < "input.txt") | sort | uniq > "output.txt")()


# ==============================================================================================
# 4. Working with paths and directories
# ==============================================================================================

##---------------------------------------##
## Using local.cwd for current directory ##
##---------------------------------------##

'''
local.cwd gives you the current working directory
It's a Path object with many useful methods
Can be used in path operations and comparisons
'''

# ## Get current directory
# 
from plumbum import local

cwd = local.cwd
print(cwd)
# /home/user/project

print(type(cwd))
# <class 'plumbum.machines.local.LocalPath'>

# ## List files in current directory
# 
files = local.cwd.list()
print(files)
# [<LocalPath /home/user/project/file1.txt>, <LocalPath /home/user/project/file2.py>, ...]

# ## Get directory name
# 
print(local.cwd.name)
# project

##--------------------------------------------##
## Changing directories with context managers ##
##--------------------------------------------##
'''
Use local.cwd as context manager to temporarily change directory
Directory automatically reverts when context exits
Safer than os.chdir() as it always restores original directory
'''

# ## Temporary directory change
# 
from plumbum import local
from plumbum.cmd import pwd

print("Before:", pwd())
# Before: /home/user/project

with local.cwd("/tmp"):
    print("Inside context:", pwd())
    # Inside context: /tmp

    # Run commands in /tmp
    from plumbum.cmd import ls
    files = ls["-la"]()
    print(files)

print("After:", pwd())
# After: /home/user/project

# ## Nested directory changes
# 
with local.cwd("/home"):
    print(pwd())
    # /home

    with local.cwd("user/Documents"):
        print(pwd())
        # /home/user/Documents

    print(pwd())
    # /home

##-------------------------------------##
## Path manipulation with local.path() ##
##-------------------------------------##
'''
local.path() creates Path objects for file operations
Path objects support / operator for joining paths
Many convenient methods: exists(), is_file(), is_dir(), etc.
'''

# ## Create path objects
# 
from plumbum import local

# Using local.path()
data_dir = local.path("/home/user/data")
print(data_dir)
# /home/user/data

# ## Join paths with / operator
# 
base = local.cwd
config_file = base / "config" / "settings.json"
print(config_file)
# /home/user/project/config/settings.json

# ## Check path properties
# 
file_path = local.cwd / "script.py"

if file_path.exists():
    print("File exists")

    if file_path.is_file():
        print("It's a file")

    print(f"Size: {file_path.stat().st_size} bytes")

# ## Path operations
# 
# Get parent directory
script_path = local.path("/home/user/project/src/main.py")
print(script_path.dirname)
# /home/user/project/src

# Get filename
print(script_path.name)
# main.py

# Get extension
print(script_path.suffix)
# .py

##-----------------##
## File operations ##
##-----------------##
'''
Path objects support common file operations
Can read, write, delete files directly
Works seamlessly with command objects
'''

# ## Read file content
# 
file_path = local.cwd / "Curriculum.txt"

# Read entire file
content = file_path.read()
print(content)
# (File contents)

# Read as lines
lines = file_path.read().splitlines()
print(lines)
# ['line1', 'line2', 'line3']

# ## Write to file
# 
output_file = local.cwd / "output.txt"

# Write string to file
output_file.write("Hello, Plumbum!\n")

# Append to file
output_file.write("More content\n", append=True)

# ## Delete file
# 
temp_file = local.cwd / "temp.txt"
temp_file.touch()  # Create empty file

if temp_file.exists():
    temp_file.delete()
    print("File deleted")

# ## Copy and move files
# 
source = local.cwd / "source.txt"
destination = local.cwd / "backup" / "source_backup.txt"

# Copy file
source.copy(destination)

# Move file (rename)
old_path = local.cwd / "old_name.txt"
new_path = local.cwd / "new_name.txt"
old_path.move(new_path)


# ==============================================================================================
# 5. Foreground and background execution
# ==============================================================================================

##------------------------------##
## Foreground execution with FG ##
##------------------------------##
'''
FG (foreground) runs command and prints output directly to terminal
Use & operator to attach FG to command
Output is not captured, goes to stdout/stderr directly
Useful for interactive commands or when you want live output
'''

# ## Run command in foreground
# 
from plumbum import FG
from plumbum.cmd import ls, grep

# Output appears directly in terminal
(ls["-a"] | grep[".py"]) & FG
# file1.py
# file2.py
# script.py

# ## Foreground with long-running command
# 
from plumbum.cmd import ping

# See output in real-time
ping["-c", "4", "google.com"] & FG
# PING google.com (142.250.185.46) 56(84) bytes of data.
# 64 bytes from lhr25s34-in-f14.1e100.net: icmp_seq=1 ttl=118 time=10.2 ms
# ...

# ## Interactive command in foreground
# 
from plumbum.cmd import python

# Run Python interpreter interactively
python & FG
# (Opens Python REPL in terminal)

##------------------------------##
## Background execution with BG ##
##------------------------------##
'''
BG (background) runs command without blocking
Returns a Future object immediately
Can check status, wait for completion, get return code
Process runs asynchronously in the background
'''

# ## Run command in background
# 
from plumbum import BG
from plumbum.cmd import sleep, echo

# Start command, returns immediately
future = (sleep["5"]) & BG
print(future)
# <Future ['/usr/bin/sleep', '5'] (running)>

print("Command is running in background...")
# Command is running in background...

# Wait for completion
future.wait()
print("Command completed!")
# (After 5 seconds)
# Command completed!

# ## Multiple background commands
# 
from plumbum.cmd import sleep
from plumbum import BG

# Start multiple background processes
future1 = (sleep["3"]) & BG
future2 = (sleep["2"]) & BG
future3 = (sleep["4"]) & BG

print("All commands started")

# Wait for all to complete
future1.wait()
print("Future 1 done")

future2.wait()
print("Future 2 done")

future3.wait()
print("Future 3 done")

##-----------------------------------##
## Working with background processes ##
##-----------------------------------##
'''
Future objects provide methods to interact with background processes
Can check if running, wait with timeout, get return code
stdout/stderr can be captured if redirected
'''

# ## Check if process is running
# 
from plumbum import BG
from plumbum.cmd import sleep

future = (sleep["3"]) & BG

# Check status
print(f"Ready: {future.ready()}")
# Ready: False

import time
time.sleep(4)

print(f"Ready: {future.ready()}")
# Ready: True

# ## Get return code
# 
from plumbum.cmd import echo
from plumbum import BG

future = (echo["Hello"]) & BG
future.wait()

# Get return code
return_code = future.return_code
print(f"Return code: {return_code}")
# Return code: 0

# ## Capture output from background process
# 
from plumbum.cmd import ls, grep
from plumbum import BG

# Redirect output to capture it
future = ((ls["-a"] | grep["\.py"]) > "bg_output.txt") & BG
future.wait()

# Read captured output
from plumbum.cmd import cat
output = cat["bg_output.txt"]()
print(output)
# file1.py
# file2.py

##---------------------------------##
## Getting return codes and output ##
##---------------------------------##
'''
Background processes can capture output and return codes
Use run() with stdout/stderr parameters for more control
'''

# ## Background with captured output
# 
from plumbum import local
from plumbum.cmd import echo

# Using popen for background with output capture
process = echo["Background output"].popen()

# Do other work while it runs
print("Process running...")

# Get output
stdout, stderr = process.communicate()
return_code = process.returncode

print(f"Output: {stdout}")
# Output: Background output
print(f"Return code: {return_code}")
# Return code: 0


# ==============================================================================================
# 6. Advanced local operations
# ==============================================================================================

##-----------------------##
## Environment variables ##
##-----------------------##
'''
Access and modify environment variables via local.env
Changes only affect subprocess, not parent Python process
Can pass custom environment to commands
'''

# ## Access environment variables
# 
from plumbum import local

# Get environment variable
home = local.env["HOME"]
print(f"Home directory: {home}")
# Home directory: /home/user

# Get with default value
custom_var = local.env.get("MY_VAR", "default_value")
print(custom_var)
# default_value

# ## Set environment variables for commands
# 
from plumbum.cmd import python

# Run command with custom environment
cmd = python["-c", "import os; print(os.environ.get('MY_VAR'))"]
result = cmd.with_env(MY_VAR="custom_value")()
print(result)
# custom_value

# ## Modify environment temporarily
# 
from plumbum import local
from plumbum.cmd import env

# Create modified environment
custom_env = local.env.copy()
custom_env["CUSTOM_VAR"] = "test_value"

# Run command with custom environment
with local.env(**custom_env):
    result = env()
    print("CUSTOM_VAR=test_value" in result)
    # True

##------------------------------------------##
## Running with different working directory ##
##------------------------------------------##
'''
Use .with_cwd() to run command in specific directory
More flexible than context managers for single commands
Directory change only affects that command
'''

# ## Run command in specific directory
# 
from plumbum import local
from plumbum.cmd import ls, pwd

# Run ls in /tmp directory
result = ls.with_cwd("/tmp")()
print(result)
# (Files in /tmp)

# Verify current directory unchanged
print(pwd())
# (Original directory)

# ## Chain with other operations
# 
from plumbum.cmd import python

# Run Python script from specific directory
result = python["script.py"].with_cwd("/home/user/project")()
print(result)

##------------------##
## Timeout handling ##
##------------------##
'''
Use timeout parameter to limit command execution time
Raises ProcessTimedOut exception if timeout exceeded
Useful for commands that might hang
'''

# ## Command with timeout
# 
from plumbum.cmd import sleep
from plumbum import ProcessTimedOut

try:
    # This will timeout after 2 seconds
    sleep["5"].run(timeout=2)
except ProcessTimedOut as e:
    print(f"Command timed out: {e}")
    # Command timed out: ...

# ## Timeout with captured output
# 
from plumbum.cmd import ping

try:
    # Ping with 2-second timeout
    return_code, stdout, stderr = ping["-c", "10", "google.com"].run(timeout=2)
except ProcessTimedOut:
    print("Ping command timed out")
    # Ping command timed out

##---------------------------------##
## Error handling and return codes ##
##---------------------------------##
'''
Commands raise ProcessExecutionError if return code is non-zero
Can allow any return code with retcode=None
Access return code, stdout, stderr from exception
'''

# ## Handle command failure
# 
from plumbum.cmd import ls
from plumbum import ProcessExecutionError

try:
    ls["nonexistent_file"]()
except ProcessExecutionError as e:
    print(f"Command failed: {e.args[0]}")
    print(f"Return code: {e.retcode}")
    print(f"Stderr: {e.stderr}")
# Command failed: Unexpected exit code: 2
# Return code: 2
# Stderr: ls: cannot access 'nonexistent_file': No such file or directory

# ## Allow any return code
# 
# Won't raise exception
return_code, stdout, stderr = ls["nonexistent"].run(retcode=None)
print(f"Command exited with: {return_code}")
# Command exited with: 2

# ## Check specific return codes
# 
from plumbum.cmd import grep

# grep returns 1 when no match found (not an error)
try:
    result = grep["pattern", "file.txt"].run(retcode=(0, 1))
    # Accepts both 0 and 1 as valid return codes
    print("Command succeeded")
except ProcessExecutionError:
    print("Unexpected return code")


# ==============================================================================================
# 8. Remote commands via SSH
# ==============================================================================================

##-------------------------------##
## Connecting to remote machines ##
##-------------------------------##
'''
Plumbum supports remote command execution via SSH
Use SshMachine or ParamikoMachine to connect
Remote commands work like local commands
Requires SSH access to remote machine
'''

# ## Connect with SshMachine (uses system SSH)
# 
from plumbum.machines.ssh_machine import SshMachine

# Connect to remote machine
remote = SshMachine("user@example.com")

# Get remote command
r_ls = remote["ls"]
print(r_ls)
# RemoteCommand(<SshMachine ssh://user@example.com>, <RemotePath /usr/bin/ls>)

# Run remote command
result = r_ls["-la"]()
print(result)
# (Remote directory listing)

# Close connection when done
remote.close()

# ## Connect with context manager
# 
from plumbum.machines.ssh_machine import SshMachine

with SshMachine("user@example.com") as remote:
    result = remote["pwd"]()
    print(f"Remote directory: {result}")
    # Remote directory: /home/user
# Connection automatically closed

# ## Connect with password or key
# 
# With password
remote = SshMachine("example.com", user="username", password="secret")

# With SSH key
remote = SshMachine("example.com", user="username", keyfile="/home/user/.ssh/id_rsa")

# With custom SSH port
remote = SshMachine("example.com", user="username", port=2222)

##-------------------------##
## Running remote commands ##
##-------------------------##
'''
Remote commands have the same syntax as local commands
Support piping, redirection, arguments
Output is captured and returned to local machine
'''

# ## Basic remote command
# 
from plumbum.machines.ssh_machine import SshMachine

with SshMachine("user@example.com") as remote:
    # Get remote command
    r_echo = remote["echo"]

    # Run it
    result = r_echo["Hello from remote"]()
    print(result)
    # Hello from remote

# ## Remote command with arguments
# 
with SshMachine("user@example.com") as remote:
    r_ls = remote["ls"]

    # List files with options
    result = r_ls["-lah", "/var/log"]()
    print(result)
    # (Remote /var/log listing)

# ## Access remote path
# 
with SshMachine("user@example.com") as remote:
    # Get remote current directory
    print(remote.cwd)
    # /home/user

    # Check if remote file exists
    remote_file = remote.path("/etc/passwd")
    print(remote_file.exists())
    # True

##-------------------------------##
## Remote piping and redirection ##
##-------------------------------##
'''
Piping works between remote commands
Redirection can save files on remote machine
Mix remote and local commands in pipelines
'''

# ## Pipe remote commands
# 
with SshMachine("user@example.com") as remote:
    r_ls = remote["ls"]
    r_grep = remote["grep"]
    r_wc = remote["wc"]

    # Count Python files on remote machine
    result = (r_ls["-1"] | r_grep["\.py"] | r_wc["-l"])()
    print(f"Python files on remote: {result.strip()}")
    # Python files on remote: 15

# ## Remote output redirection
# 
with SshMachine("user@example.com") as remote:
    r_echo = remote["echo"]

    # Save output to remote file
    (r_echo["Remote content"] > "/tmp/remote_file.txt")()

    # Verify file was created
    r_cat = remote["cat"]
    result = r_cat["/tmp/remote_file.txt"]()
    print(result)
    # Remote content

# ## Mix remote and local commands
# 
from plumbum.cmd import grep  # Local grep
with SshMachine("user@example.com") as remote:
    r_cat = remote["cat"]

    # Read remote file, filter locally
    result = (r_cat["/var/log/syslog"] | grep["error"])()
    print(result)
    # (Error lines from remote syslog)

##--------------------------##
## File transfer operations ##
##--------------------------##
'''
Transfer files between local and remote machines
Use download() and upload() methods
Can copy entire directories recursively
'''

# ## Upload file to remote
# 
from plumbum import local
with SshMachine("user@example.com") as remote:
    local_file = local.path("local_data.txt")
    remote_path = remote.path("/tmp/remote_data.txt")

    # Upload
    remote.upload(local_file, remote_path)
    print("File uploaded")

# ## Download file from remote
# 
with SshMachine("user@example.com") as remote:
    remote_file = remote.path("/var/log/syslog")
    local_path = local.path("./syslog_copy")

    # Download
    remote.download(remote_file, local_path)
    print("File downloaded")

# ## Copy directory recursively
# 
with SshMachine("user@example.com") as remote:
    # Upload directory
    remote.upload(local.path("./local_dir"), remote.path("/tmp/remote_dir"))

    # Download directory
    remote.download(remote.path("/etc/config"), local.path("./config_backup"))


# ==============================================================================================
# 9. Command modifiers and utilities
# ==============================================================================================

##-------------------------------##
## Using modifiers (TF, RETCODE) ##
##-------------------------------##
'''
Plumbum provides modifiers to change command behavior
TF: Get True/False based on return code
RETCODE: Get just the return code (ignore output)
'''

# ## TF modifier (True/False)
# 
from plumbum import TF
from plumbum.cmd import test

# Check if file exists (returns True/False)
result = test["-f", "existing_file.txt"] & TF
print(result)
# True

result = test["-f", "nonexistent.txt"] & TF
print(result)
# False

# ## RETCODE modifier
# 
from plumbum import RETCODE
from plumbum.cmd import ls

# Get only return code
return_code = ls["-la"] & RETCODE
print(return_code)
# 0

return_code = ls["nonexistent"] & RETCODE(retcode=None)
print(return_code)
# 2

# ## Combine modifiers
# 
from plumbum.cmd import grep

# Check if pattern exists in file
found = (grep["pattern", "data.txt"] & TF)
if found:
    print("Pattern found")
else:
    print("Pattern not found")

##---------------------##
## Command composition ##
##---------------------##
'''
Create reusable command templates
Bind arguments to create specialized commands
Compose commands for complex operations
'''

# ## Create command template
# 
from plumbum.cmd import ls

# Create specialized ls command
ls_long = ls["-la"]

# Use it multiple times
result1 = ls_long["/tmp"]()
result2 = ls_long["/var"]()
result3 = ls_long["/home"]()

# ## Bind arguments
# 
from plumbum.cmd import grep

# Create grep command that always ignores case
grep_ignore_case = grep["-i"]

# Use with different patterns
result1 = grep_ignore_case["error", "log.txt"]()
result2 = grep_ignore_case["warning", "log.txt"]()

# ## Function returning configured command
# 
from plumbum.cmd import find

def find_files(extension, directory="."):
    """Create find command for specific file extension"""
    return find[directory, "-name", f"*.{extension}"]

# Find Python files
py_files = find_files("py", "/home/user/project")()
print(py_files)

# Find text files
txt_files = find_files("txt")()
print(txt_files)

##-------------------------------------##
## Creating reusable command templates ##
##-------------------------------------##
'''
Build complex commands from simpler parts
Store commands as objects for reuse
Create command libraries for common tasks
'''

# ## Command library for common operations
# 
from plumbum.cmd import tar, gzip, find

class BackupCommands:
    @staticmethod
    def compress_directory(source_dir, output_file):
        """Create compressed archive of directory"""
        cmd = tar["czf", output_file, source_dir]
        return cmd

    @staticmethod
    def find_large_files(directory, size_mb=100):
        """Find files larger than specified size"""
        cmd = find[directory, "-type", "f", "-size", f"+{size_mb}M"]
        return cmd

    @staticmethod
    def disk_usage_report(directory):
        """Get disk usage report"""
        from plumbum.cmd import du, sort
        cmd = du["-h", directory] | sort["-rh"]
        return cmd

# Use command library
backup_cmd = BackupCommands.compress_directory("/home/user/data", "backup.tar.gz")
backup_cmd()

large_files = BackupCommands.find_large_files("/var", 50)()
print(large_files)

# ## Parameterized command builder
# 
from plumbum.cmd import ps, grep, awk

def process_monitor(process_name, sort_by="memory"):
    """Monitor specific process with sorting"""

    # Base command
    cmd = ps["aux"] | grep[process_name]

    # Sort by memory or CPU
    if sort_by == "memory":
        cmd = cmd | awk["{print $4, $11}"]
    elif sort_by == "cpu":
        cmd = cmd | awk["{print $3, $11}"]

    return cmd

# Monitor Python processes by memory
result = process_monitor("python", "memory")()
print(result)

# Monitor Chrome by CPU
result = process_monitor("chrome", "cpu")()
print(result)
