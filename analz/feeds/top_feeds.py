
from feeds.streams import FeedlyStreams
from feeds.gen_playlist import Playlist
from slugify import slugify
from feeds.er_tiny_db import ERTinyDB
import random


class TLFeedlyPlaylist:

    def __init__(self, nm, src='FEEDLY', limit=2, rand=False):
        self.eu = FeedlyStreams(nm)
        self.trk_lst = self.eu.trk_list
        self.name = nm
        self.filename = slugify(str(self.name +))
        self.limit = limit
        if rand:
            self.trk_lst = random.shuffle(self.trk_lst)
        if len(self.trk_lst) > self.limit:
            self.select_tracks = self.trk_lst[0:self.limit]
        else:
            self.select_tracks = self.trk_lst

        self.source = src
        self.playlist = Playlist(self.select_tracks, name=self.name, author=None, src=self.source, type='EXT')
        self.db = ERTinyDB()
        self.doc_id = self.store_playlist()

    def publish(self):
        with open(TLFeedlyPlaylist.feeds_dir + TLFeedlyPlaylist.ec_dir + self.filename + '-' +
                  str(self.doc_id) + '.m3u', 'w+') as ec_m3u:
            ec_m3u.write(self.playlist.m3u.ext_to_m3u())
            ec_m3u.close()

    def store_playlist(self):
         self.doc_id = self.db.insert(self.playlist.tiny_db_playlist_model)
         return self.doc_id

    def retrieve_playlist(self, d_id):
        self.doc_id = self.db.get(self,d_id)
        return self.doc_id

        




