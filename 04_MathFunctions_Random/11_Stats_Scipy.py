'''
scipy.stats  —  Statistical Functions
=======================================

One of SciPy's largest modules. Organised into these areas:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART A — CONTINUOUS DISTRIBUTIONS  (rv_continuous API)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1.  rv_continuous API        : pdf/cdf/sf/ppf/isf/rvs/stats/fit/expect/interval
 2.  norm                     : Normal / Gaussian
 3.  t                        : Student's t
 4.  chi2                     : Chi-squared
 5.  f                        : F-distribution
 6.  expon                    : Exponential
 7.  gamma / erlang           : Gamma family
 8.  beta                     : Beta
 9.  lognorm                  : Log-normal
10.  uniform                  : Uniform
11.  weibull_min / weibull_max: Weibull
12.  pareto / genpareto       : Pareto / Generalised Pareto
13.  cauchy                   : Cauchy
14.  laplace                  : Laplace / Double Exponential
15.  logistic                 : Logistic
16.  gumbel_r / gumbel_l / genextreme : Extreme value
17.  skewnorm                 : Skew-normal
18.  truncnorm / truncexpon   : Truncated distributions
19.  loguniform               : Log-uniform
20.  rv_histogram             : Empirical distribution from histogram

PART B — DISCRETE DISTRIBUTIONS  (rv_discrete API)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
21.  rv_discrete API          : pmf/cdf/sf/ppf/rvs/stats
22.  binom                    : Binomial
23.  poisson                  : Poisson
24.  geom                     : Geometric
25.  hypergeom                : Hypergeometric
26.  nbinom                   : Negative Binomial
27.  bernoulli                : Bernoulli
28.  randint                  : Discrete Uniform
29.  zipf / zipfian           : Zipf / Zipfian (power law)

PART C — MULTIVARIATE DISTRIBUTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
30.  multivariate_normal      : Multivariate Gaussian
31.  dirichlet                : Dirichlet
32.  multinomial              : Multinomial
33.  wishart / invwishart     : Wishart / Inverse Wishart
34.  multivariate_t           : Multivariate t

PART D — SUMMARY & DESCRIPTIVE STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
35.  describe                 : n, min, max, mean, variance, skewness, kurtosis
36.  gmean / hmean / pmean    : geometric, harmonic, power mean
37.  skew / kurtosis          : higher-order moments
38.  mode / trim_mean / tmean / tsem : robust location measures
39.  sem / iqr / variation    : spread measures
40.  moment                   : raw/central moments of any order

PART E — FREQUENCY STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
41.  cumfreq / relfreq        : cumulative and relative frequency
42.  percentileofscore        : percentile rank of a score
43.  scoreatpercentile        : score at a given percentile
44.  rankdata / tiecorrect    : rank transform

PART F — CORRELATION & ASSOCIATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
45.  pearsonr                 : Pearson r + p-value
46.  spearmanr                : Spearman ρ
47.  kendalltau               : Kendall τ (a, b, c variants)
48.  pointbiserialr           : Point-biserial r
49.  somersd                  : Somers' D
50.  chi2_contingency         : χ² test + Cramér's V

PART G — STATISTICAL TESTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  G1  One-sample tests
51.  ttest_1samp              : one-sample t-test
52.  kstest / ks_1samp        : Kolmogorov-Smirnov vs theoretical distribution
53.  shapiro                  : Shapiro-Wilk normality test
54.  normaltest               : D'Agostino + Pearson omnibus normality test
55.  jarque_bera              : Jarque-Bera test
56.  chisquare                : one-way chi-squared goodness of fit

  G2  Two-sample tests
57.  ttest_ind               : independent-samples t-test (Welch & equal-var)
58.  ttest_rel               : paired t-test
59.  mannwhitneyu            : Mann-Whitney U (non-parametric t_ind)
60.  wilcoxon                : Wilcoxon signed-rank (non-parametric t_rel)
61.  ks_2samp                : two-sample Kolmogorov-Smirnov
62.  epps_singleton_2samp    : Epps-Singleton two-sample test
63.  cramervonmises_2samp    : Cramér-von Mises two-sample test
64.  ranksums                : Wilcoxon rank-sum (alias for large-sample MWU)
65.  brunnermunzel           : Brunner-Munzel test

  G3  k-sample / ANOVA tests
66.  f_oneway                : one-way ANOVA
67.  kruskal                 : Kruskal-Wallis H (non-parametric ANOVA)
68.  alexandergovern         : Alexander-Govern (heteroscedastic ANOVA)
69.  friedmanchisquare       : Friedman test (non-parametric repeated-measures)
70.  median_test             : Mood's median test
71.  levene / bartlett / fligner : variance homogeneity tests

  G4  Association / contingency tests
72.  chi2_contingency        : chi-squared test of independence
73.  fisher_exact            : Fisher's exact test (2×2)
74.  barnard_exact / boschloo_exact : unconditional exact tests

  G5  Post-hoc & multiple comparisons
75.  tukey_hsd               : Tukey HSD post-hoc
76.  dunnett                 : Dunnett's test vs control

PART H — DISTRIBUTION FITTING & KDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
77.  dist.fit()              : MLE parameter fitting
78.  fit()                   : new unified fit() function (SciPy ≥ 1.9)
79.  gaussian_kde            : kernel density estimation
80.  monte_carlo_test        : permutation/bootstrap p-value

PART I — CONFIDENCE INTERVALS & RESAMPLING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
81.  bootstrap               : bootstrap confidence intervals (BCa / percentile)
82.  permutation_test        : exact or Monte Carlo permutation test
83.  dist.interval()         : equal-tailed credible / confidence interval
84.  bayes_mvs              : Bayesian mean/var/std credible intervals

PART J — QUASI-MONTE CARLO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
85.  qmc.Halton              : Halton low-discrepancy sequence
86.  qmc.Sobol               : Sobol' sequence
87.  qmc.LatinHypercube      : Latin hypercube sampling
88.  qmc.discrepancy         : L2-star discrepancy
89.  qmc.scale               : scale QMC samples to a [l, u] box
'''

import numpy as np
import scipy.stats as stats
from scipy.stats import qmc

rng = np.random.default_rng(42)

# ── Shared test data ──────────────────────────────────────────────────────────
N = 100
x_norm   = rng.normal(loc=5.0, scale=2.0, size=N)   # normal sample, μ=5, σ=2
x_exp    = rng.exponential(scale=2.0, size=N)        # exponential sample
x_pos    = np.abs(rng.normal(3, 1, N)) + 0.1        # positive reals


# =========================================================================================
#═════════════════════════════  PART A — CONTINUOUS DISTRIBUTIONS  ═══════════════════════════════#
# =========================================================================================

##-------------------##
## rv_continuous API ##
##-------------------##
'''
Every continuous distribution in scipy.stats is an instance (or frozen instance)
of rv_continuous. They all share the same method interface:

  dist = stats.norm           # unfrozen: pass params at every call
  d    = stats.norm(loc=5, scale=2)  # frozen: params baked in

Core methods (unfrozen: pass loc/scale/shape; frozen: no extra args needed):
  .pdf(x)          : probability density function f(x)
  .logpdf(x)       : log PDF  (numerically stable)
  .cdf(x)          : cumulative distribution function P(X ≤ x)
  .logcdf(x)       : log CDF
  .sf(x)           : survival function  1 - CDF(x) = P(X > x)
  .logsf(x)        : log SF  (accurate in far tails)
  .ppf(q)          : percent-point function (quantile / inverse CDF)
  .isf(q)          : inverse SF: x such that SF(x) = q
  .rvs(size, random_state) : random variates
  .stats(moments)  : mean ('m'), variance ('v'), skewness ('s'), kurtosis ('k')
  .mean() / .var() / .std() / .median()
  .moment(n)       : n-th non-central moment
  .entropy()       : differential entropy h = -∫ f log f dx
  .fit(data)       : MLE parameter estimation
  .fit_loc_scale(data, *args) : fit loc/scale with fixed shape params
  .expect(func)    : E[func(X)] = ∫ func(x) f(x) dx
  .interval(confidence) : equal-tailed interval [a, b] containing fraction p

  loc   : shifts the distribution (adds a constant to X)
  scale : scales the distribution (multiplies X)
  shape : distribution-specific shape parameters (e.g. df for t, a,b for beta)
'''

# Unfrozen vs frozen usage
print("=== rv_continuous API ===")
p_unfrozen = stats.norm.pdf(1.0, loc=0, scale=1)        # N(0,1) pdf at x=1
p_frozen   = stats.norm(loc=0, scale=1).pdf(1.0)        # same, frozen
print(f"pdf(1|N(0,1)) unfrozen={p_unfrozen:.6f}  frozen={p_frozen:.6f}")   # same
# pdf(1|N(0,1)) unfrozen=0.241971  frozen=0.241971

d_norm = stats.norm(loc=0, scale=1)   # frozen standard normal — used below
print(f"CDF(1.96) = {d_norm.cdf(1.96):.4f}")    # 0.9750
print(f"PPF(0.975)= {d_norm.ppf(0.975):.4f}")   # 1.9600  (z* for 95% CI)
print(f"SF(1.96)  = {d_norm.sf(1.96):.4f}")     # 0.0250
print(f"ISF(0.025)= {d_norm.isf(0.025):.4f}")   # 1.9600  (= ppf(0.975))

mn, vr, sk, ku = d_norm.stats(moments='mvsk')
print(f"N(0,1) mean={mn}, var={vr}, skew={sk}, kurt={ku}")
# N(0,1) mean=0.0, var=1.0, skew=0.0, kurt=0.0

print(f"Entropy N(0,1) = {d_norm.entropy():.4f}")   # 0.5*log(2πe) ≈ 1.4189
print(f"E[X²] N(0,1)   = {d_norm.expect(lambda x: x**2):.4f}")   # = var = 1.0

ci = d_norm.interval(0.95)
print(f"95% interval N(0,1): [{ci[0]:.4f}, {ci[1]:.4f}]")   # [-1.96, 1.96]

samp = d_norm.rvs(size=5, random_state=0)
print(f"5 samples: {samp.round(4)}")

##------##
## norm ##
##------##
'''
stats.norm(loc=0, scale=1)
  Normal (Gaussian) distribution.  μ = loc,  σ = scale.

  PDF: f(x) = exp(-x²/2) / sqrt(2π)          for x ∈ ℝ
  Mean=loc, Var=scale², Skew=0, ExKurt=0.

  Key uses: CLT approximation, z-tests, linear regression residuals,
            Bayesian conjugate prior for known-variance Gaussian likelihood.
'''
print("\n=== norm ===")
d = stats.norm(loc=5, scale=2)
print(f"pdf(5)={d.pdf(5):.4f}  cdf(7)={d.cdf(7):.4f}")   # peak, ~0.841
print(f"ppf(0.90)={d.ppf(0.90):.4f}")   # 5 + 2*1.2816 = 7.563
print(f"rvs mean≈{d.rvs(10000, random_state=0).mean():.3f}")   # ≈ 5.0

##---##
## t ##
##---##
'''
stats.t(df, loc=0, scale=1)
  Student's t-distribution.  df = degrees of freedom.

  PDF: f(x) ∝ (1 + x²/df)^(-(df+1)/2)        for x ∈ ℝ
  Mean=0 (df>1), Var=df/(df-2) (df>2).
  Heavy tails; approaches N(0,1) as df→∞.

  Key uses: t-tests, small-sample inference, robust regression, Bayesian
            analysis with unknown variance.
'''
print("\n=== t ===")
for df in [1, 5, 30, 1000]:
    d_t = stats.t(df)
    tail = d_t.sf(1.96)
    print(f"  df={df:4d}  P(T>1.96)={tail:.4f}  (N(0,1): 0.0250)")
# As df increases, converges to normal

# Critical values: t* for two-sided 95% CI
for df in [5, 10, 20, 30, 120]:
    t_star = stats.t.ppf(0.975, df)
    print(f"  df={df:3d}  t*(0.975)={t_star:.4f}")
  # df=   1  P(T>1.96)=0.1502  (N(0,1): 0.0250)
  # df=   5  P(T>1.96)=0.0536  (N(0,1): 0.0250)
  # df=  30  P(T>1.96)=0.0297  (N(0,1): 0.0250)
  # df=1000  P(T>1.96)=0.0251  (N(0,1): 0.0250)
  # df=  5  t*(0.975)=2.5706
  # df= 10  t*(0.975)=2.2281
  # df= 20  t*(0.975)=2.0860
  # df= 30  t*(0.975)=2.0423
  # df=120  t*(0.975)=1.9799

##------##
## chi2 ##
##------##
'''
stats.chi2(df, loc=0, scale=1)
  Chi-squared distribution.  df = degrees of freedom.

  If Z_1...Z_k ~ N(0,1) iid then X = ΣZ_i² ~ χ²(k).
  PDF: f(x) = x^(k/2-1)*exp(-x/2) / (2^(k/2)*Γ(k/2))  for x ≥ 0
  Mean=df, Var=2*df.

  Key uses: goodness-of-fit tests, variance inference, likelihood ratio tests.
'''
print("\n=== chi2 ===")
df_chi = 5
d_chi  = stats.chi2(df_chi)
print(f"χ²(5) mean={d_chi.mean():.1f}, var={d_chi.var():.1f}")   # χ²(5) mean=5.0, var=10.0
print(f"Critical value χ²(5, 0.95) = {d_chi.ppf(0.95):.4f}")     # 11.0705
print(f"P(X > 11.07) = {d_chi.sf(11.0705):.4f}")                  # ≈ 0.05

