'''
Python has open() function which is used to open a file and returns a file object (file pointer).
The open() function takes two parameters: the file name and the mode in which the file
should be opened. The mode can be 'r' for reading, 'w' for writing, 'a' for appending, and 'b' for binary mode.

All types of files can be opened in Python, including text files, binary files (e.g image), and more.

All file modes:
'r'  - Read (default mode). Opens a file for reading, error if the file does not exist.
'w'  - Write. Opens a file for writing, creates a new file if it does not exist, truncates the file to zero length if it exists.
'x'  - Exclusive creation. Opens a file for writing, creates a new file, and raises an error if the file already exists.
'a'  - Append. Opens a file for appending at the end of the file without truncating it, creates a new file if it does not exist.
'b'  - Binary mode. Opens a file in binary mode (e.g., 'rb' or 'wb').
't'  - Text mode (default). Opens a file in text mode (e.g., 'rt' or 'wt').
'+'  - Read and write. Opens a file for both reading and writing (e.g., 'r+' or 'w+').
'r+' - Read and write. Opens a file for both reading and writing, error if the file does not exist.
'w+' - Write and read. Opens a file for both writing and reading, creates a new file if it does not exist, truncates the file to zero length if it exists.
'x+' - Exclusive creation and read. Opens a file for both writing and reading, creates a new file, and raises an error if the file already exists.
'a+' - Append and read. Opens a file for both appending and reading (e.g., 'a+').
'''

txt_demo_dir = '/home/longdpt/Documents/Academic/DataScience_MachineLearning_Python_SQL/01_Python_Basic/txt_files_demo'

#---------------------------------------------------------------------------------------------#
#---------------------------------- Read a file ----------------------------------------------#
#---------------------------------------------------------------------------------------------#

#######################
## (NOTT REOMMENDED) ##
## file = open().... ##
## txt = file.read() ##
## file.close()      ##
#######################

file = open(file = f'{txt_demo_dir}/JohnnyJohnny.txt', mode = 'r')  # "file" variable here is a file pointer
content = file.read()  # Read the entire file content as a whole string
file.close()
# (Must close the file pointer maunally)

print(content)  # Print the content of the file
# Johnny Johnny
# Yes Papa
# Eating sugar
# No, Papa

print(type(content)) # <class 'str'>


#############################
##     (REOMMENDED)        ##
## with open() as file:    ##
##      txt = file.read()  ##
#############################

with open(file = f'{txt_demo_dir}/JohnnyJohnny.txt', mode = 'r') as file:
    content = file.read()  # Read the entire file content as a whole string
# The file is automatically closed after the block of code is executed, no need to close it manually

print(content)
# Johnny Johnny
# Yes Papa
# Eating sugar
# No, Papa

print(type(content)) # <class 'str'>


# file.read(n) reads the first n characters from the file, if n is not specified, it reads the entire file.
with open(file = f'{txt_demo_dir}/JohnnyJohnny.txt', mode = 'r') as file:
    first_10_chars = file.read(10)  # Read the first 10 characters from the file
print(first_10_chars)  # Johnny Johnny
# (If the file has less than n characters, it will read the entire file and return it as a string)


#####################
## file.readline() ##
#####################

# file.readline() reads a single line from the file, including the newline character at the end of the line.
with open(file = f'{txt_demo_dir}/HumptyDumpty.txt', mode = 'r') as file:
    line1 = file.readline()  # Read the first line
    line2 = file.readline()  # Read the second line
    line3 = file.readline()  # Read the third line

print(line1)  # Humpty Dumpty sat on a wall,
print(line2)  # Humpty Dumpty had a great fall.
print(line3)  # All the king's horses

print(repr(line1))  # 'Humpty Dumpty sat on a wall,\n'
print(repr(line2))  # 'Humpty Dumpty had a great fall.\n
print(repr(line3))  # 'All the king\'s horses\n'
# (they have the newline character at the end of the line)

# Can use line.startwith() to check if the line starts with a specific string
print(line1.startswith('Humpty'))  # True
print(line3.startswith('Humpty'))  # False


######################
## file.readlines() ##
######################

# file.readlines() reads all lines from the file and returns a list of strings, each string is a line in the file.
with open(file = f'{txt_demo_dir}/HumptyDumpty.txt', mode = 'r') as file:
    list_lines = file.readlines()  # Read all lines into a list
                                   # Read the line as raw string, including the newline character at the end of the line

print(list_lines)  
# ['Humpty Dumpty sat on a wall,\n', 'Humpty Dumpty had a great fall.\n', "All the king's horses\n", "And all the king's men\n", 'Couldn\'t put Humpty together again.\n']


# Can use list comprehension to remove the newline character at the end of each line
list_lines = [line.strip() for line in list_lines]  # Remove the newline character
print(list_lines)
# ['Humpty Dumpty sat on a wall,', 'Humpty Dumpty had a great fall.', ... ]

