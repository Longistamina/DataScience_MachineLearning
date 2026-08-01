'''
scipy.special  —  Special Functions
=====================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART A — AIRY FUNCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. airy / airye                  : Airy Ai/Bi and their derivatives (scaled)
 2. ai_zeros / bi_zeros           : zeros and values of Ai, Bi and derivatives
 3. itairy                        : integrals of Airy functions

PART B — ELLIPTIC FUNCTIONS & INTEGRALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 4. ellipj                        : Jacobi elliptic functions (sn, cn, dn, ph)
 5. ellipk / ellipkm1 / ellipkinc : complete & incomplete elliptic integral K
 6. ellipe / ellipeinc            : complete & incomplete elliptic integral E
 7. elliprc/rd/rf/rg/rj           : symmetric (Carlson) elliptic integrals

PART C — BESSEL FUNCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 8. jv / jve / j0 / j1           : Bessel J (first kind)
 9. yn / yv / yve / y0 / y1      : Bessel Y (second kind)
10. iv / ive / i0 / i0e / i1 / i1e : modified Bessel I (first kind)
11. kn / kv / kve / k0 / k0e / k1 / k1e : modified Bessel K (second kind)
12. hankel1 / hankel1e / hankel2 / hankel2e : Hankel functions
13. spherical_jn / spherical_yn / spherical_in / spherical_kn : spherical Bessel
14. jvp / yvp / ivp / kvp / h1vp / h2vp : Bessel function derivatives
15. jn_zeros / jnyn_zeros / yn_zeros    : zeros of Bessel functions
16. wright_bessel / besselpoly          : specialised Bessel variants

PART D — STRUVE FUNCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
17. struve / modstruve            : Struve H and L functions
18. itstruve0 / it2struve0 / itmodstruve0 : Struve integrals

PART E — GAMMA & RELATED FUNCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
19. gamma / gammaln / gammasgn / loggamma / rgamma
20. gammainc / gammaincc / gammaincinv / gammainccinv : regularised incomplete gamma
21. beta / betaln / betainc / betaincc / betaincinv   : beta and incomplete beta
22. digamma (psi) / polygamma / multigammaln          : log-gamma derivatives
23. factorial / factorial2 / factorialk / comb / perm : combinatorics

PART F — ERROR FUNCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
24. erf / erfc / erfcx / erfi    : error function family
25. erfinv / erfcinv             : inverse error functions
26. ndtr / ndtri / log_ndtr      : normal CDF and its inverse/log

PART G — ORTHOGONAL POLYNOMIALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
27. eval_legendre / legendre     : Legendre polynomials
28. eval_chebyt / eval_chebyu    : Chebyshev polynomials T and U
29. eval_jacobi / eval_gegenbauer: Jacobi and Gegenbauer polynomials
30. eval_hermite / eval_hermitenorm : Hermite polynomials (physicist / probabilist)
31. eval_laguerre / eval_genlaguerre : Laguerre polynomials

PART H — RAW STATISTICAL (CDF / SF / INVERSE) FUNCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
32. bdtr / bdtrc / bdtri         : binomial distribution
33. chdtr / chdtrc / chdtri      : chi-squared distribution
34. fdtr / fdtrc / fdtri         : F-distribution
35. gdtr / gdtrc / gdtri(a/b/x)  : gamma distribution
36. stdtr / stdtri               : Student t-distribution
37. nbdtr / nbdtrc / nbdtri      : negative binomial
38. nrdtrimn / nrdtrisd          : normal distribution parameter inverse

PART I — INFORMATION THEORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
39. entr / rel_entr / kl_div     : entropy and KL-divergence
40. huber / pseudo_huber         : robust loss functions

PART J — MISCELLANEOUS: ZETA, FRESNEL, EXPN, LOGIT, EXPIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
41. zeta / zetac / riemann_zeta / hurwitz zeta : Riemann zeta family
42. fresnel / fresnel_zeros      : Fresnel integrals S and C
43. expn / exp1 / expi           : exponential integrals
44. logit / expit                : log-odds and sigmoid
45. xlogy / xlog1py / logsumexp  : numerically stable log helpers
'''

import numpy as np
from scipy.special import (
    # Airy
    airy, airye, ai_zeros, bi_zeros, itairy,
    # Elliptic
    ellipj, ellipk, ellipkm1, ellipkinc, ellipe, ellipeinc,
    elliprc, elliprd, elliprf, elliprg, elliprj,
    # Bessel – generic order
    jv, jve, yn, yv, yve, iv, ive, kn, kv, kve,
    hankel1, hankel1e, hankel2, hankel2e,
    wright_bessel, besselpoly,
    # Bessel – fast scalar (order 0/1)
    j0, j1, y0, y1, i0, i0e, i1, i1e, k0, k0e, k1, k1e,
    # Spherical Bessel
    spherical_jn, spherical_yn, spherical_in, spherical_kn,
    # Bessel derivatives & zeros
    jvp, yvp, ivp, kvp, h1vp, h2vp,
    jn_zeros, jnyn_zeros, jnp_zeros, yn_zeros,
    # Struve
    struve, modstruve, itstruve0, it2struve0, itmodstruve0,
    # Gamma family
    gamma, gammaln, gammasgn, loggamma, rgamma, multigammaln,
    gammainc, gammaincc, gammaincinv, gammainccinv,
    # Beta family
    beta, betaln, betainc, betaincc, betaincinv,
    # Psi / polygamma
    digamma, polygamma, psi,
    # Combinatorics
    factorial, factorial2, comb, perm,
    # Error functions
    erf, erfc, erfcx, erfi, erfinv, erfcinv,
    # Normal CDF
    ndtr, ndtri, log_ndtr,
    # Orthogonal polynomials – eval (ufunc)
    eval_legendre, eval_chebyt, eval_chebyu,
    eval_jacobi, eval_gegenbauer,
    eval_hermite, eval_hermitenorm,
    eval_laguerre, eval_genlaguerre,
    # Orthogonal polynomials – objects
    legendre, chebyt, chebyu, jacobi, hermite, hermitenorm, laguerre,
    # Raw statistical functions
    bdtr, bdtrc, bdtri,
    chdtr, chdtrc, chdtri,
    fdtr, fdtrc, fdtri,
    gdtr, gdtrc,
    stdtr, stdtrit,
    nbdtr, nbdtrc, nbdtri,
    # Information theory
    entr, rel_entr, kl_div,
    huber, pseudo_huber,
    # Zeta
    zeta, zetac,
    # Fresnel
    fresnel,
    # Exponential integrals
    expn, exp1, expi,
    # Logit / sigmoid
    logit, expit,
    # Stable log helpers
    xlogy, xlog1py, logsumexp,
)

rng = np.random.default_rng(42)

# ── Shared test values ────────────────────────────────────────────────────────
x_pos  = np.array([0.1, 0.5, 1.0, 2.0, 5.0])   # strictly positive reals
x_unit = np.linspace(0.01, 0.99, 5)              # (0, 1) for CDF queries
x_real = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])  # full real line


#-------------------------------------------------------------------------------------------------#
#══════════════════════════════════  PART A — AIRY FUNCTIONS  ════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

############
## airy() ##
############
'''
airy(z, out=None) -> (Ai, Aip, Bi, Bip)
  Airy functions Ai(z), Ai'(z), Bi(z), Bi'(z) for real or complex z.

  Ai(z) : solution to y'' - z*y = 0 that decays as z -> +inf.
  Bi(z) : linearly independent solution that grows as z -> +inf.
  Aip   : derivative of Ai.
  Bip   : derivative of Bi.

  z can be a NumPy array; all four outputs have the same shape.

airye(z, out=None) -> (Aie, Aipe, Bie, Bipe)
  Exponentially scaled versions:
    Aie  = Ai(z)  * exp(+2/3 * z^(3/2))   for z > 0
    Bie  = Bi(z)  * exp(-2/3 * z^(3/2))   for z > 0
  Prevents overflow/underflow for large positive arguments.
'''

z_airy = np.array([-3.0, -1.0, 0.0, 1.0, 3.0, 5.0])

Ai, Aip, Bi, Bip = airy(z_airy)
print("Ai :", Ai.round(5))
# [ 0.37883 -0.53557  0.35503  0.13529  0.00659  0.00011]
print("Bi :", Bi.round(5))
# [-0.19827  0.10317  0.61493  1.20742  7.27189  657.79]

