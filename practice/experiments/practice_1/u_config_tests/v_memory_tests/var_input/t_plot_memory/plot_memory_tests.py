import glob, os
import re
import matplotlib.pyplot as plt


#output_dir_600 = '/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/var_input/z_output'
output_dir_600 = '/home/blaughli/tracking_project/practice/experiments/practice_1/u_config_tests/v_memory_tests/var_input/t_plot_memory/v_mem_files_to_plot'

os.chdir(output_dir_600)

postfix_list = ['K','M','G']

mem_list = []
run_name_list = []

for filename in glob.glob("run_memory_info_*.txt"):
    
    try:
        found = re.search('run_memory_info_(.+?)\.txt', filename).group(1)
    except AttributeError:
        found = "missing_run_metadata"

    run_name_list.append(found)
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        good_lines = []
        for line in lines:
            if len(line) > 0:
                postfix = line[-1]
                if postfix in postfix_list:
                    value = float(line[:-1])
                    if postfix == 'K':
                        good_lines.append(value/1000000)
                    elif postfix == 'M':
                        good_lines.append(value/1000)
                    else:
                        good_lines.append(value)
        mem_list.append(good_lines)

# from G4G
#def sort_lists(list1, list2):
#    zipped_pairs = zip(list2, list1)
#    z = [x for _, x in sorted(zipped_pairs)]
#    return z
#
#print(sort_lists(run_name_list,mem_list))

fig,ax = plt.subplots()

for ii in range(len(mem_list)):
    ax.plot(mem_list[ii],label = run_name_list[ii])
    
ax.legend()
ax.set_xlabel("Time (x 10 seconds)")
ax.set_ylabel("Memory usage (GB)")

#plt.title('Memory (GB) vs time, for 20 runs, from 1 float to 1200 in increments of 600')
plt.title('Memory (GB) vs time, from 1 float to 10,000 by factors of 10')


plt.show()

