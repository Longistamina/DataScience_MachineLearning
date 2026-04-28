'''
4.3 Formulating constraints in CVXPY. Below we give several convex constraints on scalar variables x, y, and z. 
Express each one as a set of DCP compliant constraints in CVXPY. 

To check DCP compliance, use the .is_DCP() method on each constraint.

(a) 1/x + 1/y ≤ 1,  x ≥ 0,  y ≥ 0.

(b) xy ≥ 1,  x ≥ 0,  y ≥ 0.

(c) (x + y)² / √y ≤ x - y + 5  (with implicit constraint y ≥ 0).

(d) x + z ≤ 1 + √(xy - z²),  x ≥ 0,  y ≥ 0.  Hint.  √(xy - z²) = √( y(x - z²/y) ).
'''

# Disciplined convex programming (DCP) is a system for constructing mathematical expressions 
# with known curvature from a given library of base functions
# CVXPY uses DCP to ensure that the specified optimization problems are convex.

# Visit dcp.stanford.edu for a more interactive introduction to DCP.
# (read https://dcp.stanford.edu/rules first, then do the quizz)

'''
PURPOSE of this exercise: Learn how to formulate a True DCP constraints
Because only when all constraints are DCP, the problem is solvable
'''

import cvxpy as cp

x = cp.Variable(name = "x")
y = cp.Variable(name = "y")
z = cp.Variable(name = "z")


#--------------------------
## (a) 1/x + 1/y ≤ 1,  x ≥ 0,  y ≥ 0.
#--------------------------

constraints_a = [
    cp.power(x, -1) + cp.power(y, -1) <= 1, # set 1/x + 1/y then the is_DCP() will return False
    -x <= 0, # x ≥ 0
    -y <= 0, # y ≥ 0
]

for constraint in constraints_a:
    print(f"{constraint} ___ {constraint.is_dcp()} DCP")
# power(x, -1.0) + power(y, -1.0) <= 1.0 ___ True DCP
# -x <= 0.0 ___ True DCP
# -y <= 0.0 ___ True DCP


#--------------------------
## (b) xy ≥ 1,  x ≥ 0,  y ≥ 0.
#--------------------------

constraints_b = [
    -cp.log(x) - cp.log(y) <= 0, # xy ≥ 1 (only when x and y are positive)
    -x <= 0,
    -y <= 0
]

for constraint in constraints_b:
    print(f"{constraint} ___ {constraint.is_dcp()} DCP")
# -log(x) + -log(y) <= 0.0 ___ True DCP
# -x <= 0.0 ___ True DCP
# -y <= 0.0 ___ True DCP


#--------------------------
## (c) (x + y)² / √y ≤ x - y + 5  (with implicit constraint y ≥ 0)
#--------------------------

'''
(x + y)² / √y ≤ x - y + 5

Since (x + y)² and √y are non-negative
We can deduce that (x - y + 5) must also non-negative (because (x - y + 5) is greater than a non-negative number)

<=> (x + y)² / (x - y + 5) ≤ √y

<=> (x + y)² / (x - y + 5) - √y ≤ 0
'''

constraints_c = [
     cp.quad_over_lin((x + y), (x - y + 5)) - cp.sqrt(y) <= 0, # use quad_over_lin() to avoid is_dcp() == False
    -y <= 0, # implicit constraint                             # cp.quad_over_lin(x,y) represent ||x||²/y
    -x + y <= 5 # implicit constraint
]

for constraint in constraints_c:
    print(f"{constraint} ___ {constraint.is_dcp()} DCP")
# quad_over_lin(x + y, x + -y + 5.0) + -power(y, 0.5) <= 0.0 ___ True DCP
# -y <= 0.0 ___ True DCP
# -x + y <= 5.0 ___ True DCP



#--------------------------
## (d) x + z ≤ 1 + √(xy - z²),  x ≥ 0,  y ≥ 0.  
## Hint.  √(xy - z²) = √( y(x - z²/y) ).
#--------------------------

'''
x + z ≤ 1 + √(xy - z²)

<=> x + z - 1 - √(xy - z²) ≤ 0

<=> x + z - 1 - √( y(x - z²/y) ) ≤ 0 

Apply hint: √( y(x - z²/y) ) is a geometric mean between y and (x - z²/y) => concave
'''

constraints_d = [
    x + z - 1 - cp.geo_mean(cp.hstack([y, x - cp.quad_over_lin(z, y)])) <= 0, # Use cp.hstack() to combine [y, z²/y] into a CVXPY horizontal expression vector
    -x <= 0,
    -y <= 0
]

for constraint in constraints_d:
    print(f"{constraint} ___ {constraint.is_dcp()} DCP")
# x + z + -1.0 + -geo_mean(Hstack(reshape(y, (1,), F), reshape(x + -quad_over_lin(z, y), (1,), F)), (1/2, 1/2)) <= 0.0 ___ True DCP
# -x <= 0.0 ___ True DCP
# -y <= 0.0 ___ True DCP
