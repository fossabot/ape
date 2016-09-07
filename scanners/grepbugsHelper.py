#!/usr/bin/env python

# Copyrights (c) 2016 Sai Uday Shankar Korlimarla
# Check the project license in the LICENSE file
# SPDX License Identifier GPL-2.0

# flawfinder - find potential security flaws ("hits") in source code
# Source: http://www.dwheeler.com/flawfinder/
# Man page at http://manpages.ubuntu.com/manpages/precise/man1/flawfinder.1.html

import re
import subprocess
import sys
import os
import tempfile
import shutil
import zipfile
import tarfile
from StringIO import StringIO
import glob
import re
from pymongo import MongoClient

def fetch_and_save(scan_id, upload_id):
    print(scan_id)


def grepbugsHelper(upload_id, package):
    
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(package) as to_scan_Zip:
        to_scan_Zip.extractall(temp_dir)
    dir_to_scan = [x[0] for x in os.walk(temp_dir)]
    #print(dir_to_scan[1])
    current_dir = os.getcwd()
    os.chdir(os.path.expanduser('~'))
    os.chdir('GrepBugs/')
  
    #print str(dir_to_scan[1])
    command_to_run = 'python ~/GrepBugs/grepbugs.py -d ' + str(dir_to_scan[1])
    output = os.popen(command_to_run).read().split('\n')
    os.chdir(current_dir)
    shutil.rmtree(dir_to_scan[1])
    
    scan_id_match = re.compile('.*-.*-.*', re.IGNORECASE)
    
    for item in output:
        scan_id = scan_id_match.findall(item)
        if scan_id:
            fetch_and_save(scan_id[0], upload_id)


if __name__ == '__main__':
    grepbugsHelper(sys.argv[1], sys.argv[2])
