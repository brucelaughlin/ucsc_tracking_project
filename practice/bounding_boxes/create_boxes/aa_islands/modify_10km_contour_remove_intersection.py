# OK, new plan, per Chris and Ecologists!  For islands with intersecting isolines, insert artificial
# 0-dimensional coastline "extension" between the islands, remove all of the isoline points in the
# intersections of their polygons, and treat as one big piece of land.

# Furthermore, we want to impose lines dividing "inshore" and "offshore" coasts, per the ecologists.

# V1 is half-working, but need to add the "lower piece" of the 2nd island's isoline FIRST,
# then add the 1st island's isoline, then add the "upper Piece" of the 2nd island's isoline
# (all excluding the isoline points in the intersection)

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


# Need to change things - store the "previous isoline" separately, and 
# only look at the "next" one in the loop
previous_isoline = island_isolines[0] 


for island_dex in range(0,num_islands_intersecting-1):

    combined_isoline_lon = []
    combined_isoline_lat = []

    p = []
    for ii in range(len(previous_isoline)):
        p.append((previous_isoline[ii,0],previous_isoline[ii,1]))

    q = []
    for ii in range(len(island_isolines[island_dex+1])):
        q.append((island_isolines[island_dex+1][ii,0],island_isolines[island_dex+1][ii,1]))


    # Compute the (true mathematical) intersection of the polygons
    pp = Polygon(p)
    qq = Polygon(q)
    internal_points = pp.intersection(qq)

    # Add points not in the intersection to the combined_isoline

    p_lon_pre_1,p_lat_pre_1=internal_points.exterior.xy

    p_lon_pre_2 = list(p_lon_pre_1)    
    p_lat_pre_2 = list(p_lat_pre_1)    

    # Round polygon coordinates and intersection coordinates, otherwise precisions don't match and we can't filter...??
    round_param = 3

    p_lon = list(np.around(np.array(p_lon_pre_2),round_param))
    p_lat = list(np.around(np.array(p_lat_pre_2),round_param))

    coord_tuples_intersection = merge_lists(p_lon,p_lat)

    isoline_2_dex = 0
    # Step 1: Add the "lower piece" of the 2nd island's isoline
    for ii in range(len(island_isolines[island_dex+1])):
        if (round(island_isolines[island_dex+1][ii,0],round_param),round(island_isolines[island_dex+1][ii,1],round_param)) in coord_tuples_intersection:
            isoline_2_dex = ii
            break
        else:
            combined_isoline_lon.append(island_isolines[island_dex+1][ii,0])
            combined_isoline_lat.append(island_isolines[island_dex+1][ii,1])

    # Step 2: Add the 1st island's isoline
    for ii in range(len(previous_isoline)):
        if (round(previous_isoline[ii,0],round_param),round(previous_isoline[ii,1],round_param)) not in coord_tuples_intersection:
            combined_isoline_lon.append(previous_isoline[ii,0])
            combined_isoline_lat.append(previous_isoline[ii,1])

    # Step 3: Add the "upper piece" of the 2nd island's isoline
    for ii in range(isoline_2_dex,len(island_isolines[island_dex+1])):
        if (round(island_isolines[island_dex+1][ii,0],round_param),round(island_isolines[island_dex+1][ii,1],round_param)) not in coord_tuples_intersection:
            combined_isoline_lon.append(island_isolines[island_dex+1][ii,0])
            combined_isoline_lat.append(island_isolines[island_dex+1][ii,1])

    previous_isoline = np.column_stack([combined_isoline_lon,combined_isoline_lat])



# Close and store the final isoline
combined_isoline = np.append(previous_isoline,[previous_isoline[0,:]],axis=0)

#fig, ax = plt.subplots()
#ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")
#ax.plot(combined_isoline[:,0],combined_isoline[:,1])
#plt.show()


output_file = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15_island_1_through_4_blob.p'

file = open(output_file,'wb')
pickle.dump(combined_isoline,file)
file.close()








