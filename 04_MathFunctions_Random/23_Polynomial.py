'''
numpy.polynomial  —  modern API  (recommended for all new code)
================================================================
All six convenience classes share an identical interface.
Coefficient convention: coef[i] is the coefficient of degree i  (low → high order).
This is the REVERSE of legacy poly1d which stores highest-degree first.

1. Polynomial (power series)  —  numpy.polynomial.polynomial.Polynomial
   p(x) = c0 + c1·x + c2·x² + ...
   + Polynomial(coef)           : construct from coefficient array [c0, c1, c2, ...].
   + Polynomial.fromroots(r)    : construct from roots.
   + Polynomial.fit(x, y, deg)  : least-squares fit to data.
   + Polynomial.basis(deg)      : single basis polynomial of given degree.

2. Shared convenience-class interface  (identical across all six classes)
   Construction & class methods:
   + Class(coef)                : from coefficient array.
   + Class.fromroots(roots)     : from roots; expands into the class's basis.
   + Class.fit(x, y, deg, ...)  : least-squares fit; handles domain/window mapping.
   + Class.basis(deg)           : unit basis polynomial (one non-zero coefficient).
   + Class.identity()           : the identity map p(x) = x in the class's basis.
   Attributes:
   + p.coef                     : coefficient array.
   + p.degree()                 : degree of the polynomial.
   + p.domain                   : [lo, hi] interval of the data/input.
   + p.window                   : [lo, hi] interval that domain maps to (default [-1, 1]).
   Evaluation & arithmetic:
   + p(x)                       : evaluate at scalar, array, or another polynomial.
   + p + q, p - q, p * q        : arithmetic (result stays in same class).
   + p // q, p % q, divmod(p,q) : polynomial floor-division and remainder.
   + p ** n                     : repeated multiplication.
   Calculus:
   + p.deriv(m=1)               : m-th derivative.
   + p.integ(m=1, k=0, lbnd=0)  : m-th antiderivative; k = integration constants.
   Roots & conversion:
   + p.roots()                  : all roots of the polynomial.
   + p.convert(kind, domain, window): change class or domain/window.
   + p.mapparms()               : (shift, scale) mapping from domain to window.
   Trimming & utilities:
   + p.trim(tol)                : remove trailing coefficients below tolerance.
   + p.cutdeg(deg)              : truncate to at most degree deg.
   + p.truncate(size)           : truncate to at most size coefficients.
   + p.linspace(n, domain)      : n evenly-spaced (x, y) pairs over domain.
   + p.copy()                   : return an independent copy.

3. Chebyshev  —  numpy.polynomial.chebyshev.Chebyshev
   p(x) = Σ cₙ Tₙ(x),   Tₙ(cos θ) = cos(nθ)
   Best choice for numerical computation: near-optimal approximation, minimal Runge effect.
   Same interface as Polynomial; all examples below use the shared API.

4. Legendre  —  numpy.polynomial.legendre.Legendre
   p(x) = Σ cₙ Pₙ(x),   orthogonal on [-1, 1] w.r.t. weight 1.
   Used in Gauss-Legendre quadrature, physics (spherical harmonics connection).

5. Hermite (physicists)  —  numpy.polynomial.hermite.Hermite
   p(x) = Σ cₙ Hₙ(x),   Hₙ(x) = (-1)ⁿ eˣ² (d/dx)ⁿ e^{-x²}
   Orthogonal on (-∞, ∞) w.r.t. weight e^{-x²}.
   Used in quantum harmonic oscillator, Gaussian quadrature.

6. HermiteE (probabilists)  —  numpy.polynomial.hermite_e.HermiteE
   p(x) = Σ cₙ Heₙ(x),   Heₙ(x) = (-1)ⁿ eˣ²/2 (d/dx)ⁿ e^{-x²/2}
   Orthogonal on (-∞, ∞) w.r.t. weight e^{-x²/2}.
   Used in statistics (Edgeworth expansion), Hermite-Gauss quadrature.

7. Laguerre  —  numpy.polynomial.laguerre.Laguerre
   p(x) = Σ cₙ Lₙ(x),   orthogonal on [0, ∞) w.r.t. weight e^{-x}.
   Used in Gauss-Laguerre quadrature, hydrogen radial wave functions.

8. Legacy API  (numpy.poly1d — do NOT use in new code)
   Coefficient convention: highest degree first  [cN, ..., c1, c0]
   + np.poly1d(coef)            : construct from high→low coefficient array.
   + np.poly(roots)             : coefficient array from roots.
   + np.polyval(p, x)           : evaluate polynomial at x.
   + np.polyfit(x, y, deg)      : least-squares fit; returns high→low coefficients.
   + np.polyder(p, m)           : m-th derivative coefficients.
   + np.polyint(p, m, k)        : m-th antiderivative coefficients.
   + np.polyadd/polysub/polymul/polydiv: arithmetic on coefficient arrays.
   + np.roots(coef)             : roots from high→low coefficient array.
'''

