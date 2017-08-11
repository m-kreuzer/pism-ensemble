
"""
--- THIS IS A PERSONAL SETTNGS FILE ---
If you are not the author, you should not edit, but rather copy it to a new
file, for example settings_yourname.py.
Then add 2 lines to the pism_ensemble.settings_handler function. And
use settings_yourname.py freely.
"""

import os, pwd
import numpy as np
import collections

username = pwd.getpwuid(os.getuid()).pw_name

## create these scripts if True.
create_smoothing_script = False
create_full_physics_script = True
create_restart_prepare_script = True

optimize_tillphi = False #works only with PISM code version
#https://github.com/talbrecht/pism_pik/tree/pik_newdev_paleo_07
# use a predefined tillphi, if False, use the topg_to_phi parametrization.
read_tillphi = True
create_paleo_script = False

## use hashes or numbers as ensemble member identifiers
use_numbers_as_ens_id = True
initial_ensemble_number = 1262

ensemble_params_defaults={"gamma_T":1.0,"overturning_coeff":0.5,
                          "sia_e":2.0,"ssa_e":1.0,
                          "till_efo":0.04,"ppq":0.75,
                          # constant for now
                          "prec":0.05,
                          "pdd_snow":3.0,"pdd_ice":8.8,"pdd_std":5.0,
                          "uthres":100.0,"till_dec":3.16887646154128,
                          "ecalv":1.0e17,"hcalv":50.0,
                          }

ensemble_variables = {}
for param_name,param_default in ensemble_params_defaults.items():
  ensemble_variables[param_name] = np.array([param_default])

ensemble_name = "pismpik_038_initmip08km"
grid_id = "initmip8km"
# with this option, certain fixed-in-time variables are taken from input_file,
# and other model-state variables from start_from_file
regrid_from_inputfile = True
## for creation of input data, see icesheets/pism_input project.
#input_data_path = "/p/projects/tumble/mengel/pismInputData/20170316_PismInputData"
input_file = "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc"
ocean_file = "schmidtko_"+grid_id+".nc"
# from where the full physics simulation starts.
start_from_file = "/p/tmp/mengel/pism_out/pismpik_037_initmip16km_1239/snapshots_300000.000.nc"

# equi ensemble parameters
ensemble_variables['ssa_e'] = np.array([0.8,1.0])
ensemble_variables['sia_e'] = np.array([2.])
ensemble_variables['ppq'] = np.array([0.5,0.75])
ensemble_variables['till_efo'] = np.array([0.04])
# these two are for PICO
# overturning_coeff in 1e6 kg-1 s-1, e6 is set in run script.
ensemble_variables['overturning_coeff'] = np.array([0.5])
# gamma_T in 1.e-5  m/s, e-5 is set in run script.
ensemble_variables['gamma_T'] = np.array([1,5])

# Torstens set
# ensemble_variables['ssa_e'] = np.array([0.4,0.6,0.8])
# ensemble_variables['sia_e'] = np.array([2.0])
# ensemble_variables['ppq'] = np.array([0.25,0.5,0.75])
# #ensemble_variables['ppq'] = np.array([0.75])
# #ensemble_variables['prec'] = np.array([1.02,1.04,1.07])
# ensemble_variables['prec'] = np.array([0.02])
# ensemble_variables['gamma_T'] = np.array([1.0])
# ensemble_variables['overturning_coeff'] = np.array([0.8])
# ensemble_variables['till_dec'] = np.array([3.1])
# ensemble_variables['till_efo'] = np.array([0.01,0.02,0.04])


extra_variables = ("surface_mass_balance_average,basal_mass_balance_average,"
                     "diff_mask,diff_usurf,tillphi,tillwat,ocean_kill_mask,"
                     "velbar_mag,velsurf_mag,velbar,flux_mag,"
                     "taub_mag,taub,tauc,taud_mag,"
                     "salinity_ocean,theta_ocean,shelfbmassflux,shelfbtemp,bmelt,"
                     "cell_area,mask,thk,topg,dHdt,dbdt,usurf,"
                     "ice_surface_temp,climatic_mass_balance,precipitation,air_temp")
