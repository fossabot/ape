import mechanize
import nltk
from bs4 import BeautifulSoup
from html2text import html2text
import re
from urllib import urlopen


def clean_html(html):
    # Source: http://stackoverflow.com/questions/26002076/python-nltk-clean-html-not-implemented
    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()

url = "http://googlechromereleases.blogspot.com/2010/03/stable-channel-update.html"
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Firefox')]
html = br.open(url).read().decode('utf-8')
cleanhtml = clean_html(html)
web_text = html2text(cleanhtml)

# Tokenization
web_tokens = nltk.word_tokenize(web_text)
web_pos_tag = nltk.pos_tag(web_tokens)

text_ch = nltk.ne_chunk(web_pos_tag)
for chunk in text_ch:
    if hasattr(chunk, 'label'):
        print(chunk.label(), " ".join(c[0] for c in chunk.leaves()))
