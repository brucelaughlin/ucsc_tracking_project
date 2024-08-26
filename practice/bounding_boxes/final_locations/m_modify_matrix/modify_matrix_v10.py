# Looking at the domain plots of islands, I realize that my box numbers for islands (especially islands 1,2 and 5-8)
# are not "in order" - in other words, the pdf won't look intuitive, since, for instance, boxes 13 and 20 represent
# the same island, but will appear far apart

#v8: switched to np.savez saving

# v7: just added more settlement time statistics, but didn't want to break anything

#V6: had one-off error in the tick_positions.  Should maybe just do away with the "box number" idea, and start at 0 (not 1)

#V5: now we have a list of lists for oxygen data saved (we test at multiple exposure levels)

#V4: using updated island boxes, saving V3 in case

#V3: using new histogram save format (lists)

# box index (ie "number" - 1) order changes: 
# [9,10,11,12,13,14,15,16] -> [9,16,10,15,11,14,12,13]


# -------------------------------------------------------
# Input file
# -------------------------------------------------------
#pdf_file_name = 'pdf_data_output_releaseLoc_vs_settleTime_test3.p'
#pdf_file_name = 'pdf_data_output_seasonal_v3_tenFileTest.p'
#pdf_file_name = 'pdf_data_output_seasonal_rangeO2_v4_oneFileTest.p'
#pdf_file_name = 'pdf_data_output_seasonal_rangeO2_v4_tenFileTest.p'
#pdf_file_name = 'pdf_data_output_seasonal_rangeO2_v4_run_test3.p'
#pdf_file_name = "pdf_data_output_seasonal_rangeO2_v4_test4_physics_only_AKs_1en5.p"
#pdf_file_name = "pdf_data_output_seasonal_rangeO2_pld_20_30_z_two_file_test.p"
#pdf_file_name = "pdf_data_output_seasonal_rangeO2_pld_20_30_z_two_file_test.npz"
#pdf_file_name = "pdf_data_output_seasonal_ranges_O2_pH___pld_20_30_z_two_file_test.npz"
pdf_file_name = "pdf_data_output_seasonal_ranges_O2_pH___pld_20_29_z_two_file_test.npz"
# -------------------------------------------------------

import pickle
import numpy as np
import os

base_path = '/home/blaughli/tracking_project/'
pdf_raw_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'

pdf_raw_file = pdf_raw_directory + pdf_file_name

pdf_file_swapped_name = os.path.splitext(pdf_file_name)[0] + "_swapped"
pdf_swapped_file_out = pdf_raw_directory + pdf_file_swapped_name

points_type_line = 'psi'
box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'modify_islands/'
#islands_dir = 'aa_islands/'
continent_dir = 'continent/'
input_dir_islands = box_dir + islands_dir + 'z_output/'
input_dir_continent = box_dir + continent_dir + 'z_output/'




#file = open(pdf_raw_file,'rb')
#bio_window_opening_distribution,pdf_arrays_T,pdf_arrays_O2,pdf_list_connectivity,pdf_list_settleTime,counter_array,oxygen_limit_list = pickle.load(file)
#file.close()

d = np.load(pdf_raw_file)

#settlers_timestep_settled = d['settlers_timestep_settled']
#settlers_assigned_bio_windows = d['settlers_assigned_bio_windows']
#bio_window_opening_distribution = d['bio_window_opening_distribution'] 
pdf_arrays_T = d['pdf_arrays_T']
pdf_arrays_O2 = d['pdf_arrays_O2']
pdf_arrays_pH = d['pdf_arrays_pH']
pdf_arrays_connectivity = d['pdf_arrays_connectivity'] 
pdf_arrays_settleTime = d['pdf_arrays_settleTime']
counter_array = d['counter_array']
oxygen_limit_list = d['oxygen_limit_list']
pH_limit_list = d['pH_limit_list']

pdf_arrays_connectivity_swapped = np.zeros_like(pdf_arrays_connectivity)
pdf_arrays_settleTime_swapped = np.zeros_like(pdf_arrays_settleTime)
pdf_arrays_T_swapped = np.zeros_like(pdf_arrays_T)
pdf_arrays_O2_swapped = np.zeros_like(pdf_arrays_O2)
pdf_arrays_pH_swapped = np.zeros_like(pdf_arrays_pH)
#pdf_list_connectivity_swapped = []
#pdf_list_settleTime_swapped = []
#pdf_arrays_T_swapped = []
#pdf_arrays_O2_swapped = []

