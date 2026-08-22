'''
scipy.optimize  —  Optimization and root finding
=================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART A — MINIMIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. minimize_scalar()         : 1-D minimization (brent / bounded / golden).
 2. minimize() — unconstrained: Nelder-Mead, Powell, CG, BFGS, L-BFGS-B,
                                Newton-CG, trust-ncg, trust-krylov, trust-exact.
 3. minimize() — constrained  : Bounds, LinearConstraint, NonlinearConstraint,
                                SLSQP, COBYLA, trust-constr.
 4. Method selection guide    : table of solver capabilities.

PART B — GLOBAL OPTIMIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 5. differential_evolution()  : stochastic population search.
 6. basinhopping()            : iterated local search with random perturbation.
 7. shgo()                    : simplicial homology global optimisation.
 8. dual_annealing()          : simulated + fast annealing hybrid.
 9. direct()                  : DIRECT: dividing rectangles.
10. brute()                   : exhaustive grid search.

PART C — LEAST-SQUARES & CURVE FITTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. least_squares()           : nonlinear least-squares with bounds and robust loss.
12. curve_fit()               : nonlinear LS wrapper for model fitting.
13. lsq_linear()              : bounded linear LS.
14. nnls()                    : non-negative linear LS.
15. isotonic_regression()     : monotone regression.

PART D — ROOT FINDING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
16. root_scalar()             : 1-D roots via brentq / bisect / newton / halley / secant / toms748.
17. root()                    : N-D root finding (hybr, lm, broyden).
18. fixed_point()             : fixed-point iteration.
19. elementwise               : find_root / bracket_root / find_minimum / bracket_minimum.

PART E — LINEAR PROGRAMMING & ASSIGNMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
20. linprog()                 : linear programming (LP).
21. milp()                    : mixed-integer LP.
22. linear_sum_assignment()   : Hungarian algorithm.
23. quadratic_assignment()    : graph matching / QAP.

PART F — UTILITIES & LEGACY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
24. approx_fprime / check_grad: finite-difference gradient check.
25. rosen family              : Rosenbrock benchmark function.
26. bracket()                 : bracket a 1-D minimum.
27. Legacy API                : fsolve, fmin, leastsq.
'''

import numpy as np
from scipy import optimize
from scipy.optimize import (
    minimize_scalar, minimize,
    Bounds, LinearConstraint, NonlinearConstraint,
    differential_evolution, basinhopping, shgo, dual_annealing, direct, brute,
    least_squares, curve_fit, lsq_linear, nnls, isotonic_regression,
    root_scalar, root, fixed_point,
    linprog, milp,
    linear_sum_assignment, quadratic_assignment,
    approx_fprime, check_grad, bracket,
    rosen, rosen_der, rosen_hess, rosen_hess_prod,
    fsolve, fmin, leastsq,
    SR1, BFGS as OptBFGS,
)
from scipy.optimize import elementwise
from scipy.special import j1


# =========================================================================================
#  PART A — MINIMIZATION 
# =========================================================================================

##-------------------##
## minimize_scalar() ##
##-------------------##
'''
minimize_scalar(fun, bracket=None, bounds=None, method='brent', tol=None, options=None)

Minimises a scalar function of a single variable.

Methods:
  'brent'   : Brent's method using parabolic interpolation — DEFAULT, fast, derivative-free.
              bracket=(a,b) or (a,b,c) hints where to search.
              A bracket triple (a,b,c) requires f(b) < f(a) and f(b) < f(c) with a < b < c.
  'golden'  : Golden section search — slower than brent; for reference only.
  'bounded' : Guaranteed search in [bounds[0], bounds[1]] — use when you know the interval.

Returns OptimizeResult with:
  res.x   : minimiser.
  res.fun : function value at minimum.
  res.nit / res.nfev : iteration and function evaluation counts.
'''

# Brent: unconstrained minimum of f(x) = (x-2)(x+1)^2
f_1d = lambda x: (x - 2) * (x + 1)**2

res_brent = minimize_scalar(f_1d, method='brent')
print(res_brent.x.round(8))    # 1.0  (true minimum)
print(res_brent.fun.round(8))   # -4.0 (true minimum value)

# Provide a bracket hint to steer toward the desired local minimum
res_bracket = minimize_scalar(f_1d, bracket=(0, 1.5), method='brent')
print(res_bracket.x.round(6))  # 1.0

# Bounded: guaranteed search in [a, b]
# Bessel J1 minimum near x=5.33 within [4, 7]
res_bounded = minimize_scalar(j1, bounds=(4, 7), method='bounded')
print(res_bounded.x.round(6))   # 5.331442

# Find minimum of sin(x) in [2, 5]
res_sin = minimize_scalar(np.sin, bounds=(2, 5), method='bounded')
print(res_sin.x.round(6))    # 4.712389 ≈ 3pi/2
print(res_sin.fun.round(6))   # -1.0

# Golden: educational comparison — same answer, more evaluations
res_golden = minimize_scalar(f_1d, method='golden')
print(np.isclose(res_golden.x, res_brent.x, atol=1e-5))  # True


##----------------------------##
## minimize() — unconstrained ##
##----------------------------##
'''
minimize(fun, x0, args=(), method=None, jac=None, hess=None, hessp=None,
         bounds=None, constraints=(), tol=None, callback=None, options=None)

Minimises a scalar-valued function of a vector argument.

fun   : f(x, *args) → float.
x0    : initial guess (1-D array).
jac   : gradient. Can be:
          callable jac(x) → array
          True    (fun returns (f, grad) tuple — avoids duplicate computation)
          '2-point', '3-point', 'cs'  (finite-difference approximation)
hess  : Hessian. Callable, 'BFGS', 'SR1', LinearOperator, or '2-point'.
hessp : callable hessp(x, p) returning H(x)*p (Hessian-vector product).
bounds: Bounds object or list of (lo, hi) pairs (supported only by some methods).
constraints: list of dicts or NonlinearConstraint / LinearConstraint objects.

Returns OptimizeResult:
  res.x       : solution array.
  res.fun     : objective value at solution.
  res.success : bool.
  res.message : termination reason.
  res.nfev, res.njev, res.nhev : evaluation counts.
  res.jac     : gradient at solution (if computed).
  res.hess_inv: approximate inverse Hessian (BFGS only).
'''

# Reference benchmark: Rosenbrock function, N=5
# f(x) = sum [100*(x[i+1] - x[i]^2)^2 + (1 - x[i])^2]
# Minimum = 0 at x = [1, 1, ..., 1]
x0_5 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])

# ── Nelder-Mead: derivative-free simplex algorithm.
# Use when: gradients unavailable or noisy; simple low-dimensional problems.
# Caution: slow convergence for n > ~10; no guarantees for constrained problems.
res_nm = minimize(rosen, x0_5, method='Nelder-Mead',
                  options={'xatol': 1e-8, 'fatol': 1e-8, 'maxiter': 100000})
print(res_nm.x.round(4))   # [1. 1. 1. 1. 1.]
print(res_nm.success)       # True

# ── Powell: derivative-free line search along conjugate directions.
# Better than Nelder-Mead for separable or near-separable problems.
res_pow = minimize(rosen, x0_5, method='Powell',
                   options={'xtol': 1e-8, 'ftol': 1e-8})
print(res_pow.x.round(6)) # [1. 1. 1. 1. 1.]
print(res_pow.success)  # True

# ── CG (Conjugate Gradient): uses gradient; good for large unconstrained smooth problems.
# No bounds or constraints supported.
res_cg = minimize(rosen, x0_5, method='CG', jac=rosen_der)
print(res_cg.x.round(6)) # [1.       1.       0.999999 0.999998 0.999996]
print(res_cg.success)  # True

# ── BFGS: quasi-Newton; builds an approximate inverse Hessian iteratively.
# DEFAULT choice for smooth unconstrained problems when gradient is available.
res_bfgs = minimize(rosen, x0_5, method='BFGS', jac=rosen_der)
print(res_bfgs.x.round(6)) # [1.       1.       1.       1.       1.000001]
print(res_bfgs.nfev, res_bfgs.njev)  # far fewer calls than Nelder-Mead

# BFGS with numerical gradient (slower but convenient — no analytic gradient needed)
res_bfgs_fd = minimize(rosen, x0_5, method='BFGS', jac='2-point')
print(np.allclose(res_bfgs.x, res_bfgs_fd.x, atol=1e-4))  # True

# Avoid redundant f/grad evaluation: return (f, grad) together with jac=True
def rosen_and_grad(x):
    return rosen(x), rosen_der(x)

res_jac_true = minimize(rosen_and_grad, x0_5, method='BFGS', jac=True)
print(np.allclose(res_jac_true.x, res_bfgs.x, atol=1e-5))  # True

