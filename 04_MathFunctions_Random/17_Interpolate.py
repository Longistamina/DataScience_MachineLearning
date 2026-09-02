'''
scipy.interpolate  —  interpolation and approximation
======================================================

1. Univariate interpolation — modern OOP API
   + CubicSpline()              : C² piecewise cubic; best general 1-D choice.
   + PchipInterpolator()        : C¹ monotone-preserving cubic; avoids overshoot.
   + Akima1DInterpolator()      : C¹ "visually pleasing" cubic; robust to outliers.
   + CubicHermiteSpline()       : C¹ cubic given both values AND derivatives at nodes.
   + BarycentricInterpolator()  : numerically stable Lagrange interpolation (C∞).
   + FloaterHormannInterpolator(): barycentric rational interpolation (C∞, no poles).
   + KroghInterpolator()        : Hermite interpolation to arbitrary derivative order.

2. B-spline interpolation — make_interp_spline + BSpline
   + make_interp_spline()       : construct an interpolating B-spline of any degree.
   + BSpline()                  : low-level B-spline object (knots, coefficients, degree).
   + BSpline.design_matrix()    : sparse collocation matrix for custom fitting.

3. 1-D spline smoothing & approximation
   + make_smoothing_spline()    : auto-tuned smoothing spline via GCV criterion.
   + make_lsq_spline()          : least-squares B-spline with user-specified knots.
   + make_splrep()              : bounded-error smoothing spline (newer functional API).
   + make_splprep()             : parametric curve smoothing (N-D input).

4. Low-level piecewise structures
   + PPoly()                    : piecewise polynomial in power basis; used by CubicSpline.
   + BPoly()                    : piecewise polynomial in Bernstein basis.
   PPoly / BPoly methods:
   + .derivative() / .antiderivative(): calculus on piecewise polynomials.
   + .solve() / .roots()        : find x where p(x) = y.
   + .extend()                  : append new breakpoints and coefficients.

5. Multivariate interpolation — unstructured data
   + LinearNDInterpolator()     : piecewise linear on Delaunay triangulation (N-D).
   + NearestNDInterpolator()    : nearest-neighbour (N-D).
   + CloughTocher2DInterpolator(): C¹ cubic on 2-D triangulation.
   + RBFInterpolator()          : radial basis function interpolation (N-D).
   + griddata()                 : convenience wrapper for all unstructured ND methods.

6. Grid-based multivariate interpolation
   + RegularGridInterpolator()  : interpolation on a rectilinear N-D grid.
   + interpn()                  : convenience wrapper for RegularGridInterpolator.
   + RectBivariateSpline()      : bivariate spline on a 2-D rectangular grid.

7. Additional tools
   + lagrange()                 : Lagrange interpolating polynomial as numpy.poly1d.
   + approximate_taylor_polynomial(): estimate Taylor polynomial by finite differences.
   + pade()                     : Padé rational approximation from power-series coefficients.
   + AAA()                      : AAA rational approximation (complex-capable, no poles).

8. Legacy API  (do NOT use in new code)
   + interp1d()                 : replaced by make_interp_spline / CubicSpline.
   + UnivariateSpline()         : FITPACK OOP smoothing; replaced by make_smoothing_spline.
   + InterpolatedUnivariateSpline(): FITPACK OOP interpolating; replaced by make_interp_spline.
   + LSQUnivariateSpline()      : FITPACK OOP fixed-knot LSQ; replaced by make_lsq_spline.
   + splrep() + splev()         : FITPACK functional interface; replaced by make_splrep.
   + Rbf()                      : replaced by RBFInterpolator.

9. NumPy supportive parts
   + np.interp()                : linear 1-D interpolation on sorted (xp, fp) arrays.
   + np.searchsorted()          : find insertion indices; building block for interpolators.
   + Polynomial.fit() / Chebyshev.fit(): polynomial/Chebyshev least-squares (see file 14).
'''

import numpy as np
from scipy.interpolate import (
    AAA,
    Akima1DInterpolator,
    BarycentricInterpolator,
    BPoly,
    BSpline,
    CloughTocher2DInterpolator,
    CubicHermiteSpline,
    CubicSpline,
    FloaterHormannInterpolator,
    InterpolatedUnivariateSpline,
    KroghInterpolator,
    LinearNDInterpolator,
    LSQUnivariateSpline,
    NearestNDInterpolator,
    PchipInterpolator,
    PPoly,
    RBFInterpolator,
    RectBivariateSpline,
    RegularGridInterpolator,
    UnivariateSpline,
    approximate_taylor_polynomial,
    griddata,
    interp1d,
    interpn,
    lagrange,
    make_interp_spline,
    make_lsq_spline,
    make_smoothing_spline,
    make_splprep,
    make_splrep,
    pade,
    splantider,
    splder,
    splev,
    splint,
    splrep,
    sproot,
)

# ── Shared sample data ───────────────────────────────────────────────────────────────────────────
rng = np.random.default_rng(0)

# Sparse 1-D nodes — intentionally unevenly spaced
x_nodes = np.array([0., 1., 2., 3., 5., 7., 8., 9., 10.])
y_nodes = np.sin(x_nodes)

# Dense evaluation grid
x_fine = np.linspace(0, 10, 200)

# Noisy data for smoothing
x_noisy = np.linspace(0, 2 * np.pi, 50)
y_noisy = np.sin(x_noisy) + 0.15 * rng.standard_normal(50)

# True values for error comparison
y_true_fine  = np.sin(x_fine)
y_true_nodes = np.sin(x_nodes)


# =========================================================================================
# 1. Univariate interpolation — modern OOP API
# =========================================================================================

##---------------##
## CubicSpline() ##
##---------------##
'''
CubicSpline(x, y) fits a C² (twice continuously differentiable) piecewise cubic polynomial
that passes exactly through every data point.

bc_type controls boundary conditions at the two endpoints:
  'not-a-knot' (default) : third derivative is continuous at the 2nd and 2nd-to-last knots.
  'natural'              : second derivative = 0 at endpoints (S''(a)=S''(b)=0).
  'clamped'              : first derivative = 0 at endpoints.
  ((1, va), (1, vb))     : prescribe 1st (or 2nd) derivative at each endpoint explicitly.
  'periodic'             : for periodic data; y[0] must equal y[-1].

Returns a PPoly (piecewise power-basis polynomial) object.
All PPoly methods (.derivative, .antiderivative, .roots, .solve) are available.
'''

cs = CubicSpline(x_nodes, y_nodes)

print(cs(np.pi).round(6))
# ≈ sin(π) ≈ 0.0  (very close to zero; interpolates through the nodes, not the true function)

print(cs(x_fine[:5]).round(4))
# [0.     0.0563 0.1113 0.1651 0.2175]
# values near sin(x) for small x

# Max error over [0, 10]
print(np.abs(cs(x_fine) - y_true_fine).max().round(5))
# small — CubicSpline is O(h⁴) accurate for smooth functions

# First derivative
cs_d1 = cs.derivative()            # returns a new PPoly
print(cs_d1(0.).round(4))
# 1.1328
# ≈ cos(0) = 1.0  (true derivative at x=0)

# Second derivative
cs_d2 = cs.derivative(2)
# -0.4873
# ≈ -sin(0) = 0.0

# Antiderivative: ∫₀ˣ sin(t) dt = 1 - cos(x)
cs_int = cs.antiderivative()
print(cs_int(np.pi).round(4))
# 2.005
# ≈ 2.0  (1 - cos(π) = 2)

# Roots: find where the interpolant crosses zero
roots = cs.roots()
print(roots.round(4))
# [-8.0526  0.      3.1496  6.2799  9.4355 12.4427]  ≈ multiples of π  (zeros of sin)

# Boundary conditions
cs_natural = CubicSpline(x_nodes, y_nodes, bc_type='natural')
cs_clamped = CubicSpline(x_nodes, y_nodes, bc_type='clamped')

