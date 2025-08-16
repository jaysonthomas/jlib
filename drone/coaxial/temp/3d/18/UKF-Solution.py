#!/usr/bin/env python
# coding: utf-8

# # UKF
# 
# In this exercise, you will become familiar with the UKF method which is a robust tool for estimating the value of the measured quantity. Later in the exercise, you will apply it to estimate the position of the one-dimensional quadcopter with can move only in the vertical axis. 
# 
# Next, you will create the class that will have all the functions needed to perform the localization of the object in the one-dimensional environment. 
# 
# As mentioned For simplicity, will use a drone that can only move in the vertical direction for the given drone the state function is simply vertical position and velocity $X=(\dot{z},z)$. The control input for the drone is the vertical acceleration $u = \ddot{z}$. For KF we have to define the measurement error associated with the measuring the hight variable. 

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")

import numpy as np 
import math
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import jdc
from ipywidgets import interactive
from scipy.stats import multivariate_normal
from scipy.linalg import sqrtm

pylab.rcParams['figure.figsize'] = 10, 10


# In[2]:


pylab.rcParams['figure.figsize'] = 10, 10


# # UKF 

# As a reminder from the theory let us list the constants used in UKF method.
# 
# * $N$ represents the configuration space dimension and in this case, it is equal to 2. 
# 
# * $\lambda$ is a scaling parameter. $\lambda = \alpha^2 (N+k)-N$
# 
# * $\gamma$ describes how far from the mean we would like to select the sigma points along the eigenvectors. $\gamma =\sqrt{N+\lambda}$
# 
# * $\alpha$ determins the spread of the sigma points and it set as $1$.
# 
# * $k$ is the secondary scaling parameter which is set to $3-N$.
# 
# * Finally $\beta$ is set 2 as we assume that the distribution is Gaussian in nature. 

# In[3]:


class UKF:
    
    def __init__(self,
                 sensor_sigma,             # Motion noise
                 velocity_sigma,           # Velocity uncertainty
                 position_sigma,           # Velocity uncertainty
                 dt                        # dt time between samples 
                ):
        
        # Sensor measurement covariance
        self.r_t = np.array([[sensor_sigma**2]])
        
        # Motion model noise for velocity and position
        self.q_t = np.array([[velocity_sigma**2,0.0],
                             [0.0,position_sigma**2]]) 
        
        self.dt = dt
        
        self.mu = np.array([[0.0],
                            [0.0]])
        
        self.sigma = np.array([[0.0, 0.0],
                               [0.0, 0.0]])
        
        self.mu_bar = self.mu
        self.sigma_bar = self.sigma
        
        self.n = self.q_t.shape[0] 
        self.sigma_points = np.zeros((self.n, 2*self.n+1)) 
        
        # Creating the contestants 
        self.alpha = 1.0
        self.betta = 2.0
        self.k = 3.0 - self.n
        
        self.lam = self.alpha**2 * (self.n + self.k) - self.n
        self.gamma = np.sqrt(self.n + self.lam)
        
        self.x_bar = self.sigma_points


    def initial_values(self,mu_0, sigma_0):
        self.mu = mu_0
        self.sigma = sigma_0
    


# Declaring the initial values and initializing the object. 

# In[4]:


z = 2.0                         # Initial position
v = 1.0                         # Initial velocity
dt = 1.0                        # The time difference between measures
motion_error = 0.01             # Sensor sigma
velocity_sigma = 0.01           # Velocity uncertainty
position_sigma = 0.01           # Position uncertainty


mu_0 = np.array([[v],
                 [z]]) 

cov_0 = np.array([[velocity_sigma**2, 0.0],
                    [0.0, position_sigma**2]])

u = np.array([0.0])     # no commant is given \ddot{z} = 0 

MYUKF=UKF(motion_error, velocity_sigma, position_sigma, dt)

MYUKF.initial_values(mu_0, cov_0)