# Memoize expensive computation with lru_cache (shared across f and grad calls)
from functools import lru_cache
@lru_cache(maxsize=None)
def expensive_rosen(x_tuple):
    x = np.array(x_tuple)
    return rosen(x)   # in real code this would be slow

# ── L-BFGS-B: limited-memory BFGS with box bounds. Best for large n.
# Uses only m recent gradient vectors (m=10 default) — O(m*n) memory vs O(n^2).
res_lbfgsb = minimize(rosen, x0_5, method='L-BFGS-B', jac=rosen_der)
print(res_lbfgsb.x.round(6)) # [1.       1.       1.       1.000001 1.000002]

# L-BFGS-B with box bounds
bounds_box = [(0.0, 2.0)] * 5   # each variable in [0, 2]
res_lbfgsb_bounded = minimize(rosen, x0_5, method='L-BFGS-B', jac=rosen_der,
                               bounds=bounds_box)
print(res_lbfgsb_bounded.x.round(6)) # [1.       1.       1.       0.999999 0.999999]
                                     # within [0,2]^5; true minimum [1,...,1] is feasible

# ── Newton-CG: second-order method using the Hessian.
# Best for medium-scale problems where H can be computed or approximated cheaply.
# Supports full Hessian (hess=) or Hessian-vector product (hessp=) — the latter
# avoids forming the full n*n matrix (better for large n, especially sparse).
res_ncg = minimize(rosen, x0_5, method='Newton-CG',
                   jac=rosen_der, hess=rosen_hess,
                   options={'xtol': 1e-8})
print(res_ncg.x.round(6)) # [1. 1. 1. 1. 1.]
print(res_ncg.nhev)  # 24 - number of Hessian evaluations

# Newton-CG with Hessian-vector product (avoids storing full H matrix)
res_ncg_hp = minimize(rosen, x0_5, method='Newton-CG',
                      jac=rosen_der, hessp=rosen_hess_prod,
                      options={'xtol': 1e-8})
print(np.allclose(res_ncg.x, res_ncg_hp.x, atol=1e-5))  # True

# ── Trust-region family: fit quadratic model in trust-region ball ||p|| <= Delta.
# Adjust Delta based on agreement with actual function — more robust than line search.

# trust-ncg: uses CG to solve the trust-region subproblem (approximate; large-scale).
res_tncg = minimize(rosen, x0_5, method='trust-ncg',
                    jac=rosen_der, hess=rosen_hess,
                    options={'gtol': 1e-8})
print(res_tncg.x.round(6)) # [1. 1. 1. 1. 1.]

# trust-krylov: uses GLTR/truncated Krylov subspace — better for indefinite Hessians.
res_tkrylov = minimize(rosen, x0_5, method='trust-krylov',
                       jac=rosen_der, hessp=rosen_hess_prod,
                       options={'gtol': 1e-8})
print(res_tkrylov.x.round(6)) # [1. 1. 1. 1. 1.]

# trust-exact: solves trust-region subproblem nearly exactly (3-4 Cholesky factorizations).
# Fewer iterations than trust-ncg/krylov; requires full Hessian; best for n < ~1000.
res_texact = minimize(rosen, x0_5, method='trust-exact',
                      jac=rosen_der, hess=rosen_hess,
                      options={'gtol': 1e-8})
print(res_texact.x.round(6)) # [1. 1. 1. 1. 1.]
print(res_texact.nit)   # 13 - fewest iterations among trust methods

# ── Passing extra args to the objective function
def rosen_scaled(x, scale):
    return scale * rosen(x)

res_args = minimize(rosen_scaled, x0_5, method='BFGS',
                    jac=lambda x, s: s * rosen_der(x),
                    args=(2.0,))
print(np.allclose(res_args.x, np.ones(5), atol=1e-4))  # True — scale doesn't shift minimum

# ── Callback: monitor convergence during optimisation
history = []
def cb(xk):
    history.append(rosen(xk))

minimize(rosen, x0_5, method='BFGS', jac=rosen_der, callback=cb)
print(len(history), history[0] > history[-1])  # 25 True — objective decreases

##--------------------------##
## minimize() — constrained ##
##--------------------------##
'''
Constrained minimisation methods:

method='SLSQP'        : Sequential Least-Squares Programming.
                        Constraints as dicts with keys 'type', 'fun', 'jac'.
                        'type': 'eq' (h(x)==0) or 'ineq' (g(x)>=0).
                        Fast for small-medium n with smooth constraints.

method='trust-constr' : Modern trust-region interior-point.
                        Constraints as LinearConstraint / NonlinearConstraint objects.
                        Handles eq+ineq via lb <= c(x) <= ub.
                        Supports sparsity; best for large constrained problems.

method='COBYLA'       : Derivative-free; linear approximation to constraints.
                        Use when gradient of constraints is not available.

method='COBYQA'       : Derivative-free quadratic approximation; more modern than COBYLA.

Bounds always via Bounds(lb, ub) or list of (lo, hi).
'''

# Problem: minimize Rosenbrock (2-D) subject to:
#   x0 + 2*x1 <= 1          (linear inequality)
#   2*x0 + x1 == 1          (linear equality)
#   x0^2 + x1 <= 1          (nonlinear inequality)
#   x0^2 - x1 <= 1          (nonlinear inequality)
#   0 <= x0 <= 1,  -0.5 <= x1 <= 2.0
# True constrained solution: x ~= [0.4149, 0.1701]

def rosen_2d(x):
    return 100*(x[1]-x[0]**2)**2 + (1-x[0])**2

def rosen_2d_grad(x):
    return np.array([-400*x[0]*(x[1]-x[0]**2) - 2*(1-x[0]),
                      200*(x[1]-x[0]**2)])

bounds_2d = Bounds([0., -0.5], [1.0, 2.0])

# SLSQP: constraints as dicts
# 'ineq': g(x) >= 0   'eq': h(x) == 0
ineq_cons = {
    'type': 'ineq',
    'fun' : lambda x: np.array([1 - x[0] - 2*x[1],
                                 1 - x[0]**2 - x[1],
                                 1 - x[0]**2 + x[1]]),
    'jac' : lambda x: np.array([[-1., -2.],
                                 [-2.*x[0], -1.],
                                 [-2.*x[0],  1.]])
}
eq_cons = {
    'type': 'eq',
    'fun' : lambda x: np.array([2*x[0] + x[1] - 1]),
    'jac' : lambda x: np.array([[2., 1.]])
}

res_slsqp = minimize(rosen_2d, [0.5, 0.], method='SLSQP',
                     jac=rosen_2d_grad,
                     constraints=[eq_cons, ineq_cons],
                     bounds=bounds_2d,
                     options={'ftol': 1e-9})
print(res_slsqp.x.round(6))   # [0.41494  0.17011]
print(res_slsqp.success)       # True

# trust-constr: constraints as objects (more general; supports sparse/large problems)

# LinearConstraint: lb <= A*x <= ub
# x0 + 2*x1 <= 1  and  2*x0 + x1 == 1 (lb=ub=1 means equality)
linear_con = LinearConstraint([[1, 2], [2, 1]], [-np.inf, 1.], [1., 1.])

# NonlinearConstraint: lb <= c(x) <= ub
def nlcon_fun(x):
    return [x[0]**2 + x[1], x[0]**2 - x[1]]

def nlcon_jac(x):
    return [[2*x[0], 1.], [2*x[0], -1.]]

def nlcon_hess(x, v):
    return v[0]*np.array([[2.,0.],[0.,0.]]) + v[1]*np.array([[2.,0.],[0.,0.]])

nonlin_con = NonlinearConstraint(nlcon_fun, -np.inf, 1.,
                                 jac=nlcon_jac, hess=nlcon_hess)

res_tc = minimize(rosen_2d, [0.5, 0.], method='trust-constr',
                  jac=rosen_2d_grad, hess=SR1(),
                  constraints=[linear_con, nonlin_con],
                  bounds=bounds_2d,
                  options={'verbose': 0, 'gtol': 1e-8})
print(res_tc.x.round(6))   # [0.41494  0.17011]
print(res_tc.success)       # True

# trust-constr with SR1 quasi-Newton Hessian approximation
res_tc_sr1 = minimize(rosen_2d, [0.5, 0.], method='trust-constr',
                      jac='2-point', hess=SR1(),
                      constraints=[linear_con, nonlin_con],
                      bounds=bounds_2d, options={'gtol': 1e-8})
print(np.allclose(res_tc.x, res_tc_sr1.x, atol=1e-4))  # True

# NonlinearConstraint: Hessian via BFGS approximation (when analytic H is hard)
nonlin_con_bfgs = NonlinearConstraint(nlcon_fun, -np.inf, 1.,
                                      jac=nlcon_jac, hess=OptBFGS())
