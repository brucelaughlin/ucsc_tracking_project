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

st = settlement_times_test_array
sb = settlement_boxes_test_array

print(np.amax(st))

st_numBad = 0
sb_numBad = 0

st_numS = 0
sb_numS = 0
st_numNS = 0
sb_numNS = 0

st_numOdd = 0
sb_numOdd = 0

#Check if there are more than 1 non-zero entry for any particle (ie settlement recorded more than once)
for ii in range(np.shape(st)[0]):
    if np.sum(st[ii,:]==0) < np.shape(st)[1]-1:
        st_numBad += 1
    elif np.sum(st[ii,:]==0) == np.shape(st)[1]-1:
        st_numS += 1
    elif np.sum(st[ii,:]==0) == np.shape(st)[1]:
        st_numNS += 1
    else:
        st_numOdd += 1

    if np.sum(sb[ii,:]==0) < np.shape(sb)[1]-1:
        sb_numBad += 1
    elif np.sum(sb[ii,:]==0) == np.shape(sb)[1]-1:
        sb_numS += 1
    elif np.sum(sb[ii,:]==0) == np.shape(sb)[1]:
        sb_numNS += 1
    else:
        sb_numOdd += 1

print("numBad:")
print(st_numBad)
print(sb_numBad)
print("numS:")
print(st_numS)
print(sb_numS)
print("numNS:")
print(st_numNS)
print(sb_numNS)
print("numGood:")
print(st_numS+st_numNS)
print(sb_numS+sb_numNS)
print("numParticles:")
print(np.shape(st)[0])
print("numOdd:")
print(st_numOdd)
print(sb_numOdd)


#fig,axs = plt.subplots()
#
#n_particles = int(np.shape(settlement_times_test_array)[0])
#n_boxes = int(np.shape(settlement_times_test_array)[1])
#X = np.arange(-0.5, n_particles, 1)
#Y = np.arange(-0.5, n_boxes, 1)
#
#mesh1 = axs.pcolormesh(X,Y,settlement_times_test_array,cmap='jet')
#plt.colorbar(mesh1)
#plt.show()

