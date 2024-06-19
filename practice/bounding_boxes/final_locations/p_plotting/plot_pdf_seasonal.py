
import pickle
import numpy as np
import matplotlib.pyplot as plt

base_path = '/home/blaughli/tracking_project/'
pdf_raw_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'

#pdf_raw_file = pdf_raw_directory + 'pdf_data_output_originalOrder.p'
#pdf_raw_file = pdf_raw_directory + 'pdf_data_output.p'
pdf_raw_file = pdf_raw_directory + 'pdf_data_output_seasonal.p'

file = open(pdf_raw_file,'rb')
pdf_raw,pdf_raw_djf,pdf_raw_mam,pdf_raw_jja,pdf_raw_son,counter_array = pickle.load(file)  # When the new calc is done, saved a counter_array for checking consistency
file.close()

pdf_list = []

pdf_list.append(np.log10(np.transpose(pdf_raw_djf)))
pdf_list.append(np.log10(np.transpose(pdf_raw_mam)))
pdf_list.append(np.log10(np.transpose(pdf_raw_jja)))
pdf_list.append(np.log10(np.transpose(pdf_raw_son)))
#pdf_list.append(np.log10(pdf_raw_djf))
#pdf_list.append(np.log10(pdf_raw_mam))
#pdf_list.append(np.log10(pdf_raw_jja))
#pdf_list.append(np.log10(pdf_raw_son))

# Determined elsewhere (see/run "check_box_numbers.py")
first_continent_box_dex = 20
num_dummy_lines = 1

tick_positions = [0,4,8,10,12,37,41,48,56,60,67,78]
tick_labels = ['SC','C','SB','SN','SM','PC','PB','M','PR','PA','PM','CB']

fig,axs = plt.subplots(2,2)
plt.setp(axs,xticks=tick_positions,xticklabels=tick_labels,yticks=tick_positions,yticklabels=tick_labels)


ii = 0
for pdf_plot in pdf_list:

    ii += 1

    pdf_separated = np.empty((np.shape(pdf_plot)[0] + num_dummy_lines,np.shape(pdf_plot)[1] + num_dummy_lines))
    #pdf_separated = np.empty((np.shape(pdf_plot)[0] + num_dummy_lines,np.shape(pdf_plot)[0] + num_dummy_lines))
    pdf_separated[:] = np.nan

    pdf_separated[0:first_continent_box_dex,0:first_continent_box_dex] = pdf_plot[0:first_continent_box_dex,0:first_continent_box_dex]
    pdf_separated[first_continent_box_dex + num_dummy_lines:,0:first_continent_box_dex] = pdf_plot[first_continent_box_dex:,0:first_continent_box_dex]
    pdf_separated[0:first_continent_box_dex,first_continent_box_dex + num_dummy_lines:] = pdf_plot[0:first_continent_box_dex,first_continent_box_dex:]
    pdf_separated[first_continent_box_dex + num_dummy_lines:,first_continent_box_dex + num_dummy_lines:] = pdf_plot[first_continent_box_dex:,first_continent_box_dex:]
    #pdf_separated[0:first_continent_box_dex-1,0:first_continent_box_dex-1] = pdf_plot[0:first_continent_box_dex-1,0:first_continent_box_dex-1]
    #pdf_separated[first_continent_box_dex + num_dummy_lines:,0:first_continent_box_dex-1] = pdf_plot[first_continent_box_dex:,0:first_continent_box_dex-1]
    #pdf_separated[0:first_continent_box_dex-1,first_continent_box_dex + num_dummy_lines:] = pdf_plot[0:first_continent_box_dex-1,first_continent_box_dex:]
    #pdf_separated[first_continent_box_dex + num_dummy_lines:,first_continent_box_dex + num_dummy_lines:] = pdf_plot[first_continent_box_dex:,first_continent_box_dex:]

    n_boxes_seeded = int(np.shape(pdf_separated)[1])
    n_boxes_settled = int(np.shape(pdf_separated)[0])
    X = np.arange(-0.5, n_boxes_settled, 1)
    Y = np.arange(-0.5, n_boxes_seeded, 1)

    #fig,ax = plt.subplots()
    #ax.pcolormesh(X,Y,pdf_separated,cmap='jet')
    if ii == 1:
        mesh1 = axs[0,0].pcolormesh(X,Y,pdf_separated,cmap='jet')
    elif ii == 2:
        mesh1 = axs[0,1].pcolormesh(X,Y,pdf_separated,cmap='jet')
    elif ii == 3:
        mesh1 = axs[1,0].pcolormesh(X,Y,pdf_separated,cmap='jet')
    else:
        mesh1 = axs[1,1].pcolormesh(X,Y,pdf_separated,cmap='jet')

    plt.colorbar(mesh1)

    
    
    #ax.set_xlabel("seeding box number")
    #ax.set_ylabel("settlement box number")
    #plt.title("PDF of settlement vs seed location")
plt.show()

#
#fig,axs = plt.subplots(2,2)
#ii = 0
#for pdf_plot in pdf_list:
#
#    ii += 1
#
#    n_boxes_seeded = int(np.shape(pdf_raw)[1])
#    n_boxes_settled = int(np.shape(pdf_raw)[0])
#    X = np.arange(-0.5, n_boxes_settled, 1)
#    Y = np.arange(-0.5, n_boxes_seeded, 1)
#    if ii == 1:
#        mesh1 = axs[0,0].pcolormesh(X,Y,pdf_plot,cmap='jet')
#    elif ii == 2:
#        mesh1 = axs[0,1].pcolormesh(X,Y,pdf_plot,cmap='jet')
#    elif ii == 3:
#        mesh1 = axs[1,0].pcolormesh(X,Y,pdf_plot,cmap='jet')
#    else:
#        mesh1 = axs[1,1].pcolormesh(X,Y,pdf_plot,cmap='jet')
#
#    plt.colorbar(mesh1)
#
#    #ax.set_xlabel("seeding box number")
#    #ax.set_ylabel("settlement box number")
#    #plt.title("PDF of settlement vs seed location")
#plt.show()
#
#


