

import json
import pandas as pd
from copy import deepcopy
from feeds.promos import Promo
from pathlib import Path
from feeds.id3 import ID3
from feeds.er_tiny_db import ERTinyDB


class Track:

    def __init__(self, json_track: str, db: ERTinyDB, src='FEEDLY', make_promo=False):

        # load json track dictionary
        self.promos = []
        self.doc_id = None

        #  load Track dictionary from json

        self.d_track = json.loads(json_track)
        self.ser_trk = pd.Series(self.d_track)

        # retrieve any copy if this track is in storage, check for existing promos, delete all
        #    minimize db clutter and garbage

        # type: tinydb.document / dictionary

        docs = db.find_track(self.d_track['title'], doc_id=0)
        if docs:

            stored_track_pro_ids = docs[0]['promo_ids']
            if stored_track_pro_ids:
                pid = db.remove_promo(stored_track_pro_ids)
                print('these ids removed from tiny_db: ', str(pid))


        #  if not make_promo, this is a stand_alone track

        if not make_promo:
            self.d_track['promo_links'] = []
            self.d_track['promo_ids'] = []
            self.has_promo = False

        # assign Track src
        self.d_track['src'] = src

        # fill out minimum author and title if missing

        if self.d_track['author'] is None:
            author_title = self.d_track['title']
        else:
            author_title = self.d_track['author'] + ' - ' + self.d_track['title']

        # Build a 2line  m3u playlist for the track

        from feeds.m3u_playlist import M3UPlaylist

        #  in some mp3 tracks artist-title is in a single tag, usually the title tag. This must fit into
        #    the m32 extended playlist file format

        self.line_one = M3UPlaylist.xf_rec_marker + str(self.d_track['length']) + ',' + author_title
        url_file = self.d_track['url']
        if url_file is None:
            url_file = self.d_track['file']
        self.line_two = url_file

        # Make a promo if make_promo == True
        if make_promo:
            pro = Promo(self, db)
            self.promos.append(pro)
            promo_link = pro.d_trk['file'] if pro.d_trk['file'] else pro.d_trk['url']
            promo_doc_id = pro.doc_id
            self.d_track['promo_links'].append(promo_link)
            self.d_track['promo_ids'].append(promo_doc_id)
            self.ser_trk = pd.Series(self.d_track)



        #  Update the database with a new promo

        self.doc_id = db.insert_track(self.d_track)

    def update_db(self):
        if self.doc_id:
            removed = self.tracks_table.remove(doc_ids=[self.doc_id])
        return self.tracks_table.insert(self.d_track)

    def search_tracks(self, squery, feature):
        match = []
        for trk in self.tracks_table:
            print('squery: ', squery)
            print(feature, trk[feature])
            if squery in trk[feature]:
                match.append(trk)
        return match

    def get_promos(self):
        return self.promos

    def get_length(self):
        if self.promos:
            trk_len = 0
            promo_len = 0
            for x in self.promos:
                promo_len += x.ser_trk.length
            trk_len += self.ser_trk.length
        return promo_len + trk_len

    def get_link(self):
        if self.ser_trk.file is None:
            return self.ser_trk.url
        else:
            return self.ser_trk.file

    def add_promo(self):
        from feeds.promos import Promo
        p = Promo(self)
        self.d_track['promo_links'].append(p.d_trk['file'])
        self.ser_trk = pd.Series(self.ser_trk)
        return  p

    def remove_promos(self):
        self.promos = []
        self.d_track['promo_links'] = []
        self.d_track['promo_ids'] = []
        self.ser_trk = pd.Series(self.d_track)

    def add_promo_from_file(self, fn):
        from feeds.tinytag import TinyTag
        tt = TinyTag.get(fn)
        pth = Path(fn)
        stm = pth.stem


        PROMO_D_TRK_TEMPLATE = \
        {
            'doc_id': None,
            'title': tt.title,
            'desc': [],
            'url': None,
            'length': tt.duration,
            'author': tt.artist,
            'src': 'LOCAL',
            'file': fn,
            'path': stm,
            'parent': None
        }
        link = self.ser_trk.file if self.ser_trk.file else self.ser_trk.url
        PROMO_D_TRK_TEMPLATE['parent'] = link
        self.d_track['promo_links'].append(PROMO_D_TRK_TEMPLATE['file'])


    FEEDLY_TRACK_TEMPLATE = \
        {
            'fid': None,
            'title': None,
            'desc': [],
            'url': None,
            'mime_type': None,
            'length': -1,
            'author': None,
            'src': 'FEEDLY',
            'file': None,
            'path': None,
            'promo_links': [],
            'promo_ids': []




        }
    LOCAL_FILE_TEMPLATE = \
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
            'path': None,
            'doc_id': None,
            'promo_links': [],
            'promo_ids': []
        }
