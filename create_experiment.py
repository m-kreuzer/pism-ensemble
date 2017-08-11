

import os
import shutil
import subprocess
import pism_ensemble.pism_ensemble as pae; reload(pae)

def create_experiment(settings, ensemble_member_name,
                      ensemble_params, copy_pism_exec=True):


    runscript_path = os.path.join(settings.experiment_dir,ensemble_member_name)
    output_path = os.path.join(settings.working_dir,ensemble_member_name)
    grid = settings.grids[settings.grid_id]

    print "## creating experiment in", runscript_path

    if not os.path.exists(runscript_path):
        os.makedirs(runscript_path)
        os.makedirs(os.path.join(runscript_path,"log"))

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        os.makedirs(os.path.join(output_path,"log"))
        os.makedirs(os.path.join(output_path,"bin"))


    pae.write_pism_runscript(settings, "set_environment.template.sh", runscript_path,
                             pismcode_dir=settings.pismcode_dir,
                             working_dir=settings.working_dir,
                             input_data_dir=settings.input_data_dir,
                             pism_executable=settings.pism_executable,
                             pism_mpi_do=settings.pism_mpi_do )

    pae.write_pism_runscript(settings, settings.submit_template, runscript_path,
                             submit_class = settings.submit_class,
                             account = settings.account,
                             cluster_runtime = settings.cluster_runtime,
                             ensemble_name = ensemble_member_name,
                             number_of_cores = settings.number_of_cores,
                             username = settings.username,
                             create_smoothing_script = settings.create_smoothing_script,
                             create_full_physics_script = settings.create_full_physics_script,
                             create_paleo_script = settings.create_paleo_script)


    if (settings.create_smoothing_script):
        pae.write_pism_runscript(settings, "run_smoothing_nomass.template.sh", runscript_path,
                             code_ver = settings.pism_code_version,
                             input_file = settings.input_file,
                             ocean_file = settings.ocean_file,
                             extra_variables = settings.extra_variables,
                             timeseries_variables = settings.timeseries_variables,
                             grid = grid,
                             ep = ensemble_params )

    if (settings.create_full_physics_script):
        pae.write_pism_runscript(settings, "run_full_physics.template.sh", runscript_path,
                             code_ver = settings.pism_code_version,
                             fit_phi = settings.optimize_tillphi,
                             read_phi = settings.read_tillphi,
                             input_file = settings.input_file,
                             ocean_file = settings.ocean_file,
                             start_from_file = settings.start_from_file,
                             extra_variables = settings.extra_variables,
                             timeseries_variables = settings.timeseries_variables,
                             regrid_from_inputfile = settings.regrid_from_inputfile,
                             grid = grid,
                             ep = ensemble_params )

    if (settings.create_restart_prepare_script):
        pae.write_pism_runscript(settings, "prepare_restart.template.sh", runscript_path)

    if (settings.create_paleo_script):

        visc = ensemble_params['visc']
        if visc == 0.5:
            start_from_file = settings.start_from_file
        elif visc == 0.1:
            start_from_file = settings.start_from_file.replace("2301","2302")
        elif visc == 1.0:
            start_from_file = settings.start_from_file.replace("2301","2303")


        pae.write_pism_runscript(settings, "run_paleo.template.sh", runscript_path,
                             code_ver = settings.pism_code_version,
                             input_file = settings.input_file,
                             ocean_file = settings.ocean_file,
                             tforce_file = settings.tforce_file,
                             pforce_file = settings.pforce_file,
                             slforce_file = settings.slforce_file,
                             start_from_file = start_from_file,
                             extra_variables = settings.extra_variables,
                             timeseries_variables = settings.timeseries_variables,
                             grid = grid,
                             ep = ensemble_params )


    if copy_pism_exec:
        shutil.copy(os.path.join(settings.pismcode_dir,
                                 settings.pism_code_version,
                                 "bin","pismr"),
                    os.path.join(output_path,"bin"))

    subprocess.check_call("ncgen3 pism_config.cdl -o "+
                          os.path.join(output_path,"pism_config_default.nc"), shell=True)
    # write a custom parameter file to output path.
    # This is an alternative way to tweak parameters.
    pae.write_pism_runscript(settings, "pism_config_override.template.cdl", output_path,
                             ep = ensemble_params)

if __name__ == "__main__":

    project_root = os.path.dirname(os.path.realpath(__file__))
    settings = pae.settings_handler(project_root)

    create_experiment(settings, settings.ensemble_name,
        settings.ensemble_params_defaults)
