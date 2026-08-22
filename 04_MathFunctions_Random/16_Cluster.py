'''
scipy.cluster  —  Clustering Algorithms
=========================================

Two submodules, covered in a natural workflow order:

  • scipy.cluster.vq        — vector quantization & k-means
  • scipy.cluster.hierarchy — agglomerative / hierarchical clustering

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART A — PREPROCESSING  (scipy.cluster.vq)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. whiten                   : normalise each feature by its std deviation

PART B — K-MEANS  (scipy.cluster.vq)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 2. kmeans                   : classic Lloyd algorithm; returns codebook + distortion
 3. kmeans2                  : extended k-means with init strategies & empty-cluster handling
 4. vq                       : vector quantisation — assign observations to nearest centroid

PART C — LINKAGE CONSTRUCTION  (scipy.cluster.hierarchy)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 5. linkage                  : build linkage matrix from data or distance matrix
                               methods: single, complete, average, weighted,
                                        centroid, median, ward
 6. from_mlab_linkage /
    to_mlab_linkage          : MATLAB linkage format interop

PART D — FLAT CLUSTER EXTRACTION  (scipy.cluster.hierarchy)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 7. fcluster                 : cut linkage -> flat labels (distance / maxclust / monocrit)
 8. fclusterdata              : one-step: data -> linkage -> labels
 9. cut_tree                 : cut at multiple heights simultaneously
10. leaders                  : root node of each flat cluster

PART E — DENDROGRAM & VISUALISATION  (scipy.cluster.hierarchy)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. dendrogram               : plot / return dendrogram structure dict
12. leaves_list              : leaf ordering left-to-right in dendrogram

PART F — LINKAGE STATISTICS  (scipy.cluster.hierarchy)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
13. cophenet                 : cophenetic correlation coefficient
14. inconsistent             : inconsistency statistics per merge step
15. maxinconsts              : max inconsistency for each non-singleton cluster
16. maxdists                 : max merge distance within each cluster
17. maxRstat                 : max value of any column of inconsistent matrix

PART G — TREE STRUCTURE  (scipy.cluster.hierarchy)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
18. to_tree                  : convert linkage matrix to ClusterNode tree
19. ClusterNode              : node object — .id, .left, .right, .dist, .count
20. optimal_leaf_ordering    : reorder leaves to minimise dendrogram crossing

PART H — VALIDATION  (scipy.cluster.hierarchy)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
21. is_valid_linkage         : check linkage matrix correctness
22. is_valid_im              : check inconsistency matrix correctness
23. num_obs_linkage          : recover N from a linkage matrix
'''

import numpy as np
from scipy.cluster.vq import (
    whiten, kmeans, kmeans2, vq,
)
from scipy.cluster.hierarchy import (
    linkage, fcluster, fclusterdata, cut_tree, leaders,
    dendrogram, leaves_list,
    cophenet, inconsistent, maxinconsts, maxdists, maxRstat,
    to_tree, optimal_leaf_ordering,
    from_mlab_linkage, to_mlab_linkage,
    is_valid_linkage, is_valid_im, num_obs_linkage,
)
from scipy.spatial.distance import pdist, squareform

rng = np.random.default_rng(42)

# ── Synthetic datasets ────────────────────────────────────────────────────────
# Three well-separated 2-D Gaussian clusters
def make_blobs(n=40, centres=None, std=0.6, seed=42):
    rng_ = np.random.default_rng(seed)
    if centres is None:
        centres = np.array([[0., 0.], [5., 0.], [2.5, 4.]])
    parts = [rng_.normal(c, std, (n, 2)) for c in centres]
    X = np.vstack(parts)
    labels_true = np.repeat(np.arange(len(centres)), n)
    return X, labels_true

X, labels_true = make_blobs(n=30)   # 90 × 2, 3 clusters
X_1d = rng.normal(0, 1, (60, 1))    # 1-D data for simple demos


# =========================================================================================
#  PART A — PREPROCESSING  (scipy.cluster.vq) 
# =========================================================================================

##---------##
## whiten() #
##---------##
'''
whiten(obs, check_finite=True) -> ndarray
  Normalise each feature (column) of the observation matrix by dividing
  by that feature's standard deviation across all observations.

  This ensures every feature contributes equally to distance calculations,
  preventing features with large variance from dominating the clustering.

  obs : (M, N) array — M observations, N features.
  Returns an array of the same shape where each column has unit std dev.

  The name comes from signal processing: whitening removes inter-feature
  correlation and equalises power, like "white noise".

  IMPORTANT: always whiten BEFORE calling kmeans / kmeans2 / vq.
             Store the per-feature std so you can un-whiten centroids later:
               std = obs.std(axis=0)
               centroids_original = centroids_whitened * std
'''

X_w = whiten(X)

# Verify each column now has std ≈ 1
print("Std before whiten:", X.std(axis=0).round(4)) # [2.0371 1.9512]
print("Std after  whiten:", X_w.std(axis=0).round(4))   # [1. 1.]

# Store original std for back-transformation
X_std = X.std(axis=0)
print(f"Feature stds (for un-whitening): {X_std.round(4)}") # [2.0371 1.9512]

# Whitening on deliberately unequal-scale data
X_unequal = np.column_stack([
    rng.normal(0, 1,   90),   # feature A: std ~ 1
    rng.normal(0, 100, 90),   # feature B: std ~ 100
])
X_ueq_w = whiten(X_unequal)
print("Unequal scales, std after whiten:", X_ueq_w.std(axis=0).round(4))   # [1. 1.]


# =========================================================================================
#  PART B — K-MEANS  (scipy.cluster.vq) 
# =========================================================================================

##----------##
## kmeans() ##
##----------##
'''
kmeans(obs, k_or_guess, iter=10, thresh=1e-05, check_finite=True, seed=None)
  -> (codebook, distortion)

  Classic Lloyd's algorithm. Iterates until the distortion drops by less
  than thresh, or iter iterations are reached.

  obs          : (M, N) whitened observations.
  k_or_guess   : int  — number of clusters (random init from obs rows), OR
                 array of shape (k, N) — explicit initial centroids.
  iter         : number of restarts; best result (lowest distortion) is returned.
  thresh       : convergence threshold on change in distortion between iterations.
  seed         : random seed (for reproducible random initialisation).

  Returns:
    codebook   : (k, N) — final centroid coordinates (in whitened space).
    distortion : scalar — mean Euclidean distance from each obs to its centroid.

  Notes:
    • Distortion is comparable across runs only on the same whitened dataset.
    • iter > 1 runs multiple independent initialisations and keeps the best.
    • For better convergence use kmeans2 with init='++'.
'''

