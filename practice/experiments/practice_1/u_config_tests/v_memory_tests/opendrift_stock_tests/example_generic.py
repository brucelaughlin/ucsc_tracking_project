from datetime import datetime, timedelta
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.models.openoil import OpenOil
import sys

number_of_floats = int(sys.argv[1])
run_calc = int(sys.argv[2])
run_save = int(sys.argv[3])
buffer_length = int(sys.argv[4])

run_string_test = 'floats_{a:05d}_calcDT_{b:03d}_saveDT_{c:04d}_buffer_{d:03d}'.format(a=number_of_floats,b=run_calc,c=run_save,d=buffer_length)
tracking_output_pre = 'test_output_{}.nc'.format(run_string_test)
tracking_output_file = 'z_output/' + tracking_output_pre


o = OpenOil(loglevel=20)  # Set loglevel to 0 for debug information

# Arome atmospheric model
reader_arome = reader_netCDF_CF_generic.Reader(o.test_data_folder() + '16Nov2015_NorKyst_z_surface/arome_subset_16Nov2015.nc')
# Norkyst ocean model
reader_norkyst = reader_netCDF_CF_generic.Reader(o.test_data_folder() + '16Nov2015_NorKyst_z_surface/norkyst800_subset_16Nov2015.nc')

# Uncomment to use live data from thredds
#reader_arome = reader_netCDF_CF_generic.Reader('https://thredds.met.no/thredds/dodsC/mepslatest/meps_lagged_6_h_latest_2_5km_latest.nc')
#reader_norkyst = reader_netCDF_CF_generic.Reader('https://thredds.met.no/thredds/dodsC/sea/norkyst800m/1h/aggregate_be')

o.add_reader([reader_norkyst, reader_arome])

time = [reader_arome.start_time,
                reader_arome.start_time + timedelta(hours=30)]
#time = reader_arome.start_time


o.set_config('drift:vertical_mixing', False)
o.set_config('processes:dispersion', False)
o.set_config('processes:evaporation', False)
o.set_config('processes:emulsification', True)
o.set_config('drift:current_uncertainty', .1)
o.set_config('drift:wind_uncertainty', 1)

# Seed oil elements at defined position and time
o.seed_elements(lon=4.6, lat=60.0, radius=50, number=100000, time=time,
    wind_drift_factor=.02)

o.run(end_time=reader_norkyst.end_time, time_step=run_calc*60,
    time_step_output=run_save*60, outfile = tracking_output_file,
    export_buffer_length=buffer_length)

#o.run(end_time=reader_norkyst.end_time, time_step=1800,
#    time_step_output=3600, outfile='openoil.nc',
#    export_variables=['mass_oil'])
