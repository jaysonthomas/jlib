import matplotlib.pyplot as plt

class PlotManager:
  def __init__(self, nPlots):
    plt.figure(figsize=(10, 6))
    self.nPlots = nPlots

  def plot(self, row, col, x, y, label, xLabel, yLabel, colour='blue'):
    plt.subplot(self.nPlots, row, col)
    plt.plot(x, y, label=label, color=colour)
    plt.legend()
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid()

  def stem(self, row, col, x, y):
    plt.subplot(self.nPlots, row, col)
    plt.stem(x, abs(y), 'b', markerfmt=" ", basefmt="-b")
    plt.xlabel('Freq (Hz)')
    plt.ylabel('DFT Amplitude |X(freq)|')

  def show(self):
    plt.tight_layout()
    plt.show()
