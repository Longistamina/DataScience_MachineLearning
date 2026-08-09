'''
NumPy Universal Functions (ufunc)
==================================
https://numpy.org/doc/2.4/reference/ufuncs.html

A ufunc is a "vectorized" C-level function that operates element-by-element
on ndarrays.  It automatically handles broadcasting, type casting, and memory
layout.  Every ufunc also exposes five powerful methods:
    reduce / accumulate / reduceat / outer / at

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART A — UFUNC ANATOMY: ATTRIBUTES & INTROSPECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. nin / nout / nargs / ntypes / types / identity / signature
 2. __name__ / __doc__

PART B — OPTIONAL KEYWORD ARGUMENTS (all ufuncs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 3. out      : write result into an existing array (in-place / no alloc)
 4. where    : boolean mask — only compute at True positions
 5. casting  : type-casting policy ('no','equiv','safe','same_kind','unsafe')
 6. dtype    : override output dtype / computation dtype
 7. order    : memory layout of output ('K','C','F','A')
 8. axes / axis / keepdims : for generalised ufuncs (gufuncs)

PART C — METHOD: reduce
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 9. reduce(a, axis, dtype, out, keepdims, initial, where)
10. Multi-axis reduce / initial / where

PART D — METHOD: accumulate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. accumulate(a, axis, dtype, out)

PART E — METHOD: reduceat
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12. reduceat(a, indices, axis, dtype, out)

PART F — METHOD: outer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
13. outer(A, B)

PART G — METHOD: at   (unbuffered in-place + scatter_reduce)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
14. at(a, indices[, b])   — why it differs from fancy-indexing +=
15. scatter_sum           replicate torch.scatter_reduce_(..., reduce='sum')
16. scatter_prod          replicate torch.scatter_reduce_(..., reduce='prod')
17. scatter_mean          replicate torch.scatter_reduce_(..., reduce='mean')
18. scatter_amax          replicate torch.scatter_reduce_(..., reduce='amax')
19. scatter_amin          replicate torch.scatter_reduce_(..., reduce='amin')
20. include_self=False    replicate the include_self flag
21. 2-D scatter (dim=1)   multi-dimensional index tensors
22. Gather                replicate torch.gather()
23. Advanced: conditional scatter, batched scatter

PART H — MATH UFUNCS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
24. add / subtract / multiply / divide / floor_divide / mod / fmod / divmod
25. negative / positive / absolute / fabs / sign / rint
26. power / float_power / square / sqrt / cbrt / reciprocal
27. exp / exp2 / expm1 / log / log2 / log10 / log1p
28. logaddexp / logaddexp2
29. heaviside / gcd / lcm

PART I — TRIGONOMETRIC UFUNCS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
30. sin / cos / tan / arcsin / arccos / arctan / arctan2 / hypot
31. sinh / cosh / tanh / arcsinh / arccosh / arctanh
32. degrees / radians / deg2rad / rad2deg

PART J — BIT-TWIDDLING UFUNCS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
33. bitwise_and / bitwise_or / bitwise_xor / bitwise_not / invert
34. bitwise_left_shift / bitwise_right_shift / left_shift / right_shift

PART K — COMPARISON UFUNCS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
35. greater / greater_equal / less / less_equal / equal / not_equal
36. logical_and / logical_or / logical_xor / logical_not
37. maximum / minimum / fmax / fmin

PART L — FLOATING-POINT UFUNCS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
38. isfinite / isinf / isnan / isnat / signbit
39. copysign / nextafter / spacing
40. modf / ldexp / frexp
41. matmul (gufunc)

PART M — CREATING CUSTOM UFUNCS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
42. np.frompyfunc    : wrap any Python callable as a ufunc
43. np.vectorize     : vectorize with type inference (not a true ufunc)
'''

import numpy as np

rng = np.random.default_rng(42)

# ── shared test arrays ─────────────────────────────────────────────────────────
a   = np.array([1.0,  2.0,  3.0,  4.0,  5.0])
b   = np.array([10.0, 20.0, 30.0, 40.0, 50.0])

A   = np.arange(1, 7, dtype=float).reshape(2, 3)
# [[1, 2, 3],
#  [4, 5, 6]]

B   = np.arange(1, 7, dtype=float).reshape(3, 2)
# [[1, 2],
#  [3, 4],
#  [5, 6]]

i16 = np.array([0b1010, 0b1100, 0b0110], dtype=np.uint8)
j16 = np.array([0b0110, 0b1010, 0b1100], dtype=np.uint8)


#-------------------------------------------------------------------------------------------------#
#═══════════════════════  PART A — UFUNC ANATOMY: ATTRIBUTES & INTROSPECTION  ════════════════════#
#-------------------------------------------------------------------------------------------------#

######################
## Ufunc attributes ##
######################
'''
Every ufunc exposes a set of read-only informational attributes.

  ufunc.nin        : number of input arrays.
  ufunc.nout       : number of output arrays.
  ufunc.nargs      : total arguments = nin + nout.
  ufunc.ntypes     : number of type-resolution loops (one per dtype combo).
  ufunc.types      : list of type strings, each like 'ff->f' (float32 in/out).
  ufunc.identity   : identity element used by .reduce() — 0 for add, 1 for multiply,
                     None for ufuncs without a natural identity.
  ufunc.signature  : for generalised ufuncs (gufuncs) only — the shape
                     signature string like '(m,n),(n,k)->(m,k)' for matmul.
                     None for element-wise ufuncs.
  ufunc.__name__   : string name.

------------------------------

Explanation of ``ufunc.identity``

For addition: x + 0 = x
=> identity = 0

For multiplication: x * 1 = x
=> identity = 1

Given x = np.array([2, 3, 4])
=> addition reduce = 0 + 2 + 3 + 4
=> multiplication reduce = 1 × 2 × 3 × 4
'''

for uf, label in [(np.add,      'add'),
                  (np.multiply, 'multiply'),
                  (np.sin,      'sin'),
                  (np.divmod,   'divmod'),
                  (np.matmul,   'matmul')]:
    print(f"{label:<12}: nin={uf.nin}, nout={uf.nout}, nargs={uf.nargs}, "
          f"ntypes={uf.ntypes}, identity={uf.identity}, "
          f"signature={uf.signature!r}")
# add         : nin=2, nout=1, nargs=3, ntypes=22, identity=0, signature=None
# multiply    : nin=2, nout=1, nargs=3, ntypes=23, identity=1, signature=None
# sin         : nin=1, nout=1, nargs=2, ntypes=8, identity=None, signature=None
# divmod      : nin=2, nout=2, nargs=4, ntypes=15, identity=None, signature=None
# matmul      : nin=2, nout=1, nargs=3, ntypes=19, identity=None, signature='(n?,k),(k,m?)->(n?,m?)'

# Inspect type-resolution loops of np.add
print("\nnp.add type loops (first 5):", np.add.types[:5])
# ['??->?', 'bb->b', 'BB->B', 'hh->h', 'HH->H']
# Lower-case = signed, upper-case = unsigned; b=int8, h=int16, i=int32, f=float32, d=float64

# np.matmul is a gufunc with a shape signature
print("matmul signature:", np.matmul.signature)   # (n?,k),(k,m?)->(n?,m?)

vec1 = np.array([1, 2, 3])
vec2 = np.array([4., 5., 6.])


#-------------------------------------------------------------------------------------------------#
#══════════════════  PART B — OPTIONAL KEYWORD ARGUMENTS (apply to all ufuncs)  ══════════════════#
#-------------------------------------------------------------------------------------------------#

#########
## out ##
#########
'''
out : array or tuple of arrays, or None (default)

  Write the result directly into an existing array without allocating a new one.
  For ufuncs with one output pass a single array; for multiple outputs (e.g.
  divmod) pass a tuple of two arrays.

  Rules:
    • Shape must broadcast correctly against the inputs.
    • out can OVERLAP with an input: np.add(a, b, out=a) is safe — NumPy
      makes temporary copies when data dependency analysis requires it.
    • Pass out=np.empty(...) to pre-allocate and reuse buffers
      (avoids GC pressure in tight loops).
    • out=... (Ellipsis) forces a 0-D output to stay as a 0-D array instead
      of being converted to a Python scalar.
'''
print("\n=== out keyword ===")
result = np.empty(5)
np.add(a, b, out=result)
print("add into pre-allocated:", result)   # [11. 22. 33. 44. 55.]

# In-place (no extra allocation): ``a += b`` is sugar for ``np.add(a, b, out=a)``
a_copy = a.copy()
np.multiply(a_copy, 2.0, out=a_copy)
print("multiply in-place:", a_copy)   # [ 2.  4.  6.  8. 10.]

# Two-output ufunc: divmod
q = np.empty(5)
r = np.empty(5)
np.divmod(b, np.array([3., 3., 3., 3., 3.]), out=(q, r))
print("divmod quotient:", q, "  remainder:", r)
# divmod quotient: [ 3.  6. 10. 13. 16.]   remainder: [1. 2. 0. 1. 2.]

# Scalar 0-D: without out=
z0 = np.add(np.float64(1.0), np.float64(2.0))
print(f"0-D without out: type={type(z0)}")           # <class 'numpy.float64'>

z0e = np.add(np.float64(1.0), np.float64(2.0), out=np.empty(()))
print(f"0-D with out=:   type={type(z0e)}, val={z0e}")  # ndarray, 3.0

###########
## where ##
###########
'''
where : boolean array, broadcast-compatible with inputs and output

  True  positions: compute the ufunc and store the result in out.
  False positions: leave the corresponding element of out UNCHANGED
                   (or uninitialized if out was freshly allocated).

  Crucially: when out is uninitialized, False positions hold garbage.
  Always initialise out explicitly when using where with partial masks.

  Use cases:
    • Conditional element-wise operations without Python loops.
    • Safe division (avoid dividing where denominator is zero).
    • Masked arrays without using np.ma.
'''
print("\n=== where keyword ===")
x = np.array([1.0, 0.0, 3.0, 0.0, 5.0])
y = np.array([2.0, 2.0, 2.0, 2.0, 2.0])
mask = (x != 0)   # only divide where x ≠ 0

