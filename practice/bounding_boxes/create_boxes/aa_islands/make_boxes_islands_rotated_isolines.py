# lat/lon area calc taken from:
# https://stackoverflow.com/questions/68118907/shapely-pyproj-find-area-in-m2-of-a-polygon-created-from-latitude-and-longi


# Using the island coastlines, including the "blob" of islands 1-4, along with the rotated isolines (ie starting points of isolines
# correspond with starting points of coastlines).
# Idea: split each island into two halves, an upper and lower, using the "bounding points" previously determined.  Then proceed
# as if doing the box calculations for two separate coastlines and isolines


# NOTE: I stored the 2nd isoline bounding point as a negative number.  So address that accordingly.  


import netCDF4
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from geopy.distance import great_circle
import scipy.interpolate as spint
import ast

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
lon_field = np.array(dset['lon_{}'.format(points_type_field)])
lat_field = np.array(dset['lat_{}'.format(points_type_field)])
mask = np.array(dset['mask_{}'.format(points_type_field)])

dset.close


box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'aa_islands/'
input_dir = box_dir + islands_dir + 'z_output/'


# Set box area threshold (should be 300km^2, right?)
#box_area_threshold = 3e7
box_area_threshold = 3e8
#---------------------------------------------------------------------
#---------------------------------------------------------------------

# For calculating area
geod = Geod(ellps="WGS84")


# load coastline artifical bounding endpoint coordinates
file = open(box_dir + islands_dir + 'island_coastline_bounding_points.txt','r')
coastline_bp_list = file.read().splitlines()
file.close()
coastline_bp_list = [ast.literal_eval(el) for el in coastline_bp_list]

# load isoline artifical bounding endpoint coordinates
file = open(box_dir + islands_dir + 'island_isoline_bounding_points_rotated.txt','r')
isoline_bp_list = file.read().splitlines()
file.close()
isoline_bp_list = [ast.literal_eval(el) for el in isoline_bp_list]



num_islands = 8

num_last_blob_island = 4

