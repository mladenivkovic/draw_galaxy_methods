#!/usr/bin/env python3

# Average image down to npixel x npixel

import tools
from matplotlib import pyplot as plt
import numpy as np

# How many pixels do you want as output?
npixel = 128



source_img = tools.get_src_img()

if source_img.shape[0] != source_img.shape[1]:
    raise ValueError("source image must be N x N pixels. You gave me", source_img.shape[0], source_img.shape[1])

new_img = np.zeros((npixel, npixel, source_img.shape[2]), dtype=source_img.dtype)

if source_img.shape[0] % npixel != 0 :
    raise ValueError("No modulo free division source image pixels vs requested pixels")

stride = source_img.shape[0] // npixel

for i in range(npixel):
    if i % 10 == 0:
        print("i=", i)
    for j in range(npixel):
        for k in range(source_img.shape[2]):
            new_img[i,j,k] = np.sum(source_img[i*stride:(i+1)*stride, j*stride:(j+1)*stride, k]) // (stride * stride)


plt.figure()
plt.imshow(new_img)

tools.savefig(new_img, addendum="reduced")



