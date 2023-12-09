
from analz.playlist.m3u_to_html import MTrack, M3UList
from pathlib import Path
from config import Config
from datetime import timedelta

class ERPlaylist:

    RDJ_M3US_DIR = Config.RDJ_M3U_TEMPLATES_DIR

    @staticmethod
    def getM3UList(fn, name=None):
        if not name:
            name = Path(fn).name
        try:
            m3ul = M3UList(fn, name=name)
        except:
            raise Exception(f"unable to initialize m3u_obj from {fn}")
        return m3ul

    def __init__(self, m3u: M3UList):
        self.m3u = m3u

    def initialize(self):
        self.trks = self.m3u.tracks
        self.name = self.m3u.name
        self.durations = [int(t.duration) for t in self.trks]
        self.ssums, self.ssum, self.smax = self.getListLength()
        self.artists = self.parseArtists()
        self.titles = self.parseTitiles()
        self.m3u_str = self.m3u.mtraks2m3u()

    def parseArtists(self):
        return [t.artist for t in self.trks]

    def parseTitiles(self):
        return [t.title for t in self.trks]


    def to_html(self):
        from analz.playlist.plutils import PLUtils
        df = self.m3u.to_html()
        htm_tbl = PLUtils.RDJplaylist2BloggerHTML(fn=None, df=df)
        return f"<div>{htm_tbl}</div>"

    def to_m3u(self):
        return self.m3u.to_simple_m3u()

    def add_mtrack(self, mtrk: MTrack):
        self.m3u.add_tracks([mtrk], update=True, inplace=True)

    def remove_track(self, tid: str): # tid == file name until MTrack objs get IDs
        self.m3u.remove_track(tid)

    def getListLength(self):

        ssums = []
        ssum = 0
        smax = 0
        for t in self.durations:
            ssums.append(self.secstr(t))
            ssum = ssum + t
            if t > smax:
                smax = t
        return ssums, self.secstr(ssum), self.secstr(smax)

    def secstr (self, secs: int):
        return str(timedelta(seconds=secs))








