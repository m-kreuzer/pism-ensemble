#!/bin/bash

#SBATCH --qos={{submit_class}}
#SBATCH --time={{cluster_runtime}}
#SBATCH --job-name={{ensemble_name}}
#SBATCH --account={{account}}
#SBATCH --output=./log/slurm_out.out
#SBATCH --error=./log/slurm_error.err
#SBATCH --ntasks={{number_of_cores}}
#SBATCH --tasks-per-node=16
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

# for parallel netcdf writings
export I_MPI_EXTRA_FILESYSTEM=on
export I_MPI_EXTRA_FILESYSTEM_LIST=gpfs

# make the PISM execution script aware that it is on compute nodes.
export PISM_ON_CLUSTER=1

{% if create_smoothing_script -%}
# restarted runs would not need to have smoothing and nomass again
# -> run_smoothing_nomass=false
run_smoothing_nomass=true
if $run_smoothing_nomass ; then
    ./run_smoothing_nomass.sh $SLURM_NTASKS > $outdir/log/pism.out
fi
{%- endif %}

{% if create_full_physics_script -%}
./run_full_physics.sh $SLURM_NTASKS >> $outdir/log/pism.out
{%- endif %}

{% if create_paleo_script -%}
./run_paleo.sh $SLURM_NTASKS >> $outdir/log/pism.out
{%- endif %}

echo run finished at `date`                     >> ./log/srunInfo


