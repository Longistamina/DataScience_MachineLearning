'''
1. RNG setup & infrastructure
   + np.random.default_rng()        : recommended way to create a Generator (uses PCG64).
   + np.random.Generator()          : Generator class; wraps any BitGenerator.
   + np.random.SeedSequence()       : converts arbitrary seeds into initial BitGenerator state.
   BitGenerators (passed to Generator):
   + np.random.PCG64                : default — excellent statistical properties and speed.
   + np.random.MT19937              : legacy Mersenne Twister (used by old RandomState).
   + np.random.Philox               : counter-based PRNG; designed for parallel streams.
   + np.random.SFC64                : Small Fast Counting; very fast, good quality.

2. Simple random data
   + rng.random()                   : uniform floats in [0, 1).
   + rng.integers()                 : uniform integers in [low, high).
   + rng.bytes()                    : random bytes string.
   + rng.choice()                   : random sample from a 1-D array (with or without replacement).

3. Permutations
   + rng.shuffle()                  : randomly shuffle an array in-place.
   + rng.permutation()              : return a new randomly permuted array (copy).
   + rng.permuted()                 : permute each row/column independently (axis-aware).

4. Continuous distributions
   + rng.uniform()                  : uniform floats on [low, high).
   + rng.random()                   : shorthand for uniform on [0, 1) (alias for rng.uniform(0,1)).
   + rng.standard_normal()          : N(0, 1) — standard Gaussian.
   + rng.normal()                   : N(loc, scale) — Gaussian with given mean and std.
   + rng.standard_exponential()     : Exp(1) — standard exponential.
   + rng.exponential()              : Exp(scale) — exponential with given scale (= 1/λ).
   + rng.gamma()                    : Gamma(shape, scale) — generalization of exponential.
   + rng.beta()                     : Beta(a, b) — bounded [0,1]; conjugate prior for Bernoulli.
   + rng.standard_gamma()           : Gamma(shape, scale=1).
   + rng.chisquare()                : χ²(df) — sum of squared normals; used in hypothesis tests.
   + rng.standard_t()               : t(df) — Student's t with given degrees of freedom.
   + rng.f()                        : F(dfnum, dfden) — ratio of χ² variables; used in ANOVA.
   + rng.lognormal()                : LogNormal(mean, sigma) — exp of a normal variable.
   + rng.logistic()                 : Logistic(loc, scale) — heavier tails than normal.
   + rng.laplace()                  : Laplace(loc, scale) — double-exponential; used in L1 models.
   + rng.triangular()               : Triangular(left, mode, right) — bounded, piecewise linear.
   + rng.power()                    : Power-function distribution on [0, 1].
   + rng.wald()                     : Wald (inverse Gaussian) distribution.
   + rng.rayleigh()                 : Rayleigh distribution — 2-D wind speed magnitude.
   + rng.pareto()                   : Pareto distribution — heavy tail (power law).
   + rng.gumbel()                   : Gumbel (extreme value) distribution.
   + rng.weibull()                  : Weibull distribution — reliability & lifetime modeling.
   + rng.vonmises()                 : von Mises (circular normal) — angles & directions.

5. Discrete distributions
   + rng.integers()                 : uniform integers (already in §2; documented in full here).
   + rng.binomial()                 : Binomial(n, p) — number of successes in n Bernoulli trials.
   + rng.poisson()                  : Poisson(lam) — number of events in a fixed interval.
   + rng.geometric()                : Geometric(p) — number of trials until first success.
   + rng.hypergeometric()           : Hypergeometric — sampling without replacement.
   + rng.negative_binomial()        : Negative binomial — number of failures before r successes.
   + rng.multinomial()              : Multinomial(n, pvals) — generalization of binomial.
   + rng.zipf()                     : Zipf / zeta distribution — rank-frequency power law.

6. Multivariate distributions
   + rng.multivariate_normal()      : multivariate Gaussian — ML features, MCMC proposals.
   + rng.multivariate_hypergeometric(): multivariate sampling without replacement.
   + rng.dirichlet()                : Dirichlet(alpha) — distribution over probability vectors.

7. Parallel generation
   + SeedSequence.spawn()           : generate independent child seeds for parallel workers.
   + rng.bit_generator.jumped()     : advance the BitGenerator state by a large fixed step.

8. scipy.stats — distributions with .rvs()  (not in numpy.random)
   + scipy.stats.<dist>.rvs()       : sample from any of 100+ scipy continuous/discrete dists.
   Common ones: norm, t, chi2, f, beta, gamma, expon, lognorm, uniform, binom, poisson, nbinom.

9. scipy.stats.qmc — Quasi-Monte Carlo  (not in numpy.random)
   + qmc.Sobol()                    : Sobol' low-discrepancy sequence (best for 2^m points).
   + qmc.Halton()                   : Halton sequence (arbitrary n; slower convergence than Sobol').
   + qmc.LatinHypercube()           : Latin Hypercube Sampling — each stratum sampled exactly once.
   + qmc.scale()                    : scale a [0,1]^d sample to arbitrary [l,u]^d bounds.
   + qmc.discrepancy()              : measure uniformity of a QMC sample (lower = better).

10. Legacy API  (numpy.random module-level functions — do NOT use in new code)
   np.random.seed()       → rng = np.random.default_rng(seed)
   np.random.rand()       → rng.random(size)
   np.random.randn()      → rng.standard_normal(size)
   np.random.randint()    → rng.integers(low, high, size)
   np.random.choice()     → rng.choice(a, size, replace, p)
   np.random.shuffle()    → rng.shuffle(a)
   np.random.permutation()→ rng.permutation(a)
   np.random.normal()     → rng.normal(loc, scale, size)
   np.random.uniform()    → rng.uniform(low, high, size)
   np.random.exponential()→ rng.exponential(scale, size)
   np.random.poisson()    → rng.poisson(lam, size)
   np.random.binomial()   → rng.binomial(n, p, size)
   np.random.multinomial()→ rng.multinomial(n, pvals, size)
   np.random.multivariate_normal() → rng.multivariate_normal(mean, cov, size)
   np.random.RandomState()→ np.random.default_rng()  (drop-in replacement)
'''

import numpy as np
from scipy.stats import qmc
import scipy.stats as spstats

# ── Shared test data ─────────────────────────────────────────────────────────────────────────────
rng = np.random.default_rng(42)     # seeded Generator — reproducible throughout this file

arr    = np.array([10, 20, 30, 40, 50])
mat    = np.arange(12).reshape(3, 4)
pop    = np.array(['a', 'b', 'c', 'd', 'e'])


# =========================================================================================
# 1. RNG setup & infrastructure
# =========================================================================================

##-------------------------##
## np.random.default_rng() ##
##-------------------------##
'''
np.random.default_rng() is the recommended way to create a Generator instance.

- No argument      : seeded from OS entropy → different sequence every run.
- Integer seed     : deterministic sequence; same seed → same output.
- SeedSequence     : for advanced seeding (parallel, hierarchical).
- BitGenerator obj : wrap an already-constructed BitGenerator.

The default BitGenerator is PCG64, which has better statistical properties and performance
than the legacy MT19937 (Mersenne Twister) used by np.random.RandomState.

Note: numpy.random functions like np.random.rand(), np.random.randn() are LEGACY
(they use a global RandomState). Always prefer rng = default_rng() for new code.
'''

