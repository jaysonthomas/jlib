from __future__ import annotations

class DCMotor:
  def __init__(self, resistance: float, K: float,
               inertia: float, friction: float, radius: float,
               color: tuple[int, int, int]):
    self.Ra = resistance
    self.K = K
    self.Jm = inertia
    self.Bm = friction

    self.color = color
    self.r = radius

    self.state = {"omega": [0], "d_omega": [0]}

  def angle(self, t=None):
    if not t:
      t = len(self.state["omega"]) - 1
    return self.state["omega"][t]

  def angular_velocity(self, t=None):
    if not t:
      t = len(self.state["d_omega"]) - 1
    return self.state["d_omega"][t]

  def update(self, dt, d_x):
    d_omega = d_x / self.r
    omega = self.angle() + d_omega * dt

    self.state["d_omega"].append(d_omega)
    self.state["omega"].append(omega)