safe_div = np.ones(5)            # initialise output to a safe fallback (1)
np.divide(y, x, out=safe_div, where=mask)
print("Safe divide (where x≠0):", safe_div)   # [2.  1.  0.6667  1.  0.4]
# Positions where mask=False keep the initialised value 1.0

# Log of positive values only
vals = np.array([-2.0, 1.0, 4.0, -1.0, np.e])
log_out = np.full(5, np.nan) # [np.nan, np.nan, np.nan, np.nan, np.nan]
np.log(vals, out=log_out, where=(vals > 0))
print("Masked log:", log_out)   # [nan  0.  1.386  nan  1.]

#############
## casting ##
#############
'''
casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}  — default 'same_kind'

  Controls which type promotions are allowed when inputs differ from the
  chosen computation loop's dtype.

  'no'        : no type casting at all; inputs must match exactly.
  'equiv'     : byte-order changes only (e.g. big→little endian).
  'safe'      : value-preserving casts only (int→float is safe; float→int is not).
  'same_kind' : safe casts + casts within the same "kind" (e.g. float32→float64).
  'unsafe'    : any cast (including float→int truncation). Use with care.

  The default 'same_kind' catches most accidental type mismatches.
'''
print("\n=== casting keyword ===")
a_int = np.array([1, 2, 3], dtype=np.int32)
b_f64 = np.array([0.5, 1.5, 2.5], dtype=np.float64)

# 'safe': int32 → float64 is fine (no precision loss)
res_safe = np.add(a_int, b_f64, casting='safe')
print("casting='safe' (int+float):", res_safe, res_safe.dtype)
# casting='safe' (int+float): [1.5 3.5 5.5] float64

# 'unsafe': float64 → int32 (truncates)
out_int = np.empty(3, dtype=np.int32)
np.add(a_int, b_f64, out=out_int, casting='unsafe')
print("casting='unsafe' (truncated):", out_int)
# casting='unsafe' (truncated): [1 3 5]

# 'no': fails if dtypes differ
try:
    np.add(a_int, b_f64, casting='no')
except TypeError as e:
    print(f"casting='no' TypeError: {e}")
# casting='no' TypeError: Cannot cast ufunc 'add' input 0 from dtype('int32') to dtype('float64') with casting rule 'no'

###########
## dtype ##
###########
'''
dtype : dtype or None (default None)

  Override the computation precision regardless of input dtypes.
  The inputs are cast to this dtype before computation, and the output has
  this dtype.  Equivalent to specifying signature=(dtype, dtype, dtype).

  Key use cases:
    • Avoid integer overflow in reduce operations (dtype=np.int64 for int32 input).
    • Force float64 computation on float32 data for accuracy.
    • Force float32 everywhere for GPU-friendliness.
'''
print("\n=== dtype keyword ===")
big_ints = np.array([1e10, 2e10, 3e10], dtype=np.int64)
overflow_wrong = np.add.reduce(big_ints, dtype=np.int16)
print(f"add.reduce dtype=int16:      {overflow_wrong}")  # 22528 (overflow)

# dtype=np.int64 accumulates in 64-bit before placing in output
overflow_ok = np.add.reduce(big_ints, dtype=np.int64)
print(f"add.reduce dtype=int64:      {overflow_ok:.1e}")   # 6.0e+10 (correct)

# Force float32 computation
a32 = np.ones(4, dtype=np.float32)
res32 = np.multiply(a32, a32, dtype=np.float32)
print(f"multiply dtype=float32: {res32.dtype}")   # float32

###########
## order ##
###########
'''
order : {'K', 'C', 'F', 'A'}  — default 'K'

  Specifies the memory layout of the OUTPUT array.
    'K' : match the element order of the inputs as closely as possible.
    'C' : row-major (C-contiguous) — last index changes fastest.
    'F' : column-major (Fortran-contiguous) — first index changes fastest.
    'A' : F-contiguous if all inputs are F-contiguous, otherwise C.

  Rarely needed in practice; useful when the result feeds Fortran code or
  GPU kernels that require a specific layout.
'''
print("\n=== order keyword ===")
X_f = np.asfortranarray(A)   # F-contiguous
res_K = np.add(X_f, 1.0, order='K')   # preserves F layout
res_C = np.add(X_f, 1.0, order='C')   # forces C layout
print(f"order='K' is F-contig: {res_K.flags['F_CONTIGUOUS']}")   # True
print(f"order='C' is C-contig: {res_C.flags['C_CONTIGUOUS']}")   # True

###########################################
## axes / axis / keepdims  (gufunc only) ##
###########################################
'''
These three parameters only apply to generalised ufuncs (gufuncs),
which operate on sub-arrays (core elements) rather than scalars.

axis : int
  Shorthand for gufuncs with a single shared core dimension.
  np.matmul has signature (n?,k),(k,m?)->(n?,m?); not using axis directly.
  np.linalg internal gufuncs (e.g. _umath_linalg.solve) use axis.

axes : list of tuples
  Full control: specify which axis (axes) of each array argument is the "core" dimension.
  For matmul with signature (i,j),(j,k)->(i,k) on a batch of matrices stored in first two dims:
    axes=[(-2,-1), (-2,-1), (-2,-1)]

keepdims : bool  (default False)
  If True, the reduced core dimensions are kept with size 1,
  so the result broadcasts correctly back against the input.
  Only valid for gufuncs where all outputs have no core dimensions
  (signatures like (i),(i)->()).
'''
print("\n=== axes/axis/keepdims (matmul gufunc) ===")
# Batch matmul: stack of (2,3) @ (3,2) -> stack of (2,2)

batch_A = np.stack([A, A * 2])             # (2, 3) -> (2, 2, 3)
print(batch_A)
# [[[ 1.  2.  3.]
#   [ 4.  5.  6.]]
#
#  [[ 2.  4.  6.]
#   [ 8. 10. 12.]]]

batch_B = np.stack([B, B * 0.5])          #  (3, 2) -> (2, 3, 2)
print(batch_B)
# [[[1.  2. ]
#   [3.  4. ]
#   [5.  6. ]]
#
#  [[0.5 1. ]
#   [1.5 2. ]
#   [2.5 3. ]]]

batch_C = np.matmul(batch_A, batch_B)      # (2, 2, 2) — batched automatically
print("Batch matmul shape:", batch_C.shape)   # (2, 2, 2)

# Explicitly specify core axes (last two dims for each operand)
batch_C2 = np.matmul(batch_A, batch_B,
                     axes=[(-2,-1), (-2,-1), (-2,-1)])

'''
-1 => last axis
-2 => second-to-last axis

What does axes=[(-2,-1), (-2,-1), (-2,-1)])
+ 1st (-2, -1) means: batch_A shape = (2, 2, 3) -> get axes (-2, -1) -> 2 matrices (2, 3)
+ 2nd (-2, -1) means: batch_B shape = (2, 3, 2) -> get axes (-2, -1) -> 2 matrices (3, 2)

perfrom matrix multiplication on these: (2, 3) @ (3, 2) = (2, 2)
since batch size is 2 (axis=0) => we have TWO matrices (2, 2)

So:
+ 3rd (-2, -1) means: put these (2, 2) result matrices at the end
=> batch_C shape = (TWO, 2, 2)
'''

print(batch_C)
# [[[22. 28.]
#   [49. 64.]]
#
#  [[22. 28.]
#   [49. 64.]]]

print("axes= explicit:", np.allclose(batch_C, batch_C2))   # True


#-------------------------------------------------------------------------------------------------#
#═══════════════════════════════  PART C — METHOD: reduce  ═══════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

##############
## reduce() ##
##############
'''
ufunc.reduce(array, axis=0, dtype=None, out=None, keepdims=False,
             initial=<no value>, where=True)

  Reduces array's dimension by one (per axis reduced) by cumulatively
  applying the ufunc left-to-right along that axis.

  For np.add.reduce:   [a, b, c, d] → ((a+b)+c)+d = sum(array)
  For np.multiply.reduce: [a, b, c] → a*b*c = prod(array)
  For np.maximum.reduce: running maximum → max(array)

  Parameters:
    axis     : int, tuple of ints, or None. None reduces over all axes.
    dtype    : accumulation precision (critical for integer overflow).
    out      : destination array for the result.
    keepdims : if True, keep reduced axes with size 1.
    initial  : starting value for the reduction.  Required when array
               is empty; also useful to inject a known value.
               For np.add it defaults to 0 (the identity); for np.multiply to 1.
    where    : boolean mask — only include True positions in the reduction.

  Equivalent standard functions:
    np.add.reduce(x)      == np.sum(x)
    np.multiply.reduce(x) == np.prod(x)
    np.maximum.reduce(x)  == np.max(x)
    np.logical_and.reduce(x) == np.all(x)
    np.logical_or.reduce(x)  == np.any(x)
'''
print("\n=== reduce ===")
x = np.array([1, 2, 3, 4, 5])

print("add.reduce (sum)    :", np.add.reduce(x))            # 15
print("multiply.reduce (prod):", np.multiply.reduce(x))    # 120
print("maximum.reduce (max):", np.maximum.reduce(x))        # 5
print("logical_and.reduce  :", np.logical_and.reduce(x > 2)) # False (1,2 fail)
print("logical_or.reduce   :", np.logical_or.reduce(x > 4))  # True (5 passes)

# 2-D reduction along specified axis
M = np.array([[1, 2, 3],
              [4, 5, 6]])
print("add.reduce axis=0 (col sums):", np.add.reduce(M, axis=0))    # [5 7 9]
print("add.reduce axis=1 (row sums):", np.add.reduce(M, axis=1))    # [6 15]
print("add.reduce axis=None (total):", np.add.reduce(M, axis=None)) # 21

# keepdims: shape stays (2, 1) instead of (3,)
row_sums = np.add.reduce(M, axis=1, keepdims=True)
print("keepdims=True:\n", row_sums)
# keepdims=True:
#  [[ 6]
#  [15]]
print("keepdims=True shape:", row_sums.shape)   # (2, 1)

