import requests
from analz.playlist.plutils import PLUtils
from config import Config
import json
import os
import shutil
import pandas as pd

from datetime import datetime

class RDJApi:
    """

    Rest URL for commands

    http://127.0.0.1:7000/opt?auth=changeme&command=PlayPlaylistTrack&arg=0

    Commands:

        PlayPlaylistTrack 'Zero based track number from playlist
        RemovePlaylistTrack 'Zero based track number from playlist
        StopPlayer
        PausePlayer 'arg=0 to unpause, 1 to pause
        RestartPlayer
        PlayFromIntro
        ClearPlaylist
        LoadTrackToTop 'Song ID as argument
        LoadTrackToBottom 'Song ID as argument
        LoadPlaylist 'Playlist ID as argument
        EnableAutoDJ 'arg=0 to disable, 1 to enable
        EnableAssisted 'arg=0 to disable, 1 to enable
        EnableEvents 'arg=0 to disable, 1 to enable
        RefreshEvents
        EnableInput 'arg=0 to disable, 1 to enable
        PlaycartByNumber 'cart number as argument
        StatusAutoDJ 'Get the status of AutoDJ option as boolean
        StatusAssisted 'Get the status of Assisted option as boolean
        StatusInput 'Get the status of Input option as boolean
        StatusQueue 'Get queue playlist number of tracks
        ShowMessage 'Display a message in RadioDJ. Message as argument
    """

    url1 = f"http://127.0.0.1:7000/opt?auth=changeme&command=PlayPlaylistTrack&arg=0"
    pw = 'vil3nin'

    @staticmethod
    def PlayPlaylistTrack():
        url = f"http://127.0.0.1:7000/opt"
        data = {'auth': RDJApi.pw, 'command': 'PlayPlaylistTrack', 'arg': '1'}
        res = requests.get(url=url, params=data)
        return res

    @staticmethod
    def StatusInput():
        url = f"http://127.0.0.1:7000/opt"
        data = {'auth': RDJApi.pw, 'command': 'StatusInput'}
        return requests.get(url=url, params=data)

    @staticmethod
    def LoadTrack(id=18394):
        url = f"http://127.0.0.1:7000/opt"
        data = {'auth': RDJApi.pw, 'command': 'LoadTrackToTop', 'arg': id}
        return requests.get(url=url, params=data)

    @staticmethod
    def get_whats_playing():
        url = 'http://127.0.0.1:7000/np'

        data = {'auth': 'vil3nin'}

        res = requests.get(url=url, params=data)
        return res


class EventQueue:
    """ An Event Messaging Queue and manager"""

    def __init__(self):
        print('instance of Event Queue')
        self.event_defs = RDJEvent.load_evt_defs()
        # print('loaded event_defs')
        self.queue = pd.Series()


    def register(self, rdjEv):
        name, obj = rdjEv
        print(f"in register: {name} / {obj}")
        ss = pd.Series({name: obj})
        self.queue = self.queue.append(ss)

    def un_register(self, name: str):
        self.queue.pop(name)

    def log_event(self, evt_out):
        log = RDJEvent.event_log
        # print(f"logging event: {evt_out}")
        log_exists = os.path.exists(log)
        log_is_empty = os.path.getsize(log) < 1

        if log_exists and not log_is_empty:

            with open(log) as f:

                l:list = json.load(f)
                if len(l) > 50:
                    old_log = f"{log}_{str(datetime.timestamp(datetime.now()))}.old"
                    with open(old_log, "w") as ff:
                        json.dump(l, ff)
                    l = [evt_out]
                else:
                    l.append(evt_out)
            with open(log, "w") as f:
                json.dump(l, f)
        else:
            with open(log, "w") as f:
                json.dump([evt_out], f)


# ser2 = ser.loc[['Pandas', 'Spark', 'Python']]

# Below are quick examples.

# Examples 1: Use Series.loc[] function to selected labels
# ser2 = ser.loc[['Pandas', 'Spark', 'Python']]

# Examples 2: Select Rows Between two Index Labels
# Includes both Spark and Python rows
# ser2 = ser.loc['Spark':'Python']

# Examples 3: Select Alternate rows by indeces
# ser2 = ser.loc['Spark':'Pandas':2]

