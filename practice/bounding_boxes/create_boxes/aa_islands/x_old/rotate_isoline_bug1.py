# After plotting the isoline with its corresponding "boundary points", I think that it will be easiest
# to proceed if I rotate the isoline until its first entry lines up with the first boundary point.

# BUG!  The original isoline had the starting point tacked onto the end, so it was a closed curve.
# But this was an artificial imposition; I need to un-do it before rotating, and then do the same
# tacking on for the rotated isoline!!!


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

isoline_bp_text_file = 'island_isoline_bounding_points_rotated.txt'
isoline_bp_text_path = box_dir + islands_dir + isoline_bp_text_file

#---------------------------------------------------------------------
#---------------------------------------------------------------------


# load artifical bounding endpoint coordinates
file = open(box_dir + islands_dir + 'island_isoline_bounding_points.txt','r')
isoline_bp_list = file.read().splitlines()
file.close()
isoline_bp_list = [ast.literal_eval(el) for el in isoline_bp_list]



#fig, ax = plt.subplots()
#ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")

num_islands = 8

num_last_blob_island = 4

island_dex = 0

for island_dex in range(num_last_blob_island,num_islands+1):   
#for island_dex in range(num_last_blob_island,num_last_blob_island+1):   




    if island_dex == num_last_blob_island:
        isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15_island_1_through_4_blob.p'
        output_file = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15_island_1_through_4_blob_rotated.p'
    else:
        isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15_island_number_{}.p'.format(island_dex)
        output_file = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15_island_number_{}_rotated.p'.format(island_dex)

    # Load the isolines
    file = open(isoline_file_in,'rb')
    isoline = pickle.load(file)
    file.close

    isoline_lon = list(isoline[:,0])    
    isoline_lat = list(isoline[:,1])    
    
    isoline_dex = 0    

    while(isoline_dex != isoline_bp_list[island_dex-num_last_blob_island][0]):
        temp_lon = isoline_lon[0]
        temp_lat = isoline_lat[0]
        isoline_lon.pop(0)
        isoline_lat.pop(0)
        isoline_lon.extend([temp_lon])
        isoline_lat.extend([temp_lat])
        isoline_dex += 1

    isoline = np.column_stack([isoline_lon,isoline_lat])


    isoline_bounding_indices = [0,isoline_bp_list[island_dex-num_last_blob_island][1]-isoline_dex]


    # ----------------
    # I had been storing negative values... that gets messy later.  So perhaps I can just make them positive, as follows:
    if isoline_bounding_indices[1] < 0:
        isoline_bounding_indices[1] = isoline_bounding_indices[1] = len(isoline_lon) +  isoline_bounding_indices[1]
    # ----------------

    with open(isoline_bp_text_path, 'a') as out_file:
        out_file.write(str(isoline_bounding_indices)+'\n')


    file = open(output_file,'wb')
    pickle.dump(isoline,file)
    file.close()


    #ax.plot(isoline[:,0],isoline[:,1])
    
    #ax.scatter(isoline[isoline_bp_list[island_dex-num_last_blob_island][0],0],isoline[isoline_bp_list[island_dex-num_last_blob_island][0],1],c='red')
    #ax.scatter(isoline[isoline_bp_list[island_dex-num_last_blob_island][1],0],isoline[isoline_bp_list[island_dex-num_last_blob_island][1],1],c='red')
    
    #ax.scatter(isoline[0,0],isoline[0,1],c='green')

    #ax.axis('image')
    #plt.show()