print(cs_natural.derivative(2)(x_nodes[[0, -1]]).round(8))
# [0.  0.]   (S'' = 0 at both ends — natural BC)

print(cs_clamped.derivative()(x_nodes[[0, -1]]).round(8))
# [0.  0.]   (S' = 0 at both ends — clamped BC)

# Periodic spline
x_per = np.linspace(0, 2 * np.pi, 9, endpoint=False)   # 8 points, same start/end value excluded
x_per = np.append(x_per, 2 * np.pi)                    # include endpoint with y[0]=y[-1]
y_per = np.sin(x_per)
cs_per = CubicSpline(x_per, y_per, bc_type='periodic')

print(cs_per(0.).round(6), cs_per(2 * np.pi).round(6))
# 0.0  0.0  (periodic: same value at both ends)

##-------------------##
## PchipInterpolator ##
##-------------------##
'''
PchipInterpolator(x, y) uses Piecewise Cubic Hermite Interpolating Polynomials (PCHIP).

C¹ (first-derivative continuous) but NOT C² — deliberate:
  - Preserves monotonicity: if data is monotone in an interval, so is the interpolant.
  - Avoids overshoot and spurious oscillations near steep gradients.
  - At the cost of slightly less smooth appearance vs CubicSpline.

Use PCHIP instead of CubicSpline when:
  - Data has sharp features or step-like transitions.
  - You need monotone interpolation (e.g. CDFs, temperature profiles).
  - Overshooting/ringing would cause physical problems.
'''

pchip = PchipInterpolator(x_nodes, y_nodes)

print(pchip(x_fine[:5]).round(4))
# [0.     0.0615 0.1225 0.1827 0.2419]

# Monotone data example: PCHIP preserves monotonicity; CubicSpline may overshoot
x_mono = np.array([0., 1., 2., 3., 4.])
y_mono = np.array([0., 0.5, 1., 1., 1.])   # monotone, flattens out

x_dense = np.linspace(0, 4, 100)
y_cs_mono   = CubicSpline(x_mono, y_mono)(x_dense)
y_pchip_mono = PchipInterpolator(x_mono, y_mono)(x_dense)

print(y_cs_mono.min().round(4), y_cs_mono.max().round(4))
# 0.0 1.0481
# may exceed [0, 1] — CubicSpline overshoots

print(y_pchip_mono.min().round(4), y_pchip_mono.max().round(4))
# [0.0, 1.0] exactly — PCHIP stays within data range

# Derivative available (C¹)
print(pchip.derivative()(x_nodes[0]).round(4))
# finite slope at left endpoint

##---------------------##
## Akima1DInterpolator ##
##---------------------##
'''
Akima1DInterpolator(x, y) computes a C¹ cubic spline using Akima's local averaging method.

Local method: each cubic piece only depends on nearby points (not all data).
  - More robust than CubicSpline in the presence of outliers.
  - Avoids excessive oscillation induced by a single anomalous data point.
  - method='akima' (default) or method='makima' (modified Akima; reduces overshooting more).

Use Akima instead of CubicSpline when:
  - Data is noisy or contains outlier-like spikes.
  - You want locality (one bad point should not pollute the whole interpolant).
'''

akima = Akima1DInterpolator(x_nodes, y_nodes)

print(akima(x_fine[:5]).round(4))
# [0.     0.0607 0.1194 0.1761 0.2308]

# Robustness demo: insert an outlier
x_out = np.array([0., 1., 2., 3., 4., 5.])
y_out = np.array([0., 1., 2., 10., 4., 5.])   # outlier at x=3

y_cs_out    = CubicSpline(x_out, y_out)(np.linspace(0, 5, 100))
y_akima_out = Akima1DInterpolator(x_out, y_out)(np.linspace(0, 5, 100))

# CubicSpline propagates oscillation across all segments
print(y_cs_out.min().round(2), y_cs_out.max().round(2))
# 0.0 10.06

# Akima confines the distortion locally
print(y_akima_out.min().round(2), y_akima_out.max().round(2))
# 0.0 10.01

# Modified Akima (less overshoot, recommended for most cases)
makima = Akima1DInterpolator(x_nodes, y_nodes, method='makima')
print(np.abs(makima(x_fine) - y_true_fine).max().round(5))
# 0.16314

##--------------------##
## CubicHermiteSpline ##
##--------------------##
'''
CubicHermiteSpline(x, y, dydx) constructs a C¹ piecewise cubic given values AND derivatives.

Use when you know the exact derivative at every node (e.g. from analytic formula, ODE output).
This is the building block for PCHIP (which computes its own derivative estimates internally).

Applications:
  - ODE solvers output (x, y, y') at each step → CubicHermiteSpline gives dense output.
  - CAD/graphics: Bézier/Hermite curves with prescribed tangents at control points.
'''

dydx_nodes = np.cos(x_nodes)    # exact derivatives of sin(x)

chs = CubicHermiteSpline(x_nodes, y_nodes, dydx=dydx_nodes)

# With exact derivatives, Hermite spline is usually more accurate than CubicSpline
print(np.abs(chs(x_fine) - y_true_fine).max().round(6))
# 0.029567
# typically smaller error than plain CubicSpline (which estimates boundary conditions)

# The derivative matches exactly at nodes
print(np.allclose(chs.derivative()(x_nodes), dydx_nodes))
# True

##-------------------------##
## BarycentricInterpolator ##
##-------------------------##
'''
BarycentricInterpolator(xi, yi) computes the unique polynomial through all N points.

Numerically stable variant of classical Lagrange interpolation using barycentric weights.
Result is a polynomial of degree N-1 passing exactly through all data points.

Pros:  exact interpolation; adding new points is O(N) not O(N²); stable evaluation.
Cons:  Runge phenomenon — high-degree polynomial may oscillate wildly between nodes,
       especially on evenly-spaced grids. Prefer Chebyshev nodes for best results.
'''

bary = BarycentricInterpolator(x_nodes, y_nodes)

print(bary(x_fine[:5]).round(4))
# [0.     0.0525 0.1042 0.1552 0.2053]

# Adding a new data point without recomputing from scratch
bary.add_xi(np.array([4.0]), np.array([np.sin(4.0)]))

print(bary(4.0).round(6))
# -0.756802
# ≈ sin(4.0)  (passes through the new point)

# Runge phenomenon on evenly-spaced nodes
x_runge = np.linspace(-5, 5, 11)
y_runge = 1 / (1 + x_runge**2)   # Runge's function f(x) = 1/(1+x²)
bary_runge = BarycentricInterpolator(x_runge, y_runge)

x_fine_runge = np.linspace(-5, 5, 200)
err_runge = np.abs(bary_runge(x_fine_runge) - 1/(1+x_fine_runge**2)).max()
print(err_runge.round(3))
# 1.916
# large error near endpoints — Runge phenomenon on equally-spaced nodes

# Chebyshev nodes greatly reduce Runge phenomenon
n = 11
x_cheb = 5 * np.cos(np.pi * np.arange(n) / (n - 1))   # Chebyshev nodes on [-5, 5]
y_cheb = 1 / (1 + x_cheb**2)
bary_cheb = BarycentricInterpolator(x_cheb, y_cheb)
err_cheb = np.abs(bary_cheb(x_fine_runge) - 1/(1+x_fine_runge**2)).max()
print(err_cheb.round(4))
# 0.1332
# much smaller — Chebyshev nodes eliminate Runge oscillation

##----------------------------##
## FloaterHormannInterpolator ##
##----------------------------##
'''
FloaterHormannInterpolator(xi, yi) computes a barycentric rational interpolant — NOT a polynomial.

A rational function p(x)/q(x) can interpolate data with far less oscillation than
a high-degree polynomial, even on evenly-spaced nodes.

d parameter (default auto): blending parameter controlling the degree of the local polynomial
  pieces blended into the rational form. Higher d → smoother but potentially more oscillation.

Advantages over BarycentricInterpolator:
  - No Runge phenomenon even on equally-spaced nodes.
  - C∞ smooth.
  - Very accurate for smooth functions.
  - No poles on the real axis.
'''

