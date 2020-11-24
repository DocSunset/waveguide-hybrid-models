# based on the tutorial and example script found here: https://scipython.com/blog/cobweb-plots/

import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

# Figure dpi
dpi = 72

def plot_cobweb(f, r, x0, nmax=400):
    """Make a cobweb plot.

    Plot y = f(x; r) and y = x for 0 <= x <= 1, and illustrate the behaviour of
    iterating x = f(x) starting at x = x0. r is a parameter to the function.

    """
    x = np.linspace(-1, 1, 100)
    fig = plt.figure(figsize=(600/dpi, 450/dpi), dpi=dpi)
    ax = fig.add_subplot(111)

    # Plot y = f(x) and y = x
    ax.plot(x, f(x, r), c='#444444', lw=2)
    ax.plot(x, x, c='#ff0000', lw=2)

    # Iterate x = f(x) for nmax steps, starting at (x0, 0).
    px, py = np.empty((2,nmax+1,2))
    px[0], py[0] = x0, 0
    for n in range(1, nmax, 2):
        px[n] = px[n-1]
        py[n] = f(px[n-1], r)
        px[n+1] = py[n]
        py[n+1] = py[n]

    # Plot the path traced out by the iteration.
    ax.plot(px, py, c='b', alpha=0.3)

    # Annotate and tidy the plot.
    ax.minorticks_on()
    ax.grid(which='minor', alpha=0.5)
    ax.grid(which='major', alpha=0.5)
    ax.set_aspect('equal')
    ax.set_xlabel('x[n]')
    ax.set_ylabel('x[n+1]')
    ax.set_title('x = f(x)')

    plt.savefig('cobweb_{:.1}_{:.2}.png'.format(x0, r), dpi=dpi)

class AnnotatedFunction:
    """A small class representing a mathematical function.

    This class is callable so it acts like a Python function, but it also
    defines a string giving its latex representation.

    """

    def __init__(self, func, latex_label):
        self.func = func
        self.latex_label = latex_label

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

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

def saturation_map(x, m):
  mx = 10*m * x
  return -mx / ((1 + abs(mx)**3.5)**(1/3.5))

def logistic_map(x, r):
  xs = (x + 1) / 2.0
  y = 4*r*x*(1-x)
  return y * 2 - 1.0

func = line_map

plot_cobweb(func, 0.0, 0.005)
plot_cobweb(func, 0.1, 0.005)
plot_cobweb(func, 0.2, 0.005)
plot_cobweb(func, 0.3, 0.005)
plot_cobweb(func, 0.4, 0.005)
plot_cobweb(func, 0.5, 0.005)
plot_cobweb(func, 0.6, 0.005)
plot_cobweb(func, 0.7, 0.005)
plot_cobweb(func, 0.8, 0.005)
plot_cobweb(func, 0.9, 0.005)
plot_cobweb(func, 1.0, 0.005)
