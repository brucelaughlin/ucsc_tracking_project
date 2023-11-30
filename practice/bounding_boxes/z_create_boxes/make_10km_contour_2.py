
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
dist_field_file = 'dist_2_coast_field_rho_coastline_wc15_no_island.mat'

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

