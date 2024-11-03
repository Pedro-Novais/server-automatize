from ._BaseRepository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, db):
        self.collection = db['users']