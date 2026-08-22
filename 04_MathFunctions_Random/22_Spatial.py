'''
scipy.spatial  —  Spatial Algorithms, Transforms & Distances
==============================================================

Covers three sub-namespaces in a logical build-up order:
  • scipy.spatial.transform  — 3-D rotation objects and interpolation
  • scipy.spatial            — KD-trees, Delaunay, ConvexHull, Voronoi, utilities
  • scipy.spatial.distance   — pairwise distance computation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART A — ROTATION  (scipy.spatial.transform)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. Rotation.from_euler / from_quat / from_rotvec / from_matrix
 2. Rotation.as_euler / as_quat / as_rotvec / as_matrix
 3. Rotation.apply / inv / magnitude / mean / concatenate
 4. Rotation.identity / random

PART B — ROTATION INTERPOLATION  (scipy.spatial.transform)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 5. Slerp                            : spherical linear interpolation
 6. RotationSpline                   : smooth cubic rotation spline

PART C — KD-TREE  (scipy.spatial)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 7. KDTree / cKDTree                 : build & nearest-neighbour queries
 8. .query                           : k nearest neighbours
 9. .query_ball_point                : all points within radius r
10. .query_pairs                     : all pairs within distance r
11. .count_neighbors                 : pair counts vs radius (RDF)
12. .sparse_distance_matrix          : sparse distance matrix

PART D — DELAUNAY TRIANGULATION  (scipy.spatial)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
13. Delaunay                         : tessellation, simplices, neighbours
14. .find_simplex                    : locate which triangle contains a point
15. .transform / .equations          : barycentric coordinates, hyperplane
16. tsearch                          : functional simplex search

PART E — CONVEX HULL  (scipy.spatial)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
17. ConvexHull                       : vertices, simplices, equations
18. .area / .volume                  : surface area and enclosed volume
19. Point-in-hull membership test

PART F — VORONOI DIAGRAMS  (scipy.spatial)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
20. Voronoi                          : vertices, regions, ridges
21. SphericalVoronoi                 : Voronoi on the sphere surface

PART G — HALFSPACE INTERSECTION  (scipy.spatial)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
22. HalfspaceIntersection            : feasible region from linear inequalities

PART H — UTILITY FUNCTIONS  (scipy.spatial)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
23. procrustes                       : optimal rigid alignment of two point sets
24. geometric_slerp                  : spherical linear interpolation of points
25. distance_matrix / minkowski_distance : dense pairwise distance matrices

PART I — PAIRWISE DISTANCE COMPUTATION  (scipy.spatial.distance)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
26. cdist                            : all pairs between two collections
27. pdist                            : all pairs within one collection
28. squareform                       : condense ↔ square matrix conversion

PART J — CONTINUOUS VECTOR DISTANCES  (scipy.spatial.distance)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
29. euclidean / sqeuclidean          : L2 and squared-L2
30. minkowski / cityblock / chebyshev: Lp family
31. cosine / correlation             : angle-based distances
32. mahalanobis / seuclidean         : distribution-aware distances
33. jensenshannon / directed_hausdorff : divergence-based and set distances

PART K — BOOLEAN / SET DISTANCES  (scipy.spatial.distance)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
34. hamming / jaccard / dice         : overlap-based distances
35. rogerstanimoto / russellrao / sokalmichener / sokalsneath : association metrics
36. yule / kulczynski1               : additional boolean metrics
'''

import numpy as np
from scipy.spatial.transform import Rotation, Slerp, RotationSpline
from scipy.spatial import (
    KDTree, cKDTree, Rectangle,
    Delaunay, ConvexHull, Voronoi, SphericalVoronoi, HalfspaceIntersection,
    tsearch, distance_matrix, minkowski_distance, minkowski_distance_p,
    procrustes, geometric_slerp,
)
from scipy.spatial.distance import (
    cdist, pdist, squareform,
    euclidean, sqeuclidean,
    minkowski, cityblock, chebyshev,
    cosine, correlation,
    mahalanobis, seuclidean,
    jensenshannon, directed_hausdorff,
    hamming, jaccard, dice,
    rogerstanimoto, russellrao, sokalmichener, sokalsneath,
    yule, kulczynski1,
)

rng = np.random.default_rng(42)

# ── Common test point clouds ──────────────────────────────────────────────────
pts_2d  = rng.uniform(0, 10, (20, 2))     # 20 random 2-D points
pts_3d  = rng.uniform(0, 10, (30, 3))     # 30 random 3-D points
pts_unit = pts_3d / np.linalg.norm(pts_3d, axis=1, keepdims=True)  # on unit sphere


# =========================================================================================
#  PART A — ROTATION  (scipy.spatial.transform) 
# =========================================================================================

##----------##
## Rotation ##
##----------##
'''
Rotation is the central class in scipy.spatial.transform.
It wraps one or more 3-D rotations and supports multiple representations:

  Euler angles   : from_euler(seq, angles, degrees=False)
  Quaternions    : from_quat([x, y, z, w])     # scalar-last convention
  Rotation vector: from_rotvec(vec)            # axis * angle (radians)
  Rotation matrix: from_matrix(R)              # 3x3 orthogonal matrix

Scalar/array: pass a single angle or an array of angles to get a
single Rotation or a "stacked" Rotation of shape (N,).

Key properties:
  Rotation.single : True if this is a scalar (non-stacked) rotation.
  len(r)          : number of rotations in a stacked object.
'''

# ── Construction ─────────────────────────────────────────────────────────────

## from_euler
# seq:  'x','y','z'  — intrinsic axes (body-fixed, lower-case)
#        'X','Y','Z' — extrinsic axes (space-fixed, upper-case)
# Each letter specifies one rotation axis; multiple letters chain them.

r_z90 = Rotation.from_euler('z', 90, degrees=True)   # 90° around z
r_xyz = Rotation.from_euler('xyz', [30, 45, 60], degrees=True)   # roll-pitch-yaw

# Stack: array of angles -> stacked Rotation
angles_stack = np.array([[0, 0, 0], [90, 0, 0], [0, 90, 0]])
r_stack = Rotation.from_euler('xyz', angles_stack, degrees=True)
print(f"Stacked rotation count: {len(r_stack)}")   # 3

## from_quat  [x, y, z, w]  — scalar LAST
# Unit quaternion (x,y,z,w) with w = cos(θ/2), (x,y,z) = sin(θ/2)*axis
q_vec = np.array([0.0, 0.0, np.sin(np.pi/4), np.cos(np.pi/4)])   # 90° around z
r_quat = Rotation.from_quat(q_vec)
print(f"Quaternion rotation angle: {r_quat.magnitude() * 180/np.pi:.2f}°")   # 90.00°

# normalize=True (default) normalises |q|=1; useful if quaternion is noisy
q_unnorm = np.array([0.0, 0.0, 0.71, 0.71])   # slightly off-unit
r_norm = Rotation.from_quat(q_unnorm)          # auto-normalised

## from_rotvec
# Rotation vector: direction = axis, magnitude = angle in radians
rotvec_z90 = np.array([0.0, 0.0, np.pi/2])     # 90° around z-axis
r_rv = Rotation.from_rotvec(rotvec_z90)
print(f"Rotvec magnitude: {r_rv.magnitude():.4f} rad = {r_rv.magnitude()*180/np.pi:.2f}°")
# 1.5708 rad = 90.00°

# Small-angle: from_rotvec is numerically stable near zero
r_tiny = Rotation.from_rotvec([1e-9, 0, 0])
print(f"Tiny rotation: {r_tiny.magnitude():.2e} rad")   # 1.00e-09 rad

## from_matrix  (3×3 rotation matrix)
theta = np.pi / 3   # 60°
R_mat = np.array([
    [ np.cos(theta), -np.sin(theta), 0],
    [ np.sin(theta),  np.cos(theta), 0],
    [            0,              0,  1],
])
r_mat = Rotation.from_matrix(R_mat)
print(f"Matrix rotation (60° around z): {r_mat.as_euler('zxz', degrees=True)[0].round(4)}°")
# Matrix rotation (60° around z): 60.0°

## identity / random
r_id  = Rotation.identity()                          # no rotation
r_rnd = Rotation.random(5, random_state=rng)         # 5 uniformly random rotations
print(f"Random rotation magnitudes: {r_rnd.magnitude().round(3)}")
# Random rotation magnitudes: [1.427 2.02  1.288 2.918 2.887]


