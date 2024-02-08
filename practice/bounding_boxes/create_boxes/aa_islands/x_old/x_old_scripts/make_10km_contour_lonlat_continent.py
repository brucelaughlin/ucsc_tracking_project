
import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from skimage import measure
#from geopy import distance
#from scipy import interpolate
import scipy.interpolate as spint


#---------------------------------------------------------------------
#---------------------------------------------------------------------
#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

output_dir = 'z_output/'

dist_field_file = 'dist_2_coast_field_rho_coastline_wc15_no_islands.mat'

#output_file = 'isodistance_ij_coords_rho_coastline_wc15_no_islands.p'
output_file = output_dir + 'isodistance_lonlat_coords_rho_coastline_wc15_no_islands.p'


base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc15_grd_no_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

points_type_field = 'rho'

lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])

dset.close



#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------



dist_field = scipy.io.loadmat(dist_field_file)
dist_field = dist_field['dist_field']



RGI = spint.RegularGridInterpolator
# create interpolator to get lat/lon at isoline points
x = np.arange(np.shape(lon_field)[0])
y = np.arange(np.shape(lon_field)[1])
rgi_lon = RGI([x,y],lon_field)
rgi_lat = RGI([x,y],lat_field)


# dist_2_coast returned values in km
# So we set "10" as our countour value

distance_from_coast = 10
contours = measure.find_contours(np.transpose(dist_field), distance_from_coast)


# Assume that the longest contour returned is the one we want....
max_length = 0 
contour_index = 0 
dex = 0 
for contour in contours:
    if np.shape(contour)[0] > max_length:
        max_length = np.shape(contour)[0]
        contour_index = dex 
    dex += 1

isoline_ij = contours[contour_index]

isoline_lonlat = np.zeros(np.shape(isoline_ij))
for ii in range(np.shape(isoline_ij)[0]):
    isoline_lonlat[ii,0] = rgi_lon((isoline_ij[ii,0], isoline_ij[ii,1]))
    isoline_lonlat[ii,1] = rgi_lat((isoline_ij[ii,0], isoline_ij[ii,1]))


file = open(output_file,'wb')
pickle.dump(isoline_lonlat,file)
file.close()










