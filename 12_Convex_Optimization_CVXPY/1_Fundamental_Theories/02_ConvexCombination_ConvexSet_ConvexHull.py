    # https://www.youtube.com/watch?v=QV5qtTq1Tro&list=PL-DDW8QIRjNOVxrU2efygBw0xADVOgpmw&index=2

'''
#----------------------------------------------------------------#
#------------------------ CONVEX SET ----------------------------#
#----------------------------------------------------------------#

A convex set is a subset where, for any two points in the set, 
the entire line segment connecting them is also contained within the set.

Example: A solid triangle is a convex set. 
         If you pick any two points inside or on the triangle, 
         the entire line segment between them will also be inside or on the triangle.
         ("on the triangle" means that line overlap one of the triangle sides)

#### Mathematical definition:

Let S be a vector space over ℝ. A subset C ⊆ S is convex if:
        ∀ x,y ∈ C, ∀ t ∈ [0,1]: (1-t)x + ty ∈ C

Alternative formulation:
A set C is convex if for any two points x,y ∈ C, the line segment connecting them lies entirely within C.


#------------------------------------------------------------------------#
#------------------------ CONVEX COMBINATION ----------------------------#
#------------------------------------------------------------------------#

A convex combination is a linear combination of points where all coefficients are non-negative and sum to 1. 
More formally, given points x₁, x₂, ..., xₙ, a convex combination is:
        
                α₁x₁ + α₂x₂ + ... + αₙxₙ

        where αᵢ ≥ 0 and α₁ + α₂ + ... + αₙ = 1.

        (so convex combination is actually affine combination but with αᵢ ≥ 0)

Example: Consider two points A = (1, 2) and B = (5, 6). 
         A convex combination would be 0.3A + 0.7B = 0.3(1,2) + 0.7(5,6) = (3.8, 4.8). 
         This point lies on the line segment between A and B.
         

#-----------------------------------------------------------------#
#------------------------ CONVEX HULL ----------------------------#
#-----------------------------------------------------------------#

The convex hull is the smallest convex set that contains a given set of points.

Example: Consider four points forming corners of a square with one additional point inside. 
         The convex hull would be the original square.

#### Mathematical definition

Given a set X, the convex hull conv(X) is defined as:

1. Minimal Definition:
   conv(X) = smallest convex set containing X

2. Intersection Definition:
   conv(X) = ⋂{C : C is convex and X ⊆ C}

3. Convex Combinations Definition:
   conv(X) = {∑ᵢ₌₁ⁿ λᵢxᵢ : n ∈ ℕ, xᵢ ∈ X, λᵢ ≥ 0, ∑ᵢ₌₁ⁿ λᵢ = 1}

So, convex hull is the outcome of convexifying a given set X

If set X is already a convex set, then conv(X) = X

KEY PROPERTIES:
- Convex hulls are always convex sets
- For finite point sets: conv(X) is a polytope (polytope = hinh da dien)
- Computational complexity: O(n log n) in 2D, O(n log h) output-sensitive
'''
