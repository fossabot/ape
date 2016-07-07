from pymongo import MongoClient
import sys
import os
import re
from getProject import getProject
import zipfile


def product(package):
    product = getProject(package)
    minify(package, product)

def minify(package, product):
    zipreader = zipfile.ZipFile(os.path.abspath(package))
    name_list = zipreader.namelist()
    version_raw = name_list[0]
    version_raw = version_raw.strip('/')
    ver_match = re.match(".*(\d+[_\.]\d+[_\.]\d+([a-z]+)?)", version_raw)
    version = ''
    stdout_results = ''
    results = []
    if ver_match:
        version = ver_match.group(1)
        version = version.replace('_','.')
        results = getCPE(product,version)
    else:
        results = getCPE(product)
    for each_cpe in results:
        print(each_cpe)


def getCPE(productname, version):
    client = MongoClient()
    vFeed = client['vFeed']
    cve_cpe = vFeed.cve_cpe
    regexpattern = ".*"+productname+".*"+version+".*"
    cve_cpe_cur = cve_cpe.find({'cpeid': {'$regex': regexpattern}}, {'_id':0, 'cpeid':1, 'cveid':1})
    cve_cpes = []
    for each_finding in cve_cpe_cur:
        cve_cpes.append(each_finding)
    return cve_cpes

if __name__ == '__main__':
    product(sys.argv[1])
