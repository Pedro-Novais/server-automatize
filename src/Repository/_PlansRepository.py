from ._BaseRepository import BaseRepository

class PlansRepository(BaseRepository):
    def __init__(self, db):
        self.db = db
        self.collection = self.db['plans']