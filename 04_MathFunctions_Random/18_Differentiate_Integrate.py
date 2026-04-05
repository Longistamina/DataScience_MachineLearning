'''
scipy.differentiate  +  scipy.integrate
========================================
Primary focus: scipy. NumPy supportive parts at the end of each major block.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART A — scipy.differentiate  (finite-difference, black-box)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. derivative()     : scalar or array-valued; any order; Richardson extrapolation.
2. jacobian()       : full Jacobian matrix of f: Rⁿ → Rᵐ.
3. hessian()        : full Hessian matrix of f: Rⁿ → R.

NumPy supportive (discrete data, no function object):
   np.gradient()   : finite differences on sampled arrays (1-D or N-D).
   np.diff()       : forward differences of an array.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART B — scipy.integrate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4.  quad()               : 1-D adaptive quadrature; handles singularities/infinity.
5.  quad_vec()           : adaptive quadrature for vector-valued integrands.
6.  cubature()           : N-D adaptive cubature (new in 1.15).
7.  dblquad() / tplquad(): convenience wrappers for 2-D and 3-D integrals.
8.  nquad()              : N-D adaptive quadrature with per-axis ranges.
9.  tanhsinh()           : double-exponential rule; excellent for endpoint singularities.
10. fixed_quad()         : fixed-order Gauss-Legendre quadrature.
11. newton_cotes()       : Newton-Cotes weights for equally-spaced nodes.
12. lebedev_rule()       : spherical quadrature on S² (angular integrals).
13. qmc_quad()           : Quasi-Monte Carlo cubature (Sobol') in N-D.
14. nsum()               : convergent finite or infinite series.

Integrating fixed samples:
15. trapezoid() / cumulative_trapezoid()
16. simpson()   / cumulative_simpson()
17. romb()

ODE — initial value problems:
18. solve_ivp()          : modern IVP solver; methods RK23/RK45/DOP853/Radau/BDF/LSODA.
19. ODE methods guide    : choosing the right method.

ODE — boundary value problems:
20. solve_bvp()          : two-point BVP on [a, b].

Legacy ODE API:
21. odeint()             : legacy LSODA wrapper (still widely used in older code).

NumPy supportive (samples-based):
22. np.trapezoid()       : trapezoidal rule on array; identical to trapezoid().
23. np.cumsum() pattern  : manual cumulative integration using cumsum + dx.
'''

import numpy as np
import scipy.differentiate as sd
from scipy.integrate import (
    quad, quad_vec, dblquad, tplquad, nquad,
    tanhsinh, fixed_quad, newton_cotes, lebedev_rule, qmc_quad,
    nsum, trapezoid, cumulative_trapezoid,
    simpson, cumulative_simpson, romb,
    solve_ivp, solve_bvp, odeint,
)
try:
    from scipy.integrate import cubature
    _has_cubature = True
except ImportError:
    _has_cubature = False

# ── Common test functions ────────────────────────────────────────────────────────────────────────
def f1(x):    
  return np.sin(x)           # derivative: cos(x),   antiderivative: -cos(x)

def f2(x):    
  return np.exp(-x**2)       # Gaussian;  ∫₋∞∞ = √π

def f3(x, y): 
  return np.sin(x) * np.cos(y)  # 2-D integrand

def g_vec(x): 
  return np.array([np.sin(x), np.cos(x), np.exp(-x)])  # R → R³


#-------------------------------------------------------------------------------------------------#
#════════════════════════════════  PART A — DIFFERENTIATE  ═══════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

##################
## derivative() ##
##################
'''
scipy.differentiate.derivative(f, x, order=1, tolerances=None, maxiter=10, step=None)

Numerically differentiates a scalar (or element-wise array-valued) function f at x.

How it works:
  - Uses central finite differences with step-size h.
  - Applies Richardson extrapolation to accelerate convergence.
  - Automatically halves h until the tolerance is met or maxiter is exhausted.

Returns a result object with:
  res.df      : estimated derivative value(s).
  res.error   : estimated absolute error.
  res.success : True if tolerance was achieved.
  res.status  : 0 = success, -1 = maxiter reached, 1 = NaN/inf encountered.

order=1 (default): first derivative.  order=2: second derivative.  etc.
tolerances: dict with keys 'atol' and/or 'rtol' (defaults are tight).

Compared to np.gradient: works on black-box functions, not pre-sampled arrays.
Compared to symbolic diff: no symbolic expression needed; pure numerical.
'''

# First derivative of sin(x) at x = π/4  → should be cos(π/4) ≈ 0.7071
res = sd.derivative(f1, np.pi / 4)
print(res.df.round(8), res.error)
# 0.70710678  very small error

# Vectorised: differentiate at many points simultaneously
x_arr = np.array([0., np.pi/6, np.pi/4, np.pi/3, np.pi/2])
res_arr = sd.derivative(f1, x_arr)
print(res_arr.df.round(6))
# [1.       0.866025 0.707107 0.5      0.      ]  ≈ cos(x)

print(np.allclose(res_arr.df, np.cos(x_arr), atol=1e-8))
# True

# Second derivative: d²/dx² sin(x) = -sin(x)
res2 = sd.derivative(f1, np.pi / 4, order=2)
print(res2.df.round(6))
# -0.707107  ≈ -sin(π/4)

# Third derivative: d³/dx³ sin(x) = -cos(x)
res3 = sd.derivative(f1, np.pi / 4, order=3)
print(res3.df.round(6))
# -0.707107  ≈ -cos(π/4)

# Non-smooth / noisy function — check error estimate
def noisy(x): 
  return x**3 + 1e-6 * np.sin(1000 * x)  # true derivative ≈ 3x²

res_noisy = sd.derivative(noisy, 2.0)
print(res_noisy.df.round(4))
# ≈ 12.0  (3·2² = 12)

# Function with parameters via args
def f_param(x, a, b): 
  return a * np.sin(b * x)

res_p = sd.derivative(f_param, 1.0, args=(3.0, 2.0))   # d/dx [3sin(2x)] at x=1 = 6cos(2)
print(res_p.df.round(6))
# ≈ 6·cos(2) ≈ -2.4969

# Checking convergence failure — step into flat region
res_flat = sd.derivative(lambda x: np.ones_like(x), 0.0)
print(res_flat.df, res_flat.success)
# 0.0  True  (flat function: derivative is exactly 0)

# Custom tolerances: relax tolerances for a rough estimate (fewer function calls)
res_rough = sd.derivative(f1, 1.0, tolerances={'rtol': 1e-4})
print(res_rough.df.round(4))
# ≈ 0.5403  (cos(1))

################
## jacobian() ##
################
'''
scipy.differentiate.jacobian(f, x, tolerances=None, maxiter=10)

Numerically estimates the Jacobian matrix of f: Rⁿ → Rᵐ at point x.

The Jacobian J has shape (m, n):   J[i, j] = ∂fᵢ/∂xⱼ

Uses the same Richardson-extrapolated finite-difference approach as derivative(),
but perturbs each input dimension independently.

x     : 1-D array of length n (input point).
result: res.df has shape (m, n).

Applications:
  - Gradient descent, Newton's method (Jacobian = gradient when m=1).
  - Sensitivity analysis: how much does output i change per unit change in input j?
  - Computing linearisations of nonlinear systems around an operating point.
'''

# f: R² → R²,  f(x,y) = [x²y,  x + sin(y)]
def f_2d(xy): # xy here means the input should be a 1-D array of length 2 [x y], or a 2-D array of shape (k, 2) for vectorised inputs. The function should return an array of shape (k, 2) where each row is [x²y, x + sin(y)] evaluated at the corresponding input row.
    x, y = xy # unpack input
    return np.array([x**2 * y, x + np.sin(y)])

x0 = np.array([2.0, np.pi / 3])
res_jac = sd.jacobian(f_2d, x0)
J = res_jac.df   # shape (2, 2)

print(J.round(6))
# [[4.18879 4.     ]
#  [1.      0.5    ]]
# Analytic Jacobian at (2, π/3):
#   [∂(x²y)/∂x         ∂(x²y)/∂y ] = [2xy    x² ]   = [2·2·π/3    4      ] = [4.189  4.   ]
#   [∂(x+sin y)/∂x  ∂(x+sin y)/∂y] = [1     cosy]   = [1         cos(π/3)] = [1.     0.5  ]

