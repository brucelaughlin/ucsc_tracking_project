# Looking at the domain plots of islands, I realize that my box numbers for islands (especially islands 1,2 and 5-8)
# are not "in order" - in other words, the pdf won't look intuitive, since, for instance, boxes 13 and 20 represent
# the same island, but will appear far apart

# v12: just adding the "release_counts_per_cell" key

# v11: add argparse - time to mature

#v8: switched to np.savez saving

# v7: just added more settlement time statistics, but didn't want to break anything

#V6: had one-off error in the tick_positions.  Should maybe just do away with the "box number" idea, and start at 0 (not 1)

#V5: now we have a list of lists for O2 data saved (we test at multiple exposure levels)

#V4: using updated island boxes, saving V3 in case

#V3: using new histogram save format (lists)

# box index (ie "number" - 1) order changes: 
# [9,10,11,12,13,14,15,16] -> [9,16,10,15,11,14,12,13]



import pickle
import numpy as np
import os
import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("input_file")
args = parser.parse_args()
pdf_file_name = args.input_file



base_path = '/home/blaughli/tracking_project/'
pdf_raw_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'

#pdf_raw_file = pdf_raw_directory + pdf_file_name

pdf_raw_file = pdf_file_name

base = os.path.splitext(pdf_raw_file)[0]

swapped_directory = base.rsplit('/', 1)[0] + '/z_swapped/'
Path(swapped_directory).mkdir(parents=True, exist_ok=True)


pdf_file_swapped_name = swapped_directory + base.split('/')[-1] + "_swapped"
#pdf_file_swapped_name = swapped_directory + base.split('/')[-1] 
#pdf_file_swapped_name = swapped_directory + base.split('/')[-1] + ".npz"

#pdf_file_swapped_name = os.path.splitext(pdf_file_name)[0] + "_swapped"

pdf_swapped_file_out = pdf_file_swapped_name

box_dir = base_path + 'practice/bounding_boxes/create_boxes/'
islands_dir = 'modify_islands/'
#islands_dir = 'aa_islands/'
continent_dir = 'continent/'
input_dir_islands = box_dir + islands_dir + 'z_output/'
input_dir_continent = box_dir + continent_dir + 'z_output/'




#file = open(pdf_raw_file,'rb')
#bio_window_opening_distribution,pdf_arrays_T,pdf_arrays_O2,pdf_list_connectivity,pdf_list_settleTime,counter_array,O2_limit_list = pickle.load(file)
#file.close()

d = np.load(pdf_raw_file)

pdf_arrays_T = d['pdf_arrays_T']
pdf_arrays_O2 = d['pdf_arrays_O2']
pdf_arrays_pH = d['pdf_arrays_pH']
pdf_arrays_connectivity = d['pdf_arrays_connectivity']
release_counts_per_cell  = d['release_counts_per_cell']
pdf_arrays_settleTime = d['pdf_arrays_settleTime']
counter_array = d['counter_array']
O2_limit_list = d['O2_limit_list']
pH_limit_list = d['pH_limit_list']

release_counts_per_cell_swapped = np.zeros_like(release_counts_per_cell)
pdf_arrays_connectivity_swapped = np.zeros_like(pdf_arrays_connectivity)
pdf_arrays_settleTime_swapped = np.zeros_like(pdf_arrays_settleTime)
pdf_arrays_T_swapped = np.zeros_like(pdf_arrays_T)
pdf_arrays_O2_swapped = np.zeros_like(pdf_arrays_O2)
pdf_arrays_pH_swapped = np.zeros_like(pdf_arrays_pH)

print(np.shape(pdf_arrays_O2))

print(np.shape(release_counts_per_cell))

# -------------------------------------------------------
# ISLANDS 4-8
dx2_og =  [8,9,10,11,12,13,14,15]
dx2_new = [8,15,9,14,10,13,11,12]

unchanged_boxes = [0,1,2,3,4,5,6,7]
# -------------------------------------------------------

# Re-do with np arrays.  Still this feels a bit hacky


