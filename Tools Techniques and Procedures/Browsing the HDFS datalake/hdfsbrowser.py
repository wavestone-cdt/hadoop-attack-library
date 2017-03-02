#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of HDFSBrowser.
#
# Copyright (C) 2016, Mahdi Braik <braik.mahdi at gmail.com>
# All rights reserved.
#
# HDFSBrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HDFSBrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with HDFSBrowser.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import requests
import json
from lxml import etree
from StringIO import StringIO
import logging
import re
import argparse
from multiprocessing import Pool
import time

# Script version
VERSION = '0.1'


# Global vars
API = "/webhdfs/v1"
option = "LISTSTATUS"
HOST = "localhost"
PORT = 50070
HTTP = "http"
HTTPS = "https"

# Logger definition
LOGLEVELS = {0 : 'ERROR', 1 : 'INFO', 2 : 'DEBUG'}
logger_output = logging.StreamHandler(sys.stdout)
logger_output.setFormatter(logging.Formatter('[%(levelname)s][%(name)s] %(message)s'))

logger_gen = logging.getLogger("General")
logger_gen.addHandler(logger_output)

# HDFS's file class definition
class File_HDFS():
    """ 
        Class representation of HDFS file
    """
    def __init__(self, filetype, permission, owner, group, pathSuffix, modificationTime, path):
        self.filetype = filetype
        self.perm = permission
        self.owner = owner
        self.group = group
        self.pathSuffix = pathSuffix
        self.lastModif = modificationTime
        self.path = path
        self.children = []

    def is_directory(self):
        return True if self.filetype == "DIRECTORY" else False

    def print_HDFS(self):
        # t = "d" if self.is_directory() else "-"
        print self.perm + "  " + self.owner + ":" + self.group + "  " + str(self.lastModif) + "  " + self.pathSuffix + "  " + self.path

    def get_url(self):
        return "http://" + HOST + ":" + str(PORT) + API + self.path + "?op=" + option + "&user.name=" + self.owner

    def print_HDFS_csv(self):
        return ";".join([str(self.lastModif), self.filetype, self.perm, self.owner, self.group, self.pathSuffix, self.get_url()]) + "\n"

    def add_child(self, child):
        self.children.append(child)


# Useful functions
f = lambda x : [int(i) for i in bin(x)[2:].zfill(3)]
g = lambda tuplet_list : tuplet_list[0] if tuplet_list[1] else '-'
h = lambda l1, l2 : [t for t in zip(l1,l2)]


def perm_to_str(num):
    """
        Integer to UNIX permission
    """
    s = ['r', 'w', 'x']
    num = [int(i) for i in str(num)]

    if all(map(lambda x : x < 8, num)) and len(num) == 3:
        return "".join(map(lambda x : "".join(map(g, h(s, f(x)))), num))
    else:
        return "--ERROR--"


def parse_hdfs_json(json_string, path):
    #print repr(json_string)
    data_json = json.loads(json_string)
    files_HDFS = []

    for f in data_json['FileStatuses']['FileStatus']:
        tmp_path = path + f["pathSuffix"] + ("/" if f["type"] == "DIRECTORY" else "")
        permission = perm_to_str(int(f["permission"]))
        files_HDFS.append(File_HDFS(f["type"], permission, f["owner"], f["group"], f["pathSuffix"], f["modificationTime"], tmp_path))
    
    return files_HDFS


def parse_hdfs_xml(xml_string):
    tree = etree.parse(StringIO(xml_string))
    files_HDFS = []
    for e in tree.xpath("/listing")[0].getchildren():
        f = { 
                "permission" : None,
                "owner" : None,
                "group" : None,
                "pathSuffix" : None,
                "modified" : None,
                "path" : None
                }
        if e.tag == "directory" or e.tag == "file":
            f["filetype"] = e.tag
    
            for attribut in e.keys():
                f[attribut] = e.get(attribut)

            f["pathSuffix"] = f["path"].split("/")[-1]
            files_HDFS.append(File_HDFS(f["filetype"], f["permission"], f["owner"], f["group"], f["pathSuffix"], f["modified"], f["path"]))
    return files_HDFS


def request_namenode(path, user):
    """
        Request HDFS via HTTP(S) to get file list
           using the REST API : /webhdfs/v1
    """
    op = "op=LISTSTATUS"
    URL = "http://" + HOST + ":" + str(PORT) + API + path + "?" + op + "&user.name=" + user
    #print 'URL %s' % URL
    response = requests.get(URL)
    data = None
    if response.ok: 
        data = response.text
    else: 
        error("Unable to access the following resource : %s" % (URL))
    return data