# ── Conversion between representations ───────────────────────────────────────

r_test = Rotation.from_euler('xyz', [30, 45, 60], degrees=True)

q_out  = r_test.as_quat()           # (x, y, z, w)
rv_out = r_test.as_rotvec()         # axis*angle vector
M_out  = r_test.as_matrix()         # 3×3 matrix
e_out  = r_test.as_euler('xyz', degrees=True)  # back to Euler

print("as_quat()  :", q_out.round(4))        # [0.0223 0.4397 0.3604 0.8224]
print("as_rotvec():", rv_out.round(4))       # [0.0474 0.9354 0.7668] (axis*angle)
print("as_euler() :", e_out.round(2))        # [30. 45. 60.]

# Round-trip: euler -> matrix -> euler should recover original angles
r_rt = Rotation.from_matrix(r_test.as_matrix())
print(np.allclose(r_rt.as_euler('xyz', degrees=True), [30, 45, 60]))   # True


# ── Applying rotations ────────────────────────────────────────────────────────
'''
r.apply(vectors, inverse=False)
  Rotates an array of 3-D vectors by this rotation.
  If r is stacked (N rotations) and vectors is (N,3), applies each rotation
  to the corresponding vector (broadcast). If vectors is (3,), applies all N
  rotations to the same vector.

r.inv()  : returns the inverse rotation (= transpose of rotation matrix).
'''

v = np.array([1.0, 0.0, 0.0])   # unit x-vector
r_z90_result = r_z90.apply(v)
print("Rotate x by 90° around z:", r_z90_result.round(6))   # [0. 1. 0.]

# Inverse rotation: un-rotate
v_back = r_z90.inv().apply(r_z90_result)
print("Inverse rotation back  :", v_back.round(6))   # [1. 0. 0.]

# Rotate multiple vectors at once
vs = np.eye(3)   # [x, y, z] unit vectors
rotated = r_z90.apply(vs)
print("Rotate all three axes by 90° around z:\n", rotated.round(6))
# [[ 0  1  0]   <- x becomes y
#  [-1  0  0]   <- y becomes -x
#  [ 0  0  1]]  <- z unchanged

# Stacked: apply each rotation to one vector
v_single = np.array([1.0, 0.0, 0.0])
results = r_stack.apply(v_single)   # shape (3, 3): one result per rotation
print("Stacked apply results shape:", results.shape)   # (3, 3)


# ── Composition, magnitude, mean ─────────────────────────────────────────────
'''
r1 * r2           : compose rotations (apply r2 first, then r1).
                    Uses __mul__ overload — equivalent to r1.apply(r2.apply(v)).
r.magnitude()     : angle of rotation in radians. Scalar or array.
r.mean(weights=None) : chordal L2 mean rotation (Fréchet mean on SO(3)).
Rotation.concatenate([r1, r2, ...]) : stack multiple Rotation objects.
'''

r_a = Rotation.from_euler('z', 45, degrees=True)
r_b = Rotation.from_euler('x', 30, degrees=True)

r_composed = r_a * r_b   # first rotate by b (x 30°), then by a (z 45°)
print(f"Composed magnitude: {r_composed.magnitude()*180/np.pi:.2f}°") # 53.65°

# Mean of a cluster of rotations
r_cluster = Rotation.from_euler('z', [10, 12, 11, 9, 10], degrees=True)
r_mean = r_cluster.mean()
print(f"Mean angle: {r_mean.as_euler('zyx', degrees=True)[0]:.2f}°")   # ≈ 10.4°

# Concatenate stacked rotations
r_all = Rotation.concatenate([r_a, r_b, r_composed])
print(f"Concatenated length: {len(r_all)}")   # 3


# =========================================================================================
#  PART B — ROTATION INTERPOLATION  (scipy.spatial.transform) 
# =========================================================================================

##-------##
## Slerp ##
##-------##
'''
Slerp(times, rotations)
  Spherical Linear intERPolation between a sequence of key-frame rotations.

  times     : 1-D array of key-frame timestamps (monotonically increasing).
  rotations : stacked Rotation of the same length as times.

  slerp(t)  : interpolate at new times t (must lie within [times[0], times[-1]]).

  Slerp traces the shortest geodesic arc on SO(3) between each pair of key frames.
  The angular velocity is constant within each segment (unlike Euler spline).
  Use RotationSpline for C2-smooth interpolation.
'''

key_times = np.array([0.0, 1.0, 2.0, 3.0])
key_rots  = Rotation.from_euler('z', [0, 90, 0, -90], degrees=True)

slerp_fn = Slerp(key_times, key_rots)

# Evaluate at intermediate times
t_interp = np.linspace(0, 3, 13)
r_interp  = slerp_fn(t_interp)
angles_interp = r_interp.as_euler('zyx', degrees=True)[:, 0]   # z component
print("Slerp z-angles at t:", angles_interp.round(1))
# [  0.  22.5  45.  67.5  90.  67.5  45.  22.5  0.  -22.5 -45.  -67.5 -90.]

# Verify key-frame values are exact
r_at_keys = slerp_fn(key_times)
print(np.allclose(r_at_keys.as_euler('zyx', degrees=True)[:, 0], [0, 90, 0, -90], atol=1e-10))
# True

# Slerp of 3-D rotations (not just z-axis)
key_rots_3d = Rotation.from_euler('xyz', [[0,0,0], [90,0,0], [0,90,0], [0,0,90]], degrees=True)
slerp_3d = Slerp(key_times, key_rots_3d)
r_mid = slerp_3d(1.5)   # halfway between frame 1 and 2
print(f"3-D slerp at t=1.5 magnitude: {r_mid.magnitude()*180/np.pi:.2f}°") # 70.53°

##----------------##
## RotationSpline ##
##----------------##
'''
RotationSpline(times, rotations)
  Cubic rotation spline with C2 continuity (smooth angular velocity and acceleration).
  Constructed from key-frame rotations; uses cubic Hermite interpolation in so(3).

  spline(t)               : interpolated Rotation at times t.
  spline(t, order=1)      : angular velocity vector at times t  (shape (..., 3)).
  spline(t, order=2)      : angular acceleration vector at times t.

  Prefer over Slerp when you need smooth angular velocity (e.g. camera paths, robot joints).
'''

rs = RotationSpline(key_times, key_rots_3d)

t_fine = np.linspace(0, 3, 61)
r_fine = rs(t_fine)

# Angular velocity (rad/s)
omega = rs(t_fine, order=1)   # shape (61, 3)
print("Angular velocity shape:", omega.shape)   # (61, 3)
print("Max |ω| :", np.linalg.norm(omega, axis=1).max().round(4)) # 2.684

# Angular acceleration
alpha = rs(t_fine, order=2)   # shape (61, 3)
print("Max |α| :", np.linalg.norm(alpha, axis=1).max().round(4)) # 7.293

# Spline passes through key frames exactly
print(np.allclose(rs(key_times).as_euler('xyz', degrees=True),
                  key_rots_3d.as_euler('xyz', degrees=True), atol=1e-10))   # True


# =========================================================================================
#  PART C — KD-TREE  (scipy.spatial) 
# =========================================================================================

##------------------------##
## KDTree / cKDTree build ##
##------------------------##
'''
KDTree(data, leafsize=10, compact_nodes=True, copy_data=False,
       balanced_tree=True, boxsize=None)
  kd-tree for O(log N) nearest-neighbour queries in d dimensions.

  data      : (N, d) array of N points in d-dimensional space.
  leafsize  : max points per leaf node. Default 10 is good in practice.
  compact_nodes: use tighter bounding boxes (slower build, faster query).
  balanced_tree: build a balanced tree (slower build, more predictable query).
  boxsize   : if provided, use toroidal (periodic) boundary conditions.

cKDTree  : C-implemented version — same API, much faster for large datasets.
           cKDTree is preferred in almost all cases.

Both support the same query methods. Choose KDTree only when you need
pure-Python subclassing.
'''

tree = cKDTree(pts_2d)          # build in 2-D
print(f"KDTree: {len(pts_2d)} points, leafsize=10") # 20 points, leafsize=10

# Periodic boundary (box = [10, 10])
tree_periodic = cKDTree(pts_2d, boxsize=[10.0, 10.0])

