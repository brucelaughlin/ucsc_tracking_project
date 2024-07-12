
import pickle
import numpy as np
import matplotlib.pyplot as plt


#-------------------- EDIT THESE -------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
mask_dir = '/home/blaughli/tracking_project/practice/bounding_boxes/create_boxes/continent/z_modify_psi/'

mask_file = 'mask_psi_bl_islands.p'

mask_path = mask_dir + mask_file
#---------------------------------------------------------------------
#---------------------------------------------------------------------


file = open(mask_path,'rb')
#mask_pre = pickle.load(file)
mask = pickle.load(file)
file.close

#mask = mask_pre.astype(int)

fig, ax = plt.subplots()
ax.pcolormesh(range(np.shape(mask)[1]),range(np.shape(mask)[0]),mask,shading="nearest")

plt.show()


