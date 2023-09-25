import numpy as np
from opendrift.readers import reader_ROMS_native
from opendrift.models.oceandrift import OceanDrift

from netCDF4 import Dataset

his_file = 'wc12_his.nc'

his_data = Dataset(his_file)
rho_mask = his_data.variables['mask_rho'][:]

o = OceanDrift(loglevel=20)  # Set loglevel to 0 for debug information

#nordic_native = reader_ROMS_native.Reader(o.test_data_folder() +
    #'wc12_his.nc')

#nordic_native = reader_ROMS_native.Reader('wc12_his.nc')
nordic_native = reader_ROMS_native.Reader('his_file')

o.add_reader(nordic_native)

# -124, 38

o.seed_elements(lon=-124, lat=38., radius=0, number=10,
                z=np.linspace(0, -150, 10), time=nordic_native.start_time)


o.run(time_step=3600)

print(o)

o.plot(linecolor='z', fast=True)

o.animation(color='z', buffer=.1, fast=True)
