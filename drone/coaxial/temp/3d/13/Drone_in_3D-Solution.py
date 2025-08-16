#!/usr/bin/env python
# coding: utf-8

# # 3D EKF
# 
# In this exercise, you will learn that you can continue using the same code that you created earlier for three-dimensional flight. You have already went through a similar exercise when you transitioned from a one-dimensional to a two-dimensional example. In that case you had to change the values in several matrices, but rest of the estimation code remained the same. You will see that the same is true moving from 2D to 3D. 
# 
# In this exercise, you simply test the correctness of your implementation. In the final project at the end of the lesson, you will be asked to estimate the drone's position and attitude using these same EKF equations.
# 
# <img src="Dronein3D.png" width="500" height="500">
# 
# 
# For this exercise, we will use the following setup: the state will be obtained using GPS measurements and the yaw will be obtained from the magnetometer. Thus, the state vector has the next form $X=[x,y,z,\dot{x},\dot{y},\dot{z},\psi]^T$. The complementary filter will be used to determine the roll and pitch of the drone. 
# 
# We will use the accelerometer and gyro measurements to determine the $\ddot{x},\ddot{y},\ddot{z}$ and $p,q,r$. These mesurements will be used as a control inputs for the filter. 
# 
# We are using NED system where $z$ is directed down. The yaw will be tracked relative to the magnetic north. 
# 
# Thus, $u=[\ddot{x},\ddot{y},\ddot{z},\dot{\psi}]^T$

# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")

import numpy as np 
from math import sin, cos
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import jdc
from ipywidgets import interactive
from scipy.stats import multivariate_normal
np.set_printoptions(precision=2)
import time 

pylab.rcParams['figure.figsize'] = 10, 10


# # EKF 
# In order to perform the predict and update steps for the 3D EKF, we need to know the mean and the standard deviation for measurement and motion. The measurement error is related to how good our measuring tool is, and the motion error is associated with how well the drone executes a given command. 

# In[3]:


class EKF:
    def __init__(self,
                 motion_error,             # Motion noise
                 angle_sigma_yaw,          # Angle sigma
                 velocity_sigma,           # Velocity uncertainty
                 position_sigma,           # Position uncertainty
                 dt                        # dt time between samples 
                ):
        
        # Sensor measurement sigma 
        self.r_t = np.array([[motion_error**2]]) # THIS WILL CHANGE
        
        # Motion model noise 
        self.q_t = np.array([[position_sigma**2,0.0,0.0,0.0,0.0,0.0,0.0],         
                             [0.0,position_sigma**2,0.0,0.0,0.0,0.0,0.0],
                             [0.0,0.0,position_sigma**2,0.0,0.0,0.0,0.0],
                             [0.0,0.0,0.0,velocity_sigma**2,0.0,0.0,0.0],
                             [0.0,0.0,0.0,0.0,velocity_sigma**2,0.0,0.0],
                             [0.0,0.0,0.0,0.0,0.0,velocity_sigma**2,0.0],
                             [0.0,0.0,0.0,0.0,0.0,0.0,angle_sigma_yaw**2]]) 
        
        self.dt = dt
        self.mu = np.array([0])
        self.sigma = np.array([0])
        
        self.mu_bar = self.mu
        self.sigma_bar = self.sigma
        
        self.X=np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0])
        self.gravity=9.81
        self.phi=0.0
        self.psi=0.0
        self.theta=0.0
        
    def initial_values(self,mu_0, sigma_0):
        self.mu= mu_0
        self.sigma = sigma_0
        