##----------##
## .query() ##
##----------##
'''
tree.query(x, k=1, eps=0, p=2, distance_upper_bound=np.inf, workers=1)
  Find the k nearest neighbours of query point(s) x.

  x    : (d,) or (M, d) — one or many query points.
  k    : number of neighbours to return.
  eps  : approximate query — neighbour within (1+eps) * true_distance. Faster.
  p    : Minkowski p-norm (p=2 Euclidean, p=1 Manhattan, p=inf Chebyshev).
  distance_upper_bound : ignore neighbours farther than this distance.
  workers : number of threads (-1 = all available).

  Returns:
    dd : (M, k) distances to the k nearest neighbours.
    ii : (M, k) indices into tree.data of those neighbours.
  For k=1, shapes are (M,) and (M,).
'''

query_pt = np.array([5.0, 5.0])

# Single nearest neighbour
dd1, ii1 = tree.query(query_pt, k=1)
print(f"Nearest neighbour: index={ii1}, dist={dd1:.4f}, point={pts_2d[ii1].round(4)}")
# Nearest neighbour: index=16, dist=2.1707, point=[3.2583 3.7046]

# 3 nearest neighbours
dd3, ii3 = tree.query(query_pt, k=3)
print(f"3-NN distances: {dd3.round(4)}") # [2.1707 2.7857 2.8069]
print(f"3-NN indices  : {ii3}") # [16  7  0]

# Batch query: many points at once
queries = np.array([[2.0, 2.0], [8.0, 8.0], [5.0, 0.0]])
dd_batch, ii_batch = tree.query(queries, k=2)
print("Batch 2-NN distances:\n", dd_batch.round(4))
#  [[2.1187 2.4493]
#  [0.4128 1.1818]
#  [0.5501 0.8398]]

# Approximate query (eps=0.1): up to 10% error, can be faster on high-d data
dd_approx, ii_approx = tree.query(query_pt, k=3, eps=0.1)

# Manhattan distance (p=1)
dd_l1, ii_l1 = tree.query(query_pt, k=3, p=1)
print(f"L1 3-NN distances: {dd_l1.round(4)}") # [3.0371 3.2935 3.3508]

# Upper bound: only return neighbours within distance 2.0
dd_ub, ii_ub = tree.query(query_pt, k=5, distance_upper_bound=2.0)
valid = ii_ub < len(pts_2d)   # inf entries mark "no neighbour within bound"
print(f"Neighbours within r=2: {valid.sum()}") # 0

##---------------------##
## .query_ball_point() ##
##---------------------##
'''
tree.query_ball_point(x, r, p=2, eps=0, workers=1, return_sorted=False)
  Find all points within distance r of query point(s) x.

  x : (d,) single point or (M, d) array of M points.
  r : radius (scalar or array of length M for per-point radii).

  Returns:
    list of arrays (if x is 1-D): indices of points within r.
    list of lists  (if x is 2-D): one list of indices per query point.

  O(N * r^d / V) on average — efficient for small r relative to data extent.
'''

# All points within distance 3 of query_pt
idx_ball = tree.query_ball_point(query_pt, r=3.0)
print(f"Points within r=3 of (5,5): {len(idx_ball)} points, indices={idx_ball}")
# Points within r=3 of (5,5): 4 points, indices=[0, 16, 10, 7]

# Different radius for each query point
r_per_point = np.array([1.0, 3.0, 2.0])
idx_multi = tree.query_ball_point(queries, r=r_per_point)
for i, (q, r, idx) in enumerate(zip(queries, r_per_point, idx_multi)):
    print(f"  query {q}, r={r}: {len(idx)} neighbours")
  # query [2. 2.], r=1.0: 0 neighbours
  # query [8. 8.], r=3.0: 6 neighbours
  # query [5. 0.], r=2.0: 3 neighbours

##----------------##
## .query_pairs() ##
##----------------##
'''
tree.query_pairs(r, p=2, eps=0, output_type='set')
  Find all pairs of points within distance r of each other.

  Returns a set of (i, j) pairs with i < j.
  Equivalent to: {(i,j) for i in range(N) for j in range(i+1,N) if dist(i,j) <= r}
  but O(N log N) rather than O(N²).

  output_type : 'set' (default) or 'ndarray' for (M, 2) index matrix.
  Useful for: building proximity graphs, molecular dynamics cutoff lists.
'''

pairs = tree.query_pairs(r=2.0)
print(f"Pairs within r=2.0: {len(pairs)} pairs") # 17 pairs

# As array for easy indexing
pairs_arr = tree.query_pairs(r=2.0, output_type='ndarray')
print("Pairs array shape:", pairs_arr.shape)   # (M, 2) (or 17x2)

# Compute all those pairwise distances
if len(pairs_arr) > 0:
    dists_pairs = np.linalg.norm(pts_2d[pairs_arr[:, 0]] - pts_2d[pairs_arr[:, 1]], axis=1)
    print(f"All pair distances ≤ 2.0: max={dists_pairs.max():.4f}")   # ≤ 2.0
# All pair distances ≤ 2.0: max=1.9765

##--------------------##
## .count_neighbors() ##
##--------------------##
'''
tree.count_neighbors(other, r, p=2, weights=None, cumulative=True)
  Count pairs (i from self, j from other) with dist(i,j) <= r.

  other     : another KDTree (can be self for auto-correlations).
  r         : scalar or array of radii.
  cumulative: if True, return cumulative count N(r).
              if False, return count in annulus (r_prev, r].
  weights   : per-point weights for weighted counts.

  Used for: radial distribution function (RDF), correlation functions,
            2-point statistics in cosmology and materials science.
'''

radii = np.array([0.5, 1.0, 2.0, 3.0, 5.0])
counts_cum  = tree.count_neighbors(tree, radii)            # cumulative
counts_ann  = tree.count_neighbors(tree, radii, cumulative=False)  # per annulus
print("Cumulative pair counts:", counts_cum) # [ 24  32  54 100 172]
print("Annular pair counts   :", counts_ann) # [24  8 22 46 72]

# Two-tree version: count pairs between two different sets
tree2 = cKDTree(rng.uniform(0, 10, (15, 2)))
cross_counts = tree.count_neighbors(tree2, radii)
print("Cross pair counts:", cross_counts)
# [  2  10  38  66 127]

##---------------------------##
## .sparse_distance_matrix() ##
##---------------------------##
'''
tree.sparse_distance_matrix(other, max_distance, p=2, output_type='dok_matrix')
  Compute a sparse matrix of distances, including only pairs within max_distance.

  Returns a scipy.sparse matrix (default DOK, alternatively 'coo_matrix',
  'csr_matrix', 'csr_array', or 'ndarray').

  Much more memory-efficient than a dense distance matrix when max_distance is small
  relative to the data extent.
'''

from scipy.sparse import issparse

sp_dm = tree.sparse_distance_matrix(tree, max_distance=2.0)
print(f"Sparse distance matrix type : {type(sp_dm)}") # <class 'scipy.sparse._dok.dok_matrix'>
print(f"Non-zero entries            : {sp_dm.nnz}") # 54
print(f"Density                     : {sp_dm.nnz / (len(pts_2d)**2):.3f}") # 0.135

# Convert to CSR for efficient arithmetic
sp_csr = sp_dm.tocsr()


# =========================================================================================
#  PART D — DELAUNAY TRIANGULATION 
# =========================================================================================

##----------##
## Delaunay ##
##----------##
'''
Delaunay(points, furthest_site=False, incremental=False, qhull_options='')
  Delaunay tessellation of a set of points in N dimensions.

  For 2-D: produces triangles.  For 3-D: tetrahedra.  For N-D: N-simplices.
  The triangulation maximises the minimum angle (circumsphere criterion).

Key attributes:
  .points      : (N, d) input point coordinates.
  .simplices   : (M, d+1) int array — row = vertex indices of one simplex.
  .neighbors   : (M, d+1) int — .neighbors[i, j] is the simplex opposite vertex j
                 in simplex i.  -1 means boundary (no neighbor).
  .vertex_to_simplex : (N,) — one simplex that contains each vertex.
  .convex_hull : (K, d) — simplices on the convex hull boundary.

Methods:
  .find_simplex(xi) : which simplex each query point falls in (-1 = outside hull).
  .transform        : (M, d+1, d) affine transformation for barycentric coordinates.
  .plane_distance(xi): signed distances to hyperplanes (used by find_simplex).
'''

