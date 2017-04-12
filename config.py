
pism_executable="./bin/pismr"

input_file = "albmap_bedmap2_bhflxcap_5km_RtopoRefThkBedmZwallyBasins_lite.nc"
# should be regridded first.
atmosphere_file = "HadCM3_c20_onlyPrecipTemp_15km_ready.for.pism.nc"
ocean_file = "Antarctic_shelf_data_potential.temps_pismready_5km.nc"

# Ocean Box Model Parameters
overturning_coefficient = 1.000000e+06
# turbulent heat transfer coefficient
gamma_T = 2.000000e-05

##### PARAMETERS #####
PWFRAC=0.93
PHIMIN=5
E_SIA=4.5
E_SSA=0.8
Q=0.33
EIGEN_K=2e16
CALVTHK=200

start_year=100000
end_year=100100

# should not be necessary, as we want to avoid regridding within PISM.
THIRTYKMGRID="-Mx 200 -My 200 -Lz 5000 -Lbz 2000 -Mz 41 -Mbz 16"
TWENTYKMGRID="-Mx 300 -My 300 -Lz 5000 -Lbz 2000 -Mz 81 -Mbz 21"
FIFTEENKMGRID="-Mx 400 -My 400 -Lz 5000 -Lbz 2000 -Mz 81 -Mbz 21"
TWELVEKMGRID="-Mx 500 -My 500 -Lz 5000 -Lbz 2000 -Mz 101 -Mbz 31"
TENKMGRID="-Mx 600 -My 600 -Lz 5000 -Lbz 2000 -Mz 101 -Mbz 31"
SEVENKMGRID="-Mx 800 -My 800 -Lz 5000 -Lbz 2000 -Mz 151 -Mbz 31"
FIVEKMGRID="-Mx 1200 -My 1200 -Lz 5000 -Lbz 2000 -Mz 201 -Mbz 51"
grid=FIVEKMGRID


###### output settings

extratm = "0:10:1000000"
timestm = "0:1:1000000"
snapstm = "0:1:1000000"

extra_vars="thk,topg,velbar_mag,flux_mag,mask,dHdt,usurf,hardav,velbase,velsurf,velbar,wvelbase,wvelsurf,tauc,deviatoric_stresses,climatic_mass_balance,gl_mask,rank,bmelt,Soc,Soc_base,Toc,Toc_base,Toc_inCelsius,T_star,Toc_anomaly,overturning,heatflux,basalmeltrate_shelf,basins,BOXMODELmask,BOXMODELmask2,OCEANMEANmask,ICERISESmask,DistGL,DistIF,cell_area,ocean_temp,tillwat,mask,thk,edot_1,edot_2,salinity,salinity_ocean,thetao,theta_ocean,shelfbmassflux,shelfbtemp,strain_rates"
extra_opts="-extra_file extra -extra_split -extra_times $extratm -extra_vars $extra_vars"
ts_vars="ivol,imass,slvol,iareag,iareaf,iarea,surface_ice_flux,grounded_basal_ice_flux,sub_shelf_ice_flux,nonneg_rule_flux,discharge_flux,max_hor_vel,ienthalpy,max_diffusivity,dt"
ts_opts="-ts_times $timestm -ts_vars $ts_vars -ts_file timeseries.nc"
snaps_opts="-save_file snapshots -save_times $snapstm -save_split -save_size medium"

##### OPTIONS #####
# init_opts="-boot_file $input_data_dir/$infile $PIGONEKMGRID"
init_opts="-bootstrap -i $infile $grid"
atm_opts="-surface given -surface_given_file $atmfile"
ocean_opts="-ocean cavity -ocean_cavity_file $oceanfile"
#calv_opts="-calving eigen_calving,thickness_calving -eigen_calving_K $EIGEN_K  -thickness_calving_threshold $CALVTHK"
calv_opts="-calving ocean_kill -ocean_kill_file $infile"

subgl_opts="-subgl -no_subgl_basal_melt"
basal_opts="-yield_stress mohr_coulomb -topg_to_phi 5,15,-1000,1000"
stress_opts="-stress_balance ssa+sia -sia_flow_law gpbld -ssa_method fd -ssa_flow_law gpbld -ssafd_ksp_rtol 1e-7"
stress_opts="-stress_balance sia -sia_flow_law gpbld"

strongksp_opts="-ssafd_ksp_type gmres -ssafd_ksp_norm_type unpreconditioned -ssafd_ksp_pc_side right -ssafd_pc_type asm -ssafd_sub_pc_type lu"

run_opts="-ys $start_year -ye $end_year -o_format netcdf4_parallel -pik -o final.nc"
#run_opts="-ys $start_year -ye $end_year -pik "
options="$init_opts $atm_opts $ocean_opts $calv_opts $ts_opts \
$subgl_opts $basal_opts $run_opts $stress_opts"

$PISM_DO $options
#gdb --args $PISM_DO $options
# mpiexec -n 4
# valgrind --tool=memcheck -q --num-callers=20 --log-file=valgrind.log.%p $PISM_DO -malloc off $options
