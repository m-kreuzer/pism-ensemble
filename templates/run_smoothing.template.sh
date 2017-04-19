#!/bin/bash

# created by matthias.mengel@pik-potsdam.de

# get user and platform-specific variables like working_dir, pismcodedir,
# pism_exec and mpi command
source set_environment.sh

runname=`echo $PWD | awk -F/ '{print $NF}'`
codever=`echo $PWD | awk -F/ '{print $NF}' | awk -F_ '{print $1}'`
thisdir=`echo $PWD`
outdir=$working_dir/$runname
PISM_EXEC=$pism_exec

echo $outdir

# create output directory and copy executable and source
mkdir -p $outdir/bin
mkdir -p $outdir/src
mkdir -p $outdir/log

# get new pism code if fetch is argument
if [ "$1" = "fetch" ]
  then
  rsync -aCv $pismcode_dir/$codever/bin/pismr $outdir/bin/
  cd $pismcode_dir/$codever
  echo ------ `date` --- $RUNNAME ------                  >> $thisdir/log/versionInfo
  echo "commit $(git log --pretty=oneline --max-count=1)" >> $thisdir/log/versionInfo
  echo "branch $( git branch | grep \*)"                  >> $thisdir/log/versionInfo
  cd $thisdir
fi

NN=2  # default number of processors
if [ $# -gt 0 ] ; then  # if user says "exp.sh 8" then NN = 8
  NN="$1"
fi

###### use only MPI if job is submitted
if [ -n "${PISM_ON_CLUSTER:+1}" ]; then  # check if env var is set
  echo "$SCRIPTNAME this run was submitted, use MPI"
  PISM_MPIDO=$pism_mpi_do
  echo "$SCRIPTNAME      PISM_MPIDO = $PISM_MPIDO"
else
  echo "$SCRIPTNAME this is interactive, skip use of MPI"
  PISM_MPIDO=""
  NN=""
  echo "$SCRIPTNAME      PISM_MPIDO = $PISM_MPIDO"
fi
PISM_DO="$PISM_MPIDO $NN $PISM_EXEC"

infile=$input_data_dir/{{input_file}}
atmfile=$infile
oceanfile=$input_data_dir/{{ocean_file}}
grid="{{grid}}"

###### output settings
start_year=100000
end_year=100200
extratm=0:100:1000000
timestm=0:1:1000000
snapstm=0:100:1000000
extra_opts="-extra_file extra -extra_split -extra_times $extratm -extra_vars {{extra_variables}}"
ts_opts="-ts_times $timestm -ts_vars {{timeseries_variables}} -ts_file timeseries.nc"
snaps_opts="-save_file snapshots -save_times $snapstm -save_split -save_size medium"
output_opts="$extra_opts $snaps_opts $ts_opts"

###### boundary conditions
atm_opts="-surface simple -atmosphere given -atmosphere_given_file $infile"
ocean_opts="-ocean cavity -ocean_cavity_file $oceanfile -gamma_T {{gamma_T}} \
            -overturning_coeff {{overturning_coeff}}"
calv_opts="-calving ocean_kill -ocean_kill_file $infile"
bed_opts="-bed_def none -hydrology null"
subgl_opts="-subgl -no_subgl_basal_melt"

###### ice physics
basal_opts="-yield_stress mohr_coulomb -topg_to_phi 5,15,-1000,1000"
stress_opts="-stress_balance sia -sia_flow_law gpbld -sia_e {{sia_enhancement}}"

###### technical
init_opts="-bootstrap -i $infile $grid -config my_pism_config.nc"
## netcdf4_parallel needs compilation with
run_opts="-ys $start_year -ye $end_year -o_format netcdf4_parallel -pik -o final.nc"

## allow for batch preparation of runs (set runit to false by script)
runit=true
if [ "$runit" = false ]; then exit; fi

options="$init_opts $run_opts $atm_opts $ocean_opts $calv_opts $bed_opts $subgl_opts \
         $basal_opts $stress_opts $output_opts"

cd $outdir
$PISM_DO $options
#gdb --args $PISM_DO $options
# mpiexec -n 4
# valgrind --tool=memcheck -q --num-callers=20 --log-file=valgrind.log.%p $PISM_DO -malloc off $options

# -i /p/tmp/albrecht/pism17/pismOut/forcing/forcing2120_TPSO/initdata/pism_bedmap2_racmo_uplift_velrignot_lgmokill_15km.nc -bootstrap -Mx 400 -My 400 -Lz 7000 -Lbz 2000 -Mz 141 -Mbz 21 -calving ocean_kill -ocean_kill_file /p/tmp/albrecht/pism17/pismOut/forcing/forcing2120_TPSO/initdata/pism_bedmap2_racmo_uplift_velrignot_lgmokill_15km.nc -bed_def none -hydrology null -atmosphere pik_temp -temp_era_interim -atmosphere_pik_temp_file /p/tmp/albrecht/pism17/pismOut/forcing/forcing2120_TPSO/initdata/pism_bedmap2_racmo_uplift_velrignot_lgmokill_15km.nc -surface pdd -ocean cavity -ocean_cavity_file /p/tmp/albrecht/pism17/pismOut/forcing/forcing2120_TPSO/initdata/Schmidtko.jouzel07temponly_basins_constPD.nc -gamma_T 1.0e-5 -overturning_coeff 0.8e6 -value_C 0.8e6 -exclude_icerises -number_of_basins 20 -continental_shelf_depth -2000 -sia_e 2.0 -pik -topg_to_phi 1.0,45.0,-500.0,1000.0 -bed_smoother_range 5.0e3 -y 200 -o /p/tmp/albrecht/pism17/pismOut/forcing/forcing2120_TPSO/results/result_boot_15km.nc -options_left -verbose 2 -o_order zyx -o_size big