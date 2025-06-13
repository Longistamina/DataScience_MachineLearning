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

'''