res_tc_bfgs = minimize(rosen_2d, [0.5, 0.], method='trust-constr',
                       jac='2-point', hess=SR1(),
                       constraints=nonlin_con_bfgs,
                       bounds=bounds_2d, options={'gtol': 1e-8})
print(res_tc_bfgs.x.round(4))  # [0.7075 0.4995] (not the true solution, but satisfies constraints and is a local minimum)

# COBYLA: derivative-free constrained optimisation
# All constraints must be c(x) >= 0
res_cobyla = minimize(rosen_2d, [0.5, 0.], method='COBYLA',
                      constraints=[
                          {'type': 'ineq', 'fun': lambda x: 1 - x[0] - 2*x[1]},
                          {'type': 'ineq', 'fun': lambda x: 2*x[0] + x[1] - 1},
                          {'type': 'ineq', 'fun': lambda x: 1 - (2*x[0] + x[1])},
                          {'type': 'ineq', 'fun': lambda x: 1 - x[0]**2 - x[1]},
                          {'type': 'ineq', 'fun': lambda x: 1 - x[0]**2 + x[1]},
                      ],
                      options={'rhobeg': 0.5, 'maxiter': 5000})
print(res_cobyla.x.round(4))  # approximately [0.4149, 0.1701]


'''
LOCAL MINIMISATION METHOD SELECTION TABLE
=====================================================================================
Method          Bounds  NL Constraints  Gradient  Hessian  Sparsity  Notes
-------------------------------------------------------------------------------------
Nelder-Mead     *                                                    Derivative-free simplex
Powell          *                                                    Derivative-free line search
CG                              *                                    Conjugate gradient
BFGS                            *                                    Quasi-Newton; DEFAULT
L-BFGS-B        *               *                             *      Large n, box-bounded
TNC             *               *                             *      Truncated Newton, bounded
Newton-CG                       *        *       (or hessp)   *      2nd-order, large sparse
trust-ncg                       *        *       (or hessp)   *      Trust region, large sparse
trust-krylov                    *        *       (or hessp)   *      Better for indefinite H
trust-exact                     *        *       (full only)         Fewer iters, medium n
dogleg                          *        *       (full only)         Simple trust region
SLSQP           *       *       *                                    Fast for small n
COBYLA          *       *                                            Derivative-free, robust
COBYQA          *       *                                            Modern derivative-free
trust-constr    *       *       *        *                    *      Most general constrained
=====================================================================================

Decision guide:
  No gradient available              -> Nelder-Mead (small n) or Powell / COBYLA
  Smooth unconstrained               -> BFGS (default)
  Large n, unconstrained             -> L-BFGS-B (box bounds) or Newton-CG (with H)
  Box bounds only                    -> L-BFGS-B or TNC
  Equality + inequality constraints  -> SLSQP (easy) or trust-constr (large/sparse)
  Sparse Hessian (finite elements)   -> Newton-CG or trust-krylov with hessp=
  Indefinite or near-singular H      -> trust-krylov > trust-ncg
  Medium n, full H cheap             -> trust-exact (fewest iterations)
'''


# =========================================================================================
#  PART B — GLOBAL OPTIMIZATION 
# =========================================================================================

# Common test function: eggholder — many local minima on [-512, 512]^2
def eggholder(x):
    return (-(x[1]+47) * np.sin(np.sqrt(abs(x[0]/2 + x[1]+47)))
            - x[0] * np.sin(np.sqrt(abs(x[0] - (x[1]+47)))))

bounds_egg = [(-512., 512.), (-512., 512.)]
# Known global minimum ~= -959.64 at x ~= [512, 404.2]

# Rastrigin in 2-D: fast demo function
def rastrigin(x):
    n = len(x)
    return 10*n + sum(xi**2 - 10*np.cos(2*np.pi*xi) for xi in x)
# Global minimum = 0 at x = [0, 0, ...]

bounds_rast = [(-5.12, 5.12)] * 2

##--------------------------##
## differential_evolution() ##
##--------------------------##
'''
differential_evolution(func, bounds, strategy='best1bin', maxiter=1000,
                       popsize=15, tol=0.01, mutation=(0.5,1), recombination=0.7,
                       seed=None, callback=None, disp=False, polish=True,
                       init='latinhypercube', atol=0, updating='immediate',
                       workers=1, constraints=(), x0=None, integrality=None,
                       vectorized=False)

Stochastic population-based evolutionary algorithm.
For each "agent" x in the population, a trial vector is created by mutating
and crossing over other members. Agents with lower f are kept.

strategy   : mutation strategy. Options include:
               'best1bin' (default), 'best2bin', 'rand1bin', 'randtobest1bin'.
polish     : if True, run a final L-BFGS-B local minimisation (default True).
workers    : parallelise fitness evaluations (-1 = all CPUs).
integrality: 1-D array marking integer decision variables.
vectorized : func(x) accepts (n, d) array for batched evaluation.
constraints: NonlinearConstraint / LinearConstraint for feasibility.

Use when: multimodal function; bounds known; no gradient; need global search.
Very reliable in practice; not guaranteed but rarely fails for good bounds.
'''

res_de = differential_evolution(rastrigin, bounds_rast, seed=42, maxiter=500,
                                  popsize=15, tol=1e-8, polish=True)
print(res_de.x.round(6), res_de.fun.round(6))  # ~[0,0]  0.0
print(res_de.success)  # True

# With nonlinear constraint: x0^2 + x1^2 <= 10
nlc_de = NonlinearConstraint(lambda x: x[0]**2 + x[1]**2, 0, 10)
res_de_con = differential_evolution(rastrigin, bounds_rast, seed=42,
                                     constraints=nlc_de, polish=True)
print(np.linalg.norm(res_de_con.x) <= 10 + 1e-6)  # True — feasible

# Integer variables: x0 must be an integer
res_de_int = differential_evolution(lambda x: (x[0]-3)**2 + (x[1]-1.5)**2,
                                     [(-5,5), (-5,5)], seed=42,
                                     integrality=[1, 0])
print(res_de_int.x)   # x0 should be 3 (integer), x1 near 1.5


##----------------##
## basinhopping() ##
##----------------##
'''
basinhopping(func, x0, niter=100, T=1.0, stepsize=0.5, minimizer_kwargs=None,
             take_step=None, accept_test=None, callback=None, interval=50,
             disp=False, niter_success=None, seed=None)

Iterated local search with random perturbations:
  1. From current x, run a local minimiser (default: L-BFGS-B).
  2. Perturb x randomly with step size stepsize.
  3. Accept/reject the new basin via Metropolis criterion (temperature T).
  4. Repeat niter times.

T              : "temperature" — higher = more likely to accept worse solutions.
niter_success  : stop early if global minimum unchanged for this many steps.
minimizer_kwargs: dict passed to scipy.optimize.minimize for local search.
take_step      : custom callable that takes current x and returns a new x.

Use when: smooth function with many basins; a good local minimiser is available.
'''

def multiwell(x):
    return np.sin(x[0]) * np.cos(x[1]) + 0.1*(x[0]**2 + x[1]**2)

res_bh = basinhopping(multiwell, x0=[2., 2.],
                       minimizer_kwargs={'method': 'L-BFGS-B',
                                         'bounds': [(-5,5), (-5,5)]},
                       niter=200, T=1.0, stepsize=0.5, seed=42)

print(res_bh.x.round(4), res_bh.fun.round(6)) # [1.2655 2.572 ] 0.018488
print(res_bh.lowest_optimization_result.success)  # True

# Custom step function
class RandomDisplacement:
    def __init__(self, stepsize=0.5):
        self.stepsize = stepsize
    def __call__(self, x):
        x += np.random.uniform(-self.stepsize, self.stepsize, x.shape)
        return x

res_bh_custom = basinhopping(multiwell, [0., 0.], niter=100, seed=42,
                               take_step=RandomDisplacement(0.3),
                               minimizer_kwargs={'method': 'BFGS'})
print(res_bh_custom.fun.round(4)) # -0.7946


##--------##
## shgo() ##
##--------##
'''
shgo(func, bounds, args=(), constraints=None, n=100, iters=1, callback=None,
     minimizer_kwargs=None, options=None, sampling_method='simplicial')

Simplicial Homology Global Optimisation.
  1. Samples the domain using a simplicial complex (or Sobol', etc.).
  2. Uses topological properties to identify basins of attraction.
  3. Runs a local minimiser in each identified basin.

Key advantage: finds ALL local minima (accessible via res.xl, res.funl).
Deterministic with sampling_method='simplicial'.
Converges in finite evaluations for Lipschitz functions.

sampling_method='simplicial': systematic, deterministic.
sampling_method='sobol'     : QMC Sobol', more nodes but often faster.
n     : sampling points per iteration.
iters : sampling iterations (increase for harder problems).
'''