def request_namenode_multi(file_HDFS):
    return request_namenode(file_HDFS.path, file_HDFS.owner)

def request_namenode_multi2(file_HDFS, q):
    return request_namenode(file_HDFS.path, file_HDFS.owner)


def hdfs_listpaths(user, path, use_recursion, output):
    """
        Request HDFS to get the native list
           using the SOAP API : /listPaths
    """
    rec = "yes" if use_recursion else "no"
    URL = "http://" + HOST + ":" + str(PORT) + "/listPaths" + path + "?recursive=" + rec

    try:
        response = requests.get(URL)
        if response.ok:
            files_HDFS = parse_hdfs_xml(response.content)
            if output:
                with open(output, 'w') as f:
                    for e in files_HDFS: f.write(e.print_HDFS_csv())
                f.close()
            else:
                for e in files_HDFS: e.print_HDFS()
    except:
        #print error("Unable to access the following resource : %s" % (URL))
        print sys.exc_info()
        return False
    return True


def hdfs_ls(path, user, output):
    json_string = request_namenode(path, user)
    t = []
    if json_string:
        files_HDFS = parse_hdfs_json(json_string, path)
        jobs = []
        for e in files_HDFS:
            #e.print_HDFS()
            if e.is_directory(): 
                p = Process(target=hdfs_ls, args=(e.path, e.owner, output))

                for child in hdfs_ls(e.path, e.owner, output):
                    e.add_child(child)
    return files_HDFS


def init_ls(path, user, port, depth, output):
    json_string = request_namenode(path, user)
    files_HDFS = parse_hdfs_json(json_string, path)
    if depth:
        hdfs_ls_multi(files_HDFS, depth - 1)
    return files_HDFS


def hdfs_ls_multi(files_HDFS, depth):
    p = Pool(10)
    #t_deb = time.time()
    json_strings = p.map(request_namenode_multi, files_HDFS)
    p.close()
    p.join()
    #t_fin = time.time()
    #duration = t_fin - t_deb
    #print duration
    for parent, json_string in zip(files_HDFS, json_strings):
        #print "yolo json_string '%s', parent '%s'" % (json_string, parent.print_HDFS())
        tt = parse_hdfs_json(json_string, parent.path)
        if depth:
            output = hdfs_ls_multi([e for e in tt if e.is_directory()], depth - 1)

        parent.children = tt


def print_arbo(file_HDFS):
    if file_HDFS.children != []:
        print file_HDFS.path + " : "
        for child in file_HDFS.children:
            child.print_HDFS()
        print 
        for child in file_HDFS.children:
            print_arbo(child)


def print_list(files_HDFS):
    for e in files_HDFS:
        e.print_HDFS()
    print
    for e in files_HDFS:
        print_arbo(e)


service_names = {
        "whdfs"   : "WebHDFS",
        "httpfs"  : "HttpFS"
        }

service_ports = {
        "whdfs"   : 50070,
        "httpfs"  : 14000
        }


def build_URL(protocol, host, port, rp_path, root_path, api_path, option):
    """
        Build the URL to request
    """
    if rp_path:
        return "%s://%s:%s%s%s%s?op=%s" % (protocol, host, port, rp_path, api_path, root_path, option)
    else:
        return "%s://%s:%s%s%s?op=%s" % (protocol, host, port, api_path, root_path, option)


def test_service(method, port):
    """
        Only testing if the service is up and responding
    """
    info("Testing service %s" % (service_names[method]))
    try:
        URL = build_URL(PROTOCOL, HOST, port, RP_PATH , "/", API, option)
        #print URL
        response = requests.get(URL)
        if response.ok:
            success("Service %s is available\n" % (service_names[method]))
            return True
        else:
            print error("Service %s seems to be down\n")
            return False
    except:
        error("Exception during requesting the service\n")
        return False


def test_all_services():
    """
        Test the default services : Web HDFS / HttpFS
    """
    info("Beginning to test services accessibility using default ports ...")
    found_services = {}
    counter = 0

    for service in service_names:
        if test_service(service, service_ports[service]):
            found_services.update({service : True})
            counter += 1
        else:
            found_services.update({service : False})

    if counter:
        success("Sucessfully retrieved %d services" % (counter))
    else:
        error("No service found.")
    return found_services, counter

