import numpy as np

class Sensor:
  def __init__(self, sigma=0.01):
    self.sigma = sigma    
      
  def measure(self, x_t):
    '''
    x_t is the drone's true state.
    sigma is the standard deviation of the normal distribution.
    Gaussian noise is added to the true measurement to simulate a realistic altitude measurement.
    '''
    return x_t + np.random.normal(0.0, self.sigma)