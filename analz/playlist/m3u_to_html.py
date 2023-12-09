
from pathlib import PurePath, Path

import pandas as pd


class MTrack:
    """ A class modeling an audio track extracted from an M3U playlist. """
    cols = ['duration', 'artist', 'title', 'file', 'url']
    test_props = {'duration':199,
                  'artist': 'Trampled By  Turtles',
                  'title': 'Wait So Long',
                  'file': f"F:/youtube_downloads/watchhouse/Mandolin Orange - Boots of Spanish Leather (Bob Dylan Cover) - Audiotree Live/Trampled by Turtles - Wait So Long.mp3"
    }

    @staticmethod

    def getTrack(props: dict):
        return MTrack(dur=props['duration'],
                      art=props['artist'],
                      tit=props['title'],
                      fn=props['file'])

    def __init__(self, dur=-1, art=None, tit=None, fn=None, url=None):

        self.duration = dur
        self.artist = art
        self.title = tit
        self.file = fn
        self.url = url

    def to_string(self):
        return 'duration:' + str(self.duration) + ', artist: ' + self.artist + \
               ', title: ' + self.title + ', file: ' + str(self.file) + ', url: ' + self.url

    def to_m3u_str(self):
        l1 = f"{M3UList.xf_rec_marker}{str(self.duration)}, {self.artist} - {self.title}"
        l2 = f"{self.file}"
        return [l1, l2]

    def get_row(self):
        return [self.duration, self.artist, self.title, self.file, self.url]

    # def get_series_row(self):
    #     ser = pd.Series(self.get_row(), index=MTrack.cols)
    #     return ser


