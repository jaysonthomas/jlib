import matplotlib.pyplot as plt

class PlotManager:
  def __init__(self, nPlots):
    plt.figure(figsize=(10, 6))
    self.nPlots = nPlots

  def plot(self, row, col, x, y, label, xLabel, yLabel):
    plt.subplot(self.nPlots, row, col)
    plt.stem(x, y, label=label)
    plt.legend()
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid()

  def show(self):
    plt.tight_layout()
    plt.show()
