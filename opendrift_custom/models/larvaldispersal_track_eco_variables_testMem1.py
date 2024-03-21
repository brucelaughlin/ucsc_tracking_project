# Same as V1, except adding deactivation after 90 days.  See the update method

#import datetime
#import numpy as np
#import logging; logger = logging.getLogger(__name__)
#from opendrift.models.oceandrift import Lagrangian3DArray, OceanDrift
#from opendrift.config import CONFIG_LEVEL_ESSENTIAL, CONFIG_LEVEL_BASIC, CONFIG_LEVEL_ADVANCED

import sys
from datetime import datetime, timedelta
import numpy as np
#from scipy.interpolate import interp1d
import logging; logger = logging.getLogger(__name__)
from opendrift.models.oceandrift import Lagrangian3DArray, OceanDrift
from opendrift.config import CONFIG_LEVEL_ESSENTIAL, CONFIG_LEVEL_BASIC, CONFIG_LEVEL_ADVANCED


#---------------------------------------------------------------------------------
# At some point may want to define a class for the particles, like:

# class LarvalElement(Lagrangian3DArray):
#---------------------------------------------------------------------------------



class LarvalDispersal(OceanDrift):
    """Following example of LarvalFish, and trying to add behavior for larva

    """
    # Again, may want to implement and then use your own class of element, a-la:
    #ElementType = LarvalElement
    ElementType = Lagrangian3DArray

    #max_speed = 1  # m/s     # Why was this here??? Did I have a specific reason, or did I copy it from OceanDrift???

    required_variables = {
        'x_sea_water_velocity': {'fallback': 0},
        'y_sea_water_velocity': {'fallback': 0},
        'x_wind': {'fallback': 0},
        'y_wind': {'fallback': 0},
        'sea_floor_depth_below_sea_level': {'fallback': 100},
        'ocean_vertical_diffusivity': {'fallback': 0.01, 'profiles': True},
        'ocean_mixed_layer_thickness': {'fallback': 50},
        'upward_sea_water_velocity': {'fallback': 0},
        'surface_downward_x_stress': {'fallback': 0},
        'surface_downward_y_stress': {'fallback': 0},
        'turbulent_kinetic_energy': {'fallback': 0},
        'turbulent_generic_length_scale': {'fallback': 0},
        'land_binary_mask': {'fallback': None},
        'sea_water_temperature': {'fallback': 10, 'profiles': True},
        'sea_water_salinity': {'fallback': 34, 'profiles': True},
        }
        #'CalC': {'fallback': 0},
        #'DON': {'fallback': 0},
        #'NH4': {'fallback': 0},
        #'NO3': {'fallback': 0},
        #'PON': {'fallback': 0},
        #'Pzooplankton': {'fallback': 0},
        #'SiOH4': {'fallback': 0},
        #'TIC': {'fallback': 0},
        #'alkalinity': {'fallback': 0},
        #'diatom': {'fallback': 0},
        #'mesozooplankton': {'fallback': 0},
        #'microzooplankton': {'fallback': 0},
        #'nanophytoplankton': {'fallback': 0},
        #'omega': {'fallback': 0},
        #'opal': {'fallback': 0},
        #'oxygen': {'fallback': 0},
        #'pCO2': {'fallback': 0},
        #'pH': {'fallback': 0},
        }

        # Deleted all having to do with waves, and not sure I need these either:
        # (see old versions for the exhaustive list)



    required_profiles_z_range = [0, -50]  # The depth range (in m) which profiles should cover

    def __init__(self, *args, **kwargs):

        # Calling general constructor of parent class
        super(LarvalDispersal, self).__init__(*args, **kwargs)

        # IBM configuration options
        self._add_config({
            'IBM:fraction_of_timestep_swimming':
                {'type': 'float', 'default': 0.15,
                 'min': 0.0, 'max': 1.0, 'units': 'fraction',
                 'description': 'Fraction of timestep swimming',
                 'level': CONFIG_LEVEL_ADVANCED},
            })

        self._set_config_default('drift:vertical_mixing', True)

    # ---------------------------------------------------------------------------------------------
    # Will we want to update properties of the larvae?  See LarvalFish for what was here

    #def update_terminal_velocity(self, Tprofiles=None,
    #                             Sprofiles=None, z_index=None):
    #    """Calculate terminal velocity for Pelagic Egg

    #    according to
    #    S. Sundby (1983): A one-dimensional model for the vertical
    #    distribution of pelagic fish eggs in the mixed layer
    #    Deep Sea Research (30) pp. 645-661

    #    Method copied from ibm.f90 module of LADIM:
    #    Vikebo, F., S. Sundby, B. Aadlandsvik and O. Otteraa (2007),
    #    Fish. Oceanogr. (16) pp. 216-228
    #    """

    
    #def update_larvae(self):
    # ---------------------------------------------------------------------------------------------

    # Copied from LarvalFish 
    def larvae_vertical_migration(self):

        # Note: hardcoding a guessed average length (1mm) of the larvae; is this how we want to do things?
        larvae_length = 1
        # Note: length is in mm:
        # https://opendrift.github.io/_modules/opendrift/models/larvalfish.html#LarvalFish.larvae_vertical_migration


        # Vertical migration of Larvae
        # Swim function from Peck et al. 2006

        #L = self.elements.length[larvae] # I don't have this implemented, so I hack it:
        L = np.ones(len(self.elements))*larvae_length
       

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

        #self.elements.z[larvae] = np.minimum(0, self.elements.z[larvae] + direction*max_migration_per_timestep)
        self.elements.z = np.minimum(0, self.elements.z + direction*max_migration_per_timestep)

    def update(self):

        #self.update_larvae() # Not implemented, not wanted?
        self.advect_ocean_current()

        # Stokes drift
        #self.stokes_drift()

        #self.update_terminal_velocity()
        self.vertical_mixing()
        self.larvae_vertical_migration()

        # Deactivate floats after 90 days
        self.deactivate_elements(self.elements.age_seconds > 7776000, reason='age > 90 days')


