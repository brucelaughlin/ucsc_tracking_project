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
grid_file_in = 'wc15n_grd.nc'
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
islands_dir = 'modify_islands/'
continent_dir = 'continent/'
input_dir_islands = box_dir + islands_dir + 'z_output/'
input_dir_continent = box_dir + continent_dir + 'z_output/'

points_dir = base_path + 'practice/bounding_boxes/determine_initial_points/'
points_in_boxes_file_in_continent = points_dir + 'z_output/' +'points_in_boxes_lon_lat_continent.p'
points_in_boxes_file_in_islands = points_dir + 'z_output/' + 'points_in_boxes_lon_lat_islands.p'

#---------------------------------------------------------------------
#---------------------------------------------------------------------

# Load the points

file = open(points_in_boxes_file_in_continent,'rb')
points_in_boxes_continent = pickle.load(file)
file.close

file = open(points_in_boxes_file_in_islands,'rb')
points_in_boxes_islands = pickle.load(file)
file.close

fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")



#---------------------------------------------------------------------
# Continent

bounding_boxes_file_in = input_dir_continent + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(points_type_line)

# Load the boxes
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close

box_dex = 0 
for box in boxes_lonlat:
    if box is not None:
        ax.plot(box[0],box[1],c = 'white',linewidth=0.6)

        #if box_dex % 2 == 0:
        #    marker_point = '.' 
        #else:
        #    marker_point = 'x' 

        marker_point = '.' 
        ax.scatter(points_in_boxes_continent[box_dex][0,:],points_in_boxes_continent[box_dex][1,:], marker = marker_point)
            
        box_dex += 1



#---------------------------------------------------------------------
# Islands

num_islands = 8
num_last_blob_island = 4

box_dex = 0

for island_dex in range(num_last_blob_island,num_islands+1):
#for island_dex in range(num_last_blob_island,num_last_blob_island+1):

    bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15n_island_number_{}.p'.format(island_dex)

    # Load the boxes
    file = open(bounding_boxes_file_in,'rb')
    boxes_lonlat = pickle.load(file)
    file.close

    for box in boxes_lonlat:
        if box is not None:
           ax.plot(box[0],box[1],c = 'white',linewidth=0.6)
    
        marker_point = '.' 
            
        #if box_dex_offshore % 2 == 0:
        #    marker_point = '.' 
        #else:
        #    marker_point = 'x' 
        
        ax.scatter(points_in_boxes_islands[box_dex][0,:],points_in_boxes_islands[box_dex][1,:], marker = marker_point)
        box_dex += 1
                



plot_title = '300km^2 coastal boxes\n10km offshore distance as outer wall'
plt.title(plot_title)

ax.axis('image')
plt.show()











