'''
Python script can be imported as a module to use its functions in other scripts.
Or it can be run directly to execute its code.

__name__ is a special variable that indicates whether the script is being run directly or imported as a module.

(if __name__ == "__main__") is True => the script is being run directly.
(if __name__ != "__main__") is False => the script is being imported as a module.
'''


#----------------------------------------------------------------------------------------------------#
#----------------------------- Import the module in the same directory ------------------------------#
#----------------------------------------------------------------------------------------------------#

''' The current directory MUST be in the same path as the module to import it directly.'''
import os
os.chdir("/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic")
# demo_module_same_directory.py module is in this directory
# => must move the current directory to this path to import the module directly

'''
After importing a module, a directory named __pycache__ will be created in the parent directory of that module.
This directory contains the compiled bytecode of the module, which is used to speed up future imports.

This directory is automatically created by Python when a module is imported.
You can safely ignore this directory, as it is not necessary for the module to work.
'''

#########################################
## import one function from the module ##
#########################################

from demo_module_same_directory import add

# Call the function
result = add(5, 3)
print(f"Result of the imported function: {result}")

# | INFO     | demo_module_same_directory:add:7 - This module is being imported
# 5 + 3 = 8


##################################################
## import all functions from the module using * ##
##################################################

''' DEMO if __name__ == "__main__" '''

from demo_module_same_directory import *

_ = add(5, 3)  # Assign to _ to avoid printing output in the console
# | INFO     | demo_module_same_directory:add:7 - This module is being imported
# 5 + 3 = 8

_ = subtract(10, 4) 
# | INFO     | demo_module_same_directory:subtract:15 - This module is being imported
# 10 - 4 = 6


#----------------------------------------------------------------------------------------------------#
#-------------------- Import the module from a package (different directory) ------------------------#
#----------------------------------------------------------------------------------------------------#

'''
Python package is a directory that contains an __init__.py file and can contain submodules.
So, when creating a package, must create an __init__.py file in the package directory.

The contents of the __init__.py file can be empty, or it can contain initialization code for the package.
'''
##################

''' The current directory MUST be in the same path as the package to import it. '''
import os
os.chdir("/home/longdpt/Documents/Academic/DataScience_MachineLearning/01_Python_Basic")
# demo_package is in this directory
# => must move the current directory to this path to import the demo_package


#----------------
## Import a module from module_1
#----------------

from demo_package.package_module_1 import subtract

_ = subtract(1255, 250)
# | INFO     | demo_package.package_module_1:subtract:15 - This module is being imported
# 1255 - 250 = 1005


#----------------
## Import all modules from module_2
#----------------

from demo_package.package_module_2 import *

_ = multiply(6, 2)
# | INFO     | demo_package.package_module_2:multiply:7 - This module is being imported
# 6 * 2 = 12

_ = divide(10, 2)
# | INFO     | demo_package.package_module_2:divide:15 - This module is being imported
# 10 / 2 = 5.0


#----------------------------------------------------------------------------------------------------#
#-------------------------------- Note about "from package import *" --------------------------------#
#----------------------------------------------------------------------------------------------------#

'''
PEP8 (Python Enhancement Proposal 8) recommends against using "from package import *" 

Because it can lead to confusion and make the code less readable.

Reasons:
# pollute the caller’s namespace and obscure the origin of identifiers,
# make accidental name collisions more likely,
# hobble tooling and auto-completion, and
# tie code correctness to the order of import * statements, which is fragile.
'''