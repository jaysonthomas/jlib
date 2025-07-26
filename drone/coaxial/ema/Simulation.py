from .CoaxialDrone import CoaxialDrone
from .PIDController import PIDController
from .EMAEstimator import EMAEstimator as Estimator
from .Sensor import Sensor

class Simulation():
  def reset(self, kp, kd, ki, massErr):
    self.sensor = Sensor(0.1)
    self.drone = CoaxialDrone(massErr=massErr)
    self.estimator = Estimator(self.drone.X[0], 0.95)
    self.controller = PIDController(kp, kd, ki)
    
  def __init__(self, z_target, z_dot_target, z_ddot_target, 
               t, dt, kp, kd, ki, massErr):
    self.t = t
    self.dt = dt
    self.z_target = z_target
    self.z_dot_target = z_dot_target
    self.z_ddot_target = z_ddot_target

    self.reset(kp, kd, ki, massErr)

  def run(self, controllerInputOption, logger):
    '''
    Options
    0 - use target (ideal) altitude measurements.
    1 - Use measured values (ideal with some gaussian noise).
    2 - Use an estimation of the measured values.
    '''
    y_t = 0.0
    x_hat_t = 0.0
    u = 0.0
    for i in range(1, self.z_target.shape[0] - 1):
      # Advance state
      self.drone.set_rotors_angular_velocities(u, 0.0)
      self.drone.advance_state(self.dt)

      # Measure/Estimate
      y_t = self.drone.X[0]
      if controllerInputOption != 0:
        y_t = self.sensor.measure(self.drone.X[0])

      x_hat_t = y_t
      if controllerInputOption == 2:
        x_hat_t = self.estimator.estimate(y_t)
      
      # Log
      logger.update(y_t, x_hat_t, self.drone.X)

      # Control
      u = self.controller.control(self.z_target[i], x_hat_t, 
                                  self.z_dot_target[i], self.drone.X[2],
                                  self.z_ddot_target[i], self.dt)