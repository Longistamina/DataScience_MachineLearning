'''
# Log-Concave and Log-Convex Functions

================================================================================

A nonnegative function f on a convex domain X ⊆ ℝⁿ is called **log-concave** if its logarithm is concave, 
and **log-convex** if its logarithm is convex.

----------------------
Definition (Log-Concave): f is log-concave ⇔ for all x,y∈X and θ∈[0,1]:  
    
    f(θx+(1-θ)y) ≥ f(x)^θ * f(y)^(1-θ)  

Equivalently, if f > 0 on X:  
    log[f(θx+(1-θ)y)] ≥ θ*log[f(x)] + (1-θ)*[logf(y)].

----------------------
Definition (Log-Convex): f is log-convex ⇔ for all x,y∈X and θ∈[0,1]:  
    f(θx+(1-θ)y) ≤ f(x)^θ * f(y)^(1-θ)  

Equivalently, if f>0,  
     log[f(θx+(1-θ)y)] ≤ θ*log[f(x)] + (1-θ)*log[f(y)].

----------------------
Key Properties  
- Every concave nonnegative function is log-concave, but a log-concave function need not be concave 
    (e.g. Gaussian: f(x)=exp(-x²/2)).  
- Every log-convex function is convex (since the exponential of a convex function is convex).  
- Log-concave ⇒ quasiconcave: all superlevel sets {x: f(x) ≥ α} are convex.  
- Log-convex ⇒ quasiconvex: all sublevel sets {x: f(x) ≤ α} are convex.

Second-Derivative Test (1D)  
- f is log-concave ⇔ f f″ ≤ (f′)² on domain where f>0.  
- f is log-convex ⇔ f f″ ≥ (f′)².
(f f″ simply means the product of a function and its second derivative at the same point)

Examples  
- Log-Concave: Gaussian density f(x)=(2π)^-½ exp(-x²/2), Laplace density f(x)=½ exp(-|x|).  
- Log-Convex: Exponential f(x)=e^{ax} (a real), gamma function on (0,∞).  
- Neither/Edge: x² (convex but not log-convex), indicator function of a convex set (log-concave by allowing f=0).

Operations Preserving  
- Products of log-concave functions remain log-concave.  
- Nonnegative weighted sums preserve log-concavity.  
- Marginalization (integration) preserves log-concavity (Prékopa-Leindler theorem).

================================================================================

CONSEQUENCES OF THE LOG-CONCAVE INTEGRATION PROPERTY

================================================================================

**Prékopa’s theorem** states: If H(x, y) is log-concave on ℝ^{m+n}, then its marginal  
 M(y) = ∫_{ℝ^m} H(x, y) dx  
is also log-concave in y.

Key consequences:

1. **Closure under Marginalization**  
   - Marginals of log-concave densities are log-concave.  
   - Any projection of a log-concave measure preserves log-concavity.

2. **Closure under Convolution (Expanded)**  
   - The convolution of two log-concave functions f and g, defined as  
         (f * g)(x) = ∫ f(x-y)g(y)dy  
     is also log-concave.
   - In probability, this means the sum of two independent log-concave random variables 
     has a log-concave distribution.
   - **Why?** Convolution is a special case of marginalization:  
         H(x, y) = f(x-y) g(y) is log-concave in (x, y), 
         so integrating out y gives a log-concave function in x.
   - **Implications:**  
     • Log-concave distributions are stable under addition (sums), 
       so properties like unimodality and concentration are preserved.  
     • This is crucial in probability, statistics, and combinatorics, 
       where sums or mixtures of random variables are common.

3. **Functional and Geometric Inequalities**  
   - Underlies the Prékopa-Leindler and Brunn-Minkowski inequalities.  
   - Supports isoperimetric and concentration results in high dimensions.

4. **Convexity of Level Sets**  
   - Superlevel sets {y : M(y) ≥ α} are convex for any α.  
   - Feasible regions defined by marginals are convex, aiding optimization.

5. **Preservation under Linear Mappings**  
   - Affine images of log-concave functions remain log-concave.

6. **Statistical Modeling**  
   - Enables tractable inference: integrating out latent variables in a log-concave joint density 
     preserves log-concavity of the observed marginal.

**Summary:**  
The integration property makes log-concave functions robust under marginalization and convolution, 
central to convex geometry, probability, optimization, and statistics.

================================================================================

YIELD FUNCTION AS A CONSEQUENCE OF LOG-CONCAVE CONVOLUTION

================================================================================

**Yield Function Definition:**  
Suppose x ∈ ℝⁿ represents nominal (designed) parameters for a product,  
w ∈ ℝⁿ is a random vector of manufacturing variations (noise),  
and S ⊆ ℝⁿ is the set of acceptable (spec-compliant) values.

The **yield function** is:
 Y(x) = P(x + w ∈ S)
    = ∫_{w ∈ ℝⁿ} 1_S(x + w) p(w) dw

where 1_S(·) is the indicator function of S, and p(w) is the probability density of w.

**Convolution Form:**  
Y(x) = (1_S * p)(x)
   = ∫ 1_S(x - y) p(y) dy

**Log-Concave Consequence:**  
- If S is convex and p(w) is log-concave (e.g., Gaussian, Laplace),  
  then Y(x) is a log-concave function of x [6].
- This follows because:
  - The indicator function 1_S is log-concave when S is convex.
  - The convolution of two log-concave functions is log-concave [1][2][6].

**Implications:**  
- The **yield region** {x : Y(x) ≥ α} is convex for any α ∈ [0,1].
- This property enables efficient optimization and robust design, 
since maximizing or constraining yield can be done over convex sets.

**Summary:**  
The log-concave convolution property ensures that, under convex specs and log-concave noise, 
the yield as a function of design parameters is log-concave—making yield optimization tractable and robust.

================================================================================



'''