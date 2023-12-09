import datetime
import json
# import time
# from typing import Dict
import openai
import os
import requests
from config import Config
from analz.feeds.entries import Entry
# from bs4 import BeautifulSoup as BS
import PyPDF2
from bs4 import BeautifulSoup

class Chunk:
    def __init__(self, txt):
        wl = lambda x: len(x.split(' '))
        self.txt = txt
        self.num_words = wl(self.txt)
        self.num_tokens = int(self.num_words / .75)

class Prompt:
    def __init__(self, ch: Chunk):
        self.chunk = ch
        self.txt = ch.txt
        self.prompt_str = None

    def _initialize(self, pstr ):
        self.prompt_str = pstr

class Summary:
    test_dt_str = "Jun 23 2022 07:31PM"

    @staticmethod
    def convert_datestr2datetime(datestr=test_dt_str):
        from dateutil import parser
        DT = parser.parse(datestr)
        return DT

    def __init__(self,
                 txt,
                 title,
                 author,
                 url,
                 dprod: datetime.datetime,
                 opub: datetime.datetime=None,
                 dpub: datetime.datetime=None,
                 id: str=None,
                 published: int=0):


        self.txt = txt
        self.title = Summary.capitalizeEachWord(title)
        self.date_produced = dprod
        if id:
            self.id = id

        else:
            self.id = REUtils.replaceNonAlphaNumericChars(f"{self.title}{str(self.orig_published.timestamp())}")
        self.author = Summary.capitalizeEachWord(author)  # comma separated list in string
        self.url = url

        self.orig_published = opub
        if published:
            self.published = True
        else:
            self.published = False
        if dpub and isinstance(dpub, datetime.datetime):
            self.date_published = dpub
            self.published = True
        else:
            self.published = False
            self.date_published = None

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)


    def setPublished(self):
        d = datetime.datetime.now()
        self.date_published = d
        self.published = True

    # def setOrigPublished(self, date: datetime.datetime):
    #     self.orig_published = date

    def getOrigPublisheDT(self):
        return self.orig_published

    def getOrigPublishedSTR(self):
        return self.orig_published.strftime("%B %e, %Y")

    def to_dict(self):
        dd = {
            'txt': self.txt,
            'title': self.title,
            'author': self.author,
            'url': self.url,
            'id': self.id,
            'date_produced': str(self.date_produced)

        }
        if self.orig_published:
            dd['orig_published'] = str(self.orig_published)
        if self.published:
            dd['published'] = 1
            dd['date_published'] = str(self.date_published)
        else:
            self.published = 0
        return dd

    @staticmethod
    def from_dict(d: dict):
        dprod = Summary.convert_datestr2datetime(d['date_produced'])
        is_p = d.get('published', 0)

        if is_p:
            dpub = Summary.convert_datestr2datetime(d.get('date_published'))
        else:
            dpub = None
        opub = d.get('orig_published', None)
        if opub:
            opub = Summary.convert_datestr2datetime(d.get('orig_published'))

        return Summary(
            d['txt'],
            d['title'],
            d['author'],
            d['url'],
            dprod,
            opub=opub,

            id=d.get('id', None),
            published=is_p,
            dpub=dpub if is_p else None

        )

    # def save_to_json(self):
    #     from filelock import FileLock
    #     import os
    #     lock = FileLock("file.lock")
    #     summaries_json = Config.SUMMARIES_JSON
    #     with lock:
    #         if os.path.exists(summaries_json):
    #             with open(summaries_json ) as f:
    #                 data = json.load(f)
    #                 data.append(self.to_dict())
    #             with open(summaries_json, "w") as f:
    #                 json.dump(data, f)
    #         else:
    #             with open(summaries_json, "w") as f:
    #                 json.dump(self.to_dict(), f)



    @staticmethod
    def capitalizeEachWord(s: str):
        words = s.split(' ')
        cwords = list(map(str.capitalize, words))
        return ' '.join(cwords)

