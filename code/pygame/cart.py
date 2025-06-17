from __future__ import annotations
from math import sin, cos, pow
from dcMotor import DCMotor
from pole import Pole

class InPixels:
  def __init__(self, x, y, maxX, maxY):
    self.x = x
    self.y = y


class Cart:
  def __init__(self, mass: float, cart_friction: float,
                x0: float, min_x: float, max_x: float,
                color: tuple[int, int, int], 
                motor: DCMotor, pole: Pole):
    self.m = mass
    self.u_c = cart_friction
    self.min_x = min_x
    self.max_x = max_x
    self.color = color

    self.motor = motor

    self.state = {"x": [x0], "d_x": [0], "dd_x": [0]}

    self.pole = pole

  def total_mass(self):
    return self.m + self.pole.m

  def x(self, t=None):
    if not t:
      t = len(self.state["x"]) - 1
    return self.state["x"][t]

  def velocity(self, t=None):
    if not t:
      t = len(self.state["d_x"]) - 1
    return self.state["d_x"][t]

  def acceleration(self, t=None):
    if not t:
      t = len(self.state["dd_x"]) - 1
    return self.state["dd_x"][t]

  def getOldDdx(self, pole, d_x, g, f, M):
    sum1 = pole.m * sin(pole.angle()) * cos(pole.angle())
    sum2 = pole.m * pole.lh() * pole.angular_velocity() ** 2 * sin(pole.angle())
    sum3 = pole.u_p * pole.angular_velocity() * cos(pole.angle()) / pole.lh()
    sum4 = pole.m * cos(pole.angle()) ** 2
    dd_x = (g * sum1 - 7 / 3 * (f + sum2 - self.u_c * d_x) - sum3) / (
        sum4 - 7 / 3 * (M + self.motor.Jm / self.motor.r**2)
    )

    return dd_x
  
  def getNewDdx(self, pole, f, d_x, g):
    poleDotTheta = pole.angular_velocity()
    n1 = f
    n2 = -pole.m * pole.lh() * pole.dd_theta * cos(pole.angle())
    n3 = +pole.m * pole.lh() * poleDotTheta * poleDotTheta * sin(pole.angle())
    d = self.m + pole.m
    dd_x = (n1 + n2 + n3)/d

    return dd_x
  
  def update(self, dt: float, Va: float, g: float):
    x = self.x()
    d_x = self.velocity()
    M = self.total_mass()

    f = (1 / self.motor.r**2) * (
        self.motor.K / self.motor.Ra * (Va * self.motor.r - self.motor.K * d_x)
        - self.motor.Bm * d_x
    )
    f=0
    print(f"force: {f}")
    pole = self.pole
    dd_x = self.getNewDdx(pole, f, d_x, g)
    # dd_x = self.getOldDdx(pole, d_x, g, f, M)
    d_x = d_x + dd_x * dt
    x = self.clamp(x + d_x * dt)

    self.state["dd_x"].append(dd_x)
    self.state["d_x"].append(d_x)
    self.state["x"].append(x)

    pole.update(dt, dd_x, g)
    self.motor.update(dt, d_x)

  def clamp(self, x: float):
    if x > self.max_x:
      return self.max_x
    elif x < self.min_x:
      return self.min_x
    return x
