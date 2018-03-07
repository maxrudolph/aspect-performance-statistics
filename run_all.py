# This python script generates submission scripts (slurm-style)
# For the aspect performance benchmarks

import numpy as np
import matplotlib.pyplot as plt
from subprocess import run
import os

base_input = "setups/spherical_shell_expensive_solver.prm"     # The 'base' input file that gets modified

# modify this to contain the commands necessary to setup MPI environment
environment_setup_commands = "module purge; module load impi local-gcc-6.3.0"

cluster_description = "PI4CS_COEUS_aspect_2.0-pre"
core_counts = [1,2,4,8]#,10,20,40,80,120,160,180,200,300,400,500,800,1000]
refinement_levels = [2,3]#4,5,6]
#                                          0   1   2   3    4    5     6
minimum_core_count_for_refinement_level = [0,  0,  1, 10,  10, 500,  500]# for refinement levels 0-6
maximum_core_count_for_refinement_level = [0,  0,150,400,1000, 1500,1500]

setups = [1,]
tasks_per_node = 20

def generate_input_file(base_file_name,output_file_name,dictionary):
    """Read the 'base' input file from base_file_name, replace strings 
    using dictionary, and write new output file to output_file_name"""
    fh = open(base_file_name,'r')
    run(['rm','-f',output_file_name])
    ofh = open(output_file_name,'w')
    for line in fh:        
        for key in dictionary:
            if key in line:                
                line = line.replace(key,str(dictionary[key]))
        ofh.write(line)
    fh.close()
    ofh.close()

for core_count in core_counts:
    for resolution in refinement_levels:
        if( core_count >= minimum_core_count_for_refinement_level[resolution]
            and
            core_count <= maximum_core_count_for_refinement_level[resolution]):
            for setup in setups:
                output_file = "tmp/{:s}/output_{:d}_{:d}_{:d}".format(cluster_description,core_count,resolution,setup)
                input_file = "tmp/input_{:d}_{:d}_{:d}".format(core_count,resolution,setup)
                print(output_file)
                parameters = dict([])
                parameters['OUTPUT_DIRECTORY'] = output_file
                parameters['RESOLUTION'] = resolution
                
                # do string replacement on the base input file
                generate_input_file(base_input,input_file,parameters)

                aspect_command = "mpirun -n {:d} ./aspect {:s}".format(core_count,input_file)
                print(aspect_command)

                batch_command = "sbatch -p allcpu -n {:d} --exclusive --ntasks-per-node={:d} ".format(core_count,tasks_per_node) + aspect_command
                print(batch_command)
                #os.system(batch_command)