for island_dex in range(num_last_blob_island,num_islands+1):
#for island_dex in range(num_last_blob_island,num_last_blob_island+1):
#for island_dex in range(6,7):

    print('\n')
    print('\n')
    print('island number: {}'.format(island_dex))
    print('\n')
    print('\n')

    # Set an index for the bounding point lists (the lists of points used to split the coastlines and isolines)
    bp_dex = island_dex-num_last_blob_island

    # Load coastline and isoline coordinates
    if island_dex == num_last_blob_island:

        coastline_inshore_file_in = input_dir + 'coastline_coords_wc15n_island_1_through_4_combined_inshore.p'
        coastline_offshore_file_in = input_dir + 'coastline_coords_wc15n_island_1_through_4_combined_offshore.p'
        isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15n_island_1_through_4_blob_rotated.p'

        # Load the coastlines
        file = open(coastline_inshore_file_in,'rb')
        coastline_lonlat_1 = pickle.load(file)
        file.close
        file = open(coastline_offshore_file_in,'rb')
        coastline_lonlat_2 = pickle.load(file)
        file.close
        coastline_lonlat = np.append(coastline_lonlat_1,coastline_lonlat_2,axis=0)

    else:
        coastline_file_in = input_dir + 'coastline_coords_wc15n_island_number_{}.p'.format(island_dex)
        isoline_file_in = input_dir + 'isodistance_lonlat_coords_rho_coastline_wc15n_island_number_{}_rotated.p'.format(island_dex)

        # Load the coastlines
        file = open(coastline_file_in,'rb')
        coastline_lonlat = pickle.load(file)
        file.close
        coastline_lonlat = coastline_lonlat[0]

    # Load the isolines
    file = open(isoline_file_in,'rb')
    isoline_lonlat = pickle.load(file)
    file.close



    for inoffshore_switch in range(0,2):
    
        if inoffshore_switch == 0:
            bounding_boxes_file_out = input_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_inshore.p'.format(island_dex)
        else:
            bounding_boxes_file_out = input_dir + 'bounding_boxes_lonlat_wc15n_island_number_{}_offshore.p'.format(island_dex)

        if inoffshore_switch == 0:
            coast_lon = list(coastline_lonlat[0:coastline_bp_list[bp_dex][1]+1,0])
            coast_lat = list(coastline_lonlat[0:coastline_bp_list[bp_dex][1]+1,1])
            isoline_lon = list(isoline_lonlat[0:isoline_bp_list[bp_dex][1]+1,0])
            isoline_lat = list(isoline_lonlat[0:isoline_bp_list[bp_dex][1]+1,1])
        else:
            coast_lon = list(coastline_lonlat[coastline_bp_list[bp_dex][1]:,0])
            coast_lat = list(coastline_lonlat[coastline_bp_list[bp_dex][1]:,1])
            isoline_lon = list(isoline_lonlat[isoline_bp_list[bp_dex][1]:,0])
            isoline_lat = list(isoline_lonlat[isoline_bp_list[bp_dex][1]:,1])
            #coast_lon = list(coastline_lonlat[coastline_bp_list[bp_dex][1]:,0]) + [coastline_lonlat[0,0]]
            #coast_lat = list(coastline_lonlat[coastline_bp_list[bp_dex][1]:,1]) + [coastline_lonlat[0,1]]
            #isoline_lon = list(isoline_lonlat[isoline_bp_list[bp_dex][1]:,0]) + [isoline_lonlat[0,0]]
            #isoline_lat = list(isoline_lonlat[isoline_bp_list[bp_dex][1]:,1]) + [isoline_lonlat[0,1]]

        num_points_coast = len(coast_lon)
        num_points_isoline = len(isoline_lon)

        bounding_boxes_lonlat = []

        walk_switch = True

        coast_dex = 1
        isoline_dex = 1

        closees_dex = 0

        while walk_switch == True:

            print('\n')
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


                #print('jj = {}, closest_dex = {}'.format(jj,closest_dex))


                # THIS MUST CHANGE, ESPECIALLY FOR ISLANDS - WANT BALANCED BOXES, SO NEED TO 
                # CHANGE THRESHOLD AND REOCMPUTE IF LAST BOX IS TOO LARGE/SMALL

                # ALSO, CHRIS WANTS TO JUST ADD THE LAST BOX TO THE PREVIOUS, NOT MAKE A SMALL ONE
                # AS I DO HERE

                # add final polygon if we used the final isoline or coast point
                if closest_dex == num_points_isoline-1 or jj == num_points_coast-1:

                    #print('\n')
                    #print('jj = {}, num_points_coast-1 = {}'.format(jj,num_points_coast-1))

                    #if jj == num_points_coast-1:
                    #    polygon_lon = polygon_wall_onshore_lon[:] + isoline_lon[-1:isoline_dex-2:-1]
                    #    polygon_lat = polygon_wall_onshore_lat[:] + isoline_lat[-1:isoline_dex-2:-1]
                    
                    if jj == num_points_coast-1:
                        # Must handle the case where we haven't added a single box yet, and therefore need to just create one final box
                        if len(bounding_boxes_lonlat) == 0:
                            polygon_lon = coast_lon[:] + isoline_lon[::-1]
                            polygon_lat = coast_lat[:] + isoline_lat[::-1]
                        else:
                            #polygon_lon = polygon_wall_onshore_lon[:] + isoline_lon[-1:isoline_dex-2:-1]
                            #polygon_lat = polygon_wall_onshore_lat[:] + isoline_lat[-1:isoline_dex-2:-1]
                            polygon_lon = polygon_wall_onshore_lon[:] + isoline_lon[:isoline_dex-2:-1]
                            polygon_lat = polygon_wall_onshore_lat[:] + isoline_lat[:isoline_dex-2:-1]

                    else: 
                        polygon_wall_onshore_lon.append(coast_lon[jj+1:])
                        polygon_wall_onshore_lat.append(coast_lat[jj+1:])
                        #polygon_lon = polygon_wall_onshore_lon[:] + isoline_lon[-1:isoline_dex-2:-1]
                        #polygon_lat = polygon_wall_onshore_lat[:] + isoline_lat[-1:isoline_dex-2:-1]
                        polygon_lon = polygon_wall_onshore_lon[:] + isoline_lon[:isoline_dex-2:-1]
                        polygon_lat = polygon_wall_onshore_lat[:] + isoline_lat[:isoline_dex-2:-1]

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
                    print('final automatically generated polygon area: {}'.format(str(poly_area)))
                    
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
                
                polygon_test = Polygon(polygon_test_list)
                poly_area, poly_perimeter = geod.geometry_area_perimeter(polygon_test)
                
                if poly_area >= box_area_threshold:

                    bounding_boxes_lonlat.append(np.array([polygon_lon,polygon_lat]))

                    isoline_dex = closest_dex + 1
                    coast_dex = jj + 1

                    print('polygon area: {},  threshold: {}'.format(poly_area,box_area_threshold))
                    print('island number: {}'.format(island_dex))
                    print('\n')

                    break


        file = open(bounding_boxes_file_out,'wb')
        pickle.dump(bounding_boxes_lonlat,file)
        file.close()


    bp_dex += 1



