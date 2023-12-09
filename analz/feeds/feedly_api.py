# -*- coding: utf-8 -*-
"""
Created on Mon May 21 20:13:18 2018

@author: johnc
"""

import requests
import urllib
import urllib.parse
import pprint
import json
from analz.feeds.entries import Entry
import os
from pathlib import Path, WindowsPath
import shutil
from datetime import datetime
from config import Config


pp = pprint.PrettyPrinter(indent=4)


class FeedlyAPI:
    #  static vars and methods
    __doc__ = "FeedlyAPI: Extract feeds from Feedly Aggregator"
    cbpp_feed_id = 'feed/http://www.cbpp.org/rss/feeds/comprehensiveTopics.xml'

    #  instance methods

    def __init__(self):

        self.auth_header = None
        self.api_host = 'cloud.feedly.com'
        self.conf = ERFeedlyConf(host=self.api_host)
        self.feeds = None
        # self.subs = None  # self.get_subscriptions()
        # self.feeds_ids = dict()

    def initialize(self, update=False):
        self.auth_header = self.conf.authorization
        self.subs = self.get_subscriptions(update)
        if update:
            self._save_subs_to_json()
        self.feeds = [Feed(s, self) for s in self.subs]

    def _save_subs_to_json(self):
        fn = ERFeedlyConf.subs_json
        with open(fn, "w") as f:
            json.dump(self.subs, f)

    def find_feed(self, s_expr: str):
        feeds = []
        found = False
        for f in self.feeds:

            title = f.title
            if title:
                title_l = title.lower()
                if s_expr.lower() in title_l:
                    found = True
                    feeds.append(f)




        return feeds, found

    def get_entry_ids(self, feed_id):
        # stream_id = urllib.parse.quote(feed_id)
        url = f"https://{self.api_host}/v3/streams/ids"
        auth = self.conf.authorization
        params = {"streamId": feed_id, "count": 10}
        r = requests.get(url, params=params, headers=auth)
        return r.json()

    def get_feeds_by_category(self, cats: list):
        cat_feeds = []
        for feed in self.feeds:
            categories = feed.categories
            if categories:
                for cat in categories:
                    if cat['label'] in cats:
                        cat_feeds.append(Feed(feed))

            else:
                print(f"No categories for {feed['title']}")
        return cat_feeds

    def refresh_feedly_access_token(self):
        er_conf = self.conf
        items = er_conf.get('items')

        r_token = items.get('feedly_refresh_token')
        print(f'refresh_token: {r_token}')
        path = '/v3/auth/token'
        client_id = 'feedlydev'
        client_secret = 'feedlydev'
        headers = {"Content-type": "application/json"}
        p_data = {'refresh_token': r_token, 'client_id': client_id,
                 'client_secret': client_secret, 'grant_type': 'refresh_token'}
        # print(f'post data: \n{p_data}')
        r = requests.post('https://cloud.feedly.com' + path, headers=headers, data=p_data)
        return r

    def get_subscriptions(self, update):
        subs_ep = '/v3/subscriptions'
        url = 'https://' + self.api_host + subs_ep

        if update:
            r = requests.get(url, headers=self.conf.authorization)
            # self.subs = r
            # self._save_subs_to_json()
            return json.loads(r.text)
        else:
            with open(ERFeedlyConf.subs_json) as f:
                dsubs = json.load(f)
                # print(f"dsubs:{dsubs}")
            return dsubs
    
    def get_feed(self, f_id):
        feed_path = '/v3/feeds/' + urllib.parse.quote_plus(f_id)
        print('feed_path', feed_path)
        url = 'https://' + self.api_host + feed_path
        print('url', url)
        r = requests.get(url, headers=self.conf.authorization)
        return r.json()
    
    def get_stream(self, sid, max=10):
        
        stream_path = '/v3/streams/contents'
        
        url = 'https://' + self.api_host + stream_path
        payload = {'streamId': sid, 'count': max}
        r = requests.get(url, params=payload, headers=self.conf.authorization)
        return r.json()

        # get CBPP feed, and 10 entries

    def get_raw_feed_entries(self, feed_id, max=10):
        feed_entries = self.get_stream(feed_id, max)
        # print(f"feed entries: \n{feed_entries}")
        return feed_entries.get('items')

    def getFeedEntries(self, feed_id=cbpp_feed_id):
        fentries = self.get_raw_feed_entries(feed_id=feed_id)
        # print(f"got {len(fentries)} feed entries for feed id: {feed_id}")
        # print(f" raw entry[0]:\n{fentries[0]}")
        feedEntries = [Entry(e) for e in fentries]
        # print(f"return initialized entry objects")
        return feedEntries

    
    def get_entry(self, fid, eid):
        for e in self.getFeedEntries(fid):
            if e.id == eid:
                return e
        return None

