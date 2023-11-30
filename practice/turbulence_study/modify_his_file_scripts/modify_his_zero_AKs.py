#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# zero-out the AKs values 


import netCDF4

base_path = '/home/blaughli/tracking_project/history_files/'

file_to_change = base_path + 'wc12_his_v0_Ks_0_base.nc'

dset = netCDF4.Dataset(file_to_change, 'r+')
dset['AKs'][:] = 0
dset.close()

