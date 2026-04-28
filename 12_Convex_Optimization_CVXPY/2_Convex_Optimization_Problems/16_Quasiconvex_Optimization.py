"""
======================================================================
QUASICONVEX OPTIMIZATION VIA CONVEX FEASIBILITY PROBLEMS
======================================================================

Problem formulation:
minimize    f0(x)
subject to  fi(x) ≤ 0,  i = 1,...,m
            A x = b
with f0 quasiconvex and fi convex

Note: Quasiconvex problems can have local minima that are not global.

======================================================================
1. CONVEX REPRESENTATION OF SUBLEVEL SETS
======================================================================

For each t, define φ_t(x) convex in x such that
    f0(x) ≤ t   ⟷   φ_t(x) ≤ 0

Example:
    f0(x) = p(x) / q(x)
    where p is convex, q is concave, p(x) ≥ 0, q(x) > 0 on dom f0
Choose φ_t(x) = p(x) – t q(x)
    for t ≥ 0, φ_t is convex
    and p(x)/q(x) ≤ t if and only if φ_t(x) ≤ 0

======================================================================
2. QUASICONVEX OPTIMIZATION AS CONVEX FEASIBILITY
======================================================================

For fixed t, solve the convex feasibility problem in x:
    φ_t(x) ≤ 0
    fi(x) ≤ 0,  i = 1,...,m
    A x = b
If feasible, then t ≥ p* (optimal value)
If infeasible, then t ≤ p*

======================================================================
3. BISECTION METHOD FOR QUASICONVEX OPTIMIZATION
======================================================================

Given initial bounds l ≤ p* ≤ u and tolerance ε > 0:
repeat:
    t = (l + u) / 2
    solve feasibility problem for t
    if feasible:
        u = t
    else:
        l = t
until u – l ≤ ε

This requires exactly ceil(log2((u – l)/ε)) iterations.

Short explanation:  
Transform the quasiconvex minimization into a sequence of convex feasibility checks by bisection on the objective bound t.  
"""
