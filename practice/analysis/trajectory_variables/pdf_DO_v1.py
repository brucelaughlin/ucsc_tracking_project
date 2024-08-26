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
tracking_output_dir = '/data03/blaughli/tracking_project_output/test3_physics_only/'
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



tracking_output_files = [f for f in listdir(tracking_output_dir) if isfile(join(tracking_output_dir,f))]
tracking_output_files.sort()



tracking_output_file = tracking_output_dir + tracking_output_files[0]
dset = netCDF4.Dataset(tracking_output_file, 'r')

oxygen_all = dset.variables['oxygen'][:]
temp_all = dset.variables['sea_water_temperature'][:]

particle_labels = dset.variables['trajectory'][:]
lon_all = dset.variables['lon'][:]
lat_all = dset.variables['lat'][:]
z_all = dset.variables['z'][:]
status_all = dset.variables['status'][:]
time = np.array(dset['time'])

o2_test = dset.variables['oxygen']

dset.close()


oxygen_all *= conversionFactor
















