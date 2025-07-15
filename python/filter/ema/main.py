import numpy as np
from ema import EMA

# Sampling frequency
fs = 16000
ts = 1/16000

# Subsampling period: 5ms, 200Hz
tss = 0.005

ema = EMA()

alpha1 = ema.getAlpha(ts, tss)
fc1 = ema.getFc(alpha1, ts)
print(f"For fs=16kHz, fss=200Hz, (alpha, fc) =\
       ({alpha1}, {fc1}")

alpha2 = ema.getAlpha(1, tss)
fc2 = ema.getFc(alpha2, 1)
print(f"For fs=1, fss=200Hz, (alpha, fc) = \
      ({alpha2}, {fc2}")

print(f"{np.abs(alpha1-alpha2)}")
