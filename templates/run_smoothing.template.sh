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
mkdir -v -p $outdir/bin
mkdir -v -p $outdir/src
mkdir -v -p $outdir/log

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

infile={{input_file}}
atmfile=$infile
oceanfile={{ocean_file}}

# Ocean Box Model Parameters
overturning_coeff={{overturning_coeff}}
gamma_T={{gamma_t}}


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
extratm=0:10:1000000
timestm=0:1:1000000
snapstm=0:1:1000000

###### output settings
extra_opts="-extra_file extra -extra_split -extra_times $extratm -extra_vars {{extra_variables}}"
ts_opts="-ts_times $timestm -ts_vars {{timeseries_variables}} -ts_file timeseries.nc"
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

## allow for batch preparation of runs (set runit to false by script)
runit=true
if [ "$runit" = false ]; then exit; fi

cd $outdir

run_opts="-ys $start_year -ye $end_year -o_format netcdf4_parallel -pik -o final.nc"
#run_opts="-ys $start_year -ye $end_year -pik "
options="$init_opts $atm_opts $ocean_opts $calv_opts $ts_opts \
$subgl_opts $basal_opts $run_opts $stress_opts"

$PISM_DO $options
#gdb --args $PISM_DO $options
# mpiexec -n 4
# valgrind --tool=memcheck -q --num-callers=20 --log-file=valgrind.log.%p $PISM_DO -malloc off $options
