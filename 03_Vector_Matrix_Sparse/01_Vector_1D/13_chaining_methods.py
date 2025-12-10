'''
Chaining methods is a technique used in programming to call multiple methods on the same object. 
This is typically done by having each method return the object itself (often referred to as "self" in object-oriented programming), 
allowing subsequent methods to be called on that returned object.
'''

import numpy as np

################################
## One-liner chaining methods ##
################################

np.random.seed(0)
mean_vector = np.random.uniform(0, 10, 5).round(2).mean()

print(mean_vector)
# 5.672

#################################
## Multi-line chaining methods ##
#################################

np.random.seed(0)
print(
    np.random.uniform(0, 10, 10)  # Generate 5 random numbers between 0 and 10
    .round(2)                     # Round the numbers to 2 decimal places
    .mean()                       # Calculate the mean of the rounded numbers
    .round(1)                     # Round the mean to 1 decimal place
)
# 6.2