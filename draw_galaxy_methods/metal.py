#!/usr/bin/env python3

# upscale reduced image, but keep it looking pixelated, and like something out of a simulation

import tools
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np

mpl.rcParams["figure.subplot.top"] = 1.0
mpl.rcParams["figure.subplot.bottom"] = 0.0
mpl.rcParams["figure.subplot.right"] = 1.0
mpl.rcParams["figure.subplot.left"] = 0.0
mpl.rcParams["figure.figsize"] = (10,10)


source_img = tools.get_src_img()

if source_img.shape[0] != source_img.shape[1]:
    raise ValueError("source image must be N x N pixels. You gave me", source_img.shape[0], source_img.shape[1])
npixel = source_img.shape[0]

new_img = np.zeros((npixel, npixel), dtype=source_img.dtype)

new_img[:, :] = source_img[:,:,0]**2 +  source_img[:,:,1]**2 + source_img[:,:,2]**2
new_img = np.sqrt(new_img)


import h5py
outfile="NGC7496.hdf5"
hfile = h5py.File(outfile, "w")

dat = hfile.create_dataset("image", new_img.shape, dtype="f", compression="gzip")
dat[:] = new_img[:]

hfile.close()


plt.figure()
plt.gca().axis("off")
plt.imshow(new_img, interpolation="none")

figname=tools.get_outputfigname("density_field")
plt.savefig(figname, dpi=200)



