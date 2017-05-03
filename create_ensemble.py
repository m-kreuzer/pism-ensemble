"""
Create the ensemble of PISM runs, using the function of
create_experiments.py.
"""


import pism_settings as ps; reload(ps)
import user_and_platform_settings as up_settings; reload(up_settings)
import pism_ant_equi.pism_ant_equi as pae; reload(pae)
import create_experiment as ce; reload(ce)

ensemble_members = pae.span_ensemble(ps.ensemble_variables,
                                     use_numbers=up_settings.use_numbers_as_ens_id)


for em_id in ensemble_members.index[0:2]:

    ens_params = ensemble_members.ix[em_id].to_dict()
    ens_member_name = ps.ensemble_name+"_"+em_id

    ce.create_experiment(ensemble_member_name=ens_member_name,
                         ensemble_params=ens_params,
                         copy_pism_exec=False)

ensemble_members.to_csv(up_settings.ensemble_paramater_map,sep=" ")