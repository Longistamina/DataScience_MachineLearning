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
mean_matrix = np.random.uniform(0, 10, (3, 4)).mean(axis=0).round(3)

print(mean_matrix)
# [6.454 5.815 6.107 6.552]

#################################
## Multi-line chaining methods ##
#################################

np.random.seed(0)
print(
    np.random.uniform(0, 10, (3, 4))  # Generate a random 3x4 matrix between 0 and 10
    .transpose()                      # Transpose the matrix to 4x3
    .mean(axis=0)                     # Calculate the mean vertically (for each column)
    .round(2)                         # Round the mean to 2 decimal place
)
# [6.03  6. 6.67]