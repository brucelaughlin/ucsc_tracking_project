# V1 : leaving all the added environment variables from my naive copy of OceanDrift...
# V2 will remove those not in LarvalFish, and which don't seem needed

# I previously mistakenly edited my own version of OceanDrift; really I should
# have inherited OceanDrift and modified where needed.  
# So here, I copied "LarvalFish" as a template.
# I finally looked at the model_template in the OpenDrift models directory,
# which cleared many things up


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



# At some point may want to define a class for the particles, like:

# class LarvalElement(Lagrangian3DArray):



class LarvalDispersal(OceanDrift):
    """Following example of LarvalFish, and trying to add behavior for larva

    """
    # Again, may want to implement and then use your own class of element, a-la:
    #ElementType = LarvalElement

    ElementType = Lagrangian3DArray

    #max_speed = 1  # m/s     # Why was this here??? Did I have a specific reason, or did I copy it from OceanDrift???


    #ElementType = LarvalElement

    required_variables = {
        'x_sea_water_velocity': {'fallback': 0},
        'y_sea_water_velocity': {'fallback': 0},
        'sea_surface_wave_significant_height': {'fallback': 0},
        'x_wind': {'fallback': 0},
        'y_wind': {'fallback': 0},
        'land_binary_mask': {'fallback': None},
        'sea_floor_depth_below_sea_level': {'fallback': 100},
        'ocean_vertical_diffusivity': {'fallback': 0.01, 'profiles': True},
        'ocean_mixed_layer_thickness': {'fallback': 50},
        'sea_water_temperature': {'fallback': 10, 'profiles': True},
        'sea_water_salinity': {'fallback': 34, 'profiles': True},
        'sea_surface_wave_stokes_drift_x_velocity': {'fallback': 0},
        'sea_surface_wave_stokes_drift_y_velocity': {'fallback': 0},

        'upward_sea_water_velocity': {'fallback': 0},
        'sea_surface_wave_period_at_variance_spectral_density_maximum':
            {'fallback': 0},
        'sea_surface_wave_mean_period_from_variance_spectral_density_second_frequency_moment': {'fallback': 0},
        'sea_surface_swell_wave_to_direction': {'fallback': 0, 'important': False},
        'sea_surface_swell_wave_peak_period_from_variance_spectral_density': {'fallback': 0, 'important': False},
        'sea_surface_swell_wave_significant_height': {'fallback': 0, 'important': False},
        'sea_surface_wind_wave_to_direction': {'fallback': 0, 'important': False},
        'sea_surface_wind_wave_mean_period': {'fallback': 0, 'important': False},
        'sea_surface_wind_wave_significant_height': {'fallback': 0, 'important': False},
        'surface_downward_x_stress': {'fallback': 0},
        'surface_downward_y_stress': {'fallback': 0},
        'turbulent_kinetic_energy': {'fallback': 0},
        'turbulent_generic_length_scale': {'fallback': 0},
        'CalC': {'fallback': 0, 'profiles': True},
        'DON': {'fallback': 0, 'profiles': True},
        'NH4': {'fallback': 0, 'profiles': True},
        'NO3': {'fallback': 0, 'profiles': True},
        'PON': {'fallback': 0, 'profiles': True},
        'Pzooplankton': {'fallback': 0, 'profiles': True},
        'SiOH4': {'fallback': 0, 'profiles': True},
        'TIC': {'fallback': 0, 'profiles': True},
        'alkalinity': {'fallback': 0, 'profiles': True},
        'diatom': {'fallback': 0, 'profiles': True},
        'mesozooplankton': {'fallback': 0, 'profiles': True},
        'microzooplankton': {'fallback': 0, 'profiles': True},
        'nanophytoplankton': {'fallback': 0, 'profiles': True},
        'omega': {'fallback': 0, 'profiles': True},
        'opal': {'fallback': 0, 'profiles': True},
        'oxygen': {'fallback': 0, 'profiles': True},
        'pCO2': {'fallback': 0, 'profiles': True},
        'pH': {'fallback': 0, 'profiles': True},
        }




    }

    required_profiles_z_range = [0, -50]  # The depth range (in m) which profiles should cover

    def __init__(self, *args, **kwargs):

        # Calling general constructor of parent class
        super(LarvalFish, self).__init__(*args, **kwargs)

        # IBM configuration options
        self._add_config({
            'IBM:fraction_of_timestep_swimming':
                {'type': 'float', 'default': 0.15,
                 'min': 0.0, 'max': 1.0, 'units': 'fraction',
                 'description': 'Fraction of timestep swimming',
                 'level': CONFIG_LEVEL_ADVANCED},
            })

        self._set_config_default('drift:vertical_mixing', True)

    def update_terminal_velocity(self, Tprofiles=None,
                                 Sprofiles=None, z_index=None):
        """Calculate terminal velocity for Pelagic Egg

        according to
        S. Sundby (1983): A one-dimensional model for the vertical
        distribution of pelagic fish eggs in the mixed layer
        Deep Sea Research (30) pp. 645-661

        Method copied from ibm.f90 module of LADIM:
        Vikebo, F., S. Sundby, B. Aadlandsvik and O. Otteraa (2007),
        Fish. Oceanogr. (16) pp. 216-228
        """
        g = 9.81  # ms-2

        # Pelagic Egg properties that determine buoyancy
        eggsize = self.elements.diameter  # 0.0014 for NEA Cod
        eggsalinity = self.elements.neutral_buoyancy_salinity
        # 31.25 for NEA Cod

        # prepare interpolation of temp, salt
        if not (Tprofiles is None and Sprofiles is None):
            if z_index is None:
                z_i = range(Tprofiles.shape[0])  # evtl. move out of loop
                # evtl. move out of loop
                z_index = interp1d(-self.environment_profiles['z'],
                                   z_i, bounds_error=False)
            zi = z_index(-self.elements.z)
            upper = np.maximum(np.floor(zi).astype(np.uint8), 0)
            lower = np.minimum(upper + 1, Tprofiles.shape[0] - 1)
            weight_upper = 1 - (zi - upper)

        # do interpolation of temp, salt if profiles were passed into
        # this function, if not, use reader by calling self.environment
        if Tprofiles is None:
            T0 = self.environment.sea_water_temperature
        else:
            T0 = Tprofiles[upper, range(Tprofiles.shape[1])] * \
                 weight_upper + \
                 Tprofiles[lower, range(Tprofiles.shape[1])] * \
                 (1 - weight_upper)
        if Sprofiles is None:
            S0 = self.environment.sea_water_salinity
        else:
            S0 = Sprofiles[upper, range(Sprofiles.shape[1])] * \
                 weight_upper + \
                 Sprofiles[lower, range(Sprofiles.shape[1])] * \
                 (1 - weight_upper)

        # The density difference between a pelagic egg and the ambient water
        # is regulated by their salinity difference through the
        # equation of state for sea water.
        # The Egg has the same temperature as the ambient water and its
        # salinity is regulated by osmosis through the egg shell.
        DENSw = self.sea_water_density(T=T0, S=S0)
        DENSegg = self.sea_water_density(T=T0, S=eggsalinity)
        dr = DENSw - DENSegg  # density difference

        # water viscosity
        my_w = 0.001 * (1.7915 - 0.0538 * T0 + 0.007 * (T0 ** (2.0)) - 0.0023 * S0)
        # ~0.0014 kg m-1 s-1

        # terminal velocity for low Reynolds numbers
        W = (1.0 / my_w) * (1.0 / 18.0) * g * eggsize ** 2 * dr

        # check if we are in a Reynolds regime where Re > 0.5
        highRe = np.where(W * 1000 * eggsize / my_w > 0.5)

        # Use empirical equations for terminal velocity in
        # high Reynolds numbers.
        # Empirical equations have length units in cm!
        my_w = 0.01854 * np.exp(-0.02783 * T0)  # in cm2/s
        d0 = (eggsize * 100) - 0.4 * \
             (9.0 * my_w ** 2 / (100 * g) * DENSw / dr) ** (1.0 / 3.0)  # cm
        W2 = 19.0 * d0 * (0.001 * dr) ** (2.0 / 3.0) * (my_w * 0.001 * DENSw) ** (-1.0 / 3.0)
        # cm/s
        W2 = W2 / 100.  # back to m/s

        W[highRe] = W2[highRe]
        self.elements.terminal_velocity = W

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

        # Hatching of eggs
        eggs = np.where(self.elements.hatched==0)[0]
        if len(eggs) > 0:
            amb_duration = np.exp(3.65 - 0.145*self.environment.sea_water_temperature[eggs]) # Total egg development time (days) according to ambient temperature (Ellertsen et al. 1988)
            days_in_timestep = self.time_step.total_seconds()/(60*60*24)  # The fraction of a day completed in one time step
            amb_fraction = days_in_timestep/amb_duration # Fraction of development time completed during present time step
            self.elements.stage_fraction[eggs] += amb_fraction # Add fraction completed during present timestep to cumulative fraction completed
            hatching = np.where(self.elements.stage_fraction[eggs]>=1)[0]
            if len(hatching) > 0:
                logger.debug('Hatching %s eggs' % len(hatching))
                self.elements.hatched[eggs[hatching]] = 1 # Eggs with total development time completed are hatched (1)

        larvae = np.where(self.elements.hatched==1)[0]
        if len(larvae) == 0:
            logger.debug('%s eggs, with maximum stage_fraction of %s (1 gives hatching)'
                         % (len(eggs), self.elements.stage_fraction[eggs].max()))
            return

        # Increasing weight of larvae
        avg_weight_before = self.elements.weight[larvae].mean()
        growth = self.fish_growth(self.elements.weight[larvae],
                                  self.environment.sea_water_temperature[larvae])
        self.elements.weight[larvae] += growth
        avg_weight_after = self.elements.weight[larvae].mean()
        logger.debug('Growing %s larve from average size %s to %s' %
              (len(larvae), avg_weight_before, avg_weight_after))

        # Increasing length of larvae, according to Folkvord (2005)
        w = self.elements.weight[larvae]
        self.elements.length[larvae] = np.exp(2.296 + 0.277 * np.log(w) - 0.005128 *np.log10(w)**2)

    def larvae_vertical_migration(self):

        larvae = np.where(self.elements.hatched==1)[0]
        if len(larvae) == 0:
            return

        # Vertical migration of Larvae
        # Swim function from Peck et al. 2006
        L = self.elements.length[larvae]
        swim_speed = (0.261*(L**(1.552*L**(-0.08))) - 5.289/L) / 1000
        f = self.get_config('IBM:fraction_of_timestep_swimming')
        max_migration_per_timestep = f*swim_speed*self.time_step.total_seconds()

        # Using here UTC hours. Should be changed to local solar time,
        # although a phase shift of some hours should not make much difference
        if self.time.hour < 12:
            direction = -1  # Swimming down when light is increasing
        else:
            direction = 1  # Swimming up when light is decreasing

        self.elements.z[larvae] = np.minimum(0, self.elements.z[larvae] + direction*max_migration_per_timestep)

    def update(self):

        self.update_fish_larvae()
        self.advect_ocean_current()

        # Stokes drift
        self.stokes_drift()

        self.update_terminal_velocity()
        self.vertical_mixing()
        self.larvae_vertical_migration()