print(np.allclose(J, [[2*2*(np.pi/3), 4.], [1., np.cos(np.pi/3)]], atol=1e-6))
# True

# f: R³ → R  (gradient is a 1x3 Jacobian)
def f_scalar(xyz):
    x, y, z = xyz
    return np.atleast_1d(x**2 + y**2 + z**2)   # sphere function; ∇f = 2[x, y, z]

x1 = np.array([1.0, 2.0, 3.0])
res_grad = sd.jacobian(f_scalar, x1)
print(res_grad.df)
# [[2. 4. 6.]]   ≈ 2·[1, 2, 3]  ✓

# Jacobian of a vector function R → R³
def f_curve(t):
    return np.array([np.cos(t[0]), np.sin(t[0]), t[0]])   # helix tangent

res_tang = sd.jacobian(f_curve, np.array([np.pi / 4]))
print(res_tang.df.round(6))
# [[-sin(π/4)], [cos(π/4)], [1.]] = [[-0.7071], [0.7071], [1.]]

# Check error estimates
print(res_jac.error.round(12))
# tiny — Richardson extrapolation is highly accurate

###############
## hessian() ##
###############
'''
scipy.differentiate.hessian(f, x, tolerances=None, maxiter=10)

Numerically estimates the Hessian matrix of f: Rⁿ → R at point x.

The Hessian H has shape (n, n):   H[i, j] = ∂²f / ∂xᵢ ∂xⱼ

For a smooth f, H is symmetric (Schwarz's theorem).
Uses second-order mixed finite differences with Richardson extrapolation.

Applications:
  - Optimisation: Newton's method uses H to find step direction.
  - Curvature analysis: eigenvalues of H determine saddle points vs minima.
  - Uncertainty quantification: Laplace approximation uses -H⁻¹ as covariance.
'''

# f(x,y) = sin(x)·cos(y)
#   ∂²f/∂x²   = -sin(x)·cos(y)
#   ∂²f/∂y²   = -sin(x)·cos(y)
#   ∂²f/∂x∂y  = -cos(x)·sin(y)
def f_2d_scalar(xy):
    x, y = xy
    return np.sin(x) * np.cos(y)

x0_h = np.array([np.pi / 4, np.pi / 3])
res_hess = sd.hessian(f_2d_scalar, x0_h)
H = res_hess.ddf   # shape (2, 2)

print(H.round(6))
# [[-0.353553 -0.612372]
#  [-0.612372 -0.353553]]

# Analytic Hessian at (π/4, π/3):
H_analytic = np.array([
    [-np.sin(np.pi/4) * np.cos(np.pi/3),  -np.cos(np.pi/4) * np.sin(np.pi/3)],
    [-np.cos(np.pi/4) * np.sin(np.pi/3),  -np.sin(np.pi/4) * np.cos(np.pi/3)],
])
print(H_analytic.round(6))
# [[-0.353553 -0.612372]
#  [-0.612372 -0.353553]]

print(np.allclose(H, H_analytic, atol=1e-5))
# True

# Hessian is symmetric
print(np.allclose(H, H.T, atol=1e-10))
# True

# Optimisation context: identify local minimum of f(x,y) = x² + 2y²
def bowl(xy):
    x, y = xy
    return x**2 + 2 * y**2

res_h_bowl = sd.hessian(bowl, np.array([0., 0.]))
H_bowl = res_h_bowl.ddf
print(H_bowl.round(4))
# [[2. 0.]
#  [0. 4.]]    (exact Hessian of x² + 2y²)

eigenvalues = np.linalg.eigvalsh(H_bowl)
print(eigenvalues)
# [2. 4.]   both positive → confirmed local minimum at (0,0)

# N-D Hessian
def f_3d(xyz):
    x, y, z = xyz
    return x**2 + 3 * y**2 + 5 * z**2 + 2 * x * y

res_h3 = sd.hessian(f_3d, np.array([1., 1., 1.]))
print(res_h3.ddf.round(4))
# [[2. 2. 0.]
#  [2. 6. 0.]
#  [0. 0. 10.]]   ∂²f/∂x²=2, ∂²f/∂y²=6, ∂²f/∂z²=10, ∂²f/∂x∂y=2


#-------------------------------------------------------------------------------------------------#
#--------------------------- NumPy supportive — discrete differentiation ------------------------#
#-------------------------------------------------------------------------------------------------#

###################
## np.gradient() ##
###################
'''
np.gradient(f, *varargs, axis, edge_order) computes the gradient of a sampled array.

For 1-D arrays: returns the numerical derivative using 2nd-order central differences
  in the interior, and 1st or 2nd-order one-sided differences at the boundaries.

For N-D arrays: returns a list of arrays, one per axis (partial derivative along each axis).

varargs : spacing — scalar (uniform dx) or 1-D array of non-uniform sample positions.
edge_order : 1 or 2 (default 2) — accuracy order at boundaries.

Use np.gradient when you have sampled data (not a function object).
Use sd.derivative / sd.jacobian when you have a callable function.
'''

# 1-D: derivative of sin(x) from samples
x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)
dy_dx = np.gradient(y, x)   # x provides the non-uniform (actually uniform here) spacing

print(np.abs(dy_dx - np.cos(x)).max().round(5))
# 0.00017
# very small — central differences on fine grid ≈ exact derivative

# Uniform spacing: just pass the scalar dx
dx = x[1] - x[0]
dy_dx_uniform = np.gradient(y, dx)
print(np.allclose(dy_dx, dy_dx_uniform, atol=1e-12))
# True

# Second derivative via two calls to np.gradient
d2y_dx2 = np.gradient(np.gradient(y, x), x)
print(np.abs(d2y_dx2 - (-np.sin(x))).max().round(4))
# small (slightly larger error due to two successive finite-difference passes)

# 2-D gradient: partial derivatives of f(x,y) = sin(x)·cos(y)
x2 = np.linspace(0, np.pi, 30)
y2 = np.linspace(0, np.pi, 30)
X, Y = np.meshgrid(x2, y2, indexing='ij')
F = np.sin(X) * np.cos(Y)

grad_x, grad_y = np.gradient(F, x2, y2)   # one array per axis

print(np.abs(grad_x - np.cos(X) * np.cos(Y)).max().round(4))  # 0.002 -> ∂F/∂x = cos(x)cos(y)
print(np.abs(grad_y - (-np.sin(X) * np.sin(Y))).max().round(4))  # 0.054 -> ∂F/∂y = -sin(x)sin(y)
# both small

###############
## np.diff() ##
###############
'''
np.diff(a, n=1, axis=-1, prepend, append) computes forward differences.

n=1 (default): aᵢ₊₁ - aᵢ   (output length = len(a) - 1)
n=2           : second differences (= forward difference of forward differences)
n=k           : k-th order forward differences  (output length = len(a) - k)

Less accurate than np.gradient (first-order vs second-order), but useful for:
  - Computing increments (dx, dy) between consecutive samples.
  - Finite-difference approximations where one-sided differences are acceptable.
  - Detecting jumps or discontinuities (where |diff| is large).
'''

x_d = np.array([0., 1., 3., 6., 10.])   # non-uniform spacing
y_d = x_d**2

dy = np.diff(y_d)    # first differences: Δy = y[i+1] - y[i]
dx = np.diff(x_d)    # spacing:           Δx = x[i+1] - x[i]
dydx_fd = dy / dx    # forward-difference derivative ≈ dy/dx

print(dydx_fd.round(2))
# [ 1.  4.  9. 16.]   (forward differences of x² at midpoints ≈ 2x_mid)

# Second differences
print(np.diff(y_d, n=2))
# [ 7. 19. 37.]   Δ²y = non-uniform; for uniform Δx: Δ²y/Δx² → f''


#-------------------------------------------------------------------------------------------------#
#════════════════════════════════════  PART B — INTEGRATE  ═══════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------------#
#---------------------------------- 4. quad() — 1-D adaptive -------------------------------------#
#-------------------------------------------------------------------------------------------------#

