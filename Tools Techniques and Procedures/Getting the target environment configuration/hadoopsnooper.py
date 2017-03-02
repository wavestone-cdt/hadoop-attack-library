#!/usr/bin/env python
import sys, os
import requests
import re
from lxml import etree
import argparse
from StringIO import StringIO

CONF_DIR = "./hadoopsnooper"
tab = [8042, 8088, 8480, 19888, 50070]

# Create XML file with key, value dictionnary 
def create_file_with_attributes(filename, attributes):
    tree = etree.Element("configuration")
    for key, v in attributes.iteritems():
        prop = etree.SubElement(tree, "property")
        name = etree.SubElement(prop, "name")
        value = etree.SubElement(prop,"value")
        name.text, value.text = key, v
    with open(CONF_DIR + filename, 'w') as f:
        f.write(etree.tostring(tree, pretty_print=True))
    
# Build hdfs-site.xml file
def create_hdfs_site(datanode = None):
    filename = "hdfs-site.xml"
    attributes = { 
            "dfs.datanode.address": datanode,
            "dfs.client.use.datanode.hostname":  "true"
            }
    create_file_with_attributes(filename, attributes)
    print "[+] %s successfully created" % filename

# Build core-site.xml file
def create_core_site(namenode = None):
    filename = "core-site.xml"
    if namenode:
        attributes = { "fs.defaultFS":  namenode }
    else:
        attributes = { "fs.defaultFS": "random.hadoop" }
    create_file_with_attributes(filename, attributes)
    print "[+] %s successfully created" % filename

# Build yarn-site.xml file
def create_yarn_site(conf):
    filename = "yarn-site.xml"
    attributes = {}
    configuration = etree.parse(conf)

    # yarn.resourcemanager.address attribute
    tmp_property = configuration.xpath("/configuration/property[name='yarn.resourcemanager.address']/value")
    attributes["yarn.resourcemanager.address"] = parse_attribute(tmp_property[0].text, configuration)

    tmp_property = configuration.xpath("/configuration/property[name='yarn.application.classpath']/value")
    attributes["yarn.application.classpath"] = parse_attribute(tmp_property[0].text, configuration)

    create_file_with_attributes(filename, attributes)
    print "[+] %s successfully created" % filename

# Build mapred-site.xml file
def create_mapred_site(conf):
    filename = "mapred-site.xml"
    attributes = { "mapreduce.framework.name" : "yarn" }
    configuration = etree.parse(conf)

    # mapreduce.jobhistory.address attribute
    tmp_property = configuration.xpath("/configuration/property[name='mapreduce.jobhistory.address']/value")
    attributes["mapreduce.jobhistory.address"] = tmp_property[0].text

    create_file_with_attributes(filename, attributes)
    print "[+] %s successfully created" % filename

# Parsing hadoop configuration
def parse_attribute(attr, configuration):
    if re.search("\$\{.*\}", attr):
        tmp_attr = re.findall("\$\{(.*)\}", attr)
        tmp_property = configuration.xpath("/configuration/property[name='%s']/value" % tmp_attr[0])
        attr = tmp_property[0].text
    return attr

# Get configuration from Web interfaces
def get_hadoop_conf(host):
    for port in tab:
        try:
            response = requests.get("http://" + host + ":" + str(port) + "/conf")
            if response.ok:
                return StringIO(response.content)
        except Exception:
            pass
    return None

# Main function
def main():
    VERSION = "0.1-dev"
    global CONF_DIR

    parser = argparse.ArgumentParser(description = """

    __  __          __                 _____                                  
   / / / /___ _____/ /___  ____  ____ / ___/____  ____  ____  ____  ___  _____
  / /_/ / __ `/ __  / __ \/ __ \/ __ \\__ \/ __ \/ __ \/ __ \/ __ \/ _ \/ ___/
 / __  / /_/ / /_/ / /_/ / /_/ / /_/ /__/ / / / / /_/ / /_/ / /_/ /  __/ /    
/_/ /_/\__,_/\__,_/\____/\____/ .___/____/_/ /_/\____/\____/ .___/\___/_/     
                             /_/                          /_/                 
    """, 
       prog = "hadoopsnooper.py",
       formatter_class = argparse.RawTextHelpFormatter)

    # Positionnal argument
    parser.add_argument("host", action = "store", help = "host")

    # Optionnal arguments
    parser.add_argument("--nn", type = str, default = None, action = "store", help = "Cluster namenode")
    parser.add_argument("--dn", type = str, default = None, action = "store", help = "Cluster datanodes addresses")
    parser.add_argument("-o", "--output-dir", type = str, default = "hadoopsnooper/", action = "store", help = "Output directory")
    parser.add_argument("--batch", default = False, action = "store_true", help = "Never ask for user input, use the default behaviour")

    if len(sys.argv) == 1:
        print "[!] Missing host ... Exiting !"
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args()
        host = args.host
        CONF_DIR = args.output_dir + "/"
        namenode = args.nn
        datanode = args.dn
        batch_mode = args.batch

    if not os.path.isdir(CONF_DIR):
        message = "Specified destination path does not exist, do you want to create it ? [y/N]"
        if not batch_mode: 
            doCreate = raw_input(message).upper()
        else:
            doCreate = 'N'
            print(message)

        if doCreate == 'Y':
            print "[+] Creating configuration directory"
            os.makedirs(CONF_DIR)
        else:
            print "[!] Directory not created ... Exiting"
            sys.exit(1)

    files =  map(lambda x : CONF_DIR + x, [ "core-site.xml", "hdfs-site.xml", "mapred-site.xml", "yarn-site.xml" ])
    if any(map(os.path.isfile, files)):
        message = "Destination directory already contains configuration files, do you want to continue (all existing files will be deleted) ? [Y/n]"
        if not batch_mode: 
            doDelete = raw_input(message).upper()
        else:
            doDelete = "Y"
            print(message)

        if doDelete == 'Y': 
            for f in files: 
                if os.path.isfile(f): os.remove(f)
        else:
            print "[!] Files not deleted ... Exiting"

    conf = get_hadoop_conf(host)
    if conf:
        # Generating core-site.xml
        create_core_site(namenode)
    
        # Generating core-site.xml
        create_mapred_site(conf)
    
        # Generating core-site.xml
        create_yarn_site(conf)

        if datanode:
            create_hdfs_site(datanode)
    else:
        print "[-] No configuration found ... Exiting"

if __name__ == "__main__":
    main()
