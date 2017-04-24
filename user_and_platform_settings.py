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

## could either be for smoothing and nomass, or for full physics run
## FIXME: currently unused
# runscript_template = "run_smoothing_nomass.template.sh"
runscript_template = "run_full_physics.template.sh"

cluster_runtime = "0-23:50:00"
number_of_cores = 16
username = pwd.getpwuid(os.getuid()).pw_name
project_root = os.path.dirname(os.path.abspath(__file__))

experiment_dir = os.path.join("/home/",username,"pism_experiments")
# base pism code directory
pismcode_dir = os.path.join("/home/",username,"pism")
# specific version as subfolder.
# create_ensemble will try to copy the pismcode_dir/pism_code_version/bin/pismr
pism_code_version = "pismpik"
working_dir = os.path.join("/p/tmp/",username,"pism_out")
input_data_dir = "/p/projects/tumble/mengel/pismInputData/20170316_PismInputData"
# PIK clusterwith slurm-specific compile, options for petsc
pism_mpi_do = "srun -n"
# else for PIK cluster
# pism_mpi_do = "mpiexec.hydra -bootstrap slurm -n"

# where to look for the executable in the output directory
pism_executable = "./bin/pismr"
