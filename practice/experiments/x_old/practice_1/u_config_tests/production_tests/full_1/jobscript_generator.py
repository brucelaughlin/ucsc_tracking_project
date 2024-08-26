# Following Chris' advice, going to generate "job scripts" for each job, where a job is a single
# batch of jobs sent to slurm.  Once one is done, start the next, manually at first, until
# we have finished the experiment

# I'm still finishing up my parallel job tests, but for now it is clear that running 6 jobs of 20 seeds
# each is faster (by %40) than running 3 jobs of 40 seeds each on a cluster.  It may turn out that 12 jobs
# of 10 seeds each is ideal, etc.  Just adjust as needed, noting that we have 20 cores per cluster node.


import numpy as np
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
import sys
import os



# "n_seed" 
n_seed = 20

# Again, this is determined by the parallelization tests
n_cores_per_node = 6

# I believe this parameter is the total number of nodes on the cluster I'm allowing the experiment to use
n_nodes = 6

# We're planning to seed every other day, as previous tests by Chris and Patrick showed this to provide
# sufficient de-correlation.  Perhaps later we should do updated de-correlation time scale tests.
n_days_per_job =  n_seed * 2

# Chris wrote "n_cores_per_node = 10"... but it's 20, right?  Do I need to not use them all?

n_jobs = n_cores_per_node * n_nodes



# Actually, it seems as though Chris may have forgotten that a key constraint is memory... My parallelization tests
# sought to maximize memory usage, ie run as many jobs as possible on a node without overflowing.  So, since none
# of my permutations used more than 20 cores, I don't see why we need to do any calculations of "jobs per node" based
# on the number of cores available.


for jj = 1:

