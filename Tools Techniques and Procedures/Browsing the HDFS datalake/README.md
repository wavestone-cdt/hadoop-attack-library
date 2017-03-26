Browsing the HDFS datalake
==========================

Description
-----------
There are 2 different and distinct approaches to browse the HDFS datalake:  
A. Through the [WebHDFS API](#webhdfs)  
B. Through the [native Hadoop CLI](#hadoop-cli)  
  
  
-------
WebHDFS
-------
**WebHDFS offers REST API** for users to access data on the HDFS filesystem using the HTTP protocol. The activation of this feature is configured on the cluster side through the following directive in the `hdfs-site.xml` file:
```
dfs.webhdfs.enabled: true|false     Enable WebHDFS (REST API) in Namenodes and Datanodes.
```

**The API allows to perform all [possible actions](http://hadoop.apache.org/docs/r2.7.2/hadoop-project-dist/hadoop-hdfs/WebHDFS.html) on the HDFS filesystem (view, create, modify, etc.).**  

By default, if Kerberos authentication is not enabled, no credential is needed to request these services: **only user identification is needed using the `user.name` parameter**.  
WebHDFS API are exposed on the following services:
* DataNode HDFS DataNode WebUI on **port 50075**
* Third-party HttpFS module on **port 14000**  

Another possible method to list the content is to call the [`/listPaths/` URI on a NameNode WebUI on port 50070](https://blog.cloudera.com/blog/2009/08/hadoop-default-ports-quick-reference/) which returns an XML file.  

HDFSBrowser
-----------
`HDFSBrowser` has been developed to allow attackers to easily browse the HDFS filesystem using WebHDFS and HttpFS services. `HDFSBrowser` is able to handle the different known methods. 

### Usage
```
$ python hdfsbrowser.py  -h
usage: hdfsbrowser.py [-h] [--port PORT] [-o OUTPUT_FILE] [--ssl]
                       [--target-uri TARGET_URI] [-r] [--root-path ROOT_PATH]
                       [-m {all,whdfs,httpfs}] [--time-out TIME_OUT]
                       [-d DEPTH] [--threads THREADS] [--proxy PROXY]
                       [--header HEADER]
                       host

 
     _   _____________ ___________                                 
    | | | |  _  \  ___/  ___| ___ \                                
    | |_| | | | | |_  \ `--.| |_/ /_ __ _____      _____  ___ _ __ 
    |  _  | | | |  _|  `--. \ ___ \ '__/ _ \ \ /\ / / __|/ _ \ '__|
    | | | | |/ /| |   /\__/ / |_/ / | | (_) \ V  V /\__ \  __/ |   
    \_| |_/___/ \_|   \____/\____/|_|  \___/ \_/\_/ |___/\___|_|  

    

positional arguments:
  host                  host

optional arguments:
  -h, --help            show this help message and exit
  --port PORT           HDFS port
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Write to file instead of stdout
  --ssl                 Try SSL/TLS
  --target-uri TARGET_URI
                        Target URI of the Hadoop installation
  -r, --recursive       Be recursive
  --root-path ROOT_PATH
                        Root path for the directory listing
  -m {all,whdfs,httpfs}, --method {all,whdfs,httpfs}
                        Method to use [
  --time-out TIME_OUT   Timeout for request
  -d DEPTH, --depth DEPTH
                        Recursion depth while listing directories
  --threads THREADS     Number of threads
  --proxy PROXY         Use proxy on given port
  --header HEADER       Pass custom header to server
```

### Dependencies
* Python 2
* `requests` and `lxml` modules: `$ pip install requests lxml`
  
----------
Hadoop CLI
----------
Browsing the HDFS datalake can also be achieved with the **native Hadoop CLI client** after validating the following prerequisites:  
* [Setting up an Hadoop attack environment](../Setting%20up%20an%20Hadoop%20attack%20environment)  
* [Getting the target environment configuration](../Getting%20the%20target%20environment%20configuration)  
  
Then, the `$ hadoop fs` command should be used, for instance:
* `$ hadoop fs -ls /` to list the content of the root path
* `$ hadoop fs -put <local_file> <remote_file>` to upload a local file on HDFS 
* `$ hadoop fs -get <remote_file> <local_file>` to download a remote file

If Kerberos authentication is not enabled, it is **possible to choose the desired user** by using the following environment variable:
```
$ HADOOP_USER_NAME=<username>
```
Using the `hdfs` user is relevant as it has maximum privileges over the HDFS datalake:
```
$ export HADOOP_USER_NAME=hdfs
```

Take a look at the `hadoop fs` usage and [documentation](https://hadoop.apache.org/docs/r2.7.2/hadoop-project-dist/hadoop-common/FileSystemShell.html) for complementary information:
```
$ hadoop fs
Usage: hadoop fs [generic options]
	[-appendToFile <localsrc> ... <dst>]
	[-cat [-ignoreCrc] <src> ...]
	[-checksum <src> ...]
	[-chgrp [-R] GROUP PATH...]
	[-chmod [-R] <MODE[,MODE]... | OCTALMODE> PATH...]
	[-chown [-R] [OWNER][:[GROUP]] PATH...]
	[-copyFromLocal [-f] [-p] [-l] <localsrc> ... <dst>]
	[-copyToLocal [-p] [-ignoreCrc] [-crc] <src> ... <localdst>]
	[-count [-q] [-h] <path> ...]
	[-cp [-f] [-p | -p[topax]] <src> ... <dst>]
	[-createSnapshot <snapshotDir> [<snapshotName>]]
	[-deleteSnapshot <snapshotDir> <snapshotName>]
	[-df [-h] [<path> ...]]
	[-du [-s] [-h] <path> ...]
	[-expunge]
	[-find <path> ... <expression> ...]
	[-get [-p] [-ignoreCrc] [-crc] <src> ... <localdst>]
	[-getfacl [-R] <path>]
	[-getfattr [-R] {-n name | -d} [-e en] <path>]
	[-getmerge [-nl] <src> <localdst>]
	[-help [cmd ...]]
	[-ls [-d] [-h] [-R] [<path> ...]]
	[-mkdir [-p] <path> ...]
	[-moveFromLocal <localsrc> ... <dst>]
	[-moveToLocal <src> <localdst>]
	[-mv <src> ... <dst>]
	[-put [-f] [-p] [-l] <localsrc> ... <dst>]
	[-renameSnapshot <snapshotDir> <oldName> <newName>]
	[-rm [-f] [-r|-R] [-skipTrash] <src> ...]
	[-rmdir [--ignore-fail-on-non-empty] <dir> ...]
	[-setfacl [-R] [{-b|-k} {-m|-x <acl_spec>} <path>]|[--set <acl_spec> <path>]]
	[-setfattr {-n name [-v value] | -x name} <path>]
	[-setrep [-R] [-w] <rep> <path> ...]
	[-stat [format] <path> ...]
	[-tail [-f] <file>]
	[-test -[defsz] <path>]
	[-text [-ignoreCrc] <src> ...]
	[-touchz <path> ...]
	[-truncate [-w] <length> <path> ...]
	[-usage [cmd ...]]

Generic options supported are
-conf <configuration file>     specify an application configuration file
-D <property=value>            use value for given property
-fs <local|namenode:port>      specify a namenode
-jt <local|resourcemanager:port>    specify a ResourceManager
-files <comma separated list of files>    specify comma separated files to be copied to the map reduce cluster
-libjars <comma separated list of jars>    specify comma separated jar files to include in the classpath.
-archives <comma separated list of archives>    specify comma separated archives to be unarchived on the compute machines.

The general command line syntax is
bin/hadoop command [genericOptions] [commandOptions]
```