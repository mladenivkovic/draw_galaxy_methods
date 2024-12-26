#!/usr/bin/env python3

# upscale reduced image, but keep it looking pixelated

import tools
from matplotlib import pyplot as plt
import numpy as np

# How many pixels do you want as output?
npixel = 2048


source_img = tools.get_src_img(addendum="reduced")

if source_img.shape[0] != source_img.shape[1]:
    raise ValueError("source image must be N x N pixels. You gave me", source_img.shape[0], source_img.shape[1])

new_img = np.zeros((npixel, npixel, source_img.shape[2]), dtype=source_img.dtype)

if npixel % source_img.shape[0]!= 0 :
    raise ValueError("No modulo free division source image pixels vs requested pixels")

stride = npixel // source_img.shape[0]

for i in range(source_img.shape[0]):
    if i % 10 == 0:
        print("i=", i)
    for j in range(source_img.shape[1]):
        for k in range(source_img.shape[2]):
            new_img[i*stride:(i+1)*stride+1,j*stride:(j+1)*stride+1,k] = source_img[i,j,k]

plt.figure()
plt.imshow(new_img)

tools.savefig(new_img, addendum="upscaled")



