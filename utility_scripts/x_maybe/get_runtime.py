import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
import xarray
import opendrift

#------------------
#------------------
output_base = '/home/blaughli/tracking_project/practice/experiments/practice_1/z_output/'



#test_number = '7'
test_run_numbers = [7,'8_1','8_2']



performance_list = []

for num in test_run_numbers:
    
    tracking_output_pre = 'test_output_{}.nc'.format(str(num))
    tracking_output_file = output_base + tracking_output_pre

    performance_list.append(xarray.open_dataset(tracking_output_file).performance)
    
    #print(xarray.open_dataset(tracking_output_file).performance)


#o = LarvalDispersal()
#o.io_import_file(tracking_output_file)



