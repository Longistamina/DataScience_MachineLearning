'''
# Supporting Hyperplane Theorem

The supporting hyperplane theorem is another fundamental result in convex analysis 
that complements the separation hyperplane theorem discussed earlier. 

While the separation theorem deals with separating disjoint convex sets, 
the supporting hyperplane theorem focuses on the relationship 
between a convex set and hyperplanes that "support" it at boundary points.

## Fundamental Statement

The supporting hyperplane theorem states that for any convex set C in n-dimensional Euclidean space ℝⁿ 
and any boundary point x₀ ∈ ∂C, there exists a supporting hyperplane H containing x₀ such that 
the entire convex set C lies on one side of H.

Formally, there exists a nonzero vector a and a real number b such that:

⟨a, x₀⟩ = b
⟨a, x⟩ ≤ b for all x ∈ C

The hyperplane H = {x : ⟨a, x⟩ = b} is called a supporting hyperplane of C at x₀.

## Definition of Supporting Hyperplane

A supporting hyperplane of a set S in Euclidean space ℝⁿ is a hyperplane that satisfies two key properties:

1. **Containment Property**: S is entirely contained in one of the two closed half-spaces bounded by the hyperplane
2. **Contact Property**: S has at least one boundary point on the hyperplane

The supporting hyperplane "touches" the convex set at the boundary point 
without cutting through the interior of the set.

## Geometric Interpretation

Geometrically, the supporting hyperplane theorem provides a powerful characterization of convex sets. 
At any boundary point of a convex set, there exists at least one "flat" surface (hyperplane) 
that touches the set at that point while keeping the entire set on one side of the surface.

This geometric property reflects the "smoothness" of convex sets in the sense that 
they have no "inward-pointing corners" or concave portions that would prevent the existence of such supporting hyperplanes.

## Relationship to Separation Theorem

The supporting hyperplane theorem can be viewed as a special case of the separation hyperplane theorem. 
Specifically, it separates a single point (the boundary point) from the interior of the convex set.

The connection becomes evident when we consider that if x₀ is a boundary point of C, then x₀ and the interior of C are disjoint. 
The separation theorem then guarantees the existence of a hyperplane separating these, which becomes the supporting hyperplane.

## Proof Strategy

The standard proof of the supporting hyperplane theorem employs several key techniques:

**Step 1: Sequence Construction**: For a boundary point x₀, 
                                   construct a sequence {xₙ} of points outside the closure of C that converges to x₀.

**Step 2: Projection Analysis**: For each xₙ, find its projection onto the closed convex set C, denoted as yₙ. 
                                 Define the unit vector aₙ = (xₙ - yₙ)/||xₙ - yₙ||.

**Step 3: Separation Property**: The projection theorem guarantees that ⟨aₙ, y⟩ ≤ ⟨aₙ, yₙ⟩ < ⟨aₙ, xₙ⟩ for all y ∈ C.

**Step 4: Limit Process**: Since {aₙ} lies on the unit sphere (compact set), it has a convergent subsequence. 
                           Taking the limit gives the desired supporting hyperplane.

## Uniqueness and Multiplicity

Unlike the separation theorem, the supporting hyperplane at a given boundary point is not necessarily unique. 
A convex set can have multiple supporting hyperplanes at the same boundary point, particularly at "corners" or vertices of the set.

**Unique Supporting Hyperplane**: When the convex set is strictly convex, 
                                  the supporting hyperplane at each boundary point is unique. 
                                  This occurs when the boundary is "smooth" without any flat portions or corners.

**Multiple Supporting Hyperplanes**: 
At vertices or along flat faces of polytopes, 
there can be infinitely many supporting hyperplanes passing through the same boundary point.

## Converse Theorem

The supporting hyperplane theorem has a significant converse that provides a characterization of convex sets:

**Converse Supporting Hyperplane Theorem**: 
If a set S is closed, has nonempty interior, 
and has a supporting hyperplane at every point of its boundary, then S is convex.

This converse is particularly important because it provides a geometric criterion for convexity. 
The proof typically shows that if S satisfies these conditions but is not convex, 
then there would exist a line segment with endpoints in S that passes outside S, 
contradicting the supporting hyperplane property at some boundary point.

## Applications in Optimization

**Characterization of Convex Sets**: Every nonempty closed convex set can be represented 
                                     as the intersection of all its supporting half-spaces. 
                                     This provides the fundamental connection between convex sets and linear inequalities.

**Optimality Conditions**: In convex optimization, the supporting hyperplane theorem underlies the development of optimality conditions. 
                            At an optimal point on the boundary of the feasible region, the gradient of the objective function 
                            must be a normal vector to a supporting hyperplane.

**Farkas' Lemma**: The supporting hyperplane theorem provides an alternative route to proving Farkas' lemma, 
                   which is fundamental to linear programming duality theory.

**Mixed-Integer Programming**: The Extended Supporting Hyperplane (ESH) algorithm uses supporting hyperplanes 
                               to generate tight polyhedral approximations of convex feasible regions in mixed-integer nonlinear programming.

## Normal Cones and Subdifferentials

The supporting hyperplane theorem is intimately connected to the concept of normal cones 
and subdifferentials in convex analysis:

**Normal Cone**: At a boundary point x₀ of a convex set C, the normal cone NC(x₀) consists of all vectors 
                 that are normal to supporting hyperplanes at x₀. When the supporting hyperplane is unique, 
                 the normal cone reduces to a ray.

**Subdifferential Connection**: For a convex function f, the subdifferential ∂f(x₀) at a point x₀ consists of all vectors 
                                that define supporting hyperplanes to the epigraph of f at (x₀, f(x₀)).

## Extensions and Generalizations

**Infinite-Dimensional Spaces**: The Hahn-Banach separation theorem extends the supporting hyperplane theorem to infinite-dimensional topological vector spaces, requiring continuous linear functionals instead of simple inner products.

**Non-Convex Extensions**: Recent research has shown that supporting hyperplane results can be extended 
                           to certain non-convex sets when viewed from specific perspective points, 
                           opening new avenues for analysis of non-convex optimization problems.

**Manifold Generalizations**: The theorem can be generalized to convex sets on Riemannian manifolds using tangent spaces and geodesics, 
                              providing tools for optimization on curved spaces.

## Computational Aspects

**Supporting Hyperplane Algorithms**: Computational methods for finding supporting hyperplanes 
                                      include gradient-based approaches for smooth convex sets 
                                      and subgradient methods for non-smooth cases.

**Polyhedral Approximation**: Supporting hyperplanes provide the foundation for polyhedral approximation methods, 
                              where complex convex sets are approximated by the intersection 
                              of finitely many supporting half-spaces.

**Numerical Stability**: Computing supporting hyperplanes numerically requires careful attention to conditioning 
                         and stability, particularly near points where multiple supporting hyperplanes exist.

## Significance in Convex Analysis

The supporting hyperplane theorem serves as a bridge between the geometric properties of convex sets 
and the algebraic tools of linear programming and optimization. 
It provides the theoretical foundation for understanding how convex sets can be characterized by linear inequalities 
and how optimization problems over convex sets can be solved efficiently.

The theorem's importance extends beyond pure mathematics into practical applications 
wherever convex optimization appears, from machine learning algorithms like support vector machines 
to economic equilibrium models and engineering design problems. 

Its geometric intuition makes it one of the most accessible yet powerful results in convex analysis, 
providing both theoretical insight and practical computational tools for dealing with convex optimization problems.
'''