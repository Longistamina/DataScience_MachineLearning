'''
PyTorch also supports GPU acceleration for tensor computations using CUDA.

The difference between PyTorch and CuPy is that PyTorch supports autograd engine for back progapation
(CuPy does not).
'''

import torch

torch.set_printoptions(linewidth=1000)

##########################
## Create Tensor on GPU ##
##########################

torch.manual_seed(0)
tensor = torch.rand(10000, 10000, device='cuda:0')

print(tensor)
# tensor([[0.3990, 0.5167, 0.0249,  ..., 0.9971, 0.8137, 0.0429],
#         [0.1117, 0.5124, 0.6413,  ..., 0.2033, 0.4244, 0.7405],
#         [0.7685, 0.7422, 0.4577,  ..., 0.5380, 0.1010, 0.4636],
#         ...,
#         [0.5471, 0.9743, 0.9763,  ..., 0.6386, 0.4802, 0.0591],
#         [0.4013, 0.6963, 0.8307,  ..., 0.6674, 0.3551, 0.0153],
#         [0.2846, 0.1924, 0.9891,  ..., 0.1611, 0.7280, 0.1510]], device='cuda:0')

print(tensor.device)
# cuda:0

print(tensor.requires_grad)
# False

######################
## Demo calculation ##
######################

# Pseudo-inverse
print(torch.pinverse(tensor))
# tensor([[-0.0370,  0.0311, -0.0813,  ..., -0.0195, -0.0050, -0.0555],
#         [-0.0552,  0.0350, -0.1106,  ..., -0.0235, -0.0035, -0.0428],
#         [ 0.0049, -0.0107,  0.0170,  ..., -0.0019, -0.0042, -0.0021],
#         ...,
#         [ 0.0281, -0.0224,  0.0471,  ...,  0.0060, -0.0038,  0.0283],
#         [ 0.0188, -0.0081,  0.0435,  ...,  0.0046, -0.0094,  0.0152],
#         [-0.0022,  0.0090, -0.0208,  ...,  0.0140, -0.0094, -0.0224]], device='cuda:0')
'''Takes a very long time to compute....'''
