import numpy as np
import math

class CoaxialDrone:
  '''
  k_f - Thrust coefficient
  k_m - Angular torque coefficient
  m - Mass of the vehicle
  i_z - Moment of inertia about the z-axis
  '''
  def __init__(self, k_f=0.1,  k_m=0.1,
                m=0.5, i_z=0.2, massErr=1):
    self.k_f = k_f
    self.k_m = k_m
    self.m = m * massErr
    self.i_z = i_z

    self.omega_1 = 0.0
    self.omega_2 = 0.0
    self.g = 9.81

    self.X = np.array([0.0, 0.0, 0.0, 0.0])

  def z_ddot(self, m):
    '''
    Drone's mass is not used, so that the caller can provide a mass with a margin of error.
    '''
    f_1 = self.k_f * self.omega_1**2
    f_2 = self.k_f * self.omega_2**2
    return self.g - (f_1 + f_2) / m

  def psi_ddot(self):
    cw_torque = self.k_m * self.omega_1**2
    ccw_torque = self.k_m * self.omega_2**2
    net_torque = ccw_torque - cw_torque
    return net_torque / self.i_z

  def set_rotors_angular_velocities(self, z_ddot, psi_ddot):
    term_1 = self.m * (self.g - z_ddot) / (2 * self.k_f)
    term_2 = self.i_z * psi_ddot / (2 * self.k_m)

    self.omega_1 = 0.0
    self.omega_2 = 0.0

    if (term_1 + term_2) > 0.0:
      self.omega_1 = math.sqrt(term_1 + term_2)

    if (term_1 - term_2) > 0.0:
      self.omega_2 = -math.sqrt(term_1 - term_2)

    return self.omega_1, self.omega_2

  def advance_state(self, dt, actual_mass):
    X_dot = np.array(
        [self.X[2], self.X[3], self.z_ddot(actual_mass), self.psi_ddot()]
    )
    self.X = self.X + X_dot * dt
