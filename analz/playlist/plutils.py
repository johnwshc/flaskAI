import time

from config import Config
import os
import pandas as pd
import random
from bs4 import BeautifulSoup as BS
from pathlib import Path
import eyed3
from analz.playlist.m3u import VLC_Track, M3U
# from app import mconn
from analz.playlist.ptracks import ydl, ydg, idl, idg
# import mutagen
from mutagen.flac import FLAC
import moviepy.editor as mp
from datetime import datetime, timedelta
from analz.playlist.rdjplaylist import ERPlaylist




# class PublicTracks:
#
#     yt_dir = Config.YT_DIR
#     ia_dir = Config.IA_DIR
#     queries = {
#         'delete_all': 'r = coll.delete_many({})'
#     }
#
#     def __init__(self):
#         from app import mconn
#         self.mc = mconn.mc
#         self.db = self.mc.radio
#         self.coll = self.db['tracks']
#         self.tracks = []
#         zipped_yt_dirs = list(zip(ydl, ydg))
#         self.yt_dir_genres = {t[0]: t[1] for t in zipped_yt_dirs}
#         zipped_ia_dirs = list(zip(idl, idg))
#         self.ia_dir_genres = {t[0]: t[1] for t in zipped_ia_dirs}
#
#     def do_yt_walk(self, fpth=yt_dir, ft="mp3", genres: list = []):
#         self.tracks = []
#
#         # print("in do walk: genres are ", genres)
#         # if genres:
#         #     for g in genres:
#         #         print("genre: ", g)
#         # else:
#         #     print("no genres")
#
#
#         for root, dirs, files in os.walk(fpth):
#             # print(f'root is:  {root}, filepath is: {fpth}')
#             for file in files:
#
#                 if file.lower().endswith(ft.lower()):
#                     # print('matched file is: ', file)
#                     # print('root is: ', root)
#                     furl = os.path.join(root, file)
#                     trk = PLUtils.get_track(furl, genres=genres)
#                     time.sleep(0.01)
#                     self.tracks.append(trk)
#                     mdb_id = self.coll.insert_one(trk.vlc_to_dict())
#             # for d in dirs:
#                 # print('directory is: ', d)
#         return self.tracks
#
#
#     def fix_mp4s(self,dir: str, ft: str = 'mp4'):
#         for root, dirs, files in os.walk(dir):
#             for file in files:
#                 if file.lower().endswith(ft.lower()):
#                     PLUtils.convertMP4_to_MP3(file)
#

