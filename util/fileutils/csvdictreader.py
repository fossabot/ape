# Author: Sai Uday Shankar Korlimarla
# skorlimarla@unomaha.edu
# Copyright (c) 2016
#!/usr/bin/env python

# Written in python3
# CSV Reader helper class for mongo
#
#  STANDALONE script
# Read csv file by passing as an argument to the program
#
# Inheriting
# csvparser parse method will return data


import sys
import os
import csv


class csvparser:
    '''
    CSV File reader
        Parse CSV File
        Read Header
        Read CSV line by line
        Construct a dictinoary as field(from header) with value (from row in CSV)
        If the data is to be required into another program, inherit it
    '''
    def __init__(self, file_path):
        '''
        Init
        '''
        self.file_path = os.path.abspath(file_path)

    def parse(self):
        '''
        Parse starts reading the file
            to retrieve headers
            to retrieve data in csv
            returns a dictionary of the data
            This returned data can be dumped into mongodb directly
        '''
        datafile = self.file_path
        data = []
        with open(datafile, 'r') as csvreader:
            dictreader = csv.DictReader(csvreader)
            for line in dictreader:
                data.append(line)
        return data


if __name__ == '__main__':
    '''
    csv_dict will now have data
        If the data is to be required into another program, inherit it
    '''
    csv_file = csvparser(sys.argv[1])
    csv_dict = csv_file.parse()
    print("--------------------------------------------")
    print("----------CSV READER helper class ----------")
    print("--------------------------------------------")
    print(csv_dict)
    print("--------------------------------------------")
    print("---------------END -------------------------")
    print("--------------------------------------------")
