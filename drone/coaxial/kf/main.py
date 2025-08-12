import numpy as np 
#import math
import matplotlib.pylab as pylab
from ipywidgets import interactive
from scipy.stats import multivariate_normal

from .KF import KF
from .StateSpaceDisplay import state_space_display

pylab.rcParams['figure.figsize'] = 10, 10 

dt = 1.0                        # The time difference between measurements

# Initial velocity 1.0 and altitude 0.0
v = 1.0
z = 0.0
mu_0 = np.array([[v], 
                 [z]]) 

velocity_sigma = 0.1            # Initial velocity uncertainty
position_sigma = 0.1            # Initial position uncertainty
sigma_0 = np.array([[velocity_sigma**2, 0.0],
                    [0.0, position_sigma**2]])

u = np.array([0.0])     # no control input is given \ddot{z} = 0 

# Initialize the object
noise = 0.1
kf = KF(noise, noise, noise, dt)
kf.resetState(mu_0, sigma_0)

kf.predict(u)
# print(f"Predicted state estimate\nmu_bar = {kf.mu_bar}, sigma_bar = {kf.sigma_bar}")

# Introduce a single measurement close to the predicted position. Update the drone's estimated position.
measurement = 1.01
kf.update(measurement)
# print(f"State belief after the measurement update:\nMean belief = {kf.mu}, covariance belief = {kf.sigma}")

state_space_display(mu_0, sigma_0, kf.mu_bar, kf.sigma_bar, kf.mu, kf.sigma)

# Please note that if you have peformed all operations correctly the updated state should be better defined than the initial state and the predicted state (the ovals should occupy a smaller area).

# ### KF + PID
# 
# In this section, we will once again ask our drone to hover at a constant height of -1m, but this time we will use a Kalman Filter to estimate the drone's altitude, instead of averaging as we had done previously.

from CoaxialDrone import CoaxialCopter
from PIDcontroller import PIDController_with_ff
from coaxial.kf.pathGenerator import flight_path


# First, we will generate a flight path, which will be a constant height of -1m. 

total_time = 10.0  # Total flight time
dt = 0.01          # Time intervale between measurements 

t, z_path, z_dot_path, z_dot_dot_path =  flight_path(total_time, dt,'constant')


# ###  Sensing
# 
# To generate the measurement data, we will simulate a range-finding sensor by adding noise to the actual altitude measurements.

class Sensor:
    def __init__(self):
        pass
        
    def measure(self, z, sigma=0.001): 
        return z + np.random.normal(0.0, sigma)

from DronewithPIDControllerKF import DronewithPIDKF
sensor_sigma  = 0.1
velocity_sigma = 0.1
position_sigma = 0.1 
kf = KF(sensor_sigma, velocity_sigma, position_sigma, dt)


# Let's compare two estimates of the drone's altitude:
# 
# - the estimate produced by the Kalman Filter,
# - the estimate we obtained earlier, using the measurements directly.
# 
# The graph below will display the estimate obtained by using the measurements directly. By checking the use_kf checkbox, you can see the estimate produced by the Kalman Filter. 

# Initializing the drone with PID controller and providing information of the desired flight path. 
FlyingDrone = DronewithPIDKF(z_path, z_dot_path, z_dot_dot_path, t, dt, Sensor, KF)

interactive_plot = interactive(FlyingDrone.PID_controller_with_KF, 
                               position_sigma = (0.0, 0.1, 0.001),
                               motion_sigma = (0.0, 0.1, 0.001))

# This section will allow you to test the different PID controller parameters and compare flight path when using the direct measurement and the KF estimated value to control the drone. 

from DronewithPIDControllerKF import DronewithPIDKFKnobs

FlyingDroneKnobs = DronewithPIDKFKnobs(z_path, z_dot_path, z_dot_dot_path, t, dt, Sensor, KF)

interactive_plot = interactive(FlyingDroneKnobs.PID_controller_with_KF_knobs,
                               k_p=(5.0, 35.0, 1),
                               k_d=(0.0, 10, 0.5), 
                               k_i=(0.0, 10, 0.5), 
                               mass_err =(0.7, 1.31, 0.01),
                               sigma = (0.0, 0.1, 0.001),
                               position_sigma = (0.0, 0.1, 0.001),
                               motion_sigma = (0.0, 0.1, 0.001))