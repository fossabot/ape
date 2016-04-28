# Author: Sai Uday Shankar Korlimarla
# skorlimarla@unomaha.edu
# Copyright (c) 2016
#!/usr/bin/env python

# Written in python3
# XLS Reader helper class for mongo
#
#  STANDALONE script
# Read xls file by passing as an argument to the program
#
# Inheriting
# xlsparser parse method will return data


# Module for reading excel files xlrd
# Module for creating ecxel files xlwd


import sys
import os

# pip install xlrd
# OR use the requirements.txt
import xlrd




class xlsparser:
    '''
    XLS File reader
        Parse XLS File
        Read Header
        Read XLS line by line
        Construct structured data array from xls (By Sheet number)
        If the data is to be required into another program, inherit it
    '''
    def __init__(self, file_path):
        '''
        Init
        '''
        self.file_path = os.path.abspath(file_path)
        
    def parse(self, sheet_number):
        '''
        Parse starts reading the file
            to retrieve headers
            to retrieve data in XLS
            returns a dictionary of the data
            This returned data can be dumped into mongodb directly
        '''
        datafile = self.file_path
        workbook = xlrd.open_workbook(datafile)
        sheet = workbook.sheet_by_index(sheet_number)
        data = [[sheet.cell_value(row,col)
                    for col in range(sheet.ncols)]
                        for row in range(sheet.nrows)]
        return data

if __name__ == '__main__':
    '''
    xls_dict will now have data
        If the data is to be required into another program, inherit it
        file location and sheet number
    '''
    xls_file = xlsparser(sys.argv[1])

    # sheet number is the second argument
    xls_dict = xls_file.parse(int(sys.argv[2]))
    print("--------------------------------------------")
    print("----------xls READER helper class ----------")
    print("--------------------------------------------")
    print(xls_dict)
    print("--------------------------------------------")
    print("---------------END -------------------------")
    print("--------------------------------------------")