rng_unseeded = np.random.default_rng()          # different output every run
rng_seeded   = np.random.default_rng(42)        # reproducible
rng_large    = np.random.default_rng(2**128 - 1) # seeds can be arbitrarily large integers

print(rng_seeded)
# Generator(PCG64)  — shows the underlying BitGenerator

print(rng_seeded.random())
# 0.7739560485559633  (first draw from seed=42)
# NOTE: calling rng_seeded.random() again gives a DIFFERENT value — the Generator is stateful;
# each call advances its internal state to the next number in the sequence.
# To reproduce the same value, you must re-create the Generator with the same seed.

print(np.random.default_rng(42).random())
# 0.7739560485559633  (fresh Generator with same seed → same first value)

##-----------------------##
## np.random.Generator() ##
##-----------------------##
'''
np.random.Generator wraps any BitGenerator to provide distribution methods.

All four built-in BitGenerators:
  PCG64    — default; permuted congruential generator. Best general-purpose choice.
  MT19937  — Mersenne Twister; legacy default used by RandomState. Slower, larger state.
  Philox   — counter-based PRNG; deterministic, ideal for reproducible parallel streams.
  SFC64    — Small Fast Counting; fastest of the four; very good quality.

All produce the same distribution interface; only the underlying bit stream differs.
'''

from numpy.random import Generator, PCG64, MT19937, Philox, SFC64

rng_pcg  = Generator(PCG64(42))
rng_mt   = Generator(MT19937(42))
rng_phi  = Generator(Philox(42))
rng_sfc  = Generator(SFC64(42))

print(rng_pcg.random())   # 0.7739560485559633   (PCG64 with seed 42)
print(rng_mt.random())    # 0.5419938930062744   (MT19937 with seed 42 — different stream)
print(rng_phi.random())   # 0.08607763073528474  (Philox)
print(rng_sfc.random())   # 0.5299360452325557   (SFC64)

##------------------------##
## np.random.SeedSequence ##
##------------------------##
'''
np.random.SeedSequence converts an arbitrary seed into a high-quality state for any BitGenerator.

- Accepts any non-negative integer of any size, or a sequence of integers.
- Ensures independent child streams via spawn(), even from the same parent seed.
- Internally used by default_rng(); also useful directly for fine-grained control.
'''

from numpy.random import SeedSequence

ss = SeedSequence(12345)
print(ss.entropy)
# 12345  (the seed provided)

# Generate the initial state for a BitGenerator
bg_state = PCG64(ss)
print(Generator(bg_state).random())
# 0.5488135039273248

# spawn() creates n independent child SeedSequences (for parallel workers — see section 7)
children = ss.spawn(4)
print([type(c).__name__ for c in children])
# ['SeedSequence', 'SeedSequence', 'SeedSequence', 'SeedSequence']


# =========================================================================================
# 2. Simple random data
# =========================================================================================

##--------------##
## rng.random() ##
##--------------##
'''
rng.random() draws uniform floats from [0.0, 1.0).

- size=None  : returns a scalar.
- size=int   : returns a 1-D array.
- size=tuple : returns an array of that shape.

The output dtype is always float64.
For float32, use rng.random(size=..., dtype=np.float32).
'''

print(rng.random())
# 0.950714306...  (single float)

print(rng.random(5))
# [0.7319939  0.5986585  0.1560186  0.1559945  0.0580836]

print(rng.random((2, 3)))
# [[0.8661762  0.7080726  0.0205845]
#  [0.9699099  0.8324426  0.2123391]]

# Scale to [a, b): a + (b - a) * rng.random(...)
print(5 + 10 * rng.random(4))
# values in [5, 15)

##----------------##
## rng.integers() ##
##----------------##
'''
rng.integers() draws uniform random integers from [low, high).

- low  : lower bound (inclusive).
- high : upper bound (exclusive by default); pass endpoint=True to make it inclusive.
- dtype: any integer dtype (default np.intp, which is int64 on 64-bit systems).

Replaces the legacy np.random.randint() and np.random.random_integers().
'''

print(rng.integers(0, 10))
# 5  (single integer in [0, 10))

print(rng.integers(0, 10, size=6))
# [0 4 5 9 6 5]

print(rng.integers(1, 7, size=(2, 3)))   # simulating 2×3 dice rolls
# [[4 4 5]
#  [2 5 4]]

print(rng.integers(0, 10, endpoint=True, size=5))   # [0, 10] inclusive
# [2 4 7 7 9]

##-------------##
## rng.bytes() ##
##-------------##
'''
rng.bytes() returns a Python bytes object of length n filled with random bytes.

Useful for generating keys, tokens, or raw binary data.
Not suitable for cryptographic purposes (use secrets.token_bytes() instead).
'''

print(rng.bytes(8))
# b'\x...'  (8 random bytes; exact value varies)

print(len(rng.bytes(16)))
# 16

##--------------##
## rng.choice() ##
##--------------##
'''
rng.choice() draws random samples from an array or range.

- a          : 1-D array to sample from, or integer n to sample from range(n).
- size       : output shape.
- replace    : True (default) = with replacement; False = without replacement.
- p          : probability weights for each element (must sum to 1).
- axis       : axis along which to sample for multi-dimensional arrays.
- shuffle    : if False and replace=False, output retains input order.
'''

print(arr)
# [10 20 30 40 50]

print(rng.choice(arr))
# 30  (single random element)

print(rng.choice(arr, size=3))
# [40 10 40]  (with replacement — allowing repeats)

print(rng.choice(arr, size=3, replace=False))
# [20 50 40]  (without replacement — no repeats)

print(rng.choice(arr, size=3, p=[0.1, 0.1, 0.5, 0.1, 0.2]))
# [30 30 50]  (30 has p=0.5, so drawn more often)

print(rng.choice(pop, size=4))
# ['b' 'a' 'c' 'b']  (works with string arrays too)

# Multi-dimensional: choice along axis=0 picks entire rows
print(rng.choice(mat, size=2, axis=0))
# [[ 8  9 10 11]
#  [ 0  1  2  3]]
# picks 2 of the 3 rows at random


# =========================================================================================
# 3. Permutations
# =========================================================================================

##---------------##
## rng.shuffle() ##
##---------------##
'''
rng.shuffle() randomly shuffles an array IN-PLACE along a given axis.

- Modifies the array directly; returns None.
- axis=0 (default): shuffle rows (treats the array as a sequence of rows).
- axis=1: shuffle within each row independently.
- For 1-D arrays, shuffles all elements.
'''

a = arr.copy()
rng.shuffle(a)
print(a)
# [30 10 50 20 40]  (in-place shuffle; original order gone)

m = mat.copy()
rng.shuffle(m)           # shuffles rows (axis=0)
print(m)
# [[ 8  9 10 11]   ← row 2 is now first
#  [ 0  1  2  3]
#  [ 4  5  6  7]]

rng.shuffle(m, axis=1)   # shuffles columns within each row
print(m)
# each row is an independent column permutation

##-------------------##
## rng.permutation() ##
##-------------------##
'''
rng.permutation() returns a NEW randomly permuted copy (does NOT modify in-place).

- If argument is an integer n, returns a permuted np.arange(n).
- If argument is an array, returns a copy with rows shuffled (axis=0).
- Use when you need the original array unchanged.
'''

print(rng.permutation(8))
# [2 7 5 0 1 3 6 4]  (random permutation of [0, 1, ..., 7])