def warning(message):
    print "\044[93m[!] \033[0m" + message

def success(message):
    print "\033[92m[+] \033[0m" + message

def error(message):
    print "\033[91m[-] \033[0m" + message

def info(message):
    print message


def main():

    VERSION = '0.1-dev'

    parser = argparse.ArgumentParser(description=""" 
     _   _____________ ___________                                 
    | | | |  _  \  ___/  ___| ___ \                                
    | |_| | | | | |_  \ `--.| |_/ /_ __ _____      _____  ___ _ __ 
    |  _  | | | |  _|  `--. \ ___ \ '__/ _ \ \ /\ / / __|/ _ \ '__|
    | | | | |/ /| |   /\__/ / |_/ / | | (_) \ V  V /\__ \  __/ |   
    \_| |_/___/ \_|   \____/\____/|_|  \___/ \_/\_/ |___/\___|_|  

    """,
        prog='hdfsbrowser.py',
        formatter_class=argparse.RawTextHelpFormatter)
    
    # Positional args
    parser.add_argument('host', action='store',  help='host')

    # Optional args
    parser.add_argument('--port', type=int, action='store', default=None, help='HDFS port')
    parser.add_argument('-o', '--output-file', type=str, action='store', help='Write to file instead of stdout')
    parser.add_argument('--ssl', action='store_true', default=False, help='Try SSL/TLS')
    parser.add_argument('--target-uri', type=str, action='store', default=None, help='Target URI of the Hadoop installation')
    parser.add_argument('-r', '--recursive', action='store_true', default=False, help='Be recursive')
    parser.add_argument('--root-path', type=str, action='store', default="/", help='Root path for the directory listing')
    parser.add_argument('-m', '--method', choices={"whdfs", "httpfs", "all"}, action='store', default="all", help='Method to use [')
    parser.add_argument('--time-out', type=int, action='store', default=5, help='Timeout for request')
    parser.add_argument( '-d', '--depth', type=int, action='store', default=-1, help='Recursion depth while listing directories')
    parser.add_argument( '--threads', type=int, action='store', default=2, help='Number of threads')
    parser.add_argument( '--proxy', type=str, action='store', default=None, help='Use proxy on given port')
    parser.add_argument( '--header', type=str, action='store', default=None, help='Pass custom header to server')


    global  LOGLEVELS, HOST, PORT, PROTOCOL, URL, RP_PATH, ROOT_PATH


    if len(sys.argv) == 1:
        print "\033[91" + "[!] Missing host ... Exiting"
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args()
        HOST = args.host
        if args.port: 
            PORT = args.port
        else:
            if args.method == "httpfs": PORT = 14000
            else: PORT = 50070
        PROTOCOL = HTTPS if args.ssl else HTTP
        ROOT_PATH = args.root_path
        RP_PATH = args.target_uri
        THREAD = args.threads
        

    if args.method == "all":
        if args.port: warning("Method all does not support --port option : test will be performed using default ports (14000, 50070)")
        services, counter = test_all_services()
        if counter:
            if services.has_key("whdfs"):
                PORT = service_ports["whdfs"]
                result = hdfs_listpaths("user", ROOT_PATH, args.recursive, args.output_file)
                if not result:
                    files_HDFS = init_ls(ROOT_PATH, "hdfs", service_ports["whdfs"], args.depth, args.output_file)
                    print_list(files_HDFS)
            else:
                PORT = service_ports["httpfs"]
                files_HDFS = init_ls(ROOT_PATH, "hdfs", service_ports["whdfs"], args.depth, args.output_file)
                print_list(files_HDFS)

    elif args.method == "whdfs":
        info("Trying using method WebHDFS (default port : 50070), trying on port %s" % (PORT))
        if test_service(args.method, PORT):
            files_HDFS = init_ls(ROOT_PATH, "hdfs", PORT, args.depth, args.output_file)
            print_list(files_HDFS)

    elif args.method == "httpfs":
        info("Trying using method HttpFS (default port : 14000), trying on port %s" % (PORT))
        if test_service(args.method, PORT):
            files_HDFS = init_ls(ROOT_PATH, "hdfs", PORT, args.depth, args.output_file)
            print_list(files_HDFS)

    else:
        error("Method %s does not exist, you can use (whdfs, httpfs)" % (args.method))

    return None

if __name__ == "__main__":
    main()