class Summaries:
    def __init__(self):
        print(f"In Summaries.__init__")
        self.summaries = Summaries.getSummaries(Config.SUMMARIES_JSON)


    def isDuplicate(self, s: Summary):
        for ss in self.summaries:
            if ss == s:
                return True
        return False


    def add_summary(self, s: Summary):

        try:

            if self.isDuplicate(s):
                raise Exception("duplicate Summary Add Not Allowed")
            else:
                self.summaries.append(s)
                self.summaries = sorted(self.summaries, key=lambda x: x.date_produced, reverse=True)

        except Exception as inst:
            print(inst)

    def get_summaries_by_author(self, auth:str):
        return [s for s in self.summaries if auth in s.author]

    def get_summary_by_title(self, title: str):
        lc = [s for s in self.summaries if title == s.title]
        if lc:
            return lc[0]
        else:
            return None

    def get_summary_by_url(self, url: str):
        lc = [s for s in self.summaries if s.url == url]
        if lc:
            return lc[0]
        else:
            return None

    def get_summary_by_id(self, sid):
        for s in self.summaries:
            if sid == s.id:
                return s
        return None



    def remove_by_url(self, url):
        r_summ = None
        for i in range(len(self.summaries)):
            if self.summaries[i].url == url:
                r_summ = self.summaries.pop(i)
                return r_summ


    def list_by_title(self):
        tlist = [s.title for s in self.summaries]
        return tlist

    def list_by_author(self):
        return [s.author for s in self.summaries]

    def list_by_unpublished(self):
        return [s.id for s in self.summaries if not s.published]

    def list_by_published(self):
        return [s.id for s in self.summaries if s.published]

    def list_by_title_auth_url(self):
        return [(s.title, s.author, s.url, s.published) for s in self.summaries ]

    def list_by_date_produced(self):
        dates_produced = sorted(self.summaries, key= lambda s: s.date_produced, reverse=True)

    @staticmethod
    def fix_id(sd: dict):
        new_d = {'txt':sd['txt'], 'title': sd['title'], 'author': sd['author'], 'url': sd['url'],
                'date_produced': sd['date_produced'] }
        dtdp = Summary.convert_datestr2datetime(sd['date_produced'])
        ts = dtdp.timestamp()
        ids = f"{sd['title']}{str(ts)}"
        new_d['id'] =  REUtils.replaceNonAlphaNumericChars(ids)
        return new_d

    @staticmethod
    def getSummaries(json_fn: str):
        try:
            with open(json_fn) as f:



                data = json.load(f)
                sdata = [Summary.from_dict(d) for d in data]
                return sdata
        except Exception as inst:
            print(f" Error loading json summaries file: {Config.SUMMARIES_JSON}, ex: {inst}")

    def saveSummaries(self):
        import shutil
        from filelock import FileLock
        from pathlib import Path
        lock = FileLock("file.lock")
        with lock:
            if os.path.exists(Config.SUMMARIES_JSON):
                tss = str(datetime.datetime.now().timestamp())
                old_fn = f"{Path(Config.SUMMARIES_JSON).name}_{tss}.old"
                shutil.copy(Config.SUMMARIES_JSON,f"{Config.SUMMARIES_DIR}/{old_fn}")
            with open(Config.SUMMARIES_JSON, "w") as f:
                ssummaries = [s.to_dict() for s in self.summaries]
                json.dump(ssummaries, f)

# class for making gpt queries for soc econ
class SocEconGPT:
    openai.api_key = Config.OPENAI_SECRET_KEY

    @staticmethod
    def get_completion(prompt, model="gpt-3.5-turbo"):
        # Andrew mentioned that the prompt completion paradigm is preferable for this class

        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,  # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]