import numpy as np
from numpy.polynomial import (
                               Chebyshev,
                               Hermite,
                               HermiteE,
                               Laguerre,
                               Legendre,
                               Polynomial,
)

# ── Shared sample data ───────────────────────────────────────────────────────────────────────────
rng = np.random.default_rng(0)

x_data = np.linspace(-1, 1, 20)
y_data = np.sin(np.pi * x_data) + 0.1 * rng.standard_normal(20)  # noisy sine

x_eval = np.array([-1., -0.5, 0., 0.5, 1.])


# =========================================================================================
# 1. Polynomial (power series)
# =========================================================================================

##--------------##
## Polynomial() ##
##--------------##
'''
Polynomial(coef) represents p(x) = c0 + c1·x + c2·x² + ... + cN·xᴺ

coef[i] is the coefficient of xⁱ  (ascending degree — index equals degree).
This is OPPOSITE to legacy poly1d which stores [cN, ..., c0] (descending).

domain  : [lo, hi] range of the input variable  (default [-1, 1]).
window  : [lo, hi] range that domain linearly maps to  (default [-1, 1]).
When domain == window the polynomial is in "natural" (unscaled) form.
'''

# p(x) = 1 + 2x + 3x²  → coef = [1, 2, 3]
p = Polynomial([1., 2., 3.])

p
# Polynomial([1., 2., 3.], domain=[-1.,  1.], window=[-1.,  1.], symbol='x')

print(p)
# 1.0 + 2.0·x + 3.0·x²

print(p.coef)
# [1. 2. 3.]

print(p.degree())
# 2

# Evaluate at a scalar
print(p(0.))
# 1.0   (p(0) = 1 + 0 + 0)

print(p(1.))
# 6.0   (1 + 2 + 3)

print(p(-1.))
# 2.0   (1 - 2 + 3)

# Evaluate at an array
print(p(x_eval))
# [2.   0.75 1.   2.75 6.  ]

# Polynomial composition: substitute another polynomial for x
q_shift = Polynomial([1., 1.])   # q(x) = 1 + x
print(p(q_shift).coef)
# [6. 8. 3.]  — p(1+x) = 1+2(1+x)+3(1+x)² = 6+8x+3x²

##------------------------##
## Polynomial.fromroots() ##
##------------------------##
'''
Polynomial.fromroots(roots) constructs the unique monic polynomial with the given roots.

p(x) = (x - r0)(x - r1)···(x - rN)
Complex conjugate pairs produce real coefficients when roots come in conjugate pairs.
'''

p_r = Polynomial.fromroots([1., 2., 3.])

p_r
# Polynomial([-6., 11., -6.,  1.], ...)   → -6 + 11x - 6x² + x³

print(p_r)
# -6.0 + 11.0·x - 6.0·x² + 1.0·x³

print(p_r(1.), p_r(2.), p_r(3.))
# 0.0  0.0  0.0   (verifies roots)

# Complex conjugate pair → real coefficients
p_cplx = Polynomial.fromroots([1j, -1j])   # roots at ±i
print(p_cplx.coef.real)
# [1. 0. 1.]   → x² + 1

