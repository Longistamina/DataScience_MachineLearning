'''
Pathlib provides iterdir, glob, rglob, and walk methods for file system operations.

These methods allow you to iterate over directory contents, 
search for files matching patterns, and traverse directories recursively.

#################################################################

Flow of contents:
1. path_object.iterdir() - Iterate over directory contents. (like os.scandir())
2. path_object.glob(pattern) - Search for files matching a pattern in the directory. (like glob.glob())
3. path_object.rglob(pattern) - Recursively search for files matching a pattern in the directory and subdirectories.
4. path_object.walk() [Python 3.12+] - Recursively walk through the directory tree, yielding tuples of directory paths and file names.
'''

from pathlib import Path
import re

demo_path = Path("/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data")


#----------------------------------------------------------------------------------------------------------------#
#------------------------------------- 1. path_object.iterdir() -------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#

# .iterdir() returns an iterator of Path objects for the entries in the directory.
# To access the entries, you can use a for loop or convert it to a list.
# (works like os.scandir())

###############
## Basic use ##
###############

for entry in demo_path.iterdir():
    print(entry)
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/csv_tsv_files
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/txt_files
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/xml_files


######################
# Filtering entries ##
######################

for entry in demo_path.iterdir():
    if entry.is_file():
        print(f"File: {entry.name}")
    elif entry.is_dir():
        print(f"Directory: {entry.name}")
    else:
        print(f"Other: {entry.name}")
# Directory: csv_tsv_files
# Directory: txt_files
# Directory: json_files
# Directory: xml_files


###################################
## iter through its subdirectory ##
###################################

for entry in demo_path.joinpath("xml_files").iterdir():
    print(entry.name)
# food.xml
# plant_catalog.xml
# music_cd.xml
# new_written_starwars.xml


#####################################################
## combine with regular expression to filter files ##
#####################################################

json_pattern = r".*json.*"
txt_pattern = r".*txt.*"

for entry in demo_path.iterdir():
    if re.match(json_pattern, str(entry)): # convert the Path object to string for regex matching
        print(f"JSON directory: {entry.name}")
    
    elif re.match(txt_pattern, str(entry)):
        print(f"TXT directory: {entry.name}")
    
    else:
        continue

# TXT directory: txt_files
# JSON directory: json_files


#-------------------------------------------------------------------------------------------------------------#
#------------------------------------- 2. path_object.glob() -------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

# .glob(pattern) returns an iterator of Path objects matching the specified pattern in the directory.
# It works like glob.glob() but returns Path objects instead of strings.

''' glob DOES NOT allow regular expressions '''

'''
glob patterns:
- '*' matches everything
- '?' matches any single character
- '**' matches any number of directories (recursive)
- '/*.txt' matches all .txt files in the current directory
- 'subdir/*.txt' matches all .txt files in the 'subdir' directory
- 'subdir/**/*.txt' matches all .txt files in the 'subdir' directory (for glob() only, not rglob())
- [a-z] matches any single character in the range a-z
- [0-9] matches any single digit from 0 to 9
- [1-9][0-9] matches any two-digit number from 10 to 99
- [a-e|t-z] matches any character between a-c or between t-z
- [!a-z] matches any single character not in the range a-z
- *[!.py|!.txt] matches any files whose extension is not ".py" or ".txt"
'''
###############
## Basic use ##
###############

# search for all .sh files in the current directory
for entry in Path.cwd().glob("*.sh"): 
    print(entry.name)
# merge_mp4.sh
# download_youtube_commandline.sh


# search for all .txt files in the current directory
for entry in Path.cwd().glob("*.txt"):
    print(entry.name)
# Unrar_file.txt
# Python_Important_packages.txt
# vscode_install_settings.txt


########################
## Apply more pattern ##
########################

for entry in Path.cwd().joinpath("01_Python_Basic").glob("[1-2][0-9]_*.py"):  # '**' for recursive search
    print(entry.name)
# 10_String_methods_Cell.py
# 11_chr_ord.py
# 12_re_RegularExpression_regex.py
# 13_datetime_timedelta.py
# 14_calendar_import.py
# 15_if_elif_else.py
# 16_match_case.py
# 17_try_except_assertion_else.py
# 19_while_Loop_Nest.py
# 20_break_continue_pass.py
# 21_List_create_methods_comprehension.py
# 22_Tuple_create_methods_comprehension.py
# 23_Set_Frozenset_create_operations_methods.py
# 24_Dictionary_create_methods_comprehension.py
# 25_unpacking_operators.py
# 18_for_Loop_Nest_enumerate.py
# 26_TXT_open_read_write.py
# 27_CSV_TSV_open_read_write.py
# 28_JSON_load_dump.py
# 29_XML_parse_create_write.py


################################
## Exclusive glob() using "!" ##
################################

