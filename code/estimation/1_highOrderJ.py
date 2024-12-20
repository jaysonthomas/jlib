import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as LA

def generateH(k, m):
  """
  Creates a matrix where each row is of the form: 
  [t**degree, t**(degree-1), ..., 1] 
  """
  t = np.random.uniform(-5, 5, k)
  H = np.zeros((k, m))
  for i in np.arange(m-1, -1, -1):
    H[:, -i-1] = t**i
  return H, t

def collectMeasurements(x, k, m):
  H, t = generateH(k, m)
  # Create m noisy observations, where the noise distribution is gaussian
  y = H @ x + np.random.normal(0, 1, size=(k))
  plt.plot(t, y, 'bx')
  plt.title("Noisy Observations")
  plt.show()

  return y, H

# Setup
k = 100
m = 4
x = np.random.randn(m) * 2 # np.array([8, 4, 2, 1])

y, H = collectMeasurements(x, k, m)
print(f'H: {H.shape}')
xHat = LA.pinv(H.T @ H) @ H.T @ y

print(xHat)
print(x)