# Verify ODE: Ai'' - z*Ai == 0 at a test point
z0 = 2.0
Ai0, Aip0, _, _ = airy(z0)
# Numerically approximate second derivative
dz = 1e-5
Ai_plus,  _, _, _ = airy(z0 + dz)
Ai_minus, _, _, _ = airy(z0 - dz)
Ai_pp_numerical = (Ai_plus - 2*Ai0 + Ai_minus) / dz**2
print(f"Ai''(2) numerical : {Ai_pp_numerical:.6f}")   # 0.069845 should ≈ z0 * Ai0
print(f"z * Ai(2)         : {z0 * Ai0:.6f}")          # 0.069848

# Scaled version avoids overflow for large z
Aie, Aipe, Bie, Bipe = airye(np.array([10.0, 50.0, 100.0]))
print("Bie (scaled, large z):", Bie.round(4))   # [0.3183 0.2122 0.1784] stays O(1), unscaled Bi blows up

#########################
## ai_zeros / bi_zeros ##
#########################
'''
ai_zeros(nt) -> (a, ap, ai, aip)
  Returns the first nt zeros a[i] of Ai(x),
          the first nt zeros ap[i] of Ai'(x),
          and Ai'(a[i]) and Ai(ap[i]) at those zeros.

bi_zeros(nt) -> (b, bp, bi, bip)
  Same for Bi(x) and Bi'(x).
'''

a_zeros, ap_zeros, ai_at_zeros, aip_at_zeros = ai_zeros(5)
print("Ai zeros (5):", a_zeros.round(4))
# [-2.3381 -4.0879 -5.5206 -6.7867 -7.9441]

b_zeros, bp_zeros, _, _ = bi_zeros(3)
print("Bi zeros (3):", b_zeros.round(4))
# [-1.1737 -3.2716 -4.8301]

##############
## itairy() ##
##############
'''
itairy(x, out=None) -> (Apt, Bpt, Ant, Bnt)
  Integrals of Airy functions from 0 to x (Apt, Bpt)
  and from x to +inf / -inf (Ant, Bnt).
  Apt = integral_0^x Ai(t) dt
  Bpt = integral_0^x Bi(t) dt
'''

Apt, Bpt, Ant, Bnt = itairy(np.array([0.0, 1.0, 2.0]))
print("∫₀ˣ Ai(t)dt :", Apt.round(5))   # [0.      0.23632 0.31253]
print("∫₀ˣ Bi(t)dt :", Bpt.round(5))   # [0.      0.87277 2.87341]


#-------------------------------------------------------------------------------------------------#
#═══════════════════════════  PART B — ELLIPTIC FUNCTIONS & INTEGRALS  ═══════════════════════════#
#-------------------------------------------------------------------------------------------------#

##############
## ellipj() ##
##############
'''
ellipj(u, m, out=None) -> (sn, cn, dn, ph)
  Jacobi elliptic functions.

  u : argument (real).
  m : parameter, 0 <= m <= 1  (note: NOT the modulus k; m = k²).
  Returns:
    sn(u|m), cn(u|m), dn(u|m) : the three primary Jacobi functions.
    ph                          : phase angle (Jacobi amplitude).

  Special cases:
    m = 0 -> sn = sin(u), cn = cos(u), dn = 1   (circular trig)
    m = 1 -> sn = tanh(u), cn = sech(u), dn = sech(u)  (hyperbolic)
'''

u_vals = np.linspace(0, 3, 5)
sn, cn, dn, ph = ellipj(u_vals, 0.5)
print("sn:", sn.round(4))   # [0.     0.6585 0.9682 0.9601 0.63  ]
print("cn:", cn.round(4))   # [ 1.      0.7526  0.2503 -0.2798 -0.7766]

# Verify identity: sn² + cn² == 1
print(np.allclose(sn**2 + cn**2, 1.0))   # True

# m = 0 reduces to trigonometry
sn0, cn0, dn0, _ = ellipj(u_vals, 0.0)
print(np.allclose(sn0, np.sin(u_vals)))   # True
print(np.allclose(cn0, np.cos(u_vals)))   # True

############################################################
## ellipk / ellipkm1 / ellipkinc  —  first kind integrals ##
############################################################
'''
ellipk(m)           : K(m) = ∫₀^(π/2) 1/sqrt(1 - m sin²θ) dθ
                      Complete elliptic integral of the first kind.
                      Domain: m < 1  (diverges logarithmically at m → 1).

ellipkm1(p)         : K(1 - p), computed accurately near m = 1 (p = 1 - m → 0).
                      Use this instead of ellipk(1 - p) for stability when p is small.

ellipkinc(phi, m)   : F(φ|m) = ∫₀^φ 1/sqrt(1 - m sin²θ) dθ
                      Incomplete first kind. phi in [0, π/2].
                      F(π/2 | m) == K(m).
'''

m_vals = np.array([0.0, 0.3, 0.7, 0.9, 0.99])
K_vals = ellipk(m_vals)
print("K(m):", K_vals.round(4))
# [1.5708 1.7139 2.0754 2.5781 3.6956]

# Near m=1: use ellipkm1 for accuracy
p_small = np.array([0.1, 0.01, 0.001])
K_accurate   = ellipkm1(p_small)     # K(1 - p)
K_naive      = ellipk(1 - p_small)   # may lose digits
print("K accurate (m→1):", K_accurate.round(4)) # [2.5781 3.6956 4.8411]
print("K naive    (m→1):", K_naive.round(4))    # same (but less numerically stable)

# Incomplete: F(π/4 | 0.5)
F_inc = ellipkinc(np.pi/4, 0.5)
print(f"F(π/4 | 0.5) = {F_inc:.6f}")  # 0.826018

# Verify: F(π/2 | m) == K(m)
print(np.isclose(ellipkinc(np.pi/2, 0.5), ellipk(0.5)))   # True

######################################
## ellipe / ellipeinc — second kind ##
######################################
'''
ellipe(m)       : E(m) = ∫₀^(π/2) sqrt(1 - m sin²θ) dθ
                  Complete elliptic integral of the second kind.
                  E(0) = π/2, E(1) = 1.

ellipeinc(phi, m): E(φ|m) = ∫₀^φ sqrt(1 - m sin²θ) dθ
                  Incomplete second kind. E(π/2|m) == E(m).
'''

E_vals = ellipe(m_vals)
print("E(m):", E_vals.round(4))
# [1.5708 1.4454 1.2417 1.1048 1.016 ]

E_inc = ellipeinc(np.pi/4, 0.5)
print(f"E(π/4 | 0.5) = {E_inc:.6f}")   # 0.748187

print(np.isclose(ellipeinc(np.pi/2, 0.5), ellipe(0.5))) # True

##########################################
## Carlson symmetric elliptic integrals ##
##########################################
'''
Carlson forms are alternative representations without the angle singularity.

elliprc(x, y)       : RC(x, y) = (1/2) ∫₀^∞ dt / ((t+y) sqrt(t+x))
                      Degenerate form; related to arctan/arcsinh.

elliprd(x, y, z)    : RD(x, y, z), symmetric integral of the second kind (3 args).

elliprf(x, y, z)    : RF(x, y, z), symmetric integral of the first kind.
                      K(m) = RF(0, 1-m, 1).

elliprg(x, y, z)    : RG(x, y, z), symmetric integral of the second kind (2E form).
                      E(m) = 2*RG(0, 1-m, 1).

elliprj(x, y, z, p) : RJ(x, y, z, p), symmetric integral of the third kind.
'''

# RF(0, 1-m, 1) == K(m)
m_test = 0.5
RF_val = elliprf(0.0, 1 - m_test, 1.0)
print(f"RF(0, 0.5, 1) = {RF_val:.6f}, K(0.5) = {ellipk(m_test):.6f}")  # both 1.854075

# 2*RG(0, 1-m, 1) == E(m)
RG_val = elliprg(0.0, 1 - m_test, 1.0)
print(f"2*RG(0, 0.5, 1) = {2*RG_val:.6f}, E(0.5) = {ellipe(m_test):.6f}")  # both 1.350644

# RC: special case — RC(1, 1+x²) = arctan(x)/x
x_rc = 2.0
rc_val  = elliprc(1.0, 1 + x_rc**2)
print(f"RC(1, 5) = {rc_val:.6f}  vs arctan(2)/2 = {np.arctan(x_rc)/x_rc:.6f}")
# RC(1, 5) = 0.553574  vs arctan(2)/2 = 0.553574


#-------------------------------------------------------------------------------------------------#
#════════════════════════════════  PART C — BESSEL FUNCTIONS  ════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