# Chi2 as sum of squared normals
z_vals = rng.standard_normal((10000, df_chi))
chi2_samples = (z_vals**2).sum(axis=1)
print(f"Simulated χ²(5) mean={chi2_samples.mean():.3f} (expect 5)") # Simulated χ²(5) mean=5.029 (expect 5)

##---##
## f ##
##---##
'''
stats.f(dfn, dfd, loc=0, scale=1)
  F-distribution.  dfn=numerator df, dfd=denominator df.

  If X~χ²(m), Y~χ²(n) independent, then (X/m)/(Y/n) ~ F(m,n).
  Mean=dfd/(dfd-2) for dfd>2.

  Key uses: ANOVA F-test, regression significance, comparing variances.
'''
print("\n=== F ===")
d_f = stats.f(dfn=3, dfd=20)
print(f"F(3,20) mean={d_f.mean():.4f}")           # 20/18 ≈ 1.111
print(f"F* for α=0.05: {d_f.ppf(0.95):.4f}")      # 3.0984
print(f"P(F > 3.10) = {d_f.sf(3.10):.4f}")        # ≈ 0.050

##-------##
## expon ##
##-------##
'''
stats.expon(loc=0, scale=1)
  Exponential distribution.  Mean = scale = 1/λ (rate parameterisation λ=1/scale).

  PDF: f(x) = (1/scale) * exp(-x/scale)  for x ≥ loc
  Memoryless: P(X > s+t | X > s) = P(X > t).
  Mean=scale, Var=scale², Skew=2, ExKurt=6.

  Key uses: inter-arrival times in Poisson processes, survival analysis.
'''
print("\n=== expon ===")
d_exp = stats.expon(scale=2.0)   # mean = 2
print(f"Mean={d_exp.mean()}, Var={d_exp.var()}")   # Mean=2.0, Var=4.0

# Memorylessness check
s, t_ = 3.0, 1.0
lhs = d_exp.sf(s + t_) / d_exp.sf(s)
rhs = d_exp.sf(t_)
print(f"Memoryless: P(X>4|X>3)={lhs:.6f} == P(X>1)={rhs:.6f}")   # True
# Memoryless: P(X>4|X>3)=0.606531 == P(X>1)=0.606531

##-------##
## gamma ##
##-------##
'''
stats.gamma(a, loc=0, scale=1)
  Gamma distribution.  a = shape (α), scale = 1/rate (β=1/scale).

  PDF: f(x) = x^(a-1)*exp(-x/scale) / (scale^a * Γ(a))  for x ≥ 0
  Mean=a*scale, Var=a*scale².
  Special cases: a=1 → Exponential; a=k (integer) → Erlang.
  Sum of k Exponential(scale) r.v.s ~ Gamma(k, scale).

  Key uses: Bayesian conjugate for Poisson rate, survival, queueing.
'''
print("\n=== gamma ===")
d_gam = stats.gamma(a=3, scale=2)   # shape=3, scale=2
print(f"Gamma(3,2) mean={d_gam.mean()}, var={d_gam.var()}")   # mean=6.0, var=12.0

# Sum of 3 exponentials ~ Gamma(3, scale)
sim_sum = sum(stats.expon(scale=2).rvs((10000, 3), random_state=i).sum(axis=1)
              for i in range(1)) / 1  # one trial
g_sim = d_gam.rvs(10000, random_state=0)
print(f"Gamma rvs mean≈{g_sim.mean():.3f} (expect 6)") # mean≈5.956 (expect 6)

##------##
## beta ##
##------##
'''
stats.beta(a, b, loc=0, scale=1)
  Beta distribution on [loc, loc+scale].  a, b > 0 are shape parameters.

  PDF: f(x) ∝ x^(a-1) * (1-x)^(b-1)  on [0,1] (standard).
  Mean = a/(a+b),  Var = ab/((a+b)²(a+b+1)).
  Special cases: a=b=1 → Uniform; a=b → symmetric around 0.5.
  a>1,b>1 → unimodal; a<1,b<1 → U-shaped; a<1,b>1 → J-shaped.

  Key uses: Bayesian conjugate for Binomial proportion, random proportions,
            Kumaraswamy approximation, project management (PERT).
'''
print("\n=== beta ===")
for a, b in [(1, 1), (2, 5), (5, 2), (0.5, 0.5)]:
    d_b = stats.beta(a, b)
    print(f"Beta({a},{b}) mean={d_b.mean():.4f} mode={max(0,(a-1)/(a+b-2)) if a+b>2 else 'at edge'}")
# Beta(1,1) mean=0.5000 mode=at edge
# Beta(2,5) mean=0.2857 mode=0.2
# Beta(5,2) mean=0.7143 mode=0.8
# Beta(0.5,0.5) mean=0.5000 mode=at edge

# Bayesian binomial proportion: after 7 heads in 10 flips
# Prior: Beta(1,1) → Posterior: Beta(1+7, 1+3) = Beta(8, 4)
prior = stats.beta(1, 1)
posterior = stats.beta(8, 4)
ci_95 = posterior.interval(0.95)
print(f"Posterior Beta(8,4): mean={posterior.mean():.4f}, 95% CI={np.array(ci_95).round(4)}")
# Posterior Beta(8,4): mean=0.6667, 95% CI=[0.3903 0.8907]

##---------##
## lognorm ##
##---------##
'''
stats.lognorm(s, loc=0, scale=1)
  Log-normal distribution.  s = σ (std of underlying normal), scale = exp(μ).
  If X ~ LN(s, scale) then log(X) ~ N(log(scale), s²).

  PDF: f(x) = exp(-(log(x/scale))²/(2s²)) / (x*s*sqrt(2π))  for x > 0
  Mean=scale*exp(s²/2), Var=scale²*exp(s²)*(exp(s²)-1).

  Key uses: stock prices, income distributions, particle sizes.
  Parameterisation: s=σ_ln, scale=exp(μ_ln).
'''
print("\n=== lognorm ===")
mu_ln, sig_ln = 1.0, 0.5
d_ln = stats.lognorm(s=sig_ln, scale=np.exp(mu_ln))
print(f"LN mean={d_ln.mean():.4f} (expect {np.exp(mu_ln + sig_ln**2/2):.4f})") # mean=3.0802 (expect 3.0802) 
print(f"LN var={d_ln.var():.4f}") # var=2.6948

# Simulated log-normal via underlying normal
x_log = rng.lognormal(mean=mu_ln, sigma=sig_ln, size=10000)
print(f"sim mean={x_log.mean():.4f}, std={x_log.std():.4f}") # sim mean=3.0785, std=1.6715

##---------##
## uniform ##
##---------##
'''
stats.uniform(loc=0, scale=1)
  Uniform distribution on [loc, loc+scale].

  PDF: f(x) = 1/scale  for x ∈ [loc, loc+scale].
  Mean = loc + scale/2,  Var = scale²/12.
'''
print("\n=== uniform ===")
d_u = stats.uniform(loc=2, scale=6)   # Uniform[2, 8]
print(f"U[2,8] mean={d_u.mean()}, var={d_u.var():.4f}")   # mean=5.0, var=3.0000
print(f"P(3 < X < 6) = {d_u.cdf(6) - d_u.cdf(3):.4f}")   # 0.5

##---------------------------##
## weibull_min / weibull_max ##
##---------------------------##
'''
stats.weibull_min(c, loc=0, scale=1)  — Weibull distribution (most common form).
  c = shape (k), scale = λ.
  PDF: f(x) = (c/scale)*(x/scale)^(c-1)*exp(-(x/scale)^c)  for x ≥ 0
  c<1: decreasing failure rate (infant mortality).
  c=1: constant failure rate (exponential).
  c>1: increasing failure rate (wear-out).

stats.weibull_max(c)  — Reflected Weibull (maximum-domain-of-attraction).
'''
print("\n=== weibull_min ===")
for c in [0.5, 1.0, 2.0, 3.5]:
    d_w = stats.weibull_min(c, scale=2)
    print(f"  c={c}: mean={d_w.mean():.4f}, median={d_w.median():.4f}")
  # c=0.5: mean=4.0000, median=0.9609
  # c=1.0: mean=2.0000, median=1.3863
  # c=2.0: mean=1.7725, median=1.6651
  # c=3.5: mean=1.7995, median=1.8012

##--------------------##
## pareto / genpareto ##
##--------------------##
'''
stats.pareto(b, loc=0, scale=1)
  Pareto distribution.  b = shape (α), scale = x_m (minimum value).
  PDF: f(x) = b/x^(b+1) for x ≥ 1 (standard); mean=b/(b-1) if b>1.
  Heavy tail: P(X>x) ~ x^(-b).

stats.genpareto(c, loc=0, scale=1)
  Generalised Pareto.  c=ξ (tail index).
  c>0: heavy-tailed Pareto-like.
  c=0: Exponential.
  c<0: bounded support (Beta-like).
  Used in Peaks Over Threshold (POT) extreme value modelling.
'''
print("\n=== pareto / genpareto ===")
d_pa = stats.pareto(b=3)
print(f"Pareto(3) mean={d_pa.mean():.4f}, var={d_pa.var():.4f}")   # mean=1.5000, var=0.7500

d_gp = stats.genpareto(c=0.2)   # heavy-tailed
print(f"GenPareto(ξ=0.2) mean={d_gp.mean():.4f}") # mean=1.2500

##--------##
## cauchy ##
##--------##
'''
stats.cauchy(loc=0, scale=1)
  Cauchy (Lorentz) distribution.
  PDF: f(x) = 1/(π*scale*(1+((x-loc)/scale)²))  for x ∈ ℝ.
  Mean and variance are UNDEFINED (heavy tails; no finite moments).
  CLT does NOT apply.  Median = loc,  IQR = 2*scale.

  Key uses: ratio of two independent normals, resonance phenomena,
            robust statistics (Cauchy prior), physics (Breit-Wigner).
'''
print("\n=== cauchy ===")
d_ca = stats.cauchy(loc=0, scale=1)
print(f"Cauchy median={d_ca.median():.4f}")   # 0

samp_c = d_ca.rvs(10000, random_state=0)
print(f"Sample mean of 10000 Cauchy: {samp_c.mean():.2f}  (undefined, wildly varying)")
# 2.57  (undefined, wildly varying)

print(f"Sample median             : {np.median(samp_c):.4f}  (stable ≈ 0)")
# Sample median: -0.0204  (stable ≈ 0)

##---------##
## laplace ##
##---------##
'''
stats.laplace(loc=0, scale=1)
  Laplace (double exponential) distribution.
  PDF: f(x) = exp(-|x-loc|/scale) / (2*scale).
  Mean=loc, Var=2*scale², Skew=0, ExKurt=3.
  Heavier tails than normal but lighter than Cauchy.
  MLE of location = median; equivalent to L1 (MAE) regression.
'''
print("\n=== laplace ===")
d_la = stats.laplace(loc=0, scale=1)
print(f"Laplace var={d_la.var()}, kurtosis={d_la.stats('k')}")   # var=2.0, kurtosis=3.0

##----------##
## logistic ##
##----------##
'''
stats.logistic(loc=0, scale=1)
  Logistic distribution.
  PDF: f(x) = exp(-(x-loc)/scale) / (scale*(1+exp(-(x-loc)/scale))²).
  CDF: F(x) = 1/(1+exp(-(x-loc)/scale))  — the sigmoid function!
  Mean=loc, Var=π²*scale²/3.

  Logistic regression: assumes log-odds is linear; residuals are logistic.
'''
print("\n=== logistic ===")
d_lo = stats.logistic(loc=0, scale=1)
# CDF of logistic IS the sigmoid
x_test = 2.0
print(f"Logistic CDF(2) = {d_lo.cdf(x_test):.6f}") # 0.880797
print(f"Sigmoid(2)      = {1/(1+np.exp(-x_test)):.6f}")   # same

##------------------------------------##
## Extreme value: gumbel / genextreme ##
##------------------------------------##
'''
stats.gumbel_r(loc=0, scale=1)  : right-skewed Gumbel (max-domain-of-attraction).
stats.gumbel_l(loc=0, scale=1)  : left-skewed Gumbel (reflected).
stats.genextreme(c, loc, scale) : Generalised Extreme Value (GEV).
  c=0 : Gumbel (type I).
  c>0 : Fréchet (heavy-tailed, type II).
  c<0 : Weibull-type (bounded, type III).

  GEV is the limiting distribution of block maxima (Fisher-Tippett theorem).
  Used in flood frequency analysis, extreme wind speeds, financial tail risk.
'''
print("\n=== extreme value - Gumbel ===")
d_gu = stats.gumbel_r(loc=0, scale=1)
print(f"Gumbel mean={d_gu.mean():.4f} (≈ Euler-Mascheroni γ={0.5772:.4f})") # mean=0.5772
print(f"Gumbel mode=0 (loc), skew={d_gu.stats('s'):.4f}")   # skew = 1.1396

d_gev = stats.genextreme(c=0.3, loc=0, scale=1)   # Fréchet type
print(f"GEV(ξ=0.3) mean={d_gev.mean():.4f}") # mean=0.3418

