
import os
import sys
import pwd
import jinja2
import subprocess
import itertools
import hashlib
import collections
import pandas

def write_pism_runscript(up_settings, template, runscript_path, **kwargs):

    """ This writes a PISM run script.
    """

    # make jinja aware of templates in the templates folder
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                searchpath=os.path.join(up_settings.project_root,"templates")))

    scen_template = jinja_env.get_template(template)
    out = scen_template.render(**kwargs)

    script_to_write = os.path.join(runscript_path,template.replace("template.",""))

    with open(script_to_write, 'w') as f:
        f.write(out)
    subprocess.check_call("chmod u+x "+script_to_write, shell=True)

    print "Wrote",script_to_write


def span_ensemble(ensemble_variables,start_number=0):

    parameter_combinations = list(itertools.product(*ensemble_variables.values()))
    parameter_names = ensemble_variables.keys()

    ensemble_members = collections.OrderedDict()

    for i,pc in enumerate(parameter_combinations):


        em_id = hashlib.sha224(str(pc)).hexdigest()[0:10]

        em_id += " "+str(i + start_number)

        em_params = {name:pc[i] for i,name in enumerate(parameter_names)}
        ensemble_members[em_id] = em_params

    ensemble_members = pandas.DataFrame(ensemble_members)
    ensemble_members = ensemble_members.transpose()

    return ensemble_members


def settings_handler(setting_directory):

    username = pwd.getpwuid(os.getuid()).pw_name

    if setting_directory not in sys.path:
        sys.path.append(settings_directory)

    if "albr" in username:
        import settings_torsten as settings

    elif "meng" in username:
        import settings_matthias as settings

    else:
        print "Create your settings file first."
        print "copy the example settings.py to settings_yourname.py"
        print "and edit the import_settings() function."
        raise NotImplementedError

    return settings