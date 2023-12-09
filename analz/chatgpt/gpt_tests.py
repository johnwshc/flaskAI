import datetime

from analz.ai.socgpt import  NextRecessionPost as NR
from analz.feeds.feedly_api import FeedlyAPI, Feed
from analz.ai.socgpt import PDFContent, Summaries, Summary, EContent
from config import Config
from app.jinjautils import JinjaUtils as JU
import os


class SummaryManager:
    labels = ['economics', 'marxism', 'research']
    image_resources = {
        "nr_KarlMarxLnk":
            "https://accesspartnership.com/wp-content/uploads/2022/04/karl-marx-5299055_1280-e1596016530198.jpg",
        "lenin_in_disguise":
            "https://pbs.twimg.com/media/FF_n1lPX0AcM207.jpg"
        }

    sample_inputs = {
        'summaries': [Summary,],
        'authors': [{"name": "joe", 'about': 'asshole'},],
        'dates_published': [datetime.datetime.now().strftime("%m/%d/%Y"),]
    }
    sample_publish_props = {
        'imagelink': image_resources['lenin_in_disguise'],
        'template': 'se_ai_post_content.html',
        'about': 'Lenin In Disguise: Making a Comeback.',
        'blogname': 'socialist-economics',
        'title': 'The Marxist Summaries',
        'date': 'November 20, 2023',
        'heading': 'ChatGPT-assisted summaries of blog posts by Michael Roberts, a UK Marxist economist.'
   }

    def sync_orig_published(self):

        for e in self.econtents:
            eurl = e.url
            print(eurl)
            op = e.entry.orig_published
            print(f"e_orig_pub: {e.orig_published}")
            if op:
                summ = self.Summaries.get_summary_by_url(eurl)
                if summ:
                    print(f"found matching summ title: {summ.url}")
                    rsumm = self.Summaries.remove_by_url(summ.url)
                    rsumm.orig_published = op
                    self.Summaries.add_summary(rsumm)
                    print(f"updated summary: {rsumm.title} with orig_published: {rsumm.orig_published}")
                else:
                    print("failed to find econtent.title in summaries ")
            else:
                print("econtent obj has no orig_published value. ")



    @staticmethod
    def get_summary_manager():
        sm = SummaryManager()
        return sm

    def __init__(self, feed_update=False):

        self.workflows = [] # generate 5 Next Recession Summaries
        if os.path.exists(Config.SUMMARIES_JSON):
            print(f"json db exists, {Config.SUMMARIES_JSON}")
            self.Summaries = None
        else:
            self.summaries = None
        self.gt = GTests(update=feed_update)
        self.feeds = self.gt.fapi.feeds
        self.entries = []
        self.ju = JU()

    def loadSummaryDB(self):
        self.Summaries = Summaries()


    def setProdWorkFlow(self, feed_id ,  build=False):
        self.entries = self.gt.fapi.getFeedEntries(feed_id)
        self.econtents = [EContent(e) for e in self.entries]
        if build:
            self.build_summaries()


    def getPubWorkFlow(self, summary: Summary, aabout=None):

        title = summary.title
        author = summary.author
        about = aabout if aabout else 'Unknown'
        url = summary.url
        published = summary.published if summary.published else False
        date_published = summary.date_published if summary.date_published else None
        orig_published = summary.orig_published if summary.orig_published else None
        summary_text = summary.txt


    def build_summaries(self):
        import time
        for e in self.econtents:
            if isinstance(e, EContent):
                e.gpt_fire()
                self.Summaries.summaries.append(e.gpt_summary)
                time.sleep(5)


