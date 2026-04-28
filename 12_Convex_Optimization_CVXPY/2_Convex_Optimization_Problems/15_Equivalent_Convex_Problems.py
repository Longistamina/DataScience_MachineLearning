'''
================================================================================
EQUIVALENT CONVEX PROBLEMS - ELIMINATING EQUALITY CONSTRAINTS
================================================================================

DEFINITION OF EQUIVALENT PROBLEMS:
Two optimization problems are (informally) equivalent if the solution of one 
can be readily obtained from the solution of the other, and vice-versa.

TRANSFORMATION: ELIMINATING EQUALITY CONSTRAINTS

Original Problem:
minimize    f₀(x)
subject to  fᵢ(x) ≤ 0,  i = 1,...,m
            Ax = b

Equivalent Problem (after eliminating equality constraints):
minimize (over z)  f₀(Fz + x₀)
subject to         fᵢ(Fz + x₀) ≤ 0,  i = 1,...,m

KEY RELATIONSHIP:
Ax = b  ⟺  x = Fz + x₀ for some z

WHERE:
- F: Matrix whose columns form a basis for the null space of A
- x₀: Any particular solution to Ax = b
- z: New optimization variable (typically lower dimensional than x)

WHY THIS WORKS:
1. Any point satisfying Ax = b can be written as x = Fz + x₀
2. F's columns span the null space of A (directions where Ax doesn't change)
3. x₀ is any fixed point satisfying the equality constraint
4. By parameterizing x this way, we automatically satisfy Ax = b

BENEFITS:
- Reduces problem dimension (z has fewer components than x if A has full row rank)
- Eliminates equality constraints completely
- Converts constrained problem to simpler form with only inequality constraints
- Preserves convexity of the original problem

GEOMETRIC INTERPRETATION:
- Original feasible set: intersection of {x: Ax = b} with inequality constraints
- New feasible set: inequality constraints applied to the affine subspace {x: Ax = b}
- We're essentially "projecting" the problem onto the constraint surface Ax = b

EXAMPLE:
Original: minimize x₁² + x₂² subject to x₁ + x₂ = 1
- Here A = [1 1], b = 1
- Null space of A spanned by F = [1; -1] (or any scalar multiple)
- Particular solution x₀ = [0.5; 0.5]
- Parametrization: x = z[1; -1] + [0.5; 0.5]
- New problem: minimize (z + 0.5)² + (-z + 0.5)² = 2z² + 0.5
- Solution: z* = 0, giving x* = [0.5; 0.5]

================================================================================
4 CONVEX PROBLEM TRANSFORMATIONS
================================================================================

---------------------------------------

1. INTRODUCING EQUALITY CONSTRAINTS

Original Problem:
minimize    f₀(A₀x + b₀)
subject to  fᵢ(Aᵢx + bᵢ) ≤ 0,  i = 1,...,m

Equivalent Problem:
minimize (over x, yᵢ)  f₀(y₀)
subject to             fᵢ(yᵢ) ≤ 0,   i = 1,...,m
                       yᵢ = Aᵢx + bᵢ, i = 0,1,...,m

Short explanation: Replace composed functions with auxiliary variables and equality constraints.
This technique separates the linear transformations from the nonlinear functions, often simplifying analysis.

---------------------------------------

2. INTRODUCING SLACK VARIABLES FOR LINEAR INEQUALITIES

Original Problem:
minimize    f₀(x)
subject to  aᵢᵀx ≤ bᵢ,  i = 1,...,m

Equivalent Problem:
minimize (over x, s)  f₀(x)
subject to            aᵢᵀx + sᵢ = bᵢ,  i = 1,...,m
                      sᵢ ≥ 0,           i = 1,...,m

Short explanation: Convert linear inequalities to equalities by adding non-negative slack variables.
This is fundamental in linear programming and turns inequality constraints into equality + bound constraints.

---------------------------------------

3. EPIGRAPH FORM

Original Standard Form:
minimize    f₀(x)
subject to  fᵢ(x) ≤ 0,  i = 1,...,m
            Ax = b

Equivalent Epigraph Form:
minimize (over x, t)  t
subject to             f₀(x) - t ≤ 0
                       fᵢ(x) ≤ 0,    i = 1,...,m
                       Ax = b

Short explanation: Introduce variable t to upper−bound the objective.
This converts the objective into a constraint and yields a linear objective.

---------------------------------------

4. MINIMIZING OVER SOME VARIABLES

Original Problem:
minimize    f₀(x₁, x₂)
subject to  fᵢ(x₁) ≤ 0,  i = 1,...,m

Equivalent Reduced Problem:
minimize    f̃₀(x₁)
subject to  fᵢ(x₁) ≤ 0,  i = 1,...,m

where f̃₀(x₁) = infₓ₂ f₀(x₁, x₂)

Short explanation: When x₂ appears only in the objective, we can analytically minimize over x₂ to reduce dimensionality.
This uses partial minimization to simplify the problem.

---------------------------------------

WHEN TO USE THESE TRANSFORMATIONS:

1. INTRODUCING EQUALITY CONSTRAINTS:
   Use when you need to separate linear or affine transformations from nonlinear functions, 
   making the problem structure clearer and often simplifying gradients and Hessians.

2. INTRODUCING SLACK VARIABLES:
   Use when converting linear inequalities into equalities plus nonnegative bounds makes constraint handling easier, 
   as in interior-point or active-set algorithms.

3. EPIGRAPH FORM:
   Use when you want a linear objective and prefer to cast the original objective as a constraint; 
   this is useful for methods that exploit linearity in the objective, such as certain conic solvers.

4. PARTIAL MINIMIZATION (MINIMIZING OVER SOME VARIABLES):
   Use when some variables appear only in the objective; 
   analytically minimize over them to reduce problem dimension and simplify computations while preserving convexity.

'''