# 2-D example
np.random.seed(0)
pts_tri = rng.uniform(0, 10, (12, 2))
tri = Delaunay(pts_tri)

print(f"Delaunay: {len(pts_tri)} points -> {len(tri.simplices)} triangles") # 12 points -> 16 triangles
print("Simplices shape:", tri.simplices.shape)    # (M, 3) — each row = 3 vertex indices
print("Neighbors shape:", tri.neighbors.shape)   # (M, 3) — one neighbour per edge

# Inspect one triangle
i_tri = 0
verts = tri.points[tri.simplices[i_tri]]
print(f"Triangle 0 vertices:\n{verts.round(3)}")
# [[1.533 1.793]
#  [1.964 3.103]
#  [1.228 8.311]]

print(f"Triangle 0 neighbors: {tri.neighbors[i_tri]}") # [ 1 -1  2]

##-----------------##
## .find_simplex() ##
##-----------------##
'''
tri.find_simplex(xi, bruteforce=False, tol=None) -> int array
  Returns the index of the simplex that contains each query point in xi.
  Returns -1 for points outside the convex hull.

  xi         : (d,) or (M, d) query points.
  bruteforce : bypass the tree and scan all simplices (for debugging).
  tol        : tolerance for point-on-boundary decisions.

  Used for: point location, barycentric interpolation, mesh processing.
'''

q_inside  = np.array([[5.0, 5.0], [3.0, 7.0]])
q_outside = np.array([[15.0, 15.0], [-1.0, -1.0]])

s_in  = tri.find_simplex(q_inside)
s_out = tri.find_simplex(q_outside)
print(f"Inside  -> simplex index: {s_in}")    # Inside  -> simplex index: [4 4]
print(f"Outside -> simplex index: {s_out}")   # [-1, -1]

# Which simplex each original point belongs to
s_all = tri.find_simplex(pts_tri)
print("All original points found:", np.all(s_all >= 0))   # True

##-------------------------##
## Barycentric coordinates ##
##-------------------------##
'''
tri.transform  : (M, d+1, d) array.
  For simplex i: transform[i, :d, :] is the linear map and transform[i, d, :] is the offset.
  Barycentric coords (λ₀, λ₁, ..., λ_d) of point p in simplex i:
    b = transform[i, :d, :] @ (p - transform[i, d, :])
    λ = [b[0], b[1], ..., 1 - b.sum()]
  All λ ≥ 0 and Σλ = 1 for interior points.
'''

def barycentric_coords(tri, point):
    si = tri.find_simplex(point)
    if si == -1:
        return None, -1
    T = tri.transform[si, :2, :]   # 2×2 affine map
    r = tri.transform[si, 2, :]    # reference vertex
    b = T @ (point - r)
    bary = np.append(b, 1 - b.sum())
    return bary, si

bary, si = barycentric_coords(tri, np.array([5.0, 5.0]))
print(f"Barycentric coords in simplex {si}: {bary.round(4)}") # [0.663  0.2405 0.0965]
print(f"All non-negative: {np.all(bary >= -1e-10)}")   # True
print(f"Sum = 1: {np.isclose(bary.sum(), 1.0)}")        # True

# Reconstruct point from barycentric coords
verts_si = tri.points[tri.simplices[si]]
reconstructed = (bary[:, None] * verts_si).sum(axis=0)
print(f"Reconstructed: {reconstructed.round(4)}")   # [5. 5.]

##-----------##
## tsearch() ##
##-----------##
'''
tsearch(tri, xi) -> int array
  Functional wrapper around tri.find_simplex(xi).
  Identical result; exists for NumPy compat.
'''

xi_test = np.array([[4.0, 4.0], [6.0, 6.0]])
print("tsearch:", tsearch(tri, xi_test))   # [1, 6] same as find_simplex


# =========================================================================================
#  PART E — CONVEX HULL 
# =========================================================================================

##------------##
## ConvexHull ##
##------------##
'''
ConvexHull(points, incremental=False, qhull_options='')
  Convex hull of a set of points in N dimensions.

  For 2-D: convex polygon.  For 3-D: convex polyhedron.

Key attributes:
  .points    : (N, d) all input points.
  .vertices  : 1-D int array — indices of hull vertices (for 2-D, in CCW order).
  .simplices : (M, d) int — facets. For 2-D: edges (pairs). For 3-D: triangular faces.
  .neighbors : (M, d) — neighboring facets (one per simplex vertex).
  .equations : (M, d+1) — [normal, offset] for each facet hyperplane.
               For 2-D facet i: equations[i, :2] @ x + equations[i, 2] == 0.
               Normal points outward.
  .area      : scalar — surface area (perimeter in 2-D).
  .volume    : scalar — volume (area in 2-D).

  qhull_options: 'QJ' joggle input (handle degenerate cases),
                 'Qt' triangulated output.
'''

hull_2d = ConvexHull(pts_2d)
print(f"2-D hull: {len(hull_2d.vertices)} vertices, {len(hull_2d.simplices)} edges") # 7 vertices, 7 edges
print(f"Perimeter : {hull_2d.area:.4f}") # 30.1777
print(f"Area      : {hull_2d.volume:.4f}") # 59.6168 (.volume = area in 2-D)
print("Hull vertices:", hull_2d.vertices) # [12 11 15  2  4 13  8]

# For 3-D
hull_3d = ConvexHull(pts_3d)
print(f"3-D hull: {len(hull_3d.vertices)} vertices, {len(hull_3d.simplices)} faces") # 3-D hull: 16 vertices, 28 faces
print(f"Surface area : {hull_3d.area:.4f}") # 257.9609
print(f"Volume       : {hull_3d.volume:.4f}") # 302.8867

# Facet hyperplane equations: outward normals
print("Equations (first 3):")
print(hull_2d.equations[:3].round(4))
# [[  0.9641  -0.2655  -6.9879]
#  [  0.0125   0.9999  -9.7672]
#  [  0.3127   0.9498 -11.5189]]
# Each row: [nx, ny, offset] where [nx,ny]@x + offset <= 0 for interior points

##--------------------------##
## Point-in-hull membership ##
##--------------------------##
'''
A point p is inside the convex hull iff it satisfies all half-space inequalities:
  (hull.equations[:, :-1] @ p + hull.equations[:, -1]) <= 0

For 3-D use scipy.spatial.ConvexHull or pass the equations directly.
'''

def point_in_hull(point, hull, tol=1e-12):
    return np.all(hull.equations[:, :-1] @ point + hull.equations[:, -1] <= tol)

p_inside_2d  = np.mean(pts_2d[hull_2d.vertices], axis=0)   # centroid of hull vertices
p_outside_2d = np.array([100.0, 100.0])

print(f"Centroid inside hull : {point_in_hull(p_inside_2d,  hull_2d)}")   # True
print(f"Far point outside    : {point_in_hull(p_outside_2d, hull_2d)}")   # False

# Incremental hull: add points one at a time (avoid full rebuild)
hull_incr = ConvexHull(pts_2d[:10], incremental=True)
hull_incr.add_points(pts_2d[10:])
print(f"Incremental hull area: {hull_incr.volume:.4f}")   # 59.6168


# =========================================================================================
#  PART F — VORONOI DIAGRAMS 
# =========================================================================================

##---------##
## Voronoi ##
##---------##
'''
Voronoi(points, furthest_site=False, incremental=False, qhull_options='')
  Voronoi diagram of a set of points in N dimensions.
  The Voronoi diagram is the dual of the Delaunay triangulation.

Key attributes:
  .points         : (N, d) input generator points.
  .vertices       : (M, d) Voronoi vertex coordinates (finite vertices only).
  .regions        : list of N lists — each list gives vertex indices of one region.
                    -1 in a list means an infinite vertex (open region).
  .ridge_points   : (R, 2) — each ridge separates two generator points.
  .ridge_vertices : list of R lists — vertex indices of each ridge edge.
                    -1 = infinite ridge (extends to infinity).
  .point_region   : (N,) — maps generator i to its region index in .regions.

Note: outer points always have open (infinite) regions in Euclidean Voronoi.
      Use SphericalVoronoi for closed regions on the sphere.
'''

vor = Voronoi(pts_2d)
print(f"Voronoi: {len(vor.vertices)} finite vertices") # 31 finite vertices
print(f"Regions: {len(vor.regions)} (including empty and infinite)") # 21 (including empty and infinite)
print(f"Ridges : {len(vor.ridge_points)}") # 50

