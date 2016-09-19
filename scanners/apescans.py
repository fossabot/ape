from pymongo import MongoClient

from os import listdir
from os.path import isfile, join, isdir, exists
import sys
import hashlib
from os import walk
from flawfinder import create_temporary_copy
from getProject import getProject
from openhub import *
from  grepbugsHelper import  grepbugsHelper
from cpesearch import product
from consolidation import start_consolidation

def startApe(directory_name):
    # Mongo Connection to localhost - NO user/pass
    client = MongoClient()
    # Database of Interest
    apedb = client.apedb
    ##############
    # Collections#
    ##############
    # packages
    uploads = apedb.uploads
    # FlawFinder results for packages
    flawfinder = apedb.flawfinder
    # OpenHub
    openhub = apedb.openhub
    # Grebbugs
    grepbugs_details = apedb.grepbugs_details
    grepbugs_result = apedb.grepbugs_result
    # NVD matches
    nvd_match = apedb.nvd_match
    
    # Consolidation
    apepackage = apedb.apepackage

    # Drop previous scans & Scan information
    uploads.drop()
    flawfinder.drop()
    openhub.drop()
    grepbugs_result.drop()
    grepbugs_details.drop()
    nvd_match.drop()
    apepackage.drop()
 
    filenames = []
    package_ids = []
    for (dirpath, dirnames, filenames) in walk(directory_name):
        filenames = filenames        
    for file_name in filenames:
        file_name = directory_name + file_name
        uid = uploads.insert_one({'name':file_name}).inserted_id
        package_ids.append(uid)
    for each_id in package_ids:
        # Fetch Uploads
        package_name = uploads.find_one({'_id': each_id}, {'_id':0, 'name':1})['name']
        print("Scanning {0} with ID: {1}".format(package_name,each_id))

        # FlawFinderScan
        create_temporary_copy(each_id, package_name)
        print("Flawfinder completed")

        #Get OpenHub Tag
        tag = getProject(package_name)    
        uploads.update_one({'_id': each_id}, {'$set': {'project_tag': tag}})
        #print("Tag generation completed")
 
        # OpenHub Tag generation & Information extraction
      
        requstedPath = 'project'
        searchAttr = tag
        OhlohPath = setOhlohPathType(requstedPath)
        searchAttr = tag
        params = setOhlohAPIkey()
        baseURL = setOhlohBaseURL()
        OhlohAbsURL = preParse(OhlohBaseURL= baseURL,OhlohPath=OhlohPath, searchAttr=searchAttr, params=params)
        elementTree = xmlDocTree(OhlohAbsURL)
        if requstedPath == 'people':
            parse_people(elementTree=elementTree)
        elif requstedPath == 'organization':
            parse_organization(elementTree=elementTree)
        elif requstedPath == 'project':
            openhubData = parse_project(elementTree=elementTree)
        openhub_id = insert_into_database(openhubData, each_id)
        uploads.update_one({'_id': each_id}, {'$set': {'openhub_id': openhub_id}})
        
        print("OpenHub information fetch completed")

        # GrepBugs - Signature scanning
        grepbugsHelper(each_id, package_name)
        print("grepping bugs")

        # CPE Searches 
        print("Finding NVD Matches - CPE, CVE, CWE, CVSS Score")
        product(uid, package_name)
        
    # Start Consolidation
    # print("Consolidating Scans")
    # start_consolidation(apedb)
    # print("Consolidatin completed")
    # Generate report 
    
if __name__ == '__main__':
    dir_name = ''
    if isdir(sys.argv[1]):
        dir_name  = sys.argv[1]
        startApe(dir_name)
    else:
        sys.stdout.write("Invalid Directory / No Access\n")    
