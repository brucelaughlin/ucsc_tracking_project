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

land_type = 'continent/'
%land_type = 'islands/'

base_dir = '/home/blaughli/tracking_project/'
grid_dir = 'grid_data/'
file_dir = strcat('practice/bounding_boxes/create_boxes/',land_type,'z_output/')
%grid_file = 'wc15_grd_no_islands.nc'
grid_file = 'wc15n_grd_continent.nc'

grid_path = strcat(base_dir,grid_dir,grid_file)


save_file = strcat('dist_2_coast_field_',point_type_field,'_coastline_wc15n_continent.mat')

%coast_i_file = strcat('coast_coords_',point_type_line,'_wc15_continent_i.txt')
%coast_j_file = strcat('coast_coords_',point_type_line,'_wc15_continent_j.txt')
coast_lon_file = strcat('coast_coords_',point_type_line,'_wc15n_continent_lon.txt')
coast_lat_file = strcat('coast_coords_',point_type_line,'_wc15n_continent_lat.txt')

%coast_i_in = strcat(base_dir,file_dir,coast_i_file)
%coast_j_in = strcat(base_dir,file_dir,coast_j_file)
coast_lon_in = strcat(base_dir,file_dir,coast_lon_file)
coast_lat_in = strcat(base_dir,file_dir,coast_lat_file)

save_file_path = strcat(base_dir,file_dir,save_file)

% -----------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------


mask = ncread(grid_path,'mask_rho');
%mask = ncread(grid_path,'mask_psi');

% Need psi lon/lat to get lon/lat of coast coords, which were defined using psi points
%lon_mask = ncread(grid_path,'lon_psi');
%latp_mask = ncread(grid_path,'lat_psi');
lon_mask = ncread(grid_path,'lon_rho');
lat_mask = ncread(grid_path,'lat_rho');



% Dirty Matlab - need to add 1 to each element of these coast i/j vectors
%fileID = fopen(coast_i_in,'r');
fileID = fopen(coast_lon_in,'r');
formatSpec = '%f';
%coast_mask_i = fscanf(fileID,formatSpec);
coast_lon = fscanf(fileID,formatSpec);
fclose(fileID);
%coast_mask_i = coast_mask_i + 1;

%fileID = fopen(coast_j_in,'r');
fileID = fopen(coast_lat_in,'r');
formatSpec = '%f';
%coast_mask_j = fscanf(fileID,formatSpec);
coast_lat = fscanf(fileID,formatSpec);
fclose(fileID);
%coast_mask_j = coast_mask_j + 1;




%lonc = []
%latc = []


% I guess I am confused about i and j - feed them in reversed order
% and this seems to work...


% Use psi points, right? (since that what was used to define the coast..)
%for ii = 1:max(size(coast_mask_i))
%    lonc(ii) = lon_mask(coast_mask_j(ii),coast_mask_i(ii));
%    latc(ii) = lat_mask(coast_mask_j(ii),coast_mask_i(ii));
%end




% Again, we should use Psi points for our box boundaries, right???

%dist_field = dist2coast_gcircle(lon_mask,lat_mask,mask,lonc,latc);
dist_field = dist2coast_gcircle(lon_mask,lat_mask,mask,coast_lon,coast_lat);


save(save_file_path,'dist_field')





