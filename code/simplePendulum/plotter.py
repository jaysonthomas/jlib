import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation

class Plotter:
  def __init__(self, gridRows=1, gridCols=1, widthRatio=[1], heightRatio=[1], darkMode=True):
    if (darkMode):
      self.setDarkMode()
    self.fig = plt.figure()

    # height/width_ratios describes the relative height/width of 
    # rows/columns respectively.
    self.grid = gridspec.GridSpec(gridRows, gridCols, width_ratios=widthRatio, height_ratios=heightRatio)
  
  def animate(self, updateFunc, nFrames, interval=1, blit=True):
    ani = animation.FuncAnimation(self.fig, updateFunc, frames=nFrames, interval=interval, blit=blit)
    plt.show()

  def setDarkMode(self):
    # Change matplotlib defaults
    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['axes.titlecolor'] = 'white'
    plt.rcParams['figure.facecolor'] = 'black'
    plt.rcParams['legend.labelcolor'] = 'white'
    plt.rcParams['xtick.labelcolor'] = 'white'
    plt.rcParams['ytick.labelcolor'] = 'white'
    plt.rcParams['grid.color'] = '#707070'

  def subPlotSetup(self, gridX=slice(None), gridY=slice(None), xLimit=None, yLimit=None, xLabel=None, yLabel=None):
    ax = self.fig.add_subplot(self.grid[gridX, gridY])
    ax.set_xlim(xLimit[0], xLimit[1])
    ax.set_ylim(yLimit[0], yLimit[1])
    ax.set_ylabel(yLabel)
    ax.set_xlabel(xLabel)
    ax.grid()
    return ax
      