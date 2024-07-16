# Moving towards exposure statistics

# Looking at Jerome's files: 
#    float oxygen(ocean_time,s_rho,eta_rho,xi_rho) ;
#      oxygen:long_name = "time-averaged dissolved oxygen concentration" ;
#      oxygen:units = "millimole_oxygen meter-3" ;

# desired units: mg/L

molarMassO2 = 31.999 # g/mol

conversionFactor = molarMassO2/1000  #worked this out on papre



# Input Files
#---------------------------------------------------------------------
#tracking_output_dir = '/data03/blaughli/tracking_project_output/z_one_file_test/'
tracking_output_dir_1 = '/data03/blaughli/tracking_project_output/test3_physics_only/'
tracking_output_dir_2 = '/data03/blaughli/tracking_project_output/test4_physics_only_AKs_1en5/'
#---------------------------------------------------------------------



import datetime
import netCDF4
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as plt_path
from scipy.interpolate import interp1d
from geopy.distance import great_circle
import scipy.interpolate as spint
from os import listdir
from os.path import isfile, join
import sys

#---------------------------------------------------------------------
# Need to know the number of DAYS of each particle's life (fixed unless I change the
# the deactivation time in the model code)
run_length_days = 91


# Save the number of days in the drifting window before the settlement window opens
first_settlement_day = 30

# Opendrift output times are seconds since Jan 1, 1979
base_datetime = datetime.datetime(1970,1,1,0,0,0)



tracking_output_files_1 = [f for f in listdir(tracking_output_dir_1) if isfile(join(tracking_output_dir_1,f))]
tracking_output_files_1.sort()

tracking_output_files_2 = [f for f in listdir(tracking_output_dir_2) if isfile(join(tracking_output_dir_2,f))]
tracking_output_files_2.sort()


tracking_output_file = tracking_output_dir_1 + tracking_output_files_1[0]
dset = netCDF4.Dataset(tracking_output_file, 'r')

particle_labels_1 = dset.variables['trajectory'][:]
lon_all_1 = dset.variables['lon'][:]
lat_all_1 = dset.variables['lat'][:]
z_all_1 = dset.variables['z'][:]
status_all_1 = dset.variables['status'][:]
time_1 = np.array(dset['time'])
oxygen_all_1 = dset.variables['oxygen'][:]
temp_all_1 = dset.variables['sea_water_temperature'][:]

dset.close()

oxygen_all_1 *= conversionFactor


tracking_output_file = tracking_output_dir_2 + tracking_output_files_2[0]
dset = netCDF4.Dataset(tracking_output_file, 'r')

particle_labels_2 = dset.variables['trajectory'][:]
lon_all_2 = dset.variables['lon'][:]
lat_all_2 = dset.variables['lat'][:]
z_all_2 = dset.variables['z'][:]
status_all_2 = dset.variables['status'][:]
time_2 = np.array(dset['time'])
oxygen_all_2 = dset.variables['oxygen'][:]
temp_all_2 = dset.variables['sea_water_temperature'][:]

dset.close()

oxygen_all_2 *= conversionFactor


o2_diff = oxygen_all_1 - oxygen_all_2
num_data = np.shape(o2_diff)[0]*np.shape(o2_diff)[1] - np.ma.count_masked(o2_diff)
num_diff_o2 =  np.sum(o2_diff > 0) + np.sum(o2_diff < 0) 
fraction_diff_o2 = num_diff_o2/num_data


temp_diff = temp_all_1 - temp_all_2
num_diff_temp =  np.sum(temp_diff > 0) + np.sum(temp_diff < 0) 
fraction_diff_temp = num_diff_temp/num_data


lon_diff = lon_all_1 - lon_all_2
num_diff_lon =  np.sum(lon_diff > 0) + np.sum(lon_diff < 0) 
fraction_diff_lon = num_diff_lon/num_data


z_diff = z_all_1 - z_all_2
num_diff_z =  np.sum(z_diff > 0) + np.sum(z_diff < 0) 
fraction_diff_z = num_diff_z/num_data


plt.pcolormesh(z_diff)
plt.title("Differences in depth between runs with fallback AKs of 0.1 and 0.00001 m$^{2}$/s, single output file (1 out of 208)")
plt.ylabel("particle number")
plt.xlabel("output timestep (days)")

clb = plt.colorbar()
clb.ax.set_ylabel("depth difference (m)")

plt.show()