# The non-python elements:
for entry in Path.cwd().joinpath("01_Python_Basic").glob("*[!.py]"):  # Exclude all .py files
    print(entry.name)
# demo_data
# Exercises
# demo_package


# The elements that do not start with '0', '1', '2' or '3:
for entry in Path.cwd().joinpath("01_Python_Basic").glob("[!0-3]*"):  # Exclude all files starting with '0' or '1'
    print(entry.name)
# 40_multi_threading.py
# 41_multi_processing.py
# demo_data
# Exercises
# demo_module_same_directory.py
# demo_package
# 43_logging.py
# 44_loguru_logger.py
# 42_ArgumentParser_MainFunction.py
# 45_Debugging_demonstration.py


#############################
## ** for recursive search ##
#############################

for entry in demo_path.glob("**/*.xml"):  # '**' for recursive search
    print(entry)
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/xml_files/food.xml
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/xml_files/plant_catalog.xml
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/xml_files/music_cd.xml
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/xml_files/new_written_starwars.xml


for entry in demo_path.glob("*.xml"): # Without '**', return nothing
    print(entry)
    # (no output, because there are no .xml files in the given directory)


#####################################################
## combine with regular expression to filter files ##
#####################################################

target_pattern = r"^0\d{1}_.*\.py$"

for entry in Path.cwd().joinpath("01_Python_Basic").glob("*.py"): # Glob for all .py files
    if re.match(target_pattern, entry.name): # filter out .py files that satisfy the regex pattern
        print(entry.name)

# 02_Comments_singleLine_multipleLines.py
# 03_String_FormatSymbol.py
# 04_Variables.py
# 05_Casting_Convert_Datatypes.py
# 06_Operators.py
# 07_input_eval.py
# 08_import_dir_math_random.py
# 09_String_slicing_repr_RawString.py
# 01_print_termcolor.py


#################################
## Count the number of matches ##
#################################

# Count the number of python files in the 01_Python_Basic using normal glob("*.py")
py_count = sum(1 for _ in Path.cwd().joinpath("01_Python_Basic").glob("*.py")) # Use "_" as a looping factor to complete the for loop syntax, but not needed later
print(py_count) # 46

# Count the number of non-python files in the current directory using recursive glob("**/*[!.py]")
non_py_count = sum(1 for _ in Path.cwd().glob("**/*[!.py]"))
print(non_py_count) # 1926


#-------------------------------------------------------------------------------------------------------------#
#------------------------------------- 3. path_object.rglob() ------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

# .rglob(pattern) is similar to .glob() 
#  but it recursively searches for files matching the specified pattern in the directory and all its subdirectories.
# (so it works like glob() with '**' )

###############
## Basic use ##
###############

for entry in demo_path.rglob("*.json"):  # rglob for recursive search
    print(entry)

# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files/books.json
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files/emps.json
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files/LakeHuron.json
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files/large_100_age_1000.json
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files/Nile.json
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files/orange.json
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files/rivers.json
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files/sleep.json
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files/tivis.json
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files/women.json
# /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic/demo_data/json_files/new_written_jsondump.json


################################################
## Filter results with Path object attributes ##
################################################

for entry in Path.cwd().rglob("*.py"):
    if entry.parent.name == "02_Python_class_OOP":
        print(entry.name)

# 01_class_self_Introduction.py
# 04_other_magic_methods.py
# 05_ClassMethod.py
# 06_StaticMethod.py
# 07_inheritance.py
# 02_init_InstanceAttribute.py
# 03_dict_repr_ClassAttribute.py
# item.py
# 08_property_getter_setter_underscore.py
# 09_OOP_principles.py


#################################
## Exclusive rglob() using "!" ##
#################################

# The non-python elements:
for entry in Path.cwd().joinpath("01_Python_Basic").rglob("*[!.py|!.json]"):  # Exclude all .py and .json files
    print(entry.name)
# demo_data
# demo_package
# drinks.csv
# weather.tsv
# write_dictionary.csv
# write_list.csv
# write_quoting_all.csv
# write_quoting_non_numeric.csv
# write_tsv.tsv
# medals.csv
# ADream.txt
# Customers.txt
# HumptyDumpty.txt
# JohnnyJohnny.txt
# Rain.txt
# StudentScores.txt
# food.xml
# music_cd.xml
# new_written_starwars.xml
# plant_catalog.xml


# The elements that do not start with '0', '1', '2' or '3 and not a json file:
for entry in Path.cwd().joinpath("01_Python_Basic").rglob("[!0-3]*[!.json]"):  # Exclude all files starting with '0' or '1'
    print(entry.name)
