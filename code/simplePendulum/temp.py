# %%
import numpy as np
from scipy.integrate import solve_ivp

# matplotlib imports
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
import plotter

def figureSetup():
  fig = plt.figure()

  # height/width_ratios describes the relative height/width of 
  # rows/columns respectively.
  grid = gridspec.GridSpec(2,2, width_ratios=[1,2], height_ratios=[1,1])
  return fig, grid    

def subPlotSetup(fig, gridLoc, xLimit=None, yLimit=None, xLabel=None, yLabel=None):
  ax = fig.add_subplot(gridLoc)
  ax.set_xlim(xLimit[0], xLimit[1])
  ax.set_ylim(yLimit[0], yLimit[1])
  ax.set_ylabel(yLabel)
  ax.set_xlabel(xLabel)
  ax.grid()
  return ax
    
def pend_pos(theta):
  return (ell*np.sin(theta), -ell*np.cos(theta))

# assign constants (g, ell) values
g = 9.81
ell = 1

# initial conditions: theta=30 deg, velocity=0
theta0 = np.deg2rad(30)
theta_dot0 = 0

# set the simulation time and frames per second
t_final = 5
fps = 60

def pendulum_ODE(t, y): 
  '''
  Pendulum's differential equations of motion
  y[0] is theta, y[1] is theta_dot
  '''
  return (y[1], -g*np.sin(y[0])/ell)

# solve the ODE, 30 fps
sol = solve_ivp(pendulum_ODE, [0, t_final], (theta0, theta_dot0), 
    t_eval=np.linspace(0,t_final,t_final*fps+1))

# output of the solver
theta, theta_dot = sol.y
t = sol.t

# convert from radians to degrees
theta_deg = np.rad2deg(sol.y[0])
theta_dot_deg = np.rad2deg(sol.y[1])

# optional: save theta_deg in a CSV file
# np.savetxt('pend.csv', np.transpose([t, theta_deg, theta_dot_deg]), delimiter=',')

# bonus! Customize color scheme in matplotlib
# change matplotlib defaults
# plt.rcParams['axes.facecolor'] = 'black'
# plt.rcParams['axes.labelcolor'] = 'white'
# plt.rcParams['axes.titlecolor'] = 'white'
# plt.rcParams['figure.facecolor'] = 'black'
# plt.rcParams['legend.labelcolor'] = 'white'
# plt.rcParams['xtick.labelcolor'] = 'white'
# plt.rcParams['ytick.labelcolor'] = 'white'
# plt.rcParams['grid.color'] = '#707070'

fig, grid = figureSetup()
yLabel = r'$\theta$ (deg), $\dot \theta$ (deg/s)'
ax0 = subPlotSetup(fig, grid[0,0], xLimit=[0,t_final], yLimit=[-100,100], yLabel=yLabel)

theta_curve, = ax0.plot(t[0], theta_deg[0], 'b', label=r'$\theta$')
theta_dot_curve, = ax0.plot(t[0], theta_dot_deg[0], 'r', label= r'$\dot \theta$')
ax0.legend()

yLabel = r'$\dot \theta$ (deg/s)'
xLabel = r'$\theta$ (deg)'
ax1 = subPlotSetup(fig, grid[1,0], xLimit=[-100,100], yLimit=[-100,100], yLabel=yLabel, xLabel=xLabel)

phase_curve, = ax1.plot(theta_deg[0], theta_dot_deg[0], 'b')
phase_dot, =  ax1.plot(theta_deg[0], theta_dot_deg[0], 'ro')

ax2 = fig.add_subplot(grid[:,1])
ax2.set_xlim(-1, 1)
ax2.set_ylim(-1.5, 0.5)
ax2 = subPlotSetup(fig, grid[:,1], xLimit=[-1,1], yLimit=[-1.5,0.5])
                   
# draw the pendulum
x0, y0 = pend_pos(theta0)
line, = ax2.plot([0, x0], [0, y0], lw=2, c='w')
circle = ax2.add_patch(plt.Circle(pend_pos(theta0), 0.05, fc='r', zorder=3))


def animate(i):
    theta_curve.set_data(t[:i+1], theta_deg[:i+1])
    theta_dot_curve.set_data(t[:i+1], theta_dot_deg[:i+1])

    phase_curve.set_data(theta_deg[:i+1], theta_dot_deg[:i+1])
    phase_dot.set_data((theta_deg[i], theta_dot_deg[i]))

    x, y = pend_pos(theta[i])
    line.set_data([0, x], [0, y])
    circle.set_center((x, y))

plotter.Plotter(2, 2, [1,1], [1,2])
# # save a video: 30 fps
ani = animation.FuncAnimation(fig, animate, frames=len(t), interval=1, blit=True)
plt.show()
# ffmpeg_writer = animation.FFMpegWriter(fps=fps)
# ani.save('all.mp4', writer=ffmpeg_writer)

