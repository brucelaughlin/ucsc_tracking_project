#!/usr/bin/env python3



import pickle
import netCDF4
import numpy as np
import matplotlib.pyplot as plt

#RGI = spint.RegularGridInterpolator

base_path = '/home/blaughli/tracking_project/'
grid_directory = 'grid_data/'
grid_file_in = 'wc12_grd_no_islands.nc'
grid_path_in = base_path + grid_directory + grid_file_in

dset = netCDF4.Dataset(grid_path_in, 'r')
psi_mask = dset['mask_psi']
#rho_lon_grid = dset['lon_rho']
#rho_lat_grid = dset['lat_rho']
dset.close

psi = np.array(psi_mask)

file = open('coastline_coords_psi_file.p','rb')

coast_coords = pickle.load(file)

file.close

plt.pcolor(psi)
plt.plot(coast_coords[:,1],coast_coords[:,0],'r')



