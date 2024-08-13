
#------------------------------------------------------------------
pdf_file_name_pre = "pdf_data_output_seasonal_rangeO2_pld_20_30_z_two_file_test.npz"
#------------------------------------------------------------------



import numpy as np
import matplotlib.pyplot as plt
import os

# os.path.join, not your stupid pluses

pdf_file_name = os.path.splitext(pdf_file_name_pre)[0] + "_swapped" + os.path.splitext(pdf_file_name_pre)[1]

base_path = '/home/blaughli/tracking_project/'
pdf_raw_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'
pdf_raw_file = pdf_raw_directory + pdf_file_name


#file = open(pdf_raw_file,'rb')
#settlers_assigned_bio_windows,pdf_list_exposure_T,pdf_list_of_lists_O2,pdf_list_connectivity,pdf_list_settleTime,counter_array,box_num_mod,tick_positions,tick_labels,first_continent_box_num,oxygen_limit_list = pickle.load(file)
#file.close()


d = np.load(pdf_raw_file)

settlers_assigned_bio_windows = d['settlers_assigned_bio_windows']
bio_window_opening_distribution = d['bio_window_opening_distribution']
#pdf_list_exposure_T = d['pdf_list_exposure_T']
#pdf_list_of_lists_O2 = d['pdf_list_of_lists_O2']
#pdf_list_connectivity = d['pdf_list_connectivity']
pdf_list_settleTime = d['pdf_list_settleTime']
#counter_array = d['counter_array']
#oxygen_limit_list = d['oxygen_limit_list']

# Ask paul about pdb

pdf = pdf_list_settleTime[0,:,:]
#pdf = pdf_list_settleTime[0]

#pdf_colSum = np.sum(pdf,axis=1)
pdf_colSum = np.sum(pdf,axis=0)


# something is weird in my assigned win

#settlers_assigned_bio_windows = settlers_assigned_bio_windows[1:]

#plt.plot(pdf_colSum)
#plt.plot(bio_window_opening_distribution,c='r')

plt.scatter(,settlers_assigned_bio_windows)


plt.show()




