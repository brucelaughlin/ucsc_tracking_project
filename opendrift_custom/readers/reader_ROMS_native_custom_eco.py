from opendrift.readers.reader_ROMS_native import Reader


class ReaderEco(Reader):
#class Reader(Reader):
    """Just addiing biogeochemical variables to the reader"""

    # Should I try to modify "initial_time" ??  I am still confused by all the different timestamps I see
    #def __init__(self, initial_time=datetime(2000,1,1,0,0)):
    def __init__(self, filename=None, name=None, gridfile=None, standard_name_mapping={},
             save_interpolator=False, interpolator_filename=None):
        
        # Run constructor of parent Reader class
        super(ReaderEco, self).__init__(filename, name, gridfile, standard_name_mapping,
             save_interpolator, interpolator_filename)
        
        new_variables = {
            'CO2flx': 'CO2flx',
            'CalC': 'CalC',
            'DON': 'DON',
            'NH4': 'NH4',
            'NO3': 'NO3',
            'PON': 'PON',
            'Pzooplankton': 'Pzooplankton',
            'SiOH4': 'SiOH4',
            'TIC': 'TIC',
            'alkalinity': 'alkalinity',
            'diatom': 'diatom',
            'mesozooplankton': 'mesozooplankton',
            'microzooplankton': 'microzooplankton',
            'nanophytoplankton': 'nanophytoplankton',
            'omega': 'omega',
            'opal': 'opal',
            'oxygen': 'oxygen',
            'pCO2': 'pCO2',
            'pH': 'pH',
            }

        self.ROMS_variable_mapping.update(new_variables)
