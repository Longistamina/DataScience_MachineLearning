'''
"os" is a built-in Python module that provides a way of using operating system dependent functionality,
like reading or writing to the file system, executing shell commands, and more.

This module allows you to interact with the underlying operating system in a platform-independent way.
It includes functions to work with files and directories, manage processes, and perform other system-related tasks.
It is commonly used for tasks such as file manipulation, environment variable access, and executing system commands.

The "os" module is part of the Python Standard Library, 
so it is available in any Python installation without needing to install anything extra.
'''

######

'''
Flow of contents:
1. Basic Inspection: os.name, os.uname(), os.cpu_count()
2. Working Directory Navigation: os.getcwd(), os.chdir()
3. File and Directory Operations: os.listdir(), os.scandir(), 
                                  os.mkdir(), os.makedirs(), os.rmdir(), shutil.rmtree(), os.remove(), 
                                  os.rename()
4. Running System Commands: os.system(), os.popen(), os.execv() os.execvp(), os.execvpe()
5. Working with file permissions: os.chmod()
6. Environment Variables: os.environ, os.getenv(), os.putenv()
'''

import os
from loguru import logger


#----------------------------------------------------------------------------------------------------#
#------------------------------------ 1. Basic Inspection -------------------------------------------#
#----------------------------------------------------------------------------------------------------#

#############
## os.name ##
#############
'''
os.name returns the name of the operating system dependent module imported.
It can return 'posix', 'nt', 'os2', 'ce', 'java', or 'riscos'.
This can be useful to determine the platform your code is running on.
'''

print(os.name)  # posix 
# (Linux, macOS)


# Example of using os.name to check the platform
if os.name == 'nt':
    print("Running on Windows")
elif os.name == 'posix':
    print("Running on Unix-like OS (Linux, macOS)")
else:
    print("Running on an unknown OS")

# >>> Running on Unix-like OS (Linux, macOS)

################
## os.uname() ##
################
'''
os.uname() returns a tuple containing information about the operating system.
It includes the system name, node name (hostname), release, version, and machine type
'''

print(os.uname())
# posix.uname_result(sysname='Linux', nodename='fedora', release='6.15.4-200.fc42.x86_64', 
#                    version='#1 SMP PREEMPT_DYNAMIC Fri Jun 27 15:32:46 UTC 2025', machine='x86_64')


# Example of using os.uname() to get system information
system_info = os.uname()
print(f"System: {system_info.sysname}") # System: Linux
print(f"Node Name: {system_info.nodename}") # Node Name: '192.168.1.32.non-exists.ptr.local'
print(f"Release: {system_info.release}") # Release: 6.15.4-200.fc42.x86_64
print(f"Version: {system_info.version}") # Version: #1 SMP PREEMPT_DYNAMIC Fri Jun 27 15:32:46 UTC 2025
print(f"Machine: {system_info.machine}") # Machine: x86_64

####################
## os.cpu_count() ##
####################
'''os.cpu_count() returns the number of CPUs in the system.'''

print(os.cpu_count()) # 32
# 32 (threads)
# 16 (cores)


#---------------------------------------------------------------------------------------------#
#------------------------------- 2. Working Directory Navigation -----------------------------#
#---------------------------------------------------------------------------------------------#

#################
## os.getcwd() ##
#################
'''os.getcwd() returns the current working directory as a string. (like "pwd" command in Linux)'''

print(os.getcwd())  # /home/longdpt/Documents/Academic/DataScience_MachineLearning

################
## os.chdir() ##
################
'''os.chdir(path) changes the current working directory to the specified path. (like "cd" command in Linux)'''

# Change to a different directory
os.chdir('/home/longdpt/Documents/Academic')  

# Change to the parent directory
os.chdir('..')  # The '..' means the parent directory of the current working directory

# Verify the change
print(os.getcwd())  # /home/longdpt/Documents


#----------------------------------------------------------------------------------------------#
#------------------------------- 3. File and Directory Operations -----------------------------#
#----------------------------------------------------------------------------------------------#

##################
## os.listdir() ##
##################
'''os.listdir(path) returns a list of the entries in the directory given by path.'''

# List files in the current directory ('.' means current directory)
print(os.listdir('.'))  
# ['01_Python_Basic', 'merge_mp4.sh', 'Unrar_file.txt', '.git', 'Python_Important_packages.txt', 'vscode_install_settings.txt', 'Calculus_ConvexOptimization', '.gitignore', '02_Python_class_OOP']