for ii in range(np.shape(pdf_arrays_O2)[0]):
    for jj in range(np.shape(pdf_arrays_O2)[1]):
        if ii == 0:
            prc = np.copy(release_counts_per_cell[jj,:])
            pf = np.copy(pdf_arrays_connectivity[jj,:,:])
            pfTimes = np.copy(pdf_arrays_settleTime[jj,:,:])
            pfT = np.copy(pdf_arrays_T[jj,:,:])
        pfO2 = np.copy(pdf_arrays_O2[ii,jj,:,:])

        # Rows
        if ii == 0:
            prc[dx2_og] = prc[dx2_new]
            pf[dx2_og] = pf[dx2_new]
            pfTimes[dx2_og] = pfTimes[dx2_new]
            pfT[dx2_og] = pfT[dx2_new]
        pfO2[dx2_og] = pfO2[dx2_new]
        
        # Columns
        if ii == 0:
            prc[dx2_og] = prc[dx2_new]
            pf[:,dx2_og] = pf[:,dx2_new]

        if ii == 0:
            release_counts_per_cell_swapped[jj,:] = prc
            pdf_arrays_connectivity_swapped[jj,:,:] = pf
            pdf_arrays_settleTime_swapped[jj,:,:] = pfTimes
            pdf_arrays_T_swapped[jj,:,:] = pfT
        pdf_arrays_O2_swapped[ii,jj,:,:] = pfO2
    
for ii in range(np.shape(pdf_arrays_pH)[0]):
    for jj in range(np.shape(pdf_arrays_pH)[1]):
        pfpH = np.copy(pdf_arrays_pH[ii,jj,:,:])
        pfpH[dx2_og] = pfpH[dx2_new]
        pdf_arrays_pH_swapped[ii,jj,:,:] = pfpH





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

bounding_boxes_file_in = input_dir_continent + 'bounding_boxes_lonlat_coords_psi_coastline_wc15n_continent.p'
#bounding_boxes_file_in = input_dir_continent + 'bounding_boxes_lonlat_coords_{}_coastline_wc15n_continent.p'.format(points_type_line)
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


# REMEMBER - WHEN LOOKING AT THE DOMAIN PLOT, THE FIRST BOX HAS NUMBER 1.  HERE, THE FIRST BOX HAS INDEX 0.  SO SUBTRACT
# 1 FROM WHAT YOU SEE ON THE DOMAIN PLOT!!!

# May as well save the box numbers to use for labels here
box_num_labels_islands_print = [0,2,4,6,8,10,12,14]
box_num_labels_continent_print = [19,25,30,33,37,42,52,56,63,73,77] # fixed the one off?
box_num_labels_print = box_num_labels_islands_print + box_num_labels_continent_print



tick_labels_continent = ['TJ','PV','PM','PC','PB','PS','PR','PA','CM','CB','HB']
tick_labels_islands = ['SCl','Ca','SB','SN','SM','SR','SC','An']
tick_labels = tick_labels_islands + tick_labels_continent

# Wait, maybe this is what I want
tick_positions = box_num_labels_print

# -------------------------------------------------------
# -------------------------------------------------------

d = {}
d['pdf_arrays_T'] = pdf_arrays_T_swapped
d['pdf_arrays_O2'] = pdf_arrays_O2_swapped
d['pdf_arrays_pH'] = pdf_arrays_pH_swapped
d['pdf_arrays_connectivity'] = pdf_arrays_connectivity_swapped
d['pdf_arrays_settleTime'] = pdf_arrays_settleTime_swapped
d['release_counts_per_cell'] = release_counts_per_cell_swapped

d['counter_array'] = counter_array
d['O2_limit_list'] = O2_limit_list
d['pH_limit_list'] = pH_limit_list
d['box_num_mod'] = box_num_mod
d['tick_positions'] = tick_positions
d['tick_labels'] = tick_labels
d['first_continent_box_num'] = first_continent_box_num

np.savez(pdf_swapped_file_out, **d)


#print(pdf_swapped_file_out)

print(np.shape(pdf_arrays_O2_swapped))