#for ii in range(len(pdf_arrays_O2)):
#    pdf_arrays_O2_swapped.append([])
#pdf_arrays_pH_swapped = []
#for ii in range(len(pdf_arrays_pH)):
#    pdf_arrays_pH_swapped.append([])

print(np.shape(pdf_arrays_O2))


# -------------------------------------------------------
## ISLAND 1
#dx1 = [0,1,2,3]
#swap_dst1 = [0,1]
#swap_src1 = [1,2]

# ISLANDS 4-8
dx2_og =  [8,9,10,11,12,13,14,15]
#dx2_og =  [9,10,11,12,13,14,15,16]
dx2_new = [8,15,9,14,10,13,11,12]
#dx2_new = [9,16,10,15,11,14,12,13]

unchanged_boxes = [0,1,2,3,4,5,6,7]
#unchanged_boxes = [0,1,2,3,4,5,6,7,8]
# -------------------------------------------------------

# Re-do with np arrays.  Still this feels a bit hacky


for ii in range(np.shape(pdf_arrays_O2)[0]):
    for jj in range(np.shape(pdf_arrays_O2)[1]):
        if ii == 0:
            pf = np.copy(pdf_arrays_connectivity[jj,:,:])
            pfTimes = np.copy(pdf_arrays_settleTime[jj,:,:])
            pfT = np.copy(pdf_arrays_T[jj,:,:])
        pfO2 = np.copy(pdf_arrays_O2[ii,jj,:,:])

        # Rows
        if ii == 0:
            pf[dx2_og] = pf[dx2_new]
            pfTimes[dx2_og] = pfTimes[dx2_new]
            pfT[dx2_og] = pfT[dx2_new]
        pfO2[dx2_og] = pfO2[dx2_new]
        
        # Columns
        if ii == 0:
            pf[:,dx2_og] = pf[:,dx2_new]

        if ii == 0:
            pdf_arrays_connectivity_swapped[jj,:,:] = pf
            pdf_arrays_settleTime_swapped[jj,:,:] = pfTimes
            pdf_arrays_T_swapped[jj,:,:] = pfT
        pdf_arrays_O2_swapped[ii,jj,:,:] = pfO2
    
for ii in range(np.shape(pdf_arrays_pH)[0]):
    for jj in range(np.shape(pdf_arrays_pH)[1]):
        pfpH = np.copy(pdf_arrays_pH[ii,jj,:,:])
        pfpH[dx2_og] = pfpH[dx2_new]
        pdf_arrays_pH_swapped[ii,jj,:,:] = pfpH


#for ii in range(len(pdf_arrays_O2)):
#    for jj in range(len(pdf_list_connectivity)):
#        if ii == 0:
#            pf = np.copy(pdf_list_connectivity[jj])
#            pfTimes = np.copy(pdf_list_settleTime[jj])
#            pfT = np.copy(pdf_arrays_T[jj])
#        pfO2 = np.copy(pdf_arrays_O2[ii][jj])
#
#        # Rows
#        if ii == 0:
#            pf[dx2_og] = pf[dx2_new]
#            pfTimes[dx2_og] = pfTimes[dx2_new]
#            pfT[dx2_og] = pfT[dx2_new]
#        pfO2[dx2_og] = pfO2[dx2_new]
#        
#        # Columns
#        if ii == 0:
#            pf[:,dx2_og] = pf[:,dx2_new]
#
#        if ii == 0:
#            pdf_list_connectivity_swapped.append(pf)
#            pdf_list_settleTime_swapped.append(pfTimes)
#            pdf_arrays_T_swapped.append(pfT)
#        pdf_arrays_O2_swapped[ii].append(pfO2)
#    
#for ii in range(len(pdf_arrays_pH)):
#    for jj in range(len(pdf_list_connectivity)):
#        pfpH = np.copy(pdf_arrays_pH[ii][jj])
#        pfpH[dx2_og] = pfpH[dx2_new]
#        pdf_arrays_pH_swapped[ii].append(pfpH)