# List files in a specific directory
print(os.listdir('/home/longdpt/Documents/Academic'))
# ['Biotech_books_summary', 'MachineLearning_ThayLoi', 'Cancer_NGS_ThayLoi', 'DataScience_HCMUS', 'LDS9 Chapter 12 Cung cấp tài nguyên triển khai hệ thống Master - Workers.rar', 'LDS9 Bigdata.rar', 'LDS8.rar', 'HTDS_272.rar', 'Biotechnology_HCMUS', 'Toan_hoc_chan_phuong.pdf', 'git_practice', 'Bioinformatics_Linux_R_Python', 'DataScience_MachineLearning', 'Programming_Materials']


# Store output of os.listdir() in a variable
dir_contents = os.listdir('/home/longdpt/Documents/Academic')
print(dir_contents)

##################
## os.scandir() ##
##################
'''
os.scandir() is similar to os.listdir() but returns an iterator of DirEntry objects, which include file attributes.
This is more efficient for large directories as it avoids multiple system calls.
'''

# scan then printout each entry in the directory
with os.scandir('/home/longdpt/Documents/Academic') as entries:
    print(entries) # <posix.ScandirIterator object at 0x7f4da1f29930>
    for entry in entries:
        print(entry)
        # <DirEntry 'Biotech_books_summary'>
        # <DirEntry 'MachineLearning_ThayLoi'>
        # <DirEntry 'Cancer_NGS_ThayLoi'>
        # <DirEntry 'DataScience_HCMUS'>
        # <DirEntry 'LDS9 Chapter 12 Cung cấp tài nguyên triển khai hệ thống Master - Workers.rar'>
        # <DirEntry 'LDS9 Bigdata.rar'>
        # <DirEntry 'LDS8.rar'>
        # <DirEntry 'HTDS_272.rar'>
        # <DirEntry 'Biotechnology_HCMUS'>
        # <DirEntry 'Toan_hoc_chan_phuong.pdf'>
        # <DirEntry 'git_practice'>
        # <DirEntry 'Bioinformatics_Linux_R_Python'>
        # <DirEntry 'DataScience_MachineLearning'>
        # <DirEntry 'Programming_Materials'>


# scan then printout each entry's attributes (name, type, size)
with os.scandir('/home/longdpt/Documents/Academic') as entries:
    for entry in entries:
        if entry.is_file():
            print(f"File: {entry.name}, Size: {entry.stat().st_size} bytes")
        elif entry.is_dir():
            print(f"Directory: {entry.name}")
            # Directory: Biotech_books_summary
            # Directory: MachineLearning_ThayLoi
            # Directory: Cancer_NGS_ThayLoi
            # Directory: DataScience_HCMUS
            # File: LDS9 Chapter 12 Cung cấp tài nguyên triển khai hệ thống Master - Workers.rar, Size: 18511520311 bytes
            # File: LDS9 Bigdata.rar, Size: 12382626277 bytes
            # File: LDS8.rar, Size: 11672272532 bytes
            # File: HTDS_272.rar, Size: 3878818433 bytes
            # Directory: Biotechnology_HCMUS
            # File: Toan_hoc_chan_phuong.pdf, Size: 272921745 bytes
            # Directory: git_practice
            # Directory: Bioinformatics_Linux_R_Python
            # Directory: DataScience_MachineLearning
            # Directory: Programming_Materials

################
## os.mkdir() ##
################
'''
os.mkdir(path) creates a new directory at the specified path.
NOTE: This will raise an error if the directory already exists.
'''

# current working directory: '/home/longdpt/Documents/Academic/DataScience_MachineLearning/'
# Create a new directory named 'new_directory' in current working directory
os.mkdir('new_directory')

# Create a new directory in an EXISTED parent directory
os.mkdir('/home/longdpt/Documents/Academic/DataScience_MachineLearning/new_directory_2')


'''Note: if the parent directory does not exist, it will raise a FileNotFoundError.'''
try:
    os.mkdir('parent_dir/child_dir')
except Exception as e:
    logger.error(e)
# | ERROR    | __main__:<module>:4 - [Errno 2] No such file or directory: 'parent_dir/child_dir'
# => use os.makedirs()

###################
## os.makedirs() ##
###################
'''
os.makedirs(path) creates a directory recursively, 
meaning it will create all intermediate-level directories needed to contain the leaf directory.
'''

os.makedirs('parent_dir/child_dir/grandchild_dir')
# This will create 'parent_dir', 'child_dir', and 'grandchild_dir'
# even if 'parent_dir' or 'child_dir' does not exist.


