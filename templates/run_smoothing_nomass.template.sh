#!/bin/bash

# created by matthias.mengel@pik-potsdam.de

# get user and platform-specific variables like working_dir, pismcodedir,
# pism_exec and mpi command
source set_environment.sh

runname=`echo $PWD | awk -F/ '{print $NF}'`
#code_version=`echo $PWD | awk -F/ '{print $NF}' | awk -F_ '{print $1}'`
code_version={{code_ver}}
thisdir=`echo $PWD`
outdir=$working_dir/$runname
PISM_EXEC=$pism_exec

NN=2  # default number of processors
if [ $# -gt 0 ] ; then  # if user says "exp.sh 8" then NN = 8
  NN="$1"
fi

###### use MPI only if job is submitted
if [ -n "${PISM_ON_CLUSTER:+1}" ]; then  # check if env var is set
  echo "This run was submitted, use MPI"
  PISM_MPIDO=$pism_mpi_do
else
  echo "This is interactive, skip use of MPI"
  PISM_MPIDO=""
  NN=""
fi

ncgen3 $outdir/pism_config_override.cdl -o $outdir/pism_config_override.nc

# get new pism code if fetch is argument, write git hash to version log file
if [ "$1" = "fetch" ]; then
  mkdir -p $outdir/log
  rsync -aCv $pismcode_dir/$code_version/bin/pismr $outdir/bin/
  cd $pismcode_dir/$code_version
  echo ------ `date` --- $RUNNAME ------                  >> $thisdir/log/version_info.txt
  echo "commit $(git log --pretty=oneline --max-count=1)" >> $thisdir/log/version_info.txt
  echo "branch $( git branch | grep \*)"                  >> $thisdir/log/version_info.txt
  cd $thisdir
fi

echo "PISM_MPIDO = $PISM_MPIDO"
PISM_DO="$PISM_MPIDO $NN $PISM_EXEC"

infile=$input_data_dir/{{input_file}}
atmfile=$infile
tillphi_file=$infile
oceanfile=$input_data_dir/{{ocean_file}}

# same as in pism-ant-equi pism_settings.py
# keep this for reference for manual edits
grid30km="-Mx 200 -My 200 -Lz 6000 -Lbz 2000 -Mz 41 -Mbz 16"
grid20km="-Mx 300 -My 300 -Lz 6000 -Lbz 2000 -Mz 81 -Mbz 21"
grid15km="-Mx 400 -My 400 -Lz 6000 -Lbz 2000 -Mz 81 -Mbz 21"
grid12km="-Mx 500 -My 500 -Lz 6000 -Lbz 2000 -Mz 101 -Mbz 31"
grid10km="-Mx 600 -My 600 -Lz 6000 -Lbz 2000 -Mz 101 -Mbz 31"
grid7km="-Mx 800 -My 800 -Lz 6000 -Lbz 2000 -Mz 151 -Mbz 31"
grid5km="-Mx 1200 -My 1200 -Lz 6000 -Lbz 2000 -Mz 201 -Mbz 51"
# 2km grid: vertical resolution as from spinup.sh greenland-std example
grid2km="-Mx 3000 -My 3000 -Lz 6000 -Lbz 2000 -Mz 501 -Mbz 41 -skip -skip_max 50"

grid="{{grid}}"

######## SMOOTHING ########

###### output settings
start_year=100000
end_year=100200
extratm=0:10:1000000
timestm=0:1:1000000
snapstm=0:100:1000000
extra_opts="-extra_file extra -extra_split -extra_times $extratm -extra_vars {{extra_variables}}"
ts_opts="-ts_times $timestm -ts_vars {{timeseries_variables}} -ts_file timeseries_smoothing.nc"
snaps_opts="-save_file snapshots -save_times $snapstm -save_split -save_size medium"
output_opts="$extra_opts $snaps_opts $ts_opts"

###### boundary conditions
atm_opts="-surface simple -atmosphere given -atmosphere_given_file $infile"
ocean_opts="-ocean pik -meltfactor_pik 5e-3"
calv_opts="-calving ocean_kill -ocean_kill_file $infile"
bed_opts="-bed_def none -hydrology null"
subgl_opts="-subgl -no_subgl_basal_melt"

###### ice physics
basal_opts="-yield_stress mohr_coulomb " #-topg_to_phi 5,15,-1000,1000"
stress_opts="-stress_balance sia -sia_flow_law gpbld" # -sia_e {{ep['sia_e']}}"

###### technical
init_opts="-bootstrap -i $infile $grid -config $outdir/pism_config_default.nc -config_override $outdir/pism_config_override.nc"
## netcdf4_parallel needs compilation with -DPism_USE_PARALLEL_NETCDF4=YES
run_opts="-ys $start_year -ye $end_year -pik -o smoothing.nc -options_left"
# -o_format netcdf4_parallel

options="$init_opts $run_opts $atm_opts $ocean_opts $calv_opts $bed_opts \
         $subgl_opts $basal_opts $stress_opts $output_opts"

echo "### Smoothing options: ###"
echo $PISM_DO $options
cd $outdir
$PISM_DO $options

######## NO MASS ########

infile=smoothing.nc

end_year=200000
extratm=0:2000:1000000
timestm=0:100:1000000
snapstm=0:2000:1000000
extra_opts="-extra_file extra -extra_split -extra_times $extratm -extra_vars {{extra_variables}}"
ts_opts="-ts_times $timestm -ts_vars {{timeseries_variables}} -ts_file timeseries_no_mass.nc"
snaps_opts="-save_file snapshots -save_times $snapstm -save_split -save_size medium"
output_opts="$extra_opts $snaps_opts $ts_opts"

###### ice physics
stress_opts="-no_mass"

###### technical
init_opts="-i $infile -config $outdir/pism_config_default.nc -config_override $outdir/pism_config_override.nc"
## netcdf4_parallel needs compilation with -DPism_USE_PARALLEL_NETCDF4=YES
run_opts="-ye $end_year -pik -o no_mass.nc -options_left"
# -o_format netcdf4_parallel

options="$init_opts $run_opts $atm_opts $ocean_opts $calv_opts $bed_opts \
         $subgl_opts $basal_opts $stress_opts $output_opts"

echo "### No-mass options: ###"
echo $PISM_DO $options
cd $outdir
$PISM_DO $options

## add again the tillphi variable from input data
## (it is not written after option no_mass)
# -6 converts to 64-bit offset format, same as original PISM output
ncks -O -6 -v tillphi $tillphi_file tillphi_tempfile.nc
# workaround: convert to float like in PISM output
ncap2 -O -s "lon_bnds=float(lon_bnds);lat_bnds=float(lat_bnds)" tillphi_tempfile.nc tillphi_tempfile.nc
cp no_mass.nc no_mass_tillphi.nc
ncks -A -v tillphi tillphi_tempfile.nc no_mass_tillphi.nc
