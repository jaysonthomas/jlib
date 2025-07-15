import numpy as np

class Sensor:
  def __init__(self, x_hat, alpha):
    '''
    x_hat is the state estimate.
    Initialise the Sensor object with the initial altitude estimation. 
    '''
    self.x_hat = x_hat         
    self.alpha = alpha         
      
  def measure(self, x_t, sigma = 0.01):
    '''
    x_t is the drone's true state.
    sigma is the standard deviation of the normal distribution.
    Gaussian noise is added to the true measurement to simulate a realistic altitude measurement.
    '''
    self.z_t = x_t + np.random.normal(0.0, sigma)
    return self.z_t


  def estimate(self, z_t):
    '''
    Drone's altitude is estimated using the weighted (exponential) average method.
    '''
    self.x_hat = (self.alpha * self.x_hat) + (1 - self.alpha) * z_t
    return self.x_hat