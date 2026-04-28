'''
4.3 Prove that x* = (1, 1/2, -1) is optimal for the optimization problem

minimize    (1/2) xᵀPx + qᵀx + r
subject to  -1 ≤ xᵢ ≤ 1,   i = 1, 2, 3,

where

P = [ 13   12   -2
      12   17    6
      -2    6   12 ]  

q = [ -22.0 -14.5 13.0 ]

r = 1.
'''

import cvxpy as cp
import numpy as np

print(cp.installed_solvers())
# ['CLARABEL', 'OSQP', 'SCIPY', 'SCS']

'''
CVXPY offers various solvers to solve the problem. 

Checkout this link for more information:
https://www.cvxpy.org/tutorial/solvers/index.html
'''

#--------------------
## Define variable
#--------------------

x = cp.Variable(name = "x", shape = (3,1))

#--------------------
## Define constants
#--------------------

P = cp.Constant(
    name = "P",
    value = np.array([
        [13, 12, -2],
        [12, 17, 6],
        [-2, 6, 12]
    ])
)
'''Here in QP, the P matrix must be a PSD (can use np.linalg.eigvals(P.value) to check)'''
print(P.value)
# [[13. 12. -2.]
#  [12. 17.  6.]
#  [-2.  6. 12.]]

q = cp.Constant(
    name = "q",
    value = np.array([-22, -14.5, 13])
)
print(q.value)
# [-22.  -14.5  13. ]

r = cp.Constant(name = "r", value = 1)
print(r.value)
# 1.0

#--------------------
## Define problem and solve
#--------------------

problem = cp.Problem(
    objective = cp.Minimize(0.5*cp.quad_form(x, P) + q.T@x + r), # Must use cp.quad_form() instead of x.T@P@x to achieve DCP
    constraints = [
        x <= 1,
        -x <= 1 # x >= -1
    ]

)

problem.solve(solver = 'CLARABEL') # Solve problem using CLARABEL solver

print(
    (
        f"Status: {problem.status}\n"
        f"Optimal Value: {problem.value}\n"
        f"Optimal variables: {x.value.flatten()}" # Use .flatten() to convert 2D array to 1D for better readability
    )
)
# Status: optimal
# Optimal Value: -21.62499998049554
# Optimal variables: [ 0.99999999  0.50000001 -1.        ]