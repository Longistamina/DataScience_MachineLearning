'''
Packed-Array Input Functions
=============================

A "packed-array input" function is one that receives ALL its variables
bundled into a SINGLE array argument, then unpacks them inside the body:

    def f(xy):
        x, y = params          # unpack 2 variables
        return x**2 + y**2

    def f(abc):
        a, b, c = params       # unpack 3 variables
        return a*b - c

    def f(params):
        vals = params[:n]      # unpack n variables by slicing
        weights = params[n:]   # unpack the rest
        ...

This is NOT about 2-D or 3-D space specifically.
It is a SIGNATURE CONVENTION used whenever:
  • A library calls your function with a single flat array
    (scipy.optimize, scipy.integrate, scipy.linalg, curve_fit …)
  • You want one function to handle both a single input and a batch
  • You group "related variables" into one logical unit

###############################

Flow of contents:

0. The Core Pattern — pack → call → unpack

1. Unpacking Strategies
   + by name          : a, b, c = params
   + by slicing       : params[:k], params[k:]
   + by reshape       : params.reshape(r, c)
   + by index         : params[0], params[1]

2. Return Shapes
   + scalar return
   + 1-D array return (same length as input)
   + 2-D array return (Jacobian / matrix)
   + tuple return (value + gradient together)

3. Handling Variable-Length Inputs (n variables, not fixed)
   + params of length n
   + splitting into named groups

4. Vectorised Form — single point vs batch
   + np.atleast_2d trick
   + column-wise unpacking for batches

5. Defensive Patterns
   + shape validation inside the function
   + normalising input with np.asarray

6. Real scipy Use-Cases
   + scipy.optimize.minimize      (scalar objective)
   + scipy.optimize.root          (vector residual)
   + scipy.integrate.solve_ivp    (ODE state vector)
   + scipy.optimize.curve_fit     (parameter vector)
'''

import numpy as np
from scipy import optimize, integrate


#-------------------------------------------------------------------------------------------------------#
#----------------------------------- 0. The Core Pattern -----------------------------------------------#
#-------------------------------------------------------------------------------------------------------#

'''
NORMAL multi-argument function:
    def f(a, b, c):
        return a + b * c

PACKED-ARRAY equivalent:
    def f(params):
        a, b, c = params        # <-- unpack on line 1
        return a + b * c

Both compute the same thing. You use the packed form whenever a library
(or a design decision) requires exactly ONE array argument.

The caller side:
    normal form :  f(1, 2, 3)
    packed form :  f(np.array([1, 2, 3]))

The array can be any dtype, any length.
The variable names inside are just labels — params, x, state, theta,
coeffs, p … all common in practice.
'''

# Simplest possible example
def f_packed(params):
    a, b, c = params
    return a + b * c

p = np.array([1.0, 2.0, 3.0])
print(f_packed(p))   # 7.0   (1 + 2*3)

# Compare with normal form — identical result
def f_normal(a, b, c):
    return a + b * c

print(f_normal(1.0, 2.0, 3.0))   # 7.0


#------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 1. Unpacking Strategies --------------------------------------------#
#------------------------------------------------------------------------------------------------------------#

###########################
## By name (most common) ##
###########################
'''
Use when the number of variables is small and each has a clear meaning.
Python tuple unpacking: left-hand side must match length exactly.
'''

def area_of_ellipse(lw):
    '''params = [semi_major, semi_minor]'''
    a, b = lw
    return np.pi * a * b

lw = np.array([5.0, 3.0])
print(area_of_ellipse(np.array(lw)))   # 47.1239...

#-------#

def quadratic_at_x2(abc):
    '''params = [a, b, c] — evaluate ax² + bx + c at x=2.'''
    a, b, c = abc
    x = 2.0
    return a*x**2 + b*x + c

abc = np.array([1.0, -3.0, 2.0])
print(quadratic_at_x2(abc))   # 0.0  (roots at x=1 and x=2)

'''
NOTE: "lw" and "abc" are just variable names — they could be anything. 
       The unpacking pattern is the same: a, b = params or a, b, c = params.
'''

##################################
## By slicing (variable groups) ##
##################################
'''
Use when params splits naturally into two or more groups,
each with a different role, and the group size may vary.
'''

def weighted_sum(params, n_vals):
    '''
    params[:n_vals]  = values
    params[n_vals:]  = weights
    Returns the weighted sum of values.
    '''
    values  = params[:n_vals]
    weights = params[n_vals:]
    return np.dot(values, weights)

