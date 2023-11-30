#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import netCDF4
import numpy as np
import matplotlib.pyplot as plt
#from scipy.stats import norm
import matplotlib.ticker as mticker

# text formatting magic for plot legend
f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
fmt = mticker.FuncFormatter(g)



base_path = '/home/blaughli/tracking_project/'

tracking_output_directory = 'practice/turbulence_study/'






path_pre = base_path + tracking_output_directory


file_names = []
file_names.append('profile_turb_study_wc12_his_v0_Ks_uniform_1e-1_psi_uniform.nc')
file_names.append('profile_turb_study_wc12_his_v0_Ks_uniform_1e-2_psi_uniform.nc')
file_names.append('profile_turb_study_wc12_his_v0_Ks_uniform_1e-3_psi_uniform.nc')
file_names.append('profile_turb_study_wc12_his_v0_Ks_uniform_1e-4_psi_uniform.nc')
#file_names.append('profile_turb_study_wc12_his_v0_Ks_linear_1e-2_1e-1_psi_uniform.nc')

Ks_values = []
Ks_values.append(1e-1)
Ks_values.append(1e-2)
Ks_values.append(1e-3)
Ks_values.append(1e-4)

# initialize in loop
time_domain = []
z_bottom = 0

#for ii in range(4):
for ii in range(len(file_names)):

    file_path = path_pre + file_names[ii]    

    dset = netCDF4.Dataset(file_path, 'r')
    z = dset.variables['z'][:]
        
    if ii == 0:
        time_domain = list(dset.variables['age_seconds'][:][0,:])
        z_bottom = round(np.absolute(z[0,0]))
    
    dset.close()
    
    z_std = []
    for jj in range(np.shape(z)[1]):
        z_std.append(np.std(z[:,jj]-z[:,1]))
        

    plt.plot(z_std,label = ("$Ks = 10^{{{}}}$").format(int(np.log10(Ks_values[ii]))))



    

    std_theory = [np.sqrt(Ks_values[ii] * 2 * t) for t in time_domain]
    plt.plot(std_theory,plt.gca().lines[-1].get_color(),linestyle='dashed')    
    



plt.legend()

plot_title = r'$\sigma$(depths) vs time'
#plot_txt="I need the caption to be present a little below X-axis"


plt.title(plot_title)
plt.ylabel(r'$\sigma$(depths(t)-depths(t=0)) (m)')
plt.xlabel('t = time since seeding (hours)')

#plt.text(0.5, -0.05, r'bottom depth$= $'+str(z_bottom), ha='center')

#plt.figtext(.45, .85, r"bottom depth$= $"+str(z_bottom),fontsize = 7)
plt.figtext(.45, .87, fr'bottom depth$= {str(z_bottom)}$m',fontsize = 7)
plt.figtext(.4, .77, r"$\sigma_{theory} = \sqrt{2Kt}$",fontsize = 12)


#plt.text(.5, .05, txt, ha='center')
#plt.figtext(0.5, 0.01, plot_txt, wrap=True, horizontalalignment='center', va='top', fontsize=12)
#plt.show()





