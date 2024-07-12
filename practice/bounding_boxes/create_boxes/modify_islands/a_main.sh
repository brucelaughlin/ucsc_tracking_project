#! /bin/bash

# Run all the scripts to make the boxes

python s1_coastline_define_walk_psi_bl_lonlat_islands_individual_1.py

python s2_save_coastline_txt_lonlat_island_individual.py

python s3_make_10km_contour_lonlat_islands_individual_combine_1.py

python s4_modify_10km_contour_remove_intersection.py

python s5_artificial_coastline_blob_islands_V3.py







