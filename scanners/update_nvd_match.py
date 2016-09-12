from pymongo import MongoClient
import os
import sys


def update_cvss():
    client = MongoClient()
    apedb = client.apedb
    vFeed = client.vFeed

    nvd_match = apedb.nvd_match
    nvd_db = vFeed.nvd_db

    for each_match in nvd_match.find({}):
        nvd_db_entry = {}
        if nvd_db.find_one({'cveid': each_match['cveid']}):
            nvd_db_entry = nvd_db.find_one({'cveid': each_match['cveid']})
        else:
            nvd_db_entry['cvss_base'] = 0
        

        nvd_match.update({'_id': each_match['_id']}, {'$set': {'cvss_base':nvd_db_entry['cvss_base']}})
        
         



if __name__ == '__main__':
    update_cvss()
