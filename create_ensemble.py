"""
Create the ensemble of PISM runs, using the function of
create_experiments.py.
"""

import os
import pism_ensemble.pism_ensemble as pae; reload(pae)
import create_experiment as ce; reload(ce)

project_root = os.path.dirname(os.path.realpath(__file__))
settings = pae.settings_handler(project_root)

ensemble_members = pae.span_ensemble(settings.ensemble_variables,
                                     start_number=settings.initial_ensemble_number)

print ensemble_members

for em_id in ensemble_members.index:

    ens_params = ensemble_members.ix[em_id].to_dict()

    em_id_num=""
    if settings.use_numbers_as_ens_id:
        em_id_num = em_id.split(" ")[1]
    else:
        em_id_num = em_id.split(" ")[0]

    ens_member_name = settings.ensemble_name+"_"+em_id_num

    print "\n"+ens_member_name
    for pname,pval in ens_params.items():
      if len(dict(settings.ensemble_variables)[pname])>1:
        print pname,pval

    ce.create_experiment(settings, ens_member_name, ens_params,
                         copy_pism_exec=True)

## Read the here written csv file somewhere else with
## df = pandas.read_csv(file_name,index_col=0,sep=" ")
ensemble_members.to_csv(settings.ensemble_map_file,sep=" ", index_label="ens_member")
print "Wrote ensemble map file to", settings.ensemble_map_file