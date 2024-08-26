import pickle
import numpy as np
import matplotlib.pyplot as plt

base_path = '/home/blaughli/tracking_project/'
pdf_raw_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'

#pdf_raw_file = pdf_raw_directory + 'pdf_data_output_originalOrder.p'
#pdf_raw_file = pdf_raw_directory + 'pdf_data_output.p'
#pdf_raw_file = pdf_raw_directory + 'pdf_data_output_seasonal.p'
pdf_raw_file = pdf_raw_directory + 'test_pdf_data.p'

file = open(pdf_raw_file,'rb')
pdf_raw,pdf_raw_djf,pdf_raw_mam,pdf_raw_jja,pdf_raw_son,counter_array = pickle.load(file)  # When the new calc is done, saved a counter_array for checking consistency
file.close()

#a=pdf_raw>0

for ii in range(np.shape(pdf_raw)[0]): 
    for jj in range(np.shape(pdf_raw)[1]): 
        if pdf_raw[ii,jj] > 0: 
            print("({},{}): {}".format(ii,jj,pdf_raw[ii,jj]))