# ### Transition model and predict step
# We will use the rotation matrix to define the transition model from body frame to global frame $R_{bg}$. The transition function for the 3D case using the state vector that we defined will be:
# 
# $$
# \begin{align}
#   g(x_t, u_t, \Delta t) &=
#   \left[  \begin{array}{c}
#       x_{t,x} +  x_{t,\dot{x}} \Delta t \\
#       x_{t,y} +  x_{t,\dot{y}} \Delta t \\
#       x_{t,z} + x_{t,\dot{z}} \Delta t\\
#       x_{t,\dot{x}} \\
#       x_{t,\dot{y}} \\
#       x_{t,\dot{z}} - g \Delta t \\
#       x_{t, \psi}\\
#     \end{array}\right] + 
#   \left[ \begin{array}{cccc}
#       0&0&0&0\\
#       0&0&0&0\\
#       0&0&0&0\\
#       R_{bg}[0:]&&&0\\
#       R_{bg}[1:]&&&0\\
#       R_{bg}[2:]&&&0\\
#       0&0&0&1
#       \end{array}
#     \right]   u_t \Delta t
# \end{align}
# $$
# 
# And the Jacobian: 
# 
# $$
# g'(x_t, u_t, \Delta t) = \left [ \begin{array}{ccccccc}
#       1 & 0 & 0 & \Delta t & 0 & 0 & 0\\
#       0 & 1 & 0 & 0 & \Delta t & 0 & 0\\
#       0 & 0 & 1 & 0 & 0 & \Delta t & 0\\
#       0 & 0 & 0 & 1 & 0 & 0 & R'_{bg}[0:]u_t[0:3] \Delta t\\
#       0 & 0 & 0 & 0 & 1  & 0 & R'_{bg}[1:]u_t[0:3] \Delta t\\
#       0 & 0 & 0 & 0 & 0 & 1 &  R'_{bg}[2:]u_t[0:3] \Delta t\\
#       0 & 0 & 0 & 0 & 0 & 0 & 1
#     \end{array}
#     \right] 
# $$
# 
# Where $R'_{bg}$ is $\frac{\partial}{\partial \psi}$ of the rotation matrix. 
# 
# ### New transition functions 
# 
# In this section we will also implement the matrixes for $g(x_y,u_t,\Delta t) = a + b u_t \Delta t$ and $g'(x_y,u_t,\Delta t)$ also note that $u_t = [\ddot{x},\ddot{y},\ddot{z},\dot{\psi}]$ and $\Delta t= dt$.

# In[4]:


get_ipython().run_cell_magic('add_to', 'EKF', '\n@property\ndef R_bg(self):\n    \n    R_bg=np.array([[cos(self.phi)*cos(self.psi)-sin(self.phi)*cos(self.theta)*sin(self.psi), \n                    cos(self.phi)*sin(self.psi)+sin(self.phi)*cos(self.theta)*cos(self.psi),\n                    sin(self.phi)*sin(self.theta)],\n                   [-sin(self.phi)*cos(self.psi)-cos(self.phi)*cos(self.theta)*sin(self.psi),\n                    -sin(self.phi)*sin(self.psi)+cos(self.phi)*cos(self.theta)*cos(self.psi),\n                    cos(self.phi)*sin(self.theta)],\n                   [sin(self.theta)*sin(self.psi),-sin(self.theta)*cos(self.psi),cos(self.theta)]])\n    \n    return R_bg\n\n@property\ndef R_bg_prime(self):\n\n    R = np.array([[-cos(self.phi)*sin(self.psi)-sin(self.phi)*cos(self.theta)*cos(self.psi),\n                   cos(self.phi)*cos(self.psi)-sin(self.phi)*cos(self.theta)*sin(self.psi), 0.0],\n                  [sin(self.phi)*sin(self.psi)-cos(self.phi)*cos(self.theta)*cos(self.psi),\n                  -sin(self.phi)*cos(self.psi),0.0],\n                  [sin(self.theta)*cos(self.psi),sin(self.theta)*sin(self.psi),0.0]])\n    \n    \n    \n    return np.transpose(R)\n\n\n@property\ndef a(self):\n    a= np.zeros((self.X.shape[0],1))\n    \n    a = np.array([[self.mu[0] + self.mu[3] * self.dt],\n                  [self.mu[1] + self.mu[4] * self.dt],\n                  [self.mu[2] + self.mu[5] * self.dt],\n                  [self.mu[3]],\n                  [self.mu[4]],\n                  [self.mu[5] + self.gravity * self.dt],\n                  [self.mu[6]]])\n    \n    \n    return a \n\n@property\ndef b(self):\n    \n    b= np.zeros((self.X.shape[0],4))\n    b[3:6,:3] = self.R_bg\n    b[-1,-1] = 1\n    \n    return b \n\n\ndef g(self,u):\n    \n    g_3d = np.add(self.a[:,:,0], np.matmul(self.b, (u* self.dt)))\n    \n    return g_3d\n\n\ndef g_prime(self,u):\n    \n    g_prime=np.identity(self.mu.shape[0])\n    g_prime[0,3] = self.dt\n    g_prime[1,4] = self.dt\n    g_prime[2,5] = self.dt\n    g_prime[3:6,5:6] =np.matmul(self.R_bg_prime, (u[:3]*self.dt) )\n    \n    return g_prime\n    ')


# ### Predict 
# Now that we have implemented the proper expressions for $g$ and $g'$ we can perform the prediction step. Please note that the given step is exactly like the one that you already implemented for one-dimensional case.

# In[5]:


get_ipython().run_cell_magic('add_to', 'EKF', '\ndef predict(self, u):\n    previous_covariance = self.sigma\n    mu_bar = self.g(u)\n    G_now  = self.g_prime(u)\n    sigma_bar = np.matmul(G_now,np.matmul(previous_covariance,np.transpose(G_now))) + self.q_t\n    \n    self.mu_bar  = mu_bar \n    self.sigma_bar = sigma_bar\n    \n    return mu_bar, sigma_bar')


