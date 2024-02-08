
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

land_type = 'continent'
#land_type = 'islands'

base_path = '/home/blaughli/tracking_project/'

grid_directory = 'grid_data/'
grid_file_in = 'wc15n_grd.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

points_type_field = 'rho'
lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])
mask = np.array(dset['mask_{}'.format(points_type_field)])


dset.close

box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'aa_islands/'
continent_dir = 'continent/'
input_file_dir = 'z_output/'

if land_type == 'continent':
    coastline_coords_file_in = box_dir + continent_dir + input_file_dir + 'coastline_coords_psi_file_wc15n_{}.p'.format(land_type)
else:
    coastline_coords_file_in = box_dir + islands_dir + input_file_dir + 'coastline_coords_psi_file_wc15n_{}.p'.format(land_type)

#---------------------------------------------------------------------
#---------------------------------------------------------------------

# Load the coastlines
file = open(coastline_coords_file_in,'rb')
coastlines_lonlat = pickle.load(file)
file.close

fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")

ax.plot(coastlines_lonlat[:,0],coastlines_lonlat[:,1])
#ax.plot(coastlines_lonlat[0:1,0],coastlines_lonlat[0:1,1])


ax.axis('image')
plt.show()









