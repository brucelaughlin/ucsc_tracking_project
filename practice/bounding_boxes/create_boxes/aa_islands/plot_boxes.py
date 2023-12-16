
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

input_file_dir = 'z_output/'

base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc15_grd_no_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

points_type_line = 'psi'
points_type_field = 'rho'


#isoline_coord_file_in = input_file_dir + 'isodistance_ij_coords_{}_coastline_wc15_no_islands.p'.format(points_type_line)
bounding_boxes_file_in = input_file_dir + 'bounding_boxes_lonlat_coords_{}_coastline_wc15_continental.p'.format(points_type_line)
#coastline_coords_file_in = input_file_dir + 'coastline_coords_{}_file_wc15_continent.p'.format(points_type_line)
dist_field_file_in = input_file_dir + 'dist_2_coast_field_{}_coastline_wc15_no_islands.mat'.format(points_type_field)
mask = np.array(dset['mask_{}'.format(points_type_field)])
lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])
lon_line = np.array(dset['lon_{}'.format(points_type_line)])
lat_line = np.array(dset['lat_{}'.format(points_type_line)])


dset.close
#---------------------------------------------------------------------
#---------------------------------------------------------------------

# Load the "distance field" - plot over this
dist_field = scipy.io.loadmat(dist_field_file_in)
dist_field = dist_field['dist_field']


# Load the boxes
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close

fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")

for box in boxes_lonlat:
    if box is not None:
       #ax.plot(box[1],box[0])
       ax.plot(box[0],box[1])

ax.axis('image')
plt.show()