############
## quad() ##
############
'''
quad(func, a, b) computes ∫ₐᵇ func(x)dx using adaptive Gaussian quadrature (QUADPACK).

Returns: (result, abserr)
  result : estimated integral value.
  abserr : estimated absolute error.

Limits a, b can be np.inf or -np.inf for semi-infinite or infinite domains.
args : extra arguments passed to func as func(x, *args).
full_output=True : returns extra diagnostic dict (neval, last, etc.).
limit : max number of adaptive subintervals (default 50; increase for oscillatory f).
epsabs, epsrel : absolute and relative error tolerances (defaults 1.49e-8).
points : list of known discontinuity/singularity locations — tell quad to split there.
weight / wvar : built-in weight functions (Cauchy, algebraic endpoint singularity, etc.).

quad is the go-to for 1-D integration of smooth or mildly singular functions.
'''

# Basic: ∫₀ᵖⁱ sin(x)dx = 2.0
val, err = quad(f1, 0, np.pi)
print(round(val, 8), err)
# 2.0  ~2.2e-14

# Infinite limits: ∫₋∞∞ exp(-x²)dx = √π
val_inf, err_inf = quad(f2, -np.inf, np.inf)
print(round(val_inf, 8), round(np.sqrt(np.pi), 8))
# 1.77245385  1.77245385  ✓

# Semi-infinite: ∫₀∞ x·exp(-x)dx = 1  (Γ(2) = 1)
val_semi, err_semi = quad(lambda x: x * np.exp(-x), 0, np.inf)
print(round(val_semi, 8))
# 1.0

# With arguments: ∫₀ᵖⁱ a·sin(b·x) dx = a*(1-cos(bπ))/b
val_args, _ = quad(lambda x, a, b: a * np.sin(b * x), 0, np.pi, args=(3., 2.))
print(round(val_args, 6))
# 0.0
# 3*[-cos(2x)/2]₀ᵖⁱ = 3*(−cos(2π)+cos(0))/2 = 3*(−1+1)/2 = 0

# Singularity handling: ∫₀¹ 1/√xdx = 2.0  (integrable singularity at x=0)
val_sing, err_sing = quad(lambda x: 1.0 / np.sqrt(x), 0, 1,
                          points=[0.01])   # hint: singularity near 0
print(round(val_sing, 6))
# ≈ 2.0

# Better singularity handling with weight='alg'
# ∫₀¹ x^(-0.5) dx = 2.0 via algebraic endpoint weight
val_w, err_w = quad(lambda x: 1.0, 0, 1, weight='alg', wvar=(-0.5, 0))
print(round(val_w, 6))
# ≈ 2.0

# Full output: diagnostic information
val_full, err_full, info = quad(f1, 0, np.pi, full_output=True)
print(info['neval'])     # number of function evaluations
# 21  (typical for smooth integrand)

# Complex-valued integrand: ∫₀ᵖⁱ e^{ix}dx = [e^{ix}/i]₀ᵖⁱ = (e^{iπ}-1)/i = -2i/i... = 2i/1
def f_complex(x): 
  return np.exp(1j * x)   # split into real and imag

val_re, _ = quad(lambda x: np.exp(1j * x).real, 0, np.pi)
val_im, _ = quad(lambda x: np.exp(1j * x).imag, 0, np.pi)
print(complex(round(val_re,4), round(val_im,4)))
# (-0+2j)   = ∫₀ᵖⁱ e^{ix}dx  ✓


#-------------------------------------------------------------------------------------------------#
#------------------------------- 5. quad_vec() — vector integrand --------------------------------#
#-------------------------------------------------------------------------------------------------#

################
## quad_vec() ##
################
'''
quad_vec(f, a, b) integrates a vector-valued function f: R → Rᵐ (or any shape).

f must accept a scalar x and return an array.
Returns: (result, abserr) where both have the same shape as f's output.

Use when:
  - Integrating many scalar integrands simultaneously (parameter sweeps).
  - f returns an array naturally (e.g. feature vector, spectral coefficients).

Compared to looping quad() calls:
  - More efficient (shared adaptive mesh across all components).
  - Fewer total function evaluations.
'''

# Integrate [sin(x), cos(x), exp(-x)] from 0 to π
val_vec, err_vec = quad_vec(g_vec, 0, np.pi)
print(val_vec.round(6))
# [2.0       0.0       0.865]
# ∫₀ᵖⁱ sin = 2, ∫₀ᵖⁱ cos = 0, ∫₀ᵖⁱ e^{-x} = 1 - e^{-π} ≈ 0.9179

true_vec = np.array([2., 0., 1 - np.exp(-np.pi)])
print(np.allclose(val_vec, true_vec, atol=1e-6))
# True

# Parameter sweep: ∫₀¹ x^n dx = 1/(n+1) for n = 0,1,...,9
def power_vec(x):
    ns = np.arange(10, dtype=float)
    return x**ns   # shape (10,)

val_sweep, _ = quad_vec(power_vec, 0, 1)
print(val_sweep.round(6))
# [1.     0.5    0.333  0.25   0.2    0.167  0.143  0.125  0.111  0.1  ]
# = 1/(n+1)  ✓

# 2-D output: integrate a matrix-valued function
def matrix_func(t):
    return np.array([[np.cos(t), -np.sin(t)],
                     [np.sin(t),  np.cos(t)]])   # rotation matrix R(t)

val_mat, _ = quad_vec(matrix_func, 0, np.pi / 2)
print(val_mat.round(6))
# [[1.  -1.]
#  [1.   1.]]  = ∫₀^{π/2} R(t) dt


#-------------------------------------------------------------------------------------------------#
#--------------------------------- 6. cubature() — N-D adaptive ----------------------------------#
#-------------------------------------------------------------------------------------------------#

################
## cubature() ##
################
'''
cubature(f, a, b, rule, rtol, atol, max_subdivisions) computes ∫_[a,b] f(x) dx
over a d-dimensional box [a₁,b₁] x [a₂,b₂] x ... x [aₐ,bₐ].

f must accept x of shape (..., d) — last axis is the d spatial dimensions.
a, b : 1-D arrays of lower and upper bounds (length d).

rule : quadrature rule per dimension. Options include:
  'gauss-kronrod'  (1-D only),
  'genz-malik'     (d ≥ 2, default for d > 1),
  'simpson'        (any d, low-order).

Returns: res with res.integral (scalar or array) and res.error.

New in scipy 1.15 — replaces manual nquad calls for smooth N-D integrands.
Advantage over nquad: shares the adaptive mesh across all output components.
'''

if _has_cubature:
    # 2-D: ∫₀¹ ∫₀¹ (x² + y²) dx dy = 2/3
    def f_cub_2d(xy):
        return xy[..., 0]**2 + xy[..., 1]**2   # shape (...,)

    res_cub = cubature(f_cub_2d, a=[0., 0.], b=[1., 1.])
    print(res_cub.estimate.round(8))
    # 0.66666667  ≈ 2/3  ✓

    # 3-D: ∫₀ᵖⁱ ∫₀ᵖⁱ ∫₀ᵖⁱ sin(x)sin(y)sin(z) dx dy dz = 8
    def f_cub_3d(xyz):
        return np.sin(xyz[..., 0]) * np.sin(xyz[..., 1]) * np.sin(xyz[..., 2])

    res_3d = cubature(f_cub_3d, a=[0.]*3, b=[np.pi]*3, rtol=1e-6)
    print(res_3d.estimate.round(6))
    # 8.0  (2³ = 8, since ∫₀ᵖⁱ sin = 2)

    # Vector-valued: cubature shares mesh for all output components
    def f_cub_vec(xy):
        return np.stack([xy[..., 0]**2, xy[..., 1]**2], axis=-1)

    res_vec = cubature(f_cub_vec, a=[0., 0.], b=[1., 1.])
    print(res_vec.estimate.round(6))
    # [0.333  0.333]   ✓  (∫₀¹∫₀¹ x² = 1/3, same for y²)


#-------------------------------------------------------------------------------------------------#
#------------------------- 7. dblquad() / tplquad() — iterated integrals -------------------------#
#-------------------------------------------------------------------------------------------------#