# Examples 4: Use loc[] and lambda
# ser2 = ser.loc[lambda x : x == 28000]

# Examples 5: Use loc[] property & OR condition
# ser2 = ser.loc[lambda x : (x  28000)]


class ERMonitor:
    # Functions setup

    def __init__(self):
        self.name = "case_bot"
        # self.scheduler = ERSchedular()
        self.event_queue = EventQueue()
        self.control = self.initialize_playlists()

    def initialize_playlists(self):
        return RDJEventControl(self.event_queue)

    def fire_all_m3u_changes(self):
        q = self.event_queue.queue
        keys = q.keys()
        objs = [q.get(k) for k in keys]
        vv = [o.fire() for o in objs]
        return vv


class RDJEvent(object):
    """ The RDJEvent class models an Radio DJ Event,
       with a common interface of a specific m3u playlist file.
       It further provides methods for updating an
       event schedule. Specific rdj events will subclass this template """

    categories = ['monday', 'tuesday', 'wednesday', 'thursday',
                  'friday', 'saturday', 'sunday', 'daily', 'all', 'Default']
    event_types = {'last_fanny': 'Repeat By Day',
                   'last_wnl': 'Repeat By Day',
                   'mystery_radio': 'Repeat By Day',
                   'old_time_stories': 'Repeat By Day',
                   'bg_days': 'Repeat By Day',
                   'bg_nite': 'Repeat By Day'}

    # sample_datetime_string:
    #   dt_string = "12/11/2018 09:15:32"
    #
    # # Considering date is in dd/mm/yyyy format
    # dt_object1 = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")
    # print("dt_object1 =", dt_object1)

    default_event_data = {

        'last_fanny': {
            'm3u_files': ['stlast.m3u'],
            'cat': categories[8],
            'type': 'Repeat By Day',
            'stime': '19:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },

        'wnl_last': {
            'm3u_files': ['wnl_last.m3u'],
            'cat': categories[8],
            'type': 'Repeat By Day',
            'stime': '20:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'bg_days': {
            'm3u_files': ['bg_days.m3u'],
            'cat': categories[1],
            'type': 'Repeat By Day',  # Tuesday
            'stime': '06:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'bg_nite': {
            'm3u_files': ['bg_nite.m3u'],  # Tuesday Night Bluegrass
            'cat': categories[1],
            'type': 'Repeat By Day',
            'stime': '16:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'jazz_day': {
            'm3u_files': ['jazz_day.m3u'],  # Friday Jazz
            'cat': categories[4],
            'type': 'Repeat By Day',
            'stime': '06:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'jazz_night': {
            'm3u_files': ['jazz_nite.m3u'],  # Friday Jazz
            'cat': categories[4],
            'type': 'Repeat By Day',
            'stime': '16:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'rr_days': {
            'm3u_files': ['roots_days.m3u'],  # Wednesday Roots
            'cat': categories[2],
            'type': 'Repeat By Day',
            'stime': '06:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'rr_nite': {
            'm3u_files': ['roots_nite.m3u'],  # Wednesday night roots
            'cat': categories[2],
            'type': 'Repeat By Day',
            'stime': '16:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'mystery_radio': {
            'm3u_files': ['mystery.m3u'],  # Every Night Mystery
            'cat': categories[8],
            'type': 'Repeat By Day',
            'stime': '21:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'sstories': {
            'm3u_files': ['sstories.m3u'],  # Every Night Short Stories
            'cat': categories[8],
            'type': 'Repeat By Day',
            'stime': '22:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'salty': {
            'm3u_files': ['salty_last.m3u'],  # salty dog shows
            'cat': categories[9],
            'type': 'Repeat By Day',
            'stime': None,  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'moose': {
            'm3u_files': ['moose_last.m3u'],  # blues moose shows
            'cat': categories[9],
            'type': 'Repeat By Day',
            'stime': None,  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'cntry_days': {
            'm3u_files': ['cntry_days.m3u'],  # Monday Country Days
            'cat': categories[0],
            'type': 'Repeat By Day',
            'stime': '06:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'cntry_nite': {
            'm3u_files': ['cntry_nite.m3u'],  # Monday Country Nights
            'cat': categories[0],
            'type': 'Repeat By Day',
            'stime': '16:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'blues_radio_days': {
            'm3u_files': ['salty_last.m3u', 'moose_last.m3u'],  # Saturday Blues Radio
            'cat': categories[5],
            'type': 'Repeat By Day',
            'stime': '06:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'jazz_radio_nite': {
            'm3u_files': ['jazz_radio_nite.m3u'],  # Saturday night jazz Radio
            'cat': categories[5],
            'type': 'Repeat By Day',
            'stime': '16:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
       },
        'night_shift': {
            'm3u_files': ['night_shift.m3u'],  # Everydat Night Shift
            'cat': categories[8],
            'type': 'Repeat By Day',
            'stime': '23:55:00',  # format:  "%d/%m/%Y %H:%M:%S"
       }

    }
    rdj_m3u_dir = Config.RDJ_M3U_TEMPLATES_DIR
    event_log = Config.RDJ_EVENT_LOG
    events_def = Config.RDJ_EVENTS_DEF

    @staticmethod
    def load_evt_defs():
        if os.path.exists(RDJEvent.events_def):
            with open(RDJEvent.events_def) as f:
                d = json.load(f)
            return d

        else:
            return RDJEvent.default_event_data

    @staticmethod
    def save_evt_defs(d: dict = default_event_data):
        import shutil
    #     back up existing defs, if any
        if os.path.exists(RDJEvent.events_def):

            sts = str(datetime.timestamp())
            nfn = f"{RDJEvent.events_def}_{sts}.old"
            shutil.copy(RDJEvent.events_def, nfn)
            # print(f"copied {RDJEvent.events_def} to {nfn}")
            with open(RDJEvent.events_def, "w") as f:
                json.dump(d, f)
        else:
            with open(RDJEvent.events_def, "w") as f:
                json.dump(d, f)

    def __init__(self):
        print(" Instance of RDJEvemt ")
        # class datetime.datetime(year, month, day, hour=0, minute=0, second=0,
        #                   microsecond=0, tzinfo=None, *, fold=0)¶

        # hour_time_start is in format 'HH:MM:SS'  -- ignored in some commands

        self.enable = False
        self.ts = datetime.now()
        self.evmq = None

    def setEVMQ(self, evmq: EventQueue):
        self.evmq = evmq



    # def log_event(self, ev_out: dict = None):
    #     logger = self.evmq.logger
    # 
    #     sample_event = {'event_type':
    #                         'Repeat By Day',
    #                     'dt': '08/29/2023, 11:07:05',
    #                     'category': 'all',
    #                     'event_m3u_files': ['stlast.m3u'],
    #                     'rdj_start_time': '19:01:00',
    #                     'ename': 'last_fanny.fire'
    #                     }
    #     if not ev_out:
    #         ev_out = sample_event
    #     print(f"logging event: {ev_out}")
    #     logger.append(ev_out)


################################################################
# def __init__(self, length):
#     super().__init__(length, length)
##################################################################


class LastFanny(RDJEvent):
    from datetime import datetime

    # dt_string = "12/11/2018 09:15:32"
    #
    # # Considering date is in dd/mm/yyyy format
    # dt_object1 = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")
    # print("dt_object1 =", dt_object1)
    #
    # # Considering date is in mm/dd/yyyy format
    # dt_object2 = datetime.strptime(dt_string, "%m/%d/%Y %H:%M:%S")
    # print("dt_object2 =", dt_object2)
    LF_START_TIME = "19:01:00"  # HH:MM:SS

    def __init__(self, evmq: EventQueue):
        super().__init__()
        print("instance of LastFanny")
        edef = RDJEvent.default_event_data['last_fanny']
        self.evt_dic = edef
        self.evmq = evmq

        # dd = {'last_fanny':
        #         {
        #             'm3u_files': ['stlast.m3u'],
        #             'cat': RDJEvent.categories[8],
        #             'type': 'Repeat By Day',
        #             'stime': '19:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
        #         }
        # }


        self.rdj_start_time = edef['stime']
        self.name = 'last_fanny'
        self.event_type = self.evt_dic['type'] # Repeat by day
        self.category = self.evt_dic['cat']  # all
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time
        }

    def fire(self):
        # print(f"writing last_fanny playlist m3u file")
        #         write target playlist file to rdj_templates dir
        st_list = PLUtils.getSTPlaylists()
        # print("got playlists")
        for fn in self.event_m3u_files:
            # print(f" fire...: rewrite {fn}")
            with open(f"{self.rdj_m3u_dir}/{fn}", "w") as f:
                f.writelines(st_list)
        #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)


class WNLLast(RDJEvent):
    LWNL_START_TIME = "20:01:00"  # HH:MM:SS

    def __init__(self, evmq: EventQueue):
        super().__init__()
        print("instance of WNLLast")
        edef: dict = RDJEvent.default_event_data['wnl_last']
        self.evt_dic = edef
        self.evmq = evmq

      # message queue for receiving cmds (fire) now in base class

        # evt_dic model:
        # 'wnl_last': {
        #     'm3u_files': ['wnl_last.m3u'],
        #     'cat': categories[8],
        #     'type': 'Repeat By Day',
        #     'stime': '20:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
        # # },

        self.rdj_start_time = edef['stime']
        self.name = 'wnl_last'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']  # all
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time
        }

    def fire(self):
        # print(f"writing last_fanny playlist m3u file")
        #         write target playlist file to rdj_templates dir
        wnl_list = PLUtils.getWNLPlaylists()
        # print("got wnl playlists", wnl_list)
        for fn in self.event_m3u_files:
            # print(f" fire...: rewrite {fn}")
            with open(f"{self.rdj_m3u_dir}/{fn}", "w") as f:
                f.writelines(wnl_list)
        #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)


class Mystery(RDJEvent):
    MYSTERY_START_TIME = "21:01:00"  # HH:MM:SS

    def __init__(self, evmq: EventQueue):
        super().__init__()
        print("instance of Mystery")
        edef = RDJEvent.default_event_data['mystery_radio']
        self.evt_dic = edef
        self.evmq =  evmq

        # 'mystery_radio': {
        #     'm3u_files': ['mystery.m3u'],  # Every Night Mystery
        #     'cat': categories[8],
        #     'type': 'Repeat By Day',
        #     'stime': '21:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
        # }

        self.rdj_start_time = edef['stime']
        self.name = 'mystery_radio'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']  # all
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))



    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time
        }

    #  Select one m3u file at random from files beginning with 'mystery'
    #
    def fire(self):
        # print(f"writing mystery playlist m3u file")
        #         write target playlist file to rdj_templates dir
        mys_m3u = PLUtils.getMysteryM3Us(key=None)
        fnew = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{mys_m3u}"
        # print(f"new myst m3u file: {fnew}")
        f = self.event_m3u_files[0]
        fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
        # print(f"current mys file: {fcurr}")
        fold = f'{fcurr}_{str(datetime.timestamp(datetime.now()))}.old'
        # print(f"saved curr file: {fold}")
        shutil.copy(fcurr,fold)
        shutil.copy(fnew, fcurr)
        # print(f"Renamed current pl to curr.name.ts.old; copied new to curr.name")


        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)

