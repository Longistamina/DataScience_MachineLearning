'''
#--------------------------------------------------------------#
#-------------------- Affine Combination ----------------------#
#--------------------------------------------------------------#

An affine combination of vectors x₁, x₂, ..., xₙ is a linear combination

              x =  α₁x₁ + α₂x₂ + ... + αₙxₙ

        where the coefficients αᵢ satisfy: ∑ αᵢ = 1.

The coefficients can be positive or negative, but must sum to one. 
This represents a weighted average that may extend beyond the convex hull of the points.

Example:
For points v₁ and v₂:
            
            v = 0.5 v₁ + 0.5 v₂,

            the midpoint is an affine combination, since 0.5 + 0.5 = 1.

Another example: v = 2 v₁ - v₂, since 2 + (-1) = 1.

#-------------------------------------------#
#--------------- Affine Set ----------------#
#-------------------------------------------#

An affine set is a subset of a vector space that contains every affine combination of its points. 
Specifically, a set A is affine if, for any finite collection of points x₁, x₂, ..., xₙ 
in A and any scalars a₁, a₂, ..., aₙ whose sum equals 1,

                    a₁ + a₂ + ⋯ + aₙ = 1,

the point x formed by the affine combination

                  x =  a₁ x₁ + a₂ x₂ + ⋯ + aₙ xₙ

also lies in A.


####### Example: prove a set is an affine set
        
        The set C = { (x, y) ∈ ℝ² | y = 2x + 1 } is affine.
Proof:
        Take p₁ = (x₁, 2x₁ + 1), p₂ = (x₂, 2x₂ + 1) in C.
For any θ,
p = θ p₁ + (1 - θ) p₂
  = (θ x₁ + (1 - θ) x₂, θ(2x₁ + 1) + (1 - θ)(2x₂ + 1))
  = (x, 2x + 1),

  where x = θ x₁ + (1 - θ) x₂.

Thus, p ∈ C, so C is affine.

######## Counterexample: prove a set is not an affine set
    
    D = { (x, y) | y = x² } is not affine.

Take p₁ = (1, 1), p₂ = (-1, 1) in D.

For θ = 0.5,
    p = 0.5 p₁ + 0.5 p₂ = (0, 1),

    but y = x² at x=0 is 0, not 1, so p ∉ D.

Hence, D is not affine.


#----------------------------------------------------#
#-------------------- Summary -----------------------#
#----------------------------------------------------#

- Affine combination: linear combination with coefficients summing to 1.
- Affine set: closed under affine combinations (contains the entire line through any two points).
- Example affine set: line y = 2x + 1.
- Example non-affine set: parabola y = x².
'''