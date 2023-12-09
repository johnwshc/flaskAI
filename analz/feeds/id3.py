
from pydub import AudioSegment
import os
from pathlib import Path
import shutil
from tinytag import TinyTag
from mutagen.easyid3 import EasyID3
import mutagen


class ID3:
    samp_f = 'c:\\itunes2\\copies\\03 Amnesia.m4a'

    # {'genre': [u'Space Funk'], 'title': [u'This is a title'], 'artist': [u'Artist Name']}
    # @staticmethod
    # def add_tags(fp, tags: dict):
    #
    #     try:
    #         meta = EasyID3(fp)
    #     except mutagen.id3.ID3NoHeaderError:
    #         meta = mutagen.File(fp, easy=True)
    #         meta.add_tags()
    #     meta['title'] = tags.get('title')
    #     meta['artist'] = tags.get('artist')
    #     # meta['duration'] = tags.get('duration')
    #     meta['genre'] = tags.get('genre', None)
    #     meta['album'] = tags.get('album', None)
    #     meta.save()

    @staticmethod
    def convert_song(song_file, fmt, out_dir):
        meta_info = ID3.get_song_info(song_file)
        song = AudioSegment.from_file(song_file, format=fmt)
        p_song = Path(song_file)
        song_out_fn = p_song.stem + '.mp3'
        song.export(out_dir + '\\' + song_out_fn, format='mp3', tags=meta_info.dict(), id3v2_version='3')
        tup = (out_dir + '\\' + song_out_fn, meta_info.dict() )
        return tup

    @staticmethod
    def convert_raw_mp3(song_file, out_fn, meta, fmt='mp3', out_dir='c:\\itunes2\\promo'):
        song = AudioSegment.from_file(song_file,format=fmt)
        # p_song =  Path(song_file)
        # song_out_fn = p_song.stem + '.mp3'
        song.export(out_fn, format='mp3', tags=meta.dict(), id3v2_version='3')
        tup = (out_dir + '\\' + out_fn, meta.dict())
        return tup

    @staticmethod
    def merge_audio_segments(f1, f2, f_out, out_dir, meta, fade=1000):
        __doc__= 'Luv Pydub -- Merge two tracks (e.g. promo and track) -  rewrite meta data, add cross-fade'
        combined = AudioSegment.empty()
        combined = combined.append(f1, crossfade=fade)
        combined = combined.append(f2)
        combined.export(out_dir + "\\" + f_out, format="mp3", tags=meta.dict(), id3v2_version='3')

    # @staticmethod
    # def add_new_tags(f, tags):
    #     ID3.add_tags(f, tags)

    @staticmethod
    def get_song_info(filepath):
        # m = MetaInfo()
        try:
            p = Path(filepath)
            tag = TinyTag.get(filepath)
            # print(tag)
        except LookupError:
            return MetaInfo()
        # make sure everthing returned (except length) is a string
        for attribute in ['artist', 'title', 'duration', 'album', 'genre']:
            # print('attribute in: ', attribute)
            if (getattr(tag, attribute) is None) or (getattr(tag, attribute) == ''):
                # print('attr is: ', getattr(tag, attribute))
                if attribute == 'title':
                    if ' - ' in p.stem:
                        ss = p.stem.split(' - ', 1)
                        setattr(tag, attribute, ss[1])
                        # print('after setting title to ' + ss[1] + ':', getattr(tag, attribute))
                    else:
                        setattr(tag, attribute, p.stem)

                elif attribute == 'artist':
                    if ' - ' in p.stem:
                        ss = p.stem.split(' - ')
                        setattr(tag, attribute, ss[0])

                    else:
                        setattr(tag, attribute, 'Unknown')

                elif attribute == 'genre':
                    setattr(tag, attribute, 'Unknown')

                else:  # album
                    setattr(tag, attribute, 'Unknown')

        print('artist: ' + tag.artist + ', title: ' + tag.title + ', duration: ' + str(tag.duration) + ', album: '
              + tag.album + ', genre: ' + tag.genre)
        return MetaInfo(artist=tag.artist, title=tag.title, length=tag.duration, album=tag.album, genre=tag.genre)

    @staticmethod
    def convert_m4a(start, out, path):

        converted = []
        moved = []
        deleted = []
        out = '\\'.join([out,path])

        for dirname, dirnames, filenames in os.walk(start):
            # print path to all subdirectories first.
            #         for subdirname in dirnames:
            #             print(os.path.join(dirname, subdirname))

            # print path to all filenames.
            for filename in filenames:
                song = os.path.join(dirname, filename)
                p = Path(song)
                ext = p.suffix
                if ext == '.mp3':
                    moved.append(song)
                    shutil.copy(song, out)
                elif ext == '.wma':
                    ID3.convert_song(song, 'wma', out)
                    shutil.copy(song, out)
                    converted.append(song)
                    moved.append(song)
                elif ext == '.flac':
                    ID3.convert_song(song, 'flac', out)
                    shutil.copy(song, out)
                    converted.append(song)
                    moved.append(song)
                elif ext == '.mp4':
                    ID3.convert_song(song, 'mp4', out)
                    shutil.copy(song,out)
                    converted.append(song)
                    moved.append(song)
                elif ext == '.m4a':
                    ID3.convert_song(song, 'm4a', out)
                    converted.append(song)
                    shutil.copy(song, out)
                    moved.append(song)
                else:
                    deleted.append(filename)
                    os.remove(filename)
        return deleted, moved, converted


class MetaInfo:
    def __init__(self, artist='', title='', length=0, album='', genre=''):
        self.artist = artist
        self.title = title
        self.duration = length
        self.album = album
        self.genre = genre

    def dict(self):
        return {
            'artist': self.artist,
            'title': self.title,
            'duration': self.duration,
            'album': self.album,
            'genre': self.genre


            }