p2 = np.array([1.0, 2.0, 3.0,     # values
               0.5, 0.3, 0.2])     # weights
print(weighted_sum(p2, n_vals=3))  # 1*0.5 + 2*0.3 + 3*0.2 = 1.7

#-------#

def linear_model_residuals(params, x_data, y_data):
    '''
    params = [slope, intercept]
    Returns residuals: y_data - (slope*x + intercept)
    '''
    slope, intercept = params
    y_pred = slope * x_data + intercept
    return y_data - y_pred

x = np.array([1., 2., 3., 4., 5.])
y = np.array([2., 4., 5., 4., 5.])
weights = np.array([0.6, 2.2])

residuals = linear_model_residuals(weights, x, y)
print("Residuals:", residuals.round(3))   # [-0.8  -0.4   0.   -1.2  -0.4]

################
## By reshape ##
################
'''
Use when the packed array represents a 2-D structure
(e.g. a matrix, a list of coordinates, a weight tensor).
reshape does NOT copy data — it is just a view.
'''

def frobenius_norm(params, shape):
    '''params is a flat array; treat it as a matrix, return its norm.'''
    M = params.reshape(shape)
    return np.linalg.norm(M, 'fro')

flat = np.array([1., 2., 3., 4., 5., 6.])
print(frobenius_norm(flat, (2, 3)))   # sqrt(1+4+9+16+25+36) ≈ 9.539

#------#

def affine_transform(params, points):
    '''
    params = flat array of length 6 = [A_flat(4), b(2)]
    A is 2x2 matrix, b is 2D translation vector.
    Applies y = A @ point + b to each point.
    points: shape (k, 2)
    '''
    A = params[:4].reshape(2, 2)
    b = params[4:]
    return points @ A.T + b          # (k, 2)

pts   = np.array([[1., 0.], [0., 1.], [1., 1.]])
theta = np.pi / 4
R_flat = np.array([np.cos(theta), -np.sin(theta),
                   np.sin(theta),  np.cos(theta),
                   0., 0.])          # rotation + zero translation
print(affine_transform(R_flat, pts).round(4))
# [[ 0.7071  0.7071]
#  [-0.7071  0.7071]
#  [ 0.      1.4142]]

##############
## By index ##
##############
'''
Use for very short params (1-2 elements) or when only specific indices matter.
Less readable than name-unpacking for > 3 elements.
'''

def exponential_decay(params, t):
    '''params[0]=amplitude, params[1]=decay_rate.  f(t) = A * exp(-r*t)'''
    return params[0] * np.exp(-params[1] * t)

t_vals = np.array([0., 1., 2., 3.])
print(exponential_decay(np.array([10.0, 0.5]), t_vals).round(4))
# [10.      6.0653  3.6788  2.2313]


#------------------------------------------------------------------------------------------------------------#
#--------------------------------------- 2. Return Shapes ---------------------------------------------------#
#------------------------------------------------------------------------------------------------------------#

###################
## Scalar return ##
###################
'''
f : R^n -> R
Used as objective in minimize, as integrand in quad, as loss function.
'''

def sum_of_squares(params):
    '''f(params) = sum of squares of all elements. Minimum at origin.'''
    return np.sum(params**2)

print(sum_of_squares(np.array([1., 2., 3.])))   # 14.0
print(sum_of_squares(np.zeros(10)))              # 0.0

#------#

def log_likelihood_normal(params, data):
    '''
    params = [mu, log_sigma]  (log_sigma ensures sigma > 0 unconstrained)
    Returns negative log-likelihood of data under N(mu, sigma^2).
    '''
    mu        = params[0]
    log_sigma = params[1]
    sigma     = np.exp(log_sigma)
    n         = len(data)
    return 0.5*n*np.log(2*np.pi) + n*log_sigma + np.sum((data-mu)**2)/(2*sigma**2)

data_sample = np.array([2.1, 1.9, 2.0, 2.3, 1.8])
print(log_likelihood_normal(np.array([2.0, np.log(0.2)]), data_sample).round(4))
# -1.5775

######################
## 1-D array return ##
######################
'''
f : R^n -> R^m
Used as residual in least_squares, as RHS in root, as dy/dt in solve_ivp.
Output length can differ from input length.
'''

