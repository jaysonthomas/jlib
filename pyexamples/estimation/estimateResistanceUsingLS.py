import numpy as np
import matplotlib.pyplot as plt

# Column vectors.
I = np.mat([0.2, 0.3, 0.4, 0.5, 0.6]).T
V = np.mat([1.23, 1.38, 2.06, 2.47, 3.17]).T

H = I
y = V
R = np.linalg.inv(np.dot(H.T, H)) * H.T * y

print('The slope parameter (i.e., resistance) for the best-fit line is:')
print(f'{R}\n{R[0,0]}')

R = R[0,0]
I_line = np.arange(0, 0.8, 0.1)
V_line = R*I_line

plt.scatter(np.asarray(I), np.asarray(V))
plt.plot(I_line, V_line)
plt.xlabel('current (A)')
plt.ylabel('voltage (V)')
plt.grid(True)
plt.show()