import os

import time
from fabric.api import *
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

env.hosts = [x.strip() for x in parser.get('env', 'hosts').split(",")]
env.user = parser.get('env', 'user')

download_folder = parser.get('log', 'download_folder')


def status():
    print env.hosts
    print env.user
    print download_folder


def setup():
    sudo("apt-get install collectl -y")
    sudo("sed -i '/DaemonCommands =/c\DaemonCommands =-P -f /var/log/collectl' /etc/collectl.conf")
    start()
    time.sleep(3)
    stop()
    print "Finished setting up collectl"


def start():
    with warn_only():
        sudo("rm -rf /var/log/collectl/*")
    sudo("service collectl start")
    print "started collectl as a service"


def stop():
    sudo("/etc/init.d/collectl flush")
    sudo("service collectl stop")
    print "stopped collectl"


'''
Graphing and collecting stats
eg: fab collect:folder=mytest,test=spark
'''


def collect(folder="collectl", test="default"):
    global download_folder
    if not download_folder.endswith(os.path.sep):
        download_folder = download_folder + os.path.sep

    if not os.path.exists(download_folder + folder):
        os.makedirs(download_folder + folder)
    get("/var/log/collectl/*.tab.gz", download_folder + folder + os.path.sep + env.host + "-" + test + ".gz")

    os.chdir(download_folder + folder)
    os.system("find . -name '*.gz'| xargs gzip -d")

    print "logs were downloaded to ==> " + os.getcwd()
