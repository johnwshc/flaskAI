from analz.feeds.feedly_api import Feed, FeedlyAPI, ERFeedlyConf
from analz.feeds.entries import Entry
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd


class FeedEntryTest:
    cbpp_feed_id =  'feed/http://www.cbpp.org/rss/feeds/comprehensiveTopics.xml'

    def __init__(self):
        self.fapi = FeedlyAPI()
        self.fapi.initialize()

        # get CBPP feed, and 10 entries
    def get_feed_entries(self, feed_id=cbpp_feed_id, max=10 ):
        cbpp_entries = self.fapi.get_stream(feed_id)
        return cbpp_entries.get('items')

    def getFeedEntries(self,feed_id=cbpp_feed_id):
        cbpp_entries = self.get_feed_entries(feed_id=feed_id)
        feedEntries = [Entry(e) for e in cbpp_entries]
        return feedEntries

    def feed_entries_report(self):
        summaries = []
        title_fids = self.fapi.feeds_ids
        for ftitle, fid in title_fids.items():
            entries = self.fapi.getFeedEntries(feed_id=fid)
            for e in entries:
                if e.hasSummary:
                    summaries.append({'feed_title': ftitle,
                                      'entry title': e.title,
                                      'summary_len': e.summary_len
                                      }
                                     )
        return summaries

    def parseSummaries2df(self, sums: list):
        ftitles = []
        etitles = []
        sumlens = []
        for s in sums:
            if s['feed_title']:
                ftitles.append(s['feed_title'])
            else:
                ftitles.append("None")
            if s['entry_title']:
                etitles.append(s['entry_title'])
            else:
                etitles.append("None")
            if s['summary_len']:
                sumlens.append(s['summary_len'])
            else:
                sumlens.append(0)
        return pd.DataFrame({'feed_title': ftitles, 'entry_title': etitles, 'summary_len': sumlens})


# pbgc cust id =  9065252


class Scraper:
    blogger_url = 'https://economics.enlightenradio.org/2023/04/dean-baker-get-over-it-china-is-bigger.html'
    proj_syn_url = 'https://www.project-syndicate.org/commentary/economic-costs-of-china-america-conflict-by-stephen-s-roach-2023-04'
    mr_fid = "feed/http://thenextrecession.wordpress.com/feed/"
    mr_nr = "https://thenextrecession.wordpress.com/2023/04/22/a-multipolar-world-and-the-dollar/"
    def __init__(self, url):
        self.r = requests.get(url)

    @staticmethod
    def getScrape(url=blogger_url, save=False):
        clean_txts = []
        if url == Scraper.blogger_url:
            sc = Scraper(url)
            bs = BS(sc.r.content, 'lxml')
            txt = bs.text
            clean_txts.append(txt.replace("\n", "").split("Posted byThe Red Caboose", maxsplit=1)[0])
        elif url == Scraper.mr_nr:
            sc = Scraper(url)
            return [sc.r.content]

        else:
            pass
        return clean_txts

        # if save:
        #     with open(f"html_scrapes/blogger_raw.html", "w") as f:
        #         f.write(sc.r.content)






