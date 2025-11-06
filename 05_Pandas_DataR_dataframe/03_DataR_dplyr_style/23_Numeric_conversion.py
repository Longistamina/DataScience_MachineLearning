'''
1. dr.as_integer(): Convert to Integer

2. dr.as_double(): Convert to Double

3. dr.as_numeric(): Convert to Numeric
'''

import datar.all as dr
from datar import f
import pandas as pd

from pipda import register_verb
dr.filter = register_verb(func = dr.filter_)
dr.slice = register_verb(func = dr.slice_)

# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")


#---------------------------------------------------------------------------------------------------------------#
#------------------------------------------ 1. dr.as_integer() -------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