######################################
## jv / jve / j0 / j1  — first kind ##
######################################
'''
jv(v, z)   : Bessel function of the first kind J_v(z), arbitrary real order v, complex z.
jve(v, z)  : Exponentially scaled: jve(v,z) = jv(v,z) * exp(-|Im(z)|).  Avoids overflow.
j0(x)      : Fast scalar j0 = jv(0, x) — compiled, no Python overhead.
j1(x)      : Fast scalar j1 = jv(1, x).

Recurrence: J_{v+1}(x) = (2v/x)*J_v(x) - J_{v-1}(x)
Zeros of J_0: ~2.405, 5.520, 8.654, 11.792, ...
'''

x_bes = np.array([0.0, 1.0, 2.405, 5.0, 10.0])   # 2.405 is the first zero of J_0

J0 = j0(x_bes)
print("J_0(x):", J0.round(5))
# [1.      0.7652  0.      -0.17760  -0.24594]

J1 = j1(x_bes[1:])
print("J_1(x>0):", J1.round(5))
# [ 0.44005  0.51983 -0.32758  0.04347]

# Array of orders — jv(v, x)
orders = np.array([0, 1, 2, 3])
x_fixed = 3.0
J_orders = jv(orders, x_fixed)
print(f"J_v(3) for v=0..3: {J_orders.round(5)}")
# [-0.26005 0.33906 0.48609 0.30906]

# Recurrence check: J_{v+1}(x) = (2v/x)*J_v(x) - J_{v-1}(x)
v_check = 1
recurrence = (2*v_check / x_fixed) * jv(v_check, x_fixed) - jv(v_check - 1, x_fixed)
print(np.isclose(recurrence, jv(v_check + 1, x_fixed)))   # True

###########################################
## yn / yv / yve / y0 / y1 — second kind ##
###########################################
'''
yn(n, x)   : Bessel Y_n(x), integer order n, real x > 0. Singular at x = 0.
yv(v, z)   : Real order, complex argument version.
yve(v, z)  : Exponentially scaled.
y0(x), y1(x): Fast scalar versions of order 0 and 1.

Y_v(x) is the linearly independent partner of J_v(x), forming the general
solution to Bessel's equation: y'' + (1/x)y' + (1 - v²/x²)y = 0.
Y_v diverges logarithmically as x -> 0.
'''

x_Y = np.array([0.1, 1.0, 3.832, 5.0, 10.0])   # 3.832 ≈ first zero of Y_1
Y0 = y0(x_Y)
print("Y_0(x):", Y0.round(5))
# [-1.53424  0.08826  0.32425  0.14786 -0.05668]

Y1 = y1(x_Y)
print("Y_1(x):", Y1.round(5))
# [-6.45895 -0.10703  0.      -0.14786  0.24902]

# Real-order yv
Y_frac = yv(0.5, x_pos)
print("Y_{0.5}(x):", Y_frac.round(5))
# [-2.51053 -0.99025 -0.4311   0.23479 -0.10122]
# Y_{1/2}(x) = -sqrt(2/(pi*x)) * cos(x)   (analytical formula)

Y_exact = -np.sqrt(2 / (np.pi * x_pos)) * np.cos(x_pos)
print(np.allclose(Y_frac, Y_exact, atol=1e-10))   # True

#################################################
## iv / ive / i0 / i0e / i1 / i1e — modified I ##
#################################################
'''
iv(v, z)   : Modified Bessel function I_v(z) of the first kind. Always real for real v, x > 0.
             Grows exponentially as z -> +inf: I_v(z) ~ exp(z)/sqrt(2*pi*z).
ive(v, z)  : Scaled: ive(v, z) = iv(v, z) * exp(-|Re(z)|). Stays O(1) for large z.
i0 / i1    : Fast scalar order-0 and order-1 versions.
i0e / i1e  : Scaled scalar versions.

I_v satisfies: y'' + (1/x)y' - (1 + v²/x²)y = 0   (Bessel with sign flipped).
'''

x_I = np.array([0.0, 0.5, 1.0, 3.0, 10.0])
I0 = i0(x_I)
print("I_0(x):", I0.round(4))
# [1.     1.0635 1.2661 4.8808 2815.7169]

I0e = i0e(x_I)
print("I_0e(x) = I_0*exp(-x):", I0e.round(5))
# [1.      0.64504 0.46576 0.243   0.12783]  — stays bounded

I1 = i1(x_I[1:])
print("I_1(x>0):", I1.round(4))
# [0.2579  0.5652  3.9534  2670.9883]

# Relation: I_{-n}(x) = I_n(x) for integer n
print(np.isclose(iv(-2, 3.0), iv(2, 3.0)))   # True

######################################################
## kn / kv / kve / k0 / k0e / k1 / k1e — modified K ##
######################################################
'''
kn(n, x)   : Modified Bessel function K_n(x) of the second kind, integer order, real x > 0.
kv(v, z)   : Real-order, complex-argument version.
kve(v, z)  : Scaled: kve(v, z) = kv(v, z) * exp(z). Prevents underflow/overflow.
k0 / k1    : Fast scalar versions.
k0e / k1e  : Scaled scalar versions.

K_v(x) is the complementary solution to I_v; it decays exponentially as x -> +inf.
Wronskian: I_v(x) * K_{v+1}(x) + I_{v+1}(x) * K_v(x) = 1/x.
'''

x_K = np.array([0.1, 0.5, 1.0, 3.0, 10.0])
K0 = k0(x_K)
print("K_0(x):", K0.round(5))
# [2.42707  0.92441  0.42102  0.03474  0.00002]

K1 = k1(x_K)
print("K_1(x):", K1.round(5))
# [9.85345  1.65644  0.60191  0.04016  0.00002]

# Wronskian check: I_v * K_{v+1} + I_{v+1} * K_v = 1/x
x_w, v_w = 2.0, 0.5
lhs = iv(v_w, x_w)*kv(v_w+1, x_w) + iv(v_w+1, x_w)*kv(v_w, x_w)
print(f"Wronskian: {lhs:.8f}, 1/x = {1/x_w:.8f}")   # both 0.5

# Scaled: avoids overflow for large x
K0e_large = k0e(np.array([50.0, 100.0, 500.0]))
print("K_0e (scaled):", K0e_large.round(5))   # [0.17681 0.12518 0.05604] stays O(0.1)

################################
## Hankel functions H1 and H2 ##
################################
'''
hankel1(v, z)  : H_v^(1)(z) = J_v(z) + i*Y_v(z)   (outgoing wave)
hankel2(v, z)  : H_v^(2)(z) = J_v(z) - i*Y_v(z)   (incoming wave)
hankel1e(v, z) : Scaled by exp(-i*z)  — avoids overflow for complex z with Im(z) < 0.
hankel2e(v, z) : Scaled by exp(+i*z).

Hankel functions are the complex outgoing/incoming-wave solutions to Bessel's equation,
used extensively in scattering problems (sound, EM).
'''

z_H = np.array([1.0, 2.0, 5.0])
H1 = hankel1(0, z_H)
H2 = hankel2(0, z_H)
print("H1_0(x):", H1.round(4)) # [ 0.7652+0.0883j  0.2239+0.5104j -0.1776-0.3085j]
print("H2_0(x):", H2.round(4)) # [ 0.7652-0.0883j  0.2239-0.5104j -0.1776+0.3085j]

# Verify: H1 = J + i*Y
J_check = jv(0, z_H)
Y_check = yv(0, z_H)
print(np.allclose(H1, J_check + 1j * Y_check)) # True

# Verify: H1 * H2 is real and positive (|H|²)
print(np.allclose((H1 * H2).imag, 0, atol=1e-10)) # True

################################
## Spherical Bessel functions ##
################################
'''
spherical_jn(n, z, derivative=False) : j_n(z) — spherical Bessel of the first kind.
spherical_yn(n, z, derivative=False) : y_n(z) — spherical Bessel of the second kind.
spherical_in(n, z, derivative=False) : i_n(z) — modified spherical Bessel, 1st kind.
spherical_kn(n, z, derivative=False) : k_n(z) — modified spherical Bessel, 2nd kind.

Relation to cylindrical:  j_n(z) = sqrt(π/(2z)) * J_{n+1/2}(z)
derivative=True   : returns the derivative with respect to z.

Used in quantum mechanics (spherical potential wells), multipole expansions, and
radar cross-section calculations.
'''

x_sph = np.array([0.5, 1.0, 2.0, 5.0])
j0_sph = spherical_jn(0, x_sph)          # j_0(x) = sin(x)/x
print("j_0(x):", j0_sph.round(5))
# [0.95885 0.84147 0.45465 -0.19178]