# initial: useful for empty arrays and injecting a head value
print("add.reduce([], initial=100):", np.add.reduce(np.array([]), initial=100))  # 100
print("add.reduce([1,2], initial=10):", np.add.reduce([1, 2], initial=10))       # 13

# where: only sum over even elements
w = np.array([True, False, True, False, True])
print("add.reduce where=[T,F,T,F,T]:", np.add.reduce(x, where=w, initial=0))   # 1+3+5=9

# dtype to prevent integer overflow
big = np.array([100_000] * 100, dtype=np.int32)
wrong = np.add.reduce(big, dtype=np.int16)   # overflows to -27008
right = np.add.reduce(big, dtype=np.int64)   #  10000000 (correct)
print(f"int16 reduce (overflows): {wrong}  |  int64 reduce: {right}")

# Multi-axis reduction: reduce over axes (0, 1) simultaneously
print("add.reduce axis=(0,1):", np.add.reduce(M, axis=(0, 1)))   # 21
# ``np.add.reduce(M, axis=(1, 0))`` does the same thing


#-------------------------------------------------------------------------------------------------#
#═════════════════════════════  PART D — METHOD: accumulate  ═════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

##################
## accumulate() ##
##################
'''
ufunc.accumulate(array, axis=0, dtype=None, out=None)

  Like reduce, but stores every intermediate result — the running (cumulative)
  application of the ufunc.  Output has the same shape as input.

  np.add.accumulate([1,2,3,4]) → [1, 1+2, 1+2+3, 1+2+3+4] = [1, 3, 6, 10]
  np.multiply.accumulate(x)    → running product (like math.factorial list)
  np.maximum.accumulate(x)     → running maximum

  Equivalent functions:
    np.add.accumulate(x)       == np.cumsum(x)
    np.multiply.accumulate(x)  == np.cumprod(x)

  Only one axis may be reduced at a time (unlike reduce).
  Output shape is identical to input shape.
'''
print("\n=== accumulate ===")
x = np.array([1, 2, 3, 4, 5])

print("add.accumulate      :", np.add.accumulate(x))         # [ 1  3  6 10 15]
print("multiply.accumulate :", np.multiply.accumulate(x))    # [  1   2   6  24 120]
print("maximum.accumulate  :", np.maximum.accumulate(np.array([3,1,4,1,5,9,2,6]))) # [ 3  3  4  4  5  9  9  9]
print("minimum.accumulate  :", np.minimum.accumulate(np.array([9,5,6,2,8,1,3]))) # [9 5 5 2 2 1 1]

# 2-D: accumulate along columns (axis=0) or rows (axis=1)
M = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
print("add.accumulate axis=0 (cumsum per column):\n", np.add.accumulate(M, axis=0))
#  [[ 1  2  3]
#   [ 5  7  9]
#   [12 15 18]]
print("add.accumulate axis=1 (cumsum per row):\n", np.add.accumulate(M, axis=1))
#  [[ 1  3  6]
#   [ 4  9 15]
#   [ 7 15 24]]

# Log-sum-exp accumulation: logaddexp accumulates in log-space
log_probs = np.log(np.array([0.1, 0.3, 0.2, 0.4]))
log_cumsum = np.logaddexp.accumulate(log_probs)
print("logaddexp.accumulate (log cumsum):", np.exp(log_cumsum).round(4))
# [0.1  0.4  0.6  1.0] (cumulative probability)

# Running maximum useful for high-water mark / drawdown
prices = np.array([100., 105., 102., 108., 103., 112., 109.])
peak   = np.maximum.accumulate(prices)
drawdown = (prices - peak) / peak * 100
print("Running peak   :", peak) # [100. 105. 105. 108. 108. 112. 112.]
print("Drawdown (%)   :", drawdown.round(2)) # [ 0.    0.   -2.86  0.   -4.63  0.   -2.68]


#-------------------------------------------------------------------------------------------------#
#══════════════════════════════  PART E — METHOD: reduceat  ══════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

################
## reduceat() ##
################
'''
ufunc.reduceat(array, indices, axis=0, dtype=None, out=None)

  Performs a LOCAL reduce over sub-ranges defined by indices.
  Produces an output of the SAME length as indices.

  For each i in range(len(indices)):
    If i < len(indices)-1 and indices[i] < indices[i+1]:
      out[i] = ufunc.reduce(array[indices[i] : indices[i+1]])
    Else (last segment OR indices[i] >= indices[i+1]):
      out[i] = array[indices[i]]    ← single element (no reduction!)

  Key insight: indices[i] >= indices[i+1] means "no slice" — just copy.
  Indices must be non-negative integers; must be valid for the array axis.

  Think of it as a "group-by reduce" where indices mark segment starts.
  Equivalent to (but faster than):
    [ufunc.reduce(array[indices[i]:indices[i+1]]) for i in range(len(indices))]
  with the last segment going to end-of-array.
'''
print("\n=== reduceat ===")
x = np.array([1., 2., 3., 4., 5., 6., 7., 8.])

# Segment starts: [0, 3, 5] → segments [0:3], [3:5], [5:end]
idx = [0, 3, 5]
print("add.reduceat (group sums):", np.add.reduceat(x, idx))
# [0:3] = 1+2+3=6,  [3:5] = 4+5=9,  [5:8] = 6+7+8=21  →  [6. 9. 21.]

print("max.reduceat (group max) :", np.maximum.reduceat(x, idx))
# [3. 5. 8.]

# Single-element "no-reduce" when consecutive indices are equal or decreasing
idx2 = [0, 2, 2, 5]  # indices[2]=2 >= indices[2+1]=5? No, 2<5; but indices[1]=2 == indices[2]=2
print("reduceat [0,2,2,5]:", np.add.reduceat(x, [0, 2, 2, 5]))
# [0:2]=1+2=3, [2:2]=x[2]=3 (single), [2:5]=3+4+5=12, [5:]=6+7+8=21  → [3. 3. 12. 21.]

# 2-D: reduceat along rows (axis=0)
M = np.arange(12, dtype=float).reshape(4, 3)
# Group rows 0-1 and rows 2-3
row_groups = np.add.reduceat(M, [0, 2], axis=0)
print("add.reduceat rows [0,2]:\n", row_groups)
#  [[0+3 1+4 2+5], [6+9 7+10 8+11]] = [[3 5 7],[15 17 19]]

# Practical use: segment statistics (like groupby sum for sorted group labels)
values = np.array([10., 20., 30., 40., 50., 60., 70., 80., 90.])
# Groups: [0:3], [3:6], [6:9]
group_starts = np.array([0, 3, 6])
print("Group sums:", np.add.reduceat(values, group_starts))         # [60. 150. 240.]
print("Group max :", np.maximum.reduceat(values, group_starts))     # [30. 60. 90.]
print("Group min :", np.minimum.reduceat(values, group_starts))     # [10. 40. 70.]

# Sparse group-by: use np.unique to get segment starts from sorted labels
labels = np.array([0, 0, 0, 1, 1, 2, 2, 2, 2])   # group labels (must be sorted)
_, starts = np.unique(labels, return_index=True)
print("Group sums via unique:", np.add.reduceat(values, starts))   # [ 60.  90. 300.]


#-------------------------------------------------------------------------------------------------#
#═══════════════════════════════  PART F — METHOD: outer  ════════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

###########
## outer ##
###########
'''
ufunc.outer(A, B, /, **kwargs)
  Apply ufunc to all pairs (a, b) with a in A and b in B.
  Output shape: A.shape + B.shape.

  For binary ufuncs: out[i, j] = ufunc(A[i], B[j]).
  Not restricted to 1-D inputs.

  np.add.outer(A, B)          : out[i,j] = A[i] + B[j]
  np.multiply.outer(A, B)     : out[i,j] = A[i] * B[j]  (outer product)
  np.subtract.outer(A, B)     : out[i,j] = A[i] - B[j]  (pairwise differences)
  np.equal.outer(A, B)        : out[i,j] = (A[i] == B[j])  (membership mask)
  np.logical_and.outer(A, B)  : out[i,j] = A[i] & B[j]

  np.multiply.outer(A, B) == np.outer(A, B) == np.tensordot(A, B, 0)
  for 1-D arrays, but outer() generalises to any shape.
'''
print("\n=== outer ===")
u = np.array([1., 2., 3.])
v = np.array([10., 20., 30., 40.])

# Outer product — standard linear algebra outer product
print("multiply.outer:\n", np.multiply.outer(u, v))
# [[ 10  20  30  40]
#  [ 20  40  60  80]
#  [ 30  60  90 120]]

# Pairwise differences — useful for distance matrices
print("subtract.outer (pairwise diff):\n", np.subtract.outer(u, u))
# [[ 0 -1 -2]
#  [ 1  0 -1]
#  [ 2  1  0]]

# add.outer: broadcasting addition table
print("add.outer:\n", np.add.outer(np.array([0,10,20]), np.array([1,2,3])))
# [[ 1  2  3]
#  [11 12 13]
#  [21 22 23]]

# equal.outer: one-hot encoding via membership
categories = np.array([0, 1, 2])
samples    = np.array([0, 2, 1, 2, 0])
one_hot    = np.equal.outer(samples, categories).astype(int)
print("One-hot encoding:\n", one_hot)
# [[1 0 0]
#  [0 0 1]
#  [0 1 0]
#  [0 0 1]
#  [1 0 0]]

# power.outer: exponentiation table
print("power.outer:\n", np.power.outer(np.arange(1, 4), np.arange(0, 4)))
# [[1 1 1 1]
#  [1 2 4 8]
#  [1 3 9 27]]

# 2-D outer: shape becomes A.shape + B.shape
P = np.array([[1., 2.], [3., 4.]])
Q = np.array([[5., 6.], [7., 8.]])
PQ = np.multiply.outer(P, Q)
print("2-D outer shape:", PQ.shape)   # (2,2,2,2)
print("PQ[0,0]:", PQ[0, 0])          # [[5 6],[7 8]] = 1 * Q


#-------------------------------------------------------------------------------------------------#
#══════════════════════════════════  PART G — METHOD: at  ════════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

