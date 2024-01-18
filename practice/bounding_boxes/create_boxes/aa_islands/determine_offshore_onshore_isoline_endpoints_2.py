# Originally stored negative indices... that gets messy later


import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from skimage import measure
import scipy.interpolate as spint
import ast
from geopy.distance import great_circle

#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

#land_type = 'continent'
land_type = 'islands'

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

isoline_bp_text_file = 'island_isoline_bounding_points.txt'
isoline_bp_text_path = box_dir + islands_dir + isoline_bp_text_file

#---------------------------------------------------------------------
#---------------------------------------------------------------------

# load artifical bounding endpoint coordinates
file = open(box_dir + islands_dir + 'island_coastline_bounding_points.txt','r')
bounding_point_list = file.read().splitlines()
file.close()
bounding_point_list = [ast.literal_eval(el) for el in bounding_point_list]



#fig, ax = plt.subplots()
#ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")

num_islands = 8

num_last_blob_island = 4

island_dex = 0

for island_dex in range(num_last_blob_island,num_islands+1):   
#for island_dex in range(num_last_blob_island,num_last_blob_island+1):   


    if island_dex == num_last_blob_island:

        coastline_inshore_file_in = input_dir + 'coastline_coords_wc15_island_1_through_4_combined_inshore.p'
        coastline_offshore_file_in = input_dir + 'coastline_coords_wc15_island_1_through_4_combined_offshore.p'
        isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15_island_1_through_4_blob.p'

        # Load the coastlines
        file = open(coastline_inshore_file_in,'rb')
        coastline_lonlat_1 = pickle.load(file)
        file.close
        file = open(coastline_offshore_file_in,'rb')
        coastline_lonlat_2 = pickle.load(file)
        file.close
        #coastline = np.append(coastline_lonlat_1[0],coastline_lonlat_2[0],axis=0)
        coastline = np.append(coastline_lonlat_1,coastline_lonlat_2,axis=0)

    else:
        coastline_file_in = input_dir + 'coastline_coords_wc15_island_number_{}.p'.format(island_dex)
        isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15_island_number_{}.p'.format(island_dex)

        # Load the coastlines
        file = open(coastline_file_in,'rb')
        coastline_lonlat = pickle.load(file)
        file.close
        coastline = coastline_lonlat[0]

    # Load the isolines
    file = open(isoline_file_in,'rb')
    isoline = pickle.load(file)
    file.close


    # Need to figure out the corresponding inshore/offshore bounding points on the isolines

    # Code taken from "make_boxes_general_lonlat_1.py", modified, some comments may be weird

    # Store the bounding indices, and then write to a text file
    isoline_bounding_indices = []

       
    
    # First bounding point

    coast_bounding_point_dex = bounding_point_list[island_dex-num_last_blob_island][0]
   
 
    #isoline_dex = 0
    # see which remaining (ie not already used) isoline point is nearest
    # Set a dummy "dmax" which will be replaced after the fist iteration
    dmax = 1e1000
    closest_dex = None
    #for ii in range(isoline_dex,np.shape(isoline)[0]):
    for ii in range(np.shape(isoline)[0]):
        #dist = great_circle((coast_lat[jj],coast_lon[jj]),(isoline_lat[ii],isoline_lon[ii]))
        dist = great_circle((coastline[coast_bounding_point_dex][1],coastline[coast_bounding_point_dex][0]),(isoline[ii][1],isoline[ii][0]))
        dist = dist._Distance__kilometers
        if dist < dmax: 
            dmax = dist
            closest_dex = ii

    isoline_bounding_indices.append(closest_dex)


    # Second bounding point
    
    coast_bounding_point_dex = bounding_point_list[island_dex-num_last_blob_island][1]

    #isoline_dex = 0
    # see which remaining (ie not already used) isoline point is nearest
    # Set a dummy "dmax" which will be replaced after the fist iteration
    dmax = 1e1000
    closest_dex = None
    #for ii in range(isoline_dex,np.shape(isoline)[0]):
    for ii in range(np.shape(isoline)[0]):
        #dist = great_circle((coast_lat[jj],coast_lon[jj]),(isoline_lat[ii],isoline_lon[ii]))
        dist = great_circle((coastline[coast_bounding_point_dex][1],coastline[coast_bounding_point_dex][0]),(isoline[ii][1],isoline[ii][0]))
        dist = dist._Distance__kilometers
        if dist < dmax: 
            dmax = dist
            closest_dex = ii

    isoline_bounding_indices.append(closest_dex)

    
    with open(isoline_bp_text_path, 'a') as out_file:
        out_file.write(str(isoline_bounding_indices)+'\n') 


    #ax.plot(coastline[:,0],coastline[:,1])
    #ax.plot(isoline[:,0],isoline[:,1])
    #ax.scatter(coastline[0,0],coastline[0,1],c='blue')

    #ax.scatter(coastline[bounding_point_list[island_dex-num_last_blob_island][0],0],coastline[bounding_point_list[island_dex-num_last_blob_island][0],1],c='red')
    #ax.scatter(coastline[bounding_point_list[island_dex-num_last_blob_island][1],0],coastline[bounding_point_list[island_dex-num_last_blob_island][1],1],c='red')

    #ax.axis('image')
    #plt.show()









