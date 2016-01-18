# collectl-monitoring

![alt text](https://github.com/shelan/collectl-monitoring/blob/master/img/screenshot.png "Screenshot")

This project will monitor a cluster using collectl and provide a report for the collected data. This tool can be used for performance tests. This supports a typical workflow of start monitoring, stop monitoring and plotting collected results.

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
--------------------------------------------

At present this tool can be used to draw the graphs after collecting data.


 This uses **python fabric** to cordinate deployment across servers.
 
 navigate to *SOURCE_ROOT*
 
 and you can use fabric commands to peform following actions
 
 * ```setup``` - To setup Collectl in remote servers
 * ```start``` - To start Collectl as a service in remote servers
 * ```stop ```- To stop the Collectl service in remote servers
    
 You may issue fabric tasks as following. For an example if you need to setup collectl in remote servers.
    
  ``` fab setup -i <path to ssh key> ```
  or
  ``` fab setup -p <password of the ssh user>```
    
 * ``` collect:folder=<Folder>,test=<Name of test> ```This will collect logs from remote servers
 
 ### How to Structure your collectl logs 
 -----------------------------------------
  When you download your logs from the fab command ```collect:folder=<$folder>,test=<$name_of_test>```,
  
  * firstly it will create a folder, (If it does not exist) for the $folder name you given in the command.
  
  * Then all the files from remote servers will be downloaded into that *folder* appending the ip address and $name_of_test
  that you have given in the command.
 
### Example scenario
------------------------------------------
    
Let's imagine that you needed to run an experiment to measure system level performance for Apache Spark and Apache Flink in Following    machines.
    
``` 52.12.10.123 , 54.214.91.253 , 54.218.138.101 ```
    
First you need to setup as mentioned in the above [section] (https://github.com/shelan/collectl-monitoring#how-to-use-to-collect-data-from-servers)
     to install collectl in the machines.
    
After that,
    
* Just before you run your experiment issue the command
    
    
``` fab start -i <path to ssh key of you remoter server's ssh user> ``` ( alternatively you may give -p <password of remote user>)
    
* After finishing your experiment
    
``` fab stop -i <path to ssh key of you remoter server's ssh user> ``` ( alternatively you may give -p <password of remote user>)
     
     
Lets say you ran this experiment for Apache Flink and you need to name the collected files as below in a folder called terasort-600
     
52.12.10.123-flink , 54.214.91.253-flink , 54.218.138.101-flink
     
If you issue the following command,
     
fab collect:folder=teragen-600,test=flink it will collect the files in to a folder named terasort-600.
    
You might redo the same thing with Apache Spark performance test and below you can see a sample directory structure after you collect both Spark and Flink data.
    
    ```
    terasort-600/
    ├── 52.12.10.123-flink
    ├── 52.12.10.123-spark
    ├── 54.214.91.253-flink
    ├── 54.214.91.253-spark
    ├── 54.218.138.101-flink
    └── 54.218.138.101-spark
    
    ```
  
    

 
 
 
