

import subprocess
import glob
import sys 
import os
import time
# Compress the output file

tracking_output_file = "/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/test_full1/z_output/tracking_output_calcDT_1440_saveDT_1440_buffer_100_nSeed_20_startNudge_000.nc"

bash_command = "ls -lh {}".format(tracking_output_file)
process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
size_raw = process.stdout.read()


bash_command = "nc_compress {}".format(tracking_output_file)
process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

time.sleep(20)

bash_command = "ls -lh {}".format(tracking_output_file)
process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
size_compressed = process.stdout.read()

print('\noutput file size (raw): {}\n'.format(size_raw))
print(' \noutput file size (compressed): {}\n'.format(size_compressed))







