import numpy as np

class EMA:
  @staticmethod
  def getAlpha(ts, tss):
    return np.pi/((tss/ts) + np.pi)

  @staticmethod
  def getFc(alpha, ts):
    return alpha / (2 * np.pi * ts * (1-alpha))