class BGDays(RDJEvent):

    """ Radio DJ Bluegrass Days Event """
    name = 'bg_days'
    def __init__(self, evmq: EventQueue):
        super().__init__()

        # 'bg_days': {
        #     'm3u_files': ['bg_days.m3u'],
        #     'cat': categories[1],
        #     'type': 'Repeat By Day',  # Tuesday
        #     'stime': '06:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
        # },

        print("instance of BGDays")
        edef = RDJEvent.default_event_data['bg_days']
        self.evmq = evmq
        self.evt_dic = edef
        self.rdj_start_time = edef['stime']
        self.name = 'bg_days'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']  # all
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time,
            'ename': 'bg_days.fire'

        }

    def fire(self):
        # print(f"writing bg_days playlist m3u file")
        #         write target playlist file to rdj_templates dir
        bg_days_m3u = PLUtils.getBGDays()  # random bg m3u file  as str
        # print(f"bg)days m3u fn: {bg_days_m3u}")
        fnew = bg_days_m3u
        # print(f"new bgdays m3u file: {fnew}")
        f = self.event_m3u_files[0]
        fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
        fold = f"{fcurr}_{str(datetime.timestamp(datetime.now()))}.old"
        shutil.copy(fcurr, fold)
        shutil.copy(fnew, fcurr)
        # print(f"Renamed current pl to curr.name.ts.old; wrote new m3u str to curr.name")
        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)