class M3UList:
    """ A class parsing and modeling the extended m3u playlist file, plus operations
        extracting audio track data; and converting to HTML."""

    # class attributes

    types = ['EXT', 'SIMPLE']
    xf_descriptor = '#EXTM3U'
    xf_rec_marker = '#EXTINF:'
    xf_desc = '#D:'
    sf_comment = '# '
    http_marker = 'http'
    rdf_marker =  '#RDJDATA:'
    #  static methods

    @staticmethod
    def test_1():
        from config import Config
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        m3u_fn = 'bg_nite.m3u'
        fn1 = f"{dir}/{m3u_fn}"
        slines1 = M3UList.get_lines(fn1)
        fn2 = f"{dir}/bg_days.m3u"
        slines2 = M3UList.get_lines(fn2)

        m3u1 = M3UList(fn1, slines1, name='test1')
        m3u1.initialize()
        print(f"m3u1 num_tracks: {len(m3u1.tracks)}")
        print("Adding two tracks from separate list....")
        m3u2 = M3UList(fn2, slines2, name="test2")
        m3u2.initialize()
        add_tracks = m3u2.tracks[-2:]
        return m3u1, add_tracks

    @staticmethod
    def save_as(f: str):
        with open(f, "w") as ff:
            ff.write(f)

    @staticmethod
    def get_lines(f:str):
        # print("in get_lines, file is :", f)
        paragraph = Path(f).read_text(encoding='utf-8')
        lines = paragraph.split('\\n')
        return lines




    @staticmethod
    def get_type(lines: list):
        if lines[0] == M3UList.xf_descriptor:
            return M3UList.types[0]
        else:
            return M3UList.types[1]

    @staticmethod
    def parse_m3ue2(line: str):
        __doc__ = """returns a tuple (path -- relative or absolute [or None if 
            file is in current directory as m3u] ,file)"""

        # print('in parse_m3ue2: ', line)
        if line.startswith('http'):
            return None, line

        else:  # a windows path
            ss = line.split('\\')
            pp = PurePath('\\\\'.join(ss))
            # path = pp.parent
            file = str(pp)
            return None, file

    @staticmethod
    def parse_m3ue1(line: str):
        """ Returns a tuple (duration,title)
            for line one of EXT M3U format. """

        ref, rest = line.split(':', maxsplit=1)
        lss = rest.split(',', maxsplit=1)
        duration = lss[0]
        artist_title = lss[1]
        if ' - ' in artist_title:
            title, artist = lss[1].split(' - ', maxsplit=1)
        else:
            if '.mp3' in artist_title:
                title = '.'.join(artist_title.split('.')[0:-1])
                artist = None
            else:
                title = artist_title
                artist = None
        return duration, artist, title

    @staticmethod
    def parse_m3u_path(line: str):
        __doc__ = ''' From second line in  M#U EXT Format, returns a tuple (path -- 
            relative or absolute [or None if 
            file is in current directory as m3u] ,file or url)'''

        # print('in parse_m3ue2: ', line)
        if line.startswith('http'):
            return None, line

        else:  # a windows path
            ss = line.split('\\')
            pp = PurePath('\\\\'.join(ss))
            # path = pp.parent
            file = str(pp)
            return None, file

    @staticmethod
    def list_2_html(l):

        ll = [ x for x in l if x is not None]
        if len(l) < 1:
            return None
        else:
            return ll

        # return str(List(l))

    # @staticmethod
    # def m3u2htm_file(fin, fout=None, artist=[], name=None):
    #     m3u = M3UList(fin, artists=artist, name=name)
    #     if fout:
    #         with open(fout, 'w+') as f:
    #             f.write(m3u.table_html)
    #     return m3u.to_HTML()


    @staticmethod
    def format_m3u_rdj_lines(lines: list):

        tup = ()
        oldlines = lines.copy()
        newlines = list()
        rdjlines = list()

        for l in oldlines:
            l = str(l)
            if l.startswith(M3UList.xf_rec_marker):
                newlines.append(l)
            elif l.startswith(M3UList.rdf_marker):
                rdjlines.append(l)
            else:
                pp = Path(l)
                newlines.append(pp.as_posix())

        return newlines, rdjlines

    # Instance methods

    def __init__(self,
                 m3u_fn:str = None,
                 lines: list = None,
                 name = 'test_name'):
        self.fn = m3u_fn
        self.lines = lines
        if not self.lines:
            if self.fn:
                self.lines = M3UList.get_lines(self.fn)
            else:
                raise Exception("no file name, no l ines")

        self.rdj = self.__isRDJ(self.lines)
        self.type = M3UList.get_type(self.lines)
        # self.src = 'LOCAL'
        if name is None:
            self.name = self.fn
        else:
            self.name = name
        self.comments = []
        self.tracks = self.process_lines(rdj=self.rdj)

    def initialize(self):

        self.compact_file()
        self.mt = None

        self.list_of_trks = [mt.get_row() for mt in self.tracks]
        self.trk_cnt = len(self.tracks)
        # self.df = self.html_from_array()
        self.artists = self.get_artists()
        # self.table_html = str(self.html_from_array())



    def add_tracks(self, trks: [MTrack], update=True, inplace=False):
        if inplace:
            for t in trks:
                self.tracks.append(t)
                #     update instance
                #           add to self.lines str rep from m3u file track format
                l1, l2 = t.to_m3u_str()
                self.lines.append(l1)
                self.lines.append(l2)
            self.initialize()

            #   update file?
            if update:
                with open(self.fn, "w") as f:
                    lines = self.to_simple_m3u()
                    f.write(lines)
            return self

        else: # return new m3ulist with added track[s]
            old_trks = self.tracks.copy()
            new_trks = trks
            old_lines = self.lines.copy()

            for t in new_trks:
                old_trks.append(t)
                #     update instance
                #           add to self.lines str rep from m3u file track format
                l1, l2 = t.to_m3u_str()
                old_lines.append(l1)
                old_lines.append(l2)

            return M3UList(m3u_fn=self.fn, lines=old_lines, name=self.name)

    def remove_track(self, trk_fn: str):
        track = None

        x = 0
        for t in self.tracks:
            if t.file == trk_fn:
                track = t
                del self.tracks[x]
                self.lines = M3UList.mtraks2m3u()
                self.initialize()
                return t
            else:
                x += 1
        return None



    def __isRDJ(self, lines):
        isRDJ = False
        for l in lines:
            l = str(l)
            if l.startswith(M3UList.rdf_marker):
                isRDJ = True
                return isRDJ
        return isRDJ

    def mtraks2m3u(self):
        slines = [M3UList.xf_descriptor]
        for t in self.tracks:
            slines.extend(t.to_m3u_str())
        return self.to_simple_m3u(slines=slines)


    def to_simple_m3u(self, slines=None):
        """returns string representation"""

        slines = '\n'.join(slines)

        return slines

    def compact_file(self):

        self.lines = [line for line in self.lines if line != '\n']
        self.lines = [l.strip() for l in self.lines]

    # def to_HTML(self):
    #     """ Return playlist table with artists header as HTML string. """
    #     return '<div><h3> Playlist Artists </h3> <br/>' + str(List(M3UList.list_2_html(self.artists))) \
    #            + '</div> <br/> <div>' + self.table_html + '</div>'

    # def to_html_file(self):
    #     nfn = PurePath(self.fn)
    #     ppp = str(nfn.parent) + '\\' + str(nfn.stem) + '.html'
    #     with open (ppp, mode="w") as f:
    #         f.write(self.to_HTML())

    def get_artists(self):
        """ Return list of artists in playlist. """

        return list(dict.fromkeys([x.artist for x in self.tracks if x.artist]))



    # def html_from_array(self):
    #     list_of_trks = [mt.get_row() for mt in self.tracks]
    #     htbl = Table(rows=list_of_trks, border=2, header_row=MTrack.cols)
    #     return htbl
        
    def process_lines(self, rdj=True):
        """ Parse lines of M3U Track. """
        line_count = 0
        trks = []
        # parse m3u #EXTINF lines, 2 per track
        if rdj:
            self.lines, self.rdjlines = M3UList.format_m3u_rdj_lines(self.lines[1:])
            # print(f"length of new (- rdj)  lines {len(self.lines)}")
            # print(f"length of rdjlines: {len(self.rdjlines)}")
            # print(f"lenght of self.lines equals twice rdj info lines {len(self.rdjlines) == len(self.lines) / 2}")
            self.lines.insert(0, M3UList.xf_descriptor )

        for line in self.lines:
            if line == '\n' or line.startswith(M3UList.xf_descriptor):
                continue

            # '''{
            #
            #     "title": null,            #
            #     "url": null,            #
            #     "duration": -1,
            #     "artist": null,
            #     "file": null
            #
            #  }   '''

            elif line.startswith(M3UList.xf_rec_marker) and (
                    line_count % 2 == 0):  # line 1 in m3u ext track format.
                self.mt = MTrack()
                self.mt.duration, self.mt.artist, self.mt.title = M3UList.parse_m3ue1(line)
                line_count += 1

            else:  # line 2 in m3u ext track format.
                if (line_count % 2) != 0:
                    (path, file) = self.parse_m3ue2(line)
                    if path is None and file.startswith('http'):
                        self.mt.url = file
                        self.mt.file = None
                    else:
                        if path is not None:
                            self.mt.file = str(f"{path}/file")
                            self.mt.url = None
                        else:
                            self.mt.file = file
                            self.mt.f = path
                            self.mt.url = None

                    trks.append(self.mt)
                    line_count += 1
                    self.mt = MTrack()

                else:
                    # if line.startswith('# '):
                    #     self.comments.append(line)
                    # else:
                    print("Do not recognize: " + line)
                    self.mt = MTrack()

                    continue

        return trks

    def to_html(self):

        d =  {'artist': [t.artist for t in self.tracks],
              'title': [t.title for t in self.tracks],
              'duration': [t.duration for t in self.tracks]
              }
        df = pd.DataFrame(d)
        return df