def polynomial_residuals(params, x_data, y_data):
    '''
    params = [a0, a1, a2, ...] polynomial coefficients (lowest power first).
    Returns residuals: y_data - polynomial(x_data).
    '''
    y_pred = np.polyval(params[::-1], x_data)   # polyval uses highest-first order
    return y_data - y_pred

x_d = np.linspace(0, 2, 6)
y_d = 1 + 2*x_d + 0.5*x_d**2 + np.random.default_rng(1).normal(0, 0.05, 6)
res = polynomial_residuals(np.array([1., 2., 0.5]), x_d, y_d)
print("Poly residuals:", res.round(4))   # small numbers near 0
# Poly residuals: [ 0.0173  0.0411  0.0165 -0.0652  0.0453  0.0223]

#-----#

def system_of_equations(params):
    '''
    params = [x, y, z]
    Returns [F1, F2, F3] — residuals of a 3-equation nonlinear system.
    Used with scipy.optimize.root.
    '''
    x, y, z = params
    F1 = x**2 + y**2 + z**2 - 1      # unit sphere
    F2 = x + y - z                    # plane 1
    F3 = x - y + 2*z - 1             # plane 2
    return np.array([F1, F2, F3])

print(system_of_equations(np.array([1., 0., 1.])))   # some nonzero residuals
# [1. 0. 2.]

######################
## 2-D array return ##
######################
'''
f : R^n -> R^(n x n)
Used as Jacobian in root/minimize, as covariance, as sensitivity matrix.
'''

def jacobian_of_system(params):
    '''
    Analytical Jacobian of system_of_equations above.
    Returns shape (3, 3): J[i, j] = dFi / d(params[j]).
    '''
    x, y, z = params
    return np.array([[2*x,  2*y,  2*z],   # dF1/d(x,y,z)
                     [1,    1,    -1  ],   # dF2/d(x,y,z)
                     [1,    -1,   2   ]])  # dF3/d(x,y,z)

print(jacobian_of_system(np.array([0.5, 0.5, 0.5])))
# [[1.  1.  1.]
#  [1.  1. -1.]
#  [1. -1.  2.]]

##################
## Tuple return ##
##################
'''
Some APIs accept a function that returns (value, gradient) together,
saving one extra function call.
'''

def with_gradient(params):
    '''Returns (scalar_value, gradient_array) together.'''
    val  = np.sum(params**2)
    grad = 2 * params
    return val, grad

val, grad = with_gradient(np.array([1., 2., 3.]))
print(f"value={val}, grad={grad}")   # value=14.0, grad=[2. 4. 6.]


#------------------------------------------------------------------------------------------------------------#
#------------------------ 3. Handling Variable-Length Inputs (n variables, not fixed) -----------------------#
#------------------------------------------------------------------------------------------------------------#

'''
When the number of variables is not known at definition time, you use
len(params), loops, or slicing arithmetic to handle any length.
'''

def generalised_power_sum(params):
    '''
    params = [v1, v2, ..., vn, exponent]
    Returns sum(vi ** exponent) for i in 1..n.
    Works for any n >= 1.
    '''
    exponent = params[-1]       # last element is always the exponent
    values   = params[:-1]      # everything before it are the values
    return np.sum(values ** exponent)

print(generalised_power_sum(np.array([1., 2., 3., 2.])))         # 1+4+9=14   (exp=2)
print(generalised_power_sum(np.array([1., 2., 3., 4., 5., 3.]))) # 1+8+27+64+125=225 (exp=3)

#------#

def named_groups(params, group_sizes):
    '''
    Split params into named groups by their sizes.
    group_sizes: dict like {'weights': 3, 'biases': 2, 'scale': 1}
    Returns a dict mapping each name to its slice of params.
    '''
    result = {}
    cursor = 0
    for name, size in group_sizes.items():
        result[name] = params[cursor : cursor + size]
        cursor += size
    return result

flat_params = np.array([0.1, 0.2, 0.3,    # weights (3)
                        0.5, 0.6,          # biases  (2)
                        2.0])              # scale   (1)

groups = named_groups(flat_params, {'weights': 3, 'biases': 2, 'scale': 1})
print("weights:", groups['weights'])   # [0.1 0.2 0.3]
print("biases :", groups['biases'])    # [0.5 0.6]
print("scale  :", groups['scale'])     # [2.0]


#------------------------------------------------------------------------------------------------------------#
#----------------------------- 4. Vectorised Form — single point vs batch -----------------------------------#
#------------------------------------------------------------------------------------------------------------#