########
## at ##
########
'''
ufunc.at(a, indices, b=None)

  Perform UNBUFFERED in-place operation on array `a` at positions `indices`.
  For binary ufuncs: a[indices] = ufunc(a[indices], b)
  For unary ufuncs:  a[indices] = ufunc(a[indices])

  ─── WHY .at() EXISTS: the repeated-index problem ────────────────────────────
  Fancy-index assignment (a[idx] += b) is BUFFERED:
    • NumPy reads a[idx] once into a buffer.
    • Computes buffer + b.
    • Writes back ONCE per unique index.
    • If index i appears k times, only the LAST write survives for += /
      only the last += increment is applied (not k increments).

  np.add.at(a, idx, b) is UNBUFFERED:
    • For each position in idx (in order), it reads the CURRENT value of a,
      applies the ufunc immediately, and writes back.
    • Repeated indices accumulate correctly: each occurrence of index i
      contributes one increment.

  This makes .at() the NumPy equivalent of PyTorch's scatter_reduce_()
  family, as shown in the extensive examples below.
'''

# ── Motivating example: the buffered vs unbuffered difference ─────────────────
print("\n=== at vs fancy-index buffering problem ===")
idx = np.array([0, 0, 0])    # index 0 repeated 3 times
src = np.array([1., 2., 3.])

out_buffered = np.zeros(3)
out_buffered[idx] += src       # WRONG: only last value applied
print("Buffered   (a[idx]+=src):", out_buffered)   # [3. 0. 0.]  ← only src[2]=3

out_unbuffered = np.zeros(3)
np.add.at(out_unbuffered, idx, src)               # CORRECT
print("Unbuffered (add.at)     :", out_unbuffered) # [6. 0. 0.]  ← 1+2+3=6


# ─────────────────────────────────────────────────────────────────────────────
# SCATTER / GATHER EQUIVALENTS FOR torch.scatter_reduce_() / torch.gather()
#
# PyTorch API:
#   out.scatter_reduce_(dim, index, src, reduce, *, include_self=True)
#   reduce ∈ {'sum', 'prod', 'mean', 'amax', 'amin'}
#
# Shape convention (1-D):
#   For each i: out[index[i]] <reduce>= src[i]
#
# NumPy equivalents built from ufunc.at():
#   sum   → np.add.at(out, index, src)
#   prod  → np.multiply.at(out, index, src)
#   mean  → add.at + count, then divide
#   amax  → np.maximum.at  (initialise with -∞ or include_self value)
#   amin  → np.minimum.at  (initialise with +∞ or include_self value)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*68)
print("SCATTER_REDUCE REPLICATIONS  (torch.scatter_reduce_ in NumPy)")
print("="*68)

src   = np.array([1., 2., 3., 4., 5., 6.])
index = np.array([2,  0,  2,  1,  0,  2 ])
# Mapping:  out[2]←1, out[0]←2, out[2]←3, out[1]←4, out[0]←5, out[2]←6
# Expected sums:  out[0]=2+5=7, out[1]=4, out[2]=1+3+6=10

# demo ``np.add.at()``
out = np.zeros(3)
np.add.at(out, index, src)
print(out) # [ 7.  4. 10.]

# ── scatter_sum  ──────────────────────────────────────────────────────────────
print("\n--- scatter_sum ---")
'''
torch:  out.scatter_reduce_(0, index, src, reduce='sum', include_self=True)

include_self=True  (default): out's initial values participate in the reduction.
include_self=False          : reset out to identity (0) before scattering.

numpy:
  out = initial_self.copy()   # self values
  np.add.at(out, index, src)  # accumulate src into out at index positions
'''

def scatter_sum(src, index, include_self=True, self_val=None):
    '''1-D scatter reduce with sum.  Returns a new array.'''

    out_size = len(np.unique(index))

    if self_val is None:
        self_val = np.zeros(out_size)
    out = self_val.copy() if include_self else np.zeros(out_size)
    np.add.at(out, index, src)
    return out

out_sum = scatter_sum(src, index)
print(f"scatter_sum (include_self=True, self=0): {out_sum}")  # [7. 4. 10.]

# include_self=True with non-zero self
self_tensor = np.array([100., 200., 300.])
out_sum_self = scatter_sum(src, index, include_self=True, self_val=self_tensor)
print(f"scatter_sum (include_self=True, self=[100,200,300]): {out_sum_self}")
# [100+2+5, 200+4, 300+1+3+6] = [107. 204. 310.]

out_sum_noself = scatter_sum(src, index, include_self=False)
print(f"scatter_sum (include_self=False): {out_sum_noself}")  # [7. 4. 10.]


# ── scatter_prod  ─────────────────────────────────────────────────────────────
print("\n--- scatter_prod ---")
'''
torch:  out.scatter_reduce_(0, index, src, reduce='prod', include_self=True)

numpy:
  out = self_val.copy()          # include_self=True: start from self values
  # include_self=False: start from identity (1.0) regardless of self
  np.multiply.at(out, index, src)
'''

def scatter_prod(src, index, include_self=True, self_val=None):

    out_size = len(np.unique(index))

    if self_val is None:
        self_val = np.ones(out_size)
    out = self_val.copy() if include_self else np.ones(out_size)
    np.multiply.at(out, index, src)
    return out

out_prod = scatter_prod(src, index)
print(f"scatter_prod (include_self=True, self=1): {out_prod}")
# out[0] = 1*2*5=10, out[1] = 1*4=4, out[2] = 1*1*3*6=18  →  [10.  4. 18.]

out_prod_self = scatter_prod(src, index, include_self=True,
                             self_val=np.array([2., 3., 4.]))
print(f"scatter_prod (self=[2,3,4]): {out_prod_self}")
# out[0]=2*2*5=20, out[1]=3*4=12, out[2]=4*1*3*6=72  →  [20. 12. 72.]

out_prod_noself = scatter_prod(src, index, include_self=False)
print(f"scatter_prod (include_self=False): {out_prod_noself}")  # [10.  4. 18.]


# ── scatter_mean  ─────────────────────────────────────────────────────────────
print("\n--- scatter_mean ---")
'''
torch:  out.scatter_reduce_(0, index, src, reduce='mean', include_self=True)

The "mean" reduction requires tracking how many values contribute to each slot.

include_self=True  : count starts at 1 (self's value is one contribution).
include_self=False : count starts at 0 (only src values contribute).

numpy:
  # Step 1: compute per-slot sum (using add.at)
  # Step 2: compute per-slot count
  # Step 3: out_mean = (self_sum + scatter_sum) / total_count
'''

def scatter_mean(src, index, include_self=True, self_val=None):

    out_size = len(np.unique(index))

    if self_val is None:
        self_val = np.zeros(out_size)

    # count: 1 per slot if include_self, 0 if not
    count = np.ones(out_size, dtype=float) if include_self else np.zeros(out_size, dtype=float)
    np.add.at(count, index, 1.0)      # add 1 per occurrence in index

    # sum: start from self if include_self, else from 0
    out_s = self_val.copy() if include_self else np.zeros(out_size)
    np.add.at(out_s, index, src)

    # avoid division by zero (slots with count=0 stay at 0)
    return np.where(count > 0, out_s / count, 0.0)

out_mean = scatter_mean(src, index, include_self=False)
print(f"scatter_mean (include_self=False): {out_mean}")
# out[0]=(2+5)/2=3.5, out[1]=4/1=4, out[2]=(1+3+6)/3=10/3≈3.333

out_mean_self = scatter_mean(src, index, include_self=True,
                             self_val=np.array([10., 20., 30.]))
print(f"scatter_mean (include_self=True, self=[10,20,30]): {out_mean_self.round(4)}")
# out[0]=(10+2+5)/3=17/3≈5.667, out[1]=(20+4)/2=12, out[2]=(30+1+3+6)/4=40/4=10

K = len(np.unique(index))
count_check = np.zeros(K)
np.add.at(count_check, index, 1)
print(f"  count per slot: {count_check}")   # [2. 1. 3.]


# ── scatter_amax  ─────────────────────────────────────────────────────────────
print("\n--- scatter_amax ---")
'''
torch:  out.scatter_reduce_(0, index, src, reduce='amax', include_self=True)

numpy:
  include_self=True  : initialise out with self values (they compete with src).
  include_self=False : initialise out with -∞ (identity for maximum), then
                       overwrite slots that received no src with -∞ → can
                       choose to leave as -∞ or treat as 0 per use case.
  np.maximum.at(out, index, src)  — unbuffered: each src[i] competes with
    the CURRENT value of out[index[i]], updating it if larger.
'''

def scatter_amax(src, index, include_self=True, self_val=None):

    out_size = len(np.unique(index))

    if self_val is None:
        self_val = np.zeros(out_size)
    # include_self=True : start with self values
    # include_self=False: start with -inf so only src values matter
    if include_self:
        out = self_val.copy()
    else:
        out = np.full(out_size, -np.inf)
    np.maximum.at(out, index, src)
    return out

out_amax = scatter_amax(src, index, include_self=False)
print(f"scatter_amax (include_self=False): {out_amax}")
# out[0]=max(2,5)=5, out[1]=max(4)=4, out[2]=max(1,3,6)=6  →  [5. 4. 6.]

out_amax_self = scatter_amax(src, index, include_self=True,
                             self_val=np.array([100., 0., 2.]))
print(f"scatter_amax (self=[100,0,2]): {out_amax_self}")
# out[0]=max(100,2,5)=100, out[1]=max(0,4)=4, out[2]=max(2,1,3,6)=6 → [100. 4. 6.]

# Step-by-step trace: watch unbuffered maximum update
print("Trace of np.maximum.at for index=[2,0,2,1,0,2], src=[1,2,3,4,5,6]:")
out_trace = np.full(K, -np.inf)
for step, (i, s) in enumerate(zip(index, src)):
    old = out_trace[i]
    np.maximum.at(out_trace, np.array([i]), np.array([s]))
    print(f"  step {step}: index={i}, src={s}, {old:.0f} → {out_trace[i]:.0f}")
