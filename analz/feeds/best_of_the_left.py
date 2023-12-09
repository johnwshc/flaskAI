# import pandas as pd
# from feeds.tracks import Track
# from feeds.streams import FeedlyStreams
# import json
#
#
# class BestOfTheLeft(FeedlyStreams):
#
#     def __init__(self):
#         super().__init__()
#
#         self.feed_id = self.fapi.feeds_ids['Best of the Left']
#         self.stream_id = self.feed_id
#
#         self.feed = None
#         self.df = None
#         self.trk_list = None
#         self.get_track_list()
#
#     def get_track_list(self):
#         self.feed = json.loads(self.fapi.get_stream(self.stream_id))
#         trks = []
#         items = self.feed['items']
#         dtrk = Track.get_feedly_track_template()
#         for trk in items:
#             dtrk['fid'] = trk.get('id', None)
#             dtrk['title'] = trk.get('title', None)
#             ct = trk.get('content', None)
#             if ct:
#                 print('content -- ', ct)
#                 dtrk['desc'].append(trk['content'])
#             dtrk['url'] = trk.get('enclosure')[0].get('href')
#             dtrk['length'] = trk.get('enclosure')[0].get('length')
#             dtrk['mime_type'] = trk.get('enclosure')[0].get('type')
#             dtrk['author'] = trk.get('author', None)
#
#             trks.append(Track(json.dumps(dtrk)))
#             dtrk = Track.get_feedly_track_template()
#         sers = []
#         for t in trks:
#             sers.append(t.ser_trk)
#         self.df = pd.DataFrame(data=sers)
#         self.trk_list = trks
#
#     # def get_eu_entries():
#     #     trks = []
#     #
#     #     for trk in sample_entries['items']:
#     #         dtrk = {'fid':trk.get('id',None),
#     #                'title':trk.get('title',None),
#     #                'desc':trk.get('content',None),
#     #                'url': trk.get('enclosure')[0].get('href'),
#     #                'length':trk.get('enclosure')[0].get('length'),
#     #                'mime_type':trk.get('enclosure')[0].get('type'),
#     #                'author':trk.get('author',None)
#     #                }
#     #         trks.append(Track(json.dumpdtrk))
#     #     sers = []
#     #     for t in trks:
#     #         sers.append(t.ser_trk)
#     #
#     #     return pd.DataFrame(data=sers)