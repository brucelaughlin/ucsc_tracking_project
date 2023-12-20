
import pickle
import numpy as np


#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

output_dir = 'z_output/'

point_type = 'psi'

num_islands = 8

for island_dex in range(1,num_islands+1):

    coastline_lon_out = output_dir + 'coast_coords_wc15_lon_island_number_{}.txt'.format(island_dex) 
    coastline_lat_out = output_dir + 'coast_coords_wc15_lat_island_number_{}.txt'.format(island_dex)
    coastline_file_in = output_dir + 'coastline_coords_wc15_island_number_{}.p'.format(island_dex)
    
    file = open(coastline_file_in,'rb')
    coast_coords = pickle.load(file)
    file.close

    coast_coords = coast_coords[0]

    num_points = np.shape(coast_coords)[0]

    coast_lon_list = list(coast_coords[:,0])
    coast_lat_list = list(coast_coords[:,1])

    with open(coastline_lon_out, 'w') as f:
        for coord in coast_lon_list:
            f.write(f"{coord}\n")

    with open(coastline_lat_out, 'w') as f:
        for coord in coast_lat_list:
            f.write(f"{coord}\n")