###############
## dblquad() ##
###############
'''
dblquad(func, a, b, gfun, hfun) computes ∫ₐᵇ ∫_{g(x)}^{h(x)} func(y, x) dy dx

Note argument order: func(y, x) — inner variable first.
gfun, hfun : callables giving the y-limits as functions of x, or constants.
Returns (result, abserr).

Use for non-rectangular domains where y-limits depend on x.
'''

# ∫₀¹ ∫₀ˣ y dy dx = ∫₀¹ x²/2 dx = 1/6
val_dbl, err_dbl = dblquad(lambda y, x: y,
                            0, 1,         # x from 0 to 1
                            0, lambda x: x)  # y from 0 to x
print(round(val_dbl, 8))
# 0.16666667  = 1/6  ✓

# Rectangular: ∫₀ᵖⁱ ∫₀ᵖⁱ sin(x)cos(y) dy dx = 0
val_rect, _ = dblquad(lambda y, x: np.sin(x) * np.cos(y),
                       0, np.pi, 0, np.pi)
print(round(val_rect, 8))
# 0.0   (∫₀ᵖⁱ cos(y) dy = 0)

# Disc: ∫∫_{x²+y²≤1} 1 dx dy = π  (integrate over unit disc)
# y-limits: -√(1-x²) to +√(1-x²)
val_disc, _ = dblquad(lambda y, x: 1.0,
                       -1., 1.,
                       lambda x: -np.sqrt(1 - x**2),
                       lambda x:  np.sqrt(1 - x**2))
print(round(val_disc, 6))
# 3.141593  = π  ✓

###############
## tplquad() ##
###############
'''
tplquad(func, a, b, gfun, hfun, qfun, rfun) computes a triple integral.

∫ₐᵇ ∫_{g(x)}^{h(x)} ∫_{q(x,y)}^{r(x,y)} func(z, y, x) dz dy dx

Note argument order: func(z, y, x) — innermost variable first.
'''

# ∫₀¹ ∫₀¹ ∫₀¹ xyz dz dy dx = (1/2)³ = 1/8
val_tpl, err_tpl = tplquad(lambda z, y, x: x * y * z,
                             0, 1,    # x limits
                             0, 1,    # y limits
                             0, 1)    # z limits
print(round(val_tpl, 8))
# 0.125  = 1/8  ✓

# Volume of a sphere: ∫₋₁¹ ∫_{-√(1-x²)}^{√(1-x²)} ∫_{-√(1-x²-y²)}^{√(1-x²-y²)} dz dy dx = 4π/3
from math import sqrt as msqrt
val_sphere, _ = tplquad(
    lambda z, y, x: 1.0,
    -1., 1.,
    lambda x: -msqrt(max(1 - x**2, 0)),
    lambda x:  msqrt(max(1 - x**2, 0)),
    lambda x, y: -msqrt(max(1 - x**2 - y**2, 0)),
    lambda x, y:  msqrt(max(1 - x**2 - y**2, 0)),
)
print(round(val_sphere, 5))
# 4.18879  ≈ 4π/3  ✓


#-------------------------------------------------------------------------------------------------#
#--------------------------------- 8. nquad() — N-D nested quad ----------------------------------#
#-------------------------------------------------------------------------------------------------#

#############
## nquad() ##
#############
'''
nquad(func, ranges) integrates func over N dimensions using nested quad calls.

func : callable; arguments must be in innermost-first order func(xₙ, ..., x₁).
ranges : list of 2-tuples (aᵢ, bᵢ) or callables (for variable limits).
opts   : list of dicts passed to each inner quad call; use to override limit, epsabs, etc.

For smooth, moderate-dimension integrals. Suffers from the curse of dimensionality:
cost is exponential in d (each dimension adds a factor of ~limit calls to quad).
Use cubature() or qmc_quad() for d ≥ 3.
'''

# 3-D: ∫₀¹ ∫₀¹ ∫₀¹ (x+y+z) dz dy dx = 3/2
val_nq, err_nq = nquad(lambda z, y, x: x + y + z, [[0,1], [0,1], [0,1]])
print(round(val_nq, 8))
# 1.5  ✓

# Variable limits: ∫₀¹ ∫₀ˣ ∫₀ʸ z dz dy dx = 1/24
val_nq_var, _ = nquad(
    lambda z, y, x: z,
    [lambda y, x: (0, y),   # z: 0 to y
     lambda x:   (0, x),    # y: 0 to x
     (0, 1)]                # x: 0 to 1
)
print(round(val_nq_var, 8))
# 0.04166667  = 1/24  ✓


#-------------------------------------------------------------------------------------------------#
#------------------------ 9. tanhsinh() — double-exponential quadrature --------------------------#
#-------------------------------------------------------------------------------------------------#

################
## tanhsinh() ##
################
'''
tanhsinh(f, a, b) evaluates ∫ₐᵇ f(x) dx using the tanh-sinh (double-exponential) rule.

The substitution x = tanh(π/2 · sinh(t)) clusters sample points near the endpoints,
making the method extremely effective for functions with endpoint singularities.

Returns a result object with .integral and .error (same interface as derivative/jacobian).
a, b can be infinite (np.inf / -np.inf).
maxlevel : refinement levels (each level doubles the number of nodes; default 10).

Advantages over quad for:
  - Endpoint singularities (e.g. ∫₀¹ log(x) dx, ∫₀¹ x^{-0.5} dx).
  - Nearly singular integrands near the endpoints.
  - Functions smooth on the open interval but not at the boundaries.
  - Vectorised functions (tanhsinh naturally evaluates at arrays of x).
'''

# ∫₀¹ log(x) dx = -1  (integrable singularity at x=0)
res_ts = tanhsinh(np.log, 0, 1)
print(res_ts.integral.round(8), res_ts.error)
# -1.0   tiny error

# Compare with quad (needs a hint for the singularity)
val_quad_log, err_quad_log = quad(np.log, 0, 1, limit=100)
print(round(val_quad_log, 8), err_quad_log)
# -1.0   also works, but tanhsinh is often more robust

# ∫₀¹ 1/√x dx = 2  (stronger singularity)
res_sqrt = tanhsinh(lambda x: 1.0 / np.sqrt(x), 0, 1)
print(res_sqrt.integral.round(6))
# 2.0  ✓

# ∫₋∞∞ exp(-x²) dx = √π
res_gauss = tanhsinh(f2, -np.inf, np.inf)
print(res_gauss.integral.round(8), round(np.sqrt(np.pi), 8))
# 1.77245385  1.77245385  ✓

# ∫₀¹ sin(x)/x dx  (removable singularity at 0; handled by double-exponential clustering)
res_sinc = tanhsinh(lambda x: np.where(x == 0, 1.0, np.sin(x)/x), 0, 1)
print(res_sinc.integral.round(8))
# 0.94608307  (known constant Si(1))


#-------------------------------------------------------------------------------------------------#
#------------------------------- 10. fixed_quad() — fixed Gauss order ----------------------------#
#-------------------------------------------------------------------------------------------------#

##################
## fixed_quad() ##
##################
'''
fixed_quad(func, a, b, n=5) computes ∫ₐᵇ func(x) dx using n-point Gauss-Legendre quadrature.

Returns (val, None) — no error estimate.

For a polynomial of degree ≤ 2n-1, the result is exact.
For smooth non-polynomial functions, accuracy improves as n increases.

Use instead of quad when:
  - The integrand is smooth and well-behaved (no singularities).
  - Speed is critical and a fixed number of function evaluations is acceptable.
  - You want to integrate many similar integrals (same n, different a/b or args).

Do NOT use for oscillatory, singular, or nearly singular integrands — use quad.
'''

# ∫₀ᵖⁱ sin(x) dx = 2.0
val_fq5, _ = fixed_quad(f1, 0, np.pi, n=5)
val_fq10, _ = fixed_quad(f1, 0, np.pi, n=10)
val_fq20, _ = fixed_quad(f1, 0, np.pi, n=20)

print(abs(val_fq5  - 2.0))   # 1.1028447266525632e-07 - error at n=5
print(abs(val_fq10 - 2.0))   # 2.6645352591003757e-15 - error at n=10 — smaller
print(abs(val_fq20 - 2.0))   # 2.6645352591003757e-15 - error at n=20 — even smaller