# Can use list comprehension to check if the line starts with a specific string
list_lines = [line for line in list_lines if line.startswith('Humpty')]
print(list_lines)  # ['Humpty Dumpty sat on a wall,', 'Humpty Dumpty had a great fall.']


# file.readlines() can also be used to read a specific number of lines from the file
with open(file = f'{txt_demo_dir}/HumptyDumpty.txt', mode = 'r') as file:
    first_3_lines = file.readlines(3)  # Read the first 3 lines from the file
print(first_3_lines)
# ['Humpty Dumpty sat on a wall,\n', 'Humpty Dumpty had a great fall.\n', "All the king's horses\n"]
# (If the file has less than n lines, it will read the entire file and return it as a list of strings)


#####################
## file.readable() ##
#####################

# file.readable() returns True if the file is readable, False otherwise.
with open(file = f'{txt_demo_dir}/JohnnyJohnny.txt', mode = 'r') as file:
    is_readable = file.readable()  # Check if the file is readable
print(is_readable)  # True


###########################################################
## Most memory-efficient way to read a file line by line ##
###########################################################
with open(file = f'{txt_demo_dir}/ADream.txt', mode = 'r') as file:
    print("Student scores:")
    for line in file:
        print(line.strip())


#---------------------------------------------------------------------------------------------#
#---------------------------------- Write to a file ------------------------------------------#
#---------------------------------------------------------------------------------------------#

##################
## file.write() ##
##################

# file.write() writes a string to the file, if the file does not exist, it creates a new file.
# If the file exists, it truncates the file to zero length before writing (overwrite)

with open(file = f'{txt_demo_dir}/StudentScores.txt', mode = 'w') as file:
    file.write("Student scores:\n")  # Write a string to the file
    file.write("Alice: 90\n")
    file.write("Bob: 85\n")
    file.write("Charlie: 95\n")

# Check the content of the file
with open(file = f'{txt_demo_dir}/StudentScores.txt', mode = 'r') as file:
    content = file.read()   

print(content)
# Student scores:
# Alice: 90
# Bob: 85
# Charlie: 95

################### let's overwrite the file again ###################
with open(file = f'{txt_demo_dir}/StudentScores.txt', mode = 'w') as file:
    file.write("New Student scores:\n")  # Write a new string to the file
    file.write("David: 88\n")
    file.write("Eva: 92\n")

# Check the content of the file again
with open(file = f'{txt_demo_dir}/StudentScores.txt', mode = 'r') as file:
    content = file.read()

print(content)
# New Student scores:
# David: 88
# Eva: 92


#######################
## file.writelines() ##
#######################

# file.writelines() writes a list of strings to the file, if the file does not exist, it creates a new file.
# If the file exists, it truncates the file to zero length before writing (overwrite)

with open(file = f'{txt_demo_dir}/StudentScores.txt', mode = 'w') as file:
    lines = [
        "New Student scores:\n",
        "Frank: 80\n",
        "Grace: 87\n",
        "Hannah: 93\n"
    ]
    file.writelines(lines)  # Write a list of strings to the file

# Check the content of the file again
with open(file = f'{txt_demo_dir}/StudentScores.txt', mode = 'r') as file:
    content = file.read()

print(content)
# New Student scores:
# Frank: 80
# Grace: 87
# Hannah: 93


#####################
## file.writable() ##
#####################

# file.writable() returns True if the file is writable, False otherwise.
with open(file = f'{txt_demo_dir}/StudentScores.txt', mode = 'a') as file: # use mode 'a' to avoid truncating the file to zero length
    is_writable = file.writable()  # Check if the file is writable
print(is_writable)  # True

# False if the file is opened in read mode
with open(file = f'{txt_demo_dir}/StudentScores.txt', mode = 'r') as file:
    is_writable = file.writable()  # Check if the file is writable
print(is_writable)  # False

'''
NOTE: if the file has previous contents, then when you open it in write mode ('w'), 
      it will truncate the file to zero length before writing.
      Even if you write nothing to the file, it will still create an empty file !!!!
=> That's why in this part, we use append mode ('a') to avoid truncating the file to zero length.
'''


#---------------------------------------------------------------------------------------------------#
#---------------------------------- Write with append mode -----------------------------------------#
#---------------------------------------------------------------------------------------------------#

# file.write() and file.writelines() can also be used to append to a file without truncating it.
# If the file does not exist, it creates a new file.

# using append mode 'a' or 'a+' (append and read)

with open(file = f'{txt_demo_dir}/StudentScores.txt', mode = 'a') as file:
    file.write("Ivy: 89\n")  # Append a string to the file
    file.writelines(["Jack: 91\n", "Kathy: 84\n"])  # Append a list of strings to the file  

# Check the content of the file again
with open(file = f'{txt_demo_dir}/StudentScores.txt', mode = 'r') as file:
    content = file.read()

print(content)
# New Student scores:
# Frank: 80
# Grace: 87
# Hannah: 93
# Ivy: 89
# Jack: 91
# Kathy: 84