class BGNite(RDJEvent):

    """ Radio DJ Bluegrass Nights Event """

    name = 'bg_night'

    def __init__(self, evmq: EventQueue):
        super().__init__()

        #
        # 'bg_nite': {
        #     'm3u_files': ['bg_nite.m3u'],  # Tuesday Night Bluegrass
        #     'cat': categories[1],
        #     'type': 'Repeat By Day',
        #     'stime': '16:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
        # }

        print("instance of BGNite")
        edef = RDJEvent.default_event_data['bg_nite']
        self.evt_dic = edef

        self.evmq = evmq  # message queue for receiving cmds (fire)

        self.rdj_start_time = edef['stime']
        self.name = 'bg_nite'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']  # all
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time,
            'ename': ''
        }

    def fire(self):
        # print(f"writing bg_days playlist m3u file")
        #         write target playlist file to rdj_templates dir
        bg_nite_m3u = PLUtils.getBGNite()
        fnew = bg_nite_m3u
        f = self.event_m3u_files[0]
        fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
        fold = f"{fcurr}_{str(datetime.timestamp(datetime.now()))}.old"
        shutil.copy(fcurr, fold)
        shutil.copy(fnew, fcurr)
        # print(f"Renamed current pl to curr.name.ts.old; copied new to curr.name")

        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)