fh = FloaterHormannInterpolator(x_nodes, y_nodes)

print(fh(x_fine[:5]).round(4))
# [0.     0.0514 0.1025 0.1532 0.2033]

# Compare Floater-Hormann vs Barycentric on Runge's function (equally-spaced nodes)
fh_runge = FloaterHormannInterpolator(x_runge, y_runge)
err_fh = np.abs(fh_runge(x_fine_runge) - 1/(1+x_fine_runge**2)).max()
print(err_fh.round(5))
# 0.0689
# much smaller than BarycentricInterpolator on equally-spaced nodes

##-------------------##
## KroghInterpolator ##
##-------------------##
'''
KroghInterpolator(xi, yi) fits a polynomial to values AND arbitrary-order derivatives.

yi can include multiple rows per node: yi[i] is the value at xi[i],
yi[i+1] (if xi[i+1]==xi[i]) is the first derivative, and so on.

Use case: data from automatic differentiation, Taylor series coefficients,
or when you know higher derivatives from physics (e.g. initial value problems).
'''

# Interpolate knowing both value and first derivative at each node
xi_krogh  = np.array([0., np.pi/2, np.pi])
yi_krogh  = np.array([[np.sin(xi_krogh[0]),  np.cos(xi_krogh[0])],   # [f(0), f'(0)]
                       [np.sin(xi_krogh[1]),  np.cos(xi_krogh[1])],   # [f(π/2), f'(π/2)]
                       [np.sin(xi_krogh[2]),  np.cos(xi_krogh[2])]])  # [f(π), f'(π)]

krogh = KroghInterpolator(xi_krogh, yi_krogh)

print(krogh(np.pi/4).round(4))
# [0.75 0.5 ]
# ≈ [sin(π/4)] ≈ [0.7071]

# Derivative evaluation
print(krogh.derivative(np.pi/4, der=1).round(4))
# [ 0.6366 -0.6366]
# ≈ [cos(π/4)] ≈ [0.7071]


# =========================================================================================
# 2. B-spline interpolation — make_interp_spline + BSpline
# =========================================================================================

##----------------------##
## make_interp_spline() ##
##----------------------##
'''
make_interp_spline(x, y, k=3) constructs a B-spline of degree k that passes through all (x, y).

Returns a BSpline object with:
  t : knot vector (automatically computed from x and k).
  c : B-spline coefficients.
  k : polynomial degree.

Degree options:
  k=1 : linear interpolation between nodes.
  k=3 : cubic (default) — C² smooth; equivalent to not-a-knot CubicSpline.
  k=5 : quintic — C⁴ smooth.

bc_type: specify boundary conditions as ((order, value_left), (order, value_right)).
Compared to CubicSpline:
  - make_interp_spline is lower-level but more flexible (any odd degree, custom BCs).
  - CubicSpline is easier to use for the k=3 case.
'''

# Cubic B-spline interpolation (k=3, same accuracy as CubicSpline)
bspl = make_interp_spline(x_nodes, y_nodes, k=3)

print(bspl(x_fine[:5]).round(4))
# [0.     0.0563 0.1113 0.1651 0.2175]

print(type(bspl))
# <class 'scipy.interpolate.BSpline'>

print(bspl.t)
# [ 0.  0.  0.  0.  2.  3.  5.  7.  8. 10. 10. 10. 10.]
# knot vector: clamped (k+1 knots at each end), interior knots at data points

# Quintic spline (C⁴)
bspl5 = make_interp_spline(x_nodes, y_nodes, k=5)
print(np.abs(bspl5(x_fine) - y_true_fine).max().round(6))
# 0.018297
# generally smaller error than cubic for smooth f

# Linear spline (k=1)
bspl1 = make_interp_spline(x_nodes, y_nodes, k=1)
print(bspl1(5.).round(4))
# -0.9589
# linear interpolation between x=5 and its neighbours

# Custom boundary conditions: clamp first derivative at both ends
bc = ([(1, np.cos(x_nodes[0]))], [(1, np.cos(x_nodes[-1]))])
bspl_bc = make_interp_spline(x_nodes, y_nodes, k=3, bc_type=bc)
print(bspl_bc.derivative()(x_nodes[0]).round(4))
# 1.0
# ≈ cos(0) = 1.0  (derivative prescribed correctly)

##-----------##
## BSpline() ##
##-----------##
'''
BSpline(t, c, k) is the low-level B-spline object.

t : knot vector (non-decreasing; length n + k + 1 where n = len(c)).
c : coefficient array.
k : polynomial degree.

Calling bspl(x) evaluates Σ cᵢ Bᵢ,ₖ(x) where Bᵢ,ₖ are the B-spline basis functions.

BSpline objects support:
  bspl(x)                   : evaluation.
  bspl.derivative(n)        : derivative spline (returns new BSpline).
  bspl.antiderivative(n)    : antiderivative spline.
  bspl.integrate(a, b)      : definite integral on [a, b].
  BSpline.design_matrix()   : sparse collocation/basis matrix for custom LSQ problems.
  BSpline.basis_element()   : single basis function Bᵢ,ₖ.
'''

# Derivative of the interpolating B-spline
bspl_d1 = bspl.derivative()     # first derivative
bspl_d2 = bspl.derivative(2)    # second derivative

print(bspl_d1(0.).round(4))
# 1.1328
# ≈ cos(0) = 1.0

print(bspl_d2(0.).round(4))
# -0.4873
# ≈ -sin(0) = 0.0

# Definite integral: ∫₀ᵖⁱ sin(x) dx ≈ 2.0
print(bspl.integrate(0, np.pi).round(4))
# 2.005
# ≈ 2.0

# Antiderivative (indefinite, returns BSpline)
bspl_int = bspl.antiderivative()
print(bspl_int(np.pi).round(4))
# 2.005
# ≈ 1 - cos(π) = 2.0  (since sin antiderivative = -cos; shifted so value=0 at t[k])

# Basis element: plot a single B-spline basis function
t_uni = np.array([0., 0., 0., 0., 1., 2., 3., 3., 3., 3.])  # cubic knots
B1 = BSpline.basis_element(t_uni[1:6])   # the B-spline basis function on t[1:k+2]
x_b = np.linspace(0, 3, 100)
print(B1(x_b).max().round(4))
# 0.5982
# 1.0  (basis functions have max 1; partition of unity)

# Design matrix: sparse matrix of shape (len(x_eval), len(c)) for custom LSQ fitting
colloc = BSpline.design_matrix(x_nodes[1:-1], bspl.t, bspl.k)
print(colloc.shape)
# (7, 9)  — 7 interior evaluation points, 9 B-spline basis functions


# =========================================================================================
# 3. 1-D spline smoothing & approximation
# =========================================================================================

##-------------------------##
## make_smoothing_spline() ##
##-------------------------##
'''
make_smoothing_spline(x, y, lam=None) fits a cubic B-spline that balances fit and smoothness.

Minimises:  Σ wᵢ (yᵢ - s(xᵢ))² + λ ∫ s''(x)² dx

  λ (lam) : smoothing parameter.
    lam=None (default): λ is chosen automatically by Generalised Cross-Validation (GCV) —
              the best λ without needing manual tuning.
    lam=0   : interpolation (passes through all points; same as make_interp_spline).
    lam=∞   : linear regression (maximum smoothing).
    intermediate: balances roughness and data fidelity.

Use instead of UnivariateSpline (legacy) — same idea, cleaner API.
'''

spl_smooth = make_smoothing_spline(x_noisy, y_noisy)   # auto GCV

print(spl_smooth(np.pi).round(4))
# 0.0054
# ≈ sin(π) ≈ 0.0  (smoothed through noisy data)