# Trace of np.maximum.at for index=[2,0,2,1,0,2], src=[1,2,3,4,5,6]:
#   step 0: index=2, src=1.0, -inf → 1
#   step 1: index=0, src=2.0, -inf → 2
#   step 2: index=2, src=3.0, 1 → 3
#   step 3: index=1, src=4.0, -inf → 4
#   step 4: index=0, src=5.0, 2 → 5
#   step 5: index=2, src=6.0, 3 → 6


# ── scatter_amin  ─────────────────────────────────────────────────────────────
print("\n--- scatter_amin ---")
'''
torch:  out.scatter_reduce_(0, index, src, reduce='amin', include_self=True)

numpy:
  np.minimum.at(out, index, src)
  Initialise with +∞ (include_self=False) or self values (include_self=True).
'''

def scatter_amin(src, index, include_self=True, self_val=None):

    out_size = len(np.unique(index))

    if self_val is None:
        self_val = np.zeros(out_size)
    if include_self:
        out = self_val.copy()
    else:
        out = np.full(out_size, np.inf)
    np.minimum.at(out, index, src)
    return out

out_amin = scatter_amin(src, index, include_self=False)
print(f"scatter_amin (include_self=False): {out_amin}")
# out[0]=min(2,5)=2, out[1]=min(4)=4, out[2]=min(1,3,6)=1  →  [2. 4. 1.]

out_amin_self = scatter_amin(src, index, include_self=True,
                             self_val=np.array([0., 10., 5.]))
print(f"scatter_amin (self=[0,10,5]): {out_amin_self}")
# out[0]=min(0,2,5)=0, out[1]=min(10,4)=4, out[2]=min(5,1,3,6)=1 → [0. 4. 1.]


# ── 2-D scatter  (torch dim=1)  ───────────────────────────────────────────────
print("\n--- 2-D scatter (dim=1) ---")
'''
torch (dim=1):
  For each i,j: out[i][index[i][j]] <reduce>= src[i][j]

In NumPy each ROW is processed independently.  For a 2-D index tensor of
shape (N, L) and src of shape (N, L), the row subscript `rows` is just
np.arange(N) broadcast across the column dimension.

  rows = np.arange(N)[:, None]          # (N, 1)  — broadcast over cols
  np.add.at(out, (rows, index), src)    # tuple index: (row, col)
'''

N, L, M_out = 3, 4, 5
src_2d   = np.array([[1., 2., 3., 4.],
                     [5., 6., 7., 8.],
                     [9., 10., 11., 12.]])    # (3, 4)
index_2d = np.array([[0, 2, 0, 4],
                     [1, 3, 1, 2],
                     [4, 0, 3, 2]])            # (3, 4)  — col indices into out

# Scatter sum along dim=1
out_2d = np.zeros((N, M_out))
rows = np.arange(N)[:, None]                  # (3, 1)
np.add.at(out_2d, (rows, index_2d), src_2d)
print("2-D scatter_sum (dim=1):")
print(out_2d)
# [[ 4.  0.  2.  0.  4.]
#  [ 0. 12.  8.  6.  0.]
#  [10.  0. 12. 11.  9.]]
# Row 0: out[0,0]=1+3=4, out[0,2]=2, out[0,4]=4  → [4 0 2 0 4]
# Row 1: out[1,1]=5+7=12, out[1,3]=6, out[1,2]=8  → [0 12 8 6 0]
# Row 2: out[2,4]=9, out[2,0]=10, out[2,3]=11, out[2,2]=12 → [10 0 12 11 9]

# Verify row 0 manually
assert out_2d[0, 0] == 1 + 3  # index_2d[0]=[0,2,0,4]: cols 0 appears twice (src 1,3)
assert out_2d[0, 2] == 2      # col 2 once
assert out_2d[0, 4] == 4      # col 4 once
print("2-D scatter assertions passed.")

# 2-D scatter amax (dim=1)
out_2d_max = np.full((N, M_out), -np.inf)
np.maximum.at(out_2d_max, (rows, index_2d), src_2d)
print("2-D scatter_amax (dim=1):")
print(out_2d_max)

#--------------------------------------------------
# ── Gather - fancy indexing  (torch.gather)  ───────────────────────────────────────────────────
#--------------------------------------------------

print("\n--- Gather - fancy indexing (torch.gather equivalent) ---")
'''
torch.gather(input, dim, index)
  Reads from input at positions specified by index.
  out[i][j][k] = input[i][index[i][j][k]][k]   for dim=1

1-D gather (dim=0):
  out[i] = input[index[i]]
  numpy: out = input[index]

2-D gather along dim=0:
  out[i,j] = input[index[i,j], j]
  numpy: out = input[index, np.arange(ncols)]  (with broadcasting)

2-D gather along dim=1:
  out[i,j] = input[i, index[i,j]]
  numpy: out = input[np.arange(nrows)[:,None], index]
'''

input_1d = np.array([10., 20., 30., 40., 50.])
idx_1d   = np.array([4, 0, 2, 2, 1])
gathered_1d = input_1d[idx_1d]
print("1-D gather:", gathered_1d)   # [50. 10. 30. 30. 20.]

input_2d = np.array([[1.,  2.,  3.,  4.],
                     [5.,  6.,  7.,  8.],
                     [9., 10., 11., 12.]])
idx_dim1 = np.array([[3, 0, 1],
                     [2, 2, 0],
                     [1, 3, 2]])   # (3, 3) — col indices (dim=1)

# Gather dim=1: for each row i, pick columns specified by idx_dim1[i]
gathered_dim1 = input_2d[np.arange(3)[:, None], idx_dim1]
print("2-D gather dim=1:")
print(gathered_dim1)
# Row 0: input[0, [3,0,1]] = [4,1,2]
# Row 1: input[1, [2,2,0]] = [7,7,5]
# Row 2: input[2, [1,3,2]] = [10,12,11]

# Gather dim=0: for each col j, pick rows specified by idx_dim0[i,j]
idx_dim0 = np.array([[2, 0],
                     [1, 2],
                     [0, 1]])   # (3, 2) — row indices (dim=0)
gathered_dim0 = input_2d[idx_dim0, np.arange(2)]   # broadcast col index
# idx_dim0[i,j] selects the row; arange(2) is the column
print("2-D gather dim=0:")
print(gathered_dim0)
# [input[2,0]=9,  input[0,1]=2]
# [input[1,0]=5,  input[2,1]=10]
# [input[0,0]=1,  input[1,1]=6]


# ── Advanced scatter patterns  ────────────────────────────────────────────────
print("\n--- Advanced: conditional scatter ---")
'''
Only scatter values where a condition on src is True.
Equivalent to: out.scatter_reduce_(0, index[mask], src[mask], reduce='sum')
'''
mask = src > 3.0
filtered_idx = index[mask]    # [1, 0, 2]  (src=4, 5, 6)
filtered_src = src[mask]      # [4., 5., 6.]
out_cond = np.zeros(K)
np.add.at(out_cond, filtered_idx, filtered_src)
print(f"Conditional scatter (src>3): {out_cond}")   # [5. 4. 6.]

print("\n--- Advanced: batched scatter (loop over batch dim) ---")
'''
For batch size B with (different) index/src per item, loop over batch.
Vectorised batch scatter is possible via .at() with (batch_idx, scatter_idx).
'''
B = 4
src_batch   = np.arange(B * 3, dtype=float).reshape(B, 3)  # (4, 3)
index_batch = np.array([[0, 1, 0],
                        [2, 0, 1],
                        [1, 1, 2],
                        [0, 2, 2]])                           # (4, 3)
out_batch = np.zeros((B, 3))
batch_rows = np.arange(B)[:, None]   # (4, 1)
np.add.at(out_batch, (batch_rows, index_batch), src_batch)
print("Batched scatter_sum:")
print(out_batch)
# [[ 2.  1.  0.]
#  [ 4.  5.  3.]
#  [ 0. 13.  8.]
#  [ 9.  0. 21.]]

print("\n--- Advanced: scatter with unary ufunc (in-place negation at indices) ---")
'''
np.negative.at(a, indices)  — negate selected elements in-place.
np.absolute.at(a, indices)  — absolute value of selected elements.
np.reciprocal.at(a, indices)— invert selected elements.
'''
a_inplace = np.array([1., -2., 3., -4., 5.])
np.negative.at(a_inplace, [0, 2, 4])   # negate elements at indices 0,2,4
print(f"negative.at [0,2,4]: {a_inplace}")   # [-1.  -2.  -3.  -4.  -5.]

a_abs = np.array([1., -2., 3., -4., 5.])
np.absolute.at(a_abs, [1, 3])
print(f"absolute.at [1,3]  : {a_abs}")   # [1. 2. 3. 4. 5.]

# np.power.at: square specific elements
a_pow = np.array([1., 2., 3., 4., 5.])
np.power.at(a_pow, [1, 3], 2)   # square elements at index 1 and 3
print(f"power.at [1,3] **2 : {a_pow}")   # [1.  4.  3. 16.  5.]


#-------------------------------------------------------------------------------------------------#
#════════════════════════════════  PART H — MATH UFUNCS  ═════════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

print("\n=== Math ufuncs ===")

#############################################################
## add / subtract / multiply / divide / floor_divide / mod ##
#############################################################
'''
np.add(x1, x2)           : x1 + x2   (triggered by a + b when a or b is ndarray)
np.subtract(x1, x2)      : x1 - x2
np.multiply(x1, x2)      : x1 * x2
np.divide(x1, x2)        : x1 / x2   (true division, always float)
np.true_divide(x1, x2)   : same as divide
np.floor_divide(x1, x2)  : x1 // x2  (round toward -inf)
np.remainder(x1, x2)     : x1 % x2   (same sign as divisor)
np.mod(x1, x2)           : alias for remainder
np.fmod(x1, x2)          : C-style fmod (same sign as DIVIDEND, not divisor)
np.divmod(x1, x2)        : (floor_divide, remainder) simultaneously

Key differences: remainder vs fmod for negative numbers.
'''
x = np.array([-7., -3., 3., 7.])
d = np.array([ 3.,  2., 2., 3.])
print("remainder (% like Python):", np.remainder(x, d))   # [ 2.  1.  1.  1.]
print("fmod      (% like C)     :", np.fmod(x, d))        # [-1. -1.  1.  1.]
# remainder: result has sign of divisor; fmod: sign of dividend

