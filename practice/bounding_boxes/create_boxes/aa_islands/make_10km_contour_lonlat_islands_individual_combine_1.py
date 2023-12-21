# For some islands, contours are segmented where they intersect other islands
# So, combine them...


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


base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc15_grd_no_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

points_type_field = 'rho'

lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])

dset.close


islands_dir = base_path + 'practice/bounding_boxes/create_boxes/aa_islands/'

output_dir = islands_dir + 'z_output/'

#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

num_islands = 8

#for island_dex in range(1,num_islands+1):
for island_dex in range(2,3):

    #---------------------------------------------------------------------
    output_file = output_dir + 'isodistance_lonlat_coords_rho_coastline_wc15_island_number_{}.p'.format(island_dex)
    
    dist_field_file = output_dir + 'dist_2_coast_field_rho_coastline_wc15_island_number_{}.mat'.format(island_dex)
    dist_field = scipy.io.loadmat(dist_field_file)
    dist_field = dist_field['dist_field']
    #---------------------------------------------------------------------



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


#    # Assume that the longest contour returned is the one we want....
#    max_length = 0 
#    contour_index = 0 
#    dex = 0 
#    for contour in contours:
#        if np.shape(contour)[0] > max_length:
#            max_length = np.shape(contour)[0]
#            contour_index = dex 
#        dex += 1
#
#    isoline_ij = contours[contour_index]
    
    # Assume all contours returned are relevant, combine them into single contour
    isoline_ij = np.vstack(contours)


   # if len(contours) > 1:
   #     idx = np.argwhere(np.diff(np.sign(y1_interp - y2_interp))).flatten()




    isoline_lonlat = np.zeros(np.shape(isoline_ij))
    for ii in range(np.shape(isoline_ij)[0]):
        isoline_lonlat[ii,0] = rgi_lon((isoline_ij[ii,0], isoline_ij[ii,1]))
        isoline_lonlat[ii,1] = rgi_lat((isoline_ij[ii,0], isoline_ij[ii,1]))


    file = open(output_file,'wb')
    pickle.dump(isoline_lonlat,file)
    file.close()