# Basic usage: find 3 centroids
codebook, distortion = kmeans(X_w, 3, seed=42)
print(f"kmeans distortion : {distortion:.4f}") # 0.3254
print("Centroids (whitened space):\n", codebook.round(4))
#  [[ 2.3991e+00 -5.6600e-02]
#  [ 3.6300e-02  2.2000e-03]
#  [ 1.2219e+00  2.0252e+00]]

# Un-whiten centroids to get them back in original units
centroids_orig = codebook * X_std
print("Centroids (original space):\n", centroids_orig.round(4))
#  [[ 4.8871e+00 -1.1040e-01]
#  [ 7.4000e-02  4.3000e-03]
#  [ 2.4891e+00  3.9515e+00]]

# Multiple restarts (iter=20) for more reliable convergence
cb_best, dist_best = kmeans(X_w, 3, iter=20, seed=0)
print(f"Best distortion over 20 restarts: {dist_best:.4f}") # 0.3254

# Explicit initial centroids (warm start)
init_centroids = X_w[[0, 30, 60]]   # pick one point from each true cluster
cb_warm, dist_warm = kmeans(X_w, init_centroids, seed=42)
print(f"Warm-start distortion: {dist_warm:.4f}") # 0.3254

# Elbow method: plot distortion vs k to choose the optimal k
distortions = []
k_range = range(1, 8)
for k in k_range:
    _, d = kmeans(X_w, k, iter=5, seed=0)
    distortions.append(d)
print("Distortion by k:", [f"{d:.3f}" for d in distortions])
# Distortion by k: ['1.391', '0.896', '0.325', '0.289', '0.257', '0.235', '0.224']
# Large drop from k=1->2->3, then flattens — elbow at k=3

##-----------##
## kmeans2() ##
##-----------##
'''
kmeans2(data, k, iter=10, thresh=1e-05, minit='random',
        missing='warn', check_finite=True, seed=None)
  -> (centroid, label)

  Enhanced k-means offering:
    • Better initialisation strategies (minit parameter).
    • Explicit handling of empty clusters (missing parameter).
    • Returns per-observation labels directly (unlike kmeans which needs vq).

  data   : (M, N) whitened observations.
  k      : int (number of clusters) or (k, N) initial centroids.
  iter   : number of Lloyd iterations (NOT restarts — use a loop for that).

  minit options:
    'random'   : choose k random rows from data as initial centroids. (default)
    'points'   : same as 'random' (alias).
    '++'       : k-means++ initialisation — spreads initial centroids to
                 reduce the chance of bad local minima. Preferred in practice.
    'matrix'   : k is interpreted as the (k, N) initial centroid matrix.

  missing options:
    'warn'     : emit a warning if a cluster becomes empty; centroid set to NaN.
    'raise'    : raise ClusterError if a cluster becomes empty.
    'drop'     : silently remove empty clusters.

  Returns:
    centroid : (k, N) — final centroid coordinates.
    label    : (M,)   — cluster index (0 to k-1) for each observation.

  Comparison with kmeans():
    kmeans()  -> (codebook, distortion)  # needs separate vq() for labels
    kmeans2() -> (centroid, label)       # labels included; no multi-restart
'''

# k-means++ init (better than random for non-spherical clusters)
centroid_pp, label_pp = kmeans2(X_w, 3, iter=30, minit='++', seed=42)
print("\nkmeans2 (++) label distribution:", np.bincount(label_pp))   # ~[30 30 30]
print("kmeans2 centroids (whitened):\n", centroid_pp.round(4))
#  [[ 2.3991e+00 -5.6600e-02]
#  [ 1.2219e+00  2.0252e+00]
#  [ 3.6300e-02  2.2000e-03]]

# Random init (may land in local minima on tough datasets)
centroid_rnd, label_rnd = kmeans2(X_w, 3, iter=30, minit='random', seed=42)
print("kmeans2 (random) label distribution:", np.bincount(label_rnd)) # [30 30 30]

# Verify quality: all 3 true clusters should map to distinct kmeans labels
# (Adjusted by permutation invariance)
from itertools import permutations
def cluster_accuracy(true, pred):
    best = 0
    for perm in permutations(np.unique(pred)):
        mapped = np.zeros_like(pred)
        for new, old in enumerate(perm):
            mapped[pred == old] = new
        best = max(best, (mapped == true).mean())
    return best

acc = cluster_accuracy(labels_true, label_pp)
print(f"kmeans2 (++) accuracy: {acc:.2%}")   # should be ~100% on well-separated blobs

# k=5 to see empty-cluster handling (more clusters than natural groups)
centroid_5, label_5 = kmeans2(X_w, 5, iter=20, minit='++', missing='warn', seed=0)
print(f"k=5 label distribution: {np.bincount(label_5)}") # [30  9 30  5 16]

# Explicit initial centroids via minit='matrix'
init_mat = X_w[np.array([0, 30, 60])]   # one seed per true cluster
centroid_m, label_m = kmeans2(X_w, init_mat, minit='matrix', iter=30)
print(f"kmeans2 (matrix init) accuracy: {cluster_accuracy(labels_true, label_m):.2%}") # 100%

##------##
## vq() ##
##------##
'''
vq(obs, code_book, check_finite=True) -> (code, dist)
  Vector quantisation: assign each observation to its nearest centroid.

  obs       : (M, N) whitened observations.
  code_book : (k, N) centroid coordinates (from kmeans or kmeans2).

  Returns:
    code : (M,)   int array — index of the nearest centroid for each obs.
    dist : (M,)   float array — Euclidean distance from obs to its centroid.

  vq is a "hard assignment" step. It is the E-step of the EM algorithm for
  Gaussian mixture models under equal-covariance and equal-weight assumptions.

  Use cases:
    • Quantise a new test set using a codebook trained on training data.
    • Compute per-observation distortion for outlier detection.
    • Image compression: replace each pixel block with its nearest code vector.
'''

