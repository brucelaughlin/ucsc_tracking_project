# Turn off vertical migration for now; start with just physics

# v3: try adding growth, and then a map from length to speed.  Also want latitude adjustements for each particle,
# not just '38' used as the latitude for "meters per degree lon"

# v2: try to add shoreward swimming.  Ideally, not in fixed direction, but actually to nearest coast

#import datetime
#import numpy as np
#import logging; logger = logging.getLogger(__name__)
#from opendrift.models.oceandrift import Lagrangian3DArray, OceanDrift
#from opendrift.config import CONFIG_LEVEL_ESSENTIAL, CONFIG_LEVEL_BASIC, CONFIG_LEVEL_ADVANCED

import sys
from datetime import datetime, timedelta
import numpy as np
import pickle
from scipy import spatial
import netCDF4
import logging; logger = logging.getLogger(__name__)
from opendrift.models.oceandrift import Lagrangian3DArray, OceanDrift
from opendrift.config import CONFIG_LEVEL_ESSENTIAL, CONFIG_LEVEL_BASIC, CONFIG_LEVEL_ADVANCED

#---------------------------------------------------------------------------------
# At some point may want to define a class for the particles, like:

# class LarvalElement(Lagrangian3DArray):
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Swim data
#swim_data_file = '/home/blaughli/tracking_project/practice/onshore_swim_work/z_production/swim_data_simple_v1.p'
swim_data_file = '/home/blaughli/tracking_project/practice/onshore_swim_work/z_production/swim_data.p'

file = open(swim_data_file,'rb')
mask,mask_flat,coord_array,onshore_swim_component_x,onshore_swim_component_y,onshore_swim_component_x_map,onshore_swim_component_y_map = pickle.load(file)
#mask,mask_flat,coord_array,onshore_swim_component_x,onshore_swim_component_y,neg_grad_norm_map_x,neg_grad_norm_map_y = pickle.load(file)
#mask,mask_flat,coord_array,onshore_swim_component_x,onshore_swim_component_y = pickle.load(file)
#mask_flat,coord_array,onshore_swim_component_x,onshore_swim_component_y = pickle.load(file)
file.close()

# Need to know how much distance is covered by a degree of lat and lon, since my swim data
# ranges in values from -1 to 1.  So I think I want to have swimming happen in a direction, and
# the distance will depend on a "swim speed" parameter, which should probably be based on length of larvae.

# For now, just set latitude to be 38 (halfway between 32 and 44, the rough extremes in the domain).
# Perhaps the exact latitude doesn't matter for the scales we're talking about?

model_lat_avg = 38 # CHANGE IF WE NEED TO BE MORE ACCURATE (ie make specific to each particle... ugh!)

meters_per_degree_lat = 111111
meters_per_degree_lon = meters_per_degree_lat * np.cos(np.radians(model_lat_avg))

# Also for now, just set a constant max swim speed (later should make it dependent on larvae size)
# From Kashef paper, speeds for rockfish larvae: at parturation: 0.5-1.8 cm/s;"newly settled": 8.6 to 53.5cm/s

#swim_speed_max = 10 #5m/s  FOR TESTING; ALL PARTICLES SHOULD REMAIN WITHIN TWO GRID CELLS OF A COASTLINE
#swim_speed_max = 100 #5m/s  FOR TESTING; ALL PARTICLES SHOULD REMAIN WITHIN TWO GRID CELLS OF A COASTLINE
#swim_speed_max = 5 #5m/s  FOR TESTING; ALL PARTICLES SHOULD REMAIN WITHIN TWO GRID CELLS OF A COASTLINE
swim_speed_max = 0.01 #10cm/s
#swim_speed_max = 0.1 #10cm/s
#swim_speed_max = -0.1 #10cm/s

test_file_out_0 = "/home/blaughli/tracking_project/practice/onshore_swim_work/particle_data_0.p"
test_file_out_1 = "/home/blaughli/tracking_project/practice/onshore_swim_work/particle_data_1.p"
test_save_dex = 0 # Save when equals 5 (5 timesteps in, right?)

#---------------------------------------------------------------------------------

# Define the particle deactivation time (seconds).
drift_days = 150
drift_seconds = (drift_days) * 24 * 60 * 60 