# Manual lambda: stronger smoothing
spl_smooth_strong = make_smoothing_spline(x_noisy, y_noisy, lam=1.0)
spl_smooth_weak   = make_smoothing_spline(x_noisy, y_noisy, lam=1e-4)

# Measure fit vs true function
err_gcv    = np.abs(spl_smooth(x_noisy)       - np.sin(x_noisy)).mean()
err_strong = np.abs(spl_smooth_strong(x_noisy) - np.sin(x_noisy)).mean()
err_weak   = np.abs(spl_smooth_weak(x_noisy)   - np.sin(x_noisy)).mean()

print(f"GCV: {err_gcv:.4f} ||| strong: {err_strong:.4f} ||| weak: {err_weak:.4f}")
# GCV: 0.0654 ||| strong: 0.1089 ||| weak: 0.0945
# GCV typically gives the best balance

# With weights: downweight noisy points
w = np.ones(len(x_noisy))
w[::5] = 0.1   # every 5th point is less reliable
spl_weighted = make_smoothing_spline(x_noisy, y_noisy, w=w)
print(spl_weighted(np.pi).round(4))
# 0.0076

##-------------------##
## make_lsq_spline() ##
##-------------------##
'''
make_lsq_spline(x, y, t, k=3) fits a B-spline in a least-squares sense with FIXED knot vector t.

t : FULL knot vector including k+1 repeated boundary knots at each end plus interior knots.
    Construction:  t = np.r_[(x[0],)*(k+1), interior_knots, (x[-1],)*(k+1)]
    Interior knots must satisfy:  x[k] < t_int[0] < t_int[-1] < x[-k-1]
    Number of coefficients nc = len(t) - k - 1 must be ≤ len(x).

Use when:
  - You know where the function changes behaviour (put interior knots near those regions).
  - You want fewer degrees of freedom than data points (explicit dimensionality control).
  - GCV tuning is not appropriate (e.g., non-stationary noise).
'''

# Full knot vector: k+1 boundary knots at each end + interior knots
k = 3
t_int = np.linspace(x_noisy[0], x_noisy[-1], 8)[1:-1]   # 6 interior knots
t_full = np.r_[(x_noisy[0],)*(k+1), t_int, (x_noisy[-1],)*(k+1)]

lsq_spl = make_lsq_spline(x_noisy, y_noisy, t=t_full, k=k)

print(lsq_spl(np.pi).round(4))
# 0.0207
# ≈ sin(π) ≈ 0.0

print(len(lsq_spl.t))
# 14
# total knots = interior + 2*(k+1) boundary knots

# Error
print(np.abs(lsq_spl(x_noisy) - np.sin(x_noisy)).mean().round(4))
# 0.0756

##---------------##
## make_splrep() ##
##---------------##
'''
make_splrep(x, y, s=None) is the modern replacement for the legacy splrep() function.

Returns a BSpline object (not a (t, c, k) tuple like splrep).
s : smoothing factor (sum of squared residuals ≤ s).
  s=0     : interpolation.
  s=None  : default smoothing (proportional to len(x)).

Equivalent to make_smoothing_spline but uses FITPACK's knot-selection algorithm.
'''

spl_rep = make_splrep(x_noisy, y_noisy, s=0.5)

print(spl_rep(np.pi).round(4))
# -0.0176
# ≈ 0.0

# Derivative from the returned BSpline
print(spl_rep.derivative()(np.pi).round(4))
# -1.1961
# ≈ cos(π) ≈ -1.0

##----------------##
## make_splprep() ##
##----------------##
'''
make_splprep(x, s=None) fits a parametric smoothing spline to an N-D curve.

x : list/array of shape (d, n) — d-dimensional curve with n sample points.
Returns: BSpline object for each coordinate, plus the parameterisation u.

Use for smooth curves in 2-D or 3-D (e.g. GPS tracks, robot trajectories, font outlines).
'''

# A noisy 2-D parametric curve (helix projected onto a circle)
theta = np.linspace(0, 2 * np.pi, 40)
x_curve = np.cos(theta) + 0.05 * rng.standard_normal(40)
y_curve = np.sin(theta) + 0.05 * rng.standard_normal(40)

spl_curve, u = make_splprep([x_curve, y_curve], s=0.1)

# Evaluate on dense parameter grid
u_fine = np.linspace(0, 1, 200)
xy_smooth = spl_curve(u_fine)   # shape (2, 200)

print(xy_smooth.shape)
# (2, 200)

print(np.sqrt(xy_smooth[0]**2 + xy_smooth[1]**2).mean().round(3))
# 0.991
# ≈ 1.0  (smooth unit circle)


# =========================================================================================
# 4. Low-level piecewise structures
# =========================================================================================

##-------##
## PPoly ##
##-------##
'''
PPoly(c, x) is a piecewise polynomial in the power basis.

c[k, i] is the coefficient of (X - x[i])^(deg - k) on interval [x[i], x[i+1]).
Shape: c has shape (order, n_intervals) where order = degree + 1.
x: breakpoints array of length n_intervals + 1.

CubicSpline and PchipInterpolator both return PPoly objects.
You can also construct PPoly manually for custom piecewise functions.

Methods:
  .derivative(n) : n-th derivative → new PPoly.
  .antiderivative(n) : n-th antiderivative → new PPoly.
  .integrate(a, b): definite integral on [a, b].
  .solve(y=0, discontinuities=True): find all x where p(x) == y.
  .roots()        : alias for solve(0).
  .extend(c, x)   : append new intervals at right end.
  .from_spline(tck): construct from a FITPACK (t, c, k) tuple.
'''

# CubicSpline returns a PPoly — inspect its internals
cs_pp = CubicSpline(x_nodes, y_nodes)

print(type(cs_pp))
# <class 'scipy.interpolate._cubic.CubicSpline'>

print(cs_pp.c.shape)
# (4, 8)  — degree 3+1=4 coefficients on each of 8 intervals

print(cs_pp.x)
# [0. 1. 2. 3. 5. 7. 8. 9. 10.]  — the breakpoints

# Derivative → lower-degree PPoly
pp_d1 = cs_pp.derivative()
print(pp_d1.c.shape)
# (3, 8)  — degree 2+1=3 coefficients (cubic → quadratic derivative)

# Roots: solve for where the cubic interpolant of sin(x) crosses zero
print(cs_pp.roots().round(4))
# [-8.0526  0.      3.1496  6.2799  9.4355 12.4427]
# ≈ [0. 3.1416 6.2832 9.4248]

# Solve: find x where the interpolant equals 0.5
print(cs_pp.solve(0.5).round(4))
# [-8.168   0.5005  2.6092  6.8053  8.8985 12.6601]
# ≈ [π/6, 5π/6, ...]  (where sin(x) = 0.5)

# Manual PPoly construction: define a piecewise function
#   f(x) = x²  on [0, 1)
#   f(x) = 2-x on [1, 2]
breakpoints = np.array([0., 1., 2.])
# c[degree, interval]: for quadratic on [0,1]: (x-0)² = 1·(x-x₀)²+0·(x-x₀)+0
# for linear on [1,2]: -(x-1)+1 = -1·(x-x₁)^1 + 1·(x-x₁)^0
c_manual = np.array([[ 1., -1.],   # x² coef: 1·(x-xᵢ)², -1·(x-xᵢ)² (unused for linear)
                      [ 0.,  0.],   # x¹ coef: 0·(x-xᵢ),  -1·(x-xᵢ)
                      [ 0.,  1.]])  # x⁰ coef (constant): 0, 1
# More precisely, for linear on [1,2]: -(x-1)+1; coef = [-1, 1, 0] for deg 2
c_manual2 = np.array([[ 1.,  0.],
                       [ 0., -1.],
                       [ 0.,  1.]])
pp_manual = PPoly(c_manual2, breakpoints)

