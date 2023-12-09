
from tinydb import TinyDB, Query
from config import Config


class ERTinyDB:

    instance_count = 0

    @staticmethod
    def get_instance_count():
        return ERTinyDB.instance_count

    def __init__(self, db_base=Config.DB_DIR_LOCAL):
        self.db = TinyDB(db_base + '\\er_db.json')
        ERTinyDB.instance_count += 1
        self.tracks_table = self.db.table('tracks')
        self.pls_table = self.db.table('play_lists')
        self.promos_table = self.db.table('promos')

    def purge_all(self):
        self.db.purge()

    def find_track(self, title, doc_id=0):
        if doc_id > 0:
            return self.tracks_table.get(doc_id=doc_id)
        else:
            squery = Query()
            res = self.tracks_table.search(squery.title == title)
            return res

    def find_promo(self, title, doc_id=0):
        if doc_id > 0:
            return self.promos_table.get(doc_id=doc_id)
        else:
            squery = Query()
            res = self.promos_table.search(squery.title == title)
            return res[0]

    def get_promo(self, doc_id):
        doc = self.find_promo(None,doc_id=doc_id)
        return doc

    @staticmethod
    def get_tiny_db():
        print('ERTinyDB instance count: ',  ERTinyDB.instance_count + 1)
        return ERTinyDB()

    #  insert new promo -- doc_id returned
    def insert_promo(self, expr: dict):
        doc_id = self.promos_table.insert(expr)
        return doc_id

    #  Insert new track  -- doc_id returned
    def insert_track(self, expr: dict):
        doc_id = self.tracks_table.insert(expr)
        return doc_id

    #  returns a list, even if one
    # def search(self, expr: Query):
    #     res = self.db.search(expr)
    #     return res
    #
    # def remove(self, expr: list):
    #     res = self.db.remove(expr)
    #     return res

    def remove_track(self, doc_ids=[]):
        return self.tracks_table.remove(doc_ids=doc_ids)

    def remove_promo(self, doc_ids=[]):
        return self.promos_table.remove(doc_ids= doc_ids)

    def purge_tracks(self):
        return self.tracks_table.purge()

    def purge_promos(self):
        return self.promos_table.purge()

    def purge_all(self):
        l = self.purge_tracks()
        l.append(self.purge_promos())
        return l

    # def save_playlist(self, d_playlist):
    #     return self.db.insert(d_playlist)
    #
    # def find_all(self):
    #     return self.db.all()

    def close(self):
        return self.db.close()

    def get(self,d_id):
        doc = self.db.get(doc_id=d_id)
        return doc

    def get_all(self):
        return self.db.all()



    # def add_track(self, trk):
    #     return self.tracks_table.insert(trk.d_track)
    #
    # def add_playlist(self, pls):
    #     pass
    #
    # def add_promo(self, pro):
    #     pass





