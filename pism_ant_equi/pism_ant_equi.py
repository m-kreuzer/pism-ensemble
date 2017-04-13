
import os
import jinja2



def write_pism_runscript(up_settings, template, runscript_path, **kwargs):

    """ This writes a PISM run script.
    """

    # make jinja aware of templates in the templates folder
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                searchpath=os.path.join(up_settings.project_root,"templates")))

    print os.path.join(up_settings.project_root,"templates")
    scen_template = jinja_env.get_template(template)
    out = scen_template.render(**kwargs)

    if not os.path.exists(runscript_path): os.makedirs(runscript_path)

    script_to_write = os.path.join(runscript_path,template.replace("template.",""))

    with open(script_to_write, 'w') as f:
        f.write(out)
    print "Wrote",script_to_write,"to"
    print runscript_path
