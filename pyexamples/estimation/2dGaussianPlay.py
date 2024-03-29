# # 2D Gaussian
# 
# We recover mean and covariance matrix of a 2D Gaussian. We use these values to draw a visual representation to exploring how changing the mean and covariance alters the distribution.

import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as LA
from matplotlib.patches import Ellipse

def create_ellipse(mu, angle, width, height):
    # angle is plotted such that it starts from 180 and goes
    # clockwise instead of from 0 degrees and goes counter-clockwise
    # so 135 degrees -> 45 degrees
    return Ellipse(xy=mu, width=2*width, height=2*height, angle=angle,
                      facecolor='none', edgecolor='k', linewidth=3.5)

def plot_ellipse(mu, sigma):  
    # (w, v) = LA.eig(sigma)
    # angle = np.degrees(np.arctan2(v[1, 0], v[0, 0]))
    
    ax = plt.gca()
    angle = 20
    ellipse = create_ellipse(mu, angle, 10, 1)
    # ellipse = create_ellipse(mu, angle, w[0], w[1])
    ax.add_patch(ellipse)
    plt.plot(mu[0], mu[1], 'ro')

# Covariance matrix of the samples. Output: 2x2 matrix
C = np.cov(samples[:, 0], samples[:, 1])
print("Covariance =\n", C)

# Mean of the samples. Output: 2-element array
mean = np.mean(samples, 0)
print("Mean =\n", mean)

# Plot an ellipse which acts as a visual representation of the mean and covariance. Mean is represented by the red dot and the samples are the blue dots.
plt.title('Covariance')
plt.axis('equal')
plt.xlabel('VARIABLE 1')
plt.ylabel('VARIABLE 2')

plt.plot(samples[:500, 0], samples[:500, 1], 'bx')
plot_ellipse(mean, C)

# Fiddle with the diagonal values to get a better feel how it influences the distribution.
# plt.plot(samples[:500, 0], samples[:500, 1], 'bx')
# plot_ellipse(mean, np.array([[C[0, 0], 0], [0, C[1, 1]]]))
plt.show()