from fabric.api import run, sudo, task
from fabric.context_managers import settings

def status(name):
    with settings(ok_ret_codes=[0,3]):
        out = sudo('/sbin/service %s status' % name)
    return 'running' if out.return_code == 0 else 'stopped'

def start(name):
    sudo('/sbin/service %s start' % name)

def stop(name):
    sudo('/sbin/service %s stop' % name)

def reload(name):
    sudo('/sbin/service %s reload' % name)

def restart(name):
    sudo('/sbin/service %s restart' % name)

def ensure_started(name):
    if status(name) != 'running':
        start(name)

def ensure_stopped(name):
    if status(name) != 'stopped':
        stop(name)

def is_auto_start_enabled(name):
    with settings(ok_ret_codes=[0,1]):
        out = sudo('/sbin/chkconfig --list %s | grep -q :on' % name)
    return True if out.return_code == 0 else False

def enable_auto_start(name):
    sudo('/sbin/chkconfig %s on' % name)

def disable_auto_start(name):
    sudo('/sbin/chkconfig %s off' % name)

def ensure_auto_start_enabled(name):
    if not is_auto_start_enabled(name):
        enable_auto_start(name)

def ensure_auto_start_disabled(name):
    if is_auto_start_enabled(name):
        disable_auto_start(name)
