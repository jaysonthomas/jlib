import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

class Plotter:
  def __init__(self):
    pylab.rcParams["figure.figsize"] = 10, 10
    self.fontSize = 10

  def plot(self, t, z, zEstimate, x):
    self.plotNoEstimation(t, z, x)
    self.plotAfterEstimation(t, z, zEstimate, x)
    self.plotError(t, z, x)
    plt.show()

  def plotAfterEstimation(self, t, z, zEstimate, x):
    plt.subplot(312)
    plt.plot(t[1:], z[0], linestyle="-", marker=".", color="red", label="Path w noiseless input")
    plt.plot(t[1:], x[2][:, 0], linestyle="-", color="blue", linewidth=3, label="Path w estimated input")
    plt.scatter(t[1:], z[2][:, 0], color="black", marker=".", alpha=0.3, label="Measurements")
    plt.plot(t[1:],zEstimate[2][:, 0], linestyle="-", color="green", linewidth=3, label="Averaged height")

    plt.title("Height vs time").set_fontsize(self.fontSize)
    plt.xlabel("$t$ [sec]").set_fontsize(self.fontSize)
    plt.ylabel("Altitude [m]").set_fontsize(self.fontSize)
    plt.xticks(fontsize=self.fontSize)
    plt.yticks(fontsize=self.fontSize)
    plt.legend()
    plt.grid()

  def plotError(self, t, z, x):
    plt.subplot(313)
    error = z[0][1]- x[0][:, 0]
    plt.plot(t[1:], error, linestyle="-", marker=".", color="blue", label="Ideal input")
    error = z[0][1]- x[1][:, 0]
    plt.plot(t[1:], error, linestyle="-", marker=".", color="green", label="Measured input")
    error = z[0][1]- x[2][:, 0]
    plt.plot(t[1:], error, linestyle="-", marker=".", color="pink", label="Estimated input")
    
    plt.title("Error value ").set_fontsize(self.fontSize)
    plt.xlabel("$t$ [sec]").set_fontsize(self.fontSize)
    plt.ylabel("$z_{target} - z_{actual}$ [$m$]").set_fontsize(self.fontSize)
    plt.xticks(fontsize=self.fontSize)
    plt.yticks(fontsize=self.fontSize)
    plt.legend()
    plt.grid()

  def plotNoEstimation(self, t, z, x):
    plt.subplot(311)
    plt.plot(t[1:], z[0], linestyle="-", marker=".", color="red", label="Path w noiseless input")
    plt.plot(t[1:], x[1][:, 0], linestyle="-", color="blue", linewidth=3, label="Path w measured input")
    plt.scatter(t[1:], z[1][:, 0], color="black", marker=".", alpha=0.3, label="Measurements")

    
    plt.title("Height vs time").set_fontsize(self.fontSize)
    plt.xlabel("$t$ [sec]").set_fontsize(self.fontSize)
    plt.ylabel("Altitude [m]").set_fontsize(self.fontSize)
    plt.xticks(fontsize=self.fontSize)
    plt.yticks(fontsize=self.fontSize)
    plt.legend()
    plt.grid()