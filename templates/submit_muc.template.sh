#!/bin/bash
#  DO NOT USE environment = COPY_ALL

#@ job_name = smuc_$(cluster)_$(stepid)
#@ class = micro
#@ group = pr94ga
#@ notify_user = mengel@pik-potsdam.de
#@ job_type = MPICH
#@ output = ./log/loadl.out
#@ error  = ./log/loadl.err
#@ wall_clock_limit = 47:30:00
#@ notification=always
#@ network.MPI = sn_all,not_shared,us
#@ node = 5
#@ tasks_per_node = 28
#@ island_count = 1
#@ energy_policy_tag = albrecht_pism_2015
#@ minimize_time_to_solution = yes
#@ queue

. /etc/profile
. /etc/profile.d/modules.sh

#setup of environment
module unload mpi.ibm
module unload netcdf
module load mpi.intel
module load intel
module load gcc/6
module load petsc/3.7
module load gsl/2.3
module load netcdf/mpi/4.3
module load hdf5/mpi
module load fftw/mpi/3.3

# get user and computer specific variables like paths
source set_environment.sh
runname=`echo $PWD | awk -F/ '{print $NF}'`
outdir=$working_dir/$runname

echo $LOADL_STEP_ID
echo $HOME
echo $LOADL_PROCESSOR_LIST
echo $LOADL_TOTAL_TASKS
echo $outdir

number_of_cores=`echo $LOADL_PROCESSOR_LIST | wc -w`
echo $number_of_cores

export PISM_ON_CLUSTER=1
run_smoothing_nomass.sh $LOADL_TOTAL_TASKS > $outdir/log/smoothing_nomass.out
run_full_physics.sh $LOADL_TOTAL_TASKS >> $outdir/log/full_physics.out

