import numpy as np

class DFT():
  def __init__(self, input):
    '''
    Input wave signal.
    '''
    self.x = input
    self.N = len(input)

  def getAmplitudeOfFreqs(self):
    X = []

    for k in range(self.N):
      X_k = 0

      for n in range(self.N):
        e = np.exp(2j * np.pi * k * n/self.N)
        X_k += self.x[n]/e

      X.append(X_k)

    return np.array(X)

  def getAmplitudeOfFreqsVectorised(self):
    n = np.arange(self.N)
    k = n.reshape((self.N, 1))
    e = np.exp(-2j * np.pi * k * n/self.N)

    return np.dot(e, self.x)
  
  def getFreqs(self):
    return list(range(0, self.N))