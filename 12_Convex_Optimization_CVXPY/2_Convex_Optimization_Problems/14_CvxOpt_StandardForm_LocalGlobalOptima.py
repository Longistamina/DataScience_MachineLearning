'''

'''"""
================================================================================
CONVEX OPTIMIZATION PROBLEM STANDARD FORM
================================================================================

Standard Form Convex Optimization Problem

minimize f₀(x)
subject to fᵢ(x) ≤ 0,  i = 1, ..., m
          aᵢᵀx = bᵢ,  i = 1, ..., p

Key Requirements for Convexity:
- f₀, f₁, ..., fₘ are CONVEX functions
- Equality constraints are affine (linear functions)

Alternative Compact Form:
minimize f₀(x)
subject to fᵢ(x) ≤ 0,  i = 1, ..., m
          Ax = b

where A is an m×n matrix and b is an m-dimensional vector.

Quasiconvex Extension:
The problem is quasiconvex if f₀ is quasiconvex (and f₁, ..., fₘ remain convex).

Why This Form Matters:

1. Convex Feasible Set: The feasible set of a convex optimization problem is always convex. This is because:
   - Each constraint fᵢ(x) ≤ 0 defines a convex set (sublevel set of convex function)
   - Each equality constraint aᵢᵀx = bᵢ defines a convex set (hyperplane)
   - The intersection of convex sets is convex

2. Global Optimality: Any local minimum is guaranteed to be a global minimum for convex problems.

3. Efficient Algorithms: This standard form enables polynomial-time algorithms with convergence guarantees.

4. Duality Theory: The standard form provides a clean foundation for developing dual problems and strong duality results.

5. Practical Implementation: Most convex optimization solvers expect input in this standard form.

Important Property: The feasible set of a convex optimization problem is convex

This fundamental property ensures that:
- The problem has no "holes" or disconnected regions
- Line segments between any two feasible points remain feasible
- Gradient-based methods can navigate the feasible region efficiently
- The geometry supports powerful theoretical results

================================================================================
EXAMPLE
================================================================================

#######################
#### WRONG example ####
#######################
    minimize f₀(x) = x₁⁴ + x₂⁵
    subject to f₁(x) = x₁/(1 + x₂²) ≤ 0
            h₁(x) = (x₁ + x₂)² = 0

• f₀ is convex; feasible set {(x₁,x₂) | x₁ = -x₂ ≤ 0} is convex

• not a convex problem (according to our definition): f₁ is not convex, h₁ 
  is not affine

#######################
#### RIGHT example ####
#######################

Equivalent (but not identical) to the convex problem

    minimize x₁² + x₂²
    subject to x₁ ≤ 0 (this is a convex constraint)
               x₁ + x₂ = 0 (this is an affine constraint)

================================================================================
LOCAL AND GLOBAL OPTIMA
================================================================================

any locally optimal point of a convex problem is (globally) optimal

proof: suppose x is locally optimal, but there exists a feasible y with
f₀(y) < f₀(x)

x locally optimal means there is an R > 0 such that

z feasible, ||z - x||₂ ≤ R  ⟹  f₀(z) ≥ f₀(x)

consider z = θy + (1 - θ)x 
with θ = R/(2||y - x||₂)

• ||y - x||₂ > R, so 0 < θ < 1/2
• z is a convex combination of two feasible points, hence also feasible
• ||z - x||₂ = R/2 and

f₀(z) ≤ θf₀(y) + (1 - θ)f₀(x) < f₀(x)

which contradicts our assumption that x is locally optimal

================================================================================
FIRST-ORDER OPTIMALITY CONDITION FOR CONVEX OPTIMIZATION
================================================================================

What the condition means:
∇f₀(x)ᵀ(y - x) ≥ 0 for all feasible y

BREAKDOWN OF THE MATH:
- ∇f₀(x): Gradient of objective function at point x (vector pointing in direction of steepest increase)
- (y - x): Direction vector from current point x to any other feasible point y
- ∇f₀(x)ᵀ(y - x): Dot product = |gradient| × |direction| × cos(θ)
- ≥ 0: This dot product must be non-negative

WHAT THIS MEANS GEOMETRICALLY:
1. The angle θ between gradient and any feasible direction must be ≥ 90°
2. The gradient "points outward" from the feasible set
3. No feasible direction can decrease the objective function

INTUITIVE EXPLANATION:
- Imagine you're on a hill (the objective function)
- x is your current position
- The gradient shows the steepest uphill direction from x
- The condition says: "No matter which way you can legally move (feasible directions), 
  you cannot go downhill"
- This means x is at the bottom of the hill within the allowed region

WHY IT WORKS FOR CONVEX PROBLEMS:
- In convex problems, any local minimum is automatically global minimum
- The first-order condition is both necessary AND sufficient
- If the condition holds, x is guaranteed to be the global optimum

SUPPORTING HYPERPLANE INTERPRETATION:
- The gradient defines a hyperplane (like a flat surface) passing through x
- This hyperplane "supports" the feasible set (entire set lies on one side)
- The feasible set cannot "dip below" this hyperplane
- This geometric fact ensures x is optimal

PRACTICAL MEANING:
- This is the mathematical foundation for gradient descent
- At the optimum, the gradient must be "blocked" by constraints
- If unconstrained: gradient = 0 (special case)
- If constrained: gradient points "outward" from feasible region

EXAMPLE:
Minimize f(x,y) = x² + y² subject to x + y ≥ 1
- At optimum (0.5, 0.5): gradient = (1, 1)
- Any feasible direction (y-x) makes angle ≥ 90° with gradient (1,1)
- Moving along constraint boundary: (1,1)·(1,-1) = 0 ≥ 0 ✓
- Moving into feasible region: (1,1)·(1,1) = 2 > 0 ✓

================================================================================
THREE TYPES OF OPTIMALITY CONDITIONS IN CONVEX OPTIMIZATION
================================================================================

1. UNCONSTRAINED PROBLEM:
   x is optimal if and only if:
   x ∈ dom f₀,    ∇f₀(x) = 0

   Short explanation: At the optimum, the gradient must be zero since we can move in any direction.
   This is the standard calculus condition for finding minima.

2. EQUALITY CONSTRAINED PROBLEM:
   minimize f₀(x) subject to Ax = b

   x is optimal if and only if there exists a ν such that:
   x ∈ dom f₀,    Ax = b,    ∇f₀(x) + Aᵀν = 0

   Short explanation: The gradient of the objective plus weighted constraint gradients equals zero.
   This is the method of Lagrange multipliers where ν are the multipliers.

3. MINIMIZATION OVER NONNEGATIVE ORTHANT:
   minimize f₀(x) subject to x ≽ 0

   x is optimal if and only if:
   x ∈ dom f₀,    x ≽ 0,    { ∇f₀(x)ᵢ ≥ 0  if xᵢ = 0
                              { ∇f₀(x)ᵢ = 0  if xᵢ > 0

   Short explanation: For inactive constraints (xᵢ > 0), gradient component is zero; for active constraints (xᵢ = 0), gradient points outward.
   This captures the complementary slackness condition for box constraints.

"""
