import nltk
import html2text
import mechanize
import sys
import re

# Simulate a browser
def get_html_from_url(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]
    html = br.open(url).read().decode('utf-8')
    cleanhtml = clean_html(html)
    clean_html_data = html2text(cleanhtml)
    return clean_html_data



# Wikipedia - World war -II intorduction
def text_to_tag(text):

    text_tag = nltk.pos_tag(nltk.word_tokenize(text))
    text_ch = nltk.ne_chunk(text_tag)
    #return text_ch

    for chunk in text_ch:
        if hasattr(chunk, 'label'):
            print(chunk.label(), " ".join(c[0] for c in chunk.leaves()))


def clean_html(html):
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
def get_html_from_url(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]
    html = br.open(url).read().decode('utf-8')
    cleanhtml = clean_html(html)
    clean_html_data = html2text.html2text(cleanhtml)
    return clean_html_data

# This function presents precision vs. recall problem. precision is being sacrifised.
def chunk_label_type(chunk_label):
    if (chunk_label == 'ORGANIZATION' or chunk_label == 'FACILITY' or chunk_label == 'GPE'):
        return True
    return False
# Tokenization
# get tokens
# Parts of Speech tagger
# Then chunk for ORGANIZATION or FACILITY or GPE
# These tags can be used later for similarity - to identify CVEs
def clean_html_to_tokens(clean_html_data):
    web_tokens = nltk.word_tokenize(clean_html_data)
    web_pos_tag = nltk.pos_tag(web_tokens)
    raw_chunks = nltk.ne_chunk(web_pos_tag)
    text_chunks = []
    chunk_index = 0
    for chunk in raw_chunks:
        # Uncomment this condition and comment below one - if accuracy on CVE vendor can be promised
        #if hasattr(chunk, 'label') and chunk_label_type(chunk.label()):
        if hasattr(chunk, 'label'):
            text_chunks.append(''.join(c[0] for c in chunk.leaves()))
    return text_chunks



if __name__ == '__main__':
    text_chunks = clean_html_to_tokens(get_html_from_url(sys.argv[1]))
    print(text_chunks)