'''
A function written for ONE packed input can be extended to handle a
BATCH of packed inputs by changing how it unpacks.

Single point:  params shape (n,)    →  extract scalars by name
Batch:         params shape (k, n)  →  extract columns by index

The np.atleast_2d trick lets you write ONE function that handles both.
'''

###################################################
## np.atleast_2d + column-slice = works for both ##
###################################################

def gaussian_pdf(params):
    '''
    params = [x, mu, sigma]  — shape (3,) or (k, 3)
    Returns scalar or (k,) array of Gaussian density values.
    '''
    params = np.atleast_2d(params)    # always (k, 3) now
    x     = params[:, 0]
    mu    = params[:, 1]
    sigma = params[:, 2]
    pdf   = np.exp(-0.5 * ((x - mu) / sigma)**2) / (sigma * np.sqrt(2 * np.pi))
    return pdf.squeeze()              # back to scalar if k=1

# Single point — returns scalar
print(gaussian_pdf(np.array([0.0, 0.0, 1.0])).round(6))   # 0.398942

# Batch of 4 points — returns (4,) array — SAME function call
batch_params = np.array([[0.0, 0.0, 1.0],
                         [1.0, 0.0, 1.0],
                         [2.0, 2.0, 0.5],
                         [-1., 0.0, 2.0]])
print(gaussian_pdf(batch_params).round(6))
# [0.398942  0.241971  0.797885  0.176033]

##################################################
## Loop-based vectorisation (clear alternative) ##
##################################################

def apply_to_batch(f_single, batch):
    '''
    Apply a single-point packed function to each row of a batch.
    batch: shape (k, n). f_single expects shape (n,).
    '''
    return np.array([f_single(row) for row in batch])

def entropy(params):
    '''params = probability vector. Returns Shannon entropy (nats).'''
    p = np.asarray(params)
    p = p[p > 0]
    return -np.sum(p * np.log(p))

distributions = np.array([[0.25, 0.25, 0.25, 0.25],   # uniform  — max entropy
                          [1.00, 0.00, 0.00, 0.00],   # certain  — zero entropy
                          [0.50, 0.25, 0.25, 0.00],   # mixed
                          [0.70, 0.20, 0.10, 0.00]])  # skewed

entropies = apply_to_batch(entropy, distributions)
print("Entropies:", entropies.round(4))
# [1.3863  0.      1.0397  0.8018]


#------------------------------------------------------------------------------------------------------------#
#-------------------------------------- 5. Defensive Patterns -----------------------------------------------#
#------------------------------------------------------------------------------------------------------------#
'''
Two things to add when your packed function will be called by external code
(library callbacks, user-facing APIs):
  1. np.asarray  — accepts lists, tuples, or ndarrays cleanly
  2. Shape check — fail early with a clear message
'''

######################################
## np.asarray — normalise the input ##
######################################

def safe_sum_of_squares(params):
    '''Accepts list, tuple, or ndarray — always converts first.'''
    params = np.asarray(params, dtype=float)
    return np.sum(params**2)

print(safe_sum_of_squares([1, 2, 3]))               # 14.0  (list)
print(safe_sum_of_squares((1.0, 2.0, 3.0)))         # 14.0  (tuple)
print(safe_sum_of_squares(np.array([1., 2., 3.])))  # 14.0  (ndarray)

##############################
## Shape check — fail early ##
##############################

def validated_quadratic(params):
    '''
    params must be exactly length 3: [a, b, c].
    Evaluates ax^2 + bx + c at x=1.
    '''
    params = np.asarray(params, dtype=float)
    if params.shape != (3,):
        raise ValueError(
            f"params must have shape (3,), got {params.shape}. "
            f"Expected [a, b, c]."
        )
    a, b, c = params
    return a + b + c    # at x=1: a*1^2 + b*1 + c

print(validated_quadratic([1., 2., 3.]))   # 6.0

try:
    validated_quadratic([1., 2.])          # wrong length
except ValueError as e:
    print(f"ValueError: {e}")
# ValueError: params must have shape (3,), got (2,). Expected [a, b, c].


#------------------------------------------------------------------------------------------------------------#
#---------------------------------- 6. Real scipy Use-Cases -------------------------------------------------#
#------------------------------------------------------------------------------------------------------------#

#############################
## scipy.optimize.minimize ##
#############################
'''
minimize(fun, x0) calls fun(params) expecting a SCALAR return.
jac(params) is called for the gradient — returns 1-D array same length as params.
'''