# Assign all observations to nearest centroid from kmeans codebook
codes, dists = vq(X_w, codebook)
print("\nvq code distribution:", np.bincount(codes))   # ~[30 30 30]
print("Mean distance to centroid:", dists.mean().round(4)) # 0.3254
print("Max  distance to centroid:", dists.max().round(4)) # 1.0956

# Outlier detection: observations far from their centroid
threshold = np.percentile(dists, 95)
outliers  = np.where(dists > threshold)[0]
print(f"Outlier indices (top 5% distance): {outliers}") # [ 2 15 69 71 81]

# New observations (test set) quantised against training codebook
X_test = rng.normal(0, 1, (10, 2))
X_test_w = X_test / X_std           # apply same whitening scale as training
codes_test, dists_test = vq(X_test_w, codebook)
print(f"Test codes : {codes_test}") # [1 1 1 1 0 1 1 1 1 1]
print(f"Test dists : {dists_test.round(4)}") # [0.4695 1.1735 1.2067 1.1011 1.1147 0.2775 0.958  0.4261 0.2634 0.7142]

# Image compression analogy: reconstruct from codebook
X_reconstructed = codebook[codes] * X_std   # un-whiten
reconstruction_error = np.mean((X - X_reconstructed)**2)
print(f"MSE reconstruction error: {reconstruction_error:.4f}") # 0.2650


# =========================================================================================
#  PART C — LINKAGE CONSTRUCTION  (scipy.cluster.hierarchy) 
# =========================================================================================

##-----------##
## linkage() ##
##-----------##
'''
linkage(y, method='single', metric='euclidean', optimal_ordering=False)
  -> Z  (ndarray of shape (N-1, 4))

  Perform hierarchical / agglomerative clustering.

  y  : condensed distance vector (output of pdist), OR
       (N, d) observation matrix (distances computed internally).
       Passing a condensed vector is more memory-efficient.

  method : linkage criterion — how inter-cluster distance is defined:
    'single'   : d(A,B) = min distance between any point in A and any in B.
                 Produces long, "chained" clusters. Sensitive to outliers.
    'complete' : d(A,B) = max distance. Produces compact, roughly equal-size clusters.
    'average'  : d(A,B) = mean of all pairwise distances (UPGMA). Good general choice.
    'weighted' : d(A,B) weighted mean (WPGMA). Ignores cluster sizes.
    'centroid' : d(A,B) = Euclidean distance between centroids (UPGMC).
                 Can cause "inversions" (non-monotone dendrograms).
    'median'   : d(A,B) = median centroid distance (WPGMC). Also can invert.
    'ward'     : minimises total within-cluster variance (Ward's criterion).
                 Produces compact, balanced clusters. Requires Euclidean distance.

  optimal_ordering : if True, reorders leaves to minimise dendrogram crossings.

  Output Z — each row (i) represents one merge:
    Z[i, 0], Z[i, 1] : indices of the two clusters being merged.
                        Indices < N are original observations.
                        Indices >= N refer to previously formed clusters.
    Z[i, 2]          : distance between the merged clusters.
    Z[i, 3]          : number of original observations in the new cluster.

  After N-1 merges a single cluster containing all N points is formed.
'''

# From raw observations (euclidean metric is default)
Z_ward    = linkage(X, method='ward')
Z_single  = linkage(X, method='single')
Z_complete= linkage(X, method='complete')
Z_average = linkage(X, method='average')
Z_centroid= linkage(X, method='centroid')   # may produce inversions

print("Linkage matrix shape:", Z_ward.shape)       # (N-1, 4) = (89, 4)
print("First 3 merges (ward):\n", Z_ward[:3].round(4))
#  [[7.90e+01 8.60e+01 3.61e-02 2.00e+00]
#  [3.30e+01 4.10e+01 4.91e-02 2.00e+00]
#  [4.00e+00 1.80e+01 5.88e-02 2.00e+00]]
# Each row: [idx_a, idx_b, distance, cluster_size]

# From a pre-computed condensed distance matrix
Y_dist = pdist(X, metric='euclidean')
Z_from_pdist = linkage(Y_dist, method='ward')
print("Linkage from pdist equals from obs:",
      np.allclose(Z_ward, Z_from_pdist, atol=1e-10))   # True

# Different metrics (pass condensed distance vector)
Y_cos = pdist(X, metric='cosine')
Z_cos = linkage(Y_cos, method='average')

# Last merge always combines everything into one cluster
last_merge = Z_ward[-1]
print(f"Final merge: clusters {int(last_merge[0])} + {int(last_merge[1])}, "
      f"dist={last_merge[2]:.4f}, total_obs={int(last_merge[3])}")   # total_obs = N = 90

# Inspect distances to understand cluster structure
merge_dists = Z_ward[:, 2]
print(f"Merge distances — min: {merge_dists.min():.4f}, "
      f"max: {merge_dists.max():.4f}, "
      f"big gap at: {np.sort(np.diff(merge_dists))[-3:].round(4)}") # [ 1.0069  1.0397 20.9785]
# Large jumps between natural clusters signal the right number of groups

##-------------------------------------##
## from_mlab_linkage / to_mlab_linkage ##
##-------------------------------------##
'''
MATLAB's linkage uses 1-based indexing; scipy uses 0-based.

from_mlab_linkage(Z) : convert MATLAB linkage (1-based) -> scipy (0-based).
to_mlab_linkage(Z)   : convert scipy linkage (0-based)  -> MATLAB (1-based).

Only the first two columns (cluster indices) differ; distance and count are unchanged.
'''

Z_matlab = to_mlab_linkage(Z_ward)
Z_back   = from_mlab_linkage(Z_matlab)
print("MATLAB round-trip matches:", np.allclose(Z_back, Z_ward))   # True
print("MATLAB linkage first row:", Z_matlab[0])   
# [8.00000000e+01 8.70000000e+01 3.60847096e-02]
# indices are +1 vs scipy


# =========================================================================================
#  PART D — FLAT CLUSTER EXTRACTION  (scipy.cluster.hierarchy) 
# =========================================================================================

