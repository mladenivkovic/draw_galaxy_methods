# AMR related stuff.

import numpy as np
from matplotlib import patches as ptch

max_level_reached = 0


class amr_params():
    """
    Global AMR parameters.
    """

    def __init__(self, ncells, extent, ax, image, amr_image, refine_threshold, verbose=False):

        # max number of cells
        self.ncells = ncells

        # coordinate extent of box in both dimensions
        self.extent = extent
        self.dcellmin = extent / ncells

        # ax object to draw on
        self.ax = ax

        # actual background/underlying image
        self.image = image

        if np.atleast_3d(image).shape[2] != 1 or image.shape[0] != ncells or image.shape[1] != ncells:
            raise ValueError("Image must be in shape (ncells, ncells, 1), but currently is", np.atleast_3d(image).shape)

        # image that contains averaged values according to the
        # AMR grid
        self.amr_image = amr_image

        if amr_image.shape != image.shape:
            raise ValueError("parameters 'image' and 'amr_image' must have same shape.")

        # criterion to refine further
        self.refine_threshold = refine_threshold

        # am I talkative?
        self.verbose = verbose

        # internal counters and flags
        self.leafcount = 0
        self.maxdepthcount = 0
        self.max_depth_reached = False

        # Find max refinement level
        self.levelmax = 0
        while self.ncells // (2**self.levelmax) != 1:
            self.levelmax += 1
            if self.levelmax == 128:
                raise ValueError("Reached levelmax=128?? That's too much")

        if self.ncells != 2**self.levelmax:
            raise ValueError(
                    "ncells is not a power of 2, but needs to be. ncells=", 
                    self.ncells, 
                    "levelmax=", 
                    self.levelmax, 
                    "mod=", 
                    self.ncells/2**self.levelmax)
        print("Found levelmax", self.levelmax)

        return



class cell():
    """
    A cell object used to construct AMR grid in 2D.
    """


    def __init__(self, i, j, amr_params):

        self.params = amr_params

        if i >= self.params.ncells:
            raise ValueError("Error: i =", i, "ncells=", self.params.ncells)
        if j >= self.params.ncells:
            raise ValueError("Error: i =", i, "ncells=", self.params.ncells)

        # index of cell.
        self.i = i
        self.j = j
        # refinement level
        self.level = 0
        self.children = []
        self.parent = None

        #  self.edgecolor = "k"
        self.edgecolor = "r"

        return

    def get_cell_width(self):
        w = self.params.extent / (2 ** self.level)
        return w

    def get_cell_integer_width(self):
        w = self.params.ncells // (2 ** self.level)
        return w

    def draw(self):

        dx = self.params.dcellmin
        width = self.get_cell_width()
        nc = self.params.ncells
        x = (nc - self.i) * dx - width
        y = self.j * dx
        self.params.ax.add_patch(
                ptch.Rectangle((y, x), width, width, edgecolor=self.edgecolor, lw=1, fill=False, zorder=1)
                )

    def report(self):
        """
        Print some information about the cell.
        """
        print(
                "REPORT: i", 
                self.i, 
                "j", 
                self.j,
                "dx", 
                self._get_dx(), 
                "w", 
                self._get_width(), 
                "children:", 
                self.children, 
                "parent:", 
                self.parent
                )
        return


    def get_contents(self):
        """
        Calculate how much of the quantity of the image this cell contains.
        """

        w = self.get_cell_integer_width()
        i = self.i
        j = self.j
        img = self.params.image

        if w == 1:
            return img[i, j]
        else:
            return np.sum(img[i:i+w,j:j+w])


    def inc_leafcount(self):
        if self.params.verbose:
            print("Reached leaf at", self.i, self.j, "level=", self.level)

        self.params.leafcount += 1

        if self.params.leafcount > self.params.ncells * self.params.ncells:
            raise ValueError("Found more leaves than cells. Something's fucky")

        return


    def inc_maxdepthcount(self):
        if self.params.verbose:
            print("reached levelmax leaf at", self.i, self.j)
        else:
            if not self.params.max_depth_reached:
                print("reached max depth")
                self.params.max_depth_reached = True
        self.params.maxdepthcount += 1
        if self.params.maxdepthcount > self.params.ncells * self.params.ncells:
            raise ValueError("Found more maxdepth counts than cells. Something's fucky")
        return


    def get_cell_volume(self):

        w = self.get_cell_width()
        return w*w


    def get_density(self):

        contents = self.get_contents()
        volume = self.get_cell_volume()

        if volume == 0.:
            return ValueError("Got zero volume")

        return contents/volume



    def do_refine(self):
        """
        Defines criterion for further refinement. Returns
        true if you should keep refining.
        """

        #  density = self.get_density()
        # just use contents for now. Seems to work better.
        density = self.get_contents()

        return density > self.params.refine_threshold


    def write_image_maxlevel_leaf(self):
        """
        write the value in the output image for a leaf
        cell that is at the max level
        """

        i = self.i
        j = self.j
        self.params.amr_image[i, j] = self.params.image[i,j]
        return


    def write_image(self):
        """
        write the value in the output image for a leaf
        cell that isn't at the max level
        """

        i = self.i
        j = self.j

        w = self.get_cell_integer_width()

        val = np.mean(self.params.image[i:i+w, j:j+w])
        self.params.amr_image[i:i+w, j:j+w] = val

        return



    def refine(self):
        
        if self.level == self.params.levelmax:
            self.draw()
            self.write_image_maxlevel_leaf()
            self.inc_leafcount()
            self.inc_maxdepthcount()
            return 

        if self.do_refine():
            # keep refining
            cw = self.get_cell_integer_width()
            cwhalf = cw // 2
            if cwhalf < 1:
                raise ValueError("Something's fucky")

            i = self.i
            j = self.j
            par = self.params
            child1 = cell(i, j, par)
            child2 = cell(i, j+cwhalf, par)
            child3 = cell(i+cwhalf, j, par)
            child4 = cell(i+cwhalf, j+cwhalf, par)

            global max_level_reached
            max_level_reached = max(max_level_reached, self.level + 1)

            for child in [child1, child2, child3, child4]:
                self.children.append(child)
                child.parent = self
                child.level = self.level + 1
                child.refine()

        else:
            self.draw()
            self.write_image()
            self.inc_leafcount()
            return



