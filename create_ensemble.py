"""
Create the ensemble of PISM runs, using the function of
create_experiments.py.
"""

import itertools
import shutil
import pism_settings as ps; reload(ps)
import pism_ant_equi.pism_ant_equi as pae; reload(pae)
import create_experiment as ce; reload(ce)

parameter_names,ensemble_members = pae.span_ensemble(ps.ensemble_variables)

for em_id in ensemble_members.keys()[0:2]:

    ens_params = ensemble_members[em_id]
    ens_member_name = ps.ensemble_name+"_"+em_id

    ce.create_experiment(ensemble_member_name=ens_member_name,
                         ensemble_params=ens_params,
                         copy_pism_exec=False)

