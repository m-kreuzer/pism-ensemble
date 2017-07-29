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
  mkdir -p $outdir/log/
  rsync -aCv $pismcode_dir/$code_version/bin/pismr $outdir/bin/
  cd $pismcode_dir/$code_version
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
#fit_tillphi={{fit_phi}}
#read_tillphi={{read_phi}}

######## FULL PHYSICS EQUILIBRIUM ########
infile={{start_from_file}}
# if restart is set to true below, start from the following file
# (will be updated through the prepare_restart script)
restart_file=snapshots_restart_202000.000.nc

###### output settings
start=200000
length=50000
extratm=$((start)):50:$((start+length))
timestm=$((start)):1:$((start+length))
snapstm=$((start)):500:$((start+length))

extra_opts="-extra_file extra -extra_split -extra_times $extratm -extra_vars {{extra_variables}}"
ts_opts="-ts_times $timestm -ts_vars {{timeseries_variables}} -ts_file timeseries.nc"
snaps_opts="-save_file snapshots -save_times $snapstm -save_split -save_size medium"
output_opts="$extra_opts $snaps_opts $ts_opts"

###### boundary conditions
# if [ "${fit_tillphi,,}" = true ]; then
{% if fit_phi -%}
pscale=`echo "8.2*(1.07-1.0)" | bc -l` #motivated by 7degree temperature change over 1000m height
phi_iter="-prescribe_gl -iterative_phi $origfile -tphi_inverse 500.0 -hphi_inverse 250.0 \
        -phimax_inverse 70.0 -phimin_inverse 2.0 -phimod_inverse 2e-3"
atm_opts="-atmosphere pik_temp,lapse_rate -temp_era_interim -atmosphere_pik_temp_file $infile \
        -surface pdd,forcing -temp_lapse_rate 0.0 -smb_lapse_rate 0.0 \
        -precip_scale_factor $pscale -atmosphere_lapse_rate_file $origfile \
         -force_to_thickness_file $origfile -force_to_thickness_alpha 2e-4 \
         $phi_iter "
calv_opts="-calving ocean_kill -ocean_kill_file $origfile"
outname="equi-fit.nc"
{% else %}
# else
atm_opts="-surface simple -atmosphere given -atmosphere_given_file $atmfile"
calv_opts="-calving eigen_calving,thickness_calving -eigen_calving_K 1e17  \
         -thickness_calving_threshold 200"
outname="equi.nc"
# fi
{%- endif %}

ocean_opts="-ocean cavity -ocean_cavity_file $oceanfile -gamma_T {{ep['gamma_T']}}e-5 \
            -overturning_coeff {{ep['overturning_coeff']}}e6 \
            -exclude_icerises -continental_shelf_depth -2000" #new

bed_opts="-bed_def none -hydrology null"
subgl_opts="" #"-subgl -no_subgl_basal_melt"

###### ice physics
# if [ "${read_tillphi,,}" = true ]; then
{% if read_phi -%}
basal_opts="-yield_stress mohr_coulomb \
            -pseudo_plastic -pseudo_plastic_q {{ep['ppq']}} \
            -pseudo_plastic_uthreshold 100.0 \
            -till_effective_fraction_overburden {{ep['till_efo']}}"
{% else %}
basal_opts="-topg_to_phi 5.0,45.0,-300.0,700.0 \
            -pseudo_plastic -pseudo_plastic_q {{ep['ppq']}} \
            -pseudo_plastic_uthreshold 100.0 \
            -till_effective_fraction_overburden {{ep['till_efo']}}"
            #-yield_stress mohr_coulomb
{%- endif %}

stress_opts="-pik -stress_balance ssa+sia -sia_e {{ep['sia_e']}} \
             -ssa_method fd -ssa_e {{ep['ssa_e']}} " #\
             #-ssa_flow_law gpbld -sia_flow_law gpbld -ssafd_ksp_rtol 1e-7 "

###### technical
# -config $outdir/pism_config_default.nc -config_override $outdir/pism_config_override.nc"
## netcdf4_parallel needs compilation with -DPism_USE_PARALLEL_NETCDF4=YES
run_opts="-o $outname -verbose 2 -options_left -o_format netcdf4_parallel"
#-o_order zyx -o_size big -backup_interval 3.0 "

restart=false
if $restart ; then
  init_opts="-i $restart_file -ye $((start+length))"
else
  init_opts="-i $infile -ys $start -y $length"
fi

options="$init_opts $run_opts $atm_opts $ocean_opts $calv_opts $bed_opts $subgl_opts \
         $basal_opts $stress_opts $output_opts"

diff_opts="-yield_stress mohr_coulomb -ssa_flow_law gpbld -sia_flow_law gpbld -ssafd_ksp_rtol 1e-7 \
           -subgl -no_subgl_basal_melt"

echo "### Full-physics options: ###"
echo $PISM_DO $options #$diff_opts

cd $outdir
$PISM_DO $options

# if [ "${fit_tillphi,,}" = true ]; then
{% if fit_phi -%}
ncap2 -O -s 'precipitation=climatic_mass_balance' $outname $outname
ncap2 -O -s 'where(precipitation==0.0) precipitation=0.001' $outname $outname
{%- endif %}
# fi
