'''
The os.path module is an essential tool for data scientists working with file systems in Python. 
It provides platform-independent functions for manipulating file and directory paths, 
making your code portable across different operating systems. 

####################################################################

Flow of contents:
1. Checking if a path exists using `os.path.exists()`
2. Check if a path is an abosolute path using `os.path.isabs()`
3. Checking if a path is a directory using `os.path.isdir()`
4. Checking if a path is a file using `os.path.isfile()`
5. Joining paths using `os.path.join()`
6. Getting the base name of a path using `os.path.basename()`
7. Getting the directory name of a path using `os.path.dirname()`
8. Splitting a path into its components using `os.path.split()`, `os.path.splitdrive()`, and `os.path.splitext()`
9. Using `os.path.normpath()` to normalize paths
10. Using `os.path.abspath()` to get the absolute path
11. Using `os.path.relpath()` to get a relative path
12. Using `os.path.commonpath()` to find the common path prefix
13. Using `os.path.commonprefix()` to find the common prefix of a list of paths
14. Using `os.path.sep` and `os.path.altsep` to understand path separators
15. Using `os.path.curdir` and `os.path.pardir` for current and parent directories
16. Using `os.path.islink()` to check for symbolic links
17. Using `os.walk()` to traverse directories
18. Using `os.path.getsize()` to get the size of a file
19. Using `os.path.getmtime()` to get the last modification time of a file
20. Using `os.path.getatime()` to get the last access time of a file
21. Using `os.path.getctime()` to get the creation time of a file
22. Using `os.path.samefile()` to check if two paths point to the same file
'''

import os

#---------------------------------------------------------------------#
#------------------- 1. Checking if a path exists --------------------#
#---------------------------------------------------------------------#

# Check a directory path
os.path.exists('/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic')
# True


# Check a file path
os.path.exists('/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/01_print_end_sep_termcolor.py')
# True


# Check a non-existing path
os.path.exists('non_existing_dir/non_existing_file.txt')
# False


#-------------------------------------------------------------------------------#
#------------------- 2. Check if a path is an absolute path --------------------#
#-------------------------------------------------------------------------------#

# Check an absolute path
os.path.isabs('/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/01_print_termcolor.py')
# True


# Check a non-absolute path
os.path.isabs('01_Python_Basic/01_print_termcolor.py')
# False


#-------------------------------------------------------------------------------#
#------------------- 3. Checking if a path is a directory ----------------------#
#-------------------------------------------------------------------------------#

# Check if a path is a directory
os.path.isdir('/home/longdpt/Documents/Academic/DataScience_MachineLearning/')
# True


# Check if a non-directory path
os.path.isdir('/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/01_print_termcolor.py')
# False


#-------------------------------------------------------------------------------#
#------------------- 4. Checking if a path is a file ---------------------------#
#-------------------------------------------------------------------------------#

# Check if a path is a file
os.path.isfile('/home/longdpt/Documents/Academic/DataScience_MachineLearning/Libraries_Installation.txt')
# True


# Check a non-file path
os.path.isfile('/home/longdpt/Documents/Academic/DataScience_MachineLearning')
# False


# Check a non-existing path
os.path.isfile('non_existing_file.txt')
# False


#-------------------------------------------------------------------------------#
#------------------- 5. Joining paths using os.path.join -----------------------#
#-------------------------------------------------------------------------------#
'''os.path.join() is used to join one or more path components intelligently.'''

# Join components without leading or trailing slashes
joined_path = os.path.join('dir_1', 'dir_2', 'file.txt')
print(joined_path) # dir_1/dir_2/file.txt


# Join components with leading or trailing slashes
joined_path = os.path.join('dir_parent/', 'dir_child/', 'file.txt')
print(joined_path) # dir_parent/dir_child/file.txt

'''
NOTE: os.path.join() automatically handles the path separators based on the operating system.
====> produces the same output even with or without leading or trailing slashes.
'''


#-------------------------------------------------------------------------------#
#------------------- 6. Getting the base name of a path ------------------------#
#-------------------------------------------------------------------------------#

demo_file_path = 'dir_1/dir_2/file.txt'
demo_dir_path = 'dir_1/dir_2/dir_3'


# Get the base name of the file path
base_name_file = os.path.basename(demo_file_path)
print(base_name_file) # file.txt

# Get the base name of the directory path
base_name_dir = os.path.basename(demo_dir_path)
print(base_name_dir) # dir_3

# Get the base name of a path with trailing slash
print(os.path.basename('/home/longdpt/Documents/')) # (an empty string)
'''NOTE: returns an empty string if the path ends with a trailing slash.'''


#-------------------------------------------------------------------------------#
#------------------- 7. Getting the directory name of a path -------------------#
#-------------------------------------------------------------------------------#