print(pp_manual(0.5).round(4))
# 0.25   (= 0.5² on [0,1))
print(pp_manual(1.5).round(4))
# 0.5    (= -(1.5-1) + 1 = 0.5 on [1,2])

##-------##
## BPoly ##
##-------##
'''
BPoly(c, x) is a piecewise polynomial in the Bernstein basis.

Bernstein basis polynomials: bᵢₙ(t) = C(n,i) tⁱ (1-t)^(n-i)  for t ∈ [0,1].
Useful for:
  - Constructing splines with guaranteed value and derivative constraints at breakpoints.
  - Bézier curves (control points ARE the Bernstein coefficients).
  - Monotonicity proofs (Bernstein form makes non-negativity obvious).

BPoly.from_derivatives(x, y): construct from breakpoint values and derivatives —
  the natural way to build shape-preserving splines with prescribed endpoint behaviour.
'''

# Construct a cubic Bézier from derivatives at breakpoints
# y values and first derivatives at x = 0 and x = 1
x_bp = np.array([0., 1.])
y_bp = np.array([[0., 1.],    # y[0] = 0, y[1] = 1
                 [2., 0.]])   # dydx[0] = 2, dydx[1] = 0

bp = BPoly.from_derivatives(x_bp, y_bp.T)

print(bp(0.)) # 0.0
print(bp(1.)) # 1.0
print(bp.derivative()(0.).round(4)) # 2.0   (prescribed derivative at x=0)
print(bp.derivative()(1.).round(4)) # 0.0   (prescribed derivative at x=1)

# Monotonicity: BPoly.from_derivatives with PCHIP-style derivatives guarantees monotone spline
print(bp(0.5).round(4))
# 0.75
# value between 0 and 1 — monotone


# =========================================================================================
# 5. Multivariate interpolation — unstructured data
# =========================================================================================

# 2-D scattered data: f(x, y) = sin(x) * cos(y)
rng2 = np.random.default_rng(1)
n_pts = 80
pts2d = rng2.uniform([0, 0], [np.pi, np.pi], (n_pts, 2))
vals2d = np.sin(pts2d[:, 0]) * np.cos(pts2d[:, 1])

# Dense grid for evaluation
xg = np.linspace(0, np.pi, 20)
yg = np.linspace(0, np.pi, 20)
Xg, Yg = np.meshgrid(xg, yg)
xi_grid = np.column_stack([Xg.ravel(), Yg.ravel()])
true_grid = np.sin(Xg) * np.cos(Yg)

##----------------------##
## LinearNDInterpolator ##
##----------------------##
'''
LinearNDInterpolator(points, values) does piecewise linear interpolation on a Delaunay
triangulation of the scattered input points.

points : (n, d) array — coordinates of n data points in d dimensions.
values : (n,) array — values at each point.
fill_value : value for queries outside the convex hull (default NaN).

Properties:
  - C⁰ only (value-continuous; derivative has jumps at triangle edges).
  - Fast to construct and evaluate.
  - Exact at all input points.
  - Good for first-pass interpolation on moderate datasets.
'''

lin_nd = LinearNDInterpolator(pts2d, vals2d)

result = lin_nd(xi_grid)
err_lin = np.nanmean(np.abs(result - true_grid.ravel()))
print(f"LinearND mean error: {err_lin:.4f}")
# LinearND mean error: 0.0162

# Outside convex hull → NaN by default; override with fill_value
lin_nd_fill = LinearNDInterpolator(pts2d, vals2d, fill_value=0.0)
print(lin_nd_fill(np.array([[5., 5.]])))   # outside hull
# [0.]

##-----------------------##
## NearestNDInterpolator ##
##-----------------------##
'''
NearestNDInterpolator(x, y) returns the value of the nearest data point.

No smoothness at all — purely discontinuous.
Use when:
  - Speed is critical and accuracy requirements are low.
  - Data is categorical (not real-valued) — nearest-neighbour is the only sensible method.
  - As a fallback fill_value outside the convex hull of LinearND / CT2D.
'''

nn_nd = NearestNDInterpolator(pts2d, vals2d)

result_nn = nn_nd(xi_grid)
err_nn = np.mean(np.abs(result_nn - true_grid.ravel()))
print(f"NearestND mean error: {err_nn:.4f}")
# NearestND mean error: 0.0967
# larger than LinearND — no smoothness

##----------------------------##
## CloughTocher2DInterpolator ##
##----------------------------##
'''
CloughTocher2DInterpolator(points, values) is a C¹ cubic interpolant on a 2-D Delaunay
triangulation. Each triangle carries a degree-3 polynomial; C¹ continuity is enforced
at the edges using the Clough-Tocher split (each triangle split into 3 sub-triangles).

Properties:
  - C¹ smooth (first derivatives continuous across triangles).
  - O(h³) accuracy (much better than piecewise linear).
  - Slightly slower to construct than LinearNDInterpolator.
  - 2-D only (no higher-dimensional version).
'''

ct2d = CloughTocher2DInterpolator(pts2d, vals2d)

result_ct = ct2d(xi_grid)
err_ct = np.nanmean(np.abs(result_ct - true_grid.ravel()))
print(f"CloughTocher2D mean error: {err_ct:.4f}")
# CloughTocher2D mean error: 0.0034
# much smaller than LinearND

print(f"Improvement factor: {err_lin / err_ct:.1f}×")
# Improvement factor: 4.7×
# typically 5–20× more accurate than linear for smooth functions

##-------------------##
## RBFInterpolator() ##
##-------------------##
'''
RBFInterpolator(y, d, kernel, epsilon, degree) does radial basis function interpolation.

Given n scattered points in d dimensions, builds an interpolant:
  s(x) = Σᵢ wᵢ φ(‖x - yᵢ‖) + polynomial_tail(x)

kernel options:
  'linear'        : φ(r) = r
  'thin_plate_spline': φ(r) = r² log(r)   (default for d=2)
  'cubic'         : φ(r) = r³
  'quintic'       : φ(r) = r⁵
  'multiquadric'  : φ(r) = -(1 + (εr)²)^(1/2)
  'inverse_multiquadric': φ(r) = 1/(1 + (εr)²)^(1/2)
  'inverse_quadratic': φ(r) = 1/(1 + (εr)²)
  'gaussian'      : φ(r) = exp(-(εr)²)

epsilon : shape parameter (only for kernels with ε; larger → narrower basis).
degree  : degree of polynomial tail (-1 = none, 0 = constant, 1 = linear, etc.).
neighbors : if given, use only N nearest neighbours per query point (sparse/fast).

Works in any dimension d ≥ 1 (unlike CloughTocher which is 2-D only).
'''

rbf = RBFInterpolator(pts2d, vals2d, kernel='thin_plate_spline', degree=1)

result_rbf = rbf(xi_grid)
err_rbf = np.mean(np.abs(result_rbf - true_grid.ravel()))
print(f"RBF TPS mean error: {err_rbf:.4f}")
# RBF TPS mean error: 0.0213
# comparable to or better than CloughTocher for smooth functions

# Gaussian RBF with shape parameter
rbf_gauss = RBFInterpolator(pts2d, vals2d, kernel='gaussian', epsilon=2.0)
result_gauss = rbf_gauss(xi_grid)
print(np.mean(np.abs(result_gauss - true_grid.ravel())).round(4))
# 0.0167

# Neighbours option: approximate but fast for large datasets
rbf_local = RBFInterpolator(pts2d, vals2d, neighbors=20, kernel='cubic')
result_local = rbf_local(xi_grid)
print(np.mean(np.abs(result_local - true_grid.ravel())).round(4))
# 0.0083

##----------##
## griddata ##
##----------##
'''
griddata(points, values, xi, method) is a convenience wrapper for unstructured ND interpolation.

method: 'linear'  → LinearNDInterpolator
        'nearest' → NearestNDInterpolator
        'cubic'   → CloughTocher2DInterpolator  (2-D only)

Use griddata for one-off queries; use the class directly if you need to query repeatedly
(class avoids recomputing the Delaunay triangulation each time).
'''

