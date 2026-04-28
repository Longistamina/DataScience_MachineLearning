'''
================================================================================

                CORE IDEAS AND EXAMPLE OF QUASICONVEX FUNCTIONS

================================================================================

## Definition
A function f: ℝⁿ → ℝ is quasiconvex if for all x, y ∈ dom(f) and all λ ∈ [0,1]:
    f(λx + (1–λ)y) ≤ max{f(x), f(y)}  

Equivalently, all its sublevel sets     
    C_α(f) = {x ∈ dom(f) : f(x) ≤ α}  
are convex for every α ∈ ℝ [1][2].


## Geometric Interpretation
Quasiconvexity means “no valleys” deeper than the higher of two endpoints. 
Any line segment through the graph never rises above the maximum of its endpoints. 
Sublevel sets form nested convex regions.


## Relation to Convexity
- Every convex function is quasiconvex, but not vice versa.  
- A quasiconvex function need not satisfy the first-order support condition ∇f(x)ᵀ(y–x) ≥ 0.


## First-Order Characterization (Differentiable Case)
If f is differentiable, f is quasiconvex if and only if for all x, y:
    f(y) ≤ f(x) ⇒ ∇f(x)ᵀ(y–x) ≤ 0  
Gradient at x points “uphill” away from any lower-value point.


## Example: Ratio of Affine Functions:  
    f(x) = (aᵀx + b)/(cᵀx + d), dom(f) = {x : cᵀx + d > 0}  

This function is quasiconvex when cᵀx + d > 0 and denominator positive, since its sublevel sets  
    {x : (aᵀx + b)/(cᵀx + d) ≤ α} ⇔ {x : aᵀx + b – α(cᵀx + d) ≤ 0}  
are halfspaces, hence convex.


## Key Properties
1. **Preservation under Monotone Transformations**: 
   If φ is nondecreasing and f is quasiconvex, then φ∘f is quasiconvex.  

2. **Maximum of Quasiconvex Functions**: 
   The pointwise maximum of any family of quasiconvex functions is quasiconvex. 

3. **Quasiconcavity Dual**: 
   –f is quasiconcave whenever f is quasiconvex.

   
## Why It Matters
Quasiconvex functions arise in fractional programming, economics (utility ratios), and robustness analysis. 
They allow efficient level-set methods and generalized gradient algorithms even when convexity fails.


================================================================================

INTERNAL RATE OF RETURN (IRR) AS A QUASICONCAVE FUNCTION

================================================================================

## Definition and Mathematical Foundation
The **Internal Rate of Return (IRR)** is the discount rate that makes the net present value (NPV) of all cash flows 
from an investment equal to zero. Mathematically, for a cash flow stream x = (x₀, x₁, ..., xₙ), the IRR is defined as:

                RR(x) = inf{r ≥ 0 | PV(x,r) = 0}

where the present value function is:
                PV(x,r) = Σᵢ₌₀ⁿ xᵢ/(1+r)ⁱ

Here, x₀ < 0 represents the initial investment (cash outflow) 
and x₁, x₂, ..., xₙ are subsequent cash flows (typically positive inflows).


## IRR as a Quasiconcave Function
**Theorem**: The IRR function is quasiconcave with respect to cash flow vectors.

**Proof Structure**: IRR is quasiconcave because its superlevel sets are convex. 
For any threshold R ≥ 0, the superlevel set is defined as:
                
                {x : IRR(x) ≥ R}

This is equivalent to:
{x : Σᵢ₌₀ⁿ xᵢ/(1+r)ⁱ ≥ 0 for all 0 ≤ r ≤ R}

Since this represents the intersection of halfspaces (linear inequalities), it forms a convex set, proving quasiconcavity.


## Geometric and Economic Interpretation
**Superlevel Set Interpretation**: For any return threshold R, 
the set of all cash flow streams achieving IRR ≥ R forms a convex region. This means:

- If two investment projects both achieve IRR ≥ R, then any portfolio (convex combination) of these projects also achieves IRR ≥ R
- This reflects the economic principle that diversification preserves return thresholds

**Modified Jensen's Inequality**: For quasiconcave functions, we have:
        IRR(θx + (1-θ)y) ≥ min{IRR(x), IRR(y)}

This means combining two investment projects yields an IRR at least as good as the worse of the two individual IRRs.


## Relationship to Present Value Function
**Present Value Function Properties**:
- PV(x,r) = Σᵢ₌₀ⁿ xᵢ/(1+r)ⁱ is linear in the cash flows x
- For fixed x, PV(x,r) is a decreasing function of the interest rate r
- The function is convex in r, meaning NPV curves are "bowl-shaped" when plotted against interest rates

**IRR as Inverse Function**: IRR can be viewed as the inverse of the present value function:
IRR(x) = PV⁻¹(0|x)

The quasiconcavity of IRR emerges from the convexity properties of the present value function 
combined with the inverse relationship.


================================================================================

JENSEN'S INEQUALITY

================================================================================

## Definition
For a convex function f and any set of points x₁, x₂, ..., xₙ in its domain 
with nonnegative weights w₁, w₂, ..., wₙ such that Σwᵢ = 1:

    f(w₁x₁ + w₂x₂ + ... + wₙxₙ) ≤ w₁f(x₁) + w₂f(x₂) + ... + wₙf(xₙ)

**Probabilistic Form**: If X is a random variable and f is convex, then:
    E[f(X)] ≥ f(E[X])

**Intuitive Meaning**: The function value of a weighted average is at most the weighted average of function values.


## Geometric Interpretation
Jensen's inequality generalizes the fact that for convex functions, 
the line segment connecting any two points on the graph lies above the function itself. 

The inequality extends this to weighted averages of multiple points.


## Key Examples
**Quadratic Mean-Arithmetic Mean**: Using f(x) = x², we get:
    E[X²] ≥ (E[X])²

This is equivalent to saying Var(X) ≥ 0.

**Arithmetic Mean-Geometric Mean**: Using f(x) = -ln(x), we obtain:
(x₁ · x₂ · ... · xₙ)^(1/n) ≤ (x₁ + x₂ + ... + xₙ)/n.

**Harmonic Mean**: Using f(x) = 1/x for x > 0 gives harmonic mean inequalities.


## Proof Strategy
The proof uses the fact that any convex function lies above its tangent line at any point. 
For a convex function f at point μ = E[X], there exists a tangent line L(x) = a + bx such that f(x) ≥ L(x) for all x. 

Taking expectations:
    E[f(X)] ≥ E[L(X)] = E[a + bX] = a + bE[X] = L(E[X]) = f(E[X]) [13][16][19]


## Equality Conditions
Equality holds in Jensen's inequality if and only if:
- All points are equal (x₁ = x₂ = ... = xₙ), OR
- The function is linear on the relevant domain

For strictly convex functions, equality occurs only when all points are equal [13].


## Concave Functions
For concave functions, Jensen's inequality reverses:
    f(w₁x₁ + ... + wₙxₙ) ≥ w₁f(x₁) + ... + wₙf(xₙ)

In probabilistic form: f(E[X]) ≥ E[f(X)]


## Applications
**Information Theory**: Used in entropy calculations and KL-divergence bounds
**Statistics**: Fundamental in proving variance properties and concentration inequalities  
**Economics**: Utility theory and risk analysis
**Machine Learning**: Expectation-maximization algorithms and variational methods


## Summary
Jensen's inequality provides a fundamental relationship between function values and expectations for convex/concave functions. 
It bridges geometry (convexity) with probability theory (expectations), making it one of the most versatile tools in mathematical analysis.

================================================================================
'''