class FeedlyAccess:
    feedly_user_id = '4d7004f6-ed84-4452-8605-fad277041e08'
    feedly_pro_access_token = 'Az6qhwMFcuM4XM-f9brF4xJAFQik6rWYN8Cx4ySWKOYX2ZTp4EhjoJSjqMEtNO_S3koCUA0KwafEsDFjWXZ8glh_N8AWrE7Ajb0sPFml2pAhDtaPbr_rXQ4qV9dfLI8FmeOXbyZzNZuP10mXLrJoQ7En7ZHd8cjdHEnSmIVEpx-4XdNhFxUpFBbak0RnXhZWNWrJLwyDQsaCM7MH_aIpQypSdvHDE3xfb0MJ4MQVK6XlX7psZeCB_pDe89u3cn1IWw:feedlydev'
    feedly_refresh_token = "A_f6A_pI2XDCEpz6AS89Cygmyn0pr0ut1YGPsOjRFOg0_fnPet6eKyfQsSm_xKy5fxKRWCAljl4y3jG4F0A3-PuVucLXY5TAE6MNncXC6M10LWVVOsMpgcQ0vbxwmrWws1SVUh9EN3q2LcswX3bAXt67wpwtaLYZHA_nr6o7xSupf7o9TQrhSAIkwb7DIPKRS5SPXrshi1crewKWrThOr3Hp7GdQcw:feedlydev"
    client_id = "feedlydev"
    client_secret = "feedlydev"

    @staticmethod
    def _FAtodict():
        return {
            'feedly_user_id': FeedlyAccess.feedly_user_id,
            'feedly_pro_access_token': FeedlyAccess.feedly_pro_access_token,
            'feedly_refresh_token': FeedlyAccess.feedly_refresh_token,
            'client_id': FeedlyAccess.client_id,
            'client_secret': FeedlyAccess.client_secret
        }

    @staticmethod
    def FA_selected_keys(keys: list):
        if len(FeedlyAccess._FAtodict().keys()) < len(keys):
            raise Exception(f"too many keys in {keys}")
        if not keys:
            raise Exception(f"no keys found. ")

        return {  k:v for k,v in FeedlyAccess._FAtodict().items() if k in keys }


    @staticmethod
    def load_conf():
        with open(Config.FEEDLY_CONF_JSON) as f:
            return json.load(f)


    @staticmethod
    def save_conf():

        # rename old file

        cfile  = Config.FEEDLY_CONF_JSON
        if not os.path.exists(cfile):
            with open(cfile, "w") as f:
                json.dump(FeedlyAccess._FAtodict(), f)
            print(f"saved {cfile} without error")
        else:
            pcf = Path(cfile)
            ts_ext = str(datetime.timestamp(datetime.now())).split('.')[0]
            old_file = f"{pcf.parents[0]}\\{pcf.stem}_{ts_ext}.{pcf.suffix}"
            os.rename(cfile, old_file)
            with open(cfile, "w") as f:
                json.dump(FeedlyAccess._FAtodict(), f)
            print(f"saved {cfile} without error")
#         write to json file

class ERFeedlyConf:
    #   ###################### FEEDLY API ##########################


    json_file = Config.FEEDLY_CONF_JSON
    subs_json = 'f:\\python_apps\\flaskAI\\json\\feedly\\fsubs2.json'
    entries_json = 'f:\\python_apps\\flaskAI\\json\\feedly\\fentries.json'


    def __init__(self, host):
        # self.feedly_radio_titles = self.get_radio_titles()
        # self.soc_econ_titles = self.get_soc_econ_titles()
        self.host = host
        self.auth_types = ('Bearer ', 'OAuth ')
        self.access_token = FeedlyAccess.feedly_pro_access_token
        self.refresh_token = FeedlyAccess.feedly_refresh_token
        self.feedly_userid = FeedlyAccess.feedly_user_id
        self.authorization = {'Authorization': self.auth_types[1] + self.access_token}

    def get_auth_token(self):
        data = {'response_type': 'code',
                'client_id': 'feedlydev',
                'redirect_uri': 'https"//localhost:8080',
                'scope': 'https://cloud.feedly.com/subscriptions'
                }
        url = f"https://{self.host}/v3/auth/auth"
        print(f"url: {url}")
        headers = {'Content-type': 'application/json'}
        res = requests.get(url=url, headers=headers,  data=data)
        return res


#         GET /v3/auth/auth
# This call must use the HTTPS endpoint.
    # Feedly will return an error if you try to use the HTTP endpoint.
#
# Input
#   response_type
#       string Indicates the type of token requested.
#       At this time, this field will always have the value 'code'
#   client_id
#       string:  Indicates the client that is making the request.
    #       The value passed in this parameter must exactly
    #       match the value set during the partnership program.
#   redirect_uri
#       string: Determines where the response is sent.
    #       The value of this parameter must exactly match
    #       one of the values set during the partnership program
    #       (including case, and trailing ‘/’). If it is a URL,
    #       it must use HTTPS. Make sure this parameter is URL-encoded!
    #       On sandbox, the default list includes “http://localhost”,
    #       “http://localhost:8080” and “urn:ietf:wg:oauth:2.0:oob”.