print(rng.permutation(arr))
# [40 30 10 20 50]  (arr is unchanged)
print(arr)
# [10 20 30 40 50]  (original untouched)

print(rng.permutation(mat, axis=0))
# rows of mat in a new random order (column order preserved within each row)

##----------------##
## rng.permuted() ##
##----------------##
'''
rng.permuted() shuffles elements independently along a given axis.

Key distinction from shuffle/permutation:
  shuffle/permutation: treats entire rows (or columns) as atomic units → rows stay intact.
  permuted           : independently permutes elements within each row (or column).

- out=array: write result into an existing array (in-place operation).
- Returns a new array by default (unlike shuffle which is always in-place).
'''

m = mat.copy()

print(m)

# Shuffle each row independently (axis=1)
print(rng.permuted(m, axis=1))
# [[ 3  0  2  1]    ← elements within row 0 shuffled
#  [ 6  5  7  4]    ← elements within row 1 shuffled independently
#  [ 9  8 11 10]]   ← elements within row 2 shuffled independently

# Shuffle each column independently (axis=0)
print(rng.permuted(m, axis=0))
# each column's elements are shuffled independently

# Compare: permutation shuffles whole rows (columns stay paired)
print(rng.permutation(m))
# e.g. row 2 is now row 0, but all 4 values in row 2 are together


# =========================================================================================
# 4. Continuous distributions
# =========================================================================================

##---------------##
## rng.uniform() ##
##---------------##
'''
rng.uniform() draws uniform floats from [low, high).

rng.uniform(0, 1) is equivalent to rng.random().
Use rng.uniform() when you need a range other than [0, 1).
'''

print(rng.uniform())
# 0.6...  (default is [0, 1), equivalent to rng.random())

print(rng.uniform(-5, 5, size=4))
# [-1.4  3.2  0.7 -3.8]  (uniform on [-5, 5))

print(rng.uniform(low=[0, 10], high=[1, 20]))
# [0.52 14.7]  (vectorised bounds: first from [0,1), second from [10,20))

##-----------------------##
## rng.standard_normal() ##
##-----------------------##
'''
rng.standard_normal() draws samples from N(0, 1) — zero mean, unit variance.

Faster than rng.normal(0, 1) because it skips argument validation.
For non-standard normal, use rng.normal(loc, scale).
'''

print(rng.standard_normal())
# -0.234...  (single standard normal draw)

print(rng.standard_normal(5))
# [-0.27  1.23 -0.98  0.41 -1.55]

print(rng.standard_normal((2, 3)))
# [[-0.46  0.12  0.84]
#  [ 1.07 -0.24 -0.63]]

##--------------##
## rng.normal() ##
##--------------##
'''
rng.normal() draws samples from N(loc, scale²) — Gaussian distribution.

loc   : mean (μ).
scale : standard deviation (σ).  Must be > 0.

Applications: noise modelling, prior distributions, Monte Carlo integration.
'''

print(rng.normal())
# 0.48...  (default loc=0, scale=1 → same as standard_normal)

print(rng.normal(loc=5, scale=2, size=4))
# [6.2  3.8  5.7  2.1]  (mean ≈ 5, std ≈ 2)

# Vectorised: different mean for each sample
print(rng.normal(loc=[0, 10, 100], scale=1))
# [-0.3   9.8  99.7]

##----------------------------##
## rng.standard_exponential() ##
##----------------------------##
'''
rng.standard_exponential() draws from Exp(1): f(x) = exp(-x), x ≥ 0.

Mean = 1, variance = 1.
For Exp(λ), use rng.exponential(scale=1/λ).
'''

print(rng.standard_exponential(5))
# [0.23  1.87  0.05  2.41  0.63]  (all positive; mean ≈ 1)

##-------------------##
## rng.exponential() ##
##-------------------##
'''
rng.exponential() draws from Exp(scale): f(x) = (1/scale)·exp(-x/scale), x ≥ 0.

scale = 1/λ (mean of the distribution).
Applications: inter-arrival times (queuing), radioactive decay, survival analysis.
'''

print(rng.exponential(scale=2, size=5))
# [1.1  4.2  0.3  0.9  3.7]  (mean ≈ 2)

# Simulate Poisson process: inter-arrival times with rate λ=3 events/sec
lam = 3
interarrival = rng.exponential(scale=1/lam, size=10)
arrival_times = np.cumsum(interarrival)
print(arrival_times.round(3))
# cumulative arrival times for 10 events

##-------------##
## rng.gamma() ##
##-------------##
'''
rng.gamma() draws from Gamma(shape, scale).

PDF: f(x) ∝ x^(shape-1) · exp(-x/scale),  x > 0
shape (k): controls shape (k=1 → exponential; integer k → Erlang).
scale (θ): controls spread (= 1/rate).

Applications: waiting times for k events, Bayesian conjugate prior for Poisson rate.
'''

print(rng.gamma(shape=2, scale=1, size=5))
# [1.4  3.2  0.9  2.0  1.7]  (mean = shape*scale = 2)

print(rng.gamma(shape=1, scale=2, size=3))
# same distribution as Exp(scale=2)

##------------##
## rng.beta() ##
##------------##
'''
rng.beta() draws from Beta(a, b) on [0, 1].

a, b > 0 (shape parameters).
  a=b=1       : uniform distribution on [0, 1]
  a=b > 1     : bell-shaped, symmetric around 0.5
  a > b       : skewed toward 1
  a < b       : skewed toward 0

Applications: Bayesian prior for probabilities, proportions, A/B testing.
'''

print(rng.beta(a=2, b=5, size=4))
# [0.18  0.31  0.24  0.11]  (mean = a/(a+b) = 2/7 ≈ 0.29)

print(rng.beta(a=1, b=1, size=3))
# [0.72  0.14  0.93]  (uniform — equivalent to rng.random())

##-----------------##
## rng.chisquare() ##
##-----------------##
'''
rng.chisquare() draws from χ²(df) distribution.

χ²(df) is the sum of df squared standard normal variables: Σ Z_i² for Z_i ~ N(0,1).
Mean = df, variance = 2·df.

Applications: goodness-of-fit tests, confidence intervals for variance,
              test statistics in regression (df = degrees of freedom).
'''

print(rng.chisquare(df=3, size=5))
# [2.1  5.4  0.8  3.2  1.6]  (mean ≈ 3)

print(rng.chisquare(df=1, size=3))
# equivalent to rng.standard_normal(3)**2  (one squared normal)

##------------------##
## rng.standard_t() ##
##------------------##
'''
rng.standard_t() draws from Student's t distribution with given degrees of freedom.

t(df) resembles N(0,1) but with heavier tails; as df → ∞, t → N(0,1).
Mean = 0 (for df > 1), variance = df/(df-2) (for df > 2).

Applications: t-tests, Bayesian modelling with uncertain variance, robust regression.
'''

print(rng.standard_t(df=5, size=4))
# [-1.3   0.7  -0.2   2.1]  (heavier tails than normal)

print(rng.standard_t(df=100, size=3))
# ≈ standard normal (large df → tails shrink)

##---------##
## rng.f() ##
##---------##
'''
rng.f() draws from the F distribution with dfnum and dfden degrees of freedom.

F = (χ²_m / m) / (χ²_n / n)  where m=dfnum, n=dfden.
Always non-negative. Right-skewed, especially for small df.

Applications: F-test in ANOVA, comparing variances, regression model significance.
'''

