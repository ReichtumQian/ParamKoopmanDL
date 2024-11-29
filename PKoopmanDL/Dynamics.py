import torch
from tqdm import tqdm


class DiscreteDynamics:

  def __init__(self, trans_func, dim, param_dim=0):
    self._trans_func = trans_func
    self._dim = dim
    self._param_dim = param_dim

  def step(self, x, u):
    return self._trans_func.step(x, u)

  @property
  def dim(self):
    return self._dim

  @property
  def param_dim(self):
    return self._param_dim

  def traj(self, x0, u0, traj_len):
    x = [x0]
    # if do not need parameter
    if u0 == None:
      u0 = torch.zeros(1, 1)
    # if the parameters are time-independent
    if u0.size(0) == 1:
      u = u0.expand(traj_len - 1, -1)
    else:
      assert (u0.size(0) == traj_len - 1)
      u = u0
    for i in range(traj_len - 1):
      x.append(self.step(x[-1], u[i].unsqueeze(0)))
    return torch.stack(x, dim=1)  # size: (N, traj_len, number of state)


class KoopmanDynamics(DiscreteDynamics):
  """Koopman Dynamics of the form \\Psi_{n+1} = K \\Psi_n.
     The states are updated from the dictionary's output
  """

  def __init__(self, koopman, dictionary, state_pos, state_dim, param_dim=0):
    super().__init__(koopman, state_dim, param_dim)
    self._dictionary = dictionary
    self._state_pos = state_pos

  def step(self, x, u):
    psi = self._dictionary(x)
    return self._trans_func.step(psi, u)[:, self._state_pos]


class KoopmanODEDynamics(DiscreteDynamics):
  """Koopman Dynamics of the form \\Psi_{n+1} = K \Psi_n.
     The states x are obtained from the ODESolver.
  """

  def __init__(self, ode_solver, koopman, dictionary, state_dim, param_dim=0):
    super().__init__(koopman, state_dim, param_dim)
    self._koopman = koopman
    self._dictionary = dictionary
    self._ode = ode_solver

  def step(self, x, u):
    psi = self._dictionary(x)
    return self._trans_func.step(psi, u)

  def traj(self, x0, u0, traj_len):
    if u0.size(0) == 1:
      u = u0.expand(traj_len, -1)
    else:
      assert u0.size(0) == traj_len - 1
      u = u0
    x = [self._dictionary(x0)]
    state = x0
    for i in tqdm(range(traj_len - 1), desc='Generating trajectory'):
      x.append(self.step(state, u[i].unsqueeze(0)))
      state = self._ode.step(state, u[i].unsqueeze(0))
    return torch.stack(x, dim=1)  # size: (N, traj_len, number of state)