class JazzDay(RDJEvent):

    # 'jazz_day': {
    #     'm3u_files': ['jazz_day.m3u'],  # Friday Jazz
    #     'cat': categories[4],
    #     'type': 'Repeat By Day',
    #     'stime': '06:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
    # }

    """ Radio DJ Bluegrass Nights Event """

    name = 'jazz_day'

    def __init__(self, evmq: EventQueue):
        super().__init__()

        print("instance of JazzDay")

        edef: dict = RDJEvent.default_event_data['jazz_day']
        self.evt_dic = edef
        self.evmq = evmq  # message queue for receiving cmds (fire)

        self.rdj_start_time = edef['stime']
        self.name = 'jazz_day'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time,
            'ename': ''
        }

    def fire(self):
        # print(f"writing bg_days playlist m3u file")
        #         write target playlist file to rdj_templates dir
        jazz_day_m3u = PLUtils.getJazzDay()
        fnew = jazz_day_m3u
        # print(f"fnew: {fnew}")
        f = self.event_m3u_files[0]
        fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
        # print(f"fcurr: {fcurr}")
        fold = f"{fcurr}_{str(datetime.timestamp(datetime.now()))}.old"
        # print(f"fold: {fold}")
        shutil.copy(fcurr, fold)
        shutil.copy(fnew, fcurr)
        # print(f"Renamed current pl to curr.name.ts.old; copied new to curr.name")

        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)

class JazzNight(RDJEvent):

    # 'jazz_night': {
    #     'm3u_files': ['jazz_nite.m3u'],  # Friday Jazz
    #     'cat': categories[4],
    #     'type': 'Repeat By Day',
    #     'stime': '16:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
    # }

    """ Radio DJ Bluegrass Nights Event """

    name = 'jazz_night'

    def __init__(self, evmq: EventQueue = None):
        super().__init__()

        print("instance of JazzNight")
        edef = RDJEvent.default_event_data['jazz_night']
        self.evt_dic = edef   

        self.rdj_start_time = edef['stime']
        self.name = 'jazz_night'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq = evmq
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time,
            'ename': ''
        }

    def fire(self):
        # print(f"writing bg_days playlist m3u file")
        #         write target playlist file to rdj_templates dir
        jazz_night_m3u = PLUtils.getJazzNight()
        fnew = jazz_night_m3u
        f = self.event_m3u_files[0]
        fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
        fold = f"{fcurr}_{str(datetime.timestamp(datetime.now()))}.old"
        shutil.copy(fcurr, fold)
        shutil.copy(fnew, fcurr)
        # print(f"Renamed current pl to curr.name.ts.old; copied new to curr.name")

        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)


