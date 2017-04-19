"""
Submit the ensemble of PISM runs, as created with
create_ensemble.py, to the batch system of cluster PIK or SUPERMUC.
"""

import os
import itertools
import subprocess
import pism_settings as ps; reload(ps)
import user_and_platform_settings as up_settings; reload(up_settings)


parameter_combinations = list(itertools.product(*ps.ensemble_variables.values()))
parameter_names = ps.ensemble_variables.keys()

for pc in parameter_combinations[0:4]:

    ens_member_id = "_".join([k+str(pc[i]) for i,k in
                              enumerate(parameter_names)])
    ens_member_name = ps.ensemble_name+"_"+ens_member_id
    ens_member_path = os.path.join(up_settings.experiment_dir,ens_member_name)
    subprocess.check_call("cd "+ens_member_path+" && sbatch submit.sh",
                          shell=True)


