# v1: Trying to get a (truncated normal) distribution of settlement window opening times to assign to the larvae
# at the beginning of their lives

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

n_larvae = 11844 # (taken from log files - this is how many are seeded at a single time, for all runs)

first_settlement_day = 31
run_length_days = 91

lower = 0
upper = run_length_days - first_settlement_day
number_standard_deviations = 3

mu = upper/2

sigma = (upper - mu)/number_standard_deviations


X = stats.truncnorm(
        (lower-mu)/sigma, (upper-mu)/sigma, loc=mu, scale=sigma)

windows_pre1 = X.rvs(n_larvae)
windows_pre2 = np.round(windows_pre1).astype(np.int32)
windows = windows_pre2.tolist()


