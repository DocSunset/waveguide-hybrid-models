import sys
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

iterate = int(sys.argv[1])

dpi=72

m = -0.8
b = 0.6
def clarinet_map(x, r):
  d = -(0.95*x + r)
  p = d * (m * d + b) + r
  return np.clip(p, -1, 1)

def flute_map(x, r):
  return np.clip(p, -1, 1)

x = np.linspace(-1, 1, 100)
y = x
fig = plt.figure(figsize=(600/dpi, 450/dpi), dpi=dpi)
ax = fig.add_subplot(111)

# Plot y = f(x) and y = x
for i in range(0, iterate):
  y = clarinet_map(y, 0.8)

ax.plot(x, y, c='#444444', lw=2)
ax.plot(x, x, c='#ff0000', lw=2)

plt.plot()
plt.show()
