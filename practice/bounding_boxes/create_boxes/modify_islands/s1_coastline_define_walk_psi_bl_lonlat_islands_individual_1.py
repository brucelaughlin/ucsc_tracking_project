# walking the psi_mask_bl grid
# point, assuming the prevoius point was blow, and checking in a
# clockwise manner

# Use "psi_bl", as defined by Chris!

import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import ast

#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

base_path = '/home/blaughli/tracking_project/'

box_dir_general = base_path + 'practice/bounding_boxes/create_boxes/'

islands_dir = box_dir_general + 'modify_islands/'

output_dir = islands_dir + 'z_output/'

grid_directory = 'grid_data/'
#grid_file_in = 'wc15_grd_only_islands.nc'
grid_file_in = 'wc15n_grd_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in

psi_bl_file_in = 'mask_psi_bl_islands.p'
psi_bl_path_in = output_dir + psi_bl_file_in

coast_starting_coords_file = "s0_island_coast_starting_coordinates.txt"

coastline_outFileName_template = "coastline_coords_wc15n_island_number_{}.p"


#---------------------------------------------------------------------
dset = netCDF4.Dataset(grid_path_in, 'r')

points_type_psi = 'psi'
lon_psi = np.array(dset['lon_{}'.format(points_type_psi)])
lat_psi = np.array(dset['lat_{}'.format(points_type_psi)])

mask_u = np.array(dset['mask_u'])
mask_v = np.array(dset['mask_v'])

dset.close

#---------------------------------------------------------------------
#---------------------------------------------------------------------


# Need to modify this to work for islands, ie no longer have the condition
# that the coast ends at the edge of the grid

# load psi_bl mask
file = open(psi_bl_path_in,'rb')
psi = pickle.load(file)
file.close

# load island starting coordinates
file = open(coast_starting_coords_file,'r')
#file = open('island_coast_starting_coordinates.txt','r')
starting_point_list = file.read().splitlines()
file.close()
starting_point_list = [ast.literal_eval(el) for el in starting_point_list]

# size of domains i and j
n_i = np.shape(psi)[0]
n_j = np.shape(psi)[1]

# begin algorithm...
# walk around clockwise, coast on the right, looking left first then clockwise


island_dex = 0

for starting_point in starting_point_list:
    
    coordinate_array_list = []
    island_dex += 1
    coastline_file_out = output_dir + coastline_outFileName_template.format(island_dex)
    #coastline_file_out = output_dir + 'coastline_coords_wc15n_island_number_{}.p'.format(island_dex)


    coast_lon = []
    coast_lat = []

    # If I got i/j of the grid dims backwards, switch the order of the starting coordinates
    initial_dim_iterate = 1 #adjust j till we hit the coast
    ii = starting_point[0]
    jj = starting_point[1]
    current_psi = psi[ii,jj]
    while current_psi == 0:
        jj -= 1;
        current_psi = psi[ii,jj]
     
    jj = jj + 1    
     
    # current point = "cp"
    cp = [ii,jj]



    # Make fake last_point, to the south of starting point 
    # (may be better choice, depending on where starting point is - want the
    # fake point to enforce the desired starting direction of walk/traversal)
    
    # Last point = "lp"
    lp = [cp[0]-1,cp[1]] # for islands, starting in a NW corner
    #lp = [cp[0],cp[1]+1] # for west coast continent, starting in most SW point of land mask

    coast_lon.append(lon_psi[ii,jj])
    coast_lat.append(lat_psi[ii,jj])

    dex = 0
    while True:
        
        dex += 1
      
        # cp left of lp
        if cp[1] < lp[1]:
            try:
                # look down
                if mask_u[ii,jj] != 1 and 0 <= jj-1 < n_j:
                    ii -= 1
                # look left
                elif mask_v[ii,jj] != 1 and 0 <= jj-1 < n_j:
                    jj -= 1
                # look up
                elif mask_u[ii+1,jj] != 1 and 0 <= jj-1 < n_j:
                    ii += 1
                # look right
                elif mask_v[ii,jj+1] != 1 and 0 <= jj-1 < n_j:
                    jj += 1
                else:
                    break
            except:
                break


        # cp above lp
        elif cp[0] > lp[0]:
            try:
                # look left
                if mask_v[ii,jj] != 1 and 0 <= jj-1 < n_j:
                    jj -= 1
                # look up
                elif mask_u[ii+1,jj] != 1 and 0 <= jj-1 < n_j:
                    ii += 1
                # look right
                elif mask_v[ii,jj+1] != 1 and 0 <= jj-1 < n_j:
                    jj += 1
                # look down
                elif mask_u[ii,jj] != 1 and 0 <= jj-1 < n_j:
                    ii -= 1
                else:
                    break
            except:
                break

        # cp right of lp
        elif cp[1] > lp[1]:
            try:
                # look up
                if mask_u[ii+1,jj] != 1 and 0 <= jj-1 < n_j:
                    ii += 1
                # look right
                elif mask_v[ii,jj+1] != 1 and 0 <= jj-1 < n_j:
                    jj += 1
                # look down
                elif mask_u[ii,jj] != 1 and 0 <= jj-1 < n_j:
                    ii -= 1
                # look left
                elif mask_v[ii,jj] != 1 and 0 <= jj-1 < n_j:
                    jj -= 1
                else:
                    break
            except:
                break

        # cp below lp
        elif cp[0] < lp[0]:
            try:
                # look right
                if mask_v[ii,jj+1] != 1 and 0 <= jj-1 < n_j:
                    jj += 1
                # look down
                elif mask_u[ii,jj] != 1 and 0 <= jj-1 < n_j:
                    ii -= 1
                # look left
                elif mask_v[ii,jj] != 1 and 0 <= jj-1 < n_j:
                    jj -= 1
                # look up
                elif mask_u[ii+1,jj] != 1 and 0 <= jj-1 < n_j:
                    ii += 1
                else:
                    break
            except:
                break


        coast_lon.append(lon_psi[ii,jj])
        coast_lat.append(lat_psi[ii,jj])

        # Stop the algorithm if we've looped around
        if lon_psi[ii,jj] in coast_lon[:-1]:
            if coast_lat[:-1][coast_lon[:-1].index(lon_psi[ii,jj])] == lat_psi[ii,jj]: 
                final_coordinates = np.zeros((len(coast_lon),2))
                final_coordinates[:,0] = coast_lon
                final_coordinates[:,1] = coast_lat
                coordinate_array_list.append(final_coordinates) 
                break

        lp = cp
        cp = [ii,jj]


    file = open(coastline_file_out,'wb')
    pickle.dump(coordinate_array_list,file)
    file.close()