print(rng.f(dfnum=5, dfden=20, size=4))
# [0.8  1.4  0.3  2.1]  (values > 1 suggest larger numerator variance)

##-----------------##
## rng.lognormal() ##
##-----------------##
'''
rng.lognormal() draws from LogNormal(mean, sigma) — always positive.

If Y ~ N(mean, sigma²), then X = exp(Y) ~ LogNormal(mean, sigma).
Mean of X = exp(mean + sigma²/2), always positive.

Applications: income/wealth distributions, stock prices, biological concentrations.
'''

print(rng.lognormal(mean=0, sigma=1, size=4))
# [1.3  0.4  2.7  0.9]  (always positive, right-skewed)

print(np.log(rng.lognormal(mean=2, sigma=0.5, size=1000)).mean().round(3))
# ≈ 2.0  (log of samples is approximately normal with mean=2)

##----------------##
## rng.logistic() ##
##----------------##
'''
rng.logistic() draws from the Logistic(loc, scale) distribution.

Similar to normal but with heavier tails; CDF is the logistic sigmoid function.
Used in logistic regression (link function), Gumbel extreme value theory.
'''

print(rng.logistic(loc=0, scale=1, size=4))
# [-1.7  0.3  2.1 -0.4]  (heavier tails than normal)

##---------------##
## rng.laplace() ##
##---------------##
'''
rng.laplace() draws from the Laplace(loc, scale) distribution — "double exponential".

f(x) = (1/2b)·exp(-|x-μ|/b)  where b=scale.
Heavier tails than Gaussian; maximum likelihood for Laplace → L1 (LASSO) regression.

Applications: sparse modelling, image processing, signal noise.
'''

print(rng.laplace(loc=0, scale=1, size=4))
# [-0.3   2.1  -1.4   0.1]

##------------------##
## rng.triangular() ##
##------------------##
'''
rng.triangular() draws from the Triangular(left, mode, right) distribution.

Bounded on [left, right] with peak probability at mode.
Useful for project management (PERT estimates) and simple bounded simulations.
'''

print(rng.triangular(left=0, mode=3, right=5, size=4))
# [2.7  1.4  3.1  2.9]  (bounded in [0, 5], peak near 3)

##------------##
## rng.wald() ##
##------------##
'''
rng.wald() draws from the Wald (Inverse Gaussian) distribution.

Parameters: mean and scale (lambda).
Always positive, right-skewed. Models first passage times in Brownian motion.
'''

print(rng.wald(mean=1, scale=3, size=4))
# [0.6  1.2  0.8  2.1]

##----------------##
## rng.rayleigh() ##
##----------------##
'''
rng.rayleigh() draws from the Rayleigh distribution.

If X, Y ~ N(0, σ²), then sqrt(X²+Y²) ~ Rayleigh(σ).
scale = σ. Mean = σ·√(π/2) ≈ 1.253·σ.

Applications: 2-D wind/wave speed magnitude, signal envelope, wireless propagation.
'''

print(rng.rayleigh(scale=1, size=4))
# [0.7  1.4  0.3  2.1]  (always positive)

##--------------##
## rng.pareto() ##
##--------------##
'''
rng.pareto() draws from the Pareto distribution with shape parameter a.

Pareto principle ("80-20 rule"): heavy power-law tail.
Note: NumPy uses the Lomax (shifted Pareto) form — add 1 to get standard Pareto.
'''

print(rng.pareto(a=2, size=4))
# [0.2  1.4  0.1  3.7]  (heavy right tail for small a)

# Standard Pareto (starts at x_min=1): add 1
print(1 + rng.pareto(a=3, size=4))
# [1.1  2.3  1.4  1.6]

##--------------##
## rng.gumbel() ##
##--------------##
'''
rng.gumbel() draws from the Gumbel (Type I Extreme Value) distribution.

Used to model the maximum (or minimum) of many independent samples.
Applications: floods, financial risk, material strength, climate extremes.
'''

print(rng.gumbel(loc=0, scale=1, size=4))
# [-0.3   2.7  -0.1   1.2]  (right-skewed)

##---------------##
## rng.weibull() ##
##---------------##
'''
rng.weibull() draws from the Weibull distribution with shape parameter a.

Note: NumPy returns unit-scale Weibull; multiply by scale for Weibull(a, scale).
  a < 1: decreasing hazard rate (early failures)
  a = 1: constant hazard rate (exponential distribution)
  a > 1: increasing hazard rate (wear-out failures)

Applications: reliability engineering, lifetime data, wind energy (turbine output).
'''

scale_w = 2.0
print(scale_w * rng.weibull(a=1.5, size=4))
# [1.3  0.7  2.8  1.6]  (always positive)

print(rng.weibull(a=1, size=3))
# equivalent to standard exponential (a=1 → exponential)

##----------------##
## rng.vonmises() ##
##----------------##
'''
rng.vonmises() draws from the von Mises (circular normal) distribution on [-π, π].

mu    : mean direction (radians).
kappa : concentration parameter (κ=0 → uniform on circle; κ→∞ → point mass at mu).

Applications: wind direction, protein backbone angles, signal processing on a circle.
'''

print(rng.vonmises(mu=0, kappa=4, size=5).round(3))
# [-0.123  0.452 -0.231  0.071  0.341]  (concentrated near 0; in radians)

print(rng.vonmises(mu=0, kappa=0, size=3).round(3))
# [-2.4  1.1  0.7]  (kappa=0 → uniform on [-π, π])


# =========================================================================================
# 5. Discrete distributions
# =========================================================================================

##----------------##
## rng.binomial() ##
##----------------##
'''
rng.binomial() draws from Binomial(n, p) — number of successes in n Bernoulli trials.

n : number of independent trials.
p : probability of success per trial (0 ≤ p ≤ 1).
Mean = n·p, variance = n·p·(1-p).

Applications: A/B test outcomes, defect counting, coin flips.
'''

print(rng.binomial(n=10, p=0.3, size=5))
# [3 2 4 3 2]  (values in [0, 10]; mean ≈ 3)

print(rng.binomial(n=1, p=0.5, size=8))
# [1 0 1 1 0 0 1 0]  (Bernoulli trials — fair coin flips)

# Simulate 1000 A/B tests: proportion of successes
results = rng.binomial(n=100, p=0.25, size=1000) / 100
print(results.mean().round(3), results.std().round(3))
# ≈ 0.250  0.043

##---------------##
## rng.poisson() ##
##---------------##
'''
rng.poisson() draws from Poisson(lam) — number of events in a fixed interval.

lam : expected number of events (λ ≥ 0).
Mean = variance = λ.

Applications: customer arrivals, server requests, photon counts, mutations per genome.
'''

print(rng.poisson(lam=3, size=6))
# [2 4 3 1 5 3]  (values ≥ 0; mean ≈ 3)

print(rng.poisson(lam=0.5, size=5))
# [0 1 0 0 1]  (rare events)

print(rng.poisson(lam=[1, 5, 20], size=(3, 3)))
# each column uses a different λ

##-----------------##
## rng.geometric() ##
##-----------------##
'''
rng.geometric() draws from Geometric(p) — number of trials until first success.

p : probability of success per trial.
Mean = 1/p, variance = (1-p)/p².

Applications: number of items tested before finding a defect; spam filter trials.
'''