# 40_multi_threading.py
# 41_multi_processing.py
# demo_data
# demo_module_same_directory.py
# demo_package
# 43_logging.py
# 44_loguru_logger.py
# 42_ArgumentParser_MainFunction.py
# 45_Debugging_demonstration.py
# Exercise_session_03_Birthday_StudentClassify.py
# Exercise_session_04_List_practice.py
# Exercise_session_05_Tuple_Set_Frozenset.py
# Exercise_session_06_Dictionary_UnpackingOperators.py
# Exercise_session_07_TXT_CSV_TSV.py
# Exercise_session_08_JSON_XML.py
# Exercise_session_01_calculate_circumference_area.py
# Exercise_session_02_StringMethods_RegularExpression.py
# Exercise_session_09_os_shutil.py
# package_module_2.py
# __init__.py
# package_module_1.py
# drinks.csv
# weather.tsv
# write_dictionary.csv
# write_list.csv
# write_quoting_all.csv
# write_quoting_non_numeric.csv
# write_tsv.tsv
# medals.csv
# ADream.txt
# Customers.txt
# HumptyDumpty.txt
# JohnnyJohnny.txt
# Rain.txt
# StudentScores.txt
# food.xml
# music_cd.xml
# new_written_starwars.xml
# plant_catalog.xml


############################################
## filter results with regular expression ##
############################################

expected_pattern = r"^1\d{1}_.*\.py$"

for entry in Path.cwd().rglob("*.py"):
    if re.match(expected_pattern, entry.name):
        print(Path(entry.parent.name, entry.name))  # print the file and the name of its nearest parent directory
        # output = Path(entry.parent.name) / entry.name
        # print(output)

# 01_Python_Basic/10_String_methods_Cell.py
# 01_Python_Basic/11_chr_ord.py
# 01_Python_Basic/12_re_RegularExpression_regex.py
# 01_Python_Basic/13_datetime_timedelta.py
# 01_Python_Basic/14_calendar_import.py
# 01_Python_Basic/15_if_elif_else.py
# 01_Python_Basic/16_match_case.py
# 01_Python_Basic/17_try_except_assertion_else.py
# 01_Python_Basic/19_while_Loop_Nest.py
# 01_Python_Basic/18_for_Loop_Nest_enumerate.py
# 02_Convex_Optimization_CVXPY/10_Quasiconvex_Functions.py
# 02_Convex_Optimization_CVXPY/11_LogConcave_LogConvex.py
# 02_Convex_Optimization_CVXPY/12_Convexity_respect_Generalized_Inequalities.py
# 02_Convex_Optimization_CVXPY/13_OptimizationStandardForm_LocalOptimal_ImplicitConstraints.py
# 02_Convex_Optimization_CVXPY/14_CvxOpt_StandardForm_LocalGlobalOptima.py


#################################
## Count the number of matches ##
#################################

# Count the number of python files in the current directory using rglob("*.py")
py_count = sum(1 for _ in Path.cwd().rglob("*.py")) # Use "_" as a looping factor to complete the for loop syntax, but not needed later
print(py_count) # 202

# Count the number of non-python and non-json files in the current directory using rglob("*[!.py|!.json]")
non_py_json_count = sum(1 for _ in Path.cwd().rglob("*[!.py|!.json]"))
print(non_py_json_count) # 1502


#--------------------------------------------------------------------------------------------------------------#
#------------------------------------- 4. path_object.walk() --------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

# path_object.walk() is a method that recursively walks through the directory tree, 
# yielding tuples of directory paths and file names.
# (like os.walk() but returns Path objects)

target_path = "/home/longdpt/Documents/Academic/DataScience_MachineLearning/"

###############
## Basic use ##
###############

for dirpath, dirnames, filenames in Path(target_path).walk():
    if ".git" in dirpath.parts:  # skip directories related to '.git'
        continue
    
    print(f'Current Directory: {dirpath}')
    for dirname in dirnames:
        print(f'Directory: {dirname}')
    for filename in filenames:
        print(f'File: {filename}')
    print('---')

# Current Directory: /home/longdpt/Documents/Academic/DataScience_MachineLearning/Calculus_ConvexOptimization/02_Convex_Optimization_CVXPY/exercises
# Directory: figures
# Directory: python
# File: additional_exercises.pdf


#######################################################
## combine with joinpath() to specify a subdirectory ##
#######################################################

for dirpath, dirnames, filenames in Path(target_path).joinpath("01_Python_Basic").walk():
    print(f'Current Directory: {dirpath}')
    for dirname in dirnames:
        print(f'Directory: {dirname}')
    for filename in filenames:
        print(f'File: {filename}')
    print('---')

# Current Directory: /home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic
# Directory: Exercises
# Directory: demo_data
# File: 02_Comments_singleLine_multipleLines.py
# File: 03_String_FormatSymbol.py
# File: 04_Variables.py
# File: 05_Casting_Convert_Datatypes.py
# File: 06_Operators.py
# File: 07_input_eval.py
# File: 10_String_methods_Cell.py