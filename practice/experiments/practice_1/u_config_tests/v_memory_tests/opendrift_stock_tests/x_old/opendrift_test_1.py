

from opendrift.models.oceandrift import OceanDrift
from opendrift.readers import reader_netCDF_CF_generic

o = OceanDrift(loglevel=0)

test_forcing_file_path = '/home/blaughli/opendrift/tests/test_data/16Nov2015_NorKyst_z_surface/norkyst800_subset_16Nov2015.nc'

reader_norkyst = reader_netCDF_CF_generic.Reader(test_forcing_file_path)

from opendrift.readers import reader_global_landmask
reader_landmask = reader_global_landmask.Reader(extent=[2, 59, 8, 63])  # lonmin, latmin, lonmax, latmax


o.add_reader([reader_landmask, reader_norkyst, reader_nordic])