class RRDays:

    # 'rr_days': {
    #     'm3u_files': ['roots_days.m3u'],  # Wednesday Roots
    #     'cat': categories[2],
    #     'type': 'Repeat By Day',
    #     'stime': '06:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
    # },
    """ Radio DJ Roots and Rock N Roll Event """

    name = 'rr_days'

    def __init__(self, evmq: EventQueue = None):
        super().__init__()
      
        print("instance of RRDays")
        edef = RDJEvent.default_event_data[RRDays.name]
        self.evt_dic = edef
        self.evmq = evmq
        self.rdj_start_time = edef['stime']
        self.name = 'rr_days'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time,
            'ename': ''
        }

    def fire(self):
        # print(f"writing rr_days playlist m3u file")
        #         write target playlist file to rdj_templates dir
        rr_days_m3u = PLUtils.getRRDays()
        fnew = rr_days_m3u
        f = self.event_m3u_files[0]
        fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
        fold = f"{fcurr}_{str(datetime.timestamp(datetime.now()))}.old"
        shutil.copy(fcurr, fold)
        shutil.copy(fnew, fcurr)
        # print(f"Renamed current pl to curr.name.ts.old; copied new to curr.name")

        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)


class RRNite:

        # 'rr_nite': {
        #     'm3u_files': ['roots_nite.m3u'],  # Wednesday night roots
        #     'cat': categories[2],
        #     'type': 'Repeat By Day',
        #     'stime': '16:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
        # },
        """ Radio DJ RR Nights Event """

        name = 'rr_nite'

        def __init__(self, evmq: EventQueue = None):
            super().__init__()

            print("instance of RRNite")
            edef = RDJEvent.default_event_data[RRNite.name]
            self.evt_dic = edef
           
            self.evmq = evmq  # message queue for receiving cmds (fire)

            self.rdj_start_time = edef['stime']
            self.name = 'rr_nite'
            self.event_type = self.evt_dic['type']  # Repeat by day
            self.category = self.evt_dic['cat']
            self.event_m3u_files = self.evt_dic['m3u_files']
            self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
            self.evmq.register((self.name, self))

        def __to_dict(self):
            return {
                'name': self.name,
                'event_type': self.event_type,
                'dt': self.dt,
                'category': self.category,
                'event_m3u_files': self.event_m3u_files,
                'rdj_start_time': self.rdj_start_time,
                'ename': ''
            }

        def fire(self):
            # print(f"writing rr_nite playlist m3u file")
            #         write target playlist file to rdj_templates dir
            rr_nite_m3u = PLUtils.getRRNite()
            fnew = rr_nite_m3u
            # print(f"got fnew: {fnew}")
            f = self.event_m3u_files[0]
            fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
            # print(f"curr file: {fcurr}")
            fold = f"{fcurr}_{str(datetime.timestamp(datetime.now()))}.old"
            shutil.copy(fcurr, fold)
            shutil.copy(fnew, fcurr)
            # print(f"Renamed current pl to curr.name.ts.old; copied new to curr.name")

            # #  record to event log (json file)
            self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            ev_out = self.__to_dict()
            ev_out['ename'] = f"{self.name}.fire"
            self.evmq.log_event(ev_out)


class ShortStories(RDJEvent):

    # 'sstories': {
    #     'm3u_files': ['sstories.m3u'],  # Every Night Short Stories
    #     'cat': categories[8],
    #     'type': 'Repeat By Day',
    #     'stime': '22:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
    # }

    """ Radio DJ Short Stories Event """

    name = 'sstories'

    def __init__(self, evmq: EventQueue):
        super().__init__()

        print("instance of ShortStories")
        edef: dict = RDJEvent.default_event_data[ShortStories.name]
        self.evt_dic = edef
        
        self.evmq = evmq  # message queue for receiving cmds (fire)

        self.rdj_start_time = edef['stime']
        self.name = 'sstories'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time,
            'ename': ''
        }

    def fire(self):
        # print(f"writing rr_nite playlist m3u file")
        #         write target playlist file to rdj_templates dir
        sstories_m3u = PLUtils.getSStories()
        fnew = sstories_m3u
        f = self.event_m3u_files[0]
        fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
        fold = f"{fcurr}_{str(datetime.timestamp(datetime.now()))}.old"
        shutil.copy(fcurr, fold)
        shutil.copy(fnew, fcurr)
        # print(f"Renamed current pl to curr.name.ts.old; copied new to curr.name")

        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)