res_shgo = shgo(rastrigin, bounds_rast, n=200, iters=3,
                sampling_method='sobol')
print(res_shgo.x.round(6), res_shgo.fun.round(6))  # [0,0]  0.0
print(res_shgo.success)  # True

# Access ALL local minima found (sorted by function value)
print(f"SHGO found {len(res_shgo.xl)} local minima")
print(res_shgo.funl[:3].round(4))  # [0.    0.995 0.995] top 3 local minima

# With nonlinear constraint
res_shgo_c = shgo(rastrigin, bounds_rast,
                  constraints={'type': 'ineq', 'fun': lambda x: 4 - x[0]**2 - x[1]**2},
                  n=100)
print(res_shgo_c.x.round(4)) # [-0. -0.]


##------------------##
## dual_annealing() ##
##------------------##
'''
dual_annealing(func, bounds, args=(), maxiter=1000, minimizer_kwargs=None,
               initial_temp=5230, restart_temp_ratio=2e-5, visit=2.62, accept=-5.0,
               maxfun=1e7, seed=None, no_local_search=False, callback=None, x0=None)

Combines simulated annealing (SA) and fast simulated annealing (FSA) with
local search to escape local minima. Effective for highly multimodal functions.

initial_temp : starting temperature (higher = more exploration).
visit        : parameter for visiting distribution (2.62 ~ Cauchy-like tail).
accept       : parameter for acceptance distribution.
no_local_search: if True, pure annealing without local polish.

Use when: function is highly multimodal or non-smooth; differential evolution fails.
'''

res_da = dual_annealing(rastrigin, bounds_rast, seed=42, maxiter=3000)
print(res_da.x.round(6), res_da.fun.round(8))  # ~[0,0]  0.0
print(res_da.success)  # True

# Harder test: eggholder
res_da_egg = dual_annealing(eggholder, bounds_egg, seed=42, maxiter=5000)
print(res_da_egg.fun.round(4))   # ~-955 to -959 (near global -959.64)

##----------##
## direct() ##
##----------##
'''
direct(func, bounds, args=(), eps=1e-4, maxfun=None, maxiter=1000,
       locally_biased=True, f_min=-np.inf, f_min_rtol=1e-4,
       vol_tol=1e-16, len_tol=1e-6, callback=None)

DIRECT (DIviding RECTangles): deterministic, derivative-free, space-partitioning.

Algorithm:
  1. Normalise the search space to [0,1]^n.
  2. Identify "potentially optimal" hyperrectangles.
  3. Divide them and evaluate at their centres.
  4. Repeat until budget exhausted.

locally_biased=True : DIRECT-l; biases toward local refinement (good for smooth).
locally_biased=False: original DIRECT; unbiased (good for highly multimodal).
f_min              : known lower bound on f — enables early stopping.

Advantages: fully deterministic; no randomness; systematic coverage.
Disadvantages: scales poorly with n (curse of dimensionality); best for n <= 10.
'''

res_dir = direct(rastrigin, bounds_rast, maxiter=500)
print(res_dir.x.round(4), round(res_dir.fun, 4))   # near [0,0]
print(res_dir.success)  # True

# Early stopping when known lower bound is achieved
res_dir_lb = direct(rastrigin, bounds_rast, f_min=0., f_min_rtol=1e-8)
print(res_dir_lb.x.round(4)) # [0. 0.]


##---------##
## brute() ##
##---------##
'''
brute(func, ranges, args=(), Ns=20, full_output=False, finish=None, disp=False, workers=1)

Exhaustive grid search: evaluates func on an Ns-point grid in each dimension,
then optionally refines the best grid point with a local minimiser (finish=).

ranges : list of (lo, hi) or slice(lo, hi, step) objects.
Ns     : number of equally-spaced points per axis.
finish : local minimiser to polish (default scipy.optimize.fmin; use None to skip).
full_output=True : also return the grid and all function values.

Cost: O(Ns^n) evaluations. Use only for n <= 3.
'''

# f(x,y) = (x-1)^2 + (y+0.5)^2  -> minimum at (1, -0.5)
def f_bowl_2d(x):
    return (x[0]-1)**2 + (x[1]+0.5)**2

res_brute = brute(f_bowl_2d, ranges=[(-2, 3), (-2, 2)], Ns=50, finish=optimize.fmin)
print(res_brute.round(4))  # [1.0  -0.5]

# With full output (returns minimum, f-value, grid, grid-values)
x_min_b, f_min_b, grid, Jout = brute(f_bowl_2d, ranges=[(-2,3), (-2,2)],
                                      Ns=20, full_output=True, finish=None)
print(x_min_b.round(2), f_min_b.round(4)) # [ 0.89 -0.53] 0.0118
print(grid[0].shape)   # (20, 20) grid of x0 values


'''
GLOBAL OPTIMISER COMPARISON TABLE
==========================================================================
Solver                Bounds  NL Constraints  Deterministic  Best for
--------------------------------------------------------------------------
differential_evolution  *       *             No             Robust general-purpose
basinhopping                                  No             Good local min available
shgo                    *       *             Yes            Finding ALL local minima
dual_annealing          *                     No             Highly multimodal / rough
direct                  *                     Yes            Small n; systematic
brute                   *                     Yes            Very small n; exhaustive
==========================================================================
'''


# =========================================================================================
#  PART C — LEAST-SQUARES & CURVE FITTING 
# =========================================================================================

##-----------------##
## least_squares() ##
##-----------------##
'''
least_squares(fun, x0, jac='2-point', bounds=(-inf,inf), method='trf',
              ftol=1e-8, xtol=1e-8, gtol=1e-8, x_scale=1.0,
              loss='linear', f_scale=1.0, max_nfev=None, verbose=0,
              tr_solver=None, jac_sparsity=None, args=(), kwargs={})

Solves:  min_x  (1/2) * sum(rho(fi(x)^2))   s.t.  lb <= x <= ub

fun    : residual vector function fun(x) -> array of shape (m,).
jac    : analytic Jacobian (m*n array), or '2-point'/'3-point'/'cs' for FD.
method : 'trf' (Trust Region Reflective, DEFAULT); 'dogbox'; 'lm' (Levenberg-Marquardt, no bounds).
loss   : loss function for robustness:
           'linear'  : standard LS (default).
           'soft_l1' : L2 near 0, L1 for large residuals.
           'huber'   : smooth L1.
           'cauchy'  : heavy-tailed; robust to extreme outliers.
           'arctan'  : bounded; very heavy outliers.
f_scale: threshold separating inliers from outliers (non-linear loss only).
jac_sparsity: sparse matrix describing Jacobian structure (efficient FD for large systems).

Returns OptimizeResult with:
  res.x      : solution.
  res.cost   : (1/2) * sum(residuals^2) at solution.
  res.fun    : residual vector at solution.
  res.jac    : Jacobian at solution.
  res.success, res.message.
'''

rng_fit = np.random.default_rng(0)
t_data  = np.linspace(0, 4, 30)
a_true, b_true = 3.5, 1.2
y_data  = a_true * np.exp(-b_true * t_data) + rng_fit.normal(0, 0.1, len(t_data))

def residuals_exp(params, t, y):
    a, b = params
    return a * np.exp(-b * t) - y   # residuals (zero at perfect fit)

def jac_exp(params, t, y):
    a, b = params
    J = np.zeros((len(t), 2))
    J[:, 0] = np.exp(-b * t)            # dr/da
    J[:, 1] = -a * t * np.exp(-b * t)   # dr/db
    return J

res_ls = least_squares(residuals_exp, x0=[1., 1.],
                        jac=jac_exp, bounds=(0, [10., 10.]),
                        args=(t_data, y_data))
print(res_ls.x.round(4))    # ~[3.5, 1.2]
print(res_ls.success)        # True
print(np.allclose(res_ls.x, [a_true, b_true], atol=0.2))  # True

# Robust fitting: loss='soft_l1' downweights outliers
y_outlier = y_data.copy()
y_outlier[[5, 15, 25]] += 3.0   # inject 3 large outliers

res_plain   = least_squares(residuals_exp, [1.,1.], args=(t_data, y_outlier))
res_robust  = least_squares(residuals_exp, [1.,1.], args=(t_data, y_outlier),
                             loss='soft_l1', f_scale=0.5)

print("Plain LS (outliers):", res_plain.x.round(3))    # [3.445 0.843] pulled by outliers
print("Robust LS (outliers):", res_robust.x.round(3))  # [3.52  1.147] closer to truth

# Enzymatic reaction model (Kowalik & Morrison benchmark)
# fi(x) = x0*(ui^2 + ui*x1)/(ui^2 + ui*x2 + x3) - yi
def model_enz(x, u):
    return x[0]*(u**2 + x[1]*u) / (u**2 + x[2]*u + x[3])

