'''
warnings is a built-in Python module that provides a way to issue warning messages to users of your code. 

Warnings are typically used to indicate that something unexpected happened, 
but it is not severe enough to raise an exception and halt the program.

###########################################################################

1. Issue a Warning: 
   + Basic usage: warnings.warn("warning message")
   + Specify Warning Category: warnings.warn("message", WarningCategory)

2. List of all Warning Categories:
   + Warning
   + UserWarning
   + DeprecationWarning
   + FutureWarning
   + PendingDeprecationWarning
   + RuntimeWarning
   + SyntaxWarning
   + ImportWarning
   + UnicodeWarning
   + BytesWarning
   + ResourceWarning

3. Create a Custom Warning using class:
   + class CustomWarning(UserWarning):....

4. Control Warning Behavior:
   + Simple filter: warnings.simplefilter(action, category=WarningCategory)
   + RegEx filter: warnings.filterwarnings(action, message='', category=WarningCategory)
   + All warning actions: "error", "ignore", "always", "default", "module", "once"
'''

import warnings


#----------------------------------------------------------------------------------------------------------#
#----------------------------------------- 1. Issue a Warning ---------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

#################
## Basic usage ##
#################

warnings.warn("This is a basic warning message.")
# <stdin>:1: UserWarning: This is a basic warning message.

'''
<stdin>:1: -> Location where the warning was issued (file and line number)
UserWarning: -> Type of warning (by default, UserWarning is used)
This is a basic warning message. -> The actual warning message
'''

##############################
## Specify Warning Category ##
##############################

warnings.warn("This is a deprecation warning.", DeprecationWarning)
# <stdin>:1: DeprecationWarning: This is a deprecation warning.

warnings.warn("This is a runtime warning.", RuntimeWarning)
# <stdin>:1: RuntimeWarning: This is a runtime warning


#----------------------------------------------------------------------------------------------------------#
#----------------------------------- 2. List of all Warning Categories ------------------------------------#
#----------------------------------------------------------------------------------------------------------#

'''
Warning: A base class for all warning categories.

UserWarning: A user-generated warning.

DeprecationWarning: Indicates that a feature is deprecated and will be removed in future versions.

FutureWarning: For end users, warns about changes in future versions of Python.

PendingDeprecationWarning: Similar to DeprecationWarning, but indicates that the feature is not yet deprecated.

RuntimeWarning: Warns about runtime issues that are not necessarily fatal (dubious behavior).

SyntaxWarning: Warns about dubious syntax that may lead to errors.

ImportWarning: Warns about issues during importing modules.

UnicodeWarning: Warns about Unicode-related issues.

BytesWarning: Warns about issues related to byte and bytearray operations.

ResourceWarning: Warns about resource usage issues, such as unclosed files.
'''


#----------------------------------------------------------------------------------------------------------#
#------------------------------ 3. Create a Custom Warning using class ------------------------------------#
#----------------------------------------------------------------------------------------------------------#

class DataQualityWarning(UserWarning):
    """Warning for data quality issues"""
    pass

warnings.warn("Data quality issue detected.", DataQualityWarning)
# <stdin>:1: DataQualityWarning: Data quality issue detected.


#----------------------------------------------------------------------------------------------------------#
#------------------------------------ 4. Control Warning Behavior -----------------------------------------#
#----------------------------------------------------------------------------------------------------------#

from loguru import logger

###################
## Simple filter ##
###################
'''warnings.simplefilter(action, category=WarningCategory) gives simple control over warning behavior.'''

# Ignore all DeprecationWarnings
warnings.simplefilter(action="ignore", category=DeprecationWarning)
warnings.warn("This is a deprecation warning.", DeprecationWarning)  # No output

# Convert all RuntimeWarnings into errors
warnings.simplefilter("error", RuntimeWarning)
try:
    warnings.warn("This is a runtime warning.", RuntimeWarning)
except RuntimeWarning as e:
    logger.error(f"Caught an error: {e}")
# 2025-11-18 15:11:27.898 | ERROR    | __main__:<module>:4 - Caught an error: This is a runtime warning.

##################
## RegEx filter ##
##################
'''warnings.filterwarnings(action, message='', category=WarningCategory) allows more granular control using regex.'''

# Ignore warnings containing "deprecated"
warnings.filterwarnings("ignore", message=".*deprecated.*")

warnings.warn("This feature is deprecated.", DeprecationWarning)  
# No output (because its message matches the regex, having the "deprecated" word)

warnings.warn("This is a future warning.", FutureWarning)
# <stdin>:1: FutureWarning: This is a future warning.

#########################
## All warning actions ##
#########################
'''
"error": Convert the warning into an exception.

"ignore": Ignore the warning.

"always": Always print the warning.

"default": Print the warning the first time it is encountered from a particular location.

"module": Print the warning the first time it is encountered in each module.

"once": Print the warning only the first time it is encountered, regardless of location.
'''