##------------##
## fcluster() ##
##------------##
'''
fcluster(Z, t, criterion='inconsistent', depth=2, R=None, monocrit=None)
  -> labels  (ndarray of shape (N,), dtype int, 1-based)

  Cut the linkage tree Z to form flat clusters.

  Z         : (N-1, 4) linkage matrix from linkage().
  t         : threshold value — meaning depends on criterion.

  criterion options:
    'distance'    : merge clusters whose linkage distance exceeds t into separate groups.
                    t is a distance threshold. Equivalent to drawing a horizontal
                    line on the dendrogram.
    'maxclust'    : form at most t clusters (cut at the merge that first creates t groups).
    'inconsistent': (default) use the inconsistency statistic; merges with
                    inconsistency > t form cluster boundaries.
    'maxclust_monocrit': like maxclust but using a monotone criterion array.
    'monocrit'    : form clusters based on a custom monotone criterion array.

  Returns 1-based integer labels (cluster 1, 2, ..., k).
  Note: label assignment is NOT guaranteed to be stable across scipy versions.
'''

# Distance threshold: cuts linkage tree where gap is large
# First, find a natural threshold from the dendrogram gap
sorted_dists = np.sort(Z_ward[:, 2])
gaps = np.diff(sorted_dists)
t_auto = sorted_dists[np.argmax(gaps) + 1] * 0.5 + sorted_dists[np.argmax(gaps)] * 0.5
print(f"\nAuto-threshold from largest gap: {t_auto:.4f}") # 14.8561

labels_dist = fcluster(Z_ward, t=t_auto, criterion='distance')
print("fcluster (distance) unique labels:", np.unique(labels_dist)) # [1 2 3]
print("fcluster (distance) counts:", np.bincount(labels_dist)[1:]) # [30 30 30]

# maxclust: directly request 3 clusters
labels_3 = fcluster(Z_ward, t=3, criterion='maxclust')
print(f"\nfcluster (maxclust=3) distribution: {np.bincount(labels_3)[1:]}") # [30 30 30]
print(f"Accuracy with true labels: {cluster_accuracy(labels_true, labels_3 - 1):.2%}") # 100%

# maxclust=2 and maxclust=5 for comparison
labels_2 = fcluster(Z_ward, t=2, criterion='maxclust')
labels_5 = fcluster(Z_ward, t=5, criterion='maxclust')
print(f"maxclust=2 distribution: {np.bincount(labels_2)[1:]}") # [30 60]
print(f"maxclust=5 distribution: {np.bincount(labels_5)[1:]}") # [30 12 18 16 14]

# inconsistent criterion (default): uses depth=2 look-back
labels_incon = fcluster(Z_ward, t=0.7, criterion='inconsistent', depth=2)
print(f"\nfcluster (inconsistent, t=0.7) unique labels: {np.unique(labels_incon)}")
# [ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
#  25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48
#  49 50 51 52 53 54 55 56 57 58 59 60]

# Compare linkage methods: do single / complete / average / ward agree?
for name, Z_m in [('single', Z_single), ('complete', Z_complete),
                   ('average', Z_average), ('ward', Z_ward)]:
    lbl = fcluster(Z_m, t=3, criterion='maxclust')
    acc = cluster_accuracy(labels_true, lbl - 1)
    print(f"  {name:<10} maxclust=3  accuracy={acc:.2%}")
  # single     maxclust=3  accuracy=100.00%
  # complete   maxclust=3  accuracy=100.00%
  # average    maxclust=3  accuracy=100.00%
  # ward       maxclust=3  accuracy=100.00%

##----------------##
## fclusterdata() ##
##----------------##
'''
fclusterdata(X, t, criterion='inconsistent', metric='euclidean',
             depth=2, method='single', R=None)
  -> labels  (ndarray shape (N,))

  Convenience wrapper: computes pdist + linkage + fcluster in one call.
  NOT recommended for large datasets (recomputes everything each call).
  Use it for quick exploration; for production use the three-step pipeline.

  X         : (N, d) observation matrix.
  t, criterion, depth : passed directly to fcluster.
  metric    : passed to pdist.
  method    : linkage method.
'''

labels_fcd = fclusterdata(X, t=3, criterion='maxclust',
                          method='ward', metric='euclidean')
print(f"\nfclusterdata accuracy: {cluster_accuracy(labels_true, labels_fcd - 1):.2%}") # 100%

##------------##
## cut_tree() ##
##------------##
'''
cut_tree(Z, n_clusters=None, height=None)
  -> (N, len(n_clusters)) int array of 0-based cluster labels

  Cut the linkage tree at multiple levels simultaneously.

  n_clusters : int or list of ints — number(s) of clusters to cut at.
  height     : float or list of floats — distance height(s) to cut at.
  At least one of n_clusters or height must be provided.

  Returns a 2-D array; each column corresponds to one cut.
  Labels are 0-based (unlike fcluster which is 1-based).

  Useful for exploring the entire hierarchy in one call rather than
  calling fcluster repeatedly.
'''

# Multiple cuts at once
cuts = cut_tree(Z_ward, n_clusters=[2, 3, 4, 5])
print("\ncut_tree shape:", cuts.shape)   # (90, 4) — 4 different partitions

for col, k in enumerate([2, 3, 4, 5]):
    lbl = cuts[:, col]
    acc = cluster_accuracy(labels_true, lbl)
    print(f"  k={k}: distribution={np.bincount(lbl)}, accuracy={acc:.2%}")
  # k=2: distribution=[60 30], accuracy=66.67%
  # k=3: distribution=[30 30 30], accuracy=100.00%
  # k=4: distribution=[30 30 16 14], accuracy=84.44%
  # k=5: distribution=[12 18 30 16 14], accuracy=71.11%

# Height-based cuts
h_vals = [1.0, 3.0, 8.0]
cuts_h = cut_tree(Z_ward, height=h_vals)
print(f"\nHeight cuts {h_vals} -> unique clusters per cut:",
      [len(np.unique(cuts_h[:, i])) for i in range(len(h_vals))])
# Height cuts [1.0, 3.0, 8.0] -> unique clusters per cut: [18, 7, 3]

##-----------##
## leaders() ##
##-----------##
'''
leaders(Z, T) -> (L, M)
  Find the "leader" (root node index) of each flat cluster.

  Z : linkage matrix.
  T : flat cluster labels (output of fcluster — 1-based).

  Returns:
    L : array of node indices (>= N are internal merge nodes).
    M : corresponding cluster labels in T.

  The leader of cluster c is the highest internal node such that all
  observations below it belong to c.  Useful for:
    • Identifying which merge in Z gave rise to each flat cluster.
    • Navigating the ClusterNode tree (see Part G).
'''

