import numpy as np
from plotly import graph_objects as go

# =======================================
# Constant and helper functions
# =======================================

mu0 = 4*np.pi # * 1e-7
I = 5

def flatten_arrays(*args, to_list=False, unsqueeze=False):
    out = []
    for arr in args:
        out.append(
            arr.flatten().tolist() if to_list
            else arr.flatten()[:, None] if unsqueeze
            else arr.flatten()
        )
    return out

# =======================================
# p = (x, y, z) = points in the field
# =======================================

n_per_axis = 10

x, y, z = np.mgrid[-5:5:n_per_axis*1j, -5:5:n_per_axis*1j, -5:5:n_per_axis*1j]
x, y, z = flatten_arrays(x, y, z, unsqueeze=True)

# print(x.shape)
# (n_per_axis**3, 1)

# =============================================
# r = (rx, ry, rz) = segments of the coils
# a, phi and dphi for polar coordinate
# =============================================

n_coils = 5
n_line_segments = 50

a = 2
phi = np.linspace(0, 2*np.pi, n_line_segments) # (n_line_segments)
dphi = 2*np.pi / n_line_segments

phi = np.tile(phi, n_coils)[None, :] # expand phi to (1, n_line_segments*n_coils)


rx = a * np.cos(phi) # (1, n_line_segments*n_coils)
ry = a * np.sin(phi)

rz = np.linspace(-2, 2, n_coils)
rz = np.repeat(rz, n_line_segments)[None, :] # (1, n_line_segments*n_coils)

# =============================================
# R = (Rx, Ry, Rz) = p - r
# =============================================

Rx = x - rx # (n_per_axis**3, n_line_segments*n_coils)
Ry = y - ry
Rz = z - rz

R_norm = np.sqrt(Rx**2 + Ry**2 + Rz**2 + 1e-6) # (n_per_axis**3, n_line_segments*n_coils)

R = np.stack([Rx, Ry, Rz], axis=-1) # (n_per_axis**3, n_line_segments*n_coils, 3)

# =============================================
# dl = dr = (dr/dphi) * dphi
# =============================================

dlx = drx = np.gradient(rx, phi.squeeze(), axis=-1) * dphi # (1, n_line_segments*n_coils)
dly = dry = np.gradient(ry, phi.squeeze(), axis=-1) * dphi
dlz = drz = np.gradient(rz, phi.squeeze(), axis=-1) * dphi

dl = np.stack([dlx, dly, dlz], axis=-1) # (1, n_line_segments*n_coils, 3)

# =============================================
# cross product dlxR
# =============================================

dlxR = np.cross(a=dl, b=R, axisa=-1, axisb=-1) # (n_per_axis**3, n_line_segments*n_coils, 3)

# =======================================================
# B = integrate/sum over all line segments (axis=1)
# =======================================================

R_norm = R_norm[..., None] # (n_per_axis**3, n_line_segments*n_coils, 1)

B = ((mu0*I) / (4*np.pi)) * np.sum(dlxR / R_norm**3, axis=1)

Bx, By, Bz = np.unstack(B, axis=-1)

Bx = np.nan_to_num(Bx, nan=0.0, posinf=0.0, neginf=0.0)
By = np.nan_to_num(By, nan=0.0, posinf=0.0, neginf=0.0)
Bz = np.nan_to_num(Bz, nan=0.0, posinf=0.0, neginf=0.0)

##--------------##
## Plotting!!!! ##
##--------------##

x, y, z = flatten_arrays(x, y, z, to_list=True)
rx, ry, rz = flatten_arrays(rx, ry, rz, to_list=True)
Bx, By, Bz = flatten_arrays(Bx/max(Bx), By/max(By), Bz/max(Bz))

fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=rx, y=ry, z=rz,
    mode="markers+lines",
    name="Coils",
    showlegend=True,
    marker=dict(color="green"),
    line=dict(color="green")
))

fig.add_trace(go.Cone(
    x=x, y=y, z=z,
    u=Bx, v=By, w=Bz,
    showlegend=True,
    showscale=False,
    name="Magnetic field vectors"
))

# Seed points for Streamtubes (grid surrounding the loop)
x_starts, y_starts, z_starts = np.mgrid[-2:2:5j, -2:2:5j, 1:1:5j]
x_starts, y_starts, z_starts = flatten_arrays(x_starts, y_starts, z_starts, to_list=True)

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