##----------##
## skewnorm ##
##----------##
'''
stats.skewnorm(a, loc=0, scale=1)
  Skew-normal distribution.  a = shape (skewness parameter).
  a=0: reduces to N(loc, scale²).
  a>0: right-skewed; a<0: left-skewed.
  |a|→∞: approaches half-normal.
'''
print("\n=== skewnorm ===")
for a in [-5, 0, 5]:
    d_sn = stats.skewnorm(a, loc=0, scale=1)
    print(f"  a={a:3d}: mean={d_sn.mean():.4f}, skew={d_sn.stats('s'):.4f}")
  # a= -5: mean=-0.7824, skew=-0.8510
  # a=  0: mean=0.0000, skew=0.0000
  # a=  5: mean=0.7824, skew=0.8510

##-----------##
## truncnorm ##
##-----------##
'''
stats.truncnorm(a, b, loc=0, scale=1)
  Truncated normal: N(loc, scale²) restricted to [loc+a*scale, loc+b*scale].
  a, b are standardised bounds (in units of scale).

  To truncate N(μ, σ²) to [lo, hi]:
    a = (lo - μ) / σ
    b = (hi - μ) / σ
    d = stats.truncnorm(a, b, loc=μ, scale=σ)
'''
print("\n=== truncnorm ===")
mu, sigma = 5.0, 2.0
lo, hi    = 2.0, 8.0
a_tn = (lo - mu) / sigma
b_tn = (hi - mu) / sigma
d_tn = stats.truncnorm(a_tn, b_tn, loc=mu, scale=sigma)
print(f"Truncated N(5,2) on [2,8]: mean={d_tn.mean():.4f}, std={d_tn.std():.4f}") # mean=5.0000, std=1.4853
samp_tn = d_tn.rvs(10000, random_state=0)
print(f"All in [2,8]: {(samp_tn >= 2).all() and (samp_tn <= 8).all()}")   # True

##------------##
## loguniform ##
##------------##
'''
stats.loguniform(a, b)
  Log-uniform (reciprocal) distribution on [a, b].
  PDF: f(x) = 1/(x * log(b/a)).
  Equivalent to stats.uniform on log scale.
  Common prior for scale parameters in Bayesian inference (Jeffreys prior).
'''
print("\n=== loguniform ===")
d_lu = stats.loguniform(1e-3, 1e3)   # 10⁻³ to 10³ (6 orders of magnitude)
print(f"loguniform median = {d_lu.median():.4f}") # 1.0 (geometric midpoint)
print(f"loguniform mean   = {d_lu.mean():.4f}") # 72.3823

##--------------##
## rv_histogram ##
##--------------##
'''
stats.rv_histogram(histogram, density=True)
  Build an empirical distribution from a histogram.

  histogram : (values, bin_edges) tuple — output of np.histogram().
  density   : if True, histogram values are treated as densities (normalised).

  Useful when you have a pre-computed histogram and want to compute CDF,
  sample from it, or compute statistics.
'''
print("\n=== rv_histogram ===")
x_hist = rng.normal(0, 1, 1000)
hist_counts, bin_edges = np.histogram(x_hist, bins=30, density=True)
d_rv_hist = stats.rv_histogram((hist_counts, bin_edges))
print(f"rv_histogram mean ≈ {d_rv_hist.mean():.4f}")   # -0.0322 (≈ 0)
print(f"rv_histogram CDF(0) ≈ {d_rv_hist.cdf(0):.4f}")  # 0.5068 (≈ 0.5)


# =========================================================================================
#════════════════════════════  PART B — DISCRETE DISTRIBUTIONS  ══════════════════════════════════#
# =========================================================================================

##-----------------##
## rv_discrete API ##
##-----------------##
'''
Discrete distributions share the same interface as rv_continuous, with:
  .pmf(k)  : probability mass function P(X = k)
  .logpmf(k)
  .cdf(k)  : P(X ≤ k)   (right-continuous step function)
  .ppf(q)  : smallest k with CDF(k) ≥ q
  .rvs(size)
  .stats(moments)
  No .pdf() — use .pmf() instead.
'''

##-------##
## binom ##
##-------##
'''
stats.binom(n, p)
  Binomial distribution.  n = trials, p = success probability.
  PMF: P(X=k) = C(n,k) * p^k * (1-p)^(n-k)  for k = 0,1,...,n.
  Mean=np, Var=np(1-p).
  Approximation: → N(np, np(1-p)) for large n; → Poisson(np) for small p.
'''
print("\n=== binom ===")
d_bi = stats.binom(n=20, p=0.3)
print(f"Binom(20,0.3) mean={d_bi.mean()}, var={d_bi.var()}")   # mean=6.0, var=4.2
k_vals = np.arange(0, 21)
print(f"PMF(k=6) = {d_bi.pmf(6):.4f}")    # 0.1916 (mode)
print(f"P(X≤8)   = {d_bi.cdf(8):.4f}")    # 0.8867
print(f"P(X≥10)  = {d_bi.sf(9):.4f}")     # 0.0480 = 1 - P(X≤9)

# 95th percentile: smallest k with P(X≤k)≥0.95
print(f"95th percentile: {d_bi.ppf(0.95):.0f}")   # 9

##---------##
## poisson ##
##---------##
'''
stats.poisson(mu)
  Poisson distribution.  mu = λ = rate parameter.
  PMF: P(X=k) = e^(-λ) * λ^k / k!  for k = 0,1,2,...
  Mean=Var=λ.
  Approximates Binom(n,p) when n large, p small, np=λ.

  Key uses: count data (arrivals, events per unit time/area).
'''
print("\n=== poisson ===")
d_po = stats.poisson(mu=4)
print(f"Poisson(4) mean={d_po.mean()}, var={d_po.var()}")   # mean=4.0, var=4.0
print(f"P(X=4) = {d_po.pmf(4):.4f}")    # 0.1954  (mode)
print(f"P(X=0) = {d_po.pmf(0):.4f}")    # 0.0183  (probability of no events)

# Compare Poisson vs Normal approximation (large λ)
lam = 100
d_po100 = stats.poisson(lam)
print(f"Poisson(100) mean={d_po100.mean()}, std={d_po100.std():.4f}") # mean=100.0, std=10.0000
print(f"Normal approx P(X≤95) ≈ {stats.norm(lam, np.sqrt(lam)).cdf(95):.4f}") # 0.3085
print(f"Poisson exact P(X≤95) = {d_po100.cdf(95):.4f}")   # 0.3312 (close)

##------##
## geom ##
##------##
'''
stats.geom(p)
  Geometric distribution.  p = success probability per trial.
  PMF: P(X=k) = (1-p)^(k-1) * p  for k = 1,2,3,...
  Mean = 1/p,  Var = (1-p)/p².
  Number of trials until (and including) the first success.
  Discrete memoryless distribution.
'''
print("\n=== geom ===")
d_ge = stats.geom(p=0.25)
print(f"Geom(0.25) mean={d_ge.mean()}, var={d_ge.var()}")   # mean=4.0, var=12.0
print(f"P(X=1) = {d_ge.pmf(1):.4f}")   # 0.25 (success on first trial)

##-----------##
## hypergeom ##
##-----------##
'''
stats.hypergeom(M, n, N)
  Hypergeometric distribution (sampling WITHOUT replacement).
  M = population size, n = number of "success states", N = draws.
  PMF: P(X=k) = C(n,k)*C(M-n,N-k)/C(M,N)  for k = max(0,N+n-M)..min(n,N).
  Mean=N*n/M, Var=N*n*(M-n)*(M-N) / (M²*(M-1)).

  vs Binom: use Binom when sampling with replacement (or large population).
  Classic example: quality control (defective items in a batch).
'''
print("\n=== hypergeom ===")
M, n_h, N_h = 50, 10, 7   # 50 items, 10 defective, draw 7
d_hg = stats.hypergeom(M, n_h, N_h)
print(f"Hypergeom(50,10,7) mean={d_hg.mean():.4f}")   # 1.4
print(f"P(0 defective in 7) = {d_hg.pmf(0):.4f}") # 0.1867 

##--------##
## nbinom ##
##--------##
'''
stats.nbinom(n, p)
  Negative Binomial distribution.
  n = number of successes, p = success probability.
  PMF: P(X=k) = C(k+n-1,k) * (1-p)^k * p^n  for k=0,1,2,...
  X = number of FAILURES before the nth success.
  Mean=n*(1-p)/p, Var=n*(1-p)/p².
  Generalises Poisson (overdispersed count data).
'''
print("\n=== nbinom ===")
d_nb = stats.nbinom(n=5, p=0.4)
print(f"NBinom(5,0.4) mean={d_nb.mean():.4f}")   # 5*0.6/0.4 = 7.5

##-----------##
## bernoulli ##
##-----------##
'''
stats.bernoulli(p)
  Bernoulli distribution (single binary trial).  p = P(X=1).
  PMF: P(X=1)=p, P(X=0)=1-p.
  Mean=p, Var=p*(1-p).
  Special case of Binom(1, p).
'''
print("\n=== bernoulli ===")
d_ber = stats.bernoulli(p=0.7)
print(f"Bernoulli(0.7) mean={d_ber.mean()}, var={d_ber.var():.4f}")   # mean=0.7, var=0.2100

##---------##
## randint ##
##---------##
'''
stats.randint(low, high)
  Discrete uniform distribution on {low, low+1, ..., high-1}.
  (Note: high is EXCLUSIVE, consistent with Python range convention.)
  PMF: P(X=k) = 1/(high-low).
'''
print("\n=== randint ===")
d_ri = stats.randint(1, 7)   # die roll {1,2,3,4,5,6}
print(f"Die mean={d_ri.mean()}, var={d_ri.var():.4f}")   # 3.5, 35/12≈2.917

##------##
## zipf ##
##------##
'''
stats.zipf(a)
  Zipf distribution (Zeta distribution).  a > 1.
  PMF: P(X=k) = 1/(k^a * ζ(a))  for k = 1,2,3,...
  Heavy-tailed power-law: the k-th most common element appears 1/k^a as often as the first.
  Mean = ζ(a-1)/ζ(a) if a>2.

stats.zipfian(a, n)
  Zipfian distribution (truncated): support {1,...,n}.
  More practical for finite vocabularies (text, URLs).
'''
print("\n=== zipf/zipfian ===")
d_zf = stats.zipf(a=2.0)
print(f"Zipf(2) P(X=1)={d_zf.pmf(1):.4f}, P(X=2)={d_zf.pmf(2):.4f}") # P(X=1)=0.6079, P(X=2)=0.1520

d_zi = stats.zipfian(a=1.5, n=1000)
print(f"Zipfian(1.5,1000) mean={d_zi.mean():.4f}") # mean=24.2438


# =========================================================================================
#═══════════════════════════  PART C — MULTIVARIATE DISTRIBUTIONS  ═══════════════════════════════#
# =========================================================================================

##---------------------##
## multivariate_normal ##
##---------------------##
'''
stats.multivariate_normal(mean, cov, allow_singular=False)
  Multivariate normal distribution N(μ, Σ).

  mean : (d,) mean vector.
  cov  : (d,d) positive semi-definite covariance matrix.

  Methods:
    .pdf(x)       : density at point(s) x.
    .logpdf(x)    : log density.
    .cdf(x)       : CDF (only for low dimensions; uses quasi-Monte Carlo).
    .rvs(size)    : samples.
    .entropy()    : 0.5*log(det(2πe Σ)).

  Mahalanobis distance: (x-μ)@inv(Σ)@(x-μ) — chi2(d) distributed.
'''
print("\n=== multivariate_normal ===")
mu_mv  = np.array([1.0, 2.0])
cov_mv = np.array([[1.0, 0.8], [0.8, 2.0]])
d_mv   = stats.multivariate_normal(mean=mu_mv, cov=cov_mv)

samp_mv = d_mv.rvs(size=1000, random_state=0)
print(f"Sample mean : {samp_mv.mean(axis=0).round(4)}")   # [1.0229 2.0261]
print(f"Sample cov :\n{np.cov(samp_mv.T).round(4)}")     # ≈ [[1, 0.8],[0.8, 2]]
print(f"Entropy     : {d_mv.entropy():.4f}") # 2.9916
print(f"pdf(μ)      : {d_mv.pdf(mu_mv):.6f}") # 0.136474 (peak density)

# Mahalanobis distance: each sample should be chi2(2) distributed
inv_cov = np.linalg.inv(cov_mv)
diff = samp_mv - mu_mv
maha2 = np.einsum('ij,jk,ik->i', diff, inv_cov, diff)   # (x-μ)ᵀΣ⁻¹(x-μ)
# Fraction inside 95% ellipse: should be ≈ 0.95
chi2_95 = stats.chi2(df=2).ppf(0.95)
print(f"Fraction inside 95% confidence ellipse: {(maha2 <= chi2_95).mean():.4f}")   # ≈ 0.95

##-----------##
## dirichlet ##
##-----------##
'''
stats.dirichlet(alpha)
  Dirichlet distribution on the probability simplex.
  alpha : (k,) concentration parameters (all > 0).
  Mean  : alpha / sum(alpha).
  Var_i : α_i*(Σα-α_i) / (Σα²*(Σα+1)).

  Special case: Dirichlet(1,...,1) = Uniform over simplex.
  Conjugate prior for Categorical / Multinomial likelihood.
  Larger α_i → more probability mass near e_i.
  Smaller sum(α) → more concentrated / extreme distributions.
'''
print("\n=== dirichlet ===")
alpha = np.array([2.0, 5.0, 1.0])
d_dir = stats.dirichlet(alpha)
print(f"Dirichlet mean: {d_dir.mean().round(4)}") # [0.25, 0.625, 0.125]
print(f"Dirichlet var : {d_dir.var().round(4)}") # [0.0208 0.026  0.0122]

