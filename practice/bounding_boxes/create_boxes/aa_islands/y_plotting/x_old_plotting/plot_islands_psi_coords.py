
import netCDF4
import matplotlib.pyplot as plt
import numpy as np

#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc15_grd_only_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

#points_type = 'psi'
points_type = 'rho'
mask = np.array(dset['mask_{}'.format(points_type)])

dset.close

#---------------------------------------------------------------------
#---------------------------------------------------------------------


fig, ax = plt.subplots()
ax.pcolormesh(range(np.shape(mask)[1]),range(np.shape(mask)[0]),mask,shading="nearest")


