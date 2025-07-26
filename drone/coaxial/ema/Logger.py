import numpy as np

class Logger:
  def __init__(self):
    self.reset()

  def reset(self):
    self.x = np.array([0.0, 0.0, 0.0, 0.0])
    self.z = 0.0
    self.x_hat = 0.0

  def update(self, z_t, x_hat_t, x_t):
    self.x = np.vstack((self.x, x_t))
    self.z = np.vstack((self.z, z_t))
    self.x_hat = np.vstack((self.x_hat, x_hat_t))

  def get(self):
    return self.z, self.x_hat, self.x