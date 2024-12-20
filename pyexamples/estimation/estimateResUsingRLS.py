import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt

I = np.array([0.2, 0.3, 0.4, 0.5, 0.6])
y = np.array([1.23, 1.38, 2.06, 2.47, 3.17])

# Batch solution
H = np.ones((5,2))
H[:, 0] = I

x_ls = LA.pinv(H.T @ H) @H.T @y
print(f'The slope and offset parameters of the best-fit line are [R_1, R_0]: {x_ls}')

I_line = np.arange(0, 0.8, 0.1)
y_line = x_ls[0]*I_line + x_ls[1]

## Recursive solution

#Initialize the 2x2 covaraince matrix (i.e. P_0). Off-diangonal elements should be zero.
P_k = np.array([[9, 0], 
                [0, 0.1]])

# Initialize the 2x1 parameter vector x.
x_k = np.array([4.0, 0.0])

# The voltage measurement variance (denoted by R, not to be confused with resistance).
R_k = 0.0225

# Pre allocate space to save our estimates at every step.
num_meas = y.shape[0]   # Gets the number of rows in y
x_hist = np.zeros((num_meas + 1,2))
P_hist = np.zeros((num_meas + 1,2,2))   # m+1, 2, 2

x_hist[0] = x_k
P_hist[0] = P_k

#Iterate over the measurements
for k in range(num_meas):
  #Construct H_k
  H_k = np.array([[I[k], 1.0]])

  print(H_k @ P_k @ H_k.T + R_k)
  #Construct K_k
  K_k = P_k @ H_k.T @ LA.pinv(H_k @ P_k @ H_k.T + R_k)
                  
  # Estimate update
  residual = y[k]- (H_k @ x_k)
  x_k = x_k + (K_k @ residual)

  #Uncertainty update
  P_k = (np.eye(2,2) - (K_k @ H_k)) @ P_k

  #Keep track of our history
  P_hist[k+1] = P_k
  x_hist[k+1] = x_k
    
print('The parameters of the line fit are ([R, b]):')
print(x_hist)
print(P_hist)

plt.scatter(I, y, label='Data')
plt.plot(I_line, y_line, label='Batch Solution')
plt.xlabel('current (A)')
plt.ylabel('voltage (V)')
plt.grid(True)

for k in range(num_meas):
  y_line = x_hist[k,0]*I_line + x_hist[k,1]
  plt.plot(I_line, y_line, label='Measurement {}'.format(k))

plt.legend()
plt.show()