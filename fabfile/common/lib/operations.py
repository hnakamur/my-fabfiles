from fabric.api import sudo, run

def run_or_sudo(use_sudo=False):
    return sudo if use_sudo else run