##------------------##
## Polynomial.fit() ##
##------------------##
'''
Polynomial.fit(x, y, deg) fits a polynomial of given degree to data using least squares.

Key differences from legacy np.polyfit():
  - Returns a Polynomial object (not just coefficients).
  - Automatically sets domain = [min(x), max(x)] and maps it to window = [-1, 1].
  - This domain/window scaling prevents ill-conditioning for large or shifted x values.
  - Use p.convert() to recover coefficients in the unscaled natural basis.
  - Supports weight array w and full=True for residuals/rank/singular values.
'''

p_fit = Polynomial.fit(x_data, y_data, deg=5)

print(p_fit)
# -0.04990745 + 2.81821027·x + 0.05307845·x² - 4.17038099·x³ + 0.04942161·x⁴ + 1.39896223·x⁵

print(p_fit.domain)
# [-1.  1.]  (auto-set from x_data range)

print(p_fit(0.).round(4))
# -0.0499

print(p_fit(0.5).round(4))
# 0.898

# Convert to recover unscaled coefficients in the natural power basis
p_natural = p_fit.convert()
print(p_natural.coef.round(4))
# [-0.0499  2.8182  0.0531 -4.1704  0.0494  1.399 ]
# unscaled power-series coefficients [c0, c1, ..., c5]

# Comparison: np.polyfit returns bare array; harder to use safely
coef_legacy = np.polyfit(x_data, y_data, deg=5)
print(coef_legacy.round(4))
# [ 1.399   0.0494 -4.1704  0.0531  2.8182 -0.0499]
# [cN, ..., c0] descending — error-prone

##--------------------##
## Polynomial.basis() ##
##--------------------##
'''
Polynomial.basis(deg) returns the unit basis polynomial of given degree.
Polynomial.basis(n) = xⁿ  (the monomial of degree n).
Polynomial.identity() returns the identity map p(x) = x.
'''

print(Polynomial.basis(0).coef)
# [1.]   → 1

print(Polynomial.basis(3).coef)
# [0. 0. 0. 1.]   → x³

print(Polynomial.basis(3)(2.))
# 8.0   (2³ = 8)

print(Polynomial.identity().coef)
# [0. 1.]   → x


# =========================================================================================
# 2. Shared convenience-class interface
# =========================================================================================

# Use Polynomial throughout; all methods work identically on Chebyshev, Legendre, etc.
p = Polynomial([1., 2., 3.])      # 1 + 2x + 3x²
q = Polynomial([0., 1., 0., 1.])  # x + x³

##----------------------------------##
## Attributes: coef, degree, domain ##
##----------------------------------##

print(p.coef)
# [1. 2. 3.]

print(p.degree())
# 2

print(p.domain, p.window)
# [-1.  1.] [-1.  1.]

##------------##
## Arithmetic ##
##------------##
'''
All six classes support +, -, *, //, %, divmod, **.
Result inherits the type of the left operand.
Polynomials with mismatched domain/window raise TypeError — use .convert() first.
Note: instances are immutable; augmented operators (+=, -=) are not supported.
'''

print((p + q).coef)
# [1. 3. 3. 1.]   coefficients added degree-by-degree

print((p - q).coef)
# [ 1.  1.  3. -1.]

print((p * q).coef)
# [0. 1. 0. 4. 2. 3.]   (convolution of coefficients)

print((q ** 2).coef)
# [0. 0. 1. 0. 2. 0. 1.]   (x + x³)² = x² + 2x⁴ + x⁶

# Floor division and remainder: q = quot * p + rem
quot, rem = divmod(q, p)
print(quot.coef.round(4)) # [-0.2222  0.3333]
print(rem.coef.round(4)) # [0.2222 1.1111]

print(np.allclose((quot * p + rem).coef, q.coef))
# True   (verifies the division identity)

##-------------------------##
## Calculus: deriv / integ ##
##-------------------------##
'''
p.deriv(m=1) computes the m-th derivative.
p.integ(m=1, k=0, lbnd=0) computes the m-th antiderivative.
  k    : integration constant(s) — scalar or list of m constants.
  lbnd : lower bound of integration (value where antiderivative = 0).
Both return a new polynomial in the same class.
'''

p_d = Polynomial([3., 2., 1.])   # 3 + 2x + x²

print(p_d.deriv(1).coef)
# [2. 2.]   → 2 + 2x  (d/dx [3 + 2x + x²] = 2 + 2x)

