# type: ignore
import numpy as np
import waveManager as wm
import plotManager as pm
import dft

wm = wm.WaveManager(100)
pm = pm.PlotManager(1)

input = wm.create([1, 3, 20], [2.0, 1.5, 1.0])
pm.plot(2, 1, wm.t, input, 'Wave', 'Time', 'Amplitude')

dft = dft.DFT(input)
# pm.plot(2, 2, dft.getFreqs(), abs(dft.getAmplitudeOfFreqs()), "DFT", "Freq(Hz)", "Amplitude")
pm.plot(2, 2, dft.getFreqs(), dft.getAmplitudeOfFreqs(), "DFT2", "Freq(Hz)", "Amplitude", colour='orange')
# X = dft.getAmplitudeOfFreqsVectorised()
# N = len(X)
# n = np.arange(N)
# T = N/100
# freq = n/T 

# pm.stem(2, 2, freq, abs(X))
pm.show()