# Ridge between generators 0 and 1
ridge_idx = 0
gen_pair = vor.ridge_points[ridge_idx]
vrt_pair = vor.ridge_vertices[ridge_idx]
print(f"Ridge {ridge_idx}: generators {gen_pair}, vertices {vrt_pair}")
# Ridge 0: generators [ 4 13], vertices [-1, 4]
# vertex index -1 means one end goes to infinity

# Finite ridges only
finite_ridges = [rv for rv in vor.ridge_vertices if -1 not in rv]
print(f"Finite ridges: {len(finite_ridges)}") # 43

# Area of each Voronoi cell (finite cells only)
from scipy.spatial import ConvexHull as _CH
cell_areas = []
for region_idx in vor.point_region:
    region = vor.regions[region_idx]
    if -1 not in region and len(region) > 0:
        cell_verts = vor.vertices[region]
        try:
            cell_areas.append(_CH(cell_verts).volume)   # .volume = area in 2-D
        except Exception:
            pass
print(f"Finite Voronoi cells: {len(cell_areas)}, mean area: {np.mean(cell_areas):.3f}")
# Finite Voronoi cells: 13, mean area: 9.436

##------------------##
## SphericalVoronoi ##
##------------------##
'''
SphericalVoronoi(points, radius=1, center=None, threshold=1e-06)
  Voronoi diagram restricted to the surface of a sphere.
  All Voronoi regions are guaranteed to be closed (finite) and cover the sphere.

  points    : (N, 3) — must lie on the sphere of given radius and center.
  radius    : sphere radius (default 1).
  center    : sphere center (default origin).

Key attributes:
  .vertices : (M, 3) Voronoi vertex coordinates on the sphere surface.
  .regions  : list of N lists — each list is the (ordered) vertex indices of one region.

Methods:
  .sort_vertices_of_regions() : order region vertices in CCW order (call before area calculation).
  .calculate_areas()          : area of each Voronoi region on the sphere.
                                Sum of all areas = 4π r² (total sphere surface).
'''

sv = SphericalVoronoi(pts_unit, radius=1.0, center=np.array([0., 0., 0.]))
sv.sort_vertices_of_regions()

areas = sv.calculate_areas()
print(f"SphericalVoronoi: {len(pts_unit)} points -> {len(sv.vertices)} vertices") # SphericalVoronoi: 30 points -> 56 vertices
print(f"Total area = {areas.sum():.6f}, 4π = {4*np.pi:.6f}") # should match
print(f"Mean cell area: {areas.mean():.4f} = 4π/{len(pts_unit)} = {4*np.pi/len(pts_unit):.4f}") # Mean cell area: 0.4189 = 4π/30 = 0.4189


# =========================================================================================
#  PART G — HALFSPACE INTERSECTION 
# =========================================================================================

##-----------------------##
## HalfspaceIntersection ##
##-----------------------##
'''
HalfspaceIntersection(halfspaces, interior_point, incremental=False, qhull_options='')
  Compute the intersection of a set of half-spaces in N dimensions.
  Each half-space is defined by: A @ x + b <= 0   (a linear inequality).

  halfspaces     : (M, d+1) array — each row is [a₁, a₂, ..., aₙ, b].
                   The half-space is {x : a·x + b ≤ 0}.
  interior_point : a point strictly inside the intersection (feasible point).
                   Required by Qhull; can be found with scipy.optimize.linprog.

Key attributes:
  .intersections : (K, d) — vertices of the feasible polytope (extreme points).
  .dual_points   : dual representation used by Qhull.
  .dual_facets   : dual tessellation.

Use case: feasible region of a linear programme, polytope H-representation.
'''

# Define a 2-D square: [-1, 1]² using 4 half-spaces
# half-space: [normal..., -offset] so that normal·x ≤ offset
halfspaces = np.array([
    [ 1,  0, -2],    #  x ≤ 2
    [-1,  0, -2],    # -x ≤ 2  =>  x ≥ -2
    [ 0,  1, -2],    #  y ≤ 2
    [ 0, -1, -2],    # -y ≤ 2  =>  y ≥ -2
])
interior_pt = np.array([0.0, 0.0])   # origin is strictly inside [-2, 2]²

hs = HalfspaceIntersection(halfspaces, interior_pt)
print("Halfspace vertices (corners of square):")
print(hs.intersections.round(4))
# [[-2. -2.]
#  [ 2. -2.]
#  [-2.  2.]
#  [ 2.  2.]]
# (order may vary)
print(f"Number of intersection vertices: {len(hs.intersections)}") # 4

# 3-D example: intersection of 6 half-spaces = unit cube
halfspaces_3d = np.array([
    [ 1,  0,  0, -1], [-1,  0,  0, -1],
    [ 0,  1,  0, -1], [ 0, -1,  0, -1],
    [ 0,  0,  1, -1], [ 0,  0, -1, -1],
])
hs_3d = HalfspaceIntersection(halfspaces_3d, np.array([0., 0., 0.]))
print(f"Cube intersection vertices: {len(hs_3d.intersections)} (expect 8)") # 8


# =========================================================================================
#  PART H — UTILITY FUNCTIONS  (scipy.spatial) 
# =========================================================================================

##------------##
## procrustes ##
##------------##
'''
procrustes(data1, data2) -> (mtx1, mtx2, disparity)
  Procrustes analysis: find the optimal similarity transform (translation, rotation,
  uniform scaling) that maps data2 onto data1.

  Both matrices must have the same shape (M, d).
  Returns:
    mtx1      : standardised data1 (zero-centred, Frobenius norm = 1).
    mtx2      : standardised and best-fit-transformed data2.
    disparity : sum of squared element-wise differences after alignment.
                0 means perfect fit; 1 means orthogonal (worst case after normalisation).

  Useful for: shape analysis, comparing molecule conformations, aligning point clouds.
  Note: only finds the best rotation/reflection — not an affine transform.
        For a full rigid body alignment in 3-D, see Kabsch algorithm.
'''

# "Ground truth" triangle
shape1 = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3)/2]])

# Rotated + scaled + translated version
theta_p = np.pi / 4
R_p = np.array([[np.cos(theta_p), -np.sin(theta_p)],
                [np.sin(theta_p),  np.cos(theta_p)]])
shape2 = (shape1 @ R_p.T) * 2 + np.array([3.0, 5.0])   # scale=2, translate=(3,5)

mtx1, mtx2, disparity = procrustes(shape1, shape2)
print(f"Procrustes disparity: {disparity:.6f}") # ≈ 0.0 (perfect shape match)
print(f"mtx1 Frobenius norm : {np.linalg.norm(mtx1):.4f}") # 1.0
print(f"mtx2 Frobenius norm : {np.linalg.norm(mtx2):.4f}") # ≈ 1.0

# Noisy shape: add perturbation
shape2_noisy = shape2 + rng.normal(0, 0.1, shape2.shape)
_, _, disp_noisy = procrustes(shape1, shape2_noisy)
print(f"Noisy Procrustes disparity: {disp_noisy:.4f}") # > 0 (0.0076)

##-----------------##
## geometric_slerp ##
##-----------------##
'''
geometric_slerp(start, end, t, tol=1e-7)
  Spherical linear interpolation between two points on a unit n-sphere.

  start, end : (d,) unit vectors on the sphere. Both must have |x| = 1.
  t          : float or array in [0, 1]. t=0 -> start, t=1 -> end.

  Returns: (len(t), d) interpolated unit vectors.
  Traces the great-circle arc (geodesic on the sphere).

  For 3-D rotation interpolation prefer Slerp(Rotation, ...) from transform.
  geometric_slerp operates on plain unit vectors, e.g. for interpolating
  camera positions on a sphere or colours on the colour sphere.
'''

# Interpolate between two antipodal-ish points on the unit sphere
start_sph = np.array([1.0, 0.0, 0.0])   # x-pole
end_sph   = np.array([0.0, 1.0, 0.0])   # y-pole

t_sph = np.linspace(0, 1, 6)
path  = geometric_slerp(start_sph, end_sph, t_sph)
print("Slerp path (great-circle arc):")
print(path.round(4))
# [[ 1.      0.     -0.    ]
#  [ 0.9511  0.309  -0.    ]
#  [ 0.809   0.5878 -0.    ]
#  [ 0.5878  0.809  -0.    ]
#  [ 0.309   0.9511 -0.    ]
#  [ 0.      1.     -0.    ]]
# Each row is a unit vector; the path follows the great circle arc in the x-y plane.

