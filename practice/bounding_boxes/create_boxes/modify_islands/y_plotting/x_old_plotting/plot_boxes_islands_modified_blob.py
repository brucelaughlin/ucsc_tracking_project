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
lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])
mask = np.array(dset['mask_{}'.format(points_type_field)])

dset.close


box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'aa_islands/'
input_dir = box_dir + islands_dir + 'z_output/'


# Set box area threshold (should be 300km, right?)
box_area_threshold = 3e7
#---------------------------------------------------------------------
#---------------------------------------------------------------------

# For calculating area
geod = Geod(ellps="WGS84")


# load coastline artifical bounding endpoint coordinates
file = open(box_dir + islands_dir + 'island_coastline_bounding_points.txt','r')
coastline_bp_list = file.read().splitlines()
file.close()
coastline_bp_list = [ast.literal_eval(el) for el in coastline_bp_list]

# load isoline artifical bounding endpoint coordinates
file = open(box_dir + islands_dir + 'island_isoline_bounding_points_rotated.txt','r')
isoline_bp_list = file.read().splitlines()
file.close()
isoline_bp_list = [ast.literal_eval(el) for el in isoline_bp_list]



num_islands = 8

num_last_blob_island = 4


fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")



for island_dex in range(num_last_blob_island,num_islands+1):
#for island_dex in range(num_last_blob_island,num_last_blob_island+1):



    # Set an index for the bounding point lists (the lists of points used to split the coastlines and isolines)
    bp_dex = island_dex-num_last_blob_island

    for inoffshore_switch in range(0,2):
    

        if inoffshore_switch == 0:
            bounding_boxes_file_in = input_dir + 'bounding_boxes_lonlat_wc15_island_number_{}_inshore.p'.format(island_dex)
        else:
            bounding_boxes_file_in = input_dir + 'bounding_boxes_lonlat_wc15_island_number_{}_offshore.p'.format(island_dex)


        # Load the boxes
        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)
        file.close

        for box in boxes_lonlat:
            if box is not None:
               ax.plot(box[0],box[1])




ax.axis('image')
plt.show()











