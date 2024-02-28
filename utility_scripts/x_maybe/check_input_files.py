import netCDF4
import numpy as np
from datetime import datetime

# ocean_time:long_name = "averaged time since initialization"
# ocean_time:units = "seconds since 1900-01-01 00:00:00"



history_base = '/home/blaughli/tracking_project/jerome_history_files/'
his_dir_year = 'Run_1988/'
#his_file_pre = 'wc15n_avg_year.nc'
his_file_pre = 'wc15n_avg_0001.nc'
his_file = history_base + his_dir_year + 'to_delete/' + his_file_pre


dset = netCDF4.Dataset(his_file, 'r')

u = np.array(dset['u'])
ocean_time = np.array(dset['ocean_time'])

ocean_time = ocean_time[0]

seconds_1900 = datetime(1900,1,1).timestamp()

ocean_time_adjusted = ocean_time + seconds_1900

starting_date = datetime.fromtimestamp(ocean_time_adjusted)