q, r = np.divmod(x, d)
print("divmod quotient:", q, "  remainder:", r)
# divmod quotient: [-3. -2.  1.  2.]   remainder: [2. 1. 1. 1.]

#########################################################
## negative / positive / absolute / fabs / sign / rint ##
#########################################################
'''
np.negative(x)   : -x   (triggered by -a)
np.positive(x)   : +x   (explicit unary +)
np.absolute(x)   : |x|  (works on complex: |a+ib| = sqrt(a²+b²))
np.fabs(x)       : |x|  float-only, slightly faster for non-complex
np.sign(x)       : -1 / 0 / +1 for negative / zero / positive
np.rint(x)       : round to nearest integer (banker's rounding: ties → even)
'''
z = np.array([-2.7, -0.5, 0.0, 0.5, 2.5, 3.0])
print("sign :", np.sign(z))    # [-1. -1.  0.  1.  1.  1.]
print("rint :", np.rint(z))    # [-3. -0.  0.  0.  2.  3.]  (ties→even: -0.5→0, 0.5→0, 2.5→2)

z_cplx = np.array([3. + 4.j, -1. + 0.j])
print("absolute (complex):", np.absolute(z_cplx))   # [5. 1.]

#############################################################
## power / float_power / square / sqrt / cbrt / reciprocal ##
#############################################################
'''
np.power(x1, x2)       : x1 ** x2  (integer powers stay integer if inputs are int)
np.float_power(x1, x2) : x1 ** x2  (always float64 — avoids int overflow; handles
                           negative bases with non-integer exponents → returns nan)
np.square(x)           : x**2  (faster than power(x, 2))
np.sqrt(x)             : √x   (nan for negative reals; use np.emath.sqrt for complex)
np.cbrt(x)             : ∛x   (real cube root; handles negatives: cbrt(-8)=-2)
np.reciprocal(x)       : 1/x  (integer input: rounds toward zero; use float input)
'''
p = np.array([2., 3., 4., -8.])
print("square  :", np.square(p))          # [ 4.  9. 16. 64.]
print("sqrt    :", np.sqrt(np.abs(p)))    # [ 1.414  1.732  2.  2.828]
print("cbrt    :", np.cbrt(p))            # [ 1.26   1.44   1.587  -2.  ]
print("power   :", np.power(2., np.array([0., 1., 2., 3., 10.]))) # [1. 2. 4. 8. 1024.]
print("float_power(-1, 0.5):", np.float_power(-1, 0.5))   # nan (real domain)
print("reciprocal:", np.reciprocal(p))   # [0.5   0.333  0.25  -0.125]

#####################################################
## exp / exp2 / expm1 / log / log2 / log10 / log1p ##
#####################################################
'''
np.exp(x)    : eˣ
np.exp2(x)   : 2ˣ
np.expm1(x)  : eˣ - 1  (accurate near x=0; avoids catastrophic cancellation)
np.log(x)    : natural log ln(x)
np.log2(x)   : log₂(x)
np.log10(x)  : log₁₀(x)
np.log1p(x)  : log(1+x)  (accurate near x=0)

Precision tip: for small x, expm1(x) ≫ exp(x)-1  and  log1p(x) ≫ log(1+x).
'''
tiny = np.array([1e-15, 1e-10, 1e-5])
print("exp(tiny)-1  :", np.exp(tiny) - 1)   # precision lost for 1e-15
print("expm1(tiny)  :", np.expm1(tiny))     # accurate for all
print("log1p(tiny)  :", np.log1p(tiny))     # accurate for all
print("log(1+tiny)  :", np.log(1 + tiny))   # precision lost for 1e-15

x_exp = np.array([1., 2., 4., 8., 1024.])
print("log2 :", np.log2(x_exp))    # [0. 1. 2. 3. 10.]
print("log10:", np.log10(np.array([1., 10., 100., 1000.])))   # [0. 1. 2. 3.]

############################
## logaddexp / logaddexp2 ##
############################
'''
np.logaddexp(x1, x2)  : log(eˣ¹ + eˣ²) computed stably.
                         = x1 + log(1 + exp(x2-x1))  (stable if x1 ≥ x2)
np.logaddexp2(x1, x2) : log₂(2ˣ¹ + 2ˣ²)

Use for numerically stable log-sum-exp in probability:
  log(p1 + p2) = logaddexp(log_p1, log_p2)

Also available as a reduce for the full log-sum-exp:
  np.logaddexp.reduce(log_probs)
'''
lp1 = np.log(0.3)
lp2 = np.log(0.7)
print("logaddexp:", np.logaddexp(lp1, lp2))          # log(1.0) = 0.0
print("naive    :", np.log(np.exp(lp1) + np.exp(lp2)))  # same (no overflow here)

# logaddexp.reduce = log-sum-exp
log_probs = np.array([-1000., -999., -998.])   # would underflow with exp()
lse = np.logaddexp.reduce(log_probs)
print(f"log-sum-exp {log_probs}: {lse:.4f}")   # -997.5917... (correct)

###########################
## heaviside / gcd / lcm ##
###########################
'''
np.heaviside(x1, x2)  : 0 if x1<0, x2 if x1=0, 1 if x1>0.
                         x2 is the value at exactly zero (commonly 0.0 or 0.5).
np.gcd(x1, x2)        : greatest common divisor of |x1| and |x2|.
np.lcm(x1, x2)        : lowest common multiple of |x1| and |x2|.
'''
h_input = np.array([-2., -1., 0., 1., 2.])
print("heaviside(x, 0.5):", np.heaviside(h_input, 0.5))   # [0. 0. 0.5 1. 1.]
print("heaviside(x, 1.0):", np.heaviside(h_input, 1.0))   # [0. 0. 1.  1. 1.]

a_int = np.array([12, 15, 24, 0])
b_int = np.array([ 8, 25, 36, 5])
print("gcd:", np.gcd(a_int, b_int))   # [4 5 12 5]
print("lcm:", np.lcm(a_int, b_int))   # [24 75 72  0]


#-------------------------------------------------------------------------------------------------#
#══════════════════════════════  PART I — TRIGONOMETRIC UFUNCS  ══════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

print("\n=== Trigonometric ufuncs ===")

##################################################################
## sin / cos / tan / arcsin / arccos / arctan / arctan2 / hypot ##
##################################################################
'''
np.sin / np.cos / np.tan       : standard trig (input in RADIANS)
np.arcsin / np.arccos / np.arctan : inverse trig (output in RADIANS)
np.arctan2(y, x)               : 4-quadrant arctangent; range (-π, π].
                                  More numerically stable than arctan(y/x).
np.hypot(x1, x2)               : sqrt(x1²+x2²); avoids overflow for large inputs.

Identities verified:
  sin²(x) + cos²(x) == 1
  arctan2(sin(x), cos(x)) == x  (mod 2π)
  hypot(x1, x2) == ||(x1, x2)||₂
'''
theta = np.linspace(0, 2*np.pi, 7)
s, c = np.sin(theta), np.cos(theta)
print("sin² + cos² = 1:", np.allclose(s**2 + c**2, 1.0))   # True
print("arctan2 recovery :", np.allclose(np.arctan2(s, c), theta - 2*np.pi*(theta > np.pi)))

# arctan2 quadrant awareness
angles = np.arctan2(np.array([ 1.,  1., -1., -1.]),   # y
                    np.array([ 1., -1.,  1., -1.]))    # x
print("arctan2 quadrants:", np.degrees(angles))   # [45. 135. -45. -135.]

print("hypot(3,4):", np.hypot(3., 4.))   # 5.0 (Pythagorean triple)

######################################################
## sinh / cosh / tanh / arcsinh / arccosh / arctanh ##
######################################################
'''
Hyperbolic functions. Identities:
  cosh²(x) - sinh²(x) == 1
  tanh(x) = sinh(x)/cosh(x)
  arctanh is the logit-like function: arctanh(x) = 0.5*log((1+x)/(1-x))
'''
x_h = np.array([0., 0.5, 1., 2.])
print("cosh²-sinh²=1:", np.allclose(np.cosh(x_h)**2 - np.sinh(x_h)**2, 1.0))   # True
print("tanh(1):", np.tanh(1.))   # 0.7616...

###########################################
## deg2rad / rad2deg / degrees / radians ##
###########################################
'''
np.deg2rad(x)  : degrees → radians  (== x * π/180)
np.rad2deg(x)  : radians → degrees  (== x * 180/π)
np.degrees(x)  : alias for rad2deg
np.radians(x)  : alias for deg2rad
'''
deg = np.array([0., 30., 45., 60., 90., 180., 360.])
rad = np.deg2rad(deg)
print("deg→rad:", rad.round(4)) # [0.     0.5236 0.7854 1.0472 1.5708 3.1416 6.2832]
print("rad→deg:", np.rad2deg(rad))   # back to original
print("sin(30°):", np.sin(np.deg2rad(30.)))   # 0.5


#-------------------------------------------------------------------------------------------------#
#════════════════════════════  PART J — BIT-TWIDDLING UFUNCS  ════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

print("\n=== Bit-twiddling ufuncs ===")

##########################################################
## bitwise_and / bitwise_or / bitwise_xor / bitwise_not ##
##########################################################
'''
np.bitwise_and(x1, x2)  : x1 & x2   — AND each bit pair
np.bitwise_or(x1, x2)   : x1 | x2   — OR each bit pair
np.bitwise_xor(x1, x2)  : x1 ^ x2   — XOR each bit pair
np.bitwise_not(x)        : ~x        — flip all bits (== invert)
np.invert(x)             : alias for bitwise_not

All operate on integer (or boolean) arrays.
For boolean arrays: same as logical_and, logical_or, etc. but element-wise.
For unsigned integers they are the standard bitwise operations.
'''
a_b = np.array([0b1010, 0b1100, 0b0110], dtype=np.uint8)
b_b = np.array([0b0110, 0b1010, 0b1100], dtype=np.uint8)

