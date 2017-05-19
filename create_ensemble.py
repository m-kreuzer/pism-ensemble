"""
Create the ensemble of PISM runs, using the function of
create_experiments.py.
"""


import pism_settings as ps; reload(ps)
import user_and_platform_settings as up_settings; reload(up_settings)
import pism_ant_equi.pism_ant_equi as pae; reload(pae)
import create_experiment as ce; reload(ce)

ensemble_members = pae.span_ensemble(ps.ensemble_variables,
                                     start_number=up_settings.initial_ensemble_number)

print ensemble_members
#ens_mem_num={}

for em_id in ensemble_members.index:

    ens_params = ensemble_members.ix[em_id].to_dict()

    em_id_num=""
    if up_settings.use_numbers_as_ens_id:
        em_id_num = em_id.split(" ")[1]
    else:
        em_id_num = em_id.split(" ")[0]

    ens_member_name = ps.ensemble_name+"_"+em_id_num

    print "\n"+ens_member_name
    for pname,pval in ens_params.items():
      if len(dict(ps.ensemble_variables)[pname])>1:
        print pname,pval

    ce.create_experiment(ensemble_member_name=ens_member_name,
                         ensemble_params=ens_params,
                         copy_pism_exec=True)

## Read the here written csv file somewhere else with
## df = pandas.read_csv(file_name,index_col=0,sep=" ")
ensemble_members.to_csv(up_settings.ensemble_paramater_map,sep=" ",
                        index_label="ens_member")

#with open(up_settings.ensemble_paramater_map, 'r') as infile,
#open(up_settings.ensemble_paramater_map+"test", 'w') as outfile:
#    data = infile.read()
#    data = data.replace('"', '')
#    outfile.write(data)

print "Wrote ensemble map file to", up_settings.ensemble_paramater_map