'''
This file talks about permutation and reshaping arrays/tensors
in multi-head attention mechanism (mha).

B: batch
N: array length
D: highly expressive dimension
H: head
Dh: dim of each head
(H * Dh = D)

In mha, from an array of [B, N, D],
we need to split it into multiple heads
like this [B, H, N, Dh] before moving to the next step.

Our original tensor has shape `[B, N, D]`.
For each batch item and each token/array position,
its `D` features are stored together:
```
[B, N, D]
       └── one token's D features
```

To create `H` heads, we want to
split each token's `D` features into `H × Dh`:
```array.reshape(B, N, H, Dh)```

This gives:
```[B, N, H, Dh]```

But attention needs the head dimension before the sequence dimension:
```[B, H, N, Dh]```

So we then swap (permute) the `N` and `H` axes:
```array.reshape(B, N, H, Dh).permute(0, 2, 1, 3)```

or, equivalently:
```array.reshape(B, N, H, Dh).transpose(1, 2)```

-------------------------------------------------------------------------------------

Why not directly use `array.reshape(B, H, N, Dh)`?

Because that would divide the original flat sequence in the wrong order.
It would treat the data as though the head dimension came before the token dimension,
grouping features across different tokens into a head.

In reality, we want to split the features of "each individual token" into heads first,
and only then move the head axis to the desired position.

In short:
```
Correct:
[B, N, D] → [B, N, H, Dh] → [B, H, N, Dh]
              split D              reorder axes

Incorrect:
[B, N, D] → [B, H, N, Dh]
              reshape interprets the elements in the wrong grouping
```

`reshape` changes how we "group" consecutive elements.
`permute` / `transpose` changes the "order of axes".

-------------------------------------------------------------------------------------

0. Create a Linear class that emulates Pytorch Linear

1. Example with common arrays/tensors:
   [B, N, low] -> [B, N, D] -> [B, N, H, Dh] -> [B, H, N, Dh]

2. Example with equivariant arrays/tensors:
   [B, N, C] -> [B, N, C, 1] -> [B, N, C, D] -> [B, N, C, H, Dh] -> [B, H, N, C, Dh] -> [B, H, N, C*Dh]
'''

import numpy as np

np.set_printoptions(linewidth=200, suppress=True)

# ========================================================================================
# 0. Create a Linear class that emulates Pytorch Linear
# ========================================================================================

class Linear:
    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        self.in_features = in_features
        self.out_features = out_features

        bound = np.sqrt(1 / in_features)
        self.weights = np.random.uniform(-bound, bound, size=(out_features, in_features))

        if bias:
            self.bias = np.random.uniform(-bound, bound, size=out_features)
        else:
            self.bias = None

    def __call__(self, input: np.ndarray):
        assert input.ndim >= 2, "The input must have 2 or more dimensions"

        *remain, _, _ = input.shape
        dims_to_expand = np.ones(len(remain)).astype(np.int64)

        if self.bias is not None:
            return input @ self.weights.reshape(*dims_to_expand, self.out_features, self.in_features).swapaxes(-1, -2) + self.bias
        else:
            return input @ self.weights.reshape(*dims_to_expand, self.out_features, self.in_features).swapaxes(-1, -2)

# ========================================================================================
# 1. Example with common arrays/tensors:
#    [B, N, low] -> [B, N, D] -> [B, N, H, Dh] -> [B, H, N, Dh]
# ========================================================================================

batch = 3
n = 15
dim = 16
heads = 2

array_common = np.random.randn(batch, n, 4)
linear_common = Linear(4, dim)

out_common = linear_common(array_common) # [B, N, low] -> [B, N, dim]
out_common = out_common.reshape(batch, n, heads, -1) # [B, N, dim] -> [B, N, heads, dim_head]
out_common = out_common.swapaxes(1, 2) # [B, N, heads, dim_head] -> [B, heads, N, dim_head]

print(out_common.shape)
# (3, 2, 15, 8)

# =============================================================================================================
# 2. Example with equivariant arrays/tensors:
#    [B, N, C] -> [B, N, C, 1] -> [B, N, C, D] -> [B, N, C, H, Dh] -> [B, H, N, C, Dh] -> [B, H, N, C*Dh]
# =============================================================================================================
'''
For arrays/tensors operations that require equivariance,
we cannot transform directly from [B, N, C] -> [B, N, D]
because it will break equivariance.
(The typical examples are batches of 3D point cloud coordinates [B, N, 3])
=> Why? Because directly transform like above
   makes different channels C (x-y-z axes) mix together,
   which destroys the equivariance.

In such situations, we need to unsqueeze the arrays/tensors into [B, N, C, 1] first,
then transform into higher dimension [B, N, C, D] laters.
This keeps the channels C unmixed -> Preserve equivariance.

Moreover, in order to maintain equivariance, we must not apply bias (bias=False),
meaning `out = in @ A.T` only (not `out = in @ A.T + bias`).

After achieving [B, N, C, D], we can then split into multiple heads and permute the dimensions.
'''

batch = 4
n = 15
channels = 3
dim = 16
heads = 2

array_equi = np.random.randn(batch, n, channels) # [B, N, C]
linear_equi = Linear(1, dim)

out_equi = linear_equi(array_equi[..., None]) # [B, N, C] -> [B, N, C, 1] -> [B, N, C, D]
out_equi = out_equi.reshape(batch, n, channels, heads, -1) # [B, N, C, D] -> [B, N, C, heads, dim_head]
out_equi = out_equi.transpose(0, 3, 1, 2, 4) # [B, heads, N, C, dim_head]
out_equi = out_equi.reshape(batch, heads, n, -1) # [B, heads, N, C*dim_head]

print(out_equi.shape)
# (4, 2, 15, 24)

'''
At the final step, why convert the arrays to [B, heads, N, C*dim_head]
but not keep it as [B, heads, N, C, dim_head]?

Because, we need to perform the matmul(Q, K.transpose())
to get the [B, heads, N, N] attention score array.

Q = [B, heads, N, C*dim_head]
K.transpose() = [B, heads, C*dim_head, N]

=> matmul(Q, K.transpose()) = [B, heads, N, N]

(
If we keep [B, heads, N, C, dim_head],
then the output will be [B, heads, N, C, C]
=> wrong
)
'''
