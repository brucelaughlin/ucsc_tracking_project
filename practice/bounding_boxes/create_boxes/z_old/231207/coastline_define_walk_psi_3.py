# walking the psi_mask grid, starting in lower right corner, assuming we start on land
# point, assuming the prevoius point was blow, and checking in a
# clockwise manner

# It's becoming embarrassing to see all these "psi" scripts... shouldn't things be "general",
# and what in here should exist as a function?

import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt



#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
grid_file_in = 'wc15_grd_no_islands.nc'
coastline_file_out = 'coastline_coords_psi_file_wc15_continent.p'
#---------------------------------------------------------------------
#---------------------------------------------------------------------





base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_path_in = base_path + grid_directory + grid_file_in

dset = netCDF4.Dataset(grid_path_in, 'r')
psi_mask = dset['mask_psi']
#rho_lon_grid = dset['lon_rho']
#rho_lat_grid = dset['lat_rho']
dset.close

psi = np.array(psi_mask)
#lon = np.array(rho_lon_grid)
#lat = np.array(rho_lat_grid)

# size of domains i and j
n_i = np.shape(psi)[0]
n_j = np.shape(psi)[1]

# begin algorithm...

coast_coordinates = []

# Start in lower right of grid (for wc12, this is land near scb)
# This assumes we start on land.  need to adjust if that's not the case
initial_dim_iterate = 1 #adjust j till we hit the coast
ii = 0
jj = n_j - 1
current_psi = psi[ii,jj]
while current_psi == 0:
    jj -= 1;
    current_psi = psi[ii,jj]
 
jj = jj + 1    
 
# current point = "cp"
cp = [ii,jj]



# Make fake last_point, which is below current_point (not in grid)
# Last point = "lp"
#lp = [cp[0]-1,cp[1]]
lp = [cp[0],cp[1]+1]

coast_coordinates.append(cp)

p = 1

# Remember: we're walking with the coastline to our left.  


# Issues: 
# 1) This is not general.  Firstly, the above work determines an initial point,
# but assumes that we are on the west coast of CA somewhere.
# 2) Also not general because we don't handle going above the grid
# correctly.  So we just assume that as soon as we hit the last row
# (ie the top of the grid), the coast ends

# 3) I'm doing this inefficiently: I'm saving a list of lists.  So I'm going to modify
# this so that I just save a single nx2 array, but even then, it would save memory
# to not create the original list of lists to begin with...

dex = 0
while True:
    
    dex += 1
  
    # problem dex = 155
    
    #if dex == 155:
    #    print("left")
    #    print(psi[ii-1,jj])
    #    print(psi[ii,jj-1])
    #    print(psi[ii+1,jj])
    #    print(psi[ii,jj+1])


    # cp left of lp
    if cp[1] < lp[1]:
        try:
            # look down
            if psi[ii-1,jj] != 1 and 0 <= ii-1 < n_i:
                ii -= 1
            # look left
            elif psi[ii,jj-1] != 1 and 0 <= jj-1 < n_j:
                jj -= 1
            # look up
            elif psi[ii+1,jj] != 1 and 0 <= ii+1 < n_i:
                ii += 1
            # look right
            elif psi[ii,jj+1] != 1 and 0 <= jj+1 < n_j:
                jj += 1
            else:
                #print(dex)
                break
        except:
            break


    # cp above lp
    elif cp[0] > lp[0]:
        try:
            # look left
            if psi[ii,jj-1] != 1 and 0 <= jj-1 < n_j:
                jj -= 1
            # look up
            elif psi[ii+1,jj] != 1 and 0 <= ii+1 < n_i:
                ii += 1
            # look right
            elif psi[ii,jj+1] != 1 and 0 <= jj+1 < n_j:
                jj += 1
            # look down
            elif psi[ii-1,jj] != 1 and 0 <= ii-1 < n_i:
                ii -= 1
            else:
                #print(dex)
                break

        except:
            break

    # cp right of lp
    elif cp[1] > lp[1]:
        try:
            # look up
            if psi[ii+1,jj] != 1 and 0 <= ii+1 < n_i:
                ii += 1
            # look right
            elif psi[ii,jj+1] != 1 and 0 <= jj+1 < n_j:
                jj += 1
            # look down
            elif psi[ii-1,jj] != 1 and 0 <= ii-1 < n_i:
                ii -= 1
            # look left
            elif psi[ii,jj-1] != 1 and 0 <= jj-1 < n_j:
                jj -= 1
            else:
                #print(dex)
                break
        except:
            break

    # cp below lp
    elif cp[0] < lp[0]:
        try:
            # look right
            if psi[ii,jj+1] != 1 and 0 <= jj+1 < n_j:
                jj += 1
            # look down
            elif psi[ii-1,jj] != 1 and 0 <= ii-1 < n_i:
                ii -= 1
            # look left
            elif psi[ii,jj-1] != 1 and 0 <= jj-1 < n_j:
                jj -= 1
            # look up
            elif psi[ii+1,jj] != 1 and 0 <= ii+1 < n_i:
                ii += 1
            else:
                #print(dex)
                break
        except:
            break


    coast_coordinates.append([ii,jj])
    lp = cp
    cp = [ii,jj]

    #print(lp)
    #print(cp)
    #print('\n')


final_coordinates = np.zeros((dex,2))
for n in range(dex):
    final_coordinates[n,0] = coast_coordinates[n][0]
    final_coordinates[n,1] = coast_coordinates[n][1]


file = open(coastline_file_out,'wb')
pickle.dump(final_coordinates,file)
file.close()