labels_for_leaders = fcluster(Z_ward, t=3, criterion='maxclust')
L, M = leaders(Z_ward, labels_for_leaders)
N_obs = len(X)
print(f"\nLeaders: node indices={L}, cluster labels={M}") # node indices=[175 176 174], cluster labels=[2 3 1]
print(f"Internal nodes (>= N={N_obs}): {L[L >= N_obs]}") # Internal nodes (>= N=90): [175 176 174]


# =========================================================================================
#  PART E — DENDROGRAM & VISUALISATION 
# =========================================================================================

##--------------##
## dendrogram() ##
##--------------##
'''
dendrogram(Z, p=30, truncate_mode=None, color_threshold=None,
           get_leaves=True, orientation='top', labels=None,
           count_sort=False, distance_sort=False,
           show_leaf_counts=True, no_plot=False,
           no_labels=False, leaf_font_size=None, leaf_rotation=None,
           leaf_label_func=None, show_contracted=False,
           link_color_func=None, ax=None, above_threshold_color='C0')
  -> dict

  Draw (or describe) the dendrogram for linkage matrix Z.

  Z              : linkage matrix.
  p              : for truncated dendrograms, show only the last p merges.
  truncate_mode  : None (full), 'lastp' (last p merges), 'level' (up to depth p).
  color_threshold: links below this distance are coloured differently.
                   Default: 0.7 * max(Z[:, 2]).
  orientation    : 'top', 'bottom', 'left', 'right'.
  labels         : (N,) array of leaf labels (strings).
  no_plot        : if True, skip drawing — just return the dict. Useful for
                   extracting leaf order or colours programmatically.

  Returns a dict with keys:
    'icoord', 'dcoord' : x/y coordinates of each link for matplotlib plotting.
    'ivl'              : leaf labels (left to right).
    'leaves'           : list of original observation indices (leaf order).
    'color_list'       : colour string for each link.
    'leaves_color_list': colour for each leaf.
'''

# no_plot=True — get structure without drawing
ddata = dendrogram(Z_ward, no_plot=True)
print("\nDendrogram leaf order (first 10):", ddata['leaves'][:10]) # [58, 44, 55, 32, 31, 37, 59, 39, 34, 45]
print("Number of links coloured:", len(set(ddata['color_list']))) # 4

# Truncated dendrogram: show only the top 10 merges
ddata_trunc = dendrogram(Z_ward, truncate_mode='lastp', p=10, no_plot=True)
print("Truncated ivl labels:", ddata_trunc['ivl']) # ['(14)', '(4)', '(12)', '(12)', '(5)', '(13)', '(16)', '(9)', '69', '(4)']

# colour_threshold: manual threshold to colour clusters
# (default is 0.7 * max_distance)
max_d = Z_ward[:, 2].max()
ddata_ct = dendrogram(Z_ward, color_threshold=0.5 * max_d, no_plot=True)

# With matplotlib (only run if display available)
try:
    import matplotlib
    matplotlib.use('Agg')   # non-interactive backend
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Full dendrogram
    dendrogram(Z_ward, ax=axes[0], color_threshold=0.5*max_d,
               above_threshold_color='grey', leaf_font_size=7)
    axes[0].set_title('Ward linkage — full dendrogram')
    axes[0].axhline(y=0.5*max_d, color='red', linestyle='--', label='cut')
    axes[0].legend()

    # Truncated (last 15 merges)
    dendrogram(Z_ward, ax=axes[1], truncate_mode='lastp', p=15,
               show_contracted=True, leaf_font_size=9)
    axes[1].set_title('Ward linkage — truncated (last 15 merges)')

    plt.tight_layout()
    plt.savefig('/tmp/dendrogram.png', dpi=100)
    plt.close()
    print("Dendrogram saved to /tmp/dendrogram.png")
except Exception as e:
    print(f"Matplotlib plot skipped: {e}")

##---------------##
## leaves_list() ##
##---------------##
'''
leaves_list(Z) -> ndarray of shape (N,)
  Return the left-to-right ordering of leaves in the dendrogram.
  Equivalent to dendrogram(Z, no_plot=True)['leaves'] but without
  computing the full dendrogram structure dict.

  Used to reorder a distance matrix so that nearby clusters are adjacent
  — the classic "clustered heatmap" ordering.
'''

order = leaves_list(Z_ward)
print("\nLeaf order (first 15):", order[:15]) # [58 44 55 32 31 37 59 39 34 45 54 57 40 49 56]

# Reorder distance matrix for a clustered heatmap layout
D_full = squareform(pdist(X))
D_reordered = D_full[np.ix_(order, order)]   # reorder rows and columns
print("D reordered shape:", D_reordered.shape)   # (90, 90), now block-diagonal
print("First block (top-left 5x5):\n", D_reordered[:5, :5].round(3))
#  [[0.    0.295 0.177 0.545 0.341]
#  [0.295 0.    0.128 0.25  0.208]
#  [0.177 0.128 0.    0.372 0.265]
#  [0.545 0.25  0.372 0.    0.352]
#  [0.341 0.208 0.265 0.352 0.   ]]


# =========================================================================================
#  PART F — LINKAGE STATISTICS 
# =========================================================================================

##------------##
## cophenet() ##
##------------##
'''
cophenet(Z, Y=None) -> (c, coph_dists)   if Y provided
                    -> c                  if Y is None (only correlation)

  Compute the cophenetic correlation coefficient.

  The cophenetic distance between two observations is the height at which
  they first join the same cluster in the dendrogram.
  The cophenetic correlation r_c measures how faithfully the hierarchical
  clustering preserves the original pairwise distances.

  Z : linkage matrix.
  Y : condensed pairwise distance vector (from pdist). If None, only c is returned.

  Returns:
    c          : Pearson correlation between original and cophenetic distances.
                 Range [-1, 1]; values near 1 mean the dendrogram is a good
                 representation of the pairwise distance structure.
                 r_c > 0.75 is generally considered a good fit.
    coph_dists : condensed array of cophenetic distances (same length as Y).

  Interpretation:
    High r_c (~0.9+) : dendrogram faithfully represents distances.
    Low  r_c (<0.6)  : cluster structure poorly reflected; consider another method.
'''

Y_pdist = pdist(X)
c_ward,    coph_w  = cophenet(Z_ward,    Y_pdist)
c_single,  _       = cophenet(Z_single,  Y_pdist)
c_complete,_       = cophenet(Z_complete,Y_pdist)
c_average, _       = cophenet(Z_average, Y_pdist)

