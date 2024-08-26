import glob
import netCDF4
import numpy as np
import matplotlib.pyplot as plt

#tracking_output_dir = '/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/var_input/z_output/'
tracking_output_dir = '/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/var_input/v_test_output/one_profile_per_box_10day_separation_study'
tracking_output_file_wildCard = tracking_output_dir + 'test_output_floats_*.nc'

tracking_output_file_list = []
for filename in glob.glob(tracking_output_file_wildCard):
    tracking_output_file_list.append(filename)
tracking_output_file_list.sort()

tracking_output_file = tracking_output_file_list[0]

dset = netCDF4.Dataset(tracking_output_file, 'r')

lon_truth = dset.variables['lon'][:]
lat_truth = dset.variables['lat'][:]
z_truth = dset.variables['z'][:]
dset.close()

tracking_output_file_list.pop(0)

num_floats = np.shape(lon_truth)[0]
num_days = int(np.shape(lon_truth)[1]/24)

lon_diffs = []
lat_diffs = []
z_diffs = []

timestep_strings = []

def mean_rmse(best,test):
    return (np.sqrt(np.mean((test-best)**2, axis = 0)))

for tfile in tracking_output_file_list:

    timestep_string_pre1 = tfile.split('calcDT_')
    timestep_string_pre2 = timestep_string_pre1[1].split('_')
    timestep_strings.append(timestep_string_pre2[0])

    dset = netCDF4.Dataset(tfile, 'r')
    
    lon = np.array(dset.variables['lon'][:])
    lat = np.array(dset.variables['lat'][:])
    z = np.array(dset.variables['z'][:])
    dset.close()

    lon_d = lon - np.array(lon_truth)
    lat_d = lat - np.array(lat_truth)
    z_d = z - np.array(z_truth)

    lon_diffs.append(list(mean_rmse(lon_truth,lon)))
    lat_diffs.append(list(mean_rmse(lat_truth,lat)))
    z_diffs.append(list(mean_rmse(z_truth,z)))


test_var = 'Longitude'
fig,ax = plt.subplots()
for ii in range(len(lon_diffs)):
    ax.plot(lon_diffs[ii][:],label = timestep_strings[ii])
plt.title("Separation study: {}\n{} floats, {} days".format(test_var,num_floats,num_days))
ax.set_xlabel("Simulation time (hours)")
ax.set_ylabel("RMSE difference \n from 1-minute timestep run \n (degrees longitude)")
ax.legend()
plt.show()


test_var = 'Latitude'
fig,ax = plt.subplots()
for ii in range(len(lat_diffs)):
    ax.plot(lat_diffs[ii][:],label = timestep_strings[ii])
plt.title("Separation study: {}\n{} floats, {} days".format(test_var,num_floats,num_days))
ax.set_xlabel("Simulation time (hours)")
ax.set_ylabel("RMSE difference \n from 1-minute timestep run \n (degrees latitude)")
ax.legend()
plt.show()


test_var = 'Depth'
fig,ax = plt.subplots()
for ii in range(len(z_diffs)):
    ax.plot(z_diffs[ii][:],label = timestep_strings[ii])
plt.title("Separation study: {}\n{} floats, {} days".format(test_var,num_floats,num_days))
ax.set_xlabel("Simulation time (hours)")
ax.set_ylabel("RMSE difference \n from 1-minute timestep run \n (depth in meters)")
ax.legend()
plt.show()






