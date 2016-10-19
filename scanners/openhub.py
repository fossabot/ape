# Original SourceCode
# https://github.com/blackducksoftware/ohloh_api/blob/master/examples/account_sample.py
"""
The MIT License (MIT)
Copyright (c) 2013 Thijs Triemstra
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
This is an example of using the Ohloh API from Python.
Detailed information can be found on GitHub:
     https://github.com/blackducksw/ohloh_api
This example uses the ElementTree library for XML parsing
(included in Python 2.5 and newer):
     http://effbot.org/zone/element-index.htm
This example retrieves basic Ohloh account information
and outputs it as simple name: value pairs.
Pass your Ohloh API key as the first parameter to this script.
Ohloh API keys are free. If you do not have one, you can obtain one
at the Ohloh website:
     https://www.openhub.net/accounts/<your_login>/api_keys/new
Pass the email address of the account as the second parameter to this script.
"""

'''
 Changes Inclusion Update
 Copyright (c) 2016
 Author: Sai Uday Shankar Korlimarla
 Email: skorlimarla@unomaha.edu
'''

import sys
import urllib
import hashlib
from os.path import expanduser

from pymongo import MongoClient

# import ElementTree based on the python version
'''
# Hailmary elementtree imports
# using xml.etree for now
try:
  import elementtree.ElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET
'''
import xml.etree.ElementTree as ET
# We pass the MD5 hash of the email address


def setOhlohBaseURL():
    '''
    Ohloh base URL is https://www.openhub.net/
    '''
    return "https://www.openhub.net/"

def email_to_md5(emailAddress):
    '''
    emailAddress: Address of a person to be found on Ohloh
    email_to_md5 returns MD5 hexdigest
    '''
    email = hashlib.md5()
    email.update(emailAddress)
    return str(email.hexdigest())



def setOhlohAPIkey():
    '''
    Read Ohloh API Key from configuration file
    '''
    apiKey = ''
    home = expanduser("~")
    file = home + '/.apeconfig/openhub.conf'
    with open(file, 'r') as OhlohConf:
        apiKey = OhlohConf.readline().strip()
    return urllib.urlencode({'api_key': apiKey, 'v': 1})

def setOhlohPathType(path):
    '''
    Choice of paths on Ohloh:
        Usage:
            Choose one of (people, organization, project)
    '''
    OhlohPaths = {"people":'accounts', 'organization':'org', 'project': 'p' }
    return OhlohPaths[path]

def preParse(OhlohBaseURL, OhlohPath, searchAttr, params):
    '''
    Construct a URL for Ohloh API
        Args: OhlohBaseURL, path, search attributes and params (API Key)
        Warning: if something other than email is used, hexdigest is still produced

    '''
    if OhlohPath == 'accounts':
        searchAttr = email_to_md5(searchAttr)
    OhlohFormedURL = "{0}{1}/{2}.xml?{3}".format(OhlohBaseURL, OhlohPath, searchAttr, params)
    return OhlohFormedURL


def xmlDocTree(OhlohFormedURL):
    '''
    Read a URL and return XML object of Ohloh results
    Args:
        Ohloh URL to access Ohloh API
    '''
    f = urllib.urlopen(OhlohFormedURL)
    # Parse the response into a structured XML object and return
    tree = ET.parse(f)
    elementTree = tree.getroot()
    error = elementTree.find("error")
    if error:
        print('Ohloh returned:', ET.tostring(error))
        sys.exit(-1)
    return elementTree

def parse_people(elementTree):
    '''
    Parse and Pick content if path choice is people
    Args:
        elementTree from xmlDocTree
    '''
    for node in elementTree.find("result/account"):
        if node.tag == "kudo_score":
            print "%s:" % node.tag
            for score in elem.find("result/account/kudo_score"):
                print "\t%s:\t%s" % (score.tag, score.text)
        else:
            print "%s:\t%s" % (node.tag, node.text)

