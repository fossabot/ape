import os
import sys
import re
from pymongo import MongoClient
from bson.objectid import ObjectId
from collections import Counter


def drop_consolidation(apepackage):
    apepackage.drop()


def start_consolidation(apedb):
    apepackage = apedb.apepackage
    apepackage.drop()

    uploads = apedb.uploads
    openhub = apedb.openhub
    flawfinder = apedb.flawfinder
    grepbugs_result = apedb.grepbugs_result
    grepbugs_details = apedb.grepbugs_details
    nvd_match = apedb.nvd_match

    for each_upload in uploads.find({}):
        openhub_id =  each_upload['openhub_id']
        upload_id = each_upload['_id']
       
        openhub_data = get_openhub_data(openhub, openhub_id)
        flawfinder_data = get_flawfinder_data(flawfinder, upload_id)
        grepbugs_result_data = get_gb_results_data(grepbugs_result, upload_id)
        grepbugs_details_data = get_gb_details_data(grepbugs_details, upload_id)
        nvd_match_data = get_nvd_match_data(nvd_match, upload_id)

        

        if nvd_match_data['nvd_cwe_count'] == 0:
            nvd_match_data['nvd_cwe_count'] = 1
        if grepbugs_details_data['total_code'] == 0:
            grepbugs_details_data['total_code'] = 1
        
        nvd_match_data['nvd_cwe_density'] = float(nvd_match_data['nvd_cwe_count']) / float(grepbugs_details_data['total_code'])
        flawfinder_data['intrinsic_cwe_density'] = float(flawfinder_data['cwe_count']) / float(grepbugs_details_data['total_code'])
        if grepbugs_result_data['regex_categories_count'] == 0:
            grepbugs_result_data['regex_categories_count'] = 1
        signature_density = float(grepbugs_details_data['total_code']) / float(grepbugs_result_data['regex_categories_count'])
        grepbugs_result_data['signature_density'] = signature_density
      
        apeid = apepackage.insert_one({'upload_id': upload_id}).inserted_id
        for key in flawfinder_data:
            apepackage.update_one({'_id': apeid}, {'$set': {key: flawfinder_data[key]}})
          
        for key in openhub_data:
            apepackage.update_one({'_id': apeid}, {'$set': {key : openhub_data[key]}})
        for key in grepbugs_details_data:
            apepackage.update_one({'_id': apeid}, {'$set': {key: grepbugs_details_data}})
        for key in grepbugs_result_data:
            apepackage.update_one({'_id': apeid}, {'$set': {key: grepbugs_result_data[key]}})
    
        for key in nvd_match_data:
            apepackage.update_one({'_id': apeid}, {'$set': {key: nvd_match_data[key]}})
       
        
    sys.stdout.write("[+] Done\n")
   
def get_openhub_data(openhub, openhub_id):
    ohloh_data_raw = openhub.find_one({'_id': ObjectId(openhub_id)})
    ohloh_data = {}
    ohloh_data['project_name'] = ohloh_data_raw['project_name']
    ohloh_data['loc'] = ohloh_data_raw['loc']
    ohloh_data['commitcount'] = ohloh_data_raw['commitcount']
    ohloh_data['rating'] = ohloh_data_raw['rating']
    ohloh_data['languages_count'] = len(ohloh_data_raw['languages'])
    ohloh_data['communiting_rating'] = ohloh_data_raw['rating_count']
    return ohloh_data

def get_flawfinder_data(flawfinder, upload_id):
    flawfinder_data = {}
    cwe_prefreq = []
    cwe_category = []
    flawfinder_data['affected_files_count'] = flawfinder.find({'upload_id': upload_id}).count()
    cwe_count = 0
    for each_file in flawfinder.find({'upload_id': upload_id}):
        cwe_count += len(each_file['WeaknessID'])
        for each_cweid in each_file['WeaknessID']:
            cwe_prefreq.append(each_cweid)
        cwe_category.append(each_file['Category'].strip('()'))
    flawfinder_data['cwe_count'] = cwe_count

    for key in Counter(cwe_prefreq):
        flawfinder_data[key] = Counter(cwe_prefreq)[key]
   
    for key in Counter(cwe_category):
        flawfinder_data[key] = Counter(cwe_category)[key]
    
    return flawfinder_data

