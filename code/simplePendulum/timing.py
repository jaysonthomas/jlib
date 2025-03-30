import numpy as np

class Timing:
  def __init__(self, start, end, fps):
    self.start = start
    self.end = end
    self.h = 1/fps      # step size

    self.t = np.arange(start, end + self.h, self.h)
    self.nInstances = len(self.t)
