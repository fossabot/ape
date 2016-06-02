from pymongo import MongoClient
import nltk
import sys
import mechanize
import nltk
from bs4 import BeautifulSoup
from html2text import html2text
import re
from urllib import urlopen
import pprint
import json

class cvetags:
    def __init__(self):
        # Create a mongodb client
        self.client = MongoClient("mongodb://localhost:27017")

    def vfeed_db(self):
        vfeed_db = self.client.vFeed
        # Return database connection client for vFeed -
        return vfeed_db

    #Function to clean HTML content
    # Imporve REGEX if need be
    def clean_html(self, html):
        # Source: http://stackoverflow.com/questions/26002076/python-nltk-clean-html-not-implemented
        # First we remove inline JavaScript/CSS:
        clean_html_data = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
        # Then we remove html comments. This has to be done before removing regular
        # tags since comments can contain '>' characters.
        clean_html_data = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", clean_html_data)
        # Next we can remove the remaining tags:
        clean_html_data = re.sub(r"(?s)<.*?>", " ", clean_html_data)
        # Finally, we deal with whitespace
        clean_html_data = re.sub(r"&nbsp;", " ", clean_html_data)
        clean_html_data = re.sub(r"  ", " ", clean_html_data)
        clean_html_data = re.sub(r"  ", " ", clean_html_data)
        return clean_html_data.strip()

    # Function to fetch data from URL
    # Sanitize data - get text and get rid of everything else
    # Use clean_html for cleaning html data
    def get_html_from_url(self, url):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Firefox')]
        html = br.open(url).read().decode('utf-8')
        cleanhtml = self.clean_html(html)
        clean_html_data = html2text(cleanhtml)
        return clean_html_data

    # This function presents precision vs. recall problem. precision is being sacrifised.
    def chunk_label_type(self, chunk_label):
        if (chunk_label == 'ORGANIZATION' or chunk_label == 'FACILITY' or chunk_label == 'GPE'):
            return True
        return False
    # Tokenization
    # get tokens
    # Parts of Speech tagger
    # Then chunk for ORGANIZATION or FACILITY or GPE
    # These tags can be used later for similarity - to identify CVEs
    def clean_html_to_tokens(self, clean_html_data):
        web_tokens = nltk.word_tokenize(clean_html_data)
        web_pos_tag = nltk.pos_tag(web_tokens)
        raw_chunks = nltk.ne_chunk(web_pos_tag)
        text_chunks = []
        chunk_index = 0
        for chunk in raw_chunks:
            # Uncomment this condition and comment below one - if accuracy on CVE vendor can be promised
            #if hasattr(chunk, 'label') and self.chunk_label_type(chunk.label()):
            if hasattr(chunk, 'label'):
                text_chunks.append(''.join(c[0] for c in chunk.leaves()))
        return text_chunks

    def startTextChunkGeneration(self):
            vfeed_db = cve_tagger.vfeed_db()
            # Using projection - to fetch refname filed only - for generating tags
            # _id:0 is not being used - _id is unique and is suitable for updates - cve_chunks_tag

            projection = {"refname":1, "text_chunks":1}

            count = 0
            for cve_ref in vfeed_db.cve_reference.find({}):
                count+=1
                print("[AT] {}".format(count))
                try:
                    if len(cve_ref['text_chunks']):
                        pass
                except Exception as e:
                        text_chunks = []
                        try:
                            text_chunks = cve_tagger.clean_html_to_tokens(cve_tagger.get_html_from_url(cve_ref['refname']))
                        except Exception as e:
                            pass
                        vfeed_db.cve_reference.update({'_id': cve_ref['_id'],
                                                        'refname': cve_ref['refname']},
                                                        {"$set": {
                                                            'text_chunks': text_chunks
                                                        }})
                        print("[+] Captured new chunks")
                        print(cve_ref)


            sys.stdout.write("[+] Text Chunking done!")


if __name__ == '__main__':
    cve_tagger = cvetags()
    cve_tagger.startTextChunkGeneration()
