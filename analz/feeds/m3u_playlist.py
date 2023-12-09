# -*- coding: utf-8 -*-
"""
Created on Tue May 22 17:06:02 2018

@author: johnc
"""

import pandas as pd
import json
# from config import Config
from urllib.parse import urlparse, urlunparse
import os.path
from pathlib import PurePath
from random import shuffle


class M3UPlaylist:

    __doc__ = ''' M3UPlaylist: construct a pandas DataFrame of tracks from a M3U playlist. '''
    types = ['EXT', 'SIMPLE']
    xf_descriptor = '#EXTM3U'
    xf_rec_marker = '#EXTINF:'
    xf_desc = '#D:'
    sf_comment = '# '
    http_marker = 'http'

    def __init__(self, m3u_obj,  type='EXT', src='FEEDLY', author=None, name=None):

        if isinstance(m3u_obj, list):
            self.lines = None
            self.type = type
            self.src = src
            self.author = author
            self.name = name
            self.items = m3u_obj
            self.num_items = len(self.items)
            self.comments = []
        elif isinstance(m3u_obj, str):

            self.lines = M3UPlaylist.get_lines(m3u_obj)
            self.compact_file()
            self.type = type
            self.src = src
            self.author = author
            self.items = self.get_items()
            self.num_items = len(self.items)
            self.name = name
            self.comments = []

        else:
            print(' oooops....sum\'p\'in not rite lucy')

    @staticmethod
    def get_lines(f):
        with open(f) as m3u:
            return m3u.readlines()

    def compact_file(self):
        self.lines = [line for line in self.lines if line != '\n']
        self.lines = [l.strip() for l in self.lines]

    def get_type(self):
        if self.lines[0] == M3UPlaylist.xf_descriptor:
            return M3UPlaylist.types[0]
        else:
            return M3UPlaylist.types[1]

    def get_simple_items(self):
        from feeds.tracks import Track
        tracks = []
        trk = {'desc': []}
        half_trk = {'desc': []}
        for line in self.lines:
            if line.startswith(M3UPlaylist.sf_comment):
                self.comments.append(line)
                continue
            elif line.startswith(M3UPlaylist.http_marker):
                o = urlparse(line)
                # '''{
                #     "fid": null,
                #     "title": null,
                #     "desc": null,
                #     "url": null,
                #     "mime_type": null,
                #     "length": -1,
                #     "author": null,
                #     "src": "FEEDLY",
                #     "path": null
                #     "file": null
                #
                #  }   '''
                half_trk['url'] = urlunparse(o)
                half_trk['path'] = o.path
                half_trk['author'] = self.author
                half_trk['src'] = self.src
                half_trk['length'] = -1
                half_trk['title'] = M3UPlaylist.get_title_from_path(o.path)
                half_trk['mime_type'] = None
                half_trk['desc'] = []
                half_trk['fid'] = None
                half_trk['file'] = M3UPlaylist.get_file_from_path(o.path)

                tracks.append(Track(json.dumps(half_trk)))
                half_trk = trk.copy()

            elif '\\' in line:   # a Win OS path
                (path, file) = os.path.split(line)
                title = file.split('.')[0]
                half_trk['url'] = None
                half_trk['path'] = path
                half_trk['author'] = self.author
                half_trk['src'] = self.src
                half_trk['length'] = 0
                half_trk['title'] = title
                half_trk['mime_type'] = None
                half_trk['desc'] = []
                half_trk['fid'] = None
                half_trk['file'] = '\\'.join(path, file)

                tracks.append(Track(json.dumps(half_trk)))
                half_trk = trk.copy()

            else:
                print('Do not recognize this:  ' + line)

        return tracks

    def get_extended_items(self):
        return self.process_lines()

    @staticmethod
    def get_title_from_path(pth):
        return '.'.join(pth.split('/')[-1].split('.')[0:-1])

    @staticmethod
    def get_file_from_path(pth):
        return pth.split('/')[-1]

    def get_items(self):
        if self.type == M3UPlaylist.types[1]:  # Simple
            return self.get_simple_items()
        elif self.type == M3UPlaylist.types[0]:    # Extended format
            return self.get_extended_items()
        else:
            print('unknown item type')
            return None

    def insert_track(self, track, pos):
        pass

    @staticmethod
    def parse_m3ue1(line: str):

        # __doc__ = '''returns a tuple (duration,title)'''

        # print('in parse_m3ue1: ', line)
        ls = line.split(':',maxsplit=1)
        l = ls[1]
        lss = l.split(',', maxsplit=1)
        duration = lss[0]
        artist_title = lss[1]
        if ' - ' in artist_title:
            artist, title = lss[1].split(' - ', maxsplit=1)
        else:
            if '.mp3' in artist_title:
                title = '.'.join(artist_title.split('.')[0:-1])
                artist = None
            else:
                title = artist_title
                artist = None
        return duration, artist, title

    @staticmethod
    def parse_m3ue2(line: str):
        # print('line: ' + line)

        # __doc__ = '''returns a tuple (path -- relative or absolute [or None if
        #     file is in current directory as m3u] ,file)'''

        # print('in parse_m3ue2: ', line)
        if line.startswith('http'):
            return None, line

        else: # a windows path
            ss = line.split('\\')
            pp = PurePath('\\\\'.join(ss))
            # path = pp.parent
            file = str(pp)
            return None, file

    def process_lines(self):
        from feeds.tracks import Track
        trk_cnt = 0
        line_count = 0
        tracks = []
    # parse m3u #EXTINF lines, 2 per track
        trk  = {'desc': []}
        lines = self.lines
        # print('lines[0]:', lines[0])
        half_trk = {'desc': []}
        for line in lines:
            if line == '\n' or line.startswith('#EXTM3U'):
                continue

            # '''{
            #     "fid": null,
            #     "title": null,
            #     "desc": null,
            #     "url": null,
            #     "mime_type": null,
            #     "length": -1,
            #     "author": null,
            #     "src": "FEEDLY",
            #     "path": null,
            #     "file": null
            #
            #  }   '''

            elif line.startswith(M3UPlaylist.xf_rec_marker) and (line_count % 2 == 0): # line 1 in m3u ext track format.
                (length, author, title) = M3UPlaylist.parse_m3ue1(line)
                half_trk['length'] = length
                half_trk['title'] = title
                half_trk['author'] = author
                line_count += 1

            else: # line 2 in m3u ext track format.

                if (line_count % 2) != 0:
                    (path, file) = M3UPlaylist.parse_m3ue2(line)
                    if path is None and file.startswith('http'):
                        half_trk['url'] = file
                        half_trk['file'] = file
                    else:
                        if path is not None:
                            half_trk['path'] = str(path + file)
                            half_trk['url'] = None
                        else:
                            half_trk['file'] = file
                            half_trk['path'] = path
                            half_trk['url'] = None

                    half_trk['src'] = self.src
                    half_trk['mime_type'] = None
                    half_trk['fid'] = None
                    tracks.append(Track(json.dumps(half_trk)))
                    half_trk = trk.copy()
                    line_count += 1
                    trk_cnt += 1

                else:
                    # if line.startswith('# '):
                    #     self.comments.append(line)
                    # else:
                    print("Do not recognize: " + line )

        # df = self.__to_df(tracks)
        # if len(df) == 1:
        #     self.is_single_track = True
        # else:
        #     self.is_single_track = False

        return tracks

    def ext_to_m3u(self):
        slines = []
        # insert header
        slines.append(M3UPlaylist.xf_descriptor)
        for trk in self.items:

            if trk.ser_trk.author is None:
                author_title = trk.ser_trk.title
            else:
                author_title = trk.ser_trk.author + ' - ' + trk.ser_trk.title

            l1 = M3UPlaylist.xf_rec_marker + str(trk.ser_trk.length) + ',' + author_title
            url_file = trk.ser_trk.url
            if url_file is None:
                url_file = trk.ser_trk.file
            l2 = url_file
            slines.append(l1)
            slines.append(l2)
        return '\n'.join(slines)

    def simple_to_m3u(self) -> str:
        simple_lines = []
        for trk in self.items:
            if trk.ser_trk.url is None:
                simple_lines.append(trk.ser_trk.file)
            else:
                simple_lines.append(trk.ser_trk.url)

        return '\n'.join(simple_lines)
    
    def __to_df(self,dic):

        ar_sers = []
        for trk in self.items:
            ar_sers.append(trk.ser_trk)
        return pd.DataFrame(ar_sers)

    def insert_track(self, track, pos='bottom'):
        if pos == 'bottom':
            self.num_items = len(self.items)
        else:
            if pos == 'top':
                self.items.insert(0, track)
            else:
                pass  # no insert except top and bottom
        self.num_items = len(self.items)

    def delete_track(self, index):
        del self.items[index]
        self.num_items = len(self.items)

    def randomize_tracks(self):
        shuffle(self.items)

    def get_subset(self, sub_tracks, src, name, author):
        return M3UPlaylist(sub_tracks, src, name, author)

    def print_m3u_file(self, fname):
        with open(fname, "w+") as f:
            if self.type == self.types[0]:
                # ext
                f.write(self.ext_to_m3u())
            if self.type == self.types[1]:
                # simple
                f.write(self.simple_to_m3u())











