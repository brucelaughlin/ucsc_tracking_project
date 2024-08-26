# Comparing (near?) terminal positions when different output timesteps are used

import os
import glob
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import geopy.distance

cwd = os.getcwd()
tracking_output_dir = cwd + '/z_output/'
tracking_output_file_wildCard = tracking_output_dir + 'test_output_*.nc'

tracking_output_file_list = []
for filename in glob.glob(tracking_output_file_wildCard):
    tracking_output_file_list.append(filename)
tracking_output_file_list.sort()

horz_diffs = []

timestep_strings = []
timestep_floats = []

fileCount = 0
#tfile = tracking_output_file_list[len(tracking_output_file_list) - 1]
for tfile in tracking_output_file_list:
#for ii in range(len(tracking_output_file_list)-2, len(tracking_output_file_list)):

#    tfile = tracking_output_file_list[ii]
    
    fileCount += 1

    timestep_string_pre1 = tfile.split('saveDT_')
    timestep_string_pre2 = timestep_string_pre1[1].split('_')
    #timestep_strings.append(int(int(timestep_string_pre2[0])/60))
    timestep_strings.append(str(float(timestep_string_pre2[0])/60))
    timestep_floats.append(float(timestep_string_pre2[0])/60)

    dset = netCDF4.Dataset(tfile, 'r')

    lon = np.array(dset.variables['lon'][:])
    lat = np.array(dset.variables['lat'][:])
    dset.close()
    
    n_floats = np.shape(lon)[0]
    n_timesteps = np.shape(lon)[1]

    horz_d = np.zeros((n_floats,1))

    for ii in range(n_floats):
        coords_penultimate = (lat[ii,n_timesteps-2],lon[ii,n_timesteps-2])
        coords_ultimate = (lat[ii,n_timesteps-1],lon[ii,n_timesteps-1])
        horz_d[ii] = geopy.distance.geodesic(coords_penultimate,coords_ultimate).km

    #horz_diffs.append(list(np.mean(horz_d, axis = 0)))
    horz_diffs.append(float(np.mean(horz_d, axis = 0)))
 
#print(timestep_strings)

test_line_y = [horz_diffs[0],horz_diffs[-1]]
test_line_x = [timestep_floats[0],timestep_floats[-1]]

test_var = 'Horizontal Distance'
fig,ax = plt.subplots()
#ax.plot(horz_diffs)
#ax.plot(test_line_x[:],test_line_y[:],color='r')
ax.plot(timestep_floats[:],horz_diffs[:],marker='*')
plt.title("Separation Study:\n Distance between penultimate and ultimate saved positions\n as a function of output timestep.\n (all other parameters equal)")
ax.set_xlabel("Output timestep (hours)")
ax.set_ylabel("Distance between final 2 positions (km)")
#ax.set_xticks(range(len(timestep_strings)))
#ax.set_xticklabels(timestep_strings)
plt.grid()

# ripped from SO
for i_x, i_y in zip(timestep_floats,horz_diffs):
    plt.text(i_x, i_y, '({}, {:.01f})'.format(i_x, i_y))

plt.show()


