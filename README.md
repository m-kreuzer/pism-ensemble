## PISM-ANT-EQUI - Prepare equilibrium runs with Python


This code aims at easy and transparent creation of PISM run scripts.
It is specific for the Antarctic ice sheet and works across HPC platforms.

### Usage
Edit `user_and_platform_settings.py` and `pism_setting.py` so that they
fit your needs.

Then run `python create_experiment.py`

### Directory structure for experiments

The directory structure is currently hard-coded:

`experiment_dir` and `working_dir` can be set in  `user_and_platform_settings.py`.
`python create_experiment.py`
creates an experiment folder in `experiment_dir` with name `ensemble_name` as set in
`pism_setting.py`. PISM output is written to the folder `ensemble_name`
in the `working_dir` directory.

### License
