Setting up an Hadoop attack environment
=======================================

Description
-----------
This tutorial explains how to set up a working environment in order to perform attacks from the **Hadoop client CLI** such as:
* [Browsing the HDFS datalake](../Browsing the HDFS datalake)
* [Remote executing commands](../Executing remote commands)  

This tutorial is valid for a Linux environment and has been tested on Kali.

1. Download the latest [Hadoop binary release](http://hadoop.apache.org/releases.html)
    ```
    $ cd /opt && wget http://apache.mirrors.ovh.net/ftp.apache.org/dist/hadoop/common/hadoop-2.7.3/hadoop-2.7.3.tar.gz
    ```  

2. Decompress the archive
    ```
    $ tar xvf hadoop-2.7.3.tar.gz
    ```

3. Set, if not already done, the `JAVA_HOME` environment variable (use `$ update-alternatives --config java` to find your Java path)
    ```
    $ export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-i386
    ```

4. (Optional) Add the Hadoop `bin` path to the `PATH` environment variable
    ```
    $ export PATH=$PATH:/opt/hadoop-2.7.3/bin
    ```

5. Test that everything is OK
    ```
    $ hadoop version
    ```