class REUtils:
    @staticmethod
    def replaceNonAlphaNumericChars(s:str):
        import re
        return re.sub('[^0-9a-zA-Z]+', '_', s)
    
    @staticmethod
    def get_sentences(txt):
        import re
        tpat1 = r'([A-Z][^\.!?]*[\.!?])'
        pat = re.compile(tpat1, re.M)
        sentences = pat.findall(txt)
        return sentences

    @staticmethod
    def compute_chunks(sentences, chunk_size=700 ):
        wl = lambda x: len(x.split(' '))
        sensums = []
        chunks = []
        for s in sentences:
            nw = wl(s)
            sensums.append((nw,s))

            chunk_sum = sum([x[0] for x in sensums])
            if chunk_sum >= chunk_size:
                sens = [ss[1] for ss in sensums]
                ctxt = ' '.join(sens)
                chunks.append(Chunk(ctxt))
                sensums.clear()

        return chunks

class EContent:
    shared_token_limit = 4097  # tokens shared between prompt and completion.
    response_completion_token_limit = 1000
    prompt_token_limit = 3000
    shared_words_limit = shared_token_limit * .75
    prompt_word_limit = prompt_token_limit * .75
    response_word_limit = response_completion_token_limit * .75
    test_fl = "f:\\python_apps\\flaskER\\html_scrapes\\MRBlog.html"
    test2_fl = "f:\\python_apps\\flaskER\\html_scrapes\\text.txt"
    prompt_props: dict[str, int] = {
        'prompt_size': 750,
        'response_size': 500
    }

    # EContent instantiation parameters:
    #   -- entry: an Entry object representing a FeedlyAPI JSON feed item (article)
    #   -- psize: default prompt text chunk size (suitable for GPT completion)
    #   -- rsize: suggested GPT response size, in words

    def __init__(self, entry: Entry, props=prompt_props):
        self.wl = lambda x: len(x.split(' '))
        self.entry = entry
        self.orig_published = entry.orig_published
        self.id = self.entry.eid  #  The eid is used throughout this app shared 1:1 with its summary
        self.fid = self.entry.id  #  The feedly rss service id.

        self.author = self.entry.author if self.entry.author else 'Unknown'
        self.prompt_text_size = props['prompt_size']
        self.response_text_size = props['response_size']
        self.title = entry.title
        self.url = entry.url
        self.hasSummary = True if entry.summary else False
        self.hasContent = True if entry.content else False

        if self.hasContent:

            self.content_text = entry.content

        else:
            if not self.hasSummary:
                raise Exception(f"No summary or content in entry: {entry.title}")

            self.summary_text = entry.summary
            self.content_text = entry.summary

        self.content_word_len = self.wl(self.content_text)
        self.chunks = self.entry.chunks

    def gpt_fire(self, recursive=True):

        if recursive:
            orig_published = self.entry.orig_published
            try:
                tsummary = EContent.get_generic_recursive_summary(self.chunks)
                self.gpt_summary = Summary(tsummary, self.title, self.author, self.url,
                                           datetime.datetime.now(), None)


            except Exception as inst:
                print(inst)
                raise inst

        else:
            try:
                tsummary = EContent.summarize_by_parts(self.chunks)
                self.gpt_summary = Summary(tsummary, self.title, self.author, self.url,
                                           datetime.datetime.now(), None)

            except Exception as inst:
                print(inst)
                raise inst


    # This summarize method separately summarizes chunks of a document
    #   larger than OpenAI token limits will handle at once, approx 3k words
    #      (2K, counting response sizes -- se_summaries -- ranging from 300 to 1K words)
    #
    #  This method simply joins the separate chunk summries

    @staticmethod
    def summarize_by_parts(chunks):
        from analz.ai.prompts import GenSEPrompt
        summaries = []

        for c in chunks:
            prompt_obj = Prompt(c)
            prompt_str = GenSEPrompt.prompt_1(prompt_obj.txt)
            summaries.append(SocEconGPT.get_completion(prompt_str))
        if len(summaries) > 1:
            summ_join = ' '.join(summaries)
            sprompt = GenSEPrompt.prompt_combine_summaries(summ_join)
            return SocEconGPT.get_completion(sprompt)
        else:
            return summaries[0]

    @staticmethod
    def get_generic_recursive_summary(chunks, summ: str = ''):
        from analz.ai.prompts import GenSEPrompt as GP
        if len(chunks) > 0:
            chunk =  chunks.pop(0)
            chunk_txt = chunk.txt
            s_chunk = summ + chunk_txt
            prompt_str = GP.prompt_1(s_chunk)
            gpt_summary = SocEconGPT.get_completion(prompt_str)
            return EContent.get_generic_recursive_summary(chunks, summ=gpt_summary)
        else:
            return summ

