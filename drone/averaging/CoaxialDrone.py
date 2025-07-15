import numpy as np
import math


class CoaxialCopter:
  '''
  k_f - Thrust coefficient
  k_m - Angular torque coefficient
  m - Mass of the vehicle
  i_z - Moment of inertia about the z-axis
  '''
  def __init__(self, k_f=0.1,  k_m=0.1,
                m=0.5, i_z=0.2):
    self.k_f = k_f
    self.k_m = k_m
    self.m = m
    self.i_z = i_z

    self.omega_1 = 0.0
    self.omega_2 = 0.0
    self.g = 9.81

    self.X = np.array([0.0, 0.0, 0.0, 0.0])

  def z_dot_dot(self, m):
    '''
    Drone's mass is not used, so that the caller can provide a mass with a margin of error.
    '''
    f_1 = self.k_f * self.omega_1**2
    f_2 = self.k_f * self.omega_2**2
    acceleration = self.g - (f_1 + f_2) / m
    return acceleration

  def psi_dot_dot(self):
    cw_torque = self.k_m * self.omega_1**2
    ccw_torque = self.k_m * self.omega_2**2

    net_torque = ccw_torque - cw_torque
    angular_acc = net_torque / self.i_z

    return angular_acc

  def set_rotors_angular_velocities(self, linear_acc, angular_acc):
    term_1 = self.m * (-linear_acc + self.g) / (2 * self.k_f)
    term_2 = self.i_z * angular_acc / (2 * self.k_m)

    if (term_1 + term_2) > 0.0:
        omega_1 = math.sqrt(term_1 + term_2)
    else:
        omega_1 = 0.0

    if (term_1 - term_2) > 0.0:
        omega_2 = -math.sqrt(term_1 - term_2)
    else:
        omega_2 = 0.0

    self.omega_1 = omega_1
    self.omega_2 = omega_2

    return self.omega_1, self.omega_2

  def advance_state(self, dt, actual_mass):
    X_dot = np.array(
        [self.X[2], self.X[3], self.z_dot_dot(actual_mass), self.psi_dot_dot()]
    )

    # Change in state will be
    self.X = self.X + X_dot * dt

    return self.X
