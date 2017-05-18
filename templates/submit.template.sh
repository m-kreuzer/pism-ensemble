#!/bin/bash

#SBATCH --qos={{submit_class}}
#SBATCH --time={{cluster_runtime}}
#SBATCH --job-name={{ensemble_name}}
#SBATCH --account={{account}}
#SBATCH --output=./log/slurm_out.out
#SBATCH --error=./log/slurm_error.err
#SBATCH --ntasks={{number_of_cores}}
#SBATCH --tasks-per-node=16
#SBATCH --profile=energy
#SBATCH --acctg-freq=energy=5
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user={{username}}@pik-potsdam.de

# get user and platform-specific variables like working_dir, pismcodedir,
# pism_exec and mpi command
source set_environment.sh

runname=`echo $PWD | awk -F/ '{print $NF}'`
outdir=$working_dir/$runname

module purge
module load pism/stable08_srunpetsc

# needed for srun
export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
export OMP_NUM_THREADS=1

export PISM_ON_CLUSTER=1

if [ -f "./run_smoothing_nomass.sh" ]
then
./run_smoothing_nomass.sh $SLURM_NTASKS > $outdir/log/pism.out
fi 

if [ -f "./run_full_physics.sh" ]
then
./run_full_physics.sh $SLURM_NTASKS >> $outdir/log/pism.out
fi

if [ -f "./run_paleo.sh" ]
then
  ./run_paleo.sh $SLURM_NTASKS >> $outdir/log/pism.out
fi
echo run finished at `date`                     >> ./log/srunInfo