u_enz = np.array([4., 2., 1., .5, .25, .167, .125, .1, .0833, .0714, .0625])
y_enz = np.array([.1957,.1947,.1735,.16,.0844,.0627,.0456,.0342,.0323,.0235,.0246])

def fun_enz(x):
    return model_enz(x, u_enz) - y_enz

res_enz = least_squares(fun_enz, [2.5, 3.9, 4.15, 3.9],
                         bounds=(0, 100), method='trf')
print(res_enz.x.round(4))  # ~[0.1928, 0.1913, 0.1231, 0.1361]

# Cost after fit
print(f"Final cost: {res_enz.cost:.2e}")   # ~1.5e-4

##-------------##
## curve_fit() ##
##-------------##
'''
curve_fit(f, xdata, ydata, p0=None, sigma=None, absolute_sigma=False,
          check_finite=True, bounds=(-inf,inf), method=None,
          jac=None, full_output=False, nan_policy=None, **kwargs)

Wraps least_squares for the common case of fitting a model to data.

f      : callable f(xdata, *params) -> model predictions.
p0     : initial parameter guess (default: all 1s — often needs to be set).
sigma  : measurement uncertainties.
           absolute_sigma=True  : treated as actual std devs; covariance is correct.
           absolute_sigma=False : only relative weighting (scales covariance uniformly).
bounds : (lb_array, ub_array) for parameter bounds.

Returns (popt, pcov):
  popt : best-fit parameters.
  pcov : covariance matrix. sqrt(diag(pcov)) = parameter standard errors.
         If pcov contains inf, the fit failed or parameters are underdetermined.

full_output=True : also returns (popt, pcov, infodict, mesg, ier).
method : 'lm' (default, Levenberg-Marquardt, no bounds), 'trf' or 'dogbox' (with bounds).
'''

def exp_model(t, a, b):
    return a * np.exp(-b * t)

popt, pcov = curve_fit(exp_model, t_data, y_data, p0=[1., 1.])
print(popt.round(4))                        # ~[3.5, 1.2]
print(np.sqrt(np.diag(pcov)).round(4))      # standard errors

# With sigma (measurement uncertainties) and bounds
sigma_data = np.full_like(y_data, 0.1)
popt_b, pcov_b = curve_fit(exp_model, t_data, y_data,
                            p0=[1., 1.], bounds=(0, [10., 5.]),
                            sigma=sigma_data, absolute_sigma=True)
print(popt_b.round(4)) # [3.5501 1.2381]

# 95% confidence interval from covariance
perr = np.sqrt(np.diag(pcov_b))
print("95% CI:", (1.96 * perr).round(4)) # 95% CI: [0.138 0.074]

# Fit sinusoid: A*sin(omega*t + phi) + C
def sinusoid(t, A, omega, phi, C):
    return A * np.sin(omega * t + phi) + C

t_sin = np.linspace(0, 4*np.pi, 200)
y_sin = 2.5*np.sin(1.3*t_sin - 0.4) + 1.0 + rng_fit.normal(0, 0.2, 200)

popt_sin, pcov_sin = curve_fit(sinusoid, t_sin, y_sin,
                                p0=[2., 1., 0., 0.],
                                bounds=([0, 0, -np.pi, -5], [10, 5, np.pi, 5]))
print(popt_sin.round(3))   # ~[2.5, 1.3, -0.4, 1.0]

# Multi-dimensional xdata: pass as extra column
# y = a*x[:,0] + b*x[:,1] + c (plane fit)
rng2 = np.random.default_rng(5)
x2d = rng2.uniform(0, 5, (50, 2))
y2d = 2.0*x2d[:,0] + 0.5*x2d[:,1] + 1.0 + rng2.normal(0, 0.2, 50)

def plane(x, a, b, c):
    return a*x[:,0] + b*x[:,1] + c

popt_plane, _ = curve_fit(plane, x2d, y2d, p0=[1., 1., 0.])
print(popt_plane.round(3))   # ~[2.0, 0.5, 1.0]
                             #  [1.993 0.493 1.07 ]


##--------------##
## lsq_linear() ##
##--------------##
'''
lsq_linear(A, b, bounds=(-inf, inf), method='trf', tol=1e-10,
           lsq_solver=None, max_iter=None, verbose=0)

Solves:  min_x  ||Ax - b||_2   subject to  lb <= x <= ub

A : matrix (m x n), dense or sparse.
b : observation vector (m,).
method : 'trf' (default, Trust Region Reflective) or 'bvls' (active-set, exact).

Returns OptimizeResult with res.x, res.cost (0.5*||Ax-b||^2), res.fun (residual Ax-b).
'''

rng_lsq = np.random.default_rng(1)
A_lsq   = rng_lsq.normal(0, 1, (20, 5))
x_true  = np.abs(rng_lsq.normal(0, 1, 5))   # non-negative ground truth
b_lsq   = A_lsq @ x_true + rng_lsq.normal(0, 0.1, 20)

# Non-negative constraint
res_lsq_lin = lsq_linear(A_lsq, b_lsq, bounds=(0, np.inf))
print(res_lsq_lin.x.round(4)) # [0.6405 0.8133 0.1129 0.6403 1.2016]
print((res_lsq_lin.x >= -1e-10).all())   # True all non-negative ✓

# Box-constrained: each variable in [0, 2]
res_box = lsq_linear(A_lsq, b_lsq, bounds=(0, 2.))
print((res_box.x >= 0).all() and (res_box.x <= 2).all())  # True


##--------##
## nnls() ##
##--------##
'''
nnls(A, b, maxiter=None, atol=None)

Solves:  argmin_x  ||Ax - b||_2   subject to  x >= 0

Non-Negative Least Squares (Lawson-Hanson algorithm).
Simpler interface than lsq_linear for the pure non-negativity constraint case.

Returns (x, residual_norm) where residual_norm = ||Ax - b||_2.
'''

x_nnls, rnorm_nnls = nnls(A_lsq, b_lsq)
print(x_nnls.round(4)) # [0.6405 0.8133 0.1129 0.6403 1.2016]
print((x_nnls >= -1e-10).all()) # True all non-negative ✓
print(round(rnorm_nnls, 6)) # 0.503418 ||Ax - b||_2

# nnls and lsq_linear(bounds=(0,inf)) should give the same result
print(np.allclose(x_nnls, res_lsq_lin.x, atol=1e-4))  # True


##-----------------------##
## isotonic_regression() ##
##-----------------------##
'''
isotonic_regression(y, weights=None, increasing=True)

Fits a monotone non-decreasing step function to y using Pool Adjacent Violators:

  min_x  sum(wi * (xi - yi)^2)   s.t.  x1 <= x2 <= ... <= xn

Returns OptimizeResult with res.x (monotone fitted values) and res.blocks (group IDs).
Use for: monotone denoising, calibration, order-constrained estimation.
'''

rng_iso = np.random.default_rng(2)
x_iso   = np.arange(20, dtype=float)
y_noisy = 0.3*x_iso + rng_iso.normal(0, 1.5, 20)

res_iso = isotonic_regression(y_noisy, increasing=True)
print(np.all(np.diff(res_iso.x) >= -1e-12))   # True non-decreasing ✓

# Non-increasing isotonic regression
res_iso_dec = isotonic_regression(-y_noisy, increasing=True)
print(np.all(np.diff(-res_iso_dec.x) <= 1e-12))   # True non-increasing ✓

# Weighted: extra weight on reliable measurements
w = np.ones(20)
w[8:12] = 5.   # central points measured more accurately
res_iso_w = isotonic_regression(y_noisy, weights=w, increasing=True)
print(np.all(np.diff(res_iso_w.x) >= -1e-12))  # True still monotone ✓


# =========================================================================================
#  PART D — ROOT FINDING 
# =========================================================================================

##---------------##
## root_scalar() ##
##---------------##
'''
root_scalar(f, args=(), method=None, bracket=None, fprime=None, fprime2=None,
            x0=None, x1=None, xtol=None, rtol=None, maxiter=None, options=None)

Finds x such that f(x) = 0 for a scalar function.

Method auto-selected based on what information you provide:
  bracket=(a,b)                   -> brentq (guaranteed; default for bracket)
  x0, fprime                      -> newton (Newton-Raphson; fast near root)
  x0, fprime, fprime2             -> halley (cubic convergence)
  x0, x1  (no derivatives)       -> secant (superlinear; no guarantee)
  bracket + method specified      -> bisect / ridder / toms748

Returns RootResults with res.root, res.iterations, res.function_calls, res.converged.

CONVERGENCE RATES (per function evaluation):
  bisect   : 1.0  — guaranteed; slowest
  brentq   : 1.62 — guaranteed with bracket; fast; DEFAULT
  toms748  : 1.65 — slightly faster than brentq
  ridder   : 1.41 — guaranteed with bracket; quadratic
  secant   : 1.62 — no bracket needed; no guarantee
  newton   : 1.41 — needs fprime; fast near root
  halley   : 1.44 — needs fprime and fprime2; fastest per iter
'''