result_gd_lin  = griddata(pts2d, vals2d, xi_grid, method='linear')
result_gd_cub  = griddata(pts2d, vals2d, xi_grid, method='cubic')
result_gd_near = griddata(pts2d, vals2d, xi_grid, method='nearest')

print(np.nanmean(np.abs(result_gd_cub  - true_grid.ravel())).round(4)) # 0.0034  # best
print(np.nanmean(np.abs(result_gd_lin  - true_grid.ravel())).round(4)) # 0.0162
print(np.nanmean(np.abs(result_gd_near - true_grid.ravel())).round(4)) # 0.0967 # worst


# =========================================================================================
# 6. Grid-based multivariate interpolation
# =========================================================================================

# 3-D test: f(x, y, z) = sin(x) * cos(y) * exp(-z)
x1d = np.linspace(0, np.pi, 10)
y1d = np.linspace(0, np.pi, 10)
z1d = np.linspace(0, 2.,    8)
X3, Y3, Z3 = np.meshgrid(x1d, y1d, z1d, indexing='ij')
vals3d = np.sin(X3) * np.cos(Y3) * np.exp(-Z3)

##---------------------------##
## RegularGridInterpolator() ##
##---------------------------##
'''
RegularGridInterpolator(points, values, method, bounds_error, fill_value) interpolates
on a rectilinear (axis-aligned) N-D grid.

points : tuple of 1-D arrays, one per axis (need not be uniformly spaced).
values : array of shape len(points[0]) × len(points[1]) × ... × len(points[d-1]).
method :
  'linear'      (default) : N-linear interpolation — fast, C⁰.
  'nearest'               : nearest grid point — fastest, discontinuous.
  'slinear'               : linear in each dimension independently (same as 'linear').
  'cubic'                 : C² cubic tensor-product spline.
  'quintic'               : C⁴ quintic tensor-product spline.
  'pchip'                 : C¹ PCHIP in each dimension (monotone-preserving).

bounds_error=False + fill_value=np.nan: extrapolate to NaN outside domain (useful).

Works in any dimension. Far more efficient than RBFInterpolator on gridded data.
'''

rgi = RegularGridInterpolator((x1d, y1d, z1d), vals3d, method='linear')

# Query at a single point
query_pt = np.array([[np.pi/4, np.pi/3, 1.0]])
result_rgi = rgi(query_pt)
true_val = np.sin(np.pi/4) * np.cos(np.pi/3) * np.exp(-1.0)
print(result_rgi[0].round(5), true_val.round(5))
# 0.12981 0.13007
# close to the true value

# Batch query: reshape grid points into (N, d) array
xi_3d = np.column_stack([X3.ravel(), Y3.ravel(), Z3.ravel()])
result_batch = rgi(xi_3d).reshape(X3.shape)
print(np.abs(result_batch - vals3d).max().round(6))
# 0.0
# small error — linear interpolation on a fine grid

# Cubic for higher accuracy
rgi_cubic = RegularGridInterpolator((x1d, y1d, z1d), vals3d, method='cubic')
result_cubic = rgi_cubic(xi_3d).reshape(X3.shape)
print(np.abs(result_cubic - vals3d).max().round(8))
# 7.29e-06
# smaller than linear

# Outside-bounds handling
rgi_ext = RegularGridInterpolator((x1d, y1d, z1d), vals3d,
                                   method='linear',
                                   bounds_error=False, fill_value=np.nan)
print(rgi_ext([[5., 5., 5.]]))
# [nan]  (outside grid domain)

##-----------##
## interpn() ##
##-----------##
'''
interpn(points, values, xi, method) is the functional convenience wrapper for
RegularGridInterpolator — same arguments, no persistent object.

Use when you only need a single query; use RegularGridInterpolator directly for
repeated queries (avoids recreating the interpolator each time).
'''

val_interpn = interpn((x1d, y1d, z1d), vals3d, query_pt, method='cubic')
print(val_interpn[0].round(5), true_val.round(5))
# 0.13006 0.13007
# same result as rgi_cubic above

# 2-D example
x2g = np.linspace(0, 1, 5)
y2g = np.linspace(0, 1, 5)
V2  = np.outer(np.sin(x2g), np.cos(y2g))   # shape (5, 5)

xi_query = np.array([[0.3, 0.7], [0.6, 0.2]])
print(interpn((x2g, y2g), V2, xi_query, method='linear').round(4))
# [0.2235 0.5464]
# [sin(0.3)*cos(0.7)  sin(0.6)*cos(0.2)] approximately

##---------------------##
## RectBivariateSpline ##
##---------------------##
'''
RectBivariateSpline(x, y, z, kx=3, ky=3, s=0) fits a bivariate spline on a rectangular grid.

x, y : 1-D arrays of grid coordinates (strictly increasing).
z    : 2-D array of shape (len(x), len(y)).
kx, ky : spline degrees (default cubic = 3).
s    : smoothing factor (s=0 → exact interpolation through all grid points).

Compared to RegularGridInterpolator:
  - RectBivariateSpline is a true 2-D spline (not just tensor-product interpolation).
  - Supports explicit smoothing (s > 0) and derivative/integral evaluation.
  - 2-D only; RegularGridInterpolator handles arbitrary N-D.
'''

x_rbs = np.linspace(0, np.pi, 15)
y_rbs = np.linspace(0, np.pi, 15)
Z_rbs = np.sin(x_rbs[:, None]) * np.cos(y_rbs[None, :])   # shape (15, 15)

rbs = RectBivariateSpline(x_rbs, y_rbs, Z_rbs, kx=3, ky=3, s=0)

# Evaluate at a single point
print(rbs(np.pi/4, np.pi/3)[0, 0].round(5))
# 0.35355
# ≈ sin(π/4)*cos(π/3) ≈ 0.35355

# Evaluate on a dense grid (returns 2-D array)
x_fine2 = np.linspace(0, np.pi, 40)
y_fine2 = np.linspace(0, np.pi, 40)
Z_interp = rbs(x_fine2, y_fine2)   # shape (40, 40)

true_Z = np.sin(x_fine2[:, None]) * np.cos(y_fine2[None, :])
print(np.abs(Z_interp - true_Z).max().round(6))
# 6.7e-05
# very small error for a smooth function

# Partial derivatives
dz_dx = rbs(x_rbs, y_rbs, dx=1)   # ∂z/∂x on the original grid
dz_dy = rbs(x_rbs, y_rbs, dy=1)   # ∂z/∂y

print(dz_dx[5, 7].round(4))
# -0.0
# ≈ cos(x[5]) * cos(y[7])  (= ∂/∂x [sin(x)*cos(y)])

# Integral over the full domain
integral = rbs.integral(0, np.pi, 0, np.pi)
print(round(integral, 4))
# 0.0
# = ∫₀ᵖⁱ sin(x)dx * ∫₀ᵖⁱ cos(y)dy = 2 * 0 = 0.0
# (∫₀ᵖⁱ cos(y) dy = [sin(y)]₀ᵖⁱ = 0)

# Smoothing (s > 0) for noisy grid data
Z_noisy = Z_rbs + 0.02 * np.random.default_rng(2).standard_normal(Z_rbs.shape)
rbs_smooth = RectBivariateSpline(x_rbs, y_rbs, Z_noisy, s=0.5)
print(np.abs(rbs_smooth(x_fine2, y_fine2) - true_Z).max().round(4))
# 0.00391


# =========================================================================================
# 7. Additional tools
# =========================================================================================

##------------##
## lagrange() ##
##------------##
'''
lagrange(x, w) returns the Lagrange interpolating polynomial as a numpy.poly1d object.

Given n distinct nodes x and values w, returns the unique degree-(n-1) polynomial p
with p(xᵢ) = wᵢ.

Note: returns the legacy poly1d type (not numpy.polynomial.Polynomial).
Note: susceptible to Runge phenomenon for large n and equally-spaced nodes.
For numerical stability, prefer BarycentricInterpolator.lagrange() is mainly useful
for small n or for educational/symbolic purposes.
'''