class CntryDays(RDJEvent):

    # 'cntry_days': {
    #     'm3u_files': ['cntry_days.m3u'],  # Monday Country Days
    #     'cat': categories[0],
    #     'type': 'Repeat By Day',
    #     'stime': '06:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
    # },

    """ Radio DJ Country Music Days Event """

    name = 'cntry_days'

    def __init__(self, evmq: EventQueue):
        super().__init__()

        print("instance of CntryDays")
        edef = RDJEvent.default_event_data[CntryDays.name]
        self.evt_dic = edef
        self.evmq = evmq  # message queue for receiving cmds (fire)

        self.rdj_start_time = edef['stime']
        self.name = 'cntry_days'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time,
            'ename': ''
        }

    def fire(self):
        # print(f"writing rr_nite playlist m3u file")
        #         write target playlist file to rdj_templates dir
        cntry_days_m3u = PLUtils.getCntryDays()
        fnew = cntry_days_m3u
        f = self.event_m3u_files[0]
        fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
        fold = f"{fcurr}_{str(datetime.timestamp(datetime.now()))}.old"
        shutil.copy(fcurr, fold)
        shutil.copy(fnew, fcurr)
        # print(f"Renamed current pl to curr.name.ts.old; copied new to curr.name")

        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)


class CntryNite(RDJEvent):

    """ Radio DJ Country Music Nite Event """

    #  'cntry_nite': {
    #     'm3u_files': ['cntry_nite.m3u'],  # Monday Country Nights
    #     'cat': categories[0],
    #     'type': 'Repeat By Day',
    #     'stime': '16:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
    # }

    name = 'cntry_nite'

    def __init__(self, evmq: EventQueue):
        super().__init__()

        print("instance of CntryNite")
        edef = RDJEvent.default_event_data[CntryNite.name]
        self.evt_dic = edef

        self.evmq = evmq  # message queue for receiving cmds (fire)

        self.rdj_start_time = edef['stime']
        self.name = 'cntry_nite'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):

        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time,
            'ename': ''
        }

    def fire(self):
        # print(f"writing rr_nite playlist m3u file")
        #         write target playlist file to rdj_templates dir
        cntry_nite_m3u = PLUtils.getCntryNite()
        fnew = cntry_nite_m3u
        f = self.event_m3u_files[0]
        fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
        fold = f"{fcurr}_{str(datetime.timestamp(datetime.now()))}.old"
        shutil.copy(fcurr, fold)
        shutil.copy(fnew, fcurr)
        # print(f"Renamed current pl to curr.name.ts.old; copied new to curr.name")

        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)


class BluesRadioDays(RDJEvent):

    """ playing blues radio streams or podcasts """
    #
    # 'blues_radio_days': {
    #     'm3u_files': ['blues_radio_days.m3u'],  # Saturday Blues Radio
    #     'cat': categories[5],
    #     'type': 'Repeat By Day',
    #     'stime': '06:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
    # },
    name = 'blues_radio_days'

    def __init__(self, evmq: EventQueue):
        super().__init__()

        print("instance of BluesRadioDays")
        edef: dict = RDJEvent.default_event_data[BluesRadioDays.name]
        self.evt_dic = edef

        self.evmq = evmq  # message queue for receiving cmds (fire)
        self.rdj_start_time = edef['stime']
        self.name = 'blues_radio_days'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time,
            'ename': ''
        }

    def fire(self):
        # print(f"writing blues radio days playlist m3u file")
        #         write target playlist file to rdj_templates dir
        salt, moose = PLUtils.getBluesRadioDays()


        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        ev_out['description'] = f'reset salty_last {salt} and moose_last  {moose} m3us'
        self.evmq.log_event(ev_out)



