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

# How many pixels do you want as output?
npixel = 200

source_img = tools.get_src_img(addendum="reduced")

if source_img.shape[0] != source_img.shape[1]:
    raise ValueError("source image must be N x N pixels. You gave me", source_img.shape[0], source_img.shape[1])

new_img = np.zeros((npixel, npixel), dtype=source_img.dtype)

if npixel % source_img.shape[0]!= 0 :
    raise ValueError("No modulo free division source image pixels vs requested pixels")

stride = npixel // source_img.shape[0]

for i in range(source_img.shape[0]):
    if i % 10 == 0:
        print("i=", i)
    for j in range(source_img.shape[1]):
        for k in range(source_img.shape[2]):
            new_img[i*stride:(i+1)*stride+1,j*stride:(j+1)*stride+1] = source_img[i,j,k]



plt.figure()
plt.gca().axis("off")
plt.imshow(new_img, interpolation="none")

figname=tools.get_outputfigname("density_field")
plt.savefig(figname, dpi=200)