print(rng.geometric(p=0.3, size=6))
# [3 1 5 1 2 4]  (always ≥ 1; mean ≈ 1/0.3 ≈ 3.3)

##----------------------##
## rng.hypergeometric() ##
##----------------------##
'''
rng.hypergeometric() draws from the Hypergeometric distribution.

Sampling WITHOUT replacement from a population:
  ngood   : number of "good" items in population.
  nbad    : number of "bad" items in population.
  nsample : sample size (≤ ngood + nbad).

Output: number of "good" items in the sample.
Applications: quality control, card drawing, clinical trials.
'''

# Population: 15 defective, 35 good; sample 10
print(rng.hypergeometric(ngood=35, nbad=15, nsample=10, size=5))
# [7 8 6 8 7]  (values in [0,10]; mean = 10*35/50 = 7)

##-------------------------##
## rng.negative_binomial() ##
##-------------------------##
'''
rng.negative_binomial() draws from the Negative Binomial distribution.

Number of failures before achieving n successes, each with probability p.
  n : number of successes required.
  p : probability of success per trial.
Mean = n·(1-p)/p, variance = n·(1-p)/p².

Applications: overdispersed count data (RNA-seq read counts, insurance claims).
'''

print(rng.negative_binomial(n=5, p=0.5, size=5))
# [4 7 3 6 5]  (mean = 5*(0.5)/0.5 = 5)

##-------------------##
## rng.multinomial() ##
##-------------------##
'''
rng.multinomial() draws from the Multinomial(n, pvals) distribution.

Generalizes binomial to k > 2 outcomes:
  n     : total number of trials.
  pvals : probability of each outcome (must sum to 1 or ≤ 1; last is 1-sum(rest)).
Output: counts for each category (sums to n).

Applications: dice rolls, topic models (LDA), election simulations.
'''

# 20 dice rolls; each face has probability 1/6
counts = rng.multinomial(n=20, pvals=[1/6]*6)
print(counts)
# [3 4 2 5 3 3]  (6 values, sum = 20)

# Batch: 5 independent multinomial samples
print(rng.multinomial(n=100, pvals=[0.2, 0.3, 0.5], size=5))
# [[21 29 50]
#  [19 32 49]
#  [22 28 50]
#  [20 31 49]
#  [18 30 52]]  (each row sums to 100)

##------------##
## rng.zipf() ##
##------------##
'''
rng.zipf() draws from the Zipf (zeta) distribution.

P(k) ∝ 1/k^a,  k = 1, 2, 3, ...  (a > 1 for finite mean)
a > 1 : valid distribution; smaller a → heavier tail.
a = 2 : classic Zipf's law (word frequency, city populations, internet traffic).

Applications: natural language word frequencies, web link counts, wealth distributions.
'''

print(rng.zipf(a=2, size=8))
# [1 3 1 1 2 1 8 1]  (most samples are 1; occasional large values)

print(rng.zipf(a=1.5, size=5))
# [1 12 2 1 4]  (heavier tail for smaller a)


# =========================================================================================
# 6. Multivariate distributions
# =========================================================================================

##---------------------------##
## rng.multivariate_normal() ##
##---------------------------##
'''
rng.multivariate_normal() draws from a multivariate Gaussian distribution.

mean  : 1-D array of length d — the mean vector.
cov   : (d, d) positive semidefinite covariance matrix.
size  : number of samples (each sample is a d-vector).

Applications: ML feature simulation, MCMC proposals, Gaussian process sampling,
              portfolio return modelling (mean-variance analysis).
'''

mean = np.array([0.0, 5.0])
cov  = np.array([[1.0, 0.8],
                 [0.8, 2.0]])   # positively correlated

samples = rng.multivariate_normal(mean, cov, size=5)
print(samples)
# [[-0.3   4.2]
#  [ 0.9   6.1]
#  [-1.2   3.7]
#  [ 0.4   5.3]
#  [ 1.1   6.5]]  (each row is a 2-D draw; x1≈0, x2≈5; positively correlated)

print(samples.mean(axis=0).round(2))
# ≈ [0. 5.]

print(np.cov(rng.multivariate_normal(mean, cov, size=10000), rowvar=False).round(2))
# [[1.  0.8]
#  [0.8 2. ]]  (empirical covariance ≈ true cov)

# 3-D uncorrelated Gaussian
mean3 = [0, 0, 0]
cov3  = np.diag([1., 4., 9.])   # variances 1, 4, 9 → stds 1, 2, 3

samples3 = rng.multivariate_normal(mean3, cov3, size=4)
print(samples3.round(2))
# [[-0.3   0.8  -2.1]
#  [ 0.7  -1.4   1.5]
#  [-1.1   2.3  -3.2]
#  [ 0.4  -0.7   0.9]]

##-----------------------------------##
## rng.multivariate_hypergeometric() ##
##-----------------------------------##
'''
rng.multivariate_hypergeometric() draws multivariate samples without replacement.

Generalizes hypergeometric to k categories:
  colors   : 1-D array giving the count of each category in the population.
  nsample  : total number of items to draw.

Output: counts for each category (sums to nsample).
Applications: multi-class sampling without replacement (deck of cards, multi-urn problems).
'''

# Bag contains 12 red, 8 blue, 5 green balls; draw 10 without replacement
colors = [12, 8, 5]   # 25 balls total

draw = rng.multivariate_hypergeometric(colors, nsample=10)
print(draw)
# [5 3 2]  (sums to 10; proportional to [12, 8, 5])

# 4 independent draws
print(rng.multivariate_hypergeometric(colors, nsample=10, size=4))
# [[5 3 2]
#  [6 2 2]
#  [4 4 2]
#  [6 3 1]]

##-----------------##
## rng.dirichlet() ##
##-----------------##
'''
rng.dirichlet() draws from the Dirichlet(alpha) distribution.

alpha : 1-D array of positive concentration parameters (length = k categories).
Output: 1-D arrays of length k that sum to 1 (samples from the probability simplex).

  Uniform: all alpha[i] equal → symmetric prior.
  Sparse : alpha[i] << 1  → samples concentrate near corners (mostly zeros).
  Dense  : alpha[i] >> 1  → samples are nearly uniform.

Applications: Bayesian prior over categorical probabilities, Latent Dirichlet Allocation (LDA),
              topic modelling, Dirichlet Process mixture models.
'''

# Symmetric Dirichlet (uniform prior over 4-category probabilities)
alpha_sym = np.array([1., 1., 1., 1.])
print(rng.dirichlet(alpha_sym))
# [0.21 0.38 0.14 0.27]  (sums to 1; symmetric around 0.25)

print(rng.dirichlet(alpha_sym, size=3))
# [[0.17 0.31 0.28 0.24]
#  [0.42 0.08 0.35 0.15]
#  [0.26 0.22 0.11 0.41]]  (3 independent samples)

# Concentrated: alpha >> 1 → samples near [0.25, 0.25, 0.25, 0.25]
alpha_conc = np.array([100., 100., 100., 100.])
print(rng.dirichlet(alpha_conc).round(3))
# [0.252 0.248 0.249 0.251]  (nearly uniform, little variance)

# Sparse: alpha << 1 → samples near simplex vertices (mostly zeros)
alpha_sparse = np.array([0.1, 0.1, 0.1, 0.1])
print(rng.dirichlet(alpha_sparse).round(4))
# [0.0012  0.9873  0.0001  0.0114]  (one category dominates)

