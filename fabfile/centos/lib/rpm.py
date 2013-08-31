from fabric.api import run, sudo, task
from fabric.context_managers import settings
from fabfile.common.lib.operations import run_or_sudo

def ensure_installed(name=None, path=None, use_sudo=False):
    pkg_name = packagename(path) if name is None else name
    if not is_installed(pkg_name):
        install(path or name, use_sudo=use_sudo)

def is_installed(name):
    with settings(ok_ret_codes=[0,1]):
        out = run('rpm -q %s' % name, warn_only=True)
    return out.return_code == 0

def packagename(path):
    out = run('rpm -q --qf %%{Name} -p "%s"' % path)
    return out.stdout

def install(name_or_path, use_sudo=False):
    run_fn = run_or_sudo(use_sudo)
    run_fn('yum install -y "%s"' % name_or_path)
