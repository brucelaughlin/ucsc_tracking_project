# Study of separation between different runs, when varying calculation timestep
# V2: calculate distance between points, not just lat/lon differences

import glob
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import geopy.distance

tracking_output_dir = '/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/config_tests_2/separation_study_v2/z_output/'
tracking_output_file_wildCard = tracking_output_dir + 'test_output_*.nc'

tracking_output_file_list = []
for filename in glob.glob(tracking_output_file_wildCard):
    tracking_output_file_list.append(filename)
tracking_output_file_list.sort()

tracking_output_file = tracking_output_file_list[0]
#tracking_output_file = tracking_output_file_list[len(tracking_output_file_list) - 3]

dset = netCDF4.Dataset(tracking_output_file, 'r')

lon_baseline = dset.variables['lon'][:]
lat_baseline = dset.variables['lat'][:]
z_baseline = dset.variables['z'][:]
dset.close()

tracking_output_file_list.pop(0)

num_floats = np.shape(lon_baseline)[0]
num_days = int(np.shape(lon_baseline)[1]/24)

#lon_diffs = []
#lat_diffs = []
horz_diffs = []
z_diffs = []

timestep_strings = []

def mean_rmse(best,test):
    return (np.sqrt(np.mean((test-best)**2, axis = 0)))


fileCount = 0
#tfile = tracking_output_file_list[len(tracking_output_file_list) - 1]
for tfile in tracking_output_file_list:
#for ii in range(len(tracking_output_file_list)-2, len(tracking_output_file_list)):

#    tfile = tracking_output_file_list[ii]
    
    fileCount += 1

    timestep_string_pre1 = tfile.split('calcDT_')
    timestep_string_pre2 = timestep_string_pre1[1].split('_')
    timestep_strings.append(timestep_string_pre2[0])

    dset = netCDF4.Dataset(tfile, 'r')

    lon = np.array(dset.variables['lon'][:])
    lat = np.array(dset.variables['lat'][:])
    z = np.array(dset.variables['z'][:])
    dset.close()
    
    z_d = z - np.array(z_baseline)
    z_diffs.append(list(mean_rmse(z_baseline,z)))

    horz_d = np.empty_like(lon)
    for ii in range(np.shape(lon)[0]):
        print('{} of {}, {} of {}'.format(fileCount, len(tracking_output_file_list), ii, np.shape(lon)[0]))
        for jj in range(np.shape(lon)[1]):
            coords_baseline = (lat_baseline[ii,jj],lon_baseline[ii,jj])
            coords_test = (lat[ii,jj],lon[ii,jj])
            horz_d[ii,jj] = geopy.distance.geodesic(coords_baseline,coords_test).km

    horz_diffs.append(list(np.mean(horz_d, axis = 0)))
    
    #lon_d = lon - np.array(lon_baseline)
    #lat_d = lat - np.array(lat_baseline)

    #lon_diffs.append(list(mean_rmse(lon_baseline,lon)))
    #lat_diffs.append(list(mean_rmse(lat_baseline,lat)))





test_var = 'Horizontal Distance'
fig,ax = plt.subplots()
for ii in range(len(horz_diffs)):
    ax.plot(horz_diffs[ii][:],label = timestep_strings[ii])
plt.title("Separation study: {}\n{} floats, {} days".format(test_var,num_floats,num_days))
ax.set_xlabel("Simulation time (hours)")
ax.set_ylabel("Mean distance \n from 1-minute timestep run \n (km)")
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


#test_var = 'Longitude'
#fig,ax = plt.subplots()
#for ii in range(len(lon_diffs)):
#    ax.plot(lon_diffs[ii][:],label = timestep_strings[ii])
#plt.title("Separation study: {}\n{} floats, {} days".format(test_var,num_floats,num_days))
#ax.set_xlabel("Simulation time (hours)")
#ax.set_ylabel("RMSE difference \n from 1-minute timestep run \n (degrees longitude)")
#ax.legend()
#plt.show()
#
#
#test_var = 'Latitude'
#fig,ax = plt.subplots()
#for ii in range(len(lat_diffs)):
#    ax.plot(lat_diffs[ii][:],label = timestep_strings[ii])
#plt.title("Separation study: {}\n{} floats, {} days".format(test_var,num_floats,num_days))
#ax.set_xlabel("Simulation time (hours)")
#ax.set_ylabel("RMSE difference \n from 1-minute timestep run \n (degrees latitude)")
#ax.legend()
#plt.show()