# LDA prior: asymmetric alpha reflects known topic frequencies
alpha_lda = np.array([0.5, 2.0, 0.3])   # topic 2 expected to dominate
print(rng.dirichlet(alpha_lda, size=5).round(3))
# each row is a document's topic distribution; topic 2 (index 1) gets more weight


# =========================================================================================
# 7. Parallel generation
# =========================================================================================

##----------------------##
## SeedSequence.spawn() ##
##----------------------##
'''
SeedSequence.spawn(n) creates n independent child SeedSequences from a parent.

Each child produces a statistically independent stream — perfect for parallel workers.
Pattern: create parent seed → spawn n children → create one Generator per child.
The child streams are guaranteed to be independent even if the parent seed is known.

This is the RECOMMENDED pattern for reproducible parallel random number generation.
'''

parent_ss = SeedSequence(99)
child_seeds = parent_ss.spawn(4)   # spawn 4 independent child seeds

# Each worker gets its own independent Generator
worker_rngs = [Generator(PCG64(s)) for s in child_seeds]

for i, r in enumerate(worker_rngs):
    print(f"worker {i}: {r.random(3).round(4)}")
# worker 0: [0.6536 0.1173 0.5680]
# worker 1: [0.9756 0.2435 0.7102]
# worker 2: [0.3489 0.8901 0.4512]
# worker 3: [0.1237 0.6654 0.9081]  (all different, all reproducible)

# Hierarchical spawning: workers can further spawn their own children
sub_children = child_seeds[0].spawn(2)   # worker 0 spawns 2 sub-workers

##------------------------##
## bit_generator.jumped() ##
##------------------------##
'''
rng.bit_generator.jumped(n) advances the BitGenerator state by n * 2^128 steps.

Creates non-overlapping streams of length 2^128 — effectively infinite for any simulation.
Faster to set up than SeedSequence.spawn(), but tied to PCG64 / Philox.
SeedSequence.spawn() is generally preferred for its flexibility.

Note: jumped() is available on PCG64 and Philox (not MT19937 or SFC64).
'''

base_rng = Generator(PCG64(42))

# Create 3 streams by jumping ahead
stream_0 = Generator(base_rng.bit_generator)                    # original
stream_1 = Generator(base_rng.bit_generator.jumped(1))          # jumped once
stream_2 = Generator(base_rng.bit_generator.jumped(2))          # jumped twice

print(stream_0.random(3).round(4))   # [0.7740 0.4359 0.0259]
print(stream_1.random(3).round(4))   # [0.4132 0.8711 0.5986]  (non-overlapping)
print(stream_2.random(3).round(4))   # [0.2037 0.6217 0.3071]

# Verify that the same base seed with jump=0 gives the same result
base_check = Generator(PCG64(42))
print(base_check.random(3).round(4))
# [0.7740 0.4359 0.0259]  — matches stream_0


# =========================================================================================
# 8. scipy.stats — distributions with .rvs()
# =========================================================================================

##--------------------------##
## scipy.stats.<dist>.rvs() ##
##--------------------------##
'''
scipy.stats has 100+ parametric distributions; every one supports .rvs() for sampling.

Usage pattern: dist = scipy.stats.<name>(params); samples = dist.rvs(size=n)
Or in one call: scipy.stats.<name>.rvs(params, size=n)

Advantages over numpy.random for sampling:
  - Distributions not in numpy.random (t-location-scale, lomax, truncnorm, etc.)
  - Consistent API: .rvs(), .pdf(), .cdf(), .ppf(), .stats() all on the same object.
  - random_state accepts np.random.Generator for reproducibility.
  - Frozen distributions: fix params once, call rvs(size) many times.

Performance note: for distributions that exist in both (norm, gamma, beta, etc.),
  numpy.random is significantly faster. Use scipy.stats when numpy lacks the distribution.
'''

# Frozen distribution: fix parameters, reuse
norm_dist   = spstats.norm(loc=0, scale=1)
gamma_dist  = spstats.gamma(a=2, scale=1)
t_dist      = spstats.t(df=5)
beta_dist   = spstats.beta(a=2, b=5)

print(norm_dist.rvs(size=4, random_state=rng))
# [-0.23  1.07 -0.52  0.81]  (standard normal)

print(gamma_dist.rvs(size=4, random_state=rng))
# [1.4  3.2  0.7  2.1]  (Gamma(2,1))

print(t_dist.rvs(size=4, random_state=rng))
# [-0.9  0.4  1.7 -1.2]  (Student's t with df=5)

# ── scipy-only distributions (not in numpy.random) ─────────────────────────────────────────────

# Truncated normal: normal distribution clipped to [a, b] in units of sigma
trunc_norm = spstats.truncnorm(a=-2, b=2, loc=0, scale=1)   # clipped at ±2σ
print(trunc_norm.rvs(size=5, random_state=rng).round(3))
# [-1.21  0.43  1.78 -0.84  0.07]  (all in [-2, 2])

# Log-logistic (Fisk) distribution
loglogistic = spstats.fisk(c=2)
print(loglogistic.rvs(size=4, random_state=rng).round(3))
# [0.83  2.41  1.12  0.47]

# Lomax (Pareto type II)
lomax = spstats.lomax(c=2)
print(lomax.rvs(size=4, random_state=rng).round(3))
# [0.21  1.83  0.47  0.09]

# Discrete: negative binomial via scipy (different parameterisation from numpy)
nbinom = spstats.nbinom(n=10, p=0.4)
print(nbinom.rvs(size=5, random_state=rng))
# [12  8 14  9 11]

# Levy-stable distribution — not in numpy at all
stable = spstats.levy_stable(alpha=1.5, beta=0)
print(stable.rvs(size=4, random_state=rng).round(3))
# [ 0.7  3.2 -1.1  0.4]  (heavy tails)

# All distributions share the same inspection API
print(norm_dist.mean(), norm_dist.std())                    # 0.0  1.0
print(norm_dist.ppf(0.975).round(4))                        # 1.96  (z-score for 95% CI)
print(norm_dist.cdf(1.96).round(4))                         # 0.975
print(norm_dist.interval(0.95))                             # (-1.96, 1.96)


# =========================================================================================
# 9. scipy.stats.qmc — Quasi-Monte Carlo
# =========================================================================================

##-------------##
## qmc.Sobol() ##
##-------------##
'''
qmc.Sobol() generates a Sobol' low-discrepancy sequence in [0,1]^d.

QMC vs Monte Carlo:
  Monte Carlo (numpy.random.random): independent uniform points → clusters and gaps.
  Quasi-Monte Carlo (Sobol):         deterministic low-discrepancy sequence → fills space evenly.
  Convergence: MC error ~ O(1/√n); QMC error ~ O((log n)^d / n) — faster in low-medium dimensions.

Key parameters:
  d           : number of dimensions.
  seed        : for scrambling (randomized Sobol' — always use scrambling).
  scramble    : True (default) — scrambled Sobol' has better uniformity and provable error bounds.

IMPORTANT: n must be a power of 2 for Sobol'; other sizes give suboptimal sequences.
'''

engine = qmc.Sobol(d=2, scramble=True, seed=42)
sample = engine.random(n=16)   # 16 = 2^4 points in [0,1]^2

