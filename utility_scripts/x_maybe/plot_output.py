
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path
sys.path.append(os.path.abspath("/home/blaughli/tracking_project/opendrift_custom/models"))
from larvaldispersal_track_eco_variables_v2 import LarvalDispersal
import opendrift


# -------------
test_number = '99'
# -------------

output_base = '/home/blaughli/tracking_project/practice/experiments/practice_1/z_output/'
figure_output_base = '/home/blaughli/tracking_project/practice/experiments/practice_1/y_figures/'
tracking_output_pre = 'test_output_{}.nc'.format(str(test_number))
tracking_output_file = output_base + tracking_output_pre

output_png_pre = 'domain_plot_experiment_{}.png'.format(str(test_number))
output_png_file = figure_output_base + output_png_pre
output_mp4_pre = 'domain_plot_experiment_{}.mp4'.format(str(test_number))
output_mp4_file = figure_output_base + output_mp4_pre

# -------------


# I got this from looking at the output file metadata
#total_number_floats = 6374
total_number_floats = 4764

#o = LarvalDispersal()
#o.io_import_file(tracking_output_file)


o = opendrift.open(tracking_output_file, elements=np.arange(0,total_number_floats,10))
#o = opendrift.open(tracking_output_file)

o.plot(filename=output_png_file,linecolor="z",fast = True)
#o.animation(filename=output_mp4_file,linecolor="z",fast = True)

#o = opendrift.open(file_path)

#o.plot(linecolor='z', fast=True)

#o.plot_property('z')


#o.animate()
