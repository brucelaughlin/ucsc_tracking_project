
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

num_islands_intersecting = 4

island_isolines = []
island_coastlines = []
new_isolines = []


for island_dex in range(1,num_islands_intersecting+1):   
#for island_dex in range(1,3):   

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



# OK, it looks like the contours go clockwise, so their starting coordinates should be apparent from plots

#for island_dex in range(0,num_islands_intersecting-1):   
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
    # I think the higher of the 2 points comes first
    common_points = x.bounds
    cp_dex = 2

    # ok let's change these polygons.  a bit ad-hoc, hope it works generally
    # Assuming we can keep the first isoline point (ie it's not an intersection point)

    #new_isoline_1 = np.zeros((1,2))
    #new_isoline_2 = np.zeros((1,2))
    #new_isoline_1[0,:] = island_isolines[island_dex][0,:]
    #new_isoline_2[0,:] = island_isolines[island_dex+1][0,:]
    new_isoline_1 = np.empty((1,2), float)
    new_isoline_2 = np.empty((1,2), float)




    # Assuming there will only ever be 0 or 2 intersections, right?
    if len(common_points) > 0:

        # Treat the forst island's isoline
        # Isoline begins in the "dead zone"...
        
        cp_dex = 2
        iso_dex = 0
        
        for ii in range(0,len(island_isolines[island_dex])):
            if island_isolines[island_dex][ii,0] < common_points[cp_dex]:
                new_isoline_1 = np.vstack((new_isoline_1,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
                cp_dex = 0
                iso_dex = ii
                break
            
        for ii in range(iso_dex,len(island_isolines[island_dex])):
            #if island_isolines[island_dex][ii,0] > common_points[cp_dex] and island_isolines[island_dex][ii,0] < common_points[cp_dex+2]:
            if island_isolines[island_dex][ii,0] < common_points[cp_dex] and island_isolines[island_dex][ii,0] < common_points[cp_dex+2]:
                new_isoline_1 = np.vstack((new_isoline_1,island_isolines[island_dex][ii,:]))
            else:
                new_isoline_1 = np.vstack((new_isoline_1,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
                break


        # Treat the second island's isoline

        if island_dex + 1 == num_islands_intersecting:

            cp_dex = 0
            iso_dex = 0
            
            for ii in range(0,len(island_isolines[island_dex+1])):
                iso_dex += 1
                if island_isolines[island_dex+1][ii,0] > common_points[cp_dex]:
                    new_isoline_2 = np.vstack((new_isoline_2,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
                    cp_dex += 2
                    break
                
            for ii in range(iso_dex,len(island_isolines[island_dex+1])):
                if island_isolines[island_dex+1][ii,0] > common_points[cp_dex]: 
                    new_isoline_2 = np.vstack((new_isoline_2,island_isolines[island_dex+1][ii,:]))
                else:
                    new_isoline_2 = np.vstack((new_isoline_2,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
                    break

        else:

            cp_dex = 2
            iso_dex = 0

            for ii in range(0,len(island_isolines[island_dex+1])):
                iso_dex += 1
                if island_isolines[island_dex+1][ii,0] > common_points[cp_dex]:
                    new_isoline_2 = np.vstack((new_isoline_2,island_isolines[island_dex+1][ii,:]))
                else:
                    new_isoline_2 = np.vstack((new_isoline_2,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
                    cp_dex -= 2
                    break

            for ii in range(iso_dex,len(island_isolines[island_dex+1])):
                iso_dex += 1
                if island_isolines[island_dex+1][ii,0] > common_points[cp_dex]:
                    
                    new_isoline_2 = np.vstack((new_isoline_2,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
                    new_isoline_2 = np.vstack((new_isoline_2,island_isolines[island_dex+1][iso_dex:,:]))
                    break

      
    # The way I did things (creating "empty" array, then "appending", it seems the first entry
    # in each array is a pair of infinitesimal values
    new_isoline_1 = np.delete(new_isoline_1,0,0)
    new_isoline_2 = np.delete(new_isoline_2,0,0)

    island_isolines[island_dex] = new_isoline_1
    island_isolines[island_dex+1] = new_isoline_2


    # plotting to check.  these files loaded by other plotting script
    fig, ax = plt.subplots()
    ax.pcolormesh(lon_field,lat_field,mask,shading="nearest")
    zx=[x[0] for x in p]
    zy=[x[1] for x in p]
    zzx=[x[0] for x in q]
    zzy=[x[1] for x in q]
    #ax.plot(zx,zy)
    #ax.plot(zzx,zzy)
    ax.plot(new_isoline_1[:,0],new_isoline_1[:,1])
    ax.plot(new_isoline_2[:,0],new_isoline_2[:,1])


for island_dex in range(0,num_islands_intersecting-1):   

    output_file = input_dir + 'isodistance_lonlat_processed_v1_wc15_island_number_{}.p'.format(island_dex)
    file = open(output_file,'wb')
    pickle.dump(island_isolines[island_dex],file)
    file.close()













#
#    # Assuming there will only ever be 0 or 2 intersections, right?
#    if len(common_points) > 0:
#        
#        iso_dex = 1
#
#        for ii in range(0,len(island_isolines[island_dex])):
#            if island_isolines[island_dex][ii,0] < common_points[cp_dex]:
#                new_isoline_1 = np.vstack((new_isoline_1,island_isolines[island_dex][ii,:]))
#                iso_dex += 1
#            else:
#                new_isoline_1 = np.vstack((new_isoline_1,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
#                cp_dex += 2
#                break
#
#        for ii in range(iso_dex,len(island_isolines[island_dex])):
#            if island_isolines[island_dex][ii,0] > common_points[cp_dex]:
#                #new_isoline_1 = new_isoline_1.vstack((new_isoline_1,island_isolines[island_dex][ii,:])
#                iso_dex += 1
#            else:
#                new_isoline_1 = np.vstack((new_isoline_1,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
#                
#                new_isoline_1 = np.vstack((new_isoline_1,island_isolines[island_dex][iso_dex:,:]))
#
#                # Reset the common point index for use in the other polygon
#                cp_dex -= 2
#                break
#
#       
#        # Now treat the other island's isoline
#        # Hmm.. I think I designed things so that the first point in the second island's isoline
#        # is in the "dead zone"...
#        iso_dex = 1
#
#        for ii in range(0,len(island_isolines[island_dex+1])):
#            if island_isolines[island_dex+1][ii,0] > common_points[cp_dex]:
#                #new_isoline_2 = np.vstack((new_isoline_2,island_isolines[island_dex+1][ii,:]))
#                iso_dex += 1
#            else:
#                if cp_dex == 0:
#                    new_isoline_2 = np.vstack((new_isoline_2,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
#                    cp_dex += 2
#                new_isoline_2 = np.vstack((new_isoline_2,island_isolines[island_dex+1][ii,:]))
#                break
#
#        for ii in range(iso_dex,len(island_isolines[island_dex+1])):
#            if island_isolines[island_dex+1][ii,0] > common_points[cp_dex]:
#                #new_isoline_2 = new_isoline_2.vstack((new_isoline_2,island_isolines[island_dex+1][ii,:])
#                iso_dex += 1
#            else:
#                new_isoline_2 = np.vstack((new_isoline_2,np.array([common_points[cp_dex],common_points[cp_dex+1]])))
#                
#                new_isoline_2 = np.vstack((new_isoline_2,island_isolines[island_dex+1][iso_dex:,:]))
#
#                cp_dex += 2
#                break
#
#