samp_dir = d_dir.rvs(size=5, random_state=0)
print("Samples (rows sum to 1):\n", samp_dir.round(4))
#  [[0.4558 0.4954 0.0489]
#  [0.0686 0.8898 0.0416]
#  [0.1771 0.8159 0.007 ]
#  [0.2371 0.6026 0.1603]
#  [0.5024 0.48   0.0175]]
print("Row sums:", samp_dir.sum(axis=1).round(8))   # all 1.0

##-------------##
## multinomial ##
##-------------##
'''
stats.multinomial(n, p)
  Multinomial distribution.  n = total trials, p = (k,) probability vector.
  Generalisation of Binomial to k>2 categories.
  PMF: P(X=x) = n! / (x_1!...x_k!) * p_1^x_1 ... p_k^x_k.
  Mean_i = n*p_i, Var_i = n*p_i*(1-p_i), Cov(i,j) = -n*p_i*p_j.
'''
print("\n=== multinomial ===")
p_mult = np.array([0.2, 0.5, 0.3])
d_mult = stats.multinomial(n=10, p=p_mult)
print(f"Multinomial mean: {d_mult.mean()}")    # [2, 5, 3]
x_sample = d_mult.rvs(size=3, random_state=0)
print("Samples:\n", x_sample)
print("Row sums:", x_sample.sum(axis=1))   # all 10

##----------------------##
## wishart / invwishart ##
##----------------------##
'''
stats.wishart(df, scale)
  Wishart distribution — matrix generalisation of Chi-squared.
  df : degrees of freedom (must be >= dimension d).
  scale : (d,d) positive definite scale matrix.
  Mean = df * scale.
  If columns of X ~ N(0, Σ), then X@X.T ~ Wishart(n, Σ).
  Conjugate prior for multivariate normal precision matrix.

stats.invwishart(df, scale)
  Inverse-Wishart: conjugate prior for covariance matrix Σ.
  Mean = scale / (df - d - 1).
'''
print("\n=== wishart / invwishart ===")
scale_W = np.eye(3)
d_wish = stats.wishart(df=5, scale=scale_W)
W_samp = d_wish.rvs(random_state=0)
print("Wishart sample (3×3 PSD matrix):\n", W_samp.round(4))
#  [[14.8444  6.7966  1.5417]
#  [ 6.7966  4.7084  1.9426]
#  [ 1.5417  1.9426  7.3944]]

print(f"Wishart mean = df*scale = 5*I:\n{d_wish.mean()}") 
# [[5. 0. 0.]
#  [0. 5. 0.]
#  [0. 0. 5.]]

d_iw = stats.invwishart(df=7, scale=scale_W)
IW_samp = d_iw.rvs(random_state=0)
print("InvWishart sample:\n", IW_samp.round(4))
#  [[ 0.0674 -0.0683  0.0099]
#  [-0.0683  0.3996 -0.0902]
#  [ 0.0099 -0.0902  0.0825]]

##----------------##
## multivariate_t ##
##----------------##
'''
stats.multivariate_t(loc, shape, df)
  Multivariate t-distribution.  Heavier tails than multivariate normal.
  df→∞ converges to multivariate_normal.
  Mean = loc (df>1), Cov = df/(df-2) * shape (df>2).
  Used in robust Bayesian modelling and copula construction.
'''
print("\n=== multivariate_t ===")
d_mvt = stats.multivariate_t(loc=[0, 0], shape=np.eye(2), df=4)
samp_mvt = d_mvt.rvs(size=1000, random_state=0)
print(f"Multivariate t sample mean: {samp_mvt.mean(axis=0).round(4)}")   # [-0.0888  0.0099]
print(f"Sample var (expect 4/(4-2)=2): {samp_mvt.var(axis=0).round(3)}") # [1.763 1.787]


# =========================================================================================
#═══════════════════════  PART D — SUMMARY & DESCRIPTIVE STATISTICS  ═════════════════════════════#
# =========================================================================================

##------------##
## describe() ##
##------------##
'''
stats.describe(a, axis=0, ddof=1, bias=True, nan_policy='propagate')
  -> DescribeResult(nobs, minmax, mean, variance, skewness, kurtosis)

  One-call summary: count, (min,max), mean, variance, skewness, kurtosis.

  ddof       : delta degrees of freedom for variance (1 = sample, 0 = population).
  bias       : if False, correct skewness and kurtosis for bias.
  kurtosis   : EXCESS kurtosis (= kurtosis - 3); 0 for normal.
  nan_policy : 'propagate' (default), 'raise', or 'omit'.
'''
print("\n=== describe ===")
res = stats.describe(x_norm, ddof=1)
print(f"n={res.nobs}, min={res.minmax[0]:.3f}, max={res.minmax[1]:.3f}") # n=100, min=1.098, max=9.283
print(f"mean={res.mean:.4f}, var={res.variance:.4f}") # mean=4.8995, var=2.4129
print(f"skew={res.skewness:.4f}, excess_kurt={res.kurtosis:.4f}") # skew=-0.1370, excess_kurt=-0.2691

# 2-D array: axis=0 gives column-wise statistics
X_2d = rng.normal(0, 1, (50, 3))
res2 = stats.describe(X_2d, axis=0)
print(f"2-D describe shape: mean={res2.mean.shape}")   # (3,)

##-----------------------##
## gmean / hmean / pmean ##
##-----------------------##
'''
stats.gmean(a, axis=0, dtype=None, weights=None, nan_policy='propagate', keepdims=False)
  Geometric mean: (∏ aᵢ)^(1/n) = exp(mean(log(aᵢ))).
  Appropriate for ratios, growth rates, log-normal data.
  More resistant to large values than arithmetic mean.

stats.hmean(a, axis=0, dtype=None, weights=None, nan_policy='propagate', keepdims=False)
  Harmonic mean: n / Σ(1/aᵢ).
  Appropriate for rates, speeds (average of reciprocals).
  Always ≤ geometric mean ≤ arithmetic mean (AM-GM-HM inequality).

stats.pmean(a, p, axis=0, dtype=None, weights=None, nan_policy='propagate', keepdims=False)
  Power mean (generalised mean): (Σ aᵢ^p / n)^(1/p).
  p=-1: harmonic; p=1: arithmetic; p=2: RMS; p→0: geometric; p→∞: max.
'''
print("\n=== gmean / hmean / pmean ===")
a_means = np.array([1.0, 2.0, 4.0, 8.0])
print(f"Arithmetic mean : {a_means.mean():.4f}")          # 3.75
print(f"Geometric mean  : {stats.gmean(a_means):.4f}")    # 2.8284 = 2^(1+2+4+8)/4... = (1*2*4*8)^(1/4) = 2^(6/4)
print(f"Harmonic mean   : {stats.hmean(a_means):.4f}")    # 2.1333
print(f"Power mean p=2  : {stats.pmean(a_means, 2):.4f}") # 4.6098 (RMS, largest)

# AM ≥ GM ≥ HM
print(f"AM≥GM≥HM: {a_means.mean():.4f} ≥ {stats.gmean(a_means):.4f} ≥ {stats.hmean(a_means):.4f}")
# AM≥GM≥HM: 3.7500 ≥ 2.8284 ≥ 2.1333

##-----------------##
## skew / kurtosis ##
##-----------------##
'''
stats.skew(a, axis=0, bias=True, nan_policy='propagate', keepdims=False)
  Sample skewness = m₃ / m₂^(3/2) where mₙ = n-th central moment.
  0: symmetric; >0: right-tailed; <0: left-tailed.
  bias=False: applies Fisher-Pearson correction for small samples.

stats.kurtosis(a, axis=0, fisher=True, bias=True, ...)
  Excess kurtosis (Fisher): m₄/m₂² - 3.  Normal distribution → 0.
  fisher=False: non-excess (Pearson) kurtosis (add 3).
  >0: leptokurtic (heavy tails, e.g. t); <0: platykurtic (light tails, e.g. uniform).
'''
print("\n=== skew / kurtosis ===")
for dist_name, sample in [('Normal',  x_norm),
                           ('Exp',     x_exp),
                           ('Uniform', rng.uniform(0, 1, N))]:
    sk = stats.skew(sample)
    ku = stats.kurtosis(sample)
    print(f"  {dist_name:<10}: skew={sk:.3f}, excess_kurt={ku:.3f}")
  # Normal    : skew=-0.137, excess_kurt=-0.269
  # Exp       : skew=1.786, excess_kurt=4.556
  # Uniform   : skew=-0.110, excess_kurt=-1.190

##---------------------------------##
## mode / trim_mean / tmean / tsem ##
##---------------------------------##
'''
stats.mode(a, axis=0, nan_policy='propagate', keepdims=False)
  Modal value and its count.
  For continuous data or unique values, every element is a mode.
  Returns ModeResult(mode, count).

stats.trim_mean(a, proportiontocut, axis=0)
  Trimmed mean: discard a fraction proportiontocut from each tail, average rest.
  Robust to outliers. proportiontocut=0.1 → 10% trimmed mean.

stats.tmean(a, limits=None, inclusive=(True,True), axis=None)
  Trimmed mean restricted to observations in a given [lo, hi] range.
  limits=(lo,hi) — only observations where lo ≤ x ≤ hi are included.

stats.tsem(a, limits=None, inclusive=(True,True), axis=0, ddof=1)
  Trimmed standard error of the mean.
'''
print("\n=== mode / trim_mean / tmean ===")
a_cat = np.array([1, 2, 2, 3, 3, 3, 4, 4])
m = stats.mode(a_cat)
print(f"mode={m.mode}, count={m.count}")   # mode=3, count=3

print(f"10% trimmed mean (x_norm): {stats.trim_mean(x_norm, 0.1):.4f}") # 4.9444
print(f"tmean (2 to 8)           : {stats.tmean(x_norm, limits=(2, 8)):.4f}") # 4.9615
print(f"tsem  (2 to 8)           : {stats.tsem(x_norm,  limits=(2, 8)):.6f}") # 0.141831

##-----------------------##
## sem / iqr / variation ##
##-----------------------##
'''
stats.sem(a, axis=0, ddof=1, nan_policy='propagate')
  Standard error of the mean: std(a) / sqrt(n).
  95% CI for mean: mean ± 1.96 * sem (large n).

stats.iqr(a, axis=0, rng=(25,75), scale=1.0, nan_policy='propagate',
          interpolation='fraction', keepdims=False)
  Inter-quartile range Q3 - Q1.
  scale='normal': divide by 1.3490 so that IQR ≈ σ for normal (robust σ estimator).

stats.variation(a, axis=0, ddof=0, nan_policy='propagate', keepdims=False)
  Coefficient of variation: std / mean.  Dimensionless relative spread.
'''
print("\n=== sem / iqr / variation ===")
print(f"SEM of x_norm: {stats.sem(x_norm):.4f}") # 0.1553
print(f"95% CI: ({x_norm.mean() - 1.96*stats.sem(x_norm):.3f}, "
      f"{x_norm.mean() + 1.96*stats.sem(x_norm):.3f})") # (4.595, 5.204)
print(f"IQR of x_norm  : {stats.iqr(x_norm):.4f}") # 2.1578
print(f"Robust σ (IQR/1.349): {stats.iqr(x_norm, scale='normal'):.4f}")   # 1.5996
print(f"CV (coeff var) : {stats.variation(x_pos):.4f}") # 0.3356

##----------##
## moment() ##
##----------##
'''
stats.moment(a, moment=1, axis=0, nan_policy='propagate', center=None, keepdims=False)
  Compute the n-th central moment (by default): E[(X - mean(X))^n].
  moment=1: 0 (first central moment is always 0).
  moment=2: variance (= std²).
  moment=3: related to skewness.
  moment=4: related to kurtosis.

  center=None (default): uses sample mean; center=0: raw moments.
'''
print("\n=== moment ===")
for n in range(1, 5):
    m_n = stats.moment(x_norm, moment=n)
    print(f"  central moment {n}: {m_n:.6f}")
# m1≈0, m2≈var, m3 related to skew, m4 related to kurt
  # central moment 1: 0.000000
  # central moment 2: 2.388781
  # central moment 3: -0.505727
  # central moment 4: 15.583166


# =========================================================================================
#═══════════════════════════════  PART E — FREQUENCY STATISTICS  ═════════════════════════════════#
# =========================================================================================

##-------------------##
## cumfreq / relfreq ##
##-------------------##
'''
stats.cumfreq(a, numbins=10, defaultreallimits=None, weights=None)
  -> CumfreqResult(cumcount, lowerlimit, binsize, extrapoints)
  Cumulative frequency histogram.
  cumcount[i] = number of observations in bins 0..i.

stats.relfreq(a, numbins=10, defaultreallimits=None, weights=None)
  -> RelfreqResult(frequency, lowerlimit, binsize, extrapoints)
  Relative frequency histogram: frequency[i] = proportion in bin i.
'''
print("\n=== cumfreq / relfreq ===")
cf = stats.cumfreq(x_norm, numbins=10)
print(f"Cumfreq bins: {cf.cumcount.astype(int)}")   # [  1   8  20  35  53  76  95  98  99 100] increasing to N
rf = stats.relfreq(x_norm, numbins=10)
print(f"Relfreq (sum≈1): {rf.frequency.sum():.4f}")   # 1.0

