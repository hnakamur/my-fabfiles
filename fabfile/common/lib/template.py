from datetime import datetime
import hashlib
import os
from StringIO import StringIO

from fabric.api import env, hide, put, settings
from fabric.contrib import files
from fabric.utils import apply_lcwd
from fabfile.common.lib.operations import run_or_sudo
from fabfile.common.lib import file

FABRIC_MANAGED_DEFAULT_FORMAT = "Fabric managed: %(dest)s copied from %(src)s"

def ensure_template(filename, destination, context=None, template_dir=None, use_sudo=False, backup=True, mirror_local_mode=False, mode=None, fabric_managed_format=FABRIC_MANAGED_DEFAULT_FORMAT):
    run_fn = run_or_sudo(use_sudo)
    # Normalize destination to be an actual filename, due to using StringIO
    with settings(hide('everything'), warn_only=True):
        if run_fn('test -d %s' % _expand_path(destination)).succeeded:
            sep = "" if destination.endswith('/') else "/"
            destination += sep + os.path.basename(filename)

    context = modify_context(filename, destination, context=context,
        fabric_managed_format=fabric_managed_format)
    text = render_as_text(filename, context=context, template_dir=template_dir)
    local_sum = hashlib.sha256(text).hexdigest()
    remote_sum = file.calc_sha256sum(destination, use_sudo=use_sudo)
    if remote_sum == local_sum:
        return False

    # Use mode kwarg to implement mirror_local_mode, again due to using
    # StringIO
    if mirror_local_mode and mode is None:
        mode = os.stat(filename).st_mode
        # To prevent put() from trying to do this
        # logic itself
        mirror_local_mode = False

    # Back up original file
    if backup and exists(destination):
        run_fn("cp %s{,.bak}" % _expand_path(destination))

    # Upload the file.
    put(
        local_path=StringIO(text),
        remote_path=destination,
        use_sudo=use_sudo,
        mirror_local_mode=mirror_local_mode,
        mode=mode
    )
    return True

def modify_context(filename, destination, context=None, fabric_managed_format=FABRIC_MANAGED_DEFAULT_FORMAT):
    if context is None:
        context = {}
    context['fabric_managed'] = format_fabric_managed(filename, destination,
        fabric_managed_format)
    return context

def format_fabric_managed(filename, destination,
        fabric_managed_format=FABRIC_MANAGED_DEFAULT_FORMAT):
    return fabric_managed_format % {
        'dest': destination,
        'src': filename
    }

def render_as_text(filename, context=None, template_dir=None):
    try:
        template_dir = template_dir or os.getcwd()
        template_dir = apply_lcwd(template_dir, env)
        from jinja2 import Environment, FileSystemLoader
        jenv = Environment(loader=FileSystemLoader(template_dir))
        text = jenv.get_template(filename).render(**context or {})
        # Force to a byte representation of Unicode, or str()ification
        # within Paramiko's SFTP machinery may cause decode issues for
        # truly non-ASCII characters.
        text = text.encode('utf-8')
        return text
    except ImportError:
        import traceback
        tb = traceback.format_exc()
        abort(tb + "\nUnable to import Jinja2 -- see above.")

def _expand_path(path):
    return '"$(echo %s)"' % path
