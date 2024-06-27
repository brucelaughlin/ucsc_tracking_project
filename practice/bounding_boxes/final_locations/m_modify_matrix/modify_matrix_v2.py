# Looking at the domain plots of islands, I realize that my box numbers for islands (especially islands 1,2 and 5-8)
# are not "in order" - in other words, the pdf won't look intuitive, since, for instance, boxes 13 and 20 represent
# the same island, but will appear far apart

# box index (ie "number" - 1) order changes: 
# [0,1,2,3] - > [1,2,1,3]
# [12,13,14,15,16,17,18,19,20] -> [12,19,13,18,14,17,15,16]


import pickle
import numpy as np
import matplotlib.pyplot as plt

base_path = '/home/blaughli/tracking_project/'
pdf_raw_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'

pdf_raw_file = pdf_raw_directory + 'pdf_data_output_seasonal_test3.p'

pdf_modified_file_out = pdf_raw_directory + 'pdf_data_output_seasonal_test3_modified.p'

file = open(pdf_raw_file,'rb')
p0,p1,p2,p3,p4,counter_array = pickle.load(file)  # When the new calc is done, saved a counter_array for checking consistency
#pdf_raw,pdf_raw_djf,pdf_raw_mam,pdf_raw_jja,pdf_raw_son,counter_array = pickle.load(file)  # When the new calc is done, saved a counter_array for checking consistency
file.close()

pdf_list = []
pdf_list.append(p0)
pdf_list.append(p1)
pdf_list.append(p2)
pdf_list.append(p3)
pdf_list.append(p4)

pdf_list_modified = []

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

for jj in range(len(pdf_list)):

    pf = np.copy(pdf_list[jj])

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
    #    if jj == 0:
    #        dx2[swap_dst2[ii]], dx2[swap_src2[ii]] = dx2[swap_src2[ii]], dx2[swap_dst2[ii]]
    #columns
    pf[:,dx2_og] = pf[:,dx2_new]
    #for ii in range(len(swap_dst2)):
    #    pf[:,[swap_dst2[ii],swap_src2[ii]]] = pf[:,[swap_src2[ii],swap_dst2[ii]]]

    pdf_list_modified.append(pf)
    
#print(dx1)
#print(dx2)

pm0 = pdf_list_modified[0]
pm1 = pdf_list_modified[1]
pm2 = pdf_list_modified[2]
pm3 = pdf_list_modified[3]
pm4 = pdf_list_modified[4]

box_num_islands_mod = unchanged_boxes + dx2_new
#box_num_islands_mod = unchanged_boxes + dx2
#box_num_islands_mod = dx1 + unchanged_boxes + dx2

# May as well save the box numbers to use for labels here
box_num_labels_print = [2,6,9,11,13,15,17,20]
#box_num_labels_real = [2,6,9,11,13,14,15,16]

file = open(pdf_modified_file_out,'wb')
#pickle.dump([pm0,pm1,pm2,pm3,pm4,counter_array,box_num_islands_mod,box_num_labels_print,box_num_labels_real],file)
pickle.dump([pm0,pm1,pm2,pm3,pm4,counter_array,box_num_islands_mod,box_num_labels_print],file)
#pickle.dump([pm0,pm1,pm2,pm3,pm4,counter_array,box_num_islands_mod],file)
#pickle.dump([p0,p1,p2,p3,p4,counter_array],file)
file.close()









#pf[[0,1]] = pf[[1,0]]
#pf[[1,2]] = pf[[2,1]]
#pf[:,[0,1]] = pf[:,[1,0]]
#pf[:,[1,2]] = pf[:,[2,1]]


# [12,13,14,15,16,17,18,19,20] -> [12,19,13,18,14,17,15,16]

