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


if sys.version_info >= (3, 0):
    from tkinter import *
    import tkinter,tkFileDialog
    import tkMessageBox
else :
    from Tkinter import *
    import Tkinter,tkFileDialog
    import tkMessageBox

class launcher(object):
    def __init__(self):
        # Create the window
        current_row=0
        
        self.root = Tk()
        self.root.title("CTSU SFR Calculator 1.0 ")
        
        root = self.root
        
        self.bamboo=""
        self.path=StringVar()
        
        self.intro = Label(root, fg="red", justify=LEFT)
        self.intro.config(text="""Instructions:
            1. Enter the bamboo opportunity number.
            2. Provide the path to a configuration.xml file.
            3. Press Go.
            4. E-mail the bamboonumber.xml to ash.patel@renesas.com."""
        )
        self.intro.grid(row=current_row, columnspan=2, sticky=W, padx=10, pady=10)
        
        current_row += 1

        ############# Bamboo Number ###############
        Label(root, text="Bamboo opportunity number:", fg="dark red").grid(row=current_row, sticky=W, columnspan=2, padx=10)
        current_row += 1
        
        bamboo_entry = Entry(root, width=80)
        
        ############# Configuration.xml Path ###############
        Label(root, text="Locate configuration.xml:", fg="dark red").grid(row=current_row, sticky=W, columnspan=2, padx=10)
        current_row += 1
        
        
        

class SYNERGY(object):
    def __init__(self, src):
        if False == os.path.exists(src):
            logging.error("File %s does not exist." % src)
            sys.exit(1)
            
        self.src = src
        DOMTree = xml.dom.minidom.parse(src)
        cproject = DOMTree.documentElement
        
        optionValues = cproject.getElementsByTagName("property")
        for optionValue in optionValues:
            if optionValue.hasAttribute("id"):
                attr_id = optionValue.getAttribute("id")
                if "config.bsp.common.id1"==attr_id:
                    optionValue.setAttribute("value", "0xFFFFFFFF")
                if "config.bsp.common.id2"==attr_id:
                    optionValue.setAttribute("value", "0xFFFFFFFF")
                if "config.bsp.common.id3"==attr_id:
                    optionValue.setAttribute("value", "0xFFFFFFFF")
                if "config.bsp.common.id4"==attr_id:
                    optionValue.setAttribute("value", "0xFFFFFFFF")
                    



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                                     """
                                     Parse a Synergy Configuration file and generate component information.
                                     """)
    parser.add_argument('-o', '--output', dest='outfile', default="./output.csv", help='Specify location where a csv file can be output.')
    parser.add_argument('-l', '--log', dest='logfile', help='Specify where logger information should be output.')
    parser.add_argument('-i', '--input', dest='infile', help='Specify full path to configuration.xml file. E.g.: \"./my_folder/configuration.xml\" ')
