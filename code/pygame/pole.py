from __future__ import annotations
from math import sin, cos, pow
import numpy as np

class Pole:
  def __init__(self, mass: float, angle0: float,
                length: float, pole_friction: float,
                color: tuple[int, int, int]):
    self.m = mass
    self.l = length
    self.u_p = pole_friction
    self.color = color

    self.state = {
        "theta": [angle0],
        "d_theta": [0],
    }
    self.dd_theta = 0

  def getOldDTheta(self, theta, d_theta, g, dd_x):
    dd_theta = (3 / (7 * self.lh())) * (
    (g * sin(theta))
    - (dd_x * cos(theta))
    - ((self.u_p * d_theta) / (self.m * self.lh()))
    )

    return dd_theta
  
  def getNewDTheta(self, theta, dd_x, g):
    J = (self.m * pow(self.lh(), 2))/3
    n1 = -self.m * self.lh() * dd_x * cos(theta)
    n2 = -self.m * g * self.lh() * sin(theta)
    d1 = J
    d2 = self.m * pow(self.lh(), 2)

    dd_theta = (n1 + n2)/(d1 + d2)
    return dd_theta
  
  def update(self, dt: float, dd_x: float, g: float):
    theta = self.angle()
    d_theta = self.angular_velocity()
    dd_theta = self.getNewDTheta(theta, dd_x, g)
    # dd_theta = self.getOldDTheta(theta, d_theta, g, dd_x)
    self.dd_theta = dd_theta
    d_theta = d_theta + dd_theta * dt
    theta = theta + d_theta * dt

    self.state["d_theta"].append(d_theta)
    self.state["theta"].append(theta)

  def lh(self):
    return self.l

  def angle(self, t=None):
    if not t:
      t = len(self.state["theta"]) - 1
    return self.state["theta"][t]

  def angular_velocity(self, t=None):
    if not t:
      t = len(self.state["d_theta"]) - 1
    return self.state["d_theta"][t]

  def __str__(self):
    return f"Pole:\n  Mass: {self.m}\n  Length: {self.l}\n  Friction: {self.u_p}\n"