# Exact for polynomial of degree ≤ 2n-1
# n=5 integrates x^8 exactly since deg 8 < 2*5-1=9
val_poly, _ = fixed_quad(lambda x: x**8, 0, 1, n=5)
print(abs(val_poly - 1./9))   # exact: ∫₀¹ x⁸ = 1/9
# ≈ 0.0  (machine precision)

# Batched over many intervals: integrate x^2 over [0,1], [1,2], [2,3]
edges = np.array([[0.,1.], [1.,2.], [2.,3.]])
results_fq = [fixed_quad(lambda x: x**2, a, b, n=3)[0] for a, b in edges]
print(np.array(results_fq).round(6))
# [0.333, 2.333, 6.333]


#-------------------------------------------------------------------------------------------------#
#-------------------------- 11. newton_cotes() — weights for equal spacing -----------------------#
#-------------------------------------------------------------------------------------------------#

####################
## newton_cotes() ##
####################
'''
newton_cotes(rn, equal=0) returns Newton-Cotes weights and error coefficient.

rn : int (degree = number of sub-intervals) or 1-D array of relative node positions.
equal=1 : force equally-spaced nodes (always).

Returns (an, B) where:
  an : weight array of length n+1 (for degree-n rule).
  B  : error coefficient (error ≈ B * h^(n+2) * f^(n+1)(ξ)).

Newton-Cotes rules for reference:
  n=1 : trapezoidal rule  (weights [1/2, 1/2])
  n=2 : Simpson's 1/3 rule (weights [1/6, 4/6, 1/6])
  n=3 : Simpson's 3/8 rule
  n=4 : Boole's rule

These are mainly useful for understanding weights used by trapezoid() and simpson().
For actual integration, use trapezoid/simpson/quad — not newton_cotes directly.
'''

# Trapezoidal weights
w_trap, B_trap = newton_cotes(1, equal=1)
print(w_trap)
# [0.5  0.5]   (midpoint weight * h for each endpoint)

# Simpson's 1/3 rule weights
w_simp, B_simp = newton_cotes(2, equal=1)
print(w_simp)
# [0.1667  0.6667  0.1667]  = [1/6, 4/6, 1/6] * h (where h=1 here)

# Boole's rule (degree 4)
w_boole, B_boole = newton_cotes(4, equal=1)
print(w_boole.round(6))
# [0.0778  0.3556  0.1333  0.3556  0.0778]  = [7/90, 32/90, 12/90, 32/90, 7/90] * h

# Apply manually: ∫₀¹ sin(x) dx using Simpson's rule with 3 nodes
x_nc = np.linspace(0, 1, 3)
y_nc = np.sin(x_nc)
h_nc = x_nc[1] - x_nc[0]
val_nc = np.dot(w_simp * h_nc, y_nc)
print(round(val_nc, 8))
# ≈ 1 - cos(1) ≈ 0.45969769


#-------------------------------------------------------------------------------------------------#
#----------------------------- 12. lebedev_rule() — sphere quadrature ----------------------------#
#-------------------------------------------------------------------------------------------------#

####################
## lebedev_rule() ##
####################
'''
lebedev_rule(n) returns (points, weights) for n-th order Lebedev quadrature on S².

Lebedev quadrature integrates functions over the unit sphere S² exactly for
all spherical harmonics up to degree n (for suitable n).

Returns:
  points : (N, 3) array of unit vectors (x, y, z) on S².
  weights: (N,) array of positive weights summing to 4π (area of S²).

n must be one of a specific set of values: 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, ...
  (run lebedev_rule(0) or check docs for the full list of available orders)

Use for:
  - Integrating functions of direction (angular integrals in 3-D).
  - Electronic structure calculations (atomic orbitals).
  - Diffusion MRI (orientation distribution functions).
  - Rendering (environment map integrals in computer graphics).
'''

pts, wts = lebedev_rule(5)   # 5th order: 6 points
print(pts.shape, wts.shape)
# (3, 14)  (14,)  — pts[0]=x, pts[1]=y, pts[2]=z coordinates; 14 quadrature points

print(wts.sum().round(8))
# 12.56637  ≈ 4π  (weights sum to sphere area)

# ∫_{S²} 1 dΩ = 4π
val_sphere_area = np.sum(wts)
print(round(val_sphere_area, 6), round(4 * np.pi, 6))
# 12.566371  12.566371  ✓

# ∫_{S²} x² dΩ = 4π/3  (by symmetry: ∫ x²+y²+z² = 4π, and x²=y²=z² by symmetry)
val_x2 = np.dot(wts, pts[0]**2)   # pts[0] = x-coordinates
print(round(val_x2, 6), round(4 * np.pi / 3, 6))
# 4.188790  4.188790  ✓

# Higher order: more accurate for higher-degree polynomials
pts_hi, wts_hi = lebedev_rule(21)
print(pts_hi.shape)
# (3, 170)  — 170 quadrature points for order 21

# Integrate Y_2^0(θ,φ) = √(5/4π) * (3cos²θ - 1) / 2  — a degree-2 spherical harmonic
# ∫_{S²} |Y_2^0|² dΩ = 1 (normalised)
z = pts_hi[2]   # z-coordinates = cos(θ)
Y20 = np.sqrt(5 / (4 * np.pi)) * (3 * z**2 - 1) / 2
val_Y20 = np.dot(wts_hi, Y20**2)
print(round(val_Y20, 6))
# 1.0  ✓


#-------------------------------------------------------------------------------------------------#
#------------------------------- 13. qmc_quad() — Quasi-Monte Carlo ------------------------------#
#-------------------------------------------------------------------------------------------------#

################
## qmc_quad() ##
################
'''
qmc_quad(func, a, b, n_estimates=8, n_points=1024, qrng=None) integrates over a
d-dimensional box [a, b] using Quasi-Monte Carlo with Sobol' sequences.

func : accepts (..., d)-shaped input; returns (...) output.
a, b : 1-D arrays of bounds (length d).
n_estimates : number of independent estimates (for error estimation); default 8.
n_points    : QMC sample size per estimate; should be a power of 2.
qrng        : a scipy.stats.qmc sampler (default Sobol').

Returns: res with .integral and .error.

Why QMC instead of plain Monte Carlo?
  O((log n)^d / n) vs O(1/√n) convergence — much faster for moderate d.
  See also file 13_Random.py section 9 (scipy.stats.qmc) for the sampler itself.

Use for:
  - High-dimensional integrals (d > 5) where adaptive quadrature is too expensive.
  - Smooth integrands (QMC advantage is largest for smooth functions).
  - Stochastic simulation integrals.
'''

# 2-D: ∫₀¹ ∫₀¹ sin(πx)·sin(πy)dxdy = (2/π)² ≈ 0.4053
def f_qmc(xy):
    return np.sin(np.pi * xy[..., 0]) * np.sin(np.pi * xy[..., 1])

res_qmc = qmc_quad(f_qmc, a=[0., 0.], b=[1., 1.], n_points=2048)
print(res_qmc.integral.round(6), (2 / np.pi)**2)
# ≈ 0.00033 0.40528473456935116

# 5-D: ∫₀¹⁵ Π sin(πxᵢ)dx = (2/π)⁵ ≈ 0.10457
def f_5d(x):
    return np.prod(np.sin(np.pi * x), axis=-1)

res_5d = qmc_quad(f_5d, a=np.zeros(5), b=np.ones(5), n_points=2048)
true_5d = (2 / np.pi)**5
print(res_5d.integral.round(5), round(true_5d, 5))
# 0.0 0.10457

# Compare accuracy: QMC vs plain MC at same sample count
rng_mc = np.random.default_rng(0)
n = 2048 * 8
x_mc = rng_mc.uniform(0, 1, (n, 5))
mc_est = f_5d(x_mc).mean()
print(f"MC error: {abs(mc_est - true_5d):.2e}   QMC error: {abs(res_5d.integral - true_5d):.2e}")
# MC error: 1.71e-03   QMC error: 1.05e-01


#-------------------------------------------------------------------------------------------------#
#------------------------------------ 14. nsum() — series summation ------------------------------#
#-------------------------------------------------------------------------------------------------#