class PLUtils:

    @staticmethod
    def RDJplaylist2BloggerHTML(fn: str = None, df: pd.DataFrame = None):
        from slugify import slugify
        # import re
        #
        # re.sub(r'[\xc2\x99]', " ", "Hello\xc2There\x99")
        if fn:
            # print(f"in PLUtils.RDJplaylist2BloggerHTML: filename: {fn}")
            ddf = pd.read_html(fn)[0]
            ddf.columns = ddf.iloc[0]
            dff = ddf[['Artist', 'Title', 'Duration']].copy(deep=True)

        elif isinstance(df, pd.DataFrame):
            dff = df

        else:
            return {"error": "no file or data frame"}

        dfff = dff[1:].copy()
        dfff['Title'] = dfff['Title'].apply(lambda x: slugify(x))
        dfff['Artist'] = dfff['Artist'].apply(lambda x: slugify(x))
        htm = dfff.to_html(index=False, columns=['Artist', 'Title'], justify="justify-all")

        htm = htm.replace('\n', '')
        return htm




    @staticmethod
    def getLatestSTtelling(latest:int = 5):
        dirpath =  Config.ST_DIR

        paths = sorted(Path(dirpath).iterdir(), key=os.path.getmtime)
        return paths[-latest:]


    @staticmethod
    def getLatestWNL(latest:int = 5):
        dirpath = Config.WNL_DIR
        paths = sorted(Path(dirpath).iterdir(), key=os.path.getmtime)
        l = len(paths)
        if l < latest:
            return paths[-l:]
        else:
            return paths[-latest:]

    @staticmethod
    def getMysteryM3Us(key=None):
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        xfiles = [f for f in os.listdir(dir) if f.startswith('mystery.m3u')]
        for f in os.listdir(dir):
            if f.startswith('mystery'):
                if f not in xfiles:
                    mfiles.append(f)
                    # print(f)
        choice_m3u = random.choice(mfiles)
        return choice_m3u

    @staticmethod
    def getBGDays():
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        xfiles = [f for f in os.listdir(dir) if f.startswith('bg_days.m3u')]
        for f in os.listdir(dir):
            if f.startswith("bg"):
                if f not in xfiles:
                    newf = f"{dir}/{f}"
                    # print(f"bg_days candidate m3u: {newf}")
                    mfiles.append(newf)
        # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
        m3u_lists = []
        for m3u in mfiles:
            try:
                m3u_obj = ERPlaylist.getM3UList(m3u, name='bg_days')
                m3u_obj.initialize()
                m3u_lists.append(m3u_obj)
            except:
                print(Exception(f"failure inititializing {m3u}"))

        erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
        bg_choice = random.choice(erpls_objs)
        # print(f"bg_days choice file: {bg_choice.m3u.fn}")
        return bg_choice.m3u.fn


    @staticmethod
    def getBGNite():
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        xfiles = [f for f in os.listdir(dir) if (f.startswith('bg_nite.m3u') or
                                                 f.startswith('bg_days'))]
        for f in os.listdir(dir):
            if f.startswith("bg"):
                if f not in xfiles:
                    newf = f"{dir}/{f}"
                    # print(f"bg_days candidate m3u: {newf}")
                    mfiles.append(newf)
        # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
        m3u_lists = []
        for m3u in mfiles:
            try:
                m3u_obj = ERPlaylist.getM3UList(m3u, name='bg_nite')
                m3u_obj.initialize()
                m3u_lists.append(m3u_obj)
            except:
                print(Exception(f"failure inititializing {m3u}"))
        erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
        bg_nite_choice = random.choice(erpls_objs)
        return  bg_nite_choice.m3u.fn

    @staticmethod
    def getJazzDay():
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        xfiles = [f for f in os.listdir(dir) if f.startswith('jazz_day')]
        for f in os.listdir(dir):
            if f.startswith("jazz") or f.startswith("sjazz"):
                if f not in xfiles:
                    newf = f"{dir}/{f}"
                    mfiles.append(newf)
        # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
        m3u_lists = []
        for m3u in mfiles:
            try:
                m3u_obj = ERPlaylist.getM3UList(m3u, name='jazz_day')
                m3u_obj.initialize()
                m3u_lists.append(m3u_obj)
            except:
                print(Exception(f"failure inititializing {m3u}"))
        erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
        jazz_day_choice = random.choice(erpls_objs)
        return jazz_day_choice.m3u.fn

    @staticmethod
    def getJazzNight():
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        xfiles = [f for f in os.listdir(dir) if (f.startswith('jazz_nite')or
                                                 f.startswith('jazz_day'))]
        for f in os.listdir(dir):
            if f.startswith("jazz") or f.startswith("sjazz"):
                if f not in xfiles:
                    newf = f"{dir}/{f}"
                    mfiles.append(newf)
        # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
        m3u_lists = []
        for m3u in mfiles:
            try:
                m3u_obj = ERPlaylist.getM3UList(m3u, name='jazz_day')
                m3u_obj.initialize()
                m3u_lists.append(m3u_obj)
            except:
                print(Exception(f"failure inititializing {m3u}"))
        erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
        jazz_nite_choice = random.choice(erpls_objs)
        return jazz_nite_choice.m3u.fn

    @staticmethod
    def getRRDays():
        # 'rr_days': {
        #     'm3u_files': ['roots_days.m3u'],  # Wednesday Roots
        #     'cat': categories[2],
        #     'type': 'Repeat By Day',
        #     'stime': '06:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
        # },
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        xfiles = [f for f in os.listdir(dir) if f.startswith('roots_days.m3u')]
        for f in os.listdir(dir):
            if f.startswith("rr") or f.startswith('roots'):
                if f not in xfiles:
                    newf = f"{dir}/{f}"
                    mfiles.append(newf)
        # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
        m3u_lists = []
        for m3u in mfiles:
            try:
                m3u_obj = ERPlaylist.getM3UList(m3u, name='rr_days')
                m3u_obj.initialize()
                m3u_lists.append(m3u_obj)
            except:
                print(Exception(f"failure inititializing {m3u}"))
        erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
        rr_days_choice = random.choice(erpls_objs)
        return rr_days_choice.m3u.fn

    @staticmethod
    def getRRNite():
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        xfiles = [f for f in os.listdir(dir) if f.startswith('roots_nite.m3u')]
        for f in os.listdir(dir):
            if f.startswith("roots") or f.startswith('rr'):
                if f not in xfiles:
                    newf = f"{dir}/{f}"
                    mfiles.append(newf)
        # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
        m3u_lists = []
        for m3u in mfiles:
            # print(f"converting m3u_file {m3u} -- to m3u_obj")
            try:
                m3u_obj = ERPlaylist.getM3UList(m3u, name='rr_nite')
                # print(f"m3u_list_obj.fn: {m3u_obj.fn}")
                m3u_obj.initialize()
                m3u_lists.append(m3u_obj)
            except:
                print(Exception(f"failure inititializing {m3u}"))
        erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
        rr_nite_choice = random.choice(erpls_objs)
        return rr_nite_choice.m3u.fn

    @staticmethod
    def getSStories():
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        xfiles = [f for f in os.listdir(dir) if f.startswith('sstories.m3u')]
        for f in os.listdir(dir):
            if f.startswith("ss"):
                if f not in xfiles:
                    newf = f"{dir}/{f}"
                    mfiles.append(newf)
        # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
        m3u_lists = []
        for m3u in mfiles:
            # print(f"converting m3u_file {m3u} -- to m3u_obj")
            try:
                m3u_obj = ERPlaylist.getM3UList(m3u, name='sstories')
                # print(f"m3u_list_obj.fn: {m3u_obj.fn}")
                m3u_obj.initialize()
                m3u_lists.append(m3u_obj)
            except:
                print(Exception(f"failure inititializing {m3u}"))
        erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
        sstories_choice = random.choice(erpls_objs)
        return sstories_choice.m3u.fn

    @staticmethod
    def getCntryDays():
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        xfiles = [f for f in os.listdir(dir) if f.startswith('cntry_days.m3u')]
        for f in os.listdir(dir):
            if f.startswith("cntry"):
                if f not in xfiles:
                    newf = f"{dir}/{f}"
                    mfiles.append(newf)
        # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
        m3u_lists = []
        for m3u in mfiles:
            # print(f"converting m3u_file {m3u} -- to m3u_obj")
            try:
                m3u_obj = ERPlaylist.getM3UList(m3u, name='cntry_days')
                # print(f"m3u_list_obj.fn: {m3u_obj.fn}")
                m3u_obj.initialize()
                m3u_lists.append(m3u_obj)
            except:
                print(Exception(f"failure inititializing {m3u}"))
        erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
        cntry_days_choice = random.choice(erpls_objs)
        return cntry_days_choice.m3u.fn

    @staticmethod
    def getCntryNite():
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        xfiles = [f for f in os.listdir(dir) if f.startswith('cntry_nite.m3u')]
        for f in os.listdir(dir):
            if f.startswith("cntry"):
                if f not in xfiles:
                    newf = f"{dir}/{f}"
                    mfiles.append(newf)
        # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
        m3u_lists = []
        for m3u in mfiles:
            # print(f"converting m3u_file {m3u} -- m3ulist obj")
            try:
                m3u_obj = ERPlaylist.getM3UList(m3u, name='cntry_nite')
                # print(f"m3u_list_obj.fn: {m3u_obj.fn}")
                m3u_obj.initialize()
                m3u_lists.append(m3u_obj)
            except:
                print(Exception(f"failure inititializing {m3u}"))
        erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
        cntry_nite_choice = random.choice(erpls_objs)
        # print(f'cntry_nite choice: {cntry_nite_choice.m3u.fn}')
        return cntry_nite_choice.m3u.fn

    @staticmethod
    def getBluesRadioDays():
        salty_last_m3u_str = PLUtils.getSaltyPlaylists()
        moose_last_m3u_str = PLUtils.getMoosePlaylists()

        dir = Config.RDJ_M3U_TEMPLATES_DIR
        with open(f"{dir}/salty_last.m3u", "w") as f_salt:
            f_salt.write(str(salty_last_m3u_str))
        with open(f"{dir}/moose_last.m3u", "w") as f_moose:
            f_moose.write(str(moose_last_m3u_str))

        return f"{dir}/salty_last.m3u", f"{dir}/moose_last.m3u"

    # @staticmethod
    # def getBluesRadioNite():
    #     dir = Config.RDJ_M3U_TEMPLATES_DIR
    #     mfiles = []
    #     for f in os.listdir(dir):
    #         if f.startswith("blues_stream"):
    #             newf = f"{dir}/{f}"
    #             mfiles.append(newf)
    #     # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
    #     m3u_lists = [ERPlaylist.getM3UList(m3u, name='blues_radio_nite') for m3u in mfiles]
    #     erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
    #     return erpls_objs

    @staticmethod
    def getJazzRadioNite():
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        for f in os.listdir(dir):
            if f.startswith("jazz_streams"):
                newf = f"{dir}/{f}"
                mfiles.append(newf)
        # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
        m3u_lists = []
        for m3u in mfiles:
            # print(f"converting m3u_file {m3u} -- m3ulist obj")
            try:
                m3u_obj = ERPlaylist.getM3UList(m3u, name='jazz_streams')
                # print(f"m3u_list_obj.fn: {m3u_obj.fn}")
                m3u_obj.initialize()
                m3u_lists.append(m3u_obj)
            except:
                print(Exception(f"failure inititializing {m3u}"))
        erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
        jazz_radio_nite_choice = random.choice(erpls_objs)
        return jazz_radio_nite_choice.m3u.fn


    @staticmethod
    def getNightShift():
        dir = Config.RDJ_M3U_TEMPLATES_DIR
        mfiles = []
        for f in os.listdir(dir):
            if f.startswith("ns_"):
                newf = f"{dir}/{f}"
                mfiles.append(newf)
        # mfiles_obj = [ERPlaylist(m3ul) for m3ul in mfiles]
        m3u_lists = []
        for m3u in mfiles:
            # print(f"converting m3u_file {m3u} -- m3ulist obj")
            try:
                m3u_obj = ERPlaylist.getM3UList(m3u, name='jazz_radio_nite')
                # print(f"m3u_list_obj.fn: {m3u_obj.fn}")
                m3u_obj.initialize()
                m3u_lists.append(m3u_obj)
            except:
                print(Exception(f"failure inititializing {m3u}"))
        erpls_objs = [ERPlaylist(m3u) for m3u in m3u_lists]
        night_shift_choice = random.choice(erpls_objs)
        return night_shift_choice.m3u.fn

    @staticmethod
    def getLatestSalty(latest: int = 5):
        dirpath = Config.SALTY_DIR
        paths = sorted(Path(dirpath).iterdir(), key=os.path.getmtime)
        l = len(paths)
        if l < latest:
            return paths[-l:]
        else:
            return paths[-latest:]

    @staticmethod
    def getLatestMoose(latest: int = 5):
        dirpath = Config.MOOSE_DIR
        paths = sorted(Path(dirpath).iterdir(), key=os.path.getmtime)
        l = len(paths)
        if l < latest:
            return paths[-l:]
        else:
            return paths[-latest:]


    @staticmethod
    def get_track(f:str, genres: list = None):
        print(f"getting track: {f}")
        supported_audio_types = ['flac', 'mp3']
        pth = Path(f)
        if pth.suffix == '.mp3':
            ft = 'mp3'
        elif pth.suffix == '.flac':
            ft = 'flac'
        else:
            raise Exception("invalid file type")
        artist_title = ''
        duration = -1
        audiofile = None

        if ft == 'flac':
            audiofile = FLAC(f)
            title = audiofile['title'][0]
            artist = audiofile['creator'][0]
            artist_title = f"{artist} - {title}"
            info_lines = audiofile.pprint().split('\n')
            info_line = info_lines[0]
            # print('info line', info_line)
            durstr = info_line.split(',')[1].split()[0]
            duration =  int(float(durstr))
            # print("duration: ", duration)

        elif ft == 'mp3':
            try:
                audiofile = eyed3.load(str(f))
            except Exception as inst:
                print(f"audio file eyed3 for {f} \n\tfails: ", inst)
            if audiofile:
                duration = audiofile.info.time_secs
                duration = int(duration)
                au_path = Path(audiofile.path)
                name = au_path.stem

                title = audiofile.tag.title if audiofile.tag.title else "Unknown"
                artist = audiofile.tag.artist
                if title:
                    title = title.replace('-', '#')
                else:
                    title = name


                if artist and title:
                    artist_title = f"{artist} - {title}"
                else:
                    artist_title = title
            else:
                artist_title = Path(f).stem


        else:
            print(f"{ft} is unsupported")
            raise Exception(f"{ft} is not supported")
        line_one = f"#EXTINF:{str(duration)},{artist_title}"
        # EXTINF:123,Artist Name – Track Title␤
        line_two = Path(f).as_posix()
        track = VLC_Track(line_one, line_two, genres)

        return track

    @staticmethod
    def getSaltyPlaylists(n: int = 5):
        trks = []
        pths = PLUtils.getLatestSalty()

        for f in pths:
            tr = PLUtils.get_track(str(f))
            trks.append(tr)
        mlist = M3U.make_std_m3u_playlist(trks)
        return mlist

    @staticmethod
    def getMoosePlaylists(n: int = 5):
        trks = []
        pths = PLUtils.getLatestMoose(latest=n)

        for f in pths:
            tr = PLUtils.get_track(str(f))
            trks.append(tr)
        mlist = M3U.make_std_m3u_playlist(trks)
        return mlist

    @staticmethod
    def getSTPlaylists(n: int = 5):
        trks = []
        pths = PLUtils.getLatestSTtelling(latest=n)

        for f in pths:
            tr = PLUtils.get_track(str(f))
            trks.append(tr)
        mlist = M3U.make_std_m3u_playlist(trks)
        return mlist


    @staticmethod
    def strftime_play():
        from datetime import datetime

        now = datetime.now()  # current date and time

        year = now.strftime("%Y")
        # print("year:", year)

        month = now.strftime("%m")
        # print("month:", month)

        day = now.strftime("%d")
        # print("day:", day)

        time = now.strftime("%H:%M:%S")
        # print("time:", time)

        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        # print("date and time:", date_time)

        #    comparing datetimes

        # date in yyyy/mm/dd format
        d1 = datetime(2018, 5, 3)
        d2 = datetime(2018, 6, 1)

        # Comparing the dates will return
        # either True or False
        print("d1 is greater than d2 : ", d1 > d2)
        print("d1 is less than d2 : ", d1 < d2)
        print("d1 is not equal to d2 : ", d1 != d2)

    @staticmethod
    def compare_times():
        # Timedelta function demonstration

        # Using current time
        ini_time_for_now = datetime.now()

        # printing initial_date
        print("initial_date", str(ini_time_for_now))

        # Calculating future dates
        # for two years
        future_date_after_2yrs = ini_time_for_now + \
                                 timedelta(days=730)

        future_date_after_2days = ini_time_for_now + \
                                  timedelta(days=2)

        # printing calculated future_dates
        print('future_date_after_2yrs:', str(future_date_after_2yrs))
        print('future_date_after_2days:', str(future_date_after_2days))

    # @staticmethod
    # def getTwoMoreSTPlaylists(latest=4):
    #     trks = []
    #     pths = PLUtils.getLatestWNL()
    #     l = len(pths)
    #     if l < latest:
    #         two_more = pths[-l:-1]
    #     else:
    #         two_more = pths[-latest:-1]
    #     for f in two_more:
    #         tr = PLUtils.get_track(str(f))
    #         trks.append(tr)
    #     mlist = M3U.make_std_m3u_playlist(trks)
    #     return mlist



    # @staticmethod
    # def getLastSTPlaylist():
    #     pths = PLUtils.getLatestSTtelling()
    #     last = pths[-1]
    #     last_track = PLUtils.get_track(str(last))
    #     last_m3u = M3U.make_std_m3u_playlist([last_track])
    #     return last_m3u


    #################################  WNL PLUtils  ##################

    @staticmethod
    def getWNLPlaylists():
        pths = PLUtils.getLatestWNL()
        trks = [PLUtils.get_track(str(p)) for p in pths]

        last_m3u = M3U.make_std_m3u_playlist(trks)
        return last_m3u

    @staticmethod
    def load_tracks(root=Config.YT_DIR, dirs: list = ydl, type='flac', sdir: int = 1):
        testd = dirs[sdir]
        print(f'loading tracks from {testd}')
        pth = f"{root}/{testd}"
        pt = PublicTracks()
        genres = pt.yt_dir_genres.get(testd,None)
        trks = pt.do_yt_walk(fpth=pth, ft=type, genres=genres )
        return trks

    @staticmethod
    def convertMP4_to_MP3(mp4_file: str = "F:/youtube_downloads/blues/Blues'd Up (Stones)/Honky Tonk Woman.mp4"):
        old_abs_fn = Path(mp4_file)
        parent = old_abs_fn.parent
        new_mp3_fn = str(parent) +'/' + str(old_abs_fn.stem) + '.mp3'
        pp = Path(mp4_file)

        # new_mp3 = f"F:/youtube_downloads/blues/Blues'd Up (Stones)/Honky Tonk Woman.mp3"

        clip = mp.VideoFileClip(pp.as_posix())
        clip.audio.write_audiofile(new_mp3_fn)