##---------------------------------------##
## percentileofscore / scoreatpercentile ##
##---------------------------------------##
'''
stats.percentileofscore(a, score, kind='rank', nan_policy='propagate')
  Compute the percentile rank of a score relative to a sample.
  kind='rank'  : percentage of values ≤ score.
  kind='weak'  : percentage of values ≤ score (same as 'rank').
  kind='strict': percentage of values < score.
  kind='mean'  : average of 'weak' and 'strict'.

stats.scoreatpercentile(a, per, limit=(), interpolation_method='fraction', axis=None)
  (Legacy; prefer np.percentile or np.quantile.)
  Returns the score at the given percentile.
'''
print("\n=== percentileofscore ===")
a_perc = np.array([10, 20, 30, 40, 50])
score  = 30
print(f"percentileofscore(30, rank)  = {stats.percentileofscore(a_perc, score, 'rank'):.1f}")   # 60.0
print(f"percentileofscore(30, strict)= {stats.percentileofscore(a_perc, score, 'strict'):.1f}") # 40.0
print(f"percentileofscore(30, mean)  = {stats.percentileofscore(a_perc, score, 'mean'):.1f}")   # 50.0

##-----------------------##
## rankdata / tiecorrect ##
##-----------------------##
'''
stats.rankdata(a, method='average', axis=None, nan_policy='propagate')
  Assign ranks to data, handling ties according to method:
  'average' : tied values get mean of their ranks (default).
  'min'     : tied values get minimum rank.
  'max'     : tied values get maximum rank.
  'dense'   : like 'min' but no gaps in rank sequence.
  'ordinal' : arbitrary tiebreak by position in array.

stats.tiecorrect(rankvals)
  Tie correction factor for Mann-Whitney / Kruskal-Wallis tests.
  Returns 1.0 when no ties, < 1.0 when ties are present.
'''
print("\n=== rankdata ===")
a_rank = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5])
print("average ranks:", stats.rankdata(a_rank, method='average')) # [5.  1.5 6.  1.5 7.5 9.  3.  8.  7.5]
print("min ranks    :", stats.rankdata(a_rank, method='min')) # [4 1 5 1 6 9 3 8 6]
print("dense ranks  :", stats.rankdata(a_rank, method='dense')) # [3 1 4 1 5 7 2 6 5]
print(f"Tie correction: {stats.tiecorrect(stats.rankdata(a_rank)):.4f}") # 0.9833


# =========================================================================================
#═════════════════════════════  PART F — CORRELATION & ASSOCIATION  ══════════════════════════════#
# =========================================================================================

##----------##
## pearsonr ##
##----------##
'''
stats.pearsonr(x, y, alternative='two-sided') -> PearsonRResult
  Pearson product-moment correlation coefficient r and its p-value.

  r ∈ [-1, 1]:  1=perfect positive linear, 0=no linear, -1=perfect negative.
  p-value: two-sided test H₀: r=0.
  .statistic : r value.
  .pvalue    : p-value.
  .confidence_interval(confidence_level) : CI for r using Fisher Z-transform.

  Assumes:
    • Both variables approximately normal.
    • Linear relationship.
    • Homoscedasticity.
'''
print("\n=== pearsonr ===")
x_corr = rng.normal(0, 1, 50)
y_corr = 2 * x_corr + rng.normal(0, 0.5, 50)   # strong linear relationship
res_pr = stats.pearsonr(x_corr, y_corr)
print(f"Pearson r={res_pr.statistic:.4f}, p={res_pr.pvalue:.4e}")   # r=0.9734, p=2.2793e-32 (r≈0.97, p≈0)
ci_pr = res_pr.confidence_interval(0.95)
print(f"95% CI for r: [{ci_pr.low:.4f}, {ci_pr.high:.4f}]") # [0.9533, 0.9849]

# Independent: r should be near 0
y_ind = rng.normal(0, 1, 50)
res_ind = stats.pearsonr(x_corr, y_ind)
print(f"Independent r={res_ind.statistic:.4f}, p={res_ind.pvalue:.4f}")   # r=-0.0177, p=0.9031 (p > 0.05)

##-----------##
## spearmanr ##
##-----------##
'''
stats.spearmanr(a, b=None, axis=0, nan_policy='propagate',
                alternative='two-sided') -> SpearmanrResult
  Spearman rank correlation ρ.  Pearson r of the ranks.

  Non-parametric: works for any monotonic relationship (not just linear).
  Robust to outliers and non-normal distributions.
  ρ = 1 if y = f(x) for any strictly increasing f.
  Returns .statistic and .pvalue (and .correlation / .pvalue for matrix form).
'''
print("\n=== spearmanr ===")
y_mono = x_corr**3 + rng.normal(0, 0.1, 50)   # monotonic but nonlinear
res_sp_lin  = stats.spearmanr(x_corr, y_corr)
res_sp_mono = stats.spearmanr(x_corr, y_mono)
print(f"Spearman (linear)    ρ={res_sp_lin.statistic:.4f}") # ρ=0.9321
print(f"Spearman (monotonic) ρ={res_sp_mono.statistic:.4f}") # ρ=0.9236 (also high)

# Matrix form: pass 2-D array, get correlation matrix
X_corr_mat = np.column_stack([x_corr, y_corr, y_ind])
rho_mat, p_mat = stats.spearmanr(X_corr_mat)
print("Spearman correlation matrix:\n", rho_mat.round(3))
#  [[ 1.     0.932 -0.033]
#  [ 0.932  1.     0.005]
#  [-0.033  0.005  1.   ]]

##------------##
## kendalltau ##
##------------##
'''
stats.kendalltau(x, y, initial_lexsort=None, nan_policy='propagate',
                 method='auto', alternative='two-sided') -> KendalltauResult
  Kendall τ rank correlation.

  τ = (C - D) / sqrt((C+D+T)(C+D+U))
  C = concordant pairs, D = discordant, T = x-ties, U = y-ties.

  variant='b' (default): τ_b — handles ties properly.
  variant='c': τ_c — for rectangular contingency tables.
  More conservative than Spearman for small samples.
  method='auto': uses O(n log n) merge-sort algorithm when possible.
'''
print("\n=== kendalltau ===")
res_kt = stats.kendalltau(x_corr, y_corr)
print(f"Kendall τ={res_kt.statistic:.4f}, p={res_kt.pvalue:.4e}") # τ=0.7992, p=2.6298e-16

# Somers' D: asymmetric rank correlation (one variable is ordinal response)
res_sd = stats.somersd(x_corr, y_corr)
print(f"Somers' D={res_sd.statistic:.4f}, p={res_sd.pvalue:.4e}") # D=0.7992, p=2.2002e-74

##----------------##
## pointbiserialr ##
##----------------##
'''
stats.pointbiserialr(x, y) -> PointbiserialrResult
  Point-biserial correlation: Pearson r when one variable is dichotomous (0/1).
  Equivalent to Pearson r between a boolean and a continuous variable.
  Returns .statistic (r) and .pvalue.
'''
print("\n=== pointbiserialr ===")
x_cont = rng.normal(0, 1, 50)
x_bin  = (x_cont > 0).astype(float) + rng.normal(0, 0.1, 50)   # noisy binary
grp    = (x_cont > 0).astype(int)
res_pb = stats.pointbiserialr(grp, x_bin)
print(f"Point-biserial r={res_pb.statistic:.4f}, p={res_pb.pvalue:.4e}") # r=0.9793, p=5.7988e-35

##------------------##
## chi2_contingency ##
##------------------##
'''
stats.chi2_contingency(observed, correction=True, lambda_=None)
  Chi-squared test of independence for a contingency table.

  observed   : (r, c) table of observed counts.
  correction : if True (default), apply Yates' continuity correction for 2×2.
  lambda_    : None → χ², 'log-likelihood' → G-test, 'freeman-tukey' → Freeman-Tukey.

  Returns: Chi2ContingencyResult with:
    .statistic : χ² value.
    .pvalue    : p-value under H₀ of independence.
    .dof       : degrees of freedom = (r-1)*(c-1).
    .expected_freq: expected cell counts under independence.

  Also useful for: Cramér's V = sqrt(χ²/(n * min(r-1, c-1))).
'''
print("\n=== chi2_contingency ===")
obs_table = np.array([[50, 30, 20],   # group A
                       [20, 40, 40]])  # group B
res_ct = stats.chi2_contingency(obs_table, correction=False)
print(f"χ²={res_ct.statistic:.4f}, df={res_ct.dof}, p={res_ct.pvalue:.4f}") # χ²=20.9524, df=2, p=0.0000
print("Expected counts:\n", res_ct.expected_freq.round(2))
#  [[35. 35. 30.]
#  [35. 35. 30.]]

# Cramér's V: effect size for chi-squared
n_ct = obs_table.sum()
cramer_v = np.sqrt(res_ct.statistic / (n_ct * min(obs_table.shape[0]-1, obs_table.shape[1]-1)))
print(f"Cramér's V = {cramer_v:.4f}")   # V = 0.3237 (0=no association, 1=perfect)


# =========================================================================================
#═════════════════════════════════  PART G — STATISTICAL TESTS  ══════════════════════════════════#
# =========================================================================================

# ────────────────────── G1 : ONE-SAMPLE TESTS ─────────────────────────────────

##-------------##
## ttest_1samp ##
##-------------##
'''
stats.ttest_1samp(a, popmean, axis=0, nan_policy='propagate',
                  alternative='two-sided') -> TtestResult
  One-sample t-test: H₀: mean(a) == popmean.

  alternative: 'two-sided' (default), 'less', 'greater'.
  Returns .statistic (t), .pvalue, .df.
  Assumes data are approximately normal (or n > ~30 by CLT).
'''
print("\n=== ttest_1samp ===")
res_t1 = stats.ttest_1samp(x_norm, popmean=5.0)
print(f"t={res_t1.statistic:.4f}, p={res_t1.pvalue:.4f}, df={res_t1.df}") # t=-0.6472, p=0.5190, df=99
# True mean is 5, so p > 0.05 (fail to reject H₀)

res_t1_false = stats.ttest_1samp(x_norm, popmean=0.0)
print(f"t={res_t1_false.statistic:.4f}, p={res_t1_false.pvalue:.4e}")  # t=31.5412, p=1.9003e-53 (p ≈ 0 -> reject)

# One-sided: test if mean > 4
res_t1_one = stats.ttest_1samp(x_norm, popmean=4.0, alternative='greater')
print(f"H₀: μ≤4  t={res_t1_one.statistic:.4f}, p={res_t1_one.pvalue:.4f}")
# H₀: μ≤4  t=5.7904, p=0.0000

##-------------------##
## ks_1samp / kstest ##
##-------------------##
'''
stats.kstest(rvs, cdf, args=(), N=20, alternative='two-sided', method='auto')
stats.ks_1samp(x, cdf, args=(), alternative='two-sided', method='auto')
  Kolmogorov-Smirnov one-sample test.
  H₀: x comes from the given theoretical distribution (cdf).

  rvs  : array of observations or callable (for kstest).
  cdf  : callable — CDF function of theoretical distribution, or string
         name of a scipy.stats distribution.
  KS statistic: D = max|F_n(x) - F(x)|.

  method: 'auto' (exact for n≤10000), 'exact', 'approx', 'asymp'.
'''
print("\n=== ks_1samp ===")
# Test x_norm against N(5,4) = N(5,2²)
res_ks = stats.ks_1samp(x_norm, stats.norm(loc=5, scale=2).cdf)
print(f"KS N(5,2): D={res_ks.statistic:.4f}, p={res_ks.pvalue:.4f}")  # D=0.1196, p=0.1054 (p > 0.05 (correct dist))

res_ks_wrong = stats.ks_1samp(x_norm, stats.norm(loc=0, scale=1).cdf)
print(f"KS N(0,1): D={res_ks_wrong.statistic:.4f}, p={res_ks_wrong.pvalue:.4e}")  # D=0.9515, p=7.5557e-132 (p ≈ 0 (wrong dist))

# Using kstest with string name
res_kstest = stats.kstest(x_exp, 'expon', args=(0, 2))   # expon(loc=0, scale=2)
print(f"kstest Expon(2): D={res_kstest.statistic:.4f}, p={res_kstest.pvalue:.4f}") # D=0.0588, p=0.8600 (p > 0.05 (correct dist))

##---------##
## shapiro ##
##---------##
'''
stats.shapiro(x) -> ShapiroWilkResult(.statistic, .pvalue)
  Shapiro-Wilk test for normality.  Best for small samples (n < 5000).
  H₀: the data come from a normal distribution.
  W statistic ∈ (0, 1]; W near 1 → likely normal.
  High power for detecting deviations from normality.
'''
print("\n=== shapiro ===")
res_sw_norm = stats.shapiro(x_norm[:50])
res_sw_exp  = stats.shapiro(x_exp[:50])
print(f"Shapiro-Wilk (Normal):     W={res_sw_norm.statistic:.4f}, p={res_sw_norm.pvalue:.4f}") # W=0.9841, p=0.7301
print(f"Shapiro-Wilk (Exponential):W={res_sw_exp.statistic:.4f},  p={res_sw_exp.pvalue:.4e}") # W=0.7925,  p=5.9247e-07
# Normal p > 0.05 (don't reject), Exp p ≪ 0.05 (reject normality)

