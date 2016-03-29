import sys
from pymongo import MongoClient
from vfeedModel import *

mongo_url = 'mongodb://localhost:27017/'
client = MongoClient(mongo_url)

# vfeedTables = vfeedDB.get_tables()
# print(vfeedTables)

# NVD Database
nvdDB = client['nvddb']

# Collections - Tables of interest from vfeed.db
cve_cpe = nvdDB.cve_cpe
cve_cwe = nvdDB.cve_cwe
cve_ref = nvdDB.cve_ref
cwe_capec = nvdDB.cwe_capec
cwe_category = nvdDB.cwe_category
cwe_db = nvdDB.cwe_db
map_cve_exploitdb = nvdDB.map_cve_exploitdb
map_cve_milw0rm = nvdDB.map_cve_milw0rm
map_cve_msf = nvdDB.map_cve_msf
map_cve_nessus = nvdDB.map_cve_nessus
map_cve_nmap = nvdDB.map_cve_nmap
map_cve_openvas = nvdDB.map_cve_openvas
map_cve_osvdb = nvdDB.map_cve_osvdb
map_cve_oval = nvdDB.map_cve_oval
map_cve_saint = nvdDB.map_cve_saint
map_cve_scip = nvdDB.map_cve_scip
map_cve_snort = nvdDB.map_cve_snort
map_cve_surikata = nvdDB.map_cve_surikata
nvd_db = nvdDB.nvd_db


# Drop the database collectionss
# This needs to be changed
def drop_nvd_db():
    pass
# Query object with peewee

# Bulk inserts - Drop collection before doing this!
def migrate_cve_cpe():
    Query_cve_cpe = CveCpe.select(CveCpe.cpeid, CveCpe.cveid).join(NvdDb).where(NvdDb.cveid==CveCpe.cveid)
    for q_cve_cpe in Query_cve_cpe:
        #print(q_cve_cpe.cpeid, q_cve_cpe.cveid.cveid)
        cve_cpe_post = {}
        cve_cpe_post['cpeid'] = str(q_cve_cpe.cpeid)
        cve_cpe_post['cveid'] = str(q_cve_cpe.cveid.cveid)
        cve_cpe.insert_one(cve_cpe_post)
        del cve_cpe_post

def migrate_nvd_db():
    Query_nvd_db = NvdDb.select()
    for q_nvd_db in Query_nvd_db:
        nvd_db_post = {}
        nvd_db_post['cveid'] = q_nvd_db.cveid
        nvd_db_post['date_published'] = q_nvd_db.date_published
        nvd_db_post['date_modified'] = q_nvd_db.date_modified
        nvd_db_post['summary'] = q_nvd_db.summary
        nvd_db_post['cvss_base'] = q_nvd_db.cvss_base
        nvd_db_post['cvss_impact'] = q_nvd_db.cvss_impact
        nvd_db_post['cvss_exploit'] = q_nvd_db.cvss_exploit
        nvd_db_post['cvss_access_vector'] = q_nvd_db.cvss_access_vector
        nvd_db_post['cvss_access_complexity'] = q_nvd_db.cvss_access_complexity
        nvd_db_post['cvss_authentication'] = q_nvd_db.cvss_authentication
        nvd_db_post['cvss_confidentiality_impact'] = q_nvd_db.cvss_confidentiality_impact
        nvd_db_post['cvss_integrity_impact'] = q_nvd_db.cvss_integrity_impact
        nvd_db_post['cvss_availability_impact'] = q_nvd_db.cvss_availability_impact
        nvd_db.insert_one(nvd_db_post)
        del nvd_db_post

def migrate_cve_cwe():
    Query_cve_cwe = CveCwe.select(CveCwe.cweid, CveCwe.cveid).join(NvdDb).where(NvdDb.cveid==CveCwe.cveid)
    for q_cve_cpe in Query_cve_cwe:
        #print(q_cve_cpe.cpeid, q_cve_cpe.cveid.cveid)
        cve_cwe_post = {}
        cve_cwe_post['cveid'] = str(q_cve_cpe.cveid.cveid)
        cve_cwe_post['cweid'] = str(q_cve_cpe.cweid)
        cve_cwe.insert_one(cve_cwe_post)
        del cve_cwe_post


def main():
    print("[+] Dropping CVE_CPE correaltions! :-\\")
    cve_cpe.drop()
    print("[+] Dropping NVD CVE data")
    nvd_db.drop()
    print("[+] Re-Creating NVD CVE Data")
    migrate_nvd_db()
    print("[+] Done!")
    print("[+] Re-Createing CVE_CPE correlations")
    migrate_cve_cpe()
    print("[+] Done!")
    print("[+] Re-Createing CVE_CWE correlations")
    migrate_cve_cwe()
    print("[+] Done")

if __name__ == '__main__':
    main()
