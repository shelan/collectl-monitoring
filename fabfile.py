import os
import time
from fabric import contrib
from fabric.api import *

download_folder = '/Users/shelan/projects/karamel/karamel-stats/'

env.hosts = ['172.28.128.7']

env.user = "vagrant"


# def update():
#     with cd("/srv/django/myapp"):
#         run("git pull")


def setup():
    sudo("apt-get install collectl -y")
    # sudo("service collectl start -p")
    # time.sleep(5)
    # sudo("service collectl stop")
    sudo("sed -i '/DaemonCommands =/c\DaemonCommands =-P -f /var/log/collectl' /etc/collectl.conf")


def start():
    with warn_only():
        sudo("rm -rf /var/log/collectl/*")
    sudo("service collectl start")


def stop():
    sudo("/etc/init.d/collectl flush")
    sudo("service collectl stop")


def reload():
    sudo("service apache2 reload")


def collect():
    with cd("/var/log/collectl"):
        with warn_only():
            sudo("rm -rf *.tab")
            sudo("find . -name '*.gz'| xargs gzip -d")
    if not os.path.exists(download_folder + env.host):
        os.mkdir(download_folder + env.host)
    get("/var/log/collectl/*.tab", download_folder + env.host)