##------------##
## normaltest ##
##------------##
'''
stats.normaltest(a, axis=0, nan_policy='propagate') -> NormaltestResult
  D'Agostino-Pearson combined omnibus test for normality.
  Combines skewness and kurtosis into a single χ²(2) statistic.
  Works better for large samples than Shapiro-Wilk.
  H₀: data come from a normal distribution.
'''
print("\n=== normaltest ===")
res_nt = stats.normaltest(x_norm)
print(f"normaltest: stat={res_nt.statistic:.4f}, p={res_nt.pvalue:.4f}")   # stat=0.4731, p=0.7893 (p > 0.05)

res_nt_exp = stats.normaltest(x_exp)
print(f"normaltest (Exp): stat={res_nt_exp.statistic:.4f}, p={res_nt_exp.pvalue:.4e}") # stat=49.1796, p=2.0931e-11

##-------------##
## jarque_bera ##
##-------------##
'''
stats.jarque_bera(x, *, axis=None, nan_policy='propagate', keepdims=False)
  Jarque-Bera test for normality using skewness and kurtosis.
  JB = n/6 * (S² + K²/4)  where S=skewness, K=excess kurtosis.
  JB ~ χ²(2) asymptotically under H₀: normality.
  Designed for large samples; less reliable for small n.
'''
print("\n=== jarque_bera ===")
res_jb = stats.jarque_bera(x_norm)
print(f"Jarque-Bera: stat={res_jb.statistic:.4f}, p={res_jb.pvalue:.4f}") # stat=0.6145, p=0.7355

##-----------##
## chisquare ##
##-----------##
'''
stats.chisquare(f_obs, f_exp=None, ddof=0, axis=0) -> Power_divergenceResult
  One-way chi-squared goodness-of-fit test.
  H₀: observed frequencies match expected frequencies.
  χ² = Σ (O - E)² / E,  df = k - 1 - ddof.
  f_exp=None → uniform expected frequencies.
'''
print("\n=== chisquare ===")
# Test if a die is fair
die_obs = np.array([18, 22, 15, 20, 19, 16])   # 6 faces, 110 rolls
die_exp = np.full(6, die_obs.sum() / 6)
res_cs  = stats.chisquare(die_obs, f_exp=die_exp)
print(f"Die fairness: χ²={res_cs.statistic:.4f}, p={res_cs.pvalue:.4f}")   # χ²=1.8182, p=0.8737 (p > 0.05)


# ────────────────────── G2 : TWO-SAMPLE TESTS ─────────────────────────────────

##-----------##
## ttest_ind ##
##-----------##
'''
stats.ttest_ind(a, b, axis=0, equal_var=True, nan_policy='propagate',
                permutations=None, random_state=None, alternative='two-sided',
                trim=0) -> TtestResult
  Independent (two-sample) t-test.  H₀: mean(a) == mean(b).

  equal_var=True  : Student's t (pooled variance — assumes equal variances).
  equal_var=False : Welch's t   (unequal variances — more robust, preferred in practice).
  trim            : Yuen's t-test (trimmed mean version, robust to outliers).
  permutations    : if int, use permutation test instead of t-distribution.
'''
print("\n=== ttest_ind ===")
group_a = rng.normal(5, 2, 50)
group_b = rng.normal(6, 2, 50)   # different mean

res_ti_student = stats.ttest_ind(group_a, group_b, equal_var=True) 
res_ti_welch   = stats.ttest_ind(group_a, group_b, equal_var=False) 
print(f"Student t: t={res_ti_student.statistic:.4f}, p={res_ti_student.pvalue:.4f}") # t=-1.2726, p=0.2062
print(f"Welch   t: t={res_ti_welch.statistic:.4f},   p={res_ti_welch.pvalue:.4f}") # t=-1.2726,   p=0.2065

# One-sided: is group_b > group_a?
res_one = stats.ttest_ind(group_a, group_b, alternative='less')
print(f"One-sided (a<b): p={res_one.pvalue:.4f}")   # p=0.1031
# This means that we fail to reject H₀: mean(a) ≥ mean(b)
# If we set their std=1 instead of 2, we would get p=0.0001 (reject H₀: mean(a) ≥ mean(b))

# Trim=0.1: Yuen's robust version
res_yuen = stats.ttest_ind(group_a, group_b, trim=0.1)
print(f"Yuen (10% trim): t={res_yuen.statistic:.4f}, p={res_yuen.pvalue:.4f}") # t=-1.3764, p=0.1726

##-----------##
## ttest_rel ##
##-----------##
'''
stats.ttest_rel(a, b, axis=0, nan_policy='propagate', alternative='two-sided')
  Paired (related-samples) t-test.  H₀: mean(a-b) == 0.
  Equivalent to ttest_1samp(a - b, popmean=0).
  More powerful than ttest_ind when observations are naturally paired
  (before/after, matched subjects).
'''
print("\n=== ttest_rel ===")
before = rng.normal(5, 1, 30)
effect = rng.normal(1, 0.5, 30)   # true treatment effect
after  = before + effect
res_tr = stats.ttest_rel(before, after)
print(f"Paired t: t={res_tr.statistic:.4f}, p={res_tr.pvalue:.4e}") # Paired t: t=-13.3031, p=7.1158e-14 (p ≪ 0.05)

##--------------##
## mannwhitneyu ##
##--------------##
'''
stats.mannwhitneyu(x, y, use_continuity=True, alternative='two-sided',
                   axis=0, method='auto', nan_policy='propagate') -> MannwhitneyuResult
  Mann-Whitney U test (non-parametric alternative to ttest_ind).
  H₀: P(X > Y) = 0.5 (x and y have the same distribution).
  Does NOT assume normality.
  method='auto': exact for small n, asymptotic otherwise.
  U statistic: number of pairs (xᵢ, yⱼ) with xᵢ > yⱼ.
  Closely related to Wilcoxon rank-sum test.
'''
print("\n=== mannwhitneyu ===")
x_skew = rng.exponential(2, 40)
y_skew = rng.exponential(3, 40)   # different median
res_mw = stats.mannwhitneyu(x_skew, y_skew, alternative='two-sided')
print(f"Mann-Whitney U={res_mw.statistic:.1f}, p={res_mw.pvalue:.4f}") # U=532.0, p=0.0101

##----------##
## wilcoxon ##
##----------##
'''
stats.wilcoxon(x, y=None, zero_method='wilcox', correction=False,
               alternative='two-sided', method='auto', nan_policy='propagate')
  Wilcoxon signed-rank test (non-parametric paired test).
  H₀: median of differences is 0.
  Non-parametric alternative to ttest_rel.
  zero_method: how to handle zero differences.
  method='auto': exact for n≤25, asymptotic otherwise.
'''
print("\n=== wilcoxon ===")
res_wc = stats.wilcoxon(before, after, alternative='less')
print(f"Wilcoxon: stat={res_wc.statistic:.1f}, p={res_wc.pvalue:.4e}") # stat=0.0, p=9.3132e-10 (p ≪ 0.05)

##----------##
## ks_2samp ##
##----------##
'''
stats.ks_2samp(data1, data2, alternative='two-sided', method='auto')
  Two-sample Kolmogorov-Smirnov test.
  H₀: data1 and data2 come from the same continuous distribution.
  D = max|F_n1(x) - F_n2(x)|.
  Sensitive to differences in location, scale, or shape.
  Non-parametric; no distributional assumption.
'''
print("\n=== ks_2samp ===")
d1 = rng.normal(0, 1, 100)
d2 = rng.normal(0.5, 1, 100)   # different location
res_ks2 = stats.ks_2samp(d1, d2)
print(f"KS 2samp: D={res_ks2.statistic:.4f}, p={res_ks2.pvalue:.4f}") # D=0.3300, p=0.0000

# Same distribution
d3 = rng.normal(0, 1, 100)
res_ks2_same = stats.ks_2samp(d1, d3)
print(f"KS 2samp (same dist): D={res_ks2_same.statistic:.4f}, p={res_ks2_same.pvalue:.4f}") # D=0.1300, p=0.3682 (same distribution, p > 0.05)

##----------------##
## cramervonmises ##
##----------------##
'''
stats.cramervonmises(rvs, cdf, args=())             # one-sample
stats.cramervonmises_2samp(x, y, method='auto')     # two-sample

  Cramér-von Mises test — alternative to KS; uses integral of squared differences
  instead of maximum, making it more sensitive to deviations in the tails.
  Two-sample: H₀: x and y have the same distribution.
'''
print("\n=== cramervonmises_2samp ===")
res_cvm = stats.cramervonmises_2samp(d1, d2)
print(f"CvM 2samp: stat={res_cvm.statistic:.4f}, p={res_cvm.pvalue:.4f}") # stat=1.9331, p=0.0000

##----------##
## ranksums ##
##----------##
'''
stats.ranksums(x, y, alternative='two-sided', nan_policy='propagate')
  Wilcoxon rank-sum test (large-sample approximation of Mann-Whitney U).
  Uses normal approximation; suitable for large samples with ties.
'''
print("\n=== ranksums ===")
res_rs = stats.ranksums(x_skew, y_skew)
print(f"Ranksums: stat={res_rs.statistic:.4f}, p={res_rs.pvalue:.4f}") # stat=-2.5788, p=0.0099

##---------------##
## brunnermunzel ##
##---------------##
'''
stats.brunnermunzel(x, y, alternative='two-sided', distribution='t',
                    nan_policy='propagate')
  Brunner-Munzel test: H₀: P(X < Y) = 0.5.
  More robust than Mann-Whitney when variance/shape differs between groups.
  distribution='t': use t approximation; 'normal': use normal.
'''
print("\n=== brunnermunzel ===")
res_bm = stats.brunnermunzel(x_skew, y_skew)
print(f"Brunner-Munzel: stat={res_bm.statistic:.4f}, p={res_bm.pvalue:.4f}") # stat=2.7664, p=0.0071


# ────────────────────── G3 : k-SAMPLE / ANOVA TESTS ──────────────────────────

##----------##
## f_oneway ##
##----------##
'''
stats.f_oneway(*args, axis=0) -> F_onewayResult(.statistic, .pvalue)
  One-way ANOVA F-test.  H₀: all group means are equal.
  Assumes: normality within groups, equal variances (homoscedasticity),
           independent observations.
  F = MSbetween / MSwithin.
  For k=2 groups: F == t² from ttest_ind.
'''
print("\n=== f_oneway ===")
g1 = rng.normal(5, 1.5, 30)
g2 = rng.normal(6, 1.5, 30)
g3 = rng.normal(5.5, 1.5, 30)
res_f = stats.f_oneway(g1, g2, g3)
print(f"ANOVA F={res_f.statistic:.4f}, p={res_f.pvalue:.4f}") # F=4.7812, p=0.0107

##---------##
## kruskal ##
##---------##
'''
stats.kruskal(*args, nan_policy='propagate', axis=0, keepdims=False)
  Kruskal-Wallis H test (non-parametric one-way ANOVA).
  H₀: all groups have the same distribution (same median).
  Based on ranks; does not assume normality.
  H ~ χ²(k-1) asymptotically.
'''
print("\n=== kruskal ===")
res_kw = stats.kruskal(g1, g2, g3)
print(f"Kruskal-Wallis H={res_kw.statistic:.4f}, p={res_kw.pvalue:.4f}") # H=8.3704, p=0.0152

##-------------------##
## friedmanchisquare ##
##-------------------##
'''
stats.friedmanchisquare(*args) -> FriedmanchisquareResult
  Friedman test (non-parametric repeated-measures / two-way ANOVA).
  H₀: repeated measures on same subjects have same distribution.
  Each *arg is a column of measurements (subjects × conditions).
'''
print("\n=== friedmanchisquare ===")
subj = 20
cond_a = rng.normal(5, 1, subj)
cond_b = cond_a + rng.normal(1, 0.5, subj)   # treatment effect
cond_c = cond_a + rng.normal(2, 0.5, subj)   # larger effect
res_fr = stats.friedmanchisquare(cond_a, cond_b, cond_c)
print(f"Friedman: stat={res_fr.statistic:.4f}, p={res_fr.pvalue:.4e}") # stat=32.4000, p=9.2136e-08  

##-------------##
## median_test ##
##-------------##
'''
stats.median_test(*args, ties='below', correction=True, lambda_=None,
                  nan_policy='propagate')
  Mood's median test: H₀: all groups have the same median.
  Chi-squared test on a 2×k contingency table (above/below grand median).
  Less powerful than Kruskal-Wallis but more robust to heteroscedasticity.
'''
print("\n=== median_test ===")
res_mt = stats.median_test(g1, g2, g3)
print(f"Median test: stat={res_mt.statistic:.4f}, p={res_mt.pvalue:.4f}, median={res_mt.median:.4f}")
# stat=5.6000, p=0.0608, median=5.6443

##-----------------------------##
## levene / bartlett / fligner ##
##-----------------------------##
'''
stats.levene(*args, center='median', proportiontocut=0.05)
  Levene test for equality of variances.  Robust (uses medians by default).
  H₀: all groups have equal variances.  center='mean': Brown-Forsythe test.

stats.bartlett(*args)
  Bartlett test for equality of variances.  More powerful but sensitive to normality.
  H₀: σ₁² = σ₂² = ... = σₖ².  Do not use if data are non-normal.

stats.fligner(*args, center='median', proportiontocut=0.05)
  Fligner-Killeen test: distribution-free test for variance homogeneity.
  Most robust of the three.
'''
print("\n=== levene / bartlett / fligner ===")
g_eq   = [rng.normal(0, 1, 30), rng.normal(0, 1, 30), rng.normal(0, 1, 30)]
g_uneq = [rng.normal(0, 1, 30), rng.normal(0, 2, 30), rng.normal(0, 3, 30)]

