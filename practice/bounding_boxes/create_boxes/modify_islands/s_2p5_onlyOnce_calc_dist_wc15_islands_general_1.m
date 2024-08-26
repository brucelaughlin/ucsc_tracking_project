% SYNTAX
% ------
% dist2cst=dist2coast_gcircle(lonr,latr,maskr,lonc,latc);
%
% where lonr,latr are the lon/lat points of the grid 
%       maskr is the mask of the grid (used to only find dist for ocean points
%       lonc,latc define the coastline (can and should probably have NaNs in it)
%  and  dist is what's returned (in meters);

% -----------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------
% --------------------------- EDIT THESE --------------------------------------------
% -----------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------

point_type_line = 'psi'
point_type_field = 'rho'

base_dir = '/home/blaughli/tracking_project/'
grid_dir = 'grid_data/'
file_dir = 'practice/bounding_boxes/create_boxes/aa_islands/z_output/'
grid_file = 'wc15n_grd_islands.nc'

grid_path = strcat(base_dir,grid_dir,grid_file)



% -----------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------


mask = ncread(grid_path,'mask_rho');

% Need psi lon/lat to get lon/lat of coast coords, which were defined using psi points
lon_mask = ncread(grid_path,'lon_rho');
lat_mask = ncread(grid_path,'lat_rho');

num_islands = 8

for island_dex = 1:num_islands

    save_file = strcat('dist_2_coast_field_',point_type_field,'_coastline_wc15n_island_number_',num2str(island_dex),'.mat')
    save_file_path = strcat(base_dir,file_dir,save_file)

    coast_lon_file = strcat('coast_coords_wc15n_lon_island_number_',num2str(island_dex),'.txt')
    coast_lat_file = strcat('coast_coords_wc15n_lat_island_number_',num2str(island_dex),'.txt')
    coast_lon_in = strcat(base_dir,file_dir,coast_lon_file)
    coast_lat_in = strcat(base_dir,file_dir,coast_lat_file)


    % Dirty Matlab - need to add 1 to each element of these coast i/j vectors
    fileID = fopen(coast_lon_in,'r');
    formatSpec = '%f';
    coast_lon = fscanf(fileID,formatSpec);
    fclose(fileID);

    fileID = fopen(coast_lat_in,'r');
    formatSpec = '%f';
    coast_lat = fscanf(fileID,formatSpec);
    fclose(fileID);

    dist_field = dist2coast_gcircle(lon_mask,lat_mask,mask,coast_lon,coast_lat);

    save(save_file_path,'dist_field')

end



