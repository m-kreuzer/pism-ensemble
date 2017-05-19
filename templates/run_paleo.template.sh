#!/bin/bash

# created by matthias.mengel@pik-potsdam.de and torsten.albrecht@pik-potsdam.de

# get user and platform-specific variables like working_dir, pismcodedir,
# pism_exec and mpi command
source set_environment.sh

runname=`echo $PWD | awk -F/ '{print $NF}'`
#codever=`echo $PWD | awk -F/ '{print $NF}' | awk -F_ '{print $1}'`
codever={{code_ver}}
thisdir=`echo $PWD`
outdir=$working_dir/$runname
PISM_EXEC=$pism_exec

NN=2  # default number of processors
if [ $# -gt 0 ] ; then  # if user says "exp.sh 8" then NN = 8
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

ncgen3 $outdir/pism_config_override.cdl -o $outdir/pism_config_override.nc

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


echo "PISM_MPIDO = $PISM_MPIDO"
PISM_DO="$PISM_MPIDO $NN $PISM_EXEC"

origfile=$input_data_dir/{{input_file}}
atmfile=$input_data_dir/{{input_file}}
oceanfile=$input_data_dir/{{ocean_file}}
grid="{{grid}}"

######## PALEO SPIN-UP ########
infile={{start_from_file}}
tforcefile=$input_data_dir/{{tforce_file}}
pforcefile=$input_data_dir/{{pforce_file}}
slforcefile=$input_data_dir/{{slforce_file}}

###### output settings
length=205000
extratm=$((-length)):1000:0
timestm=$((-length)):1:0
snapstm=$((-length)):5000:0
extra_opts="-extra_file extra -extra_times $extratm -extra_vars {{extra_variables}}" #-extra_split
ts_opts="-ts_times $timestm -ts_vars {{timeseries_variables}} -ts_file timeseries.nc"
snaps_opts="-save_file snapshots -save_times $snapstm -save_split -save_size medium"
output_opts="$extra_opts $snaps_opts $ts_opts"

###### boundary conditions
#atm_opts="-surface simple -atmosphere given -atmosphere_given_file $atmfile"
pscale=`echo "8.2*(1.07-1.0)" | bc -l` #motivated by 7degree temperature change over 1000m height
atm_opts="-atmosphere pik_temp,delta_T,paleo_precip -temp_era_interim -atmosphere_pik_temp_file $infile \
          -atmosphere_delta_T_file $tforcefile -atmosphere_paleo_precip_file $tforcefile \
          -surface pdd,lapse_rate -temp_lapse_rate 0.0 -smb_lapse_rate 0.0 \
          -precip_scale_factor $pscale -surface_lapse_rate_file $origfile "

ocean_opts="-ocean cavity,delta_SL -ocean_cavity_file $oceanfile -ocean_delta_SL_file $slforcefile \
            -exclude_icerises -number_of_basins 20 -continental_shelf_depth -2000 \ 
            -gamma_T {{ep['gamma_T']}}e-5 -overturning_coeff {{ep['overturning_coeff']}}e6" #TODO: Put to config

calv_opts="-calving eigen_calving,thickness_calving,ocean_kill \
           -ocean_kill_file $origfile -ocean_kill_mask "
           #-eigen_calving_K 1e17 -thickness_calving_threshold 75 "

bed_opts="-bed_def lc -hydrology null"
subgl_opts="-subgl " #-no_subgl_basal_melt" #-tauc_slippery_grounding_lines

###### ice physics
basal_opts="-yield_stress mohr_coulomb -pseudo_plastic " #-topg_to_phi 5,45,-500,1000"
            #-pseudo_plastic_q {{ep['ppq']}} -pseudo_plastic_uthreshold 100.0 -till_effective_fraction_overburden 0.03"
stress_opts="-pik -stress_balance ssa+sia -ssa_method fd \
             -sia_flow_law gpbld -ssa_flow_law gpbld  -ssafd_ksp_rtol 1e-7 "
             #-sia_e {{ep['sia_e']}} -ssa_e {{ep['ssa_e']}}"

###### technical
config_opts="-config $outdir/pism_config_default.nc -config_override $outdir/pism_config_override.nc"
regrid_opts="-bootstrap $grid -regrid_file $infile -regrid_vars topg,thk,usurf,Href,tillwat,bmelt,enthalpy,litho_temp,temp,tillphi"
init_opts="-i $infile $regrid_opts"
## netcdf4_parallel needs compilation with -DPism_USE_PARALLEL_NETCDF4=YES
run_opts="-ys $((-length)) -ye 0 -o paleo.nc -o_size big -o_order zyx -backup_interval 3.0 -verbose 2 -options_left"

options="$init_opts $config_opts $run_opts $atm_opts $ocean_opts $calv_opts $bed_opts $subgl_opts \
         $basal_opts $stress_opts $output_opts"

echo "### Paleo options: ###"
echo $PISM_DO $options

cd $outdir
$PISM_DO $options