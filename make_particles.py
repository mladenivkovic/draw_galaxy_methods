#!/usr/bin/env python3

# upscale reduced image, but keep it looking pixelated, and like something out of a simulation
# add cell borders to show cells, make it look like an AMR simulation

import tools
from AMR import *
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np

mpl.rcParams["figure.subplot.top"] = 1.0
mpl.rcParams["figure.subplot.bottom"] = 0.0
mpl.rcParams["figure.subplot.right"] = 1.0
mpl.rcParams["figure.subplot.left"] = 0.0
mpl.rcParams["figure.figsize"] = (10, 10)

# how many particles to use
nparts = 50000
xp = np.zeros(nparts)
yp = np.zeros(nparts)

# internal coordinates extent, i.e. boxsize
extent = 1.

source_img = tools.get_src_img(addendum="reduced")

# convert to floats
if source_img.dtype != np.uint8:
    raise ValueError("Can't handle image data with this data type yet")

if source_img.shape[0] != source_img.shape[1]:
    raise ValueError("source image must be N x N pixels. You gave me", source_img.shape[0], source_img.shape[1])

ncells = source_img.shape[0]

# the image used to refine grid
new_img_float = np.zeros((ncells, ncells))

for i in range(source_img.shape[0]):
    for j in range(source_img.shape[1]):
        # TODO: this assumes source_img is data type integer
        new_img_float[i,j] = np.sum((255 - source_img[i,j,:]))

        # Dummy testing values
        #  if i < 64:
        #      if j < 64:
        #          new_img_float[i,j] = 1.
        #      else:
        #          new_img_float[i,j] = 4.
        #  else:
        #      if j < 64:
        #          new_img_float[i,j] = 16.
        #      else:
        #          new_img_float[i,j] = 64.


plt.figure()
ax = plt.subplot(111)
ax.axis("off")

# Invert image: High values = bright
new_img_float = np.abs(new_img_float - new_img_float.max())

# normalize
new_img_float = new_img_float / new_img_float.max()
# help the sampling out to look better by scaling the probabilities
new_img_float = new_img_float**2


def random_positions(rng):

    x = rng.uniform(0., extent)
    y = rng.uniform(0., extent)

    return x, y


def get_image_value(x, y, image):

    dc = extent / ncells

    j = int((extent - x) * ncells)
    i = int(y * ncells)

    return image[i,j]


def sample_image(rng, image):
    
    x, y = random_positions(rng)
    
    imgval = get_image_value(x, y, image)
    sample = rng.uniform(0., 1.)

    return sample <= imgval, x, y

    



rng = np.random.default_rng(seed=666)

n_accepted = 0
n_tried = 0

for i in range(nparts):
    if i % 100 == 0 and i > 0:
        print("{0:6d}/{1:6d}, acceptance rate {2:.3f}".format(i, nparts, n_accepted/n_tried))
    accepted = False
    while not accepted:
        n_tried += 1
        accepted, x, y = sample_image(rng, new_img_float)
    n_accepted += 1

    xp[i] = x
    yp[i] = y

# transform coordinates from imshow() image coordinates to math-like coordinates
yp = np.abs(yp - extent)
xp = np.abs(xp - extent)

plt.imshow(np.zeros(new_img_float.shape), interpolation="none", extent=[0., 1., 0., 1.], zorder=0, cmap="inferno")

plt.scatter(xp, yp, s=1, c="C1", marker="o", alpha=0.4)

#  plt.show()

figname=tools.get_outputfigname("particles")
plt.savefig(figname, dpi=200)
print("Saved", figname)
