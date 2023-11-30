
# I think that I have reversed i and j in all of this work.
# i think that i corresponds roughly to longitude, and j to lattitude

import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

file = open('isodistance_ij_coords.p','rb')
isodist_ij = pickle.load(file)
file.close
isodist_i = isodist_ij[:,0]
isodist_j = isodist_ij[:,1]


#lines = loadtxt("coast_coords_psi_i.txt", comments="#", delimiter=",", unpack=False)
coast_i = np.loadtxt("coast_coords_psi_i.txt",unpack=False)
coast_j = np.loadtxt("coast_coords_psi_j.txt",unpack=False)

num_points = len(coast_i)

coast_ij = np.zeros((len(coast_i),2))

coast_ij[:,0] = coast_i
coast_ij[:,1] = coast_j


for ii in range(num_points -1):
    
    # define vectors
    dx = coast_i[ii+1] - coast_i[ii]
    dy = coast_j[ii+1] - coast_j[ii]
    mx = (coast_i[ii+1] + coast_i[ii])/2
    my = (coast_j[ii+1] + coast_j[ii])/2

    # unit normalized perpendicular vector components
    l = np.sqrt(dx**2 + dy**2)
    ux = -dy/l
    uy = dx/l
    
    # go 4 units in both directions
    step = 4
    x1 = mx + ux*step
    y1 = my + uy*step
    x0 = mx - ux*step
    y0 = my - uy*step
    
    # j or "y" is actually our "domain" for our "curves"
    # yeah... may need to reverse some things...
    
    yp = [y0,y1]
    xp = [x0,x1]
    
    
    #f1 = interp1d(x1, yp, kind = 'linear')
    #f2 = interp1d(x2, y2, kind = 'linear')
    #f1 = interp1d(yp,xp, kind = 'linear')
    f2 = interp1d(coast_j,coast_i, kind = 'linear')
    f1 = interp1d(yp,xp, kind = 'linear',fill_value="extrapolate")
    #f2 = interp1d(coast_j,coast_i, kind = 'linear',fill_value="extrapolate")
    
    #xx = np.linspace(max(x1[0], x2[0]), min(x1[-1], x2[-1]), 1000)
    #yy = np.linspace(max(yp[0], coast_j[0]), min(yp[-1], coast_j[-1]), 1000)
    yy = np.linspace(max(yp[0], coast_j[0]), min(yp[-1], coast_j[-1]), 1000)





    #y1_interp = f1(xx)
    #y2_interp = f2(xx)
    x1_interp = f1(yy)
    x2_interp = f2(yy)
    
    
    #idx = np.argwhere(np.diff(np.sign(y1_interp - y2_interp))).flatten()
    idy = np.argwhere(np.diff(np.sign(x1_interp - x2_interp))).flatten()













