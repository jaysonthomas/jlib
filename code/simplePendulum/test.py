import matplotlib.animation as animation
import matplotlib.pyplot as plt
from plotter import Plotter

class Animator:
  def __init__(self):
    plotter = Plotter(gridRows=2, gridCols=2, widthRatio=[1, 2], heightRatio=[1, 1])
    self.fig = plotter.fig

    ax = plotter.subPlotSetup(gridX=0, gridY=0, xLimit=[0,20], yLimit=[-100,100])

    self.pTheta, = ax.plot(1, 10)
    self.seenFrames = set()

  def animate(self, nFrames, interval=100, blit=True):
    ani = animation.FuncAnimation(self.fig, self.update, frames=nFrames, interval=interval, blit=blit)
    plt.show()

  def update(self, i):
    if i not in self.seenFrames:
      self.seenFrames.add(i)
    else:
      return self.pTheta,
    
    if i == 19:
      self.seenFrames.clear()
    
    print(i)
    return self.pTheta,

animator = Animator()
animator.animate(20)
