import matplotlib.pyplot as plt, numpy as np
from plotter import Plotter
import pendulum
import matplotlib.animation as animation

class Animator:
  def __init__(self, rk, pendulum, nFrames):
    self.seenFrames = set()
    self.nFrames = nFrames
    self.stateInDeg = []
    self.t = []
    self.stateInDeg.append(np.rad2deg(rk.y[0]).tolist())
    self.t.append(rk.t[0])

    plotter = Plotter(gridRows=2, gridCols=2, widthRatio=[1,2], heightRatio=[1,1])
    self.fig = plotter.fig
    self.rk = rk
    self.pendulum = pendulum

    # Pendulum
    x0, y0 = pendulum.getPos(rk.y[0][0])
    ax2 = plotter.subPlotSetup(gridY=1, xLimit=[-1,1], yLimit=[-1.5,0.5])
    self.pPendString, = ax2.plot([0, x0], [0, y0], lw=2, c='w')
    self.pPendBob = ax2.add_patch(plt.Circle([x0,y0], 0.05, fc='r', zorder=3))

    # State
    tStart, tEnd = rk.t[0], rk.t[-1]
    y0 = rk.y[0]
    yLabel = r'$\theta$ (deg), $\dot \theta$ (deg/s)'
    ax = plotter.subPlotSetup(gridX=0, gridY=0, xLimit=[0,tEnd], yLimit=[-100,100], yLabel=yLabel)

    self.pTheta, = ax.plot(tStart, y0[0], 'b', label=r'$\theta$')
    self.pThetaDot, = ax.plot(tStart, y0[1], 'r', label= r'$\dot \theta$')
    ax.legend()

    # Phase
    yLabel = r'$\dot \theta$ (deg/s)'
    xLabel = r'$\theta$ (deg)'
    ax1 = plotter.subPlotSetup(gridX=1, gridY=0, xLimit=[-100,100], yLimit=[-100,100], yLabel=yLabel, xLabel=xLabel)

    self.pPhaseCurve, = ax1.plot(y0[0], y0[1], 'b')
    self.pPhasePoint, =  ax1.plot(y0[0], y0[1], 'ro')

  def animate(self, interval=1, blit=True):
    ani = animation.FuncAnimation(self.fig, self.update, frames=self.nFrames-1, interval=interval, blit=blit)
    plt.show()
                  
  def update(self, i):
    if i not in self.seenFrames:
      self.seenFrames.add(i)
    else:
      return self.pTheta, self.pThetaDot, self.pPhaseCurve, self.pPhasePoint, self.pPendString, self.pPendBob,
  
    state, t = self.rk.step(i)                  # Currently, returns the state at i+1
    self.stateInDeg.append(np.rad2deg(state).tolist())
    self.t.append(t)

    print(f"State in deg:\n{self.stateInDeg}")
    print(f"\nIteration index:{i}\n{self.stateInDeg[:i+1][0]}")

    stateInDeg = np.array(self.stateInDeg)
    self.pTheta.set_data(self.t[:i+2], stateInDeg[:i+2, 0])
    self.pThetaDot.set_data(self.t[:i+2], stateInDeg[:i+2, 1])

    self.pPhaseCurve.set_data(stateInDeg[:i+2, 0], stateInDeg[:i+2, 1])
    self.pPhasePoint.set_data((stateInDeg[i:i+1, 0], stateInDeg[i:i+1, 1]))

    x, y = self.pendulum.getPos(self.rk.y[i+1][0])
    self.pPendString.set_data([0, x], [0, y])
    self.pPendBob.set_center((x, y))

    if i == self.nFrames-2:
      self.seenFrames.clear()
      self.stateInDeg = []
      self.t = []
      self.stateInDeg.append(np.rad2deg(self.rk.y[0]).tolist())
      self.t.append(self.rk.t[0])
    
    return self.pTheta, self.pThetaDot, self.pPhaseCurve, self.pPhasePoint, self.pPendString, self.pPendBob,
