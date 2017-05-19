

import os
import shutil
import subprocess
import pism_settings as ps; reload(ps)
import user_and_platform_settings as up_settings; reload(up_settings)
import pism_ant_equi.pism_ant_equi as pae; reload(pae)


def create_experiment(ensemble_member_name=ps.ensemble_name,
                      ensemble_params=ps.ensemble_params_defaults,
                      copy_pism_exec=False):


    runscript_path = os.path.join(up_settings.experiment_dir,ensemble_member_name)
    output_path = os.path.join(up_settings.working_dir,ensemble_member_name)
    grid = ps.grids[ps.resolution]

    if not os.path.exists(runscript_path):
        os.makedirs(runscript_path)
        os.makedirs(os.path.join(runscript_path,"log"))

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        os.makedirs(os.path.join(output_path,"log"))
        os.makedirs(os.path.join(output_path,"bin"))

    if (up_settings.create_smoothing_script):
      pae.write_pism_runscript(up_settings, "run_smoothing_nomass.template.sh", runscript_path,
                             code_ver = up_settings.pism_code_version,
                             input_file = ps.input_file,
                             ocean_file = ps.ocean_file,
                             extra_variables = ps.extra_variables,
                             timeseries_variables = ps.timeseries_variables,
                             grid = grid,
                             ep = ensemble_params )

    if (up_settings.create_full_physics_script):
      pae.write_pism_runscript(up_settings, "run_full_physics.template.sh", runscript_path,
                             code_ver = up_settings.pism_code_version,
                             input_file = ps.input_file,
                             ocean_file = ps.ocean_file,
                             start_from_file = ps.start_from_file,
                             extra_variables = ps.extra_variables,
                             timeseries_variables = ps.timeseries_variables,
                             grid = grid,
                             ep = ensemble_params )
    if (up_settings.create_paleo_script):
      pae.write_pism_runscript(up_settings, "run_paleo.template.sh", runscript_path,
                             code_ver = up_settings.pism_code_version,
                             input_file = ps.input_file,
                             ocean_file = ps.ocean_file,
                             tforce_file = ps.tforce_file,
                             pforce_file = ps.pforce_file,
                             slforce_file = ps.slforce_file,
                             start_from_file = ps.start_from_file,
                             extra_variables = ps.extra_variables,
                             timeseries_variables = ps.timeseries_variables,
                             grid = grid,
                             ep = ensemble_params )


    pae.write_pism_runscript(up_settings, "set_environment.template.sh", runscript_path,
                             pismcode_dir=up_settings.pismcode_dir,
                             working_dir=up_settings.working_dir,
                             input_data_dir=up_settings.input_data_dir,
                             pism_executable=up_settings.pism_executable,
                             pism_mpi_do=up_settings.pism_mpi_do )

    pae.write_pism_runscript(up_settings, "submit.template.sh", runscript_path,
                             submit_class = up_settings.submit_class,
                             account = up_settings.account,
                             cluster_runtime = up_settings.cluster_runtime,
                             ensemble_name = ensemble_member_name,
                             number_of_cores = up_settings.number_of_cores,
                             username = up_settings.username)

    if copy_pism_exec:
        shutil.copy(os.path.join(up_settings.pismcode_dir,
                                 up_settings.pism_code_version,
                                 "bin","pismr"),
                    os.path.join(output_path,"bin"))

    subprocess.check_call("ncgen3 pism_config.cdl -o "+
                          os.path.join(output_path,"pism_config_default.nc"), shell=True)
    # write a custom parameter file to output path.
    # This is an alternative way to tweak parameters.
    pae.write_pism_runscript(up_settings, "pism_config_override.template.cdl", output_path,
                             ep = ensemble_params)

if __name__ == "__main__":
    create_experiment()
