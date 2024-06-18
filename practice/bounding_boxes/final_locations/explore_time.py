import numpy as np
import netCDF4
import datetime



fp = "/data03/blaughli/tracking_project_output/test2_physics_only/tracking_output_calcDT_060_saveDT_1440_buffer_100_nSeed_020_startNudge_000000.nc"

dset  = netCDF4.Dataset(fp, 'r')

time = np.array(dset['time'])

base_datetime = datetime.datetime(1970,1,1,0,0,0)

b = datetime.datetime.strptime(str(base_datetime+datetime.timedelta(seconds=time[-1])), '%Y-%m-%d %H:%M:%S')

seed_months = []

for t in time:
    seed_months.append(datetime.datetime.strptime(str(base_datetime+datetime.timedelta(seconds=t)), '%Y-%m-%d %H:%M:%S').month)


