# V3: compare using new run with better AKs, and make general updates...

#v2: color by depth
# https://stackoverflow.com/questions/20165169/change-colour-of-curve-according-to-its-y-value-in-matplotlib

# Input Files
#---------------------------------------------------------------------
tracking_output_dir_pre = "test4_physics_only_AKs_1en5/"
#---------------------------------------------------------------------


# -----------------------------------------------------------------------------------------
pdf_file = "pdf_data_output_seasonal_rangeO2_v4_test4_physics_only_AKs_1en5_swapped.p"
# -----------------------------------------------------------------------------------------


particle_numbers_islands = list(range(10000,50000,10000))
particle_numbers_full = list(range(50000,250000,50000))
#particle_numbers_islands = list(range(10000,50000,10000))
#particle_numbers_full = list(range(50000,200000,50000))

colors_paths = ['skyblue','lime','violet','orange']
#colors_paths = ['azure','lime','violet','orange']
###colors_paths = ['plum','violet','orchid','magenta']


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# make switch to turn on/off island plotting
# -----------------------------------------------------------------------------------------
#switch_plot_islands = True
switch_plot_islands = False
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
#if switch_plot_islands:
#    plot_title = 'wc_15n model domain\n300km$^{2}$ coastal boxes\n10km offshore distance as outer wall\n(Southern California Bight detail)'
#    save_image_name = "domain_scb.png"
#else:
#    plot_title = 'wc_15n model domain\n300km$^{2}$ coastal boxes\n10km offshore distance as outer wall'
#    save_image_name = "domain_full.png"


fig_paramTitle = "wc_15n model, 300km$^{2}$ coastal boxes, 10km offshore distance as outer wall, physics only, 3D advection, 30-day PLD"
fig_mainTitle = "Sample trajectories"

plot_title = fig_mainTitle + "\n" + fig_paramTitle


# -----------------------------------------------------------------------------------------
#save_plot_file = save_plot_directory + save_image_name
# -----------------------------------------------------------------------------------------



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
tracking_output_base = "/data03/blaughli/tracking_project_output/"
tracking_output_dir = tracking_output_base + tracking_output_dir_pre

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

pdf_directory = 'practice/bounding_boxes/final_locations/z_output/'
pdf_modified_file = base_path + pdf_directory + pdf_file

#file = open(pdf_modified_file,'rb')
#pdf_list_exposure_T_source_swapped,pdf_list_of_lists_O2_source_swapped,pdf_list_connectivity_swapped,pdf_list_settleTime_swapped,settlement_boxes_test_array,settlement_times_test_array,counter_array,box_num_mod,tick_positions,tick_labels,first_continent_box_dex,oxygen_limit_list = pickle.load(file)
#file.close()




tracking_output_files = [f for f in listdir(tracking_output_dir) if isfile(join(tracking_output_dir,f))]
tracking_output_files.sort()



#---------------------------------------------------------------------
#---------------------------------------------------------------------


# Get nice plot background going
# (jet color for depth, land masked with grey)

h_2 = np.multiply(mask,h)
cmap_custom = plt.colormaps['jet']
cmap_custom.set_under('0.8')


# ---------------------------------------------
# Plot parameters
box_plot_mod = 2
box_plot_mod_island = 1
#box_plot_mod = 3

font_size_num_continent = 15
font_size_num_island = 12
font_size_labels = 17


# ---------------------------------------------


# I really don't know what "vmin" is doing here, but it seems to work (copied from a stack overflow post)

fig, ax = plt.subplots()

mesh1 = ax.pcolormesh(lon_field,lat_field,h_2,shading="nearest",cmap = cmap_custom, vmin=0.001)
ax.axis('image')

particle_numbers = particle_numbers_full

selected_files = [0,2,4,7] #W,S,Su,F

#---------------------------------------------------------------------
# Testing, when working indent and make loop
#---------------------------------------------------------------------
#for tracking_output_file_pre in tracking_output_files:

tFiles = [tracking_output_files[jj] for jj in selected_files]

