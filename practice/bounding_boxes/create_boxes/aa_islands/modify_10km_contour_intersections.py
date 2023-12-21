
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

num_islands = 8

island_isolines = []
island_coastlines = []

#for island_dex in range(1,num_islands+1):   
for island_dex in range(1,3):   

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



#for island_dex in range(0,num_islands-1):   
for island_dex in range(0,1):   

    # subtract lattitudes of the isolines, to see where sign changes 
    #idx = np.argwhere(np.diff(np.sign(island_isolines[island_dex][:,1] - island_isolines[island_dex-1][:,1]))).flatten()
    
    p = []
    for ii in range(len(island_isolines[island_dex])):
        p.append((island_isolines[island_dex][ii,0],island_isolines[island_dex][ii,1]))
    
    q = []
    for ii in range(len(island_isolines[island_dex+1])):
        q.append((island_isolines[island_dex+1][ii,0],island_isolines[island_dex+1][ii,1]))


    pp = Polygon(p) 
    qq = Polygon(q)
    x = pp.intersection(qq)

    # This returns an nx2 element tuple, where n is the number of intersections.
    # the elements alternate as lon,lat
    common_points = x.bounds
    cp_dex = 0

    # ok let's change these polygons.  a bit ad-hoc, hope it works generally
    # Assuming we can keep the first isoline point (ie it's not an intersection point)

    new_isoline_1 = np.zeros((1,2))
    new_isoline_2 = np.zeros((1,2))
    new_isoline_1[0,:] = island_isolines[island_dex][0,:]
    new_isoline_2[0,:] = island_isolines[island_dex+1][0,:]


    # Assuming there will only ever be 0 or 2 intersections, right?
    if len(common_points) > 0:
        
        iso_dex = 1

        for ii in range(1,len(island_isolines[island_dex])):
            if island_isolines[island_dex][ii,0] < common_points[cp_dex]:
                new_isoline_1 = np.vstack((new_isoline_1,island_isolines[island_dex][ii,:]))
                iso_dex += 1
            else:
                new_isoline_1 = np.vstack((new_isoline_1,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
                cp_dex += 2
                break

        for ii in range(iso_dex,len(island_isolines[island_dex])):
            if island_isolines[island_dex][ii,0] > common_points[cp_dex]:
                #new_isoline_1 = new_isoline_1.vstack((new_isoline_1,island_isolines[island_dex][ii,:])
                iso_dex += 1
            else:
                new_isoline_1 = np.vstack((new_isoline_1,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
                
                new_isoline_1 = np.vstack((new_isoline_1,island_isolines[island_dex][iso_dex:,:]))

                # Reset the common point index for use in the other polygon
                cp_dex -= 2
                break

       
        # Now treat the other island's isoline
        # Hmm.. I think I designed things so that the first point in the second island's isoline
        # is in the "dead zone"...
        iso_dex = 1

        for ii in range(1,len(island_isolines[island_dex+1])):
            if island_isolines[island_dex+1][ii,0] > common_points[cp_dex]:
                #new_isoline_2 = np.vstack((new_isoline_2,island_isolines[island_dex+1][ii,:]))
                iso_dex += 1
            else:
                if cp_dex = 0:
                    new_isoline_2 = np.vstack((new_isoline_2,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
                    cp_dex += 2
                new_isoline_2 = np.vstack((new_isoline_2,island_isolines[island_dex+1][ii,:]))
                break

        for ii in range(iso_dex,len(island_isolines[island_dex+1])):
            if island_isolines[island_dex+1][ii,0] > common_points[cp_dex]:
                #new_isoline_2 = new_isoline_2.vstack((new_isoline_2,island_isolines[island_dex+1][ii,:])
                iso_dex += 1
            else:
                new_isoline_2 = np.vstack((new_isoline_2,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
                
                new_isoline_2 = np.vstack((new_isoline_2,island_isolines[island_dex+1][iso_dex:,:]))

                cp_dex += 2
                break











