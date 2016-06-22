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
    return "https://www.openhub.net/"

def email_to_md5(emailAddress):
    email = hashlib.md5()
    email.update(emailAddress)
    return str(email.hexdigest())


# Take API Key and return URL Encoded
def setOhlohAPIkey():
    apiKey = ''
    with open('openhub.conf', 'r') as OhlohConf:
        apiKey = OhlohConf.readline().strip()
    return urllib.urlencode({'api_key': apiKey, 'v': 1})

def setOhlohPathType(path):
    OhlohPaths = {"people":'accounts', 'organization':'org', 'project': 'p' }
    return OhlohPaths[path]

def preParse(OhlohBaseURL, OhlohPath, searchAttr, params):
    if OhlohPath == 'accounts':
        searchAttr = email_to_md5(searchAttr)
    OhlohFormedURL = "{0}{1}/{2}.xml?{3}".format(OhlohBaseURL, OhlohPath, searchAttr, params)
    return OhlohFormedURL


def xmlDocTree(OhlohFormedURL):
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
    print(elementTree)
    for node in elementTree.find("result/account"):
        if node.tag == "kudo_score":
            print "%s:" % node.tag
            for score in elem.find("result/account/kudo_score"):
                print "\t%s:\t%s" % (score.tag, score.text)
        else:
            print "%s:\t%s" % (node.tag, node.text)

def parse_project(elementTree):
    foundTags = []
    for node in elementTree.find("result/project/tags"):
        foundTags.append(node.text)
    if foundTags:
        return foundTags
    else:
        return ["No Tags Found!"]
def parse_organization(elementTree):
    raise NotImplementedError


def parser_not_found():
    print("[-] Error in inputs, please verify")
    raise NotImplementedError


if __name__ == '__main__':
    requstedPath = sys.argv[1]
    OhlohPath = setOhlohPathType(requstedPath)
    searchAttr = sys.argv[2]
    params = setOhlohAPIkey()
    baseURL = setOhlohBaseURL()
    OhlohAbsURL = preParse(OhlohBaseURL= baseURL,OhlohPath=OhlohPath, searchAttr=searchAttr, params=params)
    elementTree = xmlDocTree(OhlohAbsURL)
    if requstedPath == 'people':
        parse_people(elementTree=elementTree)
    elif requstedPath == 'organization':
        parse_organization(elementTree=elementTree)
    elif requstedPath == 'project':
        print(parse_project(elementTree=elementTree))
