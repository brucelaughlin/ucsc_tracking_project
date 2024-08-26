# Connectivity (release box number vs settlement box number)
pdf_list_connectivity = []
for ii in range(5):
    pdf_list_connectivity.append(np.zeros((n_boxes,n_boxes)))

# Time after PLD until settlement (saving only release location) (release box number vs settlement time)
pdf_list_settleTime_source = []
for ii in range(5):
    pdf_list_settleTime_source.append(np.zeros((n_boxes,timesteps_settlement_window)))

# Time after PLD until settlement (saving only settlement location) (release box number vs settlement time)
pdf_list_settleTime_dest = []
for ii in range(5):
    pdf_list_settleTime_dest.append(np.zeros((n_boxes,timesteps_settlement_window)))

# Number of days eposed to oxygen levels below 2.2 (saving only settlement location) (release box number vs exposure time)
pdf_list_exposureTime_oxygen_source = []
for ii in range(5):
    pdf_list_exposureTime_oxygen_source.append(np.zeros((n_boxes,timesteps_settlement_window)))

# Histogram of average Terature experienced - just estimating range, since I don't know it without processing
T_min = 0
T_max = 30
T_step = 0.1
n_T_steps = len(list(range(T_min,T_max+1,T_step)))
pdf_list_T_source = []
pdf_list_T_dest = []
for ii in range(5):
    pdf_list_T_source.append(np.zeros((n_boxes,n_T_steps)))
    pdf_list_T_dest.append(np.zeros((n_boxes,n_T_steps)))





drift_oxygen = np.zeros((num_particles,timesteps_settlement_window))
drift_T = np.zeros((num_particles,timesteps_settlement_window))

    
particle_list_exposure_oxygen = np.zeros(num_particles)
particle_list_sumT = np.zeros(num_particles)
particle_list_driftTime = np.zeros(num_particles)



