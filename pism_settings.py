
"""
Settings for the PISM model.
This should only be commited for major changes affecting all users.
"""

import os
import numpy as np
import collections

ensemble_name = "pismpik_021_equi20km"
resolution = 20 # in km
## for creation of input data, see icesheets/pism_input project.
input_data_path = "/p/projects/tumble/mengel/pismInputData/20170316_PismInputData"
input_file = "merged/bedmap2_albmap_racmo_hadcm3_I2S_20km.nc"
ocean_file = "schmidtko/schmidtko_20km_means.nc"
#
start_from_file = "/p/tmp/mengel/pism_out/pismpik_020_equilibriumtesting_20km_03/no_mass.nc"


# ensemble parameters
ssa_e = np.array([0.5,1.0])
sia_e = np.array([2.,5.])
# these two are for PICO
overturning_coeff = np.arange(0.5,6.5+3.,3.) # in Sverdrup
# gamma_T in 1.e-5  m/s, e-5 is set in run script.
gamma_T = np.arange(1,5+2.,2.)

# we create PISM run scripts for all the following parameter combinations
ensemble_variables = {"sia":sia_e,"ssa":ssa_e,"ovC":overturning_coeff,"gamT":gamma_T}
# sort by name and keep this sorting
ensemble_variables = collections.OrderedDict(
    sorted(ensemble_variables.items(), key=lambda t: t[0]))

extra_variables = ("thk,topg,velbar_mag,flux_mag,mask,usurf,salinity_ocean,"
                   "theta_ocean,shelfbmassflux,shelfbtemp")

timeseries_variables = ("ivol,imass,slvol,iareag,iareaf,sub_shelf_ice_flux,"
                        "discharge_flux,max_hor_vel,ienthalpy,max_diffusivity,dt")

# TODO: should we include skip values here?
grids = {
    30:"-Mx 200 -My 200 -Lz 5000 -Lbz 2000 -Mz 41 -Mbz 16",
    20:"-Mx 300 -My 300 -Lz 5000 -Lbz 2000 -Mz 81 -Mbz 21",
    15:"-Mx 400 -My 400 -Lz 5000 -Lbz 2000 -Mz 81 -Mbz 21",
    12:"-Mx 500 -My 500 -Lz 5000 -Lbz 2000 -Mz 101 -Mbz 31",
    10:"-Mx 600 -My 600 -Lz 5000 -Lbz 2000 -Mz 101 -Mbz 31",
    7:"-Mx 800 -My 800 -Lz 5000 -Lbz 2000 -Mz 151 -Mbz 31",
    5:"-Mx 1200 -My 1200 -Lz 5000 -Lbz 2000 -Mz 201 -Mbz 51",
    # 2km grid: vertical resolution as from spinup.sh greenland-std example
    2:"-Mx 3000 -My 3000 -Lz 5000 -Lbz 2000 -Mz 501 -Mbz 41 -skip -skip_max 50"
}
