import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt

I = np.array([0.2, 0.3, 0.4, 0.5, 0.6])
V = np.array([1.23, 1.38, 2.06, 2.47, 3.17])

## Batch Solution
H = np.ones((5,2))
H[:, 0] = I

# (2x5)(5x2) (2x5)(5x1) = (2x1)
# Here, it's not a numpy array, so there's just 2 elements.
x_ls = inv(H.T.dot(H)).dot(H.T.dot(V))
print(f'The slope and offset parameters of the best-fit line are [R, b]:\
{x_ls}')

#Plot
I_line = np.arange(0, 0.8, 0.1)
V_line = x_ls[0]*I_line + x_ls[1]

# plt.scatter(I, V)
# plt.plot(I_line, V_line)
# plt.xlabel('current (A)')
# plt.ylabel('voltage (V)')
# plt.grid(True)
# plt.show()

## Recursive solution

#Initialize the 2x2 covaraince matrix (i.e. P_0). Off-diangonal elements should be zero.
# P_k = ...
P_k = np.array([[9, 0], 
                [0, 0.1]])

# Initialize the 2x1 parameter vector x (i.e., x_0).
# x_k = ...
x_k = np.array([4.0, 0.0])

# Our voltage measurement variance (denoted by R, don't confuse with resistance).
R_k = 0.0225

# Pre allocate space to save our estimates at every step.
num_meas = I.shape[0]
x_hist = np.zeros((num_meas + 1,2))
P_hist = np.zeros((num_meas + 1,2,2))
print(P_hist.shape)
x_hist[0] = x_k
P_hist[0] = P_k

#Iterate over the measurements
for k in range(num_meas):
    #Construct H_k
    H_k = np.array([[I[k], 1.0]])
  
    #Construct K_k
    K_k = np.dot(P_k , np.dot(H_k.transpose() , inv(np.dot(H_k,np.dot(P_k,H_k.transpose())) + R_k)))
                    
    #Update our estimate
    x_k = x_k + np.dot(K_k,(V[k]-np.dot(H_k,x_k)))
 
    #Update our uncertainty
    P_k = np.dot((np.eye(2,2)-np.dot(K_k,H_k)),P_k)

    #Keep track of our history
    P_hist[k+1] = P_k
    x_hist[k+1] = x_k
    
print('The parameters of the line fit are ([R, b]):')
print(x_k)
print(P_hist)
#Plot
plt.scatter(I, V, label='Data')
plt.plot(I_line, V_line, label='Batch Solution')
plt.xlabel('current (A)')
plt.ylabel('voltage (V)')
plt.grid(True)

I_line = np.arange(0, 0.8, 0.1)
for k in range(num_meas):
    V_line = x_hist[k,0]*I_line + x_hist[k,1]
    plt.plot(I_line, V_line, label='Measurement {}'.format(k))

plt.legend()
plt.show()