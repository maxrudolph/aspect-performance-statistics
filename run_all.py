# This python script generates submission scripts (slurm-style)
# For the aspect performance benchmarks

import numpy as np
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt

from subprocess import run
import os

base_input = "setups/spherical_shell_expensive_solver.prm"     # The 'base' input file that gets modified
#cluster_label = "PI4CS_aspect-2.0-pre-40tasks"
cluster_label = "peloton-ii-32tasks-ubuntu22"

# modify this to contain the commands necessary to setup MPI environment
environment_setup_commands = ""

core_counts = [1,2,4,8,16,32,64,128,192,256,320,448,512,768]#,200,300,400]#,500,800,1000,1500]
refinement_levels = [2,3,4,5]#,6]
#                                          0   1   2   3       4     5    6
minimum_core_count_for_refinement_level = [0,  0,   1,   1,   10, 100, 500]# for refinement levels 0-6
maximum_core_count_for_refinement_level = [0,  0,1000,1000, 1000,2000,2000]

setups = [1,]
tasks_per_node = 32
# make directories for temporary files
os.system('mkdir tmp')
os.system('mkdir tmp/'+cluster_label)

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

def generate_slurm_file(slurm_file_name,ncpu,tasks_per_node,job_name,prmfile):
    """Write the slurm file"""
    fh = open(slurm_file_name,'w')
    fh.write("#!/bin/bash\n")
    fh.write("#SBATCH -p high2\n")
    fh.write("#SBATCH --account rudolphgrp\n")
    fh.write("#SBATCH -n {:d}\n".format(ncpu))
    fh.write("#SBATCH --exclusive\n")
    #fh.write("#SBATCH --ntasks-per-node={:d}\n".format(tasks_per_node))
    fh.write("#SBATCH -c 2\n")
    fh.write("#SBATCH --time=01:00:00\n")
    fh.write("#SBATCH --job-name={:s}\n".format(job_name))
    fh.write("#SBATCH --switches=1\n")
    fh.write("set -x\n")
    fh.write(environment_setup_commands + "\n")
    fh.write("module list\n")
    fh.write("srun ./aspect {:s}\n".format(prmfile))
    fh.close()
    
for core_count in core_counts:
    for resolution in refinement_levels:
        if( core_count >= minimum_core_count_for_refinement_level[resolution]
            and
            core_count <= maximum_core_count_for_refinement_level[resolution]):
            for setup in setups:
                jobname = "run_{:d}_{:d}_{:d}".format(core_count,resolution,setup)
                output_file = "tmp/{:s}/output_{:d}_{:d}_{:d}".format(cluster_label,core_count,resolution,setup)
                input_file = "tmp/{:s}/input_{:d}_{:d}_{:d}".format(cluster_label,core_count,resolution,setup)
                print(output_file)
                parameters = dict([])
                parameters['OUTPUT_DIRECTORY'] = output_file
                parameters['RESOLUTION'] = resolution
                
                # do string replacement on the base input file
                generate_input_file(base_input,input_file,parameters)
                
                
                #aspect_command = "srun ./aspect {:s}".format(input_file)
                #print(aspect_command)
                slurm_file = input_file + ".slurm"
                generate_slurm_file(slurm_file,core_count,tasks_per_node,jobname,input_file)
                os.system("sbatch " + slurm_file)
                #batch_command = "salloc -p high2 -n {:d} --exclusive --ntasks-per-node={:d} --time=30:00 --job-name={:s} --switches=1  ".format(core_count,tasks_per_node,jobname) + aspect_command 
                #print(batch_command)
                #os.system(batch_command)

