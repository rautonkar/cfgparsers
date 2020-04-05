#!/usr/bin/env python
import os
import sys
import shutil

import logging
import argparse

import re
import csv
import copy
import xml.dom.minidom

"""
Copyright (c) 2018 Onkar Raut (onkar.raut.at.renesas.com).

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class COMPONENT(object):
    def __init__(self, vendor, class_name, subgroup, group, version):
        self.vendor = vendor
        self.class_name = class_name
        self.subgroup = subgroup
        self.group = group
        self.version = version
        
class MAP(object):
    def __init__(self, csv_src, csv_out, synergy_cfg):
        if False == os.path.exists(csv_src):
            logging.error("File %s does not exist." % csv_src)
            sys.exit(1)
            
        self.src = csv_src
        
        with open(csv_src, 'rb') as csvfile,  open(csv_out, 'w') as outfile:
            reader = csv.DictReader(csvfile)
            if synergy_cfg.src in reader.fieldnames:
                logging.error("Configuration file %s is already mapped. Terminating parsing." % synergy_cfg.src)
                return
            
            writerdict = copy.deepcopy(reader.fieldnames)
            writerdict.append(synergy_cfg.src)
            
            writer = csv.DictWriter(outfile, writerdict)
            writer.writeheader()
            for row in reader:
                
                if row['Module Name'] in synergy_cfg.module_name_list:
                    logging.info("%s found in %s" %(row['Module Name'], synergy_cfg.src))
                    row[synergy_cfg.src] = "Y"
                else:
                    row[synergy_cfg.src] = "N"
                
                writer.writerow(row)
        
        """ Replace original file """
        shutil.copy(csv_out, csv_src)
        
        return
    
class SYNERGY(object):
    def __init__(self, src):
        if False == os.path.exists(src):
            logging.error("File %s does not exist." % src)
            sys.exit(1)
        
        self.src = src
        self.component_list = set()
        self.module_name_list = set()
        
        self.src = src
        DOMTree = xml.dom.minidom.parse(src)
        cproject = DOMTree.documentElement
        optionValues = cproject.getElementsByTagName("component")
        for optionValue in optionValues:
            class_name = r""
            subgroup = r""
            vendor = r""
            group = r""
            version = r""
            
            if optionValue.hasAttribute("class"):
                """ Print the class """
                class_name += optionValue.getAttribute("class")
                
            if optionValue.hasAttribute("subgroup"):
                """ Print the sub group name """
                subgroup += optionValue.getAttribute("subgroup")
                
            if optionValue.hasAttribute("group"):
                """ Print the sub group name """
                group += optionValue.getAttribute("group")
                
            if optionValue.hasAttribute("vendor"):
                """ Print the vendor name """
                vendor += optionValue.getAttribute("vendor")
                
            if optionValue.hasAttribute("version"):
                """ Print the version """
                version += optionValue.getAttribute("version")
                
            logging.info("%s, %s, %s, %s, %s" % (vendor, class_name, subgroup, group, version))
            
            new_component = COMPONENT(vendor, class_name, subgroup, group, version)
            self.component_list.add(new_component)
            self.module_name_list.add(subgroup)
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                                     """
                                     Parse a Synergy Configuration file and generate component information.
                                     """)
    parser.add_argument('-o', '--output', dest='outfile', default="./output.csv", help='Specify location where a csv file can be output.')
    parser.add_argument('-l', '--log', dest='logfile', help='Specify where logger information should be output.')
    parser.add_argument('-i', '--input', dest='infile', help='Specify full path to configuration.xml file. E.g.: \"./my_folder/configuration.xml\" ')
    parser.add_argument('-p', '--packs', dest='packs', help='Specify full path to location containing all Synergy Software Package files.')
    parser.add_argument('-m', '--map', dest='map', help='Specify full path to comma separated file which holds components to look for. ')

    parser.add_argument('--version', action='version', version='%(prog)s 2.1')
    
    args = parser.parse_args()
    
    if args.logfile is not None:
        logging.basicConfig(filename=args.logfile, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(module)s: %(asctime)s - %(levelname)s - %(message)s')
        
    synergy_config = SYNERGY(args.infile)
    map_info = MAP(args.map, args.outfile, synergy_config)