for test, name in [(stats.levene, 'levene'), (stats.bartlett, 'bartlett'),
                   (stats.fligner, 'fligner')]:
    eq_res   = test(*g_eq)
    uneq_res = test(*g_uneq)
    print(f"{name}: equal_var p={eq_res.pvalue:.4f}  unequal_var p={uneq_res.pvalue:.4f}")
# levene: equal_var p=0.7078  unequal_var p=0.0000
# bartlett: equal_var p=0.3946  unequal_var p=0.0000
# fligner: equal_var p=0.7601  unequal_var p=0.0000


# ────────────────────── G4 : ASSOCIATION / CONTINGENCY TESTS ─────────────────

##--------------##
## fisher_exact ##
##--------------##
'''
stats.fisher_exact(table, alternative='two-sided') -> OddsRatioResult
  Fisher's exact test for a 2×2 contingency table.
  Exact (no large-sample approximation needed).
  H₀: odds ratio = 1 (variables are independent).
  Use when expected cell counts < 5 (chi² approximation fails).
  Returns .statistic (odds ratio) and .pvalue.
'''
print("\n=== fisher_exact ===")
table_2x2 = np.array([[8, 2], [1, 9]])   # 20 subjects, 2×2 table
res_fe = stats.fisher_exact(table_2x2)
print(f"Fisher exact: OR={res_fe.statistic:.4f}, p={res_fe.pvalue:.4f}")   # OR≈36, p<0.05

##--------------------------##
## barnard_exact / boschloo ##
##--------------------------##
'''
stats.barnard_exact(table, alternative='two-sided', pooled=True, n=32)
  Barnard's exact test: unconditional exact test for 2×2 tables.
  More powerful than Fisher's when sample sizes are small and unequal.

stats.boschloo_exact(table, alternative='two-sided', n=32)
  Boschloo's test: even more powerful than Barnard's.
  Combines Fisher's p-value as test statistic with Barnard's unconditional approach.
'''
print("\n=== barnard_exact / boschloo_exact ===")
res_ba = stats.barnard_exact(table_2x2)
res_bo = stats.boschloo_exact(table_2x2)
print(f"Barnard exact  p={res_ba.pvalue:.4f}") # p=0.0018
print(f"Boschloo exact p={res_bo.pvalue:.4f}") # p=0.0018


# ────────────────────── G5 : POST-HOC TESTS ──────────────────────────────────

##-----------##
## tukey_hsd ##
##-----------##
'''
stats.tukey_hsd(*args) -> TukeyHSDResult
  Tukey HSD (honestly significant difference) post-hoc test.
  Run after a significant ANOVA to determine which pairs differ.

  .statistic  : pairwise mean differences matrix.
  .pvalue     : pairwise p-values (adjusted for multiple comparisons).
  .confidence_interval(confidence_level): pairwise CI for each difference.
'''
print("\n=== tukey_hsd ===")
res_hsd = stats.tukey_hsd(g1, g2, g3)
print("Tukey HSD pvalue matrix:")
print(res_hsd.pvalue.round(4))
# [[1.     0.0185 0.9784]
#  [0.0185 1.     0.0313]
#  [0.9784 0.0313 1.    ]]

ci_hsd = res_hsd.confidence_interval(0.95)
print("95% CI for group1 - group2:", (ci_hsd.low[0,1].round(4), ci_hsd.high[0,1].round(4)))
# 95% CI for group1 - group2: (np.float64(-2.0782), np.float64(-0.1561))

##---------##
## dunnett ##
##---------##
'''
stats.dunnett(*args, control=0, alternative='two-sided') -> DunnettResult
  Dunnett's test: compare multiple treatment groups to a single control.
  More powerful than Tukey HSD for control-vs-treatment comparisons.
  control : index of the control group in *args.
'''
print("\n=== dunnett ===")
control_grp  = rng.normal(5, 1.5, 30)
treatment_1  = rng.normal(6, 1.5, 30)
treatment_2  = rng.normal(5.2, 1.5, 30)
res_dn = stats.dunnett(control_grp, treatment_1, treatment_2, control=control_grp)
print("Dunnett p-values (vs control):", res_dn.pvalue.round(4)) # [1.     0.0037 0.1284]


# =========================================================================================
#═══════════════════════  PART H — DISTRIBUTION FITTING & KDE  ═══════════════════════════════════#
# =========================================================================================

##------------##
## dist.fit() ##
##------------##
'''
dist.fit(data, *args, **kwds) -> (shape_params..., loc, scale)
  Maximum Likelihood Estimation of distribution parameters from data.
  Returns a tuple: (shape_1, ..., shape_k, loc, scale).

  Fix parameters using f0, f1, ..., floc, fscale keyword arguments:
    floc=0   : fix loc=0 (do not estimate it).
    fscale=1 : fix scale=1.
  This reduces the number of free parameters.

  Note: for heavy-tailed or multi-modal data, consider using the new
  stats.fit() function which uses differential evolution.
'''
print("\n=== dist.fit() MLE ===")
# Fit normal distribution to data
x_fit = rng.normal(loc=3.0, scale=1.5, size=200)
mu_hat, sig_hat = stats.norm.fit(x_fit)
print(f"Normal fit: μ̂={mu_hat:.4f} (true 3), σ̂={sig_hat:.4f} (true 1.5)")
# Normal fit: μ̂=3.3047 (true 3), σ̂=1.5575 (true 1.5)

# Fit gamma distribution (shape, loc, scale)
x_gamma_fit = rng.gamma(shape=2, scale=3, size=500)
a_hat, loc_hat, scale_hat = stats.gamma.fit(x_gamma_fit, floc=0)   # fix loc=0
print(f"Gamma fit (floc=0): a={a_hat:.4f} (true 2), scale={scale_hat:.4f} (true 3)")
# Gamma fit (floc=0): a=2.1563 (true 2), scale=2.8089 (true 3)

# Fit exponential (fix loc=0 for proper exponential)
x_expon_fit = rng.exponential(scale=4, size=300)
_, scale_expon = stats.expon.fit(x_expon_fit, floc=0)
print(f"Expon fit: scale={scale_expon:.4f} (true 4)")
# Expon fit: scale=3.9326 (true 4)

# Log-likelihood at fitted parameters
ll = np.sum(stats.norm.logpdf(x_fit, mu_hat, sig_hat))
print(f"Log-likelihood at MLE: {ll:.4f}")
# Log-likelihood at MLE: -372.4014

# Kolmogorov-Smirnov goodness-of-fit check
ks_stat, ks_p = stats.kstest(x_fit, 'norm', args=(mu_hat, sig_hat))
print(f"KS test after fit: D={ks_stat:.4f}, p={ks_p:.4f}")   # should be p > 0.05
# KS test after fit: D=0.0355, p=0.9548

##-----------##
## stats.fit ##
##-----------##
'''
stats.fit(dist, data, bounds=None, *, guess=None, method='mle', optimizer=<...>)
  Unified fitting function.
  Uses differential evolution for global optimisation — more robust than
  the gradient-based dist.fit() for difficult likelihoods.

  dist   : a frozen or unfrozen rv_continuous distribution.
  data   : 1-D array of observations.
  bounds : dict or sequence constraining parameter bounds.
           e.g. bounds={'a': (0.1, 5), 'loc': (0, None)}.
  method : 'mle' (default) or 'mse' (minimum sum of squared errors).

  Returns FitResult with:
    .params     : named-tuple of fitted parameter values.
    .success    : bool — did optimiser converge?
    .message    : convergence message.
    .nllf()     : negative log-likelihood at fit.
    .plot(ax)   : plot data histogram + fitted PDF.
'''
print("\n=== stats.fit() ===")
try:
    res_fit = stats.fit(stats.gamma, x_gamma_fit,
                        bounds={'a': (0.5, 10), 'loc': (0, 0), 'scale': (0.5, 20)})
    print(f"stats.fit gamma: {res_fit.params}")
    print(f"Success: {res_fit.success}")
    print(f"Neg log-likelihood: {res_fit.nllf():.4f}")
except Exception as e:
    print(f"stats.fit: {e}")

# stats.fit gamma: FitParams(a=np.float64(2.1563174968015772), loc=np.float64(0.0), scale=np.float64(2.808928997083049))
# Success: True
# Neg log-likelihood: 1331.3813

##--------------##
## gaussian_kde ##
##--------------##
'''
stats.gaussian_kde(dataset, bw_method=None, weights=None)
  Gaussian kernel density estimator.

  dataset    : (d, N) array — d dimensions, N observations.
  bw_method  : bandwidth selection:
    'scott'   (default): Scott's rule h = n^(-1/(d+4)).
    'silverman': Silverman's rule.
    scalar    : multiply Scott's factor by this scalar.
    callable  : custom function of KDE instance.
  weights    : per-observation weights (normalised internally).

Methods:
  kde(x)          : evaluate estimated density at points x.
  kde.pdf(x)      : same as kde(x) — probability density.
  kde.integrate_gaussian(mean, cov) : integrate kde against a Gaussian.
  kde.integrate_box_1d(low, high)   : CDF between low and high (1-D only).
  kde.resample(size)                : draw new samples from the estimated density.
  kde.factor                        : bandwidth factor h.
  kde.covariance_factor()           : bandwidth factor (as method).
  kde.set_bandwidth(bw_method)      : change bandwidth after construction.

KDE vs histogram:
  Histogram : discontinuous, sensitive to bin width and placement.
  KDE       : smooth, continuous, parameter is bandwidth h (not n_bins).
  Undersmoothing (small h) → spiky; Oversmoothing (large h) → blurry.
'''
print("\n=== gaussian_kde ===")
x_kde = np.concatenate([rng.normal(-2, 0.5, 150),
                         rng.normal( 2, 0.8, 100)]) # bimodal

kde = stats.gaussian_kde(x_kde)
print(f"Bandwidth factor (Scott): {kde.factor:.4f}") # 0.3314

# Evaluate density at grid
x_grid = np.linspace(-5, 6, 200)
density = kde(x_grid)
print(f"KDE integrates to ≈ {np.trapezoid(density, x_grid):.6f}") # 0.999917 (≈ 1.0)

# Silverman vs Scott
kde_scott     = stats.gaussian_kde(x_kde, bw_method='scott')
kde_silverman = stats.gaussian_kde(x_kde, bw_method='silverman')
print(f"Scott bw={kde_scott.factor:.4f}, Silverman bw={kde_silverman.factor:.4f}") # bw=0.3314, Silverman bw=0.3511

# Resample from KDE (smoothed bootstrap)
resampled = kde.resample(size=100, seed=0)
print(f"Resampled shape: {resampled.shape}")   # (1, 100) for 1-D input

# 2-D KDE
x_2d_kde = rng.multivariate_normal([0, 0], [[1, 0.8], [0.8, 2]], 500)
kde_2d = stats.gaussian_kde(x_2d_kde.T)
print(f"2-D KDE pdf at origin: {kde_2d([0, 0])[0]:.6f}") # 0.121600

# Integrate box (1-D only)
prob_between = kde.integrate_box_1d(-1, 1)
print(f"P(-1 < X < 1) from KDE: {prob_between:.4f}") # 0.1515


# =========================================================================================
#════════════════════════  PART I — CONFIDENCE INTERVALS & RESAMPLING  ═══════════════════════════#
# =========================================================================================

##-----------##
## bootstrap ##
##-----------##
'''
stats.bootstrap(data, statistic, *, n_resamples=9999, batch=None,
                vectorized=None, paired=False, axis=0,
                confidence_level=0.95, alternative='two-sided',
                method='BCa', random_state=None) -> BootstrapResult

  Non-parametric bootstrap confidence interval for any statistic.

  data       : tuple of arrays (one per sample).
  statistic  : callable(data[0], ..., data[k], axis=axis) -> scalar or array.
  n_resamples: number of bootstrap resamples.
  paired     : if True, resample observations together across samples.
  method     : 'percentile', 'basic', or 'BCa' (bias-corrected accelerated).
               BCa is the most accurate but most expensive.

  Returns BootstrapResult with:
    .confidence_interval : ConfidenceInterval(low, high).
    .bootstrap_distribution : array of statistic values over resamples.
    .standard_error : bootstrap standard error of the statistic.
'''
print("\n=== bootstrap ===")
data_bs = (x_norm,)   # tuple of samples

# Bootstrap CI for the mean
res_bs_mean = stats.bootstrap(data_bs, statistic=np.mean, n_resamples=2000,
                              method='BCa', random_state=0)
ci_bs = res_bs_mean.confidence_interval
print(f"Bootstrap 95% CI for mean: [{ci_bs.low:.4f}, {ci_bs.high:.4f}]") # [4.5922, 5.1999]
print(f"Bootstrap SE of mean: {res_bs_mean.standard_error:.4f}") # 0.1522

# Bootstrap CI for the median (analytically hard — bootstrap shines here)
res_bs_med = stats.bootstrap(data_bs, statistic=np.median, n_resamples=2000,
                             method='BCa', random_state=0)
ci_med = res_bs_med.confidence_interval
print(f"Bootstrap 95% CI for median: [{ci_med.low:.4f}, {ci_med.high:.4f}]") # [4.3744, 5.4423]

