import numpy as np

class Pendulum():
  def __init__(self, l=1.0):
    self.g = 9.81
    self.l = l

  # Model and simulation 
  def getPos(self, theta):
    return (self.l*np.sin(theta), -self.l*np.cos(theta))
  
  def ode(self, y): 
    '''
    Pendulum's differential equations of motion.
    y[0] is theta, y[1] is theta_dot.
    It returns thetaDot and thetaDotDot.
    '''
    return np.array((y[1], -self.g*np.sin(y[0])/self.l))
