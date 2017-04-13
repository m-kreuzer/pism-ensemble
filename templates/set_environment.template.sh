#!/bin/bash

# set computer and user specific variables,
# this is sourced from the pism run script, so that
# the pism run script can be shared without effort.
# created by matthias.mengel@pik-potsdam.de

export pismcode_dir={{pismcode_dir}}
export working_dir={{working_dir}}
export input_data_dir={{input_data_dir}}
export pism_exec={{pism_executable}}
export pism_mpi_do="{{pism_mpi_do}}"

