# Turn off vertical migration for now; start with just physics

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

# Would be better if this could be passed...
# Define the particle deactivation time (seconds).
drift_days = 10
drift_seconds = (drift_days) * 24 * 60 * 60 

class OceanDriftDeactivate(OceanDrift):

    def __init__(self, *args, **kwargs):

        # Calling general constructor of parent class
        super(OceanDriftDeactivate, self).__init__(*args, **kwargs)

        self._set_config_default('drift:vertical_advection', True)
        self._set_config_default('drift:vertical_mixing', True)
        self._set_config_default('general:coastline_action', 'previous')


    def update(self):
        """Update positions and properties of elements."""
        # copied from "OceanDrift", with the addition of the deactivation

        # Simply move particles with ambient current
        self.advect_ocean_current()

        # Advect particles due to surface wind drag,
        # according to element property wind_drift_factor
        #self.advect_wind()

        # Stokes drift
        #self.stokes_drift()

        # Turbulent Mixing
        if self.get_config('drift:vertical_mixing') is True:
            self.update_terminal_velocity()
            self.vertical_mixing()
        else:  # Buoyancy
            self.vertical_buoyancy()

        # Vertical advection
        if self.get_config('drift:vertical_advection') is True:
            self.vertical_advection()

        # Deactivate floats after "drift_days" has passed
        self.deactivate_elements(self.elements.age_seconds > drift_seconds, reason='age > {} days'.format(drift_days))
