from fabtools.require import files

def ensure_exists(path, use_sudo=False, owner=None, group=None, mode=None):
    files.directory(path, use_sudo, owner, group, mode)
