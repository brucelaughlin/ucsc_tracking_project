

sstat --format=jobid,maxrss,averss,MaxVMsize 800928.batch




sstat -p --format=jobid,maxrss,averss,MaxVMsize 800928.batch



scontrol -o show nodes | awk '{ print $1, $13, $14}'


sinfo -N -l


# Cancel all jobs:
# replace "801" with the starting numbers of your jobs
squeue -u blaughli | grep 801 | awk '{print $1}' | xargs -n 1 scancel


