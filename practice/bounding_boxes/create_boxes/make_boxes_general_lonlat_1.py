# lat/lon area calc taken from:
# https://stackoverflow.com/questions/68118907/shapely-pyproj-find-area-in-m2-of-a-polygon-created-from-latitude-and-longi


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

from pyproj import Geod
#from shapely.geometry import Polygon
from shapely.geometry import LineString, Point, Polygon


#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
base_dir = '/home/blaughli/tracking_project/'
grid_dir = 'grid_data/'
grid_file_in = 'wc15_grd_no_islands.nc'
grid_path_in = base_dir + grid_dir + grid_file_in
dset = netCDF4.Dataset(grid_path_in, 'r')

box_file_dir = 'practice/bounding_boxes/create_boxes/'
output_dir = 'z_output/'

point_type_line = 'psi'
point_type_field = 'rho'

#isoline_coord_file_in = base_dir + box_file_dir + 'isodistance_lonlat_coords_{}_coastline_wc15_no_islands.p'.format(point_type_field)
isoline_coord_file_in = base_dir + box_file_dir + output_dir + 'isodistance_lonlat_coords_{}_coastline_wc15_no_islands.p'.format(point_type_field)

#coast_coords_in_lon = base_dir + box_file_dir + 'coast_coords_{}_wc15_continent_lon.txt'.format(point_type_line)
#coast_coords_in_lat = base_dir + box_file_dir + 'coast_coords_{}_wc15_continent_lat.txt'.format(point_type_line)
#coast_coords_in = base_dir + box_file_dir + 'coastline_coords_{}_file_wc15_continent.p'.format(point_type_line)
coast_coords_in = base_dir + box_file_dir + output_dir + 'coastline_coords_{}_file_wc15_continent.p'.format(point_type_line)

bounding_boxes_file_out = base_dir + box_file_dir + output_dir + 'bounding_boxes_lonlat_coords_{}_coastline_wc15_continental.p'.format(point_type_line)


dset.close

# Set box area threshold (should be 300km, right?)
box_area_threshold = 3e8
#---------------------------------------------------------------------
#---------------------------------------------------------------------

# from https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
#def PolyArea(x,y):
#    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

# For calculating area
geod = Geod(ellps="WGS84")


file = open(coast_coords_in,'rb')
coast_coords = pickle.load(file)
file.close

coast_lon = coast_coords[:,0]
coast_lat = coast_coords[:,1]

file = open(isoline_coord_file_in,'rb')
isoline_lonlat = pickle.load(file)
file.close
isoline_lon = list(isoline_lonlat[:,0])
isoline_lat = list(isoline_lonlat[:,1])

num_points_coast = len(coast_lon)
num_points_isoline = len(isoline_lon)

bounding_boxes_lonlat = []

walk_switch = True

coast_dex = 1
isoline_dex = 1

closees_dex = 0