print(p_d.deriv(2).coef)
# [2.]      → 2       (d²/dx²)

print(p_d.deriv(3).coef)
# [0.]      → 0       (all higher derivatives vanish)

# Antiderivative: ∫(3 + 2x + x²) dx = 3x + x² + x³/3 + C
print(p_d.integ(1).coef)
# [0.     3.     1.     0.3333]  (C = 0 by default, lbnd = 0)

print(p_d.integ(1, k=5).coef)
# [5.     3.     1.     0.3333]  (constant of integration = 5)

print(p_d.integ(1, lbnd=1).coef)
# [-4.     3.     1.     0.3333]  (antiderivative is 0 at x=1)

# Verify: derivative of antiderivative recovers original
print(np.allclose(p_d.integ(1).deriv(1).coef, p_d.coef))
# True

# Double antiderivative
print(p_d.integ(2).coef)
# [0.     0.     1.5    0.3333  0.0833]

##-------##
## Roots ##
##-------##
'''
p.roots() returns all n roots as a complex array (companion-matrix eigenvalues).
For real polynomials, complex roots always appear in conjugate pairs.
'''

p_root = Polynomial([-6., 11., -6., 1.])   # (x-1)(x-2)(x-3)

print(p_root.roots())
# [1.  2.  3.]   (all real)

p_quad = Polynomial([1., 0., 1.])   # 1 + x²  → roots at ±i
print(p_quad.roots())
# [0.-1.j  0.+1.j]

# Round-trip: fromroots → roots
roots_in = [1., -1., 2.]
p_check = Polynomial.fromroots(roots_in)
print(np.sort(p_check.roots().real).round(10))
# [-1.  1.  2.]

##---------##
## Convert ##
##---------##
'''
p.convert(kind, domain, window) converts a polynomial to another class or domain.

kind   : target class (e.g. Chebyshev, Legendre).  Default: same class.
domain : new domain interval.  Default: same domain.
window : new window interval.  Default: same window.

The polynomial value is unchanged — only its internal representation changes.
Essential when mixing polynomials built in different domains (e.g. after .fit()).
'''

p_poly = Polynomial([1., 0., -1.])   # 1 - x²

# Convert to Chebyshev representation (1 - x² = 0.5·T0 + 0 - 0.5·T2)
p_cheb = p_poly.convert(kind=Chebyshev)
print(p_cheb.coef)
# [ 0.5  0.  -0.5]

# Values must match everywhere
x_test = np.linspace(-1, 1, 50)
print(np.allclose(p_poly(x_test), p_cheb(x_test)))
# True

# mapparms(): returns (off, scl) such that x → off + scl * x maps domain to window
p_shifted = Polynomial([1., 2., 3.], domain=[0., 4.])
print(p_shifted.mapparms())
# (-1.0, 0.5)   → maps [0, 4] to [-1, 1] via  -1 + 0.5·x

##------------##
## Trim / cut ##
##------------##
'''
p.trim(tol)      : remove trailing near-zero coefficients (absolute value ≤ tol).
p.cutdeg(deg)    : zero out all coefficients above degree deg, then trim.
p.truncate(size) : keep only the first `size` coefficients.
'''

p_noisy = Polynomial([1., 2., 3., 1e-15, -2e-16])

print(p_noisy.trim().coef)
# [ 1.e+00  2.e+00  3.e+00  1.e-15 -2.e-16]  (tol=0: only exact zeros removed; near-zeros kept)

print(p_noisy.trim(tol=1e-14).coef)
# [1. 2. 3.]   (removes coefficients whose |value| ≤ 1e-14)

print(p_noisy.cutdeg(1).coef)
# [1. 2.]   (truncate to degree 1)

print(p_noisy.truncate(2).coef)
# [1. 2.]   (keep only first 2 coefficients)

##----------##
## Linspace ##
##----------##
'''
p.linspace(n, domain) returns (x, y) arrays: n evenly-spaced evaluation points.
Convenient for plotting — no need to manually construct x.
'''

p_ls = Polynomial([0., 0., 1.])   # x²
x_pts, y_pts = p_ls.linspace(5)

