Getting the target environment configuration
============================================

Description
-----------
Several **cluster parameters** have to be configured in different files on the client-side to be able to interact with an Hadoop cluster.  
These parameters can be retrieved from the **multiple Web interfaces on Hadoop components** and have to be placed accordingly in the **following files**:

#### `core-site.xml`  

Parameter name | Parameter value | Parameter example
-------------- | --------------- | -----------------
`fs.defaultFS` | The IP of the NameNode, used for filesystem metadata interaction| `hdfs://1.2.3.4:8020`
  
  
#### `hdfs-site.xml`

Parameter name | Parameter value | Parameter example
-------------- | --------------- | -----------------
`dfs.datanode.address` | The IP of the DataNode, used for file transfer| `hdfs://1.2.3.4:8020`
`dfs.client.use.datanode.hostname` | `true or false` depending of the cluster architecture (multihomed vs monohomed), it is used to specify if HDFS clients should use hostnames instead of IPs to connect to DataNodes. In most of the case, it should be set to `true` | `true`
  
  
#### `yarn-site.xml`  

Parameter name | Parameter value | Parameter example
-------------- | --------------- | -----------------
`yarn.resourcemanager.hostname` | The hostname of the ResourceManager, used to execute jobs | `foobar.example.com`
`yarn.resourcemanager.address` | The IP and port of the Resource Manager | `${yarn.resourcemanager.hostname}:8050`
`yarn.application.classpath` | The classpath of the Resource Manager, to be included when executing jobs | `$HADOOP_CONF_DIR,/usr/hdp/current/hadoop-client/*,/usr/hdp/current/hadoop-client/lib/*,/usr/hdp/current/hadoop-hdfs-client/*,/usr/hdp/current/hadoop-hdfs-client/lib/*,/usr/hdp/current/hadoop-yarn-client/*,/usr/hdp/current/hadoop-yarn-client/lib/*`
  
  
#### `mapred-site.xml`  

Parameter name | Parameter value | Parameter example
-------------- | --------------- | -----------------
`mapreduce.framework.name` | The runtime framework for executing MapReduce jobs. Can be one of `local`, `classic` or `yarn` but it should be `yarn` | `yarn`
`mapreduce.jobhistory.address` | The IP and port of the JobHistory server, used to track jobs | `foobar.example.com:10020`
`mapreduce.application.classpath` | The classpath of MapReduce, to be included when executing jobs | `$PWD/mr-framework/hadoop/share/hadoop/mapreduce/*:$PWD/mr-framework/hadoop/share/hadoop/mapreduce/lib/*:$PWD/mr-framework/hadoop/share/hadoop/common/*:$PWD/mr-framework/hadoop/share/hadoop/common/lib/*:$PWD/mr-framework/hadoop/share/hadoop/yarn/*:$PWD/mr-framework/hadoop/share/hadoop/yarn/lib/*:$PWD/mr-framework/hadoop/share/hadoop/hdfs/*:$PWD/mr-framework/hadoop/share/hadoop/hdfs/lib/*:$PWD/mr-framework/hadoop/share/hadoop/tools/lib/*:/usr/hdp/${hdp.version}/hadoop/lib/hadoop-lzo-0.6.0.${hdp.version}.jar:/etc/hadoop/conf/secure`
`mapreduce.application.framework.path` | The path of a custom job framework, notably used in HortonWorks clusters | `/hdp/apps/${hdp.version}/mapreduce/mapreduce.tar.gz#mr-framework`
  
  
Where to place these configuration files ?
------------------------------------------
By default they have to be placed in the following local folder on the attacker environment 
```
<hadoop_installation>/etc/hadoop
```
  
If you followed the [`Setting up an Hadoop attack environment` tutorial](../Setting%20up%20an%20Hadoop%20attack%20environment), it then should be placed in 
```
/opt/hadoop-2.7.3/etc/hadoop
```  
You can also use a custom folder and specify the path to it in an Hadoop command with the `--config` option:
```
$ hadoop -h
Usage: hadoop [--config confdir] [COMMAND | CLASSNAME]
```  
  
  
Where to get the parameter values ?
-----------------------------------
The cluster configuration can be retrieved on **any WebUI at the `/conf` URI on all native Hadoop components including**:
* **HDFS NameNode WebUI**, on port HTTP/50070 or HTTPS/50470  
* **HDFS DataNode WebUI**, on port HTTP/50075 or HTTPS/50475  
* **Secondary NameNode WebUI**, on port HTTP/50090  
* **YARN ResourceManager WebUI**, on port HTTP/8088 or HTTPS/8090  
* **YARN NodeManager WebUI**, on port HTTP/8042 or HTTPS/8044  
* **MapReduce v2 JobHistory Server WebUI**, on port HTTP/19888 or HTTPS/19890 
* **MapReduce v1 JobTracker WebUI**, on port HTTP/50030  
* **MapReduce v1 TaskTracker WebUI**, on port HTTP/50060  


HadoopSnooper
-------------
`HadoopSnooper` has been developped to allow attackers to **easily retrieve a suitable minimum client-side configuration** using configuration files exposed on Hadoop components' Web interfaces.  
It simply grabs a remote cluster configuration, parse it and generate the appropriate configuration files to be used in the attacker environment.

### Usage
```
$ python hadoopsnooper.py -h
usage: hadoopsnooper.py [-h] --nn NN [--dn DN] [-o OUTPUT_DIR] [--batch] host

    __  __          __                 _____                                  
   / / / /___ _____/ /___  ____  ____ / ___/____  ____  ____  ____  ___  _____
  / /_/ / __ `/ __  / __ \/ __ \/ __ \__ \/ __ \/ __ \/ __ \/ __ \/ _ \/ ___/
 / __  / /_/ / /_/ / /_/ / /_/ / /_/ /__/ / / / / /_/ / /_/ / /_/ /  __/ /    
/_/ /_/\__,_/\__,_/\____/\____/ .___/____/_/ /_/\____/\____/ .___/\___/_/     
                             /_/                          /_/                 
    

positional arguments:
  host                  host

optional arguments:
  -h, --help            show this help message and exit
  --nn NN               Cluster namenode (format: hdfs://namenode.hadoop:8020)
  --dn DN               Cluster datanodes addresses
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory
  --batch               Never ask for user input, use the default behaviour
```

### Dependencies
* Python 2
* `requests` and `lxml` modules: `$ pip install requests lxml`