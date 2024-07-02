# Looking at the domain plots of islands, I realize that my box numbers for islands (especially islands 1,2 and 5-8)
# are not "in order" - in other words, the pdf won't look intuitive, since, for instance, boxes 13 and 20 represent
# the same island, but will appear far apart

#V3: using new histogram save format (lists)

# box index (ie "number" - 1) order changes: 
# [0,1,2,3] - > [1,2,1,3]
# [12,13,14,15,16,17,18,19,20] -> [12,19,13,18,14,17,15,16]


# -------------------------------------------------------
# Input file
# -------------------------------------------------------
pdf_file_name = 'pdf_data_output_releaseLoc_vs_settleTime_test3.p'
# -------------------------------------------------------


import pickle
import numpy as np
import matplotlib.pyplot as plt

base_path = '/home/blaughli/tracking_project/'
pdf_raw_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'

pdf_raw_file = pdf_raw_directory + pdf_file_name
pdf_file_swapped_name = pdf_file_name[0:-2] + "_swapped.p"
pdf_swapped_file_out = pdf_raw_directory + pdf_file_swapped_name

points_type_line = 'psi'
box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'aa_islands/'
continent_dir = 'continent/'
input_dir_islands = box_dir + islands_dir + 'z_output/'
input_dir_continent = box_dir + continent_dir + 'z_output/'





file = open(pdf_raw_file,'rb')
pdf_list_connectivity,pdf_list_settleTime,settlement_boxes_test_array,settlement_times_test_array,counter_array = pickle.load(file)
file.close()

pdf_list_connectivity_swapped = []
pdf_list_settleTime_swapped = []




# -------------------------------------------------------
## ISLAND 1
#dx1 = [0,1,2,3]
#swap_dst1 = [0,1]
#swap_src1 = [1,2]

# ISLANDS 4-8
dx2_og = [12,13,14,15,16,17,18,19]
dx2_new = [12,14,16,18,19,17,15,13]
#swap_dst2 = [3,4,2,1]
#swap_src2 = [6,7,4,2]

unchanged_boxes = [0,1,2,3,4,5,6,7,8,9,10,11]
#unchanged_boxes = [4,5,6,7,8,9,10,11]
# -------------------------------------------------------

#print(dx1)
#print(dx2)

for jj in range(len(pdf_list_connectivity)):

    pf = np.copy(pdf_list_connectivity[jj])
    pfTimes = np.copy(pdf_list_settleTime[jj])

#    # ISLAND 1
#    # rows
#    for ii in range(len(swap_dst1)):
#        pf[[swap_dst1[ii],swap_src1[ii]]] = pf[[swap_src1[ii],swap_dst1[ii]]]
#        if jj == 0:
#            dx1[swap_dst1[ii]], dx1[swap_src1[ii]] = dx1[swap_src1[ii]], dx1[swap_dst1[ii]]
#    #columns
#    for ii in range(len(swap_dst1)):
#        pf[:,[swap_dst1[ii],swap_src1[ii]]] = pf[:,[swap_src1[ii],swap_dst1[ii]]]


    # ISLANDS 4-8
    # rows
    #for ii in range(len(swap_dst2)):
    #    pf[[swap_dst2[ii],swap_src2[ii]]] = pf[[swap_src2[ii],swap_dst2[ii]]]
    pf[dx2_og] = pf[dx2_new]
    pfTimes[dx2_og] = pfTimes[dx2_new]
    #    if jj == 0:
    #        dx2[swap_dst2[ii]], dx2[swap_src2[ii]] = dx2[swap_src2[ii]], dx2[swap_dst2[ii]]
    #columns
    pf[:,dx2_og] = pf[:,dx2_new]
    #for ii in range(len(swap_dst2)):
    #    pf[:,[swap_dst2[ii],swap_src2[ii]]] = pf[:,[swap_src2[ii],swap_dst2[ii]]]

    pdf_list_connectivity_swapped.append(pf)
    pdf_list_settleTime_swapped.append(pfTimes)
    