class JazzRadioNite(RDJEvent):

    """ Jazz Radio Streams Nite """

    # 'jazz_radio_nite': {
    #     'm3u_files': ['jazz_radio_nite.m3u'],  # Saturday night jazz Radio
    #     'cat': categories[5],
    #     'type': 'Repeat By Day',
    #     'stime': '16:01:00',  # format:  "%d/%m/%Y %H:%M:%S"
    # }

    name = 'jazz_radio_nite'

    def __init__(self, evmq: EventQueue):
        super().__init__()

        print("instance of JazzRadioNite")
        edef: dict = RDJEvent.default_event_data[JazzRadioNite.name]
        self.evt_dic = edef
        self.evmq = evmq  # message queue for receiving cmds (fire)
        self.rdj_start_time = edef['stime']
        self.name = 'jazz_radio_nite'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time,
            'ename': ''
        }

    def fire(self):

        # print(f"writing jazz radio nite playlist m3u file")

        #         write target playlist file to rdj_templates dir

        jazz_radio_nite_m3u = PLUtils.getJazzRadioNite()
        fnew = jazz_radio_nite_m3u
        # print(f"fnew: {fnew}")
        f = self.event_m3u_files[0]
        fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
        # print(f"fcurr: {fcurr}")
        fold = f"{fcurr}_{str(datetime.timestamp(datetime.now()))}.old"
        # print(f"fold: {fold}")
        try:
            shutil.copy(fcurr, fold)
            # print(f"copied {fcurr} to {fold}")
            shutil.copy(fnew, fcurr)
        except Exception() as inst:
            print(f"error copying files...{str(inst)}")
        # print(f"Renamed current pl to curr.name.ts.old; copied new to curr.name")

        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)


class NightShift(RDJEvent):
    """ mysteries and weirdness """

    # 'night_shift': {
    #     'm3u_files': ['night_shift.m3u'],  # Everydat Night Shift
    #     'cat': categories[8],
    #     'type': 'Repeat By Day',
    #     'stime': '23:55:00',  # format:  "%d/%m/%Y %H:%M:%S"
    # }



    name = 'night_shift'

    def __init__(self, evmq: EventQueue):
        super().__init__()

        print("instance of NightShift")
        edef: dict = RDJEvent.default_event_data[NightShift.name]
        self.evt_dic = edef
        self.evmq = evmq  # message queue for receiving cmds (fire)
        self.rdj_start_time = edef['stime']
        self.name = 'night_shift'
        self.event_type = self.evt_dic['type']  # Repeat by day
        self.category = self.evt_dic['cat']
        self.event_m3u_files = self.evt_dic['m3u_files']
        self.dt = datetime.strptime(self.rdj_start_time, "%H:%M:%S")
        self.evmq.register((self.name, self))

    def __to_dict(self):
        return {
            'name': self.name,
            'event_type': self.event_type,
            'dt': self.dt,
            'category': self.category,
            'event_m3u_files': self.event_m3u_files,
            'rdj_start_time': self.rdj_start_time,
            'ename': ''
        }

    def fire(self):
        # print(f"writing rr_nite playlist m3u file")

        #         write target playlist file to rdj_templates dir

        night_shift_m3u = PLUtils.getNightShift()
        fnew = night_shift_m3u
        f = self.event_m3u_files[0]
        fcurr = f"{Config.RDJ_M3U_TEMPLATES_DIR}/{f}"
        fold = f"{fcurr}_{str(datetime.timestamp(datetime.now()))}.old"
        shutil.copy(fcurr, fold)
        shutil.copy(fnew, fcurr)
        # print(f"Renamed current pl to curr.name.ts.old; copied new to curr.name")

        # #  record to event log (json file)
        self.dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ev_out = self.__to_dict()
        ev_out['ename'] = f"{self.name}.fire"
        self.evmq.log_event(ev_out)


class RDJEventControl:

    def __init__(self, eq: EventQueue):
        self.eq = eq
        self.lf = LastFanny(self.eq)
        self.wnl = WNLLast(self.eq)
        self.mys = Mystery(self.eq)
        self.bgd = BGDays(self.eq)
        self.bgn = BGNite(self.eq)
        self.jzd = JazzDay(self.eq)
        self.jzn = JazzNight(self.eq)
        self.rrd = RRDays(self.eq)
        self.rrn = RRNite(self.eq)
        self.cnd = CntryDays(self.eq)
        self.cnn = CntryNite(self.eq)
        self.brd = BluesRadioDays(self.eq)
        self.jrn = JazzRadioNite(self.eq)
        self.ns = NightShift(self.eq)











