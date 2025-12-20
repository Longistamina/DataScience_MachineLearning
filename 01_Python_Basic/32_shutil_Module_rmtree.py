'''
The shutil module (short for "shell utilities") is a powerful Python standard library module 
that provides high-level file and directory operations. 

It offers a comprehensive set of functions for copying, moving, renaming, and deleting files and directories, 
making it an essential tool for file management tasks in Python applications.

############################################

Flow of contents:
1. Copying files and directories: shutil.copy(), shutil.copy2(), shutil.copytree()
2. Moving files and directories: shutil.move()
3. Renaming files and directories: shutil.move() (also used for renaming)
4. Deleting files and directories: shutil.rmtree(), os.remove()
5. Creating and Extracting archives: shutil.make_archive(), shutil.unpack_archive()
6. Disk usage and Cmd Location
7. Miscellaneous utilities: shutil.get_terminal_size(), shutil.chown()
'''


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------- 1. Copying files and directories ------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

import shutil
import os

###########################
## shutil.copy(src, dst) ##
###########################
'''
shutil.copy() is used to copy a file from the source path (src) to the destination path (dst).
It copies the file's contents and permissions but not the metadata (like timestamps).
'''

os.system('echo "This is a demo file." > demo_file.txt')  # Create a demo file

shutil.copy('./demo_file.txt', # source file
            '/home/longdpt/Documents/Academic/DataScience_MachineLearning/demo_file_copy.txt')  # Destination copied file

# Check the original and copied files' metadata
os.system('ls -l ./demo_file.txt')
os.system('ls -l /home/longdpt/Documents/Academic/DataScience_MachineLearning/demo_file_copy.txt')

############################
## shutil.copy2(src, dst) ##
############################
'''shutil.copy2() is similar to shutil.copy(), but it also copies the file's metadata (like timestamps).'''

os.system('echo "This is a demo file." > demo_file_2.txt')  # Create a demo file

shutil.copy2('./demo_file_2.txt', # source file
            '/home/longdpt/Documents/Academic/DataScience_MachineLearning/demo_file_2_copy.txt')  # Destination copied file

# Check the original and copied files' metadata
os.system('ls -l ./demo_file_2.txt')
os.system('ls -l /home/longdpt/Documents/Academic/DataScience_MachineLearning/demo_file_2_copy.txt')

###############################
## shutil.copytree(src, dst) ##
###############################
'''
shutil.copytree() is used to copy an entire directory tree from the source path (src) to the destination path (dst).
It copies all files and subdirectories recursively.
'''

shutil.copytree('./02_Python_class_OOP',  # source directory
                '/home/longdpt/Documents/Academic/DataScience_MachineLearning/demo_dir_copy') # Destination copied directory