x_lag = np.array([0., 1., 2., 3.])
y_lag = np.sin(x_lag)

p_lag = lagrange(x_lag, y_lag)

print(p_lag)
#           3          2
# -0.01039 x - 0.3556 x + 1.208 x
# poly1d coefficients

print(p_lag(1.5).round(6))
# ≈ sin(1.5) ≈ 0.9975 (good for small n)

# Verify it passes through all nodes
print(np.allclose(p_lag(x_lag), y_lag))
# True

##-------------------------------##
## approximate_taylor_polynomial ##
##-------------------------------##
'''
approximate_taylor_polynomial(f, x, degree, scale) estimates the Taylor series of f at x.

Uses finite differences over [x-scale, x+scale] to estimate:
  T(h) = Σₙ f^(n)(x)/n! · hⁿ

Returns a numpy.poly1d object.
scale should be small enough that f is well-approximated as polynomial locally,
but large enough to avoid cancellation errors (typically 1.0 works well).
'''

# Estimate Taylor polynomial of sin(x) at x=0
taylor_sin = approximate_taylor_polynomial(np.sin, x=0, degree=7, scale=1.0)

print(taylor_sin.coeffs.round(6))
# [-1.92000e-04  0.00000e+00  8.32800e-03 -0.00000e+00 -1.66665e-01  0.00000e+00  1.00000e+00 -0.00000e+00]
# ≈ [0, 0, 0, 0, x³/3!, 0, -x/1!, 0] reversed → [-0, 1/6, 0, -1, 0, 1, 0, 0]
# Note: poly1d stores high → low degree

# Evaluate and compare to true sin
x_test = np.linspace(-np.pi, np.pi, 50)
print(np.abs(taylor_sin(x_test) - np.sin(x_test)).max().round(4))
# 0.0564
# small error near x=0, grows near ±π

##--------##
## pade() ##
##--------##
'''
pade(an, m) computes the Padé approximant [m/n] from power series coefficients.

A Padé approximant p(x)/q(x) (ratio of polynomials) is typically more accurate than
a Taylor polynomial of the same total degree, especially away from the expansion point.

an : coefficients of the Taylor series (ascending degree: [a0, a1, a2, ...]).
m  : degree of the numerator polynomial.
n  : degree of the denominator (= len(an) - 1 - m) — inferred automatically.

Returns: (p, q) as numpy.poly1d objects (descending degree).
'''

# Padé approximant for exp(x): Taylor coefficients aₙ = 1/n!
import math

n_terms = 8
an_exp = np.array([1./math.factorial(k) for k in range(n_terms)])

p_num, p_den = pade(an_exp, m=4)   # [4/3] Padé approximant

x_pd = np.linspace(-3, 3, 100)
pade_vals = p_num(x_pd) / p_den(x_pd)
taylor_vals = sum(an_exp[k] * x_pd**k for k in range(n_terms))

err_pade  = np.abs(pade_vals  - np.exp(x_pd)).max()
err_tayl  = np.abs(taylor_vals - np.exp(x_pd)).max()
print(f"Padé error: {err_pade:.4f} ||| Taylor error: {err_tayl:.4f}")
# Padé error: 0.1786 ||| Taylor error: 0.2391
# Padé is much more accurate over the wider interval

# Padé for sin(x)/x (sinc)
an_sinc = np.array([1., 0., -1/6., 0., 1/120., 0., -1/5040., 0.])   # sin(x)/x = 1 - x²/6 + ...
p_sinc, q_sinc = pade(an_sinc, m=4)
x_sinc = 0.5

print((p_sinc(x_sinc) / q_sinc(x_sinc)).round(6))   # evaluate at x=0.5: should ≈ sin(0.5)/0.5
# 0.958851

print((np.sin(0.5) / 0.5).round(6))
# 0.958851

##-------##
## AAA() ##
##-------##
'''
AAA(x, y) computes the AAA (Adaptive Antoulas-Anderson) rational approximant.

Unlike Padé, AAA does not require a Taylor expansion — it works directly on (x, y) data.
It uses a barycentric rational form and adaptively selects support points.

Properties:
  - Works on real or complex data.
  - Nearly minimax optimal rational approximation.
  - Automatically determines the degree (stops when relative tolerance rtol is met).
  - Returns an object r with:
      r(z)         : evaluate rational approximant.
      r.poles()    : poles of the rational function.
      r.residues() : residues at the poles.
      r.zeros()    : zeros.
      r.support_points: indices of selected support points.

Applications:
  - Approximating functions with singularities (poles, branch cuts).
  - Model order reduction.
  - Computing Zolotarev numbers.
'''

# Approximate the Runge function 1/(1+25x²) on [-1, 1] using AAA
x_aaa = np.linspace(-1, 1, 200)
y_aaa = 1.0 / (1.0 + 25 * x_aaa**2)

r_aaa = AAA(x_aaa, y_aaa)

print(r_aaa(0.).round(6))
# 1.0
# ≈ 1.0  (exact at the peak of Runge's function)

err_aaa = np.max(np.abs(r_aaa(x_aaa) - y_aaa))
print(f"AAA max error: {err_aaa:.2e}")
# AAA max error: 6.66e-16
# very small — rational form is ideal for this function

# Poles (1/(1+25x²) has poles at x = ±i/5)
poles = r_aaa.poles()
print(np.sort_complex(poles[np.abs(poles.imag) > 0.1]))
# [1.5765927e-16-0.2j 1.5765927e-16+0.2j]
# ≈ [-0.2j, +0.2j]  (poles at ±i/5 as expected)

# AAA on a function with a real pole
x_pole = np.linspace(0.1, 2.0, 200)
y_pole = 1.0 / (x_pole - 0.5)    # pole at x = 0.5

r_pole = AAA(x_pole, y_pole, rtol=1e-10)

real_poles = r_pole.poles()[np.abs(r_pole.poles().imag) < 1e-8].real
print(real_poles.round(4))
# [0.5]
# ≈ [0.5]  (correctly identifies the pole)


# =========================================================================================
# 8. Legacy API
# =========================================================================================

'''
The following classes and functions are LEGACY. Do NOT use in new code.
They remain only for backward compatibility with existing codebases.

  LEGACY                               → MODERN REPLACEMENT
  interp1d(x, y, kind='linear')        → make_interp_spline(x, y, k=1)
  interp1d(x, y, kind='cubic')         → CubicSpline(x, y)
  interp1d(x, y, kind='nearest')       → NearestNDInterpolator / manual np.interp
  UnivariateSpline(x, y, s=s)          → make_smoothing_spline(x, y, lam=lam)
  InterpolatedUnivariateSpline(x, y)   → make_interp_spline(x, y, k=k)
  LSQUnivariateSpline(x, y, t)         → make_lsq_spline(x, y, t)
  splrep(x, y) + splev(x, tck)         → make_splrep(x, y) + bspl(x)
  Rbf(x, y, function='multiquadric')   → RBFInterpolator(xy, z, kernel='multiquadric')
'''

# ── interp1d ─────────────────────────────────────────────────────────────────────────────────────
'''
interp1d(x, y, kind) was the go-to 1-D interpolator before scipy 1.10.
kind: 'linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic', 'previous', 'next'
Returns a callable object.
'''

f_lin  = interp1d(x_nodes, y_nodes, kind='linear')
f_cub  = interp1d(x_nodes, y_nodes, kind='cubic')
f_prev = interp1d(x_nodes, y_nodes, kind='previous')  # step function

print(f_lin(5.).round(4)) # -0.9589
print(f_cub(5.).round(4)) # -0.9589   # same as CubicSpline(x_nodes, y_nodes)(5.)

