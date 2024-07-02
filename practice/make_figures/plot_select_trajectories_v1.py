
# -----------------------------------------------------------------------------------------
#save_plot_directory = "/home/blaughli/tracking_project/figures/meetings/will_240702/"
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
islands_dir = 'aa_islands/'
continent_dir = 'continent/'
input_dir_islands = box_dir + islands_dir + 'z_output/'
input_dir_continent = box_dir + continent_dir + 'z_output/'

pdf_directory = 'practice/bounding_boxes/final_locations/z_output/'
pdf_modified_file = base_path + pdf_directory + 'pdf_data_output_seasonal_test3_modified.p'

file = open(pdf_modified_file,'rb')
p0,p1,p2,p3,p4,counter_array,box_numbers_islands_mod,tick_positions_islands = pickle.load(file)  # When the new calc is done, saved a counter_array for checking consistency
#p0,p1,p2,p3,p4,counter_array,box_numbers_islands_mod,box_numbers_islands_print,tick_positions_islands = pickle.load(file)  # When the new calc is done, saved a counter_array for checking consistency
#pdf_raw,pdf_raw_djf,pdf_raw_mam,pdf_raw_jja,pdf_raw_son,counter_array = pickle.load(file)  # When the new calc is done, saved a counter_array for checking consistency
file.close()



# Input Files
#---------------------------------------------------------------------
#tracking_output_dir = '/data03/blaughli/tracking_project_output/z_one_file_test/'
tracking_output_dir = '/data03/blaughli/tracking_project_output/test3_physics_only/'
#---------------------------------------------------------------------

tracking_output_files = [f for f in listdir(tracking_output_dir) if isfile(join(tracking_output_dir,f))]
tracking_output_files.sort()



#---------------------------------------------------------------------
#---------------------------------------------------------------------


# Get nice plot background going
# (jet color for depth, land masked with grey)

h_2 = np.multiply(mask,h)
cmap_custom = plt.colormaps['jet']
cmap_custom.set_under('0.8')

# needed?
#plt.ion()


# Now I know the boxes of interest (taken from domain plots)
tick_positions_continent_orig = [23,29,32,37,41,47,56,60,67,77]
#tick_positions_orig = [1,5,9,10,13,16,17,19,23,29,32,37,41,47,56,60,67,77]
tick_labels = ['SCl','Ca','SB','SN','SM','SR','SC','An','TJ','PV','PM','PC','PB','CB','PR','PA','CM','CBl']
#tick_labels = ['SCl','Ca','SB','SN','SR','An','SC','SM','TJ','PV','PM','PC','PB','CB','PR','PA','CM','CBl']
#tick_positions = [x+1 for x in tick_positions_orig]
#tick_positions = box_numbers_islands_print + [x+1 for x in tick_positions_continent_orig]
tick_positions = tick_positions_islands + [x+1 for x in tick_positions_continent_orig]

island_lats = [32.823,33.324,33.457,33.224,34.024,33.923,33.957,33.991]
island_lons = [-118.396,-118.345,-119.033,-119.508,-120.338,-120.138,-119.730,-119.4]

#island_lats = [32.823,33.324,33.457,33.224,33.923,33.991,33.957,34.024]
#island_lons = [-118.396,-118.345,-119.033,-119.508,-120.138,-119.4,-119.730,-120.338]

# ---------------------------------------------
# Plot parameters
box_plot_mod = 2
box_plot_mod_island = 1
#box_plot_mod = 3

font_size_num_continent = 15
font_size_num_island = 12
font_size_labels = 17

text_color = "blue"
#number_color = "gold"
#number_color = "mistyrose" # 7
#number_color = "darkorchid"
number_color = "yellow"
#number_color = "white"
#arrow_color = "white"
#arrow_color2 = "darkorange"
#arrow_color2 = "deeppink" # 8
#arrow_color2 = "fuchsia" # 8
arrow_color2 = "magenta" # 9
#arrow_color2 = "violet" # 7
#arrow_color2 = "mediumorchid"
#arrow_color2 = "plum" # 8
#arrow_color2 = "lightgray"
#arrow_color2 = "black"
arrow_width=4
va_val = "center"
offset = 100
#offset = 72
#relpos_tuple = (0,0)
relpos_tuple = (0,0)
relpos_tuple2 = (.5,.5)

# Copied from "https://www.geeksforgeeks.org/matplotlib-pyplot-annotate-in-python/"
bbox = dict(boxstyle ="round", fc ="0.95")
#bbox = dict(boxstyle ="round", fc ="0.8")
arrowprops = dict(
    arrowstyle = "->",
    lw=arrow_width,
    color=arrow_color2)
    #color=arrow_color)
arrowprops2 = dict(
    arrowstyle = "->",
    lw=arrow_width,
    color=arrow_color2)

# ---------------------------------------------


# I really don't know what "vmin" is doing here, but it seems to work (copied from a stack overflow post)

fig, ax = plt.subplots()
#fig = plt.figure()

ax.pcolormesh(lon_field,lat_field,h_2,shading="nearest",cmap = cmap_custom, vmin=0.001)
#plt.pcolormesh(lon_field,lat_field,h_2,shading="nearest",cmap = cmap_custom, vmin=0.001)
ax.axis('image')
#fig.axis('image')

#fig.canvas.draw()
#plt.show()

# for figuring out the number of the last island box
first_continent_box_dex = 0

# Islands

num_islands = 8
num_last_blob_island = 4

# for labels
box_num = 1
tick_num = 0

# Plot bounds for island plot
x_min = -121
x_max = -116.8
y_min = 32.5
y_max = 34.5

# -----------------------------------------------------------------------------------------

