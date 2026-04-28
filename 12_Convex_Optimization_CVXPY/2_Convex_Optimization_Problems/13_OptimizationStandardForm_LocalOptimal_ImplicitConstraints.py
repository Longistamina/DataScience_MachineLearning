"""
================================================================================
OPTIMIZATION PROBLEM STANDARD FORM (UPDATED)
================================================================================

###########################
## General Standard Form ##
###########################

An optimization problem in standard form is expressed as:

    minimize    f₀(x)
    subject to  fᵢ(x) ≤ 0,  i = 1, ..., m
                hⱼ(x) = 0,  j = 1, ..., p

where:
- x ∈ ℝⁿ is the optimization variable (decision variable)
- f₀(x) is the objective function (cost function)
- fᵢ(x) ≤ 0 are inequality constraint functions
- hⱼ(x) = 0 are equality constraint functions
- m ≥ 0 is the number of inequality constraints
- p ≥ 0 is the number of equality constraints

## Optimal Value

The optimal value is defined as:

    p* = inf{f₀(x) | fᵢ(x) ≤ 0, i = 1,...,m, hⱼ(x) = 0, j = 1,...,p}

Special cases:
- p* = ∞ if problem is infeasible (no x satisfies the constraints)
- p* = -∞ if problem is unbounded below


#########################
## Key Characteristics ##
#########################

1. OBJECTIVE: Always expressed as a minimization problem
2. INEQUALITIES: All written in "≤ 0" form (less than or equal to zero)
3. EQUALITIES: All written as "= 0" form
4. DOMAIN: The feasible set is D = ∩ᵢ₌₀ᵐ dom fᵢ ∩ ∩ⱼ₌₁ᵖ dom hⱼ

## Linear Programming Standard Form

For linear programs specifically, standard form is:

    minimize    cᵀx
    subject to  Ax = b
                x ≥ 0

where:
- c ∈ ℝⁿ is the coefficient vector
- A ∈ ℝᵐˣⁿ is the constraint matrix
- b ∈ ℝᵐ is the right-hand side vector (b ≥ 0)
- x ∈ ℝⁿ are the decision variables


#################################################
## Linear Programming Standard Form Properties ##
#################################################

1. ALL CONSTRAINTS ARE EQUALITIES (except non-negativity)
2. ALL VARIABLES ARE NON-NEGATIVE (x ≥ 0)
3. RIGHT-HAND SIDE IS NON-NEGATIVE (b ≥ 0)
4. OBJECTIVE CAN BE MIN OR MAX (by negating coefficients)


#######################################
## Convex Optimization Standard Form ##
#######################################

For convex optimization problems, standard form requires:

    minimize    f₀(x)
    subject to  fᵢ(x) ≤ 0,  i = 1, ..., m
                aᵢᵀx = bᵢ,  i = 1, ..., p

Additional requirements:
- f₀, f₁, ..., fₘ are CONVEX functions
- Equality constraints are AFFINE (linear)
- The feasible set is convex


#################################
## Converting to Standard Form ##
#################################

### 1. Maximization → Minimization
   max f(x) becomes min(-f(x))

### 2. Inequality Direction
   g(x) ≥ c becomes -g(x) + c ≤ 0

### 3. Equality Constraints  
   h(x) = c becomes h(x) - c = 0

### 4. Variable Bounds (for LP)
   - Unrestricted variable x: replace with x = x⁺ - x⁻ where x⁺, x⁻ ≥ 0
   - Upper bound x ≤ u: add slack variable s ≥ 0, constraint becomes x + s = u
   - Lower bound x ≥ l: substitute y = x - l where y ≥ 0

### 5. Inequality to Equality (for LP)
   - ax ≤ b: add slack variable s ≥ 0, becomes ax + s = b
   - ax ≥ b: subtract surplus variable s ≥ 0, becomes ax - s = b

   
########################
## Example Conversion ##
########################

Original problem:
    maximize    2x₁ + 3x₂
    subject to  x₁ + x₂ ≤ 4
                2x₁ - x₂ ≥ 1
                x₁ ≥ 0, x₂ unrestricted

Standard form:
    minimize    -2x₁ - 3x₂⁺ + 3x₂⁻
    subject to  x₁ + x₂⁺ - x₂⁻ + s₁ = 4
                2x₁ - x₂⁺ + x₂⁻ - s₂ = 1
                x₁, x₂⁺, x₂⁻, s₁, s₂ ≥ 0

where x₂ = x₂⁺ - x₂⁻, s₁ is slack variable, s₂ is surplus variable


###############################
## Why Standard Form Matters ##
###############################

1. ALGORITHMIC EFFICIENCY: Most optimization algorithms expect standard form
2. THEORETICAL ANALYSIS: Uniform framework for proving convergence properties
3. SOFTWARE IMPLEMENTATION: Solvers are designed for standard form input
4. DUALITY THEORY: Standard form enables clean dual problem formulation
5. SENSITIVITY ANALYSIS: Easier to analyze parameter changes


#######################
## Alternative Forms ##
#######################

1. CANONICAL FORM: Uses only inequality constraints (≤ form)
2. SLACK FORM: Explicit slack variables for simplex method
3. EPIGRAPH FORM: Reformulates as linear objective with constraint t ≥ f(x)

Standard form provides the mathematical foundation for systematic optimization problem solving 
and is essential for both theoretical development and practical implementation.


================================================================================
UNRESTRICTED VARIABLE TRANSFORMATION: x = x+ - x-
================================================================================

The Problem

In linear programming standard form, ALL variables must be non-negative (>= 0). 
However, sometimes we have variables that are unrestricted (free)
(meaning they can take any real value: positive, negative, or zero.)

=> The Solution: Variable Splitting

To handle an unrestricted variable x, we replace it with the difference of two non-negative variables:

        x = x+ - x-

where:
- x+ >= 0 (represents the "positive part")
- x- >= 0 (represents the "negative part")

How It Works

Case 1: x is positive (x > 0)
- Set x+ = x and x- = 0
- Then x = x+ - x- = x - 0 = x ✓

Case 2: x is negative (x < 0)
- Set x+ = 0 and x- = |x| = -x
- Then x = x+ - x- = 0 - (-x) = x ✓

Case 3: x is zero (x = 0)
- Set x+ = 0 and x- = 0
- Then x = x+ - x- = 0 - 0 = 0 ✓

Concrete Example

Suppose x = -5 (negative value):
- We can set x+ = 0 and x- = 5
- Then x = x+ - x- = 0 - 5 = -5 ✓

Alternatively, we could set x+ = 3 and x- = 8:
- Then x = x+ - x- = 3 - 8 = -5 ✓

The representation is NOT unique, but it always works.


================================================================================
OPTIMAL AND LOCALLY OPTIMAL POINTS
================================================================================

x is feasible if x ∈ dom f₀ and it satisfies the constraints.

A feasible x is optimal if f₀(x) = p*; X_opt is the set of optimal points

x is locally optimal if there is an R > 0 such that x is optimal for

Minimize (over z)  f₀(z)
Subject to         fᵢ(z) ≤ 0,  i = 1,...,m,  hᵢ(z) = 0,  i = 1,...,p
                  ||z - x||₂ ≤ R

## Optimal Value
The optimal value is defined as:

    p* = inf{f₀(x) | fᵢ(x) ≤ 0, i = 1,...,m, hⱼ(x) = 0, j = 1,...,p}

Special cases:
- p* = ∞ if problem is infeasible (no x satisfies the constraints)
- p* = -∞ if problem is unbounded below


Examples (with n = 1, m = p = 0)

   • f₀(x) = 1/x, dom f₀ = R₊₊: p* = 0, no optimal point

   • f₀(x) = -log x, dom f₀ = R₊₊: p* = -∞

   • f₀(x) = x log x, dom f₀ = R₊₊: p* = -1/e, x = 1/e is optimal

   • f₀(x) = x³ - 3x, p* = -∞, local optimum at x = 1


================================================================================
IMPLICIT CONSTRAINTS IN OPTIMIZATION PROBLEMS
================================================================================

################
## Definition ##
################

The standard form optimization problem has an implicit constraint:

   x ∈ D = [∩(i=0 to m) dom f_i] ∩ [∩(i=1 to p) dom h_i]

where:
- D is called the domain of the problem
- The constraints f_i(x) ≤ 0, h_i(x) = 0 are the explicit constraints
- A problem is unconstrained if it has no explicit constraints (m = p = 0)

What Are Implicit Constraints?
   Implicit constraints arise naturally from the requirement that 
   all functions in the optimization problem must be well-defined (finite) at the solution point. 
   Unlike explicit constraints which are written out clearly in the problem formulation, 
   implicit constraints are "hidden" within the domain restrictions of the functions involved.

Key Characteristics:
- They define where the objective and constraint functions are mathematically valid
- They automatically restrict the feasible region without being explicitly stated
- They cannot be violated during optimization (functions become undefined outside their domains)
- They are often overlooked but are crucial for problem feasibility

###########################################
## Example: Logarithmic Barrier Function ##
###########################################

   minimize f_0(x) = -∑(i=1 to k) log(b_i - a_i^T x)

This appears to be an unconstrained problem (no explicit constraints written), but it has implicit constraints:

   a_i^T x < b_i for all i = 1, ..., k

Explanation:
- The logarithm function log(·) is only defined for positive arguments
- For log(b_i - a_i^T x) to be well-defined, we need b_i - a_i^T x > 0
- This gives us the implicit constraint a_i^T x < b_i
- If x violates any of these constraints, the objective function becomes undefined (-∞)


#######################
## Why This Matters: ##
#######################

1. Problem Formulation: Implicit constraints help identify the true feasible region, which may be smaller than initially apparent.

2. Algorithm Design: Optimization algorithms must respect these domain restrictions to avoid numerical issues or undefined function evaluations.

3. Barrier Methods: The example shows how logarithmic barriers naturally enforce constraints through their domains, making explicit constraints unnecessary.

4. Theoretical Analysis: Understanding implicit constraints is essential for proving convergence, optimality conditions, and feasibility analysis.


#############################################
## Common Sources of Implicit Constraints: ##
#############################################

- Logarithmic functions: log(g(x)) requires g(x) > 0
- Square roots: √g(x) requires g(x) ≥ 0
- Reciprocals: 1/g(x) requires g(x) ≠ 0
- Matrix operations: Matrix inverse A^(-1) requires A to be invertible
- Norms and distances: Often require arguments to be in specific spaces

The implicit constraint concept bridges the gap between mathematical rigor and practical problem-solving, 
ensuring that optimization problems are well-posed and solvable.

================================================================================
"""