demo_path = 'dir_1/dir_2/file.txt'

# Get the directory name of the path
dir_name = os.path.dirname(demo_path)
print(dir_name) # dir_1/dir_2


#-------------------------------------------------------------------------------#
#------------------- 8. Splitting a path into its components -------------------#
#-------------------------------------------------------------------------------#

demo_path = 'dir_1/dir_2/file.txt'

#####################
## os.path.split() ##
#####################
'''os.path.split() splits the path into a tuple containing the directory and the base name.'''

split_path = os.path.split(demo_path)
print(split_path)  # ('dir_1/dir_2', 'file.txt')

##########################
## os.path.splitdrive() ##
##########################
'''os.path.splitdrive() splits the path into a tuple containing the drive and the rest of the path.'''

split_drive = os.path.splitdrive('/home/longdpt/')
print(split_drive)  # ('', 'home/longdpt/')

## It returns an empty string for the drive on non-Windows systems, as they do not have drive letters (like C:, D:, etc.).

########################
## os.path.splitext() ##
########################
'''os.path.splitext() splits the path into a tuple containing the base name and the file extension.'''

split_ext = os.path.splitext(demo_path)
print(split_ext)  # ('dir_1/dir_2/file', '.txt')

print(os.path.splitext('json_file.json'))  # ('json_file', '.json')


#--------------------------------------------------------------------------------#
#------------------- 9. Using os.path.normpath() to normalize paths -------------#
#--------------------------------------------------------------------------------#
'''os.path.normpath() normalizes the path by collapsing redundant separators and up-level references.'''

normalized_path = os.path.normpath('dir_1//dir_2/../file.txt')
print(normalized_path)  # dir_1/file.txt


#----------------------------------------------------------------------------------#
#------------------- 10. Using os.path.abspath() to get the absolute path ---------#
#----------------------------------------------------------------------------------#
'''
os.path.abspath() returns the absolute path of a given path.
NOTE: It does so by appending the current working directory to the given path if it is not absolute.
'''

absolute_path = os.path.abspath('dir_1/dir_2/file.txt')
print(absolute_path)  
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/dir_1/dir_2/file.txt


#-----------------------------------------------------------------------------------------#
#------------------- 11. Using os.path.relpath() to get a relative path ------------------#
#-----------------------------------------------------------------------------------------#

# os.path.relpath() returns the relative path from one directory to another.
relative_path = os.path.relpath('dir_1/dir_2/dir_3/file.txt',
                                 start='dir_1/dir_2')

print(relative_path)  
# dir_3/file.txt


#------------------------------------------------------------------------------------------#
#------------------- 12. Using os.path.commonpath() to find the common path prefix --------#
#------------------------------------------------------------------------------------------#
'''os.path.commonpath() returns the common path prefix of a list of paths.'''

common_path = os.path.commonpath(['dir_1/dir_2/file.txt', 'dir_1/dir_2/dir_3/file.txt'])
print(common_path)  # dir_1/dir_2


#---------------------------------------------------------------------------------------------------------#
#------------------- 13. Using os.path.commonprefix() to find the common prefix of paths -----------------#
#---------------------------------------------------------------------------------------------------------#
'''os.path.commonprefix() returns the common prefix of a list of paths.'''

common_prefix = os.path.commonprefix(['dir_1/dir_2/file.txt', 'dir_1/dir_2/dir_3/file.txt'])
print(common_prefix)  # dir_1/dir_2/


#------------------------------------------------------------------------------------------------------------#
#------------------- 14. Using os.path.sep and os.path.altsep to understand path separators -----------------#
#------------------------------------------------------------------------------------------------------------#

#################
## os.path.sep ##
#################
'''os.path.sep is the separator used by the operating system for paths.'''

print(os.path.sep)  # / on Unix-like systems, \ on Windows

####################
## os.path.altsep ##
####################
'''os.path.altsep is an alternative separator used by the operating system for paths.'''

print(os.path.altsep)  # None on Unix-like systems, / on Windows


#-----------------------------------------------------------------------------------------------------#
#------------ 15. Using os.path.curdir and os.path.pardir for current and parent directories ---------#
#-----------------------------------------------------------------------------------------------------#

####################
## os.path.curdir ##
####################
'''The symbolic name for the current directory.'''

print(os.path.curdir)  # .

####################
## os.path.pardir ##
####################
'''The symbolic name for the parent directory.'''

print(os.path.pardir)  # ..


#-----------------------------------------------------------------------------------------------------#
#------------------- 16. Using os.path.islink() to check for symbolic links --------------------------#
#-----------------------------------------------------------------------------------------------------#

# os.path.islink() checks if a path is a symbolic link.
is_link = os.path.islink('/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/01_print_termcolor.py')
print(is_link)  # False (if the file is not a symbolic link)