'''Note: if the parent directory exists, it will raise a FileNotFoundError.'''
try:
    os.makedirs('parent_dir/child_dir/grandchild_dir')
except Exception as e:
    logger.error(e)
# | ERROR    | __main__:<module>:4 - [Errno 17] File exists: 'parent_dir/child_dir/grandchild_dir'

################
## os.rmdir() ##
################
'''os.rmdir(path) removes (deletes) the EMPTY directory at the specified path.
NOTE: This will raise an error if the directory is not empty.
'''

# Remove an empty directory
os.rmdir('new_directory')  # This will remove the empty 'new_directory' created earlier


## Try to remove a non-empty directory (will raise an error) ##
try:
    os.rmdir('parent_dir')
except Exception as e:
    logger.error(e)
# | ERROR    | __main__:<module>:4 - [Errno 39] Directory not empty: 'parent_dir'

#####################
## shutil.rmtree() ##
#####################

import shutil

shutil.rmtree('parent_dir')
# This will remove 'parent_dir' and all its contents, including 'child_dir' and 'grandchild_dir'

'''
shutil.rmtree(path) removes a directory and all its contents, including subdirectories and files.
This is useful for deleting non-empty directories.

NOTE: Be careful with this command, as it will permanently delete files and directories without confirmation.
'''

#################
## os.remove() ##
#################
'''
os.remove(path) removes (deletes) the FILE at the specified path.
NOTE: This will raise an error if the file does not exist.
'''
os.system('echo "forsaken i am awakened" >> demo_os_remove.txt')  # Create a demo file with given content

os.remove('./demo_os_remove.txt')  # This will remove the 'demo_os_remove.txt' file created earlier
# os.remove('./demo_os_remove.txt')

## Try to remove a non-existing file (will raise an error) ##
try:
    os.remove('./non_existing_file.txt')
except Exception as e:
    logger.error(e)
# | ERROR    | __main__:<module>:4 - [Errno 2] No such file or directory: './non_existing_file.txt'

#################
## os.rename() ##
#################
'''
os.rename(src, dst) renames the file or directory from src (source) to dst (destination).
NOTE: If dst already exists, it will be replaced.
NOTE: If src does not exist, it will raise a FileNotFoundError.
'''

os.system('echo "forsaken i am awakened" >> demo_os_remname.txt')  # Create a demo file with given content

os.rename('./demo_os_remname.txt', './bury_the_light.txt')  # Rename the file to 'bury_the_light.txt'

# os.remove('./bury_the_light.txt') ## remove after demo ##


#----------------------------------------------------------------------------------------------#
#------------------------------- 4. Running System Commands -----------------------------------#
#----------------------------------------------------------------------------------------------#

#################
## os.system() ##
#################
'''
os.system(command) runs the command (a string) in a subshell.
It returns the exit status of the command (0 for success, non-zero for failure).
'''

os.system('echo "forsaken i am awakened"')  # Execute the shell command and display exit status
# forsaken i am awakened
# 0  (Exit status, 0 means success)


## Store the exit status in a variable ##d
exit_status = os.system('echo "forsaken i am awakened"') 
# forsaken i am awakened 
# (not return exit status)

print(exit_status)  # 0


## Create a string variable with multiple commands ##
commands = """
echo "I am the storm that is approaching"
echo "Provoking !!!"
echo "Black clouds in isolation"
pwd
shuf -i 0-9 -n 8 | xargs -I {} echo -n {}; echo ""
"""
_ = os.system(commands) # Assign to underscore to avoid displaying the exit status
# I am the storm that is approaching
# Provoking !!!
# Black clouds in isolation
# /home/longdpt/Documents/Academic/DataScience_MachineLearning
# 37412506

''' NOTE: the _ store the exit status, NOT the output of the commands. '''
## To capture the output of the commands, you can use os.popen() or subprocess module.

################
## os.popen() ##
################
'''
os.popen(command) opens a pipe to or from the command (a string) and returns a file object.
This allows you to read the output of the command or write to its input.
'''

os.popen('ls -l .') # <os._wrap_close object at 0x7f4da1e243b0>
                    # Only an object is returned, not the output of the command.

