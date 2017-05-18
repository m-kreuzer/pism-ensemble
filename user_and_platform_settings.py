"""
Platform and user specific settings
These mostly go to the set_environment.sh that is sourced from
the PISM run script.
This should only be commited for major changes affecting all users.
"""

import os
import pwd

## create run scripts if True.
create_smoothing_script = True
create_full_physics_script = False
create_paleo_script = True

## use hashes or numbers as ensemble member identifiers
use_numbers_as_ens_id = True
if use_numbers_as_ens_id:
  initial_ensemble_number = 1000


## find here the mapping between ensemble member ids and the varied parameters.
ensemble_paramater_map = "ensemble_map.txt"

cluster_runtime = "0-23:50:00"
number_of_cores = 32
account = "ice"
submit_class = "short"
username = pwd.getpwuid(os.getuid()).pw_name
project_root = os.path.dirname(os.path.abspath(__file__))

experiment_dir = os.path.join("/home/",username,"pism17/pism_experiments")
# base pism code directory
pismcode_dir = os.path.join("/home/",username,"pism17")
# specific version as subfolder.

# create_ensemble will try to copy the pismcode_dir/pism_code_version/bin/pismr
pism_code_version = "pism0.7_pik"
working_dir = os.path.join("/p/tmp/",username,"pism17/pismOut/pism_paleo")
#input_data_dir = "/p/tmp/albrecht/pism17/pismInput"
input_data_dir = "/p/projects/tumble/mengel/pismInputData/20170316_PismInputData"

# PIK cluster with slurm-specific compile, options for petsc
pism_mpi_do = "srun -n"
# else for PIK cluster
# pism_mpi_do = "mpiexec.hydra -bootstrap slurm -n"

# where to look for the executable in the output directory
pism_executable = "./bin/pismr"