# -------------------------------------------------------
# Brute force determine number of boxes, for consistent saving of labels.
# Note: I'm still manually setting island box numbers to keep/save, so this script isn't fully automatic.
# -------------------------------------------------------
num_islands = 8
num_last_blob_island = 4
box_num = 0
#box_num = 1
for island_dex in range(num_islands,num_last_blob_island-1,-1):
    bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15n_island_number_{}.p'.format(island_dex)
    file = open(bounding_boxes_file_in,'rb')
    boxes_lonlat = pickle.load(file)
    file.close
    for box in reversed(boxes_lonlat):
        if box is not None:
            box_num += 1

first_continent_box_num = box_num

bounding_boxes_file_in = input_dir_continent + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(points_type_line)
file = open(bounding_boxes_file_in,'rb')
boxes_lonlat = pickle.load(file)
file.close
for box in boxes_lonlat:
    if box is not None:
        box_num += 1
# -------------------------------------------------------





# -------------------------------------------------------
# Saving ticks, labels, box numbers, so it's all in one place.  Save, load, use...
# -------------------------------------------------------

#dx2_new = [8,15,9,14,10,13,11,12]

# Just manually determining this... 
blob_new_numbers_print = [8,10,12,14,15,13,11,9]
#blob_new_numbers_print = [9,11,13,15,16,14,12,10]

box_num_islands_mod = unchanged_boxes + blob_new_numbers_print
box_num_mod = box_num_islands_mod + list(range(max(box_num_islands_mod) + 1, box_num+1))
#box_num_mod = box_num_islands_mod + list(range(max(box_num_islands_mod) + 1, box_num))


# May as well save the box numbers to use for labels here
#dx2_new = [9,16,10,15,11,14,12,13]
box_num_labels_islands_print = [0,2,4,6,8,10,12,14]
#box_num_labels_islands_print = [1,3,5,7,9,11,13,15] # one off? (one too large)
###box_num_labels_islands_print = [2,6,9,11,13,15,17,20] # Old island boxes
box_num_labels_continent_print = [19,25,30,33,37,43,52,56,63,73] # fixed the one off?
#box_num_labels_continent_print = [20,26,31,34,38,44,53,57,64,74] # one off?
###box_num_labels_continent_print = [24,30,33,38,42,48,57,61,68,78] # old island boxes

box_num_labels_print = box_num_labels_islands_print + box_num_labels_continent_print



tick_labels_continent = ['TJ','PV','PM','PC','PB','CB','PR','PA','CM','CBl']
tick_labels_islands = ['SCl','Ca','SB','SN','SM','SR','SC','An']

tick_labels = tick_labels_islands + tick_labels_continent

# Wait, maybe this is what I want
tick_positions = box_num_labels_print
#tick_positions = [x -1 for x in box_num_labels_print]

# -------------------------------------------------------
# -------------------------------------------------------

d = {}
#d['settlers_timestep_settled'] = settlers_timestep_settled
#d['settlers_assigned_bio_windows'] = settlers_assigned_bio_windows
#d['bio_window_opening_distribution'] = bio_window_opening_distribution
d['pdf_arrays_T'] = pdf_arrays_T_swapped
d['pdf_arrays_O2'] = pdf_arrays_O2_swapped
d['pdf_arrays_pH'] = pdf_arrays_pH_swapped
d['pdf_arrays_connectivity'] = pdf_arrays_connectivity_swapped
d['pdf_arrays_settleTime'] = pdf_arrays_settleTime_swapped

#d['pdf_arrays_T_swapped'] = pdf_arrays_T_swapped
#d['pdf_arrays_O2_swapped'] = pdf_arrays_O2_swapped
#d['pdf_list_connectivity_swapped'] = pdf_list_connectivity_swapped
#d['pdf_list_settleTime_swapped'] = pdf_list_settleTime_swapped

d['counter_array'] = counter_array
d['oxygen_limit_list'] = oxygen_limit_list
d['pH_limit_list'] = pH_limit_list
d['box_num_mod'] = box_num_mod
d['tick_positions'] = tick_positions
d['tick_labels'] = tick_labels
d['first_continent_box_num'] = first_continent_box_num

np.savez(pdf_swapped_file_out, **d)


print(np.shape(pdf_arrays_O2_swapped))

#file = open(pdf_swapped_file_out,'wb')
#pickle.dump([bio_window_opening_distribution,pdf_arrays_T_swapped,pdf_arrays_O2_swapped,pdf_list_connectivity_swapped,pdf_list_settleTime_swapped,counter_array,box_num_mod,tick_positions,tick_labels,first_continent_box_num,oxygen_limit_list],file)
#file.close()





