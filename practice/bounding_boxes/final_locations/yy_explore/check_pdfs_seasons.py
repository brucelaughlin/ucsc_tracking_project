# Use the modified pdf files, which have an extra variable for the new box numbers

import pickle
import numpy as np
import matplotlib.pyplot as plt

base_path = '/home/blaughli/tracking_project/'
pdf_raw_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'

pdf_raw_file = pdf_raw_directory + 'pdf_data_output_seasonal_oneFileTest.p'

file = open(pdf_raw_file,'rb')
pdf_list_connectivity,pdf_list_settleTime,settlement_boxes_test_array,settlement_times_test_array,counter_array = pickle.load(file)  # When the new calc is done, saved a counter_array for checking consistency
file.close()

print("times")
for pdf in pdf_list_settleTime:
    print(np.amax(pdf))
    print(np.amin(pdf))


print("boxes")
for pdf in pdf_list_connectivity:
    print(np.amax(pdf))
    print(np.amin(pdf))


