#!/bin/bash

# by matthias.mengel@pik-potsdam.de ######
source set_environment.sh

runname=`echo $PWD | awk -F/ '{print $NF}'`
outdir=$working_dir/$runname

# find the latest snapshot from list of files
latest_snap=`ls $outdir/snapshots_[0-9]* | tail -1 | awk -F/ '{print $NF}'`
echo latest snapshot is $latest_snap

# get the year from snapshot name
year=`echo $latest_snap | awk -F_ '{print $NF}'`
echo $year

# copy backup to restart
rsync -aCv --update $outdir/snapshots_$year $outdir/snapshots_restart_$year

# set restart flag to true
sed -i 's/restart=false.*/restart=true/g' run_full_physics.sh

# do not run smoothing and nomass again
sed -i 's/run_smoothing_nomass=true.*/run_smoothing_nomass=false/g' submit.sh

# write newest restart to run file
sed -i 's/.*snapshots_restart.*/'restart_file=snapshots_restart_$year/g run_full_physics.sh

# save timeseries file
rsync -aCv --update $outdir/timeseries.nc $outdir/timeseries_$year
