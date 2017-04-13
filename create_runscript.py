

import os
import pism_settings as ps; reload(ps)
import user_and_platform_settings as up_settings; reload(up_settings)
import pism_ant_equi.pism_ant_equi as pae; reload(pae)

runscript_path = os.path.join(up_settings.experiment_dir,ps.ensemble_name)

if not os.path.exists(runscript_path):
    os.makedirs(runscript_path)
    os.makedirs(os.path.join(runscript_path,"log"))

pae.write_pism_runscript(up_settings, "run_smoothing.template.sh", runscript_path,
                         input_file = ps.input_file,
                         ocean_file = ps.ocean_file,
                         extra_variables = ps.extra_variables,
                         timeseries_variables = ps.timeseries_variables,
                         )

pae.write_pism_runscript(up_settings, "set_environment.template.sh", runscript_path,
                         pismcode_dir=up_settings.pismcode_dir,
                         working_dir=up_settings.working_dir,
                         input_data_dir=up_settings.input_data_dir,
                         pism_executable=up_settings.pism_executable,
                         pism_mpi_do=up_settings.pism_mpi_do
                         )

