## PISM-ANT-EQUI - Prepare equilibrium runs with Python


This code aims at easy and transparent creation of PISM run scripts.
It is specific for the Antarctic ice sheet and works across HPC platforms.

### Usage
Edit `user_and_platform_settings.py` and `pism_setting.py` so that they
fit your needs.

Then run `python create_experiment.py`

### Directory structure for experiments

Scripts for running PISM and PISM output files are written to:

```
Scripts:
experiment_dir/ensemble_name

Output files:
working_dir/ensemble_name
```

`experiment_dir` and `working_dir` are set in  `user_and_platform_settings.py`.
`ensemble_name` is set in `pism_setting.py`.
The directory structure is currently hard-coded.

### Authors
Written by Matthias Mengel, based at Potsdam Institute for Climate Impact Research.
