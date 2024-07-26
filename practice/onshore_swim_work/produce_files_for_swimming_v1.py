# Combine the "test" and "nn_test" code to create one pickle file to be loaded and used by the model

import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from skimage import measure
import scipy.interpolate as spint


base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc15n_grd_continent.nc'
grid_path_in = base_path + grid_directory + grid_file_in

swim_data_output_file_dir = 'practice/onshore_swim_work/'
swim_data_output_file_pre = 'swim_data.p'
swim_data_output_file = base_path + swim_data_output_file_dir + swim_data_output_file_pre

points_type_field = 'rho'

dset = netCDF4.Dataset(grid_path_in, 'r')

mask_rho = np.array(dset['mask_rho'])
lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])

dset.close

# Start with continent, then modify with islands
continent_directory = 'practice/bounding_boxes/create_boxes/continent/'
output_dir = base_path + continent_directory + 'z_output/'
dist_field_file = output_dir + 'dist_2_coast_field_rho_coastline_wc15n_continent.mat'
output_file = output_dir + 'isodistance_lonlat_coords_rho_coastline_wc15n_continent.p'

# Create the "dist field" from the continent distances, then modify with the island dist fields
dist_field = scipy.io.loadmat(dist_field_file)
dist_field = dist_field['dist_field']


# Now for the islands
box_dir_general = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir_pre = 'modify_islands/'
islands_dir = box_dir_general + islands_dir_pre
output_dir = islands_dir + 'z_output/'

num_islands = 8

for island_dex in range(1,num_islands+1):

    output_file = output_dir + 'isodistance_lonlat_coords_rho_coastline_wc15n_island_number_{}.p'.format(island_dex)

    dist_field_file = output_dir + 'dist_2_coast_field_rho_coastline_wc15n_island_number_{}.mat'.format(island_dex)
    dist_field_island = scipy.io.loadmat(dist_field_file)
    dist_field_island = dist_field_island['dist_field']
    
    # Store the minimum distance to land
    dist_field = np.minimum(dist_field,dist_field_island)


# Calculate the gradient
dx,dy = np.gradient(dist_field)

r,c = np.shape(dist_field)

X,Y = np.mgrid[0:r:1,0:c:1]

norms = np.sqrt(np.square(dx) + np.square(dy))

dirx = np.divide(dx,norms)
diry = np.divide(dy,norms)

dirx = dirx *-1
diry = diry *-1



# ---------------------------------------
# Now for the update mask, and coordinate array


r,c = np.shape(mask_rho)

rm1 = r-1
cm1 = c-1

# Make a new mask with a "buffer region" one cell wide along all coasts
mask = mask_rho.copy()
mask = mask.astype('int')
# invert the 0's and 1's
mask = np.where((mask==0)|(mask==1),mask^1,mask)

buff_west = np.zeros(np.shape(mask))
buff_west[:,0:rm1] = mask[:,1:r]

buff_east = np.zeros(np.shape(mask))
buff_east[:,1:r] = mask[:,0:rm1]

buff_south = np.zeros(np.shape(mask))
buff_south[1:c,:] = mask[0:cm1,:]

buff_north = np.zeros(np.shape(mask))
buff_north[0:cm1,:] = mask[1:c,:]

mask = mask + buff_west + buff_east + buff_south + buff_north

mask = np.divide(mask,mask,out=np.zeros_like(mask),where=mask!=0)

# invert the 0's and 1's (back again)
mask = mask.astype('int')
mask = np.where((mask==0)|(mask==1),mask^1,mask)

mask_flat = mask.flatten()
#mask_flat = mask_rho.flatten()
lon_flat = lon_field.flatten()
lat_flat = lat_field.flatten()

coord_array = np.vstack([lon_flat,lat_flat])
coord_array = coord_array.T

#plt.pcolormesh(lon_field,lat_field,mask)
#plt.pcolormesh(lon_field,lat_field,dist_field.T,vmin=0,vmax=200)
#plt.quiver(lon_field,lat_field,dirx.T,diry.T, color='r',scale=80)

#plt.colorbar()


#plt.show()

dirx = dirx.flatten()
diry = diry.flatten()

file = open(swim_data_output_file,'wb')
pickle.dump([mask_flat,coord_array,dirx,diry],file)
file.close()



