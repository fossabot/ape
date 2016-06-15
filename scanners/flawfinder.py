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

def flawfinderscan(directory_to_scan):
    directory_to_scan = os.path.abspath(directory_to_scan)
    flawfinder_args = ['flawfinder', '--quiet', '--dataonly',\
                       '--inputs', '--neverignore', '--followdotdir',\
                       '--columns', '--singleline',directory_to_scan]
    if os.path.isdir(directory_to_scan):
        flawfinder_out = subprocess.check_output(flawfinder_args)
        sys.stdout.write(flawfinder_out)
        # If required to iterate line by line like a human
        '''
        for line in flawfinder_out.split(os.linesep):
            print(line+"\n")
        '''
    else:
        sys.stderr.write("[-] Flawfinder Error:1")



if __name__ == '__main__':
   flawfinderscan(sys.argv[1])