class GTests:

    def __init__(self, update: bool = False):
        self.fapi = FeedlyAPI()
        self.fapi.initialize(update=update)
        self.nr_feed_id = 'feed/http://thenextrecession.wordpress.com/feed/'
        self.eq_feed_id = 'feed/http://equitablegrowth.org/feed'
        self.cbpp_feed_id = 'feed/http://www.cbpp.org/rss/feeds/comprehensiveTopics.xml'
        self.cp_feed_id = 'feed/http://www.cpusa.org/feed/?post_type=article'
        self.con_econ_feed_id = 'feed/http://conversableeconomist.blogspot.com/feeds/posts/default'
        self.epi_feed_id = 'feed/http://www.epi.org/feed/'
        self.davidharvey_feed_id = 'feed/http://davidharvey.org/feed/'
        self.afl_cio_feed_id = 'feed/http://blog.aflcio.org/wp-rss2.php'
        self.dns_id = 'feed/http://dollarsandsense.org/blog/feed'
        self.econ_update_feed_id = 'feed/http://economicupdate.podbean.com/feed/'
        self.china_daily_feed_id = 'feed/http://www.chinadaily.com.cn/rss/opinion_rss.xml'
        self.ecns_feed_id = 'feed/http://www.ecns.cn/rss/rss.xml'
        self.xinhua_feed_id = 'feed/http://www.xinhuanet.com/english/rss/chinarss.xml'
        self.outbrain_feed_id = 'feed/http://www.globaltimes.cn/rss/outbrain.xml'
        self.pw_feed_id = 'feed/http://www.peoplesworld.org/feed/?post_type=article'
        self.ccds_feed_id = 'feed/https://www.cc-ds.org/feed/'
        self.oul_feed_id = 'feed/https://ouleft.org/?feed=rss2'




    def get_marxist_feed_ids(self):
        feed_ids = {

                'Dollars and Sense': 'feed/http://dollarsandsense.org/blog/feed',
                'Economic Update': 'feed/http://economicupdate.podbean.com/feed/',
                'China Daily': 'feed/http://www.chinadaily.com.cn/rss/opinion_rss.xml',
                'CP China News Service': 'feed/http://www.ecns.cn/rss/rss.xml',
                'Xinhuanews': 'feed/http://www.xinhuanet.com/english/rss/chinarss.xml',
                'outbrain-Chinese PolySci': 'feed/http://www.globaltimes.cn/rss/outbrain.xml',
                'Peoples World': 'feed/http://www.peoplesworld.org/feed/?post_type=article',
                'CPUSA': 'feed/http://www.cpusa.org/feed/?post_type=article',
                'CCDS': 'feed/https://www.cc-ds.org/feed/',
                'Online University of the Left': 'feed/https://ouleft.org/?feed=rss2',
                'Mike Roberts': 'feed/http://thenextrecession.wordpress.com/feed/',
                'David Harvey': 'feed/http://davidharvey.org/feed/'
        }
        return feed_ids

    def get_mainstream_feed_ids(self):
        feed_ids = {
                'Equitable Growth':'feed/http://equitablegrowth.org/feed',
                'Center for Budget and Policy Priorities': 'feed/http://www.cbpp.org/rss/feeds/comprehensiveTopics.xml',
                'Conversable Economist': 'feed/http://conversableeconomist.blogspot.com/feeds/posts/default',
                'Economic Policy Institute': 'feed/http://www.epi.org/feed/',
                'AFL-CIO Blog': 'feed/http://blog.aflcio.org/wp-rss2.php',
                'Dean Baker -- CEPR': 'feed/http://feeds.feedburner.com/beat_the_press',
                'Dani Rodrik': 'feed/https://www.project-syndicate.org/rss/author/dani-rodrik',
                'Larry Summers': 'feed/http://larrysummers.com/feed/'
        }
        return feed_ids





    def testPDF(self):
        fn =  f"f:/python_apps/flaskAI/docs/w31794.pdf"
        pdfc = PDFContent(f"{fn}")
        return pdfc



    def getNR(self, num_entries=1):
        nrid = NR.NR_feed_id
        entries = self.fapi.getFeedEntries(nrid)[0:num_entries]

        return [NR(e) for e in entries]

    def active_feed_data(self):
        import json
        from config import Config
        fn = Config.SOC_ACTIVE
        with open(fn) as f:
            txt = f.read()
            return json.loads(txt)





