print(sample.shape)
# (16, 2)

print(sample[:5].round(4))
# [[0.6536 0.3197]
#  [0.1536 0.8197]
#  [0.9036 0.5697]
#  [0.4036 0.0697]
#  [0.7786 0.6947]]  (evenly fills [0,1]^2)

print(round(qmc.discrepancy(sample), 6))
# ~0.00...  (small discrepancy = good uniformity; exact value varies with scramble seed)

# Reset engine and generate a new batch
engine.reset()
batch2 = engine.random(n=16)
print(np.allclose(sample, batch2))
# False  (scrambled → different batch; but same after reset+same seed only on next random call)

# Fast-forward: skip n points without generating them (preserves sequence properties)
engine.reset()
engine.fast_forward(8)   # skip first 8 points
next_8 = engine.random(n=8)
print(next_8.shape)
# (8, 2)  — same as sample[8:] (up to scrambling)

##--------------##
## qmc.Halton() ##
##--------------##
'''
qmc.Halton() generates a Halton low-discrepancy sequence in [0,1]^d.

Differences from Sobol':
  - Works for any n (not just powers of 2) → more flexible.
  - Slower asymptotic convergence than Sobol'.
  - Scrambled by default — always leave scramble=True.
  - Earlier dimensions have much better uniformity; avoid d > 20 in practice.
'''

engine_h = qmc.Halton(d=3, scramble=True, seed=0)
sample_h = engine_h.random(n=100)

print(sample_h.shape)
# (100, 3)

print(sample_h[:4].round(4))
# [[0.  0.  0.]
#  [0.5 0.  0.333]
#  [0.25 0.5 0.667]
#  [0.75 0.25 0.111]]  (low discrepancy structure; scrambled values differ)

print(round(qmc.discrepancy(sample_h), 4))
# small value (well-distributed)

##----------------------##
## qmc.LatinHypercube() ##
##----------------------##
'''
qmc.LatinHypercube() (LHS) samples one point from each d-dimensional stratum.

Divides [0,1]^d into n equal 1-D strata along each axis; exactly one sample per stratum.
Properties:
  - Guarantees marginal uniformity along every axis (unlike plain random sampling).
  - Better than random for moderate n; less regular than Sobol'/Halton.
  - Easy to add more points (unlike Sobol' which requires power-of-2 sizes).
  - scramble=True (default): randomize within each stratum.

Applications: design of experiments, sensitivity analysis, surrogate modelling.
'''

engine_lhs = qmc.LatinHypercube(d=4, seed=42)
sample_lhs = engine_lhs.random(n=20)

print(sample_lhs.shape)
# (20, 4)

print(sample_lhs[:4].round(4))
# [[0.  0.  0.  0. ]  (values near 0, 0.05, 0.1, ... each stratum)
#  [0.05 0.05 0.05 0.05]
#  ...  (exact values depend on scramble)

# Confirm: each axis is uniformly stratified into [0/20, 1/20), [1/20, 2/20), ...
sorted_col = np.sort(sample_lhs[:, 0])
print(sorted_col.round(3))
# [0.01  0.06  0.11  0.17  0.22 ... 0.96]  — one value per 1/20-width stratum

##-------------##
## qmc.scale() ##
##-------------##
'''
qmc.scale() transforms a QMC sample from [0,1]^d to arbitrary bounds [l, u]^d.

Arguments:
  sample   : array of shape (n, d) with values in [0, 1].
  l_bounds : lower bounds per dimension (length d).
  u_bounds : upper bounds per dimension (length d).
  reverse  : if True, maps [l, u] → [0, 1] (inverse scaling).
'''

engine_s = qmc.Sobol(d=2, scramble=True, seed=5)
unit_sample = engine_s.random(n=8)

l_bounds = [-5, 100]
u_bounds  = [ 5, 200]

scaled = qmc.scale(unit_sample, l_bounds, u_bounds)
print(scaled[:4].round(2))
# [[-1.2  150.3]
#  [ 4.3  174.8]
#  [ 0.7  125.1]
#  [-3.1  162.4]]  (x1 in [-5, 5], x2 in [100, 200])

# Reverse scaling: map back to [0, 1]
unit_recovered = qmc.scale(scaled, l_bounds, u_bounds, reverse=True)
print(np.allclose(unit_recovered, unit_sample))
# True

##-------------------##
## qmc.discrepancy() ##
##-------------------##
'''
qmc.discrepancy() measures how uniformly a sample covers [0,1]^d.

Lower discrepancy = better uniformity = more accurate QMC integration.
C2 (centered L2) discrepancy is the default and most commonly used.

Useful for comparing different samplers or verifying a sample's quality.
'''

n_pts = 64

# Random MC vs QMC comparison
mc_sample  = np.random.default_rng(0).random((n_pts, 2))
sobol_eng  = qmc.Sobol(d=2, scramble=True, seed=0)
qmc_sample = sobol_eng.random(n_pts)
lhs_eng    = qmc.LatinHypercube(d=2, seed=0)
lhs_sample = lhs_eng.random(n_pts)

print(f"MC  discrepancy: {qmc.discrepancy(mc_sample):.6f}")
# MC  discrepancy: 0.002... (higher — random gaps/clusters)

print(f"LHS discrepancy: {qmc.discrepancy(lhs_sample):.6f}")
# LHS discrepancy: 0.001... (better — stratified)

print(f"Sobol discrepancy: {qmc.discrepancy(qmc_sample):.6f}")
# Sobol discrepancy: 0.0003... (best — low-discrepancy by design)

# MC integration comparison: estimate ∫_0^1 ∫_0^1 sin(πx)·sin(πy) dx dy = (2/π)² ≈ 0.4053
def f(pts): return np.sin(np.pi * pts[:, 0]) * np.sin(np.pi * pts[:, 1])

true_val = (2 / np.pi)**2
mc_est   = f(mc_sample).mean()
qmc_est  = f(qmc_sample).mean()
lhs_est  = f(lhs_sample).mean()

print(f"True:  {true_val:.6f}")
print(f"MC:    {mc_est:.6f}  (error {abs(mc_est-true_val):.2e})")
print(f"LHS:   {lhs_est:.6f}  (error {abs(lhs_est-true_val):.2e})")
print(f"Sobol: {qmc_est:.6f}  (error {abs(qmc_est-true_val):.2e})")
# Sobol error is typically 10–100× smaller than MC for the same n


# =========================================================================================
# 10. Legacy API
# =========================================================================================

'''
numpy.random module-level functions are a LEGACY interface backed by a single global
RandomState using the older MT19937 algorithm. They still work, but have drawbacks:
  - Global state: any call anywhere in the program advances the same shared state.
  - Not thread-safe.
  - MT19937 is slower and statistically weaker than PCG64 (used by default_rng).
  - np.random.seed() does not accept large integers or SeedSequence.

Use np.random.seed() to make results reproducible. Note: same seed always produces
the same SEQUENCE — calling the same function again gives the NEXT value in that sequence.
For new code, prefer rng = np.random.default_rng(seed) (see section 1).
'''

np.random.seed(42)   # seed the global RandomState for reproducibility

##---------------------##
## np.random.rand()    ##
## np.random.random()  ##
##---------------------##
'''
np.random.rand(*shape)   : uniform floats in [0, 1); shape passed as positional args.
np.random.random(size)   : identical output; shape passed as size keyword or tuple.
np.random.random_sample(): alias for random().
np.random.sample()       : another alias.
'''

