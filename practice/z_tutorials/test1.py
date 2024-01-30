from datetime import datetime, timedelta
import numpy as np
from opendrift.models.oceandrift import OceanDrift

o = OceanDrift(loglevel=20)  # Set loglevel to 0 for debug information

o.add_readers_from_list([
    'https://thredds.met.no/thredds/dodsC/sea/norkyst800m/1h/aggregate_be'])

print(o)

o.set_config('drift:horizontal_diffusivity', 10)  # m2/s

z = -np.random.rand(2000)*50
o.seed_elements(lon=4.8, lat=60.0, z=z, radius=0, number=2000,
                time=datetime.utcnow())

print(o)


o.run(duration=timedelta(hours=24), time_step=1800, outfile = 'test1_out.nc')

print(o)

#o.plot(linecolor='z', buffer=.1, show_elements=False, fast=False)
#o.animation(color='z', buffer=.1, fast=True)