#           ID3 data from TinyTag :

    mp3_ide_dict = \
        {
            'filesize': 10206132,         # not used
            'album': '16 Biggest Hits',   # not used
            'albumartist': 'Alabama',     # not used
            'artist': 'Alabama',
            'audio_offset': 91392,        # not used
            'bitrate': 256.0,             # not used
            'channels': 2,                # not used
            'comment': '                        ',  # not used
            'disc': '1', 'disc_total': '1', # not used
            'duration': 316.1263889906285,
            'genre': 'Country',            # not used
            'samplerate': 44100,           # not used
            'title': 'She and I',
            'track': '8',                  # not used
            'track_total': None,           # not used
            'year': '2007'                 # not used
         }

    @staticmethod
    def get_feedly_track_template():
        new_temp = deepcopy(Track.FEEDLY_TRACK_TEMPLATE)
        return new_temp

    @staticmethod
    def get_local_track_template():
        new_temp = deepcopy(Track.LOCAL_FILE_TEMPLATE)

        return new_temp

    @staticmethod
    def parse_title_from_url(u):
        return u.split('/')[-1]

    def update(self, obj):
        if isinstance(obj, pd.Series):
            self.ser_trk = obj
            self.d_track = obj.to_dict()
            return self
        elif isinstance(obj, dict):
            self.ser_trk = pd.Series(obj)
            self.d_track =  obj
            return self
        elif isinstance(obj, Track):
            self.d_track = deepcopy(obj.d_track)
            self.ser_trk = pd.Series(self.d_track)
            return self
        else:
            print(' update with unknown object')
            return self

    def to_json(self):
        return json.dumps(self.d_track)

    def print_m3u_file(self, fname):

        from feeds.m3u_playlist import M3UPlaylist
        with open(fname, "w+") as f:
            s_trk = M3UPlaylist.xf_descriptor
            if self.isPromo:
                for p in self.promos:
                    s_trk = s_trk + p.m3u_out()
            s_trk = s_trk + '\n' + self.line_one + '\n' + self.line_two +'\n'
            f.write(s_trk)
        return fname

    def m3u_out(self):
        from feeds.m3u_playlist import M3UPlaylist
        s_trk = M3UPlaylist.xf_descriptor
        if self.isPromo:
            for p in self.promos:
                s_trk = s_trk + p.m3u_out()
        s_trk = s_trk + '\n' + self.line_one + '\n' + self.line_two + '\n'

        return s_trk

    @staticmethod
    def get_local_track(file_name, db: ERTinyDB, promo=False):
        p_trk = Path(file_name)
        id3_data = ID3.get_song_info(file_name)
        # print(id3_data)
        dtrack_template = Track.get_local_track_template()
        dtrack_template['author'] = id3_data.artist
        dtrack_template['title'] = id3_data.title
        dtrack_template['length'] = id3_data.duration
        dtrack_template['file'] = str(p_trk)
        dtrack_template['path'] = str(p_trk.parent)
        if id3_data.genre:
            dtrack_template['genre'] = id3_data.genre
        if id3_data.album:
            dtrack_template['album'] = id3_data.album
        return Track(json.dumps(dtrack_template), db, src='LOCAL', make_promo=promo)





