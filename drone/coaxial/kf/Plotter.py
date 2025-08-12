import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
from scipy.stats import multivariate_normal

class Plotter:
  def __init__(self):
    plt.grid()
    plt.title('State Space ').set_fontsize(20)
    plt.xlabel('$z$ [m]').set_fontsize(20)
    plt.ylabel('$\\dot{z}$[$m/s$]').set_fontsize(20)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.axis('equal')    

  @staticmethod
  def legendSetup(legendList):
    plt.legend(legendList, fontsize = 14)

  @staticmethod
  def plotArrow(startX, startY, endX, endY, head_length=0.1, head_width=0.05):
    angle = np.arctan2(endY - startY, endX - startX)

    arrow_length_x = float(endX - startX - head_length * np.cos(angle))
    arrow_length_y = float(endY - startY - head_length * np.sin(angle))

    plt.arrow(startX, startY,
              arrow_length_x,
              arrow_length_y, 
              head_width=head_width, head_length=head_length, 
              fc='k', ec='k')

  @staticmethod
  def plotContour(gridX, gridY, pdf, contourLevels, colour, meanX, meanY):
    plt.contour(gridX, gridY, pdf, contourLevels, colors=colour)
    plt.scatter(meanX, meanY, color=colour)

  @staticmethod
  def plotDistAsContour(mu, sigma, configurationSpace, colour):
    stateSpace = multivariate_normal(mu, sigma)

    # levels at 1, 2 and 3 sigmas 
    distPoints = np.array([np.exp(-4.5), np.exp(-2), np.exp(-0.5)])
    contour_levels = distPoints * stateSpace.pdf(mu)
    Plotter.plotContour(configurationSpace[:, :, 0], configurationSpace[:, :, 1], 
                     stateSpace.pdf(configurationSpace), 
                     contour_levels, colour, mu[0], mu[1])
    
  @staticmethod
  def display(legendList):
    Plotter.legendSetup(legendList)
    plt.show()