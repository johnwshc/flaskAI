# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 12:36:52 2018

@author: johnc
"""

import pandas as pd
import numpy as np
from config import ERFeedlyConf
from feeds.feedly_api import FeedlyAPI
from feeds.pls_playlist import PLSPlaylist
import json
from feeds.tracks import Track
from pathlib import Path


class FeedlyStreams:
    dirs = {

        'feeds_dir': 'c:\\python_apps\\er_flask\\feeds\\playlists\\',
        'ec_dir': 'EconomicUpdate\\',
        'bol_dir': 'BestOfTheLeft\\',
        'belabored': 'BelaboredByDissentMagazine\\',
        'c-span': 'CSPAN\\',
        'npr': 'NPRNewsNow\\',
        'proj_syn': 'ProjectSyndicatePodcasts\\',
        'planet_money': 'PlanetMoney\\',
        'radiolab': 'Radiolab\\',
        'int_archive': 'InternetArchive\\',
        'sci_mag': 'ScienceMagazinePodcast\\',
        'weekly_econ': 'WeeklyEconomicsPodcast'
    }

    stream_names = {'Economic Update':'EconomicUpdate\\',
                    'Best of the Left': 'BestOfTheLeft\\',
                    'Radiolab': 'Radiolab\\',
                    'Science Magazine Podcast': 'ScienceMagazinePodcast\\',
                    'Belabored by Dissent Magazine': 'BelaboredByDissentMagazine\\',
                    'Weekly Economics Podcast': 'WeeklyEconomicsPodcast\\',
                    'NPR News Now': 'NPRNewsNow\\',
                    'Planet Money : NPR': 'PlanetMoney\\',
                    'Internet Archive - Mediatype: etree': 'InternetArchive\\',
                    'C-SPAN Radio - Washington Today': 'CSPAN\\',
                    'Project Syndicate Podcasts': 'ProjectSyndicatePodcasts\\'
                    }

    def __init__(self, name):
        self.name = name
        if name not in FeedlyStreams.stream_names.keys():
            print('invalid stream name')
        else:
            self.config = ERFeedlyConf()
            self.dconf = self.config.conf
            self.fapi = FeedlyAPI()
            self.fapi.initialize()
            self.feed_id = self.fapi.feeds_ids[self.name]
            self.stream_id = self.feed_id
            self.m3u_dir = FeedlyStreams.stream_names[self.name]
            self.playlist_dir = FeedlyStreams.dirs['feeds_dir']

            self.feed = None
            self.df = None
            self.trk_list = None
            self.get_track_list()

    def get_track_list(self):
        self.feed = json.loads(self.fapi.get_stream(self.stream_id))
        trks = []
        items = self.feed['items']
        dtrk = Track.get_feedly_track_template()
        for trk in items:
            dtrk['fid'] = trk.get('id', None)
            dtrk['title'] = trk.get('title', None)
            ct = trk.get('content', None)
            if ct:

                dtrk['desc'].append(ct['content'])

            dtrk['url'] = trk.get('enclosure')[0].get('href')
            dtrk['length'] = trk.get('enclosure')[0].get('length')
            dtrk['mime_type'] = trk.get('enclosure')[0].get('type')
            dtrk['author'] = trk.get('author', None)

            trks.append(Track(json.dumps(dtrk)))
            dtrk = Track.get_feedly_track_template()
        sers = []
        for t in trks:
            sers.append(t.ser_trk)
        self.df = pd.DataFrame(data=sers)
        self.trk_list = trks

    @staticmethod
    def add_feedly_stream(name: str, dir_name: str):
        FeedlyStreams.stream_names[name] = dir_name

    @staticmethod
    def remove_feedly_stream(name: str):
        return FeedlyStreams.stream_names.pop(name)


class LocalTracks:

    youtube = '/itunes2/youtube'
    yt_path = Path(youtube)

    def __init__(self):
        self.local_tracks = []



    @staticmethod
    def get_local_tracks_dir(path, subs=False):
        p = Path(path)
        trks = {}

        ''' LOCAL_FILE_TEMPLATE = \
        {
            'fid': None,
            'title': None,
            'desc': [],
            'url': None,
            'mime_type': None,
            'length': -1,
            'author': None,
            'src': 'LOCAL',
            'file': None,
            'path': None
        }'''

        if p.is_dir():
            trk_files = [str(trk) for trk in p.iterdir() if trk.is_file() and trk.suffix == '.mp3']
            trks = []
            for trk in trk_files:
                dtrack_template = Track.get_local_track_template()
                ptrk = Path(trk)
                # print('getting id3 data for ', trk)
                id3_data = Track.get_song_info(trk)
                dtrack_template['file'] = trk
                dtrack_template['author'] = id3_data.artist
                dtrack_template['title'] = id3_data.title
                dtrack_template['length'] = id3_data.length
                dtrack_template['path'] = str(ptrk.parent)
                trks.append(Track(json.dumps(dtrack_template), src='LOCAL'))
            return trks

        else:
            print('Not a Directory')
            return None

    
class OldTimeRadio:
    def __init__(self):
        self.config = ERFeedlyConf()
        self.dconf = self.config.conf
        self.nw_path = self.dconf['items']['OTR_path']

    def get_file_list(self, mypath):
        from os import listdir
        from os.path import isfile, join
        return  [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
    def get_johnny_dollar_playlist(self):

        path = self.nw_path + 'johnny_dollar\\'
        flist =  self.get_file_list(path)
        choice = np.random.choice(flist,10)
        trk_lst = []
        for f in choice:
            jd_title = self.get_jd_title(f)
            jd_length = 1800  #seconds -- 30 minutes
            jd_url = path + f
            jd_path = None
            jd_typ = 'local_file'
            jd_show = 'Johnny Dollar'
            trk_lst.append([jd_length,jd_title,jd_path,jd_url,jd_typ,jd_show])
        df = pd.DataFrame(columns=['length','title','path','url','media_type','show'],data=trk_lst)
        plsplay = PLSPlaylist(df, pls=None)
        return plsplay.to_pls(df)
    
    def get_philip_marlowe_playlist(self):
        path = self.nw_path + 'philip_marlowe\\'
        flist = self.get_file_list(path)
        choice = np.random.choice(flist,10)
        trk_lst = []
        for f in choice:
            pm_title = self.get_pm_title(f)
            pm_length = 1800  # seconds -- 30 minutes
            pm_url = path + f
            pm_path = None
            pm_typ = 'local_file'
            pm_show = 'Philip Marlowe'
            trk_lst.append([pm_length,pm_title,pm_path,pm_url,pm_typ,pm_show])
        df = pd.DataFrame(columns=['length','title','path','url','media_type','show'],data=trk_lst)
        plsplay = PLSPlaylist(df, pls=None)
        return plsplay.to_pls(df)
            
    # def get_pm_title(self, tr):
    #     pass
    #
    # def get_jd_title(self, tr):
    #
    #     sl = tr.split('_')[2:]
    #     jd_t = ''.join(sl)
    #     lt = list(jd_t)[:-4]
    #     return ''.join(lt)
            
    def get_pv_playlist(self):
        pass

    def get_fmgm_playlist(self):
        pass