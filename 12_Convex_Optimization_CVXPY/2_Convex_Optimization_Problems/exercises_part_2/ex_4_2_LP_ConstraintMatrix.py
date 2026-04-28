'''
4.2 "Hello World" in CVXPY. 
Use CVXPY to verify the optimal values you obtained (analytically) for exercise 4.1 in Convex Optimization.

==================================

4.1 Consider the optimization problem

minimize    f₀(x₁, x₂)
subject to  2x₁ + x₂ ≥ 1
            x₁ + 3x₂ ≥ 1
            x₁ ≥ 0,    
            x₂ ≥ 0.

Make a sketch of the feasible set. For each of the following objective functions, 
give the optimal set and the optimal value.

(a) f₀(x₁, x₂) = x₁ + x₂.
(b) f₀(x₁, x₂) = -x₁ - x₂.
(c) f₀(x₁, x₂) = x₁.
(d) f₀(x₁, x₂) = max{x₁, x₂}.
(e) f₀(x₁, x₂) = x₁² + 9x₂².
'''

import cvxpy as cp
import numpy as np

#--------------------------------
## Define the variables
#--------------------------------

x1 = cp.Variable(name = "x1")
x2 = cp.Variable(name = "x2")

#--------------------------------
## Define the constraints
#--------------------------------

# Normal way
opt_constraints = [
    -2*x1 - x2 <= -1, # 2x₁ + x₂ ≥ 1
    -x1 - 3*x2 <= -1, # x₁ + 3x₂ ≥ 1
    -x1 <= 0, # x₁ ≥ 0
    -x2 <= 0  # x₂ ≥ 0
]

# Matrix way
left_side = np.array([[-2, -1], # 4x2
                      [-1, -3],
                      [-1, 0],
                      [0, -1]])

variable_vector = cp.vstack([x1, x2]) # 2x1

right_side = [-1, -1, 0, 0]

opt_constraints_matrix = [
    left_side[i, :] @ variable_vector <= right_side[i]
    for i, _ in enumerate(right_side)
]


#-----------------------------------
## (a) f₀(x₁, x₂) = x₁ + x₂.
#-----------------------------------

# Define objective
objective_a = cp.Minimize(x1 + x2)

# Define problem: objective + constraints
problem_a = cp.Problem(
    objective = objective_a,
    constraints = opt_constraints
)

# Solve the problem
problem_a.solve()

print(
    (
        f"Status: {problem_a.status}\n"
        f"Optimal Value: {problem_a.value}\n"
        f"Optimal variables: {x1.value, x2.value}"
    )
)
# Status: optimal
# Optimal Value: 0.6000000001640435
# Optimal variables: (array(0.4), array(0.2))


''''''''''''''''''''''''''''''''''''
''' Try with constraints matrix '''
''''''''''''''''''''''''''''''''''''

objective_a = cp.Minimize(x1 + x2)

problem_a_matrix = cp.Problem(
    objective = objective_a,
    constraints = opt_constraints_matrix
)

problem_a_matrix.solve()

print(
    (
        f"Status: {problem_a_matrix.status}\n"
        f"Optimal Value: {problem_a_matrix.value}\n"
        f"Optimal variables: {x1.value, x2.value}"
    )
)
# Status: optimal
# Optimal Value: 0.6000000001640435
# Optimal variables: (array(0.4), array(0.2))


#-----------------------------------
## (b) f₀(x₁, x₂) = -x₁ - x₂.
#-----------------------------------

objective_b = cp.Minimize(-x1 - x2)

problem_b = cp.Problem(
    objective = objective_b,
    constraints = opt_constraints
)

problem_b.solve()

print(
    (
        f"Status: {problem_b.status}\n"
        f"Optimal Value: {problem_b.value}\n"
        f"Optimal variables: {x1.value, x2.value}"
    )
)
# Status: unbounded
# Optimal Value: -inf
# Optimal variables: (None, None)


#-----------------------------------
## (c) f₀(x₁, x₂) = x₁.
#-----------------------------------

objective_c = cp.Minimize(x1)

problem_c = cp.Problem(
    objective = objective_c,
    constraints = opt_constraints
)

problem_c.solve()

print(
    (
        f"Status: {problem_c.status}\n"
        f"Optimal Value: {problem_c.value}\n"
        f"Optimal variables: {x1.value, x2.value}"
    )
)
# Status: optimal
# Optimal Value: -1.95729336465049e-11
# Optimal variables: (array(-1.95729336e-11), array(1.69159744))


#-----------------------------------
## (d) f₀(x₁, x₂) = max{x₁, x₂}.
#-----------------------------------

objective_d = cp.Minimize(cp.max([x1, x2])) # NOT cp.max(x1, x2) because cp.max() takes one argument only
                                            # or can use cp.maximum(x1, x2)

problem_d = cp.Problem(
    objective = objective_d,
    constraints = opt_constraints
)

problem_d.solve()

print(
    (
        f"Status: {problem_d.status}\n"
        f"Optimal Value: {problem_d.value}\n"
        f"Optimal variables: {x1.value, x2.value}"
    )
)
# Status: optimal
# Optimal Value: 0.3333333337083394
# Optimal variables: (array(0.33333333), array(0.33333333))


#-----------------------------------
## (e) f₀(x₁, x₂) = x₁² + 9x₂².
#-----------------------------------

objective_e = cp.Minimize(x1**2 + 9*(x2**2))

problem_e = cp.Problem(
    objective = objective_e,
    constraints = opt_constraints
)

problem_e.solve()

print(
    (
        f"Status: {problem_e.status}\n"
        f"Optimal Value: {problem_e.value}\n"
        f"Optimal variables: {x1.value, x2.value}"
    )
)
# Status: optimal
# Optimal Value: 0.5000000000000002
# Optimal variables: (array(0.5), array(0.16666667))