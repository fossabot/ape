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
def migrate_nvd_db():
    Query_nvd_db = NvdDb.select()
    for q_nvd_db in Query_nvd_db:
        # Construct fields
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
        # Verify before insert
        if nvd_db.find_one(nvd_db_post) is None:
            nvd_db.insert_one(nvd_db_post)
        del nvd_db_post

def migrate_cve_cpe():
    Query_cve_cpe = CveCpe.select(CveCpe.cpeid, CveCpe.cveid).join(NvdDb).where(NvdDb.cveid==CveCpe.cveid)
    for q_cve_cpe in Query_cve_cpe:
        # Construct fields
        cve_cpe_post = {}
        cve_cpe_post['cpeid'] = str(q_cve_cpe.cpeid)
        cve_cpe_post['cveid'] = str(q_cve_cpe.cveid.cveid)
        # Verify before insert
        if cve_cpe.find_one(cve_cpe_post) is None:
            cve_cpe.insert_one(cve_cpe_post)
        del cve_cpe_post


def migrate_cve_cwe():
    Query_cve_cwe = CveCwe.select(
                                    CveCwe.cweid,
                                    CveCwe.cveid
                                ).join(NvdDb).where(NvdDb.cveid==CveCwe.cveid)
    for q_cve_cpe in Query_cve_cwe:
        # Construct fields
        cve_cwe_post = {}
        cve_cwe_post['cveid'] = str(q_cve_cpe.cveid.cveid)
        cve_cwe_post['cweid'] = str(q_cve_cpe.cweid)
        # Verify before insert
        if cve_cwe.find_one(cve_cwe_post) is None:
            cve_cwe.insert_one(cve_cwe_post)
        del cve_cwe_post

def migrate_cve_ref():
    Query_cve_ref = CveReference.select(
                                        CveReference.cveid,
                                        CveReference.refname,
                                        CveReference.refsource
                                        ).join(NvdDb).where(NvdDb.cveid==CveReference.cveid)
    for q_cve_ref in Query_cve_ref:
        # Construct fields
        cve_ref_post = {}
        cve_ref_post['cveid'] = str(q_cve_ref.cveid.cveid)
        cve_ref_post['refname'] = str(q_cve_ref.refname)
        cve_ref_post['refsource'] = str(q_cve_ref.refsource)
        # Verify before insert
        if cve_ref.find_one(cve_ref_post) is None:
            cve_ref.insert_one(cve_ref_post)
        del cve_ref_post

def migrate_cwe_db():
    Query_cwe_db = CweDb.select(
                                    CweDb.cweid,
                                    CweDb.cwetitle
                                )
    for q_cwe_ref in Query_cwe_db:
        # Construct fields
        cwe_db_post = {}
        cwe_db_post['cweid'] = str(q_cwe_ref.cweid)
        cwe_db_post['cwetitle'] = str(q_cwe_ref.cwetitle)
        # Verify before insert
        if cwe_db.find_one(cwe_db_post) is None:
            cwe_db.insert_one(cwe_db_post)
        del cwe_db_post

def migrate_cwe_category():
    Query_cwe_category = CweCategory.select(
                                                CweCategory.categoryid,
                                                CweCategory.categorytitle,
                                                CweCategory.cweid
                                            )
    for q_cwe_cat in Query_cwe_category:
        # Construct fields
        cwe_cat_post = {}
        cwe_cat_post['cweid'] = str(q_cwe_cat.cweid)
        cwe_cat_post['categoryid'] = str(q_cwe_cat.categoryid)
        cwe_cat_post['categorytitle'] = str(q_cwe_cat.categorytitle)
        # Verify before insert
        if cwe_category.find_one(cwe_cat_post) is None:
            cwe_category.insert_one(cwe_cat_post)
        del cwe_cat_post


# Call this function to start database migrations
def main():
    '''
    print("[+] Dropping NVD CVE data")
    nvd_db.drop()
    print("[+] Re-Creating NVD CVE Data")
    migrate_nvd_db()
    print("[+] Done!")
    print("[+] Dropping CVE_CPE correaltions! :-\\")
    cve_cpe.drop()
    print("[+] Re-Createing CVE_CPE correlations")
    migrate_cve_cpe()
    print("[+] Done!")
    print("[+] Dropping CVE_CWE correaltions!")
    cve_cwe.drop()
    print("[+] Re-Createing CVE_CWE correlations")
    migrate_cve_cwe()
    print("[+] Done")
    print("[+] Dropping CVE References!")
    cve_ref.drop()
    print("[+] Re-Createing CVE References")
    migrate_cve_ref()
    print("[+] Done")
    print("[+] Dropping CWE Data!")
    cwe_db.drop()
    print("[+] Re-Createing CWE Data")
    migrate_cwe_db()
    print("[+] Done")
    '''
    print("[+] Dropping CWE Categories!")
    cwe_category.drop()
    print("[+] Re-Createing CWE Categories")
    migrate_cwe_category()
    print("[+] Done")

if __name__ == '__main__':
    main()
