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
import sqlite3
import unicodedata as ud

def fetch_and_save(scan_id, upload_id, directory):
    client = MongoClient()
    db = client.apedb
    conn = sqlite3.connect('/home/ushan/GrepBugs/data/grepbugs.db')
    cur = conn.cursor()
    project_id = ''
    saved_dpath = ''
    for row in cur.execute('select project_id from scans where scan_id="%s"' % scan_id):
        project_id = row[0]
    for row in cur.execute('select project from projects where project_id="%s"' % project_id):
        saved_dpath = str(row[0])
    

    results = []

    for row in cur.execute('select * from results where scan_id="%s"' % scan_id):
        result = {}
        result['upload_id'] = upload_id
        result['directory'] = directory
        result['result_id'] = row[0]
        result['scan_id'] = row[1]
        result['language'] = row[2]
        result['regex_id'] = row[3]
        result['regex_text'] = row[4]
        result['description'] = row[5]
        results.append(result)
    
    t_results = []
    for row in cur.execute('select * from t'):
        t_result = {}
        temp_str = str(row[0])
        if(temp_str == saved_dpath):
            t_result['upload_id'] = upload_id
            t_result['directory'] = directory
            t_result['project'] = row[0]
            t_result['language'] = row[1]
            t_result['file'] = row[2]
            t_result['nBlank'] = row[3]
            t_result['nComment'] = row[4]
            t_result['nCode'] = row[5]
            t_result['nScaled'] = row[6]
            t_results.append(t_result)
    
    for entry in results:
        db.grepbugs_result.insert_one(entry)
    for entry in t_results:
        db.grepbugs_details.insert_one(entry)
    sys.stdout.write("[+] Done\n") 
    conn.close()
    sys.exit(0) 
        


def grepbugsHelper(upload_id, package): 
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(package) as to_scan_Zip:
        to_scan_Zip.extractall(temp_dir)
    dir_to_scan = [x[0] for x in os.walk(temp_dir)]
    current_dir = os.getcwd()
    os.chdir(os.path.expanduser('~'))
    os.chdir('GrepBugs/')
    command_to_run = 'python ~/GrepBugs/grepbugs.py -d ' + str(dir_to_scan[1])
    output = os.popen(command_to_run).read().split('\n')
    os.chdir(current_dir)
    shutil.rmtree(dir_to_scan[1])
    
    scan_id_match = re.compile('.*-.*-.*-.*-.*', re.IGNORECASE)
    for item in output:
        scan_id = scan_id_match.findall(item)
        if scan_id:
            fetch_and_save(scan_id[0], upload_id, str(dir_to_scan[1]))
        else:
            sys.stderr.write("no match \n")


if __name__ == '__main__':
    grepbugsHelper(sys.argv[1], sys.argv[2])
    #fetch_and_save('6ea8872a-7516-11e6-9b5c-0401064cd801', 1, '/tmp/tmp4rQcbO/openssl-OpenSSL_1_0_2c')
    