############
## nsum() ##
############
'''
nsum(f, a, b) evaluates Σ_{n=a}^{b} f(n) for integer n from a to b (inclusive).

a, b can be finite integers, or a may be any integer and b may be np.inf.
For infinite series, nsum uses Euler-Maclaurin and Richardson extrapolation.

Returns a result object with .sum and .error.

Applications:
  - Computing special function values (zeta, eta, etc.).
  - Verifying series representations.
  - Convergence of numerical series.
'''

# Basel problem: Σ_{n=1}^∞ 1/n² = π²/6
res_basel = nsum(lambda n: 1.0 / n**2, 1, np.inf)
print(res_basel.sum.round(8), round(np.pi**2 / 6, 8))
# 1.64493407  1.64493407  ✓

# Alternating series: Σ_{n=0}^∞ (-1)^n / (2n+1) = π/4
res_leibniz = nsum(lambda n: (-1.0)**n / (2*n + 1), 0, np.inf)
print(res_leibniz.sum.round(8), round(np.pi / 4, 8))
# 0.78539816  0.78539816  ✓

# Partial sum (finite upper limit): Σ_{n=1}^{100} 1/n
res_harmonic = nsum(lambda n: 1.0 / n, 1, 100)
true_harmonic = sum(1/n for n in range(1, 101))
print(res_harmonic.sum.round(8), round(true_harmonic, 8))
# 5.18737752  5.18737752

# Riemann zeta function ζ(s) = Σ_{n=1}^∞ 1/nˢ
from scipy.special import zeta
for s in [2., 3., 4.]:
    res_zeta = nsum(lambda n: n**(-s), 1, np.inf)
    print(f"ζ({s:.0f}) = {res_zeta.sum.round(6):.6f}  (scipy: {zeta(s):.6f})")
# ζ(2) = 1.644934  (scipy: 1.644934)
# ζ(3) = 1.202057  (scipy: 1.202057)
# ζ(4) = 1.082323  (scipy: 1.082323)


#-------------------------------------------------------------------------------------------------#
#----------------------- 15. trapezoid() / cumulative_trapezoid() --------------------------------#
#-------------------------------------------------------------------------------------------------#

################
## trapezoid() ##
################
'''
trapezoid(y, x=None, dx=1.0, axis=-1) integrates using the composite trapezoidal rule.

y : sample values at the quadrature nodes.
x : sample positions (1-D or same shape as y along axis).  Default: uniform spacing dx.
dx: uniform step size when x is not given.
axis: axis along which to integrate (allows batch integration over arrays).

Result:  Σᵢ (yᵢ + yᵢ₊₁)/2 · (xᵢ₊₁ - xᵢ)

Accuracy: O(h²) per interval — good for smooth f and fine grids.
For coarse grids or accurate quadrature, prefer simpson() or quad().
'''

x_t = np.linspace(0, np.pi, 1000)
y_t = np.sin(x_t)

val_trap = trapezoid(y_t, x_t)
print(val_trap.round(8))
# 1.99999835  ≈ 2.0

# Non-uniform spacing
x_nu = np.array([0., 0.1, 0.5, 1.0, 2.0, np.pi])
y_nu = np.sin(x_nu)
print(trapezoid(y_nu, x_nu).round(6))
# 1.845475
# rougher estimate due to coarser grid

# Uniform spacing (pass dx instead of x)
dx = np.pi / 999
print(trapezoid(y_t, dx=dx).round(8))
# 1.99999835
# same as above

# Batch: integrate each row of a 2-D array
Y_batch = np.array([np.sin(x_t), np.cos(x_t), np.exp(-x_t)])
vals_batch = trapezoid(Y_batch, x_t, axis=1)
print(vals_batch.round(6))
# [1.999998 0.       0.956787]

############################
## cumulative_trapezoid() ##
############################
'''
cumulative_trapezoid(y, x=None, dx=1.0, axis=-1, initial=None) returns the running
(cumulative) integral: result[i] = ∫_{x[0]}^{x[i+1]} f(x) dx.

Output length = len(y) - 1  (unless initial is given, which prepends it).
initial=0 : prepend 0 so output has the same length as y (convenient for indexing).

Use to get the antiderivative / CDF at each sample point.
'''

x_ct = np.linspace(0, np.pi, 100)
y_ct = np.sin(x_ct)

cumint = cumulative_trapezoid(y_ct, x_ct, initial=0)
print(cumint.shape)
# (100,)  ← same length as y because initial=0

# cumint[i] ≈ ∫₀^{xᵢ} sin(t) dt = 1 - cos(xᵢ)
true_cumint = 1 - np.cos(x_ct)
print(np.abs(cumint - true_cumint).max().round(5))
# 0.00017 (very small error)

print(cumint[-1].round(6))
# ≈ 2.0  (= 1 - cos(π) = 2)

# Without initial: length is len(y)-1
cumint_short = cumulative_trapezoid(y_ct, x_ct)
print(cumint_short.shape)
# (99,)


#-------------------------------------------------------------------------------------------------#
#--------------------------- 16. simpson() / cumulative_simpson() --------------------------------#
#-------------------------------------------------------------------------------------------------#

###############
## simpson() ##
###############
'''
simpson(y, x=None, dx=1.0, axis=-1) integrates using composite Simpson's rule.

Uses pairs of intervals:  ∫_{xᵢ}^{xᵢ₊₂} f ≈ h/3 · (f(xᵢ) + 4f(xᵢ₊₁) + f(xᵢ₊₂))
Accuracy: O(h⁴) per pair — significantly more accurate than trapezoid for smooth f.

Requires an odd number of equally-spaced points for the pure rule.
For even n, scipy falls back to trapezoidal for the last interval.
x can be non-uniform (scipy adapts the weights).

Preferred over trapezoid when the grid is fixed and you want more accuracy.
'''

x_s = np.linspace(0, np.pi, 1001)   # odd number of points — ideal for simpson
y_s = np.sin(x_s)

val_simp = simpson(y_s, x_s)
print(val_simp.round(12))
# 2.000000000000  (much more accurate than trapezoid for same n)

# Accuracy comparison at the same node count
val_trap_cmp = trapezoid(y_s, x_s)
print(f"trapezoid error: {abs(val_trap_cmp - 2):.2e}") # 1.64e-06
print(f"simpson error:   {abs(val_simp    - 2):.2e}")  # 1.08e-12
# simpson is typically ~1000x more accurate for smooth integrands

# Non-uniform spacing
x_nu_s = np.concatenate([[0.], np.sort(np.random.default_rng(0).uniform(0.1, np.pi-0.1, 50)), [np.pi]])
y_nu_s = np.sin(x_nu_s)
print(simpson(y_nu_s, x_nu_s).round(6))
# ≈ 2.0

##########################
## cumulative_simpson() ##
##########################
'''
cumulative_simpson(y, x=None, dx=1.0, axis=-1, initial=None) returns the running Simpson
integral using the composite 3/8 rule over adjacent pairs.

More accurate running integral than cumulative_trapezoid for smooth functions.
Same interface: initial=0 keeps output length equal to len(y).
'''

cumsimp = cumulative_simpson(y_s, x=x_s, initial=0)
true_cumsimp = 1 - np.cos(x_s)
print(np.abs(cumsimp - true_cumsimp).max().round(8))
# smaller error than cumulative_trapezoid


#-------------------------------------------------------------------------------------------------#
#-------------------------------------- 17. romb() -----------------------------------------------#
#-------------------------------------------------------------------------------------------------#

############
## romb() ##
############
'''
romb(y, dx=1.0, axis=-1, show=False) uses Romberg integration on a uniformly-spaced grid.

Requires n = 2^k + 1 samples (e.g. 3, 5, 9, 17, 33, 65, 129, ...).
Applies Richardson extrapolation on trapezoid estimates at successively halved step sizes.
This is equivalent to using all 2^k + 1 data points in the most efficient way.

Accuracy: O(h^{2k}) — much better than Simpson for the same n, if f is smooth.
Limitation: requires exactly 2^k+1 points; non-uniform spacing not supported.

Use romb over simpson when you have a power-of-2 + 1 grid and want maximum accuracy.
'''

n_romb = 2**8 + 1   # 257 equally-spaced points
x_r = np.linspace(0, np.pi, n_romb)
y_r = np.sin(x_r)
dx_r = x_r[1] - x_r[0]

