

import os
import pism_settings as ps; reload(ps)
import user_and_platform_settings as up_settings; reload(up_settings)
import pism_ant_equi.pism_ant_equi as pae; reload(pae)


runscript_path = os.path.join(up_settings.experiment_dir,ps.ensemble_name)

template = "run_smoothing.template.sh"

pae.write_pism_runscript(up_settings, template, runscript_path,
                         input_file = ps.input_file,
                         ocean_file = ps.ocean_file,
                         extra_variables = ps.extra_variables,
                         timeseries_variables = ps.timeseries_variables,
                         )