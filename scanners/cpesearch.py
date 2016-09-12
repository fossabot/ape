from pymongo import MongoClient
import sys
import os
import re
from getProject import getProject
import zipfile


def getcweid(cveid):
    client = MongoClient()
    vFeed = client['vFeed']
    cve_cwe = vFeed.cve_cwe
    found_cwes = []
    for each_cwe in cve_cwe.find({'cveid': cveid}):
        found_cwes.append(each_cwe['cweid'])
    return list(set(found_cwes))


def save_matches(nvd_matches, upload_id):
    client = MongoClient()
    db = client.apedb
    for entry in nvd_matches:
        entry['cweid'] = getcweid(entry['cveid'])
        entry['upload_id'] = upload_id
        db.nvd_match.update(entry, entry, upsert=True)

def product(upload_id, package):
    product = getProject(package)
    nvd_matches = minify(package, product)
    save_matches(nvd_matches, upload_id)

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
    return results


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
    product(sys.argv[1], sys.argv[2])
    sys.stdout.write("[+] Done\n")
    update_all_with_cwes()