print("AND:", np.bitwise_and(a_b, b_b), '=', [bin(x) for x in np.bitwise_and(a_b, b_b)])
print("OR :", np.bitwise_or(a_b, b_b),  '=', [bin(x) for x in np.bitwise_or(a_b, b_b)])
print("XOR:", np.bitwise_xor(a_b, b_b), '=', [bin(x) for x in np.bitwise_xor(a_b, b_b)])
print("NOT:", np.bitwise_not(a_b),       '=', [bin(x) for x in np.bitwise_not(a_b)])
# AND: [2 8 4] = ['0b10', '0b1000', '0b100']
# OR : [14 14 14] = ['0b1110', '0b1110', '0b1110']
# XOR: [12  6 10] = ['0b1100', '0b110', '0b1010']
# NOT: [245 243 249] = ['0b11110101', '0b11110011', '0b11111001']

# Boolean bitwise
p = np.array([True, True, False, False])
q = np.array([True, False, True, False])
print("bool AND:", np.bitwise_and(p, q))   # [T F F F]
print("bool OR :", np.bitwise_or(p, q))    # [T T T F]
print("bool XOR:", np.bitwise_xor(p, q))   # [F T T F]

# Practical: mask flag bits
FLAGS = np.array([0b1011, 0b0101, 0b1110], dtype=np.uint8)
READ_BIT  = np.uint8(0b0001)
WRITE_BIT = np.uint8(0b0010)
print("Has READ  flag:", np.bitwise_and(FLAGS, READ_BIT).astype(bool)) # [ True  True False]
print("Has WRITE flag:", np.bitwise_and(FLAGS, WRITE_BIT).astype(bool)) # [ True False  True]

# reduce and accumulate work on bitwise ops too
print("bitwise_or.reduce  :", np.bitwise_or.reduce(FLAGS))  # 15, all flags OR'd
print("bitwise_and.reduce :", np.bitwise_and.reduce(FLAGS)) # 0, only flags set in ALL

##############################
## left_shift / right_shift ##
##############################
'''
np.bitwise_left_shift(x1, x2)  : x1 << x2  — multiply by 2^x2
np.left_shift(x1, x2)          : alias
np.bitwise_right_shift(x1, x2) : x1 >> x2  — floor-divide by 2^x2
np.right_shift(x1, x2)         : alias

x2 must be non-negative; behaviour on shift ≥ bit-width is undefined (like C).
Left shift by 1 == multiply by 2; right shift by 1 == floor-divide by 2.
'''
x_bits = np.array([1, 2, 4, 8, 16, 256], dtype=np.int32)
print("left_shift  by 1:", np.left_shift(x_bits, 1))    # [2 4 8 16 32 512]
print("right_shift by 1:", np.right_shift(x_bits, 1))   # [0 1 2  4  8 128]

# Fast integer log2 for powers of 2
pow2 = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint32)
log2_pow2 = np.zeros(len(pow2), dtype=np.uint32)
for k in range(8):
    log2_pow2 += np.right_shift(pow2, k + 1).astype(bool).astype(np.uint32)
print("Fast log2(2^k):", log2_pow2)   # [0 1 2 3 4 5 6 7]


#-------------------------------------------------------------------------------------------------#
#══════════════════════════════  PART K — COMPARISON UFUNCS  ═════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

print("\n=== Comparison ufuncs ===")

#####################################################################
## greater / greater_equal / less / less_equal / equal / not_equal ##
#####################################################################
'''
np.greater(x1, x2)       : x1 > x2   (triggered by a > b)
np.greater_equal(x1, x2) : x1 >= x2
np.less(x1, x2)          : x1 < x2
np.less_equal(x1, x2)    : x1 <= x2
np.equal(x1, x2)         : x1 == x2
np.not_equal(x1, x2)     : x1 != x2

These return boolean arrays.  They are the kernel of boolean indexing.
Unlike Python operators, they broadcast and can be used with out/where.
Also available as ufuncs: np.equal.reduce() == np.all(a == b)
'''
x = np.array([1., 2., 3., 4., 5.])
y = np.array([3., 2., 3., 2., 1.])
print("x > y :", np.greater(x, y))        # [F F F T T]
print("x == y:", np.equal(x, y))           # [F T T F F]
print("x != y:", np.not_equal(x, y))       # [T F F T T]

# With out= to avoid allocation (useful in loops)
result_bool = np.empty(5, dtype=bool)
np.greater(x, 3.0, out=result_bool)
print("x > 3 (out=):", result_bool)   # [F F F T T]

# equal: all elements equal (manual np.all equivalent)
same = np.array([5, 5, 5, 5])
is_all_fives = np.all(np.equal(same, same[0]))
print("Are all elements equal? (using np.equal + np.all):", is_all_fives)  # True

##########################################################
## logical_and / logical_or / logical_xor / logical_not ##
##########################################################
'''
np.logical_and(x1, x2)  : bool(x1) AND bool(x2)   — element-wise
np.logical_or(x1, x2)   : bool(x1) OR  bool(x2)
np.logical_xor(x1, x2)  : bool(x1) XOR bool(x2)
np.logical_not(x)        : NOT bool(x)

vs bitwise: logical ops treat ANY nonzero as True, always return bool.
            bitwise ops operate on individual bits of integers.

np.logical_and.reduce(x) == np.all(x)
np.logical_or.reduce(x)  == np.any(x)
'''
x_l = np.array([0, 1, 0, 1])
y_l = np.array([0, 0, 1, 1])
print("logical_and:", np.logical_and(x_l, y_l))   # [F F F T]
print("logical_or :", np.logical_or(x_l, y_l))    # [F T T T]
print("logical_xor:", np.logical_xor(x_l, y_l))   # [F T T F]
print("logical_not:", np.logical_not(x_l))         # [T F T F]

# Works on floats: 0.0 → False, nonzero → True
print("logical_and(1.5, 0.0):", np.logical_and(1.5, 0.0))   # False

#####################################
## maximum / minimum / fmax / fmin ##
#####################################
'''
np.maximum(x1, x2) : element-wise max — PROPAGATES NaN.
np.minimum(x1, x2) : element-wise min — PROPAGATES NaN.
np.fmax(x1, x2)    : element-wise max — IGNORES NaN (returns the other value).
np.fmin(x1, x2)    : element-wise min — IGNORES NaN.

Key difference:
  maximum(3.0, nan) = nan    fmax(3.0, nan) = 3.0
  minimum(3.0, nan) = nan    fmin(3.0, nan) = 3.0

maximum.reduce(x) == np.max(x)   (propagates NaN)
fmax.reduce(x)    == np.nanmax(x) (ignores NaN)
'''
x_m = np.array([1., np.nan, 3., 4.])
y_m = np.array([4., 2., np.nan, 1.])
print("maximum:", np.maximum(x_m, y_m))   # [4. nan nan 4.]
print("fmax   :", np.fmax(x_m, y_m))      # [4. 2.  3.  4.]
print("minimum:", np.minimum(x_m, y_m))   # [1. nan nan 1.]
print("fmin   :", np.fmin(x_m, y_m))      # [1. 2.  3.  1.]

# Running maximum (all-time high): use maximum.accumulate
prices = np.array([3., 1., 4., 1., 5., 9., 2., 6.])
ath = np.maximum.accumulate(prices)
print("All-time high:", ath)   # [3. 3. 4. 4. 5. 9. 9. 9.]

# Clip using maximum + minimum
x_clip = np.array([-3., 0., 5., 12., -1.])
clipped = np.minimum(np.maximum(x_clip, 0.0), 10.0)   # clip to [0, 10]
print("Clipped [0,10]:", clipped)   # [0. 0. 5. 10. 0.]


#-------------------------------------------------------------------------------------------------#
#════════════════════════════  PART L — FLOATING-POINT UFUNCS  ═══════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

print("\n=== Floating-point ufuncs ===")

################################################
## isfinite / isinf / isnan / isnat / signbit ##
################################################
'''
np.isfinite(x) : True where x is finite (not ±inf, not NaN)
np.isinf(x)    : True where x is ±inf
np.isnan(x)    : True where x is NaN
np.isnat(x)    : True where x is NaT (Not a Time) — for datetime64/timedelta64
np.signbit(x)  : True where x has its sign bit set (negative, including -0.0)

These return boolean arrays and support broadcasting / where.
'''
vals = np.array([1., np.inf, -np.inf, np.nan, 0., -0.])
print("isfinite:", np.isfinite(vals))   # [T F F F T T]
print("isinf   :", np.isinf(vals))      # [F T T F F F]
print("isnan   :", np.isnan(vals))      # [F F F T F F]
print("signbit :", np.signbit(vals))    # [F F T F F T]  (-0 has sign bit set)

# Filter NaN using where= to avoid computing on NaN
log_safe = np.full(len(vals), np.nan)
np.log(vals, out=log_safe, where=np.isfinite(vals) & (vals > 0))
print("log (safe):", log_safe)   # [0. nan nan nan nan nan]

# datetime NaT
dt = np.array(['2024-01', 'NaT', '2024-03'], dtype='datetime64[M]')
print("isnat datetime:", np.isnat(dt))   # [F T F]

####################################
## copysign / nextafter / spacing ##
####################################
'''
np.copysign(x1, x2)  : magnitude of x1, sign of x2.
                        copysign(3., -1.) == -3.
np.nextafter(x1, x2) : next representable float from x1 toward x2.
                        nextafter(0., 1.) == 5e-324 (smallest positive float64)
np.spacing(x)         : spacing(x) == nextafter(x, inf) - x == ULP (unit in last place).
                        Machine epsilon ε_mach = spacing(1.0).
'''
print("copysign(3., -1.) :", np.copysign(3., -1.))    # -3.
print("copysign(-5., 2.) :", np.copysign(-5., 2.))    # 5.
print("nextafter(0, 1)   :", np.nextafter(0., 1.))    # 5e-324
print("nextafter(1, inf) :", np.nextafter(1., np.inf))# 1+epsilon ≈ 1.0000000000000002
print("spacing(1.0)      :", np.spacing(1.0))          # 2.22e-16 = machine epsilon
print("np.finfo vs spacing:", np.isclose(np.spacing(1.0), np.finfo(float).eps))  # True