print(np.random.rand(4))
# [0.3745 0.9507 0.7320 0.5987]

print(np.random.rand(2, 3))
# [[0.1560 0.1560 0.0581]
#  [0.8662 0.7081 0.0206]]

print(np.random.random(4))
# [0.9699 0.8324 0.2123 0.1818]  (same distribution, size keyword)

##-----------------------------##
## np.random.randn()           ##
## np.random.standard_normal() ##
##-----------------------------##
'''
np.random.randn(*shape)          : N(0,1) samples; shape as positional args.
np.random.standard_normal(size)  : identical; shape as size keyword or tuple.
'''

print(np.random.randn(4))
# [ 0.4106  0.1440  1.4543  0.7610]

print(np.random.randn(2, 3))
# [[ 0.1218  0.4439  0.3337]
#  [ 1.4940 -0.2052  0.3131]]

print(np.random.standard_normal(4))
# [-0.8541 -2.5530  0.6536  0.8644]

##---------------------##
## np.random.randint() ##
##---------------------##
'''
np.random.randint(low, high, size) : uniform integers in [low, high)  (high is exclusive).
np.random.random_integers(low, high, size) : deprecated; [low, high] inclusive — avoid.
'''

print(np.random.randint(0, 10, size=6))
# [3 7 2 4 5 1]

print(np.random.randint(1, 7, size=(2, 3)))   # simulating 2×3 dice rolls
# [[4 3 6]
#  [2 5 1]]

##--------------------##
## np.random.choice() ##
##--------------------##
'''np.random.choice(a, size, replace, p) : same signature as rng.choice().'''

print(np.random.choice([10, 20, 30, 40, 50], size=3))
# [30 10 50]  (with replacement by default)

print(np.random.choice([10, 20, 30, 40, 50], size=3, replace=False))
# [40 20 10]  (without replacement)

print(np.random.choice(5, size=4))
# [2 0 3 1]  (integer arg → samples from range(5))

##------------------------##
## np.random.shuffle()    ##
## np.random.permutation()##
##------------------------##
'''
np.random.shuffle(a)    : in-place shuffle; returns None. Same as rng.shuffle().
np.random.permutation(a): returns a new shuffled copy. Same as rng.permutation().
'''

a = np.arange(8)
np.random.shuffle(a)
print(a)
# [5 0 3 1 7 4 6 2]  (a is modified in-place)

print(np.random.permutation(8))
# [2 5 6 0 3 7 1 4]  (new array; original unchanged)

print(np.random.permutation([10, 20, 30, 40]))
# [30 40 10 20]

##--------------------##
## np.random.normal() ##
##--------------------##
'''np.random.normal(loc, scale, size) : Gaussian N(loc, scale²). Same as rng.normal().'''

print(np.random.normal(loc=0, scale=1, size=4).round(3))
# [-1.136  0.234 -1.234 -0.535]

print(np.random.normal(loc=5, scale=2, size=4).round(3))
# [4.232  7.181  3.907  5.474]

##---------------------##
## np.random.uniform() ##
##---------------------##
'''np.random.uniform(low, high, size) : uniform floats on [low, high). Same as rng.uniform().'''

print(np.random.uniform(0, 10, size=4).round(3))
# [6.318 7.152 0.202 3.023]

print(np.random.uniform(-1, 1, size=(2, 3)).round(3))
# [[-0.601  0.493 -0.143]
#  [ 0.313 -0.854  0.627]]

##-------------------------##
## np.random.exponential() ##
##-------------------------##
'''np.random.exponential(scale, size) : Exp(scale). Same as rng.exponential().'''

print(np.random.exponential(scale=2, size=5).round(3))
# [0.716 1.447 3.312 1.143 0.271]

##-----------------------##
## np.random.gamma()     ##
## np.random.beta()      ##
## np.random.chisquare() ##
##-----------------------##
'''
All continuous distributions have the same signature as their rng counterparts.
np.random.gamma(shape, scale, size)
np.random.beta(a, b, size)
np.random.chisquare(df, size)
np.random.lognormal(mean, sigma, size)
np.random.logistic(loc, scale, size)
np.random.laplace(loc, scale, size)
np.random.pareto(a, size)
np.random.weibull(a, size)
np.random.gumbel(loc, scale, size)
np.random.rayleigh(scale, size)
np.random.vonmises(mu, kappa, size)
np.random.wald(mean, scale, size)
np.random.power(a, size)
np.random.f(dfnum, dfden, size)
np.random.standard_t(df, size)
np.random.triangular(left, mode, right, size)
'''

print(np.random.gamma(shape=2, scale=1, size=4).round(3))
# [1.271 0.844 2.312 0.537]

print(np.random.beta(a=2, b=5, size=4).round(3))
# [0.274 0.193 0.421 0.138]

print(np.random.chisquare(df=3, size=4).round(3))
# [3.142 1.876 2.543 5.201]

##---------------------##
## np.random.poisson() ##
##---------------------##
'''np.random.poisson(lam, size) : Poisson(lam). Same as rng.poisson().'''

print(np.random.poisson(lam=3, size=6))
# [3 4 2 5 3 1]

print(np.random.poisson(lam=[1, 5, 20]))
# [0 6 18]  (vectorised λ)

##----------------------##
## np.random.binomial() ##
##----------------------##
'''np.random.binomial(n, p, size) : Binomial(n, p). Same as rng.binomial().'''

print(np.random.binomial(n=10, p=0.3, size=5))
# [2 3 4 2 3]

##---------------------------------##
## np.random.multinomial()         ##
## np.random.multivariate_normal() ##
##---------------------------------##
'''
np.random.multinomial(n, pvals, size)              : same as rng.multinomial().
np.random.multivariate_normal(mean, cov, size)     : same as rng.multivariate_normal().
np.random.dirichlet(alpha, size)                   : same as rng.dirichlet().
np.random.hypergeometric(ngood, nbad, nsample, size): same as rng.hypergeometric().
np.random.negative_binomial(n, p, size)            : same as rng.negative_binomial().
np.random.geometric(p, size)                       : same as rng.geometric().
np.random.zipf(a, size)                            : same as rng.zipf().
'''

print(np.random.multinomial(n=20, pvals=[1/6]*6))
# [4 2 3 5 3 3]  (sums to 20)

mean = [0., 1.]
cov  = [[1., 0.5], [0.5, 2.]]
print(np.random.multivariate_normal(mean, cov, size=3).round(3))
# [[-0.274  1.532]
#  [ 1.123  0.847]
#  [-0.891  0.214]]

print(np.random.dirichlet([1., 1., 1., 1.]).round(3))
# [0.214 0.381 0.147 0.258]  (sums to 1)

##-------------------------##
## np.random.RandomState() ##
##-------------------------##
'''
np.random.RandomState is the legacy class underlying all module-level functions above.
It uses MT19937 and can be instantiated directly to avoid touching the global state,
while keeping the old API. Treat it as a scoped version of the legacy functions.
'''

rs = np.random.RandomState(42)     # independent from the global state
print(rs.randn(4).round(3))
# [ 0.497 -0.138  0.648  1.524]

print(rs.randint(0, 10, size=5))
# [4 3 7 2 9]

print(rs.random())
# 0.374...  (same sequence as np.random.seed(42) + np.random.random())
