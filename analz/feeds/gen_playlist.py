from feeds.m3u_playlist import M3UPlaylist
from feeds.er_tiny_db import ERTinyDB
from tinydb import Query
import json
from random import sample
import config

class Playlist:

    def __init__(self, trks, type='EXT', src='FEEDLY', name=None, author=None):
        self.tracks = trks
        self.type = type
        self.dtracks = self.get_dtracks()
        self.src = src
        self.name = name
        self.author = author
        self.len = len(self.tracks)
        self.duration = self.get_duration()
        self.m3u = M3UPlaylist(self.tracks, type=self.type, src=self.src, author=self.author, name=self.name)
        self.comments = []
        self.did = None
        self.timestamp = config.Config.get_timestamp()

        self.tiny_db_playlist_model = {
            'src': self.src,
            'name': self.name,
            'timestamp': self.timestamp,
            'len': self.len,
            'duration': self.duration,
            'tracks': self.dtracks,
            'author': self.author,
            'comments': self.comments,
            'm3u': None

        }
        if self.type == M3UPlaylist.types[0]:
            self.tiny_db_playlist_model['m3u'] = self.m3u.ext_to_m3u()
        if self.type == M3UPlaylist.types[1]:
            self.tiny_db_playlist_model['m3u'] = self.m3u.simple_to_m3u()

    def get_dtracks(self):
        dic_tracks = []

        for trk in self.tracks:

            dic_tracks.append(trk.d_track)
        return dic_tracks

    def get_duration(self):
        dur: int = 0
        for trk in self.tracks:
            t_dur = trk.ser_trk.length
            if t_dur is None or t_dur == '' or t_dur in [-1, 0]:
                print(trk.ser_trk.title + ' : zero or infinite or unknown duration')
                continue
            dur += int(t_dur)
        return dur

    @staticmethod
    def get_playlist_from_db(name=None, did=None):
        q = Query()
        edb = ERTinyDB()
        # res = None
        if did:
            res = edb.get(did)
        elif name:
            res = edb.search(q.name == name)[0]
        else:
            return None
        doc = res
        trks = doc['tracks']
        src = doc['src']
        name = doc['name']
        author = doc['author']
        Trks = []
        from feeds.tracks import Track
        for trk in trks:
            Trks.append(Track(json.dumps(trk), src=src))
        return Playlist(Trks, src=src, name=name, author=author)

    def save_to_db(self):
        db = ERTinyDB()
        self.did = db.insert(self.tiny_db_playlist_model)

    def add_comment(self, comment: str):
        self.comments.append(comment)

    def get_get_randomized_playlist(self):
        r_tracks = sample(self.tracks, self.len)
        r_pl = Playlist(r_tracks,self.type, src=self.src, name=self.name + '_r')
        return r_pl

    # FIX ME
    def get_playlists_by_duration(self, target_dur, off, min_trks, max_trks):
        target = target_dur
        offset = off
        min_pl_items = min_trks
        max_pl_items = max_trks
        lengths = [(x.ser_trk.length, x.ser_trk.title) for x in self.tracks]
        ss = SubSum(lengths, target, xl=max_pl_items, ml=min_pl_items)
        ss.subset_sum(lengths)
        return ss.choices


class SubSum:

    def __init__(self, nums, tar, off_set=300, xl=10, ml=3):
        self.choices = []
        self.numbers = sorted(nums, key=lambda x: x[0])
        self.target = tar
        self.max = xl
        self.min = ml
        self.offset = off_set

    def subset_sum(self, numbers, partial=[]):
        # numbers = array track lengths, with associated track title; target = desired duration; max = max num of tracks in list
        #   min = min number of tracks in list; offset = maximum empty time (default=300, in seconds) following list before target
        #   for list to qualify --  i.e. error factor.
        s = self.s_sum(partial)
        l = len(partial)

        if self.target - self.offset <= s <= self.target:
            if self.max >= l >= self.min:
                self.choices.append(partial)
                partial = []

        if s > self.target:
            return  # if we reach the number why bother to continue

        for i in range(len(self.numbers)):
            n = numbers[i]
            remaining = numbers[i + 1:]
            self.subset_sum(remaining, partial + [n])

    def s_sum(self, part):
        s = 0
        for x in part:
            s += part[0]
        return s

    def add_playlist(self, pls):
        pass



























