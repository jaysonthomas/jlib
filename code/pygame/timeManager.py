from time import perf_counter

class TimeManager:
  def __init__(self, dt = 0.001):
    self.startTime = perf_counter()
    self.lastUpdate = 0
    self.dt = dt

  def isItTimeToUpdatePlot(self):
    self.currentTime = perf_counter() - self.startTime
    if self.currentTime > self.dt + self.lastUpdate:
      self.lastUpdate = self.currentTime
      return True
    
    return False