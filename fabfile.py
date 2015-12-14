import os
from fabric.api import *
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

# env.hosts = list(parser.get('env', 'hosts'))
# env.user = parser.get('env', 'user')

env.hosts = ['54.203.69.208','54.184.183.17','54.184.146.84']
env.user = 'ubuntu'
download_folder = parser.get('log', 'download_folder')


def status():
    print env.hosts
    print env.user
    print download_folder


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


def collect(folder="collectl",engine="default"):
    # with cd("/var/log/collectl"):
    # with warn_only():
    # sudo("rm -rf *.tab")
    # sudo("find . -name '*.gz'| xargs gzip -d")
    global download_folder
    if not download_folder.endswith(os.path.sep):
        download_folder = download_folder + os.path.sep
    print download_folder

    if not os.path.exists(download_folder + folder):
        os.makedirs(download_folder + folder)
    get("/var/log/collectl/*.tab.gz", download_folder + folder + os.path.sep +env.host+"-"+engine+".gz")

    os.chdir(download_folder + folder)
    os.system("find . -name '*.gz'| xargs gzip -d")
