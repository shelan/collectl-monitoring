import os
from fabric.api import *
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

env.hosts = parser.get('env', 'hosts')
env.user = parser.get('env', 'user')
download_folder = parser.get('log', 'download_folder')


def status():
    print env.hosts
    print env.user


def setup():
    sudo("apt-get install collectl -y")
    sudo("sed -i '/DaemonCommands =/c\DaemonCommands =-P -f /var/log/collectl' /etc/collectl.conf")


def start():
    with warn_only():
        sudo("rm -rf /var/log/collectl/*")
    sudo("service collectl start")


def stop():
    sudo("/etc/init.d/collectl flush")
    sudo("service collectl stop")


def collect(folder="collectl"):
    # with cd("/var/log/collectl"):
    # with warn_only():
    # sudo("rm -rf *.tab")
    # sudo("find . -name '*.gz'| xargs gzip -d")
    global download_folder
    if not download_folder.endswith(os.path.sep):
        download_folder = download_folder + os.path.sep

    if not os.path.exists(download_folder + env.host):
        os.mkdir(download_folder + env.host)
    get("/var/log/collectl/*.tab.gz", download_folder + folder + os.path.sep + env.host)

    os.chdir(download_folder + env.host)
    os.system("find . -name '*.gz'| xargs gzip -d")
