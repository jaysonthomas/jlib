import numpy as np
import timing

class RK4:
  def __init__(self, f, timing, y0):
    self.h = timing.h
    self.t = timing.t

    # Preallocate solution array
    self.y = np.zeros((timing.nInstances, 2))
    self.y[0] = y0  # Initial condition

    self.f = f

  def step(self, i):
    '''
    Runge-Kutta 4th order method
    '''
    k1 = self.f(self.y[i]) * self.h    # Approximate derivative at current y

    y1 = self.y[i] + k1 / 2
    k2 = self.f(y1) * self.h           # Approximate derivative at first intermediate step

    y2 = self.y[i] + k2 / 2
    k3 = self.f(y2) * self.h            # Approximate derivative at second intermediate step

    y3 = self.y[i] + k3
    k4 = self.f(y3) * self.h            # Approximate derivative at final step

    # Compute the next state
    self.y[i + 1] = self.y[i] + (k1 + (2 * k2) + (2 * k3) + k4) / 6
    return self.y[i + 1], self.t[i+1]
  