timeseries_variables = ("volume_glacierized_temperate,volume_glacierized_grounded,"
                         "volume_glacierized_shelf,volume_glacierized_cold,volume_glacierized,"
                         "mass_glacierized,enthalpy_glacierized,area_glacierized_temperate_base,"
                         "area_glacierized_grounded,area_glacierized_shelf,area_glacierized_cold_base,"
                         "area_glacierized,volume_rate_of_change_glacierized,"
                         "mass_rate_of_change_glacierized,"
                         "slvol,sub_shelf_ice_flux,"
                         "discharge_flux,max_hor_vel,max_diffusivity,dt,"
                         "surface_ice_flux,grounded_basal_ice_flux,nonneg_rule_flux")

# TODO: should we include skip values here?
grids = {
    "50km":"-Mx 120 -My 120 -Lz 6000 -Lbz 2000 -Mz 31 -Mbz 12",
    "30km":"-Mx 200 -My 200 -Lz 6000 -Lbz 2000 -Mz 41 -Mbz 16",
    "20km":"-Mx 300 -My 300 -Lz 6000 -Lbz 2000 -Mz 81 -Mbz 21",
    "15km":"-Mx 400 -My 400 -Lz 6000 -Lbz 2000 -Mz 81 -Mbz 21",
    "12km":"-Mx 500 -My 500 -Lz 6000 -Lbz 2000 -Mz 101 -Mbz 31",
    "10km":"-Mx 600 -My 600 -Lz 6000 -Lbz 2000 -Mz 101 -Mbz 31",
    "7km":"-Mx 800 -My 800 -Lz 6000 -Lbz 2000 -Mz 151 -Mbz 31",
    "5km":"-Mx 1200 -My 1200 -Lz 6000 -Lbz 2000 -Mz 201 -Mbz 51",
    # 2km grid: vertical resolution as from spinup.sh greenland-std example
    "2km":"-Mx 3000 -My 3000 -Lz 6000 -Lbz 2000 -Mz 501 -Mbz 41 -skip -skip_max 50",
    "initmip8km":"-Mx 761 -My 761 -Lz 6000 -Lbz 2000 -Mz 121 -Mbz 31 -skip -skip_max 10",
    "initmip16km":"-Mx 381 -My 381 -Lz 6000 -Lbz 2000 -Mz 81 -Mbz 21"
}

## find here the mapping between ensemble member ids and the varied parameters.
ensemble_map_file = os.path.join("ensemble_maps",
    ensemble_name+"_"+str(initial_ensemble_number)+".csv")

## set your submission script variables
cluster_runtime = "0-23:50:00"
number_of_cores = 64
account = "tumble"
submit_class = "short"
username = pwd.getpwuid(os.getuid()).pw_name

## PIK cluster with slurm-specific compile, options for petsc
pism_mpi_do = "srun -n"
submit_command = "sbatch submit.sh"
experiment_dir = os.path.join("/home/",username,"pism_experiments")
# we will look in pismcode_dir/pism_code_version/build for the pismr executable
# and copy it to the experiment_directory/bin. It runs from there.
pismcode_dir = os.path.join("/home/",username,"pism")
pism_code_version = "pismpik"
working_dir = os.path.join("/p/tmp/",username,"pism_out")
input_data_dir = "/p/projects/pism/mengel/pism_input/merged"
submit_template = "submit.template.sh"

# where to look for the executable in the output directory
pism_executable = "./bin/pismr"

## no edits needed below
# sort by name and keep this sorting
ensemble_variables = collections.OrderedDict(
    sorted(ensemble_variables.items(), key=lambda t: t[0]))

# this is a hack, but we do not know better.
project_root = os.path.dirname(os.path.abspath(__file__))
