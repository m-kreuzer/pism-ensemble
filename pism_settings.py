
"""
Settings for the PISM model.
This should only be commited for major changes affecting all users.
"""

import os
import numpy as np

ensemble_name = "pismpik_020_equilibriumtesting_20km_03"
resolution = 20 # in km
## for creation of input data, see icesheets/pism_input project.
input_data_path = "/p/projects/tumble/mengel/pismInputData/20170316_PismInputData"
input_file = "merged/bedmap2_albmap_racmo_hadcm3_I2S_20km.nc"
ocean_file = "schmidtko/schmidtko_20km_means.nc"
do_smoothing = True
do_nomass = True
do_full_physics = False

# ensemble parameters
ssa_e = np.arange(0.5,1.1,0.1)
sia_e = np.arange(2,5,1)
# these two are for PICO
overturning_coeff = 2e-5
gamma_T = 1e6

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