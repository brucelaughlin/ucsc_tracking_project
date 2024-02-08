# Prevoiusly was just saving the endpoints of the "walls" running "perpendicular"
# to the coast.  But I now want to save the entire polygons of the bounding boxes,
# so that I can easily feed them into an algorithm to determine if a tracked
# particle is in one of them.

# Last version didn't store the lower wall of the polygon...

# I guess we need to "close" polygons?  i.e. copy first point as last point

# Potential bug - does this handle the case where the prevoius box's
# "closest point" is the last isoline point?  Ie there are coast points
# left, but no more isoline points?
# Wait, I think it does...

# I think that I have reversed i and j in all of this work.
# i think that i corresponds roughly to longitude, and j to lattitude

# Ok, imagine that West is up  So X = rows, Y = cols

import netCDF4
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from geopy.distance import great_circle
import scipy.interpolate as spint



#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
base_dir = '/home/blaughli/tracking_project/'
grid_dir = 'grid_data/'
grid_file_in = 'wc15_grd_no_islands.nc'
grid_path_in = base_dir + grid_dir + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

box_file_dir = 'practice/bounding_boxes/create_boxes/'


point_type_line = 'psi'
point_type_field = 'rho'

isoline_coord_file_in = base_dir + box_file_dir + 'isodistance_ij_coords_{}_coastline_wc15_no_islands.p'.format(point_type_field)
coast_coords_in_i = base_dir + box_file_dir + 'coast_coords_{}_wc15_continent_i.txt'.format(point_type_line)
coast_coords_in_j = base_dir + box_file_dir + 'coast_coords_{}_wc15_continent_j.txt'.format(point_type_line)
bounding_boxes_file_out = base_dir + box_file_dir + 'bounding_boxes_ij_coords_{}_coastline_wc15_continental.p'.format(point_type_line)
lon_grid = dset['lon_{}'.format(point_type_field)]
lat_grid = dset['lat_{}'.format(point_type_field)]



dset.close

# want our boxes to be (at least?) 300km^2
# But wait!  I'm just gonna use i,j coordinates, for simplicity
# So, for wc_12, our grid cells are roughly 10kmx10km = 100km^2, right?
# box_area_threshold = 300e3

# So, want something at least "3 cells big"
# WAIT!!!  I used the 100km isodistance line, not 10km!  Because wc_12
# is low enough resolution that 10km is often "onshore"!
box_area_threshold = 30
#box_area_threshold = 300
#---------------------------------------------------------------------
#---------------------------------------------------------------------

RGI = spint.RegularGridInterpolator


# create interpolator to get lat/lon at isoline points
lon = np.array(lon_grid)
lat = np.array(lat_grid)
x = np.arange(np.shape(lon)[0])
y = np.arange(np.shape(lon)[1])
rgi_lon = RGI([x,y],lon)
rgi_lat = RGI([x,y],lat)


# from https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


file = open(isoline_coord_file_in,'rb')
isoline_ij = pickle.load(file)
file.close
isoline_i = list(isoline_ij[:,0])
isoline_j = list(isoline_ij[:,1])

isoline_lon = rgi_lon((isoline_i, isoline_j))
isoline_lat = rgi_lat((isoline_i, isoline_j))

coast_i = list(np.loadtxt(coast_coords_in_i,unpack=False))
coast_j = list(np.loadtxt(coast_coords_in_j,unpack=False))

num_points_coast = len(coast_i)
num_points_isoline = len(isoline_i)

coast_ij = np.zeros((len(coast_i),2))
coast_ij[:,0] = coast_i
coast_ij[:,1] = coast_j

bounding_boxes_ij = []

walk_switch = True

coast_dex = 1
isoline_dex = 1

while walk_switch == True:

    print("{},{}".format(str(coast_dex),str(num_points_coast)))

    polygon_wall_onshore_i = []
    polygon_wall_onshore_j = []

    polygon_wall_onshore_i.append(coast_i[coast_dex-1])
    polygon_wall_onshore_j.append(coast_j[coast_dex-1])

    # walk up the coast
    for jj in range(coast_dex,num_points_coast):
        cp_i = int(coast_i[jj])
        cp_j = int(coast_j[jj]) 
        
        # append current coast points to polygon
        polygon_wall_onshore_i.append(cp_i)
        polygon_wall_onshore_j.append(cp_j)

        # see which remaining (ie not already used) isoline point is nearest
        dmax = 1e10
        closest_dex = None
        for ii in range(isoline_dex,num_points_isoline):
            dist = great_circle((lat[cp_i,cp_j],lon[cp_i,cp_j]),(isoline_lat[ii],isoline_lon[ii]))
            if dist < dmax: 
                dmax = dist
                closest_dex = ii


        # add final polygon if we used the final isoline or coast point
        if closest_dex == num_points_isoline-1 or jj == num_points_coast-1:

            if jj == num_points_coast-1:
                #polygon_i = polygon_wall_onshore_i[:] + isoline_i[-1:isoline_dex-1:-1]
                #polygon_j = polygon_wall_onshore_j[:] + isoline_j[-1:isoline_dex-1:-1]
                polygon_i = polygon_wall_onshore_i[:] + isoline_i[-1:isoline_dex-2:-1]
                polygon_j = polygon_wall_onshore_j[:] + isoline_j[-1:isoline_dex-2:-1]

            else: 
                #polygon_wall_onshore_i.append(coast_i[jj+1:-1])
                #polygon_wall_onshore_j.append(coast_j[jj+1:-1])
                polygon_wall_onshore_i.append(coast_i[jj+1:])
                polygon_wall_onshore_j.append(coast_j[jj+1:])
                #polygon_i = polygon_wall_onshore_i[:] + isoline_i[-1:isoline_dex-1:-1]
                #polygon_j = polygon_wall_onshore_j[:] + isoline_j[-1:isoline_dex-1:-1]
                polygon_i = polygon_wall_onshore_i[:] + isoline_i[-1:isoline_dex-2:-1]
                polygon_j = polygon_wall_onshore_j[:] + isoline_j[-1:isoline_dex-2:-1]

            # Close polygon
            polygon_i.append(polygon_i[0])
            polygon_j.append(polygon_j[0])

            bounding_boxes_ij.append(np.array([polygon_i,polygon_j]))

            walk_switch = False
            print(str(PolyArea(polygon_i,polygon_j)))
            break


        # Build a polygon to test for area
        if isoline_dex == 1:
            polygon_i = polygon_wall_onshore_i[:] + isoline_i[closest_dex:isoline_dex-1:-1] + [isoline_i[0]]
            polygon_j = polygon_wall_onshore_j[:] + isoline_j[closest_dex:isoline_dex-1:-1] + [isoline_j[0]]
        else:
            polygon_i = polygon_wall_onshore_i[:] + isoline_i[closest_dex:isoline_dex-2:-1]
            polygon_j = polygon_wall_onshore_j[:] + isoline_j[closest_dex:isoline_dex-2:-1]
       
        # Close polygon
        polygon_i.append(polygon_i[0])
        polygon_j.append(polygon_j[0])


        if PolyArea(polygon_i,polygon_j) >= box_area_threshold:

            bounding_boxes_ij.append(np.array([polygon_i,polygon_j]))

            isoline_dex = closest_dex + 1
            coast_dex = jj + 1

            print(str(PolyArea(polygon_i,polygon_j)))
            print('\n')

            break


file = open(bounding_boxes_file_out,'wb')
#pickle.dump(walls_ij,file)
pickle.dump(bounding_boxes_ij,file)
file.close()