def get_gb_results_data(grepbugs_result, upload_id):
    gb_results_data = {}
    gb_results_data['regex_categories_count'] = grepbugs_result.find({'upload_id': upload_id}).count()
    return gb_results_data

def get_gb_details_data(grepbugs_details, upload_id):
    gb_details_data = {}
    gb_details_data['bug_hits'] = grepbugs_details.find({'upload_id': upload_id}).count()
    
    total_code = 0
    total_files = []
    for each_hit in grepbugs_details.find({'upload_id': upload_id}):
        total_code += each_hit['nCode']
        total_files.append(each_hit['file'])
    total_files = list(set(total_files))
    gb_details_data['total_code'] = total_code
    gb_details_data['total_files'] = len(total_files)
    return gb_details_data


def latest_cve(nvd_cves):
    latest_year = 0
    cve_year_pattern = re.compile('CVE-(\d+)-.\d+', re.IGNORECASE)
    for each_cve in nvd_cves:
        cve_year = cve_year_pattern.findall(each_cve)
        if cve_year and cve_year > latest_year:
            latest_year = cve_year
    return latest_year

def get_exploits(nvd_cves):
    client = MongoClient()
    vfeed = client.vFeed
    exploit_db = vfeed.map_cve_exploitdb
    
    exploit_count = 0
    for each_cve in nvd_cves:
        exploit_count += exploit_db.find({'cveid': each_cve}).count()
    
    return exploit_count


def get_nvd_match_data(nvd_match, upload_id):
    nvd_match_data = {}
    nvd_match_data['nvd_match_count'] = nvd_match.find({'upload_id': upload_id}).count()
    nvd_cpe_count = []
    nvd_cve_count = []
    nvd_cwe_count = 0
    nvd_cvss_store = []

    for each_match in nvd_match.find({'upload_id': upload_id}):
        nvd_cpe_count.append(each_match['cpeid'])
        nvd_cve_count.append(each_match['cveid'])
        nvd_cvss_store.append(each_match['cvss_base'])

    nvd_match_data['nvd_exploits'] = get_exploits(nvd_cve_count)
  
    nvd_match_data['nvd_cpe_count'] = len(list(set(nvd_cpe_count)))
    nvd_match_data['latest_year'] = latest_cve(list(set(nvd_cve_count)))
    nvd_match_data['nvd_cve_count'] = len(list(set(nvd_cve_count)))
    nvd_match_data['nvd_cwe_count'] = nvd_match_data['nvd_cve_count']
    
     
    nvd_cvss_store = list(set(nvd_cvss_store))
    if nvd_cvss_store:
        nvd_match_data['nvd_cvss_max'] = max(nvd_cvss_store)
        nvd_match_data['nvd_cvss_min'] = min(nvd_cvss_store)
    else:
        nvd_match_data['nvd_cvss_max'] = 1
        nvd_match_data['nvd_cvss_min'] = 0

    sum_cvss = 1
    for each_cvss in nvd_cvss_store:
        sum_cvss+= each_cvss
    if len(nvd_cvss_store) > 0:
        nvd_match_data['nvd_cvss_avg'] = sum_cvss/len(nvd_cvss_store)
    else:
        nvd_match_data['nvd_cvss_avg'] = sum_cvss/1
        
    return nvd_match_data

if  __name__ == '__main__':
    client = MongoClient()
    apedb = client.apedb
    apepackage = apedb.apepackage
    #drop_consolidation(apepackage)
    start_consolidation(apedb)
