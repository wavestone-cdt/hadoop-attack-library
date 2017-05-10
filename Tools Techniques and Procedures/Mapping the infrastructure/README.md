Mapping the infrastructure
==========================

Description
-----------
Etablishing a precise map of the target infrastructure is **crucial** as Hadoop environments expose **a lot of services**.
The main goal is to get to know:
* Which server holds which role: datanode, namenode and edgenode  
* Which technologies and which third-party modules are deployed: for instance Apache HBase, Apache Hive, Apache Spark, Apache Kafka, Cloudera HUE, Apache Ranger, etc.
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
**No NSE specific script specification is needed for these, as they are bundled in the [**`nselib/data/http-fingerprints.lua`**](https://github.com/nmap/nmap/blob/master/nselib/data/http-fingerprints.lua) script.  
  
Some additional NSE scripts exists in order to find some information on:
* **MapReduce v1**: hadoop-datanode-info.nse, hadoop-jobtracker-info.nse, hadoop-namenode-info.nse, hadoop-tasktracker-info.nse, hadoop-secondary-namenode-info.nse  
* **HBase**: hbase-region-info.nse, hbase-master-info.nse  
* **Flume**: flume-master-info.nse  