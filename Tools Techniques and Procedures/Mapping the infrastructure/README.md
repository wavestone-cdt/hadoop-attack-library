Mapping the infrastructure
==========================

Description
-----------
Etablishing a precise map of the target infrastructure is **crucial** as Hadoop environments expose **a lot of services**.
The main goal is to get to know:
* Which server holds which **role**: datanode, namenode and edgenode  
* Which **technologies and which third-party modules** are deployed: for instance Apache HBase, Apache Hive, Apache Spark, Apache Kafka, Cloudera HUE, Apache Ranger, etc.
  * A lot of modules along with their purpose are reported on [The Hadoop Ecosystem Table](https://hadoopecosystemtable.github.io/)
  
A good way to easily map the infrastructure is to find the WebUI:
* **HDFS NameNode WebUI**, on port HTTP/50070 or HTTPS/50470  
* **HDFS DataNode WebUI**, on port HTTP/50075 or HTTPS/50475  
* **Secondary NameNode WebUI**, on port HTTP/50090  
* **YARN ResourceManager WebUI**, on port HTTP/8088 or HTTPS/8090  
* **YARN NodeManager WebUI**, on port HTTP/8042 or HTTPS/8044  
* **MapReduce v2 JobHistory Server WebUI**, on port HTTP/19888 or HTTPS/19890  
* **MapReduce v1 JobTracker WebUI**, on port HTTP/50030  
* **MapReduce v1 TaskTracker WebUI**, on port HTTP/50060  
  
Full listings of ports used in the main Hadoop distributions are here below:
* [Hortonworks](https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.4.0/bk_HDP_Reference_Guide/content/reference_chap2.html)  
* [Cloudera](https://www.cloudera.com/documentation/enterprise/5-5-x/topics/cdh_ig_ports_cdh5.html)  
* [MapR](http://doc.mapr.com/display/MapR/Ports+Used+by+MapR)  
  
Nmap scripts
------------
Nmap from version 7.41 integrate some probes to find and recognize multiple WebUIs among: 
* **Apache Ambari**  
* **Apache Oozie**  
* **Apache Ranger**  
* **Cloudera HUE**  
* **Cloudera Manager**  
* **Hadoop MapReduce v2**  
* **Hadoop YARN**  
  
The probes are in [**`nselib/data/http-fingerprints.lua`**](https://github.com/nmap/nmap/blob/master/nselib/data/http-fingerprints.lua) database, used by the [http-enum](https://nmap.org/nsedoc/scripts/http-enum.html) module.  
Here below is an extract of a nmap port scan result against an HDP Sandbox:
```
$ nmap -sV --script=http-enum -p- 192.168.11.150

PORT      STATE SERVICE         REASON         VERSION
6080/tcp  open  http            syn-ack ttl 64 Apache Tomcat/Coyote JSP engine 1.1
| http-enum: 
|   /login.jsp: Possible admin folder
|   /login.jsp: Login page
|_  /login.jsp: Apache Ranger WebUI
|_http-server-header: Apache-Coyote/1.1

8042/tcp  open  http            syn-ack ttl 64 Jetty 6.1.26.hwx
| http-enum: 
|   /logs/: Logs
|_  /node: Hadoop YARN Node Manager version 2.7.1.2.4.0.0-169, Hadoop version 2.7.1.2.4.0.0-169
|_http-server-header: Jetty(6.1.26.hwx)

8080/tcp  open  http            syn-ack ttl 64 Jetty 8.1.17.v20150415
| http-enum: 
|_  /: Apache Ambari WebUI
|_http-server-header: Jetty(8.1.17.v20150415)

8088/tcp  open  http            syn-ack ttl 64 Jetty 6.1.26.hwx
| http-enum: 
|   /logs/: Logs
|_  /cluster/cluster: Hadoop YARN Resource Manager version 2.7.1.2.4.0.0-169, state "started", Hadoop version 2.7.1.2.4.0.0-169
|_http-server-header: Jetty(6.1.26.hwx)

19888/tcp open  http            syn-ack ttl 64 Jetty 6.1.26.hwx
| http-enum: 
|   /logs/: Logs
|_  /jobhistory: Hadoop MapReduce JobHistory WebUI
|_http-server-header: Jetty(6.1.26.hwx)
```  
It has to be noted that:
* The `-sV` nmap option is needed to correctly identify Web servers. For instance, the Hadoop JobHistory WebUI is not recognized as a Web server without `-sV`.  
* The probes are currently inefficient against Kerberized clusters are authentication is needed to access WebUIs.  
  
Some additional NSE scripts exists in order to find some information on:
* **MapReduce v1**: hadoop-datanode-info.nse, hadoop-jobtracker-info.nse, hadoop-namenode-info.nse, hadoop-tasktracker-info.nse, hadoop-secondary-namenode-info.nse  
* **HBase**: hbase-region-info.nse, hbase-master-info.nse  
* **Flume**: flume-master-info.nse  