# First, determine absolue min/max and range of Z, for consistent plotting and colorbar
z_range = 0 
z_min = 999999
z_max = 0
for ii in range(len(tFiles)):
    tracking_output_file_pre = tFiles[ii]
    tracking_output_file = tracking_output_dir + tracking_output_file_pre
    dset = netCDF4.Dataset(tracking_output_file, 'r')
    z_pre = np.abs(dset.variables['z'][particle_numbers])
    dset.close()
    z_max_pre = np.max(z_pre)
    z_min_pre = np.min(z_pre)
    if z_min_pre < z_min:
        z_min = z_min_pre
    if z_max_pre > z_max:
        z_max = z_max_pre
z_range = z_max - z_min


for ii in range(len(tFiles)):

    tracking_output_file_pre = tFiles[ii]
    tracking_output_file = tracking_output_dir + tracking_output_file_pre

    dset = netCDF4.Dataset(tracking_output_file, 'r')

    lon_pre = dset.variables['lon'][particle_numbers]
    lat_pre = dset.variables['lat'][particle_numbers]
    z_pre = np.abs(dset.variables['z'][particle_numbers])
    #z_pre = dset.variables['z'][particle_numbers]
    status = dset.variables['status'][particle_numbers]
    dset.close()

    #z_max = np.max(z_pre)
    #z_min = np.min(z_pre)
    ###z_max = np.max(np.abs(z_pre))
    ###z_min = np.min(np.abs(z_pre))
    ###z_range = z_max - z_min

    color_steps = np.linspace(0,1,1000)

    trajectory_mask = status == 0

    for jj in range(len(particle_numbers)):
#---------------------------------------------------------------------
#        jj = 0

        lon = lon_pre[jj,trajectory_mask[jj]]
        lat = lat_pre[jj,trajectory_mask[jj]]
        z = z_pre[jj,trajectory_mask[jj]]

        # hack - use scatter plot to color by depth

        for kk in range(len(lon)-1):
            lon_seg = np.linspace(lon[kk],lon[kk+1],1000)
            lat_seg = np.linspace(lat[kk],lat[kk+1],1000)
            z_seg = np.linspace(z[kk],z[kk+1],1000)
        
            z_segNorm = (z_seg - z_min)/z_range

            ax.scatter(lon_seg, lat_seg, c = cm.jet(z_segNorm), edgecolor='none')
            ax.plot(lon[0],lat[0],'co')
            ax.plot(lon[-1],lat[-1],'ro')


N = 20
cmap = plt.get_cmap('jet',N)

cbar_left = 0.8
cbar_bot = 0.2
cbar_width = 0.02
cbar_height = 0.5

#sub_ax = plt.axes([0.96, 0.55, 0.02, 0.3]) 
sub_ax = plt.axes([cbar_left,cbar_bot,cbar_width,cbar_height]) 

#norm = mpl.colors.Normalize(vmin=z_min,vmax=z_max)
norm = plt.Normalize(vmin=z_min,vmax=z_max)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
#cbar = plt.colorbar(sm, ticks=np.linspace(z_min,z_max,N+1), cax = sub_ax, boundaries=np.arange(-0.05,2.1,.1))
cbar = plt.colorbar(sm, ticks=np.linspace(z_min,z_max,N+1), cax = sub_ax)
#cbar = plt.colorbar(sm, ticks=np.linspace(z_min,z_max,N), cax = sub_ax)

cbar_label = "Depth (m)"
cbar_fontSize = 10

cbar.ax.set_ylabel(cbar_label, fontsize = cbar_fontSize)



#fig.colorbar(sm, ticks=np.linspace(z_min,z_max,N), 
#    boundaries=np.arange(-0.05,2.1,.1))
#plt.colorbar(sm, ticks=np.linspace(z_min,z_max,N), 
#    boundaries=np.arange(-0.05,2.1,.1))




#img = plt.imshow(colorbarDummyData)
#img.set_visible(False)
#fig.colorbar(img)

#color_bar = fig.colorbar(colorbarDummyData, ax = ax)








plt.show()














