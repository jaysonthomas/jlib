from time import perf_counter

class TimeManager:
  def __init__(self, dt = 0.001):
    self.startTime = perf_counter()
    self.lastUpdate = 0
    self.dt = dt

  def isItTimeToUpdatePlot(self):
    elapsedTime = perf_counter() - self.startTime
    if elapsedTime >= self.dt + self.lastUpdate:
      self.lastUpdate = elapsedTime
      return True
    
    return False