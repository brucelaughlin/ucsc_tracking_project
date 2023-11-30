
import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from skimage import measure
#from geopy import distance
#from scipy import interpolate
import scipy.interpolate as spint



# Load the "distance field" - plot over this
dist_field_file = 'dist_2_coast_field_wc12.mat'
dist_field = scipy.io.loadmat(dist_field_file)
dist_field = dist_field['dist_field']


# Load coast
file = open('coastline_coords_psi_file.p','rb')
coast_ij = pickle.load(file)
file.close


# Load offshore boundary
file = open('isodistance_ij_coords.p','rb')
isodist_ij = pickle.load(file)
file.close

# Load the walls
file = open('wall_ij_coords.p','rb')
walls_ij = pickle.load(file)
file.close



fig, ax = plt.subplots()
ax.pcolormesh(np.transpose(dist_field))

ax.plot(isodist_ij[:,1],isodist_ij[:,0],linewidth=2)
ax.plot(coast_ij[:,1],coast_ij[:,0],linewidth=2)

for wall in walls_ij:
    if wall is not None:
        #ax.plot(wall[0],wall[1])
        ax.plot(wall[1],wall[0])





ax.axis('image')
plt.show()









