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
    found_cwe = ''
    result = cve_cwe.find_one({'cveid': cveid})
    if result:
        return result['cweid']
    else:
        return "No CWE"
    


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
 
    version_raw = version_raw.replace('_', '.')
    version_raw = version_raw.replace('-','.')
   
    ver_pat_1 = re.compile('.*(\d+.+\d+.+\d+(?:))[.](.*)')
    ver_pat_2 = re.compile('.*(\d+.+\d+.+\d+[a-zA-Z0-9]+)')
    ver_pat_3 = re.compile('.*(\d+\.+\d+\.+\d+).*')
    ver_pat_4 = re.compile('.*(\d+\.\d+\..*)')

    version_found_1 = ver_pat_1.findall(version_raw)
    version_found_2 = ver_pat_2.findall(version_raw)
    version_found_3 = ver_pat_3.findall(version_raw)
    version_found_4 = ver_pat_4.findall(version_raw)

    version = ''
 
    if version_found_1:
        version =  ':'.join(version_found_1[0])
    elif version_found_2: 
        version = version_found_2[0]
    elif version_found_3:
        version = version_found_3[0]
    elif version_found_4:
        version = version_foun_4[0]
    else:
        version = ''

    results = []
    
    results = getCPE(product,version)
    
    return results


def getCPE(productname, version):
    client = MongoClient()
    vFeed = client['vFeed']
    cve_cpe = vFeed.cve_cpe
    nvd_db = vFeed.nvd_db
    regexpattern = "cpe:/.*"+productname+".*:.*"+version
    cve_cpe_cur = cve_cpe.find({'cpeid': {'$regex': regexpattern}}, {'_id':0, 'cpeid':1, 'cveid':1})
    cve_cpes = []
    for each_finding in cve_cpe_cur:
        each_finding['cvss_base'] = nvd_db.find_one({'cveid': each_finding['cveid']}, {'_id':0, 'cvss_base':1})['cvss_base']
        cve_cpes.append(each_finding)
        
    return cve_cpes


if __name__ == '__main__':
    product(sys.argv[1], sys.argv[2])
    sys.stdout.write("[+] Done\n")
