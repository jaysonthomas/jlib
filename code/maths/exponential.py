import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')

fontSize = 14

plt.rcParams['axes.labelsize'] = fontSize  # Font size for axis labels
plt.rcParams['axes.titlesize'] = fontSize  # Font size for titles

# Parameters for the complex sinusoid
t = np.linspace(0, 2 * np.pi, 500)  # Time values

# Complex sinusoid
z = np.exp(1j * 2 * t)  # e^(j2t)

# Extract real and imaginary parts
real_part = np.real(z)
imag_part = np.imag(z)

# Plotting the complex sinusoid in 2D space
plt.figure(figsize=(6, 6))

# plt.plot(t, imag_part, label="$e^{j2t}$", color="lightskyblue", linewidth=2)
# plt.plot(t, real_part, label="$e^{j2t}$", color="lightskyblue", linewidth=2)

plt.plot(real_part, imag_part, label="$e^{j2t}$", color="lightskyblue", linewidth=2)
plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
plt.axvline(0, color="black", linewidth=0.8, linestyle="--")

plt.tick_params(axis='x', labelsize=fontSize)
plt.tick_params(axis='y', labelsize=fontSize)
plt.title("Complex Sinusoid ($e^{j2t}$)")
plt.xlabel("Real Part")
plt.ylabel("Imaginary Part")
plt.grid(True)
plt.legend()
plt.axis('equal')  # Ensure the aspect ratio is 1:1
plt.show()
