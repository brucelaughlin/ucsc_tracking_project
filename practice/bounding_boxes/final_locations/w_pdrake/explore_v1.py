
import numpy as np
import netCDF4


pld_array = np.array([[5,6],[10,11],[15,17],[20,22],[30,33],[45,49],[60,65],[90,98],[120,131],[150,164],[180,197]])



tracking_output_file = '/home/blaughli/tracking_project/y_pdrake_data/fwd_data/sub_set/one_file/offline_flt_1999_APR.nc'

dset = netCDF4.Dataset(tracking_output_file, 'r')

lon_all = dset.variables['lon'][:]
time = np.array(dset['ocean_time'])
dset.close()

num_particles = np.shape(lon_all)[1]


timesteps_per_day = 2

pld_dex = 0


first_settlement_day = pld_array[pld_dex,0]
last_settlement_day = pld_array[pld_dex,1]


# THIS is the v5 adjustment: need to only use data from the pld, which begins after "first_settlement_day" and ends after "last_settlement_day"
pld_length_days = last_settlement_day - first_settlement_day + 1


timesteps_settlement_window = pld_length_days * timesteps_per_day
timesteps_full_run = (last_settlement_day+1) * timesteps_per_day + 1


first_settle_dex = first_settlement_day * timesteps_per_day +1
last_settle_dex = (last_settlement_day+1) * timesteps_per_day + 1







drift_lons = np.zeros((num_particles,timesteps_settlement_window))


# since I'm deleting rows, need to manually update the particle index
particle_id_adjusted = 0

for particle_id in range(num_particles):



    #particle_id = 2


    particle_lon = lon_all[:,particle_id]

    particle_lon_pre = particle_lon

    particle_lon = particle_lon[~particle_lon.mask].data



    if len(particle_lon) < first_settle_dex:
        if len(particle_lon) == 0:
            print('id of bad particle: {}'.format(particle_id))
#        drift_lons = np.delete(drift_lons,(particle_id_adjusted),axis=0)
        continue
    elif len(particle_lon) < last_settle_dex:
        drift_lons[particle_id,0:len(particle_lon)-first_settle_dex] = particle_lon[first_settle_dex:]
        #drift_lons[particle_id_adjusted,0:len(particle_lon)-first_settle_dex] = particle_lon[first_settle_dex:]
    else:
        drift_lons[particle_id,:] = particle_lon[first_settle_dex:last_settle_dex]
        #drift_lons[particle_id_adjusted,:] = particle_lon[first_settle_dex:last_settle_dex]

#    particle_id_adjusted = particle_id_adjusted + 1


    #drift_lons[particle_id,:] = particle_lon[first_settle_dex:last_settle_dex]
