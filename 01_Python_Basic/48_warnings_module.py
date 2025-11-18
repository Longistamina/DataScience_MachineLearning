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