class LarvalElement(Lagrangian3DArray):
    """
    Extending Lagrangian3DArray with specific properties for larval and juvenile stages of fish
    """

    variables = Lagrangian3DArray.add_variables([
        ('length', {'dtype': np.float32,
                    'units': 'mm',
                    'default': 0}),
        ('weight', {'dtype': np.float32,
                    'units': 'mg',
                    'default': 0.08})])




class LarvalDispersal(OceanDrift):
    """Following example of LarvalFish, and trying to add behavior for larva

    """
    # Again, may want to implement and then use your own class of element, a-la:
    ElementType = LarvalElement
    #ElementType = Lagrangian3DArray

    #max_speed = 1  # m/s     # Why was this here??? Did I have a specific reason, or did I copy it from OceanDrift???

    required_variables = {
        'x_sea_water_velocity': {'fallback': 0},
        'y_sea_water_velocity': {'fallback': 0},
        'x_wind': {'fallback': 0},
        'y_wind': {'fallback': 0},
        'sea_floor_depth_below_sea_level': {'fallback': 100},
        'ocean_vertical_diffusivity': {'fallback': 0.00001, 'profiles': True},
        'ocean_mixed_layer_thickness': {'fallback': 50},
        'upward_sea_water_velocity': {'fallback': 0},
        'surface_downward_x_stress': {'fallback': 0},
        'surface_downward_y_stress': {'fallback': 0},
        'turbulent_kinetic_energy': {'fallback': 0},
        'turbulent_generic_length_scale': {'fallback': 0},
        'land_binary_mask': {'fallback': None},
        'sea_water_temperature': {'fallback': 10, 'profiles': True},
        'sea_water_salinity': {'fallback': 34, 'profiles': True},
        'CalC': {'fallback': 0},
        'DON': {'fallback': 0},
        'NH4': {'fallback': 0},
        'NO3': {'fallback': 0},
        'PON': {'fallback': 0},
        'Pzooplankton': {'fallback': 0},
        'SiOH4': {'fallback': 0},
        'TIC': {'fallback': 0},
        'alkalinity': {'fallback': 0},
        'diatom': {'fallback': 0},
        'mesozooplankton': {'fallback': 0},
        'microzooplankton': {'fallback': 0},
        'nanophytoplankton': {'fallback': 0},
        'omega': {'fallback': 0},
        'opal': {'fallback': 0},
        'oxygen': {'fallback': 0},
        'pCO2': {'fallback': 0},
        'pH': {'fallback': 0},
        }

        # Deleted all having to do with waves, and not sure I need these either:
        # (see old versions for the exhaustive list)



    required_profiles_z_range = [0, -50]  # The depth range (in m) which profiles should cover

    def __init__(self, *args, **kwargs):

        # Calling general constructor of parent class
        super(LarvalDispersal, self).__init__(*args, **kwargs)

        self._set_config_default('drift:vertical_mixing', True)
        
        ## IBM configuration options
        #self._add_config({
        #    'IBM:fraction_of_timestep_swimming':
        #        {'type': 'float', 'default': 0.15,
        #         'min': 0.0, 'max': 1.0, 'units': 'fraction',
        #         'description': 'Fraction of timestep swimming',
        #         'level': CONFIG_LEVEL_ADVANCED},
        #    })


    

    # ---------------------------------------------------------------------------------------------
    # Copied from LarvalFish 
    # ---------------------------------------------------------------------------------------------

    def fish_growth(self, weight, temperature):
        # Weight in milligrams, temperature in celcius
        # Daily growth rate in percent according to
        # Folkvord, A. 2005. "Comparison of Size-at-Age of Larval Atlantic Cod (Gadus Morhua)
        # from Different Populations Based on Size- and Temperature-Dependent Growth
        # Models." Canadian Journal of Fisheries and Aquatic Sciences.
        # Journal Canadien Des Sciences Halieutiques # et Aquatiques 62(5): 1037-52.
        GR = 1.08 + 1.79 * temperature - 0.074 * temperature * np.log(weight) \
             - 0.0965 * temperature * np.log(weight) ** 2 \
             + 0.0112 * temperature * np.log(weight) ** 3

        # Growth rate(g) converted to milligram weight (gr_mg) per timestep:
        g = (np.log(GR / 100. + 1)) * self.time_step.total_seconds()/86400
        return weight * (np.exp(g) - 1.)   


    def update_fish_larvae(self):

        #larvae = np.where(self.elements.hatched==1)[0]

        # Increasing weight of larvae
        avg_weight_before = self.elements.weight.mean()
        growth = self.fish_growth(self.elements.weight,
                                  self.environment.sea_water_temperature)
        self.elements.weight += growth
        avg_weight_after = self.elements.weight.mean()
        logger.debug('Growing %s larve from average size %s to %s' %
              (len(larvae), avg_weight_before, avg_weight_after))

        # Increasing length of larvae, according to Folkvord (2005)
        w = self.elements.weight
        self.elements.length = np.exp(2.296 + 0.277 * np.log(w) - 0.005128 *np.log10(w)**2)



    def larvae_vertical_migration(self):

        # Note: hardcoding a guessed average length (1mm) of the larvae; is this how we want to do things?
        # larvae_length = 1
        # Note: length is in mm:
        # https://opendrift.github.io/_modules/opendrift/models/larvalfish.html#LarvalFish.larvae_vertical_migration


        # Vertical migration of Larvae
        # Swim function from Peck et al. 2006

        L = self.elements.length # I don't have this implemented, so I hack it:
        #L = np.ones(len(self.elements))*larvae_length
       

        # Below, with fraction_of_timestep_swimming = 0.15 (see above), this means
        # that max_migration_per_timestep = 1.75cm... is that too small?

        swim_speed = (0.261*(L**(1.552*L**(-0.08))) - 5.289/L) / 1000
        f = self.get_config('IBM:fraction_of_timestep_swimming')
        max_migration_per_timestep = f*swim_speed*self.time_step.total_seconds()

        # Using here UTC hours. Should be changed to local solar time,
        # although a phase shift of some hours should not make much difference
        if self.time.hour < 12:
            direction = -1  # Swimming down when light is increasing
        else:
            direction = 1  # Swimming up when light is decreasing

        #self.elements.z = np.minimum(0, self.elements.z + direction*max_migration_per_timestep)
        self.elements.z = np.minimum(0, self.elements.z + direction*max_migration_per_timestep)


    def larvae_onshore_swimming(self):
       #mask_flat,coord_array,onshore_swim_component_x,onshore_swim_component_y 
        
        global test_save_dex # "NOT GOOD PRACTICE", just for a test
        
        lons = self.elements.lon.reshape(-1,1)
        lats = self.elements.lat.reshape(-1,1)
        lonlatpairs = np.concatenate((lons,lats), axis=1)
        distances,indices = spatial.KDTree(coord_array).query(lonlatpairs)

        if test_save_dex == 0:
            file = open(test_file_out_0,'wb')
            pickle.dump([self.elements.lon,self.elements.lat],file)
            file.close()
        if test_save_dex == 1:
            file = open(test_file_out_1,'wb')
            pickle.dump([self.elements.lon,self.elements.lat],file)
            file.close()

        test_save_dex = test_save_dex + 1


        # Change the swim speed to depend on size; currently using "max" just for testing
        self.elements.lon = self.elements.lon + mask_flat[indices]*(onshore_swim_component_x[indices]*swim_speed_max/meters_per_degree_lon*self.time_step.total_seconds())
        self.elements.lat = self.elements.lat + mask_flat[indices]*(onshore_swim_component_y[indices]*swim_speed_max/meters_per_degree_lat*self.time_step.total_seconds())

        #---------------------------------------------------------------------------------

    def update(self):

        #self.update_larvae() # Not implemented, not wanted?
        self.advect_ocean_current()

        # Stokes drift
        #self.stokes_drift()

        #self.update_terminal_velocity()
        self.vertical_mixing()
        
        # Turn off for now, just physics
        #self.larvae_vertical_migration()

        self.larvae_onshore_swimming()

        # Deactivate floats after 90 days
        self.deactivate_elements(self.elements.age_seconds > drift_seconds, reason='age > {} days'.format(drift_days))
        #self.deactivate_elements(self.elements.age_seconds > 7776000, reason='age > 90 days')


