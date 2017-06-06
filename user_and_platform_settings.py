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
create_full_physics_script = True
optimize_tillphi = False #works only with PISM code version
#https://github.com/talbrecht/pism_pik/tree/pik_newdev_paleo_07
create_paleo_script = False

## use hashes or numbers as ensemble member identifiers
use_numbers_as_ens_id = True
if use_numbers_as_ens_id:
  initial_ensemble_number = 1200

## find here the mapping between ensemble member ids and the varied parameters.
ensemble_paramater_map = "ensemble_map.txt"
if use_numbers_as_ens_id:
  ensemble_paramater_map = "ensemble_map_"+str(initial_ensemble_number)+".txt"

cluster_runtime = "6-23:50:00"
number_of_cores = 32
account = "ice"
submit_class = "medium"
username = pwd.getpwuid(os.getuid()).pw_name
project_root = os.path.dirname(os.path.abspath(__file__))

##########################################################################

if username == "mengel": # matthias
  experiment_dir = os.path.join("/home/",username,"pism_experiments")
  pismcode_dir = os.path.join("/home/",username,"pism")
  pism_code_version = "pismpik"
  working_dir = os.path.join("/p/tmp/",username,"pism_out")
  input_data_dir = "/p/projects/tumble/mengel/pismInputData/20170316_PismInputData"

elif username == "albrecht": # torsten
  experiment_dir = os.path.join("/home/",username,"pism17/pism_experiments")
  # base pism code directory
  pismcode_dir = os.path.join("/home/",username,"pism17")
  # specific version as subfolder.

  # create_ensemble will try to copy the pismcode_dir/pism_code_version/bin/pismr
  pism_code_version = "pism0.7_pik"
  working_dir = os.path.join("/p/tmp/",username,"pism17/pismOut/pism_paleo")
  input_data_dir = "/p/tmp/albrecht/pism17/pismInput"
else:
  print "add your user-specific paths in user_and_platform_settings.py"
  raise NotImplementedError
############################################################################

# PIK cluster with slurm-specific compile, options for petsc
pism_mpi_do = "srun -n"
# else for PIK cluster
# pism_mpi_do = "mpiexec.hydra -bootstrap slurm -n"

# where to look for the executable in the output directory
pism_executable = "./bin/pismr"
