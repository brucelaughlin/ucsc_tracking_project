import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
from opendrift.readers import reader_ROMS_native
#from opendrift.models.oceandrift import OceanDrift
import time
import sys
import os
from pathlib import Path
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/models_opendrift"))
from larvaldispersal import LarvalDispersal
import opendrift

#------------------
#------------------
output_base = '/home/blaughli/tracking_project/practice/experiments/practice_1/z_output/'
test_number = 6
tracking_output_pre = 'test_output_{}.nc'.format(str(test_number))
tracking_output_file = output_base + tracking_output_pre

output_png_pre = 'domain_plot_experiment_{}.png'.format(str(test_number))
output_png_file = output_base + output_png_pre
output_mp4_pre = 'domain_plot_experiment_{}.mp4'.format(str(test_number))
output_mp4_file = output_base + output_png_pre

#------------------
#------------------

# I got this from looking at the output file metadata
total_number_floats = 6374


#o = LarvalDispersal()
#o.io_import_file(tracking_output_file)


o = opendrift.open(tracking_output_file, elements=np.arange(0,total_number_floats,10))
o.plot(filename=output_png_file,linecolor="z",fast = True)
o.animation(filename=output_mp4_file,linecolor="z",fast = True)



#o.plot(linecolor='z', fast=True)

#o.plot_property('z')