class PDFContent:

    @staticmethod
    def chunk_it(x):
        return Chunk(x)

    def __init__(self, pdf_fn, chunk_size = 700):
        wl = lambda x: len(x.split(' '))
        fobj = open(pdf_fn, 'rb')
        self.pdfR = PyPDF2.PdfReader(fobj)
        self.pages = self.pdfR.pages
        num_pages = len(self.pages)
        self.text_pages = []
        for i in range(num_pages):
            self.text_pages.append(self.pages[i].extract_text())
        self.text_tups = [(p, wl(p)) for p in self.text_pages]
        self.doc_word_len = sum([x[1] for x in self.text_tups])
        self.md = self.pdfR.metadata
        self.title = self.md.title
        self.subject = self.md.subject
        self.chunk_size = chunk_size
        fobj.close()
        self.chunks = self.getChunks(self.chunk_size)


    def getChunks(self, chunk_size: int):
        wl = lambda x: len(x.split(' '))

        chunks = []
        chunkies = []

        chunkies_sum = 0
        for p in self.text_pages:

            psum = wl(p)
            chunkies.append(p)
            chunkies_sum += psum
            if chunkies_sum >= chunk_size:
                chunk = ' '.join(chunkies)
                chunks.append(chunk)
                chunkies_sum = 0
                chunkies.clear()
        last_chunk = ' '.join(chunkies)
        chunks.append(last_chunk)
        chunkies.clear()
        return list(map(PDFContent.chunk_it, chunks))


    def get_sentence_chunks(self, chunk_size=700):
        wl =  lambda x: len(x.split(' '))
        total_plain_text = ' '.join(self.text_pages)
        chunk_sentences = ''
        chunk_sentences_wl = 0
        chunks = []
        sentences = REUtils.get_sentences(total_plain_text)
        for s in sentences:
            sl = wl(s)
            chunk_sentences_wl += sl
            chunk_sentences = ' '.join([chunk_sentences, s])
            if(wl(chunk_sentences) >= chunk_size):
                chunks.append((chunk_sentences, wl(chunk_sentences)))
                chunk_sentences = ''
                chunk_sentences_wl = 0
        if chunk_sentences:
            chunks.append((chunk_sentences, wl(chunk_sentences)))

        return chunks



class GPTException(BaseException):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code


class NextRecessionPost(EContent):
    about_nr_url = "https://thenextrecession.wordpress.com/about-2/"

    @staticmethod
    def get_about_author_text(url: str):
        htm_content = requests.get(NextRecessionPost.about_nr_url).content
        txt_content = BeautifulSoup(htm_content).text
        return htm_content, txt_content



    NR_feed_id = 'feed/http://thenextrecession.wordpress.com/feed/'
    NR_default_about = """Michael Roberts worked in the City of London 
            as an economist for over 40 years. He has closely observed 
            the machinations of global capitalism from within the dragon’s 
            den. At the same time, he was a political activist in the 
            labour movement for decades. Since retiring, he has written 
            several books.  The Great Recession – a Marxist view (2009); 
            The Long Depression (2016); Marx 200: a review of Marx’s 
            economics (2018): and jointly with Guglielmo Carchedi as 
            editors of World in Crisis (2018).  He has published 
            numerous papers in various academic economic journals and 
            articles in leftist publications."""




    def __init__(self, entry: Entry, prompt_type='g'):
        super().__init__(entry)
        # choice of a) recursive, b) by parts, c) stuff the Front, g) generic
        self. prompt_type = prompt_type
        # self.prompts = []
        # self.gpt_summary = None













