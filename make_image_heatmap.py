#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the plotting.
import matplotlib.pyplot as plt

#...for the image manipulation.
import matplotlib.image as mpimg

#...for the MATH.
import numpy as np

# For scaling images.
import scipy.ndimage.interpolation as inter

#...for the colours.
from matplotlib import colorbar, colors

# For playing with the tick marks on the colour map axis.
from matplotlib import ticker

# Load the LaTeX text plot libraries.
from matplotlib import rc

# Uncomment to use LaTeX for the plot text.
rc('font',**{'family':'serif','serif':['Computer Modern']})
rc('text', usetex=True)

# Load in the image.

## The scan image as a NumPy array.
scan_img = mpimg.imread("scan.png")

print(" *")
print(" * Image dimensions: %s" % (str(scan_img.shape)))

## The figure upon which to display the scan image.
plot = plt.figure(101, figsize=(5.0, 5.0), dpi=150, facecolor='w', edgecolor='w')

# Adjust the position of the axes.
#plot.subplots_adjust(bottom=0.17, left=0.15)
plot.subplots_adjust(bottom=0.05, left=0.15, right=0.99, top=0.95)

## The plot axes.
plotax = plot.add_subplot(111)

# Set the x axis label.
plt.xlabel("$x$")

# Set the y axis label.
plt.ylabel("$y$")

# Add the original scan image to the plot.
plt.imshow(scan_img)

## The blob centre x values [pixels].
blob_xs = []

## The blob centre x values [pixels].
blob_ys = []

## The blob radii [pixels].
blob_rs = []

# Open the blob data file and retrieve the x, y, and r values.
with open("blobs.csv", "r") as f:
    for l in f.readlines():
        blob_xs.append(float(l.split(",")[0]))
        blob_ys.append(float(l.split(",")[1]))
        blob_rs.append(float(l.split(",")[2]))

## The image scale factor.
scale = 6.0

## The width of the image scaled up by the scale factor [pixels].
w = scan_img.shape[0]

## The original width of the image [pixels].
w_o = w / scale

## The height of the image scaled up by the scale factor [pixels].
h = scan_img.shape[1]

## The original height of the image [pixels].
h_o = h / scale

print(" * Image dimensions (w,h) = (%d,%d) -> (w_o,h_o) = (%d,%d)" % (w,h,w_o,h_o))

## The number of bins in each dimension of the heatmap.
#
# We are using the original image dimensions so that our heat map
# maps to the pixels in the original image. This is mainly for
# aesthetic reasons - there would be nothing to stop us using more
# (or fewer) bins.
bins = [w_o, h_o]

## The dimensions of the heat map, taken from the scaled-up image.
map_range = [[0, w], [0, h]]

# Create the heat map using NumPy's 2D histogram functionality.
centre_heatmap, x_edges, y_edges = np.histogram2d(blob_ys, blob_xs, bins=bins, range=map_range)

## The scaled heat map image.
#
# We need to scale the heat map array because although the bin widths
# are > 1, the resultant histogram (when made into an image) creates
# an image with one pixel per bin.
zoom_img = inter.zoom(centre_heatmap, (scale, scale), order=0, prefilter=False)

## The colo(u)r map for the heat map.
cmap = plt.cm.gnuplot

## The maximum number of blob centres in the heat map.
bc_max = np.amax(centre_heatmap)
#
print(" * Maximum value in the heat map is %d." % (bc_max))

## The maximum value to use in the colo(u)r map axis.
color_map_max = bc_max

# Add the (scaled) heat map (2D histogram) to the plot.
zoomed_heat_map = plt.imshow(zoom_img, alpha=0.8, cmap=cmap,norm=colors.Normalize(vmin=0,vmax=color_map_max))

## The heat map colo(u)r bar.
cb = plt.colorbar(alpha=1.0, mappable=zoomed_heat_map)

## An object to neaten up the colour map axis tick marks.
tick_locator = ticker.MaxNLocator(nbins=7)
#
cb.locator = tick_locator
#
cb.update_ticks()

# Add a grid.
plt.grid(1)

# Crop the plot limits to the limits of the scan iteself.
plotax.set_xlim([0, h])
plotax.set_ylim([w, 0])

# Save the figure.
plot.savefig("heatmap.png")

print(" *")
