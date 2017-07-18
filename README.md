## PISM-ENSEMBLE - Prepare PISM equilibrium and paleo ensemble runs with Python

This code aims at easy and transparent creation of PISM run scripts.
It is specific for the Antarctic ice sheet and should work across HPC platforms.

### Usage
Edit `user_and_platform_settings.py` and `pism_setting.py` so that they
fit your needs.

For testing and creating a single experiment, run
`python create_experiment.py` directly.

To create an ensemble of experiments, run
`python create_ensemble.py`.

The parameters varied within the ensemble are set in `ensemble_variables`
in `pism_settings.py`. Experiment names within an ensemble are created as

`(ensemble_name)_(param_name1)(param_value1)_(param_name2)(param_value2)_...`

Submit the ensemble with `python submit_ensemble.py`.

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
The directory structure is currently hard-coded. Standard values are:

`experiment_dir = /home/(username)/pism_experiments`

`working_dir = /p/tmp/(username)/pism_out`

### License

This code is licensed under GPLv3, see the LICENSE.txt. See the commit history for authors.
