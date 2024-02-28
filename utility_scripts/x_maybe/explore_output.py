import pickle
import netCDF4
import matplotlib.pyplot as plt
import numpy as np

base_path = '/home/blaughli/tracking_project/'

box_base = base_path + 'practice/bounding_boxes/determine_points/z_output/'

box_file_lon_lat_pre = 'points_in_boxes_lon_lat_combined.p'
box_file_i_j_pre = 'points_in_boxes_i_j_combined.p'

box_lon_lat_file = box_base + box_file_lon_lat_pre
box_i_j_file = box_base + box_file_i_j_pre

file = open(box_lon_lat_file,'rb')
points_in_boxes_lon_lat= pickle.load(file)
file.close

file = open(box_i_j_file,'rb')
points_in_boxes_i_j= pickle.load(file)
file.close

sanity_box_number = 20

sanity_box_ll = points_in_boxes_lon_lat[sanity_box_number]
