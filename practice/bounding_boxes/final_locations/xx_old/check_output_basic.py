

save_output_directory = base_path + 'practice/bounding_boxes/final_locations/z_output/'
save_output_file = save_output_directory + 'pdf_data_output.p'


file = open(save_output_file,'rb')
pdf_raw_loaded = pickle.load(file)
file.close


