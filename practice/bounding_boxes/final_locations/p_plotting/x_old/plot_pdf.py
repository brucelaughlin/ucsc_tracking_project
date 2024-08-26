# Error - think I need to use lat/lon, as in version 1 I just used i/j which
# depends on the grid type... ie it's wrong to use i/j from a polygon in psi
# to bound rho points... 

# Note that "status" is 0 when the particle and active, and a large magnitude negative
# number when not.  (strange!)

import pickle
import numpy as np
import matplotlib.pyplot as plt

base_path = '/home/blaughli/tracking_project/'
save_output_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'

save_output_file = save_output_directory + 'pdf_data_output.p'
#save_output_file = save_output_directory + 'pdf_data_output_test2.p'

file = open(save_output_file,'rb')
pdf_raw = pickle.load(file)
file.close()

#n_boxes_seeded = int(np.max(initial_boxes))
#n_boxes_settled = int(np.max(settlement_boxes))
n_boxes_seeded = int(np.shape(pdf_raw)[1])
n_boxes_settled = int(np.shape(pdf_raw)[0])
X = np.arange(-0.5, n_boxes_settled, 1)
Y = np.arange(-0.5, n_boxes_seeded, 1)
fig,ax = plt.subplots()
###ax.pcolormesh(pdf_raw)
#ax.pcolormesh(X,Y,pdf_raw)
ax.pcolormesh(X,Y,pdf_raw,cmap='jet')
ax.set_xlabel("seeding box number")
ax.set_ylabel("settlement box number")
plt.title("PDF of settlement vs seed location")
plt.show()


