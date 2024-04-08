import os
import glob
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

#tracking_output_dir = '/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/var_input/z_output/'
#tracking_output_dir = '/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/var_input/v_test_output/one_profile_per_box_10day_separation_study'
#tracking_output_file_wildCard = tracking_output_dir + 'test_output_floats_*.nc'

cwd = os.getcwd()
#os.chdir(output_dir)

tracking_output_dir = cwd + '/z_output/'

tracking_output_file = tracking_output_dir + 'test_output_calcDT_060_saveDT_1440_buffer_100_nSeed_10.nc'

dset = netCDF4.Dataset(tracking_output_file, 'r')

lon = dset.variables['lon'][:]
lat = dset.variables['lat'][:]
#z = dset.variables['z'][:]

times = dset.variables['time'][:]

dset.close()

times = list(times)

base_datetime = datetime.datetime(1970,1,1,0,0,0)

times2 = []

for ii in range(len(times)):

    #times2[ii] = base_datetime + relativedelta(seconds = times[ii])
    timeTemp = base_datetime + relativedelta(seconds = times[ii])
    times2.append(timeTemp.date())