def bowl(params):
    '''Quadratic bowl: sum of weighted squares. Minimum at origin.'''
    weights = np.array([1.0, 4.0, 9.0])
    return np.sum(weights * params**2)

def bowl_gradient(params):
    weights = np.array([1.0, 4.0, 9.0])
    return 2 * weights * params

res = optimize.minimize(bowl, x0=np.array([2., 2., 2.]),
                        jac=bowl_gradient, method='L-BFGS-B')
print("\n--- scipy.optimize.minimize ---")
print(f"minimum at : {res.x.round(8)}")   # [0. 0. 0.]
print(f"value      : {res.fun:.2e}")       # ≈ 0

#########################
## scipy.optimize.root ##
#########################
'''
root(fun, x0) calls fun(params) expecting a 1-D RESIDUAL ARRAY.
Both input and output have the same length (n equations, n unknowns).
'''

def nonlinear_system(params):
    '''
    3-equation nonlinear system:
      x^2  + y  + z  = 6
      x    + y^2 + z  = 6
      x    + y  + z^2 = 6
    One real solution: (2, 2, 0) and permutations.
    '''
    x, y, z = params
    return np.array([x**2 + y   + z   - 6,
                     x   + y**2 + z   - 6,
                     x   + y   + z**2 - 6])

sol = optimize.root(nonlinear_system, x0=np.array([1., 1., 1.]))
print("\n--- scipy.optimize.root ---")
print(f"solution : {sol.x.round(6)}") # [1.645751 1.645751 1.645751
print(f"residual : {nonlinear_system(sol.x).round(10)}")   # [0. 0. 0.]

###############################
## scipy.integrate.solve_ivp ##
###############################
'''
solve_ivp(fun, t_span, y0) calls fun(t, state) where state is a 1-D array.
The function returns d(state)/dt — same shape as state.

The state vector packs all dynamic quantities together:
  state  = [quantity_1,       quantity_2,       ...]
  return = [d(quantity_1)/dt, d(quantity_2)/dt, ...]
'''

def predator_prey(t, state):
    '''
    Lotka-Volterra equations.
    state = [prey_population, predator_population]
    '''
    prey, predator = state
    alpha, beta, delta, gamma = 1.0, 0.1, 0.075, 1.5
    d_prey     = alpha * prey      - beta  * prey * predator
    d_predator = delta * prey * predator - gamma * predator
    return np.array([d_prey, d_predator])

sol_ode = integrate.solve_ivp(predator_prey,
                              t_span=(0, 15),
                              y0=np.array([10.0, 5.0]),
                              max_step=0.1)
print("\n--- scipy.integrate.solve_ivp (Lotka-Volterra) ---")
print(f"Time steps     : {len(sol_ode.t)}") # 152
print(f"Final prey     : {sol_ode.y[0, -1]:.4f}") # 9.7800
print(f"Final predators: {sol_ode.y[1, -1]:.4f}") # 17.1666

##############################
## scipy.optimize.curve_fit ##
##############################
'''
curve_fit(f, xdata, ydata) calls f(xdata, *params).
Your function lists the parameters after x — the optimiser packs and
unpacks them as a flat vector internally.  Same spirit: all free parameters
controlled through one flat array.
'''

def damped_sine(t, amplitude, decay, frequency, phase):
    '''
    Damped sinusoid: amplitude * exp(-decay*t) * sin(frequency*t + phase).
    amplitude, decay, frequency, phase are the packed unknowns.
    '''
    return amplitude * np.exp(-decay * t) * np.sin(frequency * t + phase)

t_data  = np.linspace(0, 4, 80)
y_true  = damped_sine(t_data, 3.0, 0.5, 4.0, 0.3)
y_noisy = y_true + np.random.default_rng(42).normal(0, 0.1, len(t_data))

popt, _ = optimize.curve_fit(damped_sine, t_data, y_noisy,
                             p0=[2.0, 1.0, 3.0, 0.0], maxfev=5000)
print("\n--- scipy.optimize.curve_fit (damped sine) ---")
for name, true, fitted in zip(['amplitude','decay','frequency','phase'],
                               [3.0, 0.5, 4.0, 0.3], popt):
    print(f"  {name:<12}: true={true:.2f}  fitted={fitted:.4f}")
#   amplitude   : true=3.00  fitted=2.9729
#   decay       : true=0.50  fitted=0.4950
#   frequency   : true=4.00  fitted=4.0015
#   phase       : true=0.30  fitted=0.2956