val_romb = romb(y_r, dx=dx_r)
print(val_romb.round(14))
# 2.0000000000000  — extremely accurate

print(f"trapezoid error: {abs(trapezoid(y_r, x_r) - 2):.2e}")  # 2.51e-05
print(f"simpson error:   {abs(simpson(y_r, x_r)   - 2):.2e}")  # 2.52e-10
print(f"romb error:      {abs(val_romb             - 2):.2e}") # 4.44e-16
# romb error is smallest, demonstrating Richardson extrapolation


#-------------------------------------------------------------------------------------------------#
#----------------------------- 18. solve_ivp() — modern IVP solver -------------------------------#
#-------------------------------------------------------------------------------------------------#

#################
## solve_ivp() ##
#################
'''
solve_ivp(fun, t_span, y0, method='RK45', t_eval=None, events=None,
          dense_output=False, vectorized=False, args=None, **options)

Solves the IVP:  y'(t) = fun(t, y),   y(t₀) = y₀

fun    : callable fun(t, y) → dy/dt; t is scalar, y is 1-D array.
t_span : (t0, tf) — integration interval.
y0     : initial state vector.
method : solver choice (see section 19).
t_eval : 1-D array of times at which to store y (optional; all steps stored if None).
events : callable(s) e  — integration stops when e(t,y) changes sign.
dense_output=True : attach a continuous interpolant (sol.sol(t) for any t).
vectorized=True   : fun(t, Y) where Y has shape (n, k) — parallelises evaluation.
args   : extra arguments passed to fun.

Returns OdeSolution with:
  sol.t  : integration time points.
  sol.y  : state array shape (n_eq, n_times).
  sol.success / sol.message / sol.nfev (function evaluations).
  sol.sol  : if dense_output=True, a callable interpolant.
  sol.t_events / sol.y_events : if events given.
'''

# ── Scalar ODE: y' = -y,  y(0)=1  →  y(t) = exp(-t)
def f_decay(t, y): 
  return -y

sol = solve_ivp(f_decay, t_span=(0, 5), y0=[1.0], t_eval=np.linspace(0, 5, 50))
print(sol.success)
# True

print(np.abs(sol.y[0] - np.exp(-sol.t)).max().round(8))
# 0.00045811 (very small error)

# ── Van der Pol oscillator (stiff for large μ): y'' - μ(1-y²)y' + y = 0
#                                             => y'' = μ(1-y²)y' - y
def van_der_pol(t, y, mu=1000.):
    return [y[1], mu * (1 - y[0]**2) * y[1] - y[0]]

# Method selection: stiff ODE → use Radau or BDF
sol_vdp = solve_ivp(van_der_pol, t_span=(0, 3000), y0=[2., 0.],
                    method='Radau', rtol=1e-6, atol=1e-8,
                    t_eval=np.linspace(0, 3000, 1000), args=(1000.,))
print(sol_vdp.success)
# True
print(sol_vdp.nfev)
# 9920 (relatively few evaluations — Radau adapts step size around stiff regions)

# ── Dense output: evaluate solution at arbitrary time
sol_dense = solve_ivp(f_decay, t_span=(0, 5), y0=[1.0], dense_output=True)
t_query = np.array([0.1, 0.5, 1.0, 2.5])
y_query = sol_dense.sol(t_query)   # shape (1, 4)

print(y_query[0].round(6))
# [0.904837 0.606072 0.36814  0.08216 ]

print(np.exp(-t_query).round(6))   # true values
# [0.904837 0.606531 0.367879 0.082085]
# very close

# ── Events: stop when y crosses zero (for bouncing ball example)
def ball(t, y):
    # y[0] = height, y[1] = velocity
    return [y[1], -9.81]

def hit_ground(t, y): 
  return y[0]    # zero when height = 0
hit_ground.terminal = True           # stop integration at first zero
hit_ground.direction = -1            # only trigger on decreasing zero-crossing

sol_ball = solve_ivp(ball, t_span=(0, 10), y0=[10., 0.], events=hit_ground)
print(sol_ball.t_events[0].round(4))
# [1.4278]  ≈ √(2·10/9.81) ≈ 1.4278 s  (time for ball to fall 10 m)

# ── System of ODEs: Lotka-Volterra predator-prey
def lotka_volterra(t, y, alpha=1.5, beta=1.0, delta=0.75, gamma=1.5):
    x, p = y
    return [alpha * x - beta * x * p,
            delta * x * p - gamma * p]

sol_lv = solve_ivp(lotka_volterra, t_span=(0, 15), y0=[10., 5.],
                   t_eval=np.linspace(0, 15, 300), method='RK45', rtol=1e-8)
print(sol_lv.y.shape)
# (2, 300)  — prey and predator populations at 300 time points

print(sol_lv.y[:, 0])   # initial state [10., 5.]
# [10.   5.]

# ── Second-order ODE: convert to first-order system
# y'' + 2y' + 5y = 0,  y(0)=1, y'(0)=0   (damped oscillator)
# Let z = [y, y']; z' = [y', -2y' - 5y]
def damped_osc(t, z):
    return [z[1], -2*z[1] - 5*z[0]]

sol_osc = solve_ivp(damped_osc, t_span=(0, 10),
                    y0=[1., 0.], t_eval=np.linspace(0, 10, 200))

# True solution: y(t) = e^{-t}(cos(2t) + 0.5 sin(2t))
y_true_osc = np.exp(-sol_osc.t) * (np.cos(2*sol_osc.t) + 0.5*np.sin(2*sol_osc.t))
print(np.abs(sol_osc.y[0] - y_true_osc).max().round(8))
# 0.00022858 (very small error)


#-------------------------------------------------------------------------------------------------#
#---------------------------- 19. ODE method selection guide -------------------------------------#
#-------------------------------------------------------------------------------------------------#

'''
Method       Class        Order   Use when
─────────────────────────────────────────────────────────────────────────────────────────────────
RK23         Explicit     2(3)    Non-stiff; loose tolerances; fast but low accuracy.
RK45         Explicit     4(5)    Non-stiff; DEFAULT; best general choice for smooth non-stiff.
DOP853       Explicit     8       Non-stiff; tight tolerances; smooth high-accuracy problems.
Radau        Implicit     5       STIFF; preferred stiff solver; robust and accurate.
BDF          Implicit     1-5     STIFF; backward-differentiation; large stiff systems.
LSODA        Auto         var     Auto-detects stiffness and switches; legacy default.

Detecting stiffness:
  - Solver is very slow (many rejected steps) → try Radau or BDF.
  - Problem has very different timescales (e.g. chemical kinetics, electronics).
  - Jacobian eigenvalues span many orders of magnitude.

rtol, atol: control relative and absolute error per step.
  rtol=1e-3, atol=1e-6 : fast, loose  (default rtol=1e-3)
  rtol=1e-6, atol=1e-9 : accurate
  rtol=1e-10, atol=1e-12: very accurate (use DOP853 or Radau)

max_step, first_step: override automatic step-size control.
jac : analytic Jacobian for Radau/BDF (improves speed and reliability for stiff problems).
'''

# Non-stiff: RK45 (default)
sol_nonstiff = solve_ivp(lambda t, y: np.cos(t), (0, 10), [0.], method='RK45')
print(sol_nonstiff.nfev)
# 68

# Stiff: BDF with analytic Jacobian
def robertson(t, y):
    # Robertson chemical kinetics — classic stiff benchmark
    return [
        -0.04 * y[0] + 1e4 * y[1] * y[2],
         0.04 * y[0] - 1e4 * y[1] * y[2] - 3e7 * y[1]**2,
         3e7 * y[1]**2
    ]

def robertson_jac(t, y):
    return [
        [-0.04,         1e4 * y[2],        1e4 * y[1]],
        [ 0.04, -1e4 * y[2] - 6e7 * y[1], -1e4 * y[1]],
        [ 0.,           6e7 * y[1],          0.        ]
    ]

sol_rob = solve_ivp(robertson, (0, 1e11), [1., 0., 0.],
                    method='BDF', jac=robertson_jac,
                    rtol=1e-6, atol=[1e-6, 1e-10, 1e-6],
                    t_eval=[0., 1e4, 1e8, 1e11])

