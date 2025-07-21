import numpy as np

class EMAEstimator:
  def __init__(self, x_hat, alpha):
    """
    x_hat is the state estimate.
    Initialise the Estimator object with the initial altitude estimation.
    """
    self.x_hat = x_hat
    self.alpha = alpha

  def estimate(self, z_t):
    self.x_hat = (self.alpha * self.x_hat) + (1 - self.alpha) * z_t
    return self.x_hat