## Open a pipe to the 'ls' command and READ its output ##
with os.popen('ls -l .', "r") as wrap_object:
    directory_contents = wrap_object.read()  # Store the output of the command in a variable
    print(directory_contents)  # Display the output of the 'ls -l .' command
    # total 16
    # drwxrwxrwx. 1 longdpt longdpt 1720 Jul 17 13:27 01_Python_Basic
    # drwxr-xr-x. 1 longdpt longdpt  512 Jun 10 21:37 02_Python_class_OOP
    # drwxr-xr-x. 1 longdpt longdpt   56 Jul 14 15:19 Calculus_ConvexOptimization
    # -rwxrwxrwx. 1 longdpt longdpt  624 May 19 12:35 merge_mp4.sh
    # -rw-r--r--. 1 longdpt longdpt 1462 Jun 16 13:27 Python_Important_packages.txt
    # -rwxrwxrwx. 1 longdpt longdpt  106 May 19 12:35 Unrar_file.txt
    # -rw-r--r--. 1 longdpt longdpt 1697 Jun  8 16:13 vscode_install_settings.txt


## Open a pipe to the 'sort' command and WRITE to its input ##
fruits = "orange\napple\nbanana"
with os.popen("sort", "w") as wrap_object: 
    wrap_object.writelines(fruits) # Write the fruits to the sort command
    # apple
    # banana
    # orange

# This works like: printf "orange\napple\nbanana\n" | sort
# or os.system('printf "orange\napple\nbanana\n" | sort')

################
## os.execv() ##
################
'''
os.execv(file, args) replaces the current process with a new process running the specified file.
It does not return to the original process, so it is typically used in a child process
created by os.fork() or subprocess module.
'''

import os

# Example of using os.execvp() to run a command
os.execv(
    '/usr/bin/ls',  # ABSOLUTE PATH to the executable file (example here is the 'ls' command)
    ['ls', '-l', '.']  # Arguments to pass to the command
) # (NO KEYWORD ARGUMENTS)
'''
Note: This will not return to the original process (after runing this, it will EXIT CURRENT PYTHON PROCESS)
so the following lines or commands will not be executed.
'''

print("This line will not be executed if os.execvp() is called")  # This line will not be executed

#################
## os.execvp() ##
#################
'''
os.execvp(file, args) is similar to os.execv() but searches for the file in the directories listed in PATH environment variable.
It is useful when you want to run a command without specifying the absolute path.
'''

import os

os.execvp(
    file='ls',  # Path to the executable file (don't need to be absolute, will search in PATH)
    args=['ls', '-l', '.']  # Arguments to pass to the command
)
'''
Note: This will not return to the original process (after runing this, it will EXIT CURRENT PYTHON PROCESS)
so the following lines or commands will not be executed.
'''

print("This line will not be executed if os.execvp() is called")  # This line will not be executed

##########################################
## os.execvpe() with current os.environ ##
##########################################
'''
os.execvpe(file, args, env) is similar to os.execvp() 
but allows you to specify a custom environment for the new process.
'''

import os

os.execvpe(
    file='ls',  # Path to the executable file (don't need to be absolute, will search in PATH)
    args=['ls', '-l', '.'],  # Arguments to pass to the command
    env=os.environ  # Use the current environment variables
)
'''
Note: This will not return to the original process (after runing this, it will EXIT CURRENT PYTHON PROCESS)
so the following lines or commands will not be executed.
'''

print("This line will not be executed if os.execvp() is called")  # This line will not be executed

#########################################################
## os.execvpe() with customized or chosen environment ###
#########################################################

import os
import subprocess

def get_conda_env(env_name):
    """Get environment variables from a conda environment"""
    # Run a command in the conda environment to dump its environment
    result = subprocess.run(
        ['conda', 'run', '-n', env_name, 'python', '-c', 
         'import os; import json; print(json.dumps(dict(os.environ)))'],
        capture_output=True,
        text=True,
        check=True
    )
    
    import json
    return json.loads(result.stdout.strip())

# Get the environment for your conda environment
conda_env = get_conda_env('bio')
print(conda_env)  # Display the environment variables of the conda environment
# {'SHELL': '/bin/bash', 'SESSION_MANAGER': 'local/unix:@/tmp/.ICE-unix/2578,unix/unix:/tmp/.ICE-unix/2578', 'COLORTERM': 'truecolor', 'VSCODE_DEBUGPY_ADAPTER_ENDPOINTS': 

# Use it with execvpe
os.execvpe(
    file='ls',  # Path to the executable file (don't need to be absolute, will search in PATH)
    args=['ls', '-l', '.'],  # Arguments to pass to the command
    env=conda_env  # Use the conda environment variables
)
'''
Note: This will not return to the original process (after runing this, it will EXIT CURRENT PYTHON PROCESS)
so the following lines or commands will not be executed.
'''

