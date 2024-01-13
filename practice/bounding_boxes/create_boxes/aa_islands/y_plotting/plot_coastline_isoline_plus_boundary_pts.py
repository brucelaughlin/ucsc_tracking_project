
import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from skimage import measure
import scipy.interpolate as spint
import ast


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

#---------------------------------------------------------------------
#---------------------------------------------------------------------

# load artifical bounding endpoint coordinates
file = open(box_dir + islands_dir + 'island_coastline_bounding_points.txt','r')
coast_bp_list = file.read().splitlines()
file.close()
coast_bp_list = [ast.literal_eval(el) for el in coast_bp_list]

# load artifical bounding endpoint coordinates
file = open(box_dir + islands_dir + 'island_isoline_bounding_points.txt','r')
isoline_bp_list = file.read().splitlines()
file.close()
isoline_bp_list = [ast.literal_eval(el) for el in isoline_bp_list]



fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")

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
    isoline_lonlat = pickle.load(file)
    file.close

    isoline = isoline_lonlat

    ax.plot(coastline[:,0],coastline[:,1])
    ax.plot(isoline[:,0],isoline[:,1])
    ax.scatter(coastline[0,0],coastline[0,1],c='blue')

    ax.scatter(coastline[coast_bp_list[island_dex-num_last_blob_island][0],0],coastline[coast_bp_list[island_dex-num_last_blob_island][0],1],c='red')
    ax.scatter(coastline[coast_bp_list[island_dex-num_last_blob_island][1],0],coastline[coast_bp_list[island_dex-num_last_blob_island][1],1],c='red')
    
    ax.scatter(isoline[isoline_bp_list[island_dex-num_last_blob_island][0],0],isoline[isoline_bp_list[island_dex-num_last_blob_island][0],1],c='red')
    ax.scatter(isoline[isoline_bp_list[island_dex-num_last_blob_island][1],0],isoline[isoline_bp_list[island_dex-num_last_blob_island][1],1],c='red')
    
    ax.scatter(isoline[0,0],isoline[0,1],c='green')

    ax.axis('image')
    plt.show()