def f_root(x):
    return x**3 - x - 2       # root near x = 1.5214

def f_root_d(x):
    return 3*x**2 - 1

def f_root_d2(x):
    return 6*x

# brentq: default bracketing method (guaranteed, superlinear)
res_bq = root_scalar(f_root, bracket=[1, 2], method='brentq')
print(round(res_bq.root, 10))    # 1.5213797068
print(res_bq.converged)          # True

# bisect: simplest, guaranteed, but slow
res_bisect = root_scalar(f_root, bracket=[1, 2], method='bisect')
print(round(res_bisect.root, 10), res_bisect.iterations) # 1.5213797068 39

# toms748: usually fastest bracketing method
res_toms = root_scalar(f_root, bracket=[1, 2], method='toms748')
print(round(res_toms.root, 10), res_toms.function_calls) # 1.5213797068 8

# Newton-Raphson: needs fprime; no bracket required
res_newton = root_scalar(f_root, x0=1.5, fprime=f_root_d, method='newton')
print(round(res_newton.root, 10), res_newton.iterations) # 1.5213797068 4

# Halley: needs fprime + fprime2; cubic convergence per iteration
res_halley = root_scalar(f_root, x0=1.5, fprime=f_root_d, fprime2=f_root_d2,
                          method='halley')
print(round(res_halley.root, 10), res_halley.iterations)  # 1.5213797068 2 (fewest iterations)

# Secant: two starting points, no derivative
res_secant = root_scalar(f_root, x0=1.4, x1=1.6, method='secant')
print(round(res_secant.root, 10)) # 1.5213797068

# Ridder: bracket, no derivative; quadratic convergence
res_ridder = root_scalar(f_root, bracket=[1, 2], method='ridder')
print(round(res_ridder.root, 10), res_ridder.iterations) # 1.5213797068 4

# Extra arguments: find sqrt(a) as root of x^2 - a = 0
for a in [2., 3., 5.]:
    r = root_scalar(lambda x, a: x**2 - a, args=(a,), bracket=[0, 5])
    print(f"sqrt({a:.0f}) = {r.root:.6f}  (true: {a**0.5:.6f})")
# sqrt(2) = 1.414214  (true: 1.414214)
# sqrt(3) = 1.732051  (true: 1.732051)
# sqrt(5) = 2.236068  (true: 2.236068)

# Multiple roots: find each with separate brackets
roots_sin = [root_scalar(np.sin, bracket=[k*np.pi - 0.1, k*np.pi + 0.1]).root
             for k in range(-2, 3)]
print([round(r, 6) for r in roots_sin])
# [-6.283185, -3.141593, 0.0, 3.141593, 6.283185]

# Direct bracket functions (legacy-compatible standalone wrappers)
from scipy.optimize import brentq, bisect, newton
root_bq_direct = brentq(f_root, 1., 2.)
print(round(root_bq_direct, 10))
# 1.5213797068
# same as root_scalar with method='brentq'

root_newton_direct = newton(f_root, x0=1.5, fprime=f_root_d, fprime2=f_root_d2)
print(round(root_newton_direct, 10)) # 1.5213797068


##--------##
## root() ##
##--------##
'''
root(fun, x0, args=(), method='hybr', jac=None, tol=None, callback=None, options=None)

Finds x such that F(x) = 0 for F: R^n -> R^n (a vector-valued function).

method:
  'hybr'    : MINPACK's HYBRD/HYBRJ — Powell hybrid method. DEFAULT.
              Robust for moderate n; especially good near the root.
  'lm'      : Levenberg-Marquardt (MINPACK). Good for over/underdetermined systems.
  'broyden1': Broyden's first method; approximates Jacobian iteratively. Large n.
  'broyden2': Updates inverse Jacobian directly. Large n.
  'krylov'  : Krylov-space Jacobian approximation. Very large n.
  'anderson': Anderson mixing (generalised secant). Large n.
  'df-sane' : Derivative-free. No Jacobian at all.

jac : analytic Jacobian of F (highly recommended for 'hybr').

Returns OptimizeResult with res.x, res.fun (residual), res.success.
'''

# System of 2 equations:
# x0^2 + x1^2 = 1  (unit circle)
# x0 - x1 = 0      (diagonal)
# Solution: x0 = x1 = 1/sqrt(2) ~= 0.7071
def F_system(x):
    return [x[0]**2 + x[1]**2 - 1, x[0] - x[1]]

def J_system(x):
    return [[2*x[0], 2*x[1]], [1.,     -1.   ]]

res_root = root(F_system, x0=[0.5, 0.3], method='hybr')
print(res_root.x.round(8))                          # [0.70710678  0.70710678]
print(np.abs(F_system(res_root.x)).max() < 1e-10)   # True: residual near zero
print(res_root.success) # True

# With analytic Jacobian (faster convergence)
res_jac_sys = root(F_system, x0=[0.5, 0.5], jac=J_system, method='hybr')
print(np.allclose(res_root.x, res_jac_sys.x, atol=1e-8))  # True

# Classic: find where gradient of Rosenbrock is zero (= minimum)
res_rosen_root = root(rosen_der, x0=np.ones(3)*0.5, method='hybr')
print(res_rosen_root.x.round(6))   # [1. 1. 1.]
print(res_rosen_root.success) # True

# Broyden for larger systems (no full Jacobian stored)
def large_F(x):
    return np.sin(x) - 0.5*x

res_broyden = root(large_F, x0=np.zeros(10), method='broyden1')
print(res_broyden.x.round(6))   # [0. 0. ... 0.] (trivial root sin(x)=0.5x at x=0)
print(res_broyden.success) # True

##---------------##
## fixed_point() ##
##---------------##
'''
fixed_point(func, x0, args=(), xtol=1e-8, maxiter=500, method='del2')

Finds x* such that func(x*) = x* (a fixed point of func).
Uses Aitken delta^2 acceleration ('del2') or plain iteration.

Relation to root finding: fixed point of g <-> root of F(x) = g(x) - x.
Use for contraction mappings where repeated application converges.
'''

# Dottie number: x* = cos(x*) ~= 0.7391
res_fp = fixed_point(np.cos, x0=1.0)
print(res_fp.round(8))   # 0.73908513
print(abs(np.cos(res_fp) - res_fp) < 1e-8)  # True

# Newton step as a fixed-point iteration
def newton_g(x):
    f  = x**3 - x - 2
    fp = 3*x**2 - 1
    return x - f/fp

fp_res = fixed_point(newton_g, x0=1.5)
print(fp_res.round(8))   # 1.5213797068 (root of x^3 - x - 2)

# Vectorised: solve cos(x) = x for multiple starting points
res_fp_vec = fixed_point(np.cos, x0=np.array([0.5, 1.5]))
print(res_fp_vec.round(8))  # [0.73908513, 0.73908513]

##-------------##
## elementwise ##
##-------------##
'''
scipy.optimize.elementwise  (new in SciPy 1.15)

Vectorised scalar root/minimum finding: solves n independent 1-D problems
simultaneously using array-valued xl, xr.

find_root(f, xl, xr)        : Find roots in brackets [xl, xr] (arrays).
bracket_root(f, xl, xr)     : Expand a bracket until a sign change is found.
find_minimum(f, xl, xr)     : Find minima in brackets.
bracket_minimum(f, xl, xr)  : Find a bracket containing a minimum.

f must be elementwise: f(x) with array x returns array of same shape.
All functions return a result object with .x, .bracket, .status, .nfev.
'''

# find_root: solve x^2 - a = 0 for a = [1, 2, 3, 4] simultaneously
# init is (xl, xr) tuple; f(x, a) receives x as array and a via args
a_vals = np.array([1., 2., 3., 4.])
res_er = elementwise.find_root(lambda x, a: x**2 - a,
                                (np.full(4, 0.5), np.full(4, 3.)),
                                args=(a_vals,))
print(res_er.x.round(6))   # [1.  1.4142  1.7321  2.    ] = sqrt(a)

# bracket_root: automatically find sign-change brackets
res_br = elementwise.bracket_root(lambda x, a: x**2 - a,
                                   (np.full(4, 0.5), np.full(4, 3.)),
                                   args=(a_vals,))
xl_br, xr_br = res_br.bracket
print(xl_br.round(4))
# [[0.5 0.5 1.5 1.5]
#  [0.  0.  0.  2. ]]

print(xr_br.round(4))
# [[1.5 1.5 2.5 2.5]
#  [2.  2.  2.  3. ]]

