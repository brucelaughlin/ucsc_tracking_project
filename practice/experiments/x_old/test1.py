import matplotlib.pyplot as plt
import numpy as np
from opendrift.readers import reader_ROMS_native
from opendrift.models.oceandrift import OceanDrift

from netCDF4 import Dataset

his_file = 'wc12_his.nc'

his_data = Dataset(his_file)

# need to release from coastal rho points (ie within 10km from coast)
# for now, my idea is to just try getting the first
# offshore points

#rho_mask = np.array(his_data.variables['mask_rho'][:])
#rho_lon = np.array(his_data.variables['lon_rho'][:])
#rho_lat = np.array(his_data.variables['lat_rho'][:])

#lat_dim = rho_mask.shape[1]
#lon_dim = rho_mask.shape[0]
#rho_coastal_ij = np.zeros(shape=(lat_dim,2))
#rho_coastal = np.zeros(shape=(lat_dim,2))

#for i in range(1,lat_dim):
#    a = rho_mask[i,:]
#    b =  a < 0
#    if b.size > 0 & b.size < lon_dim:
        
    

#plt.figure(figsize=(4,4))
#plt.fill(rho_mask)
#plt.show()






o = OceanDrift(loglevel=20)  # Set loglevel to 0 for debug information

#nordic_native = reader_ROMS_native.Reader(o.test_data_folder() +
    #'wc12_his.nc')

#nordic_native = reader_ROMS_native.Reader('wc12_his.nc')
roms_his_reader = reader_ROMS_native.Reader(his_file)

o.add_reader(roms_his_reader)

# -124, 38

o.seed_elements(lon=-124, lat=38., radius=0, number=10, z=np.linspace(0, -150, 10), time=roms_his_reader.start_time)


o.run(time_step=3600)

print(o)

o.plot(linecolor='z', fast=True)

#o.animation(color='z', buffer=.1, fast=True)
