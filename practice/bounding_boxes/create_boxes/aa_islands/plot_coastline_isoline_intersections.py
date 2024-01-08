
import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from skimage import measure
import scipy.interpolate as spint
from shapely.geometry import Polygon

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


fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")



num_islands = 8

for island_dex in range(1,num_islands+1):   
#for island_dex in range(1,3):   

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

    isoline = isoline_lonlat

    ax.plot(coastline[:,0],coastline[:,1])
    ax.plot(isoline[:,0],isoline[:,1])

    ax.axis('image')
    plt.show()



# Now plot intersection points, to see how accurate the algorithm is


num_islands_intersecting = 4

island_isolines = []
island_coastlines = []
new_isolines = []


for island_dex in range(1,num_islands_intersecting+1):   
#for island_dex in range(0,2):   

    coastline_file_in = input_dir + 'coastline_coords_wc15_island_number_{}.p'.format(island_dex)
    isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15_island_number_{}.p'.format(island_dex)

    # Load the coastlines
    file = open(coastline_file_in,'rb')
    coastline_lonlat = pickle.load(file)
    file.close

    island_coastlines.append(coastline_lonlat[0])

    # Load the isolines
    file = open(isoline_file_in,'rb')
    isoline_lonlat = pickle.load(file)
    file.close

    island_isolines.append(isoline_lonlat)


for island_dex in range(0,num_islands_intersecting-1):
#for island_dex in range(0,1):   

    # subtract lattitudes of the isolines, to see where sign changes 
    #idx = np.argwhere(np.diff(np.sign(island_isolines[island_dex][:,1] - island_isolines[island_dex-1][:,1]))).flatten()

    p = []
    for ii in range(len(island_isolines[island_dex])):
        p.append((island_isolines[island_dex][ii,0],island_isolines[island_dex][ii,1]))

    q = []
    for ii in range(len(island_isolines[island_dex+1])):
        q.append((island_isolines[island_dex+1][ii,0],island_isolines[island_dex+1][ii,1]))


   
    #ax.plot(p)
    #ax.plot(q)


    pp = Polygon(p)
    qq = Polygon(q)
    x = pp.intersection(qq)

    # This returns an nx2 element tuple, where n is the number of intersections.
    # the elements alternate as lon,lat
    # I think the lower (?) of the 2 points comes first
    common_points = x.bounds

    if len(common_points) > 0:
        ax.scatter(common_points[0],common_points[1],color = 'red')
        ax.scatter(common_points[2],common_points[3],color = 'blue')


    # Confusing behavior, and now it's clear that I was not understanding "intersection" correctly:
    w,z=x.exterior.xy
    ax.plot(w,z)



















