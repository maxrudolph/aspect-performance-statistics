ASPECT - Advanced Solver for Problems in Earth's ConvecTion
===========================================================


About
-----

This repository contains performance statistics for the ASPECT code
(https://www.github.com/geodynamics/aspect), generated
on varying high-performance computing systems and for different model setups.
It is intended to check a new ASPECT installation for correct scaling and
performance behavior and allows to track the performance of ASPECT during
ongoing development.



Structure
---------

The repository is structured as follows:
* /setups contains a number of parameter files that we use as official performance benchmark case. These models should contain a number of properties, namely:
  * short: The model should at most run a few timesteps, to save computational time reproducing the benchmark on possibly tens of thousands of cores
  * scalable: The benchmark should run on a different number of cores, depending on the resolution
  * well-defined: The number of iterations needed for the solver should stay roughly constant with changing mesh-size. If this is not possible, it should be noted in the setup description, and care must be taken when interpreting the model runtimes of the these setups
  * self-contained: Preferentially, no additional shared library should be needed to run the models with a development version of ASPECT.

* /results contains a number of performance results for the setups given in /setups. Each subfolder is named after one of the setups, and contains subfolders for each system that performed the setup. Each of the system subfolders follows the naming scheme "${Name of System}_${ASPECT_VERSION}". Each system subfolder contains a number of files that contain the screen output of one model run. These files follow the naming scheme "output_${Number of cores}_${Refinement level}_${Number of model run}"

* /visualization contains a number of visualization scripts for the results in /results.


More information
----------------

For more information see:
 - [ASPECT's official website](http://aspect.dealii.org)
 - [ASPECT's github repository](https://www.github.com/geodynamics/aspect)
 - [ASPECT's manual](http://www.math.clemson.edu/~heister/manual.pdf)

License
-------

ASPECT is published under GPL v2 or newer.
