
import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from skimage import measure
#from geopy import distance
#from scipy import interpolate
import scipy.interpolate as spint


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
islands_dir = 'aa_islands/'
input_dir = box_dir + islands_dir + 'z_output/'

#---------------------------------------------------------------------
#---------------------------------------------------------------------


fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")



num_islands = 8

#num_island = 6

for island_dex in range(1,num_islands+1):   
#for island_dex in range(num_island,num_island+1):   

    coastline_file_in = input_dir + 'coastline_coords_wc15n_island_number_{}.p'.format(island_dex)


    # Load the coastlines
    file = open(coastline_file_in,'rb')
    coastlines_lonlat = pickle.load(file)
    file.close


    for coastline in coastlines_lonlat:
        if coastline is not None:
            #ax.plot(box[1],box[0])
            ax.plot(coastline[:,0],coastline[:,1])

#    ax.axis('image')
#    plt.show()


ax.axis('image')
plt.show()







