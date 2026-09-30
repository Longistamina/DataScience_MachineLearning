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
   [B, N, L] -> [B, N, L, 1] -> [B, N, L, D] -> [B, N, L, H, Dh] -> [B, H, N, L, Dh] -> [B, H, N, L*Dh]
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


linear = Linear(8, 16)
x = np.random.randn(10, 8)
y = linear(x)

print(y.round(3))