def parse_project(elementTree):
    '''
    Parse and pick content if path choice is project
    Args:
        elementTree from xmlDocTree
    Return:
        1. Tags for project are returned
    '''
    openhubData = {}
    tags = []
    facts = {}
    languages = {}
    logo = ''
    loc = ''
    commitcount = ''
    main_lang = ''
    activity_index = {}
    description = ''
    url = ''
    created_at = ''
    updated_at = ''
    rating = ''
    rating_count = ''
    review_count = ''
    project_id = ''
    project_name = ''
    
    if elementTree.find("result/project/name") is not None:
        project_name = elementTree.find("result/project/name").text
    if elementTree.find("result/project/id") is not None:
        project_id = elementTree.find("result/project/id").text
    if elementTree.find("result/project/tags") is not None:
        for node in elementTree.find("result/project/tags"):
            tags.append(node.text.strip())
    if elementTree.find("result/project/analysis/factoids") is not None:
        for node in elementTree.find("result/project/analysis/factoids"):
            facts[node.attrib['type'].strip()] = node.text.strip()
    if elementTree.find("result/project/analysis/languages") is not None:
        for node in elementTree.find("result/project/analysis/languages"):
            languages[node.text.strip()] = node.attrib['percentage'].strip()
    logo = ''
    if elementTree.find("result/project/small_logo_url") is not None:
        #print elementTree.find("result/project/small_logo_url") 
        logo = elementTree.find("result/project/small_logo_url").text
    if elementTree.find("result/project/analysis/total_code_lines") is not None: 
        loc = elementTree.find("result/project/analysis/total_code_lines").text
    if elementTree.find("result/project/analysis/total_commit_count") is not None:
        commitcount = elementTree.find("result/project/analysis/total_commit_count").text
    if elementTree.find("result/project/analysis/main_language_name") is not None:
        main_lang = elementTree.find("result/project/analysis/main_language_name").text
    if elementTree.find("result/project/project_activity_index"): 
        for node in elementTree.find("result/project/project_activity_index"):
            activity_index[node.tag] = node.text
    if elementTree.find("result/project/description") is not None:
        description = elementTree.find("result/project/description").text
    if elementTree.find("result/project/url") is not None:
        url = elementTree.find("result/project/url").text
    if elementTree.find("result/project/updated_at") is not None:
        updated_at = elementTree.find("result/project/updated_at").text
    if elementTree.find("result/project/created_at") is not None:
        created_at = elementTree.find("result/project/created_at").text
    if elementTree.find("result/project/average_rating") is not None:
        rating = elementTree.find("result/project/average_rating").text
    if elementTree.find("result/project/rating_count") is not None:
        rating_count = elementTree.find("result/project/rating_count").text
    if elementTree.find("result/project/review_count") is not None:
        review_count = elementTree.find("result/project/review_count").text

    openhubData['project_id'] = project_id
    openhubData['project_name'] = project_name
    openhubData['facts'] = facts
    openhubData['tags'] = tags
    openhubData['languages'] = languages
    openhubData['logo'] = logo
    openhubData['loc'] = loc
    openhubData['commitcount'] = commitcount
    openhubData['main_lang'] = main_lang
    openhubData['activity_index'] = activity_index
    openhubData['description'] = description
    openhubData['url'] = url
    openhubData['created_at'] = created_at
    openhubData['updated_at'] = updated_at
    openhubData['rating'] = rating
    openhubData['rating_count'] = rating_count
    openhubData['review_count'] = review_count

    return openhubData

def parse_organization(elementTree):
    '''
    *******************************
    * This is not yet implemented *
    *******************************
    Parse and pick content if path choice is organization
    Args:
        elementTree from xmlDocTree
    '''
    raise NotImplementedError

def insert_into_database(openhubData, upload_id):
    mongo_url = 'mongodb://localhost:27017/'
    client = MongoClient(mongo_url)
    ape_db = client['apedb']
    openhub = ape_db.openhub
    uploads = ape_db.uploads
    uploads.update({'_id': upload_id},{'$set': {'logo': openhubData['logo']}})
    if openhub.find_one(openhubData) is None:
        post_id = openhub.insert_one(openhubData).inserted_id
        return post_id
    else:
        existing = ''
        existing = openhub.find_one(openhubData)
        return existing['_id']

if __name__ == '__main__':
    requstedPath = sys.argv[1]
    searchAttr = sys.argv[2]
    OhlohPath = setOhlohPathType(requstedPath)
    searchAttr = sys.argv[2]
    upload_id = sys.argv[3]
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
        mid = insert_into_database(openhubData, upload_id)
        sys.stdout.write(str(mid))
