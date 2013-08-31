from fabric.contrib import files
from fabfile.common.lib.file import calc_sha256sum
from fabfile.common.lib.operations import run_or_sudo

def ensure_downloaded(url, dest, sha256sum=None, use_sudo=False):
    if files.exists(dest, use_sudo):
        if sha256sum is None:
            return
        result = calc_sha256sum(dest, use_sudo)
        if sha256sum == result:
            return
    download(url, dest, use_sudo)

def download(url, dest, use_sudo=False):
    run_fn = run_or_sudo(use_sudo)
    run_fn('curl -kL -o %s %s' % (dest, url))
