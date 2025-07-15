from CoaxialDrone import CoaxialCopter
from . import PIDController
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab


class DronewithPID(CoaxialCopter, PIDController):
  def __init__(self, z_target, z_dot_target, z_ddot_target, 
               t, dt, sensor):
    self.t = t
    self.dt = dt
    self.z_target = z_target
    self.z_dot_target = z_dot_target
    self.z_ddot_target = z_ddot_target
    self.sensor = sensor

  def PID_controller_with_measured_values(self, k_p, k_d, k_i, 
                                          mass_err, sigma, use_measured_height=False):
    drone = CoaxialCopter()

    # array for recording the state history
    drone_state_history = drone.X

    # Introducing a small error of the actual mass, for which the path has been calculated
    actual_mass = drone.m * mass_err

    controller = PIDController(k_p, k_d, k_i)

    # declaring the initial state of the drone with zero hight and zero velocity
    drone.X = np.array([0.0, 0.0, 0.0, 0.0])

    Drone_Sensor = self.sensor(drone.X, 0.95)
    observation_history = drone.X[0]

    # executing the flight
    for i in range(1, self.z_target.shape[0] - 1):
      # condition to use height observation to control the drone or
      # use the magically given true state
      if use_measured_height:
        z_observation = Drone_Sensor.measure(drone.X[0], sigma)

        u_bar = controller.control(
            self.z_target[i],
            z_observation,
            self.z_dot_target[i],
            drone.X[2],
            self.z_ddot_target[i],
            self.dt,
        )

        observation_history = np.vstack((observation_history, z_observation))
      else:
        u_bar = controller.control(
            self.z_target[i],
            drone.X[0],
            self.z_dot_target[i],
            drone.X[2],
            self.z_ddot_target[i],
            self.dt,
        )

        observation_history = np.vstack((observation_history, self.z_target[i]))

      drone.set_rotors_angular_velocities(u_bar, 0.0)

      # calculating the new state vector
      drone_state = drone.advance_state(self.dt, actual_mass)

      # generating a history of vertical positions for the drone
      drone_state_history = np.vstack((drone_state_history, drone_state))

    plt.subplot(211)
    plt.plot(self.t, self.z_target, linestyle="-", marker=".", color="red")
    plt.plot(self.t[1:], drone_state_history[:, 0], linestyle="-", color="blue", linewidth=3)
    if use_measured_height:
        plt.scatter(
            self.t[1:],
            observation_history[:, 0],
            color="black",
            marker=".",
            alpha=0.3,
        )

    plt.grid()
    if use_measured_height:
        plt.title("Change in height (using measured value)").set_fontsize(20)
    else:
        plt.title("Change in height (ideal case)").set_fontsize(20)

    plt.xlabel("$t$ [sec]").set_fontsize(20)
    plt.ylabel("$z-z_0$ [$m$]").set_fontsize(20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    if use_measured_height:
        plt.legend(["Planned path", "Executed path", "Observed value"], fontsize=14)
    else:
        plt.legend(["Planned path", "Executed path"], fontsize=14)
    plt.show()

    plt.subplot(212)
    plt.plot(
        self.t[1:],
        abs(self.z_target[1:] - drone_state_history[:, 0]),
        linestyle="-",
        marker=".",
        color="blue",
    )
    plt.grid()
    plt.title("Error value ").set_fontsize(20)
    plt.xlabel("$t$ [sec]").set_fontsize(20)
    plt.ylabel("||$z_{target} - z_{actual}$|| [$m$]").set_fontsize(20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(["Error"], fontsize=14)
    plt.show()

  def PID_controller_with_estimated_values(
      self, k_p, k_d, k_i, mass_err, sigma, alpha, use_estimated_height=False
  ):

      # creating the co-axial drone object
      drone = CoaxialCopter()

      # array for recording the state history
      drone_state_history = drone.X

      # introducing a small error of the actual mass and the mass for which the path has been calculated
      actual_mass = drone.m * mass_err

      # creating the control system object
      controller = PIDController(k_p, k_d, k_i)

      # declaring the initial state of the drone with zero hight and zero velocity
      drone.X = np.array([0.0, 0.0, 0.0, 0.0])

      Drone_Sensor = self.sensor(drone.X, alpha)

      # recording the estimated height for each step
      estimated_height_history = Drone_Sensor.x_hat

      observation_history = drone.X[0]

      # executing the flight
      for i in range(1, self.z_target.shape[0] - 1):

          # condition to use height observation to control the drone or
          # use the majically given true state
          if use_estimated_height:

              z_observation = Drone_Sensor.measure(drone.X[0], sigma)
              z_estimated = Drone_Sensor.estimate(z_observation)

              u_bar = controller.control(
                  self.z_target[i],
                  z_estimated,
                  self.z_dot_target[i],
                  drone.X[2],
                  self.z_ddot_target[i],
                  self.dt,
              )

          else:

              z_observation = Drone_Sensor.measure(drone.X[0], sigma)

              u_bar = controller.control(
                  self.z_target[i],
                  z_observation,
                  self.z_dot_target[i],
                  drone.X[2],
                  self.z_ddot_target[i],
                  self.dt,
              )

          drone.set_rotors_angular_velocities(u_bar, 0.0)

          # calculating the new state vector
          drone_state = drone.advance_state(self.dt, actual_mass)

          # generating a history of vertical positions for the drone
          drone_state_history = np.vstack((drone_state_history, drone_state))

          # generating the estimated height for each step
          estimated_height_history = np.vstack(
              (estimated_height_history, Drone_Sensor.x_hat)
          )
          observation_history = np.vstack((observation_history, z_observation))

      plt.subplot(211)
      plt.plot(
          self.t,
          self.z_target,
          linestyle="-",
          marker=".",
          color="red",
          label="Planned path",
      )
      if use_estimated_height:
          plt.plot(
              self.t[1:],
              estimated_height_history[:, 0],
              linestyle="-",
              color="green",
              linewidth=3,
              label="Averaged height",
          )

      plt.plot(
          self.t[1:],
          drone_state_history[:, 0],
          linestyle="-",
          color="blue",
          linewidth=3,
          label="Executed path",
      )
      plt.scatter(
          self.t[1:],
          observation_history[:, 0],
          color="black",
          marker=".",
          alpha=0.3,
          label="Observed value",
      )

      plt.grid()
      if use_estimated_height:
          plt.title("Change in height (using averaged value)").set_fontsize(20)
      else:
          plt.title("Change in height (using measured value)").set_fontsize(20)
      plt.xlabel("$t$ [sec]").set_fontsize(20)
      plt.ylabel("$z-z_0$ [$m$]").set_fontsize(20)
      plt.xticks(fontsize=14)
      plt.yticks(fontsize=14)
      plt.legend(fontsize=14)
      plt.show()

      plt.subplot(212)
      plt.plot(
          self.t[1:],
          abs(self.z_target[1:] - drone_state_history[:, 0]),
          linestyle="-",
          marker=".",
          color="blue",
      )
      plt.grid()
      plt.title("Error value ").set_fontsize(20)
      plt.xlabel("$t$ [sec]").set_fontsize(20)
      plt.ylabel("||$z_{target} - z_{actual}$|| [$m$]").set_fontsize(20)
      plt.xticks(fontsize=14)
      plt.yticks(fontsize=14)
      plt.legend(["Error"], fontsize=14)
      plt.show()