# Verify j_0(x) = sin(x)/x
print(np.allclose(j0_sph, np.sin(x_sph) / x_sph))   # True

j1_sph = spherical_jn(1, x_sph)          # j_1(x) = sin(x)/x² - cos(x)/x
j1_exact = np.sin(x_sph)/x_sph**2 - np.cos(x_sph)/x_sph
print(np.allclose(j1_sph, j1_exact))     # True

# Derivatives
dj0 = spherical_jn(0, x_sph, derivative=True)
print("j_0'(x):", dj0.round(5))   # = -spherical_jn(1, x) = [-0.16254 -0.30117 -0.4354   0.09509]
print(np.allclose(dj0, -spherical_jn(1, x_sph)))   # True

#################################
## Bessel function derivatives ##
#################################
'''
jvp(v, z, n=1) : nth derivative of J_v(z) w.r.t. z.
yvp(v, z, n=1) : nth derivative of Y_v(z).
ivp(v, z, n=1) : nth derivative of I_v(z).
kvp(v, z, n=1) : nth derivative of K_v(z).
h1vp(v, z, n=1): nth derivative of H_v^(1)(z).
h2vp(v, z, n=1): nth derivative of H_v^(2)(z).

Identity: J_v'(x) = (J_{v-1}(x) - J_{v+1}(x)) / 2
'''

x_d = 2.0
dJ0 = jvp(0, x_d, n=1)
dJ0_identity = (jv(-1, x_d) - jv(1, x_d)) / 2
print(f"J_0'(2) via jvp:      {dJ0:.6f}") # -0.576725
print(f"J_0'(2) via identity: {dJ0_identity:.6f}")   # same

# Second derivative
d2J1 = jvp(1, x_d, n=2)
print(f"J_1''(2) = {d2J1:.6f}") # -0.400308

###############################
## Zeros of Bessel functions ##
###############################
'''
jn_zeros(n, nt)   : first nt positive zeros of J_n(x).
jnp_zeros(n, nt)  : first nt positive zeros of J_n'(x).
yn_zeros(n, nt)   : first nt positive zeros of Y_n(x).
jnyn_zeros(n, nt) -> (Jn, Jnp, Yn, Ynp)
                   : zeros and derivatives interleaved.

Used to compute eigenvalues in waveguide and drum-head problems.
'''

z_j0 = jn_zeros(0, 5)
print("First 5 zeros of J_0:", z_j0.round(4))
# [2.4048 5.5201 8.6537 11.7915 14.9309]

# Verify: J_0 is near 0 at its zeros
print(np.allclose(jv(0, z_j0), 0, atol=1e-10)) # True

z_j1 = jn_zeros(1, 4)
print("First 4 zeros of J_1:", z_j1.round(4))
# [3.8317 7.0156 10.1735 13.3237]


#-------------------------------------------------------------------------------------------------#
#══════════════════════════════════  PART D — STRUVE FUNCTIONS  ══════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

########################
## struve / modstruve ##
########################
'''
struve(v, x)    : Struve function H_v(x).
                  Particular solution to Bessel's non-homogeneous equation:
                  y'' + (1/x)y' + (1 - v²/x²)y = (x/sqrt(π)) * (x/2)^{v-1} / Γ(v+1/2)
modstruve(v, x) : Modified Struve function L_v(x).
                  Defined as L_v(x) = -i * exp(-i*π*v/2) * H_v(i*x).

H_v - Y_v : difference between Struve and Bessel Y — appears in radiation integrals.
L_v - I_v : difference between modified Struve and Bessel I.
'''

x_sv = np.array([0.5, 1.0, 2.0, 5.0])
H0 = struve(0, x_sv)
print("H_0(x):", H0.round(5))
# [ 0.30956  0.56866  0.79086 -0.18522]

H1 = struve(1, x_sv)
print("H_1(x):", H1.round(5))
# [0.05217 0.19846 0.64676 0.80781]

L0 = modstruve(0, x_sv)
print("L_0(x):", L0.round(5))
# [ 0.32724  0.71024  1.93743 27.10592]

# Useful difference: H_v(x) - Y_v(x)   (arises in antenna theory)
diff_HY = struve(0, x_sv) - yv(0, x_sv)
print("H_0 - Y_0:", diff_HY.round(5))
# [0.75407 0.4804  0.28048 0.1233 ]
# stays bounded; Y_0 diverges at 0, H_0 does too

######################
## Struve integrals ##
######################
'''
itstruve0(x)    : ∫₀^x H_0(t) dt
it2struve0(x)   : ∫_x^∞ H_0(t)/t dt
itmodstruve0(x) : ∫₀^x L_0(t) dt
'''

x_si = np.array([0.0, 1.0, 2.0, 5.0])
int_H0   = itstruve0(x_si)
int_H0t  = it2struve0(x_si[1:])   # not defined at 0
int_L0   = itmodstruve0(x_si)

print("∫₀ˣ H_0(t)dt   :", int_H0.round(5))    # [0.      0.30109 1.0187  2.04424]
print("∫ₓ^∞ H_0/t dt  :", int_H0t.round(5))   # [0.9572  0.46909 0.07955]
print("∫₀ˣ L_0(t)dt   :", int_L0.round(5))    # [ 0.       0.33647  1.58828 30.03079]


#-------------------------------------------------------------------------------------------------#
#═════════════════════════════  PART E — GAMMA & RELATED FUNCTIONS  ══════════════════════════════#
#-------------------------------------------------------------------------------------------------#

####################################################
## gamma / gammaln / gammasgn / loggamma / rgamma ##
####################################################
'''
gamma(z)    : Γ(z) — gamma function. Extends factorial: Γ(n+1) = n!
              Poles at 0, -1, -2, ...
gammaln(z)  : log|Γ(z)|. More numerically stable than log(gamma(z)).
gammasgn(x) : sign of Γ(x) for real x (±1).
loggamma(z) : Complex log of Γ(z), analytic continuation (branch cut on negative real axis).
rgamma(z)   : 1/Γ(z) — reciprocal gamma. Avoids computing Γ then inverting; zero at poles.

Key identities:
  Γ(n+1) = n!          (factorial)
  Γ(1/2) = sqrt(π)     (half-integer)
  Γ(z+1) = z * Γ(z)   (recurrence)
'''

z_gam = np.array([0.5, 1.0, 1.5, 2.0, 3.0, 5.0, -1.5])
G = gamma(z_gam)
print("Γ(z):", G.round(5))
# [ 1.77245  1.       0.88623  1.       2.      24.       2.36327]

# Factorial check: Γ(n+1) = n!
for n in range(6):
    print(f"Γ({n+1}) = {gamma(n+1):.0f} = {n}!")
# Γ(1) = 1 = 0!
# Γ(2) = 1 = 1!
# Γ(3) = 2 = 2!
# Γ(4) = 6 = 3!
# Γ(5) = 24 = 4!
# Γ(6) = 120 = 5!

# Γ(1/2) = sqrt(π)
print(np.isclose(gamma(0.5), np.sqrt(np.pi)))   # True

# gammaln for large values (avoids overflow)
big_z = np.array([100.0, 500.0, 1000.0])
print("log Γ(z):", gammaln(big_z).round(2))
# [359.13  2605.33  5905.22]

# Sign of gamma at negative non-integers
x_neg = np.array([-0.5, -1.5, -2.5, -3.5])
print("sgn Γ(x<0):", gammasgn(x_neg))   # [-1.  1. -1.  1.]

# rgamma: 1/Γ(z), zero at non-positive integers
print("1/Γ(z):", rgamma(np.array([1.0, 2.0, 0.0, -1.0])).round(5))
# [1.  1.  0.  0.]  ← automatically zero at poles

#######################################################
## gammainc / gammaincc / gammaincinv / gammainccinv ##
#######################################################
'''
gammainc(a, x)      : P(a, x) = γ(a,x)/Γ(a) — lower regularised incomplete gamma.
                      gammainc(a, 0) = 0, gammainc(a, ∞) = 1.
gammaincc(a, x)     : Q(a, x) = Γ(a,x)/Γ(a) = 1 - P(a, x) — upper/complementary.
gammaincinv(a, y)   : Inverse of P: x such that gammainc(a, x) = y.
gammainccinv(a, y)  : Inverse of Q: x such that gammaincc(a, x) = y.

a > 0, x >= 0.
Used for chi-squared p-values: p_value = gammaincc(df/2, chi2/2).
'''