#   scope
#       string: only https://cloud.feedly.com/subscriptions is supported.
#   state
#       string: (optional) Indicates any state which may be useful to your application upon receipt of the response. The feedly Authorization Server roundtrips this parameter, so your application receives the same value it sent. Possible uses include redirecting the user to the correct resource in your site, nonces, and cross-site-request-forgery mitigations. Make sure this parameter is URL-encoded!

    def get_refresh_token(self):
        params = {}
        params['refresh_token'] = self.refresh_token
        params['client_secret'] = 'feedlydev'
        params['client_id'] = 'feedlydev'
        # params['Authorization'] = self.auth_types[1]
        params['grant_type'] = 'refresh_token'
        rt_path = '/v3/auth/token'
        url = f'https://{self.host}{rt_path}'
        res = requests.post(url,json=params)
        return res


    def get_radio_titles(self):
        rtitle_cats = ["radio"]
        with open(ERFeedlyConf.subs_json) as f:
            doc = f.read()
            jdoc = json.loads(doc)
            subs = jdoc[0]
            titles = []
            for s in subs:
                for c in s['er_category']:
                    if c in rtitle_cats:
                        titles.append(s['title'])
                        break
            return titles


    def get_soc_econ_titles(self):
        se_title_cats = ["econ", "labor", "china", "socialism"]
        with open(ERFeedlyConf.subs_json) as f:
            doc = f.read()
            jdoc = json.loads(doc)
            subs = jdoc[0]
            titles = []
            for s in subs:
                for c in s['er_category']:
                    if c in se_title_cats:
                        titles.append(s['title'])
                        break
            return titles

    def dic_to_json_file(self):
        js = json.dumps(self.conf, indent=4, sort_keys=True)
        fp = open(self.json_file, 'w')
        # write to json file
        fp.write(js)

        # close the connection
        fp.close()

    def json_file_to_dic(self):
        with open(self.json_file) as js:
            dic = json.load(js)
            js.close()
            return dic

    def download_file(self, url):

        local_dir = 'f:\\python_apps\\flaskER\\feeds\\downloads\\'
        local_filename = local_dir + (url.split('/')[-1])
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush() commented by recommendation from J.F.Sebastian
            f.close()
        return local_filename

    @staticmethod
    def get_local_track_data(filename):
        pass

        # audiofile = eyed3.load(filename)
        # p = Path(filename)
        #
        #
        # dtrack_temp = Track.get_local_track_template()
        #
        # dtrack_temp['file'] =
        # audiofile.tag.artist = u"Integrity"
        # audiofile.tag.album = u"Humanity Is The Devil"
        # audiofile.tag.album_artist = u"Integrity"
        # audiofile.tag.title = u"Hollow"
        # audiofile.tag.track_num = 2
        #
        # audiofile.tag.save()


class Feed:

    def __init__(self, dfeed: dict, fapi: FeedlyAPI):
        self.fapi = fapi
        # print(f"dfeed: {dfeed}")
        self.feedly_feed = dfeed
        self.id = dfeed['id']  # required
        self.title = dfeed.get('title', None)
        self.website = dfeed.get('website', None)
        self.categories = dfeed.get('categories', None)
        self.num_subscribers = dfeed.get('subscribers', None)
        self.iconUrl = dfeed.get('iconUrl', None)
        self.visualUrl = dfeed.get('visualUrl', None)
        self.labels: list = dfeed.get('topics', None)


    def to_dict(self):
        return self.feedly_feed

    @staticmethod
    def from_dict(d: dict, fapi: FeedlyAPI):
        return Feed(d, fapi)

    def setLabels(self, labels: list):
        self.labels = labels

    def addLabel(self, label: str):
        self.labels.append(label)

    def addLabels(self, labels: list):
        self.labels.extend(labels)


    def getEntries(self):
        entries = self.fapi.getFeedEntries(feed_id=self.id)
        return entries


#     """
#
# //Your user id is 4d7004f6-ed84-4452-8605-fad277041e08
# Youraccess token:
# AxxXNZK9UVO4Ic1Y8OJxXd-WYWvi2j5EYtKAmjWx9SvBpMsWDrF5pPCE9xaMEHleNi3EVUs5-wkrhFg2PL8r4RIiHJUZuOSNGV9boDjfqb1Wx7PxY2tons24hN8mQP06HJhd7zoWIjfRcHpkVXoINR7QYynv-ojMRGqLOXFl2G2t1K-LJD2_NbWaMcdbeS4CToQphm9ImRNPTHczSVkJOEqjHzHqlDMw8rlmdjoEXzO4bbHSrgxP9bLw0uCjlrSOJA:feedlydev
#
# (expires on Wed Aug 09 2023 15:08:12 GMT-0400 (Eastern Daylight Time))
#
# Your refresh token (help):
# Ayx2sjbFbFEY9HeipAt1LyK49tng43DpVIGpMY5qusNPbdSF56G0NOIjeoDPUbH1E14fiOU9RwLLw3mDWCOXqYzAtSXUNA_4wJnEKHPSs3fNRf_ScCo8xCIYmzXfWNFc33wh6WEuKDiItPqGe51sxlwFO8yUS4_cygw0No78hctdVSCtG5c4VGn3uj2aZJLIfn3hg3F8LjeRS6FCnJhwqqVBCMBFvA:feedlydev
#
#
# Do not share your tokens!
#
#     """