print(sol_rob.y[:, -1].round(6))
# [-2.46868122e+07 -4.00000000e-06  2.46868132e+07]
# steady-state solution of Robertson system

print(sol_rob.success)
# True


#-------------------------------------------------------------------------------------------------#
#------------------------------ 20. solve_bvp() — boundary value problems ------------------------#
#-------------------------------------------------------------------------------------------------#

#################
## solve_bvp() ##
#################
'''
solve_bvp(fun, bc, x, y, p=None, S=None, fun_jac=None, bc_jac=None,
          tol=1e-3, verbose=0, bc_tol=None, max_nodes=1000)

Solves a 2-point BVP:
  y'(x) = fun(x, y)
  bc(y(a), y(b)) = 0

fun  : callable fun(x, y) → dy/dx; x is (n,), y is (k, n).
bc   : callable bc(ya, yb) → residual (must be zero at solution).
x    : initial mesh (1-D array on [a, b]).
y    : initial guess for y, shape (k, len(x)).
p    : unknown parameters to be determined (e.g. eigenvalue problems).

Returns:
  sol.x, sol.y : refined mesh and solution.
  sol.sol(x)   : callable interpolant.
  sol.success

BVP vs IVP:
  IVP: conditions all specified at one endpoint → march forward in time.
  BVP: conditions split between a and b → iterative collocation.
'''

# Classic BVP: y'' = -π²·y,  y(0)=0, y(1)=0  →  y(x) = sin(πx)
def bvp_fun(x, y):
    # System: [y, y']' = [y', -π²y]
    return np.vstack([y[1], -(np.pi**2) * y[0]])

def bvp_bc(ya, yb):
    return np.array([ya[0], yb[0]])   # y(0)=0, y(1)=0

x_bvp = np.linspace(0, 1, 10)
y_guess = np.zeros((2, 10))
y_guess[0] = np.sin(np.pi * x_bvp)   # initial guess

sol_bvp = solve_bvp(bvp_fun, bvp_bc, x_bvp, y_guess)
print(sol_bvp.success)
# True

x_fine_bvp = np.linspace(0, 1, 100)
y_fine_bvp = sol_bvp.sol(x_fine_bvp)[0]
y_true_bvp = np.sin(np.pi * x_fine_bvp)
print(np.abs(y_fine_bvp - y_true_bvp).max().round(6))
# 0.99989 (error)

# BVP with unknown parameter (Sturm-Liouville eigenvalue problem)
# y'' + λy = 0,  y(0)=0, y(1)=0  →  smallest eigenvalue λ = π²
def bvp_eigen(x, y, p):
    lam = p[0]
    return np.vstack([y[1], -lam * y[0]])

def bvp_eigen_bc(ya, yb, p):
    return np.array([ya[0], yb[0], ya[1] - 1.])   # fix y'(0)=1 to avoid trivial solution

x_eig = np.linspace(0, 1, 10)
y_eig = np.zeros((2, 10))
y_eig[0] = np.sin(np.pi * x_eig)
y_eig[1] = np.pi * np.cos(np.pi * x_eig)

sol_eig = solve_bvp(bvp_eigen, bvp_eigen_bc, x_eig, y_eig, p=[10.])
print(sol_eig.p[0].round(6))
# 9.876071
# ≈ 9.869604  ≈ π²  ✓  (smallest eigenvalue)

print(round(np.pi**2, 6))
# 9.869604


#-------------------------------------------------------------------------------------------------#
#---------------------------------- 21. Legacy ODE: odeint() -------------------------------------#
#-------------------------------------------------------------------------------------------------#

##############
## odeint() ##
##############
'''
odeint(func, y0, t, args=(), Dfun=None, col_deriv=False, full_output=False,
       rtol=None, atol=None, tcrit=None, h0=0, hmax=0, hmin=0, ixpr=0,
       mxstep=0, mxhnil=0, mxordt=0, mxords=0, printmessg=0, tfirst=False)

LEGACY wrapper for ODEPACK's LSODA algorithm. Still widely used in older code.

Key differences from solve_ivp:
  - func signature: func(y, t, ...) — NOTE: t is second argument (not first!).
    Use tfirst=True for func(t, y, ...) convention.
  - t : array of times at which to return solution (not a span).
  - Returns (y, info) where y has shape (len(t), len(y0)).
  - No events support.

Modern replacement: solve_ivp(fun, (t[0], t[-1]), y0, method='LSODA', t_eval=t)
'''

# y' = -y,  y(0)=1  →  y(t) = exp(-t)
def f_odeint(y, t): 
  return -y    # note: y first, t second

t_ode = np.linspace(0, 5, 50)
y_ode = odeint(f_odeint, y0=[1.], t=t_ode)

print(y_ode.shape)
# (50, 1)  ← shape is (n_times, n_eqs) — OPPOSITE of solve_ivp which gives (n_eqs, n_times)

print(np.abs(y_ode[:, 0] - np.exp(-t_ode)).max().round(8))
# 3e-08 (very small)

# System: Lotka-Volterra  (same as solve_ivp example)
def lv_odeint(y, t, alpha=1.5, beta=1.0, delta=0.75, gamma=1.5):
    x, p = y
    return [alpha*x - beta*x*p, delta*x*p - gamma*p]

t_lv = np.linspace(0, 15, 300)
y_lv = odeint(lv_odeint, y0=[10., 5.], t=t_lv, args=(1.5, 1.0, 0.75, 1.5))

print(y_lv.shape)
# (300, 2)

# Convert odeint result to solve_ivp shape convention: transpose
y_lv_T = y_lv.T   # (2, 300)  — now matches sol.y from solve_ivp

# Modern equivalent using solve_ivp
sol_lv_modern = solve_ivp(lotka_volterra, (0, 15), [10., 5.],
                           t_eval=t_lv, method='LSODA')
print(np.allclose(y_lv_T, sol_lv_modern.y, atol=0.5))
# True
# (both LSODA; small differences accumulate over long integration)

# tfirst=True: use func(t, y) convention (same as solve_ivp)
def f_tfirst(t, y): 
  return -y

y_tfirst = odeint(f_tfirst, y0=[1.], t=t_ode, tfirst=True)
print(np.allclose(y_ode, y_tfirst))
# True


#-------------------------------------------------------------------------------------------------#
#----------------------------- NumPy supportive — sample-based integration -----------------------#
#-------------------------------------------------------------------------------------------------#

####################
## np.trapezoid() ##
####################
'''
np.trapezoid(y, x=None, dx=1.0, axis=-1) — identical to scipy.integrate.trapezoid.

Introduced in NumPy 2.0 as the official replacement for the deprecated np.trapz.
Both np.trapezoid and scipy.integrate.trapezoid produce the same results.

Use when you want no scipy dependency or are working with pure NumPy arrays.
'''

x_np = np.linspace(0, np.pi, 100)
y_np = np.sin(x_np)

print(np.trapezoid(y_np, x_np).round(6))
# ≈ 2.0  (same as trapezoid(y_np, x_np))

print(np.allclose(np.trapezoid(y_np, x_np), trapezoid(y_np, x_np)))
# True

#########################
## np.cumsum() pattern ##
#########################
'''
For uniform grids, cumulative integration with the rectangle rule is:
  ∫₀^{xᵢ} f(x) dx ≈ Σⱼ₌₀^{i-1} f(xⱼ) · dx

np.cumsum(y) * dx gives a left-Riemann running sum — less accurate than
cumulative_trapezoid but occasionally useful as a quick approximation.
'''

x_cs = np.linspace(0, np.pi, 1000)
y_cs = np.sin(x_cs)
dx_cs = x_cs[1] - x_cs[0]

# Left Riemann cumulative sum
cumrect = np.cumsum(y_cs) * dx_cs   # left endpoints

# Compare with cumulative_trapezoid (more accurate)
cumtrap = cumulative_trapezoid(y_cs, x_cs, initial=0)
true_cs = 1 - np.cos(x_cs)

print(np.abs(cumrect - true_cs).max().round(5))   # 0.00157 rectangle error
print(np.abs(cumtrap - true_cs).max().round(5))   # 0.0     trapezoid error — smaller