##########################
## modf / ldexp / frexp ##
##########################
'''
np.modf(x)       : (fractional part, integer part) both with sign of x.
                   Returns two arrays. Like math.modf but vectorised.

np.frexp(x)      : (mantissa, exponent) such that x = mantissa * 2^exponent.
                   mantissa ∈ [0.5, 1) or 0. Vectorised math.frexp.

np.ldexp(x1, x2) : x1 * 2^x2  — the inverse of frexp.
                   x1 = mantissa, x2 = exponent (must be int).
'''
x_fp = np.array([-3.75, 0.0, 1.5, 7.25])
frac, intg = np.modf(x_fp)
print("modf fractional:", frac)   # [-0.75  0.    0.5   0.25]
print("modf integral  :", intg)   # [-3.    0.    1.    7.  ]

mant, exp = np.frexp(x_fp)
print("frexp mantissa :", mant)   # [-0.9375  0.   0.75  0.90625]
print("frexp exponent :", exp)    # [ 2       0    1     3      ]
reconstructed = np.ldexp(mant, exp)
print("ldexp round-trip:", np.allclose(reconstructed, x_fp))   # True

############
## matmul ##
############
'''
np.matmul(x1, x2)  : matrix product  (gufunc, signature (n?,k),(k,m?)->(n?,m?))

  Triggered by the @ operator.  Behaviour depends on dimensionality:
  1-D @ 1-D  : inner (dot) product → scalar
  2-D @ 2-D  : matrix multiplication
  N-D @ N-D  : batch matrix multiplication (leading dims broadcast)
  1-D @ 2-D  : treat 1-D as row vector; result has 1 removed
  2-D @ 1-D  : treat 1-D as column vector; result has 1 removed

  Differences from np.dot:
    np.dot: works on any dimension pair; scalars scale everything.
    matmul: does NOT allow scalar arguments; cleaner broadcasting for batches.
'''
print("\n=== matmul (gufunc) ===")
u_v = np.array([1., 2., 3.])
v_v = np.array([4., 5., 6.])
print("1-D @ 1-D (dot product):", np.matmul(u_v, v_v))   # 32.

M22 = np.array([[1., 2.], [3., 4.]])
M22b= np.array([[5., 6.], [7., 8.]])
print("2-D @ 2-D:\n", np.matmul(M22, M22b))
# [[19. 22.], [43. 50.]]

# Batch: (B, m, k) @ (B, k, n) → (B, m, n)
batch_A = np.stack([M22, M22 * 2.])   # (2, 2, 2)
batch_B = np.stack([M22b, M22b * 0.5])
batch_C = np.matmul(batch_A, batch_B)   # (2, 2, 2)
print("batch matmul shape:", batch_C.shape)
print(np.allclose(batch_C[0], M22 @ M22b))   # True
print(np.allclose(batch_C[1], (M22*2.) @ (M22b*0.5)))  # True


#-------------------------------------------------------------------------------------------------#
#════════════════════════════  PART M — CREATING CUSTOM UFUNCS  ══════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

print("\n=== Custom ufuncs ===")

###################
## np.frompyfunc ##
###################
'''
np.frompyfunc(func, nin, nout, *, identity=None)
  Wrap any Python callable as a true ufunc.

  func     : Python callable taking nin scalar arguments, returning nout scalars.
  nin      : number of input arrays.
  nout     : number of output arrays.
  identity : identity element for .reduce() (None means reduce needs initial=).

  The resulting ufunc:
    • Supports broadcasting.
    • Supports out / where / casting keyword arguments.
    • Supports ALL five ufunc methods: reduce, accumulate, reduceat, outer, at.
    • Has .ntypes == 1 (only object dtype by default — Python scalars).
    • Is slower than C-level ufuncs because it calls Python for each element.

  ALWAYS returns object dtype.  Cast explicitly if you need float/int.
  For float output use .astype(float) or wrap with np.vectorize (see below).
'''

# Scalar add as ufunc
def _custom_add(a, b):
    # Just a silly custom binary operation: a + (b / 2)
    return a + (b / 2.0)

# Create the binary ufunc (nin=2, nout=1)
custom_op_uf = np.frompyfunc(_custom_add, nin=2, nout=1)

x_bin = np.array([10., 4., 2.])

# Evaluate element-wise (requires two arrays or broadcasting)
# Here we add x_bin to a scalar 2.0
print("custom_op(x, 2):", custom_op_uf(x_bin, 2.0))
# [11.0 5.0 3.0]

# Now .reduce() works perfectly!
# It does: _custom_add(_custom_add(10, 4), 2)
# Step 1: 10 + (4/2) = 12
# Step 2: 12 + (2/2) = 13
print("custom_op.reduce:", float(custom_op_uf.reduce(x_bin)))
# 13.0

# Binary ufunc: clamp(x, lo, hi) = max(lo, min(hi, x))
def _clamp(x, lo, hi):
    return max(lo, min(hi, x))
clamp_uf = np.frompyfunc(_clamp, nin=3, nout=1)
x_cl = np.array([-3., 0., 2., 5., 8.])
clamped = clamp_uf(x_cl, 0., 6.).astype(float)
print("clamp [0,6]:", clamped)   # [0. 0. 2. 5. 6.]

# .outer works on frompyfunc ufuncs
def _power_mod(base, exp):
    return int(base) ** int(exp) % 7
pm_uf = np.frompyfunc(_power_mod, nin=2, nout=1)
table = pm_uf.outer(np.arange(1, 5), np.arange(0, 4)).astype(int)
print("power_mod outer (mod 7):\n", table)
#  [[1 1 1 1]
#  [1 2 4 1]
#  [1 3 2 6]
#  [1 4 2 1]]

# Two-output ufunc
def _divmod_py(a, b):
    return divmod(a, b)   # (quotient, remainder)
divmod_uf = np.frompyfunc(lambda a, b: int(a) // int(b), nin=2, nout=1)
# True two-output: wrap properly
def _div(a, b):  return a // b
def _rem(a, b):  return a % b
divmod2 = np.frompyfunc(lambda a, b: (int(a)//int(b), int(a)%int(b)), 2, 2)
q_out, r_out = divmod2(np.array([10, 11, 12]), np.array([3, 3, 3]))
print("frompyfunc 2-out divmod:", q_out.astype(int), r_out.astype(int))
# [3 3 4] [1 2 0]

##################
## np.vectorize ##
##################
'''
np.vectorize(pyfunc, otypes=None, doc=None, excluded=None,
             cache=False, signature=None)
  Vectorize a Python function over array inputs.

  NOT a true ufunc (no .reduce / .accumulate / .at / .outer methods).
  Primary purpose: convenience wrapper for broadcasting, not performance.
  Slower than a true ufunc; use it for rapid prototyping.

  otypes  : output dtype as a list, e.g. [float] or ['f8', 'i4'].
            If not given, inferred by calling func once on the first element.
  excluded: set of argument names / indices to NOT vectorize over (treated
            as scalars even if arrays are passed).
  signature: generalised ufunc-style signature for non-scalar core elements.
             e.g. '(n)->(n)' for a function that maps 1-D arrays to 1-D arrays.
  cache   : cache the dtype inference call result.

  Key difference from frompyfunc:
    frompyfunc → true ufunc, object dtype, all methods.
    vectorize  → not a ufunc, respects otypes, cleaner API, no ufunc methods.
'''

# Basic usage: vectorize a function with a branch
def grade(score):
    if   score >= 90: return 'A'
    elif score >= 75: return 'B'
    elif score >= 60: return 'C'
    else:             return 'F'

grade_v = np.vectorize(grade, otypes=[str])
scores = np.array([95, 82, 67, 55, 73, 91])
print("grades:", grade_v(scores))   # ['A' 'B' 'C' 'F' 'C' 'A']

# otypes: avoid dtype inference overhead
def logistic_map(x, r):
    return r * x * (1 - x)

logmap_v = np.vectorize(logistic_map, otypes=[float])
x0 = np.array([0.1, 0.2, 0.3, 0.4])
r  = 3.9
print("logistic map:", logmap_v(x0, r).round(4)) # [0.351 0.624 0.819 0.936]

# excluded: r is a scalar parameter, not vectorised
logmap_excl = np.vectorize(logistic_map, otypes=[float], excluded=['r'])
print("excluded r  :", logmap_excl(x0, r=3.9).round(4))   # same result

# signature: function on 1-D arrays (like a gufunc)
def running_max_1d(arr):
    return np.maximum.accumulate(arr)

rmax_v = np.vectorize(running_max_1d, signature='(n)->(n)')
mat = np.array([[3, 1, 4, 1, 5],
                [9, 2, 6, 5, 3]])
print("running_max per row (signature):\n", rmax_v(mat))
# [[3 3 4 4 5]
#  [9 9 9 9 9]]


# ── Performance comparison ────────────────────────────────────────────────────
print("\n=== Performance summary ===")
import time

N = 200_000
x_perf = rng.standard_normal(N)

# C-level ufunc
t0 = time.perf_counter()
for _ in range(10): _ = np.sin(x_perf)
t_c = (time.perf_counter() - t0) / 10

# frompyfunc
import math
sin_py = np.frompyfunc(math.sin, 1, 1)
t0 = time.perf_counter()
for _ in range(3): _ = sin_py(x_perf)
t_py = (time.perf_counter() - t0) / 3

# vectorize
sin_v = np.vectorize(math.sin, otypes=[float])
t0 = time.perf_counter()
for _ in range(3): _ = sin_v(x_perf)
t_v = (time.perf_counter() - t0) / 3

print(f"np.sin   (C ufunc)  : {t_c*1000:.2f} ms") # 3.78 ms
print(f"frompyfunc(sin)     : {t_py*1000:.2f} ms  ({t_py/t_c:.0f}x slower)") # 20.54 ms  (5x slower)
print(f"vectorize(sin)      : {t_v*1000:.2f} ms  ({t_v/t_c:.0f}x slower)") # 32.12 ms  (9x slower)
# C ufunc is typically 50-200x faster than Python-wrapped versions.
# frompyfunc ≈ vectorize in speed; prefer vectorize for cleaner API,
# frompyfunc when you need the ufunc methods (reduce/accumulate/at/outer).
