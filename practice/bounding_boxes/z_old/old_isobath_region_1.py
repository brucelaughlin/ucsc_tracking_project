# idea: Start by using the 250m isobath, and drawing regions with that as the
# west wall.  Initially, can just draw lines directly east every 10km along the
# isobath, or something like that.  Later, can perhaps make the bounding
# lines have nonzero slopes (ie perpendiculur to the coast), and perhaps we
# should also try having the west line be 10km off of the coast (which feels
# harder, since I don't currently know how to compute the coast (do we have
# a coastline file, and is it easy to use?))


import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
from geopy import distance
#from scipy import interpolate
import scipy.interpolate as spint

RGI = spint.RegularGridInterpolator

base_path = '/home/blaughli/tracking_project/'
his_directory = 'history_files/'
his_file_in = 'wc12_his_v0_base.nc'
his_path_in = base_path + his_directory + his_file_in

dset = netCDF4.Dataset(his_path_in, 'r')
h_grid = dset['h']
rho_lon_grid = dset['lon_rho']
rho_lat_grid = dset['lat_rho']
dset.close

h = np.array(h_grid)
lon = np.array(rho_lon_grid)
lat = np.array(rho_lat_grid)




#h = np.transpose(h)



isobath_depth = 20
contours = measure.find_contours(h, isobath_depth)

# Assume that the longest contour returned is the one we want....
max_length = 0
contour_index = 0
dex = 0
for contour in contours:
    if np.shape(contour)[0] > max_length:
        max_length = np.shape(contour)[0]
        contour_index = dex
    dex += 1
    
isobath_ij = contours[contour_index]


x = np.arange(np.shape(lon)[0])
y = np.arange(np.shape(lon)[1])

rgi_lon = RGI([x,y],lon)
rgi_lat = RGI([x,y],lat)


isobath_lon = rgi_lon((isobath_ij[:,0], isobath_ij[:,1]))
isobath_lat = rgi_lat((isobath_ij[:,0], isobath_ij[:,1]))


fig, ax = plt.subplots()
ax.pcolormesh(lon,lat,h)
ax.plot(isobath_lon,isobath_lat,linewidth=2)
ax.axis('image')
plt.show()

# =============================================================================
# # Display the image and plot all contours found
# fig, ax = plt.subplots()
# ax.imshow(h, cmap=plt.cm.gray)
# 
# ax.plot(isobath[:, 1], isobath[:, 0], linewidth=2)
# 
# #for contour in contours:
# #    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
# 
# 
# ax.axis('image')
# #ax.set_xticks([])
# #ax.set_yticks([])
# plt.show()
# =============================================================================



# =============================================================================
# outFile = open(r'{}'.format(seed_path_out),"w")
# 
# for depth in profile_initial:
#     outFile.write('{}, {}, {}, {}\n'.format(test_point_lon,test_point_lat,depth,start_time))
# 
# outFile.close()
# 
# 
# dset.close()
# =============================================================================






