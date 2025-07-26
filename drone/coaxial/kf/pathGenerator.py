import numpy as np

def getDesiredTraj(total_time, dt, type="constant"):
  '''
  This produces the flight path.
  z_ddot - Desired acceleration over time in order to execute the given flight path
  '''
  t = np.linspace(0.0, total_time, int(total_time / dt) + 1)

  if type == "constant":
    z = -np.ones(t.shape[0])
    z_dot = np.zeros(t.shape[0])    
    z_ddot = np.zeros(t.shape[0])
  elif type == "periodic":
    z = 0.5 * np.cos(2 * t) - 0.5
    z_dot = -1 * np.sin(2 * t)
    z_ddot = -2 * np.cos(2 * t)

  return t, z, z_dot, z_ddot
