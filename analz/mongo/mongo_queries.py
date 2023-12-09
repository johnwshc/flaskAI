from app import mconn

class RadioQueries:
    def __init__(self):
        self.mc = mconn.mc
        self.db = self.mc.radio
        self.coll = self.db['tracks']

    def find_in_artist_title(self, qstring: str = 'Chuck Berry'):
        return self.coll.find({'artist_title': {'$regex': qstring}})

    def find_in_genres(self, qstring: str = 'blues'):
        cursor =  self.coll.find({"genres": [qstring]})


