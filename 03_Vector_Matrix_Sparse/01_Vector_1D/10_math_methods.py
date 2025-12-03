'''
1. Statistical reduction methods:
   + arr.mean(): Computes the mean of all elements in the vector.
   + arr.sum(): Computes the sum of all elements in the vector.
   + arr.prod(): Computes the product of all elements in the vector.
   + arr.max(): Finds the maximum value in the vector.
   + arr.min(): Finds the minimum value in the vector.
   + arr.var(): Computes the variance of the elements in the vector.
   + arr.std(): Computes the standard deviation of the elements in the vector.
   + arr.ptp(): Computes the peak-to-peak (max - min) value of the vector. (i.e., range)

2. Cumulative methods:
   + arr.cumsum(): Computes the cumulative sum of the elements in the vector.
   + arr.cumprod(): Computes the cumulative product of the elements in the vector.

3. Rounding and clipping methods:
   + arr.round(decimals=...): Rounds each element in the vector to the specified
   + arr.clip(min=..., max=...): Clips (limits) the values in the vector to be within the specified minimum and maximum bounds.

4. Complex number methods:
   + arr.real: Returns a new vector containing the real parts of the complex numbers.
   + arr.imag: Returns a new vector containing the imaginary parts of the complex numbers.
   + arr.conj(): Returns a new vector containing the complex conjugates of the complex numbers.
   + arr.conjugate(): same as arr.conj().

5. Dot product:
   + arr1.dot(arr2): Computes the dot product between two vectors of the same length.
   + arr1 @ arr2: Another syntax to compute the dot product between two vectors of the same length.
'''

import numpy as np