# find_minimum: minimise (x - a)^2 for a = [1, 2, 3]
# init is a 3-tuple (xl, xm, xr) with f(xm) < f(xl) and f(xm) < f(xr)
a_min = np.array([1., 2., 3.])
res_fm = elementwise.find_minimum(lambda x, a: (x - a)**2,
                                   (np.zeros(3), a_min, np.full(3, 5.)),
                                   args=(a_min,))
print(res_fm.x.round(6))   # [1.  2.  3.]  ✓

# bracket_minimum: find a 3-point bracket from a 2-point init
res_bm = elementwise.bracket_minimum(lambda x, a: (x - a)**2,
                                      (np.zeros(3), np.full(3, 5.)),
                                      args=(a_min,))
xl_bm, xm_bm, xr_bm = res_bm.bracket
print(xl_bm.round(3))
# [[ 0.   0.5  1.5]
#  [-3.5  0.5  2.5]]

print(xm_bm.round(3))
# [[0.5 1.5 2.5]
#  [0.5 2.5 3.5]]

print(xr_bm.round(3))
# [[1.5 2.5 4.5]
#  [2.5 3.5 4.5]]

# Use the found bracket for find_minimum
res_fm2 = elementwise.find_minimum(lambda x, a: (x - a)**2,
                                    res_bm.bracket, args=(a_min,))
print(res_fm2.x.round(6))   # [1.  2.  3.]  ✓


# =========================================================================================
#  PART E — LINEAR PROGRAMMING & ASSIGNMENT 
# =========================================================================================

##-----------##
## linprog() ##
##-----------##
'''
linprog(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None,
        bounds=None, method='highs', callback=None, options=None, x0=None)

Minimises the linear objective c . x subject to:
  A_ub . x <= b_ub     (inequality)
  A_eq . x == b_eq     (equality)
  lb <= x <= ub        (variable bounds; default: 0 <= x)

method='highs'    : HiGHS solver (DEFAULT); state-of-the-art; recommended.
method='highs-ds' : HiGHS dual simplex.
method='highs-ipm': HiGHS interior-point.

NOTE: linprog MINIMISES. To maximise c.x, minimise -c.x.

Returns OptimizeResult with:
  res.x      : optimal solution.
  res.fun    : optimal objective c.x.
  res.slack  : A_ub.x - b_ub (<=0 means satisfied).
  res.status : 0=optimal, 2=infeasible, 3=unbounded.
'''

# Production planning: maximise 5x0 + 4x1 (x0 units of product A, x1 of B)
# subject to: 6x0 + 4x1 <= 24 (machine hours); x0 + 2x1 <= 6 (labour); x0,x1 >= 0
c_lp   = [-5., -4.]   # negate for maximisation
A_ub   = [[6., 4.], [1., 2.]]
b_ub   = [24., 6.]
bounds_lp = [(0, None), (0, None)]

res_lp = linprog(c_lp, A_ub=A_ub, b_ub=b_ub, bounds=bounds_lp)
print(res_lp.x.round(6))     # [3.  1.5]
print(round(-res_lp.fun, 4))   # 21.0  (max profit)
print(res_lp.status)           # 0 = optimal

# Diet problem: minimise cost subject to nutritional minimums
costs      = np.array([1.5, 2.0, 0.8, 1.2])
nutrients  = np.array([[10, 20, 5, 8],      # protein
                        [2,  4, 15, 6],      # fibre
                        [100,50, 80, 40]])    # calories
min_req    = np.array([50., 30., 400.])      # daily minimums

res_diet = linprog(costs,
                   A_ub=-nutrients,   # A.x >= b  <=>  -A.x <= -b
                   b_ub=-min_req,
                   bounds=[(0, None)]*4)
print(res_diet.x.round(4))    # [0.     1.4815 4.0741 0.    ] optimal food quantities
print(round(res_diet.fun, 4))   # 6.2222 minimum cost

# Slack: which constraints are tight at optimality?
# res_lp.slack < 1e-8 means that constraint is binding
binding = np.array(A_ub) @ res_lp.x - np.array(b_ub)
print(binding.round(8))    # [0. 0.], negative slack = room left; 0 = constraint is tight


##--------##
## milp() ##
##--------##
'''
milp(c, constraints=None, integrality=None, bounds=None, options=None)

Mixed-Integer Linear Program:
  min  c . x
  s.t. constraints  (LinearConstraint objects: lb <= A.x <= ub)
       lb <= x <= ub
       x[i] integer where integrality[i] == 1

c            : objective coefficients.
integrality  : 0=continuous, 1=integer, 2=semi-continuous, 3=semi-integer.
bounds       : Bounds(lb, ub).

Uses HiGHS solver. For pure LP use linprog() (simpler interface).
'''

# 0-1 Knapsack: maximise 10x0 + 6x1 + 4x2 s.t. 3x0 + 5x1 + 2x2 <= 5; xi in {0,1}
c_knap    = np.array([-10., -6., -4.])   # negate for maximisation
A_knap    = np.array([[3., 5., 2.]])
con_knap  = LinearConstraint(A_knap, lb=-np.inf, ub=5.)
int_knap  = np.ones(3)                    # all integer
bnd_knap  = Bounds(lb=0., ub=1.)          # binary

res_knap  = milp(c_knap, constraints=con_knap,
                 integrality=int_knap, bounds=bnd_knap)
print(res_knap.x)          # [1. 0. 1.] -> take A and C
print(-res_knap.fun)        # 14.0
print(res_knap.success)     # True

# Mixed: x0 continuous (production amount), x1 binary (facility open/closed)
c_mix  = np.array([-3., -10.])   # maximise 3x0 + 10x1
A_mix  = np.array([[1., 0.], [0., 5.]])
con_mix = LinearConstraint(A_mix, lb=-np.inf, ub=[4., 5.])
int_mix = np.array([0, 1])        # x0 continuous, x1 integer
bnd_mix = Bounds(lb=[0., 0.], ub=[4., 1.])

res_mix  = milp(c_mix, constraints=con_mix,
                integrality=int_mix, bounds=bnd_mix)
print(res_mix.x)     # [4.  1.]
print(-res_mix.fun)  # 22.0


##-------------------------##
## linear_sum_assignment() ##
##-------------------------##
'''
linear_sum_assignment(cost_matrix, maximize=False)

Solves the linear sum assignment problem (LSAP) using the Hungarian algorithm:

  min  sum_i  cost_matrix[i, assignment[i]]
  s.t. each row and column assigned exactly once.

cost_matrix : 2-D array (n_workers, n_jobs). Can be rectangular.
maximize    : if True, maximise instead.

Returns (row_ind, col_ind):
  Optimal assignment: row i -> col col_ind[i].
  Total cost = cost_matrix[row_ind, col_ind].sum()

Time: O(n^3) for n x n. Applications: worker-job matching, tracking, registration.
'''

# Worker-job assignment
cost = np.array([[4, 1, 3],
                 [2, 0, 5],
                 [3, 2, 2]])

row_ind, col_ind = linear_sum_assignment(cost)
print(row_ind, col_ind)             # [0 1 2]  [1 0 2]
print(cost[row_ind, col_ind])       # [1 2 2]
print(cost[row_ind, col_ind].sum()) # 5 (minimum total cost)

# Maximisation: assign workers to maximise total profit
profit = np.array([[9, 2, 7],
                   [3, 6, 1],
                   [4, 5, 8]])
row_max, col_max = linear_sum_assignment(profit, maximize=True)
print(profit[row_max, col_max].sum())  # maximum total profit = 9+6+8 = 23

# Rectangular: 4 workers, 3 jobs (only 3 assignments made)
cost_rect = np.array([[1., 3., 2.],
                       [4., 2., 1.],
                       [3., 1., 4.],
                       [2., 4., 3.]])
row_r, col_r = linear_sum_assignment(cost_rect)
print(row_r, col_r) # [0 1 2] [0 2 1]
print(cost_rect[row_r, col_r].sum()) # 3.0

# Point matching: match two point sets to minimise total distance
pts_A = np.array([[0,0], [1,0], [2,0]], dtype=float)
pts_B = np.array([[2,1], [0.1,0.1], [1,1.2]], dtype=float)
dist_mat = np.linalg.norm(pts_A[:, None] - pts_B[None, :], axis=-1)
row_d, col_d = linear_sum_assignment(dist_mat)
print(dist_mat[row_d, col_d].sum().round(4)) # 2.3414


