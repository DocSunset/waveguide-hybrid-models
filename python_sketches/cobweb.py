# based on the tutorial and example script found here: https://scipython.com/blog/cobweb-plots/
# an the animation tutorial found here: https://towardsdatascience.com/animations-with-matplotlib-d96375c5442c

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

m = -0.3
b = 0.7
def clarinet_map(r, h):
  x = -(0.95*r + h)
  p = x * np.clip(m * x + b, -1, 1) + h
  return p

def flute_map(r, h):
  x = r - h;
  p = x * x * x - x;
  return np.clip(p, -1, 1)

def line_map(x, m):
  return np.clip(-2*m * x + 0.0001, -1, 1)

def saturation_map(x, n):
  m = 5
  mx = m * x
  return -mx / ((1 + abs(mx)**(2.5*(n+1)))**(1/(2.5*(n+1))))

def logistic_map(x, r):
  xs = (x + 1) / 2.0
  y = (r+3)*xs*(1-xs)
  return y * 2 - 1.0

f = saturation_map
r_min = 0.0
r_max = 1.0
x0 = 0.005
nmax = 200
duration = 10
frame_period = 20
num_frames = int(duration / (frame_period / 1000))
dpi = 72

def r(n):
  return (r_max - r_min) * n/num_frames + r_min

x = np.linspace(-1, 1, 100)
fig = plt.figure(figsize=(600/dpi, 450/dpi), dpi=dpi)
ax = fig.add_subplot(111)

# Annotate and tidy the plot.
ax.minorticks_on()
ax.grid(which='minor', alpha=0.5)
ax.grid(which='major', alpha=0.5)
ax.set_aspect('equal')
xlab = ax.set_xlabel('x[n]')
ylab = ax.set_ylabel('x[n+1]')
titl = ax.set_title('x = f(x)')

# Plot y = f(x) and y = x
ax.plot(x, x, c='#ff0000', lw=2)
fx, = ax.plot([], [], c='#444444', lw=2)
web, = ax.plot([], [], c='b', alpha=0.3)
px, py = np.empty((2,nmax+1,2))

def init():
  fx.set_data([], [])
  web.set_data([], [])
  return fx, web

def animate(n):
  rn = r(n)
  # Iterate x = f(x) for nmax steps, starting at (x0, 0).
  px[0], py[0] = x0, 0
  for n in range(1, nmax, 2):
      px[n] = px[n-1]
      py[n] = f(px[n-1], rn)
      px[n+1] = py[n]
      py[n+1] = py[n]
  fx.set_data(x, f(x, rn))
  web.set_data(px, py)
  return fx, web

anim = FuncAnimation(fig, animate, init_func=init, 
                     frames=num_frames, interval=frame_period, blit=True)

anim.save(f'{f.__name__}_cobweb_x0-{x0}_rmin-{r_min}_rmax-{r_max}.gif', writer='imagemagick')
