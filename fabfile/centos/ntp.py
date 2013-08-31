from fabric.api import sudo, task
from fabfile.centos.lib import rpm, service
from fabfile.common.lib import template

NTP_SERVERS = [
    'ntp.nict.jp',
    'ntp.jst.mfeed.ad.jp',
    'ntp.ring.gr.jp'
]

NTP_SERVICE_NAME = 'ntpd'

@task(default=True)
def ensure_setup():
    ensure_package_installed()
    changed = ensure_config_file()
    if service.status(NTP_SERVICE_NAME) == 'stopped':
        run_ntpdate()
        service.start(NTP_SERVICE_NAME)
    elif changed:
        service.restart(NTP_SERVICE_NAME)
    service.ensure_auto_start_enabled(NTP_SERVICE_NAME)

def ensure_package_installed():
    rpm.ensure_installed('ntp')

def ensure_config_file():
    context = {
        'ntp_servers': NTP_SERVERS
    }
    return template.ensure_template(
        'ntp.conf.j2',
        '/etc/ntp.conf',
        context=context,
        template_dir='fabfile/centos/templates/ntp',
        use_sudo=True,
        backup=False,
        mode=0644)

def run_ntpdate():
    sudo('/usr/sbin/ntpdate %s' % NTP_SERVERS[1])
