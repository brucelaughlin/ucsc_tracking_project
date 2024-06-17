#V2: add a few blank lines in both dimensions to separate the islands from the mainland


import pickle
import numpy as np
import matplotlib.pyplot as plt

base_path = '/home/blaughli/tracking_project/'
save_output_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'

save_output_file = save_output_directory + 'pdf_data_output_originalOrder.p'

file = open(save_output_file,'rb')
pdf_raw = pickle.load(file)
#pdf_raw, counter_array = pickle.load(file)  # When the new calc is done, saved a counter_array for checking consistency
file.close()

pdf_raw = np.log10(pdf_raw)
#pdf_raw = np.log(pdf_raw)

# Determined elsewhere (see/run "check_box_numbers.py")
first_continent_box_dex = 20
num_dummy_lines = 1

pdf_separated = np.empty((np.shape(pdf_raw)[0] + num_dummy_lines,np.shape(pdf_raw)[0] + num_dummy_lines))
pdf_separated[:] = np.nan

pdf_separated[0:first_continent_box_dex-1,0:first_continent_box_dex-1] = pdf_raw[0:first_continent_box_dex-1,0:first_continent_box_dex-1]
pdf_separated[first_continent_box_dex + num_dummy_lines:,0:first_continent_box_dex-1] = pdf_raw[first_continent_box_dex:,0:first_continent_box_dex-1]
pdf_separated[0:first_continent_box_dex-1,first_continent_box_dex + num_dummy_lines:] = pdf_raw[0:first_continent_box_dex-1,first_continent_box_dex:]
#pdf_separated[first_continent_box_dex + num_dummy_lines-1:,first_continent_box_dex + num_dummy_lines-1:] = pdf_raw[first_continent_box_dex:,first_continent_box_dex:]
pdf_separated[first_continent_box_dex + num_dummy_lines:,first_continent_box_dex + num_dummy_lines:] = pdf_raw[first_continent_box_dex:,first_continent_box_dex:]

n_boxes_seeded = int(np.shape(pdf_separated)[1])
n_boxes_settled = int(np.shape(pdf_separated)[0])
X = np.arange(-0.5, n_boxes_settled, 1)
Y = np.arange(-0.5, n_boxes_seeded, 1)
fig,ax = plt.subplots()
#ax.pcolormesh(X,Y,pdf_separated,cmap='jet')
mesh1 = ax.pcolormesh(X,Y,pdf_separated,cmap='jet')

plt.colorbar(mesh1)

ax.set_xlabel("seeding box number")
ax.set_ylabel("settlement box number")
plt.title("PDF of settlement vs seed location")
plt.show()



#n_boxes_seeded = snt(np.shape(sdf_raw)[1])
#n_boxes_settled = int(np.shape(pdf_raw)[0])
#X = np.arange(-0.5, n_boxes_settled, 1)
#Y = np.arange(-0.5, n_boxes_seeded, 1)
#fig,ax = plt.subplots()
#ax.pcolormesh(X,Y,pdf_raw,cmap='jet')
#ax.set_xlabel("seeding box number")
#ax.set_ylabel("settlement box number")
#plt.title("PDF of settlement vs seed location")
#plt.show()


