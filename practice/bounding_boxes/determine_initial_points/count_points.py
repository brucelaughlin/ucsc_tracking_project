import pickle
import numpy as np

base_path = '/home/blaughli/tracking_project/'
box_base = base_path + 'practice/bounding_boxes/determine_initial_points/z_output/'

box_file_lon_lat_pre = 'points_in_boxes_lon_lat_combined.p'
box_lon_lat_file = box_base + box_file_lon_lat_pre

file = open(box_lon_lat_file,'rb')
points_in_boxes_lon_lat= pickle.load(file)
file.close

num_rho = 0
for ii in range(len(points_in_boxes_lon_lat)):
    num_rho += np.shape(points_in_boxes_lon_lat[ii])[1]

print('Number of rho points: {}'.format(num_rho))
print('Number of seed locations (assuming 5 per profile, 0-20m depth): {}'.format(num_rho * 5))
print('Number of seed locations (assuming 4 per profile, 0-15m depth): {}'.format(num_rho * 4))
