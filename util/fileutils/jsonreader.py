# -*- coding: utf-8 -*-

# Author: Sai Uday Shankar Korlimarla
# skorlimarla@unomaha.edu
# Copyright (c) 2016
#!/usr/bin/env python

import json
import codecs
import sys
import os


# Written in python3
# JSON Reader helper class for mongo
#
#  STANDALONE script
# Read JSON from file or url
# No support for URL at this point

# Inheriting
# jsonparser parse method will return the data from json


class jsonparser:
    '''
    JSON File reader or url reader
        Does not support authentication at this point.
    '''
    def __init__(self, file_path):
        '''
        Init
        '''
        self.file_path = os.path.abspath(file_path)
        
    def parse(self):
        '''
        Parse starts reading the file
            to retrieve data in JSON
            returns a dictionary of the data
            This returned data can be dumped into mongodb directly
        '''
        datafile = self.file_path
        data = []
        if not os.path.isfile(datafile):
            sys.stdout.write("File only json reader ")
            exit(0)
        with open(datafile) as jsonreader:
            data = json.load(jsonreader)
        return data

if __name__ == '__main__':
    '''
    Pass a json file and get data from the json file
        No funny business other than reading and passing back information
    '''
    jsonfile = jsonparser(sys.argv[1])

    json_data = jsonfile.parse()
    print("--------------------------------------------")
    print("----------JSON READER helper class ----------")
    print("--------------------------------------------")
    print(json_data)
    print("--------------------------------------------")
    print("---------------END -------------------------")
    print("--------------------------------------------")
