# OK, new plan, per Chris and Ecologists!  For islands with intersecting isolines, insert artificial
# 0-dimensional coastline "extension" between the islands, remove all of the isoline points in the
# intersections of their polygons, and treat as one big piece of land.

# Furthermore, we want to impose lines dividing "inshore" and "offshore" coasts, per the ecologists.



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

# Function to merge 2 lists (lon/lat) into one list of tuples (GeeksForGeeks):

def merge_lists(list1, list2):
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list



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


combined_isoline_lon = []
combined_isoline_lat = []

combined_isoline_tuples = []

for island_dex in range(0,num_islands_intersecting-1):
#for island_dex in range(0,1):   


    p = []
    for ii in range(len(island_isolines[island_dex])):
        p.append((island_isolines[island_dex][ii,0],island_isolines[island_dex][ii,1]))

    q = []
    for ii in range(len(island_isolines[island_dex+1])):
        q.append((island_isolines[island_dex+1][ii,0],island_isolines[island_dex+1][ii,1]))


    # Compute the (true mathematical) intersection of the polygons
    pp = Polygon(p)
    qq = Polygon(q)
    internal_points = pp.intersection(qq)

    # Add points not in the intersection to the combined_isoline

    p_lon,p_lat=internal_points.exterior.xy

    p_lon_pre = list(p_lon)    
    p_lat_pre = list(p_lat)    

    # Round polygon coordinates and intersection coordinates, otherwise precisions don't match and we can't filter...??
    round_param = 3

    p_lon = list(np.around(np.array(p_lon_pre),round_param))
    p_lat = list(np.around(np.array(p_lat_pre),round_param))

    #new_points_lon = [point for point in list(island_isolines[island_dex][:,0]) if point not in p_lon]
    #new_points_lat = [point for point in list(island_isolines[island_dex][:,1]) if point not in p_lat]

    coord_tuples_intersection = merge_lists(p_lon,p_lat)

    for ii in range(len(island_isolines[island_dex])):
        if (round(island_isolines[island_dex][ii,0],round_param),round(island_isolines[island_dex][ii,1],round_param)) not in coord_tuples_intersection:
            combined_isoline_tuples.append((island_isolines[island_dex][ii,0],island_isolines[island_dex][ii,1]))



fig, ax = plt.subplots()
ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")

ax.plot(*zip(*combined_isoline_tuples))
plt.show()