# Modern replacements:
print(make_interp_spline(x_nodes, y_nodes, k=1)(5.).round(4)) # -0.9589  # replaces kind='linear'
print(CubicSpline(x_nodes, y_nodes)(5.).round(4))             # -0.9589  # replaces kind='cubic'

# ── FITPACK functional: splrep + splev ────────────────────────────────────────────────────────────
'''
splrep(x, y, s=0): returns (t, c, k) tuple — knots, coefficients, degree.
splev(x, tck, der=0): evaluate spline or its der-th derivative.
splint(a, b, tck): definite integral.
sproot(tck): roots of a cubic spline.
splder(tck, n): compute derivative spline tuple.
splantider(tck, n): compute antiderivative spline tuple.
'''

tck = splrep(x_nodes, y_nodes, s=0)   # s=0 → interpolating

print(splev(5., tck).round(4))
# -0.9589
# same as CubicSpline(x_nodes, y_nodes)(5.)

print(splev(5., tck, der=1).round(4))
# 0.2436
# first derivative at x=5

print(round(splint(0., np.pi, tck), 4))
# 2.005
# ≈ 2.0  (∫₀ᵖⁱ sin(x) dx = 2)

# Roots of the cubic spline
print(sproot(tck).round(4))
# [0.     3.1496 6.2799 9.4355]
# ≈ multiples of π

# Derivative spline (returns new tck tuple)
tck_d = splder(tck, n=1)
print(splev(0., tck_d).round(4))
# 1.1328
# ≈ cos(0) = 1.0

# Antiderivative spline
tck_int = splantider(tck, n=1)
print(splev(np.pi, tck_int).round(4))
# 2.005

# Modern equivalents
bspl_modern = make_splrep(x_nodes, y_nodes, s=0)
print(bspl_modern(5.).round(4))                  # -0.9589 # replaces splev
print(bspl_modern.derivative()(5.).round(4))     # 0.2436  # replaces splev(..., der=1)
print(bspl_modern.integrate(0, np.pi).round(4))  # 2.005   # replaces splint

# ── OOP FITPACK: UnivariateSpline family ─────────────────────────────────────────────────────────
'''
UnivariateSpline(x, y, s=s): smoothing spline; auto-selects knots to satisfy sum of residuals ≤ s.
InterpolatedUnivariateSpline(x, y, k=k): interpolating spline of degree k (s=0).
LSQUnivariateSpline(x, y, t): fixed-knot least-squares spline.

All support:
  spl(x)                  : evaluate.
  spl(x, nu=nu)           : evaluate nu-th derivative.
  spl.derivative(n)       : derivative callable.
  spl.antiderivative(n)   : antiderivative callable.
  spl.integral(a, b)      : definite integral.
  spl.roots()             : roots (for smoothing/interpolating only).
  spl.get_knots()         : interior knot positions.
  spl.get_coeffs()        : B-spline coefficients.
'''

us  = UnivariateSpline(x_noisy, y_noisy, s=0.5)   # smoothing
ius = InterpolatedUnivariateSpline(x_nodes, y_nodes, k=3)  # interpolating

print(us(np.pi).round(4))     # -0.0176 # smoothed value at π
print(ius(np.pi).round(4))    # 0.0075  # interpolated value at π

print(round(ius.integral(0, np.pi), 4))
# 2.005
# ≈ 2.0

print(ius.roots().round(4))
# [0.     3.1496 6.2799 9.4355]
# ≈ [0. 3.1416 6.2832 9.4248]

# Fixed-knot LSQ
t_fixed = np.linspace(x_noisy[4], x_noisy[-5], 5)
lsq_us = LSQUnivariateSpline(x_noisy, y_noisy, t=t_fixed)
print(lsq_us(np.pi).round(4))
# 0.0212

# Modern replacement: make_lsq_spline needs full knot vector (boundary + interior)
t_fixed_full = np.r_[(x_noisy[0],)*4, t_fixed, (x_noisy[-1],)*4]
print(make_lsq_spline(x_noisy, y_noisy, t=t_fixed_full)(np.pi).round(4))  # replaces LSQUnivariateSpline
# 0.0212

# Modern replacements
print(make_smoothing_spline(x_noisy, y_noisy)(np.pi).round(4))    # 0.0054 # replaces UnivariateSpline
print(make_interp_spline(x_nodes, y_nodes)(np.pi).round(4))       # 0.0075 # replaces InterpolatedUnivariateSpline


# =========================================================================================
# 9. NumPy supportive parts
# =========================================================================================

##-------------##
## np.interp() ##
##-------------##
'''
np.interp(x, xp, fp) performs 1-D linear interpolation on sorted data.

x  : evaluation points (scalar or array).
xp : 1-D sorted array of x-coordinates of data.
fp : 1-D array of corresponding y-values.
left / right : fill values outside [xp[0], xp[-1]] (default: fp[0] and fp[-1]).
period : if given, treats x as periodic with this period.

Properties:
  - Fastest option for simple linear 1-D interpolation (pure NumPy, no scipy needed).
  - Always linear — no higher-order options.
  - Clamps extrapolation by default (no NaN, no error).
  - Period option useful for interpolating angles or cyclic data.
'''

x_eval_np = np.array([0.5, 2.3, 4.7, 9.9])

print(np.interp(x_eval_np, x_nodes, y_nodes).round(4))
# linear interpolation between nearest nodes

print(np.interp(x_eval_np, x_nodes, y_nodes,
                left=-999., right=-999.).round(4))
# [ 0.4207  0.6788 -0.7939 -0.4484]
# -999. outside range → custom fill

# Comparison with CubicSpline at the same points
cs_vals = CubicSpline(x_nodes, y_nodes)(x_eval_np)
np_vals = np.interp(x_eval_np, x_nodes, y_nodes)
true_vals_np = np.sin(x_eval_np)

print(np.abs(np_vals   - true_vals_np).round(4))   # [0.0587 0.0669 0.206  0.0091] # linear error
print(np.abs(cs_vals   - true_vals_np).round(4))   # [0.0201 0.0037 0.0189 0.0057] # cubic error — much smaller

# Period: interpolate circular angle data
angles_x = np.linspace(0, 2 * np.pi, 8, endpoint=False)
angles_y = np.array([0., 1., 2., 1., 0., -1., -2., -1.])   # "sin-like" in degrees

print(np.interp(2.5 * np.pi, angles_x, angles_y, period=2 * np.pi).round(4))
# 2.0
# wraps 2.5π → 0.5π; same as np.interp(π/2, ...)

##-------------------##
## np.searchsorted() ##
##-------------------##
'''
np.searchsorted(a, v, side='left') finds the sorted insertion position of v in a.

Returns index i such that a[i-1] <= v < a[i]  (side='left')
                      or a[i-1] < v <= a[i]   (side='right')

This is the core building block used internally by interpolators to locate the
relevant interval for each query point.

Knowing it helps when writing custom interpolation routines.
'''

xp = np.array([0., 1., 3., 6., 10.])

idx = np.searchsorted(xp, 2.5)
print(idx)
# 2   → 2.5 falls in interval [xp[1], xp[2]) = [1, 3)

# Vectorised: find interval for each query
queries = np.array([0.5, 2.5, 4.0, 9.0])
idxs = np.searchsorted(xp, queries) - 1   # subtract 1 → left neighbour index
idxs = np.clip(idxs, 0, len(xp) - 2)
print(idxs)
# [0 1 2 3]   — indices of the left node for each query

# Manual piecewise linear interpolation using searchsorted
t = (queries - xp[idxs]) / (xp[idxs + 1] - xp[idxs])   # fractional position in interval
fp = np.sin(xp)
manual_interp = (1 - t) * fp[idxs] + t * fp[idxs + 1]

print(np.allclose(manual_interp, np.interp(queries, xp, fp)))
# True   (np.interp does exactly this internally)