print("\nCophenetic correlation:")
print(f"  ward    : {c_ward:.4f}") # 0.9428
print(f"  single  : {c_single:.4f}") # 0.9412
print(f"  complete: {c_complete:.4f}") # 0.9276
print(f"  average : {c_average:.4f}") # 0.9458
# average linkage typically has the highest cophenetic correlation

# Cophenetic distances are the dendrogram heights at which pairs first merged
print(f"Cophenetic distances — min: {coph_w.min():.4f}, max: {coph_w.max():.4f}") # min: 0.0361, max: 26.3522
print(f"# cophenetic distances: {len(coph_w)} = N*(N-1)/2 = {len(X)*(len(X)-1)//2}") # 4005 = N*(N-1)/2 = 4005

##----------------##
## inconsistent() ##
##----------------##
'''
inconsistent(Z, d=2) -> R  (ndarray of shape (N-1, 4))

  Compute inconsistency statistics for each merge step.
  For each merge i, look at the subtree of depth d below it.
  Collect all merge heights within that subtree, then compute:

  R[i, 0] : mean   of those merge heights.
  R[i, 1] : std    of those merge heights.
  R[i, 2] : count  of merges included.
  R[i, 3] : inconsistency coefficient = (Z[i,2] - R[i,0]) / R[i,1].
             How many std devs above the local mean is this merge?
             Large values indicate a merge that crosses a natural cluster boundary.

  d=2  : default look-back depth (typically sufficient).
  d=1  : consider only the immediate children.

  The inconsistency statistic is used by fcluster with criterion='inconsistent'.
'''

R = inconsistent(Z_ward, d=2)
print("\nInconsistency matrix (last 5 rows — top of tree):")
print(R[-5:].round(4))
#      mean    std   count  inconsistency
# [[ 2.3624  0.766   3.      1.1079]
#  [ 2.4664  0.7765  3.      1.1085]
#  [ 3.0284  1.3443  3.      0.9956]
#  [11.0131 12.423   3.      1.1537]
#  [18.3029 13.0795  3.      0.6154]]

# Merges with high inconsistency are natural cluster boundaries
high_incon = np.where(R[:, 3] > 2.0)[0]
print(f"Merges with inconsistency > 2.0: {high_incon}") # []
print(f"Their distances: {Z_ward[high_incon, 2].round(4)}") # []

# Depth=1 for a tighter local window
R_d1 = inconsistent(Z_ward, d=1)
print("R(d=1) last 3 rows:\n", R_d1[-3:].round(4))
#  [[ 4.3668  0.      1.      0.   ]
#  [25.3453  0.      1.      0.    ]
#  [26.3522  0.      1.      0.    ]]

##---------------##
## maxinconsts() ##
##---------------##
'''
maxinconsts(Z, R) -> MI  (ndarray shape (N-1,))

  For each non-singleton cluster (i.e. each merge step i), compute the
  maximum inconsistency coefficient of all merges in its subtree.

  Z : linkage matrix.
  R : inconsistency matrix (from inconsistent()).

  MI[i] is the max of R[j, 3] for all j in the subtree rooted at merge i.
  Use MI with criterion='monocrit' in fcluster to cut where the max
  inconsistency in the subtree exceeds a threshold.
'''

MI = maxinconsts(Z_ward, R)
print("\nmaxinconsts (last 5):", MI[-5:].round(4))
# [1.1389 1.154  1.1547 1.1547 1.1547]

# Use with monocrit in fcluster
labels_monocrit = fcluster(Z_ward, t=1.5, criterion='monocrit', monocrit=MI)
print(f"monocrit (t=1.5) distribution: {np.bincount(labels_monocrit)[1:]}") # [90]

##------------##
## maxdists() ##
##------------##
'''
maxdists(Z) -> MD  (ndarray shape (N-1,))

  For each merge step i, compute the maximum distance of any merge
  within its subtree (including itself).

  MD[i] is the largest Z[j, 2] for all j in the subtree rooted at merge i.
  For the root (last row), MD[-1] == Z[-1, 2] == max merge distance overall.

  Used with criterion='monocrit' in fcluster to cut based on the maximum
  within-cluster diameter rather than the immediate merge distance.
'''

MD = maxdists(Z_ward)
print("\nmaxdists (last 5):", MD[-5:].round(4)) # [ 3.2111  3.3271  4.3668 25.3453 26.3522]
print("Root maxdist (== max merge dist):", MD[-1].round(4), "==", Z_ward[-1, 2].round(4))
# Root maxdist (== max merge dist): 26.3522 == 26.3522

# fcluster with monocrit=maxdists: each cluster has diameter <= t
labels_md = fcluster(Z_ward, t=MD[np.searchsorted(MD, 3.0)],
                     criterion='monocrit', monocrit=MD)
print(f"maxdists monocrit distribution: {np.bincount(labels_md)[1:]}")
# maxdists monocrit distribution: [14 16 12 18 16 14]

##------------##
## maxRstat() ##
##------------##
'''
maxRstat(Z, R, i) -> MS  (ndarray shape (N-1,))

  For each merge step, compute the max value of column i of R within the subtree.

  Z : linkage matrix.
  R : inconsistency matrix (4 columns: mean, std, count, inconsistency).
  i : column index of R to maximise over (0=mean, 1=std, 2=count, 3=inconsistency).

  maxRstat(Z, R, 3) == maxinconsts(Z, R)   by definition.
  maxRstat(Z, R, 0) : max mean merge height in subtree.
  maxRstat(Z, R, 2) : max count (= depth of subtree).
'''

MS_col3 = maxRstat(Z_ward, R, 3)   # same as maxinconsts
MS_col0 = maxRstat(Z_ward, R, 0)   # max mean merge height in subtree
MS_col2 = maxRstat(Z_ward, R, 2)   # max count in subtree

print("\nmaxRstat col=3 (inconsistency) equals maxinconsts:", np.allclose(MS_col3, MI))   # True
print("maxRstat col=0 (max mean height) last 5:", MS_col0[-5:].round(4)) # [ 2.3624  2.4664  3.0284 11.0131 18.3029]
print("maxRstat col=2 (max count) last 5:", MS_col2[-5:]) # [3. 3. 3. 3. 3.]


# =========================================================================================
#  PART G — TREE STRUCTURE 
# =========================================================================================

