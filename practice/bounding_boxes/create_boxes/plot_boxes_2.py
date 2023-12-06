
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

points_type_line = 'psi'
points_type_field = 'rho'


isoline_coord_file_in = 'isodistance_ij_coords_{}_coastline_wc15_no_islands.p'.format(points_type_line)
bounding_boxes_file_in = 'bounding_boxes_ij_coords_{}_coastline_wc15_continental.p'.format(points_type_line)
coastline_coords_file_in = 'coastline_coords_{}_file_wc15_continent.p'.format(points_type_line)
dist_field_file_in = 'dist_2_coast_field_{}_coastline_wc15_no_islands.mat'.format(points_type_field)
mask = np.array(dset['mask_{}'.format(points_type_field)])
lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])
lon_line = np.array(dset['lon_{}'.format(points_type_line)])
lat_line = np.array(dset['lat_{}'.format(points_type_line)])


dset.close
#---------------------------------------------------------------------
#---------------------------------------------------------------------

RGI = spint.RegularGridInterpolator

# create interpolator to get lat/lon at isoline points
x = np.arange(np.shape(lon_line)[0])
y = np.arange(np.shape(lon_line)[1])
rgi_lon = RGI([x,y],lon_line)
rgi_lat = RGI([x,y],lat_line)


# Load the "distance field" - plot over this
dist_field = scipy.io.loadmat(dist_field_file_in)
dist_field = dist_field['dist_field']


# Load coast
file = open(coastline_coords_file_in,'rb')
coast_ij = pickle.load(file)
file.close


# Load the boxes
file = open(bounding_boxes_file_in,'rb')
boxes_ij = pickle.load(file)
file.close

x=np.arange(lon_field.shape[1])
y=np.arange(lon_field.shape[0])

fig, ax = plt.subplots()
#ax.pcolormesh(lon,lat,np.transpose(dist_field),shading="nearest")
#ax.pcolormesh(lon,lat,np.transpose(mask),shading="nearest")
#ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")
ax.pcolormesh(x,y,mask,shading="nearest")


#ax.plot(rgi_lat((coast_ij[:,0],coast_ij[:,1])),rgi_lon((coast_ij[:,0],coast_ij[:,1])),linewidth=2)
#ax.plot(rgi_lon((coast_ij[:,0],coast_ij[:,1])),rgi_lat((coast_ij[:,0],coast_ij[:,1])),linewidth=2)


for box in boxes_ij:
    if box is not None:
        ax.plot(box[1],box[0])
        #ax.plot(rgi_lat((box[0],box[1])),rgi_lon((box[0],box[1])))
        #ax.plot(rgi_lon((box[0],box[1])),rgi_lat((box[0],box[1])))


ax.axis('image')
plt.show()