# Verify all interpolated points lie on the unit sphere
norms = np.linalg.norm(path, axis=1)
print("Norms (all should be 1.0):", norms.round(8))
# [1. 1. 1. 1. 1. 1.]
# all 1.0

# 2-D unit circle interpolation (useful for smooth angle interpolation)
start_2d = np.array([1.0, 0.0])
end_2d   = np.array([0.0, 1.0])
arc_2d   = geometric_slerp(start_2d, end_2d, t_sph)
print("2-D arc angles:", np.degrees(np.arctan2(arc_2d[:, 1], arc_2d[:, 0])).round(1))
# 2-D arc angles: [ 0.  18.  36.  54.  72.  90.]

##--------------------------------------##
## distance_matrix / minkowski_distance ##
##--------------------------------------##
'''
distance_matrix(x, y, p=2, threshold=1000000)
  Compute the full (M, N) pairwise distance matrix between rows of x and y.
  Uses the Minkowski p-norm. For p=2: Euclidean.

  threshold : if M*N > threshold, use a memory-efficient loop.
  Note: for large arrays prefer cdist() from scipy.spatial.distance.

minkowski_distance(x, y, p=2)
  Lp distance between corresponding rows of x and y (element-wise).
  Returns an array of distances.

minkowski_distance_p(x, y, p=2)
  Returns the p-th power of the Lp distance (avoids the final root operation).
'''

x_dm = rng.uniform(0, 5, (4, 2))
y_dm = rng.uniform(0, 5, (3, 2))

D = distance_matrix(x_dm, y_dm, p=2)
print("Distance matrix shape:", D.shape) # (4, 3)
print("Distance matrix:\n", D.round(4))
#  [[1.4842 2.0203 1.8791]
#  [4.1682 1.6568 2.4362]
#  [2.0098 2.4211 1.1146]
#  [4.2113 2.0122 4.9367]]

# Minkowski p=1 (Manhattan)
D_l1 = distance_matrix(x_dm, y_dm, p=1)
print("L1 distance matrix:\n", D_l1.round(4))
#  [[2.0842 2.4292 2.0295]
#  [5.6717 2.0836 3.0729]
#  [2.7678 3.3243 1.3459]
#  [5.3516 2.6736 6.8184]]

# Element-wise Minkowski distance between paired rows
a_pairs = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 0.0]])
b_pairs = np.array([[1.0, 0.0], [1.0, 2.0], [0.0, 0.0]])
print("Element-wise L2:", minkowski_distance(a_pairs, b_pairs, p=2).round(4))
# [1.  1.  2.]
print("Element-wise L1:", minkowski_distance(a_pairs, b_pairs, p=1).round(4))
# [1.  1.  2.]  -- same for these specific pairs
print("Squared L2      :", minkowski_distance_p(a_pairs, b_pairs, p=2).round(4))
# [1.  1.  4.]  -- no sqrt


# =========================================================================================
#  PART I — PAIRWISE DISTANCE COMPUTATION  (scipy.spatial.distance) 
# =========================================================================================

##-------##
## cdist ##
##-------##
'''
cdist(XA, XB, metric='euclidean', *, out=None, **kwargs)
  Compute pairwise distances between all (i, j) pairs with i in XA, j in XB.

  XA : (mA, n) — mA observations in n dimensions.
  XB : (mB, n) — mB observations in n dimensions.
  Returns: (mA, mB) distance matrix.

  metric can be:
    - string name:   'euclidean', 'cosine', 'minkowski', 'cityblock',
                     'chebyshev', 'correlation', 'mahalanobis',
                     'hamming', 'jaccard', 'dice', 'jensenshannon', ...
    - callable:      any function f(u, v) -> scalar distance.

  Additional kwargs are forwarded to the metric (e.g. p=3 for minkowski,
  VI for mahalanobis inverse covariance).

cdist vs KDTree:
  cdist    : dense O(mA*mB) — fast for moderate sizes, all pairs needed.
  KDTree   : O(N log N) build + O(log N) query — fast when only k-NN needed.
'''

A = rng.uniform(0, 10, (5, 3))
B = rng.uniform(0, 10, (4, 3))

D_eucl = cdist(A, B, metric='euclidean')
print("cdist Euclidean shape:", D_eucl.shape)   # (5, 4)
print("D[0,:]:", D_eucl[0].round(4)) # D[0,:]: [7.9778 7.042  7.6923 8.0613]

# Various string metrics
D_cos  = cdist(A, B, 'cosine')
D_man  = cdist(A, B, 'cityblock')
D_cheb = cdist(A, B, 'chebyshev')
D_mink = cdist(A, B, 'minkowski', p=3)
print("Minkowski p=3:\n", D_mink.round(4))
#  [[7.7554 6.363  6.6038 7.1884]
#  [7.5246 5.426  3.9018 5.6225]
#  [4.1978 3.6573 8.2466 3.526 ]
#  [4.8846 4.9445 4.8785 5.2523]
#  [8.035  6.1517 5.0874 6.7091]]

# Custom callable metric
def l_inf(u, v):
    return np.max(np.abs(u - v))

D_custom = cdist(A, B, l_inf)
print(np.allclose(D_custom, D_cheb))   # True (Chebyshev == L∞)

# Mahalanobis: account for feature covariance
X_cov = rng.multivariate_normal([0]*3, np.eye(3)*2, 20)
VI = np.linalg.inv(np.cov(X_cov.T))   # inverse covariance
D_maha = cdist(A, B, 'mahalanobis', VI=VI)
print("Mahalanobis shape:", D_maha.shape)   # (5, 4)

##-------##
## pdist ##
##-------##
'''
pdist(X, metric='euclidean', *, out=None, **kwargs)
  Compute pairwise distances among all N*(N-1)/2 distinct pairs in X.

  X : (N, d) observations.
  Returns: condensed 1-D array of length N*(N-1)/2 (upper-triangle, row-major).
           y[k] = dist(X[i], X[j]) where k is the linear index for pair (i, j).

  More memory-efficient than cdist(X, X) since the diagonal and lower triangle
  are not stored (diagonal = 0, matrix is symmetric).

  k = N*(N-1)/2 - (N-i)*(N-i-1)/2 + (j-i-1) for pair (i, j) with i < j.
'''

X_pd = rng.uniform(0, 5, (6, 2))
Y_cond = pdist(X_pd, 'euclidean')
print(f"pdist condensed length: {len(Y_cond)} = 6*5/2 = {6*5//2}")   # 15
print("First 5 distances:", Y_cond[:5].round(4)) # [1.4935 1.6877 1.7291 3.3861 3.6754]

# Verify: pdist should equal upper triangle of cdist
D_full = cdist(X_pd, X_pd, 'euclidean')
i_upper, j_upper = np.triu_indices(6, k=1)
print(np.allclose(Y_cond, D_full[i_upper, j_upper])) # True

# Use with different metrics
Y_cos  = pdist(X_pd, 'cosine')
Y_mink = pdist(X_pd, 'minkowski', p=3)
print("Cosine pdist:", Y_cos.round(4))
# Cosine pdist: [0.0124 0.0496 0.0467 0.2849 0.3442 0.0125 0.1059 0.4036 0.4709 0.1878
#  0.5377 0.6115 0.1072 0.1469 0.0033]

##------------##
## squareform ##
##------------##
'''
squareform(X, force='no', checks=True)
  Convert between condensed and square-form distance matrices.

  condensed -> square : squareform(Y_cond)  -> (N, N) symmetric with 0 diagonal.
  square -> condensed : squareform(D_sq)    -> (N*(N-1)/2,) condensed vector.

  force : 'no'         — auto-detect direction.
          'tomatrix'   — force condensed -> square.
          'tovector'   — force square -> condensed.

  Use squareform together with pdist to go from compact to full matrix.
'''

# Condensed -> square
D_sq = squareform(Y_cond)
print("Square matrix shape:", D_sq.shape)   # (6, 6)
print("Symmetric:", np.allclose(D_sq, D_sq.T))      # True
print("Zero diagonal:", np.allclose(np.diag(D_sq), 0))  # True

# Square -> condensed (round-trip)
Y_rt = squareform(D_sq)
print("Round-trip condensed matches:", np.allclose(Y_rt, Y_cond))   # True

