from __future__ import annotations
from math import sin, cos, pow

class Pole:
  def __init__(self, mass: float, angle0: float,
                length: float, pole_friction: float,
                color: tuple[int, int, int],
                child: Pole | None):
    self.m = mass
    self.l = length
    self.u_p = pole_friction
    self.color = color

    self.state = {
        "theta": [angle0],
        "d_theta": [0],
    }

    self.child = child

  def update(self, dt: float, dd_x: float, g: float):
    theta = self.angle()
    d_theta = self.angular_velocity()

    # n1 = self.lh() * pow(d_theta, 2)
    # n2 = -dd_x * cos(theta)
    # n3 = g * sin(theta)
    # d = (self.m * pow(self.lh(), 2))/3

    # dd_theta = (self.m * self.lh() * (n1 + n2 + n3))/d

    dd_theta = (3 / (7 * self.lh())) * (
        (g * sin(theta))
        - (dd_x * cos(theta))
        - ((self.u_p * d_theta) / (self.m * self.lh()))
    )

    d_theta = d_theta + dd_theta * dt
    theta = theta + d_theta * dt

    self.state["d_theta"].append(d_theta)
    self.state["theta"].append(theta)

  def lh(self):
    return self.l / 2

  def __iter__(self):
    poles = [self]
    pole = self.child
    while pole:
      poles.append(pole)
      pole = pole.child
    return iter(poles)

  def angle(self, t=None):
    if not t:
      t = len(self.state["theta"]) - 1
    return self.state["theta"][t]

  def angular_velocity(self, t=None):
    if not t:
      t = len(self.state["d_theta"]) - 1
    return self.state["d_theta"][t]

  def __str__(self):
    return f"Pole:\n  Mass: {self.m}\n  Length: {self.l}\n  Friction: {self.u_p}\n  Child: {self.child is not None}"
