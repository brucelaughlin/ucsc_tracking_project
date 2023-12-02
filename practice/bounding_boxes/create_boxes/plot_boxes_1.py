
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

base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc15_grd_no_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

points_type = 'psi'

if points_type == 'psi':


    isoline_coord_file_in = 'isodistance_ij_coords_wc15_no_islands.p'
    bounding_boxes_file_in = 'bounding_boxes_ij_coords_psi_coastline_wc15_continental.p'
    coastline_coords_file_in = 'coastline_coords_psi_file_wc15_continent.p'
    dist_field_file_in = 'dist_2_coast_field_wc15_no_islands.mat'
    mask = np.array(dset['mask_psi'])
    #mask = np.array(dset['mask_rho'])

elif points_type == 'rho':

    isoline_coord_file_in = 'isodistance_ij_coords_rho_coastline_wc15_no_islands.p'
    bounding_boxes_file_in = 'bounding_boxes_ij_coords_rho_coastline_wc15_continental.p'
    coastline_coords_file_in = 'coastline_coords_rho_file_wc15_continent.p'
    dist_field_file_in = 'dist_2_coast_field_rho_coastline_wc15_no_islands.mat'
    mask = np.array(dset['mask_rho'])

dset.close
#---------------------------------------------------------------------
#---------------------------------------------------------------------




# Load the "distance field" - plot over this
dist_field = scipy.io.loadmat(dist_field_file_in)
dist_field = dist_field['dist_field']

#
## Load coast
#file = open(coastline_coords_file_in,'rb')
#coast_ij = pickle.load(file)
#file.close
#

#
## Load offshore boundary
#file = open(isoline_coord_file_in,'rb')
#isodist_ij = pickle.load(file)
#file.close
#

#
## Load the walls
#file = open(bounding_boxes_file_in,'rb')
#walls_ij = pickle.load(file)
#file.close
#

# Load the boxes
file = open(bounding_boxes_file_in,'rb')
boxes_ij = pickle.load(file)
file.close


fig, ax = plt.subplots()
ax.pcolormesh(np.transpose(dist_field))
ax.pcolormesh(mask)


#ax.plot(isodist_ij[:,1],isodist_ij[:,0],linewidth=2)
#ax.plot(coast_ij[:,1],coast_ij[:,0],linewidth=2)

#for wall in walls_ij:
#    if wall is not None:
#        #ax.plot(wall[0],wall[1])
#        ax.plot(wall[1],wall[0])


for box in boxes_ij:
#for box in boxes_ij[1:2]:
    if box is not None:
        ax.plot(box[1],box[0])




ax.axis('image')
plt.show()









