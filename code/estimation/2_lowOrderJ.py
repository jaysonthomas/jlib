import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt

I = np.array([0.2, 0.3, 0.4, 0.5, 0.6])
y = np.array([1.23, 1.38, 2.06, 2.47, 3.17])

H = np.ones((5,2))
H[:, 0] = I

x_ls = LA.pinv(H.T @ H) @H.T @y
print(f'The slope and offset parameters of the best-fit line are [R_1, R_0]: {x_ls}')

I_line = np.arange(0, 0.8, 0.1)
y_line = x_ls[0]*I_line + x_ls[1]

plt.scatter(I, y)
plt.plot(I_line, y_line)
plt.xlabel('current (A)')
plt.ylabel('voltage (y)')
plt.grid(True)
plt.show()