for island_dex in range(num_islands,num_last_blob_island-1,-1):

    # Set an index for the bounding point lists (the lists of points used to split the coastlines and isolines)
    bp_dex = island_dex-num_last_blob_island

    for inoffshore_switch in range(0,2):


        #if inoffshore_switch == 0:
        if inoffshore_switch == 1:
            bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15n_island_number_{}_inshore.p'.format(island_dex)
        else:
            bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15n_island_number_{}_offshore.p'.format(island_dex)


        # Load the boxes
        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)
        file.close

        for box in reversed(boxes_lonlat):
            if box is not None:
                ax.plot(box[0],box[1],c = 'white',linewidth=0.6)
                #if switch_plot_islands:
                    #if box_num % box_plot_mod_island == 0:
                        #ax.annotate(box_numbers_islands_mod[box_num-1]+1, xy = [np.mean(box[0]), np.mean(box[1])], color=number_color, ha="center", va="center", fontsize=font_size_num_continent, weight="bold")
                box_num += 1
                first_continent_box_dex += 1

# Continent

bounding_boxes_file_in = input_dir_continent + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(points_type_line)

# Load the boxes
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close

for box in boxes_lonlat:
    if box is not None:
        ax.plot(box[0],box[1],c = 'white',linewidth=0.6)
        if tick_num < len(tick_labels):
            if box_num == tick_positions[tick_num]:
                if tick_num == len(tick_labels):
                    tick_num = 0
                
            #if (box_num+1) % box_plot_mod == 0:
                #ax.annotate(box_num, xy = [np.mean(box[0]), np.mean(box[1])], color=number_color, ha="center", va="center", fontsize=font_size_num_continent, weight="bold")
        box_num += 1

if switch_plot_islands:
    plt.axis([x_min, x_max, y_min, y_max])




#---------------------------------------------------------------------
# Trajectories
#---------------------------------------------------------------------

#particle_numbers_islands = range(10000,50000,10000)
#particle_numbers_full = range(50000,200000,50000)
#colors_islands = ['plum','violet','orchid','magenta','hotpink']

#particle_number = 10000

particle_numbers = particle_numbers_full

#num_files = len(tracking_output_files)

#file_number = 0
#file_step = 50
#max_file_num = len(tracking_output_files) - (len(tracking_output_files) % file_step)
#selected_files = list(range(0,max_file_num,file_step))
#selected_files = list(range(0,len(tracking_output_files) - len(tracking_output_files) % 50)

selected_files = [0,2,4,7] #W,S,Su,F

#---------------------------------------------------------------------
# Testing, when working indent and make loop
#---------------------------------------------------------------------
#for tracking_output_file_pre in tracking_output_files:

tFiles = [tracking_output_files[jj] for jj in selected_files]

#for tracking_output_file_pre in tFiles:
for ii in range(len(tFiles)):
#for ii in range(1):
#for ii in range(1,2):
#for ii in range(2,3):
#---------------------------------------------------------------------
#    ii = 0

    #print(ii)

    #file_number += 1
    #if file_number % 20 == 0:

    tracking_output_file_pre = tFiles[ii]
    tracking_output_file = tracking_output_dir + tracking_output_file_pre

    dset = netCDF4.Dataset(tracking_output_file, 'r')

    lon_pre = dset.variables['lon'][particle_numbers]
    lat_pre = dset.variables['lat'][particle_numbers]
    z_pre = dset.variables['z'][particle_numbers]
    status = dset.variables['status'][particle_numbers]
    #lon_pre = dset.variables['lon'][particle_number]
    #lat_pre = dset.variables['lat'][particle_number]
    #z_pre = dset.variables['z'][particle_number]
    #status = dset.variables['status'][particle_number]
    dset.close()

    trajectory_mask = status == 0

    for jj in range(len(particle_numbers)):
#---------------------------------------------------------------------
#        jj = 0

        lon = lon_pre[jj,trajectory_mask[jj]]
        lat = lat_pre[jj,trajectory_mask[jj]]
        z = z_pre[jj,trajectory_mask[jj]]
        #lon = lon_pre[ii,trajectory_mask[jj]]
        #lat = lat_pre[ii,trajectory_mask[jj]]
        #z = z_pre[ii,trajectory_mask[jj]]



        ax.plot(lon,lat,c = colors_paths[ii],linewidth=2)
        ax.plot(lon[0],lat[0],'co')
        ax.plot(lon[-1],lat[-1],'ro')
        #ax.plot(lon[0],lat[0],'ro')
        #ax.plot(lon[-1],lat[-1],'co')


#colors_paths = ['azure','lime','violet','orange']

handles, labels = plt.gca().get_legend_handles_labels()

lineW = Line2D([0], [0], label='Winter trajectory', color=colors_paths[0])
lineS = Line2D([0], [0], label='Spring trajectory', color=colors_paths[1])
lineSu = Line2D([0], [0], label='Summer trajectory', color=colors_paths[2])
lineF = Line2D([0], [0], label='Fall trajectory', color=colors_paths[3])

pointS = Line2D([0], [0], label='starting location', marker='o', markersize=10, color='c' ,linestyle='')
                 #markeredgecolor='r', markerfacecolor='k', linestyle='')

pointF = Line2D([0], [0], label='ending location', marker='o', markersize=10, color='r' ,linestyle='')

# add manual symbols to auto legend
handles.extend([lineW,lineS,lineSu,lineF,pointS,pointF])

plt.legend(handles=handles)



plt.title(plot_title)

#plt.savefig(save_plot_file)
#plt.savefig(save_plot_file, bbox_inches='tight')

#plt.show(bbox_inches='tight')
plt.show()


