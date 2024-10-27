
A `TrainableDictionary` is a subclass of [[Dictionary.md|Dictionary]].
It contains a trainable neural network and $N_y$ non-trainable outputs,
mapping $\Psi: \mathbb{R}^{N \times N_x} \rightarrow \mathbb{R}^{N \times N_{\psi}}$.

## Attributes

- `__Ny` (int): The number of non-trainable outputs.

!!! info
    The attribute `_function` inherited from `Dictionary` should be an instance of `torch.nn.Module`.

## Methods

- `__init__(self, func, Nx, Npsi, Ny)`
    - `func` (torch.nn.Module): The trainable neural network.
    - `Nx` (int): The dimension of the input.
    - `Npsi` (int): The dimension of the output.
    - `Ny` (int): The number of non-trainable outputs.
- `parameters(self)`: Return the trainable parameters of the network `_function`.

