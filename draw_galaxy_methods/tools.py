#!/usr/bin/env python3

import os
from matplotlib import pyplot as plt

debug = True


def _get_src_image_name(addendum=None):

    # file containing the source image filename
    srcfilenamecontainer = "source_image_to_use"

    if not os.path.exists(srcfilenamecontainer):
        raise FileNotFoundError("Didn't find file container")

    f = open(srcfilenamecontainer, "r")
    srcfnameline = f.readline()
    srcfname = srcfnameline.strip()

    if addendum is not None:
        suffix = _get_image_suffix(srcfname)
        basename = srcfname[:-len(suffix)-1]
        srcfname =  basename + "-" + addendum + "." + suffix 

    if debug:
        print("srcfname", srcfname)

    if not os.path.exists(srcfname):
        raise FileNotFoundError("Image not found")

    return srcfname
 

def _get_image_suffix(srcfname):

    dot = None
    for i in range(len(srcfname), 0, -1):
        if srcfname[i-1] == ".":
            dot = i-1
            break

    if dot == None:
        raise ValueError("Wrong file suffix? Couldn't find dot in image filename")

    suffix = srcfname[dot+1:]

    if debug:
        print("suffix", suffix)

    return suffix



def get_src_img(addendum=None):
    """
    Read in file.

    Returns image data as numpy array.
    """

    srcfname = _get_src_image_name(addendum=addendum)

    image = plt.imread(srcfname)

    return image


def get_outputfigname(addendum):

    srcfigname = _get_src_image_name()
    suffix = _get_image_suffix(srcfigname)
    basename = srcfigname[:-len(suffix)-1]

    figname =  basename + "-" + addendum + "." + suffix 

    return figname


def savefig(image, addendum):

    figname = get_outputfigname(addendum)

    plt.imsave(figname, image)
    print("saved", figname)
    return