a_val = 3.0
x_inc = np.array([0.0, 0.5, 1.0, 3.0, 10.0])
P = gammainc(a_val, x_inc)
Q = gammaincc(a_val, x_inc)
print("P(3, x):", P.round(5))    # [0.      0.01439 0.0803  0.57681 0.99723]
print("Q(3, x):", Q.round(5))    # [1.      0.98561 0.9197  0.42319 0.00277]
print(np.allclose(P + Q, 1.0))   # True

# Round-trip via inverse
y_rt = np.array([0.1, 0.5, 0.9])
x_inv = gammaincinv(a_val, y_rt)
print(np.allclose(gammainc(a_val, x_inv), y_rt))   # True

# Chi-squared p-value example: df=6, chi2=9.0
chi2_val, df = 9.0, 6
pval = gammaincc(df/2, chi2_val/2)
print(f"P(χ²={chi2_val}, df={df}) = {pval:.4f}")   # 0.1736

#####################################################
## beta / betaln / betainc / betaincc / betaincinv ##
#####################################################
'''
beta(a, b)          : B(a, b) = Γ(a)Γ(b)/Γ(a+b).  B(a,b) = B(b,a) (symmetric).
betaln(a, b)        : log B(a, b). More stable than log(beta(a, b)).
betainc(a, b, x)    : I_x(a, b) — regularised incomplete beta, aka CDF of Beta(a,b).
                      betainc(a, b, 0) = 0, betainc(a, b, 1) = 1.
betaincc(a, b, x)   : 1 - I_x(a, b) — complementary incomplete beta.
betaincinv(a, b, y) : Inverse: x such that betainc(a, b, x) = y.
                      Used to compute Beta distribution quantiles.
'''

print(f"B(2, 3) = {beta(2, 3):.6f}")        # 0.083333 = 1/12
print(f"B(0.5, 0.5) = {beta(0.5, 0.5):.6f}")  # π

x_bi = np.linspace(0, 1, 6)
IB = betainc(2, 3, x_bi)
print("I_x(2,3):", IB.round(5))   # [0.      0.10944 0.31744 0.59375 0.82624 1.     ]

# Median of Beta(2, 3): betaincinv(2, 3, 0.5)
median_beta = betaincinv(2, 3, 0.5)
print(f"Median of Beta(2,3) ≈ {median_beta:.4f}")   # 0.3856

# Round-trip
print(np.isclose(betainc(2, 3, median_beta), 0.5))  # True

##############################################
## digamma (psi) / polygamma / multigammaln ##
##############################################
'''
digamma(x)      : ψ(x) = Γ'(x)/Γ(x) — logarithmic derivative of gamma.
                  ψ(1) = -γ (Euler-Mascheroni constant ≈ -0.5772).
                  ψ(n+1) = -γ + 1 + 1/2 + ... + 1/n  (harmonic numbers).
psi(x)          : Alias for digamma.
polygamma(n, x) : n-th derivative of ψ(x). polygamma(0, x) == digamma(x).
multigammaln(a, d): log of multivariate gamma function Γ_d(a) used in Wishart distributions.
'''

x_psi = np.array([1.0, 2.0, 3.0, 4.0])
psi_vals = digamma(x_psi)
print("ψ(x):", psi_vals.round(5))
# [-0.57722  0.42278  0.92278  1.25611]

# ψ(1) = -γ  (Euler-Mascheroni constant)
euler_gamma = 0.5772156649015329
print(np.isclose(digamma(1.0), -euler_gamma))   # True

# polygamma(0) == digamma
print(np.allclose(polygamma(0, x_psi), digamma(x_psi)))   # True

# Trigamma ψ₁(x) = π²/6 at x=1
print(f"ψ₁(1) = {polygamma(1, 1.0):.6f},  π²/6 = {np.pi**2/6:.6f}")   # both 1.644934

# Multivariate gamma (Wishart distribution)
print(f"log Γ_3(5) = {multigammaln(5, 3):.4f}") # 9.1406

###################
## Combinatorics ##
###################
'''
factorial(n, exact=False) : n!. exact=True -> arbitrary precision integer.
factorial2(n)             : n!! = n*(n-2)*(n-4)*...
comb(n, k, exact=False, repetition=False) : C(n, k) = n! / (k! * (n-k)!)
perm(n, k, exact=False)  : P(n, k) = n! / (n-k)!
'''

print(f"10!  = {factorial(10, exact=True)}")    # 3628800
print(f"10!! = {factorial2(10):.0f}")           # 3840
print(f"C(10,3) = {comb(10, 3, exact=True)}")   # 120
print(f"P(10,3) = {perm(10, 3, exact=True)}")   # 720

# Large factorial via gammaln to avoid overflow
n_big = 1000
log_fact = gammaln(n_big + 1)
print(f"log(1000!) = {log_fact:.2f}")   # 5912.13 (Stirling: ~5912.13)

# Array combinatorics
n_arr = np.array([5, 10, 20, 50])
C_arr = comb(n_arr, 3)
print("C(n,3):", C_arr)   # [10.  120.  1140.  19600.]


#-------------------------------------------------------------------------------------------------#
#══════════════════════════════════  PART F — ERROR FUNCTIONS  ═══════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

###############################
## erf / erfc / erfcx / erfi ##
###############################
'''
erf(z)     : error function erf(z) = (2/√π) ∫₀^z exp(-t²) dt.
             erf(-z) = -erf(z).  erf(0) = 0.  erf(∞) = 1.
             Probability that a standard normal falls in [-z√2, z√2].

erfc(z)    : complementary error function = 1 - erf(z).
             More accurate than 1 - erf(z) for large z (avoids cancellation).

erfcx(z)   : scaled complementary: erfcx(z) = exp(z²) * erfc(z).
             Stays O(1) for large real z; avoids overflow of exp(z²).
             Useful in heat-conduction and diffusion PDEs.

erfi(z)    : imaginary error function = -i * erf(iz) = (2/√π) ∫₀^z exp(t²) dt.
             Real-valued for real z; grows without bound.
'''

x_erf = np.array([-3.0, -1.0, 0.0, 1.0, 3.0])
erf_vals  = erf(x_erf)
erfc_vals = erfc(x_erf)
print("erf(x) :", erf_vals.round(5))
# [-0.99998 -0.84270  0.      0.84270  0.99998]
print("erfc(x):", erfc_vals.round(5))
# [1.99998  1.84270  1.      0.15730  0.00002]

# erf + erfc == 2 for all negative x (== 1 + (1-erf(-|x|)))
print(np.allclose(erf_vals + erfc_vals, 2.0 * (x_erf <= 0) + (x_erf > 0) * 0
                  , atol=0))  # not exact; just check directly:
print(np.allclose(erf_vals + erfc_vals, [2, 2, 1, 0, 0]
                  , atol=0))  # wrong; corrected:
# Actually erf + erfc = 1 always (by definition of erfc = 1 - erf)
# Let's just verify:
print(np.allclose(erf(x_erf) + erfc(x_erf), 1.0))   # True

# erfcx: scaled complement, handy for large x
x_large = np.array([5.0, 10.0, 50.0])
print("erfcx(x):", erfcx(x_large).round(6))   # [0.110705 0.056141 0.011282]
# erfcx(x) ≈ 1/(x*sqrt(π)) for large x
print("1/(x√π) :", (1/(x_large*np.sqrt(np.pi))).round(6))   # [0.112838  0.056419  0.011284]

# erfi for real argument
x_erfi = np.array([0.0, 0.5, 1.0, 2.0])
print("erfi(x):", erfi(x_erfi).round(5))   # [0.      0.61486  1.65043  18.56481]

######################
## erfinv / erfcinv ##
######################
'''
erfinv(y)   : x such that erf(x) = y.     y ∈ (-1, 1).
erfcinv(y)  : x such that erfc(x) = y.    y ∈ (0, 2).

erf and erfc are monotone, so inverses are unique.
erfinv is used in quantile functions: the z-score for a given normal probability.
erfinv(y) = ndtri((y+1)/2) / sqrt(2).
'''

y_inv = np.array([-0.9, -0.5, 0.0, 0.5, 0.9])
x_inv = erfinv(y_inv)
print("erfinv(y):", x_inv.round(5))
# [-1.16309 -0.47694  0.      0.47694  1.16309]

# Round-trip
print(np.allclose(erf(x_inv), y_inv, atol=1e-12))   # True

# erfcinv: y ∈ (0, 2)
y_ci = np.array([0.1, 0.5, 1.0, 1.5, 1.9])
x_ci = erfcinv(y_ci)
print("erfcinv(y):", x_ci.round(5))
# [1.16309  0.47694  0.     -0.47694 -1.16309]
print(np.allclose(erfc(x_ci), y_ci, atol=1e-12))    # True

