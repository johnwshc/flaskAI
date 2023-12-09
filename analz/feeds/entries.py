
from bs4 import BeautifulSoup
import pandas as pd
import requests


class Entry:

    max_chunk_size = 750  # words
    sample_dentry = {
            'fingerprint': '950aad1',
           'id': 'AcdVjFqweq/ZcwBbEfckT+hJTP/NyQ/CXlRwVRrlNzo=_187c982c944:1901321:da597fa8',
           'language': 'en',
           'originId': 'https://www.cbpp.org/blog/in-case-you-missed-it-655',
           'origin': {'streamId': 'feed/http://www.cbpp.org/rss/feeds/comprehensiveTopics.xml',
                      'title': 'CBPP Comprehensive Reports and Blog Posts',
                      'htmlUrl': 'https://www.cbpp.org/'},
           'title': 'In Case You Missed It…',
           'author': 'CBPP',
           'crawled': 1682713004356,
           'published': 1682697220000,
           'summary': {
               'content': 'This week at CBPP, we focused primarily on House Republicans’ debt-ceiling-and-cuts bill, which seeks to force harmful policies in areas including the federal budget and taxes, health, food assistance, income security, and state budgets and taxes.The federal budget and taxes. In a statement, CBPP President Sharon Parrott said the bill puts the economy at grave risk while seeking deep, unpopular program cuts and giving billions to wealthy tax cheats. She also outlined the ten years of deep cuts that the bill would exact. Parrott, Samantha Jacoby, Allison Orris, LaDonna Pavetti, David Reich, and',
               'direction': 'ltr'},
           'alternate': [{'type': 'text/html',
                          'href': 'https://www.cbpp.org/blog/in-case-you-missed-it-655'}],
           'canonicalUrl': 'https://www.cbpp.org/blog/in-case-you-missed-it-655',
           'unread': False,
           'categories': [{'id': 'user/4d7004f6-ed84-4452-8605-fad277041e08/category/global.must',
                           'label': 'Must Read'},
                          {'id': 'user/4d7004f6-ed84-4452-8605-fad277041e08/category/economics',
                           'label': 'economics'}]
        }
    def get_raw_summary(self):
        return self.dentry['summary']['content']

    def get_raw_summary_length(self):
        return self.wl(self.get_raw_summary())

    def get_raw_content(self):
        return self.dentry['content']['content']

    def get_raw_content_length(self):
        return self.wl(self.get_raw_content())

    # #############################################################
    #     ####################  CONSTRUCTOR ##################
    # #############################################################

    def __init__(self, dentry: dict, chunk_size=750):
        import re
        from analz.ai.socgpt import REUtils
        # word count f
        self.wl = lambda x: len(str(x).split(' '))
        # get sententces
        pat1 = r'([A-Z][^\.!?]*[\.!?])'
        self.pat = re.compile(pat1, re.M)

        self.dentry = dentry
        # print(f"initializing Entry from dict \n\n{dentry}")
        # id -- string the unique, immutable  ID for this particular article.
        try:
            self.id = dentry.get('id', None)  # required
            if not self.id:
                raise Exception("Feedly source ID Required to create Entry")
            self.title = dentry.get('title', None)
            if not self.title:
                raise Exception("Feedly title Required to create Entry")
            self.url = dentry.get('url', None)
            if not self.url:
                raise Exception("Feedly url Required to create Entry")
            orig_published_ts = dentry.get('published', None)  # as reported by RSS
            if orig_published_ts:  # with feedly this will always be an int, if available
                self.orig_published = pd.to_datetime(orig_published_ts, utc=True, unit='ms')
            else:
                raise Exception("Feedly orig published date Required to create Entry")

            self.eid = REUtils.replaceNonAlphaNumericChars(f"{self.url}_{str(self.orig_published.timestamp())}")

        except Exception as le:
            raise Exception(str(le))


        psummary = self.dentry.get('summary', None)
        self.summary = psummary.get('content') if psummary else None
        pcontent = dentry.get('content', None)
        self.content = pcontent.get('content') if pcontent else None
        self.url = dentry.get('canonicalUrl', None)
        self.isHTML = "unknown"
        self.author = dentry.get('author', 'Unknown')


        self.origin = dentry.get('origin', None)
        self.categories = dentry.get('categories', None)
        self.chunks = None
        self.soup = None
        self.chunk_size = chunk_size
        self.initialize()

    def initialize(self):
        # wl = lambda x: len(str(x).split(' '))
        if not self.title:
            self.title = "unknown"
        if not self.content:
            if self.url:
                self.content = requests.get(self.url).content
                if not self.content:
                    self.content = "Not Available"
            else:
                self.content = "Not Available"

        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.isHTML = bool(self.soup.find())

        if self.isHTML:
            self.content = self.soup.text.strip()
        else:
            self.content = self.content.strip()

        self.chunks = Entry.build_chunks(self.content, self.chunk_size)


    @staticmethod
    def build_chunks(text, chunk_size):
        from analz.ai.socgpt import REUtils as RE
        from analz.ai.socgpt import Chunk
        sentences = RE.get_sentences(text)
        cword_max = chunk_size
        wl = lambda x: len(str(x).split(' '))
        chunk_text = ''
        chunk_stack =[]
        stack_sum = 0
        for s in sentences:
            nwords = wl(s)
            chunk_text = ' '.join([chunk_text, s])
            stack_sum += nwords
            if stack_sum >= cword_max:
                chunk = Chunk(chunk_text)
                chunk_stack.append(chunk)
                chunk_text = ''
                stack_sum = 0
        if chunk_text:
            chunk  = Chunk(chunk_text)
            chunk_stack.append(chunk)
            chunk_text = ''


        return chunk_stack



    def toDict(self):
        return {
            'title': self.title,
            'fid': self.fid,
            'eid': self.eid,
            'summary': self.summary,
            'content': self.content,
            'url': self.url,
            'origin': self.origin,
            'author': self.author,
            'published': self.published,
            'categories': self.categories
        }
























