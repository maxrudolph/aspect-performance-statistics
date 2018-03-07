# This python script generates submission scripts (slurm-style)
# For the aspect performance benchmarks

import numpy as np
import matplotlib.pyplot as plt
from subprocess import run

base_input = "convection-box-base.prm"     # The 'base' input file that gets modified

core_counts = [1,2,4,8,10,20,40,80,120,160,180,200,300,400]
refinement_levels = [2,3,4,5,6]
setups = [1,]

for core_count in core_counts:
    for resolution in refinement_levels:
        for setup in setups:
            output_file = "output_{:d}_{:d}_{:d}".format(core_count,resolution,setup)
            print(output_file)
