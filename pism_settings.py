
"""
Settings for the PISM model.
Besides the ensemble_name, model parameters that are parsed to
the PISM run scripts should be set here.
This should only be commited for major changes affecting all users.
"""

import os
import numpy as np
import collections
import user_and_platform_settings as up_settings; reload(up_settings)

if up_settings.create_full_physics_script:

  ensemble_name = "pismpik_029_test"
  resolution = 15 # in km
  ## for creation of input data, see icesheets/pism_input project.
  #input_data_path = "/p/projects/tumble/mengel/pismInputData/20170316_PismInputData"
  input_file = "merged/bedmap2_albmap_racmo_hadcm3_I2S_"+str(resolution)+"km.nc"
  ocean_file = "schmidtko/schmidtko_"+str(resolution)+"km_means.nc"
  # from where the full physics simulation starts.
  # start_from_file = "/p/tmp/mengel/pism_out/pismpik_020_equilibriumtesting_20km_03/no_mass.nc"
  start_from_file = "/p/tmp/mengel/pism_out/pismpik_028_notillwat/no_mass_reduced.nc"

  # equi ensemble parameters
  ssa_e = np.array([0.5,1.0])
  sia_e = np.array([2.,5.])
  # these two are for PICO
  # overturning_coeff in 1e6 kg-1 s-1, e6 is set in run script.
  #overturning_coeff = np.arange(0.5,6.5+3.,3.)
  overturning_coeff = np.arange(0.5,6.5+3.,3.)
  # gamma_T in 1.e-5  m/s, e-5 is set in run script.
  gamma_T = np.arange(1,5+2.,2.)
  visc = np.array([1.0])
  ppq = np.array([0.75])
  prec = np.array([1.02])
  # we create PISM run scripts for all the following parameter combinations
  #ensemble_variables = {"sia_e":sia_e,"ssa_e":ssa_e,"overturning_coeff":overturning_coeff,"gamma_T":gamma_T}
  ensemble_variables = {"sia_e":sia_e,"ssa_e":ssa_e,"ppq":ppq,"visc":visc,"prec":prec,"overturning_coeff":overturning_coeff,"gamma_T":gamma_T}

elif up_settings.create_paleo_script:

  ensemble_name = "pism_paleo01"
  resolution = 15 # in km
  ## for creation of input data, see icesheets/pism_input project.
  #input_data_path = "/p/tmp/albrecht/pism17/pismInput"
  input_file = "bedmap2_albmap_racmo_hadcm3_I2S_schmidtko_uplift_velrignot_lgmokill_fttmask_"+str(resolution)+"km.nc"
  ocean_file = input_file
  # from where the paleo simulation starts.
  start_from_file = "/p/tmp/albrecht/pism17/pismOut/forcing/forcing2120_TPSO/results/result_nomass_"+str(resolution)+"km.nc"
  tforce_file = "timeseries_edc-wdc_temp.nc"
  pforce_file = "timeseries_edc-wdc_accum_1.05.nc"
  slforce_file = "imbrie06peltier15_sl.nc"

  # paleo ensemble paramters 
  # mantle viscosity in 1e21 Pa s, e21 is set in run script.
  #visc = np.array([0.1,0.5,1.0])
  visc = np.array([0.5])
  ssa_e = np.array([0.4,0.6,0.8])
  #ssa_e = np.array([0.6])
  #ppq = np.array([0.25,0.5,0.75])
  ppq = np.array([0.75])
  #prec = np.array([1.02,1.04,1.07])
  prec = np.array([1.02])
  gamma_T = np.array([1.0])
  overturning_coeff = np.array([0.8])
  sia_e = np.array([2.])
  # we create PISM run scripts for all the following parameter combinations
  ensemble_variables = {"sia_e":sia_e,"ssa_e":ssa_e,"ppq":ppq,"visc":visc,"prec":prec,"overturning_coeff":overturning_coeff,"gamma_T":gamma_T}
  #print ensemble_variables

else:
  print "Choose full_physics or paleo mode"


extra_variables = ("thk,topg,velbar_mag,flux_mag,mask,usurf,salinity_ocean,"
                   "theta_ocean,shelfbmassflux,shelfbtemp,dbdt,cell_area,ice_surface_temp,climatic_mass_balance")
timeseries_variables = ("volume_glacierized_temperate,volume_glacierized_grounded,"
                         "volume_glacierized_shelf,volume_glacierized_cold,volume_glacierized,"
                         "mass_glacierized,enthalpy_glacierized,area_glacierized_temperate_base,"
                         "area_glacierized_grounded,area_glacierized_shelf,area_glacierized_cold_base,"
                         "area_glacierized,volume_rate_of_change_glacierized,"
                         "mass_rate_of_change_glacierized,"
                         "slvol,sub_shelf_ice_flux,"
                         "discharge_flux,max_hor_vel,max_diffusivity,dt")

# TODO: should we include skip values here?
grids = {
    30:"-Mx 200 -My 200 -Lz 6000 -Lbz 2000 -Mz 41 -Mbz 16",
    20:"-Mx 300 -My 300 -Lz 6000 -Lbz 2000 -Mz 81 -Mbz 21",
    15:"-Mx 400 -My 400 -Lz 6000 -Lbz 2000 -Mz 81 -Mbz 21",
    12:"-Mx 500 -My 500 -Lz 6000 -Lbz 2000 -Mz 101 -Mbz 31",
    10:"-Mx 600 -My 600 -Lz 6000 -Lbz 2000 -Mz 101 -Mbz 31",
    7:"-Mx 800 -My 800 -Lz 6000 -Lbz 2000 -Mz 151 -Mbz 31",
    5:"-Mx 1200 -My 1200 -Lz 6000 -Lbz 2000 -Mz 201 -Mbz 51",
    # 2km grid: vertical resolution as from spinup.sh greenland-std example
    2:"-Mx 3000 -My 3000 -Lz 6000 -Lbz 2000 -Mz 501 -Mbz 41 -skip -skip_max 50"
}

## no edits below
# sort by name and keep this sorting
ensemble_variables = collections.OrderedDict(
    sorted(ensemble_variables.items(), key=lambda t: t[0]))
