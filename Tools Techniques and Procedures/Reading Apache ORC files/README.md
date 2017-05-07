Reading Apache ORC files
============================

Description
-----------
Apache ORC is, like Apache Parquet, a storage format widely used in Big Data environments.  
As an attacker, you might be facing this format after getting access to the datalake.  
Four options to be able to read this format:
* Use [`hive --orcfiledump`](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+ORC#LanguageManualORC-ORCFileDumpUtility): a working Hive environment is needed to run the utility  
* Use `orc-tools` standalone **uber jar**: **no external jar will be required** as they are packaged into the build
  * Compile it [yourself](https://github.com/apache/orc/tree/master/java/tools): `mvn clean compile assembly:single`  
  * or grab the latest `orc-tools-<version>-uber.jar` [here](https://repo1.maven.org/maven2/org/apache/orc/orc-tools/) 
  * or use the one provided here, currently `orc-tools-1.3.3-uber.jar`  
  
  
Usage
-----
The application consists of the following commands:
* `meta`, to read metadata
* `data`, to print data
* `scan`  

More options can be found [here](https://orc.apache.org/docs/tools.html#java-orc-tools) for future versions
```
$ java -jar orc-tools-1.3.3-uber.jar --help
ORC Java Tools

usage: java -jar orc-tools-*.jar [--help] [--define X=Y] <command> <args>

Commands:
   meta - print the metadata about the ORC file
   data - print the data from the ORC file
   scan - scan the ORC file

To get more help, provide -h to the command
```

Example with the [TestOrcFile.test1.orc](https://github.com/apache/orc/blob/master/examples/TestOrcFile.test1.orc) file
-----------------------------------------------------------------------------------------------------------------------
```
$ java -jar orc-tools-1.3.3-uber.jar data TestOrcFile.test1.orc
log4j:WARN No appenders could be found for logger (org.apache.hadoop.metrics2.lib.MutableMetricsFactory).
log4j:WARN Please initialize the log4j system properly.
log4j:WARN See http://logging.apache.org/log4j/1.2/faq.html#noconfig for more info.
Processing data file TestOrcFile.test1.orc [length: 1711]
{"boolean1":false,"byte1":1,"short1":1024,"int1":65536,"long1":9223372036854775807,"float1":1,"double1":-15,"bytes1":[0,1,2,3,4],"string1":"hi","middle":{"list":[{"int1":1,"string1":"bye"},{"int1":2,"string1":"sigh"}]},"list":[{"int1":3,"string1":"good"},{"int1":4,"string1":"bad"}],"map":[]}
{"boolean1":true,"byte1":100,"short1":2048,"int1":65536,"long1":9223372036854775807,"float1":2,"double1":-5,"bytes1":[],"string1":"bye","middle":{"list":[{"int1":1,"string1":"bye"},{"int1":2,"string1":"sigh"}]},"list":[{"int1":100000000,"string1":"cat"},{"int1":-100000,"string1":"in"},{"int1":1234,"string1":"hat"}],"map":[{"_key":"chani","_value":{"int1":5,"string1":"chani"}},{"_key":"mauddib","_value":{"int1":1,"string1":"mauddib"}}]}
```
