import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as LA

def generateH(m, n):
  """
  Creates a matrix where each row is of the form: 
  [t**degree, t**(degree-1), ..., 1] 
  """
  t = np.random.uniform(-5, 5, m)
  H = np.zeros((m, n))
  for i in np.arange(n-1, -1, -1):
    H[:, -i-1] = t**i
    # print(f'a{-i-1}, {t**i}')
  return H, t

def collectMeasurements(x, m, n):
  H, t = generateH(m, n)
  # Create m noisy observations, where the noise distribution is gaussian
  yTilde = H @ x + np.random.normal(0, 1, size=(m))
  print(f'yTilde {yTilde.shape}: {yTilde}')
  plt.plot(t, yTilde, 'bx')
  plt.title("Noisy Observations")
  plt.show()

  return yTilde, H

# Setup
# m: number of samples/measurements - the larger the value the more accurate x hat will be.
# n: size of state
# x: state, unknown in practice
m = 100
n = 4
x = np.random.randn(n) * 2 # np.array([8, 4, 2, 1])

yTilde, H = collectMeasurements(m, n)
print(f'H: {H.shape}')
xHat = LA.pinv(H.T @ H) @ H.T @ yTilde

print(xHat)
print(x)