print(x_pts)
# [-1.  -0.5   0.   0.5   1. ]

print(y_pts)
# [1.   0.25  0.   0.25  1. ]


# =========================================================================================
# 3. Chebyshev
# =========================================================================================

##-----------##
## Chebyshev ##
##-----------##
'''
Chebyshev represents p(x) = Σ cₙ Tₙ(x) in the Chebyshev basis.

Chebyshev polynomials: T₀=1, T₁=x, T₂=2x²-1, T₃=4x³-3x, ...
Defined by:  Tₙ(cos θ) = cos(nθ)

Why use Chebyshev over plain Polynomial?
  - Minimax property: degree-n Chebyshev truncation minimises the maximum error
    over [-1, 1] among all polynomials of the same degree.
  - Numerically stable: the Chebyshev basis is well-conditioned at high degree
    where power-series fitting breaks down (Runge phenomenon / ill-conditioning).
  - Clenshaw-Curtis quadrature uses Chebyshev nodes for near-optimal integration.

All interface methods are identical to Polynomial.
'''

T_poly = Chebyshev([1., 0., -0.5])   # T0 - 0.5·T2

print(T_poly.coef)
# [ 1.   0.  -0.5]

# T0(x)=1, T2(x)=2x²-1  →  T0 - 0.5·T2 = 1 - 0.5(2x²-1) = 1.5 - x²
print(T_poly(0.))
# 1.5

print(T_poly(1.))
# 0.5   (1 - 0.5·1 = 0.5)

# Basis functions
print(Chebyshev.basis(2)(0.5))   # T2(0.5) = 2(0.25) - 1 = -0.5
# -0.5

# Fitting with Chebyshev: numerically superior at higher degrees
T_fit = Chebyshev.fit(x_data, y_data, deg=7)

print(T_fit(0.).round(4))
# ≈ 0.0

# Compare residuals at x_eval: Chebyshev vs Polynomial at deg=7
P_fit7 = Polynomial.fit(x_data, y_data, deg=7)
true_vals = np.sin(np.pi * x_eval)
print(np.abs(T_fit(x_eval) - true_vals).round(5))    # Chebyshev errors
print(np.abs(P_fit7(x_eval) - true_vals).round(5))   # Polynomial errors
# Both similar at deg=7 on this small dataset; Chebyshev advantage grows at higher degree

# Convert Chebyshev fit to power series to read off standard coefficients
T_as_poly = T_fit.convert(kind=Polynomial)
print(T_as_poly.coef.round(4))

# Roots of a Chebyshev polynomial: T3(x) = 4x³ - 3x → cos(π/6), cos(π/2), cos(5π/6)
T3 = Chebyshev.basis(3)
print(np.sort(T3.roots().real).round(4))
# [-0.866  0.     0.866]

# Deriv and integ work in Chebyshev basis directly
T2 = Chebyshev.basis(2)   # T2(x) = 2x² - 1
print(T2.deriv(1).coef)
# [0. 4.]  → in Chebyshev basis: 4·T1 = 4x  ✓  (d/dx [2x²-1] = 4x)


# =========================================================================================
# 4. Legendre
# =========================================================================================

##----------##
## Legendre ##
##----------##
'''
Legendre represents p(x) = Σ cₙ Pₙ(x) — Legendre polynomials.

P₀=1, P₁=x, P₂=(3x²-1)/2, P₃=(5x³-3x)/2, ...
Orthogonal on [-1, 1]:  ∫₋₁¹ Pₘ(x)Pₙ(x) dx = 2/(2n+1) · δₘₙ

Applications:
  - Gauss-Legendre quadrature: nodes are roots of Pₙ, weights derived analytically.
  - Spectral methods for PDEs on [-1, 1].
  - Associated Legendre polynomials underlie spherical harmonics in physics.
'''

Leg = Legendre([1., 0., 0.5])   # P0 + 0.5·P2

print(Leg.coef)
# [1.  0.  0.5]

# P2(0) = (3·0-1)/2 = -0.5
print(Leg(0.))
# 0.75   (1·P0(0) + 0.5·P2(0) = 1 + 0.5·(-0.5) = 0.75)

