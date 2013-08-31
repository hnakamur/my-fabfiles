from fabric.contrib import files
from fabfile.common.lib.operations import run_or_sudo

def calc_sha256sum(path, use_sudo=False):
    if not files.exists(path, use_sudo):
        return None
    run_fn = run_or_sudo(use_sudo)
    output = run_fn("/usr/bin/sha256sum %s" % path)
    return output.stdout.split(' ', 1)[0]
