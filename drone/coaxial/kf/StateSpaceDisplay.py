import numpy as np 
import math
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

from .Plotter import Plotter

def getFlippedMu(mu):
  return [mu[1,0], mu[0,0]]

def getFlippedSigma(sigma):
  return np.array([[sigma[1,1], sigma[0,1]], 
                  [sigma[1,0], sigma[0,0]]])

def getFlipped(mu, sigma):
  return getFlippedMu(mu), getFlippedSigma(sigma)

def state_space_display(mu_0, sigma_0, mu_bar, sigma_bar, mu_updated,sigma_updated):
  mu_0, sigma_0 = getFlipped(mu_0, sigma_0)
  mu_bar, sigma_bar = getFlipped(mu_bar, sigma_bar)
  mu_updated, sigma_updated = getFlipped(mu_updated,sigma_updated)

  v = mu_0[1]
  z = mu_0[0]
  yAxisLimit = np.array([v-2, v+2])
  xAxisLimit = np.array([z-3, z+3])

  delta = 0.05
  x, y = np.mgrid[xAxisLimit[0]:xAxisLimit[1]:delta, 
                  yAxisLimit[0]:yAxisLimit[1]:delta]
    
  # A 3rd dimension is added. Each element of the 3D array is 2D.
  configuration_space = np.empty(x.shape + (2,))
  configuration_space[:, :, 0] = x; configuration_space[:, :, 1] = y

  plotter = Plotter()
  plotter.plotDistAsContour(mu_0, sigma_0, configuration_space, 'Green')        # Initial state space
  plotter.plotDistAsContour(mu_bar, sigma_bar, configuration_space, 'Red')      # Predicted state space
  plotter.plotDistAsContour(mu_updated, sigma_updated, configuration_space, 'Black')      # Updated state space  

  plotter.plotArrow(mu_0[0], mu_0[1], mu_bar[0], mu_bar[1])
  plotter.display(['Initial','Predicted', 'Updated'])
