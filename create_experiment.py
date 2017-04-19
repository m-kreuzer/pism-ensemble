

import os
import subprocess
import pism_settings as ps; reload(ps)
import user_and_platform_settings as up_settings; reload(up_settings)
import pism_ant_equi.pism_ant_equi as pae; reload(pae)

runscript_path = os.path.join(up_settings.experiment_dir,ps.ensemble_name)
output_path = os.path.join(up_settings.working_dir,ps.ensemble_name)
grid = ps.grids[ps.resolution]

if not os.path.exists(runscript_path):
    os.makedirs(runscript_path)
    os.makedirs(os.path.join(runscript_path,"log"))

if up_settings.create_smoothing_script:
    pism_run_script = "run_smoothing_nomass.sh"
    pae.write_pism_runscript(up_settings, "run_smoothing_nomass.template.sh", runscript_path,
                             input_file = ps.input_file,
                             ocean_file = ps.ocean_file,
                             extra_variables = ps.extra_variables,
                             timeseries_variables = ps.timeseries_variables,
                             sia_enhancement = 2.0,
                             grid = grid,
                             gamma_T = ps.gamma_T, overturning_coeff = ps.overturning_coeff
                             )

if up_settings.create_full_physics_script:
    pism_run_script = "run_full_physics.sh"
    pae.write_pism_runscript(up_settings, "run_full_physics.template.sh", runscript_path,
                             input_file = ps.input_file,
                             ocean_file = ps.ocean_file,
                             extra_variables = ps.extra_variables,
                             timeseries_variables = ps.timeseries_variables,
                             sia_enhancement = 2.0,
                             grid = grid,
                             gamma_T = ps.gamma_T,
                             overturning_coeff = ps.overturning_coeff
                             )

pae.write_pism_runscript(up_settings, "set_environment.template.sh", runscript_path,
                         pismcode_dir=up_settings.pismcode_dir,
                         working_dir=up_settings.working_dir,
                         input_data_dir=up_settings.input_data_dir,
                         pism_executable=up_settings.pism_executable,
                         pism_mpi_do=up_settings.pism_mpi_do
                         )

pae.write_pism_runscript(up_settings, "submit.template.sh", runscript_path,
                         submit_class = "short",
                         cluster_runtime = "1-00:00:00",
                         ensemble_name = ps.ensemble_name,
                         number_of_cores = 64,
                         username = up_settings.username,
                         pism_run_script = pism_run_script
                         )

# write a custom parameter file to output path.
# This is an alternative way to tweak parameters.
subprocess.check_call("ncgen3 pism_config.cdl -o "+
                      os.path.join(output_path,"my_pism_config.nc"), shell=True)