# Orthogonality: ∫₋₁¹ P0(x)·P2(x) dx = 0
P0_leg = Legendre.basis(0)
P2_leg = Legendre.basis(2)
x_int = np.linspace(-1, 1, 10000)
print(np.trapezoid((P0_leg * P2_leg)(x_int), x_int).round(6))
# 0.0

# Gauss-Legendre quadrature: nodes = roots of Pₙ
P5_leg = Legendre.basis(5)
gl_nodes = np.sort(P5_leg.roots().real)
print(gl_nodes.round(6))
# [-0.90618  -0.538469   0.         0.538469   0.90618 ]

# Fitting
Leg_fit = Legendre.fit(x_data, y_data, deg=5)
print(Leg_fit(0.5).round(4))
# ≈ sin(π·0.5) ≈ 1.0


# =========================================================================================
# 5. Hermite (physicists)
# =========================================================================================

##---------##
## Hermite ##
##---------##
'''
Hermite represents p(x) = Σ cₙ Hₙ(x) — physicists' Hermite polynomials.

H₀=1, H₁=2x, H₂=4x²-2, H₃=8x³-12x, ...
Recurrence:  Hₙ₊₁(x) = 2x Hₙ(x) - 2n Hₙ₋₁(x)
Orthogonal on (-∞, ∞) w.r.t. weight e^{-x²}:
  ∫₋∞∞ Hₘ(x) Hₙ(x) e^{-x²} dx = √π · 2ⁿ · n! · δₘₙ

Applications:
  - Quantum harmonic oscillator wave functions: ψₙ(x) ∝ Hₙ(x) e^{-x²/2}
  - Gauss-Hermite quadrature for ∫₋∞∞ f(x) e^{-x²} dx.
'''

H = Hermite([1., 0., 0.5])   # H0 + 0.5·H2

print(H)
# 1.0 + 0.0·H₁(x) + 0.5·H₂(x)

print(H.coef)
# [1.  0.  0.5]

# H2(1) = 4·1 - 2 = 2  →  H(1) = H0(1) + 0.5·H2(1) = 1 + 0.5·2 = 2.0
print(H(1.))
# 2.0

# H3 in power-series form: H3(x) = 8x³ - 12x
H3 = Hermite.basis(3)
print(H3.convert(kind=Polynomial).coef)
# [  0. -12.   0.   8.]   → -12x + 8x³  ✓

print(H3(2.).round(4))
# 40.0   (8·8 - 12·2 = 40)

# Orthogonality (numerical check with Gaussian weight)
x_h = np.linspace(-5, 5, 100000)
w_h = np.exp(-x_h**2)
H0_vals = Hermite.basis(0)(x_h)
H2_vals = Hermite.basis(2)(x_h)
print(np.trapezoid(H0_vals * H2_vals * w_h, x_h).round(4))
# 0.0   (orthogonal)


# =========================================================================================
# 6. HermiteE (probabilists)
# =========================================================================================

##----------##
## HermiteE ##
##----------##
'''
HermiteE represents p(x) = Σ cₙ Heₙ(x) — probabilists' Hermite polynomials.

He₀=1, He₁=x, He₂=x²-1, He₃=x³-3x, He₄=x⁴-6x²+3, ...
Recurrence:  Heₙ₊₁(x) = x Heₙ(x) - n Heₙ₋₁(x)
Orthogonal on (-∞, ∞) w.r.t. weight e^{-x²/2}:
  ∫₋∞∞ Heₘ(x) Heₙ(x) e^{-x²/2} dx = √(2π) · n! · δₘₙ

Relation to physicists':  Hₙ(x) = 2^(n/2) Heₙ(√2 · x)

Applications:
  - Edgeworth / Gram-Charlier expansion of probability densities around Gaussian.
  - Polynomial chaos expansion (UQ) with standard normal random variables.
  - Hermite-Gauss quadrature with unit-variance Gaussian weight.
'''

He = HermiteE([0., 0., 0., 1.])   # He3(x) = x³ - 3x

print(He)
# 0.0 + 0.0·He₁(x) + 0.0·He₂(x) + 1.0·He₃(x)

