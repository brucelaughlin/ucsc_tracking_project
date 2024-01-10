
import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from skimage import measure
#from geopy import distance
#from scipy import interpolate
import scipy.interpolate as spint
import ast


#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

#land_type = 'continent'
land_type = 'islands'

base_path = '/home/blaughli/tracking_project/'

grid_directory = 'grid_data/'
grid_file_in = 'wc15_grd_only_islands.nc'
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

# load artifical bridge endpoint coordinates
file = open(box_dir + islands_dir + 'artificial_coastline_insertion_points.txt','r')
bridge_point_list = file.read().splitlines()
file.close()
bridge_point_list = [ast.literal_eval(el) for el in bridge_point_list]



fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")




num_islands = 8

bp_dex = 0

for island_dex in range(1,num_islands+1):   

    coastline_file_in = input_dir + 'coastline_coords_wc15_island_number_{}.p'.format(island_dex)
    isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15_island_number_{}.p'.format(island_dex)

    # Load the coastlines
    file = open(coastline_file_in,'rb')
    coastline_lonlat = pickle.load(file)
    file.close

    coastline = coastline_lonlat[0]

    # Load the isolines
    file = open(isoline_file_in,'rb')
    isoline_lonlat = pickle.load(file)
    file.close

    #isoline = isoline_lonlat[0]
    isoline = isoline_lonlat

    ax.plot(coastline[:,0],coastline[:,1])
    ax.plot(isoline[:,0],isoline[:,1])
    ax.scatter(coastline[0,0],coastline[0,1],c='blue')

    if island_dex == 1:
        ax.scatter(coastline[bridge_point_list[bp_dex][0],0],coastline[bridge_point_list[bp_dex][0],1],c='red')
        bp_dex += 1
    elif island_dex < 4:
        ax.scatter(coastline[bridge_point_list[bp_dex-1][1],0],coastline[bridge_point_list[bp_dex-1][1],1],c='red')
        ax.scatter(coastline[bridge_point_list[bp_dex][0],0],coastline[bridge_point_list[bp_dex][0],1],c='red')
        bp_dex += 1

    ax.axis('image')
    plt.show()









