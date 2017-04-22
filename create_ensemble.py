"""
Create the ensemble of PISM runs, using the function of
create_experiments.py.
"""

import itertools
import shutil
import pism_settings as ps; reload(ps)
import create_experiment as ce; reload(ce)

parameter_combinations = list(itertools.product(*ps.ensemble_variables.values()))
parameter_names = ps.ensemble_variables.keys()

for pc in parameter_combinations[0:]:

    ens_member_id = "_".join([k+str(pc[i]) for i,k in
                              enumerate(parameter_names)])
    ens_member_name = ps.ensemble_name+"_"+ens_member_id
    # create dict with long names for parameters as keys
    # as used in create_experiment
    ensemble_params = {ps.ensemble_longnames[k]:pc[i] for i,k in
                       enumerate(parameter_names)}

    ce.create_experiment(ensemble_member_name=ens_member_name,
                         ensemble_params=ensemble_params,
                         copy_pism_exec=True)


