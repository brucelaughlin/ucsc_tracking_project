# V2: I think the last point in the north coast and the first point in the south coast are the same.  For my
# new box algorithm, with fixed cross-shore locations, I think it'll be easier ot just have one coastline file.
# So, I want to remove the redundant point and then merge the north and south, to create one coastline list.

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
grid_file_in = 'wc15n_grd_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

points_type_field = 'rho'
lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])
mask = np.array(dset['mask_{}'.format(points_type_field)])

dset.close


box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'modify_islands/'
#islands_dir = 'aa_islands/'
input_dir = box_dir + islands_dir + 'z_output/'

text_file_dir = "v_point_text_files/"

#---------------------------------------------------------------------
#---------------------------------------------------------------------

# load artifical bounding endpoint coordinates
file = open(box_dir + islands_dir + text_file_dir + 'island_coastline_bounding_points_V2.txt','r')
#file = open(box_dir + islands_dir + 'island_coastline_bounding_points_V2.txt','r')
bounding_point_list = file.read().splitlines()
file.close()
bounding_point_list = [ast.literal_eval(el) for el in bounding_point_list]



fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")

num_islands = 8

num_last_blob_island = 4

island_dex = 0

for island_dex in range(num_last_blob_island,num_islands+1):   
#for island_dex in range(num_last_blob_island,num_last_blob_island+1):   


    if island_dex == num_last_blob_island:

        coastline_inshore_file_in = input_dir + 'coastline_coords_wc15n_island_1_through_4_combined_north.p'
        coastline_offshore_file_in = input_dir + 'coastline_coords_wc15n_island_1_through_4_combined_south.p'
        #coastline_inshore_file_in = input_dir + 'coastline_coords_wc15_island_1_through_4_combined_inshore.p'
        #coastline_offshore_file_in = input_dir + 'coastline_coords_wc15_island_1_through_4_combined_offshore.p'
        
        isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15n_island_1_through_4_blob_rotated.p'
        #isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15n_island_1_through_4_blob.p'

        # Load the coastlines
        file = open(coastline_inshore_file_in,'rb')
        coastline_lonlat_1 = pickle.load(file)
        file.close
        file = open(coastline_offshore_file_in,'rb')
        coastline_lonlat_2 = pickle.load(file)
        file.close
        coastline = np.append(coastline_lonlat_1,coastline_lonlat_2[1:,:],axis=0)
        #coastline = np.append(coastline_lonlat_1,coastline_lonlat_2,axis=0)
        #coastline = np.append(coastline_lonlat_1[0],coastline_lonlat_2[0],axis=0)

    else:
        coastline_file_in = input_dir + 'coastline_coords_wc15n_island_number_{}.p'.format(island_dex)
        isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15n_island_number_{}_rotated.p'.format(island_dex)
        #isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15n_island_number_{}.p'.format(island_dex)

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

    ax.scatter(coastline[bounding_point_list[island_dex-num_last_blob_island][0],0],coastline[bounding_point_list[island_dex-num_last_blob_island][0],1],c='red')
    ax.scatter(coastline[bounding_point_list[island_dex-num_last_blob_island][1],0],coastline[bounding_point_list[island_dex-num_last_blob_island][1],1],c='red')


    for ii in range(np.shape(coastline)[0]):
        ax.annotate(ii, xy = [coastline[ii,0],coastline[ii,1]], color='white', ha="center", va="center", fontsize=15, weight="bold")
    for ii in range(np.shape(isoline)[0]):
        ax.annotate(ii, xy = [isoline[ii,0],isoline[ii,1]], color='white', ha="center", va="center", fontsize=15, weight="bold")



    #ax.axis('image')
    #plt.show()
ax.axis('image')
plt.show()