# Two-sample bootstrap for difference of means
data_2s = (group_a, group_b)
def diff_means(x, y, axis): return np.mean(x, axis=axis) - np.mean(y, axis=axis)
res_bs_diff = stats.bootstrap(data_2s, statistic=diff_means, n_resamples=2000,
                              paired=False, method='BCa', random_state=0)
ci_diff = res_bs_diff.confidence_interval
print(f"Bootstrap CI for μ_a - μ_b: [{ci_diff.low:.4f}, {ci_diff.high:.4f}]") # [-1.2279, 0.2241]
# If CI excludes 0 → significant difference

##------------------##
## permutation_test ##
##------------------##
'''
stats.permutation_test(data, statistic, *, permutation_type='independent',
                       vectorized=None, n_resamples=9999, batch=None,
                       alternative='two-sided', axis=0, random_state=None)
  Exact or Monte Carlo permutation test for any statistic.

  data             : tuple of arrays.
  statistic        : callable(data[0], ..., axis=axis) -> scalar.
  permutation_type :
    'independent'  : randomly reassign observations to groups (two-sample test).
    'pairings'     : randomly swap paired observations.
    'samples'      : randomly negate differences (sign test variant).
  n_resamples      : number of permutations. If exhaustive is feasible, use all.
  alternative      : 'two-sided', 'less', 'greater'.

  Returns PermutationTestResult:
    .statistic              : observed statistic value.
    .pvalue                 : permutation p-value.
    .null_distribution      : array of statistic under H₀ permutations.
'''
print("\n=== permutation_test ===")
def mean_diff(x, y, axis):
    return np.mean(x, axis=axis) - np.mean(y, axis=axis)

res_pt = stats.permutation_test((group_a, group_b), mean_diff,
                                n_resamples=999, permutation_type='independent',
                                alternative='two-sided', random_state=0)
print(f"Permutation test: stat={res_pt.statistic:.4f}, p={res_pt.pvalue:.4f}") # stat=-0.4990, p=0.1740

# Sign test via 'samples' type (one-sample symmetry test)
diffs = (after - before,)
def signed_sum(d, axis): return np.sum(d > 0, axis=axis)
res_sign = stats.permutation_test(diffs, signed_sum, permutation_type='samples',
                                  n_resamples=999, alternative='greater', random_state=0)
print(f"Sign test: stat={res_sign.statistic:.0f}, p={res_sign.pvalue:.4f}") # stat=30, p=0.0010

##-----------------##
## dist.interval() ##
##-----------------##
'''
dist.interval(confidence, *args, **kwds)
  Equal-tailed interval [a, b] such that P(a ≤ X ≤ b) = confidence.
  Computed as ppf((1-confidence)/2) and ppf((1+confidence)/2).

  For Normal: this is the classical confidence interval for the DISTRIBUTION,
  not for the mean. For mean CIs use ttest_1samp or bootstrap.
'''
print("\n=== interval ===")
d_t10 = stats.t(df=10)
ci_t = d_t10.interval(0.95)
print(f"t(10) 95% interval: {np.array(ci_t).round(4)}")   # [-2.228, 2.228]

# Practical use: t-based CI for mean
n_ci = len(x_norm)
mu_ci = x_norm.mean()
se_ci = x_norm.std(ddof=1) / np.sqrt(n_ci)
t_star = stats.t.ppf(0.975, df=n_ci-1)
ci_mean = (mu_ci - t_star * se_ci, mu_ci + t_star * se_ci)
print(f"95% CI for mean of x_norm: ({ci_mean[0]:.4f}, {ci_mean[1]:.4f})") # (4.5912, 5.2077)

##-----------##
## bayes_mvs ##
##-----------##
'''
stats.bayes_mvs(data, alpha=0.90) -> (mean_ci, var_ci, std_ci)
  Bayesian credible intervals for mean, variance, and std.
  Assumes flat (non-informative) priors:
    mean  ~ N(x̄, σ²/n)  marginalised → t-distributed.
    var   ~ Inv-χ²(n-1, s²).
    std   ~ Inv-χ²-derived.
  alpha : coverage probability (e.g. 0.90 for 90% CI).

  Returns namedtuples: (center, (min_val, max_val)).
  Numerically identical to frequentist t-based intervals under flat priors.
'''
print("\n=== bayes_mvs ===")
mean_ci, var_ci, std_ci = stats.bayes_mvs(x_norm, alpha=0.95)

print(f"Bayesian mean 95% CI: center={mean_ci.statistic:.4f}, "
      f"interval={np.array(mean_ci.minmax).round(4)}")
# Bayesian mean 95% CI: center=4.8995, interval=[4.5912 5.2077]

print(f"Bayesian var  95% CI: center={var_ci.statistic:.4f}, "
      f"interval={np.array(var_ci.minmax).round(4)}")
# Bayesian var  95% CI: center=2.4627, interval=[1.8601 3.2562]

print(f"Bayesian std  95% CI: center={std_ci.statistic:.4f}, "
      f"interval={np.array(std_ci.minmax).round(4)}")
# Bayesian std  95% CI: center=1.5652, interval=[1.3639 1.8045]


# =========================================================================================
#══════════════════════════════  PART J — QUASI-MONTE CARLO  ═════════════════════════════════════#
# =========================================================================================
'''
Quasi-Monte Carlo (QMC) sequences are "low-discrepancy" — they fill the unit
hypercube more uniformly than pseudo-random numbers.

Advantages over random sampling:
  • Faster convergence: O(log(N)^d / N) vs O(1/sqrt(N)) for Monte Carlo.
  • Better space-filling: no clustering or large gaps.

Use cases: numerical integration, sensitivity analysis, surrogate modelling,
           option pricing, parameter space exploration.

All QMC engines return samples in [0, 1]^d. Use qmc.scale to map to [l, u]^d.
'''

##------------##
## qmc.Halton ##
##------------##
'''
qmc.Halton(d, scramble=True, seed=None)
  Halton sequence: uses different prime bases for each dimension.
  Deterministic (scramble=False) or scrambled (scramble=True, default).
  Good for low dimensions (d ≤ ~20); deteriorates for very high d.

  .random(n)       : generate n samples.
  .fast_forward(n) : skip the first n points (useful for batching).
  .reset()         : reset to the beginning of the sequence.
'''
print("\n=== qmc.Halton ===")
halton = qmc.Halton(d=2, scramble=True, seed=42)
H = halton.random(n=16)
print("Halton 16 samples (2-D):\n", H.round(4))
#  [[0.5513 0.1518]
#  [0.0513 0.8184]
#  [0.8013 0.4851]
#  [0.3013 0.2629]
#  [0.6763 0.9295]
#  [0.1763 0.5962]
#  [0.9263 0.0407]
#  [0.4263 0.7073]
#  [0.6138 0.374 ]
#  [0.1138 0.1888]
#  [0.8638 0.8555]
#  [0.3638 0.5221]
#  [0.7388 0.2999]
#  [0.2388 0.9666]
#  [0.9888 0.6332]
#  [0.4888 0.0777]]

disc_H = qmc.discrepancy(H)
print(f"Halton discrepancy (L2-star): {disc_H:.6f}") # 0.002367

# Compare with pure random
R = rng.uniform(size=(16, 2))
disc_R = qmc.discrepancy(R)
print(f"Random discrepancy (L2-star): {disc_R:.6f}") # 0.028178
# Halton << random discrepancy → more uniform coverage

##-----------##
## qmc.Sobol ##
##-----------##
'''
qmc.Sobol(d, scramble=True, bits=30, seed=None)
  Sobol' sequence: base-2 digital net with very low discrepancy.
  Requires n to be a power of 2 for optimal properties.
  Better than Halton for moderate dimensions (up to ~40).
  scramble=True (default): random digital shift for unbiased estimation.

  .random_base2(m) : generate exactly 2^m samples (required for optimality).
'''
print("\n=== qmc.Sobol ===")
sobol = qmc.Sobol(d=3, scramble=True, seed=42)
S = sobol.random_base2(m=4)   # 2^4 = 16 samples
print(f"Sobol 16 samples shape: {S.shape}")   # (16, 3)
print(f"Sobol discrepancy: {qmc.discrepancy(S[:, :2]):.6f}") # 0.002114

##--------------------##
## qmc.LatinHypercube ##
##--------------------##
'''
qmc.LatinHypercube(d, scramble=True, strength=1, optimization=None, seed=None)
  Latin Hypercube Sampling (LHS): divides [0,1]^d into n equal strata per
  dimension and places exactly one sample per stratum.
  Guarantees stratification along each marginal.
  strength=1: standard LHS; strength=2: orthogonal array-based LHS (better).
  optimization: None, 'random-cd' (centred discrepancy), 'lloyd'.

  .random(n) : generate n LHS samples.
'''
print("\n=== qmc.LatinHypercube ===")
lhs = qmc.LatinHypercube(d=4, seed=42)
L = lhs.random(n=20)
print(f"LHS shape: {L.shape}")   # (20, 4)
print(f"LHS discrepancy: {qmc.discrepancy(L[:, :2]):.6f}") # 0.001378

# Verify marginal stratification: each dimension has one sample per stratum
for col in range(4):
    strata = (L[:, col] * 20).astype(int)   # which of 20 strata
    assert len(np.unique(strata)) == 20, "LHS strata violated!"
print("Marginal stratification verified for all 4 dimensions.")

##-----------------##
## qmc.discrepancy ##
##-----------------##
'''
qmc.discrepancy(sample, iterative=False, method='CD', workers=1)
  Compute the discrepancy of a QMC sample (measure of uniformity).

  method : 'CD'  (centred discrepancy, default),
           'WD'  (wrap-around discrepancy),
           'MD'  (mixture discrepancy),
           'L2-star' (star discrepancy — used above).
  Lower discrepancy = more uniform distribution.

  Useful for comparing different QMC engines or tuning parameters.
'''
print("\n=== qmc.discrepancy ===")
for name, samp in [('Random',  rng.uniform(size=(64, 2))),
                   ('Halton',  qmc.Halton(d=2, seed=0).random(64)),
                   ('Sobol',   qmc.Sobol(d=2,  seed=0).random_base2(6)),
                   ('LHS',     qmc.LatinHypercube(d=2, seed=0).random(64))]:
    d_cd = qmc.discrepancy(samp, method='CD')
    print(f"  {name:<8}: CD discrepancy = {d_cd:.6f}")
  # Random  : CD discrepancy = 0.003287
  # Halton  : CD discrepancy = 0.000200
  # Sobol   : CD discrepancy = 0.000153
  # LHS     : CD discrepancy = 0.000460
# Sobol and LHS typically lowest for small n; all beat random

##-----------##
## qmc.scale ##
##-----------##
'''
qmc.scale(sample, l_bounds, u_bounds, reverse=False)
  Map QMC samples from [0, 1]^d to an arbitrary hyperbox [l, u]^d.

  sample   : (n, d) array in [0, 1]^d.
  l_bounds : (d,) lower bounds.
  u_bounds : (d,) upper bounds.
  reverse  : if True, map from [l, u] back to [0, 1] (inverse scaling).

  Necessary because all QMC engines produce samples in the unit hypercube.
'''
print("\n=== qmc.scale ===")
sobol_unit = qmc.Sobol(d=3, seed=42).random_base2(5)   # (32, 3) in [0,1]
l_bounds = np.array([-5.0, 0.0,  100.0])
u_bounds = np.array([ 5.0, 10.0, 200.0])

sobol_scaled = qmc.scale(sobol_unit, l_bounds, u_bounds)
print(f"Scaled min: {sobol_scaled.min(axis=0).round(4)}") # [-4.758200e+00  4.880000e-02  1.012702e+02]
print(f"Scaled max: {sobol_scaled.max(axis=0).round(4)}") # [  4.8274   9.7473 199.1615]
print(f"Scaled dim 0 range ≈ [-5, 5]: "
      f"{sobol_scaled[:, 0].min():.3f}  to  {sobol_scaled[:, 0].max():.3f}")
# Scaled dim 0 range ≈ [-5, 5]: -4.758  to  4.827

# Round-trip: scale then reverse-scale should recover original
sobol_back = qmc.scale(sobol_scaled, l_bounds, u_bounds, reverse=True)
print(f"Round-trip error: {np.abs(sobol_back - sobol_unit).max():.2e}") # ≈ 0


# ── End-to-end: QMC integration example ──────────────────────────────────────
print("\n=== QMC Integration Example ===")
'''
Estimate ∫₀¹ ∫₀¹ sin(πx)·sin(πy) dx dy = (2/π)² ≈ 0.40528
Compare Monte Carlo (random) vs Sobol (QMC).
'''
true_val = (2 / np.pi)**2
n_int = 1024

def integrand(pts):
    return np.prod(np.sin(np.pi * pts), axis=1)

# Monte Carlo
pts_mc  = rng.uniform(size=(n_int, 2))
est_mc  = integrand(pts_mc).mean()

# Sobol QMC
pts_qmc = qmc.Sobol(d=2, seed=42).random_base2(10)   # 2^10 = 1024
est_qmc = integrand(pts_qmc).mean()

print(f"True value  : {true_val:.6f}") # 0.405285
print(f"MC estimate : {est_mc:.6f}  (error={abs(est_mc-true_val):.2e})") # 0.393078  (error=1.22e-02)
print(f"QMC estimate: {est_qmc:.6f}  (error={abs(est_qmc-true_val):.2e})") # 0.405290  (error=5.06e-06)
# QMC typically 10-100x more accurate than MC for same n