# ### Compute Sigma points 
# 
# In this step, we will implement the compute sigma step that takes the mean and covariance matrix and returns the points selected around the mean point. 
# $$
# X_{i,t} = \Bigg \{ \begin{array}{l l} =x_t & i=0 \\=x_t+\gamma S_i & i=1,...,N \\=x_t-\gamma S_{i-N} & i=N+1,...,2N \end{array}
# $$
# $S_i$ is the $i^{th}$ column of $S=\sqrt{\Sigma}$
# 
# 
# 
# ### Predict
# As a reminder from the previous 1D case we know that the transition function has the next form:
# $$
# g(x_t,u_t,\Delta t) = \begin{bmatrix} 1 & 0 \\ \Delta t & 1 \end{bmatrix} \begin{bmatrix} \dot{z}\\z \end{bmatrix} + \begin{bmatrix} \Delta t \\ 0 \end{bmatrix} \begin{bmatrix} \ddot{z} \end{bmatrix}  = A_t \mu_{t-1}+B_tu_t
# $$
# 
# The partial derivative of the $g$ relative to each component:
# $$
# g'(x_t,u_t,\Delta t) = \begin{bmatrix} 1 & 0 \\ \Delta t & 1   \end{bmatrix}
# $$
# 
# As $A$ and $B$ matrixes, in general, depend on the external parameters we declare them as the separate functions.

# In[5]:


get_ipython().run_cell_magic('add_to', 'UKF', '\ndef compute_sigmas(self):\n    S = sqrtm(self.sigma)\n    # TODO: Implement the sigma points \n    self.sigma_points[:, 0] = self.mu[:, 0]\n    \n    self.sigma_points[:, 1] = self.mu[:, 0]\n    self.sigma_points[:, 2] = self.mu[:, 0]\n    self.sigma_points[:, 1:3] += self.gamma * S\n    \n    self.sigma_points[:, 3] = self.mu[:, 0]\n    self.sigma_points[:, 4] = self.mu[:, 0]\n    self.sigma_points[:, 3:5] -= self.gamma * S\n    \n    return self.sigma_points\n\n@property\ndef a(self):\n    return np.array([[1.0, 0.0],\n                     [self.dt, 1.0]])\n\n@property\ndef b(self):\n    return np.array([[self.dt],\n                     [0.0]])\n\ndef g(self,u):\n    g = np.zeros((self.n, self.n+1))\n    g = np.matmul(self.a, self.sigma_points) + self.b * u\n    \n    return g\n\ndef predict(self, u):\n    # TODO: Implement the predicting step\n    self.compute_sigmas()\n    x_bar = self.g(u)\n    \n    self.x_bar = x_bar\n    return x_bar')


# Predicting the next position based on the initial data

# In[6]:


u = 0 # no control input is given
print(MYUKF.predict(0))


# ### Update
# Ones we selected sigma points and predicted the new state of the sigma points now it is time to estimate the value based on the predicted sigma points and the measured value. 
# 
# As a reminder, the weights for the mean and covariance are given below.
# 
# weights for the mean:
# $$
# w_i^m = \Bigg \{ \begin{array}{l l} =\frac{\lambda}{N+\lambda} & i=0 \\=\frac{1}{2(N+\lambda)} & i>0\end{array}
# $$
# 
# Weights for computing the covariance:
# $$
# w_i^c=\Bigg \{\begin{array}{l l} =\frac{\lambda}{N+\lambda} +(1-\alpha^2+\beta^2) & i=0 \\=\frac{1}{2(N+\lambda)} & i>0 \end{array}
# $$

# In[7]:


