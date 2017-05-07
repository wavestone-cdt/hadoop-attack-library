Reading Apache Parquet files
============================

Description
-----------
Apache Parquet is a storage format widely used in Big Data environments.  
As an attacker, you might be facing this format after getting access to the datalake.  
Two options to be able to read this format:
* Compile the `parquet-tools` utility to be used in the **`hadoop`** mode: a working Hadoop environment is needed to run the utility as **all Hadoop jars are required in the classpath**
* Compile the `parquet-tools` utility to in the **`local`** standalone mode: **no external Hadoop jar will be required** as they are packaged into the build  
For each of these options, guidelines are provided in [the project](https://github.com/apache/parquet-mr/tree/master/parquet-tools)

**The quicker option is to use our pre-compiled version of `parquet-tools` in `local` mode, currently [`parquet-tools-1.8.1.jar`](parquet-tools-1.8.1.jar)**

Usage
-----
The application consists of the following commands:
* `cat`, to display the parquet file. Use the `--json` option to have a prettier output
* `head`
* `schema`, to read the schema
* `meta`
* `dump`
```
$ java -jar parquet-tools-1.8.1.jar -h
usage: parquet-tools cat [option...] <input>
where option is one of:
       --debug     Enable debug output
    -h,--help      Show this help string
    -j,--json      Show records in JSON format.
       --no-color  Disable color output even if supported
where <input> is the parquet file to print to stdout

usage: parquet-tools head [option...] <input>
where option is one of:
       --debug          Enable debug output
    -h,--help           Show this help string
    -n,--records <arg>  The number of records to show (default: 5)
       --no-color       Disable color output even if supported
where <input> is the parquet file to print to stdout

usage: parquet-tools schema [option...] <input>
where option is one of:
    -d,--detailed  Show detailed information about the schema.
       --debug     Enable debug output
    -h,--help      Show this help string
       --no-color  Disable color output even if supported
where <input> is the parquet file containing the schema to show

usage: parquet-tools meta [option...] <input>
where option is one of:
       --debug     Enable debug output
    -h,--help      Show this help string
       --no-color  Disable color output even if supported
where <input> is the parquet file to print to stdout

usage: parquet-tools dump [option...] <input>
where option is one of:
    -c,--column <arg>  Dump only the given column, can be specified more than
                       once
    -d,--disable-data  Do not dump column data
       --debug         Enable debug output
    -h,--help          Show this help string
    -m,--disable-meta  Do not dump row group and page metadata
       --no-color      Disable color output even if supported
where <input> is the parquet file to print to stdout
```
