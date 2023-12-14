
grid_file = 'wc12_grd.nc.0';
grd = roms_get_grid(grid_file);
fname = 'wc12_his_single_tstep.nc';

%igrid = 1

% Getting 42 levels, but AKs has 43 levels... so, perhaps the diffusion coefficents are
% at w-points (and not rho-points)???  try it (set igrid=5)

igrid = 5;
idims = 1;
tindex = 1;
depths_w = depths(fname, grid_file, igrid, idims, tindex); 
save('depths_w.mat','depths_w');   