##-----------##
## to_tree() ##
##-----------##
'''
to_tree(Z, rd=False) -> root  (or (root, node_list) if rd=True)

  Convert the linkage matrix Z into a tree of ClusterNode objects.
  This gives a proper tree API instead of working with the raw (N-1, 4) array.

  Z     : linkage matrix.
  rd    : if True, also return a flat list of all nodes (length 2N-1).

  Returns:
    root      : ClusterNode for the root of the tree (the final merge).
    node_list : (if rd=True) list of all 2N-1 nodes; indices 0..N-1 are
                leaf nodes (original observations), N..2N-2 are internal.
'''

root, node_list = to_tree(Z_ward, rd=True)
N_obs = len(X)
print(f"\nto_tree: root id={root.id}, root dist={root.dist:.4f}, "
      f"root count={root.count}")   # count = N = 90

print(f"Total nodes: {len(node_list)} = 2*{N_obs}-1 = {2*N_obs-1}")
# Total nodes: 179 = 2*90-1 = 179

# Leaves: nodes 0..N-1
leaves_nodes = [n for n in node_list if n.is_leaf()]
print(f"Leaf nodes: {len(leaves_nodes)}")   # 90

# Internal nodes: N..2N-2
internal_nodes = [n for n in node_list if not n.is_leaf()]
print(f"Internal nodes: {len(internal_nodes)}")   # 89

##-------------##
## ClusterNode ##
##-------------##
'''
ClusterNode attributes and methods:

  .id        : int — node identifier.
               Leaf nodes: id == observation index (0 to N-1).
               Internal nodes: id == N + merge_index (N to 2N-2).

  .left      : ClusterNode — left child (or None for leaf).
  .right     : ClusterNode — right child (or None for leaf).
  .dist      : float — merge distance (0.0 for leaf nodes).
  .count     : int — number of original observations in subtree.

  .is_leaf() : bool — True if this is a leaf node (no children).

  .pre_order(func=lambda x: x.id)
             : traverse the subtree in pre-order (left-to-right),
               applying func to each leaf. Returns list of results.
               Default: returns list of leaf ids (observation indices).

  .get_count() : same as .count.
  .get_id()    : same as .id.
  .get_left()  : same as .left.
  .get_right() : same as .right.
'''

# Navigate the top of the tree
print(f"\nRoot children: left.id={root.left.id}, right.id={root.right.id}") # left.id=174, right.id=177
print(f"Root left  : count={root.left.count}, dist={root.left.dist:.4f}") # count=30, dist=3.2111
print(f"Root right : count={root.right.count}, dist={root.right.dist:.4f}") # count=60, dist=25.3453

# pre_order: get all leaf indices under the root (same as leaves_list)
leaf_ids_preorder = root.pre_order(lambda x: x.id)
print(f"pre_order leaf ids match leaves_list: "
      f"{leaf_ids_preorder == list(leaves_list(Z_ward))}")   # True

# Find all leaves in a specific subtree (left child of root)
left_leaves = root.left.pre_order(lambda x: x.id)
print(f"Left subtree leaves ({len(left_leaves)}): {left_leaves[:10]}...")
# Left subtree leaves (30): [58, 44, 55, 32, 31, 37, 59, 39, 34, 45]...

# Custom traversal: collect (id, dist) pairs at each internal node
def collect_internal(node):
    if node.is_leaf():
        return []
    return [(node.id, round(node.dist, 4))] + \
            collect_internal(node.left) + collect_internal(node.right)

top_internals = collect_internal(root)[:5]   # first 5 in pre-order
print("Top internal nodes (id, dist):", top_internals)
# Top internal nodes (id, dist): [(178, np.float64(26.3522)), (174, np.float64(3.2111)), (168, np.float64(1.7222)), (143, np.float64(0.4747)), (125, np.float64(0.2711))]

# Compute depth of each leaf (useful for imbalance analysis)
def leaf_depths(node, depth=0):
    if node.is_leaf():
        return {node.id: depth}
    d = {}
    d.update(leaf_depths(node.left,  depth + 1))
    d.update(leaf_depths(node.right, depth + 1))
    return d

depths = leaf_depths(root)
depth_vals = list(depths.values())
print(f"Leaf depths — min: {min(depth_vals)}, max: {max(depth_vals)}, "
      f"mean: {np.mean(depth_vals):.1f}")
# Leaf depths — min: 4, max: 10, mean: 7.0

##-------------------------##
## optimal_leaf_ordering() ##
##-------------------------##
'''
optimal_leaf_ordering(Z, y, metric='euclidean')
  -> Z_ordered  (same shape as Z, (N-1, 4))

  Reorder the leaves of the dendrogram to minimise the sum of distances
  between adjacent leaves (Bar-Joseph et al. 2001 algorithm).
  This is the "optimal leaf ordering" used in clustered heatmaps to make
  the visualisation easier to interpret.

  Z      : linkage matrix.
  y      : condensed distance vector (from pdist) — OR —
           (N, d) observation matrix (distances computed internally).

  Returns a new linkage matrix with the same merges but reordered leaves.
  The new leaves_list(Z_ordered) gives the optimal order.

  Note: O(N³) algorithm — can be slow for N > 2000.
'''

Z_olo = optimal_leaf_ordering(Z_ward, X)
order_std = leaves_list(Z_ward)
order_olo = leaves_list(Z_olo)

# Measure adjacent-pair distance sum before and after reordering
def adjacent_dist_sum(X, order):
    pts = X[order]
    return np.sum(np.linalg.norm(np.diff(pts, axis=0), axis=1))

sum_std = adjacent_dist_sum(X, order_std)
sum_olo = adjacent_dist_sum(X, order_olo)
print(f"\nAdjacent-pair distance sum — standard: {sum_std:.4f}, OLO: {sum_olo:.4f}") # Adjacent-pair distance sum — standard: 47.6801, OLO: 36.7246
print(f"OLO improvement: {100*(sum_std - sum_olo)/sum_std:.1f}%")   # 23.0% (OLO <= standard)


# =========================================================================================
#  PART H — VALIDATION 
# =========================================================================================

