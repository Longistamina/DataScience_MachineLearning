'''
============================================

      CORE IDEAS OF CONVEX FUNCTIONS

============================================

##################################
## Definition and Basic Concept ##
##################################

A real-valued function f: ℝⁿ → ℝ is called **convex** if its domain is a convex set 
and for any two points x, y in its domain and any λ ∈ [0,1], the inequality holds:

            f(λx + (1-λ)y) ≤ λf(x) + (1-λ)f(y)

**Geometric Interpretation**: The line segment connecting any two points on the graph lies above or on the graph itself. 
Visually, convex functions are "cup-shaped" (∪) while concave functions are "cap-shaped" (∩) [1][4][7].

**Epigraph Characterization**: A function is convex if and only if its epigraph (the set of points on or above the graph) 
forms a convex set [1][3].


##################################################
## EXTENDED-VALUE EXTENSION OF CONVEX FUNCTIONS ##
##################################################

The extended-value extension allows us to work with convex functions 
that are naturally defined only on a subset of the space 
by extending them to the entire space using infinity values[2][4][6].

**Extended Real-Valued Functions**: These are functions that take values in **R ∪ {∞} = (-∞, ∞]**, 
rather than just real numbers[2][7].

**Extended-Value Extension**: If f is a convex function with domain dom f, 
its extended-value extension f̃ : Rⁿ → R ∪ {∞} is defined as[3][4][6]:

                f̃(x) = {
                    f(x),  if x ∈ dom f
                    ∞,     if x ∉ dom f
                }


#########################################
## First-Order Condition for Convexity ##
#########################################

For a differentiable function f, convexity is equivalent to:

                    f(y) ≥ f(x) + ∇f(x)ᵀ(y - x) for all x, y ∈ dom(f)

**Interpretation**: The first-order Taylor approximation (tangent line) at any point serves as a global underestimator 
                    of the function. This means every tangent line lies entirely below the function graph [9][12][15].


##########################################
## Second-Order Condition for Convexity ##
##########################################

For twice-differentiable functions, f is convex if and only if:

                    ∇²f(x) ⪰ 0 for all x ∈ dom(f)

The Hessian matrix must be positive semidefinite everywhere in the domain. 
For single-variable functions, this reduces to f''(x) ≥ 0 [2][10][15].


#####################
## Common Examples ##
#####################

**Single Variable**:
- Linear: f(x) = ax + b (always convex)
- Quadratic: f(x) = ax² (convex if a ≥ 0)
- Exponential: f(x) = eˣ (always convex)
- Logarithm: f(x) = -log(x) on x > 0 (convex)


**Multivariable**:
- Quadratic forms: f(x) = ½xᵀPx + qᵀx + r (convex if P ⪰ 0)
- Least-squares: f(x) = ||Ax - b||²₂
- Norms: f(x) = ||x|| for any norm
- Log-sum-exponential: f(x) = log(∑ᵢ eˣⁱ)
- Quadratic-over-linear: f(x,y) = x²/y for y > 0
- Geometric mean: f(x) = (x₁ · x₂ · … · xₙ)^(1/n)
                       = exp((1/n) · (log x₁ + log x₂ + … + log xₙ))


#####################################
## Operations Preserving Convexity ##
#####################################

**Nonnegative Linear Combinations**: If f₁, f₂ are convex and a₁, a₂ ≥ 0, then a₁f₁ + a₂f₂ is convex.

**Pointwise Maximum**: If fₛ is convex for all s ∈ S, then f(x) = maxₛ∈ₛ fₛ(x) is convex.

**Affine Composition**: If f is convex, then g(x) = f(Ax + b) is convex. (restict convex function to a line)

**Partial Minimization**: If g(x,y) is convex in both variables and C is convex, then f(x) = min_{y∈C} g(x,y) is convex [17][18][21].


#########################
## Jensen's Inequality ##
#########################

For any convex function f and probability weights λᵢ ≥ 0 with ∑λᵢ = 1:

f(∑λᵢxᵢ) ≤ ∑λᵢf(xᵢ)

**Probabilistic Form**: If X is a random variable and φ is convex, then φ(E[X]) ≤ E[φ(X)]. 
This fundamental inequality underlies many important results in probability and analysis.


##################
## Sublevel Set ##
##################

**Definition**: For a function f: ℝⁿ → ℝ and a real number α ∈ ℝ, the α-sublevel set (or simply sublevel set) is defined as:

            C_α(f) = {x ∈ dom(f) : f(x) ≤ α}

**Geometric Interpretation**: The sublevel set consists of all points in the domain where the function value is at most α. 
For a one-dimensional function, this represents the x-coordinates where the graph lies on or below the horizontal line y = α.

**Key Properties**:
- If f is convex, then all its α-sublevel sets are convex for any value of α
- The converse is not true: a function can have all convex sublevel sets but not be convex itself
- Functions with convex sublevel sets are called "quasiconvex" 

**Proof of Convexity**: For a convex function f, if x, y ∈ C_α and θ ∈ [0,1], then:
f(θx + (1-θ)y) ≤ θf(x) + (1-θ)f(y) ≤ θα + (1-θ)α = α

Therefore, θx + (1-θ)y ∈ C_α, proving the sublevel set is convex.


###############
## Epigraphs ##
###############

**Definition**: The epigraph of a function f: ℝⁿ → ℝ is the set of all points lying on or above the graph of the function:

            epi(f) = {(x,t) ∈ ℝⁿ × ℝ : t ≥ f(x)}

**Geometric Interpretation**: The epigraph includes the graph of the function and the entire region above it, 
extending infinitely upward.

**Fundamental Theorem**: A function f is convex if and only if its epigraph is a convex set.

**Proof Outline**:
(⇒) If f is convex: For any (x₁,t₁), (x₂,t₂) ∈ epi(f) and λ ∈ [0,1]:
- We have f(x₁) ≤ t₁ and f(x₂) ≤ t₂
- By convexity: f(λx₁ + (1-λ)x₂) ≤ λf(x₁) + (1-λ)f(x₂) ≤ λt₁ + (1-λ)t₂
- Therefore: (λx₁ + (1-λ)x₂, λt₁ + (1-λ)t₂) ∈ epi(f)

(⇐) If epi(f) is convex: For any x₁, x₂ ∈ dom(f) and λ ∈ [0,1]:
- Points (x₁,f(x₁)) and (x₂,f(x₂)) are in epi(f)
- Their convex combination (λx₁ + (1-λ)x₂, λf(x₁) + (1-λ)f(x₂)) is also in epi(f)
- This means f(λx₁ + (1-λ)x₂) ≤ λf(x₁) + (1-λ)f(x₂), proving convexity
'''