print(He(2.).round(4))
# 2.0   (8 - 6 = 2)

# He4 in power-series form
He4 = HermiteE.basis(4)
print(He4.convert(kind=Polynomial).coef)
# [ 3.  0. -6.  0.  1.]   → 3 - 6x² + x⁴  ✓

# Orthogonality: E[He_m(X)·He_n(X)] = 0 for m≠n when X ~ N(0,1)
x_prob = np.linspace(-6, 6, 100000)
w_prob = np.exp(-x_prob**2 / 2) / np.sqrt(2 * np.pi)
He2_vals = HermiteE.basis(2)(x_prob)
He3_vals = HermiteE.basis(3)(x_prob)
print(np.trapezoid(He2_vals * He3_vals * w_prob, x_prob).round(4))
# 0.0   (orthogonal)

# E[He2(X)²] = 2! = 2 for X ~ N(0,1)
print(np.trapezoid(He2_vals**2 * w_prob, x_prob).round(4))
# 2.0   (= 2!)


# =========================================================================================
# 7. Laguerre
# =========================================================================================

##----------##
## Laguerre ##
##----------##
'''
Laguerre represents p(x) = Σ cₙ Lₙ(x) — Laguerre polynomials.

L₀=1, L₁=1-x, L₂=(x²-4x+2)/2, L₃=(-x³+9x²-18x+6)/6, ...
Orthogonal on [0, ∞) w.r.t. weight e^{-x}:
  ∫₀∞ Lₘ(x) Lₙ(x) e^{-x} dx = δₘₙ

Applications:
  - Gauss-Laguerre quadrature for ∫₀∞ f(x) e^{-x} dx.
  - Hydrogen atom radial wave functions  Rₙₗ ∝ Lₙ(x) e^{-x/2}.
  - Exponential decay integrals in spectroscopy and optics.
'''

Lag = Laguerre([1., 1., 0.5])   # L0 + L1 + 0.5·L2

print(Lag)
# 1.0 + 1.0·L₁(x) + 0.5·L₂(x)

print(Lag.coef)
# [1.  1.  0.5]

# L1(2)=1-2=-1,  L2(2)=(4-8+2)/2=-1  →  Lag(2) = 1 + (-1) + 0.5·(-1) = -0.5
print(Lag(2.))
# -0.5

# L2 in power-series form
L2_lag = Laguerre.basis(2)
print(L2_lag.convert(kind=Polynomial).coef)
# [ 1. -2.  0.5]   → 1 - 2x + 0.5x²  ✓  (= (x²-4x+2)/2)

# Gauss-Laguerre quadrature nodes = roots of L5
L5_lag = Laguerre.basis(5)
gl_lag_nodes = np.sort(L5_lag.roots().real)
print(gl_lag_nodes.round(4))
# [0.2635  1.4134  3.5964  7.0858  12.6408]  (5 nodes on [0, ∞))

# Orthogonality (numerical)
x_lag = np.linspace(0, 50, 200000)
w_lag = np.exp(-x_lag)
L1_vals = Laguerre.basis(1)(x_lag)
L3_vals = Laguerre.basis(3)(x_lag)
print(np.trapezoid(L1_vals * L3_vals * w_lag, x_lag).round(4))
# 0.0   (orthogonal)


# =========================================================================================
# 8. Legacy API (poly1d)
# =========================================================================================

'''
numpy.poly1d and the poly* functions are LEGACY — do NOT use in new code.
Kept here for understanding existing codebases and for migration.

Critical difference — coefficient ordering:
  LEGACY  np.poly1d([1, 2, 3])     → x² + 2x + 3   (highest degree first)
  MODERN  Polynomial([3, 2, 1])    → 3 + 2x + x²   (lowest degree first, index = degree)
  Same polynomial; coef arrays are exact reverses of each other.
'''

# ── np.poly1d ────────────────────────────────────────────────────────────────────────────────────
'''
np.poly1d(coef): coef stored from HIGHEST to LOWEST degree.
np.poly1d([1, 2, 3]) represents  x² + 2x + 3.
'''

p1d = np.poly1d([1., 2., 3.])   # x² + 2x + 3

print(p1d)
#    2
# 1 x + 2 x + 3

