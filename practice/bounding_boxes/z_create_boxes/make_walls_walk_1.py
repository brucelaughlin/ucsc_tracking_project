
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

RGI = spint.RegularGridInterpolator


base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc12_grd.nc.0'
grid_path_in = base_path + grid_directory + grid_file_in

dset = netCDF4.Dataset(grid_path_in, 'r')
lon_psi_grid = dset['lon_psi']
lat_psi_grid = dset['lat_psi']
dset.close

# create interpolator to get lat/lon at isoline points
lon = np.array(lon_psi_grid)
lat = np.array(lat_psi_grid)
x = np.arange(np.shape(lon)[0])
y = np.arange(np.shape(lon)[1])
rgi_lon = RGI([x,y],lon)
rgi_lat = RGI([x,y],lat)



# from https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

# want our boxes to be (at least?) 300km^2
# But wait!  I'm just gonna use i,j coordinates, for simplicity
# So, for wc_12, our grid cells are roughly 10kmx10km = 100km^2, right?
# box_area_threshold = 300e3

# So, want something at least "3 cells big"
# WAIT!!!  I used the 100km isodistance line, not 10km!  Because wc_12
# is low enough resolution that 10km is often "onshore"!
#box_area_threshold = 30
box_area_threshold = 300


#file = open('isodistance_ij_coords.p','rb')
file = open(base_path + 'practice/bounding_boxes/' +'isodistance_ij_coords.p','rb')
isoline_ij = pickle.load(file)
file.close
isoline_i = isoline_ij[:,0]
isoline_j = isoline_ij[:,1]

#isoline_lon = rgi_lon(isoline_i, isoline_j)
#isoline_lat = rgi_lat(isoline_i, isoline_j)
isoline_lon = rgi_lon((isoline_i, isoline_j))
isoline_lat = rgi_lat((isoline_i, isoline_j))

#lines = loadtxt("coast_coords_psi_i.txt", comments="#", delimiter=",", unpack=False)
coast_i = np.loadtxt("coast_coords_psi_i.txt",unpack=False)
coast_j = np.loadtxt("coast_coords_psi_j.txt",unpack=False)

num_points_coast = len(coast_i)
num_points_isoline = len(isoline_i)

coast_ij = np.zeros((len(coast_i),2))
coast_ij[:,0] = coast_i
coast_ij[:,1] = coast_j

walls_ij = []
walls_ij.append(np.array([[coast_ij[0,0],isoline_i[0]],[coast_ij[0,1],isoline_j[0]]]))

walk_switch = True

coast_dex = 1
isoline_dex = 1
wall_dex = 1

#for ii in range(1,num_points_coast-1):
while walk_switch == True:

    print("{},{}".format(str(coast_dex),str(num_points_coast)))

    polygon_i = []
    polygon_j = []

    # is this how i index numpy arrays?  from last element, want first elements of first and second row
    # I.E. start the polygon with the coastal i,j coords of the prevoius wall
    polygon_i.append(walls_ij[-1][0,0])
    polygon_j.append(walls_ij[-1][1,0])

    # walk up the coast
    #for point_coast in coast_ij[coast_dex:,coast_dex:]:
    for jj in range(coast_dex,num_points_coast):
        #cp_i = point_coast[0] 
        #cp_j = point_coast[1] 
        cp_i = int(coast_i[jj])
        cp_j = int(coast_j[jj]) 

        # append current coast points to polygon
        polygon_i.append(cp_i)
        polygon_j.append(cp_j)

        # see which remaining (ie not already used) isoline point is nearest
        dmax = 1e10
        closest_dex = None
        #for ii in range(isoline_dex,num_points_isoline+1):
        for ii in range(isoline_dex,num_points_isoline):
            dist = great_circle((lat[cp_i,cp_j],lon[cp_i,cp_j]),(isoline_lat[ii],isoline_lon[ii]))
            if dist < dmax: #and ii <= num_points_isoline:
                dmax = dist
                closest_dex = ii

        polygon_test_i = polygon_i
        polygon_test_j = polygon_j

        for ii in range(closest_dex,isoline_dex-1,-1):
            polygon_test_i.append(isoline_i[ii])
            polygon_test_j.append(isoline_j[ii])

        # add final polygon if we used the final isoline or coast point
        if closest_dex == num_points_isoline-1 or jj == num_points_coast-1:
            walls_ij.append(np.array([[coast_i[-1],isoline_i[-1]],[coast_j[-1],isoline_j[-1]]]))
            walk_switch = False
            print(str(PolyArea(polygon_i,polygon_j)))
            break

        if PolyArea(polygon_i,polygon_j) >= box_area_threshold:
            walls_ij.append(np.array([[cp_i,isoline_i[closest_dex]],[cp_j,isoline_j[closest_dex]]]))
            isoline_dex = closest_dex + 1
            coast_dex = jj + 1

            print(str(PolyArea(polygon_i,polygon_j)))
            print('\n')

            break


file = open('wall_ij_coords.p','wb')
pickle.dump(walls_ij,file)
file.close()