#############################
## ndtr / ndtri / log_ndtr ##
#############################
'''
ndtr(x)      : Φ(x) = P(Z ≤ x) for Z ~ N(0,1). The normal CDF.
               ndtr(x) = erfc(-x/sqrt(2)) / 2.
ndtri(p)     : Φ⁻¹(p) — probit function / normal quantile (ppf).
               ndtri(0.975) ≈ 1.96 (95% two-sided CI z-score).
log_ndtr(x)  : log Φ(x), computed accurately for large negative x
               where Φ(x) underflows to 0.
'''

x_nd = np.array([-3.0, -1.96, 0.0, 1.645, 1.96, 3.0])
Phi = ndtr(x_nd)
print("Φ(x):", Phi.round(5))
# [0.00135  0.025  0.5  0.95002  0.975  0.99865]

# Quantile function
p_q = np.array([0.025, 0.5, 0.95, 0.975, 0.99])
z_q = ndtri(p_q)
print("Φ⁻¹(p):", z_q.round(4))
# [-1.96  0.  1.6449  1.96  2.3263]

# Log-CDF: accurate in far left tail
x_far = np.array([-10.0, -20.0, -30.0])
print("log Φ(x):", log_ndtr(x_far))
# log Φ(x): [ -53.23128515 -203.91715537 -454.32124396] — computable, whereas ndtr gives 0


#-------------------------------------------------------------------------------------------------#
#═══════════════════════════════  PART G — ORTHOGONAL POLYNOMIALS  ═══════════════════════════════#
#-------------------------------------------------------------------------------------------------#
'''
Orthogonal polynomials satisfy ∫ w(x) P_m(x) P_n(x) dx = 0 for m ≠ n.
Two API styles are available:

  eval_*(n, x)       : vectorised ufunc, evaluates polynomial of degree n at points x.
  *(n)               : returns a numpy.poly1d (or orthopoly1d) object — useful for roots/coefficients.

The poly1d object supports:
  p.c     : coefficients [highest power ... constant]
  p.r     : roots (= zeros of the polynomial)
  p(x)    : evaluate (same as eval_*)
'''

x_poly = np.linspace(-1, 1, 5)   # canonical domain for most polynomials

##############
## Legendre ##
##############
'''
eval_legendre(n, x)  : P_n(x), Legendre polynomial of degree n.
                       Orthogonal on [-1, 1] with weight w(x) = 1.
                       Recurrence: (n+1)P_{n+1} = (2n+1)x P_n - n P_{n-1}.
Boundary conditions: P_n(1) = 1, P_n(-1) = (-1)^n.
Used in: quadrature (Gauss-Legendre), multipole expansions, angular parts of hydrogen wavefunctions.
'''

for n in range(5):
    Pn = eval_legendre(n, x_poly)
    print(f"P_{n}(x): {Pn.round(4)}")
# P_0(x): [1. 1. 1. 1. 1.]
# P_1(x): [-1.  -0.5  0.   0.5  1. ]
# P_2(x): [ 1.    -0.125 -0.5   -0.125  1.   ]
# P_3(x): [-1.      0.4375  0.     -0.4375  1.    ]
# P_4(x): [ 1.     -0.2891  0.375  -0.2891  1.    ]

# Orthogonality: ∫₋₁¹ P_m P_n dx ≈ 0 for m≠n
x_quad = np.linspace(-1, 1, 2000)
for m, n in [(0,1), (1,2), (2,3)]:
    integral = np.trapezoid(eval_legendre(m, x_quad) * eval_legendre(n, x_quad), x_quad)
    print(f"∫ P_{m}*P_{n} dx ≈ {integral:.5f}")   # all ≈ 0
# ∫ P_0*P_1 dx ≈ 0.00000
# ∫ P_1*P_2 dx ≈ 0.00000
# ∫ P_2*P_3 dx ≈ -0.00000

# legendre poly1d object
P4 = legendre(4)
print("P_4 roots:", P4.r.round(4))   # [ 0.8611 -0.8611  0.34   -0.34  ] Gauss-Legendre nodes of degree 4

###############
## Chebyshev ##
###############
'''
eval_chebyt(n, x)  : T_n(x), Chebyshev polynomial of the 1st kind.
                     Orthogonal on [-1, 1] with weight w(x) = 1/sqrt(1-x²).
                     T_n(cos θ) = cos(n θ)  — trigonometric identity.
                     Minimises maximum deviation from 0 (Chebyshev equioscillation).

eval_chebyu(n, x)  : U_n(x), Chebyshev polynomial of the 2nd kind.
                     Orthogonal with weight w(x) = sqrt(1-x²).
                     U_n(cos θ) = sin((n+1)θ)/sin θ.

Used in: polynomial interpolation (Chebyshev nodes), filter design, spectral methods.
'''

x_cheb = np.cos(np.linspace(0, np.pi, 6))   # Chebyshev nodes
T3 = eval_chebyt(3, x_cheb)
print("T_3 at Chebyshev nodes:", T3.round(4))   # [ 1.    -0.309 -0.809  0.809  0.309 -1.   ] = cos(3*arccos(x))

# T_n(cos θ) = cos(nθ)
theta = np.linspace(0, np.pi, 7)
x_t   = np.cos(theta)
print(np.allclose(eval_chebyt(5, x_t), np.cos(5 * theta)))   # True

# Chebyshev nodes of degree n: roots of T_n, optimal for interpolation
T5_poly = chebyt(5)
cheb_nodes = np.sort(T5_poly.r)
print("T_5 roots (Chebyshev nodes):", cheb_nodes.round(4)) # [-0.9511 -0.5878  0.      0.5878  0.9511]
# [-0.9511 -0.5878  0.  0.5878  0.9511]

#############
## Hermite ##
#############
'''
eval_hermite(n, x)     : H_n(x), physicist Hermite polynomial.
                         H_n''- 2x H_n' + 2n H_n = 0
                         Orthogonal on (-∞, ∞) with weight exp(-x²).
                         H_0=1, H_1=2x, H_2=4x²-2, H_3=8x³-12x.

eval_hermitenorm(n, x) : He_n(x), probabilist Hermite.
                         He_n(x) = 2^{-n/2} H_n(x/sqrt(2)).
                         Orthogonal with weight exp(-x²/2) — standard normal PDF.
                         He_1 = x, He_2 = x²-1, He_3 = x³-3x  (Hermite moments).

H_n appears in: quantum harmonic oscillator wavefunctions, moment generating functions,
                Gauss-Hermite quadrature.
'''

x_herm = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
H3 = eval_hermite(3, x_herm)
print("H_3(x):", H3)   # [-40.   4.  -0.  -4.  40.]  (= 8x³ - 12x)
print(np.allclose(H3, 8*x_herm**3 - 12*x_herm))   # True

He3 = eval_hermitenorm(3, x_herm)
print("He_3(x):", He3)   # [-2. -2.  0.  2.  2.]  (= x³ - 3x)
print(np.allclose(He3, x_herm**3 - 3*x_herm))   # True

# Gauss-Hermite quadrature nodes = roots of H_n
Hn_poly = hermite(5)
gh_nodes = np.sort(Hn_poly.r)
print("Gauss-Hermite nodes (n=5):", gh_nodes.real.round(4))
# [-2.0202 -0.9586  0.      0.9586  2.0202]

##############
## Laguerre ##
##############
'''
eval_laguerre(n, x)          : L_n(x), Laguerre polynomial.
                               Orthogonal on [0, ∞) with weight exp(-x).
                               L_0=1, L_1=1-x, L_2=1-2x+x²/2.

eval_genlaguerre(n, alpha, x) : L_n^(α)(x), generalised (associated) Laguerre polynomial.
                               Orthogonal with weight x^α * exp(-x).
                               Appears in: radial hydrogen wavefunctions (α = 2l+1),
                               Gauss-Laguerre quadrature.
'''

x_lag = np.array([0.0, 0.5, 1.0, 2.0, 5.0])
L2 = eval_laguerre(2, x_lag)
print("L_2(x):", L2.round(5))   # [ 1.     0.125 -0.5   -1.     3.5  ]
print(np.allclose(L2, 1 - 2*x_lag + x_lag**2/2))   # True

GL3 = eval_genlaguerre(3, 1.5, x_lag) # α = 1.5
print("L_3^(1.5)(x):", GL3.round(5)) # [ 6.5625   3.16667  0.77083 -1.52083  2.60417]