#-------------------------------------------------------------------------------------------------------#
#------------------------------------- 2. Moving files and directories ---------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''
shutil.move(src, dst) is used to move a file or directory from the source path (src) 
to the destination path (dst).
'''

os.mkdir('./empty_dest_dir')  # Create an empty destination directory

# Move a file
shutil.move('./demo_file.txt',  # source file
            './empty_dest_dir/')  # Destination moved file (now it will be ./empty_dest_dir/demo_file.txt)

# Move a directory
shutil.move('./demo_dir_copy',  # source directory
            './empty_dest_dir/')  # Destination moved directory (now it will be ./empty_dest_dir/demo_dir_copy)


#----------------------------------------------------------------------------------------------------------#
#------------------------------------- 3. Renaming files and directories ----------------------------------#
#----------------------------------------------------------------------------------------------------------#

os.system('echo "This is a demo file." > demo_file.txt')  # Create a demo file
os.makedirs('./original_name_dir/subdir')  # Create a directory for renaming demo

# Renaming files and directories can be done using shutil.move() as well.
shutil.move('./demo_file.txt',  # source file
            './original_name_dir/renamed_file.txt')  # Destination renamed file

shutil.move('./original_name_dir',  # source directory
            './renamed_dir')  # Destination renamed directory


#-----------------------------------------------------------------------------------------------------------#
#------------------------------------- 4. Deleting files and directories -----------------------------------#
#-----------------------------------------------------------------------------------------------------------#

shutil.copytree('./02_Python_class_OOP',  # Create a directory with subdirectories to demonstrate deletion
                '/home/longdpt/Documents/Academic/DataScience_MachineLearning/demo_dir_copy')

os.system('echo "This is a demo file." > demo_file.txt')  # Create a demo file

'''
shutil.rmtree(path) is used to delete an entire directory tree at the specified path (path).
'''

shutil.rmtree('/home/longdpt/Documents/Academic/DataScience_MachineLearning/demo_dir_copy')  # Delete the copied directory

# os.remove(path) is used to delete a single file at the specified path (path).
os.remove('./demo_file.txt')  # Delete the demo file


#------------------------------------------------------------------------------------------------------------#
#------------------------------------- 5. Creating and Extracting archives ----------------------------------#
#------------------------------------------------------------------------------------------------------------#

###########################
## shutil.make_archive() ##
###########################
'''
shutil.make_archive(base_name, format, root_dir=None, base_dir=None) is used to create an archive file.
base_name is the name of the archive file, format is the archive format (e.g, 'zip', 'tar', 'gztar', etc.),
root_dir is the root directory to archive, and base_dir is the directory within root_dir to archive.
'''

shutil.make_archive('/home/longdpt/Documents/Academic/DataScience_MachineLearning/demo_archive',  # base name (destination archive file name)
                    'zip',  # format (extension will be .zip)
                    root_dir='./02_Python_class_OOP',  # root directory to archive (source directory)
                    base_dir= '')  # base directory within root_dir to archive (set to '' to include all files in root_dir)

# List the contents of the created archive
os.system('unzip -l /home/longdpt/Documents/Academic/DataScience_MachineLearning/demo_archive.zip') 
#   Length      Date    Time    Name
# ---------  ---------- -----   ----
#      3104  06-09-2025 17:30   01_class_self_Introduction.py
#      9782  06-10-2025 17:37   04_other_magic_methods.py
#      1944  06-10-2025 11:30   05_ClassMethod.py

#############################
## shutil.unpack_archive() ##
#############################
'''
shutil.unpack_archive(filename, extract_dir=None, format=None) is used to extract an archive file.
filename is the path to the archive file, extract_dir is the directory to extract the contents,
and format is the archive format (optional, if not provided, it will be inferred from the filename).
'''

shutil.unpack_archive('./demo_archive.zip',  # source archive file to extract
                      './extracted_demo_archive',  # dst directory to extract the contents
                      'zip')  # format (optional, inferred from the filename)


#--------------------------------------------------------------------------------------------------------------------#
#------------------------------------- 6. Disk usage and Cmd Location -----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

#############################
## shutil.disk_usage(path) ##
#############################
'''
shutil.disk_usage(path) is used to get the disk usage statistics for the specified path (path). (in bytes)
'''

disk_usage = shutil.disk_usage('/')  # Get disk usage statistics for the root directory
print(f"Total: {disk_usage.total / (1024 ** 3):.2f} GB") # Convert bytes to GB by dividing by (1024 ** 3)
print(f"Used: {disk_usage.used / (1024 ** 3):.2f} GB")
print(f"Free: {disk_usage.free / (1024 ** 3):.2f} GB")

#######################
## shutil.which(cmd) ##
#######################
'''
shutil.which(cmd) is used to find the path of an executable command (cmd) in the system's PATH environment variable.
'''

python_path = shutil.which('python3')  # Find the path of the Python executable
if python_path:
    print(f"Python executable found at: {python_path}")
else:
    print("Python executable not found in PATH.")

# Python executable found at: /home/longdpt/miniconda3/envs/data/bin/python3


#------------------------------------------------------------------------------------------------------------#
#------------------------------------- 7. Miscellaneous utilities -------------------------------------------#
#------------------------------------------------------------------------------------------------------------#

################################
## shutil.get_terminal_size() ##
################################
'''
shutil.get_terminal_size(fallback=(columns, lines)) is used to get the size of the terminal window.
It returns a named tuple with the number of columns and lines in the terminal.
'''

terminal_size = shutil.get_terminal_size(fallback=(80, 24))  # Get terminal size with a fallback

print(terminal_size)
# os.terminal_size(columns=141, lines=9)

print(f"Terminal size: {terminal_size.columns} columns, {terminal_size.lines} lines")
# Terminal size: 141 columns, 9 lines

###############################################
## shutil.chown(path, user=None, group=None) ##
###############################################
'''
shutil.chown(path, user=None, group=None) is used to change the ownership of a file or directory at the specified path (path).
user is the new owner, and group is the new group (both optional).

NOTE: This operation may require superuser privileges.
'''

os.system('echo "echo Hello World!!!" > demo_permission.sh')  # Create a demo executable .sh file

shutil.chown('./demo_permission.sh', user='longdpt')  # Change ownership to 'longdpt'
shutil.chown('./demo_permission.sh', group='longdpt')  # Change group


# Check the file ownership after changing
os.system('ls -l ./demo_permission.sh')
# -rwxr-xr-x. 1 longdpt longdpt 20 Jul 18 11:26 ./demo_permission.sh