##------------------------##
## quadratic_assignment() ##
##------------------------##
'''
quadratic_assignment(A, B, method='faq', options=None)

Approximates the Quadratic Assignment Problem (QAP):

  min_P  trace(A^T P^T B P)   over all permutation matrices P

Equivalently: find permutation sigma minimising sum_ij A[i,j] * B[sigma(i), sigma(j)].

Applications: graph matching, facility layout, chip placement, network alignment.
NP-hard: heuristics only.

method='faq'  : Fast Approximate QAP (default). Gradient on continuous relaxation + rounding.
method='2opt' : Local search: iteratively swap pairs to reduce cost.
'''

rng_qa = np.random.default_rng(3)
n_qa   = 5
A_qa   = rng_qa.integers(0, 10, (n_qa, n_qa)).astype(float)
A_qa   = (A_qa + A_qa.T) / 2     # symmetric (undirected graph)
perm_true = np.array([2, 0, 4, 1, 3])
noise  = rng_qa.normal(0, 0.5, (n_qa, n_qa))
B_qa   = A_qa[np.ix_(perm_true, perm_true)] + noise
B_qa   = (B_qa + B_qa.T) / 2

res_qa = quadratic_assignment(A_qa, B_qa, method='faq',
                               options={'maximize': False, 'rng': 3})
print(res_qa.col_ind)   # [1 4 2 3 0] recovered permutation
print(res_qa.fun)       # 316.71576192033615 objective value (lower is better)

res_qa_2opt = quadratic_assignment(A_qa, B_qa, method='2opt',
                                    options={'rng': 3})
print(res_qa_2opt.fun) # 325.28359010373157


# =========================================================================================
#  PART F — UTILITIES & LEGACY 
# =========================================================================================

##----------------------------##
## approx_fprime / check_grad ##
##----------------------------##
'''
approx_fprime(xk, f, epsilon=sqrt(eps))
  Finite-difference approximation of the gradient of f at xk.
  Default epsilon ~= 1.49e-8 (sqrt of machine epsilon).

check_grad(func, grad, x0, *args, epsilon=..., direction='all')
  Compares analytic grad(x) against finite differences of func(x).
  Returns the Frobenius norm of the difference.
  Use to verify gradient implementations before passing to minimisers.
  Rule of thumb: result < 1e-5 is acceptable.
'''

x_test       = np.array([1., 2., 3.])
fd_grad      = approx_fprime(x_test, rosen)
analytic_grad= rosen_der(x_test)

print(fd_grad.round(4)) # [-400. 1002. -200.]
print(analytic_grad.round(4)) # [-400. 1002. -200.]
print(np.allclose(fd_grad, analytic_grad, atol=1e-4))  # True

# check_grad: returns gradient error
err_ok = check_grad(rosen, rosen_der, x_test)
print(f"Correct gradient error: {err_ok:.2e}")   # 2.70e-05 very small

# Detecting a wrong gradient
def bad_grad(x):
    return rosen_der(x) * 2.0   # intentionally wrong (factor of 2)

err_bad = check_grad(rosen, bad_grad, x_test)
print(f"Wrong gradient error:   {err_bad:.2e}")   # 1.10e+03 much larger

# Useful pattern: always check_grad before using analytic gradients in minimize()
def my_func(x):
    return np.sin(x[0]) * np.exp(-x[1]**2)

def my_grad(x):
    return np.array([np.cos(x[0]) * np.exp(-x[1]**2),
                     -2*x[1] * np.sin(x[0]) * np.exp(-x[1]**2)])

print(f"Custom gradient error: {check_grad(my_func, my_grad, [1., 0.5]):.2e}")  # 1.09e-08 small ✓

##--------------##
## rosen family ##
##--------------##
'''
rosen(x)          : Rosenbrock function. sum [100*(x[i+1]-x[i]^2)^2 + (1-x[i])^2].
                    Minimum = 0 at x = [1, 1, ..., 1].

rosen_der(x)      : Exact gradient (analytically derived).
rosen_hess(x)     : Exact Hessian matrix (tridiagonal structure).
rosen_hess_prod(x, p): Hessian-vector product H(x)*p without forming H explicitly.

Used as a standard benchmark because the narrow curved valley makes
convergence hard for gradient methods — tests step-size adaptation.
'''

x_min_rosen = np.ones(5)
print(rosen(x_min_rosen))               # 0.0  at the minimum
print(rosen_der(x_min_rosen))           # [0. 0. 0. 0. 0.]  gradient=0 at minimum

# Eigenvalues of Hessian confirm it is a positive definite minimum
print(np.linalg.eigvalsh(rosen_hess(x_min_rosen)).round(2))
# [5.00000e-01 3.54630e+02 7.54590e+02 1.24910e+03 1.64918e+03]
# all positive

# Hessian-vector product matches H*p
x_near = np.array([1.1, 0.9, 1.0, 1.0, 1.0])
p_test = np.ones(5)
hp = rosen_hess_prod(x_near, p_test)
print(np.allclose(hp, rosen_hess(x_near) @ p_test, atol=1e-10))  # True

# rosen accepts arrays of any length
for n in [2, 5, 10, 50]:
    res_r = minimize(rosen, np.zeros(n), method='L-BFGS-B', jac=rosen_der)
    print(f"n={n:2d}  fun={res_r.fun:.2e}  success={res_r.success}")
# n= 2  fun=1.04e-13  success=True
# n= 5  fun=1.86e-12  success=True
# n=10  fun=1.29e-10  success=True
# n=50  fun=4.17e-10  success=True

##-----------##
## bracket() ##
##-----------##
'''
bracket(func, xa=0.0, xb=1.0, args=(), grow_limit=110.0, maxiter=1000)

Finds a bracket triple (xa, xb, xc) such that:
  f(xa) > f(xb),  f(xb) < f(xc),  xa < xb < xc

i.e., xb is bracketed as a local minimum.
Returns (xa, xb, xc, fa, fb, fc, funcalls).

Use before minimize_scalar when you do not know where the minimum is.
'''

def f_bracket(x):
    return (x - 3)**2 + 2   # minimum at x = 3

xa, xb, xc, fa, fb, fc, ncalls = bracket(f_bracket, xa=0., xb=1.)
print(xa, xb, xc)         # 2.6180339999999998 3.0 3.6180339748440002, bracket containing x=3
print(fa > fb, fc > fb)   # True True -- fb is the smallest

# Pass the bracket to minimize_scalar
res_ms = minimize_scalar(f_bracket, bracket=(xa, xb, xc), method='brent')
print(res_ms.x.round(6))   # 3.0  ✓


##------------##
## Legacy API ##
##------------##
'''
fsolve(func, x0, **)  : Legacy root-finding for F: R^n -> R^n (MINPACK HYBRD).
                        Returns x array directly (no result object).
                        Modern equivalent: root(func, x0, method='hybr')

fmin(func, x0, **)    : Legacy Nelder-Mead minimisation.
                        Returns x array directly.
                        Modern equivalent: minimize(func, x0, method='Nelder-Mead')

leastsq(func, x0, **) : Legacy nonlinear LS (MINPACK LMDIF).
                        Returns (x, cov_x, infodict, mesg, ier).
                        Modern equivalent: least_squares(func, x0)

Key differences from modern API:
  - fsolve / fmin return arrays not OptimizeResult.
  - leastsq returns raw covariance; least_squares returns res.jac for you to compute it.
  - No bounds support in fsolve / fmin (use minimize/root directly).
'''

# fsolve: same system as root() example
x_fsolve = fsolve(F_system, x0=[0.5, 0.5])
print(x_fsolve.round(8))  # [0.70710678 0.70710678] same root as root() above

# fsolve with analytic Jacobian (fprime=)
x_fsolve_jac = fsolve(F_system, x0=[0.5, 0.5], fprime=J_system)
print(np.allclose(x_fsolve, x_fsolve_jac))  # True

# fmin: Nelder-Mead
x_fmin = fmin(rosen, x0_5, xtol=1e-8, ftol=1e-8, maxiter=100000, disp=False)
print(x_fmin.round(4))    # [1. 1. 1. 1. 1.]
print(type(x_fmin))        # ndarray — not OptimizeResult

# leastsq: exponential model (same data as least_squares example)
def res_leastsq_fn(params, t, y):
    return residuals_exp(params, t, y)

popt_lsq, cov_x, info, mesg, ier = leastsq(res_leastsq_fn, x0=[1., 1.],
                                             args=(t_data, y_data),
                                             full_output=True)
print(popt_lsq.round(4))    # ~[3.5, 1.2]
print(ier in [1,2,3,4])      # True -> converged

# Compute parameter std errors from cov_x
residuals_sol = residuals_exp(popt_lsq, t_data, y_data)
sigma2 = (residuals_sol**2).sum() / (len(t_data) - len(popt_lsq))
if cov_x is not None:
    perr_lsq = np.sqrt(np.diag(cov_x) * sigma2)
    print(perr_lsq.round(5))
# [0.05801 0.03112]
# parameter standard errors
# Note: curve_fit handles this automatically and is preferred.
