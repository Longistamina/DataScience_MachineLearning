'''
================================================================================

CONVEXITY WITH RESPECT TO GENERALIZED INEQUALITIES

================================================================================

Definition  
Let K ⊆ ℝᵐ be a proper cone (closed, convex, pointed, with nonempty interior), 
and define the generalized inequality  

    u ≽_K v  ⇔  u-v ∈ K.  

A function f: 𝒳→ℝᵐ on a convex domain 𝒳⊆ℝⁿ is K-convex if for all x,y ∈ 𝒳 and all λ∈[0,1]:  

    f(λx+(1-λ)y) ≽_K λf(x)+(1-λ)f(y).  

--------------------------------
Epigraph-Based Characterization  
Define the K-epigraph of f as  
    
    epi_K f = {(x,t) ∈ 𝒳×ℝᵐ : t ≽_K f(x)}.  

Then f is K-convex ⇔ epi_K f is convex in ℝⁿ×ℝᵐ.

--------------------------------
Examples of Generalized Inequalities  
1. Componentwise Order (K=ℝⁿ₊):  
   u≽_K v means uᵢ≥vᵢ for all i. 
   f:ℝⁿ→ℝⁿ is K-convex if each component fᵢ is convex and the inequality holds componentwise.  

2. PSD Order (K=Sⁿ₊):  
   Identify symmetric matrices with ℝ^m and K={M⪰0}. 
   U≽_K V means U−V is PSD. A matrix-valued F(x) is PSD-convex if  
       F(λx+(1−λ)y) ⪯ λF(x)+(1−λ)F(y).

--------------------------------
Key Properties  
- Nonnegative weighted sums: αf+βg is K-convex for α,β≥0.  
- Pointwise limits: limit of K-convex functions is K-convex.  
- Affine precomposition: f∘A is K-convex if f is K-convex and A is affine.

Geometric Interpretation  
Under generalized inequality, the “graph” {(x,f(x))} lies below each chord when measured in the cone K. Any segment between (x,f(x)) and (y,f(y)) remains within {(x,t): t≽_K f(x)}.

--------------------------------
Why It Matters  
- Multiobjective optimization (Pareto-convexity with K=ℝᵐ₊)  
- Matrix-valued approximations and robust control using PSD-convexity  
- Cone programming and generalized duality (constraints of the form Ax−b ∈ K)

================================================================================

'''