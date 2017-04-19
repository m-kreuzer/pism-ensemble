"""
Create the ensemble of PISM runs, using the function of
create_experiments.py.
"""

import itertools
import shutil
import pism_settings as ps; reload(ps)
import create_experiment as ce; reload(ce)

parameter_combinations = list(itertools.product(*ps.ensemble_variables.values()))

for pc in parameter_combinations:
    ens_member_id = "_".join([k+"_"+str(pc[i]) for i,k in
                                enumerate(ps.ensemble_variables.keys())])
    ens_member_name = ps.ensemble_name+"_"+ens_member_id

    ce.create_experiment(ensemble_member_name=ens_member_name, copy_pism_exec=True)