#print(dx1)
#print(dx2)





# -------------------------------------------------------
# Brute force determine number of boxes, for consistent saving of labels.
# Note: I'm still manually setting island box numbers to keep/save, so this script isn't fully automatic.
# -------------------------------------------------------
num_islands = 8
num_last_blob_island = 4
box_num = 1
for island_dex in range(num_islands,num_last_blob_island-1,-1):
    for inoffshore_switch in range(0,2):
        if inoffshore_switch == 1:
            bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15n_island_number_{}_inshore.p'.format(island_dex)
        else:
            bounding_boxes_file_in = input_dir_islands + 'bounding_boxes_lonlat_wc15n_island_number_{}_offshore.p'.format(island_dex)
        file = open(bounding_boxes_file_in,'rb')
        boxes_lonlat = pickle.load(file)
        file.close
        for box in reversed(boxes_lonlat):
            if box is not None:
                box_num += 1
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

box_num_islands_mod = unchanged_boxes + dx2_new
#box_num_islands_mod = unchanged_boxes + dx2
#box_num_islands_mod = dx1 + unchanged_boxes + dx2

box_num_mod = box_num_islands_mod + list(range(max(box_num_islands_mod) + 1, box_num))



#dx2_new = [12,14,16,18,19,17,15,13]
# May as well save the box numbers to use for labels here
#box_num_labels_print = [2,6,9,11,13,15,17,20] - 1
box_num_labels_islands_print = [2,6,9,11,13,15,17,20]
#box_num_labels_real = [2,6,9,11,13,14,15,16]
box_num_labels_continent_print = [24,30,33,38,42,48,57,61,68,78]
#box_num_labels_continent_print = [23,29,32,37,41,47,56,60,67,77]

box_num_labels_print = box_num_labels_islands_print + box_num_labels_continent_print



#tick_positions_continent =  [23,29,32,37,41,47,56,60,67,78]
#tick_positions_islands = box_num_labels_islands_print
#tick_positions_islands = [x-1 for x in box_num_labels_print]
tick_labels_continent = ['TJ','PV','PM','PC','PB','CB','PR','PA','CM','CBl']
tick_labels_islands = ['SCl','Ca','SB','SN','SM','SR','SC','An']
#tick_labels_islands = ['SCl','Ca','SB','SN','SR','An','SC','SM']
#tick_labels_islands = ['SC','C','SB','SN','SR','A','SC','SM']

tick_positions = [x -1 for x in box_num_labels_print]
#tick_positions = box_num_labels_print
#tick_positions = tick_positions_islands + tick_positions_continent
tick_labels = tick_labels_islands + tick_labels_continent

# -------------------------------------------------------
# -------------------------------------------------------


file = open(pdf_swapped_file_out,'wb')
pickle.dump([pdf_list_connectivity_swapped,pdf_list_settleTime_swapped,settlement_boxes_test_array,settlement_times_test_array,counter_array,box_num_mod,tick_positions,tick_labels],file)
#pickle.dump([pm0,pm1,pm2,pm3,pm4,counter_array,box_num_islands_mod,box_num_labels_print,box_num_labels_real],file)
#pickle.dump([pm0,pm1,pm2,pm3,pm4,counter_array,box_num_islands_mod,box_num_labels_print],file)
#pickle.dump([pm0,pm1,pm2,pm3,pm4,counter_array,box_num_islands_mod],file)
#pickle.dump([p0,p1,p2,p3,p4,counter_array],file)
file.close()









#pf[[0,1]] = pf[[1,0]]
#pf[[1,2]] = pf[[2,1]]
#pf[:,[0,1]] = pf[:,[1,0]]
#pf[:,[1,2]] = pf[:,[2,1]]


# [12,13,14,15,16,17,18,19,20] -> [12,19,13,18,14,17,15,16]

