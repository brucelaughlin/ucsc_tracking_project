# lat/lon area calc taken from:
# https://stackoverflow.com/questions/68118907/shapely-pyproj-find-area-in-m2-of-a-polygon-created-from-latitude-and-longi

# V2: For blob islands, no longer doing the threshold method.  Cross-shore walls re pre-determined, by "islands_blob_fixed_wall_coords_V2.txt".
# May want to do the same thing for all islands!
# ALSO:  Trying new method, where there aren't "inshore" and "offshore" boxes anymore


# Using the island coastlines, including the "blob" of islands 1-4, along with the rotated isolines (ie starting points of isolines
# correspond with starting points of coastlines).
# Idea: split each island into two halves, an upper and lower, using the "bounding points" previously determined.  Then proceed
# as if doing the box calculations for two separate coastlines and isolines


# NOTE: I stored the 2nd isoline bounding point as a negative number.  So address that accordingly.  


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
grid_file_in = 'wc15n_grd.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

points_type_field = 'rho'
lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])
mask = np.array(dset['mask_{}'.format(points_type_field)])

dset.close


box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'modify_islands/'
input_dir = box_dir + islands_dir + 'z_output/'
text_file_dir = box_dir + islands_dir + "v_point_text_files/"


fixed_wall_blob_file_pre = "islands_blob_fixed_wall_coords_V2.txt"
fixed_wall_blob_file = text_file_dir + fixed_wall_blob_file_pre


wall_bp_file_list = []

wall_bp_list_file_blob_pre = "islands_fixed_wall_coords_blob_V2.txt"
wall_bp_file_list.append(text_file_dir + wall_bp_list_file_blob_pre)

wall_bp_list_template = "islands_fixed_wall_coords_island_{}.txt"
for ii in range(5,9):
    wall_bp_file_list.append(text_file_dir + wall_bp_list_template.format(ii))





# load coastline artifical bounding endpoint coordinates
file = open(text_file_dir + 'island_coastline_bounding_points_V2.txt','r')
coastline_bp_list = file.read().splitlines()
file.close()
coastline_bp_list = [ast.literal_eval(el) for el in coastline_bp_list]

# load isoline artifical bounding endpoint coordinates
file = open(text_file_dir + 'island_isoline_bounding_points_rotated_V2.txt','r')
isoline_bp_list = file.read().splitlines()
file.close()
isoline_bp_list = [ast.literal_eval(el) for el in isoline_bp_list]



num_islands = 8

num_last_blob_island = 4

bp_file_dex = 0

for island_dex in range(num_last_blob_island,num_islands+1):
#for island_dex in range(num_last_blob_island,num_last_blob_island+1):
#for island_dex in range(6,7):

    print('\n')
    print('\n')
    print('island number: {}'.format(island_dex))
    print('\n')
    print('\n')

    # Load coastline and isoline coordinates
    if island_dex == num_last_blob_island:

        coastline_inshore_file_in = input_dir + 'coastline_coords_wc15n_island_1_through_4_combined_north.p'
        coastline_offshore_file_in = input_dir + 'coastline_coords_wc15n_island_1_through_4_combined_south.p'
        #coastline_inshore_file_in = input_dir + 'coastline_coords_wc15n_island_1_through_4_combined_inshore.p'
        #coastline_offshore_file_in = input_dir + 'coastline_coords_wc15n_island_1_through_4_combined_offshore.p'
        #isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15n_island_1_through_4_blob.p'
        isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15n_island_1_through_4_blob_rotated.p'

        # Load the coastlines
        file = open(coastline_inshore_file_in,'rb')
        coastline_lonlat_1 = pickle.load(file)
        file.close
        file = open(coastline_offshore_file_in,'rb')
        coastline_lonlat_2 = pickle.load(file)
        file.close
        coastline_lonlat = np.append(coastline_lonlat_1,coastline_lonlat_2[1:,:],axis=0)
        #coastline_lonlat = np.append(coastline_lonlat_1,coastline_lonlat_2,axis=0)

    else:
        coastline_file_in = input_dir + 'coastline_coords_wc15n_island_number_{}.p'.format(island_dex)
        isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15n_island_number_{}_rotated.p'.format(island_dex)

        # Load the coastlines
        file = open(coastline_file_in,'rb')
        coastline_lonlat = pickle.load(file)
        file.close
        coastline_lonlat = coastline_lonlat[0]

    # Load the isolines
    file = open(isoline_file_in,'rb')
    isoline_lonlat = pickle.load(file)
    file.close


    bounding_boxes_file_out = input_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}.p'.format(island_dex)
    #bounding_boxes_file_out = input_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_offshore.p'.format(island_dex)

    coast_lon = list(coastline_lonlat[:,0])
    coast_lat = list(coastline_lonlat[:,1])
    isoline_lon = list(isoline_lonlat[:,0])
    isoline_lat = list(isoline_lonlat[:,1])
    
    num_points_coast = len(coast_lon)
    num_points_isoline = len(isoline_lon)

    bounding_boxes_lonlat = []


    # crosshore wall indices
    wall_bp_file = wall_bp_file_list[bp_file_dex]
    file = open(wall_bp_file,'r')
    wall_bp_list = file.read().splitlines()
    file.close()
    wall_bp_list = [ast.literal_eval(el) for el in wall_bp_list]

    bp_file_dex += 1


    for ii in range(len(wall_bp_list)-1):
    #for ii in range(len(wall_bp_list)):

        polygon_lon = []
        polygon_lat = []
        
        polygon_lon += coast_lon[wall_bp_list[ii][0]:wall_bp_list[ii+1][0]+1]
        polygon_lat += coast_lat[wall_bp_list[ii][0]:wall_bp_list[ii+1][0]+1]
        polygon_lon += list(reversed(isoline_lon[wall_bp_list[ii][1]:wall_bp_list[ii+1][1]+1]))
        polygon_lat += list(reversed(isoline_lat[wall_bp_list[ii][1]:wall_bp_list[ii+1][1]+1]))
        #polygon_lon += list(reversed(isoline_lon[wall_bp_list[ii][1]:wall_bp_list[ii+1][1]]))
        #polygon_lat += list(reversed(isoline_lat[wall_bp_list[ii][1]:wall_bp_list[ii+1][1]]))
        polygon_lon += [coast_lon[wall_bp_list[ii][0]]]
        polygon_lat += [coast_lat[wall_bp_list[ii][0]]]
        

        bounding_boxes_lonlat.append(np.array([polygon_lon,polygon_lat]))


    print('island number: {}'.format(island_dex))
    print('\n')


    file = open(bounding_boxes_file_out,'wb')
    pickle.dump(bounding_boxes_lonlat,file)
    file.close()





