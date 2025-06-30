'''
================================================================================
                              GENERALIZED INEQUALITIES
================================================================================

GENERALIZED INEQUALITIES

Definition:
A generalized inequality is a partial ordering on ℝⁿ defined by a proper cone K, 
where for vectors x, y ∈ ℝⁿ:

    x ≼_K y  if and only if  y - x ∈ K
                            (the result of "y minus x" is in a proper cone K)

This is read as "x is less than or equal to y with respect to K" [1][5].

The strict generalized inequality is defined as:

    x ≺_K y  if and only if  y - x ∈ interior(K)

where interior(K) denotes the interior of the proper cone K [5][7].

When the cone K is clear from context, the subscript is often omitted, writing 
simply x ≼ y and x ≺ y [7].

================================================================================

PROPER CONES

Definition and Properties:
A cone K ⊆ ℝⁿ is called a proper cone if it satisfies four essential properties:

1. K is convex
2. K is closed (has its boundary)
3. K is solid (has nonempty interior)
4. K is pointed (contains no line, i.e., x ∈ K and -x ∈ K implies x = 0)

These properties ensure that the generalized inequality behaves well and has 
many desirable characteristics of ordinary inequalities [9][10][11].

Examples of Proper Cones:

## Nonnegative Orthant:
K = ℝ₊ⁿ = {x ∈ ℝⁿ : xᵢ ≥ 0 for all i}

This cone generates componentwise inequalities, where x ≼ y means xᵢ ≤ yᵢ for 
all components i [5][7].

## Positive Semidefinite Cone:
K = S₊ⁿ = {X ∈ Sⁿ : X ≽ 0}

This cone generates matrix inequalities, where X ≼ Y means Y - X is positive 
semidefinite [5][24].

## Second-Order Cone:
K = {(x, t) ∈ ℝⁿ × ℝ : ||x||₂ ≤ t}

This cone is used in second-order cone programming [6].

================================================================================

PROPERTIES OF GENERALIZED INEQUALITIES

The generalized inequality ≼_K preserves many properties of ordinary inequalities:

Reflexivity: x ≼_K x for all x ∈ ℝⁿ [24]

Transitivity: If x ≼_K y and y ≼_K z, then x ≼_K z [11][24]

Antisymmetry: If x ≼_K y and y ≼_K x, then x = y [11][24]

Preservation under Addition:
If x ≼_K y and u ≼_K v, then x + u ≼_K y + v [5]

Preservation under Nonnegative Scaling:
If x ≼_K y and α ≥ 0, then αx ≼_K αy [5][24]

However, generalized inequalities differ from ordinary inequalities in that they 
define only a partial ordering - not every pair of vectors is comparable [5][7].

================================================================================

DUAL CONE AND CHARACTERIZATION

Dual Cone Definition:
For a proper cone K, its dual cone K* is defined as:

    K* = {y : x^T y ≥ 0 for all x ∈ K}

The dual cone K* is always convex and closed, even if the original cone K is not 
convex [15][18].

Characterization Theorem:
The generalized inequality can be characterized using dual cones:

    x ≼_K y  if and only if  λ^T x ≤ λ^T y for all λ ≽_K* 0

This means that x ≼_K y holds if and only if every linear functional that is 
nonnegative on K agrees that x is less than or equal to y [1].

================================================================================

MINIMUM AND MINIMAL ELEMENTS

In the context of generalized inequalities, we distinguish between minimum and 
minimal elements of a set S ⊆ ℝⁿ.

Minimum Element:
An element x ∈ S is the minimum element of S with respect to ≼_K if:
    x ≼_K y for all y ∈ S

Equivalently, x is minimum if S ⊆ x + K [19][21].

If a minimum exists, it is unique [19].

Minimal Elements:
An element x ∈ S is a minimal element of S with respect to ≼_K if:
    For every y ∈ S with y ≼_K x, we have y = x

Equivalently, x is minimal if (x - K) ∩ S = {x} [19].

A set may have multiple minimal elements, but at most one minimum element [19].

Key Difference:
- Minimum: x is smaller than or equal to every other element in S
- Minimal: No element in S is strictly smaller than x

================================================================================

DUAL CONE CHARACTERIZATION OF MINIMUM AND MINIMAL ELEMENTS

================================================================================

The dual cone provides powerful characterizations of both minimum and minimal elements through linear optimization problems, connecting generalized inequalities with supporting hyperplanes.

## Minimum Elements via Dual Cone

**Theorem:** An element x ∈ S is minimum with respect to ≼_K if and only if for all λ ≻_K* 0, x uniquely minimizes λᵀz over z ∈ S.

**Geometric Meaning:** Every vector λ ≻_K* 0 defines a strict supporting hyperplane to S at x. The set S lies entirely in the halfspace {z : λᵀz ≥ λᵀx}, and the hyperplane touches S only at x.

## Minimal Elements via Dual Cone

**Theorem:** For convex S, x is minimal with respect to ≼_K if and only if x minimizes λᵀz over S for some nonzero λ ≽_K* 0.

**Geometric Meaning:** There exists at least one supporting hyperplane at x with normal vector in the dual cone K*. This separates x from strictly better elements.

## Key Insights

**Supporting Hyperplane Connection:**
- Minimum elements: strict supporting hyperplanes in ALL dual directions λ ≻_K* 0
- Minimal elements: supporting hyperplane in SOME dual direction λ ≽_K* 0

**Algorithmic Application:**
1. Choose λ from appropriate dual cone region
2. Solve min_{z∈S} λᵀz  
3. Solution is guaranteed minimal (or minimum if λ ≻_K* 0)

**Pareto Optimality:** For K = ℝⁿ₊, minimal elements are Pareto efficient and minimize weighted sums λᵀz where λ ≥ 0, λ ≠ 0.

This characterization unifies optimization theory with geometric hyperplane separation through the dual cone framework.

================================================================================

EXAMPLES AND APPLICATIONS

Componentwise Ordering (ℝ₊ⁿ):
For vectors in ℝⁿ with the nonnegative orthant cone:
- x ≼ y means xᵢ ≤ yᵢ for all components i
- Used in multi-objective optimization and Pareto optimality [5][23]

Matrix Ordering (S₊ⁿ):
For symmetric matrices with the positive semidefinite cone:
- X ≼ Y means Y - X is positive semidefinite
- Fundamental in semidefinite programming and control theory [5][24]

Applications in Optimization:
- Conic optimization problems [6]
- Semidefinite programming [2][6]
- Multi-objective optimization [2]
- Vector optimization problems [2]

================================================================================

GEOMETRIC INTERPRETATION

The generalized inequality x ≼_K y has a clear geometric meaning: y lies in the 
translated cone x + K. The set x + K represents all points that are "greater 
than or equal to" x according to the ordering induced by K [5][19].

For the strict inequality x ≺_K y, the point y must lie in the interior of the 
translated cone x + interior(K), ensuring that y is strictly greater than x in 
all "directions" defined by the cone [5].

The partial nature of generalized inequalities means that some pairs of points 
may not be comparable - neither x ≼_K y nor y ≼_K x may hold [5][7].

================================================================================

SUMMARY

Generalized inequalities extend the concept of ordinary inequalities to 
vector spaces using proper cones. They preserve many essential properties of 
standard inequalities while providing a framework for partial orderings in 
multidimensional spaces. Key applications include:

- Convex optimization with cone constraints
- Matrix inequalities in semidefinite programming  
- Multi-objective optimization and Pareto analysis
- Vector optimization problems

The theory of generalized inequalities provides essential tools for modern 
optimization, enabling the formulation and solution of complex problems that 
cannot be expressed using scalar inequalities alone [1][5][6].

================================================================================
'''