##--------------------##
## is_valid_linkage() ##
##--------------------##
'''
is_valid_linkage(Z, warning=False, throw=False, name=None) -> bool

  Check whether Z is a valid linkage matrix.
  A valid linkage matrix satisfies:
    1. Shape is (N-1, 4) for some N >= 2.
    2. Columns 0 and 1 are integer indices in [0, 2N-2].
    3. Each merge index < N+i for merge i (no future references).
    4. Column 3 is a positive integer (cluster size >= 1).
    5. Column 2 is non-negative (distances >= 0).

  warning : if True, print a warning message on failure (rather than raising).
  throw   : if True, raise an exception on failure.
  name    : string label included in warning/error messages.
'''

print("\nis_valid_linkage(Z_ward):", is_valid_linkage(Z_ward))   # True

# Deliberately corrupt the linkage
Z_bad = Z_ward.copy()
Z_bad[0, 0] = -1   # invalid: negative cluster index
print("is_valid_linkage(Z_bad) :", is_valid_linkage(Z_bad))    # False

Z_bad2 = Z_ward.copy()
Z_bad2[0, 2] = -0.5   # invalid: negative distance
print("is_valid_linkage(Z_bad2):", is_valid_linkage(Z_bad2))   # False

# throw=True turns invalid linkage into an exception
try:
    is_valid_linkage(Z_bad, throw=True)
except Exception as e:
    print(f"Exception raised: {type(e).__name__}: {e}")
# Exception raised: ValueError: Linkage contains negative indices.

##---------------##
## is_valid_im() ##
##---------------##
'''
is_valid_im(R, warning=False, throw=False, name=None) -> bool

  Check whether R is a valid inconsistency matrix (output of inconsistent()).
  Conditions:
    1. Shape is (N-1, 4) for some N.
    2. Column 0 (mean) and column 2 (count) are non-negative.
    3. Column 1 (std) is non-negative.
    4. Column 2 (count) >= 1.
'''

print("\nis_valid_im(R):", is_valid_im(R))   # True

R_bad = R.copy()
R_bad[0, 2] = 0   # invalid: count of 0
print("is_valid_im(R_bad):", is_valid_im(R_bad))   # False

##-------------------##
## num_obs_linkage() ##
##-------------------##
'''
num_obs_linkage(Z) -> int

  Return the number of original observations N encoded in linkage matrix Z.
  Z has shape (N-1, 4), so N = Z.shape[0] + 1.
  This is a simple convenience function.
'''

N_recovered = num_obs_linkage(Z_ward)
print(f"\nnum_obs_linkage: {N_recovered} == len(X): {len(X)}")   # both 90


# =========================================================================================
#  END-TO-END WORKFLOWS (putting it all together) 
# =========================================================================================

print("\n" + "="*70)
print("WORKFLOW 1 — K-MEANS (vq module)")
print("="*70)
'''
Standard k-means workflow:
  1. whiten     : normalise features to unit variance.
  2. kmeans2    : find centroids (k-means++ init for robustness).
  3. vq         : assign observations to centroids (for new/test data).
  4. Evaluate   : distortion, silhouette, or domain-specific metric.
'''
X_w2 = whiten(X)
std2 = X.std(axis=0)

# Step 1: choose k via elbow (already computed above)
# Step 2: fit
c2, lbl2 = kmeans2(X_w2, 3, minit='++', iter=50, seed=0)

# Step 3: assign new observations
X_new = rng.normal(2.5, 1, (5, 2))
X_new_w = X_new / std2
codes_new, dists_new = vq(X_new_w, c2)
print(f"New obs cluster assignments: {codes_new}")
print(f"New obs distances to centroid: {dists_new.round(4)}")

# Step 4: per-cluster within-group sum of squares
_, all_dists = vq(X_w2, c2)
wgss = {}
for k in range(3):
    mask = (lbl2 == k)
    wgss[k] = (all_dists[mask]**2).sum()
    print(f"Cluster {k}: n={mask.sum()}, WGSS={wgss[k]:.4f}")


print("\n" + "="*70)
print("WORKFLOW 2 — HIERARCHICAL CLUSTERING (hierarchy module)")
print("="*70)
'''
Standard hierarchical workflow:
  1. pdist      : compute condensed pairwise distances.
  2. linkage    : build linkage tree (Ward is often a good default).
  3. cophenet   : validate that the tree represents distances well.
  4. dendrogram : visually identify the number of clusters.
  5. fcluster   : cut the tree to get flat labels.
  6. Validate   : compare to ground truth or use internal indices.
'''

# Step 1
Y_w2 = pdist(X, metric='euclidean')

# Step 2
Z_w2 = linkage(Y_w2, method='ward')

# Step 3: check cophenetic correlation
c_val, _ = cophenet(Z_w2, Y_w2)
print(f"Cophenetic correlation (Ward): {c_val:.4f}")

# Step 4: find the right k from the merge-distance gap
merge_d = Z_w2[:, 2]
gap     = np.diff(merge_d)
k_hat   = len(merge_d) - np.argmax(gap[::-1]) + 1   # +1 for fence-post
print(f"Estimated k from largest gap: {k_hat}")

# Step 5
lbl_hier = fcluster(Z_w2, t=k_hat, criterion='maxclust')

# Step 6
acc_hier = cluster_accuracy(labels_true, lbl_hier - 1)
print(f"Hierarchical accuracy: {acc_hier:.2%}")

# Inspect cluster sizes and leader nodes
L_h, M_h = leaders(Z_w2, lbl_hier)
for node_id, clust_lbl in zip(L_h, M_h):
    size = int(node_list[node_id].count) if node_id < len(node_list) else '?'
    print(f"  Cluster {clust_lbl}: leader node {node_id}, size={size}")


print("\n" + "="*70)
print("WORKFLOW 3 — COMPARING ALL LINKAGE METHODS")
print("="*70)

methods = ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward']
print(f"{'Method':<12} {'Cophenetic':>12} {'Accuracy(k=3)':>15} {'valid_linkage':>15}")
print("-" * 58)
for m in methods:
    try:
        Zm = linkage(Y_w2, method=m)
        c_m, _ = cophenet(Zm, Y_w2)
        lbl_m  = fcluster(Zm, t=3, criterion='maxclust')
        acc_m  = cluster_accuracy(labels_true, lbl_m - 1)
        valid  = is_valid_linkage(Zm)
        print(f"{m:<12} {c_m:>12.4f} {acc_m:>14.2%} {str(valid):>15}")
    except Exception as e:
        print(f"{m:<12} ERROR: {e}")