# # Testing the Predict function
# 
# In this section, you will be given simple initial statements and asked to run the predict function and compare to the intuitive answer.  
# 
# First, we will declare the initial condition and then execute the prediction, and you will be able to see that the prediction for 3D is no different from the 2D that you already have seen. 

# In[6]:


x = 0.0                         # Initial position
y = 0.0                         # Initial position
z = -1.0                        # Initial position

x_dot = 2.0                     # Initial velocity
y_dot = 3.0                     # Initial velocity
z_dot = 0.0                     # Initial velocity

phi = 0.0                       # Initial roll angle
theta = 0.0                     # Initial pitch angle
psi = 0.0                       # Initial yaw angle


dt = 1.0                        # The time difference between measurements

motion_error = 0.01             # Motion error 
angle_error_yaw = 0.001         # Angle uncertainty 
velocity_sigma = 0.01           # Velocity uncertainty
position_sigma = 0.02           # Position uncertainty

mu_0 = np.array([[x],[y],[z],[x_dot],[y_dot],[z_dot],[psi]]) 
cov_0 = np.array([[position_sigma**2,0.0,0.0,0.0,0.0,0.0,0.0],        
                  [0.0,position_sigma**2,0.0,0.0,0.0,0.0,0.0],
                  [0.0,0.0,position_sigma**2,0.0,0.0,0.0,0.0],
                  [0.0,0.0,0.0,velocity_sigma**2,0.0,0.0,0.0],
                  [0.0,0.0,0.0,0.0,velocity_sigma**2,0.0,0.0],
                  [0.0,0.0,0.0,0.0,0.0,velocity_sigma**2,0.0],
                  [0.0,0.0,0.0,0.0,0.0,0.0,angle_error_yaw**2]]) 

u = np.array([[0.0],
              [0.0],
              [-9.81],
              [0.0]])           # no command is given 


# The prediction step consists of declaring the object, and then initializing and calling the prediction function.

# In[7]:


# initilize the object
myEKF=EKF(motion_error,angle_error_yaw,velocity_sigma,position_sigma,dt)

myEKF.psi=psi
myEKF.phi=phi
myEKF.theta=theta
# input the initial values 
myEKF.initial_values(mu_0, cov_0)

# call the predict function

mu_bar, sigma_bar = myEKF.predict(u)

print('mu_bar = \n',mu_bar)
print('\nsigma_bar = \n', sigma_bar)


# # Measurement Update
# 
# We assume that our observation function is, 
# 
# $$
# z_t = \begin{bmatrix}x\\y\\z \\ \dot{x}\\ \dot{y} \\ \dot{z}\end{bmatrix}
# $$
# 
# Thus, $h'$ will be,
# 
# $$
# h'=\begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0  \\ 0 & 1 & 0 & 0 & 0 & 0 & 0  \\ 0 & 0 & 1 & 0 & 0 & 0 & 0  \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0  \end{bmatrix}
# $$

# In[8]:


get_ipython().run_cell_magic('add_to', 'EKF', '\ndef h(self,x):\n    \n    h=x\n    \n    return h\n\ndef h_prime(self):\n    \n    h_prime = np.array([[1,0,0,0,0,0,0],\n                        [0,1,0,0,0,0,0],\n                        [0,0,1,0,0,0,0],\n                        [0,0,0,1,0,0,0],\n                        [0,0,0,0,1,0,0],\n                        [0,0,0,0,0,1,0]])\n    \n    return h_prime ')


# Please note that the update step is identical to the one you implemented for the one-dimensional case.

# In[9]:


get_ipython().run_cell_magic('add_to', 'EKF', '\ndef update(self, z):\n    \n    H = self.h_prime()\n    \n    S = np.matmul(np.matmul(H,self.sigma_bar),np.transpose(H)) + self.r_t     \n    \n    K = np.matmul(np.matmul(self.sigma_bar,np.transpose(H)),np.linalg.inv(S))\n    \n    mu = self.mu_bar + np.matmul(K,(z-self.h(self.mu_bar[:-1])))\n    \n    sigma = np.matmul((np.identity(7) - np.matmul(K,H)),self.sigma_bar)\n    \n    self.mu=mu\n    self.sigma=sigma\n    \n    return mu, sigma\n    ')


# # Results 

# In[10]:


measure =np.array([[ 2.05],
 [ 3.1],
 [-1.0],
 [ 2.1],
 [ 3.05],
 [ 0.]]) 

mu_updated, sigma_updated = myEKF.update(measure)
print('updated mean = \n',mu_updated)
print('\nupdated sigma = \n', sigma_updated)


# In[ ]:




