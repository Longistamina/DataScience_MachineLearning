'''
Chunking is a computational technique where we split huge data
into smaller chunks and process them one by one.

This enables processing large data on limited ressources (low RAM/VRAM),
but the trade-off is speed/performance.

-----------------------------------------------------------------------

This file demonstrates an example where we need to calculate a large NxN
distance matrix to file top_k nearest and farthest of large point clouds [N, 3]
'''

import numpy as np
from scipy.spatial.distance import cdist
from tldm import tldm

# ============================================================================================
# Example 1: compute chunked NxN distance matrix to find neareast and furthest neighbors
#            node-level chunking
# ============================================================================================

##------------------------------##
## Define `topk_chunk` function ##
##------------------------------##

def topk_chunk(coords: np.ndarray, knear: int, kfar: int, chunk_size: int) -> tuple[np.ndarray, np.ndarray]:
    x = coords
    n_max = len(x)

    # Validation
    assert knear < n_max, f"knear ({knear}) must be less than N ({n_max})"
    assert kfar < n_max, f"kfar ({kfar}) must be less than N ({n_max})"

    topk_near, topk_far = [], []

    for start in tldm(range(0, n_max, chunk_size)):
        end = min(start + chunk_size, n_max)

        # 1. Get the chunk of points (rows)
        x_chunk = x[start:end, :]
        chunk_len = end - start

        # 2. Compute distances: shape (chunk_len, n_max)
        dist = cdist(x_chunk, x)

        # 3. EXCLUDE SELF: Set distance to self to infinity
        #    The global indices of the points in this chunk are [start, start+1, ..., end-1]
        #    The local indices are [0, 1, ..., chunk_len-1]
        #    So, for local row i, the global column is (start + i)

        # Create a mask of the diagonal positions
        # local_rows = 0..chunk_len-1
        # global_cols = start..end-1
        local_indices = np.arange(chunk_len)
        global_indices = np.arange(start, end)

        # Set these specific cells to -inf
        dist[local_indices, global_indices] = -np.inf

        # 4. Sort
        sorted_idx = np.argsort(dist, axis=1)

        # 5. Extract top-k
        # Since self is now -inf, it will be sorted to the START.
        # So the first knear are the self, must get from `1 : knear+1`.
        # The last kfar are the true farthest.
        topk_near.append(sorted_idx[:, 1 : knear+1])
        topk_far.append(sorted_idx[:, -kfar:])

    topk_near = np.concatenate(topk_near, axis=0)
    topk_far = np.concatenate(topk_far, axis=0)

    return topk_near, topk_far

##--------##
## Run!!! ##
##--------##

N = 100_000
np.random.seed(42)
p = np.random.uniform(0, 100, size=(N, 3))

knear = 10
kfar = 20
chunk_size = 128

topk_near, topk_far = topk_chunk(coords=p, knear=knear, kfar=kfar, chunk_size=chunk_size)

print(topk_near.shape) # (100000, 10)
print(topk_far.shape) # (100000, 20)

# ============================================================================================
# Example 2: compute chunked NxN distance matrix then compute mean distance
#            edge_level chunking
# ============================================================================================

##-----------------------------------##
## Define `mean_dist_chunk` function ##
##-----------------------------------##

def mean_dist_chunk(coords: np.ndarray, chunk_size: int) -> np.ndarray:
    x = coords
    n = len(x)

    edges_per_node = n
    n_max = n * edges_per_node

    out = np.zeros(n)
    denom = np.zeros(n)
    for start in tldm(range(0, n_max, chunk_size)):
       end = min(start + chunk_size, n_max)

       # Generate chunked src, dst on the fly
       e = np.arange(start, end, dtype=np.int64)
       src = e // edges_per_node # [0, 0, 0, 0, ...., 1, 1, 1, 1, ....]
       dst = e % edges_per_node # [0, 1, 2, 3, ...., 0, 1, 2, 3, ...]

       keep = src != dst # remove self-loop
       src, dst = src[keep], dst[keep]

       vec = x[src, :] - x[dst, :]
       dist = np.linalg.norm(x=vec, axis=1)

       dist_sums = np.zeros(n)
       np.add.at(dist_sums, src, dist)
       out += dist_sums

       denom_sums = np.zeros(n)
       np.add.at(denom_sums, src, np.ones_like(src))
       denom += denom_sums

    return out / denom

##--------##
## Run!!! ##
##--------##

N = 100_000
np.random.seed(42)
p = np.random.uniform(0, 100, size=(N, 3))

mean_dist = mean_dist_chunk(coords=p, chunk_size=10_000_000)

print(mean_dist)

'''
def mean_dist_chunk(coords: np.ndarray, chunk_size: int) -> np.ndarray:
    x = coords
    n = len(x)

    edges_per_node = n - 1
    n_max = n * edges_per_node

    out = np.zeros(n)
    denom = np.zeros(n)
    for start in range(0, n_max, chunk_size):
       end = min(start + chunk_size, n_max)

       e = np.arange(start, end, dtype=np.int64)
       src = e // edges_per_node
       col = e % edges_per_node
       dst = np.where(col < src, col, col + 1)

       vec = x[src, :] - x[dst, :]
       dist = np.linalg.norm(x=vec, axis=1)

       dist_sums = np.zeros(n)
       np.add.at(dist_sums, src, dist)
       out += dist_sums

       denom_sums = np.zeros(n)
       np.add.at(denom_sums, src, np.ones_like(src))
       denom += denom_sums

    return out / denom
'''
