
import numpy as np

class KF:
  def __init__(self, measurement_noise, process_noise_v, process_noise_p, dt):
    '''
    Measurement noise: Uncertainty that is present in every measurement.
    Process noise v and p: Uncertainty in the velocity and position respectively.
    dt: Time between samples
    '''
    # Process noise
    # This is determined experimentally based on the vehicle model; usually remains constant. 
    self.q_t = np.array([[process_noise_v**2, 0.0],
                         [0.0, process_noise_p**2]])
    
    # Measurement noise
    # This is read off a datasheet or determined experimentally; usually remains constant.
    self.r_t =  np.array([measurement_noise**2])
    
    self.dt = dt
    
    # Default velocity, position
    self.mu = np.array([[0.0],
                        [0.0]])
    
    # Default covariance - complete certainty
    self.sigma = np.array([[0.0, 0.0],
                           [0.0, 0.0]])
    
    # Estimates
    self.mu_bar = self.mu
    self.sigma_bar = self.sigma

  @property
  def a(self):
    return np.array([[1.0, 0.0],
                     [self.dt, 1.0]])

  @property
  def b(self):
    return np.array([[self.dt],
                     [0.0]])

  @property
  def c(self):
    return np.array([[0.0, 1.0]])
  
  def g(self, mu, u):
    '''
    State transition function.
    Control input u = [\ddot{z}]
    '''
    return np.matmul(self.a, mu) + (self.b * u)

  def g_prime(self):
    '''
    Jacobian of the state transition function.
    '''
    return self.a

  def resetState(self, mu_0, sigma_0):
    '''
    Set initial state of the drone.
    '''
    self.mu = mu_0
    self.sigma = sigma_0

  def predict(self, u):
    g_prime = self.g_prime()
    self.mu_bar = self.g(self.mu, u)
    self.sigma_bar = np.matmul(g_prime, np.matmul(self.sigma, np.transpose(g_prime))) + self.q_t

  def h(self,mu):
    return np.matmul(self.c, mu) 

  def h_prime(self):
    return self.c

  def K(self, H):
    '''
    Compute Kalman gain
    '''
    S = np.matmul(np.matmul(H, self.sigma_bar), np.transpose(H)) + self.r_t     
    K = np.matmul(np.matmul(self.sigma_bar, np.transpose(H)), np.linalg.inv(S))
    return K

  def update(self, z):
    '''
    Measurement Update step.
    z is the new measurement
    '''
    H = self.h_prime()
    K = self.K(H)
    self.mu = self.mu_bar + np.matmul(K, (z - self.h(self.mu_bar)))
    self.sigma = np.matmul((np.identity(2) - np.matmul(K, H)), self.sigma_bar)