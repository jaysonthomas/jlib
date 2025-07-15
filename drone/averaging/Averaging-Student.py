#!/usr/bin/env python
# coding: utf-8

import numpy as np 
import math
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from ipywidgets import interactive
from CoaxialDrone import CoaxialCopter
from PIDcontroller import PIDController_with_ff
from PathGeneration import flight_path
from DronewithPIDControllerParameters import DronewithPID

pylab.rcParams['figure.figsize'] = 10, 10

total_time = 10.0   # Total Flight time 
dt = 0.01           # A time interval between measurements 

t, z_path, z_dot_path, z_dot_dot_path =  flight_path(total_time, dt,'constant' )


# Now let's compare three different estimates: 
# 
# - One that is actually impossible to obtain - that's the drone's true state.
# - One where we use the sensor measurements as our estimated altitude.
# - One where we use the recursive average of the sensor measurements as our estimated altitude.
# 
# We will make the comparison by looking at the path executed by the drone in each case.
# 
# First, let's see what the path looks like for the perfect state estimate, and compare that to an estimate which uses the measured values directly.

# In[ ]:


FlyingDrone = DronewithPID(z_path, z_dot_path, z_dot_dot_path, t, dt, Sensor)


# In[ ]:

plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['axes.titlecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['legend.labelcolor'] = 'white'
plt.rcParams['xtick.labelcolor'] = 'white'
plt.rcParams['ytick.labelcolor'] = 'white'
plt.rcParams['grid.color'] = '#707070'
interactive_plot = interactive(FlyingDrone.PID_controller_with_measured_values, 
                               k_p=(5.0, 35.0, 1),
                               k_d=(0.0, 10, 0.5), 
                               k_i=(0.0, 10, 0.5), 
                               mass_err =(0.7, 1.31, 0.01),
                               sigma=(0.0, 0.1, 0.001))
output = interactive_plot.children[-1]
output.layout.height = '800px'
interactive_plot


# In this section, we will use the estimated value of the altitude based on the averaging to control the drone instead of relying only on the last measurement value.

# In[ ]:


interactive_plot = interactive(FlyingDrone.PID_controller_with_estimated_values, 
                               k_p=(5.0, 35.0, 1),
                               k_d=(0.0, 10, 0.5), 
                               k_i=(0.0, 10, 0.5), 
                               mass_err =(0.7, 1.31, 0.01),
                               sigma = (0.0, 0.1, 0.001),
                               alpha = (0.51, 0.99, 0.01))
output = interactive_plot.children[-1]
output.layout.height = '800px'
interactive_plot


# # Questions:
# ---
# * Is the magnitude of the steady-state error higher or lower when using the weighted average compared to the using the measured values directly?
# * Does the drone converge at the desired altitude quicker or slower when using the weighted averaging for altitude estimation compared to using the direct altitude measurement?
# ---

# In[ ]:




