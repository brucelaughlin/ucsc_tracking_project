

tfile = '/data/blaughli/tracking_output/baseYear_1990/WC15N_GFDLTV_nRunsPerNode_15_nSeed_020_physicsOnly/tracking_output_calcDT_060_saveDT_1440_buffer_100_nSeed_020_startNudge_000000.nc'



dset = netCDF4.Dataset(tfile, 'r')
lons = dset.variables['lon'][:]
