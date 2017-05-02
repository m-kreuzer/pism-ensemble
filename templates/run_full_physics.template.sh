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

# get new pism code if fetch is argument
if [ "$1" = "fetch" ]; then
  mkdir -p $outdir/bin/
  mkdir -p $outdir/log/
  rsync -aCv $pismcode_dir/$codever/bin/pismr $outdir/bin/
  cd $pismcode_dir/$codever
  echo ------ `date` --- $RUNNAME ------                  >> $thisdir/log/versionInfo
  echo "commit $(git log --pretty=oneline --max-count=1)" >> $thisdir/log/versionInfo
  echo "branch $( git branch | grep \*)"                  >> $thisdir/log/versionInfo
  cd $thisdir
fi

NN=2  # default number of processors
if [ $# -gt 0 ]; then  # if user says "exp.sh 8" then NN = 8
  NN="$1"
fi

###### use only MPI if job is submitted
if [ -n "${PISM_ON_CLUSTER:+1}" ]; then  # check if env var is set
  echo "This run was submitted, use MPI"
  PISM_MPIDO=$pism_mpi_do
else
  echo "This is interactive, skip use of MPI"
  PISM_MPIDO=""
  NN=""
fi

echo "PISM_MPIDO = $PISM_MPIDO"
PISM_DO="$PISM_MPIDO $NN $PISM_EXEC"

atmfile=$input_data_dir/{{input_file}}
oceanfile=$input_data_dir/{{ocean_file}}
grid="{{grid}}"

######## FULL PHYSICS EQUILIBRIUM ########
infile={{start_from_file}}

###### output settings
length=100000
extratm=0:500:1000000
timestm=0:1:1000000
snapstm=0:500:1000000
extra_opts="-extra_file extra -extra_split -extra_times $extratm -extra_vars {{extra_variables}}"
ts_opts="-ts_times $timestm -ts_vars {{timeseries_variables}} -ts_file timeseries.nc"
snaps_opts="-save_file snapshots -save_times $snapstm -save_split -save_size medium"
output_opts="$extra_opts $snaps_opts $ts_opts"

###### boundary conditions
atm_opts="-surface simple -atmosphere given -atmosphere_given_file $atmfile"
ocean_opts="-ocean cavity -ocean_cavity_file $oceanfile -gamma_T {{ep['gamma_T']}}e-5 \
            -overturning_coeff {{ep['overturning_coeff']}}e6"
calv_opts="-calving eigen_calving,thickness_calving -eigen_calving_K 1e17  \
           -thickness_calving_threshold 200"
bed_opts="-bed_def none -hydrology null"
subgl_opts="-subgl -no_subgl_basal_melt"

###### ice physics
basal_opts="-yield_stress mohr_coulomb -topg_to_phi 5,15,-1000,1000"
stress_opts="-stress_balance ssa+sia -sia_flow_law gpbld -sia_e {{ep['sia_e']}} \
             -ssa_method fd -ssa_flow_law gpbld -ssa_e {{ep['ssa_e']}} -ssafd_ksp_rtol 1e-7 "

###### technical
init_opts="-i $infile -bootstrap $grid"
## netcdf4_parallel needs compilation with -DPism_USE_PARALLEL_NETCDF4=YES
run_opts="-y $length -pik -o equi.nc -verbose 2 -options_left"

options="$init_opts $run_opts $atm_opts $ocean_opts $calv_opts $bed_opts $subgl_opts \
         $basal_opts $stress_opts $output_opts"

echo "### Full-physics options: ###"
echo $PISM_DO $options

cd $outdir
$PISM_DO $options