# Full clustering workflow: hierarchical linkage uses condensed form
from scipy.cluster.hierarchy import linkage, fcluster
Z = linkage(Y_cond, method='ward')
labels = fcluster(Z, t=3, criterion='maxclust')   # 3 clusters
print("Cluster labels:", labels) # [3 2 2 3 1 1]


# =========================================================================================
#  PART J — CONTINUOUS VECTOR DISTANCES 
# =========================================================================================
'''
All functions below take two 1-D arrays u and v (same length) and return a scalar distance.
They are designed for use as callables in cdist/pdist, but also work standalone.
'''

u = np.array([1.0, 2.0, 3.0, 4.0])
v = np.array([2.0, 3.0, 1.0, 4.0])

##-------------------------##
## euclidean / sqeuclidean ##
##-------------------------##
'''
euclidean(u, v)   : sqrt(Σ(uᵢ - vᵢ)²)  — L2 distance.
sqeuclidean(u, v) : Σ(uᵢ - vᵢ)²         — squared L2, avoids sqrt.
                    Preferred in distance comparisons where only ordering matters.
'''
print(f"euclidean   : {euclidean(u, v):.4f}")    # sqrt(1+1+4+0) = 2.4495
print(f"sqeuclidean : {sqeuclidean(u, v):.4f}")  # 6.0
print(np.isclose(euclidean(u, v)**2, sqeuclidean(u, v)))   # True

##-----------------------------------##
## minkowski / cityblock / chebyshev ##
##-----------------------------------##
'''
minkowski(u, v, p=2)  : (Σ|uᵢ - vᵢ|^p)^(1/p) — generalised Lp distance.
                         p=1 -> cityblock, p=2 -> euclidean, p=∞ -> chebyshev.
cityblock(u, v)       : Σ|uᵢ - vᵢ|  — L1 / Manhattan / taxicab distance.
chebyshev(u, v)       : max|uᵢ - vᵢ| — L∞ / chessboard distance.
'''
print(f"L1  cityblock : {cityblock(u, v):.4f}")          # 1+1+2+0 = 4.0
print(f"L2  euclidean : {euclidean(u, v):.4f}")           # 2.4495
print(f"L3  minkowski : {minkowski(u, v, p=3):.4f}")      # (1+1+8)^(1/3) = 2.154
print(f"L∞  chebyshev : {chebyshev(u, v):.4f}")           # max(1,1,2,0) = 2.0

# Verify Lp ordering: L∞ <= L2 <= L1 for vectors (when d >= 1)
print(chebyshev(u,v) <= euclidean(u,v) <= cityblock(u,v)) # True

##----------------------##
## cosine / correlation ##
##----------------------##
'''
cosine(u, v)     : 1 - cos(∠u,v) = 1 - (u·v) / (|u||v|).
                   Range [0, 2]; 0 = same direction, 1 = orthogonal, 2 = opposite.
                   Invariant to magnitude — measures angular difference.

correlation(u, v): 1 - Pearson correlation coefficient.
                   = cosine(u - mean(u), v - mean(v)).
                   Range [0, 2]; 0 = perfectly correlated, 2 = anti-correlated.
                   Invariant to both magnitude AND offset (mean-centred).
'''
u_c = np.array([1.0, 2.0, 3.0])
v_c = np.array([2.0, 4.0, 6.0])   # same direction, double length

print(f"cosine(u, 2u)    : {cosine(u_c, v_c):.6f}")    # ≈ 0 (same direction)
print(f"cosine(u, -u)    : {cosine(u_c, -v_c):.6f}")   # ≈ 2 (opposite direction)

# correlation is mean-centred cosine
u_shifted = u_c + 100.0
v_shifted = v_c + 100.0
print(f"cosine  (shifted): {cosine(u_shifted, v_shifted):.4f}")   # changes with shift
print(f"corr    (shifted): {correlation(u_shifted, v_shifted):.4f}")  # same as without shift

# Pearson r = 1 - correlation
print(f"Pearson r ≈ {1 - correlation(u_c, v_c):.4f}") # 1.0 (same direction)

##--------------------------##
## mahalanobis / seuclidean ##
##--------------------------##
'''
mahalanobis(u, v, VI)
  sqrt((u-v) @ VI @ (u-v)^T)  — Mahalanobis distance.
  VI: inverse of the covariance matrix.
  Accounts for correlations and different feature scales.
  Reduces to Euclidean when VI = I.

seuclidean(u, v, V)
  sqrt(Σ (uᵢ - vᵢ)² / Vᵢ)  — standardised Euclidean distance.
  V : per-feature variance (1-D array).
  Equivalent to Mahalanobis with diagonal covariance.
'''
data_cov = rng.multivariate_normal([0, 0, 0], np.diag([1, 4, 9]), 50)
VI_cov   = np.linalg.inv(np.cov(data_cov.T))
u3, v3   = np.array([1.0, 2.0, 3.0]), np.array([2.0, 3.0, 1.0])

d_maha   = mahalanobis(u3, v3, VI_cov)
d_eucl3  = euclidean(u3, v3)
print(f"Mahalanobis : {d_maha:.4f}") # 1.3498
print(f"Euclidean   : {d_eucl3:.4f}") # 2.4495 (differ due to covariance)

# seuclidean: per-feature variance
V_feat = np.array([1.0, 4.0, 9.0])
d_se   = seuclidean(u3, v3, V_feat)
# Manually: sqrt((1-2)²/1 + (2-3)²/4 + (3-1)²/9)
d_se_manual = np.sqrt((1**2/1) + (1**2/4) + (2**2/9))
print(f"seuclidean   : {d_se:.4f}") # 1.3017
print(f"seuclidean M : {d_se_manual:.4f}")   # same
print(np.isclose(d_se, d_se_manual))          # True

##------------------------------------##
## jensenshannon / directed_hausdorff ##
##------------------------------------##
'''
jensenshannon(p, q, base=None)
  Jensen-Shannon divergence: JS(p||q) = (KL(p||m) + KL(q||m)) / 2  where m = (p+q)/2.
  Returns the sqrt of the JS divergence (a proper metric).
  Range [0, 1] (natural log base). p and q must be non-negative; needn't sum to 1.
  Symmetric, bounded, always finite — unlike KL divergence.

directed_hausdorff(u, v, seed=0)
  Directed Hausdorff distance from set u to set v:
    max_{a in u} min_{b in v} dist(a, b)
  Not symmetric! max(directed(u,v), directed(v,u)) gives the true Hausdorff distance.
  Returns: (distance, index_in_u, index_in_v) for the furthest-closest pair.
'''

# Jensen-Shannon distance between two probability distributions
p_js = np.array([0.4, 0.3, 0.2, 0.1])
q_js = np.array([0.25, 0.25, 0.25, 0.25])   # uniform
js   = jensenshannon(p_js, q_js)
print(f"Jensen-Shannon dist(p, q) = {js:.4f}")   # 0.1669 ∈ [0, 1]

# Symmetric
print(np.isclose(jensenshannon(p_js, q_js), jensenshannon(q_js, p_js)))   # True

# Same distribution -> 0
print(f"JS(p, p) = {jensenshannon(p_js, p_js):.6f}")   # 0.0

# Hausdorff distance between two point sets
set_u = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 1.0]])
set_v = np.array([[0.1, 0.1], [0.9, 0.1], [0.5, 0.9]])

d_uv, i_u, i_v = directed_hausdorff(set_u, set_v)
d_vu, i_v2,i_u2= directed_hausdorff(set_v, set_u)
d_haus = max(d_uv, d_vu)
print(f"Directed u->v: {d_uv:.4f} (worst point: u[{i_u}], v[{i_v}])") # Directed u->v: 0.1414 (worst point: u[0], v[0])
print(f"Directed v->u: {d_vu:.4f}") # Directed v->u: 0.1414
print(f"Hausdorff    : {d_haus:.4f}") # Hausdorff    : 0.1414

# Large random sets — Hausdorff detects the furthest-apart pair
A_haus = rng.uniform(0, 1, (50, 3))
B_haus = rng.uniform(0.5, 1.5, (50, 3))
d_AB = max(directed_hausdorff(A_haus, B_haus)[0], directed_hausdorff(B_haus, A_haus)[0])
print(f"Random set Hausdorff: {d_AB:.4f}")
# Random set Hausdorff: 0.8342


