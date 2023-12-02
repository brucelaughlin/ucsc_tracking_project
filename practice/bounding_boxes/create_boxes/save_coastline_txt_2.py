
import pickle
import numpy as np


#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
coastline_file_ij_in = 'coastline_coords_rho_file_wc15_continent.p'

coastline_i_out ='coast_coords_rho_wc15_continent_i.txt' 
coastline_j_out ='coast_coords_rho_wc15_continent_j.txt' 
#---------------------------------------------------------------------
#---------------------------------------------------------------------



file = open(coastline_file_ij_in,'rb')
coast_coords = pickle.load(file)
file.close

num_points = np.shape(coast_coords)[0]

coast_j_list = []
coast_i_list = []

for ii in range(num_points):
    coast_i_list.append(coast_coords[ii][0])
    coast_j_list.append(coast_coords[ii][1])

with open(coastline_i_out, 'w') as f:
    for coord in coast_i_list:
        f.write(f"{coord}\n")

with open(coastline_j_out, 'w') as f:
    for coord in coast_j_list:
        f.write(f"{coord}\n")






#f = open('coast_coords_psi_txt.txt','w')
#f.write(repr(coord_list))

#f = open('coast_coords_psi_j.txt','w')
#f.write(str(coast_j_list))
#f.close()
#f = open('coast_coords_psi_i.txt','w')
#f.write(str(coast_i_list))
#f.close()