print(p1d.coeffs)
# [1. 2. 3.]   (high → low)

print(p1d.order)
# 2   (degree)

print(p1d(0.))
# 3.0

print(p1d(1.))
# 6.0   (1 + 2 + 3)

# Migrate legacy → modern: reverse coefficient array
p_modern = Polynomial(p1d.coeffs[::-1])   # [3, 2, 1] → 3 + 2x + x²
print(np.allclose(p1d(x_eval), p_modern(x_eval)))
# True

# ── np.poly() ────────────────────────────────────────────────────────────────────────────────────
'''
np.poly(roots): returns monic coefficient array (high → low) from roots.
Equivalent to Polynomial.fromroots(roots).coef[::-1].
'''

coef_from_roots = np.poly([1., 2., 3.])
print(coef_from_roots)
# [ 1. -6. 11. -6.]   → x³ - 6x² + 11x - 6

# Modern equivalent
print(Polynomial.fromroots([1., 2., 3.]).coef)
# [-6. 11. -6.  1.]   ← same polynomial, reversed storage

# ── np.polyval() ─────────────────────────────────────────────────────────────────────────────────
'''
np.polyval(coef, x): evaluate polynomial at x given high→low coefficient array.
Modern equivalent: just call the Polynomial object directly.
'''

coef = np.array([1., -6., 11., -6.])   # x³ - 6x² + 11x - 6

print(np.polyval(coef, 1.))
# 0.0

print(np.polyval(coef, np.array([1., 2., 3.])))
# [0.  0.  0.]

# ── np.polyfit() ─────────────────────────────────────────────────────────────────────────────────
'''
np.polyfit(x, y, deg): returns coefficient array (high → low) minimising least squares.
No domain/window tracking → prone to ill-conditioning for shifted or large-range x.
'''

coef_fit = np.polyfit(x_data, y_data, deg=5)
print(coef_fit.round(4))
# [cN, ..., c0]

print(np.polyval(coef_fit, 0.).round(4))
# ≈ 0.0

# Modern equivalent gives the same values
p_fit_modern = Polynomial.fit(x_data, y_data, deg=5)
print(np.allclose(np.polyval(coef_fit, x_eval),
                  p_fit_modern.convert()(x_eval), atol=1e-10))
# True

# ── np.polyder() / np.polyint() ──────────────────────────────────────────────────────────────────
'''
np.polyder(coef, m): m-th derivative; returns high→low coefficient array.
np.polyint(coef, m, k): m-th antiderivative; k = integration constant(s).
'''

coef_p = np.array([1., 0., -1., 0.])   # x³ - x  (high → low)

print(np.polyder(coef_p, 1))
# [ 3.  0. -1.]   → 3x² - 1

print(np.polyder(coef_p, 2))
# [6. 0.]   → 6x

print(np.polyint(np.array([3., 0., -1.]), 1))
# [ 1.  0. -1.  0.]   → x³ - x + 0

print(np.polyint(np.array([3., 0., -1.]), 1, k=5))
# [ 1.  0. -1.  5.]   → x³ - x + 5

# ── np.roots() ───────────────────────────────────────────────────────────────────────────────────
'''
np.roots(coef): roots of the polynomial given by high→low coefficient array.
Numerically identical to Polynomial(coef[::-1]).roots().
'''

print(np.roots([1., -6., 11., -6.]))
# [3.  2.  1.]

# ── Polynomial arithmetic (legacy) ───────────────────────────────────────────────────────────────
'''
np.polyadd / polysub / polymul / polydiv: operate on high→low coefficient arrays.
Modern equivalent: just use +, -, *, // on Polynomial objects.
'''

a = np.array([1., 2.])        # x + 2
b = np.array([1., -1., 0.])   # x² - x

print(np.polyadd(a, b))
# [ 1.  0.  2.]   → x² + 2  (zero-padded then added)

print(np.polymul(a, b))
# [ 1. -1. -2.  0.]   → x³ - 2x  (convolution)

q_d, r_d = np.polydiv(b, a)
print(q_d, '|', r_d)
# [1. -3.]  |  [6.]   → (x² - x) = (x - 3)(x + 2) + 6
