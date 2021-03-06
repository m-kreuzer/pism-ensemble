
"""
--- THIS IS A TEMPLATE ---
This settings file is here for reference. It does not need to be up to date.
Have a look into the personal settings_*py settings file and pick the one that was
updated latest. a git log settings_somename.py may help you.
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
read_tillphi = True

create_paleo_script = False

## use hashes or numbers as ensemble member identifiers
use_numbers_as_ens_id = True
if use_numbers_as_ens_id:
  initial_ensemble_number = 1263


#"overturning_coeff":1.0,"sia_e":1.0,"ssa_e":1.0,"till_efo":0.02,"ppq":0.25,
#only via config : "pdd_snow":3.0,"pdd_ice":8.8,"pdd_std":5.0,"till_dec":3.16887646154128

ensemble_params_defaults={"gamma_T":1.0,"overturning_coeff":0.8,
                          "flex":5.0,"visc":1.0,
                          "prec":0.05,"sia_e":2.0,"ssa_e":0.6,
                          "pdd_snow":3.0,"pdd_ice":8.8,"pdd_std":5.0,
                          "uthres":100.0,"ppq":0.75,
                          "till_dec":3.16887646154128,"till_efo":0.04,
                          "ecalv":1.0e17,"hcalv":50.0,
                          }

ensemble_variables = {}
for param_name,param_default in ensemble_params_defaults.items():
  ensemble_variables[param_name] = np.array([param_default])

flex = np.array([ensemble_params_defaults['flex']])

if create_full_physics_script:

  ensemble_name = "pismpik_038_initmip08km"
  grid_id = "initmip16km"
  ## for creation of input data, see icesheets/pism_input project.
  #input_data_path = "/p/projects/tumble/mengel/pismInputData/20170316_PismInputData"
  input_file = "bedmap2_albmap_racmo_wessem_tillphi_pism_"+grid_id+".nc"
  ocean_file = "schmidtko_"+grid_id+".nc"
  # from where the full physics simulation starts.
  start_from_file = "no_mass_tillphi.nc"

  # equi ensemble parameters
  ensemble_variables['ssa_e'] = np.array([0.6,1.0])
  ensemble_variables['sia_e'] = np.array([2.])
  ensemble_variables['ppq'] = np.array([0.25,0.75])
  ensemble_variables['till_efo'] = np.array([0.02,0.04])
  # these two are for PICO
  # overturning_coeff in 1e6 kg-1 s-1, e6 is set in run script.
  ensemble_variables['overturning_coeff'] = np.array([0.5,6.5])
  # gamma_T in 1.e-5  m/s, e-5 is set in run script.
  ensemble_variables['gamma_T'] = np.array([1,5])

  if username == "albrecht": # torsten
    ensemble_name = "pismpik_04_15km_fit"
    #start_from_file = "/p/tmp/albrecht/pism17/pismOut/forcing/forcing2300_TPSO/results/result_nomass_"+str(resolution)+"km.nc"
    #start_from_file = "/p/tmp/albrecht/pism17/pismOut/forcing/forcing2300_TPSO/results/result_fit_"+str(resolution)+"km_50000yrs.nc"
    #input_file = "bedmap2_albmap_racmo_hadcm3_I2S_schmidtko_uplift_velrignot_lgmokill_fttmask_"+str(resolution)+"km.nc"
    #input_file = "bedmap2_albmap_racmo_hadcm3_I2S_tillphi_pism_"+str(resolution)+"km.nc"
    #ocean_file = "schmidtko_"+str(resolution)+"km_means.nc"

elif create_paleo_script:

  ensemble_name = "pism_paleo02"
  resolution = 15 # in km
  ## for creation of input data, see icesheets/pism_input project.
  #input_data_path = "/p/tmp/albrecht/pism17/pismInput"
  input_file = "bedmap2_albmap_racmo_hadcm3_I2S_schmidtko_uplift_velrignot_lgmokill_fttmask_"+grid_id+".nc"
  #ocean_file = input_file
  #ocean_file = "Schmidtko.jouzel07temponly_basins_resp2.nc"
  ocean_file = "schmidtko14_jouzel07_oceantemp_basins_response3.nc"
  # from where the paleo simulation starts.
  #start_from_file = "/p/tmp/albrecht/pism17/pismOut/forcing/forcing2120_TPSO/results/result_nomass_"+str(resolution)+"km.nc"
  #start_from_file = "/p/tmp/albrecht/pism17/pismOut/forcing/forcing2127_TPSO/results/result_fit_"+str(resolution)+"km_50000yrs.nc"
  start_from_file = "/p/tmp/albrecht/pism17/pismOut/forcing/forcing2301_TPSO/results/snap_forcing_"+grid_id+"_205000yrs.nc_-125000.000.nc"

  tforce_file = "timeseries_edc-wdc_temp.nc"
  pforce_file = "timeseries_edc-wdc_accum_1.05.nc"
  slforce_file = "imbrie06peltier15_sl.nc"

  # paleo ensemble paramters
  # mantle viscosity in 1e21 Pa s, e21 is set in run script.
  ensemble_variables['visc'] = np.array([0.1,0.5,1.0])
  #ensemble_variables['visc'] = np.array([0.5])
  ensemble_variables['ssa_e'] = np.array([0.4,0.6,0.8])
  #ensemble_variables['ssa_e'] = np.array([0.6])
  ensemble_variables['sia_e'] = np.array([2.0])
  ensemble_variables['ppq'] = np.array([0.25,0.5,0.75])
  #ensemble_variables['ppq'] = np.array([0.75])
  #ensemble_variables['prec'] = np.array([1.02,1.04,1.07])
  ensemble_variables['prec'] = np.array([0.02])
  ensemble_variables['gamma_T'] = np.array([1.0])
  ensemble_variables['overturning_coeff'] = np.array([0.8])
  ensemble_variables['till_dec'] = np.array([3.1])
  ensemble_variables['till_efo'] = np.array([0.01,0.02,0.04])

else:
  print "Choose full_physics or paleo (fit) mode"
  raise NotImplementedError

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
    "initmip8km":"-Mx 761 -My 761 -Lz 6000 -Lbz 2000 -Mz 121 -Mbz 31",
    "initmip16km":"-Mx 381 -My 381 -Lz 6000 -Lbz 2000 -Mz 81 -Mbz 21"
}

"""
Platform and user specific settings
These mostly go to the set_environment.sh that is sourced from
the PISM run script.
This should only be commited for major changes affecting all users.
"""


## find here the mapping between ensemble member ids and the varied parameters.
ensemble_paramater_map = "ensemble_map"
if use_numbers_as_ens_id:
  ensemble_paramater_map = "ensemble_map_"+str(initial_ensemble_number)

cluster_runtime = "0-23:50:00"
number_of_cores = 32
account = "tumble"
submit_class = "short"
username = pwd.getpwuid(os.getuid()).pw_name
project_root = os.path.dirname(os.path.abspath(__file__))

# PIK cluster with slurm-specific compile, options for petsc
pism_mpi_do = "srun -n"
submit_command = "sbatch submit.sh"

if username == "mengel": # matthias
  experiment_dir = os.path.join("/home/",username,"pism_experiments")
  pismcode_dir = os.path.join("/home/",username,"pism")
  pism_code_version = "pismpik"
  working_dir = os.path.join("/p/tmp/",username,"pism_out")
  input_data_dir = "/p/projects/pism/mengel/pism_input/merged"
  submit_template = "submit.template.sh"

# Matthias' Supermuc
elif username == "di36lav":
  experiment_dir = os.path.join("/home/hpc/pr94ga",username,"pism_experiments")
  pismcode_dir = os.path.join("/home/hpc/pr94ga",username,"pism")
  pism_code_version = "pismpik"
  working_dir = os.path.join("/gss/scratch/pr94ga/",username,"pism_out")
  input_data_dir = "/gpfs/work/pr94ga/di36lav/pism_input_files/20170718_initMIP_Input"
  submit_template = "submit_muc.template.sh"
  pism_mpi_do = "mpiexec -n"
  submit_command = "llsubmit submit_muc.sh"
elif username == "albrecht": # torsten
  experiment_dir = os.path.join("/home/",username,"pism17/pism_experiments")
  # base pism code directory
  pismcode_dir = os.path.join("/home/",username,"pism17")
  # specific version as subfolder.
  # create_ensemble will try to copy the pismcode_dir/pism_code_version/bin/pismr
  pism_code_version = "pism0.7_pik"
  working_dir = os.path.join("/p/tmp/",username,"pism17/pismOut/pism_paleo")
#  input_data_dir = "/p/projects/tumble/mengel/pismInputData/20170316_PismInputData"
  input_data_dir = "/p/tmp/albrecht/pism17/pismInput"
  submit_template = "submit.template.sh"

else:
  print "add your user-specific paths in user_and_platform_settings.py"
  raise NotImplementedError

# else for PIK cluster
# pism_mpi_do = "mpiexec.hydra -bootstrap slurm -n"

# where to look for the executable in the output directory
pism_executable = "./bin/pismr"
#pism_executable = "bin/pismr"


## no edits below
# sort by name and keep this sorting
ensemble_variables = collections.OrderedDict(
    sorted(ensemble_variables.items(), key=lambda t: t[0]))
