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
grid_file_in = 'wc15_grd_only_islands.nc'
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



pretty_h_background = np.multiply(mask,h)

fig, ax = plt.subplots()
#ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")
#ax.pcolormesh(lon_field,lat_field,pretty_h_background,shading="nearest")
ax.pcolormesh(lon_field,lat_field,h,shading="nearest")



# Continent

bounding_boxes_file_in = input_dir_continent + 'bounding_boxes_lonlat_coords_{}_coastline_wc15_continental.p'.format(points_type_line)

# Load the boxes
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close

for box in boxes_lonlat:
    if box is not None:
       ax.plot(box[0],box[1])




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
               ax.plot(box[0],box[1])


plot_title = '300km^2 coastal boxes\n10km offshore distance as outer wall'
plt.title(plot_title)

ax.axis('image')
plt.show()











