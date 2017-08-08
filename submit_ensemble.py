"""
Submit the ensemble of PISM runs, as created with
create_ensemble.py, to the batch system of cluster PIK or SUPERMUC.
"""

import os
import itertools
import subprocess
import settings; reload(settings)

ensemble_map_file = settings.ensemble_name+"_"+settings.ensemble_paramater_map+".txt"
f = open(ensemble_map_file, 'r')

f.readline() #skip first title line
for i,line in enumerate(f):
    # if i > 20:
        # print line
    if settings.use_numbers_as_ens_id:
      ens_member_id = line.split(" ")[1].rstrip('"') #use numbers
    else:
      ens_member_id = line.split(" ")[0].lstrip('"') #use hashes

    #ens_member_id = "_".join([k+str(pc[i]) for i,k in
    #                          enumerate(parameter_names)])
    ens_member_name = settings.ensemble_name+"_"+ens_member_id
    ens_member_path = os.path.join(settings.experiment_dir,ens_member_name)
    print ens_member_path

    subprocess.check_call("cd "+ens_member_path+" && "+settings.submit_command,
                          shell=True)


