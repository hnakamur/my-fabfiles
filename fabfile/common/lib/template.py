from fabric.contrib import files
from datetime import datetime

FABRIC_MANAGED_DEFAULT_FORMAT = "Fabric managed: %s copied from %s at %s"

def template(filename, destination, context=None, template_dir=None, use_sudo=False, backup=True, mirror_local_mode=False, mode=None, fabric_managed_format=FABRIC_MANAGED_DEFAULT_FORMAT):
    if context is None:
        context = {}
    context['fabric_managed'] = format_fabric_managed(filename, destination,
        fabric_managed_format)
    return files.upload_template(filename, destination,
        context=context, use_jinja=True, template_dir=template_dir,
        use_sudo=use_sudo, backup=backup, mirror_local_mode=mirror_local_mode,
        mode=mode)

def format_fabric_managed(filename, destination,
        fabric_managed_format=FABRIC_MANAGED_DEFAULT_FORMAT):
    return fabric_managed_format % (
        destination,
        filename,
        datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    )
