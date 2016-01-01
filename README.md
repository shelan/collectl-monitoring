# collectl-monitoring
This project will monitor a cluster using collectl and provide a report when required

## Demo
You can view a sample report [here](http://shelan.org/collectl-monitoring/sample/report_cpu.html).


### installing required packages
1. Install python
2. Install python PIP 
3. git clone the collectl-monitoring (this) repository.
4. change directory to the root of the cloned repository. Lets call this folder as *SOURCE_ROOT*
5. install required python packages.
    ``` pip install -r requirments.txt```

### Configuration file

change the *SOURCE_ROOT*/conf/config.ini file for your deployment servers.

```
[env]
# Remote hosts
hosts=172.28.128.5,172.28.128.6
# user to log into remote host
user=vagrant

[log]
# download folder to download colllectl logs from remote hots
download_folder=/Users/shelan/projects/karamel/karamel-stats/
```

### How to use to collect data from servers

 This uses **python fabric** to cordinate deployment across servers.
 
 navigate to *SOURCE_ROOT*
 
 and you can use fabric commands to peform following actions
 
 * ``` setup``` - To setup Collectl in remote servers
 * ```start``` - To start Collectl as a service in remote servers
 * ```stop ```- To stop the Collectl service in remote servers
    
 You may issue fabric tasks as following. For an example if you need to setup collectl in remote servers.
    
  ``` fab setup -i <path to ssh key> ```
  or
  ``` fab setup -p <password of the ssh user>```
    
 * ```collect:folder=<Folder>,test=<Name of test> ```This will collect logs from remote servers
    
 

 
 
 
