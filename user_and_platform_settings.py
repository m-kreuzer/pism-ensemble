"""
Platform and user specific settings
These mostly go to the set_environment.sh that is sourced from
the PISM run script.
This should only be commited for major changes affecting all users.
"""

import os
import pwd

## create run scripts if True.
create_smoothing_script = False
create_full_physics_script = True

## could either be for smoothing and nomass, or for full physics run
# runscript_template = "run_smoothing_nomass.template.sh"
runscript_template = "run_full_physics.template.sh"

username = pwd.getpwuid(os.getuid()).pw_name
project_root = os.path.dirname(os.path.abspath(__file__))

experiment_dir = os.path.join("/home/",username,"pism_experiments")
pismcode_dir = os.path.join("/home/",username,"pism")
working_dir = "/p/tmp/mengel/pism_out"
input_data_dir = "/p/projects/tumble/mengel/pismInputData/20170316_PismInputData"
pism_mpi_do = "mpiexec.hydra -bootstrap slurm -n"
pism_executable = "./bin/pismr"
