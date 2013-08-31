from fabric.api import task
from fabfile.centos.lib import rpm
from fabfile.common.lib import template

@task(default=True)
def ensure_setup():
    ensure_package_installed()
    ensure_config_file()

def ensure_package_installed():
    rpm.ensure_installed('sysstat')

def ensure_config_file():
    template.ensure_template(
        'sysstat.cron.j2',
        '/etc/cron.d/sysstat',
        template_dir='fabfile/centos/templates/sysstat',
        use_sudo=True,
        backup=False,
        mode=0644)