get_ipython().run_cell_magic('add_to', 'UKF', '\n@property\ndef weights_mean(self):\n    \n    w_m = np.zeros((2*self.n+1, 1))\n    # TODO: Calculate the weight to calculate the mean based on the predicted sigma points\n    \n    w_m[0] = self.lam/(self.n + self.lam) \n    w_m[1] = 1.0/(self.n + self.lam)/2\n    w_m[2] = 1.0/(self.n + self.lam)/2\n    w_m[3] = 1.0/(self.n + self.lam)/2\n    w_m[4] = 1.0/(self.n + self.lam)/2\n    \n    self.w_m = w_m\n    return w_m\n\n@property\ndef weights_cov(self):\n    \n    w_cov = np.zeros((2*self.n+1, 1))\n    # TODO: Calculate the weight to calculate the covariance based on the predicted sigma points\n    \n    w_cov[0] = self.lam/(self.n + self.lam) + 1.0 - self.alpha**2 + self.betta\n    w_cov[1] = 1.0/(self.n + self.lam)/2\n    w_cov[2] = 1.0/(self.n + self.lam)/2\n    w_cov[3] = 1.0/(self.n + self.lam)/2\n    w_cov[4] = 1.0/(self.n + self.lam)/2\n    \n    self.w_cov = w_cov\n    return w_cov\n\n\ndef h(self,Z):\n    return np.matmul(np.array([[0.0, 1.0]]), Z) \n    \n\ndef update(self,z_in):\n    \n    # TODO: Implement the update step \n    mu_bar = np.matmul(self.x_bar, self.weights_mean)             # Line 8\n    cov_bar=np.matmul(self.x_bar-mu_bar,np.transpose(self.x_bar-mu_bar) * self.weights_cov) + self.q_t # Line 9\n    z = self.h(self.x_bar)                                        # Line 10\n    mu_z = np.matmul(z, self.weights_mean)                        # Line 11 \n    cov_z = np.matmul(z - mu_z, np.transpose(z - mu_z) * self.weights_cov) + self.r_t # Line 12 \n    cov_xz = np.matmul(self.x_bar - mu_bar, np.transpose(z - mu_z) * self.weights_cov)  # Line 13\n    k = np.matmul(cov_xz, np.linalg.inv(cov_z))                   # Line 14\n    \n    mu_t =  mu_bar  + k * (z_in - mu_z)                           # Line 15\n    cov_t = cov_bar - np.matmul(k, cov_z*np.transpose(k))         # Line 16\n    \n    self.mu = mu_t\n    self.sigma = cov_t\n    \n    return mu_t, cov_t')


# Updating the estimated value based on the measurement. 

# In[8]:


z_measured = 3.11
print(MYUKF.update(z_measured))


# ### UKF + PID
# 
# In this section, the drone is controlled using the altitude estimated by UKF filter.

# In[9]:


from CoaxialDrone import CoaxialCopter
from PIDcontroller import PIDController_with_ff
from PathGeneration import flight_path


# First, we will generate the flight path which is constant height of 1m. 

# In[10]:


total_time = 10.0  # Total flight time
dt = 0.01          # Time intervale between measurements 

t, z_path, z_dot_path, z_dot_dot_path =  flight_path(total_time, dt,'constant' )


# ###  IMU
# 
# For this section, we will use a simple IMU which only adds noise to the actual altitude measurements.

# In[11]:


class IMU:
    def __init__(self):
        pass
        
    def measure(self, z, sigma=0.001): 
        return z + np.random.normal(0.0, sigma)


# In[12]:


from DronewithPIDControllerUKF import DronewithPIDUKF


# In[13]:


sensor_error  = 0.1
velocity_sigma = 0.1
position_sigma = 0.1 
MYUKF = UKF(sensor_error, velocity_sigma, position_sigma, dt)


# In[14]:


#Initializing the drone with PID controller and providing information of the desired flight path. 
FlyingDrone = DronewithPIDUKF(z_path, z_dot_path, z_dot_dot_path, t, dt, IMU, UKF)


# In[15]:


interactive_plot = interactive(FlyingDrone.PID_controler_with_KF, 
                               position_sigma = (0.0, 0.1, 0.001),
                               motion_sigma = (0.0, 0.1, 0.001))
output = interactive_plot.children[-1]
output.layout.height = '800px'
interactive_plot


# In[ ]:




