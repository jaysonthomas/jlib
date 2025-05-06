import numpy as np

class WaveManager():
  def __init__(self, f, tMin=0, tMax=1):
    '''
    f is the sampling frequency.
    t contains the time instances when samples are taken
    '''
    f = 100                
    ts = 1/f
    self.t = np.arange(tMin, tMax, ts)

  def create(self, f, a):
    x = 0
    for freq, amplitude in zip(f, a):
      x += amplitude * np.sin(2 * np.pi * freq * self.t)

    return x


