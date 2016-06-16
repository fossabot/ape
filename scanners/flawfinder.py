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


def create_temporary_copy(package):
    temp_dir = ''
    try:
        temp_dir = tempfile.mkdtemp()
        # Verify Package type - for later
        shutil.copy(os.path.abspath(package), temp_dir)
        temp_package = glob.glob(temp_dir+'/*.zip')[0]
        with zipfile.ZipFile(temp_package) as zf:
            zf.extractall(temp_dir)
            scan_target = temp_dir + '/' + zf.namelist()[0]
            clean_flawfinder_results(flawfinderscan(scan_target))
        os.remove(temp_package)
        return temp_dir

    except Exception as e:
        print(e)
        print("error")
        return None

def delete_temporary_copy(temp_dir):
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
    else:
        pass


def flawfinderscan(package_to_scan):
    package_to_scan = os.path.abspath(package_to_scan)
    flawfinder_args = ['flawfinder', '--quiet', '--dataonly',\
                       '--inputs', '--neverignore', '--followdotdir',\
                       '--columns', '--singleline', package_to_scan]
    if os.path.isdir(package_to_scan):
        flawfinder_out = subprocess.check_output(flawfinder_args)
        return(flawfinder_out)
    else:
        sys.stderr.write("[-] Flawfinder Error:1")
	sys.exit(-1)


def clean_flawfinder_results(scan_results):
    cwe_match = re.compile('CWE-\d+', re.IGNORECASE)
    cwe_list = [] 
    for line in scan_results.split(os.linesep):
         cwe_found = cwe_match.findall(line)
         if cwe_found:
             cwe_list.append(cwe_found)
    cwe_list = tuple(cwe_list)



if __name__ == '__main__':
   #flawfinderscan(sys.argv[1])
   temp_dir = create_temporary_copy(sys.argv[1])
   if temp_dir:
       delete_temporary_copy(temp_dir)
   else:
      pass
