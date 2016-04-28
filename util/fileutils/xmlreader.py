# Author: Sai Uday Shankar Korlimarla
# skorlimarla@unomaha.edu
# Copyright (c) 2016
#!/usr/bin/env python

# Written in python3
# xml Reader helper class for mongo
#
#  STANDALONE script
# Read xml file by passing as an argument to the program
#
# Inheriting
# xmlparser parse method will return data


import sys
import os
from xml.dom import minidom



class xmlparser:
    '''
    xml File reader
        Parse xml File
        Iterate over parent for child, child for sub-child
        If the data is to be required into another program, inherit it
    '''
    def __init__(self, file_path, tagName):
        '''
        Init
        '''
        self.file_path = os.path.abspath(file_path)
        self.tagName = tagName

    def parse(self):
        '''
        ################################################################
        # sub-child-argument will be a variable passed to parse method #
        ############# ARGUMENT FOR FUTURE IMPLEMENTATION ###############
        ################################################################
        **** Objects are retured not data ****
        Parse starts reading the file
            to retrieve headers
            to retrieve data in xml
            returns a dictionary of the data
            This returned data can be dumped into mongodb directly
        '''
        datafile = self.file_path
        tagName = self.tagName
        data = ''
        xmldoc = minidom.parse(datafile)
        data = xmldoc.getElementsByTagName(tagName)
        # Change implementation for future
        '''
        for tagvalues in data:
            print(tagvalues.attributes['sub-child-argument'].value)
        '''
        return data


if __name__ == '__main__':
    '''
    xml_dict will now have data
        If the data is to be required into another program, inherit it
    '''
    xml_file = xmlparser(sys.argv[1], sys.argv[2])
    xml_data = xml_file.parse()
    print("--------------------------------------------")
    print("----------xml READER helper class ----------")
    print("-----------Objects are retured not data ----")
    print("--------------------------------------------")
    # Change implementation for future
    print(type(xml_data))
    '''
    for tagvalues in xml_data:
        print(tagvalues.attributes[sys.argv[3]].value)
    '''
    print("--------------------------------------------")
    print("---------------END -------------------------")
    print("--------------------------------------------")
