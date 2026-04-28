'''
================================================================================
DEFINITIONS
================================================================================

CONVEX SET:
A set C ⊆ ℝⁿ is convex if for all x, y ∈ C and 0 ≤ θ ≤ 1:
    θx + (1-θ)y ∈ C

CONVEX FUNCTION:
A function f: ℝⁿ → ℝ is convex if its domain is a convex set and 
for all x, y ∈ dom f and 0 ≤ θ ≤ 1:
    f(θx + (1-θ)y) ≤ θf(x) + (1-θ)f(y)

================================================================================
OPERATIONS PRESERVING CONVEXITY FOR SETS
================================================================================

1. INTERSECTION
   Property: The intersection of any collection of convex sets is convex
   Formula: If Cᵢ are convex for i ∈ I, then ∩ᵢ∈I Cᵢ is convex
   
   Examples:
   • Intersection of half-spaces: {x | aᵀx ≤ b₁} ∩ {x | cᵀx ≤ b₂}
   • Polytopes as intersections of half-spaces
   • Solution sets of linear inequalities
   • Feasible regions in linear programming

2. AFFINE TRANSFORMATIONS
   Property: Both images and preimages under affine transformations preserve convexity
   
   Forward transformation: If S is convex and f(x) = Ax + b, then
   f(S) = {Ax + b | x ∈ S} is convex
   
   Inverse transformation: If T is convex and f(x) = Ax + b, then
   f⁻¹(T) = {x | Ax + b ∈ T} is convex
   
   Examples:
   • Scaling: {ax | x ∈ C} for scalar a
   • Translation: {x + b | x ∈ C} for vector b
   • Rotation and reflection of convex sets
   • Linear transformations of ellipsoids remain ellipsoids

3. CARTESIAN PRODUCT
   Property: The Cartesian product of convex sets is convex
   Formula: If A ⊆ ℝᵐ and B ⊆ ℝⁿ are convex, then A × B ⊆ ℝᵐ⁺ⁿ is convex
   
   Examples:
   • Product of intervals: [a₁,b₁] × [a₂,b₂] = rectangle
   • Product of balls: B₁ × B₂ = cylinder
   • Higher-dimensional product spaces

4. CONVEX HULL
   Property: The convex hull of any set is the smallest convex set containing it
   Formula: conv(S) = {Σᵢ λᵢxᵢ | xᵢ ∈ S, λᵢ ≥ 0, Σᵢ λᵢ = 1}
   
   Examples:
   • Convex hull of finite points forms a polytope
   • Convex hull of circles forms a shape with curved and straight boundaries

5. MINKOWSKI SUM
   Property: The Minkowski sum of convex sets is convex
   Formula: A ⊕ B = {a + b | a ∈ A, b ∈ B}
   
   Examples:
   • Sum of two balls is a larger ball
   • Sum of polytopes is a polytope

6. PERSPECTIVE FUNCTION

   Definition:
   The perspective function P : ℝⁿ⁺¹ → ℝⁿ is defined as:

      P(x, t) = x/t

   where the domain is dom(P) = {(x, t) | t > 0}.

   The perspective function divides the first n elements of a vector by its last 
   component, effectively scaling or normalizing vectors so the last component 
   becomes one, then dropping the last component.

   Convexity Preservation Property:

   Forward Transformation (Image):
   If S ⊆ dom(P) ⊆ ℝⁿ⁺¹ is convex, then the image P(S) = {P(z) | z ∈ S} is convex.

   Inverse Transformation (Preimage):
   If T ⊆ ℝⁿ is convex, then the preimage P⁻¹(T) = {(x, t) | t > 0, x/t ∈ T} is 
   also convex.

   Proof Sketch:
   The convexity preservation follows from the perspective function's 
   linear-fractional nature. For any y₁, y₂ ∈ P(S) where y₁ = x₁/t₁ and 
   y₂ = x₂/t₂, and for any α ∈ [0,1], the convex combination αy₁ + (1-α)y₂ can 
   be shown to lie in P(S) due to the convexity of S.

   Examples and Applications:

   Geometric Interpretation:
   The perspective function can be thought of as perspective projection onto the 
   hyperplane consisting of all points with last coordinate equal to 1. For any 
   fixed z, P maps all points of the form t(z,1), (t > 0) to z, which form a ray 
   emanating from the origin.

   In Optimization:
   Perspective functions are extensively used in mixed integer nonlinear 
   programming (MINLP) to generate tight, tractable relaxations. They are 
   particularly applicable when binary indicator variables force continuous 
   decision variables to take the value 0 or belong to a convex set.

7. LINEAR-FRACTIONAL FUNCTION
   Definition:
   A linear-fractional function f : ℝⁿ → ℝᵐ is defined as:

      f(x) = (Ax + b)/(cᵀx + d)

   where:
   - A ∈ ℝᵐˣⁿ, b ∈ ℝᵐ, c ∈ ℝⁿ, d ∈ ℝ
   - Domain: dom(f) = {x | cᵀx + d > 0}

   Relationship to Perspective Function:
   A linear-fractional function is the composition of a perspective function with 
   an affine function. Specifically, if g : ℝⁿ → ℝᵐ⁺¹ is affine:

      g(x) = [A/cᵀ]x + [b/d]

   and P : ℝᵐ⁺¹ → ℝᵐ is the perspective map, then f = P ∘ g.

   Convexity Preservation Property:

   Forward Transformation:
   If S ⊆ dom(f) ⊆ ℝⁿ is convex, then the image f(S) = P(g(S)) is convex.

   Inverse Transformation:
   If T ⊆ ℝᵐ is convex, then the preimage f⁻¹(T) = g⁻¹(P⁻¹(T)) is convex.

   Mathematical Foundation:
   The convexity preservation follows from the composition of convexity-preserving 
   operations:
   1. Affine transformations preserve convexity
   2. Perspective functions preserve convexity
   3. The composition of convexity-preserving operations preserves convexity

   Examples:

   Simple Linear-Fractional Function:
      f(x) = 1/(x₁ + x₂ + 1)

   This maps convex sets to convex sets in the transformed space.

   Quasiconvexity Property:
   Linear-fractional functions of the form f(x) = (aᵀx + b)/(cᵀx + d) are 
   quasilinear (both quasiconvex and quasiconcave) on their domain.

   Special Cases:
   - When c = 0, the function reduces to an affine function: f(x) = (Ax + b)/d
   - In complex analysis, linear fractional transformations (Möbius 
   transformations) have the form f(z) = (az + b)/(cz + d) where ad - bc ≠ 0

   Applications:

   Optimization:
   Linear-fractional functions commonly appear in:
   - Fractional programming problems
   - Portfolio optimization with risk measures
   - Engineering design problems with efficiency ratios

   Geometric Transformations:
   In projective geometry, linear-fractional transformations preserve certain 
   geometric properties while maintaining convexity of sets under appropriate 
   conditions.

================================================================================
OPERATIONS PRESERVING CONVEXITY FOR FUNCTIONS
================================================================================

1. NONNEGATIVE WEIGHTED SUM
   Property: Linear combinations with nonnegative coefficients preserve convexity
   Formula: If f₁, f₂, ..., fₘ are convex and α₁, α₂, ..., αₘ ≥ 0, then
   f(x) = α₁f₁(x) + α₂f₂(x) + ... + αₘfₘ(x) is convex
   
   Examples:
   • f(x) = 2x² + 3|x| (quadratic + absolute value)
   • f(x) = ||x||₁ + ||x||₂ (sum of norms)
   • f(x,y) = x² + y² + 5xy (if xy term makes it convex)
   • Weighted sum of least squares terms

2. COMPOSITION WITH AFFINE FUNCTIONS
   Property: Convex functions composed with affine functions remain convex
   Formula: If f(x) is convex and g(x) = Ax + b is affine, then f(Ax + b) is convex
   
   Examples:
   • f(x) = (2x + 1)² (quadratic composed with affine)
   • f(x) = |Ax - b| (absolute value of affine function)
   • f(x) = ||Ax - b||₂ (Euclidean norm of affine function)
   • f(x) = exp(aᵀx + b) (exponential of affine function)

3. POINTWISE MAXIMUM AND SUPREMUM
   Property: The maximum of convex functions is convex
   Formula: If f₁, f₂, ..., fₘ are convex, then
   f(x) = max{f₁(x), f₂(x), ..., fₘ(x)} is convex
   
   Extended: f(x) = sup{g(x,y) | y ∈ Y} is convex if g(x,y) is convex in x for each y
   
   Examples:
   • f(x) = max{x, -x} = |x| (absolute value)
   • f(x) = max{0, x} (positive part function)
   • f(x) = max{aᵢᵀx + bᵢ | i = 1,...,m} (maximum of affine functions)
   • Support function: Sᴄ(x) = sup{yᵀx | y ∈ C}
   • Norm as maximum: ||x||∞ = max{|xᵢ| | i = 1,...,n}

4. COMPOSITION RULES (SCALAR CASE)
   Property: Certain compositions preserve convexity
   
   Case 1: If g is convex and h is convex and nondecreasing, then h(g(x)) is convex
   Case 2: If g is concave and h is convex and nonincreasing, then h(g(x)) is convex
   
   Examples:
   • f(x) = exp(g(x)) where g(x) is convex (exponential is convex and increasing)
   • f(x) = (g(x))² where g(x) is convex (square is convex and increasing on ℝ₊)
   • f(x) = log(g(x)) where g(x) is concave and positive (log is concave)
   • f(x) = -log(g(x)) where g(x) is concave and positive

5. PARTIAL MINIMIZATION
   Property: Minimizing over some variables preserves convexity
   Formula: If f(x,y) is convex in (x,y) and C is convex, then
   g(x) = inf{f(x,y) | y ∈ C} is convex

   (fix the x and minimize f(x,y) with y as variable and x as constant, take the derivative respect to y)

   Examples:
   • Distance to convex set: dist(x,S) = inf{||x-y|| | y ∈ S}
   • Optimal value function in convex optimization
   • f(x) = inf{y | (x,y) ∈ epi(h)} where h is convex
   • Legendre-Fenchel conjugate: f*(y) = sup{yᵀx - f(x) | x ∈ dom f}

6. PERSPECTIVE FUNCTION
   --------
   --------
   Definition:                                                                 
      Let f: ℝⁿ → ℝ ∪ {+∞}. The perspective of f is                            
      persp f : ℝⁿ × ℝ₊₊ → ℝ ∪ {+∞},                                            
      persp f(x, t) = t · f(x / t)    for t > 0.

      (the · means dot product - Tich Vo Huong in vietnamese)                       
                                                                              
   Domain:                                                                     
      {(x, t) | t > 0 and (x / t) ∈ dom f}

   Example (quadratic): 
      f(u) = ‖u‖₂²  
      persp f(x, t) = t · ‖x / t‖₂²                                                        
                    = ‖x‖₂² / t
      
      (valid for t > 0) 
   --------
   --------
   Property: The perspective of a convex function is convex
   Formula: If f: ℝⁿ → ℝ is convex, then g(x,t) = t · f(x/t) is convex on 
   {(x,t) | x/t ∈ dom f, t > 0}
   
   Examples:
   • If f(x) = xᵀx, then g(x,t) = xᵀx/t is convex for t > 0
   • If f(x) = ||x||, then g(x,t) = t||x/t|| = ||x|| for t > 0
   • Perspective of quadratic forms
   • Perspective of entropy functions

7. INTEGRAL AND INFINITE SUM
   Property: Integration and infinite summation preserve convexity
   
   Integral: If f(x,α) is convex in x for each α ∈ A, then
   g(x) = ∫ f(x,α) dμ(α) is convex
   
   Infinite sum: If fᵢ(x) is convex for each i and Σᵢ fᵢ(x) converges, then
   g(x) = Σᵢ fᵢ(x) is convex
   
   Examples:
   • Expected value: E[f(x,ξ)] where f(x,ξ) is convex in x
   • Infinite series of convex functions
   • Continuous mixtures of convex functions

8. VECTOR COMPOSITION RULES
   Property: Extended composition rules for vector-valued functions
   
   If g: ℝⁿ → ℝᵐ and h: ℝᵐ → ℝ, then f(x) = h(g(x)) is convex if:
   • g is affine and h is convex
   • gᵢ are convex, h is convex and nondecreasing in each argument
   • gᵢ are concave, h is convex and nonincreasing in each argument
   
   Examples:
   • f(x) = ||Ax + b||₂ (norm of affine function)
   • f(x) = h(g₁(x), g₂(x), ..., gₘ(x)) with appropriate monotonicity

================================================================================
SPECIAL CASES AND EXTENSIONS
================================================================================

1. EPIGRAPH CHARACTERIZATION
   Property: A function is convex if and only if its epigraph is a convex set
   Formula: epi f = {(x,t) | x ∈ dom f, f(x) ≤ t}
   
2. SUBLEVEL SETS
   Property: All sublevel sets of a convex function are convex
   Formula: Sₐ = {x ∈ dom f | f(x) ≤ α} is convex for all α

3. CONVEX CONJUGATE
   Property: The convex conjugate preserves convexity
   Formula: f*(y) = sup{yᵀx - f(x) | x ∈ dom f}
   -----
   -----
   Example 1:
      If f(x) = x², then f*(y) = supₓ (xy - x²). 
      We see that the sup over x is attained when y - 2x = 0, (get derivative respect to x => y - 2x)
      => x = y/2
      
      Then, replace x = y/2 back to xy - x²
      => so we have f*(y) = y² / 4.  
   -----
   -----
   Example 2: 
            x is a vector where x1, x2, x3, ... represents the quantity of product 1, 2, 3, ...
            y is a vector where y1, y2, y3, ... represents the market price of product 1, 2, 3, ... (usually fixed)
            f(x) is the function to calculate the total cost of production

   => yᵀx will be the gross revenue
   => yᵀx - f(x) will be the net profit
   
   => f*(y) = sup{yᵀx - f(x) | x ∈ dom f} means maximize the profit over product quantity x when the market price y is given
   -----
   -----
   
4. INDICATOR FUNCTIONS
   Property: The indicator function of a convex set is convex
   Formula: Iᴄ(x) = 0 if x ∈ C, +∞ if x ∉ C

5. SUPPORT FUNCTIONS
   Property: Support functions are always convex
   Formula: σᴄ(x) = sup{yᵀx | y ∈ C}

================================================================================
COUNTEREXAMPLES - OPERATIONS THAT DO NOT PRESERVE CONVEXITY
================================================================================

1. UNION OF CONVEX SETS
   Generally not convex
   Example: [0,1] ∪ [2,3] is not convex

2. MULTIPLICATION OF CONVEX FUNCTIONS
   Generally not convex
   Example: f(x) = x², g(x) = x², but (fg)(x) = x⁴ is not convex on ℝ

3. QUOTIENT OF CONVEX FUNCTIONS
   Generally not convex
   Example: f(x)/g(x) where both are convex

4. COMPOSITION WITHOUT MONOTONICITY
   Generally not convex
   Example: sin(x²) where x² is convex but sin is not monotonic

================================================================================
APPLICATIONS IN OPTIMIZATION
================================================================================

1. CONSTRUCTING CONVEX OBJECTIVE FUNCTIONS
   • Regularization terms: f(x) + λ||x||₁
   • Composite objectives: h(Ax + b) where h is convex

2. MODELING CONSTRAINTS
   • Linear constraints: Ax ≤ b
   • Second-order cone constraints: ||Ax + b|| ≤ cᵀx + d

3. DUALITY THEORY
   • Lagrange dual function constructed using infimum operation
   • Fenchel conjugates in convex analysis

4. ALGORITHM DESIGN
   • Proximal operators for composite functions
   • Splitting methods for sums of convex functions

================================================================================
END OF DOCUMENT
================================================================================

'''

import sympy as sp
import numpy as np

x = sp.symbols("x")
y = sp.symbols("y")
x_t = sp.symbols("x_t")
y_t = sp.symbols("y_t")
A = sp.symbols("A")
B = sp.symbols("B")
Bt = sp.symbols("Bt")
C = sp.symbols("C")

result = np.transpose(np.array([x_t, y_t])) @ np.array([[A, B], [Bt, C]]) @ np.array([x, y])
print(sp.simplify(result))
