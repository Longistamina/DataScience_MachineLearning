# https://www.youtube.com/watch?v=QV5qtTq1Tro&list=PL-DDW8QIRjNOVxrU2efygBw0xADVOgpmw&index=2

'''
#-------------------------------------------------------------------------------#
#--------------- Conic Combination - Convex Cone - Conic Hull ------------------#
#-------------------------------------------------------------------------------#

##### CONIC COMBINATION #####
A conic combination (also called conical combination) of vectors x₁, x₂, ..., xₙ is:
λ₁x₁ + λ₂x₂ + ... + λₙxₙ
where all coefficients λᵢ ≥ 0

Key difference from convex combinations:
- Convex: λᵢ ≥ 0 AND Σλᵢ = 1
- Conic: λᵢ ≥ 0 (no sum constraint)

##### CONVEX CONE #####
A convex cone is a subset C satisfying:
1. Cone property: x ∈ C ⟹ λx ∈ C for all λ ≥ 0
2. Convexity: x,y ∈ C ⟹ αx + βy ∈ C for all α,β ≥ 0

Mathematical formulation:
For any x,y ∈ C and non-negative scalars α,β:
αx + βy ∈ C

Alternative characterization:
C is convex cone ⟺ C + C ⊆ C

#### CONIC HULL ####
The conic hull of set S:
cone(S) = {Σλᵢxᵢ : xᵢ ∈ S, λᵢ ≥ 0}
= smallest convex cone containing S

#### KEY RELATIONSHIP ####
Convex cones contain all conic combinations of their elements.
They extend convex hull concepts to unbounded sets.
'''

###############################################################

'''
#---------------------------------------------------------------#
#----------------------- Hyperplane ----------------------------#
#---------------------------------------------------------------#

#### DEFINITION ####
Hyperplane in ℝⁿ: H = {x ∈ ℝⁿ : pᵀx = α}
where p ∈ ℝⁿ (nonzero normal vector), α ∈ ℝ (scalar)

#### CONVEXITY PROOF ####
For X,Y ∈ H and λ ∈ [0,1]:
1. X ∈ H ⟹ a₁x₁ + ... + aₙxₙ = c
2. Y ∈ H ⟹ a₁y₁ + ... + aₙyₙ = c
3. λX + (1-λ)Y = (λx₁+(1-λ)y₁, ..., λxₙ+(1-λ)yₙ)
4. a₁[λx₁+(1-λ)y₁] + ... + aₙ[λxₙ+(1-λ)yₙ] = λc + (1-λ)c = c
5. Therefore: λX + (1-λ)Y ∈ H ✓

#### HALF-SPACE RELATIONSHIP ####
H⁺ = {x : pᵀx ≥ α} (upper half-space)
H⁻ = {x : pᵀx ≤ α} (lower half-space)
H = H⁺ ∩ H⁻ (hyperplane as intersection)

#### KEY PROPERTIES ####
- Hyperplanes are convex sets
- Intersection of convex sets is convex
- Half-spaces are convex
- Hyperplanes separate space into two regions

#### GEOMETRIC INTERPRETATION ####
H = pᵀx = α is translation of subspace pᵀx = 0
In 2D: hyperplane = line
In 3D: hyperplane = plane
'''

#######################################################

'''
#----------------------------------------------#
#------------- Euclidian Ball -----------------#
#----------------------------------------------#

#### DEFINITION ####
Closed ball: B(xc, r) = {x ∈ ℝⁿ : ‖x - xc‖₂ ≤ r}
Open ball: B(xc, r) = {x ∈ ℝⁿ : ‖x - xc‖₂ < r}
where xc = center, r > 0 = radius, ‖·‖₂ = Euclidean norm

#### CONVEXITY PROOF ####
Given: x₁, x₂ ∈ B(xc, r) and θ ∈ [0,1]
To prove: x = θx₁ + (1-θ)x₂ ∈ B(xc, r)

Step 1: ‖x₁ - xc‖₂ ≤ r and ‖x₂ - xc‖₂ ≤ r (given)

Step 2: Apply triangle inequality (‖x + y‖ ≤ ‖x‖ + ‖y‖)
‖x - xc‖₂ = ‖θx₁ + (1-θ)x₂ - xc‖₂
          = ‖θ(x₁ - xc) + (1-θ)(x₂ - xc)‖₂
          ≤ θ‖x₁ - xc‖₂ + (1-θ)‖x₂ - xc‖₂
          ≤ θr + (1-θ)r = r

Step 3: Therefore x ∈ B(xc, r) ✓

#### KEY PROPERTIES ####
- All Euclidean balls (open and closed) are convex
- 2D: ball = disk (circle)
- 3D: ball = solid sphere
- Convexity preserved under translation
- Line segments between any two points stay within ball
'''

#####################################################################

'''
#-----------------------------------------------------------#
#---------------------- Elipsoid ---------------------------#
#-----------------------------------------------------------#

Real symmetric matrix A is positive definite if:
    x^T A x > 0 for all nonzero x ∈ ℝⁿ

#### ELIPSOID DEFINITION ####
Standard form: E = {x ∈ ℝⁿ : (x-xc)ᵀP⁻¹(x-xc) ≤ 1}
where xc = center, P ≻ 0 (positive definite matrix)

Mahalanobis norm form: E(xc) = {x ∈ ℝⁿ : ‖x-xc‖²P ≤ 1}
where ‖x‖²P = xᵀPx (Mahalanobis norm squared)

Affine transformation: E = A·B + b
where B = unit ball, A invertible matrix, b ∈ ℝⁿ

#### CONVEXITY PROOF ####
For y₁, y₂ ∈ E(xc) and α ∈ [0,1]:
‖αy₁ + (1-α)y₂ - xc‖P = ‖α(y₁-xc) + (1-α)(y₂-xc)‖P
                        ≤ α‖y₁-xc‖P + (1-α)‖y₂-xc‖P
                        ≤ α·1 + (1-α)·1 = 1

Therefore: αy₁ + (1-α)y₂ ∈ E(xc) ✓

#### KEY PROPERTIES ####
- Ellipsoids are convex sets
- Image of unit ball under affine transformation
- Semi-axis lengths: 1/√λᵢ (eigenvalues of defining matrix)
- Volume: Vol(E) = √det(A⁻¹) for E = {x : xᵀAx ≤ 1}
- 2D: ellipse, 3D: ellipsoid (solid)

#### MAHALANOBIS NORM PROPERTIES ####
‖x‖²P = xᵀPx where P ≻ 0
Satisfies triangle inequality: ‖x+y‖P ≤ ‖x‖P + ‖y‖P
Essential for proving ellipsoid convexity
'''