import numpy as np
from plotly.graph_objs import Scatter3d
import sympy as sy
from plotly import graph_objects as go
from sympy import abc, pprint

# lhs
dB = sy.symbols("dB(r)")

# rhs upper
mu0 = sy.symbols(f"{abc.mu}0")
I = sy.symbols("I")
rhs_upper = mu0 * I * sy.symbols("dlxR")
rhs_lower = 4 * sy.pi * (sy.symbols("|R|")**3)

equation = sy.Eq(
    lhs=dB,
    rhs=rhs_upper/rhs_lower
)

pprint(equation)
#         I⋅dlxR⋅μ₀
# dB(r) = ─────────
#         4⋅π⋅|R|^3
'''
We need to calculate dlxR and |R|
'''

# ========================================================================================
# Define constant and helper func
# ========================================================================================

n_points_each_axis = 10
n_line_segments = 50

def meshgrid_flatten(*args, unsqueeze=False):
    flattened = []
    for x in np.meshgrid(*args, indexing="ij"):
        flattened.append(x.flatten()[:, None] if unsqueeze else x.flatten())
    return flattened

def squeeze_tolist(*args):
    squeezed = []
    for x in args:
        squeezed.append(x.squeeze().tolist())
    return squeezed

# ========================================================================================
# Computing magnetic vector field of a circular current (loop current)
# ========================================================================================

##---------------##
## p = (x, y, z) ##
##---------------##
'''
p = (x, y, z) is the field location (the tail of the magnetic vector)
'''

x = np.linspace(-5, 5, n_points_each_axis)
y = np.linspace(-5, 5, n_points_each_axis)
z = np.linspace(-5, 5, n_points_each_axis)

x, y, z = meshgrid_flatten(x, y, z, unsqueeze=True)

print(x.shape) # [1e6, 1]

##-----------------##
## a, phi and dphi ##
##-----------------##
'''
a is the diameter of the loop
phi is the angle values from 0 to 2pi (form one full loop)
dphi is the gap between each angle value (use for integration)
'''

a = 2
phi = np.linspace(0, 2*np.pi, n_line_segments)[None, :]
dphi = 2*np.pi / n_line_segments

print(phi.shape) # [1, 180]

##------------------##
## r = (rx, ry, rz) ##
##------------------##
'''
r = (rx, ry, rz) = (a*cos(phi), a*sin(phi), 0)
denotes the locations of each segment (point) on the loop

rz = 0 means the loop is lies in the (x, y) plane
'''

rx = a * np.cos(phi)
ry = a * np.sin(phi)
rz = np.zeros_like(rx)

##--------------##
## R_norm = |R| ##
##--------------##
'''
Now what we need to calculate the vectors
that point from the each point on the loop
to each point in the field
=> call that vector R
(and that's also the R we need for the Biot-Sarvart formula)

we have:
    p = R + r
=>  R = p - r

=>  Rx = x - rx = x - a*cos(phi)
    Ry = y - ry = y - a*sin(phi)
    Rz = z - rz = z

=> R = (x - a*cos(phi), y - a*sin(phi), z)

=> R_norm = |R| = sqrt((x - a*cos(phi))**2 + (y - a*sin(phi))**2 + z**2)
'''

# R_norm = np.sqrt((x - a*np.cos(phi))**2 + (y - a*np.sin(phi))**2 + z**2)

Rx = x - rx
Ry = y - ry
Rz = z - rz

eps = 1e-3
R_norm = np.sqrt(Rx**2 + Ry**2 + Rz**2 + eps**2)

print(R_norm.shape) # [1e6, 180]

##----------------------------##
## dl = dr = (dl/dphi) * dphi ##
##----------------------------##
'''
r is the locations of each point on the loop,
when you move from one point to the very nearby point on the loop,
you move dr, hence you actualy a small fraction of the loop length dl.
(it's like the story between ds and dx)

=> dl = dr
=> dl = (dr/dphi) * dphi
=> dl = (-a*sin(phi), a*cos(phi), 0) * dphi
'''

dlx = drx = -a * np.sin(phi) * dphi
dly = dry = a * np.cos(phi) * dphi
dlz = drz = np.zeros_like(dlx)

print(dlx.shape) # (1, 180)

##--------------------##
## cross product dlxR ##
##--------------------##
'''
dl X R = [-a*sin(phi), a*cos(phi), 0] X [x - a*cos(phi), y - a*sin(phi), z] * dphi

       = |    ex                  ey              ez |
         | -a*sin(phi)        a*cos(phi)          0  |
         | x - a*cos(phi)     y - a*sin(phi)      z  |

       = [a*z*cos(phi), a*z*sin(phi), a**2 - a*(x*cos(phi) + y*sin(phi))] * dphi
'''

dlxR_x = a * z * np.cos(phi) * dphi
dlxR_y = a * z * np.sin(phi) * dphi
dlxR_z = (a**2 - a*(x*np.cos(phi) + y*np.sin(phi))) * dphi

print(dlxR_x.shape) # [1e6, 8]

##----------------------##
## Calculate Bx, By, Bz ##
##----------------------##

mu0 = 4*np.pi # *1e-7
I = 10
outer = (mu0*I) / (4*np.pi)

Bx = outer * np.sum(dlxR_x/R_norm**3, axis=1) # integrating over all the dphi
By = outer * np.sum(dlxR_y/R_norm**3, axis=1)
Bz = outer * np.sum(dlxR_z/R_norm**3, axis=1)

Bx = np.nan_to_num(Bx, nan=0.0, posinf=0.0, neginf=0.0)
By = np.nan_to_num(By, nan=0.0, posinf=0.0, neginf=0.0)
Bz = np.nan_to_num(Bz, nan=0.0, posinf=0.0, neginf=0.0)

print(Bx.shape) # (1e6,)

##--------------##
## Plotting!!!! ##
##--------------##

x, y, z = squeeze_tolist(x, y, z)
rx, ry, rz = squeeze_tolist(rx, ry, rz)
Bx, By, Bz = squeeze_tolist(Bx/max(Bx), By/max(By), Bz/max(Bz))

fig = go.Figure()

fig.add_trace(Scatter3d(
    x=rx, y=ry, z=rz,
    mode="lines",
    line=dict(width=10, color="green")
))

fig.add_trace(go.Cone(
    x=x, y=y, z=z,
    u=Bx, v=By, w=Bz,
    showlegend=True,
    showscale=False,
))

# Seed points for Streamtubes (grid surrounding the loop)
x_starts = np.linspace(-2, 2, 5)
y_starts = np.linspace(-2, 2, 5)
z_starts = np.ones_like(x_starts) # never let `z_starts = 0` !!!!!!
x_starts, y_starts, z_starts = meshgrid_flatten(x_starts, y_starts, z_starts)

# Streamtube Trace (using normalized direction vectors u_dir, v_dir, w_dir)
fig.add_trace(go.Streamtube(
    x=x, y=y, z=z,
    u=Bx, v=By, w=Bz,
    starts=dict(x=x_starts, y=y_starts, z=z_starts),
    sizeref=0.3,
    showlegend=True,
    showscale=False,
    colorscale='Jet',
    name="Magnetic Field Lines"
))

fig.show(renderer="browser")