# Create a symbolic link for demonstration (uncomment the line below to create the link)
os.symlink(src="./Curriculum.txt", dst="symlink_to_curriculum.txt")

# Check a TRUE symbolic link
is_link = os.path.islink('./symlink_to_curriculum.txt')
print(is_link)  # True


#----------------------------------------------------------------------------------------------------#
#------------------------ 17. Using os.walk() to traverse directories -------------------------------#  
#----------------------------------------------------------------------------------------------------#
'''
os.path.walk() is used to traverse directories. However, it is deprecated in Python 3.x.

Instead, you can use os.walk() which is a generator that yields a tuple of (dirpath, dirnames, filenames) 
for each directory in the tree rooted at the specified directory.
'''

print(os.walk('/home/longdpt/Academic/DataScience_MachineLearning/01_Python_Basic'))
# <generator object walk at 0x7f1a1fd5b290>
# Not the content of the dir, only the generator object.

## Exmaple to use os.walk() to print all files in a directory tree ##
path_to_traverse = '/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic'

for dirpath, dirnames, filenames in os.walk(path_to_traverse):
    print(f'Current Directory: {dirpath}')
    for dirname in dirnames:
        print(f'Directory: {dirname}')
    for filename in filenames:
        print(f'File: {filename}')
    print('---')
# Current Directory: /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data
# Directory: csv_tsv_files
# Directory: txt_files
# Directory: json_files
# Directory: xml_files
# ---
# Current Directory: /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/csv_tsv_files
# File: drinks.csv
# File: medals.csv
# File: weather.tsv
# File: write_tsv.tsv
# File: write_quoting_all.csv
# File: write_quoting_non_numeric.csv
# File: write_list.csv
# File: write_dictionary.csv
# ---


#----------------------------------------------------------------------------------------------------#
#------------------- 18. Using os.path.getsize() to get the size of a file --------------------------#
#----------------------------------------------------------------------------------------------------#
'''os.path.getsize() returns the size of a file in bytes.'''

file_size = os.path.getsize('./01_Python_Basic/01_print_end_sep_termcolor.py')
print(file_size) # 5158 (bytes)


#------------------------------------------------------------------------------------------------------#
#------------------- 19. Using os.path.getmtime() to get the last modification time of a file ---------#
#------------------------------------------------------------------------------------------------------#

'''os.path.getmtime() returns the last modification time of a file as a timestamp.'''
last_mod_time = os.path.getmtime('./01_Python_Basic/01_print_end_sep_termcolor.py')
print(last_mod_time)  # 1766041388.2355113 (timestamp)


# Convert the timestamp to a human-readable format
import datetime
last_mod_time_human = datetime.datetime.fromtimestamp(last_mod_time)
print(last_mod_time_human)  # 2025-12-18 16:03:08.235511


#--------------------------------------------------------------------------------------------------------#
#------------------- 20. Using os.path.getatime() to get the last access time of a file -----------------#
#--------------------------------------------------------------------------------------------------------#

# os.path.getatime() returns the last access time of a file as a timestamp.
last_access_time = os.path.getatime('./01_Python_Basic/01_print_end_sep_termcolor.py')
print(last_access_time)  # 1766140589.234306 (timestamp)


# Convert the timestamp to a human-readable format
last_access_time_human = datetime.datetime.fromtimestamp(last_access_time)
print(last_access_time_human)  # 2023-10-15 12:34:43.9826865


#---------------------------------------------------------------------------------------------------------#
#------------------- 21. Using os.path.getctime() to get the creation time of a file ---------------------#
#---------------------------------------------------------------------------------------------------------#

# os.path.getctime() returns the creation time of a file as a timestamp.
creation_time = os.path.getctime('./01_Python_Basic/01_print_end_sep_termcolor.py')
print(creation_time)  # 1766041388.2355113 (timestamp)


# Convert the timestamp to a human-readable format
creation_time_human = datetime.datetime.fromtimestamp(creation_time)
print(creation_time_human)  # 2025-12-18 16:03:08.235511


#-----------------------------------------------------------------------------------------------------------#
#------------------- 22. Using os.path.samefile() to check if two paths point to the same file -------------#
#-----------------------------------------------------------------------------------------------------------#

# os.path.samefile() checks if two paths point to the same file.
same_file = os.path.samefile('./01_Python_Basic/01_print_end_sep_termcolor.py',
                             '/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/01_print_end_sep_termcolor.py')
print(same_file)  
# True (if both paths point to the same file)


print(os.path.samefile('./vscode_install_settings.txt', 'Libraries_Installation.txt'))
# False (if the files are different or do not exist)

''' NOTE: This function raises an OSError if either of the paths does not exist '''