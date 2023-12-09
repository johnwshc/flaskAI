class PLSPlaylist():
    __doc__ = '''PLSPlaylist: construct a pandas DataFrame of tracks from .pls playlist. '''

    def __init__(self, df, src='Feedly'):
        super().__init__()
        if df is None:
            self.file = pls
            self.pl_df = self.process_lines()
        else:
            self.pl_df = df
            self.file = None
            self.trk_count = len(df)
            self.version = 2
        if len(self.pl_df) == 1:
            self.is_single_track = True
        else:
            self.is_single_track = False

    def __parse_attr_trk(self, att):
        # pls_tags =['File','Title','Length']

        if att.startswith('File'):
            attr = att[:4]
            trk = att[4:]
        elif att.startswith('Title'):
            attr = att[:5]
            trk = att[5:]
        elif att.startswith('Length'):
            attr = att[:6]
            trk = att[6:]
        else:
            print("Error parsing attr and trk num")
        return (attr, trk)

    def process_lines(self):
        lines = []
        with open(self.file, 'r')  as f:
            for line in f.readlines():

                if line == '\n' or line.startswith('[playlist]'):
                    continue
                elif line.startswith('NumberOfEntries'):
                    line = line.strip()
                    tmps = line.split('=')
                    self.trk_count = int(tmps[1])
                    continue
                elif line.startswith('Version'):
                    line = line.strip()
                    tmps = line.split('=')
                    self.version = int(tmps[1])
                    continue

                else:
                    line = line.strip()
                    lines.append(line.split('='))
        pl_dic = {}

        for l in lines:

            attr_trk = l[0]
            attr, trk = self.__parse_attr_trk(attr_trk)
            if trk in pl_dic.keys():
                pl_dic[trk].append((attr, l[1]))
            else:
                pl_dic[trk] = [(attr, l[1])]

        print(pl_dic)
        tracks = pd.DataFrame(columns=['File', 'Length', 'Title'])

        for track in pl_dic.keys():
            print('track', track)
            idx = []
            dat = []
            attrs = pl_dic[track]
            for attr, val in attrs:
                idx.append(attr)
                dat.append(val)
            ser = pd.Series(data=dat, index=idx)
            tracks = tracks.append(ser, ignore_index=True)

        tracks = tracks.rename(columns={'Length': 'Duration'})
        print('tracks df: \n', tracks)
        return tracks

    def insert_track(self, track, pos='top'):
        if pos == 'top':

            self.pl_df.loc[-1] = track.ser_trk  # adding a row
            self.pl_df.index = self.pl_df.index + 1  # shifting index
            self.pl_df = self.pl_df.sort_index()  # sorting by index
        else:  # bottom
            self.pl_df = self.pl_df.append(track.ser_trk, ignore_index=True)

    def delete_track(self, track_id):
        self.pl_df = self.pl_df.drop(track_id)

    def to_pls(self, pl_df):

        fo = io.StringIO()

        fo.write('\n')
        fo.write('[playlist]\n\n')
        cnt = 1
        for index, row in pl_df.iterrows():
            ln = 'File' + str(cnt) + '=' + row.url + '\n\n'
            fo.write(ln)
            ln = 'Title' + str(cnt) + '=' + row.title + '\n\n'
            fo.write(ln)
            ln = 'Length' + str(cnt) + '=' + str(row.length) + '\n\n'
            fo.write(ln)
            cnt += 1
        ln = 'NumberofEntries=' + str(self.trk_count) + '\n\n'
        fo.write(ln)
        fo.write('Version=' + str(self.version) + '\n')
        return fo.getvalue()
