

# desired units: mg/L

molarMassO2 = 31.999 # g/mol

conversionFactor = molarMassO2/1000  #worked this out on papre



#input Files
#---------------------------------------------------------------------
#tracking_output_dir = '/data03/blaughli/tracking_project_output/z_one_file_test/'
tracking_output_dir_1 = '/data03/blaughli/tracking_project_output/test3_physics_only/'
tracking_output_dir_2 = '/data03/blaughli/tracking_project_output/test4_physics_only_AKs_1en5/'
#---------------------------------------------------------------------



import netCDF4
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.interpolate import interp1d
from geopy.distance import great_circle
import scipy.interpolate as spint
import ast
import time
from os import listdir
from os.path import isfile, join
import sys
import matplotlib.patches as mpatches
import matplotlib.cm as cm
from matplotlib.lines import Line2D

from pyproj import Geod
#from shapely.geometry import Polygon
from shapely.geometry import LineString, Point, Polygon



#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

base_path = '/home/blaughli/tracking_project/'

grid_directory = 'grid_data/'
grid_file_in = 'wc15n_grd.nc'
grid_path_in = base_path + grid_directory + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

points_type_field = 'rho'
points_type_line = 'psi'
lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])
mask = np.array(dset['mask_{}'.format(points_type_field)])
h = np.array(dset['h'])

dset.close


box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'modify_islands/'
continent_dir = 'continent/'
input_dir_islands = box_dir + islands_dir + 'z_output/'
input_dir_continent = box_dir + continent_dir + 'z_output/'



#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------



tracking_output_files_1 = [f for f in listdir(tracking_output_dir_1) if isfile(join(tracking_output_dir_1,f))]
tracking_output_files_1.sort()

tracking_output_files_2 = [f for f in listdir(tracking_output_dir_2) if isfile(join(tracking_output_dir_2,f))]
tracking_output_files_2.sort()


tracking_output_file = tracking_output_dir_1 + tracking_output_files_1[0]
dset = netCDF4.Dataset(tracking_output_file, 'r')

particle_labels_1 = dset.variables['trajectory'][:]
lon_all_1 = dset.variables['lon'][:]
lat_all_1 = dset.variables['lat'][:]
z_all_1 = dset.variables['z'][:]
status_all_1 = dset.variables['status'][:]
time_1 = np.array(dset['time'])
oxygen_all_1 = dset.variables['oxygen'][:]
temp_all_1 = dset.variables['sea_water_temperature'][:]

dset.close()

oxygen_all_1 *= conversionFactor


tracking_output_file = tracking_output_dir_2 + tracking_output_files_2[0]
dset = netCDF4.Dataset(tracking_output_file, 'r')

particle_labels_2 = dset.variables['trajectory'][:]
lon_all_2 = dset.variables['lon'][:]
lat_all_2 = dset.variables['lat'][:]
z_all_2 = dset.variables['z'][:]
status_all_2 = dset.variables['status'][:]
time_2 = np.array(dset['time'])
oxygen_all_2 = dset.variables['oxygen'][:]
temp_all_2 = dset.variables['sea_water_temperature'][:]

dset.close()

oxygen_all_2 *= conversionFactor


o2_diff = oxygen_all_1 - oxygen_all_2
num_data = np.shape(o2_diff)[0]*np.shape(o2_diff)[1] - np.ma.count_masked(o2_diff)
num_diff_o2 =  np.sum(o2_diff > 0) + np.sum(o2_diff < 0) 
fraction_diff_o2 = num_diff_o2/num_data


temp_diff = temp_all_1 - temp_all_2
num_diff_temp =  np.sum(temp_diff > 0) + np.sum(temp_diff < 0) 
fraction_diff_temp = num_diff_temp/num_data


lon_diff = lon_all_1 - lon_all_2
num_diff_lon =  np.sum(lon_diff > 0) + np.sum(lon_diff < 0) 
fraction_diff_lon = num_diff_lon/num_data


z_diff = z_all_1 - z_all_2
num_diff_z =  np.sum(z_diff > 0) + np.sum(z_diff < 0) 
fraction_diff_z = num_diff_z/num_data


diff_indices = z_diff != 0

num_particles = np.shape(z_diff)[0]
full_length_run = np.shape(z_diff)[1]

coord_diff_list = np.zeros((num_particles,2))

for ii in range(num_particles):
    for jj in range(full_length_run):
        if diff_indices[ii,jj]:
            coord_diff_list[ii,0] = lon_all_1[ii,jj] 
            coord_diff_list[ii,1] = lat_all_1[ii,jj] 
            break


test_array = coord_diff_list[:,0]
good_indices = test_array != 0

coords_plot = coord_diff_list[good_indices,:]





h_2 = np.multiply(mask,h)
cmap_custom = plt.colormaps['jet']
cmap_custom.set_under('0.8')








fig, ax = plt.subplots()
mesh1 = ax.pcolormesh(lon_field,lat_field,h_2,shading="nearest",cmap = cmap_custom, vmin=0.001)
ax.axis('image')

spot_color = "magenta"
#ax.scatter(coords_plot[:,0],coords_plot[:,1], c=spot_color)
#ax.scatter(coords_plot[:,0],coords_plot[:,1], c=spot_color, edgecolor='k')
ax.scatter(coords_plot[:,0],coords_plot[:,1], c=spot_color, edgecolor='k', s=200)

plt.title("First location where depth differences exist betweend runs with AKs = 0.1 and AKs = 0.00001\nfor trajectories for which such differences exist")


plt.show()








