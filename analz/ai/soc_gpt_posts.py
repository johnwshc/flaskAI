from analz.chatgpt.socgpt import EContent, Para, Prompt, SocEconGPT
from analz.chatgpt.er_gpt_prompts import NRPrompts, EQPrompts
# from analz.feeds.feedly_api import FeedlyAPI, Feed
from analz.feeds.entries import Entry
# import json
# from config import Config
import requests
from bs4 import BeautifulSoup as BS
import time


class EQGrowthPost(EContent):

    def __init__(self, entry: Entry):
        super().__init__(entry)
        self.prompts = []
        self.about = self.getEQAbout()
        self.gpt_summary = None

    def initialize(self):
        for p in self.prompt_texts:
            # print(f"num words in prompt: {p.num_words}")
            prompt_str = EQPrompts(p).prompt_str_1

            dprompt = Prompt(p, prompt_str)
            self.prompts.append(dprompt)
        self.gpt_summary = self.summarizeEntry(self.prompts)

    @staticmethod
    def getEQAbout():
        eq_about_url = 'https://equitablegrowth.org/who-we-are/about-us/'
        r = requests.get(eq_about_url)
        bs = BS(r.text)
        soup_paras = bs.findAll('p')
        pars = []
        for p in soup_paras:
            txt = p.text
            txt = txt.replace('\n', '')
            txt = txt.strip()
            pars.append(txt)
        return '\n\n'.join(pars[:4])


class CBPPPost(EContent):
    # has no content, only Feedly summary. Content pages cannot be parsed by BeautifulSoup

    def __init__(self, entry: Entry):
        super().__init__(entry)
        self.prompts = []
        self.about = self.getCBPPAbout()

        self.gpt_summary = f"""
        <div>
        <h3>{self.title}</3>
        <p> 
        <a href={self.url}>Source Website</a>
        </p>
        {self.summary_text} 
        </div>
        """
        self.gpt_summary = self.gpt_summary.replace('\n', '')
        self.gpt_summary = self.gpt_summary.replace('  ', '')

    def getCBPPAbout(self):
        import json
        cbpp_about_url = 'https://www.cbpp.org/about'
        with open('analz/feeds/json/abouts.json') as f:
            d = json.load(f)
            return d['cbpp']









