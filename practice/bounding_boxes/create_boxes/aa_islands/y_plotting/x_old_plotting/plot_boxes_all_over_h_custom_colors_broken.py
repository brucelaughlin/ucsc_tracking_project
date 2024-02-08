# lat/lon area calc taken from:
# https://stackoverflow.com/questions/68118907/shapely-pyproj-find-area-in-m2-of-a-polygon-created-from-latitude-and-longi


# Using the island coastlines, including the "blob" of islands 1-4, along with the rotated isolines (ie starting points of isolines
# correspond with starting points of coastlines).
# Idea: split each island into two halves, an upper and lower, using the "bounding points" previously determined.  Then proceed
# as if doing the box calculations for two separate coastlines and isolines



import netCDF4
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.interpolate import interp1d
from geopy.distance import great_circle
import scipy.interpolate as spint
import ast

from pyproj import Geod
#from shapely.geometry import Polygon
from shapely.geometry import LineString, Point, Polygon


#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

base_path = '/home/blaughli/tracking_project/'

grid_directory = 'grid_data/'
grid_file_in = 'wc15_grd.nc.0'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

points_type_field = 'rho'
points_type_line = 'psi'
lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])
mask = np.array(dset['mask_{}'.format(points_type_field)])
h = np.array(dset['h'])

dset.close


box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'aa_islands/'
input_dir_islands = box_dir + islands_dir + 'z_output/'
input_dir_continent = box_dir + 'z_output/'

#---------------------------------------------------------------------
#---------------------------------------------------------------------


# -------------------------------------
# Custom colormap (https://stackoverflow.com/questions/49367144/modify-matplotlib-colormap)

# create colormap
# ---------------

# I don't quite understand the math going on, but I did trial and error until I hacked
# my way into something lat looks ok.

# set upper part: 4 * 256/4 entries   (like, what is going on here?)
upper = mpl.cm.jet(np.arange(256))

# set lower part: 1 * 256/4 entries  (ok, what is going on?  I changed this)
# - initialize all entries to 1 to make sure that the alpha channel (4th column) is 1
#lower = np.ones((int(256/4),4))  (the original)
#lower = np.ones((int(256/64),4))
#lower = np.ones((int(256/128),4))
lower = np.ones((int(256/256),4))
# - modify the first three columns (RGB):
#   range linearly between white (1,1,1) and the first color of the upper colormap
for i in range(3):
    #lower[:,i] = np.linspace(1, upper[0,i], lower.shape[0])
    lower[:,i] = np.linspace(0.8, upper[0,i], lower.shape[0])  #(used 0.8 as a starting point, which is gray)

# combine parts of colormap
cmap = np.vstack(( lower, upper ))

# convert to matplotlib colormap
cmap = mpl.colors.ListedColormap(cmap, name='myColorMap', N=cmap.shape[0])


# ------------------------------------




h_masked = np.multiply(mask,h)

fig, ax = plt.subplots()
#ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")
#ax.pcolormesh(lon_field,lat_field,pretty_h_background,shading="nearest")
#ax.pcolormesh(lon_field,lat_field,h,shading="nearest")
#ax.pcolormesh(lon_field,lat_field,h,shading="nearest",cmap = plt.colormaps['jet'])
#ax.pcolormesh(lon_field,lat_field,h,shading="nearest",cmap = cmap)
ax.pcolormesh(lon_field,lat_field,h_masked,shading="nearest",cmap = cmap)



# Continent

bounding_boxes_file_in = input_dir_continent + 'bounding_boxes_lonlat_coords_{}_coastline_wc15_continental.p'.format(points_type_line)

# Load the boxes
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close

for box in boxes_lonlat:
    if box is not None:
       ax.plot(box[0],box[1],c = 'white',linewidth=0.6)




# Islands

num_islands = 8
num_last_blob_island = 4


for island_dex in range(num_last_blob_island,num_islands+1):
#for island_dex in range(num_last_blob_island,num_last_blob_island+1):

    # Set an index for the bounding point lists (the lists of points used to split the coastlines and isolines)
    bp_dex = island_dex-num_last_blob_island

    for inoffshore_switch in range(0,2):
    

        if inoffshore_switch == 0:
            bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15_island_number_{}_inshore.p'.format(island_dex)
        else:
            bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15_island_number_{}_offshore.p'.format(island_dex)


        # Load the boxes
        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)
        file.close

        for box in boxes_lonlat:
            if box is not None:
               ax.plot(box[0],box[1],c = 'white',linewidth=0.6)


plot_title = '300km^2 coastal boxes\n10km offshore distance as outer wall'
plt.title(plot_title)

ax.axis('image')
plt.show()