#-------------------------------------------------------------------------------------------------#
#═══════════════════  PART H — RAW STATISTICAL (CDF / SF / INVERSE) FUNCTIONS  ═══════════════════#
#-------------------------------------------------------------------------------------------------#
'''
scipy.special provides low-level CDF, SF (survival function = 1-CDF), and inverse functions
for common distributions. These are the primitives underlying scipy.stats distributions.
The naming convention is:
  <dist>tr  : CDF  (probability up to x)
  <dist>trc : complementary CDF / survival function
  <dist>tri : inverse of CDF (quantile function)
'''

##############
## Binomial ##
##############
'''
bdtr(k, n, p)  : P(X ≤ k) for X ~ Binomial(n, p).  k can be non-integer.
bdtrc(k, n, p) : P(X > k) — survival function.
bdtri(k, n, y) : p such that bdtr(k, n, p) = y.
'''

k_binom, n_binom, p_binom = 3, 10, 0.5
P_binom  = bdtr(k_binom, n_binom, p_binom)
Q_binom  = bdtrc(k_binom, n_binom, p_binom)
print(f"P(X ≤ 3 | n=10, p=0.5) = {P_binom:.5f}")   # 0.17188
print(f"P(X > 3 | n=10, p=0.5) = {Q_binom:.5f}")   # 0.82813
print(np.isclose(P_binom + Q_binom, 1.0))            # True

p_inv = bdtri(k_binom, n_binom, P_binom)
print(f"bdtri round-trip: p = {p_inv:.5f}")          # 0.5

#################
## Chi-squared ##
#################
'''
chdtr(v, x)  : P(X ≤ x) for X ~ χ²(v).  = gammainc(v/2, x/2).
chdtrc(v, x) : 1 - chdtr(v, x) = gammaincc(v/2, x/2).
chdtri(v, p) : x such that chdtr(v, x) = p  — chi-squared quantile.
               chdtri(v, 0.95) gives the 95th percentile of χ²(v).
'''

df_chi = 4.0
x_chi  = np.array([1.0, 4.0, 7.779, 9.488])
P_chi  = chdtr(df_chi, x_chi)
print("χ²(4) CDF:", P_chi.round(5))
# χ²(4) CDF: [0.0902  0.59399 0.89998 0.95001]

# Standard critical values: χ²(4) at 95th and 99th percentiles
print(f"χ²(4, 0.95) = {chdtri(df_chi, 0.95):.4f}")   # χ²(4, 0.95) = 0.7107
print(f"χ²(4, 0.99) = {chdtri(df_chi, 0.99):.4f}")   # χ²(4, 0.99) = 0.2971

####################
## F-distribution ##
####################
'''
fdtr(dfn, dfd, x)  : CDF of F(dfn, dfd).
fdtrc(dfn, dfd, x) : SF of F(dfn, dfd).
fdtri(dfn, dfd, p) : Quantile (inverse CDF).

Critical value F(0.05; dfn, dfd) is threshold for ANOVA significance test.
'''

dfn, dfd = 3.0, 20.0
F_crit_95 = fdtri(dfn, dfd, 0.95)
print(f"F_{{0.05}}(3, 20) = {F_crit_95:.4f}")   # 3.0984

P_F = fdtr(dfn, dfd, F_crit_95)
print(f"CDF at critical value: {P_F:.5f}")   # 0.95

############################
## Student t-distribution ##
############################
'''
stdtr(df, t)   : CDF of t(df). stdtr(df, 0) = 0.5 (symmetric about 0).
stdtrit(df, p)  : Quantile. stdtri(df, 0.975) ≈ 1.96 as df → ∞.

One-sided p-value: p_one_sided = stdtrc(df, |t_observed|) = 1 - stdtr(df, |t|).
Two-sided p-value: p_two_sided = 2 * (1 - stdtr(df, |t|)).
'''

df_t = 10.0
t_val = 2.228   # ≈ t(10) critical at 97.5%

P_t = stdtr(df_t, t_val)
print(f"P(T ≤ {t_val} | df=10) = {P_t:.5f}")   # P(T ≤ 2.228 | df=10) = 0.97499

t_crit = stdtrit(df_t, 0.975)
print(f"t(10, 0.975) = {t_crit:.4f}")            # 2.2281  (two-sided 95% CI)

# Two-sided p-value for an observed t-statistic
t_obs = 2.8
p_two = 2 * (1 - stdtr(df_t, abs(t_obs)))
print(f"Two-sided p-value (t={t_obs}, df=10): {p_two:.5f}")   # 0.01879


#-------------------------------------------------------------------------------------------------#
#══════════════════════════════  PART I — INFORMATION THEORY  ════════════════════════════════════#
#-------------------------------------------------------------------------------------------------#

##############################
## entr / rel_entr / kl_div ##
##############################
'''
entr(x)         : -x * log(x)  for x > 0, 0 for x = 0, -inf for x < 0.
                  Element-wise contribution to Shannon entropy H(p) = sum(entr(p)).

rel_entr(x, y)  : x * log(x/y)  — element-wise KL divergence contribution.
                  KL(p||q) = sum(rel_entr(p, q)).
                  rel_entr handles 0*log(0) = 0, and 0*log(0/0) = 0 correctly.

kl_div(x, y)    : x * log(x/y) - x + y   (generalised KL, includes normalisation term).
                  Reduces to rel_entr when distributions are normalised (sum=1).
'''

# Shannon entropy of a discrete distribution
p_dist = np.array([0.2, 0.3, 0.1, 0.4])
H = np.sum(entr(p_dist))
print(f"H(p) = {H:.5f} nats")   # 1.27985 nats
print(f"H(p) = {H/np.log(2):.5f} bits")   # 1.84644 bits

# Maximum entropy: uniform distribution
p_uniform = np.ones(4) / 4
print(f"H(uniform) = {np.sum(entr(p_uniform)):.5f} = log(4) = {np.log(4):.5f}")
# H(uniform) = 1.38629 = log(4) = 1.38629

# KL divergence: KL(p||q)
q_dist = np.array([0.25, 0.25, 0.25, 0.25])   # uniform
KL_pq = np.sum(rel_entr(p_dist, q_dist))
print(f"KL(p||q) = {KL_pq:.5f}") # 0.10644 (p vs uniform)

# KL is asymmetric
KL_qp = np.sum(rel_entr(q_dist, p_dist))
print(f"KL(q||p) = {KL_qp:.5f}") # 0.12178 ≠ KL(p||q)

# KL divergence is non-negative
print(KL_pq >= 0 and KL_qp >= 0) # True

##########################
## huber / pseudo_huber ##
##########################
'''
huber(delta, r)       : Huber loss = delta * (|r| - delta/2)  if |r| > delta
                                    = 0.5 * r²               if |r| ≤ delta.
                        Quadratic near 0, linear in tails — robust to outliers.
                        delta controls the transition point.

pseudo_huber(delta, r): sqrt(1 + (r/delta)²) * delta² - delta.
                        Smooth everywhere (C∞); approximates Huber.
                        Gradient: r / sqrt(1 + (r/delta)²).
'''

delta = 1.0
r_vals = np.array([-3.0, -1.0, -0.5, 0.0, 0.5, 1.0, 3.0])
H_loss  = huber(delta, r_vals)
PH_loss = pseudo_huber(delta, r_vals)
print("Huber loss      :", H_loss.round(4))
# [2.5    0.5    0.125  0.     0.125  0.5    2.5   ]
print("Pseudo-Huber    :", PH_loss.round(4))
# [2.1623 0.4142 0.1180 0.     0.1180 0.4142 2.1623]

# In the quadratic region (|r| ≤ δ): both ≈ 0.5*r²
print(np.allclose(huber(delta, 0.5), 0.5*0.5**2))   # True

# Compare to plain L2 (MSE) and L1 (MAE) for outlier at r=5
r_out = 5.0
print(f"L2={0.5*r_out**2:.1f},  L1={r_out:.1f},  Huber={huber(1.0, r_out):.1f}")
# L2=12.5   L1=5.0   Huber=4.5   ← Huber penalises outlier less than L2


#-------------------------------------------------------------------------------------------------#
#═══════════════════  PART J — ZETA, FRESNEL, EXPN, LOGIT, EXPIT, LOG HELPERS  ═══════════════════#
#-------------------------------------------------------------------------------------------------#

##################
## zeta / zetac ##
##################
'''
zeta(x, q=1)     : Hurwitz zeta ζ(x, q) = Σ_{n=0}^∞ 1/(n+q)^x.
                   zeta(x) == zeta(x, 1).

zetac(x)         : ζ(x) - 1  (removes the n=1 term for stability near x=1).
'''

