import numpy as np 
from . import pathGenerator
from .Simulation import Simulation
from .Logger import Logger
from .Plotter import Plotter

total_time = 10.0   # Total Flight time 
dt = 0.01           # A time interval between measurements 

t, z_path, z_dot_path, z_ddot_path =  pathGenerator.getDesiredTraj(total_time, dt,'constant' )


# Now let's compare three different estimates: 
# 
# - One that is actually impossible to obtain - that's the drone's true state.
# - One where we use the sensor measurements as our estimated altitude.
# - One where we use the recursive average of the sensor measurements as our estimated altitude.
# 
# We will make the comparison by looking at the path executed by the drone in each case.
# 
# First, let's see what the path looks like for the perfect state estimate, and compare that to an estimate which uses the measured values directly.

logger = Logger()
sim = Simulation(z_path, z_dot_path, z_ddot_path, t, dt, 35, 10, 10, 0.7)

                              #  k_p=(5.0, 35.0, 1),
                              #  k_d=(0.0, 10, 0.5), 
                              #  k_i=(0.0, 10, 0.5), 
                              #  mass_err =(0.7, 1.31, 0.01),
                              #  sigma=(0.0, 0.1, 0.001))

# In this section, we will use the estimated value of the altitude based on the averaging to control the drone instead of relying only on the last measurement value.

z = [None] * 3
zEstimate = [None] * 3
x = [None] * 3

for i in range(0, len(z)):
  sim.reset(35, 10, 10, 0.7)
  sim.run(i, logger)
  z[i], zEstimate[i], x[i] = logger.get()
  logger.reset()

plotter = Plotter()
plotter.plot(t, z, zEstimate, x)

# # Questions:
# ---
# * Is the magnitude of the steady-state error higher or lower when using the weighted average compared to the using the measured values directly?
# * Does the drone converge at the desired altitude quicker or slower when using the weighted averaging for altitude estimation compared to using the direct altitude measurement?