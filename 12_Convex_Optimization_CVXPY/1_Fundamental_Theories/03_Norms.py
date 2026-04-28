'''
NORM AND ITS RELATIONSHIP TO CONVEX SETS

NORM DEFINITION
Function ‖·‖: X → ℝ satisfying three properties:
1. Positive definiteness: ‖x‖ = 0 ⟺ x = 0
2. Absolute homogeneity: ‖αx‖ = |α|‖x‖ for all scalars α
3. Triangle inequality: ‖x + y‖ ≤ ‖x‖ + ‖y‖ for all x,y

COMMON NORMS
- Euclidean (ℓ₂): ‖x‖₂ = √(x₁² + ... + xₙ²)
- p-norm: ‖x‖ₚ = (∑|xᵢ|ᵖ)^(1/p) for p ≥ 1
- Maximum (ℓ∞): ‖x‖∞ = max|xᵢ|

NORM BALLS ARE CONVEX
Norm ball: B(xc, r) = {x : ‖x - xc‖ ≤ r}

Proof of convexity:
For x,y ∈ B(xc, r) and λ ∈ [0,1]:
‖λx + (1-λ)y - xc‖ = ‖λ(x-xc) + (1-λ)(y-xc)‖
                    ≤ λ‖x-xc‖ + (1-λ)‖y-xc‖    (triangle inequality)
                    ≤ λr + (1-λ)r = r           (x,y in ball)

KEY RELATIONSHIPS
- Every norm is a convex function
- Unit balls define the "shape" of different norms
- Ellipsoids are norm balls for Mahalanobis norms
- All norms in finite dimensions are equivalent
'''

################################################

'''
#-------------------------------------------------------#
#------------ P-NORM AND MAXIMUM NORM ------------------#
#-------------------------------------------------------#

#### P-NORM DEFINITION ####
The p-norm (also called ℓᵖ-norm or Minkowski norm) of vector x = (x₁, x₂, ..., xₙ) is defined as
            
            ‖x‖ₚ = (∑ᵢ₌₁ⁿ |xᵢ|ᵖ)^(1/p) where p ≥ 1

This generalizes the concept of distance and provides a family of norms by varying the value of p

SPECIAL CASES
p = 1 (Taxicab): ‖x‖₁ = ∑|xᵢ|     => This represents the distance a taxi would travel in a city with horizontal and vertical movements
p = 2 (Euclidean): ‖x‖₂ = √(∑xᵢ²) => This is the standard Euclidean distance derived from the Pythagorean theorem
p = ∞ (Maximum): ‖x‖∞ = max|xᵢ|   => Maximum norm

#### MAXIMUM NORM (L∞-NORM) ####
The maximum norm (also called infinity norm or L∞-norm) is defined as the limit case when p approaches infinity
                    
                      ‖x‖∞ = max₁≤ᵢ≤ₙ |xᵢ|

              Limiting case: lim(p→∞) ‖x‖ₚ = ‖x‖∞
              => This simplifies to the absolute value of the largest component in the vector

UNIT BALL SHAPES
p = 1: Diamond/rhombus
p = 2: Circle (2D), sphere (3D)
p = ∞: Square (2D), cube (3D)

#### KEY PROPERTIES ####
L₂-norm:
- Most common in ML
- Not robust to outliers
- Squares components (amplifies large, shrinks small)
- Used in ridge regression

L∞-norm:
- Computationally simple
- Robust to outliers
- Emphasizes worst-case component

#### NORM EQUIVALENCE ####
All p-norms equivalent in finite dimensions
Define same topology on ℝⁿ

#### P=0 CASE ####
‖x‖₀ = number of non-zero components
Not technically a norm (fails homogeneity)
Useful for measuring sparsity

'''