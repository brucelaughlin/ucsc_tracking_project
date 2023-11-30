
# I think that I have reversed i and j in all of this work.
# i think that i corresponds roughly to longitude, and j to lattitude

# Ok, imagine that West is up  So X = rows, Y = cols

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

#walls_offshore_ij = []
#walls_onshore_ij = []
walls_ij = []

#for ii in range(num_points -1):
    
# Make box "every 3 points"
save_dex = 0
h = np.arange(1,num_points-1,3)
for ii in np.arange(1,num_points-1,3):

    #ii = 1+dex*points_jump
    save_dex += 1
    
    # define vectors
    dx = coast_i[ii+1] - coast_i[ii-1]
    dy = coast_j[ii+1] - coast_j[ii-1]
    mx = (coast_i[ii+1] + coast_i[ii-1])/2
    my = (coast_j[ii+1] + coast_j[ii-1])/2

    # unit normalized perpendicular vector components
    l = np.sqrt(dx**2 + dy**2)
    ux = -dy/l
    uy = dx/l
    
    # go 4 units in both directions
    step = 100
    x1 = mx + ux*step
    y1 = my + uy*step
    x0 = mx - ux*step
    y0 = my - uy*step
    
    # A hack to try to make this method work
    # Problem: we can't subtract two curves if one
    # of them is just a vertical line.  So, add a
    # small offset, to give the vertical line a
    # non-infinite slope
    if x1-x0 == 0:
        x1 += 1e-2

    
    # j or "y" is actually our "domain" for our "curves"
    # yeah... may need to reverse some things...
    
    yp = [y0,y1]
    xp = [x0,x1]
    f1 = interp1d(xp,yp, kind = 'linear')
    f2 = interp1d(isodist_i,isodist_j, kind = 'linear',fill_value="extrapolate")
    xx = np.linspace(max(xp[0], isodist_i[0]), min(xp[-1], isodist_i[-1]), 1000)
    y1_interp = f1(xx)
    y2_interp = f2(xx)
    idx = np.argwhere(np.diff(np.sign(y1_interp - y2_interp))).flatten()

    # Store wall endpoints in array
    # First row = wall i coords
    # Second row = wall j coords
    if len(idx) == 0:
        walls_ij.append(None)
    else:
        walls_ij.append(np.array([[mx,xx[idx][0]],[my,y2_interp[idx][0]]]))


file = open('wall_ij_coords.p','wb')
pickle.dump(walls_ij,file)
file.close()






