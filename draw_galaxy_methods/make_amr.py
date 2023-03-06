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

# How many pixels do you want as output?
# make sure this is a power of two
npixel = 2048
dpi = 200

mpl.rcParams["figure.figsize"] = (npixel / dpi, npixel / dpi)

# internal image coordinate extent
extent = 1.

source_img = tools.get_src_img(addendum="reduced")

# convert to floats
if source_img.dtype != np.uint8:
    raise ValueError("Can't handle image data with this data type yet")


if source_img.shape[0] != source_img.shape[1]:
    raise ValueError("source image must be N x N pixels. You gave me", source_img.shape[0], source_img.shape[1])

ncells = source_img.shape[0]

# the image used for plotting high resolution image that still looks pixelated
new_img = np.zeros((npixel, npixel))

# the image used to refine grid
new_img_float = np.zeros((ncells, ncells))
new_img_amr = np.zeros((ncells, ncells))

if npixel % source_img.shape[0]!= 0 :
    raise ValueError("No modulo free division source image pixels vs requested pixels. sourge_img.shape=", source_img.shape)

stride = npixel // source_img.shape[0]

for i in range(source_img.shape[0]):
    for j in range(source_img.shape[1]):
        for k in range(source_img.shape[2]):
            new_img[i*stride:(i+1)*stride+1,j*stride:(j+1)*stride+1] = source_img[i,j,k]
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
ax = plt.gca()
ax.axis("off")

# Invert image: High values = bright
new_img_float = np.abs(new_img_float - new_img_float.max())

# plot what you are actually using as the image to generate AMR grid
#  plt.imshow(new_img_float, interpolation="none", extent=[0., 1., 0., 1.])
#  plt.colorbar()


# Get the AMR grid now, and draw it directly
#----------------------------------------------

# this threshold is completely arbitrary.
refine_threshold = 8 * np.mean(new_img_float)
params = amr_params(ncells, extent, ax, new_img_float, new_img_amr, refine_threshold, verbose=False)

root = cell(0, 0, params)
root.draw()
root.refine()
print("max level reached:", max_level_reached)

# check output image
#  plt.imshow(params.amr_image, interpolation="none", extent=[0., 1., 0., 1.], zorder=0)

# Scale image back up to high resolution, but keep it looking pixelated
stride = npixel // source_img.shape[0]

for i in range(source_img.shape[0]):
    for j in range(source_img.shape[1]):
            new_img[i*stride:(i+1)*stride+1,j*stride:(j+1)*stride+1] = params.amr_image[i,j]

plt.imshow(new_img, interpolation="none", extent=[0., 1., 0., 1.], zorder=0)

#  plt.show()

figname=tools.get_outputfigname("amr")
plt.savefig(figname, dpi=200)
print("Saved", figname)