while walk_switch == True:

    print("coast dex: {}, total coast points: {}".format(str(coast_dex),str(num_points_coast)))

    polygon_wall_onshore_lon = []
    polygon_wall_onshore_lat = []

    polygon_wall_onshore_lon.append(coast_lon[coast_dex-1])
    polygon_wall_onshore_lat.append(coast_lat[coast_dex-1])

    # walk up the coast
    for jj in range(coast_dex,num_points_coast):
       
        #print(coast_dex)

        # append current coast points to polygon
        polygon_wall_onshore_lon.append(coast_lon[jj])
        polygon_wall_onshore_lat.append(coast_lat[jj])

        # see which remaining (ie not already used) isoline point is nearest
        # Set a dummy "dmax" which will be replaced after the fist iteration
        dmax = 1e1000
        closest_dex = None
        for ii in range(isoline_dex,num_points_isoline):
            #dist = great_circle((coast_lat[ii],coast_lon[ii]),(isoline_lat[ii],isoline_lon[ii]))
            dist = great_circle((coast_lat[jj],coast_lon[jj]),(isoline_lat[ii],isoline_lon[ii]))
            dist = dist._Distance__kilometers
            if dist < dmax: 
                dmax = dist
                closest_dex = ii
                #print(dist)
                #print('{}  ,    {}'.format(closest_dex,dist))

        #print('{}  ,    {}'.format(closest_dex,dist))
        #walk_switch = False
        #break


        # THIS MUST CHANGE, ESPECIALLY FOR ISLANDS - WANT BALANCED BOXES, SO NEED TO 
        # CHANGE THRESHOLD AND REOCMPUTE IF LAST BOX IS TOO LARGE/SMALL

        # ALSO, CHRIS WANTS TO JUST ADD THE LAST BOX TO THE PREVIOUS, NOT MAKE A SMALL ONE
        # AS I DO HERE

        # add final polygon if we used the final isoline or coast point
        if closest_dex == num_points_isoline-1 or jj == num_points_coast-1:

            if jj == num_points_coast-1:
                #polygon_lon = polygon_wall_onshore_lon[:] + isoline_lon[-1:isoline_dex-1:-1]
                #polygon_lat = polygon_wall_onshore_lat[:] + isoline_lat[-1:isoline_dex-1:-1]
                polygon_lon = polygon_wall_onshore_lon[:] + isoline_lon[-1:isoline_dex-2:-1]
                polygon_lat = polygon_wall_onshore_lat[:] + isoline_lat[-1:isoline_dex-2:-1]

            else: 
                #polygon_wall_onshore_lon.append(coast_lon[jj+1:-1])
                #polygon_wall_onshore_lat.append(coast_lat[jj+1:-1])
                polygon_wall_onshore_lon.append(coast_lon[jj+1:])
                polygon_wall_onshore_lat.append(coast_lat[jj+1:])
                #polygon_lon = polygon_wall_onshore_lon[:] + isoline_lon[-1:isoline_dex-1:-1]
                #polygon_lat = polygon_wall_onshore_lat[:] + isoline_lat[-1:isoline_dex-1:-1]
                polygon_lon = polygon_wall_onshore_lon[:] + isoline_lon[-1:isoline_dex-2:-1]
                polygon_lon = polygon_wall_onshore_lat[:] + isoline_lat[-1:isoline_dex-2:-1]

            # Close polygon
            polygon_lon.append(polygon_lon[0])
            polygon_lat.append(polygon_lat[0])

            bounding_boxes_lonlat.append(np.array([polygon_lon,polygon_lat]))

            walk_switch = False

            # Print polygon area
            polygon_test_list = []
            for ii in range(len(polygon_lon)):
                polygon_test_list.append([polygon_lon[ii],polygon_lat[ii]])
            polygon_test = Polygon(polygon_test_list)
            poly_area, poly_perimeter = geod.geometry_area_perimeter(polygon_test)
            print(str(poly_area))
            
            break


        # Build a polygon to test for area
        if isoline_dex == 1:
            polygon_lon = polygon_wall_onshore_lon[:] + isoline_lon[closest_dex:isoline_dex-1:-1] + [isoline_lon[0]]
            polygon_lat = polygon_wall_onshore_lat[:] + isoline_lat[closest_dex:isoline_dex-1:-1] + [isoline_lat[0]]
        else:
            polygon_lon = polygon_wall_onshore_lon[:] + isoline_lon[closest_dex:isoline_dex-2:-1]
            polygon_lat = polygon_wall_onshore_lat[:] + isoline_lat[closest_dex:isoline_dex-2:-1]
       
        # Close polygon
        polygon_lon.append(polygon_lon[0])
        polygon_lat.append(polygon_lat[0])


        # Test polygon area
        polygon_test_list = []

        #point_list = []
    
        #line_string = LineString([Point(1, 2), Point(3, 4)])

        for ii in range(len(polygon_lon)):
            polygon_test_list.append([polygon_lon[ii],polygon_lat[ii]])
            #point_list.append(Point(polygon_lon[ii],polygon_lat[ii]))
        
        #line_string = LineString(point_list)

        polygon_test = Polygon(polygon_test_list)
        #polygon_test = Polygon(line_string)
        poly_area, poly_perimeter = geod.geometry_area_perimeter(polygon_test)
        
        #print(poly_area)

        if poly_area >= box_area_threshold:

            bounding_boxes_lonlat.append(np.array([polygon_lon,polygon_lat]))

            isoline_dex = closest_dex + 1
            coast_dex = jj + 1

            #print(str(poly_area))
            print('polygon area: {},  threshold: {}'.format(poly_area,box_area_threshold))
            print('\n')

            break


file = open(bounding_boxes_file_out,'wb')
#pickle.dump(walls_ij,file)
pickle.dump(bounding_boxes_lonlat,file)
file.close()






