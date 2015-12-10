import os
import time
from fabric import contrib
from fabric.api import *

download_folder = '/Users/ashansa/HS/3rdSem/mini_project/experiments-karamel/collectl-monitoring/results/1/'

env.hosts = ['46.137.66.236','54.74.232.120','54.195.65.147']

env.user = "ubuntu"


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
            #sudo("find . -name '*.gz'| xargs gzip -d")
    if not os.path.exists(download_folder + env.host):
        os.mkdir(download_folder + env.host)
    get("/var/log/collectl/*.tab.gz", download_folder + env.host)

    os.chdir(download_folder + env.host)
    os.system("find . -name '*.gz'| xargs gzip -d")


