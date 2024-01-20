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
save_file_name = 'dist_2_coast_field_rho_coastline_wc15_no_islands.mat'

grid_file = '/home/blaughli/opendrift_stuff/grid_stuff/wc15_grd_no_islands.nc';

coast_i_in = 'coast_coords_rho_wc15_continent_i.txt'
coast_j_in = 'coast_coords_rho_wc15_continent_j.txt'
% -----------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------


mask = ncread(grid_file,'mask_rho');
%mask = ncread(grid_file,'mask_psi');

% Need psi lon/lat to get lon/lat of coast coords, which were defined using psi points
%lon_mask = ncread(grid_file,'lon_psi');
%latp_mask = ncread(grid_file,'lat_psi');
lon_mask = ncread(grid_file,'lon_rho');
lat_mask = ncread(grid_file,'lat_rho');



% Dirty Matlab - need to add 1 to each element of these coast i/j vectors
fileID = fopen(coast_i_in,'r');
formatSpec = '%f';
coast_mask_i = fscanf(fileID,formatSpec);
fclose(fileID);
coast_mask_i = coast_mask_i + 1;

fileID = fopen(coast_j_in,'r');
formatSpec = '%f';
coast_mask_j = fscanf(fileID,formatSpec);
fclose(fileID);
coast_mask_j = coast_mask_j + 1;




lonc = []
latc = []


% I guess I am confused about i and j - feed them in reversed order
% and this seems to work...


% Use psi points, right? (since that what was used to define the coast..)
for ii = 1:max(size(coast_mask_i))
    lonc(ii) = lon_mask(coast_mask_j(ii),coast_mask_i(ii));
    latc(ii) = lat_mask(coast_mask_j(ii),coast_mask_i(ii));
end




% Again, we should use Psi points for our box boundaries, right???

dist_field = dist2coast_gcircle(lon_mask,lat_mask,mask,lonc,latc);


save(save_file_name,'dist_field')





