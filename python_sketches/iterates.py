import sys
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

iterate = int(sys.argv[1])

dpi=72

breath_pressure = 0.9;

m = -0.8
b = 0.6
def clarinet_map(x, r):
  d = -(0.95*x + r)
  p = d * np.clip(m * d + b, -1, 1) + r
  return p

def flute_map(x, r):
  d = -(0.95*x + r)
  p = d * (d * d - 1)
  return np.clip(p, -1, 1)

the_map = clarinet_map

x = np.linspace(-1, 1, 1000)
y = x
fig = plt.figure(figsize=(600/dpi, 450/dpi), dpi=dpi)
ax = fig.add_subplot(111)

# Plot y = f(x) and y = x
for i in range(1, iterate*2, 2):
  y = the_map(y, breath_pressure)
  ax.plot(x, y, c='#444444', lw=1)
  y = clarinet_map(y, 0.8)

ax.plot(x, x, c='#ff0000', lw=2)

plt.plot()
plt.show()
