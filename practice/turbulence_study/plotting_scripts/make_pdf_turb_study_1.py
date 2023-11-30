#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

base_path = '/home/blaughli/tracking_project/'

tracking_output_directory = 'practice/turbulence_study/'

#tracking_output_file = 'profile_turb_study_1.nc'
#racking_output_file = 'profile_turb_study_psi_line_slope1.nc'
#tracking_output_file = 'profile_turb_study_AKs_1e-1_psi_line_slope1_swimON.nc'
#tracking_output_file = 'profile_turb_study_AKs_1e-1_psi_line_slope1.nc'
#tracking_output_file = 'profile_turb_study_AKs_1e-2_psi_line_slope1.nc'
#tracking_output_file = 'profile_turb_study_wc12_his_v0_Ks_0_psi_uniform.nc'
#tracking_output_file = 'profile_turb_study_wc12_his_v0_Ks_uniform_1e-4_psi_uniform.nc'
#tracking_output_file = 'profile_turb_study_wc12_his_v0_Ks_uniform_1e-1_psi_uniform.nc'
#tracking_output_file = 'profile_turb_study_wc12_his_v0_Ks_linear_1e-2_1e-1_psi_uniform.nc'
#tracking_output_file = 'profile_turb_study_wc12_his_v0_Ks_linear_1e-4_1e-1_psi_uniform.nc'
#tracking_output_file = 'profile_turb_study_wc12_his_v0_Ks_tanh_1e-3_1_psi_uniform.nc'
#tracking_output_file = 'profile_turb_study_wc12_his_v0_Ks_Kt_Kv_0.nc_psi_uniform.nc'
tracking_output_file = 'profile_turb_study_wc12_his_v0_Ks_Kt_Kv_0.nc_psi_uniform_MIX_OFF.nc'

plot_title = '_'.join(tracking_output_file.split('_')[3:]).removesuffix('.nc')
plot_txt="I need the caption to be present a little below X-axis"

tracking_data_path = base_path + tracking_output_directory + tracking_output_file

dset = netCDF4.Dataset(tracking_data_path, 'r')

# only looking at the "z" variable here

z = dset.variables['z'][:]

z_start = z[:,1]
z_end = z[:,-1]

num_bins = 50

#plt.hist(z_start,bins=num_bins,density=True)
#plt.hist(z_end,bins=num_bins,density=True)
#plt.plot(z_start,z_end)

z_diff = z_start-z_end

z_diff_mean = np.mean(z_diff)
z_diff_std = np.std(z_diff)

x_axis = np.linspace(min(z_diff), max(z_diff), endpoint = True)
#x_axis = np.linspace(min(z_start), max(z_start), endpoint = True)

hist_0_title = plot_title + ' t=0'
hist_T_title = plot_title + ' t=T'


plt.hist(z_start,bins=num_bins,density=True)
plt.title(hist_0_title)
plt.show()
plt.hist(z_end,bins=num_bins,density=True)
plt.title(hist_T_title)
plt.show()

plt.hist(z_diff,bins=num_bins,density=True)
plt.plot(x_axis,norm.pdf(x_axis,z_diff_mean,z_diff_std),color='red')

#fig = plt.figure()
plt.title(plot_title)
plt.xlabel('x = z(t=0)-z(t=T)')
plt.ylabel('p(x)')
#plt.text(.5, .05, txt, ha='center')
#plt.figtext(0.5, 0.01, plot_txt, wrap=True, horizontalalignment='center', va='top', fontsize=12)
plt.show()





