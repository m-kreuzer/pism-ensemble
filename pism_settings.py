
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

ensemble_params_defaults={"gamma_T":1.0,"overturning_coeff":1.0,
                          "flex":5.0,"visc":1.0,
                          "prec":0.05,"sia_e":1.0,"ssa_e":1.0,
                          "pdd_snow":3.0,"pdd_ice":8.8,"pdd_std":5.0,
                          "uthres":100.0,"ppq":0.25,
                          "till_dec":3.16887646154128,"till_efo":0.02,
                          "ecalv":1.0e17,"hcalv":50.0,
                          }

ensemble_variables = {}
for param_name,param_default in ensemble_params_defaults.items():
  ensemble_variables[param_name] = np.array([param_default])

flex = np.array([ensemble_params_defaults['flex']])

if up_settings.create_full_physics_script:

  ensemble_name = "pismpik_034_ens15km"
  resolution = 15 # in km
  ## for creation of input data, see icesheets/pism_input project.
  #input_data_path = "/p/projects/tumble/mengel/pismInputData/20170316_PismInputData"
  input_file = "merged/bedmap2_albmap_racmo_hadcm3_I2S_tillphi_pism_"+str(resolution)+"km.nc"
  ocean_file = "schmidtko/schmidtko_"+str(resolution)+"km_means.nc"
  # from where the full physics simulation starts.
  start_from_file = "no_mass_tillphi.nc"

  # equi ensemble parameters
  ensemble_variables['ssa_e'] = np.array([0.6,1.0])
  ensemble_variables['sia_e'] = np.array([2.])
  ensemble_variables['ppq'] = np.array([0.25,0.75])
  ensemble_variables['till_frac_ov'] = np.array([0.02,0.04])
  # these two are for PICO
  # overturning_coeff in 1e6 kg-1 s-1, e6 is set in run script.
  ensemble_variables['overturning_coeff'] = np.array([0.5,6.5])
  # gamma_T in 1.e-5  m/s, e-5 is set in run script.
  ensemble_variables['gamma_T'] = np.array([1,5])

elif up_settings.create_paleo_script:

  ensemble_name = "pism_paleo01"
  resolution = 15 # in km
  ## for creation of input data, see icesheets/pism_input project.
  #input_data_path = "/p/tmp/albrecht/pism17/pismInput"
  input_file = "bedmap2_albmap_racmo_hadcm3_I2S_schmidtko_uplift_velrignot_lgmokill_fttmask_"+str(resolution)+"km.nc"
  #ocean_file = input_file
  #ocean_file = "Schmidtko.jouzel07temponly_basins_resp2.nc"
  ocean_file = "schmidtko14_jouzel07_oceantemp_basins_response3.nc"
  # from where the paleo simulation starts.
  #start_from_file = "/p/tmp/albrecht/pism17/pismOut/forcing/forcing2120_TPSO/results/result_nomass_"+str(resolution)+"km.nc"
  start_from_file = "/p/tmp/albrecht/pism17/pismOut/forcing/forcing2127_TPSO/results/result_fit_"+str(resolution)+"km_50000yrs.nc"
  start_from_file = "/p/tmp/albrecht/pism17/pismOut/forcing/forcing2301_TPSO/results/snap_forcing_"+str(resolution)+"km_205000yrs.nc_-125000.000.nc"

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
    50:"-Mx 120 -My 120 -Lz 6000 -Lbz 2000 -Mz 31 -Mbz 12",
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
