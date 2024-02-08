
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

#grid_file_in = 'wc12_grd_no_islands.nc'
grid_file_in = 'wc15_grd_no_islands.nc'

#dist_field_file = 'dist_2_coast_field_wc12.mat'
#dist_field_file = 'dist_2_coast_field_wc15_no_islands.mat'
dist_field_file = 'dist_2_coast_field_rho_coastline_wc15_no_islands.mat'

#output_file = 'isodistance_ij_coords.p'
#output_file = 'isodistance_ij_coords_wc15_no_islands.p'
output_file = 'isodistance_ij_coords_rho_coastline_wc15_no_islands.p'

#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------



dist_field = scipy.io.loadmat(dist_field_file)
dist_field = dist_field['dist_field']



RGI = spint.RegularGridInterpolator



# Very confused here.  I thought dist_2_coast return meters
# but none of the results are near 10000.  However, it doesn't
# seem to be KM either, since there aren't any under 10...

distance_from_coast = 10
#contours = measure.find_contours(dist_field, distance_from_coast)
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

isodistance_ij = contours[contour_index]

file = open(output_file,'wb')
pickle.dump(isodistance_ij,file)
file.close()

#
## do some plotting...
#
#base_path = '/home/blaughli/tracking_project/'
#grid_directory = 'grid_data/'
#grid_path_in = base_path + grid_directory + grid_file_in
#
#dset = netCDF4.Dataset(grid_path_in, 'r')
#psi_mask = dset['mask_psi']
#rho_lon_grid = dset['lon_rho']
#rho_lat_grid = dset['lat_rho']
#dset.close
#
#psi = np.array(psi_mask)
#lon = np.array(rho_lon_grid)
#lat = np.array(rho_lat_grid)
#
#
#x = np.arange(np.shape(lon)[0])
#y = np.arange(np.shape(lon)[1])
#
#rgi_lon = RGI([x,y],lon)
#rgi_lat = RGI([x,y],lat)
#
#
#isodistance_lon = rgi_lon((isodistance_ij[:,0], isodistance_ij[:,1]))
#isodistance_lat = rgi_lat((isodistance_ij[:,0], isodistance_ij[:,1]))
#
#
#fig, ax = plt.subplots()
#ax.pcolormesh(lon,lat,psi)
#ax.plot(isodistance_lon,isodistance_lat,linewidth=2)
#ax.axis('image')
#plt.show()
#
#