x_zeta = np.array([2.0, 3.0, 4.0, 6.0])
Z = zeta(x_zeta)
print("ζ(x):", Z.round(6))
# ζ(x): [1.644934 1.202057 1.082323 1.017343]

# Known identities
print(np.isclose(zeta(2), np.pi**2/6))    # True
print(np.isclose(zeta(4), np.pi**4/90))   # True

# Hurwitz zeta
Z_hurwitz = zeta(2.0, 2.0)   # ζ(2, 2) = ζ(2) - 1 = π²/6 - 1
print(f"ζ(2, 2) = {Z_hurwitz:.6f},  π²/6 - 1 = {np.pi**2/6 - 1:.6f}")   # both 0.644934

# zetac(x) = ζ(x) - 1
print(np.allclose(zetac(x_zeta), zeta(x_zeta) - 1.0))   # True

#######################
## Fresnel integrals ##
#######################
'''
fresnel(z) -> (S, C)
  S(z) = ∫₀^z sin(π t²/2) dt   — Fresnel sine integral
  C(z) = ∫₀^z cos(π t²/2) dt   — Fresnel cosine integral

Both S and C approach 0.5 as z -> ∞  (the Cornu spiral converges to (0.5, 0.5)).
Used in: diffraction optics, clothoid road/rail alignment, radar signal processing.
'''

z_fres = np.array([0.0, 0.5, 1.0, 2.0, 5.0, 10.0])
S, C = fresnel(z_fres)
print("Fresnel S(z):", S.round(5))
# [0.      0.06473 0.43826 0.34342 0.49919 0.46817]
print("Fresnel C(z):", C.round(5))
# [0.      0.49234 0.77989 0.48825 0.56364 0.49999]

# Cornu spiral: (C(t), S(t)) as t varies
t_cornu = np.linspace(0, 5, 500)
S_c, C_c = fresnel(t_cornu)
print(f"Cornu endpoint: C={C_c[-1]:.4f}, S={S_c[-1]:.4f}")   # Cornu endpoint: C=0.5636, S=0.4992

#############################################
## Exponential integrals: expn, exp1, expi ##
#############################################
'''
expn(n, x)  : E_n(x) = ∫₁^∞ exp(-x*t)/t^n dt   for integer n ≥ 0, x > 0.
              E_1(x) = exp1(x).  E_0(x) = exp(-x)/x.

exp1(z)     : E_1(z) = ∫_z^∞ exp(-t)/t dt.  Singular (log) at z = 0.
              exp1(x) = expn(1, x) for real x > 0.

expi(x)     : Ei(x) = P.V. ∫_{-∞}^x exp(t)/t dt  for x > 0.
              Ei(x) = -E_1(-x)  for x > 0 (related by analytic continuation).
              Used in heat conduction, nuclear reactor physics.

All three grow logarithmically near x = 0.
'''

x_exp = np.array([0.1, 0.5, 1.0, 2.0, 5.0])
E1 = exp1(x_exp)
print("E_1(x):", E1.round(5))
# E_1(x): [1.82292e+00 5.59770e-01 2.19380e-01 4.89000e-02 1.15000e-03]

En2 = expn(2, x_exp)    # E_2(x)
En3 = expn(3, x_exp)    # E_3(x)
print("E_2(x):", En2.round(5)) # E_2(x): [0.72255 0.32664 0.1485  0.03753 0.001  ]
print("E_3(x):", En3.round(5)) # E_3(x): [0.41629 0.2216  0.10969 0.03013 0.00088]

# Ei(x) for positive x
Ei = expi(x_exp)
print("Ei(x):", Ei.round(4))
# [-0.2194  0.4542  1.8951  4.9542  40.1853]

# Recurrence: E_{n+1}(x) = (exp(-x) - x*E_n(x)) / n
# Verify E_2 from E_1
E2_recur = (np.exp(-x_exp) - x_exp * E1) / 1
print(np.allclose(En2, E2_recur, atol=1e-10))   # True

###################
## logit / expit ##
###################
'''
logit(x)   : log(x / (1-x))  — log-odds function.  x ∈ (0, 1).
             Inverse of expit. Maps probability to real line.
             logit(0.5) = 0.  logit → ±∞ near 0 and 1.

expit(x)   : 1 / (1 + exp(-x))  — sigmoid / logistic function.
             Inverse of logit. Maps real line to (0, 1).
             Gradient: expit(x) * (1 - expit(x))  (used in backprop).
             Numerically stable (avoids overflow for large |x|).

Both handle arrays efficiently. Used ubiquitously in logistic regression,
neural networks, and Bayesian log-odds parameterisation.
'''

p_logit = np.array([0.01, 0.1, 0.5, 0.9, 0.99])
l = logit(p_logit)
print("logit(p):", l.round(4))
# [-4.5951 -2.1972  0.      2.1972  4.5951]

# Round-trip: expit(logit(p)) == p
print(np.allclose(expit(l), p_logit))   # True

x_sig = np.array([-5.0, -1.0, 0.0, 1.0, 5.0])
s = expit(x_sig)
print("expit(x) [sigmoid]:", s.round(5))
# [0.00669  0.26894  0.5     0.73106  0.99331]

# Derivative: σ'(x) = σ(x)(1 - σ(x))
sig_grad = s * (1 - s)
print("σ'(x):", sig_grad.round(5))
# σ'(x): [0.00665 0.19661 0.25    0.19661 0.00665]

# Numerically stable for extreme x (no overflow)
print("expit(1000):", expit(1000.0))     # exactly 1.0
print("expit(-1000):", expit(-1000.0))   # exactly 0.0

#################################
## xlogy / xlog1py / logsumexp ##
#################################
'''
xlogy(x, y)     : x * log(y), but returns 0 when x == 0 (even if y == 0 or y < 0).
                  Avoids NaN in entropy computations where 0 * log(0) should be 0.

xlog1py(x, y)   : x * log(1 + y), returning 0 when x == 0.
                  Used for log-probabilities near 0: x * log(1 + y) ≈ x*y for small y.

logsumexp(a, axis=None, b=None, keepdims=False, return_sign=False)
                : log(sum(exp(a))), computed stably by subtracting the max.
                  logsumexp(a) = max(a) + log(sum(exp(a - max(a)))).
                  Avoids overflow/underflow when exponentiating large/small values.
                  Essential in: log-space softmax, log-marginalisation, HMM forward pass.
'''

# xlogy: 0*log(0) -> 0, not NaN
p_zero = np.array([0.0, 0.5, 1.0])
print("xlogy(p, p):", xlogy(p_zero, p_zero))   # [0.  -0.34657  0.] == p*log(p)

# Cross-entropy H(p, q) = -sum(p * log(q))
p_ce = np.array([0.3, 0.4, 0.3])
q_ce = np.array([0.25, 0.5, 0.25])
cross_ent = -np.sum(xlogy(p_ce, q_ce))
print(f"H(p, q) = {cross_ent:.5f}")   # H(p, q) = 1.10904

# xlog1py: useful for Bernoulli log-likelihood
p_bern, x_bern = 0.7, 1.0
log_lik = xlogy(x_bern, p_bern) + xlog1py(1 - x_bern, -p_bern)
print(f"Bernoulli log-lik: {log_lik:.5f}")   # log(0.7) = -0.35667

# logsumexp: stable log of partition function
log_unnorm = np.array([-1000.0, -999.0, -998.0])  # would underflow with naive exp
lse = logsumexp(log_unnorm)
print(f"logsumexp: {lse:.5f}") # -997.59 (correct)
print(f"naive log-sum-exp: {np.log(np.sum(np.exp(log_unnorm))):.5f}")  # 0.0 (WRONG - underflow)

# With weights (b parameter): log(sum(b * exp(a)))
log_scores = np.array([1.0, 2.0, 3.0])
weights    = np.array([0.2, 0.5, 0.3])
lse_w = logsumexp(log_scores, b=weights)
direct = np.log(np.sum(weights * np.exp(log_scores)))
print(f"Weighted logsumexp: {lse_w:.5f} == {direct:.5f}")   # both 2.32863

# Softmax in log-space (numerically stable)
def log_softmax(x):
    return x - logsumexp(x)

logits = np.array([2.0, 1.0, 0.1, -1.0])
lsm = log_softmax(logits)
print("log-softmax:", lsm.round(4)) # [-0.4493 -1.4493 -2.3493 -3.4493]
print("softmax    :", np.exp(lsm).round(4))   # [0.6381 0.2347 0.0954 0.0318] sums to 1.0
print(np.isclose(np.sum(np.exp(lsm)), 1.0))   # True
