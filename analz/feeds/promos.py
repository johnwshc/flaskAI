from gtts import gTTS
from feeds.m3u_playlist import M3UPlaylist
from tinytag import TinyTag
from copy import deepcopy
import pandas as pd
from feeds.id3 import MetaInfo, ID3
from feeds.er_tiny_db import ERTinyDB
from config import Config
import os


class Promo:

    PROMO_DIR = Config.FEEDS_PROMO_DIR_LOCAL

    PROMO_FILE_TEMPLATE = \
        {
            'doc_id': None,
            'title': None,
            'desc': [],
            'url': None,
            'length': -1,
            'author': None,
            'src': 'LOCAL',
            'file': None,
            'path': None,
            'parent': None
        }

    @staticmethod
    def get_promo_template():
        return deepcopy(Promo.PROMO_FILE_TEMPLATE)

    def __init__(self, s_trk, db:ERTinyDB, doc=None):
        from feeds.tracks import Track

        # from feeds.tracks import Track
        if not isinstance(s_trk, Track):
            print('Track obj missing, look in storage')

            # if from storage
            if doc:

                self.doc_id = doc.doc_id
                self.d_trk = dict(doc)
                self.ser_trk = pd.Series(self.d_trk)
                self.language = 'en'
            else:
                print('error: neither track obj nor stored promo doc_id ... .so why are we here')

        else:

            self.language = 'en'
            #  get the Track Title
            self.s_trk_title = s_trk.ser_trk.title
            #  get the Track filename
            self.ser_trk_file = s_trk.ser_trk.file

            # get the Track author (or artist)
            self.s_trk_artist = s_trk.ser_trk.author

            # get and concatenate any desc strings from the Track
            if s_trk.d_track['desc']:
                self.s_trk_comment = '\n\t'.join(s_trk.d_track['desc'])
            else:
                self.s_trk_comment = ''

            # The Promo text string

            self.txt = 'The next track is %s, by %s. %s You are listening ' \
                       'to Enlighten Radio at www dot enlighten radio dot org. Our ' \
                       'pod casts are available at democracy ' \
                       'road dot pod bean dot com' % (self.s_trk_title, self.s_trk_artist, self.s_trk_comment)

            #  transform text to audio with gTTS tech
            self.myobj = gTTS(text=self.txt, lang=self.language, slow=False)

            #  The raw promo out file
            # In case bad windows file name chars are in title
            bad_chars = ['\\', '?', '*', '%']
            for c in bad_chars:
                if c in self.s_trk_title:
                    self.s_trk_title = self.s_trk_title.replace('?', '_')
            fn = Promo.PROMO_DIR + '\\' + self.s_trk_title + '.promo_raw' + '.mp3'

            # The tagged promo out file (gTTS transform does not preserve or assign mp3 tags, apparently)
            fn_tagged = Promo.PROMO_DIR + '\\' + self.s_trk_title + '.promo_tg' + '.mp3'
            self.myobj.save(fn)

            #  retrieve tags from raw transformed audio mp2
            tt = TinyTag.get(fn)

            # The MetaInfo is a class encapsulating the tags with a dict() output
            #     required by pydub for writing tags
            meta = MetaInfo(artist=tt.artist, title=tt.title,length=tt.duration, album=tt.album, genre=tt.genre)
            print(fn + ' -- ' + str(meta.duration))
            #  prepare promo attr dict
            self.d_trk = Promo.get_promo_template()
            self.d_trk['title'] = self.s_trk_title + ' - promo'
            self.d_trk['author'] = 'Admin--jcase'
            self.d_trk['file'] = fn_tagged
            self.d_trk['src'] = 'LOCAL'
            self.d_trk['url'] = None
            self.d_trk['desc'].append('Promo for ' + self.s_trk_title)
            self.d_trk['parent'] = [s_trk.ser_trk.file, s_trk.d_track['doc_id']]

            # populate MetaInfo object

            meta.artist = self.d_trk['author']
            meta.title = self.d_trk['title']
            meta.album = 'enlighten radio audio'
            meta.genre = 'promo'

            # Convert raw file to mp3 tagged file (from meta data)

            f_out, meta_d = ID3.convert_raw_mp3(fn, fn_tagged, meta, fmt='mp3', out_dir='c:\\itunes2\\promos')

            #  remove raw file

            os.remove(fn)
            self.d_trk['length'] = meta.duration
            self.ser_trk = pd.Series(self.d_trk)


            # make m3u_playlist

            author_title = self.ser_trk.title + ' - ' + self.ser_trk.author
            self.line_one = M3UPlaylist.xf_rec_marker + str(self.ser_trk.length) + ',' + author_title
            url_file = self.ser_trk.url
            if url_file is None:
                url_file = self.ser_trk.file
            self.line_two = url_file
            self.d_trk['m3u'] = self.m3u_out()
            # self.ser_trk['m3u'] = self.d_trk['m3u']

            self.ser_trk = pd.Series(self.d_trk)

            self.doc_id = db.insert_promo(self.d_trk)

    # generate an m3u for this track

    def m3u_out(self):
        return self.line_one + '\n' + self.line_two

    @staticmethod
    def create_playlist_promo(pl):
        from feeds.gen_playlist import Playlist
        pass

    # @staticmethod
    # def make_promos(start, out):
    #     promos = []
    #
    #     for dirname, dirnames, filenames in os.walk(start):
    #         # print path to all subdirectories first.
    #         #         for subdirname in dirnames:
    #         #             print(os.path.join(dirname, subdirname))
    #
    #         # print path to all filenames.
    #         for filename in filenames:
    #             song = os.path.join(dirname, filename)
    #             p = Path(song)
    #             ext = p.suffix
    #             if ext == '.mp3':
    #                 moved.append(song)
    #                 shutil.copy(song, out)
    #             elif ext == '.mp4':
    #                 ID3.convert_song(song, 'mp4', out)
    #                 converted.append(song)
    #             elif ext == '.m4a':
    #                 ID3.convert_song(song, 'm4a', out)
    #                 converted.append(song)
    #             else:
    #                 deleted.append(filename)
    #     return deleted, moved, converted
