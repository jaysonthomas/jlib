import numpy as np

class Logger:
  def __init__(self):
    self.reset()

  def reset(self):
    self.x = np.array([0.0, 0.0, 0.0, 0.0])
    self.z = 0.0
    self.zEstimate = 0.0

  def update(self, z_t, zEstimate_t, x_t):
    self.x = np.vstack((self.x, x_t))
    self.z = np.vstack((self.z, z_t))
    self.zEstimate = np.vstack((self.zEstimate, zEstimate_t))

  def get(self):
    return self.z, self.zEstimate, self.x