print("This line will not be executed if os.execvp() is called")  # This line will not be executed


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------- 5. Working with file permissions ------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
'''
os.chmod(path, mode) is used to change the file permissions 
at the specified path (path) to the given mode (mode).
'''

os.system('echo "echo Hello World!!!" > demo_permission.sh')  # Create a demo executable .sh file
os.system('ls -l ./demo_permission.sh')  # Check the file permissions before changing
# -rw-r--r--. 1 longdpt longdpt 20 Jul 18 11:26 ./demo_permission.sh


os.chmod('./demo_permission.sh', 0o755)  # Change permissions to make it executable

os.system('ls -l ./demo_permission.sh')  # Check the file permissions after changing
# -rwxr-xr-x. 1 longdpt longdpt 20 Jul 18 11:26 ./demo_permission.sh

'''
Octal    Symbolic     Common Use
-----    --------     ----------
0o755    rwxr-xr-x    Executable scripts/programs
0o644    rw-r--r--    Text files
0o700    rwx------    Private configs/keys
0o4755   rwsr-xr-x    SUID root helper
0o1777   rwxrwxrwt    World-writable directory with sticky (e.g., /tmp)
0o400    r--------    Read-only files
0o200    -w-------    Write-only files
0o100    --x------    Execute-only files (rare)
0o000    ---------    No permissions
0o600    rw-------    Private files (read/write only for owner)
0o300    -wx------    Write and execute only for owner
0o444    r--r--r--    Read-only files for everyone
0o222    -w--w--w-    Write-only files for everyone
0o111    --x--x--x    Execute-only files for everyone
0o555    r-xr-xr-x    Read and execute files for everyone
0o333    -wx-wx-wx    Write and execute files for everyone
0o666    -rw-rw-rw-    Read and write files for everyone
0o777    rwxrwxrwx    Read, write, and execute files for everyone  
'''


#----------------------------------------------------------------------------------------------#
#------------------------------- 6. Environment Variables -------------------------------------#
#----------------------------------------------------------------------------------------------#

import os

################
## os.environ ##
################
'''
os.environ is a mapping object representing the string environment.
It contains the environment variables (informaiton) of the current process.
'''

print(os.environ)
# environ({'SHELL': '/bin/bash', 'SESSION_MANAGER': 'local/unix:@/tmp/.ICE-unix/2578,unix/unix:/tmp/.ICE-unix/2578', 'COLORTERM': 'truecolor', 'VSCODE_DEBUGPY_ADAPTER_ENDPOINTS': '/home/longdpt/.vscode/extensions/ms-python.debugpy-2025.10.0-linux-x64/.noConfigDebugAdapterEndpoints/endpoint-1a7f6042c9ccdaa7.txt', 'HISTCONTROL': 'ignoredups', 'XDG_MENU_PREFIX': 'gnome-', 'TERM_PROGRAM_VERSION': '1.100.2', 'CONDA_EXE': '/home/longdpt/miniconda3/bin/conda', '_CE_M': '', 'HOSTNAME': 'fedora', 'HISTSIZE': '1000', 'JAVA_HOME': '/home/longdpt/miniconda3/envs/data/lib/jvm', 'SSH_AUTH_SOCK':

# Example of accessing an environment variable (dictionary-like access)
print(os.environ['HOME'])  # /home/longdpt
print(os.environ.get('HOME'))  # /home/longdpt


# Example of checking if an environment variable exists
if 'HOME' in os.environ:
    print("HOME environment variable exists")
else:
    print("HOME environment variable does not exist")
# HOME environment variable exists

#################
## os.getenv() ##
#################
'''
os.getenv(key, default=None) returns the value of the environment variable key if it exists, (like dict.get('key'))
otherwise returns default (None if not specified).
'''

print(os.getenv('HOME'))  # /home/longdpt
print(os.getenv('NON_EXISTING_VAR', default=None))  # None
print(os.getenv('NON_EXISTING_VAR', default='Not found'))  # Not found

print(os.getenv('SHELL'))
# '/bin/bash'

#################
## os.putenv() ##
#################
'''os.putenv(key, value) sets the environment variable key to value. (CHILD PROCESSES ONLY)'''

import os
import subprocess

os.putenv('MY_ENV_VAR', 'my_value')

# This returns None (current process)
print("Current process:", os.getenv('MY_ENV_VAR')) # None

# This shows the variable exists in child processes
result = subprocess.run(['python', '-c', 'import os; print("Child process:", os.getenv("MY_ENV_VAR"))'], 
                       capture_output=True, text=True)

print(result.stdout.strip()) # my_value