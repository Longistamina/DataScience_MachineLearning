# https://www.youtube.com/watch?v=SHJuGASZwlE&list=PL-DDW8QIRjNOVxrU2efygBw0xADVOgpmw&index=2

'''
#---------------------------------------------------------#
#--------------------- Introduction ----------------------#
#---------------------------------------------------------#

Convex optimization is a branch of mathematical optimization focused on minimizing convex functions over convex sets. 
The core idea is that both the objective function and the feasible region (defined by constraints) are convex, 
which ensures that any local minimum is also a global minimum, making these problems efficiently solvable.

Core Ideas of Convex Optimization

- Convex Objective Function: A function f(x) is convex if, for any two points x and y in its domain and any λ in [0,1], 
it satisfies:
                 f(λx + (1−λ)y) ≤ λf(x) + (1−λ)f(y).
  This property guarantees no local minima other than the global minimum.

- Convex Feasible Set: The set of points satisfying the problem’s constraints is convex, 
meaning any weighted average of two feasible points is also feasible. 
Constraints can be inequalities involving convex functions or affine equalities.

- Standard Form: A convex optimization problem typically has the form:
  minimize f(x)
  subject to g_i(x) ≤ 0, i=1,...,m
             h_j(x) = 0, j=1,...,p,
  where f and g_i are convex functions and h_j are affine functions.

- Algorithms: Efficient algorithms exist such as interior-point methods, Newton’s method, gradient descent, and subgradient methods. 
Interior-point methods are widely used for constrained problems and can handle large-scale problems effectively.


#--------------------------------------------------------------------------#
#----------------- Applications of Convex Optimization --------------------#
#--------------------------------------------------------------------------#

Convex optimization is widely applied across many fields due to its tractability and strong theoretical guarantees:

- Machine Learning: Convex loss functions (e.g., mean squared error, logistic loss) ensure stable training with unique global optima. Regularization techniques like Lasso (ℓ1) and Ridge (ℓ2) add convex penalties to control model complexity. Support Vector Machines (SVMs) use convex quadratic optimization to find maximum margin classifiers.

- Finance: Portfolio optimization problems, where the goal is to maximize returns subject to risk constraints, can be formulated as convex problems, enabling efficient and reliable solutions.

- Engineering and Control: Convex optimization is used in robust control design to ensure system stability despite uncertainties, often via Linear Matrix Inequalities (LMIs). Signal processing filter design and network flow optimization also rely on convex formulations to improve performance and resource utilization.

- Large-Scale and Real-Time Systems: Convex optimization methods scale from embedded real-time applications, where solvers execute in milliseconds, to large-scale distributed optimization coordinating many solvers for massive problems.

In summary, convex optimization leverages the mathematical properties of convex functions and sets to solve a broad class of optimization problems efficiently and reliably, underpinning advances in machine learning, finance, engineering, and beyond.

'''