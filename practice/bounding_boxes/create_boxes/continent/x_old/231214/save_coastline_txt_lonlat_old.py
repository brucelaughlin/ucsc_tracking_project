
import pickle
import numpy as np


#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
point_type = 'psi'

#coastline_file_ij_in = 'coastline_coords_{}_file_wc15_continent.p'.format(point_type)
coastline_file_in = 'coastline_coords_{}_file_wc15_continent.p'.format(point_type)

#coastline_i_out ='coast_coords_{}_wc15_continent_i.txt'.format(point_type) 
#coastline_j_out ='coast_coords_{}_wc15_continent_j.txt' .format(point_type)
coastline_lon_out ='coast_coords_{}_wc15_continent_lon.txt'.format(point_type) 
coastline_lat_out ='coast_coords_{}_wc15_continent_lat.txt' .format(point_type)
#---------------------------------------------------------------------
#---------------------------------------------------------------------



#file = open(coastline_file_ij_in,'rb')
file = open(coastline_file_in,'rb')
coast_coords = pickle.load(file)
file.close

num_points = np.shape(coast_coords)[0]

#coast_j_list = []
#coast_i_list = []
coast_lon_list = []
coast_lat_list = []

for ii in range(num_points):
    #coast_i_list.append(coast_coords[ii][0])
    #coast_j_list.append(coast_coords[ii][1])
    coast_lon_list.append(coast_coords[ii][0])
    coast_lat_list.append(coast_coords[ii][1])

#with open(coastline_i_out, 'w') as f:
with open(coastline_lon_out, 'w') as f:
    #for coord in coast_i_list:
    for coord in coast_lon_list:
        f.write(f"{coord}\n")

#with open(coastline_j_out, 'w') as f:
with open(coastline_lat_out, 'w') as f:
    #for coord in coast_j_list:
    for coord in coast_lat_list:
        f.write(f"{coord}\n")



