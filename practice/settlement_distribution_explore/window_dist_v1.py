# v1: Trying to get a (truncated normal) distribution of settlement window opening times to assign to the larvae
# at the beginning of their lives

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

n_larvae = 11844 # (taken from log files - this is how many are seeded at a single time, for all runs)

lower, upper = 90, 150

mu, sigma = 120, 10  # Taken from the report provided by Will (all assumed from the given PLD range of 90-150 days, without other info)

#lower, upper, mu, sigma = np.asarray([lower, upper, mu, sigma], dtype=np.float32)
#s = np.random.normal(mu, sigma, n_larvae)
#count, bins, ignored = plt.hist(s, 30, density=True)

X = stats.truncnorm(
        (lower-mu)/sigma, (upper-mu)/sigma, loc=mu, scale=sigma)

fig, ax = plt.subplots()

ax.hist(X.rvs(n_larvae), density=True)

x = np.linspace(X.ppf(0), X.ppf(1), 100)
#x = np.linspace(X.ppf(0.01), X.ppf(0.99), 100)

ax.plot(x, X.pdf(x),
               'r-', lw=5, alpha=0.6, label='truncnorm pdf')

plt.show()