# =========================================================================================
#  PART K — BOOLEAN / SET DISTANCES 
# =========================================================================================

'''
Boolean distance functions operate on binary (0/1 or True/False) vectors.
Given two boolean vectors u and v of length n, define the contingency table:
  ntt = (u & v).sum()   # both True
  ntf = (u & ~v).sum()  # u True, v False
  nft = (~u & v).sum()  # u False, v True
  nff = (~u & ~v).sum() # both False

Most boolean distances are ratios involving these four counts.
They all return 0 for identical vectors and 1 for maximally dissimilar vectors.
'''

# 8-bit binary vectors (e.g. feature presence/absence)
u_b = np.array([1, 0, 1, 1, 0, 0, 1, 0], dtype=bool)
v_b = np.array([1, 1, 0, 1, 0, 1, 0, 0], dtype=bool)

# Contingency table for reference
ntt = (u_b & v_b).sum()    # 2
ntf = (u_b & ~v_b).sum()   # 2
nft = (~u_b & v_b).sum()   # 2
nff = (~u_b & ~v_b).sum()  # 2
print(f"ntt={ntt}, ntf={ntf}, nft={nft}, nff={nff}")   # ntt=2, ntf=2, nft=2, nff=2

##--------------------------##
## hamming / jaccard / dice ##
##--------------------------##
'''
hamming(u, v) : fraction of positions where u and v disagree.
                = (ntf + nft) / n.  Range [0, 1].

jaccard(u, v) : 1 - |u ∩ v| / |u ∪ v|.
                = (ntf + nft) / (ntt + ntf + nft).
                Ignores nff (joint absences).  Range [0, 1].

dice(u, v)    : 1 - 2|u ∩ v| / (|u| + |v|).
                = (ntf + nft) / (2*ntt + ntf + nft).
                Like Jaccard but weights shared features double.
                Dice = 2*Jaccard / (1 + Jaccard).  Range [0, 1].
'''

print(f"hamming  : {hamming(u_b, v_b):.4f}")   # (2+2)/8 = 0.5
print(f"jaccard  : {jaccard(u_b, v_b):.4f}")   # (2+2)/(2+2+2) = 0.6667
print(f"dice     : {dice(u_b, v_b):.4f}")      # (2+2)/(4+2+2) = 0.5

# Jaccard is 0 when identical, 1 when no overlap
u_same = np.array([1, 0, 1, 0], dtype=bool)
v_same = np.array([1, 0, 1, 0], dtype=bool)
v_diff = np.array([0, 1, 0, 1], dtype=bool)
print(f"jaccard(u, u) = {jaccard(u_same, v_same):.4f}")   # 0.0
print(f"jaccard(u, ~u)= {jaccard(u_same, v_diff):.4f}")   # 1.0

# Dice <= Jaccard (Dice gives more credit to agreement)
print(dice(u_b, v_b) <= jaccard(u_b, v_b))   # True

# Non-boolean inputs are treated as non-zero = True
u_float = np.array([1.5, 0.0, 3.0, 0.0])
v_float = np.array([0.0, 2.0, 1.0, 0.0])
print(f"hamming (float) : {hamming(u_float, v_float):.4f}") # 0.7500 (3 of 4 disagree)

##-----------------------------------------------------------##
## rogerstanimoto / russellrao / sokalmichener / sokalsneath ##
##-----------------------------------------------------------##
'''
rogerstanimoto(u, v):
  (ntf + nft) / (ntt + nff + 2*(ntf+nft))
  Penalises disagreements twice as much as agreements.  Range [0, 1].

russellrao(u, v):
  (ntf + nft + nff) / n   = 1 - ntt/n
  Proportion NOT in joint agreement (including joint False pairs).
  Sensitive to joint absence.  Range [0, 1].

sokalsneath(u, v):
  2*(ntf+nft) / (2*(ntf+nft) + ntt)
  Like Dice but only counts ntt (not nff) as agreements.  Range [0, 1].
'''

print(f"rogerstanimoto : {rogerstanimoto(u_b, v_b):.4f}")   # 0.6667
print(f"russellrao     : {russellrao(u_b, v_b):.4f}")        # (2+2+2)/8 = 0.75
print(f"sokalsneath    : {sokalsneath(u_b, v_b):.4f}")       # 2*4/(2*4+2) = 8/10 = 0.8

# Quick comparison of all boolean metrics on same vectors
metrics_bool = {
    'hamming'       : hamming,
    'jaccard'       : jaccard,
    'dice'          : dice,
    'rogerstanimoto': rogerstanimoto,
    'russellrao'    : russellrao,
    'sokalmichener' : sokalmichener,
    'sokalsneath'   : sokalsneath,
    'yule'          : yule,
    'kulczynski1'   : kulczynski1,
}
print("\nAll boolean distances (u vs v):")
for name, fn in metrics_bool.items():
    try:
        print(f"  {name:<18}: {fn(u_b, v_b):.4f}")
    except Exception as e:
        print(f"  {name:<18}: ERROR — {e}")
#   hamming           : 0.5000
#   jaccard           : 0.6667
#   dice              : 0.5000
#   rogerstanimoto    : 0.6667
#   russellrao        : 0.7500
# <stdin>:3: DeprecationWarning: The sokalmichener metric is deprecated since SciPy 1.15.0 and will be removed in SciPy 1.17.0.  Replace usage of 'sokalmichener(u, v)' with 'rogerstanimoto(u, v)'.
#   sokalmichener     : 0.6667
#   sokalsneath       : 0.8000
#   yule              : 1.0000
# <stdin>:3: DeprecationWarning: The kulczynski1 metric is deprecated since SciPy 1.15.0 and will be removed in SciPy 1.17.0.  Replace usage of 'kulczynski1(u, v)' with '1/jaccard(u, v) - 1'.
#   kulczynski1       : 0.5000

##--------------------##
## yule / kulczynski1 ##
##--------------------##
'''
yule(u, v):
  2*ntf*nft / (ntt*nff + ntf*nft)
  Yule's Q coefficient (turned into a distance). Range [0, 2].
  0 = perfect association, 2 = perfect negative association.
  Undefined (NaN) when ntt*nff = 0 or ntf*nft = 0.

kulczynski1(u, v):
  (ntf + nft) / ntt
  Ratio of disagreements to joint agreements.  Range [0, ∞).
  0 = identical (u == v), ∞ when ntt = 0 (no joint positives).
  Unlike most distances, NOT bounded to [0, 1].
'''

# Yule: needs non-zero ntt, nff, ntf, nft — our u_b/v_b satisfy this
print(f"yule      : {yule(u_b, v_b):.4f}")        # 2*2*2/(2*2 + 2*2) = 8/8 = 1.0
print(f"kulczynski1: {kulczynski1(u_b, v_b):.4f}") # 0.5

# Perfect agreement
u_id = np.array([1,1,0,1,0], dtype=bool)
v_id = u_id.copy()
print(f"yule (identical)       : {yule(u_id, v_id):.4f}")          # 0.0
print(f"kulczynski1 (identical): {kulczynski1(u_id, v_id):.4f}")    # 0.0

# Boolean pdist: compute all pairwise boolean distances for a binary dataset
X_bool = rng.integers(0, 2, (8, 6)).astype(bool)
Y_jac  = pdist(X_bool, 'jaccard')
Y_ham  = pdist(X_bool, 'hamming')
print(f"\nBoolean dataset (8x6), pdist condensed length: {len(Y_jac)} = 8*7/2 = 28") # 28
print("Jaccard pdist (first 5):", Y_jac[:5].round(4)) # [0.6  0.75 1.   0.8  1.  ]
print("Hamming pdist (first 5):", Y_ham[:5].round(4)) # [0.5    0.5    0.6667 0.6667 0.6667]

# cdist: cross-distance between two binary matrices
X1_bool = rng.integers(0, 2, (4, 6)).astype(bool)
X2_bool = rng.integers(0, 2, (5, 6)).astype(bool)
D_jac_cross = cdist(X1_bool, X2_bool, 'jaccard')
print(f"Cross-Jaccard matrix: {D_jac_cross.shape}")   # (4, 5)
print(D_jac_cross.round(4))
# [[0.5    0.6667 0.75   0.8    0.    ]
#  [0.8    0.6667 0.75   0.5    0.6667]
#  [0.6    0.5    0.8    0.25   0.75  ]
#  [0.6    0.5    0.5    0.8333 0.75  ]]
