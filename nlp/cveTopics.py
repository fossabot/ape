from pymongo import MongoClient
import nltk
import sys

def get_nltk():
    sys.stdout.write("[+] Downloading all NLTK Libraries")
    try:
        nltk.download("All")
        sys.stdout.write("[+] DoneDownloading")
    except Exception as e:
        sys.stderr.write("[-] Error in Downloading, Try later")
        sys.stderr.write('Exception:\n{}'.format(e))


def get_db():
    # Create a mongodb client
    client = MongoClient("mongodb://localhost:27017")
    # Connect to mongodb vFeed database
    db = client.vFeed
    # Return database connection client for vFeed
    return db

if __name__ = '__main__':
    get_nltk()
